# Heap-use-after-free in blink::WorkerOrWorkletGlobalScope::CountUse

| Field | Value |
|-------|-------|
| **Issue ID** | [40058806](https://issues.chromium.org/issues/40058806) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Workers |
| **Platforms** | Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | nh...@chromium.org |
| **Created** | 2022-02-17 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6663752820523008

Fuzzer: b0ring_webidl_fuzzer
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x129d5a1be9e0
Crash State:
  blink::WorkerOrWorkletGlobalScope::CountUse
  base::internal::Invoker<base::internal::BindState<`lambda at ../../third_party/b
  blink::mojom::blink::BlobURLStore_ResolveAsURLLoaderFactory_ForwardToCallback::A
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=972289:972290

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6663752820523008

Issue filed automatically.



## Timeline

### cl...@chromium.org (2022-02-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-02-17)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Workers]

### cl...@chromium.org (2022-02-17)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/f7e0f2d08b8c7ec55baf8202903d865e692fb23e ([CrOSCellular] Fix non-active eSIM profiles after powerwash.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### [Deleted User] (2022-02-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### az...@chromium.org (2022-02-17)

[Empty comment from Monorail migration]

### az...@chromium.org (2022-02-18)

This does not seem related to change in https://chromium.googlesource.com/chromium/src/+/f7e0f2d08b8c7ec55baf8202903d865e692fb23e.
That CL changes ChromeOS only Cellular networking code. However the fuzzer results are for windows_asan_chrome job on Windows platform . The crash back-traces also seem unrelated to anything from the CL.

I suspect this has been wrongly labelled. Please help find a different owner to take a look.

### kh...@chromium.org (2022-02-18)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-02-24)

Oh no, this is a high sev security bug and needs an owner. If our fuzzers can find it, their fuzzers will too.

WorkerOrWorkletGlobalScope holds a weak (raw) reference to WorkerReportingProxy, which was destroyed with the frame:
    #1 0x7ffee6eca8d0 in blink::MainThreadWorkletReportingProxy::~MainThreadWorkletReportingProxy third_party/blink/renderer/core/workers/main_thread_worklet_reporting_proxy.h:19
    #2 0x7ffee6ec09eb in blink::Worklet::ContextDestroyed third_party/blink/renderer/core/workers/worklet.cc:101
    #3 0x7ffedb4b53e5 in blink::ContextLifecycleObserver::NotifyContextDestroyed third_party/blink/renderer/platform/context_lifecycle_observer.cc:46
    #4 0x7ffee15d9dff in blink::ContextLifecycleNotifier::NotifyContextDestroyed third_party/blink/renderer/platform/context_lifecycle_notifier.cc:32
    #5 0x7ffedde2bfbc in blink::LocalDOMWindow::FrameDestroyed third_party/blink/renderer/core/frame/local_dom_window.cc:902

But an IPC arrives on WorkerOrWorkletGlobalScope afterward.

=> workers/OWNERS

==3864==ERROR: AddressSanitizer: heap-use-after-free on address 0x127e545662c0 at pc 0x7ffee448a9ef bp 0x00a82c7fe6d0 sp 0x00a82c7fe718
READ of size 8 at 0x127e545662c0 thread T0
SCARINESS: 51 (8-byte-read-heap-use-after-free)
[3676:3276:0223/075035.574:VERBOSE1:file_url_loader_factory.cc(454)] FileURLLoader::Start: file:///C:/fake/support/colors-16x8-noSize.svg
==3864==WARNING: Failed to use and restart external symbolizer!
==3864==*** WARNING: Failed to initialize DbgHelp!              ***
==3864==*** Most likely this means that the app is already      ***
==3864==*** using DbgHelp, possibly with incompatible flags.    ***
==3864==*** Due to technical reasons, symbolization might crash ***
==3864==*** or produce wrong results.                           ***
    #0 0x7ffee448a9ee in blink::WorkerOrWorkletGlobalScope::CountUse third_party/blink/renderer/core/workers/worker_or_worklet_global_scope.cc:265
    #1 0x7ffee0bc6f5f in base::internal::Invoker<base::internal::BindState<`lambda at ../../third_party/blink/renderer/core/fileapi/public_url_manager.cc:149:11',cppgc::internal::BasicPersistent<blink::ExecutionContext,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy> >,void (const absl::optional<base::UnguessableToken> &, const absl::optional<blink::BlinkSchemefulSite> &)>::RunOnce base/bind_internal.h:748
    #2 0x7ffed7372d73 in blink::mojom::blink::BlobURLStore_ResolveAsURLLoaderFactory_ForwardToCallback::Accept out/Release_x64/gen/third_party/blink/public/mojom/blob/blob_url_store.mojom-blink.cc:863
    #3 0x7ffed90dc932 in mojo::InterfaceEndpointClient::HandleValidatedMessage mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:896
    #4 0x7ffedbc9877a in mojo::MessageDispatcher::Accept mojo/public/cpp/bindings/lib/message_dispatcher.cc:43
    #5 0x7ffed90e02d4 in mojo::InterfaceEndpointClient::HandleIncomingMessage mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:658
    #6 0x7ffed90f3efd in mojo::internal::MultiplexRouter::ProcessIncomingMessage mojo/public/cpp/bindings/lib/multiplex_router.cc:1096
    #7 0x7ffed90effa6 in mojo::internal::MultiplexRouter::ProcessTasks mojo/public/cpp/bindings/lib/multiplex_router.cc:931
    #8 0x7ffed90f6bc8 in mojo::internal::MultiplexRouter::LockAndCallProcessTasks mojo/public/cpp/bindings/lib/multiplex_router.cc:1124
    #9 0x7ffed8d84c24 in base::TaskAnnotator::RunTaskImpl base/task/common/task_annotator.cc:135
    #10 0x7ffedbb4f0b5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:385
    #11 0x7ffedbb4e689 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:290
    #12 0x7ffedbb26e07 in base::MessagePumpDefault::Run base/message_loop/message_pump_default.cc:38
    #13 0x7ffedbb507e0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:497
    #14 0x7ffed8d048f3 in base::RunLoop::Run base/run_loop.cc:141
    #15 0x7ffedb623d7a in content::RendererMain content/renderer/renderer_main.cc:290
    #16 0x7ffed472cf47 in content::RunOtherNamedProcessTypeMain content/app/content_main_runner_impl.cc:684
    #17 0x7ffed472ec6b in content::ContentMainRunnerImpl::Run content/app/content_main_runner_impl.cc:1044
    #18 0x7ffed472b57b in content::RunContentProcess content/app/content_main.cc:401
    #19 0x7ffed472bcff in content::ContentMain content/app/content_main.cc:429
    #20 0x7ffecdc014ca in ChromeMain chrome/app/chrome_main.cc:176
    #21 0x7ff61f6e5b16 in MainDllLoader::Launch chrome/app/main_dll_loader_win.cc:167
    #22 0x7ff61f6e2b5f in main chrome/app/chrome_exe_main_win.cc:382
    #23 0x7ff61fadd9a3 in __scrt_common_main_seh vctools/crt/vcstartup/src/startup/exe_common.inl:288
    #24 0x7fff14db84d3 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x84d3)
    #25 0x7fff154b1790 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x51790)
0x127e545662c0 is located 0 bytes inside of 32-byte region [0x127e545662c0,0x127e545662e0)
freed by thread T0 here:
    #0 0x7ff61f78d1cb in free third_party/llvm/compiler-rt/lib/asan/asan_malloc_win.cpp:82
    #1 0x7ffee6eca8d0 in blink::MainThreadWorkletReportingProxy::~MainThreadWorkletReportingProxy third_party/blink/renderer/core/workers/main_thread_worklet_reporting_proxy.h:19
    #2 0x7ffee6ec09eb in blink::Worklet::ContextDestroyed third_party/blink/renderer/core/workers/worklet.cc:101
    #3 0x7ffedb4b53e5 in blink::ContextLifecycleObserver::NotifyContextDestroyed third_party/blink/renderer/platform/context_lifecycle_observer.cc:46
    #4 0x7ffee15d9dff in blink::ContextLifecycleNotifier::NotifyContextDestroyed third_party/blink/renderer/platform/context_lifecycle_notifier.cc:32
    #5 0x7ffedde2bfbc in blink::LocalDOMWindow::FrameDestroyed third_party/blink/renderer/core/frame/local_dom_window.cc:902
    #6 0x7ffedde2c55b in blink::LocalDOMWindow::Reset third_party/blink/renderer/core/frame/local_dom_window.cc:920
    #7 0x7ffeddbe440d in blink::LocalFrame::SetDOMWindow third_party/blink/renderer/core/frame/local_frame.cc:816
    #8 0x7ffede14df72 in blink::DocumentLoader::InitializeWindow third_party/blink/renderer/core/loader/document_loader.cc:2151
    #9 0x7ffede150fa6 in blink::DocumentLoader::CommitNavigation third_party/blink/renderer/core/loader/document_loader.cc:2271
    #10 0x7ffedde71d84 in blink::FrameLoader::CommitDocumentLoader third_party/blink/renderer/core/loader/frame_loader.cc:1294
    #11 0x7ffedde7b1f3 in blink::FrameLoader::CommitNavigation third_party/blink/renderer/core/loader/frame_loader.cc:1134
    #12 0x7ffedb464a6a in blink::WebLocalFrameImpl::CommitNavigation third_party/blink/renderer/core/frame/web_local_frame_impl.cc:2408
    #13 0x7ffedb5d49a1 in content::RenderFrameImpl::CommitNavigationWithParams content/renderer/render_frame_impl.cc:2913
    #14 0x7ffedb61a301 in base::internal::FunctorTraits<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >),void>::Invoke<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >),base::WeakPtr<content: base/bind_internal.h:542
    #15 0x7ffedb619c47 in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >),base::WeakPtr<content::RenderFrameImpl>,mojo::StructPtr<blink::mojom::CommonNavigationParams>,mojo::StructPtr<blink::mojom::CommitNavigationParams>,std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >,absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >,mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>,mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>,mojo::PendingRemote<network::mojom::URLLoaderFactory>,mojo::PendingRemote<blink::mojom::CodeCacheHost>,mojo::StructPtr<content::mojom::CookieManagerInfo>,mojo::StructPtr<content::mojom::StorageInfo>,std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> > >,void (std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >)>::RunOnce base/bind_internal.h:748
    #16 0x7ffedb5d1562 in content::RenderFrameImpl::CommitNavigation content/renderer/render_frame_impl.cc:2813
    #17 0x7ffede553d9c in content::NavigationClient::CommitNavigation content/renderer/navigation_client.cc:51
    #18 0x7ffed0e700a4 in content::mojom::NavigationClientStubDispatch::AcceptWithResponder out/Release_x64/gen/content/common/navigation_client.mojom.cc:1307
    #19 0x7ffede554f4c in content::mojom::NavigationClientStub<mojo::RawPtrImplRefTraits<content::mojom::NavigationClient> >::AcceptWithResponder out/Release_x64/gen/content/common/navigation_client.mojom.h:191
    #20 0x7ffed90dca66 in mojo::InterfaceEndpointClient::HandleValidatedMessage mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:863
    #21 0x7ffedbc9877a in mojo::MessageDispatcher::Accept mojo/public/cpp/bindings/lib/message_dispatcher.cc:43
    #22 0x7ffed90e02d4 in mojo::InterfaceEndpointClient::HandleIncomingMessage mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:658
    #23 0x7ffed99d7021 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread ipc/ipc_mojo_bootstrap.cc:1008
    #24 0x7ffed99d0c3d in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce base/bind_internal.h:748
    #25 0x7ffed8d84c24 in base::TaskAnnotator::RunTaskImpl base/task/common/task_annotator.cc:135
    #26 0x7ffedbb4f0b5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:385
    #27 0x7ffedbb4e689 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:290
previously allocated by thread T0 here:
    #0 0x7ff61f78d2cb in malloc third_party/llvm/compiler-rt/lib/asan/asan_malloc_win.cpp:98
    #1 0x7ffeeb50041e in operator new vctools/crt/vcstartup/src/heap/new_scalar.cpp:35
    #2 0x7ffee9745d22 in blink::PaintWorkletGlobalScopeProxy::PaintWorkletGlobalScopeProxy third_party/blink/renderer/modules/csspaint/paint_worklet_global_scope_proxy.cc:34
    #3 0x7ffee88cef3b in blink::MakeGarbageCollected<blink::PaintWorkletGlobalScopeProxy,blink::LocalFrame *,blink::WorkletModuleResponsesMap *,unsigned int> third_party/blink/renderer/platform/heap/garbage_collected.h:34
    #4 0x7ffee88ceb7d in blink::PaintWorklet::CreateGlobalScope third_party/blink/renderer/modules/csspaint/paint_worklet.cc:244
    #5 0x7ffee6ec1376 in blink::Worklet::FetchAndInvokeScript third_party/blink/renderer/core/workers/worklet.cc:166
    #6 0x7ffee6ec409d in base::internal::Invoker<base::internal::BindState<void (blink::Worklet::*)(const blink::KURL &, const WTF::String &, blink::WorkletPendingTasks *),cppgc::internal::BasicPersistent<blink::Worklet,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>,blink::KURL,blink::V8RequestCredentials,cppgc::internal::BasicPersistent<blink::WorkletPendingTasks,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy> >,void ()>::RunOnce base/bind_internal.h:748
    #7 0x7ffed8d84c24 in base::TaskAnnotator::RunTaskImpl base/task/common/task_annotator.cc:135
    #8 0x7ffedbb4f0b5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:385
    #9 0x7ffedbb4e689 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:290
    #10 0x7ffedbb26e07 in base::MessagePumpDefault::Run base/message_loop/message_pump_default.cc:38
    #11 0x7ffedbb507e0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:497
    #12 0x7ffed8d048f3 in base::RunLoop::Run base/run_loop.cc:141
    #13 0x7ffedb623d7a in content::RendererMain content/renderer/renderer_main.cc:290
    #14 0x7ffed472cf47 in content::RunOtherNamedProcessTypeMain content/app/content_main_runner_impl.cc:684
    #15 0x7ffed472ec6b in content::ContentMainRunnerImpl::Run content/app/content_main_runner_impl.cc:1044
    #16 0x7ffed472b57b in content::RunContentProcess content/app/content_main.cc:401
    #17 0x7ffed472bcff in content::ContentMain content/app/content_main.cc:429
    #18 0x7ffecdc014ca in ChromeMain chrome/app/chrome_main.cc:176
    #19 0x7ff61f6e5b16 in MainDllLoader::Launch chrome/app/main_dll_loader_win.cc:167
    #20 0x7ff61f6e2b5f in main chrome/app/chrome_exe_main_win.cc:382
    #21 0x7ff61fadd9a3 in __scrt_common_main_seh vctools/crt/vcstartup/src/startup/exe_common.inl:288
    #22 0x7fff14db84d3 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x84d3)
    #23 0x7fff154b1790 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x51790)

### cl...@chromium.org (2022-02-24)

ClusterFuzz testcase 6663752820523008 is verified as fixed in https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=974465:974466

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-02-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-24)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M100. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-24)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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

