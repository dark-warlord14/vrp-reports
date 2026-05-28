# heap-use-after-free in content::RenderFrameHostImpl::ProcessBeforeUnloadCompleted in browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [391666328](https://issues.chromium.org/issues/391666328) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DefaultNavigationTransitions, UI>Browser>Navigation |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2025-01-23 |
| **Bounty** | $5,000.00 |

## Description

VULNERABILITY DETAILS
heap-use-after-free in content::RenderFrameHostImpl::ProcessBeforeUnloadCompleted in browser process

VERSION
Chromium	134.0.6972.0 (Developer Build) (64-bit) 
Operating System: linux-release-chromeos

REPRODUCTION CASE
1. get the lastest linux-release-chromeos asan build: gs://chromium-browser-asan/linux-release-chromeos/asan-linux-release-1409394.zip
2. runt the command:
./chrome --user-data-dir=/tmp/test --load-extension="extension_dir" 

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [browser]
=================================================================
==102046==ERROR: AddressSanitizer: heap-use-after-free on address 0x7d1f32eb5748 at pc 0x5626daaba42f bp 0x7fff89244250 sp 0x7fff89244248
READ of size 8 at 0x7d1f32eb5748 thread T0 (chrome)
==102046==WARNING: invalid path to external symbolizer!
==102046==WARNING: Failed to use and restart external symbolizer!
    #0 0x5626daaba42e in operator bool ./../../base/memory/scoped_refptr.h:319:43
    #1 0x5626daaba42e in is_null ./../../base/functional/callback_internal.h:140:34
    #2 0x5626daaba42e in operator bool ./../../base/functional/callback_internal.h:141:44
    #3 0x5626daaba42e in operator bool ./../../base/functional/callback.h:111:45
    #4 0x5626daaba42e in content::RenderFrameHostImpl::ProcessBeforeUnloadCompleted(bool, bool, base::TimeTicks const&, base::TimeTicks const&, bool) ./../../content/browser/renderer_host/render_frame_host_impl.cc:6217:7
    #5 0x5626dab3c434 in operator() ./../../content/browser/renderer_host/render_frame_host_impl.cc:15820:15
    #6 0x5626dab3c434 in Invoke<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:15815:7), base::WeakPtr<content::RenderFrameHostImpl>, bool, bool, base::TimeTicks, base::TimeTicks> ./../../base/functional/bind_internal.h:647:12
    #7 0x5626dab3c434 in MakeItSo<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:15815:7), std::__Cr::tuple<base::WeakPtr<content::RenderFrameHostImpl>, bool>, bool, base::TimeTicks, base::TimeTicks> ./../../base/functional/bind_internal.h:921:12
    #8 0x5626dab3c434 in RunImpl<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:15815:7), std::__Cr::tuple<base::WeakPtr<content::RenderFrameHostImpl>, bool>, 0UL, 1UL> ./../../base/functional/bind_internal.h:1058:14
    #9 0x5626dab3c434 in base::internal::Invoker<base::internal::FunctorTraits<content::RenderFrameHostImpl::SendBeforeUnload(bool, base::WeakPtr<content::RenderFrameHostImpl>, bool)::$_0&&, base::WeakPtr<content::RenderFrameHostImpl>&&, bool&&>, base::internal::BindState<false, false, false, content::RenderFrameHostImpl::SendBeforeUnload(bool, base::WeakPtr<content::RenderFrameHostImpl>, bool)::$_0, base::WeakPtr<content::RenderFrameHostImpl>, bool>, void (bool, base::TimeTicks, base::TimeTicks)>::RunOnce(base::internal::BindStateBase*, bool, base::TimeTicks&&, base::TimeTicks&&) ./../../base/functional/bind_internal.h:971:12
    #10 0x5626d3efe71b in base::OnceCallback<void (bool, base::TimeTicks, base::TimeTicks)>::Run(bool, base::TimeTicks, base::TimeTicks) && ./../../base/functional/callback.h:156:12
    #11 0x5626dab3c6da in operator() ./../../content/browser/renderer_host/render_frame_host_impl.cc:15836:39
    #12 0x5626dab3c6da in Invoke<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:15834:17), base::OnceCallback<void (bool, base::TimeTicks, base::TimeTicks)>, base::TimeTicks, base::TimeTicks> ./../../base/functional/bind_internal.h:647:12
    #13 0x5626dab3c6da in MakeItSo<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:15834:17), std::__Cr::tuple<base::OnceCallback<void (bool, base::TimeTicks, base::TimeTicks)>, base::TimeTicks, base::TimeTicks> > ./../../base/functional/bind_internal.h:921:12
    #14 0x5626dab3c6da in RunImpl<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:15834:17), std::__Cr::tuple<base::OnceCallback<void (bool, base::TimeTicks, base::TimeTicks)>, base::TimeTicks, base::TimeTicks>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1058:14
    #15 0x5626dab3c6da in base::internal::Invoker<base::internal::FunctorTraits<content::RenderFrameHostImpl::SendBeforeUnload(bool, base::WeakPtr<content::RenderFrameHostImpl>, bool)::$_1&&, base::OnceCallback<void (bool, base::TimeTicks, base::TimeTicks)>&&, base::TimeTicks&&, base::TimeTicks&&>, base::internal::BindState<false, false, false, content::RenderFrameHostImpl::SendBeforeUnload(bool, base::WeakPtr<content::RenderFrameHostImpl>, bool)::$_1, base::OnceCallback<void (bool, base::TimeTicks, base::TimeTicks)>, base::TimeTicks, base::TimeTicks>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:971:12
    #16 0x5626e195cebe in Run ./../../base/functional/callback.h:156:12
    #17 0x5626e195cebe in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:210:34
    #18 0x5626e19c028f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:472:11)> ./../../base/task/common/task_annotator.h:106:5
    #19 0x5626e19c028f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:470:23
    #20 0x5626e19bf17e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #21 0x5626e19c0f34 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #22 0x5626e1af8531 in base::MessagePumpEpoll::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_epoll.cc:222:55
    #23 0x5626e19c1a42 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:643:12
    #24 0x5626e18f7882 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #25 0x5626d9b82b49 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1089:18
    #26 0x5626d9b89ce0 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:156:15
    #27 0x5626d9b7a9a8 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:32:28
    #28 0x5626dfc3c805 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:710:10
    #29 0x5626dfc3f985 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1288:10
    #30 0x5626dfc3f2d9 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1140:12
    #31 0x5626dfc3a26c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:348:36
    #32 0x5626dfc3a73f in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:361:10
    #33 0x5626cf960446 in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #34 0x7eff33c67082 in __libc_start_main /build/glibc-LcI20x/glibc-2.31/csu/../csu/libc-start.c:308:16

