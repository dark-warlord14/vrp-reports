# Security: heap-use-after-free swiftshader getCurrentViewCount

| Field | Value |
|-------|-------|
| **Issue ID** | [40057672](https://issues.chromium.org/issues/40057672) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals, Internals>GPU>SwiftShader |
| **Platforms** | Linux |
| **Reporter** | [Deleted User] |
| **Assignee** | jm...@chromium.org |
| **Created** | 2021-10-21 |
| **Bounty** | $5,000.00 |

## Description

On Windows 10 - Chrome Dev Version - 96.0.4664.18
has to be launched using --no-sandbox --disable-gpu-sandbox --disable-gpu

8:114> r
rax=0000000000000000 rbx=abababababababab rcx=abababababababab
rdx=0000000000000000 rsi=abababababababab rdi=0000000000000c10
rip=00007ffca27f90b0 rsp=0000002fdd7ff550 rbp=0000000000000000
 r8=00000000000000dc  r9=0000000000000210 r10=0000000000000000
r11=0000000000000010 r12=0000000000000000 r13=00007ffc29f69a6f
r14=000001f2ecd8d1b8 r15=000000000000009c
iopl=0         nv up ei pl zr na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
ntdll!RtlAcquireSRWLockExclusive+0x10:
00007ffc`a27f90b0 f0480fba2900    lock bts qword ptr [rcx],0 ds:abababab`abababab=????????????????
8:114> k
 # Child-SP          RetAddr               Call Site
00 0000002f`dd7ff550 00007ffc`29e8681a     ntdll!RtlAcquireSRWLockExclusive+0x10
01 0000002f`dd7ff5c0 00007ffc`29e85639     vk_swiftshader!std::__1::__libcpp_mutex_lock+0xa [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\src\support\win32\thread_win32.cpp @ 78] 
02 0000002f`dd7ff5f0 00007ffc`29bedea6     vk_swiftshader!std::__1::mutex::lock+0x9 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\src\mutex.cpp @ 34] 
03 (Inline Function) --------`--------     vk_swiftshader!std::__1::unique_lock<std::__1::mutex>::unique_lock+0x8 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__mutex_base @ 119] 
04 (Inline Function) --------`--------     vk_swiftshader!marl::lock::lock+0x8 [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\third_party\marl\include\marl\mutex.h @ 75] 
05 (Inline Function) --------`--------     vk_swiftshader!marl::Event::clear+0xc [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\third_party\marl\include\marl\event.h @ 194] 
06 (Inline Function) --------`--------     vk_swiftshader!vk::Query::reset+0xc [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkQueryPool.cpp @ 32] 
07 0000002f`dd7ff620 00007ffc`29bd575e     vk_swiftshader!vk::QueryPool::reset+0x36 [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkQueryPool.cpp @ 210] 
08 0000002f`dd7ff670 00007ffc`29beeaa2     vk_swiftshader!vk::CommandBuffer::submit+0x2e [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp @ 1731] 
09 0000002f`dd7ff6c0 00007ffc`29bee151     vk_swiftshader!vk::Queue::submitQueue+0x262 [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkQueue.cpp @ 220] 
0a 0000002f`dd7ffa90 00007ffc`29bef43a     vk_swiftshader!vk::Queue::taskLoop+0xb1 [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkQueue.cpp @ 281] 
0b (Inline Function) --------`--------     vk_swiftshader!std::__1::__invoke+0xb [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\type_traits @ 3897] 
0c (Inline Function) --------`--------     vk_swiftshader!std::__1::__thread_execute+0xb [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\thread @ 280] 
0d 0000002f`dd7ffb30 00007ffc`29e91730     vk_swiftshader!std::__1::__thread_proxy<std::__1::tuple<std::__1::unique_ptr<std::__1::__thread_struct,std::__1::default_delete<std::__1::__thread_struct> >,void (vk::Queue::*)(marl::Scheduler *),vk::Queue *,marl::Scheduler *> >+0x2a [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\thread @ 293] 
0e 0000002f`dd7ffb70 00007ffc`a16b7034     vk_swiftshader!thread_start<unsigned int (__cdecl*)(void *),1>+0x50 [C:\b\s\w\ir\cache\builder\src\out\Release_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp @ 97] 
0f 0000002f`dd7ffba0 00007ffc`a2822651     KERNEL32!BaseThreadInitThunk+0x14
10 0000002f`dd7ffbd0 00000000`00000000     ntdll!RtlUserThreadStart+0x21


