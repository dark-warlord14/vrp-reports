# heap buffer overflow in sw::Blitter::fastResolve

| Field | Value |
|-------|-------|
| **Issue ID** | [40058513](https://issues.chromium.org/issues/40058513) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>SwiftShader |
| **Platforms** | Linux, Windows |
| **Reporter** | em...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-01-17 |
| **Bounty** | $7,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36

Steps to reproduce the problem:
os version:
ubuntu 20.04
chrome version：Chromium 99.0.4818.0

1 ./chrome --user-data-dir=/tmp/xx  --incognito http://localhost:8000/crash.html

What is the expected behavior?

What went wrong?
==544044==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61400000f1ff at pc 0x7f0c3024a87b bp 0x7f0c2c1452b0 sp 0x7f0c2c1452a8
WRITE of size 16 at 0x61400000f1ff thread T8
==544044==WARNING: invalid path to external symbolizer!
==544044==WARNING: Failed to use and restart external symbolizer!
    #0 0x7f0c3024a87a in sw::Blitter::fastResolve(vk::Image const*, vk::Image*, VkImageResolve2KHR) ./../../third_party/swiftshader/src/Device/Blitter.cpp:2179
    #1 0x7f0c3024a87a in ?? ??:0
    #2 0x7f0c30249679 in sw::Blitter::resolve(vk::Image const*, vk::Image*, VkImageResolve2KHR) ./../../third_party/swiftshader/src/Device/Blitter.cpp:2063
    #3 0x7f0c30249679 in ?? ??:0
    #4 0x7f0c301938d2 in vk::Image::resolveTo(vk::Image*, VkImageResolve2KHR const&) const ./../../third_party/swiftshader/src/Vulkan/VkImage.cpp:1030
    #5 0x7f0c301938d2 in ?? ??:0
    #6 0x7f0c301655d6 in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) ./../../third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:1757
    #7 0x7f0c301655d6 in ?? ??:0
    #8 0x7f0c301ad9cb in vk::Queue::submitQueue(vk::Queue::Task const&) ./../../third_party/swiftshader/src/Vulkan/VkQueue.cpp:236
    #9 0x7f0c301ad9cb in ?? ??:0
    #10 0x7f0c301ac99e in vk::Queue::taskLoop(marl::Scheduler*) ./../../third_party/swiftshader/src/Vulkan/VkQueue.cpp:288
    #11 0x7f0c301ac99e in ?? ??:0
    #12 0x7f0c301af4d8 in void* std::__1::__thread_proxy<std::__1::tuple<std::__1::unique_ptr<std::__1::__thread_struct, std::__1::default_delete<std::__1::__thread_struct> >, void (vk::Queue::*)(marl::Scheduler*), vk::Queue*, marl::Scheduler*> >(void*) ./../../buildtools/third_party/libc++/trunk/include/type_traits:3897
    #13 0x7f0c301af4d8 in __thread_execute<std::__1::unique_ptr<std::__1::__thread_struct, std::__1::default_delete<std::__1::__thread_struct> >, void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *, 2UL, 3UL> ./../../buildtools/third_party/libc++/trunk/include/thread:280
    #14 0x7f0c301af4d8 in __thread_proxy<std::__1::tuple<std::__1::unique_ptr<std::__1::__thread_struct, std::__1::default_delete<std::__1::__thread_struct> >, void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *> > ./../../buildtools/third_party/libc++/trunk/include/thread:291
    #15 0x7f0c301af4d8 in ?? ??:0
    #16 0x7f0c3b928608 in start_thread /build/glibc-eX1tMB/glibc-2.31/nptl/pthread_create.c:477
    #17 0x7f0c3b928608 in ?? ??:0

0x61400000f1ff is located 7 bytes to the right of 440-byte region [0x61400000f040,0x61400000f1f8)
allocated by thread T0 (chrome) here:
    #0 0x557e8b5d1ffe in __interceptor_malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:69
    #1 0x557e8b5d1ffe in ?? ??:0
    #2 0x7f0c304a9a5b in sw::allocateZeroOrPoison(unsigned long, unsigned long) ./../../third_party/swiftshader/src/System/Memory.cpp:81
    #3 0x7f0c304a9a5b in allocateZeroOrPoison ./../../third_party/swiftshader/src/System/Memory.cpp:116
    #4 0x7f0c304a9a5b in ?? ??:0
    #5 0x7f0c30180186 in vk::DeviceMemory::allocateBuffer() ./../../third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:323
    #6 0x7f0c30180186 in ?? ??:0
    #7 0x7f0c3017ece7 in vk::DeviceMemory::Allocate(VkAllocationCallbacks const*, VkMemoryAllocateInfo const*, VkNonDispatchableHandle<VkDeviceMemory_T*>*, vk::Device*) ./../../third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:261
    #8 0x7f0c3017ece7 in Allocate ./../../third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:103
    #9 0x7f0c3017ece7 in ?? ??:0
    #10 0x7f0c301c98a5 in vkAllocateMemory ./../../third_party/swiftshader/src/Vulkan/libVulkan.cpp:1091
    #11 0x7f0c301c98a5 in ?? ??:0
    #12 0x7f0c329420db in rx::(anonymous namespace)::FindAndAllocateCompatibleMemory(rx::vk::Context*, rx::vk::MemoryProperties const&, unsigned int, unsigned int*, VkMemoryRequirements const&, void const*, rx::vk::DeviceMemory*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_wrapper.h:1308
    #13 0x7f0c329420db in FindAndAllocateCompatibleMemory ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:103
    #14 0x7f0c329420db in ?? ??:0
    #15 0x7f0c3293d495 in rx::vk::AllocateImageMemory(rx::vk::Context*, unsigned int, unsigned int*, void const*, rx::vk::Image*, rx::vk::DeviceMemory*, unsigned long*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:144
    #16 0x7f0c3293d495 in AllocateBufferOrImageMemory<rx::vk::Image> ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:201
    #17 0x7f0c3293d495 in AllocateImageMemory ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:728
    #18 0x7f0c3293d495 in ?? ??:0
    #19 0x7f0c328ff6fe in rx::vk::ImageHelper::initMemory(rx::vk::Context*, bool, rx::vk::MemoryProperties const&, unsigned int) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:4971
    #20 0x7f0c328ff6fe in ?? ??:0
    #21 0x7f0c3282a5cf in rx::TextureVk::initImage(rx::ContextVk*, angle::FormatID, angle::FormatID, rx::ImageMipLevels) ./../../third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:2964
    #22 0x7f0c3282a5cf in ?? ??:0
    #23 0x7f0c32821180 in rx::TextureVk::ensureImageInitialized(rx::ContextVk*, rx::ImageMipLevels) ./../../third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:2377
    #24 0x7f0c32821180 in ?? ??:0
    #25 0x7f0c3283504f in rx::TextureVk::syncState(gl::Context const*, angle::BitSetT<24ul, unsigned long, unsigned long> const&, gl::Command) ./../../third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:2671
    #26 0x7f0c3283504f in ?? ??:0
    #27 0x7f0c322dcd53 in gl::Texture::generateMipmap(gl::Context*) ./../../third_party/angle/src/libANGLE/Texture.cpp:2125
    #28 0x7f0c322dcd53 in generateMipmap ./../../third_party/angle/src/libANGLE/Texture.cpp:1772
    #29 0x7f0c322dcd53 in ?? ??:0
    #30 0x7f0c32079f6f in GL_GenerateMipmap ./../../third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:1445
    #31 0x7f0c32079f6f in ?? ??:0
    #32 0x557e9f222317 in gpu::gles2::GLES2DecoderPassthroughImpl::DoGenerateMipmap(unsigned int) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1454
    #33 0x557e9f222317 in ?? ??:0
    #34 0x557e9f1ec59f in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:859
    #35 0x557e9f1ec59f in ?? ??:0
    #36 0x557e9f680835 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:70
    #37 0x557e9f680835 in ?? ??:0
    #38 0x557e9f67419f in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) ./../../gpu/ipc/service/command_buffer_stub.cc:499
    #39 0x557e9f67419f in ?? ??:0
    #40 0x557e9f673656 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command_buffer_stub.cc:151
    #41 0x557e9f673656 in ?? ??:0
    #42 0x557e9f6874c6 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) ./../../gpu/ipc/service/gpu_channel.cc:669
    #43 0x557e9f6874c6 in ?? ??:0
    #44 0x557e9f6946d6 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) ./../../base/bind_internal.h:535
    #45 0x557e9f6946d6 in ?? ??:0
    #46 0x557e9e052d7c in gpu::Scheduler::RunNextTask() ./../../base/callback.h:142
    #47 0x557e9e052d7c in RunNextTask ./../../gpu/command_buffer/service/scheduler.cc:684
    #48 0x557e9e052d7c in ?? ??:0
    #49 0x557e999bd2c3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/callback.h:142
    #50 0x557e999bd2c3 in RunTaskImpl ./../../base/task/common/task_annotator.cc:135
    #51 0x557e999bd2c3 in ?? ??:0
    #52 0x557e999ff0c3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/common/task_annotator.h:74
    #53 0x557e999ff0c3 in DoWorkImpl ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356
    #54 0x557e999ff0c3 in ?? ??:0
    #55 0x557e999fe8d7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261
    #56 0x557e999fe8d7 in ?? ??:0
    #57 0x557e999ffc91 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread_controller_with_message_pump_impl.cc:?
    #58 0x557e999ffc91 in ?? ??:0
    #59 0x557e998b7a99 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:376
    #60 0x557e998b7a99 in WorkSourceDispatch ./../../base/message_loop/message_pump_glib.cc:126
    #61 0x557e998b7a99 in ?? ??:0
    #62 0x7f0c3b7d017c in g_main_context_dispatch ??:?
    #63 0x7f0c3b7d017c in ?? ??:0

Thread T8 created by T0 (chrome) here:
    #0 0x557e8b5bb6fc in __interceptor_pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:208
    #1 0x557e8b5bb6fc in ?? ??:0
    #2 0x7f0c301acc86 in std::__1::thread::thread<void (vk::Queue::*)(marl::Scheduler*), vk::Queue*, marl::Scheduler*&, void>(void (vk::Queue::*&&)(marl::Scheduler*), vk::Queue*&&, marl::Scheduler*&) ./../../buildtools/third_party/libc++/trunk/include/__threading_support:513
    #3 0x7f0c301acc86 in thread<void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *&, void> ./../../buildtools/third_party/libc++/trunk/include/thread:307
    #4 0x7f0c301acc86 in ?? ??:0
    #5 0x7f0c301ac6fd in vk::Queue::Queue(vk::Device*, marl::Scheduler*) ./../../third_party/swiftshader/src/Vulkan/VkQueue.cpp:170
    #6 0x7f0c301ac6fd in ?? ??:0
    #7 0x7f0c30174954 in vk::Device::Device(VkDeviceCreateInfo const*, void*, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__1::shared_ptr<marl::Scheduler> const&) ./../../third_party/swiftshader/src/Vulkan/VkDevice.cpp:138
    #8 0x7f0c30174954 in ?? ??:0
    #9 0x7f0c301c8fce in VkResult vk::DispatchableObject<vk::Device, VkDevice_T*>::Create<VkDeviceCreateInfo, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__1::shared_ptr<marl::Scheduler> >(VkAllocationCallbacks const*, VkDeviceCreateInfo const*, VkDevice_T**, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__1::shared_ptr<marl::Scheduler>) ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:127
    #10 0x7f0c301c8fce in Create<vk::DispatchableObject<vk::Device, VkDevice_T *>, VkDevice_T *, VkDeviceCreateInfo, vk::PhysicalDevice *, const VkPhysicalDeviceFeatures *, std::__1::shared_ptr<marl::Scheduler> > ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:65
    #11 0x7f0c301c8fce in Create<VkDeviceCreateInfo, vk::PhysicalDevice *, const VkPhysicalDeviceFeatures *, std::__1::shared_ptr<marl::Scheduler> > ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:147
    #12 0x7f0c301c8fce in ?? ??:0
    #13 0x7f0c301c89de in vkCreateDevice ./../../third_party/swiftshader/src/Vulkan/libVulkan.cpp:981
    #14 0x7f0c301c89de in ?? ??:0
    #15 0x7f0c31556c55 in terminator_CreateDevice ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:5901
    #16 0x7f0c31556c55 in ?? ??:0
    #17 0x7f0c31551493 in loader_create_device_chain ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:5196
    #18 0x7f0c31551493 in ?? ??:0
    #19 0x7f0c3154fd17 in loader_layer_create_device ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4709
    #20 0x7f0c3154fd17 in ?? ??:0
    #21 0x7f0c31566d07 in vkCreateDevice ./../../third_party/vulkan-deps/vulkan-loader/src/loader/trampoline.c:900
    #22 0x7f0c31566d07 in ?? ??:0
    #23 0x7f0c327d7422 in rx::RendererVk::initializeDevice(rx::DisplayVk*, unsigned int) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:2306
    #24 0x7f0c327d7422 in ?? ??:0
    #25 0x7f0c327cf526 in rx::RendererVk::initialize(rx::DisplayVk*, egl::Display*, char const*, char const*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:1475
    #26 0x7f0c327cf526 in ?? ??:0
    #27 0x7f0c327747d8 in rx::DisplayVk::initialize(egl::Display*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/DisplayVk.cpp:46
    #28 0x7f0c327747d8 in ?? ??:0
    #29 0x7f0c32949159 in rx::DisplayVkXcb::initialize(egl::Display*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/linux/xcb/DisplayVkXcb.cpp:65
    #30 0x7f0c32949159 in ?? ??:0
    #31 0x7f0c32179e84 in egl::Display::initialize() ./../../third_party/angle/src/libANGLE/Display.cpp:940
    #32 0x7f0c32179e84 in ?? ??:0
    #33 0x7f0c32059d99 in egl::Initialize(egl::Thread*, egl::Display*, int*, int*) ./../../third_party/angle/src/libGLESv2/egl_stubs.cpp:448
    #34 0x7f0c32059d99 in ?? ??:0
    #35 0x7f0c32061c04 in EGL_Initialize ./../../third_party/angle/src/libGLESv2/entry_points_egl_autogen.cpp:330
    #36 0x7f0c32061c04 in ?? ??:0
    #37 0x557e9d16b98f in gl::GLSurfaceEGL::InitializeDisplay(gl::EGLDisplayPlatform) ./../../ui/gl/gl_surface_egl.cc:1427
    #38 0x557e9d16b98f in ?? ??:0
    #39 0x557e9d169362 in gl::GLSurfaceEGL::InitializeOneOff(gl::EGLDisplayPlatform) ./../../ui/gl/gl_surface_egl.cc:988
    #40 0x557e9d169362 in ?? ??:0
    #41 0x557e8d9d4d0d in ui::GLOzoneEGL::InitializeGLOneOffPlatform() ./../../ui/ozone/common/gl_ozone_egl.cc:19
    #42 0x557e8d9d4d0d in ?? ??:0
    #43 0x557e9d411708 in gl::init::InitializeGLOneOffPlatformImplementation(bool, bool, bool) ./../../ui/gl/init/gl_factory.cc:246
    #44 0x557e9d411708 in ?? ??:0
    #45 0x557e9d411207 in gl::init::(anonymous namespace)::InitializeGLOneOffPlatformHelper(bool) ./../../ui/gl/init/gl_factory.cc:167
    #46 0x557e9d411207 in ?? ??:0
    #47 0x557e9d4114b0 in gl::init::InitializeGLNoExtensionsOneOff(bool) ./../../ui/gl/init/gl_factory.cc:202
    #48 0x557e9d4114b0 in ?? ??:0
    #49 0x557e9f6e7931 in gpu::GpuInit::InitializeAndStartSandbox(base::CommandLine*, gpu::GpuPreferences const&) ./../../gpu/ipc/service/gpu_init.cc:402
    #50 0x557e9f6e7931 in ?? ??:0
    #51 0x557ea5a0ad93 in content::GpuMain(content::MainFunctionParams) ./../../content/gpu/gpu_main.cc:321
    #52 0x557ea5a0ad93 in ?? ??:0
    #53 0x557e9878d5f0 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:615
    #54 0x557e9878d5f0 in ?? ??:0
    #55 0x557e9879014e in content::RunOtherNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:687
    #56 0x557e9879014e in ?? ??:0
    #57 0x557e98791fd7 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1028
    #58 0x557e98791fd7 in ?? ??:0
    #59 0x557e9878aadc in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:399
    #60 0x557e9878aadc in ?? ??:0
    #61 0x557e9878c744 in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:427
    #62 0x557e9878c744 in ?? ??:0
    #63 0x557e8b6058ae in ChromeMain ./../../chrome/app/chrome_main.cc:177
    #64 0x557e8b6058ae in ?? ??:0
    #65 0x7f0c3a2890b2 in __libc_start_main ??:?
    #66 0x7f0c3a2890b2 in ?? ??:0

Did this work before? N/A 

Chrome version: Chromium 99.0.4818.0  Channel: dev
OS Version: 20.04

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 825 B)