0x7d1f32eb5748 is located 5704 bytes inside of 5744-byte region [0x7d1f32eb4100,0x7d1f32eb5770)
freed by thread T0 (chrome) here:
    #0 0x5626cf95f29d in operator delete(void*) _asan_rtl_:3
    #1 0x5626dab7b665 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5
    #2 0x5626dab7b665 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:300:7
    #3 0x5626dab7b665 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:269:71
    #4 0x5626dab7b665 in content::RenderFrameHostManager::UnloadOldFrame(std::__Cr::unique_ptr<content::RenderFrameHostImpl, std::__Cr::default_delete<content::RenderFrameHostImpl>>) ./../../content/browser/renderer_host/render_frame_host_manager.cc:1269:1
    #5 0x5626dab777ee in content::RenderFrameHostManager::CommitPending(std::__Cr::unique_ptr<content::RenderFrameHostImpl, std::__Cr::default_delete<content::RenderFrameHostImpl>>, std::__Cr::unique_ptr<content::StoredPage, std::__Cr::default_delete<content::StoredPage>>, bool, bool) ./../../content/browser/renderer_host/render_frame_host_manager.cc:5235:3
    #6 0x5626dab80ff4 in content::RenderFrameHostManager::PerformEarlyRenderFrameHostSwapIfNeeded(content::NavigationRequest*, bool) ./../../content/browser/renderer_host/render_frame_host_manager.cc:1592:3
    #7 0x5626dab7ed0a in content::RenderFrameHostManager::GetFrameHostForNavigation(content::NavigationRequest*, content::BrowsingContextGroupSwap*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>*) ./../../content/browser/renderer_host/render_frame_host_manager.cc:1932:5
    #8 0x5626da9cdd78 in content::NavigationRequest::SelectFrameHostForCrossDocumentNavigationWithNoUrlLoader() ./../../content/browser/renderer_host/navigation_request.cc:2839:47
    #9 0x5626da9c9313 in content::NavigationRequest::BeginNavigationImpl() ./../../content/browser/renderer_host/navigation_request.cc:2817:7
    #10 0x5626da9c6f31 in content::NavigationRequest::BeginNavigation() ./../../content/browser/renderer_host/navigation_request.cc:2406:3
    #11 0x5626dab28561 in operator() ./../../content/browser/renderer_host/render_frame_host_impl.cc:6329:30
    #12 0x5626dab28561 in Invoke<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:6318:7), base::WeakPtr<content::RenderFrameHostImpl>, base::TimeTicks, bool, bool, bool, bool> ./../../base/functional/bind_internal.h:647:12
    #13 0x5626dab28561 in MakeItSo<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:6318:7), std::__Cr::tuple<base::WeakPtr<content::RenderFrameHostImpl>, base::TimeTicks, bool, bool, bool, bool> > ./../../base/functional/bind_internal.h:921:12
    #14 0x5626dab28561 in RunImpl<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:6318:7), std::__Cr::tuple<base::WeakPtr<content::RenderFrameHostImpl>, base::TimeTicks, bool, bool, bool, bool>, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL> ./../../base/functional/bind_internal.h:1058:14
    #15 0x5626dab28561 in base::internal::Invoker<base::internal::FunctorTraits<content::RenderFrameHostImpl::ProcessBeforeUnloadCompletedFromFrame(bool, bool, content::RenderFrameHostImpl*, bool, base::TimeTicks const&, base::TimeTicks const&, bool)::$_0&&, base::WeakPtr<content::RenderFrameHostImpl>&&, base::TimeTicks&&, bool&&, bool&&, bool&&, bool&&>, base::internal::BindState<false, false, false, content::RenderFrameHostImpl::ProcessBeforeUnloadCompletedFromFrame(bool, bool, content::RenderFrameHostImpl*, bool, base::TimeTicks const&, base::TimeTicks const&, bool)::$_0, base::WeakPtr<content::RenderFrameHostImpl>, base::TimeTicks, bool, bool, bool, bool>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:971:12
    #16 0x5626d0b0ea0c in base::OnceCallback<void ()>::Run() && ./../../base/functional/callback.h:156:12
    #17 0x5626daa8fceb in content::RenderFrameHostImpl::ProcessBeforeUnloadCompletedFromFrame(bool, bool, content::RenderFrameHostImpl*, bool, base::TimeTicks const&, base::TimeTicks const&, bool) ./../../content/browser/renderer_host/render_frame_host_impl.cc:6349:21
    #18 0x5626daaba244 in content::RenderFrameHostImpl::ProcessBeforeUnloadCompleted(bool, bool, base::TimeTicks const&, base::TimeTicks const&, bool) ./../../content/browser/renderer_host/render_frame_host_impl.cc:6212:14
    #19 0x5626dab3c434 in operator() ./../../content/browser/renderer_host/render_frame_host_impl.cc:15820:15
    #20 0x5626dab3c434 in Invoke<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:15815:7), base::WeakPtr<content::RenderFrameHostImpl>, bool, bool, base::TimeTicks, base::TimeTicks> ./../../base/functional/bind_internal.h:647:12
    #21 0x5626dab3c434 in MakeItSo<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:15815:7), std::__Cr::tuple<base::WeakPtr<content::RenderFrameHostImpl>, bool>, bool, base::TimeTicks, base::TimeTicks> ./../../base/functional/bind_internal.h:921:12
    #22 0x5626dab3c434 in RunImpl<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:15815:7), std::__Cr::tuple<base::WeakPtr<content::RenderFrameHostImpl>, bool>, 0UL, 1UL> ./../../base/functional/bind_internal.h:1058:14
    #23 0x5626dab3c434 in base::internal::Invoker<base::internal::FunctorTraits<content::RenderFrameHostImpl::SendBeforeUnload(bool, base::WeakPtr<content::RenderFrameHostImpl>, bool)::$_0&&, base::WeakPtr<content::RenderFrameHostImpl>&&, bool&&>, base::internal::BindState<false, false, false, content::RenderFrameHostImpl::SendBeforeUnload(bool, base::WeakPtr<content::RenderFrameHostImpl>, bool)::$_0, base::WeakPtr<content::RenderFrameHostImpl>, bool>, void (bool, base::TimeTicks, base::TimeTicks)>::RunOnce(base::internal::BindStateBase*, bool, base::TimeTicks&&, base::TimeTicks&&) ./../../base/functional/bind_internal.h:971:12
    #24 0x5626d3efe71b in base::OnceCallback<void (bool, base::TimeTicks, base::TimeTicks)>::Run(bool, base::TimeTicks, base::TimeTicks) && ./../../base/functional/callback.h:156:12
    #25 0x5626dab3c6da in operator() ./../../content/browser/renderer_host/render_frame_host_impl.cc:15836:39
    #26 0x5626dab3c6da in Invoke<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:15834:17), base::OnceCallback<void (bool, base::TimeTicks, base::TimeTicks)>, base::TimeTicks, base::TimeTicks> ./../../base/functional/bind_internal.h:647:12
    #27 0x5626dab3c6da in MakeItSo<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:15834:17), std::__Cr::tuple<base::OnceCallback<void (bool, base::TimeTicks, base::TimeTicks)>, base::TimeTicks, base::TimeTicks> > ./../../base/functional/bind_internal.h:921:12
    #28 0x5626dab3c6da in RunImpl<(lambda at ../../content/browser/renderer_host/render_frame_host_impl.cc:15834:17), std::__Cr::tuple<base::OnceCallback<void (bool, base::TimeTicks, base::TimeTicks)>, base::TimeTicks, base::TimeTicks>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1058:14
    #29 0x5626dab3c6da in base::internal::Invoker<base::internal::FunctorTraits<content::RenderFrameHostImpl::SendBeforeUnload(bool, base::WeakPtr<content::RenderFrameHostImpl>, bool)::$_1&&, base::OnceCallback<void (bool, base::TimeTicks, base::TimeTicks)>&&, base::TimeTicks&&, base::TimeTicks&&>, base::internal::BindState<false, false, false, content::RenderFrameHostImpl::SendBeforeUnload(bool, base::WeakPtr<content::RenderFrameHostImpl>, bool)::$_1, base::OnceCallback<void (bool, base::TimeTicks, base::TimeTicks)>, base::TimeTicks, base::TimeTicks>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:971:12
    #30 0x5626e195cebe in Run ./../../base/functional/callback.h:156:12
    #31 0x5626e195cebe in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:210:34
    #32 0x5626e19c028f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:472:11)> ./../../base/task/common/task_annotator.h:106:5
    #33 0x5626e19c028f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:470:23
    #34 0x5626e19bf17e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #35 0x5626e19c0f34 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #36 0x5626e1af8531 in base::MessagePumpEpoll::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_epoll.cc:222:55
    #37 0x5626e19c1a42 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:643:12
    #38 0x5626e18f7882 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #39 0x5626d9b82b49 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1089:18
    #40 0x5626d9b89ce0 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:156:15
    #41 0x5626d9b7a9a8 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:32:28
    #42 0x5626dfc3c805 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:710:10
    #43 0x5626dfc3f985 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1288:10
    #44 0x5626dfc3f2d9 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1140:12
    #45 0x5626dfc3a26c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:348:36
    #46 0x5626dfc3a73f in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:361:10

