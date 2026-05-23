# Security: UaF in chrome!payments::PaymentRequestSheetController::UpdateHeaderView

| Field | Value |
|-------|-------|
| **Issue ID** | [40054420](https://issues.chromium.org/issues/40054420) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Payments |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2021-01-12 |
| **Bounty** | $15,000.00 |

## Description

**VERSION**  

Chrome Version: 89.0.4384.0 (Official Build) canary (x86\_64)  

Operating System: MacOS and Windows

**REPRODUCTION CASE**  

0. ensure that #enable-portals and #enable-portals-cross-origin from chrome://flags are enabled.

1. go to <http://localhost:8000/repro.html>
2. Open another tab and go to <https://maxlgu.github.io/pr/max-nonbasiccard/>
3. Click on "Busy" button.
4. In payments window try to change <http://www.google.com> to <http://localhost:8000/repro.html> then click on "Go!" button.
5. Navigate backward

Crash/3b2d5b5dfda73019.

\*\*\* WARNING: Unable to verify checksum for chrome.dll  

rax=efefefefefefefef rbx=000076d0012d3800 rcx=000076d000bf8c50  

rdx=30335b0200000001 rsi=000076d000bf8c50 rdi=000076d000ea24f8  

rip=00007ffa6645ba4b rsp=000000c17c3fc6e0 rbp=aaaaaaaaaaaaaaaa  

r8=0000000000000080 r9=00000000ff000000 r10=0000000000ff0000  

r11=8101010101010100 r12=0000000000000000 r13=aaaaaaaaaaaaaaaa  

r14=000076d000ea24d0 r15=aaaaaaaaaaaaaaaa  

iopl=0 nv up ei pl zr na po nc  

cs=0033 ss=0000 ds=0000 es=0000 fs=0053 gs=002b efl=00010246  

chrome!views::View::UpdateTooltip+0x6 [inlined in chrome!views::View::RemoveAllChildViews+0x4b]:  

00007ffa`6645ba4b ff5050 call qword ptr [rax+50h] ds:efefefef`efeff03f=????????????????  

0:000> k  

\*\*\* Stack trace for last set context - .thread/.cxr resets it

# Child-SP RetAddr Call Site

00 (Inline Function) --------`-------- chrome!views::View::UpdateTooltip+0x6 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 3083] 01 000000c1`7c3fc6e0 00007ffa`6cc335f8 chrome!views::View::RemoveAllChildViews+0x4b [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 298] 02 000000c1`7c3fc720 00007ffa`66dc4552 chrome!payments::PaymentRequestSheetController::UpdateHeaderView+0x28 [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\payment_request_sheet_controller.cc @ 298] 03 000000c1`7c3fc7a0 00007ffa`6b4e6b18 chrome!content::WebContentsImpl::DidChangeVisibleSecurityState+0x72 [c:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc @ 2348] 04 000000c1`7c3fc900 00007ffa`67bb2b1f chrome!security_interstitials::SecurityInterstitialTabHelper::DidFinishNavigation+0xd8 [c:\b\s\w\ir\cache\builder\src\components\security_interstitials\content\security_interstitial_tab_helper.cc @ 43] 05 (Inline Function) --------`-------- chrome!content::WebContentsImpl::DidFinishNavigation::<unnamed-tag>::operator()+0xf [c:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc @ 5167]  

06 (Inline Function) --------`-------- chrome!content::WebContentsImpl::WebContentsObserverList::ForEachObserver+0x237 [c:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.h @ 1447] 07 000000c1`7c3fc960 00007ffa`662a6548 chrome!content::WebContentsImpl::DidFinishNavigation+0x29f [c:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc @ 5166] 08 000000c1`7c3fcac0 00007ffa`662a63d0 chrome!content::NavigationRequest::~NavigationRequest+0x158 [c:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_request.cc @ 1338] 09 000000c1`7c3fcc90 00007ffa`65623ce7 chrome!content::NavigationRequest::~NavigationRequest+0x10 [c:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_request.cc @ 1296] 0a (Inline Function) --------`-------- chrome!std::\_\_1::default\_delete[media::RendererFactory](javascript:void(0);)::operator()+0xa [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory @ 2378]  

0b (Inline Function) --------`-------- chrome!std::__1::unique_ptr<media::RendererFactory,std::default_delete<media::RendererFactory> >::reset+0x1b [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory @ 2633] 0c (Inline Function) --------`-------- chrome!std::\_\_1::unique\_ptr<media::RendererFactory,std::default\_delete[media::RendererFactory](javascript:void(0);) >::~unique\_ptr+0x1b [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory @ 2587]  

0d (Inline Function) --------`-------- chrome!std::__1::pair<const media::RendererFactoryType,std::unique_ptr<media::RendererFactory,std::default_delete<media::RendererFactory> > >::~pair+0x1b [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\utility @ 297] 0e (Inline Function) --------`-------- chrome!std::\_\_1::allocator\_traits<std::allocator<std::\_\_tree\_node<std::\_\_value\_type<media::RendererFactoryType,std::unique\_ptr<media::RendererFactory,std::default\_delete[media::RendererFactory](javascript:void(0);) > >,void \*> > >::\_\_destroy+0x1b [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory @ 1787]  

0f (Inline Function) --------`-------- chrome!std::__1::allocator_traits<std::allocator<std::__tree_node<std::__value_type<media::RendererFactoryType,std::unique_ptr<media::RendererFactory,std::default_delete<media::RendererFactory> > >,void \*> > >::destroy+0x1b [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory @ 1619] 10 000000c1`7c3fccd0 00007ffa`66d9a0a6 chrome!std::__1::__tree<std::__value_type<media::RendererFactoryType,std::unique_ptr<media::RendererFactory,std::default_delete<media::RendererFactory> > >,std::__map_value_compare<media::RendererFactoryType,std::__value_type<media::RendererFactoryType,std::unique_ptr<media::RendererFactory,std::default_delete<media::RendererFactory> > >,std::less<media::RendererFactoryType>,1>,std::allocator<std::__value_type<media::RendererFactoryType,std::unique_ptr<media::RendererFactory,std::default_delete<media::RendererFactory> > > > >::destroy+0x47 [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__tree @ 1831] 11 (Inline Function) --------`-------- chrome!std::\_\_1::\_\_tree<std::\_\_value\_type<content::NavigationRequest \*,std::unique\_ptr<content::NavigationRequest,std::default\_delete[content::NavigationRequest](javascript:void(0);) > >,std::\_\_map\_value\_compare<content::NavigationRequest \*,std::\_\_value\_type<content::NavigationRequest \*,std::unique\_ptr<content::NavigationRequest,std::default\_delete[content::NavigationRequest](javascript:void(0);) > >,std::less<content::NavigationRequest \*>,1>,std::allocator<std::\_\_value\_type<content::NavigationRequest \*,std::unique\_ptr<content::NavigationRequest,std::default\_delete[content::NavigationRequest](javascript:void(0);) > > > >::clear+0x13 [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree @ 1870]  

12 (Inline Function) --------`-------- chrome!std::__1::map<content::NavigationRequest \*,std::unique_ptr<content::NavigationRequest,std::default_delete<content::NavigationRequest> >,std::less<content::NavigationRequest \*>,std::allocator<std::pair<content::NavigationRequest \*const,std::unique_ptr<content::NavigationRequest,std::default_delete<content::NavigationRequest> > > > >::clear+0x13 [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\map @ 1309] 13 000000c1`7c3fcd10 00007ffa`66b292df chrome!content::RenderFrameHostImpl::ResetNavigationRequests+0x26 [c:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_impl.cc @ 3275] 14 000000c1`7c3fcd60 00007ffa`66b28d10 chrome!content::WebContentsImpl::~WebContentsImpl+0x5af [c:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc @ 956] 15 000000c1`7c3fcf30 00007ffa`66056e8c chrome!content::WebContentsImpl::~WebContentsImpl+0x10 [c:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc @ 868] 16 (Inline Function) --------`-------- chrome!std::\_\_1::default\_delete[content::WebContents](javascript:void(0);)::operator()+0xa [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory @ 2378]  

17 (Inline Function) --------`-------- chrome!std::__1::unique_ptr<content::WebContents,std::default_delete<content::WebContents> >::reset+0x128 [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory @ 2633] 18 000000c1`7c3fcf70 00007ffa`665cf316 chrome!views::WebView::SetWebContents+0x1dc [c:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\webview.cc @ 97] 19 000000c1`7c3fd020 00007ffa`665cf240 chrome!views::WebView::~WebView+0xb6 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\webview.cc @ 72] 1a 000000c1`7c3fd070 00007ffa`65af0a7f chrome!views::WebView::~WebView+0x10 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\webview\webview.cc @ 69] 1b 000000c1`7c3fd0b0 00007ffa`66f7a320 chrome!views::View::~View+0x18f [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 220] 1c 000000c1`7c3fd1b0 00007ffa`65af0a7f chrome!views::View::~View+0x10 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 203] 1d 000000c1`7c3fd1f0 00007ffa`66f7a320 chrome!views::View::~View+0x18f [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 220] 1e 000000c1`7c3fd2f0 00007ffa`65af0a7f chrome!views::View::~View+0x10 [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 203] 1f 000000c1`7c3fd330 00007ffa`6acf7150 chrome!views::View::~View+0x18f [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 220] 20 (Inline Function) --------`-------- chrome!views::ScrollView::Viewport::~Viewport+0x95 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\scroll\_view.cc @ 133]  

