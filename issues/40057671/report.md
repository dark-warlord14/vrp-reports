# Security: heap-buffer-overflow swiftshader Image::copy

| Field | Value |
|-------|-------|
| **Issue ID** | [40057671](https://issues.chromium.org/issues/40057671) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | lf...@google.com |
| **Created** | 2021-10-21 |
| **Bounty** | $5,000.00 |

## Description

On Windows 10 - Chrome Stable Version - 95.0.4638.54
has to be launched using --no-sandbox --disable-gpu-sandbox --disable-gpu

2:153> r
rax=0000000000000008 rbx=0000014480f6d828 rcx=0000014480f6d828
rdx=ff414141ff414141 rsi=0000000000000020 rdi=0000000000000008
rip=00007ffc29e8ba30 rsp=00000029611ff648 rbp=ff414141ff414141
 r8=0000000000000020  r9=0000000000000025 r10=ff414141ff414141
r11=0000014480f6d828 r12=ff414141ff414141 r13=0000000000000020
r14=0000000000000048 r15=0000014480f6d828
iopl=0         nv up ei pl zr na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
vk_swiftshader!memcpy+0x40:
00007ffc`29e8ba30 0f1002          movups  xmm0,xmmword ptr [rdx] ds:ff414141`ff414141=????????????????????????????????

2:153> k
 # Child-SP          RetAddr               Call Site
00 00000029`611ff648 00007ffc`29bf5caa     vk_swiftshader!memcpy+0x40 [d:\A01\_work\6\s\src\vctools\crt\vcruntime\src\string\amd64\memcpy.asm @ 179] 
01 00000029`611ff650 00007ffc`29be572e     vk_swiftshader!vk::Image::copy+0x5da [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkImage.cpp @ 630] 
02 00000029`611ff770 00007ffc`29bfe406     vk_swiftshader!vk::CommandBuffer::submit+0x2e [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp @ 1731] 
03 00000029`611ff7c0 00007ffc`29bfdad1     vk_swiftshader!vk::Queue::submitQueue+0x266 [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkQueue.cpp @ 219] 
04 00000029`611ffba0 00007ffc`29bfed9a     vk_swiftshader!vk::Queue::taskLoop+0xb1 [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkQueue.cpp @ 280] 
05 (Inline Function) --------`--------     vk_swiftshader!std::__1::__invoke+0xb [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\type_traits @ 3897] 
06 (Inline Function) --------`--------     vk_swiftshader!std::__1::__thread_execute+0xb [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\thread @ 280] 
07 00000029`611ffc40 00007ffc`29e94430     vk_swiftshader!std::__1::__thread_proxy<std::__1::tuple<std::__1::unique_ptr<std::__1::__thread_struct,std::__1::default_delete<std::__1::__thread_struct> >,void (vk::Queue::*)(marl::Scheduler *),vk::Queue *,marl::Scheduler *> >+0x2a [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\thread @ 293] 
08 00000029`611ffc80 00007ffc`a16b7034     vk_swiftshader!thread_start<unsigned int (__cdecl*)(void *),1>+0x50 [C:\b\s\w\ir\cache\builder\src\out\Release_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp @ 97] 
09 00000029`611ffcb0 00007ffc`a2822651     KERNEL32!BaseThreadInitThunk+0x14
0a 00000029`611ffce0 00000000`00000000     ntdll!RtlUserThreadStart+0x21



ASAN Log

==10552==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x128b2f147618 at pc 0x7ff78f1e1e07 bp 0x00deab9febf0 sp 0x00deab9fec38
WRITE of size 256 at 0x128b2f147618 thread T6
==10552==WARNING: Failed to use and restart external symbolizer!
==10552==*** WARNING: Failed to initialize DbgHelp!              ***
==10552==*** Most likely this means that the app is already      ***
==10552==*** using DbgHelp, possibly with incompatible flags.    ***
==10552==*** Due to technical reasons, symbolization might crash ***
==10552==*** or produce wrong results.                           ***
    #0 0x7ff78f1e1e06 in __asan_memcpy C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cpp:22
    #1 0x7ffc29e07a91 in vk::Image::copy C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkImage.cpp:659
    #2 0x7ffc29dd95b5 in vk::CommandBuffer::submit C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp:1742
    #3 0x7ffc29e225aa in vk::Queue::submitQueue C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkQueue.cpp:243
    #4 0x7ffc29e20451 in vk::Queue::taskLoop C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkQueue.cpp:296
    #5 0x7ffc29e2446c in std::__1::__thread_proxy<std::__1::tuple<std::__1::unique_ptr<std::__1::__thread_struct,std::__1::default_delete<std::__1::__thread_struct> >,void (vk::Queue::*)(marl::Scheduler *),vk::Queue *,marl::Scheduler *> > C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\thread:291
    #6 0x7ffc2a759ef7 in thread_start<unsigned int (__cdecl*)(void *),1> C:\b\s\w\ir\cache\builder\src\out\Release_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:97
    #7 0x7ff78f1ed823 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:278
    #8 0x7ffca16b7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #9 0x7ffca2822650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x128b2f147618 is located 0 bytes to the right of 4376-byte region [0x128b2f146500,0x128b2f147618)
allocated by thread T0 here:
    #0 0x7ff78f1e237b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffc2a1455f6 in sw::allocateZero C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\System\Memory.cpp:109
    #2 0x7ffc29df3e78 in vk::DeviceMemory::allocateBuffer C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkDeviceMemory.cpp:323
    #3 0x7ffc29df3125 in vk::DeviceMemory::Allocate C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkDeviceMemory.cpp:103
    #4 0x7ffc29e3a95f in vkAllocateMemory C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\libVulkan.cpp:1065
    #5 0x7ffc2b5f1568 in rx::`anonymous namespace'::FindAndAllocateCompatibleMemory C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_utils.cpp:102
    #6 0x7ffc2b5ee698 in rx::`anonymous namespace'::AllocateAndBindBufferOrImageMemory<rx::vk::Image> C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_utils.cpp:143
    #7 0x7ffc2b5ee2f2 in rx::vk::AllocateImageMemory C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_utils.cpp:612
    #8 0x7ffc2b5bb081 in rx::vk::ImageHelper::initMemory C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_helpers.cpp:4456
    #9 0x7ffc2b5254ff in rx::TextureVk::initImage C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\TextureVk.cpp:2938
    #10 0x7ffc2b524a17 in rx::TextureVk::setStorageMultisample C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\TextureVk.cpp:1281
    #11 0x7ffc2b5248c5 in rx::TextureVk::setStorage C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\TextureVk.cpp:1253
    #12 0x7ffc2aee7773 in gl::Texture::setStorage C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Texture.cpp:1565
    #13 0x7ffc2ada976f in gl::Context::texStorage3D C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp:6441
    #14 0x7ffc2ad20e7c in GL_TexStorage3D C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp:2338
    #15 0x7ffc09a739e6 in gl::GLApiBase::glTexStorage3DFn C:\b\s\w\ir\cache\builder\src\ui\gl\gl_bindings_autogen_gl.cc:5955
    #16 0x7ffc110be048 in gpu::gles2::GLES2DecoderPassthroughImpl::DoTexStorage3D C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:2839
    #17 0x7ffc110e8ca6 in gpu::gles2::GLES2DecoderPassthroughImpl::HandleTexStorage3D C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_handlers_autogen.cc:2552
    #18 0x7ffc0d350dad in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:858
    #19 0x7ffc0d3501f4 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:796
    #20 0x7ffc0a21e016 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:70
    #21 0x7ffc07808538 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:500
    #22 0x7ffc078076ec in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:152
    #23 0x7ffc078143c2 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:666
    #24 0x7ffc0781f491 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:753
    #25 0x7ffc074477cd in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:685
    #26 0x7ffc061d668a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #27 0x7ffc08cad53f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:358

Thread T6 created by T0 here:
    #0 0x7ff78f1ee2b2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ffc2a759dd2 in _beginthreadex C:\b\s\w\ir\cache\builder\src\out\Release_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp:209
    #2 0x7ffc2a378da3 in std::__1::__libcpp_thread_create C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\src\support\win32\thread_win32.cpp:207
    #3 0x7ffc29e20839 in std::__1::thread::thread<void (vk::Queue::*)(marl::Scheduler *),vk::Queue *,marl::Scheduler *&,void> C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\thread:307
    #4 0x7ffc29e20193 in vk::Queue::Queue C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkQueue.cpp:154
    #5 0x7ffc29de8bc2 in vk::Device::Device C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkDevice.cpp:139
    #6 0x7ffc29e39f6d in vk::DispatchableObject<vk::Device,VkDevice_T *>::Create<VkDeviceCreateInfo,vk::PhysicalDevice *,const VkPhysicalDeviceFeatures *,std::__1::shared_ptr<marl::Scheduler> > C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkObject.hpp:147
    #7 0x7ffc29e39883 in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\libVulkan.cpp:955
    #8 0x7ffc2ab6bc7f in terminator_CreateDevice C:\b\s\w\ir\cache\builder\src\third_party\vulkan-deps\vulkan-loader\src\loader\loader.c:7010
    #9 0x7ffc9bda9f56 in dummy_debug_proc+0x8196 (C:\ProgramData\obs-studio-hook\graphics-hook64.dll+0x180009f56)
    #10 0x7ffbf9dee410 in DrvPresentBuffers+0x3bec10 (C:\Windows\System32\DriverStore\FileRepository\nv_dispi.inf_amd64_19c79fb6254e3b11\nvoglv64.dll+0x1810ce410)
    #11 0x7ffc2ab66a77 in loader_create_device_chain C:\b\s\w\ir\cache\builder\src\third_party\vulkan-deps\vulkan-loader\src\loader\loader.c:6361
    #12 0x7ffc2ab657ae in loader_layer_create_device C:\b\s\w\ir\cache\builder\src\third_party\vulkan-deps\vulkan-loader\src\loader\loader.c:5898
    #13 0x7ffc2ab7d3b9 in vkCreateDevice C:\b\s\w\ir\cache\builder\src\third_party\vulkan-deps\vulkan-loader\src\loader\trampoline.c:793
    #14 0x7ffc2b4e2b2c in rx::RendererVk::initializeDevice C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:2100
    #15 0x7ffc2b4dc015 in rx::RendererVk::initialize C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\RendererVk.cpp:1383
    #16 0x7ffc2b47c68f in rx::DisplayVk::initialize C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\DisplayVk.cpp:40
    #17 0x7ffc2b5f1e35 in rx::DisplayVkWin32::initialize C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\win32\DisplayVkWin32.cpp:62
    #18 0x7ffc2addf3a1 in egl::Display::initialize C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Display.cpp:890
    #19 0x7ffc2aceff35 in egl::Initialize C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\egl_stubs.cpp:448
    #20 0x7ffc2acf58fd in EGL_Initialize C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_egl_autogen.cpp:311
    #21 0x7ffc07208383 in gl::GLSurfaceEGL::InitializeDisplay C:\b\s\w\ir\cache\builder\src\ui\gl\gl_surface_egl.cc:1379    #22 0x7ffc07205616 in gl::GLSurfaceEGL::InitializeOneOff C:\b\s\w\ir\cache\builder\src\ui\gl\gl_surface_egl.cc:963
    #23 0x7ffc09b5c221 in gl::init::InitializeGLOneOffPlatform C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl_initializer_win.cc:140
    #24 0x7ffc0724b807 in gl::init::InitializeGLOneOffPlatformImplementation C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl_factory.cc:242
    #25 0x7ffc0724b08e in gl::init::`anonymous namespace'::InitializeGLOneOffPlatformHelper C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl_factory.cc:163
    #26 0x7ffc0724b3ad in gl::init::InitializeGLNoExtensionsOneOff C:\b\s\w\ir\cache\builder\src\ui\gl\init\gl_factory.cc:198
    #27 0x7ffc078363d7 in gpu::GpuInit::InitializeAndStartSandbox C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_init.cc:405
    #28 0x7ffc086c0083 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:352
    #29 0x7ffc01e7e661 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1006
    #30 0x7ffc01e7b046 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #31 0x7ffc01e7c088 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418
    #32 0x7ffbfb84147f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172
    #33 0x7ff78f135b44 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #34 0x7ff78f132c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #35 0x7ff78f52d17f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #36 0x7ffca16b7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #37 0x7ffca2822650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cpp:22 in __asan_memcpy
Shadow bytes around the buggy address:
  0x049a949a8e70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x049a949a8e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x049a949a8e90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x049a949a8ea0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x049a949a8eb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x049a949a8ec0: 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa fa
  0x049a949a8ed0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x049a949a8ee0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x049a949a8ef0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x049a949a8f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x049a949a8f10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==10552==ABORTING



## Attachments

- [min_poc.html](attachments/min_poc.html) (text/plain, 1.4 KB)
- [41414141.html](attachments/41414141.html) (text/plain, 2.0 KB)
- [utility.js](attachments/utility.js) (text/plain, 2.1 KB)

## Timeline

### [Deleted User] (2021-10-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-10-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6217594157465600.

### cl...@chromium.org (2021-10-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6038565576048640.

### es...@chromium.org (2021-10-25)

Clusterfuzz seems to think this is a null-pointer deref in GPU sandbox initialization. I'm re-running it, but in the meantime, could SwiftShader owners PTAL?

[Monorail components: Internals>GPU>SwiftShader]

### [Deleted User] (2021-10-25)

[Empty comment from Monorail migration]

### ni...@google.com (2021-10-26)

The repro sample contains only 2D texture calls, but the overflow happens on memory allocated as part of a glTexStorage3D call. Jamie, is ANGLE recycling VkDeviceMemory which might be too small, or is there another explanation for this?

### [Deleted User] (2021-10-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-03)

Is this being tracked somewhere else?

### [Deleted User] (2021-11-04)

jmadill: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-18)

