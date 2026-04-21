# AddressSanitizer: heap-use-after-free in isCubeCompatible third_party/swiftshader/src/Vulkan/VkImage.cpp:905:25

| Field | Value |
|-------|-------|
| **Issue ID** | [40059172](https://issues.chromium.org/issues/40059172) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2022-03-22 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
asan-linux-release-983326

#Reproduce
The issue was found by my fuzzer running on CF(CC Security team for access permission https://clusterfuzz.com/testcase-detail/5666142466932736),
But because it cannot be reproduced stably, CF does not automatically report.

What is the expected behavior?

What went wrong?
Type of crash
GPU process

#Analysis
I'm not familiar with the Vulcan code, but the ASAN logs clearly give the root cause of the vulnerability.
image_ is a raw pointer to a VkImage object, created on the main thread via vkCreateImage and possibly freed by the main thread.
But the image_object is passed to the T3 thread for use without observe lifetime of the object, resulting in UAF

```
template <typename T>
void VulkanFenceHelper::EnqueueVulkanObjectCleanupForSubmittedWork(
    std::unique_ptr<T> obj) {
  EnqueueCleanupTaskForSubmittedWork(
      base::BindOnce([](std::unique_ptr<T> obj, VulkanDeviceQueue* device_queue,
                        bool device_lost) { obj->Destroy(); },
                     std::move(obj)));
}
```

#asan
=================================================================
==52173==ERROR: AddressSanitizer: heap-use-after-free on address 0x611000224da0 at pc 0x7fade796f106 bp 0x7fade5e5d230 sp 0x7fade5e5d228
READ of size 4 at 0x611000224da0 thread T3
SCARINESS: 45 (4-byte-read-heap-use-after-free)
    #0 0x7fade796f105 in isCubeCompatible third_party/swiftshader/src/Vulkan/VkImage.cpp:905:25
    #1 0x7fade796f105 in requiresPreprocessing third_party/swiftshader/src/Vulkan/VkImage.cpp:1156:9
    #2 0x7fade796f105 in vk::Image::prepareForSampling(VkImageSubresourceRange const&) const third_party/swiftshader/src/Vulkan/VkImage.cpp:1203:6
    #3 0x7fade7951a31 in prepareForSampling third_party/swiftshader/src/Vulkan/VkImageView.hpp:129:37
    #4 0x7fade7951a31 in vk::Device::prepareForSampling(vk::ImageView*) third_party/swiftshader/src/Vulkan/VkDevice.cpp:455:15
    #5 0x7fade7949d34 in vk::DescriptorSet::ParseDescriptors(std::__1::array<vk::DescriptorSet*, 4ul> const&, vk::PipelineLayout const*, vk::Device*, vk::DescriptorSet::NotificationType) third_party/swiftshader/src/Vulkan/VkDescriptorSet.cpp:67:16
    #6 0x7fade7a587df in sw::Renderer::draw(vk::GraphicsPipeline const*, vk::DynamicState const&, unsigned int, int, sw::CountedEvent*, int, int, void*, VkRect2D const&, vk::Pipeline::PushConstantStorage const&, bool) third_party/swiftshader/src/Device/Renderer.cpp:433:2
    #7 0x7fade7944324 in (anonymous namespace)::CmdDrawBase::draw(vk::CommandBuffer::ExecutionState&, bool, unsigned int, unsigned int, unsigned int, int, unsigned int) third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:913:31
    #8 0x7fade7943de2 in (anonymous namespace)::CmdDraw::execute(vk::CommandBuffer::ExecutionState&) third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:937:3
    #9 0x7fade793e516 in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:2325:12
    #10 0x7fade798a626 in vk::Queue::submitQueue(vk::Queue::Task const&) third_party/swiftshader/src/Vulkan/VkQueue.cpp:104:42
    #11 0x7fade7989600 in vk::Queue::taskLoop(marl::Scheduler*) third_party/swiftshader/src/Vulkan/VkQueue.cpp:156:4
    #12 0x7fade798c11a in __invoke<void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *, void> buildtools/third_party/libc++/trunk/include/type_traits:3897:1
    #13 0x7fade798c11a in __thread_execute<std::__1::unique_ptr<std::__1::__thread_struct, std::__1::default_delete<std::__1::__thread_struct> >, void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *, 2UL, 3UL> buildtools/third_party/libc++/trunk/include/thread:280:5
    #14 0x7fade798c11a in void* std::__1::__thread_proxy<std::__1::tuple<std::__1::unique_ptr<std::__1::__thread_struct, std::__1::default_delete<std::__1::__thread_struct> >, void (vk::Queue::*)(marl::Scheduler*), vk::Queue*, marl::Scheduler*> >(void*) buildtools/third_party/libc++/trunk/include/thread:291:5
    #15 0x7fadfbada6b9 in start_thread /build/glibc-LK5gWL/glibc-2.23/nptl/pthread_create.c:333
0x611000224da0 is located 32 bytes inside of 200-byte region [0x611000224d80,0x611000224e48)
freed by thread T0 (chrome) here:
    #0 0x55e03ba03f22 in free third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:52:3
    #1 0x55e04efefb01 in operator() gpu/vulkan/vulkan_function_pointers.h:91:47
    #2 0x55e04efefb01 in vkDestroyImage gpu/vulkan/vulkan_function_pointers.h:849:10
    #3 0x55e04efefb01 in gpu::VulkanImage::Destroy() gpu/vulkan/vulkan_image.cc:142:5
    #4 0x55e050e24cab in operator() gpu/vulkan/vulkan_fence_helper.h:160:50
    #5 0x55e050e24cab in Invoke<(lambda at ../../gpu/vulkan/vulkan_fence_helper.h:159:22), std::__1::unique_ptr<gpu::VulkanImage, std::__1::default_delete<gpu::VulkanImage> >, gpu::VulkanDeviceQueue *, bool> base/bind_internal.h:423:12
    #6 0x55e050e24cab in MakeItSo<(lambda at ../../gpu/vulkan/vulkan_fence_helper.h:159:22), std::__1::unique_ptr<gpu::VulkanImage, std::__1::default_delete<gpu::VulkanImage> >, gpu::VulkanDeviceQueue *, bool> base/bind_internal.h:706:12
    #7 0x55e050e24cab in RunImpl<(lambda at ../../gpu/vulkan/vulkan_fence_helper.h:159:22), std::__1::tuple<std::__1::unique_ptr<gpu::VulkanImage, std::__1::default_delete<gpu::VulkanImage> > >, 0UL> base/bind_internal.h:779:12
    #8 0x55e050e24cab in base::internal::Invoker<base::internal::BindState<void gpu::VulkanFenceHelper::EnqueueVulkanObjectCleanupForSubmittedWork<gpu::VulkanImage>(std::__1::unique_ptr<gpu::VulkanImage, std::__1::default_delete<gpu::VulkanImage> >)::'lambda'(std::__1::unique_ptr<gpu::VulkanImage, std::__1::default_delete<gpu::VulkanImage> >, gpu::VulkanDeviceQueue*, bool), std::__1::unique_ptr<gpu::VulkanImage, std::__1::default_delete<gpu::VulkanImage> > >, void (gpu::VulkanDeviceQueue*, bool)>::RunOnce(base::internal::BindStateBase*, gpu::VulkanDeviceQueue*, bool) base/bind_internal.h:748:12
    #9 0x55e04eff65cd in Run base/callback.h:142:12
    #10 0x55e04eff65cd in gpu::VulkanFenceHelper::ProcessCleanupTasks(unsigned long) gpu/vulkan/vulkan_fence_helper.cc:129:21
    #11 0x55e04effb312 in operator() gpu/vulkan/vulkan_fence_helper.cc:171:25
    #12 0x55e04effb312 in Invoke<(lambda at ../../gpu/vulkan/vulkan_fence_helper.cc:164:7), base::WeakPtr<gpu::VulkanFenceHelper>, unsigned long> base/bind_internal.h:423:12
    #13 0x55e04effb312 in MakeItSo<(lambda at ../../gpu/vulkan/vulkan_fence_helper.cc:164:7), base::WeakPtr<gpu::VulkanFenceHelper>, unsigned long> base/bind_internal.h:706:12
    #14 0x55e04effb312 in RunImpl<(lambda at ../../gpu/vulkan/vulkan_fence_helper.cc:164:7), std::__1::tuple<base::WeakPtr<gpu::VulkanFenceHelper>, unsigned long>, 0UL, 1UL> base/bind_internal.h:779:12
    #15 0x55e04effb312 in base::internal::Invoker<base::internal::BindState<gpu::VulkanFenceHelper::CreateExternalCallback()::$_0, base::WeakPtr<gpu::VulkanFenceHelper>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:748:12
    #16 0x55e050ddc7a0 in Run base/callback.h:142:12
    #17 0x55e050ddc7a0 in gpu::(anonymous namespace)::CleanupAfterSkiaFlush(void*) gpu/command_buffer/service/skia_utils.cc:49:21
    #18 0x55e04c4a1db5 in ~GrRefCntedCallback third_party/skia/include/private/GrTypesPriv.h:996:29
    #19 0x55e04c4a1db5 in unref third_party/skia/include/core/SkRefCnt.h:180:13
    #20 0x55e04c4a1db5 in SkSafeUnref<GrRefCntedCallback> third_party/skia/include/core/SkRefCnt.h:150:14
    #21 0x55e04c4a1db5 in ~sk_sp third_party/skia/include/core/SkRefCnt.h:251:9
    #22 0x55e04c4a1db5 in pop_back_n third_party/skia/include/private/SkTArray.h:313:37
    #23 0x55e04c4a1db5 in reset third_party/skia/include/private/SkTArray.h:136:15
    #24 0x55e04c4a1db5 in callFinishedProcs third_party/skia/src/gpu/vk/GrVkCommandBuffer.h:318:24
    #25 0x55e04c4a1db5 in GrVkGpu::submitCommandBuffer(GrVkGpu::SyncQueue) third_party/skia/src/gpu/vk/GrVkGpu.cpp:391:39
    #26 0x55e04bf81da7 in GrGpu::submitToGpu(bool) third_party/skia/src/gpu/GrGpu.cpp:706:28
    #27 0x55e050e24615 in gpu::(anonymous namespace)::AngleVulkanBacking::SharedImageRepresentationGLTextureBeginAccess() gpu/command_buffer/service/shared_image_backing_factory_angle_vulkan.cc:215:19
    #28 0x55e050dd6592 in gpu::SharedImageRepresentationGLTextureBase::BeginScopedAccess(unsigned int, gpu::SharedImageRepresentation::AllowUnclearedAccess) gpu/command_buffer/service/shared_image_representation.cc:56:8
    #29 0x55e050c51aee in gpu::gles2::PassthroughResources::SharedImageData::BeginAccess(unsigned int, gl::GLApi*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:475:37
    #30 0x55e050ccece8 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBeginSharedImageAccessDirectCHROMIUM(unsigned int, unsigned int) gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:5415:22
    #31 0x55e050c5a56c in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:870:20
    #32 0x55e0510fd024 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:70:18
    #33 0x55e0510f092f in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) gpu/ipc/service/command_buffer_stub.cc:499:22
    #34 0x55e0510efde6 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:151:7
    #35 0x55e051103d76 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) gpu/ipc/service/gpu_channel.cc:670:13
    #36 0x55e051110ee6 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) base/bind_internal.h:542:12
    #37 0x55e04fad3cc7 in Run base/callback.h:142:12
    #38 0x55e04fad3cc7 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:691:26
    #39 0x55e04a8b3cc3 in Run base/callback.h:142:12
    #40 0x55e04a8b3cc3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #41 0x55e04a8f5a9d in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:387:29)> base/task/common/task_annotator.h:74:5
    #42 0x55e04a8f5a9d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:385:21
    #43 0x55e04a8f5194 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:290:41
    #44 0x55e04a8f6781 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #45 0x55e04a7ac889 in HandleDispatch base/message_loop/message_pump_glib.cc:375:46
    #46 0x55e04a7ac889 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:126:43
    #47 0x7fadfafab196 in g_main_context_dispatch
previously allocated by thread T0 (chrome) here:
    #0 0x55e03ba041ce in malloc third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:69:3
    #1 0x7fade7ca71cb in allocate third_party/swiftshader/src/System/Memory.cpp:81:42
    #2 0x7fade7ca71cb in sw::allocateZeroOrPoison(unsigned long, unsigned long) third_party/swiftshader/src/System/Memory.cpp:116:9
    #3 0x7fade79abe4c in Create<vk::Image, VkNonDispatchableHandle<VkImage_T *>, VkImageCreateInfo, vk::Device *> third_party/swiftshader/src/Vulkan/VkObject.hpp:58:23
    #4 0x7fade79abe4c in VkResult vk::ObjectBase<vk::Image, VkNonDispatchableHandle<VkImage_T*> >::Create<VkImageCreateInfo, vk::Device*>(VkAllocationCallbacks const*, VkImageCreateInfo const*, VkNonDispatchableHandle<VkImage_T*>*, vk::Device*) third_party/swiftshader/src/Vulkan/VkObject.hpp:92:10
    #5 0x7fade79abd24 in vkCreateImage third_party/swiftshader/src/Vulkan/libVulkan.cpp:1888:20
    #6 0x55e04efedcac in operator() gpu/vulkan/vulkan_function_pointers.h:91:47
    #7 0x55e04efedcac in vkCreateImage gpu/vulkan/vulkan_function_pointers.h:760:10
    #8 0x55e04efedcac in gpu::VulkanImage::Initialize(gpu::VulkanDeviceQueue*, gfx::Size const&, VkFormat, unsigned int, unsigned int, VkImageTiling, void*, void*, VkMemoryRequirements const*) gpu/vulkan/vulkan_image.cc:207:21
    #9 0x55e04efed786 in gpu::VulkanImage::Create(gpu::VulkanDeviceQueue*, gfx::Size const&, VkFormat, unsigned int, unsigned int, VkImageTiling, void*, void*) gpu/vulkan/vulkan_image.cc:53:15
    #10 0x55e050e21041 in gpu::(anonymous namespace)::AngleVulkanBacking::Initialize(gpu::SharedImageBackingFactoryGLCommon::FormatInfo const&, base::span<unsigned char const, 18446744073709551615ul> const&) gpu/command_buffer/service/shared_image_backing_factory_angle_vulkan.cc:115:9
    #11 0x55e050e20966 in gpu::SharedImageBackingFactoryAngleVulkan::CreateSharedImage(gpu::Mailbox const&, viz::ResourceFormat, unsigned int, gfx::Size const&, gfx::ColorSpace const&, GrSurfaceOrigin, SkAlphaType, unsigned int, bool) gpu/command_buffer/service/shared_image_backing_factory_angle_vulkan.cc:498:17
    #12 0x55e050dadb8f in gpu::SharedImageFactory::CreateSharedImage(gpu::Mailbox const&, viz::ResourceFormat, gfx::Size const&, gfx::ColorSpace const&, GrSurfaceOrigin, SkAlphaType, unsigned int, unsigned int) gpu/command_buffer/service/shared_image_factory.cc:300:27
    #13 0x55e0511a1680 in gpu::SharedImageStub::OnCreateSharedImage(mojo::StructPtr<gpu::mojom::CreateSharedImageParams>) gpu/ipc/service/shared_image_stub.cc:242:18
    #14 0x55e0511a10a2 in gpu::SharedImageStub::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredSharedImageRequest>) gpu/ipc/service/shared_image_stub.cc:82:7
    #15 0x55e051103c9b in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) gpu/ipc/service/gpu_channel.cc:685:27
    #16 0x55e051110ee6 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) base/bind_internal.h:542:12
    #17 0x55e04fad3cc7 in Run base/callback.h:142:12
    #18 0x55e04fad3cc7 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:691:26
    #19 0x55e04a8b3cc3 in Run base/callback.h:142:12
    #20 0x55e04a8b3cc3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #21 0x55e04a8f5a9d in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:387:29)> base/task/common/task_annotator.h:74:5
    #22 0x55e04a8f5a9d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:385:21
    #23 0x55e04a8f5194 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:290:41
    #24 0x55e04a8f6781 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #25 0x55e04a7ac889 in HandleDispatch base/message_loop/message_pump_glib.cc:375:46
    #26 0x55e04a7ac889 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:126:43
    #27 0x7fadfafab196 in g_main_context_dispatch
Thread T3 created by T0 (chrome) here:
    #0 0x55e03b9ed33c in pthread_create third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:208:3
    #1 0x7fade79898e8 in __libcpp_thread_create buildtools/third_party/libc++/trunk/include/__threading_support:513:10
    #2 0x7fade79898e8 in std::__1::thread::thread<void (vk::Queue::*)(marl::Scheduler*), vk::Queue*, marl::Scheduler*&, void>(void (vk::Queue::*&&)(marl::Scheduler*), vk::Queue*&&, marl::Scheduler*&) buildtools/third_party/libc++/trunk/include/thread:307:16
    #3 0x7fade798935f in vk::Queue::Queue(vk::Device*, marl::Scheduler*) third_party/swiftshader/src/Vulkan/VkQueue.cpp:38:16
    #4 0x7fade794f2d4 in vk::Device::Device(VkDeviceCreateInfo const*, void*, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__1::shared_ptr<marl::Scheduler> const&) third_party/swiftshader/src/Vulkan/VkDevice.cpp:138:26
    #5 0x7fade79a6532 in DispatchableObject<const VkDeviceCreateInfo *, void *, vk::PhysicalDevice *, const VkPhysicalDeviceFeatures *, std::__1::shared_ptr<marl::Scheduler> > third_party/swiftshader/src/Vulkan/VkObject.hpp:127:8
    #6 0x7fade79a6532 in Create<vk::DispatchableObject<vk::Device, VkDevice_T *>, VkDevice_T *, VkDeviceCreateInfo, vk::PhysicalDevice *, const VkPhysicalDeviceFeatures *, std::__1::shared_ptr<marl::Scheduler> > third_party/swiftshader/src/Vulkan/VkObject.hpp:65:34
    #7 0x7fade79a6532 in VkResult vk::DispatchableObject<vk::Device, VkDevice_T*>::Create<VkDeviceCreateInfo, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__1::shared_ptr<marl::Scheduler> >(VkAllocationCallbacks const*, VkDeviceCreateInfo const*, VkDevice_T**, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__1::shared_ptr<marl::Scheduler>) third_party/swiftshader/src/Vulkan/VkObject.hpp:147:10
    #8 0x7fade79a5f86 in vkCreateDevice third_party/swiftshader/src/Vulkan/libVulkan.cpp:1060:9
    #9 0x7fade8a4fe8b in terminator_CreateDevice third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:6009:11
    #10 0x7fade8a49ee3 in loader_create_device_chain third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:5248:15
    #11 0x7fade8a48717 in loader_layer_create_device third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4700:11
    #12 0x7fade8a5fec7 in vkCreateDevice third_party/vulkan-deps/vulkan-loader/src/loader/trampoline.c:920:20
    #13 0x7fade9d0bd65 in rx::RendererVk::initializeDevice(rx::DisplayVk*, unsigned int) third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:2455:5
    #14 0x7fade9d03dc5 in rx::RendererVk::initialize(rx::DisplayVk*, egl::Display*, char const*, char const*) third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:1611:9
    #15 0x7fade9cabe08 in rx::DisplayVk::initialize(egl::Display*) third_party/angle/src/libANGLE/renderer/vulkan/DisplayVk.cpp:46:39
    #16 0x7fade9e8c7f9 in rx::DisplayVkXcb::initialize(egl::Display*) third_party/angle/src/libANGLE/renderer/vulkan/linux/xcb/DisplayVkXcb.cpp:65:23
    #17 0x7fade9694ff4 in egl::Display::initialize() third_party/angle/src/libANGLE/Display.cpp:973:36
    #18 0x7fade9570509 in egl::Initialize(egl::Thread*, egl::Display*, int*, int*) third_party/angle/src/libGLESv2/egl_stubs.cpp:448:5
    #19 0x7fade9577b84 in EGL_Initialize third_party/angle/src/libGLESv2/entry_points_egl_autogen.cpp:330:12
    #20 0x7fade8c69dcc in eglInitialize third_party/angle/src/libEGL/libEGL_autogen.cpp:177:12
    #21 0x55e04eef86db in gl::GLSurfaceEGL::InitializeDisplay(gl::EGLDisplayPlatform, unsigned long) ui/gl/gl_surface_egl.cc:1470:10
    #22 0x55e04eef5d49 in gl::GLSurfaceEGL::InitializeOneOff(gl::EGLDisplayPlatform, unsigned long) ui/gl/gl_surface_egl.cc:1023:3
    #23 0x55e03e25f3df in ui::GLOzoneEGL::InitializeGLOneOffPlatform() ui/ozone/common/gl_ozone_egl.cc:19:8
    #24 0x55e04f149c81 in gl::init::InitializeGLOneOffPlatformImplementation(bool, bool, bool, unsigned long) ui/gl/init/gl_factory.cc:224:22
    #25 0x55e04f14976a in gl::init::(anonymous namespace)::InitializeGLOneOffPlatformHelper(bool, unsigned long) ui/gl/init/gl_factory.cc:150:10
    #26 0x55e04f149a16 in gl::init::InitializeGLNoExtensionsOneOff(bool, unsigned long) ui/gl/init/gl_factory.cc:179:10
    #27 0x55e051163b05 in gpu::GpuInit::InitializeAndStartSandbox(base::CommandLine*, gpu::GpuPreferences const&) gpu/ipc/service/gpu_init.cc:439:24
    #28 0x55e0576a5d0c in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:324:39
    #29 0x55e049693f68 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:611:14
    #30 0x55e049695a63 in content::RunOtherNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:693:12
    #31 0x55e049697aaf in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1023:10
    #32 0x55e049691311 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:407:36
    #33 0x55e049691a3c in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:435:10
    #34 0x55e03ba37b56 in ChromeMain chrome/app/chrome_main.cc:176:12
    #35 0x7fadf504e82f in __libc_start_main /build/glibc-LK5gWL/glibc-2.23/csu/libc-start.c:291
SUMMARY: AddressSanitizer: heap-use-after-free (/mnt/scratch0/clusterfuzz/bot/builds/chrome-test-builds_media_linux-release_eb660d5ee526c9c1c1608a71fcbe7a713c490533/revisions/asan-linux-release-983326/././libvk_swiftshader.so+0x41e105) (BuildId: 94889ac1a8584da0)
Shadow bytes around the buggy address:
  0x0c228003c960: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c228003c970: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x0c228003c980: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c228003c990: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c228003c9a0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
=>0x0c228003c9b0: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd
  0x0c228003c9c0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x0c228003c9d0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c228003c9e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c228003c9f0: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c228003ca00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:00
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
==52173==ABORTING

Did this work before? N/A 

Chrome version: 101.0.0.0  Channel: n/a
OS Version: 10.0

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 22.1 KB)

## Timeline

### [Deleted User] (2022-03-22)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-03-22)

If you need the original CF report(Although I don't think it helps) CC security team to associates the issue with CF(https://clusterfuzz.com/testcase-detail/5666142466932736).

Please add  Restrict-View-SecurityEmbargo for this issue.

### an...@google.com (2022-03-22)

[Empty comment from Monorail migration]

### an...@google.com (2022-03-22)

sugoi@, could you PTAL? 

Setting some labels here based on the trace:
- Severity high for GPU UAF
- FoundIn M98 since the relevant code areas seem to date back to 9/2

[Monorail components: Internals>GPU>SwiftShader]

### [Deleted User] (2022-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@chromium.org (2022-03-23)

Sean, please investigate and try to find the root cause. Thanks.

### cl...@chromium.org (2022-03-24)

Detailed Report: https://clusterfuzz.com/testcase?key=5666142466932736

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x611000224da0
Crash State:
  vk::Image::prepareForSampling
  vk::Device::prepareForSampling
  vk::DescriptorSet::ParseDescriptors
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&revision=983326

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5666142466932736

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2022-03-24)

ClusterFuzz testcase 5666142466932736 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2022-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-04-05)

