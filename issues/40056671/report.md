# Security: Heap-use-after-free in AutofillManager::OnLoadedServerPredictions

| Field | Value |
|-------|-------|
| **Issue ID** | [40056671](https://issues.chromium.org/issues/40056671) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | mi...@chromium.org |
| **Created** | 2021-07-26 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36

Steps to reproduce the problem:
1. apply change.diff to chromium and compile it.
2. start a server at the folder of poc.html `python -m SimpleHTTPServer 8605`
3. ./chrome --autofill-server-query-result-delay-in-seconds=3 http://127.0.0.1:8605/poc.html 
4. click the submit button and wait for crash

What is the expected behavior?

What went wrong?
n function AutofillManager::OnLoadedServerPredictions[1], postdelayedtask will call the callback with `Unretained(this)`, which will cause UAF if `this` is deleted before the task is called with a timeout.
```
  if (delay > 0) {
    query_result_delay_task_.Reset(
        base::BindOnce(&AutofillManager::PropagateAutofillPredictionsToDriver,
                       base::Unretained(this)));  // ==>[1]
    base::ThreadTaskRunnerHandle::Get()->PostDelayedTask(
        FROM_HERE,
        base::BindOnce(query_result_delay_task_.callback(), queried_forms),
        base::TimeDelta::FromSeconds(delay));
```

To trigger this UAF, you need to enable the delay with the command line switch "autofill-server-query-result-delay-in-seconds". 
And you also need a cache in autofill request, we can do this by calling `AutofillDownloadManager::OnSimpleLoaderComplete`[2], but I find that the http response always is 400, which will make the `success` be false. I can't figure out why this happens but we can bypass it by patching the response_code to 200(change.diff).

I also provide a possible patch for this UAF in patch.diff but I can't determine its correctness.

[1]https://source.chromium.org/chromium/chromium/src/+/main:components/autofill/core/browser/autofill_manager.cc;l=520
[2]https://source.chromium.org/chromium/chromium/src/+/main:components/autofill/core/browser/autofill_download_manager.cc;l=962

=================================================================
==17382==ERROR: AddressSanitizer: heap-use-after-free on address 0x6170001a8c48 at pc 0x555575c3744a bp 0x7fffffffce90 sp 0x7fffffffce88
READ of size 8 at 0x6170001a8c48 thread T0 (chrome)
[Detaching after fork from child process 18067]
    #0 0x555575c37449 in begin buildtools/third_party/libc++/trunk/include/vector:1526:30
    #1 0x555575c37449 in begin components/autofill/core/browser/form_structure.h:233:20
    #2 0x555575c37449 in password_manager::ConvertToFormPredictions(int, autofill::FormStructure const&) components/password_manager/core/browser/form_parsing/password_field_prediction.cc:103:26
    #3 0x555575a9e3f1 in password_manager::PasswordManager::ProcessAutofillPredictions(password_manager::PasswordManagerDriver*, std::__1::vector<autofill::FormStructure*, std::__1::allocator<autofill::FormStructure*> > const&) components/password_manager/core/browser/password_manager.cc:1118:9
    #4 0x555577d636e1 in Run base/callback.h:98:12
    #5 0x555577d636e1 in void base::internal::CancelableCallbackImpl<base::OnceCallback<void (std::__1::vector<autofill::FormStructure*, std::__1::allocator<autofill::FormStructure*> > const&)> >::ForwardOnce<std::__1::vector<autofill::FormStructure*, std::__1::allocator<autofill::FormStructure*> > const&>(std::__1::vector<autofill::FormStructure*, std::__1::allocator<autofill::FormStructure*> > const&) base/cancelable_callback.h:128:26
    #6 0x555577d6392d in Invoke<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void (const std::vector<autofill::FormStructure *> &)> >::*)(const std::vector<autofill::FormStructure *> &), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void (const std::vector<autofill::FormStructure *> &)> > >, const std::vector<autofill::FormStructure *> &> base/bind_internal.h:509:12
    #7 0x555577d6392d in MakeItSo<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void (const std::vector<autofill::FormStructure *> &)> >::*)(const std::vector<autofill::FormStructure *> &), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void (const std::vector<autofill::FormStructure *> &)> > >, const std::vector<autofill::FormStructure *> &> base/bind_internal.h:668:5
    #8 0x555577d6392d in RunImpl<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void (const std::vector<autofill::FormStructure *> &)> >::*)(const std::vector<autofill::FormStructure *> &), std::tuple<base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void (const std::vector<autofill::FormStructure *> &)> > > >, 0UL> base/bind_internal.h:721:12
    #9 0x555577d6392d in base::internal::Invoker<base::internal::BindState<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void (std::__1::vector<autofill::FormStructure*, std::__1::allocator<autofill::FormStructure*> > const&)> >::*)(std::__1::vector<autofill::FormStructure*, std::__1::allocator<autofill::FormStructure*> > const&), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void (std::__1::vector<autofill::FormStructure*, std::__1::allocator<autofill::FormStructure*> > const&)> > > >, void (std::__1::vector<autofill::FormStructure*, std::__1::allocator<autofill::FormStructure*> > const&)>::RunOnce(base::internal::BindStateBase*, std::__1::vector<autofill::FormStructure*, std::__1::allocator<autofill::FormStructure*> > const&) base/bind_internal.h:690:12
    #10 0x555577d63d2c in Run base/callback.h:98:12
    #11 0x555577d63d2c in Invoke<base::OnceCallback<void (const std::vector<autofill::FormStructure *> &)>, std::vector<autofill::FormStructure *> > base/bind_internal.h:608:49
    #12 0x555577d63d2c in MakeItSo<base::OnceCallback<void (const std::vector<autofill::FormStructure *> &)>, std::vector<autofill::FormStructure *> > base/bind_internal.h:648:12
    #13 0x555577d63d2c in RunImpl<base::OnceCallback<void (const std::vector<autofill::FormStructure *> &)>, std::tuple<std::vector<autofill::FormStructure *> >, 0UL> base/bind_internal.h:721:12
    #14 0x555577d63d2c in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (std::__1::vector<autofill::FormStructure*, std::__1::allocator<autofill::FormStructure*> > const&)>, std::__1::vector<autofill::FormStructure*, std::__1::allocator<autofill::FormStructure*> > >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #15 0x55556e126110 in Run base/callback.h:98:12
    #16 0x55556e126110 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #17 0x55556e15f389 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #18 0x55556e15eafa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #19 0x55556e15fd31 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #20 0x55556e01feba in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #21 0x55556e1603f4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #22 0x55556e0a17e1 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #23 0x55556524e2a5 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:987:18
    #24 0x555565252de5 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #25 0x55556524819f in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:28
    #26 0x55556cf2a4ed in RunBrowserProcessMain content/app/content_main_runner_impl.cc:608:10
    #27 0x55556cf2a4ed in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1104:10
    #28 0x55556cf295f5 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:971:12
    #29 0x55556cf22ba7 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #30 0x55556cf247c2 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #31 0x55555ffffb26 in ChromeMain chrome/app/chrome_main.cc:164:12
    #32 0x7ffff60120b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6170001a8c48 is located 584 bytes inside of 752-byte region [0x6170001a8a00,0x6170001a8cf0)
freed by thread T0 (chrome) here:
    #0 0x55555fffd83d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x555577d625dd in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x555577d625dd in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x555577d625dd in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #4 0x555577d625dd in ~pair buildtools/third_party/libc++/trunk/include/utility:394:29
    #5 0x555577d625dd in destroy<std::pair<const autofill::internal::GlobalId<autofill::FormRendererId>, std::unique_ptr<autofill::FormStructure> >, void, void> buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:318:15
    #6 0x555577d625dd in std::__1::__tree<std::__1::__value_type<autofill::internal::GlobalId<autofill::FormRendererId>, std::__1::unique_ptr<autofill::FormStructure, std::__1::default_delete<autofill::FormStructure> > >, std::__1::__map_value_compare<autofill::internal::GlobalId<autofill::FormRendererId>, std::__1::__value_type<autofill::internal::GlobalId<autofill::FormRendererId>, std::__1::unique_ptr<autofill::FormStructure, std::__1::default_delete<autofill::FormStructure> > >, std::__1::less<autofill::internal::GlobalId<autofill::FormRendererId> >, true>, std::__1::allocator<std::__1::__value_type<autofill::internal::GlobalId<autofill::FormRendererId>, std::__1::unique_ptr<autofill::FormStructure, std::__1::default_delete<autofill::FormStructure> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<autofill::internal::GlobalId<autofill::FormRendererId>, std::__1::unique_ptr<autofill::FormStructure, std::__1::default_delete<autofill::FormStructure> > >, void*>*) buildtools/third_party/libc++/trunk/include/__tree:1801:9
    #7 0x555577d61345 in clear buildtools/third_party/libc++/trunk/include/__tree:1838:5
    #8 0x555577d61345 in clear buildtools/third_party/libc++/trunk/include/map:1322:37
    #9 0x555577d61345 in autofill::AutofillManager::Reset() components/autofill/core/browser/autofill_manager.cc:454:20
    #10 0x555577d4b01e in autofill::BrowserAutofillManager::Reset() components/autofill/core/browser/browser_autofill_manager.cc:1588:20
    #11 0x555566400cd9 in void content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle*&>(void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle*&) content/browser/web_contents/web_contents_impl.h:1484:9
    #12 0x5555664020c2 in content::WebContentsImpl::DidFinishNavigation(content::NavigationHandle*) content/browser/web_contents/web_contents_impl.cc:5384:16
    #13 0x555565e14462 in content::NavigationRequest::~NavigationRequest() content/browser/renderer_host/navigation_request.cc:1530:20
    #14 0x555565e16f1d in content::NavigationRequest::~NavigationRequest() content/browser/renderer_host/navigation_request.cc:1489:41
    #15 0x555565e68c19 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #16 0x555565e68c19 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #17 0x555565e68c19 in content::Navigator::DidNavigate(content::RenderFrameHostImpl*, content::mojom::DidCommitProvisionalLoadParams const&, std::__1::unique_ptr<content::NavigationRequest, std::__1::default_delete<content::NavigationRequest> >, bool) content/browser/renderer_host/navigator.cc:532:24
    #18 0x555565eb343c in content::RenderFrameHostImpl::DidCommitNavigationInternal(std::__1::unique_ptr<content::NavigationRequest, std::__1::default_delete<content::NavigationRequest> >, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::InlinedStructPtr<content::mojom::DidCommitSameDocumentNavigationParams>) content/browser/renderer_host/render_frame_host_impl.cc:10005:34
    #19 0x555565eb0c84 in content::RenderFrameHostImpl::DidCommitNavigation(content::NavigationRequest*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>) content/browser/renderer_host/render_frame_host_impl.cc:10473:8
    #20 0x555565f37433 in Invoke<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), content::RenderFrameHostImpl *, content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams> > base/bind_internal.h:509:12
    #21 0x555565f37433 in MakeItSo<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), content::RenderFrameHostImpl *, content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams> > base/bind_internal.h:648:12
    #22 0x555565f37433 in RunImpl<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), std::tuple<base::internal::UnretainedWrapper<content::RenderFrameHostImpl>, content::NavigationRequest *>, 0UL, 1UL> base/bind_internal.h:721:12
    #23 0x555565f37433 in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::*)(content::NavigationRequest*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), base::internal::UnretainedWrapper<content::RenderFrameHostImpl>, content::NavigationRequest*>, void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>::RunOnce(base::internal::BindStateBase*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>&&, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>&&) base/bind_internal.h:690:12
    #24 0x5555641d103f in Run base/callback.h:98:12
    #25 0x5555641d103f in content::mojom::NavigationClient_CommitNavigation_ForwardToCallback::Accept(mojo::Message*) gen/content/common/navigation_client.mojom.cc:894:26
    #26 0x55556ec0dc25 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:893:23
    #27 0x55556ec1f261 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #28 0x55556ec11727 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:655:20
    #29 0x55557050b829 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:981:24
    #30 0x5555705040d4 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:509:12
    #31 0x5555705040d4 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:648:12
    #32 0x5555705040d4 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind_internal.h:721:12
    #33 0x5555705040d4 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #34 0x55556e126110 in Run base/callback.h:98:12
    #35 0x55556e126110 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #36 0x55556e15f389 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #37 0x55556e15eafa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #38 0x55556e15fd31 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #39 0x55556e020cb9 in HandleDispatch base/message_loop/message_pump_glib.cc:375:46
    #40 0x55556e020cb9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:125:43
    #41 0x7ffff7e2efbc in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51fbc)

previously allocated by thread T0 (chrome) here:
    #0 0x55555fffcfdd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x555577d5e390 in make_unique<autofill::FormStructure, const autofill::FormData &> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:28
    #2 0x555577d5e390 in autofill::AutofillManager::ParseForm(autofill::FormData const&, autofill::FormStructure const*) components/autofill/core/browser/autofill_manager.cc:415:25
    #3 0x555577d5d9e4 in autofill::AutofillManager::OnFormsSeen(std::__1::vector<autofill::FormData, std::__1::allocator<autofill::FormData> > const&) components/autofill/core/browser/autofill_manager.cc:213:37
    #4 0x555577d8f15a in autofill::ContentAutofillRouter::FormsSeen(autofill::ContentAutofillDriver*, std::__1::vector<autofill::FormData, std::__1::allocator<autofill::FormData> > const&) components/autofill/content/browser/content_autofill_router.cc:166:13
    #5 0x555577d26181 in autofill::ContentAutofillDriver::FormsSeen(std::__1::vector<autofill::FormData, std::__1::allocator<autofill::FormData> > const&) components/autofill/content/browser/content_autofill_driver.cc:465:21
    #6 0x555567fc83b4 in autofill::mojom::AutofillDriverStubDispatch::Accept(autofill::mojom::AutofillDriver*, mojo::Message*) gen/components/autofill/content/common/mojom/autofill_driver.mojom.cc:912:13
    #7 0x55556ec0d81b in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:898:54
    #8 0x55556ec1f261 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #9 0x55556ec11727 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:655:20
    #10 0x55557050b829 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:981:24
    #11 0x5555705040d4 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:509:12
    #12 0x5555705040d4 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:648:12
    #13 0x5555705040d4 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind_internal.h:721:12
    #14 0x5555705040d4 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #15 0x55556e126110 in Run base/callback.h:98:12
    #16 0x55556e126110 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #17 0x55556e15f389 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #18 0x55556e15eafa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #19 0x55556e15fd31 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #20 0x55556e01feba in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #21 0x55556e1603f4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #22 0x55556e0a17e1 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #23 0x55556524e2a5 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:987:18
    #24 0x555565252de5 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #25 0x55556524819f in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:28
    #26 0x55556cf2a4ed in RunBrowserProcessMain content/app/content_main_runner_impl.cc:608:10
    #27 0x55556cf2a4ed in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1104:10
    #28 0x55556cf295f5 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:971:12
    #29 0x55556cf22ba7 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #30 0x55556cf247c2 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #31 0x55555ffffb26 in ChromeMain chrome/app/chrome_main.cc:164:12
    #32 0x7ffff60120b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/vector:1526:30 in begin
Shadow bytes around the buggy address:
  0x0c2e8002d130: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e8002d140: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8002d150: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8002d160: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2e8002d170: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2e8002d180: fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd
  0x0c2e8002d190: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
  0x0c2e8002d1a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e8002d1b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e8002d1c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2e8002d1d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==17382==ABORTING

Did this work before? N/A 

Chrome version: 92.0.4515.107  Channel: stable
OS Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- [change.diff](attachments/change.diff) (text/plain, 740 B)
- [poc.html](attachments/poc.html) (text/plain, 230 B)
- [patch.diff](attachments/patch.diff) (text/plain, 752 B)

## Timeline

### [Deleted User] (2021-07-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-26)

+michaelbai who wrote the CL which introduced the base::Unretained. Can you follow up here please? Assigning a medium severity for a browser process UaF, but possibly requiring an esoteric triggering condition.

[Monorail components: UI>Browser>Autofill]

### do...@chromium.org (2021-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-26)

[Empty comment from Monorail migration]

### ba...@chromium.org (2021-07-26)

Thanks for the bug report.

Michael, IIRC, this code was only added to allow testers prove that some code works. Shall we just delete this delayed response flag now?

I think that this has no real-world security implications because it is an undocumented command line flag.

### [Deleted User] (2021-07-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mi...@chromium.org (2021-07-26)

Yes, this is for testing only.  the AwG owner is ooo, I will remove the code once getting the confirmation.

The interesting thing is that this task shall be cancelled in destructor,  https://source.chromium.org/chromium/chromium/src/+/main:components/autofill/core/browser/autofill_manager.cc;drc=5a5bac09390c516903e8b0a6da51d335e7b822a8;l=146

I weren't able to figure out what I did wrongly, add base owner help to check.




### mi...@chromium.org (2021-07-26)

@ajwong I randomly added you this issue because you are base owner, could you help to check what I did wrongly for using CancelableOnceCallback in AutofillManager.

Thanks!

### ba...@chromium.org (2021-07-27)

I think that the problem is not the base::Unretained(this) but rather that here:
https://source.chromium.org/chromium/chromium/src/+/main:components/autofill/core/browser/autofill_manager.cc;l=523;drc=5a5bac09390c516903e8b0a6da51d335e7b822a8
queried_forms store a set of raw pointers that can be invalidated.

If you want to keep the code, you need to add query_result_delay_task_.Cancel(); to void AutofillManager::Reset().

### mi...@chromium.org (2021-07-27)

Oh, right, thanks for spotting it.

### gi...@appspot.gserviceaccount.com (2021-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/585b3bdc010642d1cb9ff52ef48f088bf8e9e1b8

commit 585b3bdc010642d1cb9ff52ef48f088bf8e9e1b8
Author: Michael Bai <michaelbai@chromium.org>
Date: Tue Jul 27 20:54:59 2021

Aw Autofill: Cancel the task on reset

Cancel the task on AutofillManager::Reset. This task is only for
testing purpose

Bug: 1232914
Change-Id: I2fbaaaa157f7e62dbda1ae8a258e261dd68cbe4a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3056854
Commit-Queue: Michael Bai <michaelbai@chromium.org>
Reviewed-by: Dominic Battré <battre@chromium.org>
Cr-Commit-Position: refs/heads/master@{#905887}

[modify] https://crrev.com/585b3bdc010642d1cb9ff52ef48f088bf8e9e1b8/components/autofill/core/browser/autofill_manager.cc


### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-11)

michaelbai: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mi...@chromium.org (2021-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-19)

The VRP Panel has decided to award you $1,000 as a thank you for your report and efforts. 

### am...@google.com (2021-08-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-21)

removing release label as this has no security implications and was code for testing purposes 

### [Deleted User] (2021-11-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2022-12-13)

Updating security impact labels, as the impact was None.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1232914?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056671)*