jmadill: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-29)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2021-11-30)

+Frank

### lf...@google.com (2021-12-02)

Reproed right away by translating the min poc to a angle end2end test , and running with Swiftshader config.

So there's nothing spec violating about that sequence of calls, right?

### lf...@google.com (2021-12-02)

I get the feeling the 3d storage stuff earlier is a red herring. Either angle or swiftshader is doing something wrong.

### lf...@google.com (2021-12-02)

It's in ANGLE. We stage a bunch of 64x64 subresource updates and still apply them even when the image storage is respecified to 16x16.

### lf...@google.com (2021-12-02)

Adding removeStagedUpdates to setStorageMultisample makes it go away.

### lf...@google.com (2021-12-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/929c8ed4e8c3912cf027d843e7a2af47b21e5612

commit 929c8ed4e8c3912cf027d843e7a2af47b21e5612
Author: Lingfeng Yang <lfy@google.com>
Date: Thu Dec 02 02:16:14 2021

Vulkan: remove staged updates on storage set

Previously we would allow staged updates to bigger versions of a texture
to go through even if the texture was redefined via glTexStorage*.

Bug: chromium:1262080
Change-Id: I9d861fed68d4a1fdcd0777b97caf729cc74c595e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3312718
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Lingfeng Yang <lfy@google.com>