The memoryOwner found here: https://swiftshader.googlesource.com/SwiftShader/+/2f3af2452783943f7d6994030a9fffa9ba3b3cec/src/Vulkan/VkDescriptorSet.cpp#67 is destroyed as part of VulkanFenceHelper::ProcessCleanupTasks().

### [Deleted User] (2022-04-05)

srisser: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2022-04-05)

Thanks Dana for taking a closer look at this! It appears this is another case where ANGLE starts to destroy resources while SwiftShader is still using them. I'll block this on the Bunker project.

### cl...@chromium.org (2022-04-08)

ClusterFuzz testcase 5666142466932736 is flaky and no longer crashes, so closing issue.

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### cl...@chromium.org (2022-04-08)

ClusterFuzz testcase 5666142466932736 is closed as invalid, so closing issue.

### [Deleted User] (2022-07-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-08-30)

Still reproduce on CF https://clusterfuzz.com/testcase-detail/5528321691680768

### su...@chromium.org (2022-12-22)

Can someone double check this, based on https://crbug.com/chromium/1309035#c15 and address this properly?

### [Deleted User] (2022-12-23)

srisser: Uh oh! This issue still open and hasn't been updated in the last 276 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-23)

[Empty comment from Monorail migration]

### ni...@google.com (2022-12-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-25)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2022-12-27)