21 000000c1`7c3fd430 00007ffa`65af0a7f chrome!views::ScrollView::Viewport::~Viewport+0xa0 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\scroll\_view.cc @ 133]  

22 000000c1`7c3fd470 00007ffa`6acf6ec0 chrome!views::View::~View+0x18f [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 220]  

23 000000c1`7c3fd570 00007ffa`65af0a7f chrome!views::ScrollView::~ScrollView+0x10 [c:\b\s\w\ir\cache\builder\src\ui\views\controls\scroll\_view.cc @ 238]  

24 000000c1`7c3fd5b0 00007ffa`67722a67 chrome!views::View::~View+0x18f [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 220]  

25 (Inline Function) --------`-------- chrome!payments::`anonymous namespace'::SheetView::~SheetView+0xdc [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\payment\_request\_sheet\_controller.cc @ 57]  

26 000000c1`7c3fd6b0 00007ffa`65af0a7f chrome!payments::`anonymous namespace'::SheetView::~SheetView+0xe7 [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\payment_request_sheet_controller.cc @ 57] 27 000000c1`7c3fd6f0 00007ffa`6cc32c90 chrome!views::View::~View+0x18f [c:\b\s\w\ir\cache\builder\src\ui\views\view.cc @ 220] 28 000000c1`7c3fd7f0 00007ffa`6c9b4d32 chrome!ViewStack::~ViewStack+0x10 [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\view_stack.cc @ 30] 29 (Inline Function) --------`-------- chrome!std::\_\_1::default\_delete<ViewStack>::operator()+0xe [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory @ 2378]  

