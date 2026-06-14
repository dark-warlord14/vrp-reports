#  heap-use-after-free on incontent::RenderFrameHostImpl::AudioContextPlaybackStarted(int)

| Field | Value |
|-------|-------|
| **Issue ID** | [40092538](https://issues.chromium.org/issues/40092538) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Media>Autoplay, Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2018-09-23 |
| **Bounty** | $5,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36

Steps to reproduce the problem:
Version 71.0.3560.0 (Developer Build) (64-bit)
1.build new chrome with asan.
	is_asan = true
	is_debug = false
	enable_nacl = false
	treat_warnings_as_errors = false
2. ./chrome ./crash.html

What is the expected behavior?

What went wrong?
ERROR: AddressSanitizer: heap-use-after-free on address 0x61d0002bdf60 at pc 0x5631f644f043 bp 0x7fff7c3640f0 sp 0x7fff7c3640e8
READ of size 8 at 0x61d0002bdf60 thread T0 (chrome)
    #0 0x5631f644f042 in content::RenderFrameHostImpl::AudioContextPlaybackStarted(int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/render_frame_host_impl.cc:792:3
    #1 0x5631f4c60e51 in blink::mojom::AudioContextManagerStubDispatch::Accept(blink::mojom::AudioContextManager*, mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/gen/third_party/blink/public/mojom/webaudio/audio_context_manager.mojom.cc:137:13
    #2 0x5631fb533a74 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:423:32
    #3 0x5631fb54609e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/multiplex_router.cc:869:42
    #4 0x5631fb5447c1 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/multiplex_router.cc:590:38
    #5 0x5631fb52f08d in mojo::Connector::ReadSingleMessage(unsigned int*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/connector.cc:476:51
    #6 0x5631fb530b28 in mojo::Connector::ReadAllAvailableMessages() /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/connector.cc:505:10
    #7 0x5631fb581977 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:129:12
    #8 0x5631fb581977 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/system/simple_watcher.cc:273:0
    #9 0x5631fb227400 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #10 0x5631fb227400 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #11 0x5631fb223d94 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:434:46
    #12 0x5631fb224a88 in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:445:5
    #13 0x5631fb224a88 in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:517:0
    #14 0x5631fb22e8c7 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_glib.cc:309:49
    #15 0x5631fb29d8c0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #16 0x5631fa6dbaae in ChromeBrowserMainParts::MainMessageLoopRun(int*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/browser/chrome_browser_main.cc:2083:15
    #17 0x5631f5f558dd in content::BrowserMainLoop::RunMainMessageLoopParts() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main_loop.cc:1065:29
    #18 0x5631f5f5ec41 in content::BrowserMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main_runner_impl.cc:161:15
    #19 0x5631f5f4a06b in content::BrowserMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main.cc:47:28
    #20 0x5631fa5504ec in RunBrowserProcessMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:538:10
    #21 0x5631fa5504ec in content::ContentMainRunnerImpl::Run(bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:895:0
    #22 0x5631fa67cc74 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:472:29
    #23 0x5631fa54b55e in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #24 0x5631f3110a86 in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:102:12
    #25 0x7fce20a21b96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

0x61d0002bdf60 is located 224 bytes inside of 2080-byte region [0x61d0002bde80,0x61d0002be6a0)
freed by thread T0 (chrome) here:
    #0 0x5631f310e592 in operator delete(void*) _asan_rtl_:3
    #1 0x5631f64d8a97 in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2321:5
    #2 0x5631f64d8a97 in reset /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2634:0
    #3 0x5631f64d8a97 in ~unique_ptr /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2588:0
    #4 0x5631f64d8a97 in content::RenderFrameHostManager::~RenderFrameHostManager() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/render_frame_host_manager.cc:91:0
    #5 0x5631f63b9693 in content::FrameTreeNode::~FrameTreeNode() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/frame_tree_node.cc:166:1
    #6 0x5631f63bb3a9 in operator() /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2321:5
    #7 0x5631f63bb3a9 in reset /home/cowboy/chromium/src/out/chrome_asan_shared/../../buildtools/third_party/libc++/trunk/include/memory:2634:0
    #8 0x5631f63bb3a9 in content::FrameTreeNode::RemoveChild(content::FrameTreeNode*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/frame_tree_node.cc:211:0
    #9 0x5631f64568e2 in DispatchToMethodImpl<content::RenderFrameHostImpl *, void (content::RenderFrameHostImpl::*)(), std::__1::tuple<>> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/tuple.h:52:3
    #10 0x5631f64568e2 in DispatchToMethod<content::RenderFrameHostImpl *, void (content::RenderFrameHostImpl::*)(), std::__1::tuple<> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/tuple.h:60:0
    #11 0x5631f64568e2 in DispatchToMethod<content::RenderFrameHostImpl, void (content::RenderFrameHostImpl::*)(), void, std::__1::tuple<> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../ipc/ipc_message_templates.h:51:0
    #12 0x5631f64568e2 in bool IPC::MessageT<FrameHostMsg_Detach_Meta, std::__1::tuple<>, void>::Dispatch<content::RenderFrameHostImpl, content::RenderFrameHostImpl, void, void (content::RenderFrameHostImpl::*)()>(IPC::Message const*, content::RenderFrameHostImpl*, content::RenderFrameHostImpl*, void*, void (content::RenderFrameHostImpl::*)()) /home/cowboy/chromium/src/out/chrome_asan_shared/../../ipc/ipc_message_templates.h:146:0
    #13 0x5631f64549bc in content::RenderFrameHostImpl::OnMessageReceived(IPC::Message const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/render_frame_host_impl.cc:1065:5
    #14 0x5631fc949989 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../ipc/ipc_channel_proxy.cc:320:14
    #15 0x5631fb227400 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #16 0x5631fb227400 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #17 0x5631fb223d94 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:434:46
    #18 0x5631fb224a88 in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:445:5
    #19 0x5631fb224a88 in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:517:0
    #20 0x5631fb22e8c7 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_glib.cc:309:49
    #21 0x5631fb29d8c0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #22 0x5631fa6dbaae in ChromeBrowserMainParts::MainMessageLoopRun(int*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/browser/chrome_browser_main.cc:2083:15
    #23 0x5631f5f558dd in content::BrowserMainLoop::RunMainMessageLoopParts() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main_loop.cc:1065:29
    #24 0x5631f5f5ec41 in content::BrowserMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main_runner_impl.cc:161:15
    #25 0x5631f5f4a06b in content::BrowserMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main.cc:47:28
    #26 0x5631fa5504ec in RunBrowserProcessMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:538:10
    #27 0x5631fa5504ec in content::ContentMainRunnerImpl::Run(bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:895:0
    #28 0x5631fa67cc74 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:472:29
    #29 0x5631fa54b55e in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #30 0x5631f3110a86 in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:102:12
    #31 0x7fce20a21b96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

previously allocated by thread T0 (chrome) here:
    #0 0x5631f310d952 in operator new(unsigned long) _asan_rtl_:3
    #1 0x5631f6444767 in content::RenderFrameHostFactory::Create(content::SiteInstance*, content::RenderViewHostImpl*, content::RenderFrameHostDelegate*, content::FrameTree*, content::FrameTreeNode*, int, int, bool, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/render_frame_host_factory.cc:33:27
    #2 0x5631f64d9b13 in content::RenderFrameHostManager::CreateRenderFrameHost(content::SiteInstance*, int, int, int, bool, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/render_frame_host_manager.cc:1705:10
    #3 0x5631f64d9489 in content::RenderFrameHostManager::Init(content::SiteInstance*, int, int, int, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/render_frame_host_manager.cc:100:22
    #4 0x5631f63bae6a in content::FrameTreeNode::AddChild(std::__1::unique_ptr<content::FrameTreeNode, std::__1::default_delete<content::FrameTreeNode> >, int, int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/frame_tree_node.cc:189:28
    #5 0x5631f63b1a62 in content::FrameTree::AddFrame(content::FrameTreeNode*, int, int, mojo::InterfaceRequest<service_manager::mojom::InterfaceProvider>, blink::WebTreeScopeType, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, bool, base::UnguessableToken const&, blink::FramePolicy const&, content::FrameOwnerProperties const&, bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/frame_tree.cc:211:15
    #6 0x5631f6477ebe in content::RenderFrameHostImpl::OnCreateChildFrame(int, mojo::InterfaceRequest<service_manager::mojom::InterfaceProvider>, blink::WebTreeScopeType, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, bool, base::UnguessableToken const&, blink::FramePolicy const&, content::FrameOwnerProperties const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/render_frame_host_impl.cc:1535:16
    #7 0x5631f64fbbb5 in content::(anonymous namespace)::CreateChildFrameOnUI(int, int, blink::WebTreeScopeType, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, bool, base::UnguessableToken const&, blink::FramePolicy const&, content::FrameOwnerProperties const&, int, mojo::ScopedHandleBase<mojo::MessagePipeHandle>) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/render_frame_message_filter.cc:90:24
    #8 0x5631f6503849 in Invoke<void (*)(int, int, blink::WebTreeScopeType, const std::__1::basic_string<char> &, const std::__1::basic_string<char> &, bool, const base::UnguessableToken &, const blink::FramePolicy &, const content::FrameOwnerProperties &, int, mojo::ScopedHandleBase<mojo::MessagePipeHandle>), int, int, blink::WebTreeScopeType, std::__1::basic_string<char>, std::__1::basic_string<char>, bool, base::UnguessableToken, blink::FramePolicy, content::FrameOwnerProperties, int, mojo::ScopedHandleBase<mojo::MessagePipeHandle> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:416:12
    #9 0x5631f6503849 in MakeItSo<void (*)(int, int, blink::WebTreeScopeType, const std::__1::basic_string<char> &, const std::__1::basic_string<char> &, bool, const base::UnguessableToken &, const blink::FramePolicy &, const content::FrameOwnerProperties &, int, mojo::ScopedHandleBase<mojo::MessagePipeHandle>), int, int, blink::WebTreeScopeType, std::__1::basic_string<char>, std::__1::basic_string<char>, bool, base::UnguessableToken, blink::FramePolicy, content::FrameOwnerProperties, int, mojo::ScopedHandleBase<mojo::MessagePipeHandle> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:616:0
    #10 0x5631f6503849 in RunImpl<void (*)(int, int, blink::WebTreeScopeType, const std::__1::basic_string<char> &, const std::__1::basic_string<char> &, bool, const base::UnguessableToken &, const blink::FramePolicy &, const content::FrameOwnerProperties &, int, mojo::ScopedHandleBase<mojo::MessagePipeHandle>), std::__1::tuple<int, int, blink::WebTreeScopeType, std::__1::basic_string<char>, std::__1::basic_string<char>, bool, base::UnguessableToken, blink::FramePolicy, content::FrameOwnerProperties, int, mojo::ScopedHandleBase<mojo::MessagePipeHandle> >, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:689:0
    #11 0x5631f6503849 in base::internal::Invoker<base::internal::BindState<void (*)(int, int, blink::WebTreeScopeType, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, bool, base::UnguessableToken const&, blink::FramePolicy const&, content::FrameOwnerProperties const&, int, mojo::ScopedHandleBase<mojo::MessagePipeHandle>), int, int, blink::WebTreeScopeType, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, bool, base::UnguessableToken, blink::FramePolicy, content::FrameOwnerProperties, int, mojo::ScopedHandleBase<mojo::MessagePipeHandle> >, void ()>::RunOnce(base::internal::BindStateBase*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/bind_internal.h:658:0
    #12 0x5631fb227400 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #13 0x5631fb227400 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #14 0x5631fb223d94 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:434:46
    #15 0x5631fb224a88 in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:445:5
    #16 0x5631fb224a88 in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:517:0
    #17 0x5631fb22e8c7 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_glib.cc:309:49
    #18 0x5631fb29d8c0 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #19 0x5631fa6dbaae in ChromeBrowserMainParts::MainMessageLoopRun(int*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/browser/chrome_browser_main.cc:2083:15
    #20 0x5631f5f558dd in content::BrowserMainLoop::RunMainMessageLoopParts() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main_loop.cc:1065:29
    #21 0x5631f5f5ec41 in content::BrowserMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main_runner_impl.cc:161:15
    #22 0x5631f5f4a06b in content::BrowserMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main.cc:47:28
    #23 0x5631fa5504ec in RunBrowserProcessMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:538:10
    #24 0x5631fa5504ec in content::ContentMainRunnerImpl::Run(bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:895:0
    #25 0x5631fa67cc74 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:472:29
    #26 0x5631fa54b55e in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #27 0x5631f3110a86 in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:102:12
    #28 0x7fce20a21b96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/cowboy/chromium/src/out/chrome_asan_shared/chrome+0xb577042)
Shadow bytes around the buggy address:
  0x0c3a8004fb90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a8004fba0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a8004fbb0: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3a8004fbc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3a8004fbd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c3a8004fbe0: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd
  0x0c3a8004fbf0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a8004fc00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a8004fc10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a8004fc20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a8004fc30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==12378==ABORTING
Received signal 6
    #0 0x5631f30869b1 in __interceptor_backtrace /b/swarming/w/ir/kitchen-workdir/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4024:13
    #1 0x5631fb40a5ce in base::debug::StackTrace::StackTrace(unsigned long) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:820:41
    #2 0x5631fb40957d in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:341:3
    #3 0x7fce27cf4890 in __funlockfile ??:?
    #4 0x7fce27cf4890 in ?? ??:0
    #5 0x7fce20a3ee97 in __libc_signal_restore_set /build/glibc-OTsEL5/glibc-2.27/signal/../sysdeps/unix/sysv/linux/nptl-signals.h:80:0
    #6 0x7fce20a3ee97 in gsignal /build/glibc-OTsEL5/glibc-2.27/signal/../sysdeps/unix/sysv/linux/raise.c:48:0
    #7 0x7fce20a40801 in abort /build/glibc-OTsEL5/glibc-2.27/stdlib/abort.c:79:0
    #8 0x5631f30fc787 in __sanitizer::Abort() /b/swarming/w/ir/kitchen-workdir/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cc:157:3
    #9 0x5631f30fb201 in __sanitizer::Die() /b/swarming/w/ir/kitchen-workdir/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cc:59:5
    #10 0x5631f30e7579 in __asan::ScopedInErrorReport::~ScopedInErrorReport() _asan_rtl_:7
    #11 0x5631f30e6a83 in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) _asan_rtl_:1
    #12 0x5631f30e792b in __asan_report_load8 _asan_rtl_:1
    #13 0x5631f644f043 in content::RenderFrameHostImpl::AudioContextPlaybackStarted(int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/frame_host/render_frame_host_impl.cc:792:3
    #14 0x5631f4c60e52 in blink::mojom::AudioContextManagerStubDispatch::Accept(blink::mojom::AudioContextManager*, mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/gen/third_party/blink/public/mojom/webaudio/audio_context_manager.mojom.cc:137:13
    #15 0x5631fb533a75 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:423:32
    #16 0x5631fb54609f in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/multiplex_router.cc:869:42
    #17 0x5631fb5447c2 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/multiplex_router.cc:590:38
    #18 0x5631fb52f08e in mojo::Connector::ReadSingleMessage(unsigned int*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/connector.cc:476:51
    #19 0x5631fb530b29 in mojo::Connector::ReadAllAvailableMessages() /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/bindings/lib/connector.cc:505:10
    #20 0x5631fb581978 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:129:12
    #21 0x5631fb581978 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../mojo/public/cpp/system/simple_watcher.cc:273:0
    #22 0x5631fb227401 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #23 0x5631fb227401 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #24 0x5631fb223d95 in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:434:46
    #25 0x5631fb224a89 in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:445:5
    #26 0x5631fb224a89 in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:517:0
    #27 0x5631fb22e8c8 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_glib.cc:309:49
    #28 0x5631fb29d8c1 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #29 0x5631fa6dbaaf in ChromeBrowserMainParts::MainMessageLoopRun(int*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/browser/chrome_browser_main.cc:2083:15
    #30 0x5631f5f558de in content::BrowserMainLoop::RunMainMessageLoopParts() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main_loop.cc:1065:29
    #31 0x5631f5f5ec42 in content::BrowserMainRunnerImpl::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main_runner_impl.cc:161:15
    #32 0x5631f5f4a06c in content::BrowserMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/browser/browser_main.cc:47:28
    #33 0x5631fa5504ed in RunBrowserProcessMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:538:10
    #34 0x5631fa5504ed in content::ContentMainRunnerImpl::Run(bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:895:0
    #35 0x5631fa67cc75 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:472:29
    #36 0x5631fa54b55f in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #37 0x5631f3110a87 in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:102:12
    #38 0x7fce20a21b97 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0
    #39 0x5631f303902a in _start ??:0:0
  r8: 0000000000000000  r9: 00007fff7c363130 r10: 0000000000000008 r11: 0000000000000246
 r12: 0000000000000000 r13: 00007fff7c3640e8 r14: 00007fff7c364090 r15: 000056320de6f818
  di: 0000000000000002  si: 00007fff7c363130  bp: 00007fff7c3640c0  bx: 000056320dddd370
  dx: 0000000000000000  ax: 0000000000000000  cx: 00007fce20a3ee97  sp: 00007fff7c363130
  ip: 00007fce20a3ee97 efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Version 71.0.3560.0 (Developer Build) (64-bit)  Channel: dev
OS Version: Ubuntu18.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- [patch.diff](attachments/patch.diff) (application/octet-stream, 2.6 KB)

## Timeline

### cl...@chromium.org (2018-09-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5707699558547456.

### cl...@chromium.org (2018-09-24)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Mojo Internals>Sandbox>SiteIsolation]

### cl...@chromium.org (2018-09-24)

Detailed report: <https://clusterfuzz.com/testcase?key=5707699558547456>

Job Type: linux\_asan\_chrome\_mp  

Platform Id: linux

Crash Type: Heap-use-after-free READ 8  

Crash Address: 0x61d0000baf60  

Crash State:  

content::RenderFrameHostImpl::AudioContextPlaybackStarted  

blink::mojom::AudioContextManagerStubDispatch::Accept  

mojo::InterfaceEndpointClient::HandleValidatedMessage

Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=5707699558547456>

See <https://github.com/google/clusterfuzz-tools> for more information.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### sh...@chromium.org (2018-09-24)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-09-24)

hongchan: Are you a good owner for this?

[Monorail components: -Internals>Mojo -Internals>Sandbox>SiteIsolation Blink>WebAudio]

### ho...@chromium.org (2018-09-24)

I am the owner, but rtoy@ implemented this feature with mlamourie@. Reassigning the issue for the further investigation.

[Monorail components: Blink>Media>Autoplay]

### rt...@chromium.org (2018-09-24)

+hongchan

### mm...@chromium.org (2018-09-24)

Can this be a duplicate of https://crbug.com/chromium/839250?

### rt...@chromium.org (2018-09-24)

Can't tell if it's a duplicate because I can't see the backtrace.

In any case, I can reproduce this locally on my Linux box with ToT a few minutes ago.

Based on the backtrace, I'm guessing that the page is being torn down but the audio thread is still running (as is typical).  The audio thread posts a task to the main thread which calls the mojom interface to notify the browser that audible audio has started.

Someone will have to help me figure out how to handle this case.

### sh...@chromium.org (2018-09-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-25)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2018-09-26)

This is not related to https://crbug.com/chromium/839250. But it is the same root cause as https://crbug.com/chromium/888678.

This bug is because AudioContextManagerImpl takes a raw pointer to the RenderFrameHost but doesn't observe it's lifetime. The lifetime of the Mojo endpoint is managed via the connection error handler, which is not necessarily invoked before the RFH is destroyed.

Possible fixes:
- Make RenderFrameHost own the lifetime of the service
- Make AudioContextManagerImpl a WebContentsObserver and watch for RFH deletion via RenderFrameDeleted.
- Make AudioContextManagerImpl inherit content::FrameServiceBase

### rt...@chromium.org (2018-09-26)

Hongchan has started working on this.

I think this also affects M70 since support for AudioContextPlaybackStarted was also merged to M70.  Adding M70 milestone.

### cd...@gmail.com (2018-09-27)

Here is a kind of patch~
I tried a simple way,making AudioContextManagerImpl inherit FrameServiceBase to observe the RFH lifetime,by changing the AudioContextManagerImpl's constructor and AudioContextManagerImpl::Create().
This patch seems to be useful and crash didn't happen again.

Hope my work helps.
 


### sh...@chromium.org (2018-09-27)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-09-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/63f526d3fe428ae0579b35b256e72597f4bbc14c

commit 63f526d3fe428ae0579b35b256e72597f4bbc14c
Author: Hongchan Choi <hongchan@chromium.org>
Date: Fri Sep 28 17:12:29 2018

Have AudioContextManagerImpl derive from content::FrameServiceBase.

This is a fix suggested by dcheng@ at:
https://bugs.chromium.org/p/chromium/issues/detail?id=888366#c12

Locally confirmed the change stops the crash.

Bug: 888366
Test: The CL build does not crash on the repro case anymore.
Change-Id: I4b56228589b4c71f1191fb82e849240f39c938ed
Reviewed-on: https://chromium-review.googlesource.com/1246945
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Olga Sharonova <olka@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#595127}
[add] https://crrev.com/63f526d3fe428ae0579b35b256e72597f4bbc14c/content/browser/media/webaudio/OWNERS
[modify] https://crrev.com/63f526d3fe428ae0579b35b256e72597f4bbc14c/content/browser/media/webaudio/audio_context_manager_impl.cc
[modify] https://crrev.com/63f526d3fe428ae0579b35b256e72597f4bbc14c/content/browser/media/webaudio/audio_context_manager_impl.h


### ho...@chromium.org (2018-09-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-29)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-01)

Requesting merge to 70

### sh...@chromium.org (2018-10-01)

This bug requires manual review: M70 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-10-01)

