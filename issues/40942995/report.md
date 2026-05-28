# SwiftShader: UAF in isCubeCompatible  

| Field | Value |
|-------|-------|
| **Issue ID** | [40942995](https://issues.chromium.org/issues/40942995) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2023-11-15 |
| **Bounty** | $4,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os version:  

ubuntu:22.04

tested chrome version:  

Chromium 121.0.6128.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1224132.zip)  

Chromium 113.0.5624.0(I believe it should be possible to reproduce earlier than this version.）

Repro Steps:  

1 python3 -m http.server 8000 --dir=|Path|  

2 ./launcher.sh 2>&1 |grep -E 'AddressSanitizer'

Note:  

-Due to the unstable repro with single browser, I wrote a script (according to the actual environment, it is necessary to modify the path of chrome and poc in launcher.sh), opened 20 chrome, and ran poc in --headless mode. It should be reproducible in over 30 seconds.

- |--remote-debugging-port=0 --headless| is not a necessary flags, it is only for faster reproduction.

**Problem Description:**  

==750974==ERROR: AddressSanitizer: heap-use-after-free on address 0x511000073420 at pc 0x7f94094f626e bp 0x7f93fe5ba890 sp 0x7f93fe5ba888  

READ of size 4 at 0x511000073420 thread T17  

#0 0x7f94094f626d in isCubeCompatible ./../../third\_party/swiftshader/src/Vulkan/VkImage.cpp:877:25  

#1 0x7f94094f626d in requiresPreprocessing ./../../third\_party/swiftshader/src/Vulkan/VkImage.cpp:1128:9  

#2 0x7f94094f626d in vk::Image::prepareForSampling(VkImageSubresourceRange const&) const ./../../third\_party/swiftshader/src/Vulkan/VkImage.cpp:1175:6  

#3 0x7f94094c4474 in prepareForSampling ./../../third\_party/swiftshader/src/Vulkan/VkImageView.hpp:129:37  

#4 0x7f94094c4474 in vk::Device::prepareForSampling(vk::ImageView\*) ./../../third\_party/swiftshader/src/Vulkan/VkDevice.cpp:467:15  

#5 0x7f94094bb52a in vk::DescriptorSet::ParseDescriptors(std::\_\_Cr::array<vk::DescriptorSet\*, 4ul> const&, vk::PipelineLayout const\*, vk::Device\*, vk::DescriptorSet::NotificationType) ./../../third\_party/swiftshader/src/Vulkan/VkDescriptorSet.cpp:67:16  

#6 0x7f94095fb2b7 in sw::Renderer::draw(vk::GraphicsPipeline const\*, vk::DynamicState const&, unsigned int, int, sw::CountedEvent\*, int, int, void\*, VkRect2D const&, vk::Pipeline::PushConstantStorage const&, bool) ./../../third\_party/swiftshader/src/Device/Renderer.cpp:296:2  

#7 0x7f94094b4f45 in (anonymous namespace)::CmdDrawBase::draw(vk::CommandBuffer::ExecutionState&, bool, unsigned int, unsigned int, unsigned int, int, unsigned int) ./../../third\_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:957:31  

#8 0x7f94094b496b in (anonymous namespace)::CmdDraw::execute(vk::CommandBuffer::ExecutionState&) ./../../third\_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:985:3  

#9 0x7f94094add78 in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) ./../../third\_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:2330:12  

#10 0x7f940951b391 in vk::Queue::submitQueue(vk::Queue::Task const&) ./../../third\_party/swiftshader/src/Vulkan/VkQueue.cpp:104:42  

#11 0x7f940951a1f4 in vk::Queue::taskLoop(marl::Scheduler\*) ./../../third\_party/swiftshader/src/Vulkan/VkQueue.cpp:156:4  

#12 0x7f940951e1f5 in \_\_invoke<void (vk::Queue::\*)(marl::Scheduler \*), vk::Queue \*, marl::Scheduler \*, void> ./../../third\_party/libc++/src/include/\_\_type\_traits/invoke.h:312:25  

#13 0x7f940951e1f5 in \_\_thread\_execute<std::\_\_Cr::unique\_ptr<std::\_\_Cr::\_\_thread\_struct, std::\_\_Cr::default\_delete[std::\_\_Cr::\_\_thread\_struct](javascript:void(0);) >, void (vk::Queue::\*)(marl::Scheduler \*), vk::Queue \*, marl::Scheduler \*, 2UL, 3UL> ./../../third\_party/libc++/src/include/\_\_thread/thread.h:220:5  

#14 0x7f940951e1f5 in void\* std::\_\_Cr::\_\_thread\_proxy<std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<std::\_\_Cr::\_\_thread\_struct, std::\_\_Cr::default\_delete[std::\_\_Cr::\_\_thread\_struct](javascript:void(0);)>, void (vk::Queue::\*)(marl::Scheduler\*), vk::Queue\*, marl::Scheduler\*>>(void\*) ./../../third\_party/libc++/src/include/\_\_thread/thread.h:231:5  

#15 0x5564244aa348 in asan\_thread\_start(void\*) *asan\_rtl*:28

0x511000073420 is located 32 bytes inside of 200-byte region [0x511000073400,0x5110000734c8)  

freed by thread T0 (chrome) here:  

#0 0x5564244ac4e6 in \_\_interceptor\_free *asan\_rtl*:3  

#1 0x7f942ad50a4e in destroy ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_wrapper.h:1361:9  

#2 0x7f942ad50a4e in DestroyGarbage<rx::vk::Image \*, rx::vk::DeviceMemory \*, rx::vk::Allocation \*> ./../../third\_party/angle/src/libANGLE/renderer/vulkan/RendererVk.h:1126:17  

#3 0x7f942ad50a4e in void rx::RendererVk::collectGarbage<rx::vk::Image\*, rx::vk::DeviceMemory\*, rx::vk::Allocation\*>(rx::vk::ResourceUse const&, rx::vk::Image\*, rx::vk::DeviceMemory\*, rx::vk::Allocation\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/RendererVk.h:317:13  

#4 0x7f942ad51503 in releaseImage ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_helpers.cpp:5816:15  

#5 0x7f942ad51503 in rx::vk::ImageHelper::releaseImageFromShareContexts(rx::RendererVk\*, rx::ContextVk\*, rx::UniqueSerial) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_helpers.cpp:5828:5  

#6 0x7f942ab2d953 in rx::RenderbufferVk::releaseImage(rx::ContextVk\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp:331:17  

#7 0x7f942ab2cbc6 in releaseAndDeleteImage ./../../third\_party/angle/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp:309:5  

#8 0x7f942ab2cbc6 in rx::RenderbufferVk::onDestroy(gl::Context const\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp:38:5  

#9 0x7f942b0d060a in gl::Renderbuffer::onDestroy(gl::Context const\*) ./../../third\_party/angle/src/libANGLE/Renderbuffer.cpp:118:26  

#10 0x7f942b0d7479 in release ./../../third\_party/angle/src/libANGLE/RefCountObject.h:45:13  

#11 0x7f942b0d7479 in DeleteObject ./../../third\_party/angle/src/libANGLE/ResourceManager.cpp:273:19  

#12 0x7f942b0d7479 in gl::TypedResourceManager<gl::Renderbuffer, gl::RenderbufferManager, gl::RenderbufferID>::deleteObject(g

**Additional Comments:**

\*\*Chrome version: \*\* 113.0.5624.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 2.7 KB)
- [asan.log](attachments/asan.log) (text/plain, 27.4 KB)
- [launcher.sh](attachments/launcher.sh) (text/plain, 3.0 KB)
- [VUID-vkDestroyImage-image-01000.log](attachments/VUID-vkDestroyImage-image-01000.log) (text/plain, 2.1 MB)
- [VUID-vkDestroyImageView-imageView-01026.log](attachments/VUID-vkDestroyImageView-imageView-01026.log) (text/plain, 2.2 MB)
- [VUID-vkDestroyImage-image-01000.log](attachments/VUID-vkDestroyImage-image-01000.log) (text/plain, 6.2 MB)
- [VUID-vkDestroyImageView-imageView-01026.log](attachments/VUID-vkDestroyImageView-imageView-01026.log) (text/plain, 6.1 MB)
- [crash2.html](attachments/crash2.html) (text/html, 3.3 KB)
- [crash-q2-no-repro.html](attachments/crash-q2-no-repro.html) (text/html, 2.9 KB)
- [crash-q3-no-repro.html](attachments/crash-q3-no-repro.html) (text/html, 2.4 KB)
- [crash-origin-minimize-repro.html](attachments/crash-origin-minimize-repro.html) (text/html, 3.3 KB)
- [crash-q2-repro.html](attachments/crash-q2-repro.html) (text/html, 3.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 26.2 KB)

## Timeline

### [Deleted User] (2023-11-15)

[Empty comment from Monorail migration]

### ar...@google.com (2023-11-16)

Thanks!
This reproduce on my side on Linux.

+CC current OWNERS of SwiftShader:
- jonahr@
- syoussefi@
- geofflang@

Geoff, would you like to take a look at this UAF?


Here is my ASAN output:

```
==1361628==ERROR: AddressSanitizer: heap-use-after-free on address 0x5110000435e0 at pc 0x7fdfc76f62fe bp 0x7fdfb47ee8d0 sp 0x7fdfb47ee8c8
READ of size 4 at 0x5110000435e0 thread T17
==1361628==WARNING: invalid path to external symbolizer!
==1361628==WARNING: Failed to use and restart external symbolizer!
    #0 0x7fdfc76f62fd in isCubeCompatible ./../../third_party/swiftshader/src/Vulkan/VkImage.cpp:877:25
    #1 0x7fdfc76f62fd in requiresPreprocessing ./../../third_party/swiftshader/src/Vulkan/VkImage.cpp:1128:9
    #2 0x7fdfc76f62fd in vk::Image::prepareForSampling(VkImageSubresourceRange const&) const ./../../third_party/swiftshader/src/Vulkan/VkImage.cpp:1175:6
    #3 0x7fdfc76c4504 in prepareForSampling ./../../third_party/swiftshader/src/Vulkan/VkImageView.hpp:129:37
    #4 0x7fdfc76c4504 in vk::Device::prepareForSampling(vk::ImageView*) ./../../third_party/swiftshader/src/Vulkan/VkDevice.cpp:467:15
    #5 0x7fdfc76bb5ba in vk::DescriptorSet::ParseDescriptors(std::__Cr::array<vk::DescriptorSet*, 4ul> const&, vk::PipelineLayout const*, vk::Device*, vk::DescriptorSet::NotificationType) ./../../third_party/swiftshader/src/Vulkan/VkDescriptorSet.cpp:67:16
    #6 0x7fdfc77fb347 in sw::Renderer::draw(vk::GraphicsPipeline const*, vk::DynamicState const&, unsigned int, int, sw::CountedEvent*, int, int, void*, VkRect2D const&, vk::Pipeline::PushConstantStorage const&, bool) ./../../third_party/swiftshader/src/Device/Renderer.cpp:296:2
    #7 0x7fdfc76b4fd5 in (anonymous namespace)::CmdDrawBase::draw(vk::CommandBuffer::ExecutionState&, bool, unsigned int, unsigned int, unsigned int, int, unsigned int) ./../../third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:957:31
    #8 0x7fdfc76b49fb in (anonymous namespace)::CmdDraw::execute(vk::CommandBuffer::ExecutionState&) ./../../third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:985:3
    #9 0x7fdfc76ade08 in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) ./../../third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:2330:12
    #10 0x7fdfc771b421 in vk::Queue::submitQueue(vk::Queue::Task const&) ./../../third_party/swiftshader/src/Vulkan/VkQueue.cpp:104:42
    #11 0x7fdfc771a284 in vk::Queue::taskLoop(marl::Scheduler*) ./../../third_party/swiftshader/src/Vulkan/VkQueue.cpp:156:4
    #12 0x7fdfc771e285 in __invoke<void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *, void> ./../../third_party/libc++/src/include/__type_traits/invoke.h:312:25
    #13 0x7fdfc771e285 in __thread_execute<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct> >, void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *, 2UL, 3UL> ./../../third_party/libc++/src/include/__thread/thread.h:220:5
    #14 0x7fdfc771e285 in void* std::__Cr::__thread_proxy<std::__Cr::tuple<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct>>, void (vk::Queue::*)(marl::Scheduler*), vk::Queue*, marl::Scheduler*>>(void*) ./../../third_party/libc++/src/include/__thread/thread.h:231:5
    #15 0x56217bd42348 in asan_thread_start(void*) _asan_rtl_:28

0x5110000435e0 is located 32 bytes inside of 200-byte region [0x5110000435c0,0x511000043688)
freed by thread T0 (chrome) here:
    #0 0x56217bd444e6 in __interceptor_free _asan_rtl_:3
    #1 0x7fdfc9b50dce in destroy ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_wrapper.h:1361:9
    #2 0x7fdfc9b50dce in DestroyGarbage<rx::vk::Image *, rx::vk::DeviceMemory *, rx::vk::Allocation *> ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.h:1109:17
    #3 0x7fdfc9b50dce in void rx::RendererVk::collectGarbage<rx::vk::Image*, rx::vk::DeviceMemory*, rx::vk::Allocation*>(rx::vk::ResourceUse const&, rx::vk::Image*, rx::vk::DeviceMemory*, rx::vk::Allocation*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.h:300:13
    #4 0x7fdfc9b51883 in releaseImage ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:5816:15
    #5 0x7fdfc9b51883 in rx::vk::ImageHelper::releaseImageFromShareContexts(rx::RendererVk*, rx::ContextVk*, rx::UniqueSerial) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:5828:5
    #6 0x7fdfc992db33 in rx::RenderbufferVk::releaseImage(rx::ContextVk*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp:331:17
    #7 0x7fdfc992cda6 in releaseAndDeleteImage ./../../third_party/angle/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp:309:5
    #8 0x7fdfc992cda6 in rx::RenderbufferVk::onDestroy(gl::Context const*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp:38:5
    #9 0x7fdfc9ed098a in gl::Renderbuffer::onDestroy(gl::Context const*) ./../../third_party/angle/src/libANGLE/Renderbuffer.cpp:118:26
    #10 0x7fdfc9ed77f9 in release ./../../third_party/angle/src/libANGLE/RefCountObject.h:45:13
    #11 0x7fdfc9ed77f9 in DeleteObject ./../../third_party/angle/src/libANGLE/ResourceManager.cpp:273:19
    #12 0x7fdfc9ed77f9 in gl::TypedResourceManager<gl::Renderbuffer, gl::RenderbufferManager, gl::RenderbufferID>::deleteObject(gl::Context const*, gl::RenderbufferID) ./../../third_party/angle/src/libANGLE/ResourceManager.cpp:96:9
    #13 0x7fdfc9d41e22 in deleteRenderbuffer ./../../third_party/angle/src/libANGLE/Context.cpp:1178:34
    #14 0x7fdfc9d41e22 in gl::Context::deleteRenderbuffers(int, gl::RenderbufferID const*) ./../../third_party/angle/src/libANGLE/Context.cpp:6740:9
    #15 0x5621995895cd in operator() ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:356:14
    #16 0x5621995895cd in ForEach<(lambda at ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:355:7)> ./../../gpu/command_buffer/service/client_service_map.h:134:9
    #17 0x5621995895cd in DeleteServiceObjects<unsigned int, unsigned int, (lambda at ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:355:7)> ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:180:13
    #18 0x5621995895cd in gpu::gles2::PassthroughResources::Destroy(gl::GLApi*, gl::ProgressReporter*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:353:3
    #19 0x56219957e4b2 in gpu::gles2::ContextGroup::Destroy(gpu::DecoderContext*, bool) ./../../gpu/command_buffer/service/context_group.cc:636:29
    #20 0x56219959e4ec in gpu::gles2::GLES2DecoderPassthroughImpl::Destroy(bool) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:1213:13
    #21 0x562199ab16b6 in gpu::CommandBufferStub::Destroy() ./../../gpu/ipc/service/command_buffer_stub.cc:353:23
    #22 0x562199aaf80a in gpu::CommandBufferStub::~CommandBufferStub() ./../../gpu/ipc/service/command_buffer_stub.cc:136:3
    #23 0x562199af5323 in gpu::GLES2CommandBufferStub::~GLES2CommandBufferStub() ./../../gpu/ipc/service/gles2_command_buffer_stub.cc:76:49
    #24 0x562199adcaf7 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #25 0x562199adcaf7 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:297:7
    #26 0x562199adcaf7 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:263:75
    #27 0x562199adcaf7 in gpu::GpuChannel::DestroyCommandBuffer(int) ./../../gpu/ipc/service/gpu_channel.cc:1152:1
    #28 0x562199aed6c4 in Invoke<void (gpu::GpuChannel::*)(int), const base::WeakPtr<gpu::GpuChannel> &, int> ./../../base/functional/bind_internal.h:713:12
    #29 0x562199aed6c4 in MakeItSo<void (gpu::GpuChannel::*)(int), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, int> > ./../../base/functional/bind_internal.h:896:5
    #30 0x562199aed6c4 in void base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(int), base::WeakPtr<gpu::GpuChannel>, int>, void ()>::RunImpl<void (gpu::GpuChannel::*)(int), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, int>, 0ul, 1ul>(void (gpu::GpuChannel::*&&)(int), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, int>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) ./../../base/functional/bind_internal.h:968:12
    #31 0x5621906daf97 in Run ./../../base/functional/callback.h:154:12
    #32 0x5621906daf97 in base::internal::PostTaskAndReplyRelay::RunTaskAndPostReply(base::internal::PostTaskAndReplyRelay) ./../../base/threading/post_task_and_reply_impl.h:45:28
    #33 0x5621906db3ea in Invoke<void (*)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay> ./../../base/functional/bind_internal.h:631:12
    #34 0x5621906db3ea in MakeItSo<void (*)(base::internal::PostTaskAndReplyRelay), std::__Cr::tuple<base::internal::PostTaskAndReplyRelay> > ./../../base/functional/bind_internal.h:868:12
    #35 0x5621906db3ea in RunImpl<void (*)(base::internal::PostTaskAndReplyRelay), std::__Cr::tuple<base::internal::PostTaskAndReplyRelay>, 0UL> ./../../base/functional/bind_internal.h:968:12
    #36 0x5621906db3ea in base::internal::Invoker<base::internal::BindState<void (*)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:919:12
    #37 0x5621906551e8 in Run ./../../base/functional/callback.h:154:12
    #38 0x5621906551e8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:201:34
    #39 0x5621906c0148 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:11)> ./../../base/task/common/task_annotator.h:89:5
    #40 0x5621906c0148 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:461:23
    #41 0x5621906bee8a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:326:41
    #42 0x5621906c104a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #43 0x562190520aff in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #44 0x5621906c1f60 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:626:12
    #45 0x5621905d583c in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #46 0x5621a9fde980 in content::GpuMain(content::MainFunctionParams) ./../../content/gpu/gpu_main.cc:431:14
    #47 0x56218d2d17fb in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:674:14
    #48 0x56218d2d3307 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:778:12
    #49 0x56218d2d6af6 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1138:10
    #50 0x56218d2cf2cd in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:334:36

previously allocated by thread T0 (chrome) here:
[1116/143914.264882:ERROR:gl_utils.cc(412)] [.WebGL-0x51b000072a80]GL Driver Message (OpenGL, Performance, GL_CLOSE_PATH_NV, High): GPU stall due to ReadPixels
    #0 0x56217bd4477d in __interceptor_malloc _asan_rtl_:3
    #1 0x7fdfc7a8f77d in allocate ./../../third_party/swiftshader/src/System/Memory.cpp:81:42
    #2 0x7fdfc7a8f77d in sw::allocateZeroOrPoison(unsigned long, unsigned long) ./../../third_party/swiftshader/src/System/Memory.cpp:110:9
    #3 0x7fdfc773ea2e in Create<vk::Image, VkNonDispatchableHandle<VkImage_T *>, VkImageCreateInfo, vk::Device *> ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:58:23
    #4 0x7fdfc773ea2e in VkResult vk::ObjectBase<vk::Image, VkNonDispatchableHandle<VkImage_T*>>::Create<VkImageCreateInfo, vk::Device*>(VkAllocationCallbacks const*, VkImageCreateInfo const*, VkNonDispatchableHandle<VkImage_T*>*, vk::Device*) ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:92:10
    #5 0x7fdfc773e8f0 in vkCreateImage ./../../third_party/swiftshader/src/Vulkan/libVulkan.cpp:2093:20
    #6 0x7fdfc9b4dee8 in init ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_wrapper.h:1369:12
    #7 0x7fdfc9b4dee8 in rx::vk::ImageHelper::initExternal(rx::vk::Context*, gl::TextureType, VkExtent3D const&, angle::FormatID, angle::FormatID, int, unsigned int, unsigned int, rx::vk::ImageLayout, void const*, gl::LevelIndexWrapper<int>, unsigned int, unsigned int, bool, bool) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:5663:5
    #8 0x7fdfc992d5b0 in rx::RenderbufferVk::setStorageImpl(gl::Context const*, int, unsigned int, int, int, gl::MultisamplingMode) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp:129:5
    #9 0x7fdfc992dcb3 in rx::RenderbufferVk::setStorage(gl::Context const*, unsigned int, int, int) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp:169:12
    #10 0x7fdfc9ed16f3 in gl::Renderbuffer::setStorage(gl::Context const*, unsigned int, int, int) ./../../third_party/angle/src/libANGLE/Renderbuffer.cpp:149:5
    #11 0x5621996af381 in gpu::gles2::GLES2DecoderPassthroughImpl::DoRenderbufferStorage(unsigned int, unsigned int, int, int) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:2947:10
    #12 0x56219959572d in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:736:20
    #13 0x562199ac6731 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:232:35
    #14 0x562199ab34ee in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) ./../../gpu/ipc/service/command_buffer_stub.cc:507:22
    #15 0x562199ab2842 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command_buffer_stub.cc:155:7
    #16 0x562199ad3ef8 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) ./../../gpu/ipc/service/gpu_channel.cc:873:13
    #17 0x562199ae7f74 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) ./../../base/functional/bind_internal.h:713:12
    #18 0x562199ae7d3c in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> > > ./../../base/functional/bind_internal.h:896:5
    #19 0x562199ae7d3c in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:968:12
    #20 0x562199ae7d3c in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:919:12
    #21 0x56219621bea1 in Run ./../../base/functional/callback.h:154:12
    #22 0x56219621bea1 in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) ./../../gpu/command_buffer/service/scheduler_dfs.cc:740:24
    #23 0x562196219841 in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command_buffer/service/scheduler_dfs.cc:665:3
    #24 0x56219622685f in Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs *> ./../../base/functional/bind_internal.h:713:12
    #25 0x56219622685f in MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:868:12
    #26 0x56219622685f in RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:968:12
    #27 0x56219622685f in base::internal::Invoker<base::internal::BindState<void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:919:12
    #28 0x5621906551e8 in Run ./../../base/functional/callback.h:154:12
    #29 0x5621906551e8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:201:34
    #30 0x5621906c0148 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:11)> ./../../base/task/common/task_annotator.h:89:5
    #31 0x5621906c0148 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:461:23
    #32 0x5621906bee8a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:326:41
    #33 0x5621906c104a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #34 0x562190520aff in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #35 0x5621906c1f60 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:626:12
    #36 0x5621905d583c in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #37 0x5621a9fde980 in content::GpuMain(content::MainFunctionParams) ./../../content/gpu/gpu_main.cc:431:14
    #38 0x56218d2d17fb in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:674:14
    #39 0x56218d2d3307 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:778:12
    #40 0x56218d2d6af6 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1138:10

Thread T17 created by T0 (chrome) here:
    #0 0x56217bd29f51 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x7fdfc771a59a in __libcpp_thread_create ./../../third_party/libc++/src/include/__threading_support:372:10
    #2 0x7fdfc771a59a in std::__Cr::thread::thread<void (vk::Queue::*)(marl::Scheduler*), vk::Queue*, marl::Scheduler*&, void>(void (vk::Queue::*&&)(marl::Scheduler*), vk::Queue*&&, marl::Scheduler*&) ./../../third_party/libc++/src/include/__thread/thread.h:247:16
    #3 0x7fdfc7719fc5 in vk::Queue::Queue(vk::Device*, marl::Scheduler*) ./../../third_party/swiftshader/src/Vulkan/VkQueue.cpp:38:16
    #4 0x7fdfc76c0ee6 in vk::Device::Device(VkDeviceCreateInfo const*, void*, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__Cr::shared_ptr<marl::Scheduler> const&) ./../../third_party/swiftshader/src/Vulkan/VkDevice.cpp:139:26
    #5 0x7fdfc773851b in DispatchableObject<const VkDeviceCreateInfo *, void *, vk::PhysicalDevice *, const VkPhysicalDeviceFeatures *, std::__Cr::shared_ptr<marl::Scheduler> > ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:127:8
    #6 0x7fdfc773851b in Create<vk::DispatchableObject<vk::Device, VkDevice_T *>, VkDevice_T *, VkDeviceCreateInfo, vk::PhysicalDevice *, const VkPhysicalDeviceFeatures *, std::__Cr::shared_ptr<marl::Scheduler> > ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:65:34
    #7 0x7fdfc773851b in VkResult vk::DispatchableObject<vk::Device, VkDevice_T*>::Create<VkDeviceCreateInfo, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__Cr::shared_ptr<marl::Scheduler>>(VkAllocationCallbacks const*, VkDeviceCreateInfo const*, VkDevice_T**, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__Cr::shared_ptr<marl::Scheduler>) ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:147:10
    #8 0x7fdfc7737d9c in vkCreateDevice ./../../third_party/swiftshader/src/Vulkan/libVulkan.cpp:1256:9
    #9 0x7fdfc89302cf in terminator_CreateDevice ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:5833:11
    #10 0x7fdfc8933e9c in loader_create_device_chain ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4941:15
    #11 0x7fdfc8932345 in loader_layer_create_device ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4321:11
    #12 0x7fdfc8949388 in vkCreateDevice ./../../third_party/vulkan-deps/vulkan-loader/src/loader/trampoline.c:992:20
    #13 0x7fdfc995bd55 in rx::RendererVk::createDeviceAndQueue(rx::DisplayVk*, unsigned int) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:3393:5
    #14 0x7fdfc995692a in rx::RendererVk::initialize(rx::DisplayVk*, egl::Display*, char const*, char const*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:1932:9
    #15 0x7fdfc98cd1c2 in rx::DisplayVk::initialize(egl::Display*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/DisplayVk.cpp:110:39
    #16 0x7fdfc9bbf0ed in rx::DisplayVkXcb::initialize(egl::Display*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/linux/xcb/DisplayVkXcb.cpp:65:23
    #17 0x7fdfc9d9eda1 in egl::Display::initialize() ./../../third_party/angle/src/libANGLE/Display.cpp:1048:36
    #18 0x7fdfc97da15f in egl::Initialize(egl::Thread*, egl::Display*, int*, int*) ./../../third_party/angle/src/libGLESv2/egl_stubs.cpp:514:5
    #19 0x7fdfc97e262f in EGL_Initialize ./../../third_party/angle/src/libGLESv2/entry_points_egl_autogen.cpp:482:27
    #20 0x7fdfc8d074de in eglInitialize ./../../third_party/angle/src/libEGL/libEGL_autogen.cpp:177:12
    #21 0x562194fc01f7 in gl::GLDisplayEGL::InitializeDisplay(bool, std::__Cr::vector<gl::DisplayType, std::__Cr::allocator<gl::DisplayType>>, gl::EGLDisplayPlatform, gl::GLDisplayEGL*) ./../../ui/gl/gl_display.cc:783:10
    #22 0x562194fbd59c in gl::GLDisplayEGL::Initialize(bool, std::__Cr::vector<gl::DisplayType, std::__Cr::allocator<gl::DisplayType>>, gl::EGLDisplayPlatform) ./../../ui/gl/gl_display.cc:673:8
    #23 0x56217e853ff8 in ui::GLOzoneEGL::InitializeGLOneOffPlatform(bool, std::__Cr::vector<gl::DisplayType, std::__Cr::allocator<gl::DisplayType>>, gl::GpuPreference) ./../../ui/ozone/common/gl_ozone_egl.cc:25:17
    #24 0x56219532a102 in gl::init::InitializeGLOneOffPlatform(gl::GpuPreference) ./../../ui/gl/init/gl_initializer_ozone.cc:27:26
    #25 0x56219531eadb in gl::init::InitializeGLOneOffPlatformImplementation(bool, bool, bool, gl::GpuPreference) ./../../ui/gl/init/gl_factory.cc:211:24
    #26 0x56219531e2dd in gl::init::(anonymous namespace)::InitializeGLOneOffPlatformHelper(bool, gl::GpuPreference) ./../../ui/gl/init/gl_factory.cc:135:10
    #27 0x56219531e782 in gl::init::InitializeGLNoExtensionsOneOff(bool, gl::GpuPreference) ./../../ui/gl/init/gl_factory.cc:166:10
    #28 0x562199b52131 in gpu::GpuInit::InitializeAndStartSandbox(base::CommandLine*, gpu::GpuPreferences const&) ./../../gpu/ipc/service/gpu_init.cc:446:18
    #29 0x5621a9fde453 in content::GpuMain(content::MainFunctionParams) ./../../content/gpu/gpu_main.cc:357:39
    #30 0x56218d2d17fb in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:674:14
    #31 0x56218d2d3307 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:778:12
    #32 0x56218d2d6af6 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1138:10
    #33 0x56218d2cf2cd in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:334:36
    #34 0x56218d2cf9ff in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:347:10
    #35 0x56218ef67d70 in HeadlessChildMain ./../../headless/app/headless_shell.cc:191:12
    #36 0x56218ef67d70 in headless::HeadlessShellMain(content::ContentMainParams) ./../../headless/app/headless_shell.cc:252:5
    #37 0x56217bd79b2a in ChromeMain ./../../chrome/app/chrome_main.cc:175:14
    #38 0x7fdfd12456c9 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free (/usr/local/google/home/arthursonzogni/chromium/src/chromium-121.0.6115.2-linux-asan/././libvk_swiftshader.so+0x4f62fd) (BuildId: 41b0f99057895f49)
Shadow bytes around the buggy address:
  0x511000043300: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00
  0x511000043380: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x511000043400: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa f7 fa
  0x511000043480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x511000043500: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa
=>0x511000043580: fa fa fa fa fa fa f7 fa fd fd fd fd[fd]fd fd fd
  0x511000043600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x511000043680: fd fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x511000043700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x511000043780: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x511000043800: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
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

==1361628==ADDITIONAL INFO

==1361628==Note: Please include this section with the ASan report.
Task trace:

```