## Timeline

### [Deleted User] (2022-01-17)

[Empty comment from Monorail migration]

### aj...@google.com (2022-01-19)

This does not repro on Windows.

On linux asan from ~saturday this repros:

[3402668:7:0119/031455.276966:ERROR:command_buffer_proxy_impl.cc(125)] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.
[3402668:7:0119/031455.277349:ERROR:context_provider_command_buffer.cc(147)] GpuChannelHost failed to create command buffer.
Fontconfig error: Cannot load default config file: No such file: (null)
[3402870:3402870:0119/031530.883937:ERROR:gl_utils.cc(319)] [.WebGL-0x61b000090680]GL Driver Message (OpenGL, Performance, GL_CLOSE_PATH_NV, High): GPU stall due to ReadPixels
=================================================================
==3402870==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x614000052fff at pc 0x7f226368a419 bp 0x7f224f0da150 sp 0x7f224f0da148
WRITE of size 16 at 0x614000052fff thread T18
    #0 0x7f226368a418 in sw::Blitter::fastResolve(vk::Image const*, vk::Image*, VkImageResolve2KHR) third_party/swiftshader/src/Device/Blitter.cpp:2179:7
    #1 0x7f2263689105 in sw::Blitter::resolve(vk::Image const*, vk::Image*, VkImageResolve2KHR) third_party/swiftshader/src/Device/Blitter.cpp:2063:5
    #2 0x7f22635cbf3c in vk::Image::resolveTo(vk::Image*, VkImageResolve2KHR const&) const third_party/swiftshader/src/Vulkan/VkImage.cpp:1030:24
    #3 0x7f226359b066 in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:1757:12
    #4 0x7f22635e6fbe in vk::Queue::submitQueue(vk::Queue::Task const&) third_party/swiftshader/src/Vulkan/VkQueue.cpp:236:42
    #5 0x7f22635e5d23 in vk::Queue::taskLoop(marl::Scheduler*) third_party/swiftshader/src/Vulkan/VkQueue.cpp:288:4
    #6 0x7f22635e89d7 in __invoke<void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *, void> buildtools/third_party/libc++/trunk/include/type_traits:3897:1
    #7 0x7f22635e89d7 in __thread_execute<std::__1::unique_ptr<std::__1::__thread_struct, std::__1::default_delete<std::__1::__thread_struct> >, void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *, 2UL, 3UL> buildtools/third_party/libc++/trunk/include/thread:280:5
    #8 0x7f22635e89d7 in void* std::__1::__thread_proxy<std::__1::tuple<std::__1::unique_ptr<std::__1::__thread_struct, std::__1::default_delete<std::__1::__thread_struct> >, void (vk::Queue::*)(marl::Scheduler*), vk::Queue*, marl::Scheduler*> >(void*) buildtools/third_party/libc++/trunk/include/thread:291:5
    #9 0x7f2270670d7f in start_thread nptl/pthread_create.c:481:8