==30820==ERROR: AddressSanitizer: heap-use-after-free on address 0x124231c1309a at pc 0x7ffc219d1d2a bp 0x0062107fe160 sp 0x0062107fe1a8
READ of size 1 at 0x124231c1309a thread T0
==30820==WARNING: Failed to use and restart external symbolizer!
==30820==*** WARNING: Failed to initialize DbgHelp!              ***
==30820==*** Most likely this means that the app is already      ***
==30820==*** using DbgHelp, possibly with incompatible flags.    ***
==30820==*** Due to technical reasons, symbolization might crash ***
==30820==*** or produce wrong results.                           ***
    #0 0x7ffc219d1d29 in rx::ContextVk::getCurrentViewCount C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:5640
    #1 0x7ffc21a1de72 in rx::QueryVk::allocateQuery C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\QueryVk.cpp:127
    #2 0x7ffc21a1ee60 in rx::QueryVk::setupBegin C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\QueryVk.cpp:294
    #3 0x7ffc21a1eff3 in rx::QueryVk::begin C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\QueryVk.cpp:315
    #4 0x7ffc212e977f in gl::Context::beginQuery C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:1323
    #5 0x7ffc21279e43 in GL_BeginQuery C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp:41
    #6 0x7ffbf5eb2fc6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBeginQueryEXT C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:3650
    #7 0x7ffbf5ee8768 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleBeginQueryEXT C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_handlers.cc:1397
    #8 0x7ffbf2140dad in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:858
    #9 0x7ffbf21401f4 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:796
    #10 0x7ffbef00e016 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:70
    #11 0x7ffbec5f8538 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:500
    #12 0x7ffbec5f76ec in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:152
    #13 0x7ffbec6043c2 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:666
    #14 0x7ffbec60f491 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:753
    #15 0x7ffbec2377cd in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:685
    #16 0x7ffbeafc668a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #17 0x7ffbeda9d53f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:358
    #18 0x7ffbeda9cc58 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #19 0x7ffbeda76b47 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:38
    #20 0x7ffbeda9e955 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:463
    #21 0x7ffbeaf46383 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #22 0x7ffbed4b0389 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:440
    #23 0x7ffbe6c6e661 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1006
    #24 0x7ffbe6c6b046 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #25 0x7ffbe6c6c088 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418
    #26 0x7ffbe063147f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172
    #27 0x7ff78f135b44 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #28 0x7ff78f132c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #29 0x7ff78f52d17f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #30 0x7ffca16b7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #31 0x7ffca2822650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x124231c1309a is located 26 bytes inside of 648-byte region [0x124231c13080,0x124231c13308)
freed by thread T0 here:
    #0 0x7ff78f1e227b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffc219f3af7 in rx::FramebufferVk::~FramebufferVk C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp:351
    #2 0x7ffc21355a08 in gl::Framebuffer::~Framebuffer C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Framebuffer.cpp:862
    #3 0x7ffc2140c5b1 in gl::TypedResourceManager<gl::Framebuffer,gl::FramebufferManager,gl::FramebufferID>::deleteObject C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\ResourceManager.cpp:96
    #4 0x7ffc2130b5a9 in gl::Context::deleteFramebuffers C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:6625
    #5 0x7ffc2126ca8f in GL_DeleteFramebuffers C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:845
    #6 0x7ffbf5e9b14c in gpu::gles2::GLES2DecoderPassthroughImpl::DoDeleteFramebuffers C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:1050
    #7 0x7ffbf2140dad in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:858
    #8 0x7ffbf21401f4 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:796
    #9 0x7ffbef00e016 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:70
    #10 0x7ffbec5f8538 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:500
    #11 0x7ffbec5f76ec in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:152
    #12 0x7ffbec6043c2 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:666
    #13 0x7ffbec60f491 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:753
    #14 0x7ffbec2377cd in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:685
    #15 0x7ffbeafc668a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #16 0x7ffbeda9d53f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:358
    #17 0x7ffbeda9cc58 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #18 0x7ffbeda76b47 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:38
    #19 0x7ffbeda9e955 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:463
    #20 0x7ffbeaf46383 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #21 0x7ffbed4b0389 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:440
    #22 0x7ffbe6c6e661 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1006
    #23 0x7ffbe6c6b046 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #24 0x7ffbe6c6c088 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418
    #25 0x7ffbe063147f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172
    #26 0x7ff78f135b44 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #27 0x7ff78f132c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382