[modify] https://crrev.com/929c8ed4e8c3912cf027d843e7a2af47b21e5612/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/929c8ed4e8c3912cf027d843e7a2af47b21e5612/src/libANGLE/renderer/vulkan/TextureVk.cpp


### gi...@appspot.gserviceaccount.com (2021-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/675b9e6b0c2fe42d4f0f95b64d1742a3cf44a66d

commit 675b9e6b0c2fe42d4f0f95b64d1742a3cf44a66d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Dec 06 20:16:02 2021

Roll ANGLE from 8313ffe2768f to 929c8ed4e8c3 (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/8313ffe2768f..929c8ed4e8c3

2021-12-06 lfy@google.com Vulkan: remove staged updates on storage set

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jonahr@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1262080
Tbr: jonahr@google.com
Change-Id: Ib549f2f60772534a942bcf5fa1156c45ac506cf3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3318097
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#948642}

[modify] https://crrev.com/675b9e6b0c2fe42d4f0f95b64d1742a3cf44a66d/DEPS


### lf...@google.com (2021-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-08)

Requesting merge to stable M96 because latest trunk commit (948642) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (948642) appears to be after beta branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-08)

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

### [Deleted User] (2021-12-08)

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

### ad...@google.com (2021-12-09)

It looks like this is web-accessible GPU process overflow, in at least some configurations, so we should merge the fix to stable and extended stable.