[Monorail components: Internals>GPU>SwiftShader]

### [Deleted User] (2023-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2023-11-28)

[security shepherd]: geofflang@, Can you provide an update on this issue? Thanks! 

### [Deleted User] (2023-11-30)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-12-13)

Hi geofflang@! It looks like  arthursonzogni@ was able to reproduce the issue. Can you take a look at the stack trace and reassign to a good owner?

Thanks for taking a look!

[secondary shepherd]

### ja...@chromium.org (2023-12-13)

moving geofflang@ to CC and reassigning to ynovikov@ to take a look.

ynovikov@, could you take a look and provide an update? [secondary shepherd]

### yn...@chromium.org (2023-12-14)

I think geofflang@ is still the best owner for this.
SwiftShader project is understuffed, so the plan is to disable it in production Chrome in order to address this and other security issues.
Not sure when it is going to happen, though.

High priority and P1 look wrong for this bug, since SwiftShader is a software fallback which is only used when the GPU isn't usable.

### ar...@google.com (2023-12-14)

> High priority and P1 look wrong for this bug, since SwiftShader is a software fallback which is only used when the GPU isn't usable.

P1 seems appropriate. SwiftShader can be enabled on arbitrary users, even without an unusable GPU:
- The WebGPU requestAdapter method has a forceFallbackAdapter option and Chrome will use SwiftShader for the WebGPU pipeline when this option is set to true.
- Crashing the GPU 3 times before getting the SwiftShaderFallback.

### [Deleted User] (2023-12-14)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-25)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-04)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-15)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2024-01-18)

I tried this a week ago in an ANGLE end2end test and it didn't reproduce. I finally got the chance to build Chrome with ASAN and tried it as described in the OP (with multiple tabs in a loop etc) and I still cannot reproduce it.

@reporter, is this happening because of OOM?

### em...@gmail.com (2024-01-20)

[Comment Deleted]

### em...@gmail.com (2024-01-20)

I'm not quite sure why the issue can't be reproduced on other machines. Could you try not using the headless mode (by removing the --headless and --remote-debugging-port=0 in the launcher.sh), and just open 4 browsers to test it? On my machine, the issue can be reproduced in about 10 munites.

    -   @reporter, is this happening because of Out Of Memory (OOM)?
I didn't find any logs related to OOM(such as 'GL_OUT_OF_MEMORY' or 'A device memory allocation has failed') before triggering the UAF (Use-After-Free).
tested version:
Chromium 122.0.6260.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1249817.zip)

### em...@gmail.com (2024-01-21)

I've found a similar issue (https://bugs.chromium.org/p/chromium/issues/detail?id=1309035), please refer to it for more information.

### sy...@chromium.org (2024-01-22)

Not sure if that's the same issue, this one seems to come from ANGLE's internals, while the other was a Chrome bug.

> I didn't find any logs related to OOM

I honestly don't know if that exists, could you just monitor memory usage on the system while the tests run?

> Could you try not using the headless mode (by removing the --headless and --remote-debugging-port=0 in the launcher.sh), and just open 4 browsers to test it?

I actually did, headless crashed for me on an unrelated thing (parsing the command line for some reason!), so I used headless, without remote debugging port, and I opened 20 tabs (per your launcher) and left it while I went to a meeting (so, 30+ minutes). My computer has ~200GB of RAM though, so if the issue is running out of memory, that could explain the difference.

### em...@gmail.com (2024-01-22)

I opened 15 browsers (without using --headless and --remote-debugging-port), and after many tests, it consistently reproduced within a minute every time.
luancher.sh:
chrome     --user-data-dir=/tmp/xx1  --disable-gpu --incognito --no-sandbox   http://localhost:8605/crash2/crash.html  &
````
chrome     --user-data-dir=/tmp/xx15 --disable-gpu --incognito --no-sandbox   http://localhost:8605/crash2/crash.html  && fg

Here is the memory usage data I recorded(It seems that the issue is not related toOOM.):
pwn11@pwn11:~$ free -h
               total        used        free      shared  buff/cache   available