previously allocated by thread T0 here:
    #0 0x7ff78f1e237b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffc21f2062a in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffc219dee31 in rx::FramebufferVk::CreateUserFBO C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp:327
    #3 0x7ffc2135328a in gl::Framebuffer::Framebuffer C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Framebuffer.cpp:785
    #4 0x7ffc2140f2f6 in gl::FramebufferManager::AllocateNewObject C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\ResourceManager.cpp:358
    #5 0x7ffc213238f5 in gl::TypedResourceManager<gl::Framebuffer,gl::FramebufferManager,gl::FramebufferID>::checkObjectAllocationImpl<gl::Caps,egl::ShareGroup *> C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\ResourceManager.h:117
    #6 0x7ffc212e7ec7 in gl::FramebufferManager::checkFramebufferAllocation C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\ResourceManager.h:285
    #7 0x7ffc212e8046 in gl::Context::bindDrawFramebuffer C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:1232
    #8 0x7ffc2126a0c1 in GL_BindFramebuffer C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:143
    #9 0x7ffbf5e963e0 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBindFramebuffer C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:451
    #10 0x7ffbf2140dad in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:858
    #11 0x7ffbf21401f4 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:796
    #12 0x7ffbef00e016 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:70
    #13 0x7ffbec5f8538 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:500
    #14 0x7ffbec5f76ec in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:152
    #15 0x7ffbec6043c2 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:666
    #16 0x7ffbec60f491 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:753
    #17 0x7ffbec2377cd in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:685
    #18 0x7ffbeafc668a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #19 0x7ffbeda9d53f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:358
    #20 0x7ffbeda9cc58 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #21 0x7ffbeda76b47 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:38
    #22 0x7ffbeda9e955 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:463
    #23 0x7ffbeaf46383 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #24 0x7ffbed4b0389 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:440
    #25 0x7ffbe6c6e661 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1006
    #26 0x7ffbe6c6b046 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #27 0x7ffbe6c6c088 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp:5640 in rx::ContextVk::getCurrentViewCount
Shadow bytes around the buggy address:
  0x045c77e025c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x045c77e025d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x045c77e025e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x045c77e025f0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x045c77e02600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x045c77e02610: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd
  0x045c77e02620: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x045c77e02630: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x045c77e02640: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x045c77e02650: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x045c77e02660: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==30820==ABORTING

## Attachments

- [getCurrentViewCount.html](attachments/getCurrentViewCount.html) (text/plain, 2.2 KB)

## Timeline

### [Deleted User] (2021-10-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-10-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5172528018161664.

### cl...@chromium.org (2021-10-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-10-22)

Detailed Report: https://clusterfuzz.com/testcase?key=5172528018161664

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  media::VaapiWrapper::PreSandboxInitialization
  content::ContentSandboxHelper::PreSandboxStartup
  gpu::GpuInit::InitializeAndStartSandbox
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=933956

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5172528018161664

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5172528018161664 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2021-10-22)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>GPU>Internals Internals>Media]

### cl...@chromium.org (2021-10-23)

Detailed Report: https://clusterfuzz.com/testcase?key=5172528018161664

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  media::VaapiWrapper::PreSandboxInitialization
  content::ContentSandboxHelper::PreSandboxStartup
  gpu::GpuInit::InitializeAndStartSandbox
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=933956

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5172528018161664

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5172528018161664 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2021-10-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4840676162076672.

### es...@chromium.org (2021-10-25)

(re-running clusterfuzz with correct command line arguments)

[Monorail components: -Internals>Media Internals>GPU>SwiftShader]

### es...@chromium.org (2021-10-26)

Hmm, seems like Clusterfuzz still thinks this is a null deref. Swiftshader folks, can you please take a look?

### [Deleted User] (2021-10-26)

[Empty comment from Monorail migration]