2a (Inline Function) --------`-------- chrome!std::__1::unique_ptr<ViewStack,std::default_delete<ViewStack> >::reset+0x10 [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory @ 2633] 2b (Inline Function) --------`-------- chrome!std::\_\_1::unique\_ptr<ViewStack,std::default\_delete<ViewStack> >::~unique\_ptr+0x10 [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory @ 2587]  

2c 000000c1`7c3fd830 00007ffa`67954b5e chrome!payments::PaymentRequestDialogView::OnDialogClosed+0x62 [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\payment\_request\_dialog\_view.cc @ 98]  

2d (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<1,void>::MakeItSo+0x42 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 657] 2e (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (net::MDnsListenerImpl::\*)(),base::WeakPtr[net::MDnsListenerImpl](javascript:void(0);) >,void ()>::RunImpl+0x42 [c:\b\s\w\ir\cache\builder\src\base\bind\_internal.h @ 710]  

2f 000000c1`7c3fd880 00007ffa`690bcf40 chrome!base::internal::Invoker<base::internal::BindState<void (net::MDnsListenerImpl::\*)(),base::WeakPtr[net::MDnsListenerImpl](javascript:void(0);) >,void ()>::Run+0x5e [c:\b\s\w\ir\cache\builder\src\base\bind\_internal.h @ 695]  

30 (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x11 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 101] 31 (Inline Function) --------`-------- chrome!views::DialogDelegate::RunCloseCallback+0x1d [c:\b\s\w\ir\cache\builder\src\ui\views\window\dialog\_delegate.cc @ 172]  

32 000000c1`7c3fd8d0 00007ffa`6664ff48 chrome!views::DialogDelegate::WindowWillClose+0x80 [c:\b\s\w\ir\cache\builder\src\ui\views\window\dialog\_delegate.cc @ 232]  

33 (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x25 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 101] 34 000000c1`7c3fd920 00007ffa`6664fd03 chrome!views::WidgetDelegate::WindowWillClose+0x68 [c:\b\s\w\ir\cache\builder\src\ui\views\widget\widget_delegate.cc @ 211] 35 000000c1`7c3fd980 00007ffa`670c016c chrome!views::Widget::CloseWithReason+0x2e3 [c:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc @ 630] 36 (Inline Function) --------`-------- chrome!web\_modal::WebContentsModalDialogManager::CloseAllDialogs+0x2d [c:\b\s\w\ir\cache\builder\src\components\web\_modal\web\_contents\_modal\_dialog\_manager.cc @ 124]  

37 000000c1`7c3fda60 00007ffa`67bb2b1f chrome!web\_modal::WebContentsModalDialogManager::DidFinishNavigation+0x8c [c:\b\s\w\ir\cache\builder\src\components\web\_modal\web\_contents\_modal\_dialog\_manager.cc @ 136]  

38 (Inline Function) --------`-------- chrome!content::WebContentsImpl::DidFinishNavigation::<unnamed-tag>::operator()+0xf [c:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc @ 5167] 39 (Inline Function) --------`-------- chrome!content::WebContentsImpl::WebContentsObserverList::ForEachObserver+0x237 [c:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.h @ 1447]  

3a 000000c1`7c3fdaa0 00007ffa`662a6548 chrome!content::WebContentsImpl::DidFinishNavigation+0x29f [c:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc @ 5166]  

3b 000000c1`7c3fdc00 00007ffa`662a63d0 chrome!content::NavigationRequest::~NavigationRequest+0x158 [c:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_request.cc @ 1338]  

3c 000000c1`7c3fddd0 00007ffa`65d4b581 chrome!content::NavigationRequest::~NavigationRequest+0x10 [c:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_request.cc @ 1296]  

3d (Inline Function) --------`-------- chrome!std::__1::default_delete<content::NavigationRequest>::operator()+0xa [c:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory @ 2378] 3e (Inline Function) --------`-------- chrome!std::\_\_1::unique\_ptr<content::NavigationRequest,std::default\_delete[content::NavigationRequest](javascript:void(0);) >::reset+0x19 [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory @ 2633]  

3f 000000c1`7c3fde10 00007ffa`65d48d39 chrome!content::Navigator::DidNavigate+0x671 [c:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigator.cc @ 420]  

40 000000c1`7c3fe030 00007ffa`662261f1 chrome!content::RenderFrameHostImpl::DidCommitNavigationInternal+0x429 [c:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc @ 8884]  

41 000000c1`7c3fe1f0 00007ffa`66225dc9 chrome!content::RenderFrameHostImpl::DidCommitNavigation+0x411 [c:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc @ 9337]  

42 (Inline Function) --------`-------- chrome!base::internal::FunctorTraits<void (content::RenderFrameHostImpl::\*)(content::NavigationRequest \*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>),void>::Invoke+0x2d [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 498] 43 (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<0,void>::MakeItSo+0x35 [c:\b\s\w\ir\cache\builder\src\base\bind\_internal.h @ 637]  

44 (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::\*)(content::NavigationRequest \*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>),base::internal::UnretainedWrapper<content::RenderFrameHostImpl>,content::NavigationRequest \*>,void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>::RunImpl+0x35 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 710] 45 000000c1`7c3fe380 00007ffa`661b0e99 chrome!base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::\*)(content::NavigationRequest \*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>),base::internal::UnretainedWrapper<content::RenderFrameHostImpl>,content::NavigationRequest \*>,void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>::RunOnce+0x49 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 679] 46 (Inline Function) --------`-------- chrome!base::OnceCallback<void (mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);))>::Run+0xd [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 101]  