Mem:           125Gi       2.3Gi       117Gi        24Mi       5.7Gi       122Gi
Swap:          2.0Gi          0B       2.0Gi
```
before trigger first uaf:
pwn11@pwn11:~$ free -h
               total        used        free      shared  buff/cache   available
Mem:           125Gi        27Gi        92Gi       593Mi       6.1Gi        96Gi
Swap:          2.0Gi          0B       2.0Gi
after trigger first uaf:
pwn11@pwn11:~$ free -h
               total        used        free      shared  buff/cache   available
Mem:           125Gi        27Gi        92Gi       508Mi       6.0Gi        96Gi
Swap:          2.0Gi          0B       2.0Gi

### sy...@chromium.org (2024-01-22)

Thanks for verifying it's not OOM.

@Peng, the stack trace looks similar to a bug you fixed before (see https://crbug.com/chromium/1502620#c23), perhaps you'll have better luck reproducing and fixing this?

### th...@chromium.org (2024-01-30)

[secondary shepherd] penghuang@, could you confirm whether you intend to take a look at this?

### pe...@chromium.org (2024-01-30)

I think they are different. In https://crbug.com/chromium/4232858, the VkImage is destroyed by chrome, and the image could be still used by ANGLE. However i this issue, the vulkan object is destroyed via ANGLE API. And UAF is also by ANGLE. So it is likely an ANGLE issue.

### is...@google.com (2024-01-30)

This issue was migrated from crbug.com/chromium/1502620?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### sy...@chromium.org (2024-02-15)

@reporter,  do you think you could run your repro with Vulkan Validation Layers enabled? I'd love to get this fixed of course, but there's really nothing I can do without the ability to reproduce this.

### em...@gmail.com (2024-02-15)

I haven't used VVL before, but I'm willing to give it a try. Could you provide me with some steps I need to follow?

### em...@gmail.com (2024-02-15)

I can see that the Vulkan Validation Layers are already enabled in the debug build
VK_LOADER_DEBUG=all
INFO | LAYER:      Insert instance layer "VK_LAYER_KHRONOS_validation" (angledata/../libVkLayer_khronos_validation.so)

### em...@gmail.com (2024-02-15)

I'm getting this type of error message here, not sure if it's helpful.

[0216/003650.203711:ERROR:angle_platform_impl.cc(44)] RendererVk.cpp:780 (DebugUtilsMessenger): [ VUID-vkDestroyImage-image-01000 ] Validation Error: [ VUID-vkDestroyImage-image-01000 ] | MessageID = 0xf2d29b5a | vkDestroyImage():  can't be called on VkImage 0x19c400000019c4[] that is currently in use by VkImageView 0x19c500000019c5[]. The Vulkan spec states: All submitted commands that refer to image, either directly or via a VkImageView, must have completed execution (https://www.khronos.org/registry/vulkan/specs/1.3-extensions/html/vkspec.html#VUID-vkDestroyImage-image-01000)

ERR: RendererVk.cpp:780 (DebugUtilsMessenger): [ VUID-vkDestroyImage-image-01000 ] Validation Error: [ VUID-vkDestroyImage-image-01000 ] | MessageID = 0xf2d29b5a | vkDestroyImage():  can't be called on VkImage 0x19c400000019c4[] that is currently in use by VkImageView 0x19c500000019c5[]. The Vulkan spec states: All submitted commands that refer to image, either directly or via a VkImageView, must have completed execution (https://www.khronos.org/registry/vulkan/specs/1.3-extensions/html/vkspec.html#VUID-vkDestroyImage-image-01000)

```

[2257848:2258105:0216/003810.275808:ERROR:angle_platform_impl.cc(44)] RendererVk.cpp:780 (DebugUtilsMessenger): [ VUID-vkDestroyImageView-imageView-01026 ] Validation Error: [ VUID-vkDestroyImageView-imageView-01026 ] | MessageID = 0x63ac21f0 | vkDestroyImageView():  can't be called on VkImageView 0x4d500000004d5[] that is currently in use by VkDescriptorSet 0x42a000000042a[]. The Vulkan spec states: All submitted commands that refer to imageView must have completed execution (https://www.khronos.org/registry/vulkan/specs/1.3-extensions/html/vkspec.html#VUID-vkDestroyImageView-imageView-01026)

ERR: RendererVk.cpp:780 (DebugUtilsMessenger): [ VUID-vkDestroyImageView-imageView-01026 ] Validation Error: [ VUID-vkDestroyImageView-imageView-01026 ] | MessageID = 0x63ac21f0 | vkDestroyImageView():  can't be called on VkImageView 0x4d500000004d5[] that is currently in use by VkDescriptorSet 0x42a000000042a[]. The Vulkan spec states: All submitted commands that refer to imageView must have completed execution (https://www.khronos.org/registry/vulkan/specs/1.3-extensions/html/vkspec.html#VUID-vkDestroyImageView-imageView-01026)


### sy...@chromium.org (2024-02-16)

Excellent, thank you that exactly confirms the issue. That's interesting, so there's a renderbuffer's image used in a descriptor set. That only happens with ANGLE's internal shaders, so it looks like the blits in the repro file are falling back to shader-based blits. So the issue seems to be that an internal shader call is not marking the image appropriately as being in use.

I see crash.html tests both depth and stencil. Those may actually take different paths (based on hardware). Does the issue reproduce if crash.html only does the depth part? What if it only does the stencil part?

And if I provide a patch with added logs, would you be able to build and run with it?

### em...@gmail.com (2024-02-16)

I'm delighted to hear that you've pinpointed the issue. I have tested the scenarios you mentioned, and I can confirm that the issue does not occur when either the depth part or the stencil part is used exclusively.

Should you be able to provide a patch with additional logging, I would be more than happy to assist in testing it.

### sy...@chromium.org (2024-02-16)

Awesome, thank you so much. Let's start with this patch, and please keep VVL on (I'm relying on its report about which image/view is the issue):

```
diff --git a/src/libANGLE/renderer/vulkan/FramebufferVk.cpp b/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
index 2668a3098..1e5793ced 100644
--- a/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
+++ b/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
@@ -1131,6 +1131,8 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
     const bool blitDepthBuffer   = (mask & GL_DEPTH_BUFFER_BIT) != 0;
     const bool blitStencilBuffer = (mask & GL_STENCIL_BUFFER_BIT) != 0;
 
+    WARN() << "FramebufferVk::blit " << (blitDepthBuffer ? "depth " : " ") << (blitStencilBuffer ? "stencil " : " ");
+
     // If a framebuffer contains a mixture of multisampled and multisampled-render-to-texture
     // attachments, this function could be simultaneously doing a blit on one attachment and resolve
     // on another.  For the most part, this means resolve semantics apply.  However, as the resolve
@@ -1144,6 +1146,8 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
         srcFramebufferVk->getDepthStencilRenderTarget()->getImageForCopy().getSamples() > 1;
     const bool isResolve = isColorResolve || isDepthStencilResolve;
 
+    WARN() << "FramebufferVk::blit resolve? " << isResolve;
+
     bool srcFramebufferFlippedY = contextVk->isViewportFlipEnabledForReadFBO();
     bool dstFramebufferFlippedY = contextVk->isViewportFlipEnabledForDrawFBO();
 
@@ -1191,6 +1195,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
     gl::Rectangle clippedSourceArea;
     if (!gl::ClipRectangle(srcFramebufferDimensions, absSourceArea, &clippedSourceArea))
     {
+        WARN() << " - skip due to source clip";
         return angle::Result::Continue;
     }
 
@@ -1306,6 +1311,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
     gl::Rectangle blitArea;
     if (!gl::ClipRectangle(getRotatedScissoredRenderArea(contextVk), srcClippedDestArea, &blitArea))
     {
+        WARN() << " - skip due to dest clip";
         return angle::Result::Continue;
     }
 
@@ -1333,6 +1339,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
 
     if (blitColorBuffer)
     {
+        WARN() << " - Blit color";
         RenderTargetVk *readRenderTarget      = srcFramebufferVk->getColorReadRenderTarget();
         UtilsVk::BlitResolveParameters params = commonParams;
         params.srcLayer                       = readRenderTarget->getLayerIndex();
@@ -1460,6 +1467,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
 
     if (blitDepthBuffer || blitStencilBuffer)
     {
+        WARN() << " - Blit depth stencil";
         RenderTargetVk *readRenderTarget      = srcFramebufferVk->getDepthStencilRenderTarget();
         RenderTargetVk *drawRenderTarget      = mRenderTargetCache.getDepthStencil();
         UtilsVk::BlitResolveParameters params = commonParams;
@@ -1481,6 +1489,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
 
         if (canBlitWithCommand && areChannelsBlitCompatible)
         {
+            WARN() << " - Blit depth stencil with command " << blitDepthBuffer << " " << blitStencilBuffer;
             ANGLE_TRY(blitWithCommand(contextVk, sourceArea, destArea, readRenderTarget,
                                       drawRenderTarget, filter, false, blitDepthBuffer,
                                       blitStencilBuffer, flipX, flipY));
@@ -1507,25 +1516,30 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
 
             if (blitDepthBuffer)
             {
+                WARN() << " - create view for depth image " << depthStencilImage->getImage().getHandle();
                 ANGLE_TRY(depthStencilImage->initLayerImageView(
                     contextVk, textureType, VK_IMAGE_ASPECT_DEPTH_BIT, gl::SwizzleState(),
                     &depthView.get(), levelIndex, 1, layerIndex, 1,
                     gl::SrgbWriteControlMode::Default, gl::YuvSamplingMode::Default,
                     vk::ImageHelper::kDefaultImageViewUsageFlags));
+                WARN() << "   - " << depthView.get().getHandle();
             }
 
             if (blitStencilBuffer)
             {
+                WARN() << " - create view for stencil image " << depthStencilImage->getImage().getHandle();
                 ANGLE_TRY(depthStencilImage->initLayerImageView(
                     contextVk, textureType, VK_IMAGE_ASPECT_STENCIL_BIT, gl::SwizzleState(),
                     &stencilView.get(), levelIndex, 1, layerIndex, 1,
                     gl::SrgbWriteControlMode::Default, gl::YuvSamplingMode::Default,
                     vk::ImageHelper::kDefaultImageViewUsageFlags));
+                WARN() << "   - " << stencilView.get().getHandle();
             }
 
             // If shader stencil export is not possible, defer stencil blit/resolve to another pass.
             bool hasShaderStencilExport =
                 contextVk->getRenderer()->getFeatures().supportsShaderStencilExport.enabled;
+            WARN() << " - has stencil export? " << hasShaderStencilExport;
 
             // Blit depth. If shader stencil export is present, blit stencil as well.
             if (blitDepthBuffer || (blitStencilBuffer && hasShaderStencilExport))
@@ -1534,6 +1548,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
                 const vk::ImageView *stencil =
                     blitStencilBuffer && hasShaderStencilExport ? &stencilView.get() : nullptr;
 
+                WARN() << " - utilsVk.depthStencilBlitResolve";
                 ANGLE_TRY(utilsVk.depthStencilBlitResolve(contextVk, this, depthStencilImage, depth,
                                                           stencil, params));
             }
@@ -1544,6 +1559,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
                 ANGLE_VK_PERF_WARNING(contextVk, GL_DEBUG_SEVERITY_LOW,
                                       "Inefficient BlitFramebuffer operation on the stencil aspect "
                                       "due to lack of shader stencil export support");
+                WARN() << " - utilsVk.stencilBlitResolveNoShaderExport";
                 ANGLE_TRY(utilsVk.stencilBlitResolveNoShaderExport(
                     contextVk, this, depthStencilImage, &stencilView.get(), params));
             }
@@ -1551,11 +1567,14 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
             vk::ImageView depthViewObject   = depthView.release();
             vk::ImageView stencilViewObject = stencilView.release();
 
+            WARN() << " - add views to garbage";
             contextVk->addGarbage(&depthViewObject);
             contextVk->addGarbage(&stencilViewObject);
+            WARN() << " - add views to garbage ... done";
         }
     }
 
+    WARN() << " - FramebufferVk::blit ... done";
     return angle::Result::Continue;
 }
 
diff --git a/src/libANGLE/renderer/vulkan/UtilsVk.cpp b/src/libANGLE/renderer/vulkan/UtilsVk.cpp
index d739dae26..aee060585 100644
--- a/src/libANGLE/renderer/vulkan/UtilsVk.cpp
+++ b/src/libANGLE/renderer/vulkan/UtilsVk.cpp
@@ -2829,6 +2829,7 @@ angle::Result UtilsVk::blitResolveImpl(ContextVk *contextVk,
     vk::ImageLayout srcImagelayout = src->isDepthOrStencil()
                                          ? vk::ImageLayout::DepthReadStencilReadFragmentShaderRead
                                          : vk::ImageLayout::FragmentShaderReadOnly;
+    WARN() << " - UtilsVk::blitResolveImpl onImageRenderPassRead for " << src->getImage().getHandle();
     contextVk->onImageRenderPassRead(src->getAspectFlags(), srcImagelayout, src);
 
     UpdateColorAccess(contextVk, framebuffer->getState().getColorAttachmentsMask(),
@@ -2837,20 +2838,24 @@ angle::Result UtilsVk::blitResolveImpl(ContextVk *contextVk,
 
     VkDescriptorImageInfo imageInfos[2] = {};
 
+    WARN() << " - UtilsVk::blitResolveImpl using image views:";
     if (blitColor)
     {
         imageInfos[0].imageView   = srcColorView->getHandle();
         imageInfos[0].imageLayout = src->getCurrentLayout(contextVk);
+        WARN() << "   - Color: " << imageInfos[0].imageView;
     }
     if (blitDepth)
     {
         imageInfos[0].imageView   = srcDepthView->getHandle();
         imageInfos[0].imageLayout = src->getCurrentLayout(contextVk);
+        WARN() << "   - Depth: " << imageInfos[0].imageView;
     }
     if (blitStencil)
     {
         imageInfos[1].imageView   = srcStencilView->getHandle();
         imageInfos[1].imageLayout = src->getCurrentLayout(contextVk);
+        WARN() << "   - Stencil: " << imageInfos[1].imageView;
     }
 
     VkDescriptorImageInfo samplerInfo = {};
@@ -3033,7 +3038,9 @@ angle::Result UtilsVk::stencilBlitResolveNoShaderExport(ContextVk *contextVk,
 
     // Change layouts prior to computation.
     vk::CommandBufferAccess access;
+    WARN() << " - UtilsVk::stencilBlitResolveNoShaderExport onImageComputeShaderRead for " << src->getImage().getHandle();
     access.onImageComputeShaderRead(src->getAspectFlags(), src);
+    WARN() << " - UtilsVk::stencilBlitResolveNoShaderExport onImageTransferWrite for " << depthStencilImage->getImage().getHandle();
     access.onImageTransferWrite(depthStencilRenderTarget->getLevelIndex(), 1,
                                 depthStencilRenderTarget->getLayerIndex(), 1,
                                 depthStencilImage->getAspectFlags(), depthStencilImage);
@@ -3047,10 +3054,13 @@ angle::Result UtilsVk::stencilBlitResolveNoShaderExport(ContextVk *contextVk,
     ANGLE_TRY(allocateDescriptorSet(contextVk, commandBufferHelper,
                                     Function::BlitResolveStencilNoExport, &descriptorSet));
 
+    WARN() << " - UtilsVk::stencilBlitResolveNoShaderExport using image views:";
+
     // Blit/resolve stencil into the buffer.
     VkDescriptorImageInfo imageInfo = {};
     imageInfo.imageView             = srcStencilView->getHandle();
     imageInfo.imageLayout           = src->getCurrentLayout(contextVk);
+    WARN() << "   - Stencil: " << imageInfo.imageView;
 
     VkDescriptorBufferInfo bufferInfo = {};
     bufferInfo.buffer                 = blitBuffer.get().getBuffer().getHandle();
```

