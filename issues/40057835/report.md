# Security: webgl heap-buffer-overflow getDrawSubresourceSerial

| Field | Value |
|-------|-------|
| **Issue ID** | [40057835](https://issues.chromium.org/issues/40057835) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | sy...@chromium.org |
| **Created** | 2021-11-05 |
| **Bounty** | $5,000.00 |

## Description

On Windows 10 - Chrome Stable Version 95.0.4638.69
has to be launched using --no-sandbox --disable-gpu-sandbox --disable-gpu

2:036> r
rax=aaaaaaaaaaaaaaaa rbx=0000028bbf193f68 rcx=baadf00d00000004
rdx=00000000abababab rsi=000000e4659fdc28 rdi=0000028bbf1940f8
rip=00007ffbe9e84e50 rsp=000000e4659fdb98 rbp=0000000000000001
 r8=0000028bbf10a1f8  r9=0000000000000000 r10=0000000000000000
r11=0000000000000001 r12=00007ffbe9e16514 r13=0000000000000000
r14=0000028bbf18c24c r15=0000000000200200
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
libglesv2!rx::vk::`anonymous namespace'::GetImageLayerCountForView [inlined in libglesv2!rx::vk::GetLayerMode]:
00007ffb`e9e84e50 448b81a0000000  mov     r8d,dword ptr [rcx+0A0h] ds:baadf00d`000000a4=????????
2:036> k
 # Child-SP          RetAddr               Call Site
00 (Inline Function) --------`--------     libglesv2!rx::vk::`anonymous namespace'::GetImageLayerCountForView [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_helpers.cpp @ 615] 
01 000000e4`659fdb98 00007ffb`e9e2666a     libglesv2!rx::vk::GetLayerMode [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_helpers.cpp @ 7386] 
02 (Inline Function) --------`--------     libglesv2!rx::RenderTargetVk::getSubresourceSerialImpl+0xf [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\RenderTargetVk.cpp @ 78] 
03 000000e4`659fdba0 00007ffb`e9e15fbe     libglesv2!rx::RenderTargetVk::getDrawSubresourceSerial+0x2a [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\RenderTargetVk.cpp @ 86] 
04 000000e4`659fdc00 00007ffb`e9e16299     libglesv2!rx::FramebufferVk::updateDepthStencilAttachmentSerial+0x3e [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp @ 1715] 
05 (Inline Function) --------`--------     libglesv2!rx::FramebufferVk::updateDepthStencilAttachment+0x84 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp @ 1704] 
06 000000e4`659fdc60 00007ffb`e9a7f500     libglesv2!rx::FramebufferVk::syncState+0x169 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp @ 1830] 
07 000000e4`659fde70 00007ffb`e9ac0577     libglesv2!gl::Framebuffer::syncState+0x40 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Framebuffer.cpp @ 2051] 
08 (Inline Function) --------`--------     libglesv2!gl::State::syncDirtyObjects+0x2a [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\State.h @ 1186] 
09 000000e4`659fdeb0 00007ffb`e9a5e497     libglesv2!gl::State::syncDirtyObject+0xc7 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\State.cpp @ 3439] 
0a 000000e4`659fdf10 00007ffb`e9a1d26f     libglesv2!gl::Context::invalidateFramebuffer+0x77 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp @ 4770] 
0b 000000e4`659fdf70 00007ffb`9a508260     libglesv2!GL_InvalidateFramebuffer+0x8f [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp @ 1657] 
0c 000000e4`659fdfd0 00007ffb`942ea692     chrome!gpu::gles2::GLES2DecoderPassthroughImpl::DoDiscardFramebufferEXT+0xc0 [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc @ 4746] 
0d (Inline Function) --------`--------     chrome!gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl+0xe6 [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc @ 858] 
0e 000000e4`659fe040 00007ffb`93b41c05     chrome!gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands+0x112 [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc @ 796] 
0f 000000e4`659fe0b0 00007ffb`93b40cf9     chrome!gpu::CommandBufferService::Flush+0xe5 [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc @ 73] 
10 (Inline Function) --------`--------     chrome!gpu::CommandBufferStub::OnAsyncFlush+0xb3 [C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc @ 498] 
11 000000e4`659fe1c0 00007ffb`93b409fc     chrome!gpu::CommandBufferStub::ExecuteDeferredRequest+0x159 [C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc @ 149] 
12 000000e4`659fe300 00007ffb`941eaaa9     chrome!gpu::GpuChannel::ExecuteDeferredRequest+0xcc [C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc @ 669] 
13 (Inline Function) --------`--------     chrome!base::internal::FunctorTraits<void (content::BackgroundSyncOpScheduler::*)(base::OnceCallback<void ()>),void>::Invoke+0x36 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 509] 
14 (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<1,void>::MakeItSo+0x4d [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 668] 
15 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::BindState<void (content::BackgroundSyncOpScheduler::*)(base::OnceCallback<void ()>),base::WeakPtr<content::BackgroundSyncOpScheduler>,base::OnceCallback<void ()> >,void ()>::RunImpl+0x4d [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 721] 
16 000000e4`659fe3a0 00007ffb`95672513     chrome!base::internal::Invoker<base::internal::BindState<void (content::BackgroundSyncOpScheduler::*)(base::OnceCallback<void ()>),base::WeakPtr<content::BackgroundSyncOpScheduler>,base::OnceCallback<void ()> >,void ()>::RunOnce+0x69 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 694] 
17 (Inline Function) --------`--------     chrome!base::OnceCallback<void ()>::Run+0x22 [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 99] 
18 000000e4`659fe3f0 00007ffb`95d2dd2d     chrome!gpu::Scheduler::RunNextTask+0x803 [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc @ 688] 
19 (Inline Function) --------`--------     chrome!base::OnceCallback<void ()>::Run+0x10 [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 99] 
1a 000000e4`659fe530 00007ffb`95d2ce43     chrome!base::TaskAnnotator::RunTask+0x1dd [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 178] 
1b (Inline Function) --------`--------     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x217 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 360] 
1c 000000e4`659fe680 00007ffb`94a2fbe9     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x2a3 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 260] 
1d 000000e4`659fe800 00007ffb`93ee2726     chrome!base::MessagePumpDefault::Run+0xc9 [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc @ 41] 
1e 000000e4`659fe8b0 00007ffb`93fc7326     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x86 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 470] 
1f 000000e4`659fe920 00007ffb`96627fae     chrome!base::RunLoop::Run+0x1a6 [C:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 136] 
20 000000e4`659fea30 00007ffb`93e8a8b9     chrome!content::GpuMain+0x42e [C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc @ 427] 
21 (Inline Function) --------`--------     chrome!content::RunOtherNamedProcessTypeMain+0xb7 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 637] 
22 000000e4`659fedb0 00007ffb`93ea1962     chrome!content::ContentMainRunnerImpl::Run+0x1a9 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 974] 
23 (Inline Function) --------`--------     chrome!content::RunContentProcess+0x11d [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 390] 
24 000000e4`659fee80 00007ffb`93ea099f     chrome!content::ContentMain+0x152 [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 418] 
25 000000e4`659ff070 00007ff7`74535742     chrome!ChromeMain+0x18f [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 175] 
26 000000e4`659ff180 00007ff7`745352dc     chrome_exe!MainDllLoader::Launch+0x302 [C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc @ 169] 
27 000000e4`659ff400 00007ff7`7457ca92     chrome_exe!wWinMain+0xc1c [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc @ 382] 
28 (Inline Function) --------`--------     chrome_exe!invoke_main+0x21 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118] 
29 000000e4`659ff830 00007ffc`4cd17034     chrome_exe!__scrt_common_main_seh+0x106 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
2a 000000e4`659ff870 00007ffc`4cf02651     KERNEL32!BaseThreadInitThunk+0x14
2b 000000e4`659ff8a0 00000000`00000000     ntdll!RtlUserThreadStart+0x21


Also attached ASAN log from asan-linux-release-936833.

## Attachments

- [getDrawSubresourceSerial.html](attachments/getDrawSubresourceSerial.html) (text/plain, 767 B)
- [asan.log](attachments/asan.log) (text/plain, 12.2 KB)

## Timeline

### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-11-05)

$ ./builds/asan-linux-release-936784-97.0.4688.0/chrome ./pocs/1267424/getDrawSubresourceSerial.html

=================================================================                                                                                                                                                                                                                                                               
==2266517==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6060000c8ae8 at pc 0x7f7112c0808d bp 0x7ffcfa4f6600 sp 0x7ffcfa4f65f8                                                                                                                                                                                     
READ of size 8 at 0x6060000c8ae8 thread T0 (chrome)                                                                                                                                                                                                                                                                             
    #0 0x7f7112c0808c in rx::RenderTargetVk::getDrawSubresourceSerial() const third_party/angle/src/libANGLE/renderer/vulkan/RenderTargetVk.cpp:86:37                                                                                                                                                                           
    #1 0x7f7112bcd43f in rx::FramebufferVk::updateDepthStencilAttachmentSerial(rx::ContextVk*) third_party/angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp:1711:68                                                                                                                                                         
    #2 0x7f7112bcdac7 in updateDepthStencilAttachment third_party/angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp:1700:5                                                                                                                                                                                                   
    #3 0x7f7112bcdac7 in rx::FramebufferVk::syncState(gl::Context const*, unsigned int, angle::BitSetT<28ul, unsigned long, unsigned long> const&, gl::Command) third_party/angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp:1826:17                 
    #4 0x7f71125f49db in gl::Framebuffer::syncState(gl::Context const*, unsigned int, gl::Command) const third_party/angle/src/libANGLE/Framebuffer.cpp:2056:9                                                                                           
    #5 0x7f7112713511 in syncDirtyObjects third_party/angle/src/libANGLE/State.h:1181:9                                                                                                                                         
    #6 0x7f7112713511 in gl::State::syncDirtyObject(gl::Context const*, unsigned int) third_party/angle/src/libANGLE/State.cpp:3480:12                                                     
    #7 0x7f7112580788 in gl::Context::invalidateFramebuffer(unsigned int, int, unsigned int const*) third_party/angle/src/libANGLE/Context.cpp:4808:5                                      
    #8 0x7f71124eaa6f in GL_InvalidateFramebuffer third_party/angle/src/libGLESv2/entry_points_gles_3_0_autogen.cpp:1739:22                                                                
    #9 0x55a569a9ed15 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDiscardFramebufferEXT(unsigned int, int, unsigned int const volatile*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc                                                                                                                    
    #10 0x55a569a3620f in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858:20                             
    #11 0x55a569eabf95 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:70:18                                                                                                                                     
    #12 0x55a569e9fa8f in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) gpu/ipc/service/command_buffer_stub.cc:500:22                  
    #13 0x55a569e9f039 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:152:7                     
    #14 0x55a569eb2a72 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) gpu/ipc/service/gpu_channel.cc:666:13                                
    #15 0x55a569ebf2be in Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> > base/bind_internal.h:569:12                                                                                                
    #16 0x55a569ebf2be in void base::internal::InvokeHelper<true, void>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestPar
ams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) base/bind_internal.h:769:5                                                                                                                                
    #17 0x55a5688be1d7 in Run base/callback.h:142:12                                                                                                                                       
    #18 0x55a5688be1d7 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:685:26                                                                                                                          
    #19 0x55a5642b9913 in Run base/callback.h:142:12                                                                                                                                                                            
    #20 0x55a5642b9913 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:157:32                                                                                    
    #21 0x55a5642f57a8 in RunTask<> base/task/common/task_annotator.h:115:5                                                                                                                                                     
    #22 0x55a5642f57a8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:354:21                                                             
    #23 0x55a5642f5157 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30                                                                                                 
    #24 0x55a5642f5ee1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc                           
    #25 0x55a5641b071a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48                                                                                                
    #26 0x55a5642f65ab in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:12                       
    #27 0x55a5642325f9 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14                                                                                                                 
    #28 0x55a5700f5ba5 in content::GpuMain(content::MainFunctionParams const&) content/gpu/gpu_main.cc:439:14                                                                                                                                                                           
    #29 0x55a563075294 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:615:14                                                                                                                                                              
    #30 0x55a5630792f1 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:1006:10                                                                                         
    #31 0x55a5630728c7 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36                                                                                                  
    #32 0x55a5630744e2 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10                                                                                                            
    #33 0x55a5560f7825 in ChromeMain chrome/app/chrome_main.cc:172:12                                                                                                                                                                                    
    #34 0x7f7119ce0e49 in __libc_start_main csu/../csu/libc-start.c:314:16                                                                                                                                                      
                                                                                                                                                                                           
0x6060000c8ae8 is located 240 bytes to the right of 56-byte region [0x6060000c89c0,0x6060000c89f8)                                                                                                                              
allocated by thread T0 (chrome) here:                                                                                                                                                                       
    #0 0x55a5560f4fbd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3                                                                                                                                         
    #1 0x7f7112c76871 in __libcpp_operator_new<unsigned long> buildtools/third_party/libc++/trunk/include/new:235:10                                                                                        
    #2 0x7f7112c76871 in __libcpp_allocate buildtools/third_party/libc++/trunk/include/new:261:10                                                                                                           
    #3 0x7f7112c76871 in allocate buildtools/third_party/libc++/trunk/include/__memory/allocator.h:82:38                                                                                   
    #4 0x7f7112c76871 in allocate buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:261:20                                                                                            
    #5 0x7f7112c76871 in __split_buffer buildtools/third_party/libc++/trunk/include/__split_buffer:314:29                                                                                  
    #6 0x7f7112c76871 in std::__1::vector<rx::RenderTargetVk, std::__1::allocator<rx::RenderTargetVk> >::__append(unsigned long) buildtools/third_party/libc++/trunk/include/vector:1094:53
    #7 0x7f7112c711b7 in resize buildtools/third_party/libc++/trunk/include/vector:2025:15                                                                                                 
    #8 0x7f7112c711b7 in rx::TextureVk::initSingleLayerRenderTargets(rx::ContextVk*, unsigned int, gl::LevelIndexWrapper<int>, gl::RenderToTextureImageIndex) third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:2410:19                                                                                              
    #9 0x7f7112c70e41 in rx::TextureVk::getAttachmentRenderTarget(gl::Context const*, unsigned int, gl::ImageIndex const&, int, rx::FramebufferAttachmentRenderTarget**) third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:2330:9                                                                                    
    #10 0x7f7112bcda7c in getRenderTargetImpl third_party/angle/src/libANGLE/FramebufferAttachment.h:273:23                                                                                                 
    #11 0x7f7112bcda7c in getRenderTarget<rx::RenderTargetVk> third_party/angle/src/libANGLE/FramebufferAttachment.h:154:16                                                                
    #12 0x7f7112bcda7c in updateCachedRenderTarget third_party/angle/src/libANGLE/renderer/RenderTargetCache.h:163:9                                                                                                                                                                    
    #13 0x7f7112bcda7c in updateDepthStencilRenderTarget third_party/angle/src/libANGLE/renderer/RenderTargetCache.h:149:12                                                                
    #14 0x7f7112bcda7c in updateDepthStencilAttachment third_party/angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp:1697:5                                                             
    #15 0x7f7112bcda7c in rx::FramebufferVk::syncState(gl::Context const*, unsigned int, angle::BitSetT<28ul, unsigned long, unsigned long> const&, gl::Command) third_party/angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp:1826:17                                               
    #16 0x7f71125f49db in gl::Framebuffer::syncState(gl::Context const*, unsigned int, gl::Command) const third_party/angle/src/libANGLE/Framebuffer.cpp:2056:9                                                                                                                         
    #17 0x7f7112713511 in syncDirtyObjects third_party/angle/src/libANGLE/State.h:1181:9                                                                                                   
    #18 0x7f7112713511 in gl::State::syncDirtyObject(gl::Context const*, unsigned int) third_party/angle/src/libANGLE/State.cpp:3480:12                                                    
    #19 0x7f7112580788 in gl::Context::invalidateFramebuffer(unsigned int, int, unsigned int const*) third_party/angle/src/libANGLE/Context.cpp:4808:5                                     
    #20 0x7f71124eaa6f in GL_InvalidateFramebuffer third_party/angle/src/libGLESv2/entry_points_gles_3_0_autogen.cpp:1739:22                                                                                                                                                            
    #21 0x55a569a9ed15 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDiscardFramebufferEXT(unsigned int, int, unsigned int const volatile*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc                                                                           
    #22 0x55a569a3620f in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858:20                                                            
    #23 0x55a569eabf95 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:70:18                                                                                                                                     
    #24 0x55a569e9fa8f in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) gpu/ipc/service/command_buffer_stub.cc:500:22                                                                                                                  
    #25 0x55a569e9f039 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:152:7                                                                                                                  
    #26 0x55a569eb2a72 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) gpu/ipc/service/gpu_channel.cc:666:13                                                                                                                             
    #27 0x55a569ebf2be in Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> > base/bind_internal.h:569:12                                                        
    #28 0x55a569ebf2be in void base::internal::InvokeHelper<true, void>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestPar
ams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) base/bind_internal.h:769:5                                                                                                                                                               
    #29 0x55a5688be1d7 in Run base/callback.h:142:12                                                                                                                                                                                                                                    
    #30 0x55a5688be1d7 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:685:26                                                                                                                                                                                  
    #31 0x55a5642b9913 in Run base/callback.h:142:12                                                                                                                                                                                                                                    
    #32 0x55a5642b9913 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:157:32                                                                                                                                                                
    #33 0x55a5642f57a8 in RunTask<> base/task/common/task_annotator.h:115:5                                                                                                                                                                                                             
    #34 0x55a5642f57a8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:354:21                                                             
    #35 0x55a5642f5157 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30                                                                                                 
    #36 0x55a5642f5ee1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc                                                                                                                           
    #37 0x55a5641b071a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48                                                                                                                                                        
    #38 0x55a5642f65ab in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:12                                                                                                                       
    #39 0x55a5642325f9 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14                                                                                                                                                                                             
    #40 0x55a5700f5ba5 in content::GpuMain(content::MainFunctionParams const&) content/gpu/gpu_main.cc:439:14                                                                                                                                                                                                                   
    #41 0x55a563075294 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:615:14                                                                                                                                                              
    #42 0x55a5630792f1 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:1006:10                                                                                                                                                                     
    #43 0x55a5630728c7 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36                                                                                                                                 
    #44 0x55a5630744e2 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10                                                                                                                                                                    
    #45 0x55a5560f7825 in ChromeMain chrome/app/chrome_main.cc:172:12                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                        
SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/angle/src/libANGLE/renderer/vulkan/RenderTargetVk.cpp:86:37 in rx::RenderTargetVk::getDrawSubresourceSerial() const    

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5146868130316288.

### va...@chromium.org (2021-11-05)

Repros with:
Chromium	96.0.4664.0 (Developer Build) (64-bit)
Revision	85b0bd07c2597f03beeefb8b33fcfcee47dc6937-refs/heads/main@{#929513}

$ ./builds/asan-linux-release-929513-96.0.4664.0/chrome ./pocs/1267424/getDrawSubresourceSerial.html

### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-11-05)

Does not repro with:

Chromium	95.0.4638.0 (Developer Build) (64-bit)
Revision	bf9bdebd10ff5b89d2db8ce2bce69cccf3f88dae-refs/heads/main@{#920012}

$ ./builds/asan-linux-release-920012-95.0.4638.0/chrome ./pocs/1267424/getDrawSubresourceSerial.html 


### va...@chromium.org (2021-11-05)

(Not sure about other platforms)

### [Deleted User] (2021-11-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-07)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2021-11-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/ef93b32c10d8d4ed0017fc54447ad62d5cf06c00

commit ef93b32c10d8d4ed0017fc54447ad62d5cf06c00
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Nov 09 05:26:13 2021

Vulkan: Fix deferred clears vs invalidate

In this scenario:

- Clear color
- Invalidate depth
- Clear color

The invalidate step flushed the deferred color clear, but the following
clear did not expect an open render pass without any draw calls in it.

This change fixes this issue, while simultaneously optimizing invalidate
by making sure the clears accumulated during syncState() are redeferred
instead of flushed.

This issue was discovered in
https://chromium-review.googlesource.com/c/angle/angle/+/3266176 where,
as part of an unrelated fix, an accidental render pass closure is
removed.

Bug: chromium:1267424
Change-Id: Icfc0a53dbf84e6339ee23960ed847444830054e6
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3266178
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/ef93b32c10d8d4ed0017fc54447ad62d5cf06c00/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/ef93b32c10d8d4ed0017fc54447ad62d5cf06c00/src/tests/gl_tests/StateChangeTest.cpp


### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/91d3647325f7334f0fc960dd774af400379f3a8b

commit 91d3647325f7334f0fc960dd774af400379f3a8b
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Nov 08 21:27:20 2021

Fix invalidation of GL_FRAMEBUFFER invalidating READ FBO

Per spec, GL_FRAMEBUFFER means GL_DRAW_FRAMEBUFFER for
glInvalidateFramebuffer.

Bug: chromium:1267424
Change-Id: I8c9ab61ecdbd4ccee4262dc8559b2feb02b4837c
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3266176
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/91d3647325f7334f0fc960dd774af400379f3a8b/src/tests/gl_tests/FramebufferTest.cpp
[modify] https://crrev.com/91d3647325f7334f0fc960dd774af400379f3a8b/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/91d3647325f7334f0fc960dd774af400379f3a8b/src/libANGLE/Context.cpp


### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/8848f372f654c924ee3bff226b109ab135fc5622

commit 8848f372f654c924ee3bff226b109ab135fc5622
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Nov 09 05:26:13 2021

Canary: Vulkan: Fix deferred clears vs invalidate

In this scenario:

- Clear color
- Invalidate depth
- Clear color

The invalidate step flushed the deferred color clear, but the following
clear did not expect an open render pass without any draw calls in it.

This change fixes this issue, while simultaneously optimizing invalidate
by making sure the clears accumulated during syncState() are redeferred
instead of flushed.

This issue was discovered in
https://chromium-review.googlesource.com/c/angle/angle/+/3266176 where,
as part of an unrelated fix, an accidental render pass closure is
removed.

Bug: chromium:1267424
Change-Id: Icfc0a53dbf84e6339ee23960ed847444830054e6
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3266178
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270995
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/8848f372f654c924ee3bff226b109ab135fc5622/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/8848f372f654c924ee3bff226b109ab135fc5622/src/tests/gl_tests/StateChangeTest.cpp


### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/b33796c345fb01c24dc54e63c831a4d236a680e5

commit b33796c345fb01c24dc54e63c831a4d236a680e5
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Nov 08 21:27:20 2021

Canary: Fix invalidation of GL_FRAMEBUFFER invalidating READ FBO

Per spec, GL_FRAMEBUFFER means GL_DRAW_FRAMEBUFFER for
glInvalidateFramebuffer.

Bug: chromium:1267424
Change-Id: I8c9ab61ecdbd4ccee4262dc8559b2feb02b4837c
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3266176
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270996
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/b33796c345fb01c24dc54e63c831a4d236a680e5/src/tests/gl_tests/FramebufferTest.cpp
[modify] https://crrev.com/b33796c345fb01c24dc54e63c831a4d236a680e5/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/b33796c345fb01c24dc54e63c831a4d236a680e5/src/libANGLE/Context.cpp


### sy...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-09)

updating OS since this is a RBS issue so release team can appropriately track 

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/91d4d4d320061e29c6b8f99d85df02c1384734c2

commit 91d4d4d320061e29c6b8f99d85df02c1384734c2
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Nov 09 19:33:36 2021

Roll ANGLE from 67a8cf07a740 to d3e677167124 (5 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/67a8cf07a740..d3e677167124

2021-11-09 j.vigil@samsung.com EGL: EGL_KHR_lock_surface3
2021-11-09 sdefresne@chromium.org [ios] Remove support for building with Xcode clang
2021-11-09 syoussefi@chromium.org Fix invalidation of GL_FRAMEBUFFER invalidating READ FBO
2021-11-09 syoussefi@chromium.org Add test for texture state change bug
2021-11-09 syoussefi@chromium.org Vulkan: Fix deferred clears vs invalidate

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jmadill@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1266466,chromium:1267424,chromium:1267624
Tbr: jmadill@google.com
Test: Test: angle_end2end_test --gtest_filter=EGLLockSurface3Test
Change-Id: I611b96a77dedf1a56353fa41bd31aa2806c3ea3d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3271112
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#939953}

[modify] https://crrev.com/91d4d4d320061e29c6b8f99d85df02c1384734c2/DEPS


### sy...@chromium.org (2021-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-10)

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2021-11-10)

1. See https://crbug.com/chromium/1267424#c10
2. The following two: https://chromium-review.googlesource.com/c/angle/angle/+/3266178 and https://chromium-review.googlesource.com/c/angle/angle/+/3266176
3. Earlier today (in 4696), and a special update of Canary was released to make sure we get more testing until tomorrow when the changes are expected to be merged.
4. No
5. N/A
6. N/A

### sr...@google.com (2021-11-10)

Merge approved for M96 branch:4664 pls merge asap

### gi...@appspot.gserviceaccount.com (2021-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/5fb289c7541cfe7e1fb0f34a24668a92f886ffe1

commit 5fb289c7541cfe7e1fb0f34a24668a92f886ffe1
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Nov 08 21:27:20 2021

M96: Fix invalidation of GL_FRAMEBUFFER invalidating READ FBO

Per spec, GL_FRAMEBUFFER means GL_DRAW_FRAMEBUFFER for
glInvalidateFramebuffer.

Bug: chromium:1267424
Change-Id: I8c9ab61ecdbd4ccee4262dc8559b2feb02b4837c
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3266176
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270996
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3271003

[modify] https://crrev.com/5fb289c7541cfe7e1fb0f34a24668a92f886ffe1/src/tests/gl_tests/FramebufferTest.cpp
[modify] https://crrev.com/5fb289c7541cfe7e1fb0f34a24668a92f886ffe1/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/5fb289c7541cfe7e1fb0f34a24668a92f886ffe1/src/libANGLE/Context.cpp


### gi...@appspot.gserviceaccount.com (2021-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/19b0761a27183d3d395aca9c75125badef0acc8e

commit 19b0761a27183d3d395aca9c75125badef0acc8e
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Nov 09 05:26:13 2021

M96: Vulkan: Fix deferred clears vs invalidate

In this scenario:

- Clear color
- Invalidate depth
- Clear color

The invalidate step flushed the deferred color clear, but the following
clear did not expect an open render pass without any draw calls in it.

This change fixes this issue, while simultaneously optimizing invalidate
by making sure the clears accumulated during syncState() are redeferred
instead of flushed.

This issue was discovered in
https://chromium-review.googlesource.com/c/angle/angle/+/3266176 where,
as part of an unrelated fix, an accidental render pass closure is
removed.

Bug: chromium:1267424
Change-Id: Icfc0a53dbf84e6339ee23960ed847444830054e6
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3266178
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270995
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3271002

[modify] https://crrev.com/19b0761a27183d3d395aca9c75125badef0acc8e/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/19b0761a27183d3d395aca9c75125badef0acc8e/src/tests/gl_tests/StateChangeTest.cpp


### go...@chromium.org (2021-11-11)

This will need to merge to M97 as well. 

+amyressler@ (Security TPM)

### [Deleted User] (2021-11-11)

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-11)

Merge approved to M97; please go ahead and merge to branch 4692 as soon as possible. 

### gi...@appspot.gserviceaccount.com (2021-11-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f02b0f1c190702b7b1f98d5b4ec7732e408e2889

commit f02b0f1c190702b7b1f98d5b4ec7732e408e2889
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Nov 08 21:27:20 2021

M97: Fix invalidation of GL_FRAMEBUFFER invalidating READ FBO

Per spec, GL_FRAMEBUFFER means GL_DRAW_FRAMEBUFFER for
glInvalidateFramebuffer.

Bug: chromium:1267424
Change-Id: I8c9ab61ecdbd4ccee4262dc8559b2feb02b4837c
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3266176
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270996
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3271003
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3276040

[modify] https://crrev.com/f02b0f1c190702b7b1f98d5b4ec7732e408e2889/src/tests/gl_tests/FramebufferTest.cpp
[modify] https://crrev.com/f02b0f1c190702b7b1f98d5b4ec7732e408e2889/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/f02b0f1c190702b7b1f98d5b4ec7732e408e2889/src/libANGLE/Context.cpp


### gi...@appspot.gserviceaccount.com (2021-11-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/00c5db3e59847ee46b0c068ead9f01f6d0a0fa3e

commit 00c5db3e59847ee46b0c068ead9f01f6d0a0fa3e
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Nov 09 05:26:13 2021

M97: Vulkan: Fix deferred clears vs invalidate

In this scenario:

- Clear color
- Invalidate depth
- Clear color

The invalidate step flushed the deferred color clear, but the following
clear did not expect an open render pass without any draw calls in it.

This change fixes this issue, while simultaneously optimizing invalidate
by making sure the clears accumulated during syncState() are redeferred
instead of flushed.

This issue was discovered in
https://chromium-review.googlesource.com/c/angle/angle/+/3266176 where,
as part of an unrelated fix, an accidental render pass closure is
removed.

Bug: chromium:1267424
Change-Id: Icfc0a53dbf84e6339ee23960ed847444830054e6
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3266178
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270995
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3271002
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3276039

[modify] https://crrev.com/00c5db3e59847ee46b0c068ead9f01f6d0a0fa3e/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/00c5db3e59847ee46b0c068ead9f01f6d0a0fa3e/src/tests/gl_tests/StateChangeTest.cpp


### sy...@chromium.org (2021-11-12)

Done

### cl...@chromium.org (2021-11-16)

ClusterFuzz testcase 5146868130316288 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### am...@google.com (2021-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-17)

Congratulations, the VRP Panel has decided to award you $5000 for this report. Thank you for reporting this issue to us! 

### sy...@chromium.org (2021-11-19)

See crbug.com/1267027#c35 regarding clusterfuzz failures.

### sy...@chromium.org (2021-11-20)

New failures are unrelated and are tracked in crbug.com/1267697

### am...@google.com (2021-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1267424?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057835)*