[Empty comment from Monorail migration]

### ho...@chromium.org (2018-10-01)

abdulsyed@

Do you want me to proceed with the merge? The merge request was done by awhalley@ at #20.

### aw...@chromium.org (2018-10-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-10-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5315080cb609f5b3ad10609fbf5ada8579ecc39b

commit 5315080cb609f5b3ad10609fbf5ada8579ecc39b
Author: Hongchan Choi <hongchan@chromium.org>
Date: Tue Oct 02 17:27:23 2018

Have AudioContextManagerImpl derive from content::FrameServiceBase.

This is a fix suggested by dcheng@ at:
https://bugs.chromium.org/p/chromium/issues/detail?id=888366#c12

Locally confirmed the change stops the crash.

Bug: 888366
Test: The CL build does not crash on the repro case anymore.
Change-Id: I4b56228589b4c71f1191fb82e849240f39c938ed
Reviewed-on: https://chromium-review.googlesource.com/1246945
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Olga Sharonova <olka@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#595127}(cherry picked from commit 63f526d3fe428ae0579b35b256e72597f4bbc14c)
Reviewed-on: https://chromium-review.googlesource.com/1257148
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/branch-heads/3538@{#819}
Cr-Branched-From: 79f7c91a2b2a2932cd447fa6f865cb6662fa8fa6-refs/heads/master@{#587811}
[add] https://crrev.com/5315080cb609f5b3ad10609fbf5ada8579ecc39b/content/browser/media/webaudio/OWNERS
[modify] https://crrev.com/5315080cb609f5b3ad10609fbf5ada8579ecc39b/content/browser/media/webaudio/audio_context_manager_impl.cc
[modify] https://crrev.com/5315080cb609f5b3ad10609fbf5ada8579ecc39b/content/browser/media/webaudio/audio_context_manager_impl.h


### cr...@appspot.gserviceaccount.com (2018-10-02)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/5315080cb609f5b3ad10609fbf5ada8579ecc39b

Commit: 5315080cb609f5b3ad10609fbf5ada8579ecc39b
Author: hongchan@chromium.org
Commiter: hongchan@chromium.org
Date: 2018-10-02 17:27:23 +0000 UTC

Have AudioContextManagerImpl derive from content::FrameServiceBase.

This is a fix suggested by dcheng@ at:
https://bugs.chromium.org/p/chromium/issues/detail?id=888366#c12

Locally confirmed the change stops the crash.

Bug: 888366
Test: The CL build does not crash on the repro case anymore.
Change-Id: I4b56228589b4c71f1191fb82e849240f39c938ed
Reviewed-on: https://chromium-review.googlesource.com/1246945
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Olga Sharonova <olka@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#595127}(cherry picked from commit 63f526d3fe428ae0579b35b256e72597f4bbc14c)
Reviewed-on: https://chromium-review.googlesource.com/1257148
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/branch-heads/3538@{#819}
Cr-Branched-From: 79f7c91a2b2a2932cd447fa6f865cb6662fa8fa6-refs/heads/master@{#587811}

### aw...@google.com (2018-10-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-04)

Thanks cdsrc2016@! The VRP panel decided to award $5,000 and an additional $500 for helping out with the patch. Cheers!

### aw...@chromium.org (2018-10-04)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-10-05)

Thanks a lot for the reward.

### sh...@chromium.org (2019-01-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/888366?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>Autoplay, Blink>WebAudio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092538)*