previously allocated by thread T0 (chrome) here:
    #0 0x5626cf95ea3d in operator new(unsigned long) _asan_rtl_:3
    #1 0x5626daa81c5f in operator new ./../../content/public/browser/render_frame_host.h:147:3
    #2 0x5626daa81c5f in content::RenderFrameHostFactory::Create(content::SiteInstance*, scoped_refptr<content::RenderViewHostImpl>, content::RenderFrameHostDelegate*, content::FrameTree*, content::FrameTreeNode*, int, mojo::PendingAssociatedRemote<content::mojom::Frame>, base::TokenType<blink::LocalFrameTokenTypeMarker> const&, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken, bool, content::RenderFrameHostImpl::LifecycleStateImpl, scoped_refptr<content::BrowsingContextState>) ./../../content/browser/renderer_host/render_frame_host_factory.cc:39:27
    #3 0x5626dab727b3 in content::RenderFrameHostManager::CreateRenderFrameHost(content::RenderFrameHostManager::CreateFrameCase, content::SiteInstanceImpl*, int, mojo::PendingAssociatedRemote<content::mojom::Frame>, base::TokenType<blink::LocalFrameTokenTypeMarker> const&, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken, bool, scoped_refptr<content::BrowsingContextState>) ./../../content/browser/renderer_host/render_frame_host_manager.cc:4107:10
    #4 0x5626dab716cf in content::RenderFrameHostManager::InitRoot(content::SiteInstanceImpl*, bool, blink::FramePolicy, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::UnguessableToken const&) ./../../content/browser/renderer_host/render_frame_host_manager.cc:655:22
    #5 0x5626da80491c in content::FrameTree::Init(content::SiteInstanceImpl*, bool, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::RenderFrameHostImpl*, blink::FramePolicy const&, base::UnguessableToken const&) ./../../content/browser/renderer_host/frame_tree.cc:948:27
    #6 0x5626db0e0459 in content::WebContentsImpl::Init(content::WebContents::CreateParams const&, blink::FramePolicy) ./../../content/browser/web_contents/web_contents_impl.cc:3833:23
    #7 0x5626db0c201f in content::WebContentsImpl::CreateWithOpener(content::WebContents::CreateParams const&, content::RenderFrameHostImpl*) ./../../content/browser/web_contents/web_contents_impl.cc:1556:17
    #8 0x5626dcede0c2 in extensions::WebViewGuest::CreateInnerPageWithSiteInstance(std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, scoped_refptr<content::SiteInstance>, base::Value::Dict const&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>) ./../../extensions/browser/guest_view/web_view/web_view_guest.cc:531:49
    #9 0x5626dcede7bf in extensions::WebViewGuest::CreateInnerPageWithStoragePartition(std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, base::Value::Dict const&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>, std::__Cr::optional<content::StoragePartitionConfig>) ./../../extensions/browser/guest_view/web_view/web_view_guest.cc:479:3
    #10 0x5626dcef044f in void base::internal::DecayedFunctorTraits<void (extensions::WebViewGuest::*)(std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, base::Value::Dict const&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>, std::__Cr::optional<content::StoragePartitionConfig>), base::WeakPtr<extensions::WebViewGuest>&&, std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>&&, base::Value::Dict&&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>&&>::Invoke<void (extensions::WebViewGuest::*)(std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, base::Value::Dict const&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>, std::__Cr::optional<content::StoragePartitionConfig>), base::WeakPtr<extensions::WebViewGuest> const&, std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, base::Value::Dict, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>, std::__Cr::optional<content::StoragePartitionConfig>>(void (extensions::WebViewGuest::*)(std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, base::Value::Dict const&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>, std::__Cr::optional<content::StoragePartitionConfig>), base::WeakPtr<extensions::WebViewGuest> const&, std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>&&, base::Value::Dict&&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>&&, std::__Cr::optional<content::StoragePartitionConfig>&&) ./../../base/functional/bind_internal.h:729:12
    #11 0x5626dcef0200 in MakeItSo<void (extensions::WebViewGuest::*)(std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase> >, const base::Value::Dict &, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase> >, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents> >, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder> > >)>, std::__Cr::optional<content::StoragePartitionConfig>), std::__Cr::tuple<base::WeakPtr<extensions::WebViewGuest>, std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase> >, base::Value::Dict, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase> >, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents> >, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder> > >)> >, std::__Cr::optional<content::StoragePartitionConfig> > ./../../base/functional/bind_internal.h:945:5
    #12 0x5626dcef0200 in RunImpl<void (extensions::WebViewGuest::*)(std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase> >, const base::Value::Dict &, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase> >, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents> >, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder> > >)>, std::__Cr::optional<content::StoragePartitionConfig>), std::__Cr::tuple<base::WeakPtr<extensions::WebViewGuest>, std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase> >, base::Value::Dict, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase> >, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents> >, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder> > >)> >, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind_internal.h:1058:14
    #13 0x5626dcef0200 in base::internal::Invoker<base::internal::FunctorTraits<void (extensions::WebViewGuest::*&&)(std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, base::Value::Dict const&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>, std::__Cr::optional<content::StoragePartitionConfig>), base::WeakPtr<extensions::WebViewGuest>&&, std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>&&, base::Value::Dict&&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>&&>, base::internal::BindState<true, true, false, void (extensions::WebViewGuest::*)(std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, base::Value::Dict const&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>, std::__Cr::optional<content::StoragePartitionConfig>), base::WeakPtr<extensions::WebViewGuest>, std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, base::Value::Dict, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>>, void (std::__Cr::optional<content::StoragePartitionConfig>)>::RunOnce(base::internal::BindStateBase*, std::__Cr::optional<content::StoragePartitionConfig>&&) ./../../base/functional/bind_internal.h:971:12
    #14 0x5626dcdea982 in base::OnceCallback<void (std::__Cr::optional<content::StoragePartitionConfig>)>::Run(std::__Cr::optional<content::StoragePartitionConfig>) && ./../../base/functional/callback.h:156:12
    #15 0x5626dcdea715 in extensions::ExtensionsBrowserClient::GetWebViewStoragePartitionConfig(content::BrowserContext*, content::SiteInstance*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, bool, base::OnceCallback<void (std::__Cr::optional<content::StoragePartitionConfig>)>) ./../../extensions/browser/extensions_browser_client.cc:254:23
    #16 0x5626df4af849 in extensions::ChromeExtensionsBrowserClient::GetWebViewStoragePartitionConfig(content::BrowserContext*, content::SiteInstance*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, bool, base::OnceCallback<void (std::__Cr::optional<content::StoragePartitionConfig>)>) ./../../chrome/browser/extensions/chrome_extensions_browser_client.cc:1016:28
    #17 0x5626dcedd6e8 in extensions::WebViewGuest::CreateInnerPage(std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, scoped_refptr<content::SiteInstance>, base::Value::Dict const&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, absl::variant<std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, std::__Cr::unique_ptr<content::GuestPageHolder, std::__Cr::default_delete<content::GuestPageHolder>>>)>) ./../../extensions/browser/guest_view/web_view/web_view_guest.cc:446:37
    #18 0x5626ed6288e3 in guest_view::GuestViewBase::Init(std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>, scoped_refptr<content::SiteInstance>, base::Value::Dict const&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>)>) ./../../components/guest_view/browser/guest_view_base.cc:197:3
    #19 0x5626ed639d1a in guest_view::GuestViewManager::CreateGuestAndTransferOwnership(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::RenderFrameHost*, scoped_refptr<content::SiteInstance>, base::Value::Dict const&, base::OnceCallback<void (std::__Cr::unique_ptr<guest_view::GuestViewBase, std::__Cr::default_delete<guest_view::GuestViewBase>>)>) ./../../components/guest_view/browser/guest_view_manager.cc:213:14
    #20 0x5626ed639a32 in guest_view::GuestViewManager::CreateGuest(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::RenderFrameHost*, base::Value::Dict const&, base::OnceCallback<void (guest_view::GuestViewBase*)>) ./../../components/guest_view/browser/guest_view_manager.cc:195:3
    #21 0x5626dcea43d3 in extensions::GuestViewInternalCreateGuestFunction::Run() ./../../extensions/browser/api/guest_view/guest_view_internal_api.cc:89:23
    #22 0x5626dcd789ec in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension_function.cc:493:10
    #23 0x5626dcd85f3c in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost*, content::RenderProcessHost&, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value::List, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>) ./../../extensions/browser/extension_function_dispatcher.cc:442:15
    #24 0x5626dcd849bb in extensions::ExtensionFunctionDispatcher::Dispatch(mojo::StructPtr<extensions::mojom::RequestParams>, content::RenderFrameHost&, base::OnceCallback<void (bool, base::Value::List, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>) ./../../extensions/browser/extension_function_dispatcher.cc:200:3
    #25 0x5626dcd7394f in extensions::ExtensionFrameHost::Request(mojo::StructPtr<extensions::mojom::RequestParams>, base::OnceCallback<void (bool, base::Value::List, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>) ./../../extensions/browser/extension_frame_host.cc:64:9
    #26 0x5626dc0e30a8 in extensions::mojom::LocalFrameHostStubDispatch::AcceptWithResponder(extensions::mojom::LocalFrameHost*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) ./gen/extensions/common/mojom/frame.mojom.cc:3957:13
    #27 0x5626e2e6cdf6 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1005:56
    #28 0x5626e2e8467e in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #29 0x5626e2e7134a in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:724:20
    #30 0x5626e5554e26 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1202:24
    #31 0x5626e55566fa in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind_internal.h:729:12
    #32 0x5626e55566fa in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind_internal.h:921:12
    #33 0x5626e55566fa in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1058:14
    #34 0x5626e55566fa in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:971:12
    #35 0x5626e195cebe in Run ./../../base/functional/callback.h:156:12
    #36 0x5626e195cebe in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:210:34