47 000000c1`7c3fe3d0 00007ffa`689747f6 chrome!content::mojom::NavigationClient\_CommitNavigation\_ForwardToCallback::Accept+0x179 [c:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\navigation\_client.mojom.cc @ 652]  

48 000000c1`7c3fe4d0 00007ffa`68aabe4d chrome!mojo::InterfaceEndpointClient::HandleValidatedMessage+0x2b6 [c:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc @ 549]  

49 000000c1`7c3fe580 00007ffa`68aabd20 chrome!IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnProxyThread+0x10d [c:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc @ 946] 4a (Inline Function) --------`-------- chrome!base::internal::FunctorTraits<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),void>::Invoke+0x69 [c:\b\s\w\ir\cache\builder\src\base\bind\_internal.h @ 498]  

4b (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<0,void>::MakeItSo+0x71 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 637] 4c (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunImpl+0x75 [c:\b\s\w\ir\cache\builder\src\base\bind\_internal.h @ 710]  

4d 000000c1`7c3fe650 00007ffa`687f9849 chrome!base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce+0x90 [c:\b\s\w\ir\cache\builder\src\base\bind\_internal.h @ 683]  

4e (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x15 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 101] 4f 000000c1`7c3fe710 00007ffa`67f9e18f chrome!base::TaskAnnotator::RunTask+0x169 [c:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 163] 50 000000c1`7c3fe850 00007ffa`67f9de3c chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x1df [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 352] 51 000000c1`7c3fea40 00007ffa`68c2e676 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0xcc [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 266] 52 000000c1`7c3feae0 00007ffa`67e45ebe chrome!base::MessagePumpForUI::DoRunLoop+0x76 [c:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 225] 53 000000c1`7c3feb70 00007ffa`65d342ec chrome!base::MessagePumpWin::Run+0xce [c:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 82] 54 000000c1`7c3febe0 00007ffa`65a7b386 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x7c [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 463] 55 000000c1`7c3fec40 00007ffa`6671949b chrome!base::RunLoop::Run+0xb6 [c:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 133] 56 000000c1`7c3fed10 00007ffa`663ac07b chrome!ChromeBrowserMainParts::MainMessageLoopRun+0xdb [c:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc @ 1739] 57 000000c1`7c3feda0 00007ffa`663ac051 chrome!content::BrowserMainLoop::RunMainMessageLoopParts+0x1b [c:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc @ 976] 58 000000c1`7c3fedd0 00007ffa`67afcb43 chrome!content::BrowserMainRunnerImpl::Run+0x11 [c:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc @ 151] 59 000000c1`7c3fee00 00007ffa`67e39772 chrome!content::BrowserMain+0xe3 [c:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc @ 47] 5a (Inline Function) --------`-------- chrome!content::RunBrowserProcessMain+0x43 [c:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc @ 555]  