### ni...@google.com (2021-10-26)

The heap-use-after-free appears to be in ANGLE code. I'm not sure where the SwiftShader stack is from? Jamie please take a look or triage.

### [Deleted User] (2021-10-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-26)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2021-10-27)

I was able to reproduce the ASAN error in the issue description. The ClusterFuzz issue seems to be entirely unrelated. estark - can you figure out what needs to happen to decouple the two issues?

### jm...@chromium.org (2021-10-27)

I'll work on fixing the reported issue.

### gi...@appspot.gserviceaccount.com (2021-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/ca5e6f685c5d73b32bd729d5ed81115eaccbc9b3

commit ca5e6f685c5d73b32bd729d5ed81115eaccbc9b3
Author: Jamie Madill <jmadill@chromium.org>
Date: Wed Oct 27 15:28:08 2021

Vulkan: Fix accessing stale FB cached variable.

This would happen when we start a query after deleting a
Framebuffer.

Bug: chromium:1262091
Change-Id: I595360bf55fe1757779669f168c95be802b70da5
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3248142
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/ca5e6f685c5d73b32bd729d5ed81115eaccbc9b3/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/ca5e6f685c5d73b32bd729d5ed81115eaccbc9b3/src/libANGLE/renderer/vulkan/ContextVk.cpp


### gi...@appspot.gserviceaccount.com (2021-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/629e74007540e540cd54b1713729e265708025bc

commit 629e74007540e540cd54b1713729e265708025bc
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Oct 27 21:23:10 2021

Roll ANGLE from bbeba56a12dd to 36eac05f9d3b (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/bbeba56a12dd..36eac05f9d3b

2021-10-27 penghuang@chromium.org VANGLE: change the default vulkan device choose logic
2021-10-27 angle-autoroll@skia-public.iam.gserviceaccount.com Roll VK-GL-CTS from e2aeccde416b to 49afd2823061 (34 revisions)
2021-10-27 jmadill@chromium.org Vulkan: Fix accessing stale FB cached variable.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC timvp@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1260869,chromium:1262091
Tbr: timvp@google.com
Change-Id: I7a5e82d03b009732b2e3775089173435f072525a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3248708
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#935589}

[modify] https://crrev.com/629e74007540e540cd54b1713729e265708025bc/DEPS


### jm...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

Requesting merge to beta M96 because latest trunk commit (935589) appears to be after beta branch point (929512).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-29)

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

### jm...@chromium.org (2021-10-29)

1. potential heap use-after-free when falling back to software rendering
2. https://chromium-review.googlesource.com/c/angle/angle/+/3248142
3. yes
4. no


### sr...@google.com (2021-11-01)

Merge approved for m96 branch:4664 please merge before 12pm PST ( Nov 2, tuesday) so this can go out in this weeks beta release

### gi...@appspot.gserviceaccount.com (2021-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/86bd457bb95b20f99176baf22c3717f4448173d6

commit 86bd457bb95b20f99176baf22c3717f4448173d6
Author: Jamie Madill <jmadill@chromium.org>
Date: Wed Oct 27 15:28:08 2021

Vulkan: Fix accessing stale FB cached variable.

This would happen when we start a query after deleting a
Framebuffer.

Bug: chromium:1262091
Change-Id: I595360bf55fe1757779669f168c95be802b70da5
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3248142
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit ca5e6f685c5d73b32bd729d5ed81115eaccbc9b3)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3254428
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/86bd457bb95b20f99176baf22c3717f4448173d6/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/86bd457bb95b20f99176baf22c3717f4448173d6/src/libANGLE/renderer/vulkan/ContextVk.cpp


### am...@google.com (2021-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-03)

Congratulations! The VRP Panel has decided to award you $5000 for this report. Thank you for your report and nice work! 

### [Deleted User] (2021-11-03)

Awesome! Thanks!

### cl...@chromium.org (2021-11-04)

ClusterFuzz testcase 4840676162076672 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### am...@chromium.org (2021-11-04)

This clusterfuzz issue is not related to this issue; will look into how to decouple this clusterfuzz issue from this one. 

### am...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1262091?no_tracker_redirect=1

[Multiple monorail components: Internals>GPU>Internals, Internals>GPU>SwiftShader]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057672)*
