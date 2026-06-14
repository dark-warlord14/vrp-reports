# Security: heap-use-after-free in content::RenderFrameImpl::CommitFailedNavigationInternal

| Field | Value |
|-------|-------|
| **Issue ID** | [40094762](https://issues.chromium.org/issues/40094762) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>HTML>Object, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, ChromeOS |
| **Reporter** | sc...@yo.net.nz |
| **Assignee** | dg...@chromium.org |
| **Created** | 2019-04-28 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASAN reports a UaF when running the attached repro in headless mode.

./chrome --headless repro.html

**VERSION**  

Chrome Version: Chromium 76.0.3775.0 (asan-linux-release-653409)  

Operating System: Ubuntu 18.04

ASAN output:

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x61d00005e2da at pc 0x5559d4a640e3 bp 0x7ffc1f78f3b0 sp 0x7ffc1f78f3a8  

WRITE of size 1 at 0x61d00005e2da thread T0 (chrome)  

#0 0x5559d4a640e2 in content::RenderFrameImpl::CommitFailedNavigationInternal(content::CommonNavigationParams const&, content::CommitNavigationParams const&, bool, int, base::Optional<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > > const&, std::\_\_1::unique\_ptr<blink::URLLoaderFactoryBundleInfo, std::\_\_1::default\_delete[blink::URLLoaderFactoryBundleInfo](javascript:void(0);) >, base::OnceCallback<void (blink::mojom::CommitResult)>, base::OnceCallback<void (std::\_\_1::unique\_ptr<FrameHostMsg\_DidCommitProvisionalLoad\_Params, std::\_\_1::default\_delete<FrameHostMsg\_DidCommitProvisionalLoad\_Params> >, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);))>) ./../../content/renderer/render\_frame\_impl.cc:3698  

#1 0x5559d4a640e2 in ?? ??:0  

#2 0x5559d4a6481c in CommitFailedNavigation ./../../content/renderer/render\_frame\_impl.cc:3603  

#3 0x5559d4a6481c in ?? ??:0  

#4 0x5559bf311804 in ?? ??:0  

#5 0x5559bf311804 in content::mojom::FrameNavigationControlStubDispatch::AcceptWithResponder(content::mojom::FrameNavigationControl\*, mojo::Message\*, std::\_\_1::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_1::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) ./gen/content/common/frame.mojom.cc:2893  

#6 0x5559bf311804 in ?? ??:0  

#7 0x5559d4abb24c in content::mojom::FrameNavigationControlStub<mojo::RawPtrImplRefTraits[content::mojom::FrameNavigationControl](javascript:void(0);) >::AcceptWithResponder(mojo::Message\*, std::\_\_1::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_1::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) ./gen/content/common/frame.mojom.h:642  

#8 0x5559d4abb24c in ?? ??:0  

#9 0x5559c6b236fd in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:412  

#10 0x5559c6b236fd in ?? ??:0  

#11 0x5559c802c292 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread(mojo::Message) ./../../ipc/ipc\_mojo\_bootstrap.cc:912  

#12 0x5559c802c292 in ?? ??:0  

#13 0x5559c8024ec6 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:499  

#14 0x5559c8024ec6 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:599  

#15 0x5559c8024ec6 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::\_\_1::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, base::internal::PassedWrapper[mojo::Message](javascript:void(0);) >, 0, 1> ./../../base/bind\_internal.h:672  

#16 0x5559c8024ec6 in RunOnce ./../../base/bind\_internal.h:641  

#17 0x5559c8024ec6 in ?? ??:0  

#18 0x5559c68d8ddb in Run ./../../base/callback.h:97  

#19 0x5559c68d8ddb in RunTask ./../../base/task/common/task\_annotator.cc:114  

#20 0x5559c68d8ddb in ?? ??:0  

#21 0x5559c690c5dd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:363  

#22 0x5559c690c5dd in ?? ??:0  

#23 0x5559c690bb97 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:214  

#24 0x5559c690bb97 in ?? ??:0  

#25 0x5559c6821fb0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39  

#26 0x5559c6821fb0 in ?? ??:0  

#27 0x5559c690e60e in Run ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:448  

#28 0x5559c690e60e in ?? ??:0  

#29 0x5559c688d57c in ?? ??:0  

#30 0x5559c688d57c in base::RunLoop::RunWithTimeout(base::TimeDelta) ./../../base/run\_loop.cc:161  

#31 0x5559c688d57c in ?? ??:0  

#32 0x5559d67cc6bb in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer\_main.cc:223  

#33 0x5559d67cc6bb in ?? ??:0  

#34 0x5559c592cb6d in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:513  

#35 0x5559c592cb6d in ?? ??:0  

#36 0x5559c59301fa in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content\_main\_runner\_impl.cc:881  

#37 0x5559c59301fa in ?? ??:0  

#38 0x5559c5a55f84 in service\_manager::Main(service\_manager::MainParams const&) ./../../services/service\_manager/embedder/main.cc:415  

#39 0x5559c5a55f84 in ?? ??:0  

#40 0x5559c592b0c4 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content\_main.cc:19  

#41 0x5559c592b0c4 in ?? ??:0  

#42 0x5559d6d55a2e in headless::(anonymous namespace)::RunContentMain(headless::HeadlessBrowser::Options, base::OnceCallback<void (headless::HeadlessBrowser\*)>) ./../../headless/lib/browser/headless\_browser\_impl.cc:60  

#43 0x5559d6d55a2e in ?? ??:0  

#44 0x5559d6d5567a in headless::RunChildProcessIfNeeded(int, char const\*\*) ./../../headless/lib/browser/headless\_browser\_impl.cc:269  

#45 0x5559d6d5567a in ?? ??:0  

#46 0x5559c5a4db25 in headless::HeadlessShellMain(int, char const\*\*) ./../../headless/app/headless\_shell.cc:621  

#47 0x5559c5a4db25 in ?? ??:0  

#48 0x5559bd2b8e10 in ChromeMain ./../../chrome/app/chrome\_main.cc:99  

#49 0x5559bd2b8e10 in ?? ??:0  

#50 0x7f9d0e748b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310  

#51 0x7f9d0e748b96 in ?? ??:0

0x61d00005e2da is located 1626 bytes inside of 2296-byte region [0x61d00005dc80,0x61d00005e578)  

freed by thread T0 (chrome) here:  

#0 0x5559bd2b6f6d in operator delete(void\*) *asan\_rtl*  

#1 0x5559bd2b6f6d in ?? ??:0  

#2 0x5559d4a71b63 in content::RenderFrameImpl::FrameDetached(blink::WebLocalFrameClient::DetachType) ./../../content/renderer/render\_frame\_impl.cc:4417  

#3 0x5559d4a71b63 in ?? ??:0  

#4 0x5559d1edb8f7 in blink::LocalFrameClientImpl::Detached(blink::FrameDetachType) ./../../third\_party/blink/renderer/core/exported/local\_frame\_client\_impl.cc:361  

#5 0x5559d1edb8f7 in ?? ??:0  

#6 0x5559d1d12129 in blink::Frame::Detach(blink::FrameDetachType) ./../../third\_party/blink/renderer/core/frame/frame.cc:96  

#7 0x5559d1d12129 in ?? ??:0  

#8 0x5559d22578e1 in blink::HTMLPlugInElement::DisconnectContentFrame() ./../../third\_party/blink/renderer/core/html/html\_plugin\_element.cc:536  

#9 0x5559d22578e1 in ?? ??:0  

#10 0x5559d14a49f0 in blink::ChildFrameDisconnector::DisconnectCollectedFrameOwners() ./../../third\_party/blink/renderer/core/dom/child\_frame\_disconnector.cc:59  

#11 0x5559d14a49f0 in ?? ??:0  

#12 0x5559d14a3f93 in blink::ChildFrameDisconnector::Disconnect(blink::ChildFrameDisconnector::DisconnectPolicy) ./../../third\_party/blink/renderer/core/dom/child\_frame\_disconnector.cc:32  

#13 0x5559d14a3f93 in ?? ??:0  

#14 0x5559d147c528 in blink::ContainerNode::WillRemoveChildren() ./../../third\_party/blink/renderer/core/dom/container\_node.cc:655  

#15 0x5559d147c528 in ?? ??:0  

#16 0x5559d147d9ba in blink::ContainerNode::RemoveChildren(blink::SubtreeModificationAction) ./../../third\_party/blink/renderer/core/dom/container\_node.cc:794  

#17 0x5559d147d9ba in ?? ??:0  

#18 0x5559d14d8aba in blink::Document::ImplicitOpen(blink::ParserSynchronizationPolicy) ./../../third\_party/blink/renderer/core/dom/document.cc:3152  

#19 0x5559d14d8aba in ?? ??:0  

#20 0x5559d14c0cae in blink::Document::open() ./../../third\_party/blink/renderer/core/dom/document.cc:3113  

#21 0x5559d14c0cae in ?? ??:0  

#22 0x5559d14d8848 in blink::Document::open(blink::Document\*, blink::ExceptionState&) ./../../third\_party/blink/renderer/core/dom/document.cc:3063  

#23 0x5559d14d8848 in ?? ??:0  

#24 0x5559d14da452 in blink::Document::open(v8::Isolate\*, WTF::AtomicString const&, WTF::AtomicString const&, blink::ExceptionState&) ./../../third\_party/blink/renderer/core/dom/document.cc:3289  

#25 0x5559d14da452 in ?? ??:0  

#26 0x5559d007ce6d in blink::document\_v8\_internal::Open1Method(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_document.cc:4158  

#27 0x5559d007ce6d in ?? ??:0  

#28 0x5559d005de23 in blink::V8Document::OpenMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) v8\_document.cc:?  

#29 0x5559d005de23 in OpenMethodCallback ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_document.cc:7442  

#30 0x5559d005de23 in ?? ??:0  

#31 0x5559c2c4cdbd in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api-arguments-inl.h:157  

#32 0x5559c2c4cdbd in ?? ??:0  

#33 0x5559c2c4aaff in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109  

#34 0x5559c2c4aaff in ?? ??:0  

#35 0x5559c2c488c4 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-api.cc:139  

#36 0x5559c2c488c4 in ?? ??:0  

#37 0x5559c48a5e58 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit snapshot-external.cc:?  

#38 0x5559c48a5e58 in ?? ??:0  

#39 0x5559c481b0a3 in Builtins\_InterpreterEntryTrampoline snapshot-external.cc:?  

#40 0x5559c481b0a3 in ?? ??:0  

#41 0x5559c481b0a3 in Builtins\_InterpreterEntryTrampoline snapshot-external.cc:?  

#42 0x5559c481b0a3 in ?? ??:0  

#43 0x5559c4818a1c in Builtins\_JSEntryTrampoline snapshot-external.cc:?  

#44 0x5559c4818a1c in ?? ??:0  

#45 0x5559c48187f7 in Builtins\_JSEntry snapshot-external.cc:?  

#46 0x5559c48187f7 in ?? ??:0  

#47 0x5559c2f2dac8 in Call ./../../v8/src/simulator.h:138  

#48 0x5559c2f2dac8 in Invoke ./../../v8/src/execution.cc:266  

#49 0x5559c2f2dac8 in ?? ??:0  

#50 0x5559c2f2cfe5 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution.cc:358  

#51 0x5559c2f2cfe5 in ?? ??:0  

#52 0x5559c2b04c93 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) ./../../v8/src/api.cc:4989  

#53 0x5559c2b04c93 in ?? ??:0  

#54 0x5559cfe11f85 in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:457  

#55 0x5559cfe11f85 in ?? ??:0  

#56 0x5559cfe642b5 in blink::V8EventHandlerNonNull::InvokeWithoutRunnabilityCheck(blink::bindings::V8ValueOrScriptWrappableAdapter, WTF::Vector<blink::ScriptValue, 0u, WTF::PartitionAllocator> const&) ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_event\_handler\_non\_null.cc:356  

#57 0x5559cfe642b5 in ?? ??:0  

#58 0x5559cfe5fab2 in blink::JSEventHandler::InvokeInternal(blink::EventTarget&, blink::Event&, v8::Local[v8::Value](javascript:void(0);)) ./../../third\_party/blink/renderer/bindings/core/v8/js\_event\_handler.cc:122  

#59 0x5559cfe5fab2 in ?? ??:0  

#60 0x5559cfe62e9d in blink::JSBasedEventListener::Invoke(blink::ExecutionContext\*, blink::Event\*) ./../../third\_party/blink/renderer/bindings/core/v8/js\_based\_event\_listener.cc:152  

#61 0x5559cfe62e9d in ?? ??:0

previously allocated by thread T0 (chrome) here:  

#0 0x5559bd2b670d in operator new(unsigned long) *asan\_rtl*  

#1 0x5559bd2b670d in ?? ??:0  

#2 0x5559d4a2a85c in content::RenderFrameImpl::Create(content::RenderViewImpl\*, int, mojo::InterfacePtr<service\_manager::mojom::InterfaceProvider>, mojo::InterfacePtr[blink::mojom::DocumentInterfaceBroker](javascript:void(0);), base::UnguessableToken const&) ./../../content/renderer/render\_frame\_impl.cc:1337  

#3 0x5559d4a2a85c in ?? ??:0  

#4 0x5559d4a6dfb8 in content::RenderFrameImpl::CreateChildFrame(blink::WebLocalFrame\*, blink::WebTreeScopeType, blink::WebString const&, blink::WebString const&, blink::FramePolicy const&, blink::WebFrameOwnerProperties const&, blink::FrameOwnerElementType) ./../../content/renderer/render\_frame\_impl.cc:4288  

#5 0x5559d4a6dfb8 in ?? ??:0  

#6 0x5559d1ebd5d8 in blink::WebLocalFrameImpl::CreateChildFrame(WTF::AtomicString const&, blink::HTMLFrameOwnerElement\*) ./../../third\_party/blink/renderer/core/frame/web\_local\_frame\_impl.cc:1819  

#7 0x5559d1ebd5d8 in ?? ??:0  

#8 0x5559d21ed769 in blink::HTMLFrameOwnerElement::LoadOrRedirectSubframe(blink::KURL const&, WTF::AtomicString const&, bool) ./../../third\_party/blink/renderer/core/html/html\_frame\_owner\_element.cc:424  

#9 0x5559d21ed769 in ?? ??:0  

#10 0x5559d225292e in blink::HTMLPlugInElement::RequestObjectInternal(blink::PluginParameters const&) ./../../third\_party/blink/renderer/core/html/html\_plugin\_element.cc:222  

#11 0x5559d225292e in ?? ??:0  

#12 0x5559d2257daa in blink::HTMLPlugInElement::RequestObject(blink::PluginParameters const&) ./../../third\_party/blink/renderer/core/html/html\_plugin\_element.cc:608  

#13 0x5559d2257daa in ?? ??:0  

#14 0x5559d224757e in blink::HTMLObjectElement::UpdatePluginInternal() ./../../third\_party/blink/renderer/core/html/html\_object\_element.cc:289  

#15 0x5559d224757e in ?? ??:0  

#16 0x5559d225587d in blink::HTMLPlugInElement::UpdatePlugin() ./../../third\_party/blink/renderer/core/html/html\_plugin\_element.cc:301  

#17 0x5559d225587d in ?? ??:0  

#18 0x5559d1dab0dc in blink::LocalFrameView::UpdatePlugins() ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:1778  

#19 0x5559d1dab0dc in ?? ??:0  

#20 0x5559d1d937cd in blink::LocalFrameView::UpdatePluginsTimerFired(blink::TimerBase\*) ./../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:1793  

#21 0x5559d1d937cd in ?? ??:0  

#22 0x5559d09f84ea in blink::TimerBase::RunInternal() ./../../third\_party/blink/renderer/platform/timer.cc:156  

#23 0x5559d09f84ea in ?? ??:0  

#24 0x5559c68d8ddb in Run ./../../base/callback.h:97  

#25 0x5559c68d8ddb in RunTask ./../../base/task/common/task\_annotator.cc:114  

#26 0x5559c68d8ddb in ?? ??:0  

#27 0x5559c690c5dd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:363  

#28 0x5559c690c5dd in ?? ??:0  

#29 0x5559c690bb97 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:214  

#30 0x5559c690bb97 in ?? ??:0  

#31 0x5559c6821fb0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39  

#32 0x5559c6821fb0 in ?? ??:0  

#33 0x5559c690e60e in Run ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:448  

#34 0x5559c690e60e in ?? ??:0  

#35 0x5559c688d57c in ?? ??:0  

#36 0x5559c688d57c in base::RunLoop::RunWithTimeout(base::TimeDelta) ./../../base/run\_loop.cc:161  

#37 0x5559c688d57c in ?? ??:0  

#38 0x5559d67cc6bb in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer\_main.cc:223  

#39 0x5559d67cc6bb in ?? ??:0  

#40 0x5559c592cb6d in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:513  

#41 0x5559c592cb6d in ?? ??:0  

#42 0x5559c59301fa in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content\_main\_runner\_impl.cc:881  

#43 0x5559c59301fa in ?? ??:0  

#44 0x5559c5a55f84 in service\_manager::Main(service\_manager::MainParams const&) ./../../services/service\_manager/embedder/main.cc:415  

#45 0x5559c5a55f84 in ?? ??:0  

#46 0x5559c592b0c4 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content\_main.cc:19  

#47 0x5559c592b0c4 in ?? ??:0  

#48 0x5559d6d55a2e in headless::(anonymous namespace)::RunContentMain(headless::HeadlessBrowser::Options, base::OnceCallback<void (headless::HeadlessBrowser\*)>) ./../../headless/lib/browser/headless\_browser\_impl.cc:60  

#49 0x5559d6d55a2e in ?? ??:0  

#50 0x5559d6d5567a in headless::RunChildProcessIfNeeded(int, char const\*\*) ./../../headless/lib/browser/headless\_browser\_impl.cc:269  

#51 0x5559d6d5567a in ?? ??:0  

#52 0x5559c5a4db25 in headless::HeadlessShellMain(int, char const\*\*) ./../../headless/app/headless\_shell.cc:621  

#53 0x5559c5a4db25 in ?? ??:0  

#54 0x5559bd2b8e10 in ChromeMain ./../../chrome/app/chrome\_main.cc:99  

#55 0x5559bd2b8e10 in ?? ??:0  

#56 0x7f9d0e748b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310  

#57 0x7f9d0e748b96 in ?? ??:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/ubuntu/blab/asan-linux-release-653409/chrome+0x202bf0e2)  

Shadow bytes around the buggy address:  

0x0c3a80003c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a80003c10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a80003c20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a80003c30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a80003c40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c3a80003c50: fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd  

0x0c3a80003c60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a80003c70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a80003c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a80003c90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3a80003ca0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

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

Shadow gap: cc  

==1==ABORTING  

[0425/125742.783383:ERROR:headless\_shell.cc(315)] Abnormal renderer termination.

**CREDIT INFORMATION**  

Reporter credit: Scott Bell of Pulse Security

## Attachments

- [repro.html](attachments/repro.html) (text/plain, 52.5 KB)

## Timeline

### cl...@chromium.org (2019-04-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5169335627284480.

### cl...@chromium.org (2019-04-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5743731702104064.

### cl...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-04-29)

Detailed report: https://clusterfuzz.com/testcase?key=5743731702104064

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61d0000371a0
Crash State:
  ...see report...
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=653848:653850

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5743731702104064

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-04-29)