5b 000000c1`7c3feea0 00007ffa`67e3934a chrome!content::ContentMainRunnerImpl::RunBrowser+0x3f2 [c:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc @ 1059]  

5c 000000c1`7c3fefa0 00007ffa`65c64ef9 chrome!content::ContentMainRunnerImpl::Run+0x14a [c:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc @ 929]  

5d 000000c1`7c3ff040 00007ffa`65c63acd chrome!content::RunContentProcess+0x3c9 [c:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc @ 372]  

5e 000000c1`7c3ff250 00007ffa`65c638fc chrome!content::ContentMain+0x3d [c:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc @ 398]  

5f 000000c1`7c3ff2a0 00007ff7`257d15eb chrome!ChromeMain+0x18c [c:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc @ 144]  

60 000000c1`7c3ff3c0 00007ff7`257d1194 chrome\_exe!GetHandleVerifier+0x1bebb  

61 000000c1`7c3ff490 00007ff7`25859ae2 chrome\_exe!GetHandleVerifier+0x1ba64  

\*\*\* WARNING: Unable to verify checksum for KERNEL32.DLL  

62 000000c1`7c3ff880 00007ffa`9a946fd4 chrome\_exe!IsSandboxedProcess+0x85122  

63 000000c1`7c3ff8c0 00007ffa`9aa7cec1 KERNEL32!BaseThreadInitThunk+0x14  