Security marshal checking in. If I read the history here correctly, this is still a valid Severity-High bug. But since CF found it to be unreproducible in https://crbug.com/chromium/1309035#c10, it got closed in https://crbug.com/chromium/1309035#c16 and mistakenly went allpublic in https://crbug.com/chromium/1309035#c18. I'll make this restricted again because I think it was unrestricted by mistake.

I'll also ping some folks offline to inquire about the status of this one, since it's getting quite old.


### ja...@chromium.org (2023-02-06)

[Security Marshal] Hi geofflang@, can you take another look at this issue? From the comment log, it's unclear if this bug needs more work. Thanks!

### ge...@chromium.org (2023-02-07)

Peng, could you take a look at this? Looks like an interaction between Skia and ANGLE's Vulkan usage.

### pe...@chromium.org (2023-02-07)

m.cooolie, is it still happening? I cannot open https://clusterfuzz.com/testcase-detail/5528321691680768 .

### m....@gmail.com (2023-02-08)

I don't see any new crashes, but since the test sample itself reproduces unstable, I'm not sure if the issue has been fixed

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d5143b14a00807b40eada4dfb0bce610ffc1477a

commit d5143b14a00807b40eada4dfb0bce610ffc1477a
Author: Peng Huang <penghuang@chromium.org>
Date: Wed Feb 08 21:38:39 2023