0x614000052fff is located 7 bytes to the right of 440-byte region [0x614000052e40,0x614000052ff8)
allocated by thread T0 (chrome) here:
    #0 0x5596dee7a03e in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:69:3
    #1 0x7f22638f6405 in sw::allocate(unsigned long, unsigned long, bool) third_party/swiftshader/src/System/Memory.cpp:81:42
    #2 0x7f22635b7196 in vk::DeviceMemory::allocateBuffer() third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:323:11
    #3 0x7f22635b5e27 in allocate third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:261:12
    #4 0x7f22635b5e27 in vk::DeviceMemory::Allocate(VkAllocationCallbacks const*, VkMemoryAllocateInfo const*, VkNonDispatchableHandle<VkDeviceMemory_T*>*, vk::Device*) third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:103:29
    #5 0x7f2263602a41 in vkAllocateMemory third_party/swiftshader/src/Vulkan/libVulkan.cpp:1091:20
    #6 0x7f2266d7a4da in allocate third_party/angle/src/libANGLE/renderer/vulkan/vk_wrapper.h:1308:12
    #7 0x7f2266d7a4da in rx::(anonymous namespace)::FindAndAllocateCompatibleMemory(rx::vk::Context*, rx::vk::MemoryProperties const&, unsigned int, unsigned int*, VkMemoryRequirements const&, void const*, rx::vk::DeviceMemory*) third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:103:5
    #8 0x7f2266d6ebb0 in angle::Result rx::(anonymous namespace)::AllocateAndBindBufferOrImageMemory<rx::vk::Image>(rx::vk::Context*, unsigned int, unsigned int*, VkMemoryRequirements const&, void const*, VkBindImagePlaneMemoryInfo const*, rx::vk::Image*, rx::vk::DeviceMemory*) third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:144:5
    #9 0x7f2266d6e7bd in AllocateBufferOrImageMemory<rx::vk::Image> third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:201:5
    #10 0x7f2266d6e7bd in rx::vk::AllocateImageMemory(rx::vk::Context*, unsigned int, unsigned int*, void const*, rx::vk::Image*, rx::vk::DeviceMemory*, unsigned long*) third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:728:12
    #11 0x7f2266d0947e in rx::vk::ImageHelper::initMemory(rx::vk::Context*, bool, rx::vk::MemoryProperties const&, unsigned int) third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:4971:5
    #12 0x7f2266ba0a91 in rx::TextureVk::initImage(rx::ContextVk*, angle::FormatID, angle::FormatID, rx::ImageMipLevels) third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:2964:5
    #13 0x7f2266b95df9 in rx::TextureVk::ensureImageInitialized(rx::ContextVk*, rx::ImageMipLevels) third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:2377:9
    #14 0x7f2266bb1bb5 in rx::TextureVk::syncState(gl::Context const*, angle::BitSetT<24ul, unsigned long, unsigned long> const&, gl::Command) third_party/angle/src/libANGLE/renderer/vulkan/TextureVk.cpp:2671:5
    #15 0x7f2265eae1b1 in syncState third_party/angle/src/libANGLE/Texture.cpp:2125:5
    #16 0x7f2265eae1b1 in gl::Texture::generateMipmap(gl::Context*) third_party/angle/src/libANGLE/Texture.cpp:1772:5
    #17 0x7f2265b52e0a in GL_GenerateMipmap third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:1445:22
    #18 0x5596f7abbbb7 in gpu::gles2::GLES2DecoderPassthroughImpl::DoGenerateMipmap(unsigned int) gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1454:10
    #19 0x5596f7a77bdf in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:859:20
    #20 0x5596f80aef18 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:70:18
    #21 0x5596f809e61f in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) gpu/ipc/service/command_buffer_stub.cc:499:22
    #22 0x5596f809d674 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:151:7
    #23 0x5596f80b8b22 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) gpu/ipc/service/gpu_channel.cc:669:13
    #24 0x5596f80c7296 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) base/bind_internal.h:535:12
    #25 0x5596f64d8437 in Run base/callback.h:142:12
    #26 0x5596f64d8437 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:684:26
    #27 0x5596f13afba6 in Run base/callback.h:142:12
    #28 0x5596f13afba6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #29 0x5596f142a61e in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #30 0x5596f142a61e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #31 0x5596f14291b7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #32 0x5596f142b721 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #33 0x5596f1275ab9 in HandleDispatch base/message_loop/message_pump_glib.cc:376:46
    #34 0x5596f1275ab9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:126:43
    #35 0x7f2270515cda in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x53cda) (BuildId: b430f289010a80bffaaf00e9d4721155f45e8770)