### sr...@google.com (2022-02-24)

is there a CL to merge here? if so can you pls share . 

### nh...@chromium.org (2022-02-25)

Hmmm, WorkerOrWorkletGlobalScope::reporting_proxy_ was expected to outlive WorkerOrWorkletGlobalScope, but the assumption seems to be broken. As a stopgap, we could return early from WorkerOrWorkletGlobalScope::CountUse() when WorkerOrWorkletGlobalScope::IsContextDestroyed() returns true.

Note that WorkerReportingProxy lives on a parent thread, while WorkerOrWorkletGlobalScope lives on a worker thread (exception: they live on the same main thread for main thread worklets), so we cannot use WeakPtr here.

As a follow-up, we may have to audit other callsites of WorkerOrWorkletGlobalScope::ReportingProxy(), I guess most of the callsites can safely use it though.

### nh...@chromium.org (2022-02-25)

I'll take this.

https://crbug.com/chromium/1298450#c15: I think this doesn't have a fix yet.

### nh...@chromium.org (2022-02-25)

Hmm, this may need more work in addition to https://crbug.com/chromium/1298450#c16. Main thread worklets seem not to call ExecutionContext::NotifyContextDestroyed().

For threaded worklets and workers, NotifyContextDestroyed() is called on WorkerThread::PrepareForShutdownOnWorkerThread():
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_thread.cc;l=744;drc=e4086ca84eec0844e9d041c11ad822cc6b85b957