Fix UAF problem in AngleVulkanImageBacking

Right now, we use vulkan fence helper to release the backing.
It is right, if the last usage of the backing is by skia.
If the last usage is by gl, the fence helper(skia) isn't aware of
the submitted work from ANGLE, skia may call flush finish callback
to release the backing while the backing is still being referenced
by works in ANGLE. Fix the problem by calling glFinish() if the last
usage is GL.

Know issue: the finish callback of skia flush() is not always called
in order. So in edge cases, the UAF problem can still happen.

Bug: 1309035
Change-Id: I3562043650dd2b27bde3a370bef45b1226cdd48c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4232858
Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org>
Commit-Queue: Peng Huang <penghuang@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1102905}

[modify] https://crrev.com/d5143b14a00807b40eada4dfb0bce610ffc1477a/gpu/command_buffer/service/shared_image/angle_vulkan_image_backing.cc
[modify] https://crrev.com/d5143b14a00807b40eada4dfb0bce610ffc1477a/gpu/command_buffer/service/shared_image/angle_vulkan_image_backing.h


### pe...@chromium.org (2023-02-09)

The change in https://crbug.com/chromium/1309035#c32 may fix the issue. Feel free to reopen it if it happens again.

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-09)

Requesting merge to stable M110 because latest trunk commit (1102905) appears to be after stable branch point (1084008).

