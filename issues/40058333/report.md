# Security: AddressSanitizer: heap-use-after-free on drag_drop_controller.cc (chromeOS and Lacros)

| Field | Value |
|-------|-------|
| **Issue ID** | [40058333](https://issues.chromium.org/issues/40058333) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DataTransfer |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | os...@chromium.org |
| **Created** | 2021-12-23 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36

Steps to reproduce the problem:
I will provide the video and PoC on next comment

What is the expected behavior?
Not Crash!

What went wrong?
==11430==ERROR: AddressSanitizer: heap-use-after-free on address 0x615000449290 at pc 0x556cc8e326e9 bp 0x7ffc81e752a0 sp 0x7ffc81e75298
READ of size 8 at 0x615000449290 thread T0 (chrome)
==11430==WARNING: invalid path to external symbolizer!
==11430==WARNING: Failed to use and restart external symbolizer!
    #0 0x556cc8e326e8 in begin ./../../buildtools/third_party/libc++/trunk/include/vector:1518:30
    #1 0x556cc8e326e8 in begin<std::__1::vector<base::internal::CheckedObserverAdapter, std::__1::allocator<base::internal::CheckedObserverAdapter> > &> ./../../base/ranges/ranges.h:44:37
    #2 0x556cc8e326e8 in begin<std::__1::vector<base::internal::CheckedObserverAdapter, std::__1::allocator<base::internal::CheckedObserverAdapter> > &> ./../../base/ranges/ranges.h:105:10
    #3 0x556cc8e326e8 in find_if<std::__1::vector<base::internal::CheckedObserverAdapter, std::__1::allocator<base::internal::CheckedObserverAdapter> > &, (lambda at ../../base/observer_list.h:284:21), base::identity, std::__1::random_access_iterator_tag> ./../../base/ranges/algorithm.h:483:26
    #4 0x556cc8e326e8 in base::ObserverList<aura::WindowObserver, true, true, base::internal::CheckedObserverAdapter>::RemoveObserver(aura::WindowObserver const*) ./../../base/observer_list.h:283:21
    #5 0x556cc94da16e in ash::DragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ./../../ash/drag_drop/drag_drop_controller.cc:245:28
    #6 0x556cbb0e5430 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*) ./../../content/browser/web_contents/web_contents_view_aura.cc:1159:15
    #7 0x556cbad7be4a in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>) ./../../content/browser/renderer_host/render_widget_host_impl.cc:2833:9
    #8 0x556cb891a2db in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/page/widget.mojom.cc:3052:13
    #9 0x556cc4a43a9a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:900:54
    #10 0x556cc4a565a7 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #11 0x556cc4a4695a in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:657:20
    #12 0x556cc4a08d45 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:1008:24
    #13 0x556cc4a029b7 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:535:12
    #14 0x556cc4a029b7 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:699:12
    #15 0x556cc4a029b7 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__1::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind_internal.h:772:12
    #16 0x556cc4a029b7 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:741:12
    #17 0x556cc32ae426 in Run ./../../base/callback.h:142:12
    #18 0x556cc32ae426 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:135:32
    #19 0x556cc32ec953 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> ./../../base/task/common/task_annotator.h:74:5
    #20 0x556cc32ec953 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #21 0x556cc32ec1a2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #22 0x556cc32ed511 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #23 0x556cc342b78d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:195:55
    #24 0x556cc32edbca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #25 0x556cc3227b7c in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:140:14
    #26 0x556cba1b3a74 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1048:18
    #27 0x556cba1b7fbf in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:153:15
    #28 0x556cba1addda in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:30:28
    #29 0x556cc300714f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:646:10
    #30 0x556cc3009c51 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1160:10
    #31 0x556cc3009028 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1026:12
    #32 0x556cc30038db in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:398:36
    #33 0x556cc3003f41 in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:426:10
    #34 0x556cb58f0f3a in ChromeMain ./../../chrome/app/chrome_main.cc:177:12
    #35 0x7fe74dd4b0b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x615000449290 is located 400 bytes inside of 504-byte region [0x615000449100,0x6150004492f8)
freed by thread T0 (chrome) here:
    #0 0x556cb58eef7d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x556cbad61bf7 in content::RenderWidgetHostImpl::Destroy(bool) ./../../content/browser/renderer_host/render_widget_host_impl.cc:2418:12
    #2 0x556cbad5259e in content::RenderViewHostImpl::~RenderViewHostImpl() ./../../content/browser/renderer_host/render_view_host_impl.cc:351:16
    #3 0x556cbad52ce3 in content::RenderViewHostImpl::~RenderViewHostImpl() ./../../content/browser/renderer_host/render_view_host_impl.cc:345:43
    #4 0x556cbac2a0a1 in content::RenderFrameHostImpl::~RenderFrameHostImpl() ./../../content/browser/renderer_host/render_frame_host_impl.cc:1660:21
    #5 0x556cbac2d1c9 in content::RenderFrameHostImpl::~RenderFrameHostImpl() ./../../content/browser/renderer_host/render_frame_host_impl.cc:1514:45
    #6 0x556cbacc9a66 in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #7 0x556cbacc9a66 in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #8 0x556cbacc9a66 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #9 0x556cbacc9a66 in content::RenderFrameHostManager::~RenderFrameHostManager() ./../../content/browser/renderer_host/render_frame_host_manager.cc:311:3
    #10 0x556cbaa4fabe in content::FrameTreeNode::~FrameTreeNode() ./../../content/browser/renderer_host/frame_tree_node.cc:234:1
    #11 0x556cbaa41267 in content::FrameTree::~FrameTree() ./../../content/browser/renderer_host/frame_tree.cc:295:3
    #12 0x556cbb06f25c in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web_contents/web_contents_impl.cc:1087:1
    #13 0x556cbb07081f in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web_contents/web_contents_impl.cc:989:37
    #14 0x556ccf40efed in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #15 0x556ccf40efed in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #16 0x556ccf40efed in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:541:27
    #17 0x556ccf40d55f in TabStripModel::DetachWebContentsWithReasonAt(int, TabStripModelChange::RemoveReason) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:434:3
    #18 0x556ccf40d7e6 in TabStripModel::DetachAndDeleteWebContentsAt(int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:413:3
    #19 0x556ccb23408b in BrowserCloseManager::CloseBrowsers() ./../../chrome/browser/lifetime/browser_close_manager.cc:181:37
    #20 0x556ccaac5e19 in chrome::CloseAllBrowsers() ./../../chrome/browser/lifetime/application_lifetime.cc:273:26
    #21 0x556ccaac5c25 in chrome::AttemptExitInternal(bool) ./../../chrome/browser/lifetime/application_lifetime.cc:229:39
    #22 0x556ccaac7794 in chrome::ExitIgnoreUnloadHandlers() ./../../chrome/browser/lifetime/application_lifetime.cc:379:3
    #23 0x556cc32ae426 in Run ./../../base/callback.h:142:12
    #24 0x556cc32ae426 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:135:32
    #25 0x556cc32ec953 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> ./../../base/task/common/task_annotator.h:74:5
    #26 0x556cc32ec953 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #27 0x556cc32ec1a2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #28 0x556cc32ed511 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #29 0x556cc342b78d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:195:55
    #30 0x556cc32edbca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #31 0x556cc3227b7c in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:140:14
    #32 0x556cc94da0c5 in ash::DragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ./../../ash/drag_drop/drag_drop_controller.cc:237:14
    #33 0x556cbb0e5430 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*) ./../../content/browser/web_contents/web_contents_view_aura.cc:1159:15
    #34 0x556cbad7be4a in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>) ./../../content/browser/renderer_host/render_widget_host_impl.cc:2833:9
    #35 0x556cb891a2db in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/page/widget.mojom.cc:3052:13
    #36 0x556cc4a43a9a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:900:54

previously allocated by thread T0 (chrome) here:
    #0 0x556cb58ee71d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x556cbada3f7a in content::RenderWidgetHostViewAura::CreateAuraWindow(aura::client::WindowType) ./../../content/browser/renderer_host/render_widget_host_view_aura.cc:2185:13
    #2 0x556cbada3e48 in content::RenderWidgetHostViewAura::InitAsChild(aura::Window*) ./../../content/browser/renderer_host/render_widget_host_view_aura.cc:359:3
    #3 0x556cbb0e3fbd in content::WebContentsViewAura::CreateViewForWidget(content::RenderWidgetHost*) ./../../content/browser/web_contents/web_contents_view_aura.cc:1030:9
    #4 0x556cbb0c5fda in content::WebContentsImpl::CreateRenderWidgetHostViewForRenderManager(content::RenderViewHost*) ./../../content/browser/web_contents/web_contents_impl.cc:7962:16
    #5 0x556cbacdc4d8 in content::RenderFrameHostManager::CreateSpeculativeRenderFrame(content::SiteInstance*, bool) ./../../content/browser/renderer_host/render_frame_host_manager.cc:2766:18
    #6 0x556cbacd4706 in content::RenderFrameHostManager::CreateSpeculativeRenderFrameHost(content::SiteInstance*, content::SiteInstance*, bool) ./../../content/browser/renderer_host/render_frame_host_manager.cc:2677:36
    #7 0x556cbacd28bc in content::RenderFrameHostManager::GetFrameHostForNavigation(content::NavigationRequest*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >*) ./../../content/browser/renderer_host/render_frame_host_manager.cc:1085:22
    #8 0x556cbacd1c24 in content::RenderFrameHostManager::DidCreateNavigationRequest(content::NavigationRequest*) ./../../content/browser/renderer_host/render_frame_host_manager.cc:915:37
    #9 0x556cbaa52396 in content::FrameTreeNode::CreatedNavigationRequest(std::__1::unique_ptr<content::NavigationRequest, std::__1::default_delete<content::NavigationRequest> >) ./../../content/browser/renderer_host/frame_tree_node.cc:527:21
    #10 0x556cbac0b74a in content::Navigator::OnBeginNavigation(content::FrameTreeNode*, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::BeginNavigationParams>, scoped_refptr<network::SharedURLLoaderFactory>, mojo::PendingAssociatedRemote<content::mojom::NavigationClient>, scoped_refptr<content::PrefetchedSignedExchangeCache>, std::__1::unique_ptr<content::WebBundleHandleTracker, std::__1::default_delete<content::WebBundleHandleTracker> >) ./../../content/browser/renderer_host/navigator.cc:949:20
    #11 0x556cbac65c79 in content::RenderFrameHostImpl::BeginNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::BeginNavigationParams>, mojo::PendingRemote<blink::mojom::BlobURLToken>, mojo::PendingAssociatedRemote<content::mojom::NavigationClient>, mojo::PendingRemote<blink::mojom::PolicyContainerHostKeepAliveHandle>) ./../../content/browser/renderer_host/render_frame_host_impl.cc:7152:34
    #12 0x556cb9823c77 in content::mojom::FrameHostStubDispatch::Accept(content::mojom::FrameHost*, mojo::Message*) ./gen/content/common/frame.mojom.cc:5568:13
    #13 0x556cc4a43a9a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:900:54
    #14 0x556cc4a564c2 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #15 0x556cc4a4695a in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:657:20
    #16 0x556cc4a08d45 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:1008:24
    #17 0x556cc4a029b7 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:535:12
    #18 0x556cc4a029b7 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind_internal.h:699:12
    #19 0x556cc4a029b7 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__1::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/bind_internal.h:772:12
    #20 0x556cc4a029b7 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:741:12
    #21 0x556cc32ae426 in Run ./../../base/callback.h:142:12
    #22 0x556cc32ae426 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:135:32
    #23 0x556cc32ec953 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> ./../../base/task/common/task_annotator.h:74:5
    #24 0x556cc32ec953 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #25 0x556cc32ec1a2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #26 0x556cc32ed511 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #27 0x556cc342b78d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_libevent.cc:195:55
    #28 0x556cc32edbca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #29 0x556cc3227b7c in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:140:14
    #30 0x556cba1b3a74 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1048:18
    #31 0x556cba1b7fbf in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:153:15
    #32 0x556cba1addda in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:30:28
    #33 0x556cc300714f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:646:10
    #34 0x556cc3009c51 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1160:10

SUMMARY: AddressSanitizer: heap-use-after-free (/home/dadang/asan/chromeOS/asan-linux-release-953812/chrome+0x210366e8) (BuildId: eb56536d56c7b753)
Shadow bytes around the buggy address:
  0x0c2a80081200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80081210: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80081220: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80081230: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80081240: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2a80081250: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c2a80081260: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80081270: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80081280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80081290: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800812a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
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
==11430==ABORTING

Did this work before? N/A 

Chrome version: 99.0.4784.0  Channel: dev
OS Version: 99.0.4784.0

## Attachments

- [poc_1282480.webm](attachments/poc_1282480.webm) (video/webm, 5.4 MB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [open.html](attachments/open.html) (text/plain, 116 B)
- [1.html](attachments/1.html) (text/plain, 1.6 KB)
- deleted (application/octet-stream, 0 B)
- [poc_1282480_e.webm](attachments/poc_1282480_e.webm) (video/webm, 5.3 MB)
- [poc_1282480_f.webm](attachments/poc_1282480_f.webm) (video/webm, 7.8 MB)
- [poc_1282480_g.webm](attachments/poc_1282480_g.webm) (video/webm, 1.2 MB)
- [Screen recording 2022-01-18 9.53.03 AM.webm](attachments/Screen recording 2022-01-18 9.53.03 AM.webm) (video/webm, 2.5 MB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2021-12-23)

[Empty comment from Monorail migration]

### rh...@gmail.com (2021-12-23)

steps  PoC:
(1) Block any text and hold left click -> open screen capture -> take video capture
(2) Close browser

symbolized trace:

==20936==ERROR: AddressSanitizer: heap-use-after-free on address 0x615000353b10 at pc 0x558ff11916e9 bp 0x7ffdc434bd60 sp 0x7ffdc434bd58
READ of size 8 at 0x615000353b10 thread T0 (chrome)
    #0 0x558ff11916e8 in begin buildtools/third_party/libc++/trunk/include/vector:1518:30
    #1 0x558ff11916e8 in begin<std::__1::vector<base::internal::CheckedObserverAdapter, std::__1::allocator<base::internal::CheckedObserverAdapter> > &> base/ranges/ranges.h:44:37
    #2 0x558ff11916e8 in begin<std::__1::vector<base::internal::CheckedObserverAdapter, std::__1::allocator<base::internal::CheckedObserverAdapter> > &> base/ranges/ranges.h:105:10
    #3 0x558ff11916e8 in find_if<std::__1::vector<base::internal::CheckedObserverAdapter, std::__1::allocator<base::internal::CheckedObserverAdapter> > &, (lambda at ../../base/observer_list.h:284:21), base::identity, std::__1::random_access_iterator_tag> base/ranges/algorithm.h:483:26
    #4 0x558ff11916e8 in base::ObserverList<aura::WindowObserver, true, true, base::internal::CheckedObserverAdapter>::RemoveObserver(aura::WindowObserver const*) base/observer_list.h:283:21
    #5 0x558ff183916e in ash::DragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller.cc:245:28
    #6 0x558fe3444430 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*) content/browser/web_contents/web_contents_view_aura.cc:1159:15
    #7 0x558fe30dae4a in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>) content/browser/renderer_host/render_widget_host_impl.cc:2833:9
    #8 0x558fe0c792db in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*) gen/third_party/blink/public/mojom/page/widget.mojom.cc:3052:13
    #9 0x558fecda2a9a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:900:54
    #10 0x558fecdb55a7 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #11 0x558fecda595a in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:657:20
    #12 0x558fecd67d45 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:1008:24
    #13 0x558fecd619b7 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:535:12
    #14 0x558fecd619b7 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:699:12
    #15 0x558fecd619b7 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__1::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind_internal.h:772:12
    #16 0x558fecd619b7 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:741:12
    #17 0x558feb60d426 in Run base/callback.h:142:12
    #18 0x558feb60d426 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #19 0x558feb64b953 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #20 0x558feb64b953 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #21 0x558feb64b1a2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #22 0x558feb64c511 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #23 0x558feb78a78d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #24 0x558feb64cbca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #25 0x558feb586b7c in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #26 0x558fe2512a74 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1048:18
    #27 0x558fe2516fbf in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:153:15
    #28 0x558fe250cdda in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #29 0x558feb36614f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:646:10
    #30 0x558feb368c51 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1160:10
    #31 0x558feb368028 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1026:12
    #32 0x558feb3628db in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:398:36
    #33 0x558feb362f41 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:426:10
    #34 0x558fddc4ff3a in ChromeMain chrome/app/chrome_main.cc:177:12
    #35 0x7f8cb4e990b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x615000353b10 is located 400 bytes inside of 504-byte region [0x615000353980,0x615000353b78)
freed by thread T0 (chrome) here:
    #0 0x558fddc4df7d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x558fe30c0bf7 in content::RenderWidgetHostImpl::Destroy(bool) content/browser/renderer_host/render_widget_host_impl.cc:2418:12
    #2 0x558fe30b159e in content::RenderViewHostImpl::~RenderViewHostImpl() content/browser/renderer_host/render_view_host_impl.cc:351:16
    #3 0x558fe30b1ce3 in content::RenderViewHostImpl::~RenderViewHostImpl() content/browser/renderer_host/render_view_host_impl.cc:345:43
    #4 0x558fe2f890a1 in content::RenderFrameHostImpl::~RenderFrameHostImpl() content/browser/renderer_host/render_frame_host_impl.cc:1660:21
    #5 0x558fe2f8c1c9 in content::RenderFrameHostImpl::~RenderFrameHostImpl() content/browser/renderer_host/render_frame_host_impl.cc:1514:45
    #6 0x558fe3028a66 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #7 0x558fe3028a66 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #8 0x558fe3028a66 in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #9 0x558fe3028a66 in content::RenderFrameHostManager::~RenderFrameHostManager() content/browser/renderer_host/render_frame_host_manager.cc:311:3
    #10 0x558fe2daeabe in content::FrameTreeNode::~FrameTreeNode() content/browser/renderer_host/frame_tree_node.cc:234:1
    #11 0x558fe2da0267 in content::FrameTree::~FrameTree() content/browser/renderer_host/frame_tree.cc:295:3
    #12 0x558fe33ce25c in content::WebContentsImpl::~WebContentsImpl() content/browser/web_contents/web_contents_impl.cc:1087:1
    #13 0x558fe33cf81f in content::WebContentsImpl::~WebContentsImpl() content/browser/web_contents/web_contents_impl.cc:989:37
    #14 0x558ff776dfed in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #15 0x558ff776dfed in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #16 0x558ff776dfed in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) chrome/browser/ui/tabs/tab_strip_model.cc:541:27
    #17 0x558ff776c55f in TabStripModel::DetachWebContentsWithReasonAt(int, TabStripModelChange::RemoveReason) chrome/browser/ui/tabs/tab_strip_model.cc:434:3
    #18 0x558ff776c7e6 in TabStripModel::DetachAndDeleteWebContentsAt(int) chrome/browser/ui/tabs/tab_strip_model.cc:413:3
    #19 0x558ff359308b in BrowserCloseManager::CloseBrowsers() chrome/browser/lifetime/browser_close_manager.cc:181:37
    #20 0x558ff2e24e19 in chrome::CloseAllBrowsers() chrome/browser/lifetime/application_lifetime.cc:273:26
    #21 0x558ff2e24c25 in chrome::AttemptExitInternal(bool) chrome/browser/lifetime/application_lifetime.cc:229:39
    #22 0x558ff2e26794 in chrome::ExitIgnoreUnloadHandlers() chrome/browser/lifetime/application_lifetime.cc:379:3
    #23 0x558feb60d426 in Run base/callback.h:142:12
    #24 0x558feb60d426 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #25 0x558feb64b953 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #26 0x558feb64b953 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #27 0x558feb64b1a2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #28 0x558feb64c511 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #29 0x558feb78a78d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #30 0x558feb64cbca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #31 0x558feb586b7c in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #32 0x558ff18390c5 in ash::DragDropController::StartDragAndDrop(std::__1::unique_ptr<ui::OSExchangeData, std::__1::default_delete<ui::OSExchangeData> >, aura::Window*, aura::Window*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag_drop/drag_drop_controller.cc:237:14
    #33 0x558fe3444430 in content::WebContentsViewAura::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl*) content/browser/web_contents/web_contents_view_aura.cc:1159:15
    #34 0x558fe30dae4a in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr<blink::mojom::DragData>, blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr<blink::mojom::DragEventSourceInfo>) content/browser/renderer_host/render_widget_host_impl.cc:2833:9
    #35 0x558fe0c792db in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost*, mojo::Message*) gen/third_party/blink/public/mojom/page/widget.mojom.cc:3052:13
    #36 0x558fecda2a9a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:900:54

previously allocated by thread T0 (chrome) here:
    #0 0x558fddc4d71d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x558fe3102f7a in content::RenderWidgetHostViewAura::CreateAuraWindow(aura::client::WindowType) content/browser/renderer_host/render_widget_host_view_aura.cc:2185:13
    #2 0x558fe3102e48 in content::RenderWidgetHostViewAura::InitAsChild(aura::Window*) content/browser/renderer_host/render_widget_host_view_aura.cc:359:3
    #3 0x558fe3442fbd in content::WebContentsViewAura::CreateViewForWidget(content::RenderWidgetHost*) content/browser/web_contents/web_contents_view_aura.cc:1030:9
    #4 0x558fe3424fda in content::WebContentsImpl::CreateRenderWidgetHostViewForRenderManager(content::RenderViewHost*) content/browser/web_contents/web_contents_impl.cc:7962:16
    #5 0x558fe303b4d8 in content::RenderFrameHostManager::CreateSpeculativeRenderFrame(content::SiteInstance*, bool) content/browser/renderer_host/render_frame_host_manager.cc:2766:18
    #6 0x558fe3033706 in content::RenderFrameHostManager::CreateSpeculativeRenderFrameHost(content::SiteInstance*, content::SiteInstance*, bool) content/browser/renderer_host/render_frame_host_manager.cc:2677:36
    #7 0x558fe30318bc in content::RenderFrameHostManager::GetFrameHostForNavigation(content::NavigationRequest*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >*) content/browser/renderer_host/render_frame_host_manager.cc:1085:22
    #8 0x558fe3030c24 in content::RenderFrameHostManager::DidCreateNavigationRequest(content::NavigationRequest*) content/browser/renderer_host/render_frame_host_manager.cc:915:37
    #9 0x558fe2db1396 in content::FrameTreeNode::CreatedNavigationRequest(std::__1::unique_ptr<content::NavigationRequest, std::__1::default_delete<content::NavigationRequest> >) content/browser/renderer_host/frame_tree_node.cc:527:21
    #10 0x558fe2f6a74a in content::Navigator::OnBeginNavigation(content::FrameTreeNode*, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::BeginNavigationParams>, scoped_refptr<network::SharedURLLoaderFactory>, mojo::PendingAssociatedRemote<content::mojom::NavigationClient>, scoped_refptr<content::PrefetchedSignedExchangeCache>, std::__1::unique_ptr<content::WebBundleHandleTracker, std::__1::default_delete<content::WebBundleHandleTracker> >) content/browser/renderer_host/navigator.cc:949:20
    #11 0x558fe2fc4c79 in content::RenderFrameHostImpl::BeginNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::BeginNavigationParams>, mojo::PendingRemote<blink::mojom::BlobURLToken>, mojo::PendingAssociatedRemote<content::mojom::NavigationClient>, mojo::PendingRemote<blink::mojom::PolicyContainerHostKeepAliveHandle>) content/browser/renderer_host/render_frame_host_impl.cc:7152:34
    #12 0x558fe1b82c77 in content::mojom::FrameHostStubDispatch::Accept(content::mojom::FrameHost*, mojo::Message*) gen/content/common/frame.mojom.cc:5568:13
    #13 0x558fecda2a9a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:900:54
    #14 0x558fecdb54c2 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #15 0x558fecda595a in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:657:20
    #16 0x558fecd67d45 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:1008:24
    #17 0x558fecd619b7 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:535:12
    #18 0x558fecd619b7 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:699:12
    #19 0x558fecd619b7 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__1::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind_internal.h:772:12
    #20 0x558fecd619b7 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:741:12
    #21 0x558feb60d426 in Run base/callback.h:142:12
    #22 0x558feb60d426 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #23 0x558feb64b953 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #24 0x558feb64b953 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #25 0x558feb64b1a2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #26 0x558feb64c511 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #27 0x558feb78a78d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #28 0x558feb64cbca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #29 0x558feb586b7c in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #30 0x558fe2512a74 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1048:18
    #31 0x558fe2516fbf in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:153:15
    #32 0x558fe250cdda in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #33 0x558feb36614f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:646:10
    #34 0x558feb368c51 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1160:10

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/vector:1518:30 in begin
Shadow bytes around the buggy address:
  0x0c2a80062710: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80062720: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80062730: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80062740: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80062750: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2a80062760: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c2a80062770: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a80062780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a80062790: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800627a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a800627b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
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
==20936==ABORTING


### rh...@gmail.com (2021-12-23)

Additional info:

Screenshot or video recorder function is no needed. If the user lock on text selection and close the browser, the UaF triggered as well.

### rh...@gmail.com (2021-12-25)

VULNERABILITY DETAILS

Here's a object-lifetime issue in the browser process, it's possible to trigger this by closing the browser while dragging an object in the browser. It's a browser process bug which can be triggered without a compromised render.

The DragDropController[1] object contains:
```
DragOperation DragDropController::StartDragAndDrop(
    std::unique_ptr<ui::OSExchangeData> data,
    aura::Window* root_window,
    aura::Window* source_window,
    const gfx::Point& screen_location,
    int allowed_operations,
    ui::mojom::DragEventSource source) {
    ...
 ```
the process allocated a block of size 8 for "ui::mojom::DragEventSource source". After the object being freed and then tried to access it at drag_source_window_[2] caused UaF. 
```
if (drag_source_window_)
      drag_source_window_->RemoveObserver(this); // => here.
    drag_source_window_ = nullptr;
```    

From my prespective the best approach to fix this issue, that we shall to add GetWeakPtr() on DragDropController and add DCHECK(drag_source_window_).

I've uploaded the simplest way to reproduce.


[1] https://source.chromium.org/chromium/chromium/src/+/main:ash/drag_drop/drag_drop_controller.cc;drc=2c63db7ef6a10e2958e4847908ec9b2fd03e8ab2;l=145
[2] https://source.chromium.org/chromium/chromium/src/+/main:ash/drag_drop/drag_drop_controller.cc;drc=2c63db7ef6a10e2958e4847908ec9b2fd03e8ab2;l=245

### en...@google.com (2021-12-28)

[Empty comment from Monorail migration]

[Monorail components: Blink>DataTransfer]

### en...@google.com (2021-12-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-28)

[Empty comment from Monorail migration]

### en...@google.com (2021-12-28)

oshima@ please let me know if you are the correct owner.

### rh...@gmail.com (2021-12-29)

Hi enlightened@,

Good day!

I have questions regarding the security severity, based on security severity guidelines[1], this issue might be marked as High. For example we take another issue like #1233975 as reference. 

I have another step maybe this useful to set the severity:

(1) download the attachments and save on same folder.
(2) run ~/asan/chromeOS/asan-linux-release-954391/chrome --disable-popup-blocking --user-data-dir=/tmp/chromeos ( the argument --disable-popup-blocking is used, but in the real device (chromebook user) can go to directly attacker website from Chrome address bar).
(3) start python3 http.server && open http://localhost:8000/open.html.
(4) hold left click on new tab opened after the javascript loads text selection and wait for crash.


[1] https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#TOC-High-severity

### [Deleted User] (2021-12-29)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@google.com (2021-12-29)

[Empty comment from Monorail migration]

### os...@chromium.org (2022-01-05)

There are a few memory related fix went in for d&d code. Is this still happening? (I couldn't repro using "close window while dragging selected text on ToT)

### rh...@gmail.com (2022-01-05)

Hi,

Yes I was able to reproduce the issue on r955685. I've tested the steps with https://crbug.com/chromium/1282480#c4 and I'm sure it will repros with the steps https://crbug.com/chromium/1282480#c9 too.
 
Do you want me to test with latest asan build r955857(current latest asan)?

### rh...@gmail.com (2022-01-05)

Hi,

Following in the video is simulated steps from https://crbug.com/chromium/1282480#c4 and https://crbug.com/chromium/1282480#c9 on r955857.

Hope this helps.

### rh...@gmail.com (2022-01-05)

I'm used (CTRL + w)[1] to close current tab in browser on steps https://crbug.com/chromium/1282480#c4 if you missed there. 


[1] https://support.google.com/chrome/answer/157179?hl=en&co=GENIE.Platform%3DDesktop#zippy=%2Ctab-and-window-shortcuts

### os...@chromium.org (2022-01-06)

Thanks, I could reppro it. looking.

### os...@chromium.org (2022-01-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1f5969495575d819dcf44a7d94d2e0f1bb4b1d71

commit 1f5969495575d819dcf44a7d94d2e0f1bb4b1d71
Author: Mitsuru Oshima <oshima@chromium.org>
Date: Fri Jan 07 21:47:25 2022

Remove obsever only if drag_window!=drag_source_window in Cleanup

This will cause DragDropContorller::OnWindowDestroyed() not being
called which is supposed to reset the drag_source_window.

Writing a test for this scenario require some rafactoring to test
code, so let me do that in a separate CL.

Bug: 1282480
Change-Id: Id8a7efcdd4d1564f0a934a79f1a4706e4a767861
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3370727
Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Cr-Commit-Position: refs/heads/main@{#956674}

[modify] https://crrev.com/1f5969495575d819dcf44a7d94d2e0f1bb4b1d71/ash/drag_drop/drag_drop_controller.cc


### en...@chromium.org (2022-01-07)

[Empty comment from Monorail migration]

### os...@chromium.org (2022-01-08)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-01-08)

oshima@,

Thank you for fixing this issue, I've test on r956827 just now and it couldn't repro anymore.



### [Deleted User] (2022-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-08)

Requesting merge to stable M97 because latest trunk commit (956674) appears to be after stable branch point (938553).

Requesting merge to dev M98 because latest trunk commit (956674) appears to be after dev branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-08)

Merge review required: M98 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-08)

Merge review required: M97 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ce...@google.com (2022-01-10)

Please complete the merge questionnaire in https://crbug.com/chromium/1282480#c26. If the answer to 3) is 'yes' this is approved to merge for M97.

### ce...@google.com (2022-01-10)

[Empty comment from Monorail migration]

### ma...@google.com (2022-01-11)

Echoing what Cole said, this is approved for M98 if survey question 3) is true.

### os...@chromium.org (2022-01-11)

The change hasn't been pushed to canary yet (canary is 99.0.4811.0 while the fix is 99.0.4814.0 or newer). I'll update the bug once uprev happens.

### gi...@appspot.gserviceaccount.com (2022-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0a71010677563e51b14acba2c2c11fa2319b27b1

commit 0a71010677563e51b14acba2c2c11fa2319b27b1
Author: Mitsuru Oshima <oshima@chromium.org>
Date: Tue Jan 11 21:15:56 2022

Unit test for UAF scenario in DragDroController

* This CL introduce a mechanism to inject a closure to be used
 as inner loop.
* Add new test that uses this inner loop to generate events.
* This CL also fixed a bug in the test. (the drag must have been
 canceled when a source window is destroyed)

Bug: 1282480
Test: DragDropControllerTest.DragCanceledThenWindowDestroyedDuringDragDrop
Change-Id: I35ba9496d2d134672c06f1957a7829264a29854c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3378442
Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Cr-Commit-Position: refs/heads/main@{#957711}

[modify] https://crrev.com/0a71010677563e51b14acba2c2c11fa2319b27b1/ash/drag_drop/drag_drop_controller.cc
[modify] https://crrev.com/0a71010677563e51b14acba2c2c11fa2319b27b1/ash/drag_drop/drag_drop_controller_unittest.cc
[modify] https://crrev.com/0a71010677563e51b14acba2c2c11fa2319b27b1/components/exo/wayland/zwp_pointer_constraints.cc
[modify] https://crrev.com/0a71010677563e51b14acba2c2c11fa2319b27b1/ash/drag_drop/drag_drop_controller.h


### am...@chromium.org (2022-01-12)

based on the user interaction required as well as the small, if at all, potential exploitability of this issue (requires browser shutdown and would have a very narrow window to leverage exploit code to exploit), adjusting severity accordingly 

### rh...@gmail.com (2022-01-12)

amy@,

yes it's true if your statement for step https://crbug.com/chromium/1282480#c4 does require a shortcut (close browser ctrl+w) to make reproduction easier.

But if your statement for step https://crbug.com/chromium/1282480#c9 (without shortcut ctrl+w) from my perspective it may not be appropriate, because compared to issue #1233975, they also drag files into the browser and the browser automatically closes itself with javascript. Maybe in the video I uploaded in https://crbug.com/chromium/1282480#c9 it doesn't clearly show the closed browser itself, but I really didn't use the shortcut (ctrl+w).

### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### os...@chromium.org (2022-01-13)

1. Why does your merge fit within the merge criteria for these milestones?
UAF that has security risk

2. What changes specifically would you like to merge? Please link to Gerrit.
crrev.com/c/3378442

3. Have the changes been released and tested on canary?
yes (99.0.4828.0 on nocturne)

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
Yes

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No

### am...@chromium.org (2022-01-13)

Congratulation, Rheza. The VRP Panel has decided to award you $2000 for this report. Thank you for your efforts and reporting this issue to us. 

### os...@chromium.org (2022-01-13)

one correction:
> 2. What changes specifically would you like to merge? Please link to Gerrit.
crrev.com/c/3370727

### [Deleted User] (2022-01-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c62bf887c748a759415574a947245bc05d83a51d

commit c62bf887c748a759415574a947245bc05d83a51d
Author: Mitsuru Oshima <oshima@chromium.org>
Date: Fri Jan 14 17:44:02 2022

Remove obsever only if drag_window!=drag_source_window in Cleanup

This will cause DragDropContorller::OnWindowDestroyed() not being
called which is supposed to reset the drag_source_window.

Writing a test for this scenario require some rafactoring to test
code, so let me do that in a separate CL.

(cherry picked from commit 1f5969495575d819dcf44a7d94d2e0f1bb4b1d71)

Bug: 1282480
Change-Id: Id8a7efcdd4d1564f0a934a79f1a4706e4a767861
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3370727
Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#956674}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3388342
Auto-Submit: Mitsuru Oshima <oshima@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#1438}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/c62bf887c748a759415574a947245bc05d83a51d/ash/drag_drop/drag_drop_controller.cc


### gi...@appspot.gserviceaccount.com (2022-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3bff590804859f2c65a2ef0ff4d84f46ee4bce01

commit 3bff590804859f2c65a2ef0ff4d84f46ee4bce01
Author: Mitsuru Oshima <oshima@chromium.org>
Date: Fri Jan 14 17:58:51 2022

Remove obsever only if drag_window!=drag_source_window in Cleanup

This will cause DragDropContorller::OnWindowDestroyed() not being
called which is supposed to reset the drag_source_window.

Writing a test for this scenario require some rafactoring to test
code, so let me do that in a separate CL.

(cherry picked from commit 1f5969495575d819dcf44a7d94d2e0f1bb4b1d71)

Bug: 1282480
Change-Id: Id8a7efcdd4d1564f0a934a79f1a4706e4a767861
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3370727
Reviewed-by: Xiaoqian Dai <xdai@chromium.org>
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#956674}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3388340
Auto-Submit: Mitsuru Oshima <oshima@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#622}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/3bff590804859f2c65a2ef0ff4d84f46ee4bce01/ash/drag_drop/drag_drop_controller.cc


### os...@chromium.org (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-01-18)

Hello Oshima and Security Team,

Please forgive me if I'm bringing up this report again. Your help means a lot to me, so the severity of this bug and its impact can be appropriated.

1. `Ctrl+w`[1] isn't browser shutdown, and it is a current close tab. Unless the last tab is only one tab, the browser will be closed.
2. The PoC in https://crbug.com/chromium/1282480#c4 was the easiest repro because we can drag any items from the chrome startup page (last history or chrome webstore link as example in the video), which sure could not impact the attacker to exploit. 
3. I uploaded another PoC in https://crbug.com/chromium/1282480#c9 to demonstrate the impact of this bug, so I was hoping the severity could be higher than medium. (was set enlightened@google.com on https://crbug.com/chromium/1282480#c5).
4. in https://crbug.com/chromium/1282480#c12 "There are a few memory related fix went in for d&d code. Is this still happening? (I couldn't repro using "close window while dragging selected text on ToT)", I exactly don't know which PoC the developer did a test. I added new comment in https://crbug.com/chromium/1282480#c13,#c14.
5. In https://crbug.com/chromium/1282480#c15 "I'm used (CTRL + w)[1] to close current tab in browser on steps https://crbug.com/chromium/1282480#c4 if you missed there."  It's clear for steps https://crbug.com/chromium/1282480#c4 not https://crbug.com/chromium/1282480#c9.

My assumption if the researcher gives a new POC with a broader impact, then more severity is taken. 
In https://crbug.com/chromium/1282480#c9 --disable-popup-blocking was used because I currently don't know how to pass chrome from the command line to open http://localhost directly. The --disable-popup-blocking will not change the stack trace of the bug itself and is not a feature to be enabled like --enable-features=xxx.

I've recorded a two videos based on https://crbug.com/chromium/1282480#c9 but hosted it on github.io[2] and without shortcuts[3] (ctrl+w) to minimize user interaction for reference.


Ref:
[1] https://support.google.com/chrome/answer/157179?hl=en&co=GENIE.Platform%3DDesktop#zippy=%2Ctab-and-window-shortcuts
[2] poc_1282480_g.webm
[3] https://drive.google.com/file/d/1MkbE-wyAXB0NK_GtM3DGcKCl3rW-AHJX/view?usp=sharing

### os...@chromium.org (2022-01-18)

#44, is this still happening to you?
I also tested the open/close using javascript myself. (see attached video)




### rh...@gmail.com (2022-01-18)

>is this still happening to you?
I couldn't get crash after your CL https://crbug.com/chromium/1282480#c18 or after version 956674. That means you have already fixed the UAF crash.

However, I'd like to say on https://crbug.com/chromium/1282480#c44, the version before 956674 or before the fix begins.
How did you try to repro based on https://crbug.com/chromium/1282480#c16 "Thanks, I could reppro it. looking."? 
a. With shortcuts (ctrl+w).
b. Without shortcuts.

If you have not tried point b, can you please try point b or the same technique like screen recording https://crbug.com/chromium/1282480#c45 on the version before/lower 956674 or the version in your comment https://crbug.com/chromium/1282480#c16? The success of point b could be affected by security severity.

I've tested and recorded the same technique like https://crbug.com/chromium/1282480#c45 on the version when it crashes (lower than 956674).

Once again, I'm so sorry for bothering/being noise, and this is not about the version after the fix landed. 
The fixes you've done it's working well, and no crashes anymore. 


### am...@chromium.org (2022-01-18)

Hello Rheza, I spoke to the developer (oshima@) off bug earlier today, they confirmed in order to reproduce this issue they did have to close the browser window to trigger this bug in order to reproduce this bug (in the steps they took in https://crbug.com/chromium/1282480#c16) PRIOR to landing the fix. 

### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-20)

Hello, Rheza, the VRP Panel has reviewed this report and believe the reward amount is adequate for this issue and this report. We appreciate the opportunity to reassess and convey our decision making process to you here as well as over email. 

### rh...@gmail.com (2022-01-20)

[Comment Deleted]

### rh...@gmail.com (2022-01-20)

Yes Amy, thank you for your assistance.

### rz...@google.com (2022-02-02)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-02)

1. Number of CLs needed for this fix and links to them.
1 CL, https://crrev.com/c/3430928

2. Level of complexity (High, Medium, Low - Explain)
Low, no conflicts

3. Has this been merged to a stable release? beta release?
Stable, 97 and 98

4. Overall Recommendation (Yes, No)
Yes

### gm...@google.com (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-02-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e99e3f53f256e21eb27f29f1ef5797b62df61eb3

commit e99e3f53f256e21eb27f29f1ef5797b62df61eb3
Author: Mitsuru Oshima <oshima@chromium.org>
Date: Thu Feb 03 13:48:34 2022

[M96-LTS] Remove obsever only if drag_window!=drag_source_window in Cleanup

This will cause DragDropContorller::OnWindowDestroyed() not being
called which is supposed to reset the drag_source_window.

Writing a test for this scenario require some rafactoring to test
code, so let me do that in a separate CL.

(cherry picked from commit 1f5969495575d819dcf44a7d94d2e0f1bb4b1d71)

Bug: 1282480
Change-Id: Id8a7efcdd4d1564f0a934a79f1a4706e4a767861
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3370727
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#956674}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3430928
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1440}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/e99e3f53f256e21eb27f29f1ef5797b62df61eb3/ash/drag_drop/drag_drop_controller.cc


### rz...@google.com (2022-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1282480?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058333)*