SUMMARY: AddressSanitizer: heap-use-after-free (/chromium/chrome+0x1f0fc42e) (BuildId: 5ddf622ef71320fb)
Shadow bytes around the buggy address:
  0x7d1f32eb5480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d1f32eb5500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d1f32eb5580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d1f32eb5600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d1f32eb5680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x7d1f32eb5700: fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fa fa
  0x7d1f32eb5780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d1f32eb5800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d1f32eb5880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x7d1f32eb5900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d1f32eb5980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==102046==ADDITIONAL INFO

==102046==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5626dab12c6f in content::RenderFrameHostImpl::SendBeforeUnload(bool, base::WeakPtr<content::RenderFrameHostImpl>, bool) ./../../content/browser/renderer_host/render_frame_host_impl.cc:15832:13
    #1 0x5626e5548570 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1141:13
    #2 0x5626e2ee4e74 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:102:13


Command line: `/Chromium/chrome --user-data-dir=/tmp/qrgczsibjsmh --extensions-on-chrome-urls --load-extension=extension_dir --flag-switches-begin --flag-switches-end --login-user=stub-user@example.com --login-profile=test-user --file-url-path-alias=/gen=/Chromium/gen`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==102046==END OF ADDITIONAL INFO
==102046==ABORTING


## Attachments