Thread T18 created by T0 (chrome) here:
    #0 0x5596dee6373c in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:208:3
    #1 0x7f22635e6104 in __libcpp_thread_create buildtools/third_party/libc++/trunk/include/__threading_support:513:10
    #2 0x7f22635e6104 in std::__1::thread::thread<void (vk::Queue::*)(marl::Scheduler*), vk::Queue*, marl::Scheduler*&, void>(void (vk::Queue::*&&)(marl::Scheduler*), vk::Queue*&&, marl::Scheduler*&) buildtools/third_party/libc++/trunk/include/thread:307:16
    #3 0x7f22635e5a7d in vk::Queue::Queue(vk::Device*, marl::Scheduler*) third_party/swiftshader/src/Vulkan/VkQueue.cpp:170:16
    #4 0x7f22635abea8 in vk::Device::Device(VkDeviceCreateInfo const*, void*, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__1::shared_ptr<marl::Scheduler> const&) third_party/swiftshader/src/Vulkan/VkDevice.cpp:138:26
    #5 0x7f226360216a in DispatchableObject<const VkDeviceCreateInfo *, void *, vk::PhysicalDevice *, const VkPhysicalDeviceFeatures *, std::__1::shared_ptr<marl::Scheduler> > third_party/swiftshader/src/Vulkan/VkObject.hpp:127:8
    #6 0x7f226360216a in Create<vk::DispatchableObject<vk::Device, VkDevice_T *>, VkDevice_T *, VkDeviceCreateInfo, vk::PhysicalDevice *, const VkPhysicalDeviceFeatures *, std::__1::shared_ptr<marl::Scheduler> > third_party/swiftshader/src/Vulkan/VkObject.hpp:65:34
    #7 0x7f226360216a in VkResult vk::DispatchableObject<vk::Device, VkDevice_T*>::Create<VkDeviceCreateInfo, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__1::shared_ptr<marl::Scheduler> >(VkAllocationCallbacks const*, VkDeviceCreateInfo const*, VkDevice_T**, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__1::shared_ptr<marl::Scheduler>) third_party/swiftshader/src/Vulkan/VkObject.hpp:147:10
    #8 0x7f2263601b50 in vkCreateDevice third_party/swiftshader/src/Vulkan/libVulkan.cpp:981:9
    #9 0x7f2264aefda5 in terminator_CreateDevice third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:5901:11
    #10 0x7f2264aea5e3 in loader_create_device_chain third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:5196:15
    #11 0x7f2264ae8e67 in loader_layer_create_device third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4709:11
    #12 0x7f2264affe57 in vkCreateDevice third_party/vulkan-deps/vulkan-loader/src/loader/trampoline.c:900:20
    #13 0x7f2266b32a32 in rx::RendererVk::initializeDevice(rx::DisplayVk*, unsigned int) third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:2306:5
    #14 0x7f2266b28a94 in rx::RendererVk::initialize(rx::DisplayVk*, egl::Display*, char const*, char const*) third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:1475:9
    #15 0x7f2266a60bc4 in rx::DisplayVk::initialize(egl::Display*) third_party/angle/src/libANGLE/renderer/vulkan/DisplayVk.cpp:46:39
    #16 0x7f2266d83e85 in rx::DisplayVkXcb::initialize(egl::Display*) third_party/angle/src/libANGLE/renderer/vulkan/linux/xcb/DisplayVkXcb.cpp:65:23
    #17 0x7f2265ca3b92 in egl::Display::initialize() third_party/angle/src/libANGLE/Display.cpp:940:36
    #18 0x7f2265b30949 in egl::Initialize(egl::Thread*, egl::Display*, int*, int*) third_party/angle/src/libGLESv2/egl_stubs.cpp:448:5
    #19 0x7f2265b3a4a4 in EGL_Initialize third_party/angle/src/libGLESv2/entry_points_egl_autogen.cpp:330:12
    #20 0x5596f53b7981 in gl::GLSurfaceEGL::InitializeDisplay(gl::EGLDisplayPlatform) ui/gl/gl_surface_egl.cc:1427:10
    #21 0x5596f53b5312 in gl::GLSurfaceEGL::InitializeOneOff(gl::EGLDisplayPlatform) ui/gl/gl_surface_egl.cc:988:3
    #22 0x5596e18f7ecd in ui::GLOzoneEGL::InitializeGLOneOffPlatform() ui/ozone/common/gl_ozone_egl.cc:19:8
    #23 0x5596f5658200 in gl::init::InitializeGLOneOffPlatform() ui/gl/init/gl_initializer_ozone.cc:25:26
    #24 0x5596f564ccc3 in gl::init::InitializeGLOneOffPlatformImplementation(bool, bool, bool) ui/gl/init/gl_factory.cc:246:22
    #25 0x5596f564c6d6 in gl::init::(anonymous namespace)::InitializeGLOneOffPlatformHelper(bool) ui/gl/init/gl_factory.cc:167:10
    #26 0x5596f564c990 in gl::init::InitializeGLNoExtensionsOneOff(bool) ui/gl/init/gl_factory.cc:202:10
    #27 0x5596f8127627 in gpu::GpuInit::InitializeAndStartSandbox(base::CommandLine*, gpu::GpuPreferences const&) gpu/ipc/service/gpu_init.cc:402:11
    #28 0x5596ff7c4c5f in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:321:39
    #29 0x5596efcb372e in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:615:14
    #30 0x5596efcb754e in content::RunOtherNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:687:12
    #31 0x5596efcb9c37 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1029:10
    #32 0x5596efcb0926 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:399:36
    #33 0x5596efcb2744 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:427:10
    #34 0x5596deead8ec in ChromeMain chrome/app/chrome_main.cc:177:12
    #35 0x7f226f3e17ec in __libc_start_main csu/../csu/libc-start.c:332:16

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/swiftshader/src/Device/Blitter.cpp:2179:7 in sw::Blitter::fastResolve(vk::Image const*, vk::Image*, VkImageResolve2KHR)
Shadow bytes around the buggy address:
  0x0c28800025a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c28800025b0: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa
  0x0c28800025c0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c28800025d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c28800025e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c28800025f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00[fa]
  0x0c2880002600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2880002610: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2880002620: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2880002630: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2880002640: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==3402870==ABORTING