64 000000c1`7c3ff8f0 00000000`00000000 ntdll!RtlUserThreadStart+0x21

## Attachments

- [repro.html](attachments/repro.html) (text/plain, 379 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 11.2 MB)
- [repro.mkv](attachments/repro.mkv) (application/octet-stream, 1.8 MB)
- Screen Shot 2021-01-18 at 11.26.25.png (image/png, 81.2 KB)

## Timeline

### ch...@gmail.com (2021-01-12)

[Comment Deleted]

### [Deleted User] (2021-01-12)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-01-12)

This is similar to https://crbug.com/chromium/1114556.

### xi...@chromium.org (2021-01-12)

Thanks for the report! And thanks for providing extra pointer to https://crbug.com/1114556. sahel@, could you take a look at this crash too? Thanks!

link to the crash: https://crash.corp.google.com/browse?q=ReportID%3D%273b2d5b5dfda73019%27&stbtiq=&reportid=&index=0

[Monorail components: Blink>Payments]

### ro...@chromium.org (2021-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-14)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@chromium.org (2021-01-18)

I cannot reproduce the issue using the steps in the bug description. (I tried both Windows and Linux, also Chrome Stable and Dev 89.0.4385.0)
Please see the recording attached. 

By looking at the crash trace I have a tentative fix, however I cannot confirm it without being able to repro the issue.

chromium.khalil@ could you please answer the following questions?
1-Are you able to produce the issue deterministically?
2-Is the issue reproducible on Chrome Stable?
3-Have you made any changes in chrome://flags?

### sa...@chromium.org (2021-01-18)

Forgot to add the video in https://crbug.com/chromium/1165624#c9. Actually attaching it here.

### sa...@chromium.org (2021-01-18)

chromium.khalil@ the bug description suggests that the issue happens on Mac and Windows. The recording however looks like to be from Mac?
Could you please confirm whether or not the issue is reproducible on Windows?

### ch...@gmail.com (2021-01-18)

Hmm... you need to enable chrome://flags/#enable-portals and chrome://flags/#enable-portals-cross-origin.

### ch...@gmail.com (2021-01-18)

1-Are you able to produce the issue deterministically?
> Yes
2-Is the issue reproducible on Chrome Stable?
> Yes
3-Have you made any changes in chrome://flags?
enable #enable-portals and #enable-portals-cross-origin

I was able to repro this on Windows.

### ma...@chromium.org (2021-01-18)

Sahel, try enabling the two "portals" flags in about://flags. I could reproduce it with the two flags enabled.

### sa...@chromium.org (2021-01-18)

Thank you chromium.khalil@ for the prompt response and maxlg@ for trying the repro with and without the flags.

I confirm that with #enable-portals and #enable-portals-cross-origin flags enabled I can reproduce the issue. Since the issue is only reproducible by enabling portal flags and is not a recent regression (reproducible on current Chrome stable) I don't think it should be a release blocker, I also don't think it has high security severity. 



### sa...@chromium.org (2021-01-18)

[Description Changed]

### ch...@gmail.com (2021-01-18)

Sometimes, I can repro it without enabling flags with using https://lbstyle.github.io/o.html (It does take several attempts to repro)

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a1a3f9552ce156e3cc3bd0207e53b78609e4b07a

commit a1a3f9552ce156e3cc3bd0207e53b78609e4b07a
Author: Sahel Sharify <sahel@chromium.org>
Date: Tue Jan 19 19:34:07 2021

[Web Payment]PR_sheet_controller should not update views during PR abort