- [extension.zip](attachments/extension.zip) (application/zip, 1.2 KB)
- [popup.js](attachments/popup.js) (text/javascript, 859 B)
- [background.js](attachments/background.js) (text/javascript, 38 B)
- [manifest.json](attachments/manifest.json) (application/json, 281 B)
- [popup.html](attachments/popup.html) (text/html, 188 B)

## Timeline

### ct...@chromium.org (2025-01-23)

Could you please attach the contents of the zip file directly to this bug? Thanks!

### 0x...@gmail.com (2025-01-23)

The attachements

### pe...@google.com (2025-01-23)

Thank you for providing more feedback. Adding the requester to the CC list.

### ct...@chromium.org (2025-01-24)

Thank you for uploading. I am able to reproduce this on asan-linux-release-1409394 (134.0.6972.0 from Jan 21) using the instructions you have provided. I am also able to reproduce this on r1381561 (132.0.6834.0).

- Sev-High: memory corruption in browser process and not MiraclePtr protected, but downgraded as this requires a malicious extension
- FoundIn-132

Assigning to alexmos@ because the extension is largely using webview -- could you take a look or help suggest who might be a better owner? Thanks!

### ct...@chromium.org (2025-01-24)

Also noting that the repro steps are to use the CrOS-on-Linux ASAN build so that is what I have tested so far, but it may also be triggerable on regular Linux builds. For now I'm including Linux in the affected OS list out of an abundance of caution.