[3403011:1:0119/031533.487794:ERROR:command_buffer_proxy_impl.cc(328)] GPU state invalid after WaitForGetOffsetInRange.
[3402571:3402571:0119/031533.489680:ERROR:gpu_process_host.cc(972)] GPU process exited unexpectedly: exit_code=256
libva error: vaGetDriverNameByIndex() failed with unknown libva error, driver_name = (null)
[3403058:3403058:0119/031533.747728:ERROR:sandbox_linux.cc(377)] InitializeSandbox() called with multiple threads in process gpu-process.




### aj...@google.com (2022-01-19)

Note --incognito flag is not necessary.

gn args:
is_asan = true
is_debug = false
v8_enable_verify_heap = true
use_goma = true


### aj...@google.com (2022-01-19)

On Windows canary asan in incognito I get: [43404:41996:0118/190717.639:ERROR:database.cc(1777)] History SQLite error: code 1555 errno 0: UNIQUE constraint failed: context_annotations.visit_id sql: INSERT INTO context_annotations( visit_id,context_annotation_flags,duration_since_last_visit,page_end_reason,total_foreground_duration )VALUES(?,?,?,?,?) but no crash.

Adding capn based off recent commit/blame: https://source.chromium.org/chromium/_/swiftshader/SwiftShader.git/+/4487e589eb749c70ceffdfdbfd433cc1628a735b