Requesting merge to dev M111 because latest trunk commit (1102905) appears to be after dev branch point (1097615).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@chromium.org (2023-02-09)

1. 
https://chromium-review.googlesource.com/c/chromium/src/+/4232858
2.
This crash is not a reliable reproduce, and it only happens with asan build. I cannot verify the fix.
3.
No
4.
No
5.
No




### [Deleted User] (2023-02-09)

Merge review required: M111 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-09)

Merge review required: M110 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-02-13)

M111 merge approved, please merge this fix to branch 5563 by EOD tomorrow, Tuesday 14 February so this fix can be included in the next M111/beta
M110 merge approved, please merge this fix to branch 5481 by 10am Pacific, Friday, 17 February so this fix can be included in the next M110/Stable refresh 

### am...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-13)

There appears an issue with monorail today; please ignore the labels and refer to https://crbug.com/chromium/1309035#c40 regarding merge approvals 

### am...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f551eeab318726904ceb40b020a07395faf21e10

commit f551eeab318726904ceb40b020a07395faf21e10
Author: Peng Huang <penghuang@chromium.org>
Date: Mon Feb 13 21:49:26 2023

Fix UAF problem in AngleVulkanImageBacking

Right now, we use vulkan fence helper to release the backing.
It is right, if the last usage of the backing is by skia.
If the last usage is by gl, the fence helper(skia) isn't aware of
the submitted work from ANGLE, skia may call flush finish callback
to release the backing while the backing is still being referenced
by works in ANGLE. Fix the problem by calling glFinish() if the last
usage is GL.