### em...@gmail.com (2024-02-16)

The debug version I have is an older one saved without the source code, so I'll need to recompile latest version before testing. I'll update as soon as I have any results. Thanks!

### em...@gmail.com (2024-02-16)

Please refer to the attachment.

### sy...@chromium.org (2024-02-16)

Thanks. So far, the logs don't show a problem. I do see a bit of an exceptional path here for views, which may be the cause of the problem but I can't see a problem through code inspection. In particular, we typically have the image views live alongside images, so they are also released together. For depth/stencil blit in particular, the views are temporary and are added to the (context) garbage list separately from the image. However:

- I see the context garbage list is processed on submit, after whatever else might have been garbage collected. This in itself could lead to a (harmless) validation failure, but that's not the issue here. In particular, the stack trace in OP shows that `RenderbufferVk::releaseImage` leads to `DestroyGarbage` straightaway. This means that when `RenderbufferVk::releaseImage` is called, the submission in which the image was last used is considered finished.
- If the submission the image was last used is finished already (as indicated by CommandQueue), then any garbage associated with that submission must have already been cleaned up, so the views must have already been deleted.

So let me add more logs and we can dig deeper

### sy...@chromium.org (2024-02-16)

Realized while adding logs that garbage clean up is done in a thread, so I guess it _is_ possible for the first scenario to happen (the view is deleted after the image). I wouldn't expect that to crash in SwiftShader though, because the SwiftShader stack trace shows that image is in fact being rendered with. Another possibility is a confusion with the descriptor set, but let's see first if these logs turn anything up:

```
diff --git a/src/libANGLE/renderer/vulkan/CommandProcessor.cpp b/src/libANGLE/renderer/vulkan/CommandProcessor.cpp
index 80282af5b..fa652448d 100644
--- a/src/libANGLE/renderer/vulkan/CommandProcessor.cpp
+++ b/src/libANGLE/renderer/vulkan/CommandProcessor.cpp
@@ -1132,6 +1132,7 @@ void CommandQueue::handleDeviceLost(RendererVk *renderer)
         if (batch.hasFence())
         {
             VkResult status = batch.waitFence(device, renderer->getMaxFenceWaitTimeNs());
+            WARN() << "CommandQueue::handleDeviceLost -- finished " << batch.queueSerial;
             // If the wait times out, it is probably not possible to recover from lost device
             ASSERT(status == VK_SUCCESS || status == VK_ERROR_DEVICE_LOST);
 
@@ -1200,6 +1201,7 @@ angle::Result CommandQueue::finishResourceUse(Context *context,
             {
                 ANGLE_VK_TRY(context,
                              mInFlightCommands.front().waitFenceUnlocked(device, timeout, &lock));
+                WARN() << "CommandQueue::finishResourceUse -- finished " << mInFlightCommands.front().queueSerial;
             }
         }
         // Check the rest of the commands in case they are also finished.
@@ -1264,15 +1266,18 @@ angle::Result CommandQueue::waitForResourceUseToFinishWithUserTimeout(Context *c
             if (!finished)
             {
                 *result = mInFlightCommands.front().waitFenceUnlocked(device, timeout, &lock);
+                WARN() << "CommandQueue::waitForResourceUseToFinishWithUserTimeout -- finished " << mInFlightCommands.front().queueSerial;
                 // Don't trigger an error on timeout.
                 if (*result == VK_TIMEOUT)
                 {
+                    WARN() << " -- timed out";
                     break;
                 }
                 else
                 {
                     ANGLE_VK_TRY(context, *result);
                 }
+                WARN() << " -- success";
             }
             else
             {
@@ -1600,6 +1605,8 @@ angle::Result CommandQueue::checkOneCommandBatch(Context *context, bool *finishe
         ANGLE_VK_TRY(context, status);
     }
 
+    WARN() << "CommandQueue::checkOneCommandBatch -- finished " << batch.queueSerial;
+
     // Finished.
     mLastCompletedSerials.setQueueSerial(batch.queueSerial);
 
@@ -1638,6 +1645,7 @@ angle::Result CommandQueue::finishOneCommandBatchAndCleanupImpl(Context *context
     if (batch.hasFence())
     {
         VkResult status = batch.waitFence(context->getDevice(), timeout);
+        WARN() << "CommandQueue::finishOneCommandBatchAndCleanupImpl -- finished " << batch.queueSerial;
         ANGLE_VK_TRY(context, status);
     }
 
@@ -1666,6 +1674,8 @@ angle::Result CommandQueue::retireFinishedCommandsLocked(Context *context)
         CommandBatch &batch = mFinishedCommandBatches.front();
         ASSERT(batch.queueSerial <= mLastCompletedSerials);
 
+        WARN() << "CommandQueue::retireFinishedCommandsLocked -- retire " << batch.queueSerial;
+
         batch.releaseFence();
 
         if (batch.primaryCommands.valid())
diff --git a/src/libANGLE/renderer/vulkan/ContextVk.cpp b/src/libANGLE/renderer/vulkan/ContextVk.cpp
index 423b10bcb..395b29719 100644
--- a/src/libANGLE/renderer/vulkan/ContextVk.cpp
+++ b/src/libANGLE/renderer/vulkan/ContextVk.cpp
@@ -3653,6 +3653,7 @@ angle::Result ContextVk::submitCommands(const vk::Semaphore *signalSemaphore,
     {
         // Clean up garbage.
         vk::ResourceUse use(mLastFlushedQueueSerial);
+        WARN() << "ContextVk::submitCommands -- add garbage to renderer " << use << " (" << mCurrentGarbage.data() << ")";
         mRenderer->collectGarbage(use, std::move(mCurrentGarbage));
     }
 
diff --git a/src/libANGLE/renderer/vulkan/FramebufferVk.cpp b/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
index 2668a3098..1e5793ced 100644
--- a/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
+++ b/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
@@ -1131,6 +1131,8 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
     const bool blitDepthBuffer   = (mask & GL_DEPTH_BUFFER_BIT) != 0;
     const bool blitStencilBuffer = (mask & GL_STENCIL_BUFFER_BIT) != 0;
 
+    WARN() << "FramebufferVk::blit " << (blitDepthBuffer ? "depth " : " ") << (blitStencilBuffer ? "stencil " : " ");
+
     // If a framebuffer contains a mixture of multisampled and multisampled-render-to-texture
     // attachments, this function could be simultaneously doing a blit on one attachment and resolve
     // on another.  For the most part, this means resolve semantics apply.  However, as the resolve
@@ -1144,6 +1146,8 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
         srcFramebufferVk->getDepthStencilRenderTarget()->getImageForCopy().getSamples() > 1;
     const bool isResolve = isColorResolve || isDepthStencilResolve;
 
+    WARN() << "FramebufferVk::blit resolve? " << isResolve;
+
     bool srcFramebufferFlippedY = contextVk->isViewportFlipEnabledForReadFBO();
     bool dstFramebufferFlippedY = contextVk->isViewportFlipEnabledForDrawFBO();
 
@@ -1191,6 +1195,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
     gl::Rectangle clippedSourceArea;
     if (!gl::ClipRectangle(srcFramebufferDimensions, absSourceArea, &clippedSourceArea))
     {
+        WARN() << " - skip due to source clip";
         return angle::Result::Continue;
     }
 
@@ -1306,6 +1311,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
     gl::Rectangle blitArea;
     if (!gl::ClipRectangle(getRotatedScissoredRenderArea(contextVk), srcClippedDestArea, &blitArea))
     {
+        WARN() << " - skip due to dest clip";
         return angle::Result::Continue;
     }
 
@@ -1333,6 +1339,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
 
     if (blitColorBuffer)
     {
+        WARN() << " - Blit color";
         RenderTargetVk *readRenderTarget      = srcFramebufferVk->getColorReadRenderTarget();
         UtilsVk::BlitResolveParameters params = commonParams;
         params.srcLayer                       = readRenderTarget->getLayerIndex();
@@ -1460,6 +1467,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
 
     if (blitDepthBuffer || blitStencilBuffer)
     {
+        WARN() << " - Blit depth stencil";
         RenderTargetVk *readRenderTarget      = srcFramebufferVk->getDepthStencilRenderTarget();
         RenderTargetVk *drawRenderTarget      = mRenderTargetCache.getDepthStencil();
         UtilsVk::BlitResolveParameters params = commonParams;
@@ -1481,6 +1489,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
 
         if (canBlitWithCommand && areChannelsBlitCompatible)
         {
+            WARN() << " - Blit depth stencil with command " << blitDepthBuffer << " " << blitStencilBuffer;
             ANGLE_TRY(blitWithCommand(contextVk, sourceArea, destArea, readRenderTarget,
                                       drawRenderTarget, filter, false, blitDepthBuffer,
                                       blitStencilBuffer, flipX, flipY));
@@ -1507,25 +1516,30 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
 
             if (blitDepthBuffer)
             {
+                WARN() << " - create view for depth image " << depthStencilImage->getImage().getHandle();
                 ANGLE_TRY(depthStencilImage->initLayerImageView(
                     contextVk, textureType, VK_IMAGE_ASPECT_DEPTH_BIT, gl::SwizzleState(),
                     &depthView.get(), levelIndex, 1, layerIndex, 1,
                     gl::SrgbWriteControlMode::Default, gl::YuvSamplingMode::Default,
                     vk::ImageHelper::kDefaultImageViewUsageFlags));
+                WARN() << "   - " << depthView.get().getHandle();
             }
 
             if (blitStencilBuffer)
             {
+                WARN() << " - create view for stencil image " << depthStencilImage->getImage().getHandle();
                 ANGLE_TRY(depthStencilImage->initLayerImageView(
                     contextVk, textureType, VK_IMAGE_ASPECT_STENCIL_BIT, gl::SwizzleState(),
                     &stencilView.get(), levelIndex, 1, layerIndex, 1,
                     gl::SrgbWriteControlMode::Default, gl::YuvSamplingMode::Default,
                     vk::ImageHelper::kDefaultImageViewUsageFlags));
+                WARN() << "   - " << stencilView.get().getHandle();
             }
 
             // If shader stencil export is not possible, defer stencil blit/resolve to another pass.
             bool hasShaderStencilExport =
                 contextVk->getRenderer()->getFeatures().supportsShaderStencilExport.enabled;
+            WARN() << " - has stencil export? " << hasShaderStencilExport;
 
             // Blit depth. If shader stencil export is present, blit stencil as well.
             if (blitDepthBuffer || (blitStencilBuffer && hasShaderStencilExport))
@@ -1534,6 +1548,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
                 const vk::ImageView *stencil =
                     blitStencilBuffer && hasShaderStencilExport ? &stencilView.get() : nullptr;
 
+                WARN() << " - utilsVk.depthStencilBlitResolve";
                 ANGLE_TRY(utilsVk.depthStencilBlitResolve(contextVk, this, depthStencilImage, depth,
                                                           stencil, params));
             }
@@ -1544,6 +1559,7 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
                 ANGLE_VK_PERF_WARNING(contextVk, GL_DEBUG_SEVERITY_LOW,
                                       "Inefficient BlitFramebuffer operation on the stencil aspect "
                                       "due to lack of shader stencil export support");
+                WARN() << " - utilsVk.stencilBlitResolveNoShaderExport";
                 ANGLE_TRY(utilsVk.stencilBlitResolveNoShaderExport(
                     contextVk, this, depthStencilImage, &stencilView.get(), params));
             }
@@ -1551,11 +1567,14 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
             vk::ImageView depthViewObject   = depthView.release();
             vk::ImageView stencilViewObject = stencilView.release();
 
+            WARN() << " - add views to garbage";
             contextVk->addGarbage(&depthViewObject);
             contextVk->addGarbage(&stencilViewObject);
+            WARN() << " - add views to garbage ... done";
         }
     }
 
+    WARN() << " - FramebufferVk::blit ... done";
     return angle::Result::Continue;
 }
 
diff --git a/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp b/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp
index f8dd437e1..5d6fd2dfa 100644
--- a/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp
+++ b/src/libANGLE/renderer/vulkan/RenderbufferVk.cpp
@@ -306,6 +306,7 @@ void RenderbufferVk::releaseOwnershipOfImage(const gl::Context *context)
 
 void RenderbufferVk::releaseAndDeleteImage(ContextVk *contextVk)
 {
+    WARN() << "RenderbufferVk::releaseAndDeleteImage " << (mImage ? mImage->getImage().getHandle() : nullptr);
     releaseImage(contextVk);
     SafeDelete(mImage);
     mImageObserverBinding.bind(nullptr);
diff --git a/src/libANGLE/renderer/vulkan/RendererVk.cpp b/src/libANGLE/renderer/vulkan/RendererVk.cpp
index 5088328f2..90d1d5e5c 100644
--- a/src/libANGLE/renderer/vulkan/RendererVk.cpp
+++ b/src/libANGLE/renderer/vulkan/RendererVk.cpp
@@ -5326,6 +5326,7 @@ bool RendererVk::haveSameFormatFeatureBits(angle::FormatID formatID1,
 
 void RendererVk::cleanupGarbage()
 {
+    WARN() << std::this_thread::get_id() << " Clean up garbage";
     // Clean up general garbage
     mSharedGarbageList.cleanupSubmittedGarbage(this);
     // Clean up suballocation garbages
diff --git a/src/libANGLE/renderer/vulkan/ResourceVk.cpp b/src/libANGLE/renderer/vulkan/ResourceVk.cpp
index aa44a9539..365703301 100644
--- a/src/libANGLE/renderer/vulkan/ResourceVk.cpp
+++ b/src/libANGLE/renderer/vulkan/ResourceVk.cpp
@@ -81,6 +81,8 @@ SharedGarbage &SharedGarbage::operator=(SharedGarbage &&rhs)
 
 bool SharedGarbage::destroyIfComplete(RendererVk *renderer)
 {
+    WARN() << "SharedGarbage::destroyIfComplete -- garbage (" << mGarbage.data() << ") lifetime " <<
+        mLifetime << " finished? " << renderer->hasResourceUseFinished(mLifetime);
     if (renderer->hasResourceUseFinished(mLifetime))
     {
         for (GarbageObject &object : mGarbage)
diff --git a/src/libANGLE/renderer/vulkan/UtilsVk.cpp b/src/libANGLE/renderer/vulkan/UtilsVk.cpp
index d739dae26..aee060585 100644
--- a/src/libANGLE/renderer/vulkan/UtilsVk.cpp
+++ b/src/libANGLE/renderer/vulkan/UtilsVk.cpp
@@ -2829,6 +2829,7 @@ angle::Result UtilsVk::blitResolveImpl(ContextVk *contextVk,
     vk::ImageLayout srcImagelayout = src->isDepthOrStencil()
                                          ? vk::ImageLayout::DepthReadStencilReadFragmentShaderRead
                                          : vk::ImageLayout::FragmentShaderReadOnly;
+    WARN() << " - UtilsVk::blitResolveImpl onImageRenderPassRead for " << src->getImage().getHandle();
     contextVk->onImageRenderPassRead(src->getAspectFlags(), srcImagelayout, src);
 
     UpdateColorAccess(contextVk, framebuffer->getState().getColorAttachmentsMask(),
@@ -2837,20 +2838,24 @@ angle::Result UtilsVk::blitResolveImpl(ContextVk *contextVk,
 
     VkDescriptorImageInfo imageInfos[2] = {};
 
+    WARN() << " - UtilsVk::blitResolveImpl using image views:";
     if (blitColor)
     {
         imageInfos[0].imageView   = srcColorView->getHandle();
         imageInfos[0].imageLayout = src->getCurrentLayout(contextVk);
+        WARN() << "   - Color: " << imageInfos[0].imageView;
     }
     if (blitDepth)
     {
         imageInfos[0].imageView   = srcDepthView->getHandle();
         imageInfos[0].imageLayout = src->getCurrentLayout(contextVk);
+        WARN() << "   - Depth: " << imageInfos[0].imageView;
     }
     if (blitStencil)
     {
         imageInfos[1].imageView   = srcStencilView->getHandle();
         imageInfos[1].imageLayout = src->getCurrentLayout(contextVk);
+        WARN() << "   - Stencil: " << imageInfos[1].imageView;
     }
 
     VkDescriptorImageInfo samplerInfo = {};
@@ -3033,7 +3038,9 @@ angle::Result UtilsVk::stencilBlitResolveNoShaderExport(ContextVk *contextVk,
 
     // Change layouts prior to computation.
     vk::CommandBufferAccess access;
+    WARN() << " - UtilsVk::stencilBlitResolveNoShaderExport onImageComputeShaderRead for " << src->getImage().getHandle();
     access.onImageComputeShaderRead(src->getAspectFlags(), src);
+    WARN() << " - UtilsVk::stencilBlitResolveNoShaderExport onImageTransferWrite for " << depthStencilImage->getImage().getHandle();
     access.onImageTransferWrite(depthStencilRenderTarget->getLevelIndex(), 1,
                                 depthStencilRenderTarget->getLayerIndex(), 1,
                                 depthStencilImage->getAspectFlags(), depthStencilImage);
@@ -3047,10 +3054,13 @@ angle::Result UtilsVk::stencilBlitResolveNoShaderExport(ContextVk *contextVk,
     ANGLE_TRY(allocateDescriptorSet(contextVk, commandBufferHelper,
                                     Function::BlitResolveStencilNoExport, &descriptorSet));
 
+    WARN() << " - UtilsVk::stencilBlitResolveNoShaderExport using image views:";
+
     // Blit/resolve stencil into the buffer.
     VkDescriptorImageInfo imageInfo = {};
     imageInfo.imageView             = srcStencilView->getHandle();
     imageInfo.imageLayout           = src->getCurrentLayout(contextVk);
+    WARN() << "   - Stencil: " << imageInfo.imageView;
 
     VkDescriptorBufferInfo bufferInfo = {};
     bufferInfo.buffer                 = blitBuffer.get().getBuffer().getHandle();
diff --git a/src/libANGLE/renderer/vulkan/vk_helpers.cpp b/src/libANGLE/renderer/vulkan/vk_helpers.cpp
index bf1d56431..e28a289fe 100644
--- a/src/libANGLE/renderer/vulkan/vk_helpers.cpp
+++ b/src/libANGLE/renderer/vulkan/vk_helpers.cpp
@@ -5832,6 +5832,8 @@ void ImageHelper::releaseImage(RendererVk *renderer)
                                   mVmaAllocation.getHandle());
     }
 
+    WARN() << std::this_thread::get_id() << " ImageHelper::releaseImage " << mImage.getHandle() << " Use: " << mUse <<
+        " finished? " << renderer->hasResourceUseFinished(mUse);
     renderer->collectGarbage(mUse, &mImage, &mDeviceMemory, &mVmaAllocation);
     mViewFormats.clear();
     mUse.reset();
```

### em...@gmail.com (2024-02-17)

Sorry, I just saw the email. The attachment is the output result after re patching.

### sy...@chromium.org (2024-02-17)

Thank you. I can confirm the issue with the VVL errors is the fact that image itself is destroyed before its views. I have to think about how to best avoid that, this probably affects everywhere we create temp views.

However, that still doesn't explain the ASAN failures. The failure is that SwiftShader is still using the image for sampling, which is not really true, ANGLE did wait for the image to finish being used (at least according to the tracking the logs reveal). I'll try to come up with some logs in SwiftShader this time so we can match up what ANGLE thinks is happening with what SwiftShader sees. I know the logs are a lot, are you able to run and capture logs until the ASAN failure happens? The VVL error seems to be a red herring.

### em...@gmail.com (2024-02-17)

Sure, my local machine is relatively easy to replicate UAF.

### ar...@chromium.org (2024-03-08)

**[Secondary security shepherd]**

Just wanted to follow up on this HIGH severity security bug affecting the STABLE channel. @syoussefi: I see you're assigned but there haven't been updates in the past 15 days. Is there anything I can do to assist, or would you be able to provide a status update?