If the cause if higher in the stack, please reassign as appropriate.

Severity=high as rce in a sandboxed process
foundin=97 as code last touched a while ago. please update if necessary.

[Monorail components: Internals>GPU>SwiftShader]

### [Deleted User] (2022-01-19)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-01-19)

Thanks for reporting this! The crash appears to be happening at an SSE store instruction [1]. What's odd is that the address (0x61400000f1ff) is not 16-byte aligned, or even 4-byte aligned. SwiftShader only allocates memory that is at least 16-byte aligned, and this WebGL code only appears to be using RGBA8 pixels. So it's possible ANGLE passed incorrect arguments to vkCmdResolveImage(). Using the Vulkan Validation Layers might point to an issue.

There's a known bug [2] in SwiftShader's multisampe resolve code, but I don't see how it could be at the root of this off-by-one-byte issue.

[1] https://cs.opensource.google/swiftshader/SwiftShader/+/master:src/Device/Blitter.cpp;drc=1d924bd003791fa947a963ad9654eec77d50facd;l=2179
[2] https://issuetracker.google.com/177842474

[Monorail blocked-on: b/177842474]

### [Deleted User] (2022-01-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-19)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@google.com (2022-01-31)

This triggers an assert when using a Debug build of SwiftShader, which also reproduces on Windows. ANGLE makes a vkCmdResolveImage() call where the source and destination images are both 8x8, but it's attempting to resolve mipmap level 0 of the source into mipmap level 1 of the destination, which is smaller.