Know issue: the finish callback of skia flush() is not always called
in order. So in edge cases, the UAF problem can still happen.

(cherry picked from commit d5143b14a00807b40eada4dfb0bce610ffc1477a)

Bug: 1309035
Change-Id: I3562043650dd2b27bde3a370bef45b1226cdd48c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4232858
Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org>
Commit-Queue: Peng Huang <penghuang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1102905}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4246158
Cr-Commit-Position: refs/branch-heads/5563@{#432}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/f551eeab318726904ceb40b020a07395faf21e10/gpu/command_buffer/service/shared_image/angle_vulkan_image_backing.cc
[modify] https://crrev.com/f551eeab318726904ceb40b020a07395faf21e10/gpu/command_buffer/service/shared_image/angle_vulkan_image_backing.h


### am...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aeec1ba5893d7e152c756c09455211f0f2de64e2

commit aeec1ba5893d7e152c756c09455211f0f2de64e2
Author: Peng Huang <penghuang@chromium.org>
Date: Mon Feb 13 22:10:44 2023

Fix UAF problem in AngleVulkanImageBacking

Right now, we use vulkan fence helper to release the backing.
It is right, if the last usage of the backing is by skia.
If the last usage is by gl, the fence helper(skia) isn't aware of
the submitted work from ANGLE, skia may call flush finish callback
to release the backing while the backing is still being referenced
by works in ANGLE. Fix the problem by calling glFinish() if the last
usage is GL.

Know issue: the finish callback of skia flush() is not always called
in order. So in edge cases, the UAF problem can still happen.

(cherry picked from commit d5143b14a00807b40eada4dfb0bce610ffc1477a)

Bug: 1309035
Change-Id: I3562043650dd2b27bde3a370bef45b1226cdd48c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4232858
Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org>
Commit-Queue: Peng Huang <penghuang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1102905}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4245959
Cr-Commit-Position: refs/branch-heads/5481@{#1119}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/aeec1ba5893d7e152c756c09455211f0f2de64e2/gpu/command_buffer/service/shared_image/angle_vulkan_image_backing.cc
[modify] https://crrev.com/aeec1ba5893d7e152c756c09455211f0f2de64e2/gpu/command_buffer/service/shared_image/angle_vulkan_image_backing.h


### am...@chromium.org (2023-02-13)

merges completed, removing merge labels 

### am...@google.com (2023-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-17)

Congratulations! The VRP Panel has decided to award you $10,000 for this report + $3,000 fuzzer bonus. Thank you for your efforts in reporting this GPU bug and your efforts toward fuzzing Chrome -- great work! 

### am...@google.com (2023-02-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-20)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1309035?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1223346, crbug.com/swiftshader/173]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059172)*