### pe...@google.com (2025-01-24)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2025-01-24)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ct...@chromium.org (2025-01-24)

On Linux ASAN r1409394 this hits a CHECK:

[3819968:3819968:0124/105448.547508:FATAL:cloud\_policy\_invalidator.cc(369)] Check failed: state\_ == State::STARTED.

but that happens regardless of whether the extension is loaded so that build seems to just be bad on Linux.

Retrying with a newer Linux ASAN r1410671 this does not repro and the extension popup just loads as expected, so there is a possibility this is really CrOS specific (or CrOS-on-Linux specific?)

@reporter: Have you had any success reproducing this on other platforms?

### al...@chromium.org (2025-01-28)

Apologies that I haven't had a chance to dig into this yet. On first glance, it's a UAF due to calling ProcessBeforeUnloadCompleted() on a RFH that's already been deleted by a prior ProcessBeforeUnloadCompleted(), due to an early RFH swap that was done as part of navigating a newly created webview guest. There are no actual beforeunload handlers in the repro, so this should just be a PostTask from RFHI::SendBeforeUnload(). I'll set up a local Linux ChromeOS asan build to investigate further, and in the meantime adding +mcnee@ as a guestview expert who might be able to help here, and also to double-check that the recent MPArch guest changes aren't involved here.

### al...@chromium.org (2025-01-28)

I got a local repro using a ChromeOS build on Linux. Looks like the UAF is on [this line](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=6190;drc=27d34700b83f381c62e3a348de2e6dfdc08364b8) in ProcessBeforeUnloadCompleted():

```
  if (on_process_before_unload_completed_for_testing_) [[unlikely]] {
    std::move(on_process_before_unload_completed_for_testing_).Run();
  }

```

This code doesn't account for the fact that the beforeunload initiator RFH may be the same as `this`, and that `ProcessBeforeUnloadCompletedFromFrame()` may end up synchronously proceeding with a navigation which may then synchronously destroy the current RFH through the [early RFH swap](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.h;l=706;drc=c0883e36f0f65273f002c2ca8b7e9474256e00e4) code, after picking a different target RFH. The asan stack traces seem to confirm this is what's happening: the current RFH is freed as part of `PerformEarlyRenderFrameHostSwap()` deep in `ProcessBeforeUnloadCompletedFromFrame()`, then we unwind the stack back to `ProcessBeforeUnloadCompleted()` and try to dereference `on_process_before_unload_completed_for_testing_` on a freed RFH. Using webview might just be a way to force the early RFH swap to happen.

liuwilliam@, can you take a look, since this code was added a couple of months ago in your <https://chromium-review.googlesource.com/c/chromium/src/+/5919513>? Maybe this test callback can run before `ProcessBeforeUnloadCompletedFromFrame()` is called, or if it needs to run after, it should check whether RFH had been destroyed.

### mc...@chromium.org (2025-01-28)

> Using webview might just be a way to force the early RFH swap to happen.

