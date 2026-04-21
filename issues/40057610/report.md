# Security: RenderFrameHostImpl logic error leading browser UAF

| Field | Value |
|-------|-------|
| **Issue ID** | [40057610](https://issues.chromium.org/issues/40057610) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Portals, Internals>Sandbox>SiteIsolation, Platform>Apps>BrowserTag |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bt...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2021-10-14 |
| **Bounty** | $20,000.00 |

## Description

This bug is split off from <https://crbug.com/chromium/1260109> to track the RenderFrameHostImpl bug portion of that report. Details below are copied from that bug. Note that this may be similar to <https://crbug.com/chromium/1260007>.

---

= SBX: Logic error in RFHI leads to UAF  

**-------------------------** -------------------------------------------------------

I. VULNERABILITY DETAILS  

When an embedded MimeHandlerView or a Portal is created, they create an Outer and Inner WebContents with RenderFrames and RenderFrameHostImpl. The outer RenderFrameHostImpl will exist in the RenderFrame that created it.

When the outer delegate receives an OnUnloadAck IPC it will reach this branch [1]

```
 if (frame_tree_node_->render_manager()->is_attaching_inner_delegate()) {  
    RenderFrameDeleted();  
    return;  
  }  

```

Which will call the WebContentsObserver::RenderFrameDeleted observer and set the RenderFrameHost's state to `RenderFrameState::kDeleting` [2]. This will cause the RenderFrameHostImpl::~RenderFrameHostImpl destructor to not fire the `RenderFrameDeleted` observer [3]. Mojo connections were are not cleared when RenderFrameDeleted is called, meaning this frame can still bind and call Mojo IPC. Opening up UAFs on every Mojo ipc object that is protected by RendererFrameDeleted [4]. For example,

```
void InstalledAppProviderImpl::RenderFrameDeleted(  
    RenderFrameHost\* render_frame_host) {  
  if (render_frame_host_ == render_frame_host) {  
    render_frame_host_ = nullptr;  
  }  
}  

```
```
void FileSelectHelper::RenderFrameDeleted(  
    content::RenderFrameHost\* render_frame_host) {  
  if (render_frame_host == render_frame_host_)  
    render_frame_host_ = nullptr;  
}  

```

Potentially another bug: I believe that on the browser-side Portals (not renderer side) were accidentally left enabled last Novemeber after the M86 origin trial [5]. Meaning this also affects portals. If this is true (still verifying), I think this should be considered a second High severity bug as it opens up the entire portal attack surface to android.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=4573;drc=800532c0bf6712ea4ab5928da9e776d6607a10b1>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=3125;drc=800532c0bf6712ea4ab5928da9e776d6607a10b1>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=1532;drc=800532c0bf6712ea4ab5928da9e776d6607a10b1>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/file_select_helper.cc;l=782;drc=c2cda003ec3b667d69b2646e7b273d3011a795e4>  

[5] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/common/features.cc;l=174;drc=ed72593f177516f8a62d5c0ca19dc1f21259e71c>

II. EXPLOITATION DETAILS  

#todo

III. REPRODUCTION DETAILS

1. Apply the renderer process patch in 18\_embedder\_rfhi\_intercept/hack\_patch.diff to 94.0.4606.81 (git reset --hard 94.0.4606.81 && gclient sync)  
   
   1a. (run copy\_mojo\_bindings.py /path/to/chromium/out/ mojo if the offsets I provided don't work for whatever reason)
2. Run the caddy server
3. ASAN\_OPTIONS=detect\_odr\_violation=0 ./out/x64.asan/chrome --ignore-certificate-errors --disable-gpu --enable-blink-features=MojoJS,MojoJSTest <https://localhost:8080/index.html>

=================================================================  

==26298==ERROR: AddressSanitizer: heap-use-after-free on address 0x6210006be500 at pc 0x7ff9dfda596e bp 0x7ffddf9281f0 sp 0x7ffddf9281e8  

READ of size 8 at 0x6210006be500 thread T0 (chrome)  

#0 0x7ff9dfda596d in content::FileChooserImpl::EnumerateChosenDirectory(base::FilePath const&, base::OnceCallback<void (mojo::StructPtr[blink::mojom::FileChooserResult](javascript:void(0);))>) content/browser/web\_contents/file\_chooser\_impl.cc:152:47  

#1 0x7ff9d26b0782 in blink::mojom::FileChooserStubDispatch::AcceptWithResponder(blink::mojom::FileChooser\*, mojo::Message\*, std::\_\_Cr::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_Cr::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) gen/third\_party/blink/public/mojom/choosers/file\_chooser.mojom.cc:840:13  

#2 0x7ff9ea3d4e4f in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:860:56  

#3 0x7ff9ea3eb2d7 in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#4 0x7ff9ea3d9cc1 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:655:20  

#5 0x7ff9ea3fcdbe in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:1099:42  

#6 0x7ff9ea3fac61 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:719:7  

#7 0x7ff9ea3eb2d7 in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#8 0x7ff9ea3bd561 in mojo::Connector::DispatchMessage(mojo::Message) mojo/public/cpp/bindings/lib/connector.cc:546:49  

#9 0x7ff9ea3bfa09 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:604:14  

#10 0x7ff9ea3bf1d1 in mojo::Connector::OnHandleReadyInternal(unsigned int) mojo/public/cpp/bindings/lib/connector.cc:439:3  

#11 0x7ff9ea3bf1d1 in mojo::Connector::OnWatcherHandleReady(unsigned int) mojo/public/cpp/bindings/lib/connector.cc:410:3  

#12 0x7ff9ea3c0e7c in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/callback.h:166:12  

#13 0x7ff9ea3c0e7c in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.h:189:14  

#14 0x7ff9ea2ef1b9 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/callback.h:166:12  

#15 0x7ff9ea2ef1b9 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.cc:278:14  

#16 0x7ff9ea2f02e4 in void base::internal::FunctorTraits<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), void>::Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>(void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);)&&, int&&, unsigned int&&, mojo::HandleSignalsState&&) base/bind\_internal.h:509:12  

#17 0x7ff9ea2f02e4 in void base::internal::InvokeHelper<true, void>::MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>(void (mojo::SimpleWatcher::\*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);)&&, int&&, unsigned int&&, mojo::HandleSignalsState&&) base/bind\_internal.h:668:5  

#18 0x7ff9ea2f02e4 in void base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::\*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/bind\_internal.h:721:12  

#19 0x7ff9ea2f02e4 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:690:12  

#20 0x7ff9eb8f22bf in base::OnceCallback<void ()>::Run() && base/callback.h:98:12  

#21 0x7ff9eb8f22bf in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:178:33  

#22 0x7ff9eb962ebe in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:360:23  

#23 0x7ff9eb961a98 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:260:36  

#24 0x7ff9eb963dd1 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#25 0x7ff9eb74ecf9 in base::MessagePumpGlib::HandleDispatch() base/message\_loop/message\_pump\_glib.cc:375:46  

#26 0x7ff9eb74ecf9 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) base/message\_loop/message\_pump\_glib.cc:125:43  

#27 0x7ff98eb5c536 in g\_main\_context\_dispatch (/usr/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x4c536)

0x6210006be500 is located 0 bytes inside of 4672-byte region [0x6210006be500,0x6210006bf740)  

freed by thread T0 (chrome) here:  

#0 0x55f388079dfd in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x7ff9df7a0116 in std::\_\_Cr::default\_delete[content::RenderFrameHostImpl](javascript:void(0);)::operator()(content::RenderFrameHostImpl\*) const buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#2 0x7ff9df7a0116 in std::\_\_Cr::unique\_ptr<content::RenderFrameHostImpl, std::\_\_Cr::default\_delete[content::RenderFrameHostImpl](javascript:void(0);) >::reset(content::RenderFrameHostImpl\*) buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#3 0x7ff9df7a0116 in std::\_\_Cr::unique\_ptr<content::RenderFrameHostImpl, std::\_\_Cr::default\_delete[content::RenderFrameHostImpl](javascript:void(0);) >::~unique\_ptr() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:269:19  

#4 0x7ff9df7a0116 in content::RenderFrameHostManager::~RenderFrameHostManager() content/browser/renderer\_host/render\_frame\_host\_manager.cc:322:3  

#5 0x7ff9df38ebea in content::FrameTreeNode::~FrameTreeNode() content/browser/renderer\_host/frame\_tree\_node.cc:242:1  

#6 0x7ff9df6e0f68 in std::\_\_Cr::default\_delete[content::FrameTreeNode](javascript:void(0);)::operator()(content::FrameTreeNode\*) const buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#7 0x7ff9df6e0f68 in std::\_\_Cr::unique\_ptr<content::FrameTreeNode, std::\_\_Cr::default\_delete[content::FrameTreeNode](javascript:void(0);) >::reset(content::FrameTreeNode\*) buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#8 0x7ff9df6e0f68 in content::RenderFrameHostImpl::RemoveChild(content::FrameTreeNode\*) content/browser/renderer\_host/render\_frame\_host\_impl.cc:3815:22  

#9 0x7ff9df6e2455 in content::RenderFrameHostImpl::PendingDeletionCheckCompleted() content/browser/renderer\_host/render\_frame\_host\_impl.cc:7391:16  

#10 0x7ff9df6e2455 in content::RenderFrameHostImpl::PendingDeletionCheckCompletedOnSubtree() content/browser/renderer\_host/render\_frame\_host\_impl.cc:7397:5  

#11 0x7ff9d232aa69 in blink::mojom::LocalFrameHostStubDispatch::Accept(blink::mojom::LocalFrameHost\*, mojo::Message\*) gen/third\_party/blink/public/mojom/frame/frame.mojom.cc:6675:13  

#12 0x7ff9ea3d4eaa in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:898:54  

#13 0x7ff9ea3eb1ff in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:48:24  

#14 0x7ff9ea3d9cc1 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:655:20  

#15 0x7ff9e5ef7450 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc\_mojo\_bootstrap.cc:981:24  

#16 0x7ff9e5eed7fb in void base::internal::FunctorTraits<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), void>::Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>(void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>&&, mojo::Message&&) base/bind\_internal.h:509:12  

#17 0x7ff9e5eed7fb in void base::internal::InvokeHelper<false, void>::MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>(void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*&&)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>&&, mojo::Message&&) base/bind\_internal.h:648:12  

#18 0x7ff9e5eed7fb in void base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::\_\_Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0ul, 1ul>(void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*&&)(mojo::Message), std::\_\_Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul>) base/bind\_internal.h:721:12  

#19 0x7ff9e5eed7fb in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:690:12  

#20 0x7ff9eb8f22bf in base::OnceCallback<void ()>::Run() && base/callback.h:98:12  

#21 0x7ff9eb8f22bf in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:178:33  

#22 0x7ff9eb962ebe in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:360:23  

#23 0x7ff9eb961a98 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:260:36  

#24 0x7ff9eb963dd1 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#25 0x7ff9eb74d6ca in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_glib.cc:405:48  

#26 0x7ff9eb964bbe in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:467:12  

#27 0x7ff9eb835af8 in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:134:14  

#28 0x7ff9de598a98 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:987:18  

#29 0x7ff9de59e5ac in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:152:15  

#30 0x7ff9de5919aa in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser\_main.cc:49:28  

#31 0x7ff9e0fd7343 in content::RunBrowserProcessMain(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:608:10  

#32 0x7ff9e0fd7343 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content\_main\_runner\_impl.cc:1104:10  

#33 0x7ff9e0fd62ef in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:971:12  

#34 0x7ff9e0fcd981 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content/app/content\_main.cc:390:36  

#35 0x7ff9e0fcf7b2 in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:418:10  

#36 0x55f38807bdf3 in ChromeMain chrome/app/chrome\_main.cc:172:12  

#37 0x7ff98c28fbf6 in \_\_libc\_start\_main /build/glibc-S9d2JN/glibc-2.27/csu/../csu/libc-start.c:310

previously allocated by thread T0 (chrome) here:  

#0 0x55f38807959d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x7ff9df6ade02 in content::RenderFrameHostFactory::Create(content::SiteInstance\*, scoped\_refptr[content::RenderViewHostImpl](javascript:void(0);), content::RenderFrameHostDelegate\*, content::FrameTree\*, content::FrameTreeNode\*, int, mojo::PendingAssociatedRemote[content::mojom::Frame](javascript:void(0);), base::TokenType[blink::LocalFrameTokenTypeMarker](javascript:void(0);) const&, bool, content::RenderFrameHostImpl::LifecycleStateImpl) content/browser/renderer\_host/render\_frame\_host\_factory.cc:35:27  

#2 0x7ff9df7a1811 in content::RenderFrameHostManager::CreateRenderFrameHost(content::RenderFrameHostManager::CreateFrameCase, content::SiteInstance\*, int, mojo::PendingAssociatedRemote[content::mojom::Frame](javascript:void(0);), base::TokenType[blink::LocalFrameTokenTypeMarker](javascript:void(0);) const&, bool) content/browser/renderer\_host/render\_frame\_host\_manager.cc:2703:10  

#3 0x7ff9df7a1aef in content::RenderFrameHostManager::InitChild(content::SiteInstance\*, int, mojo::PendingAssociatedRemote[content::mojom::Frame](javascript:void(0);), base::TokenType[blink::LocalFrameTokenTypeMarker](javascript:void(0);) const&) content/browser/renderer\_host/render\_frame\_host\_manager.cc:344:22  

#4 0x7ff9df6e0965 in content::RenderFrameHostImpl::AddChild(std::\_\_Cr::unique\_ptr<content::FrameTreeNode, std::\_\_Cr::default\_delete[content::FrameTreeNode](javascript:void(0);) >, int, int, mojo::PendingAssociatedRemote[content::mojom::Frame](javascript:void(0);), base::TokenType[blink::LocalFrameTokenTypeMarker](javascript:void(0);) const&) content/browser/renderer\_host/render\_frame\_host\_impl.cc:3728:28  

#5 0x7ff9df382f38 in content::FrameTree::AddFrame(content::RenderFrameHostImpl\*, int, int, mojo::PendingAssociatedRemote[content::mojom::Frame](javascript:void(0);), mojo::PendingReceiver[blink::mojom::BrowserInterfaceBroker](javascript:void(0);), mojo::StructPtr[blink::mojom::PolicyContainerBindParams](javascript:void(0);), blink::mojom::TreeScopeType, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > const&, bool, base::TokenType[blink::LocalFrameTokenTypeMarker](javascript:void(0);) const&, base::UnguessableToken const&, blink::FramePolicy const&, blink::mojom::FrameOwnerProperties const&, bool, blink::mojom::FrameOwnerElementType) content/browser/renderer\_host/frame\_tree.cc:336:15  

#6 0x7ff9df6db81d in content::RenderFrameHostImpl::OnCreateChildFrame(int, mojo::PendingAssociatedRemote[content::mojom::Frame](javascript:void(0);), mojo::PendingReceiver[blink::mojom::BrowserInterfaceBroker](javascript:void(0);), mojo::StructPtr[blink::mojom::PolicyContainerBindParams](javascript:void(0);), blink::mojom::TreeScopeType, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > const&, bool, base::TokenType[blink::LocalFrameTokenTypeMarker](javascript:void(0);) const&, base::UnguessableToken const&, blink::FramePolicy const&, blink::mojom::FrameOwnerProperties const&, blink::mojom::FrameOwnerElementType) content/browser/renderer\_host/render\_frame\_host\_impl.cc:3427:16  

#7 0x7ff9df6dc9e9 in content::RenderFrameHostImpl::CreateChildFrame(int, mojo::PendingAssociatedRemote[content::mojom::Frame](javascript:void(0);), mojo::PendingReceiver[blink::mojom::BrowserInterfaceBroker](javascript:void(0);), mojo::StructPtr[blink::mojom::PolicyContainerBindParams](javascript:void(0);), blink::mojom::TreeScopeType, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > const&, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > const&, bool, blink::FramePolicy const&, mojo::StructPtr[blink::mojom::FrameOwnerProperties](javascript:void(0);), blink::mojom::FrameOwnerElementType) content/browser/renderer\_host/render\_frame\_host\_impl.cc:3461:3  

#8 0x7ff9dd72bf1f in content::mojom::FrameHostStubDispatch::Accept(content::mojom::FrameHost\*, mojo::Message\*) gen/content/common/frame.mojom.cc:4991:13  

#9 0x7ff9ea3d4eaa in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:898:54  

#10 0x7ff9ea3eb1ff in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:48:24  

#11 0x7ff9ea3d9cc1 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:655:20  

#12 0x7ff9e5ef7450 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc\_mojo\_bootstrap.cc:981:24  

#13 0x7ff9e5eed7fb in void base::internal::FunctorTraits<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), void>::Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>(void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>&&, mojo::Message&&) base/bind\_internal.h:509:12  

#14 0x7ff9e5eed7fb in void base::internal::InvokeHelper<false, void>::MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>(void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*&&)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>&&, mojo::Message&&) base/bind\_internal.h:648:12  

#15 0x7ff9e5eed7fb in void base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::\_\_Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0ul, 1ul>(void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*&&)(mojo::Message), std::\_\_Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul>) base/bind\_internal.h:721:12  

#16 0x7ff9e5eed7fb in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:690:12  

#17 0x7ff9eb8f22bf in base::OnceCallback<void ()>::Run() && base/callback.h:98:12  

#18 0x7ff9eb8f22bf in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:178:33  

#19 0x7ff9eb962ebe in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:360:23  

#20 0x7ff9eb961a98 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:260:36  

#21 0x7ff9eb963dd1 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#22 0x7ff9eb74ecf9 in base::MessagePumpGlib::HandleDispatch() base/message\_loop/message\_pump\_glib.cc:375:46  

#23 0x7ff9eb74ecf9 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) base/message\_loop/message\_pump\_glib.cc:125:43  

#24 0x7ff98eb5c536 in g\_main\_context\_dispatch (/usr/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x4c536)

SUMMARY: AddressSanitizer: heap-use-after-free content/browser/web\_contents/file\_chooser\_impl.cc:152:47 in content::FileChooserImpl::EnumerateChosenDirectory(base::FilePath const&, base::OnceCallback<void (mojo::StructPtr[blink::mojom::FileChooserResult](javascript:void(0);))>)  

Shadow bytes around the buggy address:  

0x0c42800cfc50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c42800cfc60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c42800cfc70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c42800cfc80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c42800cfc90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c42800cfca0:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c42800cfcb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c42800cfcc0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c42800cfcd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c42800cfce0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c42800cfcf0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==26298==ABORTING

<<<EOF

## Attachments

- [18_embedder_rfhi_intercept.tar.gz](attachments/18_embedder_rfhi_intercept.tar.gz) (application/octet-stream, 3.5 MB)

## Timeline

### [Deleted User] (2021-10-14)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-10-14)

[Comment Deleted]

### na...@chromium.org (2021-10-14)

Adding mcnee@ for portals.

### dc...@chromium.org (2021-10-14)

[Empty comment from Monorail migration]

[Monorail components: Blink>Portals Platform>Apps>BrowserTag]

### wf...@chromium.org (2021-10-15)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-10-15)

A little more explanation on the renderer patch:

`RenderFrameImpl::Unload` will only be called with `is_loading` set to `false` if the SwapOuterDelegateFrame is called [1], which is the case for these outer webcontent delegate frames.

The patch overwrites `RenderFrameImpl::Unload` and prevents the renderer from unloading the RenderFrameImpl in the renderer. Then it sends an OnUnloadAck to the browser to trigger `RenderFrameDeleted`. Then it executes it's own malicious javascript to bind a FileChooser which holds the render_frame_host_ that is no longer in the Created state [2].

From there in index.html, we intercept the Mojo handle created by the renderer patch I explained above, free the render_frame_host_ (which never triggers RenderFrameDeleted), and call EnumerateChosenDirectory which uses the freed render_frame_host_ because it was never nulled out in RenderFrameDeleted.

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=4345;drc=ed72593f177516f8a62d5c0ca19dc1f21259e71c
[2] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=3133;drc=f0b6f7d12ea47ad7c08fb554f678c1e73801ca36
[3] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=1529;drc=260ee0a4e02100f735284b1abc89761d69d059ba

### [Deleted User] (2021-10-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-10-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cab52ad80cb4985de0c9431d761fe9c909bbfb8f

commit cab52ad80cb4985de0c9431d761fe9c909bbfb8f
Author: Daniel Cheng <dcheng@chromium.org>
Date: Fri Oct 15 20:42:46 2021

Consistently invalidate Mojo connections when render frame is deleted.

Bug: 1260007, 1260134
Change-Id: I2ae77fcbf04b557f7f6e68b55d6c2905708fc220
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3225563
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#932196}

[modify] https://crrev.com/cab52ad80cb4985de0c9431d761fe9c909bbfb8f/content/browser/renderer_host/render_frame_host_impl.cc


### dc...@chromium.org (2021-10-15)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-10-15)

I saw there were two commits attached to the fix here. Did this happen to be a collision?

### dc...@chromium.org (2021-10-16)

Yes, both bugs have the same root cause.

### [Deleted User] (2021-10-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-16)

Requesting merge to stable M94 because latest trunk commit (932196) appears to be after stable branch point (911515).

Requesting merge to beta M95 because latest trunk commit (932196) appears to be after beta branch point (920003).

Requesting merge to dev M96 because latest trunk commit (932196) appears to be after dev branch point (929512).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-16)

Merge approved: your change passed merge requirements and is auto-approved for M96. Please go ahead and merge the CL to branch 4664 (refs/branch-heads/4664) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-16)