Approving merge to M96, branch 4664, and M97, branch 4692, unless any problems have shown up in Canary.

### gi...@appspot.gserviceaccount.com (2021-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/05e69c75905f4b9109f279ae89d2fbf574fdc442

commit 05e69c75905f4b9109f279ae89d2fbf574fdc442
Author: Lingfeng Yang <lfy@google.com>
Date: Thu Dec 02 02:16:14 2021

M96: Vulkan: remove staged updates on storage set

Previously we would allow staged updates to bigger versions of a texture
to go through even if the texture was redefined via glTexStorage*.

Bug: chromium:1262080
Change-Id: I9d861fed68d4a1fdcd0777b97caf729cc74c595e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3312718
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Lingfeng Yang <lfy@google.com>
(cherry picked from commit 929c8ed4e8c3912cf027d843e7a2af47b21e5612)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3328001

[modify] https://crrev.com/05e69c75905f4b9109f279ae89d2fbf574fdc442/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/05e69c75905f4b9109f279ae89d2fbf574fdc442/src/libANGLE/renderer/vulkan/TextureVk.cpp


### gi...@appspot.gserviceaccount.com (2021-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/1171efeec73020e5abf1fc3558a87c8fb130ab16

commit 1171efeec73020e5abf1fc3558a87c8fb130ab16
Author: Lingfeng Yang <lfy@google.com>
Date: Thu Dec 02 02:16:14 2021

