# Security: Heap-use-after-free in the ReadAnythingAppController::Install

| Field | Value |
|-------|-------|
| **Issue ID** | [360274917](https://issues.chromium.org/issues/360274917) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Accessibility, UI>Accessibility>ReadingMode |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 126.0.0.0 |
| **Reporter** | me...@gmail.com |
| **Assignee** | ab...@google.com |
| **Created** | 2024-08-16 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. download the newest asan-linux-release.zip and unzip
2. run chrome `chrome --user-data-dir=/tmp/noexist123 --no-sandbox` and open `chrome-untrusted://read-anything-side-panel.top-chrome/`
3. go back and go forward several times to trigger the UAF  
   
   Note that this function needs to download a screen\_ai library, and it's path is `/path/to/user-data/screen_ai/XXXX`, if you don't have it, please wait until it is downloaded.
   The reproduction steps are the same as those in issue <https://issues.chromium.org/issues/41490491>. You can refer to the video in [issue 41490491](https://issues.chromium.org/issues/41490491) for detailed reproduction steps.

# Problem Description

This issue shares the same trigger path as [issue 41490491](https://issues.chromium.org/issues/41490491) but results in a different ASAN report. It appears that the `SecondWeakCallback` can still be invoked after the `RenderFrame` has been deleted, leading to a use-after-free (UAF) vulnerability.
And the ASAN log shows that this issues is not protected by the miracle\_ptr.

# Summary

Security: Heap-use-after-free in the ReadAnythingAppController::Install

# Custom Questions

#### Type of crash:

tab

#### Crash state:

=================================================================
==2516==ERROR: AddressSanitizer: heap-use-after-free on address 0x61a00000a290 at pc 0x00013dc61918 bp 0x00016f341600 sp 0x00016f3415f8
READ of size 8 at 0x61a00000a290 thread T0
==2516==WARNING: invalid path to external symbolizer!
==2516==WARNING: Failed to use and restart external symbolizer!
#0 0x00013dc61914 in gin::WrappableBase::SecondWeakCallback(v8::WeakCallbackInfogin::WrappableBase const&)+0x68 (/Users/krace/fuzz/chromium\_src/src/out/ui/libgin.dylib:arm64+0x29914)
#1 0x00014841291c in v8::internal::GlobalHandles::InvokeSecondPassPhantomCallbacks()+0x394 (/Users/krace/fuzz/chromium\_src/src/out/ui/libv8.dylib:arm64+0x6e691c)
#2 0x00013dc586a8 in base::internal::Invoker<base::internal::FunctorTraits<void (v8::Task::&&)(), std::\_\_Cr::unique\_ptr<v8::Task, std::\_\_Cr::default\_deletev8::Task>&&>, base::internal::BindState<true, true, false, void (v8::Task::)(), std::\_\_Cr::unique\_ptr<v8::Task, std::\_\_Cr::default\_deletev8::Task>>, void ()>::RunOnce(base::internal::BindStateBase\*)+0x11c (/Users/krace/fuzz/chromium\_src/src/out/ui/libgin.dylib:arm64+0x206a8)
#3 0x0001035e539c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x1b139c)
#4 0x000103652648 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0x864 (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x21e648)
#5 0x00010365192c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x21d92c)
#6 0x0001034bea30 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*)+0x1b0 (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x8aa30)
#7 0x000103653c0c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x36c (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x21fc0c)
#8 0x00010356c2f0 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x1382f0)
#9 0x0001313efc54 in content::RendererMain(content::MainFunctionParams)+0x6e8 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x3167c54)
#10 0x0001315d5724 in content::RunOtherNamedProcessTypeMain(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate\*)+0x3ec (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x334d724)
#11 0x0001315d7480 in content::ContentMainRunnerImpl::Run()+0x454 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x334f480)
#12 0x0001315d353c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*)+0x5c0 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x334b53c)
#13 0x0001315d3e08 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x334be08)
#14 0x000117a5afb8 in ChromeMain+0x370 (/Users/krace/fuzz/chromium\_src/src/out/ui/libchrome\_dll.dylib:arm64+0xafb8)
#15 0x000100abcce4 in main+0x254 (/Users/krace/fuzz/chromium\_src/src/out/ui/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/129.0.6653.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000ce4)
#16 0x00018fa320dc (<unknown module>)
#17 0x8353fffffffffffc (<unknown module>)
0x61a00000a290 is located 16 bytes inside of 1176-byte region [0x61a00000a280,0x61a00000a718)
freed by thread T0 here:
#0 0x000101a04400 in \_\_sanitizer\_finish\_switch\_fiber+0xa24 (/Users/krace/fuzz/chromium\_src/src/out/ui/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x60400)
#1 0x000131357cd8 in content::RenderFrameImpl::~RenderFrameImpl()+0x4f8 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x30cfcd8)
#2 0x0001313592bc in content::RenderFrameImpl::~RenderFrameImpl()+0x8 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x30d12bc)
#3 0x000131378ea8 in content::RenderFrameImpl::FrameDetached()+0x59c (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x30f0ea8)
#4 0x0001599360e8 in blink::LocalFrameClientImpl::Detached(blink::FrameDetachType)+0x120 (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x14360e8)
#5 0x00015972c720 in blink::Frame::Detach(blink::FrameDetachType)+0x3b4 (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x122c720)
#6 0x000159732d20 in blink::Frame::SwapImpl(blink::WebFrame\*, mojo::PendingAssociatedRemoteblink::mojom::blink::RemoteFrameHost, mojo::PendingAssociatedReceiverblink::mojom::blink::RemoteFrame)+0x3b0 (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x1232d20)
#7 0x000159734b90 in blink::Frame::Swap(blink::WebRemoteFrame\*, mojo::PendingAssociatedRemoteblink::mojom::blink::RemoteFrameHost, mojo::PendingAssociatedReceiverblink::mojom::blink::RemoteFrame)+0x11c (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x1234b90)
#8 0x000159940fc4 in blink::WebFrame::Swap(blink::WebRemoteFrame\*, blink::CrossVariantMojoAssociatedRemoteblink::mojom::RemoteFrameHostInterfaceBase, blink::CrossVariantMojoAssociatedReceiverblink::mojom::RemoteFrameInterfaceBase, mojo::StructPtrblink::mojom::FrameReplicationState)+0x11c (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x1440fc4)
#9 0x00013135debc in content::RenderFrameImpl::SwapOutAndDeleteThis(bool, mojo::StructPtrblink::mojom::FrameReplicationState, base::TokenTypeblink::RemoteFrameTokenTypeMarker const&, mojo::StructPtrblink::mojom::RemoteFrameInterfacesFromBrowser, mojo::StructPtrblink::mojom::RemoteMainFrameInterfaces)+0x324 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x30d5ebc)
#10 0x00013135d3d8 in content::RenderFrameImpl::Unload(bool, mojo::StructPtrblink::mojom::FrameReplicationState, base::TokenTypeblink::RemoteFrameTokenTypeMarker const&, mojo::StructPtrblink::mojom::RemoteFrameInterfacesFromBrowser, mojo::StructPtrblink::mojom::RemoteMainFrameInterfaces)+0x370 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x30d53d8)
#11 0x00012e719054 in content::mojom::FrameStubDispatch::Accept(content::mojom::Frame\*, mojo::Message\*)+0xaa4 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x491054)
#12 0x0001012ae3e0 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*)+0x7a8 (/Users/krace/fuzz/chromium\_src/src/out/ui/libmojo\_public\_cpp\_bindings.dylib:arm64+0x223e0)
#13 0x0001012c23b4 in mojo::MessageDispatcher::Accept(mojo::Message\*)+0x2f8 (/Users/krace/fuzz/chromium\_src/src/out/ui/libmojo\_public\_cpp\_bindings.dylib:arm64+0x363b4)
#14 0x0001012b2640 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*)+0x154 (/Users/krace/fuzz/chromium\_src/src/out/ui/libmojo\_public\_cpp\_bindings.dylib:arm64+0x26640)
#15 0x000102f26458 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)+0x3dc (/Users/krace/fuzz/chromium\_src/src/out/ui/libipc.dylib:arm64+0x42458)
#16 0x000102f27e10 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped\_refptrIPC::ChannelAssociatedGroupController, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase)+0x1b8 (/Users/krace/fuzz/chromium\_src/src/out/ui/libipc.dylib:arm64+0x43e10)
#17 0x0001035e539c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x1b139c)
#18 0x000103652648 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0x864 (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x21e648)
#19 0x00010365192c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x21d92c)
#20 0x0001034bea30 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*)+0x1b0 (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x8aa30)
#21 0x000103653c0c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x36c (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x21fc0c)
#22 0x00010356c2f0 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x1382f0)
#23 0x0001313efc54 in content::RendererMain(content::MainFunctionParams)+0x6e8 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x3167c54)
#24 0x0001315d5724 in content::RunOtherNamedProcessTypeMain(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate\*)+0x3ec (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x334d724)
#25 0x0001315d7480 in content::ContentMainRunnerImpl::Run()+0x454 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x334f480)
#26 0x0001315d353c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*)+0x5c0 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x334b53c)
#27 0x0001315d3e08 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x334be08)
#28 0x000117a5afb8 in ChromeMain+0x370 (/Users/krace/fuzz/chromium\_src/src/out/ui/libchrome\_dll.dylib:arm64+0xafb8)
#29 0x000100abcce4 in main+0x254 (/Users/krace/fuzz/chromium\_src/src/out/ui/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/129.0.6653.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000ce4)
previously allocated by thread T0 here:
#0 0x000101a03ff8 in \_\_sanitizer\_finish\_switch\_fiber+0x61c (/Users/krace/fuzz/chromium\_src/src/out/ui/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x5fff8)
#1 0x000120e65220 in ReadAnythingAppController::Install(content::RenderFrame\*)+0x1bc (/Users/krace/fuzz/chromium\_src/src/out/ui/libchrome\_dll.dylib:arm64+0x9415220)
#2 0x000120dea7e0 in ChromeRenderFrameObserver::DidClearWindowObject()+0x2a8 (/Users/krace/fuzz/chromium\_src/src/out/ui/libchrome\_dll.dylib:arm64+0x939a7e0)
#3 0x00013137fef0 in content::RenderFrameImpl::DidClearWindowObject()+0x57c (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x30f7ef0)
#4 0x000159934d18 in blink::LocalFrameClientImpl::DispatchDidClearWindowObjectInMainWorld(v8::Isolate\*, v8::MicrotaskQueue\*)+0x198 (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x1434d18)
#5 0x00015ab97100 in blink::FrameLoader::DispatchDidClearWindowObjectInMainWorld()+0x1e4 (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x2697100)
#6 0x00015853e5d8 in blink::LocalWindowProxy::Initialize()+0x106c (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x3e5d8)
#7 0x000158696c54 in blink::LocalWindowProxyManager::UpdateDocument()+0xfc (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x196c54)
#8 0x00015ab35038 in blink::DocumentLoader::CreateParserPostCommit()+0x944 (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x2635038)
#9 0x00015ab3393c in blink::DocumentLoader::StartLoadingResponse()+0x240 (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x263393c)
#10 0x00015ab3e8d0 in blink::DocumentLoader::CommitNavigation()+0x18e4 (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x263e8d0)
#11 0x00015ab87fcc in blink::FrameLoader::CommitDocumentLoader(blink::DocumentLoader\*, blink::HistoryItem\*, blink::CommitReason)+0x4bc (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x2687fcc)
#12 0x00015ab91484 in blink::FrameLoader::CommitNavigation(std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>, std::\_\_Cr::unique\_ptr<blink::WebDocumentLoader::ExtraData, std::\_\_Cr::default\_deleteblink::WebDocumentLoader::ExtraData>, blink::CommitReason)+0x1328 (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x2691484)
#13 0x0001599aa37c in blink::WebLocalFrameImpl::CommitNavigation(std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>, std::\_\_Cr::unique\_ptr<blink::WebDocumentLoader::ExtraData, std::\_\_Cr::default\_deleteblink::WebDocumentLoader::ExtraData>)+0x39c (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x14aa37c)
#14 0x00013136a644 in content::RenderFrameImpl::CommitNavigationWithParams(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::\_\_Cr::unique\_ptr<content::DocumentState, std::\_\_Cr::default\_deletecontent::DocumentState>, std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>)+0xda8 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x30e2644)
#15 0x0001313afc78 in void base::internal::DecayedFunctorTraits<void (content::RenderFrameImpl::)(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::\_\_Cr::unique\_ptr<content::DocumentState, std::\_\_Cr::default\_deletecontent::DocumentState>, std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>), base::WeakPtrcontent::RenderFrameImpl&&, mojo::StructPtrblink::mojom::CommonNavigationParams&&, mojo::StructPtrblink::mojom::CommitNavigationParams&&, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>&&, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>&&, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo&&, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient&&, mojo::PendingRemotenetwork::mojom::URLLoaderFactory&&, mojo::PendingRemotenetwork::mojom::URLLoaderFactory&&, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory&&, mojo::PendingRemoteblink::mojom::CodeCacheHost&&, mojo::PendingRemoteblink::mojom::CodeCacheHost&&, mojo::StructPtrcontent::mojom::CookieManagerInfo&&, mojo::StructPtrcontent::mojom::StorageInfo&&, std::\_\_Cr::unique\_ptr<content::DocumentState, std::\_\_Cr::default\_deletecontent::DocumentState>&&>::Invoke<void (content::RenderFrameImpl::)(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::\_\_Cr::unique\_ptr<content::DocumentState, std::\_\_Cr::default\_deletecontent::DocumentState>, std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>), base::WeakPtrcontent::RenderFrameImpl const&, mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::\_\_Cr::unique\_ptr<content::DocumentState, std::\_\_Cr::default\_deletecontent::DocumentState>, std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>>(void (content::RenderFrameImpl::)(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::\_\_Cr::unique\_ptr<content::DocumentState, std::\_\_Cr::default\_deletecontent::DocumentState>, std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>), base::WeakPtrcontent::RenderFrameImpl const&, mojo::StructPtrblink::mojom::CommonNavigationParams&&, mojo::StructPtrblink::mojom::CommitNavigationParams&&, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>&&, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>&&, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo&&, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient&&, mojo::PendingRemotenetwork::mojom::URLLoaderFactory&&, mojo::PendingRemotenetwork::mojom::URLLoaderFactory&&, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory&&, mojo::PendingRemoteblink::mojom::CodeCacheHost&&, mojo::PendingRemoteblink::mojom::CodeCacheHost&&, mojo::StructPtrcontent::mojom::CookieManagerInfo&&, mojo::StructPtrcontent::mojom::StorageInfo&&, std::\_\_Cr::unique\_ptr<content::DocumentState, std::\_\_Cr::default\_deletecontent::DocumentState>&&, std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>&&)+0x3a0 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x3127c78)#16 0x0001313af82c in base::internal::Invoker<base::internal::FunctorTraits<void (content::RenderFrameImpl::&&)(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::\_\_Cr::unique\_ptr<content::DocumentState, std::\_\_Cr::default\_deletecontent::DocumentState>, std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>), base::WeakPtrcontent::RenderFrameImpl&&, mojo::StructPtrblink::mojom::CommonNavigationParams&&, mojo::StructPtrblink::mojom::CommitNavigationParams&&, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>&&, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>&&, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo&&, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient&&, mojo::PendingRemotenetwork::mojom::URLLoaderFactory&&, mojo::PendingRemotenetwork::mojom::URLLoaderFactory&&, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory&&, mojo::PendingRemoteblink::mojom::CodeCacheHost&&, mojo::PendingRemoteblink::mojom::CodeCacheHost&&, mojo::StructPtrcontent::mojom::CookieManagerInfo&&, mojo::StructPtrcontent::mojom::StorageInfo&&, std::\_\_Cr::unique\_ptr<content::DocumentState, std::\_\_Cr::default\_deletecontent::DocumentState>&&>, base::internal::BindState<true, true, false, void (content::RenderFrameImpl::)(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::\_\_Cr::unique\_ptr<content::DocumentState, std::\_\_Cr::default\_deletecontent::DocumentState>, std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>), base::WeakPtrcontent::RenderFrameImpl, mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::\_\_Cr::unique\_ptr<content::DocumentState, std::\_\_Cr::default\_deletecontent::DocumentState>>, void (std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>)>::RunOnce(base::internal::BindStateBase, std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>&&)+0x164 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x312782c)
#17 0x00013136b854 in base::OnceCallback<void (std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>)>::Run(std::\_\_Cr::unique\_ptr<blink::WebNavigationParams, std::\_\_Cr::default\_deleteblink::WebNavigationParams>) &&+0x160 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x30e3854)
#18 0x0001313671bc in content::RenderFrameImpl::CommitNavigation(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, mojo::StructPtrnetwork::mojom::URLResponseHead, mojo::ScopedHandleBasemojo::DataPipeConsumerHandle, mojo::StructPtrnetwork::mojom::URLLoaderClientEndpoints, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, base::TokenTypeblink::DocumentTokenTypeMarker const&, base::UnguessableToken const&, base::Uuid const&, std::\_\_Cr::optional<std::\_\_Cr::vector<blink::ParsedPermissionsPolicyDeclaration, std::\_\_Cr::allocatorblink::ParsedPermissionsPolicyDeclaration>> const&, mojo::StructPtrblink::mojom::PolicyContainer, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, base::OnceCallback<void (mojo::StructPtrcontent::mojom::DidCommitProvisionalLoadParams, mojo::StructPtrcontent::mojom::DidCommitProvisionalLoadInterfaceParams)>)+0x1650 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x30df1bc)
#19 0x00013134b990 in content::NavigationClient::CommitNavigation(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, mojo::StructPtrnetwork::mojom::URLResponseHead, mojo::ScopedHandleBasemojo::DataPipeConsumerHandle, mojo::StructPtrnetwork::mojom::URLLoaderClientEndpoints, std::\_\_Cr::unique\_ptr<blink::PendingURLLoaderFactoryBundle, std::\_\_Cr::default\_deleteblink::PendingURLLoaderFactoryBundle>, std::\_\_Cr::optional<std::\_\_Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::\_\_Cr::allocator[mojo::StructPtrblink::mojom::TransferrableURLLoader](javascript:void(0);)>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, base::TokenTypeblink::DocumentTokenTypeMarker const&, base::UnguessableToken const&, base::Uuid const&, std::\_\_Cr::optional<std::\_\_Cr::vector<blink::ParsedPermissionsPolicyDeclaration, std::\_\_Cr::allocatorblink::ParsedPermissionsPolicyDeclaration>> const&, mojo::StructPtrblink::mojom::PolicyContainer, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, base::OnceCallback<void (mojo::StructPtrcontent::mojom::DidCommitProvisionalLoadParams, mojo::StructPtrcontent::mojom::DidCommitProvisionalLoadInterfaceParams)>)+0x4e4 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x30c3990)
#20 0x00012e78f0d8 in content::mojom::NavigationClientStubDispatch::AcceptWithResponder(content::mojom::NavigationClient\*, mojo::Message\*, std::\_\_Cr::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_Cr::default\_deletemojo::MessageReceiverWithStatus>)+0x17f0 (/Users/krace/fuzz/chromium\_src/src/out/ui/libcontent.dylib:arm64+0x5070d8)
#21 0x0001012ae39c in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*)+0x764 (/Users/krace/fuzz/chromium\_src/src/out/ui/libmojo\_public\_cpp\_bindings.dylib:arm64+0x2239c)
#22 0x0001012c23b4 in mojo::MessageDispatcher::Accept(mojo::Message\*)+0x2f8 (/Users/krace/fuzz/chromium\_src/src/out/ui/libmojo\_public\_cpp\_bindings.dylib:arm64+0x363b4)
#23 0x0001012b2640 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*)+0x154 (/Users/krace/fuzz/chromium\_src/src/out/ui/libmojo\_public\_cpp\_bindings.dylib:arm64+0x26640)
#24 0x000102f26458 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)+0x3dc (/Users/krace/fuzz/chromium\_src/src/out/ui/libipc.dylib:arm64+0x42458)
#25 0x000102f27e10 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped\_refptrIPC::ChannelAssociatedGroupController, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase)+0x1b8 (/Users/krace/fuzz/chromium\_src/src/out/ui/libipc.dylib:arm64+0x43e10)
#26 0x0001035e539c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x1b139c)
#27 0x000103652648 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0x864 (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x21e648)
#28 0x00010365192c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x21d92c)
#29 0x0001034bea30 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*)+0x1b0 (/Users/krace/fuzz/chromium\_src/src/out/ui/libbase.dylib:arm64+0x8aa30)
SUMMARY: AddressSanitizer: heap-use-after-free (/Users/krace/fuzz/chromium\_src/src/out/ui/libgin.dylib:arm64+0x29914) in gin::WrappableBase::SecondWeakCallback(v8::WeakCallbackInfogin::WrappableBase const&)+0x68
Shadow bytes around the buggy address:
0x61a00000a000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a100: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
0x61a00000a180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x61a00000a200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x61a00000a280: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==2516==ADDITIONAL INFO
==2516==Note: Please include this section with the ASan report.
Task trace:
#0 0x00013dc57cd4 in gin::V8ForegroundTaskRunner::PostTaskImpl(std::\_\_Cr::unique\_ptr<v8::Task, std::\_\_Cr::default\_deletev8::Task>, v8::SourceLocation const&)+0xe0 (/Users/krace/fuzz/chromium\_src/src/out/ui/libgin.dylib:arm64+0x1fcd4)
#1 0x00015b0e2f9c in blink::HTMLParserScriptRunner::PendingScriptFinished(blink::PendingScript\*)+0x1fc (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x2be2f9c)
#2 0x00015b10f868 in blink::ModuleMap::Entry::DispatchFinishedNotificationAsync(blink::SingleModuleClient\*)+0x180 (/Users/krace/fuzz/chromium\_src/src/out/ui/libblink\_core.dylib:arm64+0x2c0f868)
#3 0x00010143cfc4 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x248 (/Users/krace/fuzz/chromium\_src/src/out/ui/libmojo\_public\_system\_cpp.dylib:arm64+0x18fc4)
Command line: /Users/krace/fuzz/chromium\_src/src/out/ui/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/129.0.6653.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer) --type=renderer --user-data-dir=./tmp132x3xw1 --enable-dinosaur-easter-egg-alt-images --enable-chrome-cart --no-subproc-heap-profiling --enable-blink-features=MojoJS --lang=zh-CN --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=125 --time-ticks-at-unix-epoch=-1722530498025665 --launch-time-ticks=1102700588410 --shared-files --metrics-shmem-handle=1752395122,r,2127661289661155484,5427033152330412745,2097152 --field-trial-handle=1718379636,r,15965957977100149794,5448591807746138091,262144 --variations-seed-version --seatbelt-client=152
MiraclePtr Status: NOT PROTECTED
No raw\_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw\_ptr.md for details.
==2516==END OF ADDITIONAL INFO
==2516==ABORTING
Received signal 6
[0x0001037800a4]
[0x00010373c2fc]
[0x00010377fbac]
[0x00018fdeb584]
[0x00018fdbac20]
[0x00018fcc7a30]
[0x000101a1a8d4]
[0x000101a19f14]
[0x0001019fd298]
[0x0001019fc558]
[0x0001019fda6c]
[0x00013dc61918]
[0x000148412920]
[0x00013dc586ac]
[0x0001035e53a0]
[0x00010365264c]
[0x000103651930]
[0x0001034bea34]
[0x000103653c10]
[0x00010356c2f4]
[0x0001313efc58]
[0x0001315d5728]
[0x0001315d7484]
[0x0001315d3540]
[0x0001315d3e0c]
[0x000117a5afbc]
[0x000100abcce8]
[0x00018fa320e0]
[end of stack trace]

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Timeline

### me...@gmail.com (2024-08-16)

More readable Asan log

```
=================================================================
==2516==ERROR: AddressSanitizer: heap-use-after-free on address 0x61a00000a290 at pc 0x00013dc61918 bp 0x00016f341600 sp 0x00016f3415f8
READ of size 8 at 0x61a00000a290 thread T0
==2516==WARNING: invalid path to external symbolizer!
==2516==WARNING: Failed to use and restart external symbolizer!
#0 0x00013dc61914 in gin::WrappableBase::SecondWeakCallback(v8::WeakCallbackInfogin::WrappableBase const&)+0x68 (/Users/krace/fuzz/chromium_src/src/out/ui/libgin.dylib:arm64+0x29914)
#1 0x00014841291c in v8::internal::GlobalHandles::InvokeSecondPassPhantomCallbacks()+0x394 (/Users/krace/fuzz/chromium_src/src/out/ui/libv8.dylib:arm64+0x6e691c)
#2 0x00013dc586a8 in base::internal::Invoker<base::internal::FunctorTraits<void (v8::Task::&&)(), std::__Cr::unique_ptr<v8::Task, std::__Cr::default_deletev8::Task>&&>, base::internal::BindState<true, true, false, void (v8::Task::)(), std::__Cr::unique_ptr<v8::Task, std::__Cr::default_deletev8::Task>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x11c (/Users/krace/fuzz/chromium_src/src/out/ui/libgin.dylib:arm64+0x206a8)
#3 0x0001035e539c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x1b139c)
#4 0x000103652648 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x864 (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x21e648)
#5 0x00010365192c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x21d92c)
#6 0x0001034bea30 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x8aa30)
#7 0x000103653c0c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x36c (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x21fc0c)
#8 0x00010356c2f0 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x1382f0)
#9 0x0001313efc54 in content::RendererMain(content::MainFunctionParams)+0x6e8 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x3167c54)
#10 0x0001315d5724 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x3ec (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x334d724)
#11 0x0001315d7480 in content::ContentMainRunnerImpl::Run()+0x454 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x334f480)
#12 0x0001315d353c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x5c0 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x334b53c)
#13 0x0001315d3e08 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x334be08)
#14 0x000117a5afb8 in ChromeMain+0x370 (/Users/krace/fuzz/chromium_src/src/out/ui/libchrome_dll.dylib:arm64+0xafb8)
#15 0x000100abcce4 in main+0x254 (/Users/krace/fuzz/chromium_src/src/out/ui/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/129.0.6653.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000ce4)
#16 0x00018fa320dc  (<unknown module>)
#17 0x8353fffffffffffc  (<unknown module>)
0x61a00000a290 is located 16 bytes inside of 1176-byte region [0x61a00000a280,0x61a00000a718)
freed by thread T0 here:
#0 0x000101a04400 in __sanitizer_finish_switch_fiber+0xa24 (/Users/krace/fuzz/chromium_src/src/out/ui/libclang_rt.asan_osx_dynamic.dylib:arm64+0x60400)
#1 0x000131357cd8 in content::RenderFrameImpl::~RenderFrameImpl()+0x4f8 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x30cfcd8)
#2 0x0001313592bc in content::RenderFrameImpl::~RenderFrameImpl()+0x8 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x30d12bc)
#3 0x000131378ea8 in content::RenderFrameImpl::FrameDetached()+0x59c (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x30f0ea8)
#4 0x0001599360e8 in blink::LocalFrameClientImpl::Detached(blink::FrameDetachType)+0x120 (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x14360e8)
#5 0x00015972c720 in blink::Frame::Detach(blink::FrameDetachType)+0x3b4 (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x122c720)
#6 0x000159732d20 in blink::Frame::SwapImpl(blink::WebFrame*, mojo::PendingAssociatedRemoteblink::mojom::blink::RemoteFrameHost, mojo::PendingAssociatedReceiverblink::mojom::blink::RemoteFrame)+0x3b0 (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x1232d20)
#7 0x000159734b90 in blink::Frame::Swap(blink::WebRemoteFrame*, mojo::PendingAssociatedRemoteblink::mojom::blink::RemoteFrameHost, mojo::PendingAssociatedReceiverblink::mojom::blink::RemoteFrame)+0x11c (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x1234b90)
#8 0x000159940fc4 in blink::WebFrame::Swap(blink::WebRemoteFrame*, blink::CrossVariantMojoAssociatedRemoteblink::mojom::RemoteFrameHostInterfaceBase, blink::CrossVariantMojoAssociatedReceiverblink::mojom::RemoteFrameInterfaceBase, mojo::StructPtrblink::mojom::FrameReplicationState)+0x11c (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x1440fc4)
#9 0x00013135debc in content::RenderFrameImpl::SwapOutAndDeleteThis(bool, mojo::StructPtrblink::mojom::FrameReplicationState, base::TokenTypeblink::RemoteFrameTokenTypeMarker const&, mojo::StructPtrblink::mojom::RemoteFrameInterfacesFromBrowser, mojo::StructPtrblink::mojom::RemoteMainFrameInterfaces)+0x324 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x30d5ebc)
#10 0x00013135d3d8 in content::RenderFrameImpl::Unload(bool, mojo::StructPtrblink::mojom::FrameReplicationState, base::TokenTypeblink::RemoteFrameTokenTypeMarker const&, mojo::StructPtrblink::mojom::RemoteFrameInterfacesFromBrowser, mojo::StructPtrblink::mojom::RemoteMainFrameInterfaces)+0x370 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x30d53d8)
#11 0x00012e719054 in content::mojom::FrameStubDispatch::Accept(content::mojom::Frame*, mojo::Message*)+0xaa4 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x491054)
#12 0x0001012ae3e0 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x7a8 (/Users/krace/fuzz/chromium_src/src/out/ui/libmojo_public_cpp_bindings.dylib:arm64+0x223e0)
#13 0x0001012c23b4 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f8 (/Users/krace/fuzz/chromium_src/src/out/ui/libmojo_public_cpp_bindings.dylib:arm64+0x363b4)
#14 0x0001012b2640 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x154 (/Users/krace/fuzz/chromium_src/src/out/ui/libmojo_public_cpp_bindings.dylib:arm64+0x26640)
#15 0x000102f26458 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)+0x3dc (/Users/krace/fuzz/chromium_src/src/out/ui/libipc.dylib:arm64+0x42458)
#16 0x000102f27e10 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptrIPC::ChannelAssociatedGroupController, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase)+0x1b8 (/Users/krace/fuzz/chromium_src/src/out/ui/libipc.dylib:arm64+0x43e10)
#17 0x0001035e539c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x1b139c)
#18 0x000103652648 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x864 (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x21e648)
#19 0x00010365192c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x21d92c)
#20 0x0001034bea30 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x8aa30)
#21 0x000103653c0c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x36c (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x21fc0c)
#22 0x00010356c2f0 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x1382f0)
#23 0x0001313efc54 in content::RendererMain(content::MainFunctionParams)+0x6e8 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x3167c54)
#24 0x0001315d5724 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x3ec (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x334d724)
#25 0x0001315d7480 in content::ContentMainRunnerImpl::Run()+0x454 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x334f480)
#26 0x0001315d353c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x5c0 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x334b53c)
#27 0x0001315d3e08 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x334be08)
#28 0x000117a5afb8 in ChromeMain+0x370 (/Users/krace/fuzz/chromium_src/src/out/ui/libchrome_dll.dylib:arm64+0xafb8)
#29 0x000100abcce4 in main+0x254 (/Users/krace/fuzz/chromium_src/src/out/ui/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/129.0.6653.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000ce4)
previously allocated by thread T0 here:
#0 0x000101a03ff8 in __sanitizer_finish_switch_fiber+0x61c (/Users/krace/fuzz/chromium_src/src/out/ui/libclang_rt.asan_osx_dynamic.dylib:arm64+0x5fff8)
#1 0x000120e65220 in ReadAnythingAppController::Install(content::RenderFrame*)+0x1bc (/Users/krace/fuzz/chromium_src/src/out/ui/libchrome_dll.dylib:arm64+0x9415220)
#2 0x000120dea7e0 in ChromeRenderFrameObserver::DidClearWindowObject()+0x2a8 (/Users/krace/fuzz/chromium_src/src/out/ui/libchrome_dll.dylib:arm64+0x939a7e0)
#3 0x00013137fef0 in content::RenderFrameImpl::DidClearWindowObject()+0x57c (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x30f7ef0)
#4 0x000159934d18 in blink::LocalFrameClientImpl::DispatchDidClearWindowObjectInMainWorld(v8::Isolate*, v8::MicrotaskQueue*)+0x198 (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x1434d18)
#5 0x00015ab97100 in blink::FrameLoader::DispatchDidClearWindowObjectInMainWorld()+0x1e4 (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x2697100)
#6 0x00015853e5d8 in blink::LocalWindowProxy::Initialize()+0x106c (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x3e5d8)
#7 0x000158696c54 in blink::LocalWindowProxyManager::UpdateDocument()+0xfc (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x196c54)
#8 0x00015ab35038 in blink::DocumentLoader::CreateParserPostCommit()+0x944 (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x2635038)
#9 0x00015ab3393c in blink::DocumentLoader::StartLoadingResponse()+0x240 (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x263393c)
#10 0x00015ab3e8d0 in blink::DocumentLoader::CommitNavigation()+0x18e4 (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x263e8d0)
#11 0x00015ab87fcc in blink::FrameLoader::CommitDocumentLoader(blink::DocumentLoader*, blink::HistoryItem*, blink::CommitReason)+0x4bc (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x2687fcc)
#12 0x00015ab91484 in blink::FrameLoader::CommitNavigation(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>, std::__Cr::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__Cr::default_deleteblink::WebDocumentLoader::ExtraData>, blink::CommitReason)+0x1328 (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x2691484)
#13 0x0001599aa37c in blink::WebLocalFrameImpl::CommitNavigation(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>, std::__Cr::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__Cr::default_deleteblink::WebDocumentLoader::ExtraData>)+0x39c (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x14aa37c)
#14 0x00013136a644 in content::RenderFrameImpl::CommitNavigationWithParams(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_deletecontent::DocumentState>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>)+0xda8 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x30e2644)
#15 0x0001313afc78 in void base::internal::DecayedFunctorTraits<void (content::RenderFrameImpl::)(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_deletecontent::DocumentState>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>), base::WeakPtrcontent::RenderFrameImpl&&, mojo::StructPtrblink::mojom::CommonNavigationParams&&, mojo::StructPtrblink::mojom::CommitNavigationParams&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>&&, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo&&, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient&&, mojo::PendingRemotenetwork::mojom::URLLoaderFactory&&, mojo::PendingRemotenetwork::mojom::URLLoaderFactory&&, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory&&, mojo::PendingRemoteblink::mojom::CodeCacheHost&&, mojo::PendingRemoteblink::mojom::CodeCacheHost&&, mojo::StructPtrcontent::mojom::CookieManagerInfo&&, mojo::StructPtrcontent::mojom::StorageInfo&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_deletecontent::DocumentState>&&>::Invoke<void (content::RenderFrameImpl::)(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_deletecontent::DocumentState>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>), base::WeakPtrcontent::RenderFrameImpl const&, mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_deletecontent::DocumentState>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>>(void (content::RenderFrameImpl::)(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_deletecontent::DocumentState>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>), base::WeakPtrcontent::RenderFrameImpl const&, mojo::StructPtrblink::mojom::CommonNavigationParams&&, mojo::StructPtrblink::mojom::CommitNavigationParams&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>&&, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo&&, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient&&, mojo::PendingRemotenetwork::mojom::URLLoaderFactory&&, mojo::PendingRemotenetwork::mojom::URLLoaderFactory&&, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory&&, mojo::PendingRemoteblink::mojom::CodeCacheHost&&, mojo::PendingRemoteblink::mojom::CodeCacheHost&&, mojo::StructPtrcontent::mojom::CookieManagerInfo&&, mojo::StructPtrcontent::mojom::StorageInfo&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_deletecontent::DocumentState>&&, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>&&)+0x3a0 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x3127c78)#16 0x0001313af82c in base::internal::Invoker<base::internal::FunctorTraits<void (content::RenderFrameImpl::&&)(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_deletecontent::DocumentState>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>), base::WeakPtrcontent::RenderFrameImpl&&, mojo::StructPtrblink::mojom::CommonNavigationParams&&, mojo::StructPtrblink::mojom::CommitNavigationParams&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>&&, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo&&, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient&&, mojo::PendingRemotenetwork::mojom::URLLoaderFactory&&, mojo::PendingRemotenetwork::mojom::URLLoaderFactory&&, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory&&, mojo::PendingRemoteblink::mojom::CodeCacheHost&&, mojo::PendingRemoteblink::mojom::CodeCacheHost&&, mojo::StructPtrcontent::mojom::CookieManagerInfo&&, mojo::StructPtrcontent::mojom::StorageInfo&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_deletecontent::DocumentState>&&>, base::internal::BindState<true, true, false, void (content::RenderFrameImpl::)(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_deletecontent::DocumentState>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>), base::WeakPtrcontent::RenderFrameImpl, mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_deletecontent::DocumentState>>, void (std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>)>::RunOnce(base::internal::BindStateBase, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>&&)+0x164 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x312782c)
#17 0x00013136b854 in base::OnceCallback<void (std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>)>::Run(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_deleteblink::WebNavigationParams>) &&+0x160 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x30e3854)
#18 0x0001313671bc in content::RenderFrameImpl::CommitNavigation(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, mojo::StructPtrnetwork::mojom::URLResponseHead, mojo::ScopedHandleBasemojo::DataPipeConsumerHandle, mojo::StructPtrnetwork::mojom::URLLoaderClientEndpoints, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, base::TokenTypeblink::DocumentTokenTypeMarker const&, base::UnguessableToken const&, base::Uuid const&, std::__Cr::optional<std::__Cr::vector<blink::ParsedPermissionsPolicyDeclaration, std::__Cr::allocatorblink::ParsedPermissionsPolicyDeclaration>> const&, mojo::StructPtrblink::mojom::PolicyContainer, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, base::OnceCallback<void (mojo::StructPtrcontent::mojom::DidCommitProvisionalLoadParams, mojo::StructPtrcontent::mojom::DidCommitProvisionalLoadInterfaceParams)>)+0x1650 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x30df1bc)
#19 0x00013134b990 in content::NavigationClient::CommitNavigation(mojo::StructPtrblink::mojom::CommonNavigationParams, mojo::StructPtrblink::mojom::CommitNavigationParams, mojo::StructPtrnetwork::mojom::URLResponseHead, mojo::ScopedHandleBasemojo::DataPipeConsumerHandle, mojo::StructPtrnetwork::mojom::URLLoaderClientEndpoints, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_deleteblink::PendingURLLoaderFactoryBundle>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtrblink::mojom::TransferrableURLLoader, std::__Cr::allocator<mojo::StructPtrblink::mojom::TransferrableURLLoader>>>, mojo::StructPtrblink::mojom::ControllerServiceWorkerInfo, mojo::StructPtrblink::mojom::ServiceWorkerContainerInfoForClient, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingRemotenetwork::mojom::URLLoaderFactory, mojo::PendingAssociatedRemoteblink::mojom::FetchLaterLoaderFactory, base::TokenTypeblink::DocumentTokenTypeMarker const&, base::UnguessableToken const&, base::Uuid const&, std::__Cr::optional<std::__Cr::vector<blink::ParsedPermissionsPolicyDeclaration, std::__Cr::allocatorblink::ParsedPermissionsPolicyDeclaration>> const&, mojo::StructPtrblink::mojom::PolicyContainer, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::PendingRemoteblink::mojom::CodeCacheHost, mojo::StructPtrcontent::mojom::CookieManagerInfo, mojo::StructPtrcontent::mojom::StorageInfo, base::OnceCallback<void (mojo::StructPtrcontent::mojom::DidCommitProvisionalLoadParams, mojo::StructPtrcontent::mojom::DidCommitProvisionalLoadInterfaceParams)>)+0x4e4 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x30c3990)
#20 0x00012e78f0d8 in content::mojom::NavigationClientStubDispatch::AcceptWithResponder(content::mojom::NavigationClient*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_deletemojo::MessageReceiverWithStatus>)+0x17f0 (/Users/krace/fuzz/chromium_src/src/out/ui/libcontent.dylib:arm64+0x5070d8)
#21 0x0001012ae39c in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x764 (/Users/krace/fuzz/chromium_src/src/out/ui/libmojo_public_cpp_bindings.dylib:arm64+0x2239c)
#22 0x0001012c23b4 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f8 (/Users/krace/fuzz/chromium_src/src/out/ui/libmojo_public_cpp_bindings.dylib:arm64+0x363b4)
#23 0x0001012b2640 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x154 (/Users/krace/fuzz/chromium_src/src/out/ui/libmojo_public_cpp_bindings.dylib:arm64+0x26640)
#24 0x000102f26458 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)+0x3dc (/Users/krace/fuzz/chromium_src/src/out/ui/libipc.dylib:arm64+0x42458)
#25 0x000102f27e10 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptrIPC::ChannelAssociatedGroupController, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase)+0x1b8 (/Users/krace/fuzz/chromium_src/src/out/ui/libipc.dylib:arm64+0x43e10)
#26 0x0001035e539c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x1b139c)
#27 0x000103652648 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x864 (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x21e648)
#28 0x00010365192c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x21d92c)
#29 0x0001034bea30 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/krace/fuzz/chromium_src/src/out/ui/libbase.dylib:arm64+0x8aa30)
SUMMARY: AddressSanitizer: heap-use-after-free (/Users/krace/fuzz/chromium_src/src/out/ui/libgin.dylib:arm64+0x29914) in gin::WrappableBase::SecondWeakCallback(v8::WeakCallbackInfogin::WrappableBase const&)+0x68
Shadow bytes around the buggy address:
0x61a00000a000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a100: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
0x61a00000a180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x61a00000a200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x61a00000a280: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x61a00000a500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==2516==ADDITIONAL INFO
==2516==Note: Please include this section with the ASan report.
Task trace:
#0 0x00013dc57cd4 in gin::V8ForegroundTaskRunner::PostTaskImpl(std::__Cr::unique_ptr<v8::Task, std::__Cr::default_deletev8::Task>, v8::SourceLocation const&)+0xe0 (/Users/krace/fuzz/chromium_src/src/out/ui/libgin.dylib:arm64+0x1fcd4)
#1 0x00015b0e2f9c in blink::HTMLParserScriptRunner::PendingScriptFinished(blink::PendingScript*)+0x1fc (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x2be2f9c)
#2 0x00015b10f868 in blink::ModuleMap::Entry::DispatchFinishedNotificationAsync(blink::SingleModuleClient*)+0x180 (/Users/krace/fuzz/chromium_src/src/out/ui/libblink_core.dylib:arm64+0x2c0f868)
#3 0x00010143cfc4 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x248 (/Users/krace/fuzz/chromium_src/src/out/ui/libmojo_public_system_cpp.dylib:arm64+0x18fc4)
Command line: /Users/krace/fuzz/chromium_src/src/out/ui/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/129.0.6653.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer) --type=renderer --user-data-dir=./tmp132x3xw1 --enable-dinosaur-easter-egg-alt-images --enable-chrome-cart --no-subproc-heap-profiling --enable-blink-features=MojoJS --lang=zh-CN --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=125 --time-ticks-at-unix-epoch=-1722530498025665 --launch-time-ticks=1102700588410 --shared-files --metrics-shmem-handle=1752395122,r,2127661289661155484,5427033152330412745,2097152 --field-trial-handle=1718379636,r,15965957977100149794,5448591807746138091,262144 --variations-seed-version --seatbelt-client=152
MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.
==2516==END OF ADDITIONAL INFO
==2516==ABORTING
Received signal 6
[0x0001037800a4]
[0x00010373c2fc]
[0x00010377fbac]
[0x00018fdeb584]
[0x00018fdbac20]
[0x00018fcc7a30]
[0x000101a1a8d4]
[0x000101a19f14]
[0x0001019fd298]
[0x0001019fc558]
[0x0001019fda6c]
[0x00013dc61918]
[0x000148412920]
[0x00013dc586ac]
[0x0001035e53a0]
[0x00010365264c]
[0x000103651930]
[0x0001034bea34]
[0x000103653c10]
[0x00010356c2f4]
[0x0001313efc58]
[0x0001315d5728]
[0x0001315d7484]
[0x0001315d3540]
[0x0001315d3e0c]
[0x000117a5afbc]
[0x000100abcce8]
[0x00018fa320e0]
[end of stack trace]

```

### pe...@google.com (2024-08-16)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### am...@chromium.org (2024-08-16)

Thank you for the report, Krace.

While this isn't BRP protected, there is the precondition of the compromised renderer + screen\_ai, and a fair amount of user gesture to trigger. As such, I've set this as sev-medium / S2.

Assigning to jocelyntran@ who worked on [crbug.com/41490491](https://crbug.com/41490491)

### pe...@google.com (2024-08-16)

Setting milestone because of s2 severity.

### ja...@chromium.org (2024-09-12)

Hi abigailbklein@, could you take a look and comment about any possible fixes? Thanks!

### pe...@google.com (2024-09-13)

abigailbklein: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ab...@google.com (2024-09-26)

I see the issue but I'm not quite sure how to address it. It seems that while ReadAnythingAppController::Install is running, the render frame was deleted. However, I don't understand the code in Install that creates the v8 context well enough to understand at what point this is failing. Adding a few gin owners from <https://source.chromium.org/chromium/chromium/src/+/main:gin/OWNERS> to see if they can weigh in.

### cb...@chromium.org (2024-10-07)

@bi...@chromium.org could you have a look. If I'm not mistaken `ReadAnythingAppController::OnDestruct()` should be an empty implementation, but currently frees the object [too early](https://source.chromium.org/chromium/chromium/src/+/main:chrome/renderer/accessibility/read_anything_app_controller.cc;l=443;drc=4b44bd63028a5aa82976dc4d7ed51cb78cbc6891;bpv=1;bpt=1). causing a UAF.

### ap...@google.com (2024-10-09)

Project: chromium/src  

Branch: main  

Author: Abigail Klein <[abigailbklein@google.com](mailto:abigailbklein@google.com)>  

Link:      <https://chromium-review.googlesource.com/5916610>

Replace base::unretained with weak\_ptr.

---


Expand for full commit details
```
Replace base::unretained with weak_ptr.

Fixed: 360274917
Change-Id: I510eee7f77422e6004c1f2d7f3b9f92203962d4a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5916610
Reviewed-by: Tzarial <zork@chromium.org>
Commit-Queue: Abigail Klein <abigailbklein@google.com>
Cr-Commit-Position: refs/heads/main@{#1366297}

```

---

Files:

- M `chrome/renderer/accessibility/read_anything_app_controller.cc`
- M `chrome/renderer/accessibility/read_anything_app_controller.h`

---

Hash: 4bef2016c9a03d3d6db85b72f068bb3603e4850c  

Date:  Wed Oct 09 17:36:05 2024


---

### me...@gmail.com (2024-11-01)

Hello, any update about the reward?

### am...@chromium.org (2024-11-04)

There was no VRP panel session last week due to some of us being OOO. This will be reviewed at a future VRP panel session.

### sp...@google.com (2024-11-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of heavily mitigated memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-15)

Congratulations Krace! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2025-01-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/360274917)*