### ba...@chromium.org (2022-02-25)

Just so you know, I was trying something similar (checking IsContextDestroyed() in a posted task, i.e., [1]) but UAF still happened. I'm not sure why.

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fileapi/public_url_manager.cc

### nh...@chromium.org (2022-02-25)

I'm now testing behavior here:
https://chromium-review.googlesource.com/c/chromium/src/+/3489568

### nh...@chromium.org (2022-02-25)

https://crbug.com/chromium/1298450#c19: Thanks! I think this is because main thread worklets don't call NotifyContextDestroyed(). I'll try to call it in LayoutWorkletGlobalScopeProxy::TerminateWorkletGlobalScope() etc in the CL on https://crbug.com/chromium/1298450#c20.

### nh...@chromium.org (2022-02-25)

Hmmm, the dtor of ExecutionContext that is the base class of WorkerOrWorkletGlobalScope checks DCHECK(is_context_destroyed_):
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/execution_context/execution_context.cc;l=81-83;drc=be060c5bc861d87e1c71a1e88dfc2768cb24d59c

This means NotifyContextDestroyed() is called for main thread worklets from somewhere...? I'll investigate this more...

### ba...@chromium.org (2022-02-25)

My random guess is that the posted task retains a reference to ExecutionContext so it's not destroyed yet (and NotifyContextDestroyed may not be called yet).
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fileapi/public_url_manager.cc;l=191;drc=52c3e5314c28fa65d8d0cf4dfb49443b42d1bd9a