This is expected to violate VUID-vkCmdResolveImage-dstOffset-00274 [0] when using the Vulkan Validation Layers.

Jamie can you have a look or reassign to an appropriate owner?

[0] https://www.khronos.org/registry/vulkan/specs/1.1/html/vkspec.html#VUID-vkCmdResolveImage-dstOffset-00274

[Monorail components: Internals>GPU>ANGLE]

### jm...@chromium.org (2022-01-31)

[Comment Deleted]

### jm...@chromium.org (2022-01-31)

Shabi, you've probably most recently work with blig resolve code. Does this look familiar?

### sy...@chromium.org (2022-01-31)

I can reproduce this in a test (and get VUID-vkCmdResolveImage-dstOffset-00274 indeed)

### gi...@appspot.gserviceaccount.com (2022-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/33427a4b374afa0c9f3f344fb2909fca7fa6274d

commit 33427a4b374afa0c9f3f344fb2909fca7fa6274d
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Jan 31 17:07:43 2022

Vulkan: Fix vkCmdResolveImage extents

The source framebuffer's extents were accidentally used instead of the
blit area extents.

Bug: chromium:1288020
Change-Id: Ib723db50d9687fee0453d027141a94ea26d8a4b8
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3427561
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/33427a4b374afa0c9f3f344fb2909fca7fa6274d/src/tests/gl_tests/BlitFramebufferANGLETest.cpp
[modify] https://crrev.com/33427a4b374afa0c9f3f344fb2909fca7fa6274d/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/33427a4b374afa0c9f3f344fb2909fca7fa6274d/src/tests/angle_end2end_tests_expectations.txt