Is SwiftShader still enabled in Chrome by default? The plan was to turn it down behind some disable by default command line argument.
If not, maybe this could become a `Security_Impact-None` bug?

### sy...@chromium.org (2024-03-09)

Sorry, sick kids and spring break crippled my ability to do anything here. I'll hopefully have something up for testing next week.

### sy...@chromium.org (2024-03-15)

I wrote a comment yesterday, but looks like I forgot to actually submit it. I wrote a test and found out the ordering of releasing the image and its view doesn't actually matter (at least no VVL errors). The VVL error here is actually about the image really being in use by the GPU (SwiftShader) and not just that there's a view refererencing it.

Could you please add these logs on top of the ones in #41 and see if this is somehow due to device loss?

```
diff --git a/src/libANGLE/renderer/vulkan/ContextVk.cpp b/src/libANGLE/renderer/vulkan/ContextVk.cpp
index 084149883..3f7a810eb 100644
--- a/src/libANGLE/renderer/vulkan/ContextVk.cpp
+++ b/src/libANGLE/renderer/vulkan/ContextVk.cpp
@@ -4068,6 +4068,7 @@ void ContextVk::clearAllGarbage()
 
 void ContextVk::handleDeviceLost()
 {
+    WARN() << "CONTEXT DEVICE LOST";
     vk::SecondaryCommandBufferCollector collector;
     (void)mOutsideRenderPassCommands->reset(this, &collector);
     (void)mRenderPassCommands->reset(this, &collector);
diff --git a/src/libANGLE/renderer/vulkan/RendererVk.cpp b/src/libANGLE/renderer/vulkan/RendererVk.cpp
index 9e9fce13e..01967dc8d 100644
--- a/src/libANGLE/renderer/vulkan/RendererVk.cpp
+++ b/src/libANGLE/renderer/vulkan/RendererVk.cpp
@@ -1534,6 +1534,7 @@ void RendererVk::onDestroy(vk::Context *context)
 
 void RendererVk::notifyDeviceLost()
 {
+    WARN() << "RENDERER DEVICE LOST";
     mDeviceLost = true;
     mGlobalOps->notifyDeviceLost();
 }
@@ -5581,6 +5582,7 @@ angle::Result RendererVk::submitPriorityDependency(vk::Context *context,
 
 void RendererVk::handleDeviceLost()
 {
+    WARN() << "RENDERER HANDLE DEVICE LOST";
     if (isAsyncCommandQueueEnabled())
     {
         mCommandProcessor.handleDeviceLost(this);
```

### ap...@google.com (2024-03-15)

Project: angle/angle
Branch: main

commit b3ab67d32b3adb6f62472b6046e91e6f7958926b
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Thu Mar 14 15:06:02 2024

    tests: Remove unnecessary .get() from RAII objects
    
    Bug: chromium:40942995
    Change-Id: I82509869bce3ad8f51811188fe04267f2de04786
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5370904
    Reviewed-by: Geoff Lang <geofflang@chromium.org>
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

M       src/tests/gl_tests/AtomicCounterBufferTest.cpp
M       src/tests/gl_tests/BPTCCompressedTextureTest.cpp
M       src/tests/gl_tests/BlendFuncExtendedTest.cpp
M       src/tests/gl_tests/BlitFramebufferANGLETest.cpp
M       src/tests/gl_tests/BufferDataTest.cpp
M       src/tests/gl_tests/ClientArraysTest.cpp
M       src/tests/gl_tests/ComputeShaderTest.cpp
M       src/tests/gl_tests/ContextNoErrorTest.cpp
M       src/tests/gl_tests/CopyTexture3DTest.cpp
M       src/tests/gl_tests/CopyTextureTest.cpp
M       src/tests/gl_tests/DXT1CompressedTextureTest.cpp
M       src/tests/gl_tests/DXTSRGBCompressedTextureTest.cpp
M       src/tests/gl_tests/DepthStencilFormatsTest.cpp
M       src/tests/gl_tests/DifferentStencilMasksTest.cpp
M       src/tests/gl_tests/DrawBaseVertexBaseInstanceTest.cpp
M       src/tests/gl_tests/DrawBaseVertexVariantsTest.cpp
M       src/tests/gl_tests/DrawBuffersTest.cpp
M       src/tests/gl_tests/DrawElementsTest.cpp
M       src/tests/gl_tests/ExternalBufferTest.cpp
M       src/tests/gl_tests/FenceSyncTests.cpp
M       src/tests/gl_tests/FramebufferTest.cpp
M       src/tests/gl_tests/GLSLTest.cpp
M       src/tests/gl_tests/ImageTest.cpp
M       src/tests/gl_tests/ImageTestMetal.mm
M       src/tests/gl_tests/KTXCompressedTextureTest.cpp
M       src/tests/gl_tests/MipmapTest.cpp
M       src/tests/gl_tests/MultisampleCompatibilityTest.cpp
M       src/tests/gl_tests/MultithreadingTest.cpp
M       src/tests/gl_tests/PixelLocalStorageTest.cpp
M       src/tests/gl_tests/PointSpritesTest.cpp
M       src/tests/gl_tests/ProgramPipelineTest.cpp
M       src/tests/gl_tests/RobustClientMemoryTest.cpp
M       src/tests/gl_tests/RobustResourceInitTest.cpp
M       src/tests/gl_tests/SRGBFramebufferTest.cpp
M       src/tests/gl_tests/SRGBTextureTest.cpp
M       src/tests/gl_tests/SamplersTest.cpp
M       src/tests/gl_tests/ShaderAlgorithmTest.cpp
M       src/tests/gl_tests/ShaderStorageBufferTest.cpp
M       src/tests/gl_tests/SimpleOperationTest.cpp
M       src/tests/gl_tests/SixteenBppTextureTest.cpp
M       src/tests/gl_tests/StateChangeTest.cpp
M       src/tests/gl_tests/TextureTest.cpp
M       src/tests/gl_tests/TransformFeedbackTest.cpp
M       src/tests/gl_tests/UniformBufferTest.cpp
M       src/tests/gl_tests/UniformTest.cpp
M       src/tests/gl_tests/VertexAttributeTest.cpp
M       src/tests/gl_tests/VulkanDescriptorSetTest.cpp
M       src/tests/gl_tests/VulkanPerformanceCounterTest.cpp
M       src/tests/gl_tests/WebGLCompatibilityTest.cpp
M       src/tests/gl_tests/WebGLFramebufferTest.cpp
M       src/tests/gl_tests/WebGLReadOutsideFramebufferTest.cpp

https://chromium-review.googlesource.com/5370904


### ap...@google.com (2024-03-15)

Project: angle/angle
Branch: main

commit 58065d0766e74d3f1d4213c8a80f456def3ece53
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Thu Mar 14 16:00:20 2024

    Vulkan: Add test that destroys view after the image
    
    A depth/stencil blit path can create temp views.  Temp objects are added
    to ContextVk::mCurrentGarbage, which is **appended** to the Renderer's
    garbage list.  If the image from which the view was created is released
    before the next submission (i.e. it's appended to the garbage list
    before ContextVk::mCurrentGarbage), the image can be destroyed before
    its dependent view is.
    
    This is not triggering any validation error however, so there doesn't
    seem to be a need for a fix.  For posterity, if this ordering needs to
    be fixed in the future, we can simply remove
    `ContextVk::mCurrentGarbage` and add garbage to the renderer directly.
    This was made possible a while back when the context was able to
    allocate its submission serial right away.  (Previously, the serial had
    to be determined after submission, which is why temp objects were kept
    in ContextVk until that serial is known)
    
    Bug: chromium:40942995
    Change-Id: I8a1270e635193dd7aff5b63cbf63c0c6a1fc061f
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5370782
    Reviewed-by: Yuxin Hu <yuxinhu@google.com>
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

M       src/tests/gl_tests/BlitFramebufferANGLETest.cpp

https://chromium-review.googlesource.com/5370782


### ap...@google.com (2024-03-16)

Project: chromium/src
Branch: main

commit f05f8586cdcfa83edfbc36275bdd36f55f148a0b
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Sat Mar 16 01:02:27 2024

    Roll ANGLE from 7220307bb2fb to 553e3c8038ee (8 revisions)
    
    https://chromium.googlesource.com/angle/angle.git/+log/7220307bb2fb..553e3c8038ee
    
    2024-03-15 m.maiya@samsung.com Vulkan: Async compile pipelines with different surface rotations
    2024-03-15 syoussefi@chromium.org Vulkan: Add test that destroys view after the image
    2024-03-15 kkinnunen@apple.com Make ImmutableString::beginsWith constexpr
    2024-03-15 m.maiya@samsung.com Consider textures without an attached Buffer as incomplete
    2024-03-15 syoussefi@chromium.org Vulkan: Move renderer to namespace vk
    2024-03-15 syoussefi@chromium.org tests: Remove unnecessary .get() from RAII objects
    2024-03-15 romanl@google.com Multisampling support check: sampleCounts > 1 and createFlags
    2024-03-15 romanl@google.com Trace tests: check and log zlib crc32 on decompress failure
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/angle-chromium-autoroll
    Please CC abdolrashidi@google.com,angle-team@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
    Bug: chromium:40942995
    Tbr: abdolrashidi@google.com
    Change-Id: I1f87a5b58eb838fd8c580472fa0c27e00315bd3a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5375643
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1273745}

M       DEPS
M       third_party/angle

https://chromium-review.googlesource.com/5375643


### em...@gmail.com (2024-03-18)

#47.
I apologize for the late response. I was occupied with other matters and only just saw your email.

I tested the log patch with the latest debug version and couldn't reproduce the VVL error message, but the UAF is still reproducible in the asan non-debug version.

I have modified the original POC. Now, there's no need to open multiple browsers; the issue will reproduce after several page refreshes. Could you please try the new poc?