Similar to crbug.com/993223
PaymentRequestSheetController::UpdateHeaderView gets called after the
payment request(PR) has been aborted. The fix for crbug.com/993223 early
returns in DidFinishNavigation which is the caller of UpdateHeaderView.
That's why calling UpdateHeaderView from a different function (e.g.
DidChangeVisibleSecurityState in the case of crbug.com/1165624) still
reproduces the issue.

This CL early returns in all PaymentRequestSheetController's
Update...View functions when the PR is being aborted.

Bug: 1165624
Change-Id: Ie6f8f8ff6e72ef16878aa8dc3f15e19dea1587e1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2635074
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Sahel Sharify <sahel@chromium.org>
Cr-Commit-Position: refs/heads/master@{#844843}

[modify] https://crrev.com/a1a3f9552ce156e3cc3bd0207e53b78609e4b07a/chrome/browser/ui/views/payments/payment_request_sheet_controller.cc


### ch...@gmail.com (2021-01-20)

Unable to repro this on Canary 90.0.4394.0. Fixed.

### sa...@chromium.org (2021-01-20)

Thank you chromium.khalil@ for confirming the fix.

The fix in https://crbug.com/chromium/1165624#c18 is first landed in 90.0.4394.0 on which the reporter has confirmed the fix. I let the code to be in Canary for 2 days and will merge request to M89 on Friday.

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### sa...@chromium.org (2021-01-22)

I request to merge the fix in https://crbug.com/chromium/1165624#c18 to M89. The fix has been in Canary for two days.

### [Deleted User] (2021-01-23)

Your change meets the bar and is auto-approved for M89. Please go ahead and merge the CL to branch 4389 (refs/branch-heads/4389) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-01-25)

[Bulk Edit]Please go ahead and merge the CL to branch 4389 (refs/branch-heads/4389) manually, So that the change would be picked as part of this week Dev release.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1b5af00432c9cff1670b7e4d9565f2f1b881cb7d

commit 1b5af00432c9cff1670b7e4d9565f2f1b881cb7d
Author: Sahel Sharify <sahel@chromium.org>
Date: Mon Jan 25 16:38:35 2021

[Merge M-89][Web Payment]PR_sheet_controller should not update views during PR abort

Similar to crbug.com/993223
PaymentRequestSheetController::UpdateHeaderView gets called after the
payment request(PR) has been aborted. The fix for crbug.com/993223 early
returns in DidFinishNavigation which is the caller of UpdateHeaderView.
That's why calling UpdateHeaderView from a different function (e.g.
DidChangeVisibleSecurityState in the case of crbug.com/1165624) still
reproduces the issue.

This CL early returns in all PaymentRequestSheetController's
Update...View functions when the PR is being aborted.

(cherry picked from commit a1a3f9552ce156e3cc3bd0207e53b78609e4b07a)