The provided app is [killing](https://developer.chrome.com/docs/apps/reference/webviewTag#method-terminate) the guest's renderer process. That's presumably taking us into the early swap path.

If ordering of the test callback is important, another option could be to move the callback into a local variable before the call that could destroy `this`.

### al...@chromium.org (2025-01-28)

> The provided app is killing the guest's renderer process. That's presumably taking us into the early swap path.

Indeed, great observation and explains why the <webview> tag is used - it makes it very easy to use the early swap path since the embedding app has the APIs to crash and reload the webview.

Technically, the same bug could be possible outside of <webview> on other platforms, if an attacker can find a way to crash a renderer process and then reload the corresponding frame. It wouldn't be possible to do this in an OOPIF (e.g., by forcing it to OOM and then reloading it through the window reference), since we don't use the legacy beforeunload path for subframes and also [clear](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=3829;drc=27d34700b83f381c62e3a348de2e6dfdc08364b8) beforeunload handlers when a renderer process dies, so we would skip the beforeunload path altogether. But maybe it's possible with window.open() and then crashing and reloading window.opener.

### ap...@google.com (2025-02-04)

Project: chromium/src  

Branch: main  

Author: William Liu <[liuwilliam@chromium.org](mailto:liuwilliam@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6228049>

[DNT][content] Reorder the test callback

---


Expand for full commit details
```
[DNT][content] Reorder the test callback 
 
The UAF happens when `initiator` == `this`, and `this` is deleted after 
`ProcessBeforeUnloadCompletedFromFrame()` returns. The tests don't need 
to wait for `ProcessBeforeUnloadCompletedFromFrame()` to return so we 
can run the test callback earlier to avoid the UAF. 
 
Cq-Include-Trybots: luci.chromium.try:android-12-x64-rel,android-12l-x64-dbg,android-13-x64-rel,android-14-x64-rel,android-15-x64-rel,android-pie-x86-rel,android-oreo-x86-rel 
 
Bug: 391666328 
Change-Id: I1c105e94ecc82538e13f0ece764860f18022429b 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6228049 
Commit-Queue: William Liu <liuwilliam@chromium.org> 
Reviewed-by: Kevin McNee <mcnee@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1415693}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`

---

Hash: 1d548c569d85412691197c126bd6f7da1c11b811  

Date:  Tue Feb 04 11:04:03 2025


---

### cr...@chromium.org (2025-02-05)

[Navigation Triage]

Thanks for landing r1415693! I'll mark this as fixed to get the automated steps in progress for merges, etc.

### pe...@google.com (2025-02-05)

Security Merge Request Consideration: Requesting merge to extended stable (M132) because latest trunk commit (1415693) appears to be after extended stable branch point (1381561).
Security Merge Request Consideration: Requesting merge to stable (M133) because latest trunk commit (1415693) appears to be after stable branch point (1402768).
Security Merge Request Consideration: Requesting merge to dev (M134) because latest trunk commit (1415693) appears to be after dev branch point (1415337).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pe...@google.com (2025-02-05)

**Merge approved:** your change passed merge requirements and is auto-approved for M134. Please go ahead and merge the CL to branch 6998 (refs/branch-heads/6998) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### pe...@google.com (2025-02-05)

Merge review required: M133 is already shipping to stable.

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
Owners: andywu (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### pe...@google.com (2025-02-05)

Merge review required: M132 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), alonbajayo (ChromeOS), srinivassista (Desktop)

### am...@chromium.org (2025-02-07)

merges approved for <https://crrev.com/c/6228049>, please merge this fix to:

- M134 Beta / branch 6998
- M133 Stable / branch 6943
- M132 Extended Stable / branch 6834

at your earliest convenience, before 10am Monday PT so this fix can be included in next week's updates

### li...@chromium.org (2025-02-07)

6998 : https://chromium-review.googlesource.com/c/chromium/src/+/6244238

6943: https://chromium-review.googlesource.com/c/chromium/src/+/6244403

6834: https://chromium-review.googlesource.com/c/chromium/src/+/6244239

### ap...@google.com (2025-02-07)

Project: chromium/src  

Branch: refs/branch-heads/6998  

Author: William Liu <[liuwilliam@chromium.org](mailto:liuwilliam@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6244238>

[6998][DNT][content] Reorder the test callback

---


Expand for full commit details
```
[6998][DNT][content] Reorder the test callback 
 
The UAF happens when `initiator` == `this`, and `this` is deleted after 
`ProcessBeforeUnloadCompletedFromFrame()` returns. The tests don't need 
to wait for `ProcessBeforeUnloadCompletedFromFrame()` to return so we 
can run the test callback earlier to avoid the UAF. 
 
Cq-Include-Trybots: luci.chromium.try:android-12-x64-rel,android-12l-x64-dbg,android-13-x64-rel,android-14-x64-rel,android-15-x64-rel,android-pie-x86-rel,android-oreo-x86-rel 
 
(cherry picked from commit 1d548c569d85412691197c126bd6f7da1c11b811) 
 
Bug: 391666328 
Change-Id: I1c105e94ecc82538e13f0ece764860f18022429b 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6228049 
Commit-Queue: William Liu <liuwilliam@chromium.org> 
Reviewed-by: Kevin McNee <mcnee@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1415693} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6244238 
Cr-Commit-Position: refs/branch-heads/6998@{#225} 
Cr-Branched-From: de9c6fafd8ae5c6ea0438764076ca7d04a0b165d-refs/heads/main@{#1415337}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`

---

Hash: 48958aee818b8923c0ddfbfa335b8fa967266bc5  

Date:  Fri Feb 07 14:55:25 2025


---

### pe...@google.com (2025-02-07)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ap...@google.com (2025-02-07)

Project: chromium/src  

Branch: refs/branch-heads/6943  

Author: William Liu <[liuwilliam@chromium.org](mailto:liuwilliam@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6244403>

[6943][DNT][content] Reorder the test callback

---


Expand for full commit details
```
[6943][DNT][content] Reorder the test callback 
 
The UAF happens when `initiator` == `this`, and `this` is deleted after 
`ProcessBeforeUnloadCompletedFromFrame()` returns. The tests don't need 
to wait for `ProcessBeforeUnloadCompletedFromFrame()` to return so we 
can run the test callback earlier to avoid the UAF. 
 
Cq-Include-Trybots: luci.chromium.try:android-12-x64-rel,android-12l-x64-dbg,android-13-x64-rel,android-14-x64-rel,android-15-x64-rel,android-pie-x86-rel,android-oreo-x86-rel 
 
(cherry picked from commit 1d548c569d85412691197c126bd6f7da1c11b811) 
 
Bug: 391666328 
Change-Id: I1c105e94ecc82538e13f0ece764860f18022429b 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6228049 
Commit-Queue: William Liu <liuwilliam@chromium.org> 
Reviewed-by: Kevin McNee <mcnee@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1415693} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6244403 
Cr-Commit-Position: refs/branch-heads/6943@{#1485} 
Cr-Branched-From: 72dd0b377c099e1e0230cc7345d5a5125b46ae7d-refs/heads/main@{#1402768}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`

---

Hash: 36b498591423ce5a22e15803d77efc1ba41e79e8  

Date:  Fri Feb 07 15:14:19 2025


---

### ap...@google.com (2025-02-07)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: William Liu <[liuwilliam@chromium.org](mailto:liuwilliam@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6244239>

[6834][DNT][content] Reorder the test callback

---


Expand for full commit details
```
[6834][DNT][content] Reorder the test callback 
 
The UAF happens when `initiator` == `this`, and `this` is deleted after 
`ProcessBeforeUnloadCompletedFromFrame()` returns. The tests don't need 
to wait for `ProcessBeforeUnloadCompletedFromFrame()` to return so we 
can run the test callback earlier to avoid the UAF. 
 
Cq-Include-Trybots: luci.chromium.try:android-12-x64-rel,android-12l-x64-dbg,android-13-x64-rel,android-14-x64-rel,android-15-x64-rel,android-pie-x86-rel,android-oreo-x86-rel 
 
(cherry picked from commit 1d548c569d85412691197c126bd6f7da1c11b811) 
 
Bug: 391666328 
Change-Id: I1c105e94ecc82538e13f0ece764860f18022429b 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6228049 
Commit-Queue: William Liu <liuwilliam@chromium.org> 
Reviewed-by: Kevin McNee <mcnee@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1415693} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6244239 
Cr-Commit-Position: refs/branch-heads/6834@{#4993} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`

---

Hash: 705662be9f5ec4992b2bef053932bfaeebd804be  

Date:  Fri Feb 07 15:42:09 2025


---

### qk...@google.com (2025-02-10)

Labeling as LTS-NotApplicable-126 because M126 doesn't have the suspected CL[1] 
[1] https://chromium-review.googlesource.com/c/chromium/src/+/5919513

### sp...@google.com (2025-02-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
report of mildly mitigated memory corruption bug in a non-sandboxed process, mitigated by precondition to download app (since <webview> tag is specific to apps) + install malicious extension 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-14)

Congratulations! Thank you for your efforts and reporting this issue to us!

### 0x...@gmail.com (2025-02-17)

Hi, 
According to comment  #11 and #13, this issue can be triggered in a compromised renderer process in Chromium. Webview and extension are not needed. Can it treat as a browser process UAF in the  compromised renderer and review the bounty payment?
Thanks.

### am...@chromium.org (2025-02-18)

Hello, this was assessed as a browser process UAF "mildly mitigated bug in a non-sandboxed process", as per conveyed in c#27.

While an the app download may not be needed to convey the webview tag,
an attacker would still need to find a mechanism to crash a renderer process and then reload the corresponding frame.

Therefore, there is a precondition required to make this possible and your demonstration of making this situation possible involves downloading an app download and installing a malicious extension.
We can only reward for what is reported and demonstrated by you. In this case, it was a mildly mitigated browser UAF.

### ap...@google.com (2025-02-21)

Project: chromium/src  

Branch: refs/branch-heads/6834\_160  

Author: William Liu <[liuwilliam@chromium.org](mailto:liuwilliam@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6287669>

[CfM-R132][DNT][content] Reorder the test callback

---


Expand for full commit details
```
[CfM-R132][DNT][content] Reorder the test callback 
 
The UAF happens when `initiator` == `this`, and `this` is deleted after 
`ProcessBeforeUnloadCompletedFromFrame()` returns. The tests don't need 
to wait for `ProcessBeforeUnloadCompletedFromFrame()` to return so we 
can run the test callback earlier to avoid the UAF. 
 
Cq-Include-Trybots: luci.chromium.try:android-12-x64-rel,android-12l-x64-dbg,android-13-x64-rel,android-14-x64-rel,android-15-x64-rel,android-pie-x86-rel,android-oreo-x86-rel 
 
Bug: 391666328 
Change-Id: I1c105e94ecc82538e13f0ece764860f18022429b 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6228049 
Commit-Queue: William Liu <liuwilliam@chromium.org> 
Reviewed-by: Kevin McNee <mcnee@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1415693} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6287669 
Auto-Submit: Kyle Williams <kdgwill@chromium.org> 
Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
Owners-Override: Kyle Williams <kdgwill@chromium.org> 
Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
Cr-Commit-Position: refs/branch-heads/6834_160@{#22} 
Cr-Branched-From: cdae089eab830291f81deb011febbbdc520a019e-refs/branch-heads/6834@{#4409} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`

---

Hash: 0770f34e2d6c7b3aa53118bd63cd057858e605f1  

Date:  Fri Feb 21 10:32:51 2025


---

### ch...@google.com (2025-05-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/391666328)*