Merge review required: M95 has already been cut for stable release.

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
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-16)

Merge review required: M94 is already shipping to stable.

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

### ad...@google.com (2021-10-18)

Marking as a duplicate of https://crbug.com/chromium/1260007 as it's a single root cause. We'll track merges over there.

### bt...@gmail.com (2021-10-18)

Please embargo this and all sub bugs indefinitely. Thanks

### ct...@chromium.org (2021-10-18)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-10-18)

Just a heads up, this poc still works even with this fix:
https://chromium.googlesource.com/chromium/src/+/cab52ad80cb4985de0c9431d761fe9c909bbfb8f

### ad...@google.com (2021-10-18)

Oh, thanks! In that case reopening to see what's up.

### bt...@gmail.com (2021-10-18)

[Comment Deleted]

### bt...@gmail.com (2021-10-18)

I think it might have to do with what sergei commented on in 1260007 here https://bugs.chromium.org/p/chromium/issues/detail?id=1260007#c15. I'll try to verify that's the problem here

### bt...@gmail.com (2021-10-18)

Yup that's the issue. My poc was using a Mojo binding bound to BrowserInterfaceBroker and not the AssociatedRegistry (which is invalidated by `InvalidateMojoConnection()`. So, `broker_receiver_.reset()` after `InvalidateMojoConnection()` to prevent the poc in this issue (and any other mojo binding bound to BrowserInterfaceBroker that relies on RenderFrameDeleted)