Tested version:
Chromium 124.0.6356.2 (costom asan build)
Chromium 124.0.6362.0 (gs://chromium-browser-asan/linux-release/asan-linux-release-1273779.zip)

### sy...@chromium.org (2024-03-21)

Thank you. I haven't had a chance to try it, but looking at the code I noticed this in the color resolve path:

```
            // Flush the render pass, which may incur a vkQueueSubmit, before taking any views.
            // Otherwise the view serials would not reflect the render pass they are really used in.
            // http://crbug.com/1272266#c22
            ANGLE_TRY(
                contextVk->flushCommandsAndEndRenderPass(RenderPassClosureReason::PrepareForBlit));

```

The tracking of resource has drastically changed since that was added, but I think this flush is still necessary in the latest model. The issue here is very likely the same thing. That should be easy to confirm. Does the ASAN error still reproduce with this change?

```
diff --git a/src/libANGLE/renderer/vulkan/FramebufferVk.cpp b/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
index 70e30ea3e..24eedb9c7 100644
--- a/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
+++ b/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
@@ -1495,6 +1499,9 @@ angle::Result FramebufferVk::blit(const gl::Context *context,
         }
         else
         {
+            ANGLE_TRY(
+                contextVk->flushCommandsAndEndRenderPass(RenderPassClosureReason::PrepareForBlit));
+
             // Now that all flipping is done, adjust the offsets for resolve and prerotation
             if (isDepthStencilResolve)
             {

```

### em...@gmail.com (2024-03-21)

Just tested, it can still reproduced after patching.

### sy...@chromium.org (2024-03-27)

For posterity, this change could make this easier to reproduce: <https://chromium-review.googlesource.com/c/angle/angle/+/3646597>

I'll try your new repro tomorrow and see if I can reproduce the issue (perhaps with the help of that CL)

### sy...@chromium.org (2024-03-28)

I can reproduce the ASAN failure with the minimized test case (crash2.html), thank you! The CL in the previous comment actually made the failure go away.

It also looks like disabling VK\_EXT\_shader\_stencil\_export makes the issue go away; that is the problem happens when UtilsVk blits stencil with a draw call instead of the dispatch + copy fallback. It may not be specific to stencil however, the test blits depth to that takes the same draw path, so perhaps alternating between draw and dispatch is what makes it pass when that extension is disabled.

### sy...@chromium.org (2024-03-28)

Hard to make progress given how slow it is to reproduce this. I have yet to figure this out, and it'll have to wait a week or two until I go back to the office.

In the meantime, I thought I'd make garbage cleanup faster by doing it right away (instead of deferring to thread), but I wasn't able to reproduce after that. I don't know yet if that's because I simultaneously set debug symbol level to 2 or not (because I once breaked with gdb at the crash point but couldn't get anything useful with symbol level 1).

Do you think you think you could try this patch to see if you can still reproduce with it?

```
diff --git a/src/libANGLE/renderer/vulkan/CommandProcessor.cpp b/src/libANGLE/renderer/vulkan/CommandProcessor.cpp
index 80282af5b..112ddc685 100644
--- a/src/libANGLE/renderer/vulkan/CommandProcessor.cpp
+++ b/src/libANGLE/renderer/vulkan/CommandProcessor.cpp
@@ -600,12 +600,22 @@ angle::Result CommandProcessor::queueCommand(CommandProcessorTask &&task)
 
 void CommandProcessor::requestCommandsAndGarbageCleanup()
 {
+#if 0
     if (!mNeedCommandsAndGarbageCleanup.exchange(true))
     {
         // request clean up in async thread
         std::unique_lock<std::mutex> enqueueLock(mTaskEnqueueMutex);
         mWorkAvailableCondition.notify_one();
     }
+#else
+    // Reset command buffer and clean up garbage
+    if (mRenderer->isAsyncCommandBufferResetEnabled() &&
+            mCommandQueue->hasFinishedCommands())
+    {
+        (void)mCommandQueue->retireFinishedCommands(this);
+    }
+    mRenderer->cleanupGarbage();
+#endif
 }
 
 void CommandProcessor::processTasks()
@@ -676,6 +686,7 @@ angle::Result CommandProcessor::processTasksImpl(bool *exitThread)
             ANGLE_TRY(processTask(&task));
         }
 
+#if 0
         if (mNeedCommandsAndGarbageCleanup.exchange(false))
         {
             // Always check completed commands again in case anything new has been finished.
@@ -689,6 +700,7 @@ angle::Result CommandProcessor::processTasksImpl(bool *exitThread)
             }
             mRenderer->cleanupGarbage();
         }
+#endif
     }
     *exitThread = true;
     return angle::Result::Continue;

```

### sy...@chromium.org (2024-03-28)

(I can confirm now I can still reproduce with symbol level 2, but without the above patch)

### sy...@chromium.org (2024-04-11)

A few more things to try since you can reproduce more easily:

- Can you reproduce with `--disable-gpu-compositing`?
- Can you reproduce by using variables for width/height instead of canvas.width and canvas.height? I see a lot of resource recreation because of the canvas size change, and that's producing a lot of noise while debugging.
- If the canvas size change is necessary for repro, what happens if you make the canvas NOT multisampled?

### em...@gmail.com (2024-04-11)

Here are my test results:
q1:
-   repro
q2:
-   no repro
q3:
-   no repro
I have uploaded my modified test code (regarding the second and third questions).

### sy...@chromium.org (2024-04-12)

Thank you, it looks like the recreation of canvas is playing a role here.

W.r.t q2, the changed html is not what I had in mind though. In the original repro (also in `crash-q3-no-repro.html`) there's this code:

```
        gl.canvas.width += 1;
        gl.canvas.height += 1;

```

In `crash-q2-no-repro.html`, could you please add this on the same spot (that's done only in `setupStencilFramebuffer`) and see what happens?

```
        canvasWidth += 1;
        canvasHeight += 1;

```

The reason I'm interested is because this changes the allocation sizes of the stencil images, so while with `crash-q2-no-repro.html` we may be reusing the same VMA buffers and suballocating from them perfectly (because new images fit in the same place of the old images), changing the image size will dramatically change the memory allocation patterns.

### em...@gmail.com (2024-04-12)

I'm sorry for causing you any inconvenience. I realized there were mistakes in my previous code modifications, so I've revised them. I found that the issue can still repro without these two lines of code, but the reproducibility is somewhat less stable. For example:
canvasWidth += 1;
canvasHeight += 1;
or
gl.canvas.width += 1;
gl.canvas.height += 1;

### sy...@chromium.org (2024-04-13)

Thank you for confirming that! It's likely harder to reproduce because a lot of reallocation coming from canvas is no longer being done. But this does confirm further that the piece of code in ANGLE that does depth/stencil resolve is somehow not ensuring the objects are held on to long enough.

### sy...@chromium.org (2024-05-02)

Hi again. I believe you missed it, could you please try the patch in [#comment56](https://issues.chromium.org/issues/40942995#comment56) and see if the issue is still reproducible? Feel free to try with the repro case that's easier to reproduce (to avoid false negatives). That change makes garbage cleanup synchronous, which should hopefully make the issue *easier* to reproduce, but could also be a hint if the issue goes away.

### em...@gmail.com (2024-05-02)

Sorry, I missed #56. I just tested it, and the issue can still be reproduced  after applying the patch.Attached is the ASAN log.

### ti...@chromium.org (2024-05-20)

[Secondary Security Shepherd]

syoussefi@ is there a crbug representing the removal of Swiftshader? (Or at least, its relegation to non-default configurations).

We should probably also try to fix these before that happens, but perhaps we should mark them as blocked on that bug as well?

### sy...@chromium.org (2024-05-20)

Done. I do wish I could fix this, but I can't for the life of me get the repro reliable enough to let me debug it. Code inspection didn't show anything that could lead to this.

### da...@chromium.org (2024-06-13)

How can we make progress here? We're continuing to ship this UAF that is web-reachable until we can close it.

### sy...@chromium.org (2024-06-13)

@reporter, if you disable ANGLE's use of VK\_EXT\_shader\_stencil\_export, are you still able to reproduce this? To do that, either apply this diff to code:

```
     ANGLE_FEATURE_CONDITION(
         &mFeatures, supportsShaderStencilExport,
+        false);
-        ExtensionFound(VK_EXT_SHADER_STENCIL_EXPORT_EXTENSION_NAME, deviceExtensionNames));

```

Or override the feature at runtime by setting this env var: `ANGLE_FEATURE_OVERRIDES_DISABLED=supportsShaderStencilExport`. Please verify in either case in `chrome://gpu` that this feature is disabled. Per [Comment#55](https://issues.chromium.org/issues/40942995#comment55), I could briefly reproduce the issue and disabling that extension made it go away, but I can't be sure it wasn't just a case of the issue not being reproducible anymore.

Without that feature, we use a fallback path that blits stencil less efficiently. If that makes the security issue go away, at this point I'm willing to do that given there doesn't seem to be any hope of figuring out what the actual issue is.

### em...@gmail.com (2024-06-13)

I have tested both methods multiple times and confirmed that the issue no longer reproduces. After setting the env, I also verified the GPU information:
chrome://gpu/
```
*   supportsShaderStencilExport (Vulkan features): Disabled
    condition: false (override)
    VkDevice supports the VK_EXT_shader_stencil_export extension
```

tested versions:
Chromium 127.0.6526.0
Chromium 127.0.6510.4

### ap...@google.com (2024-06-14)

Project: angle/angle
Branch: main

commit 165b85b69226a347014dd2c6d1c0a0682a874efe
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Thu Jun 13 16:54:03 2024

    Vulkan: Disable VK_EXT_shader_stencil_export on SwiftShader
    
    Bug: chromium:40942995
    Change-Id: I4c469108c420d3e68008a30f627989655a64c27c
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5630161
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
    Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

M       src/libANGLE/renderer/vulkan/vk_renderer.cpp

https://chromium-review.googlesource.com/5630161


### sy...@chromium.org (2024-06-14)

Thank you for verifying this. I hate that the original issue is not fixed, but this is at least less of a priority.

### ap...@google.com (2024-06-14)

Project: chromium/src
Branch: main

commit 5e049e101e8b201d843b39bc522adfe63c96dfc5
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Fri Jun 14 04:03:38 2024

    Roll ANGLE from 06f1b72f55f8 to 165b85b69226 (2 revisions)
    
    https://chromium.googlesource.com/angle/angle.git/+log/06f1b72f55f8..165b85b69226
    
    2024-06-14 syoussefi@chromium.org Vulkan: Disable VK_EXT_shader_stencil_export on SwiftShader
    2024-06-14 m.maiya@samsung.com Vulkan: Optimize ProgramExecutableVk::resetLayout
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/angle-chromium-autoroll
    Please CC angle-team@google.com,geofflang@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
    Bug: chromium:40942995
    Tbr: geofflang@google.com
    Change-Id: Iee28a94858e49c2658258015ed5de95bd98b7fad
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5632976
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1315029}

M       DEPS
M       third_party/angle

https://chromium-review.googlesource.com/5632976


### pe...@google.com (2024-06-14)

Requesting merge to stable (M126) because latest trunk commit (1315029) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1315029) appears to be after beta branch point (1313161).
Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2024-06-17)

merges approved for this fix disabling vk\_ext\_shader\_stencil\_export (<https://chromium-review.googlesource.com/c/angle/angle/+/5630161>) to M127 Beta and M126 Stable; please merge this fix to M127 / branch 6533 by EOD tomorrow, 18 June so this fix can be included in the next beta update

please merge this fix to M126 / branch 6478 so this fix can be included in the next M126 Stable update by EOD Thursday, 20 June so this fix can be included in the next week's M126 Stable update -- thank you.

### ap...@google.com (2024-06-18)

Project: angle/angle
Branch: chromium/6533

commit 108a8f8065c4d9a47be5e12ddae3467136bc7fe2
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Thu Jun 13 16:54:03 2024

    M127: Vulkan: Disable VK_EXT_shader_stencil_export on SwiftShader
    
    Bug: chromium:40942995
    Change-Id: I12dcd58157c7f149226c0d66cdb348af2375ac03
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5639353
    Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

M       src/libANGLE/renderer/vulkan/vk_renderer.cpp

https://chromium-review.googlesource.com/5639353


### ap...@google.com (2024-06-18)

Project: angle/angle
Branch: chromium/6478

commit 5d4df51d1d7d6a290d54111527a4798f10c7ca3c
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Thu Jun 13 16:54:03 2024

    M126: Vulkan: Disable VK_EXT_shader_stencil_export on SwiftShader
    
    Bug: chromium:40942995
    Change-Id: I5035d9b11997a1c7c839d7d62544fecca9fd1f73
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5634418
    Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

M       src/libANGLE/renderer/vulkan/vk_renderer.cpp

https://chromium-review.googlesource.com/5634418


### pe...@google.com (2024-06-18)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2024-06-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
mildly mitigated (very racy) memory corruption in the GPU process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-21)

Congratulations Cassidy Kim! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-07-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-07-02)

1.<https://crrev.com/c/5644917>
2. Low, no conflicts
3. 126
4. Yes

### ap...@google.com (2024-07-11)

Project: angle/angle
Branch: chromium/6099

commit 10e29b15ac16ff26a591899eb848f58a8df5f9f0
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Thu Jun 13 16:54:03 2024

    [M120-LTS] Vulkan: Disable VK_EXT_shader_stencil_export on SwiftShader
    
    Bug: chromium:40942995
    Change-Id: I4c469108c420d3e68008a30f627989655a64c27c
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5630161
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
    (cherry picked from commit 165b85b69226a347014dd2c6d1c0a0682a874efe)
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5644917
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
    Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
    Auto-Submit: Roger Felipe Zanoni da Silva <rzanoni@google.com>

M       src/libANGLE/renderer/vulkan/RendererVk.cpp

https://chromium-review.googlesource.com/5644917


### pe...@google.com (2024-09-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40942995)*