### [Deleted User] (2022-02-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7aa53b8bf162e8ce84a705c533af9039efa4ea6e

commit 7aa53b8bf162e8ce84a705c533af9039efa4ea6e
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Feb 02 02:15:22 2022

Roll ANGLE from 293c0b516b47 to bc3be5a83f7e (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/293c0b516b47..bc3be5a83f7e

2022-02-02 cclao@google.com Vulkan: Add a dedicated suballocation garbage list
2022-02-01 jmadill@chromium.org Vulkan: Initialize exectuable with invalid uniform serial.
2022-02-01 syoussefi@chromium.org Vulkan: Fix vkCmdResolveImage extents

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
Bug: chromium:1288020
Tbr: jonahr@google.com
Change-Id: Ibced408d48144d8a2999feb5df93852e664d2c2a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3429705
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#966013}

[modify] https://crrev.com/7aa53b8bf162e8ce84a705c533af9039efa4ea6e/DEPS


### sy...@chromium.org (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-11)

Hi syoussefi@, thanks for catching this issue needing a merge. I'm unsure as to why sheriffbot did not request merges on these at any point in the 9 days since this issue was fixed, but it's have solid canary coverage, so approving merge to M99, branch 4844 and M98, branch 4758. Please merge ASAP today - especially to M98- so this fix can be included in the stable cut for M98 respin. 

### gi...@appspot.gserviceaccount.com (2022-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/b4324a11358f082992638e8a4c34a09e51018c02

commit b4324a11358f082992638e8a4c34a09e51018c02
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Jan 31 17:07:43 2022

M99: Vulkan: Fix vkCmdResolveImage extents

The source framebuffer's extents were accidentally used instead of the
blit area extents.

Bug: chromium:1288020
Change-Id: Idb72a593f46840bf6ed964f9135f908aadd1fc1f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3457024
Reviewed-by: Tim Van Patten <timvp@google.com>

[modify] https://crrev.com/b4324a11358f082992638e8a4c34a09e51018c02/src/tests/gl_tests/BlitFramebufferANGLETest.cpp
[modify] https://crrev.com/b4324a11358f082992638e8a4c34a09e51018c02/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/b4324a11358f082992638e8a4c34a09e51018c02/src/tests/angle_end2end_tests_expectations.txt


### gi...@appspot.gserviceaccount.com (2022-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/9c1efd3def62f29dd200e92e9d0b556c1e996b3f

commit 9c1efd3def62f29dd200e92e9d0b556c1e996b3f
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Jan 31 17:07:43 2022

M98: Vulkan: Fix vkCmdResolveImage extents

The source framebuffer's extents were accidentally used instead of the
blit area extents.

Bug: chromium:1288020
Change-Id: I5c6128a191deeea2f972dc7f010be9d40c674ce6
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3457022
Reviewed-by: Tim Van Patten <timvp@google.com>

[modify] https://crrev.com/9c1efd3def62f29dd200e92e9d0b556c1e996b3f/src/tests/gl_tests/BlitFramebufferANGLETest.cpp
[modify] https://crrev.com/9c1efd3def62f29dd200e92e9d0b556c1e996b3f/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/9c1efd3def62f29dd200e92e9d0b556c1e996b3f/src/tests/angle_end2end_tests_expectations.txt


### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Congratulations - the VRP Panel has decided to award you $7,000 for this report. Thanks for your efforts and nice work! 

### am...@chromium.org (2022-02-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-05-20)

Hello OP, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them. Thank you! 

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1288020?no_tracker_redirect=1

[Multiple monorail components: Internals>GPU>ANGLE, Internals>GPU>SwiftShader]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058513)*