Detailed report: https://clusterfuzz.com/testcase?key=5169335627284480

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61d000037ba0
Crash State:
  ...see report...
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=653848:653850

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5169335627284480

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### mm...@chromium.org (2019-04-30)

dgozman@, the regression range points to https://chromium.googlesource.com/chromium/src/+log/abd417b68802064a6711c138c4480740ea8e1e62..fe84a6ddbf35d8634e68f54a310253bb495825e9?pretty=fuller&n=10000

[Monorail components: Blink>HTML>Object UI>Browser>Navigation]

### sh...@chromium.org (2019-04-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-04-30)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dg...@chromium.org (2019-04-30)

The fix is underway: https://chromium-review.googlesource.com/c/chromium/src/+/1578588

### cl...@chromium.org (2019-05-01)

ClusterFuzz has detected this issue as fixed in range 655363:655381.

Detailed report: https://clusterfuzz.com/testcase?key=5169335627284480

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61d000037ba0
Crash State:
  content::RenderFrameImpl::CommitFailedNavigationInternal
  content::RenderFrameImpl::CommitFailedNavigation
  content::mojom::FrameNavigationControlStubDispatch::AcceptWithResponder
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=653848:653850
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=655363:655381

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5169335627284480

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-05-01)

ClusterFuzz has detected this issue as fixed in range 655363:655381.

Detailed report: https://clusterfuzz.com/testcase?key=5743731702104064

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61d0000371a0
Crash State:
  content::RenderFrameImpl::CommitFailedNavigationInternal
  content::RenderFrameImpl::CommitFailedNavigation
  content::mojom::FrameNavigationControlStubDispatch::AcceptWithResponder
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=653848:653850
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=655363:655381

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5743731702104064

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-05-01)

ClusterFuzz testcase 5743731702104064 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-05-02)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-06)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-05-09)

Congrats! The Panel decided to reward $3,000 for this report :) 

A member from our finance team will be in touch shortly.

### na...@google.com (2019-05-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-08-08)

This issue was migrated from crbug.com/chromium/957436?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HTML>Object, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094762)*