### wa...@chromium.org (2022-02-25)

This may be the underlying issue behind https://crbug.com/chromium/1253581.  The crash stack there looks very similar to the issue here.

### me...@chromium.org (2022-02-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-02-25)

To fix the crash we could revert my CL that triggered it in the first place (see the bug I just merged into this, and the blamed CL there). Although even then I think it would still be possible to trigger it, since there are still CountUse callsites in the same place. They would just require a bit more setup to trigger.

### wa...@chromium.org (2022-02-25)

From https://crbug.com/chromium/1253581 it seems this has been happening at some rate in the wild for a while.

### nh...@chromium.org (2022-03-03)

Sorry for no updates. I was swamped with other misc things... I'll resume this today.

Based on https://crbug.com/chromium/1298450#c26 and https://crbug.com/chromium/1298450#c27, I'm going to fix the root cause instead of reverting the CL.

### nh...@chromium.org (2022-03-03)

cc haraken@ (reviewer of https://chromium-review.googlesource.com/c/chromium/src/+/3489568) for issue visibility.

### gi...@appspot.gserviceaccount.com (2022-03-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e871285201911d699d0bacd2c83d90c027cc7a4a

commit e871285201911d699d0bacd2c83d90c027cc7a4a
Author: Hiroki Nakagawa <nhiroki@chromium.org>
Date: Thu Mar 03 05:20:07 2022

Worker: Don't call WorkerReportingProxy::CountFeature() during context destruction

This CL avoids calling WorkerReportingProxy::CountFeature() during
context destruction.

Also, this makes sure that ExecutionContext::NotifyContextDestroyed() is
called for main thread worklets (PaintWorklet and LayoutWorklet). Before
this change, it was not called for them.

Bug: 1298450
Change-Id: If4d7ed2c45fe3a214380ade91b7a4f4f098d214e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3489568
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org>
Cr-Commit-Position: refs/heads/main@{#976977}

[modify] https://crrev.com/e871285201911d699d0bacd2c83d90c027cc7a4a/third_party/blink/renderer/core/layout/ng/custom/layout_worklet_global_scope.cc
[modify] https://crrev.com/e871285201911d699d0bacd2c83d90c027cc7a4a/third_party/blink/renderer/modules/csspaint/paint_worklet_global_scope.cc
[modify] https://crrev.com/e871285201911d699d0bacd2c83d90c027cc7a4a/third_party/blink/renderer/core/workers/worker_or_worklet_global_scope.cc


### nh...@chromium.org (2022-03-03)

It's difficult to verify the fix on https://crbug.com/chromium/1298450#c30 as the clusterfuzz claims that this issue was fixed before my change. Also I tried to reproduce this on my local environment (Linux) but failed. I wonder if other CLs could tweak a timing to run the callback or the repro program could be just flaky.

### me...@chromium.org (2022-03-03)

https://clusterfuzz.com/testcase-detail/5411380085456896 (from the bug I dup-ed into this one) seems to be a more reproducible case? That one at least was still listed as failing before your CL. Hopefully it is fixed after your CL.

### [Deleted User] (2022-03-03)

[Empty comment from Monorail migration]

### sr...@google.com (2022-03-03)

amyressler@ can you review and suggest next steps

### nh...@chromium.org (2022-03-04)

https://crbug.com/chromium/1298450#c33: Thanks! I'm now waiting for the completion of the redo task.

### nh...@chromium.org (2022-03-04)

Sorry, I wanted to say https://crbug.com/chromium/1298450#c32 (mek@'s comment).

### nh...@chromium.org (2022-03-06)

The clusterfuzz on https://crbug.com/chromium/1298450#c32 confirmed that the issue was fixed by my change. Let me start a merge process...


Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?

This issues has Security_Severity-High.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3489568

3. Have the changes been released and tested on canary?

The change was released on 101.0.4922.0. I confirmed it with the clusterfuzz.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

N/A

### sr...@google.com (2022-03-07)

Merge approved for M100 branch:pls refer to go/chrome-branches for branch info

### sr...@google.com (2022-03-07)

This bug is approved for M100 merge, please complete your merge asap so this can be included in the beta release this week. Beta RC will be cut tomorrow ( tuesday) March 8th at 3pm PST [Bulk Update]

### gi...@appspot.gserviceaccount.com (2022-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b8a64c8db6221416da0467ac3c31a5a073946d03

commit b8a64c8db6221416da0467ac3c31a5a073946d03
Author: Hiroki Nakagawa <nhiroki@chromium.org>
Date: Tue Mar 08 00:27:52 2022

[M100 Merge] Worker: Don't call WorkerReportingProxy::CountFeature() during context destruction

This CL avoids calling WorkerReportingProxy::CountFeature() during
context destruction.

Also, this makes sure that ExecutionContext::NotifyContextDestroyed() is
called for main thread worklets (PaintWorklet and LayoutWorklet). Before
this change, it was not called for them.

(cherry picked from commit e871285201911d699d0bacd2c83d90c027cc7a4a)

Bug: 1298450
Change-Id: If4d7ed2c45fe3a214380ade91b7a4f4f098d214e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3507933
Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org>
Cr-Commit-Position: refs/branch-heads/4896@{#360}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/b8a64c8db6221416da0467ac3c31a5a073946d03/third_party/blink/renderer/core/layout/ng/custom/layout_worklet_global_scope.cc
[modify] https://crrev.com/b8a64c8db6221416da0467ac3c31a5a073946d03/third_party/blink/renderer/modules/csspaint/paint_worklet_global_scope.cc
[modify] https://crrev.com/b8a64c8db6221416da0467ac3c31a5a073946d03/third_party/blink/renderer/core/workers/worker_or_worklet_global_scope.cc


### nh...@chromium.org (2022-03-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-17)

Congratulations! The VRP Panel has decided to award you $5,000 for the fuzzer report of this issue + $1,000 fuzzer bonus. Thank you for your Chrome Fuzzing efforts!

### am...@chromium.org (2022-03-17)

RV-SE at researcher's request. 

### am...@chromium.org (2022-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-17)

[Empty comment from Monorail migration]

### nh...@chromium.org (2022-03-18)

Congrats and thanks for reporting the issue!

### [Deleted User] (2022-06-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1298450?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1299165]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-03-05)

The relevant amount of time has passed for the original reasoning for this issue being under embargo. Removing this issue from under embargo and opening for public disclosure.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058806)*