Bug: 1165624
Change-Id: Ie6f8f8ff6e72ef16878aa8dc3f15e19dea1587e1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2635074
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Sahel Sharify <sahel@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#844843}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2647645
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/branch-heads/4389@{#200}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/1b5af00432c9cff1670b7e4d9565f2f1b881cb7d/chrome/browser/ui/views/payments/payment_request_sheet_controller.cc


### da...@chromium.org (2021-01-25)

Marking fixed since the change has been merged. I'll verify the change once it's in Dev.

### [Deleted User] (2021-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-10)

sahel@ as I understand it, Portals was in an origin trial which is no longer active (per https://crbug.com/chromium/1158376). Is that the case? If so I'd like to update the Security_Impact label here to None, which will affect what we do in terms of release notes, CVE filing and merges. Please confirm. Thanks!

(It would remain High severity; possibly even Critical, but as it would be impact None this would make little difference to anything).

### ad...@google.com (2021-02-10)

sahel@ please also confirm that this is entirely dependent on Portals and there's no chance that this is exploitable without Portals being enabled.

### sa...@chromium.org (2021-02-10)

The reproduction case from bug report does needs  #enable-portals and #enable-portals-cross-origin flags enabled. However per  reporter's https://crbug.com/chromium/1165624#c17 the issue is reproducible on https://lbstyle.github.io/o.html without enabling portal flags (several attempts needed).

That being said I cannot confirm that the issue is entirely dependent on Portals.

### am...@google.com (2021-02-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-10)

Congratulations, Khalil - the VRP Panel has decided to award you $15,000 for this report. Nice work! 

### ad...@google.com (2021-02-10)

Thanks sahel@. chromium.khalil@, and sahel@, do either of you have an idea whether this is reproducible on M88? (even sometimes?)

### sa...@chromium.org (2021-02-10)

Yes it is reproducible on M88 since the fix is merged to M89 only.

### ad...@chromium.org (2021-02-10)

Thanks.

In that case:
- adjusting impact to Security_Impact-Stable
- adjusting severity to Critical, since this appears to be browser process memory corruption directly achievable from HTML content with no UI interaction
- approving merge to M88, branch 4389. Please go ahead and merge sometime before the end of Thursday PST, so we can get this into next week's stable refresh.

### ad...@google.com (2021-02-10)

sahel@ has pointed out that all known repros do involve a user gesture, so bumping down to High again.

### sa...@chromium.org (2021-02-10)

Yes, a user gesture is mandatory for triggering payment request UI.


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/db3b5f8d1cdfbc693827b05e341e1246fc88634a

commit db3b5f8d1cdfbc693827b05e341e1246fc88634a
Author: Sahel Sharify <sahel@chromium.org>
Date: Wed Feb 10 22:24:00 2021

[Merge to M88][Web Payment]PR_sheet_controller should not update views during PR abort

Similar to crbug.com/993223
PaymentRequestSheetController::UpdateHeaderView gets called after the
payment request(PR) has been aborted. The fix for crbug.com/993223 early
returns in DidFinishNavigation which is the caller of UpdateHeaderView.
That's why calling UpdateHeaderView from a different function (e.g.
DidChangeVisibleSecurityState in the case of crbug.com/1165624) still
reproduces the issue.

This CL early returns in all PaymentRequestSheetController's
Update...View functions when the PR is being aborted.

(cherry picked from commit a1a3f9552ce156e3cc3bd0207e53b78609e4b07a)

Bug: 1165624
Change-Id: Ie6f8f8ff6e72ef16878aa8dc3f15e19dea1587e1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2635074
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Sahel Sharify <sahel@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#844843}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2686273
Cr-Commit-Position: refs/branch-heads/4324@{#2162}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/db3b5f8d1cdfbc693827b05e341e1246fc88634a/chrome/browser/ui/views/payments/payment_request_sheet_controller.cc


### jo...@chromium.org (2021-02-11)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-13)

[Empty comment from Monorail migration]

### ja...@google.com (2021-02-15)

[Empty comment from Monorail migration]

### gi...@google.com (2021-02-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4c8fb4994cd1f2be91a3e0aee6fb5132f6ff5f36

commit 4c8fb4994cd1f2be91a3e0aee6fb5132f6ff5f36
Author: Sahel Sharify <sahel@chromium.org>
Date: Tue Feb 16 18:14:24 2021

[M86-LTS][Web Payment]PR_sheet_controller should not update views during PR abort

Similar to crbug.com/993223
PaymentRequestSheetController::UpdateHeaderView gets called after the
payment request(PR) has been aborted. The fix for crbug.com/993223 early
returns in DidFinishNavigation which is the caller of UpdateHeaderView.
That's why calling UpdateHeaderView from a different function (e.g.
DidChangeVisibleSecurityState in the case of crbug.com/1165624) still
reproduces the issue.

This CL early returns in all PaymentRequestSheetController's
Update...View functions when the PR is being aborted.

(cherry picked from commit a1a3f9552ce156e3cc3bd0207e53b78609e4b07a)

Bug: 1165624
Change-Id: Ie6f8f8ff6e72ef16878aa8dc3f15e19dea1587e1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2635074
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Sahel Sharify <sahel@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#844843}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2692922
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Sahel Sharify <sahel@chromium.org>
Commit-Queue: Jana Grill <janagrill@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1542}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/4c8fb4994cd1f2be91a3e0aee6fb5132f6ff5f36/chrome/browser/ui/views/payments/payment_request_sheet_controller.cc


### ja...@google.com (2021-02-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-22)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1165624?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054420)*