M97: Vulkan: remove staged updates on storage set

Previously we would allow staged updates to bigger versions of a texture
to go through even if the texture was redefined via glTexStorage*.

Bug: chromium:1262080
Change-Id: I9d861fed68d4a1fdcd0777b97caf729cc74c595e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3312718
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Lingfeng Yang <lfy@google.com>
(cherry picked from commit 929c8ed4e8c3912cf027d843e7a2af47b21e5612)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3328002

[modify] https://crrev.com/1171efeec73020e5abf1fc3558a87c8fb130ab16/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/1171efeec73020e5abf1fc3558a87c8fb130ab16/src/libANGLE/renderer/vulkan/TextureVk.cpp


### gi...@appspot.gserviceaccount.com (2021-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/05e69c75905f4b9109f279ae89d2fbf574fdc442

commit 05e69c75905f4b9109f279ae89d2fbf574fdc442
Author: Lingfeng Yang <lfy@google.com>
Date: Thu Dec 02 02:16:14 2021

M96: Vulkan: remove staged updates on storage set

Previously we would allow staged updates to bigger versions of a texture
to go through even if the texture was redefined via glTexStorage*.

Bug: chromium:1262080
Change-Id: I9d861fed68d4a1fdcd0777b97caf729cc74c595e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3312718
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Lingfeng Yang <lfy@google.com>
(cherry picked from commit 929c8ed4e8c3912cf027d843e7a2af47b21e5612)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3328001

[modify] https://crrev.com/05e69c75905f4b9109f279ae89d2fbf574fdc442/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/05e69c75905f4b9109f279ae89d2fbf574fdc442/src/libANGLE/renderer/vulkan/TextureVk.cpp


### ad...@chromium.org (2021-12-10)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-12-13)

ClusterFuzz testcase 6038565576048640 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### am...@google.com (2022-01-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-06)

Congratulations, Omair! The VRP Panel has decided to award you $5,000 for this report. Thank you for your report and nice work! 

### am...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1262080?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057671)*