### gi...@appspot.gserviceaccount.com (2021-10-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d5a3bd2da61d3a8cb1b931a251a852495bd6cd62

commit d5a3bd2da61d3a8cb1b931a251a852495bd6cd62
Author: Daniel Cheng <dcheng@chromium.org>
Date: Mon Oct 18 20:49:18 2021

Revert "Consistently invalidate Mojo connections when render frame is deleted."

This reverts commit cab52ad80cb4985de0c9431d761fe9c909bbfb8f.

Reason for revert: relanding with a few more fixes

Original change's description:
> Consistently invalidate Mojo connections when render frame is deleted.
>
> Bug: 1260007, 1260134
> Change-Id: I2ae77fcbf04b557f7f6e68b55d6c2905708fc220
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3225563
> Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> Commit-Queue: Daniel Cheng <dcheng@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#932196}

Bug: 1260007, 1260134
Change-Id: I57ea066926e0848e44b76c0caab830dc3d453395
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3228408
Auto-Submit: Daniel Cheng <dcheng@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/main@{#932672}

[modify] https://crrev.com/d5a3bd2da61d3a8cb1b931a251a852495bd6cd62/content/browser/renderer_host/render_frame_host_impl.cc


### ct...@chromium.org (2021-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f52836419f364a2eefe7a6b7b7b3a66be6bb0279

commit f52836419f364a2eefe7a6b7b7b3a66be6bb0279
Author: Daniel Cheng <dcheng@chromium.org>
Date: Wed Oct 20 21:59:08 2021

Reland "Consistently invalidate Mojo connections when render frame is deleted."

This is a reland of cab52ad80cb4985de0c9431d761fe9c909bbfb8f, but also
resets a few additional fields that hold Mojo endpoints to the renderer.

Original change's description:
> Consistently invalidate Mojo connections when render frame is deleted.
>
> Bug: 1260007, 1260134
> Change-Id: I2ae77fcbf04b557f7f6e68b55d6c2905708fc220
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3225563
> Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> Commit-Queue: Daniel Cheng <dcheng@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#932196}

Bug: 1260007, 1260134
Change-Id: Ie04adf7240c2a62ccecca42da554259b0dbbbd7f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3230016
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#933654}

[modify] https://crrev.com/f52836419f364a2eefe7a6b7b7b3a66be6bb0279/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/f52836419f364a2eefe7a6b7b7b3a66be6bb0279/content/browser/renderer_host/render_frame_host_impl.cc


### [Deleted User] (2021-10-30)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2021-11-23)

dcheng: Is this fixed with c#28?

### dc...@chromium.org (2021-11-23)

No, it's still in-progress. I expect to land the more comprehensive fix next week.

### [Deleted User] (2021-12-14)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2022-01-06)

After discussing with dcheng@, we think it makes sense to close this bug (since https://crbug.com/chromium/1260134#c24 notes that the issues here are now addressed) while keeping https://crbug.com/chromium/1260007 open, and to merge r933654.  The cases described in this report should be solved by the updated InvalidateMojoConnection call (including broker_receiver_), and the other known cases are being tracked in followup fixes in https://crbug.com/chromium/1260007.  By merging r933654, we can rule out a large class of bugs, even if we need additional fixes for the ones noted in https://crbug.com/chromium/1260007.

### bt...@gmail.com (2022-01-06)

I also wanted to add that this statement also ended up being true:
```
Potentially another bug: I believe that on the browser-side Portals (not renderer side) were accidentally left enabled last Novemeber after the M86 origin trial [5]. Meaning this also affects portals. If this is true (still verifying), I think this should be considered a second High severity bug as it opens up the entire portal attack surface to android.
```

and was fixed in https://chromium-review.googlesource.com/c/chromium/src/+/3227062 shortly after. It also inspired the discovery of a similar bug in FencedFrames - https://bugs.chromium.org/p/chromium/issues/detail?id=1270358. For people like me who are interested in code archaeology (bug etymology?), it sounds like 1270358 was introduced because kPortal's feature flag implementation was being used as example code while it was left enabled. I did a quick audit and only found the kFencedFrames bug, but it seems like a pattern that could potentially pop up again in the future.

### cr...@chromium.org (2022-01-06)

Ah yes-- thanks for following up there!  (I actually had a note to myself to mention mcnee@'s r932239 but forgot to in https://crbug.com/chromium/1260134#c34.)  CC'ing dom@ for the observation in https://crbug.com/chromium/1260134#c35, as we think about ways to make such bugs less likely.

### dc...@chromium.org (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

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

### ad...@google.com (2022-01-07)

Adding 96 merge request which Sheriffbot would have done if Daniel hadn't tried to outsmart it in https://crbug.com/chromium/1260134#c37 :) In general please just mark bugs fixed so that sheriffbot can follow its automated rules.

(96 is extended stable)

### [Deleted User] (2022-01-07)

Merge review required: M96 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-07)

Thanks everyone for the updates here and on/as they pertain to https://crbug.com/chromium/1260007. Merge approved for M97, please go ahead and merge  r933654 to branch 4692 at your earliest convenience so this fix can be in the next stable security refresh. 
Also, merge approved for M96, please merge to branch 4664 so these fixes can be merged to Extended. 

### am...@chromium.org (2022-01-07)

[Empty comment from Monorail migration]

### cr...@chromium.org (2022-01-07)

Just to clarify, r933654 landed in 97.0.4677.0 and doesn't need a merge to M97.  But the merge to M96 is needed for extended stable.  Thanks!

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cd661299187203b4701393b95af99ffbe9f626d5

commit cd661299187203b4701393b95af99ffbe9f626d5
Author: Daniel Cheng <dcheng@chromium.org>
Date: Sat Jan 08 00:16:39 2022

[M96] Reland "Consistently invalidate Mojo connections when render frame is deleted."

This is a reland of cab52ad80cb4985de0c9431d761fe9c909bbfb8f, but also
resets a few additional fields that hold Mojo endpoints to the renderer.

Original change's description:
> Consistently invalidate Mojo connections when render frame is deleted.
>
> Bug: 1260007, 1260134
> Change-Id: I2ae77fcbf04b557f7f6e68b55d6c2905708fc220
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3225563
> Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> Commit-Queue: Daniel Cheng <dcheng@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#932196}

(cherry picked from commit f52836419f364a2eefe7a6b7b7b3a66be6bb0279)

Bug: 1260007, 1260134
Change-Id: Ie04adf7240c2a62ccecca42da554259b0dbbbd7f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3230016
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#933654}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3371628
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Charles Reis <creis@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1375}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/cd661299187203b4701393b95af99ffbe9f626d5/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/cd661299187203b4701393b95af99ffbe9f626d5/content/browser/renderer_host/render_frame_host_impl.cc


### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-13)

Congratulations, Brendon! The VRP Panel has decided to award you $20,000 for this report. We appreciate all your efforts from the submission of your full chain report, your through analysis in working with the Chrome Security team. 
You'll share the credit with Sergei Glazunov of Project Zero as his report was reported just narrowly (four hours!) before yours, but we wanted to bonus you for this high quality report and all your efforts following reporting this issue to us. Cheers! 

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-19)

CVE and acknowledgment to be shared with https://crbug.com/chromium/1260007; CVE and acknowledgement (but displaying both bug IDs) to be shared between Sergei and Brendon due to the impossibly tight delta between reports

### [Deleted User] (2022-04-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-13)

[Empty comment from Monorail migration]

### ti...@chromium.org (2023-07-26)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1260134?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Portals, Internals>Sandbox>SiteIsolation, Platform>Apps>BrowserTag]
[Monorail blocking: crbug.com/chromium/1260109]
[Monorail mergedwith: crbug.com/chromium/1260109]
[Monorail mergedinto: crbug.com/chromium/1260007]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057610)*
