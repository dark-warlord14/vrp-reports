# Security: use after free in GraphicsPipeline::containsImageWrite

| Field | Value |
|-------|-------|
| **Issue ID** | [40060000](https://issues.chromium.org/issues/40060000) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | em...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-06-18 |
| **Bounty** | $7,000.00 |

## Description

**VERSION** :  

Chrome Version: Chromium 104.0.5098.0(dev), 104.0.5083.0 (Official Build) dev (64-bit)  

Operating System: Ubuntu 20.04

./chrome --user-data-dir=/tmp/x1 <http://localhost:8001/crash.html>  

Wait a few seconds and it will repro immediately.  

Type of crash: [gpu]

=================================================================  

==2485541==ERROR: AddressSanitizer: heap-use-after-free on address 0x61e0000570b0 at pc 0x7fc6deac0b54 bp 0x7fc6cabf1270 sp 0x7fc6cabf1268  

READ of size 8 at 0x61e0000570b0 thread T18  

#0 0x7fc6deac0b53 in get ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/shared\_ptr.h:802:16  

#1 0x7fc6deac0b53 in vk::GraphicsPipeline::containsImageWrite() const ./../../third\_party/swiftshader/src/Vulkan/VkPipeline.cpp:299:23  

#2 0x7fc6deb9b9e7 in sw::Renderer::draw(vk::GraphicsPipeline const\*, vk::DynamicState const&, unsigned int, int, sw::CountedEvent\*, int, int, void\*, VkRect2D const&, vk::Pipeline::PushConstantStorage const&, bool) ./../../third\_party/swiftshader/src/Device/Renderer.cpp:222:39  

#3 0x7fc6dea80922 in (anonymous namespace)::CmdDrawBase::draw(vk::CommandBuffer::ExecutionState&, bool, unsigned int, unsigned int, unsigned int, int, unsigned int) ./../../third\_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:933:31  

#4 0x7fc6dea8034c in (anonymous namespace)::CmdDraw::execute(vk::CommandBuffer::ExecutionState&) ./../../third\_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:957:3  

#5 0x7fc6dea79b31 in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) ./../../third\_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:2344:12  

#6 0x7fc6deace6ef in vk::Queue::submitQueue(vk::Queue::Task const&) ./../../third\_party/swiftshader/src/Vulkan/VkQueue.cpp:104:42  

#7 0x7fc6deacd650 in vk::Queue::taskLoop(marl::Scheduler\*) ./../../third\_party/swiftshader/src/Vulkan/VkQueue.cpp:156:4  

#8 0x7fc6dead02b3 in \_\_invoke<void (vk::Queue::\*)(marl::Scheduler \*), vk::Queue \*, marl::Scheduler \*, void> ./../../buildtools/third\_party/libc++/trunk/include/type\_traits:3509:23  

#9 0x7fc6dead02b3 in \_\_thread\_execute<std::Cr::unique\_ptr<std::Cr::\_\_thread\_struct, std::Cr::default\_delete[std::Cr::\_\_thread\_struct](javascript:void(0);) >, void (vk::Queue::\*)(marl::Scheduler \*), vk::Queue \*, marl::Scheduler \*, 2UL, 3UL> ./../../buildtools/third\_party/libc++/trunk/include/thread:276:5  

#10 0x7fc6dead02b3 in void\* std::Cr::\_\_thread\_proxy<std::Cr::tuple<std::Cr::unique\_ptr<std::Cr::\_\_thread\_struct, std::Cr::default\_delete[std::Cr::\_\_thread\_struct](javascript:void(0);) >, void (vk::Queue::\*)(marl::Scheduler\*), vk::Queue\*, marl::Scheduler\*> >(void\*) ./../../buildtools/third\_party/libc++/trunk/include/thread:287:5  

#11 0x7fc6e94e7608 in start\_thread /build/glibc-SzIz7B/glibc-2.31/nptl/pthread\_create.c:477:8

0x61e0000570b0 is located 48 bytes inside of 2600-byte region [0x61e000057080,0x61e000057aa8)  

freed by thread T0 (chrome) here:  

#0 0x5584ec2526c2 in free *asan\_rtl*:3  

#1 0x7fc6e13c2143 in rx::vk::GarbageObject::destroy(rx::RendererVk\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_utils.cpp:0:0  

#2 0x7fc6e116796a in rx::vk::CommandQueue::retireFinishedCommands(rx::vk::Context\*, unsigned long) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/CommandProcessor.cpp:970:25  

#3 0x7fc6e115feb5 in rx::vk::CommandQueue::checkCompletedCommands(rx::vk::Context\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/CommandProcessor.cpp:928:12  

#4 0x7fc6e115ee75 in rx::vk::CommandQueue::submitFrame(rx::vk::Context\*, bool, egl::ContextPriority, std::Cr::vector<VkSemaphore\_T\*, std::Cr::allocator<VkSemaphore\_T\*> > const&, std::Cr::vector<unsigned int, std::Cr::allocator<unsigned int> > const&, rx::vk::Semaphore const\*, std::Cr::vector<rx::vk::GarbageObject, std::Cr::allocator[rx::vk::GarbageObject](javascript:void(0);) >&&, rx::vk::SecondaryCommandBufferList&&, rx::vk::SecondaryCommandPools\*, rx::Serial) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/CommandProcessor.cpp:1172:5  

#5 0x7fc6e1247246 in rx::RendererVk::submitFrame(rx::vk::Context\*, bool, egl::ContextPriority, std::Cr::vector<VkSemaphore\_T\*, std::Cr::allocator<VkSemaphore\_T\*> >&&, std::Cr::vector<unsigned int, std::Cr::allocator<unsigned int> >&&, rx::vk::Semaphore const\*, std::Cr::vector<rx::vk::GarbageObject, std::Cr::allocator[rx::vk::GarbageObject](javascript:void(0);) >&&, rx::vk::SecondaryCommandPools\*, rx::Serial\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:4160:9  

#6 0x7fc6e11a1b1a in rx::ContextVk::submitCommands(rx::vk::Semaphore const\*, rx::Serial\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:3062:5  

#7 0x7fc6e11a1908 in rx::ContextVk::submitFrame(rx::vk::Semaphore const\*, rx::Serial\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:3026:5  

#8 0x7fc6e11c0dd3 in rx::ContextVk::flushAndGetSerial(rx::vk::Semaphore const\*, rx::Serial\*, rx::RenderPassClosureReason) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:6622:5  

#9 0x7fc6e11b8d50 in flushImpl ./../../third\_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:6551:12  

#10 0x7fc6e11b8d50 in rx::ContextVk::onUnMakeCurrent(gl::Context const\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:5215:5  

#11 0x7fc6e0b11fae in gl::Context::unMakeCurrent(egl::Display const\*) ./../../third\_party/angle/src/libANGLE/Context.cpp:898:5  

#12 0x7fc6e0baafe2 in egl::Display::makeCurrent(egl::Thread\*, gl::Context\*, egl::Surface\*, egl::Surface\*, gl::Context\*) ./../../third\_party/angle/src/libANGLE/Display.cpp:1539:39  

#13 0x7fc6e0a6a066 in egl::MakeCurrent(egl::Thread\*, egl::Display\*, egl::Surface\*, egl::Surface\*, gl::Context\*) ./../../third\_party/angle/src/libGLESv2/egl\_stubs.cpp:486:9  

#14 0x7fc6e0a7170c in EGL\_MakeCurrent ./../../third\_party/angle/src/libGLESv2/entry\_points\_egl\_autogen.cpp:356:12  

#15 0x7fc6e012a78f in eglMakeCurrent ./../../third\_party/angle/src/libEGL/libEGL\_autogen.cpp:186:12  

#16 0x5584ffe00c4c in gl::GLContextEGL::MakeCurrentImpl(gl::GLSurface\*) ./../../ui/gl/gl\_context\_egl.cc:484:8  

#17 0x5584ffd3b521 in gl::GLContext::MakeCurrent(gl::GLSurface\*) ./../../ui/gl/gl\_context.cc:112:10  

#18 0x558502284cfd in gpu::SharedContextState::MakeCurrent(gl::GLSurface\*, bool) ./../../gpu/command\_buffer/service/shared\_context\_state.cc:565:20  

#19 0x5585026ba72f in gpu::SharedImageStub::MakeContextCurrent(bool) ./../../gpu/ipc/service/shared\_image\_stub.cc:481:26  

#20 0x5585026bd71c in gpu::SharedImageStub::OnDestroySharedImage(gpu::Mailbox const&) ./../../gpu/ipc/service/shared\_image\_stub.cc:312:8  

#21 0x5585026bb3d2 in gpu::SharedImageStub::ExecuteDeferredRequest(mojo::StructPtr[gpu::mojom::DeferredSharedImageRequest](javascript:void(0);)) ./../../gpu/ipc/service/shared\_image\_stub.cc:107:7  

#22 0x55850261539b in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)) ./../../gpu/ipc/service/gpu\_channel.cc:723:27  

#23 0x5585026222a2 in void base::internal::FunctorTraits<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), void>::Invoke<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >(void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);)&&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&) ./../../base/bind\_internal.h:541:12  

#24 0x558500d13343 in Run ./../../base/callback.h:143:12  

#25 0x558500d13343 in gpu::Scheduler::RunNextTask() ./../../gpu/command\_buffer/service/scheduler.cc:698:26  

#26 0x5584fbde106f in Run ./../../base/callback.h:143:12  

#27 0x5584fbde106f in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#28 0x5584fbe266af in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:424:29)> ./../../base/task/common/task\_annotator.h:74:5  

#29 0x5584fbe266af in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:422:21  

#30 0x5584fbe25a7e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:300:41  

#31 0x5584fbe274e7 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#32 0x5584fbcbb0e5 in HandleDispatch ./../../base/message\_loop/message\_pump\_glib.cc:375:46  

#33 0x5584fbcbb0e5 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:126:43  

#34 0x7fc6e939117c in g\_main\_context\_dispatch ??:0:0

previously allocated by thread T0 (chrome) here:  

#0 0x5584ec25296e in malloc *asan\_rtl*:3  

#1 0x7fc6dedf33b5 in allocate ./../../third\_party/swiftshader/src/System/Memory.cpp:81:42  

#2 0x7fc6dedf33b5 in sw::allocateZeroOrPoison(unsigned long, unsigned long) ./../../third\_party/swiftshader/src/System/Memory.cpp:115:9  

#3 0x7fc6deaeefa5 in Create<vk::GraphicsPipeline, VkNonDispatchableHandle<VkPipeline\_T \*>, VkGraphicsPipelineCreateInfo, vk::Device \*> ./../../third\_party/swiftshader/src/Vulkan/VkObject.hpp:58:23  

#4 0x7fc6deaeefa5 in VkResult vk::ObjectBase<vk::GraphicsPipeline, VkNonDispatchableHandle<VkPipeline\_T\*> >::Create<VkGraphicsPipelineCreateInfo, vk::Device\*>(VkAllocationCallbacks const\*, VkGraphicsPipelineCreateInfo const\*, VkNonDispatchableHandle<VkPipeline\_T\*>\*, vk::Device\*) ./../../third\_party/swiftshader/src/Vulkan/VkObject.hpp:92:10  

#5 0x7fc6deaeedae in vkCreateGraphicsPipelines ./../../third\_party/swiftshader/src/Vulkan/libVulkan.cpp:2138:21  

#6 0x7fc6e12e3164 in initGraphics ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_wrapper.h:1772:12  

#7 0x7fc6e12e3164 in rx::vk::GraphicsPipelineDesc::initializePipeline(rx::ContextVk\*, rx::vk::PipelineCache const&, rx::vk::RenderPass const&, rx::vk::PipelineLayout const&, angle::BitSetT<16ul, unsigned long, unsigned long> const&, angle::BitSetT<32ul, unsigned long, unsigned long> const&, angle::BitSetT<8ul, unsigned char, unsigned long> const&, angle::PackedEnumMap<gl::ShaderType, rx::vk::BindingPointer<rx::vk::ObjectAndSerial[rx::vk::ShaderModule](javascript:void(0);) >, 6ul> const&, rx::vk::SpecializationConstants const&, rx::vk::Pipeline\*) const ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_cache\_utils.cpp:2372:5  

#8 0x7fc6e12fdc26 in rx::GraphicsPipelineCache::insertPipeline(rx::ContextVk\*, rx::vk::PipelineCache const&, rx::vk::RenderPass const&, rx::vk::PipelineLayout const&, angle::BitSetT<16ul, unsigned long, unsigned long> const&, angle::BitSetT<32ul, unsigned long, unsigned long> const&, angle::BitSetT<8ul, unsigned char, unsigned long> const&, angle::PackedEnumMap<gl::ShaderType, rx::vk::BindingPointer<rx::vk::ObjectAndSerial[rx::vk::ShaderModule](javascript:void(0);) >, 6ul> const&, rx::vk::SpecializationConstants const&, rx::vk::GraphicsPipelineDesc const&, rx::vk::GraphicsPipelineDesc const\*\*, rx::vk::PipelineHelper\*\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_cache\_utils.cpp:4641:9  

#9 0x7fc6e1209e53 in getPipeline ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_cache\_utils.h:1782:16  

#10 0x7fc6e1209e53 in getGraphicsPipeline ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_helpers.h:2890:35  

#11 0x7fc6e1209e53 in rx::ProgramExecutableVk::getGraphicsPipeline(rx::ContextVk\*, gl::PrimitiveMode, rx::vk::GraphicsPipelineDesc const&, gl::ProgramExecutable const&, rx::vk::GraphicsPipelineDesc const\*\*, rx::vk::PipelineHelper\*\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/ProgramExecutableVk.cpp:793:27  

#12 0x7fc6e1182eda in rx::ContextVk::handleDirtyGraphicsPipelineDesc(angle::BitSetT<40ul, unsigned long, unsigned long>::Iterator\*, angle::BitSetT<40ul, unsigned long, unsigned long>) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:1816:9  

#13 0x7fc6e119931e in rx::ContextVk::setupDraw(gl::Context const\*, gl::PrimitiveMode, int, int, int, gl::DrawElementsType, void const\*, angle::BitSetT<40ul, unsigned long, unsigned long>) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:1327:9  

#14 0x7fc6e11a4502 in rx::ContextVk::drawArrays(gl::Context const\*, gl::PrimitiveMode, int, int) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:3449:9  

#15 0x7fc6e0a890bc in drawArrays ./../../third\_party/angle/src/libANGLE/Context.inl.h:133:5  

#16 0x7fc6e0a890bc in GL\_DrawArrays ./../../third\_party/angle/src/libGLESv2/entry\_points\_gles\_2\_0\_autogen.cpp:1109:22  

#17 0x55850217ba75 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(unsigned int, int, int) ./../../gpu/command\_buffer/service/gles2\_cmd\_decoder\_passthrough\_doers.cc:1218:10  

#18 0x558502147bc9 in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile\*, int, int\*) ./../../gpu/command\_buffer/service/gles2\_cmd\_decoder\_passthrough.cc:869:20  

#19 0x55850260deb4 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface\*) ./../../gpu/command\_buffer/service/command\_buffer\_service.cc:193:18  

#20 0x5585026011a8 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::Cr::vector<gpu::SyncToken, std::Cr::allocator[gpu::SyncToken](javascript:void(0);) > const&) ./../../gpu/ipc/service/command\_buffer\_stub.cc:505:22  

#21 0x558502600655 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command\_buffer\_stub.cc:152:7  

#22 0x558502615476 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)) ./../../gpu/ipc/service/gpu\_channel.cc:708:13  

#23 0x5585026222a2 in void base::internal::FunctorTraits<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), void>::Invoke<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >(void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);)&&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&) ./../../base/bind\_internal.h:541:12  

#24 0x558500d13343 in Run ./../../base/callback.h:143:12  

#25 0x558500d13343 in gpu::Scheduler::RunNextTask() ./../../gpu/command\_buffer/service/scheduler.cc:698:26  

#26 0x5584fbde106f in Run ./../../base/callback.h:143:12  

#27 0x5584fbde106f in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#28 0x5584fbe266af in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:424:29)> ./../../base/task/common/task\_annotator.h:74:5  

#29 0x5584fbe266af in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:422:21  

#30 0x5584fbe25a7e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:300:41  

#31 0x5584fbe274e7 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#32 0x5584fbcbb0e5 in HandleDispatch ./../../base/message\_loop/message\_pump\_glib.cc:375:46  

#33 0x5584fbcbb0e5 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:126:43  

#34 0x7fc6e939117c in g\_main\_context\_dispatch ??:0:0

Thread T18 created by T0 (chrome) here:  

#0 0x5584ec23b97c in pthread\_create *asan\_rtl*:3  

#1 0x7fc6deacd93d in \_\_libcpp\_thread\_create ./../../buildtools/third\_party/libc++/trunk/include/\_\_threading\_support:376:10  

#2 0x7fc6deacd93d in std::Cr::thread::thread<void (vk::Queue::\*)(marl::Scheduler\*), vk::Queue\*, marl::Scheduler\*&, void>(void (vk::Queue::\*&&)(marl::Scheduler\*), vk::Queue\*&&, marl::Scheduler\*&) ./../../buildtools/third\_party/libc++/trunk/include/thread:303:16  

#3 0x7fc6deacd3a1 in vk::Queue::Queue(vk::Device\*, marl::Scheduler\*) ./../../third\_party/swiftshader/src/Vulkan/VkQueue.cpp:38:16  

#4 0x7fc6dea8bb47 in vk::Device::Device(VkDeviceCreateInfo const\*, void\*, vk::PhysicalDevice\*, VkPhysicalDeviceFeatures const\*, std::Cr::shared\_ptr[marl::Scheduler](javascript:void(0);) const&) ./../../third\_party/swiftshader/src/Vulkan/VkDevice.cpp:138:26  

#5 0x7fc6deae7d20 in DispatchableObject<const VkDeviceCreateInfo \*, void \*, vk::PhysicalDevice \*, const VkPhysicalDeviceFeatures \*, std::Cr::shared\_ptr[marl::Scheduler](javascript:void(0);) > ./../../third\_party/swiftshader/src/Vulkan/VkObject.hpp:127:8  

#6 0x7fc6deae7d20 in Create<vk::DispatchableObject<vk::Device, VkDevice\_T \*>, VkDevice\_T \*, VkDeviceCreateInfo, vk::PhysicalDevice \*, const VkPhysicalDeviceFeatures \*, std::Cr::shared\_ptr[marl::Scheduler](javascript:void(0);) > ./../../third\_party/swiftshader/src/Vulkan/VkObject.hpp:65:34  

#7 0x7fc6deae7d20 in VkResult vk::DispatchableObject<vk::Device, VkDevice\_T\*>::Create<VkDeviceCreateInfo, vk::PhysicalDevice\*, VkPhysicalDeviceFeatures const\*, std::Cr::shared\_ptr[marl::Scheduler](javascript:void(0);) >(VkAllocationCallbacks const\*, VkDeviceCreateInfo const\*, VkDevice\_T\*\*, vk::PhysicalDevice\*, VkPhysicalDeviceFeatures const\*, std::Cr::shared\_ptr[marl::Scheduler](javascript:void(0);)) ./../../third\_party/swiftshader/src/Vulkan/VkObject.hpp:147:10  

#8 0x7fc6deae776c in vkCreateDevice ./../../third\_party/swiftshader/src/Vulkan/libVulkan.cpp:1089:9  

#9 0x7fc6dfeeaf25 in terminator\_CreateDevice ./../../third\_party/vulkan-deps/vulkan-loader/src/loader/loader.c:5637:11  

#10 0x7fc6dfee4dd0 in loader\_create\_device\_chain ./../../third\_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4864:15  

#11 0x7fc6dfee3499 in loader\_layer\_create\_device ./../../third\_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4300:11  

#12 0x7fc6dfef9f43 in vkCreateDevice ./../../third\_party/vulkan-deps/vulkan-loader/src/loader/trampoline.c:848:20  

#13 0x7fc6e1232585 in rx::RendererVk::initializeDevice(rx::DisplayVk\*, unsigned int) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:2602:5  

#14 0x7fc6e122a7aa in rx::RendererVk::initialize(rx::DisplayVk\*, egl::Display\*, char const\*, char const\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:1678:9  

#15 0x7fc6e11d6a03 in rx::DisplayVk::initialize(egl::Display\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/DisplayVk.cpp:49:39  

#16 0x7fc6e13cd3a4 in rx::DisplayVkXcb::initialize(egl::Display\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/linux/xcb/DisplayVkXcb.cpp:65:23  

#17 0x7fc6e0b9f150 in egl::Display::initialize() ./../../third\_party/angle/src/libANGLE/Display.cpp:988:36  

#18 0x7fc6e0a69c55 in egl::Initialize(egl::Thread\*, egl::Display\*, int\*, int\*) ./../../third\_party/angle/src/libGLESv2/egl\_stubs.cpp:453:5  

#19 0x7fc6e0a714d0 in EGL\_Initialize ./../../third\_party/angle/src/libGLESv2/entry\_points\_egl\_autogen.cpp:330:12  

#20 0x7fc6e012a4c8 in eglInitialize ./../../third\_party/angle/src/libEGL/libEGL\_autogen.cpp:177:12  

#21 0x5584ffe0e0b5 in gl::GLSurfaceEGL::InitializeDisplay(gl::EGLDisplayPlatform, unsigned long) ./../../ui/gl/gl\_surface\_egl.cc:1341:10  

#22 0x5584ffe0b733 in gl::GLSurfaceEGL::InitializeOneOff(gl::EGLDisplayPlatform, unsigned long) ./../../ui/gl/gl\_surface\_egl.cc:1005:27  

#23 0x5584ee80187b in ui::GLOzoneEGL::InitializeGLOneOffPlatform() ./../../ui/ozone/common/gl\_ozone\_egl.cc:19:8  

#24 0x55850007ff6d in gl::init::InitializeGLOneOffPlatformImplementation(bool, bool, bool, unsigned long) ./../../ui/gl/init/gl\_factory.cc:216:22  

#25 0x55850007fa27 in gl::init::(anonymous namespace)::InitializeGLOneOffPlatformHelper(bool, unsigned long) ./../../ui/gl/init/gl\_factory.cc:143:10  

#26 0x55850007fce2 in gl::init::InitializeGLNoExtensionsOneOff(bool, unsigned long) ./../../ui/gl/init/gl\_factory.cc:172:10  

#27 0x55850267ecf7 in gpu::GpuInit::InitializeAndStartSandbox(base::CommandLine\*, gpu::GpuPreferences const&) ./../../gpu/ipc/service/gpu\_init.cc:442:24  

#28 0x55850968aa6b in content::GpuMain(content::MainFunctionParams) ./../../content/gpu/gpu\_main.cc:325:39  

#29 0x5584faa8298d in content::RunOtherNamedProcessTypeMain(std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:705:14  

#30 0x5584faa84b15 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1045:10  

#31 0x5584faa7e23e in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:407:36  

#32 0x5584faa7e968 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:435:10  

#33 0x5584ec286311 in ChromeMain ./../../chrome/app/chrome\_main.cc:177:12  

#34 0x7fc6e7e3f082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwn11/chrome/chrome/././libvk\_swiftshader.so+0x437b53) (BuildId: 85ba1a80fea1338c)  

Shadow bytes around the buggy address:  

0x0c3c80002dc0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3c80002dd0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3c80002de0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3c80002df0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3c80002e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c3c80002e10: fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd  

0x0c3c80002e20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3c80002e30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3c80002e40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3c80002e50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3c80002e60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==2485541==ABORTING  

Received signal 6  

#0 0x5584ec20b8eb in backtrace /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_common\_interceptors.inc:4379:13  

#1 0x5584fbedb124 in base::debug::CollectStackTrace(void\*\*, unsigned long) ./../../base/debug/stack\_trace\_posix.cc:874:39  

#2 0x5584fbc57732 in StackTrace ./../../base/debug/stack\_trace.cc:221:12  

#3 0x5584fbc57732 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack\_trace.cc:218:28  

#4 0x5584fbed99bc in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo\_t\*, void\*) ./../../base/debug/stack\_trace\_posix.cc:371:3  

#5 0x7fc6e94f3420 in \_\_funlockfile :?  

#6 0x7fc6e7e5e00b in \_\_libc\_signal\_restore\_set /build/glibc-SzIz7B/glibc-2.31/signal/../sysdeps/unix/sysv/linux/internal-signals.h:86:3  

#7 0x7fc6e7e5e00b in raise /build/glibc-SzIz7B/glibc-2.31/signal/../sysdeps/unix/sysv/linux/raise.c:48:3  

#8 0x7fc6e7e3d859 in abort /build/glibc-SzIz7B/glibc-2.31/stdlib/abort.c:79:7  

#9 0x5584ec26f8a7 in \_\_sanitizer::Abort() /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/sanitizer\_common/sanitizer\_posix\_libcdep.cpp:143:3  

#10 0x5584ec26e191 in \_\_sanitizer::Die() /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/sanitizer\_common/sanitizer\_termination.cpp:58:5  

#11 0x5584ec256de7 in \_\_asan::ScopedInErrorReport::~ScopedInErrorReport() *asan\_rtl*:7  

#12 0x5584ec259a4c in \_\_asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) *asan\_rtl*:1  

#13 0x5584ec25a6c8 in \_\_asan\_report\_load8 *asan\_rtl*:1  

#12 0x7fc6deac0b54 <unknown>  

#13 0x7fc6deb9b9e8 <unknown>  

#14 0x7fc6dea80923 <unknown>  

#15 0x7fc6dea8034d <unknown>  

#16 0x7fc6dea79b32 <unknown>  

#17 0x7fc6deace6f0 <unknown>  

#18 0x7fc6deacd651 <unknown>  

#19 0x7fc6dead02b4 <unknown>  

#14 0x7fc6e94e7609 in start\_thread /build/glibc-SzIz7B/glibc-2.31/nptl/pthread\_create.c:477:8  

#15 0x7fc6e7f3a133 in \_\_clone /build/glibc-SzIz7B/glibc-2.31/misc/../sysdeps/unix/sysv/linux/x86\_64/clone.S:95:0  

r8: 0000000000000000 r9: 00007fc6cabf0280 r10: 0000000000000008 r11: 0000000000000246  

r12: 10000000000fffff r13: 0fffff0000000000 r14: 1000000000000000 r15: 2000000000000000  

di: 0000000000000002 si: 00007fc6cabf0280 bp: 6000000000000000 bx: 00007fc6cabf2700  

dx: 0000000000000000 ax: 0000000000000000 cx: 00007fc6e7e5e00b sp: 00007fc6cabf0280  

ip: 00007fc6e7e5e00b efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000  

trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000  

[end of stack trace]  

[2485408:2485408:0614/183052.019145:ERROR:command\_buffer\_proxy\_impl.cc(331)] GPU state invalid after WaitForGetOffsetInRange.  

[2485266:2485266:0614/183052.019268:ERROR:gpu\_process\_host.cc(966)] GPU process exited unexpectedly: exit\_code=134  

libva error: vaGetDriverNameByIndex() failed with unknown libva error, driver\_name = (null)

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 4.8 KB)
- [1.webm](attachments/1.webm) (video/webm, 1.6 KB)
- [asan.log](attachments/asan.log) (text/plain, 27.6 KB)
- [asan.log](attachments/asan.log) (text/plain, 27.2 KB)

## Timeline

### [Deleted User] (2022-06-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5770170874396672.

### cl...@chromium.org (2022-06-20)

ClusterFuzz testcase 5770170874396672 is closed as invalid, so closing issue.

### em...@gmail.com (2022-06-20)

What is the reason for being closed?

### xi...@chromium.org (2022-06-21)

Sorry, this was closed by mistake. I'm not able to reproduce this crash on my ASAN build. Reporter, could you try to reproduce on the latest ASAN build? Or is there any flag you enabled?

### em...@gmail.com (2022-06-21)

@xinghuilu
I tested with new version,stil can repro stable and easily, and does not need to enable other flag.
Tested Version:
macos
105.0.5127.0 (Dev) (arm64) 

ubuntu 20.04:
Version 105.0.5134.0 (Developer Build) (64-bit):asan-linux-release-1016087.zip

### aj...@google.com (2022-06-21)

tentatively adding labels

### aj...@google.com (2022-06-21)

Cannot repro on linux/HEAD

16042:16042:0621/185129.099244:ERROR:html_media_element.cc(4852)] SetError: {code=4, message="MEDIA_ELEMENT_ERROR: Format error"}

### cl...@chromium.org (2022-06-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5640078697365504.

### aj...@google.com (2022-06-21)

Does not repro on Windows HEAD.

### em...@gmail.com (2022-06-21)

Hi,@ajgo
Did you test manually?Manual tests are easy to repro,or you can try office version(none asan build)

### [Deleted User] (2022-06-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@gmail.com (2022-06-22)

Hi,@ajgo
I found that in my macos, need to add --disable-gpu launch flag,please try again.

### aj...@google.com (2022-06-23)

Thanks - I was able to repro on Windows head using:-

.\out\asan\chrome.exe --user-data-dir=tmp --no-sandbox --disable-gpu http://127.0.0.1:8001/crash.html

Sev=High - code execution in the gpu from web content.
FoundIn=102 (speculative)


### [Deleted User] (2022-06-23)

[Empty comment from Monorail migration]

### aj...@google.com (2022-06-23)

nicolascapens - please could you find a swiftshader person to take a look at this security bug.

[Monorail components: Internals>GPU>SwiftShader]

### aj...@google.com (2022-06-23)

[Empty comment from Monorail migration]

### ni...@google.com (2022-06-23)

Looks like ANGLE garbage collected a resource still in use by a draw command. Jamie can you have a closer look or find an owner?

### [Deleted User] (2022-06-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2022-06-27)

[Empty comment from Monorail migration]

### ia...@google.com (2022-06-28)

[Empty comment from Monorail migration]

### cc...@google.com (2022-06-28)

Yea, this looks like a missing retainResource call. The only place I am seeing we retain the graphics pipeline object is here.
https://chromium.googlesource.com/angle/angle/+/refs/heads/main/src/libANGLE/renderer/vulkan/ContextVk.cpp#1848

angle::Result ContextVk::handleDirtyGraphicsPipelineDesc(DirtyBits::Iterator *dirtyBitsIterator,
                                                         DirtyBits dirtyBitMask)
{
...
    mRenderPassCommands->retainResource(mCurrentGraphicsPipeline);
...
}

Now if you set up a program and issue a  draw call, you should reach handleDirtyGraphicsPipelineDesc() since pipeline should be dirty and we need to create a new pipeline. This new pipeline will be added to resource use list. Then if you issue  glFlush() and then make a very very expensive draw call that will take GPU a while to process . Because you are still using the same state, no pipeline dirty bit is set, and you will not retain mCurrentGraphicsPipeline with this current draw call. Now if you try to switch to a different program and delete the old program (or whatever takes that will trigger void GraphicsPipelineCache::release() call ), it should add the pipeline to garbage. Because the second draw call does not retain the pipeline, garbage code will wait for the first draw call to finish and destroy it. Now if you issue glFlush(), the second darw call is going to access the already deleted pipeline object.

That is merely a theory, so take with a grain of salt.  I think we need to either always retainResource(mCurrentGraphicsPipeline) for every submission, or when we switch out the current pipeline, we should add it to the  resource use list so that it will be tagged with the next submission.


### sy...@chromium.org (2022-06-29)

Probably both, to cover both when mCurrentGraphicsPipeline is used from the previous submission and then changed away to another one, and also when the next frame entirely uses mCurrentGraphicsPipeline without modifying it.

### [Deleted User] (2022-07-02)

jmadill: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2022-07-06)

Shabi, can you or Charlie be owner of this bug? Jamie's ooo, so the nagbot will just fill his inbox in the meantime if it isn't reassigned.

### sy...@chromium.org (2022-07-06)

Yes, I was internally trying to sort that out. Assigning to Frank to forward to one of his team members.

### do...@chromium.org (2022-07-13)

Security marshall ping: can this bug please get routed appropriately? It is approaching our SLO date for high severity issues.

### sy...@chromium.org (2022-07-13)

I'm looking into this. After a failed attempt at reproducing this in a test, I'm having doubts of retain actually being a problem. When releasing the program pipelines, we add them to the context garbage, which means that they are deleted when the next submission finishes; the pipeline cannot be in use after that because it is already deleted. In fact, it looks like we never need to retain pipelines (nor need them to be Resources to begin with).

I'm building (a recent-ish) chrome with ASAN enabled to see if this bug is still reproducible. If so, I'll see if I can resolve it with more retains (which I doubt). If that's not the problem, we'll have to look elsewhere.

### sy...@chromium.org (2022-07-13)

@ajgo, I can't reproduce this on a more recent Chromium. You said you could reproduce this on 102. Could you please share your gn args? And also check whether the issue is still reproducible on 105?

### em...@gmail.com (2022-07-13)

@syoussefi@chromium.org 
I tested with new verserion still repro.
(Version 105.0.5179.0 (Developer Build) (64-bit) gs://chromium-browser-asan/linux-release/asan-linux-release-1023737.zip) 
and I also tested with my own build.
is_asan = true
is_debug = false
enable_nacl = false
treat_warnings_as_errors = false
is_component_build=false
dcheck_always_on = false

v8_enable_verify_heap = true
use_v8_context_snapshot = false

### aj...@chromium.org (2022-07-13)

This continues to repro on HEAD - note you need both crash.html and 1.webm.

D:\chromium\src [(278eee3...)]> get-content .\out\Asan\args.gn
use_goma = true
enable_ipc_fuzzer = true
is_asan = true
is_component_build = false
is_debug = false
symbol_level = 1
v8_enable_verify_heap = true
dcheck_always_on = false


### aj...@chromium.org (2022-07-13)

cmdline for completeness - .\out\asan\chrome.exe --user-data-dir=tmp --no-sandbox --disable-gpu http://127.0.0.1:8001/crash.html

### sy...@chromium.org (2022-07-14)

Thanks, I didn't realize 1.webm was necessary. However, I still can't reproduce this (on Linux). One difference I notice is that I'm opening the page as simply `crash.html`, not through `http://127.0.0.1:8001/`, which doesn't just work. I presume I must be starting a web server for that, any instructions?

### em...@gmail.com (2022-07-14)

This issue can be reproduced locally,  you need add "--allow-file-access-from-files" flag, and drag poc file  to browser page.
I juset tested with macos,but it should stable with linux.
Chromium.app/Contents/MacOS/Chromium  --user-data-dir=/tmp/xx --allow-file-access-from-files  --disable-gpu

### sy...@chromium.org (2022-07-14)

Thanks I can reproduce now with --allow-file-access-from-files

### sy...@chromium.org (2022-07-18)

I'm convinced now this is a SwiftShader bug. A fence is being signaled earlier than SwiftShader is done with the submission. Here's a cleaned up version of the logs I've placed to detect this:

```
 - Create 0x61e0000e1090 <------------------- pipeline is created
 - Bind 0x61e0000e1090 <------------------- pipeline is bound to a draw call
... (draw calls)
Submit  <---------------- ANGLE makes a submission

=== SWS: event 0x606000130188 signaled? 0
vkQueueSubmit (27, 0x6030001c8ca8(1))   <----------------------------- 27 is the serial of the submission, 0x6030001c8ca8 is the fence. 1 == VK_NOT_READY (vkGetFenceStatus)
== SWS: submit: fence 0x6030001c8ca8 <----------- Queue::submit

=== SWS: CountedEvent add 0x606000130178 0x606000130188 <---------------- 0x606000130178 is &wg and 0x606000130188 is &ev in CountedEvent associated with fence
=== SWS: event 0x606000130188 signaled? 0 <-------------------------- event is not yet signaled
=== SWS: submit task 0x7fbf929ca020 <--------------------- Queue::submitQueue is called (I imagine this is in another thread?)
=== SWS: task 0x7fbf929ca020 submit cmd buffer <----------- Queue:submitQueue before Cast(submitInfo.pCommandBuffers[j])->submit(executionState);
 Submit done (27) <---------- ANGLE is done with submitting 27
=== SWS: task 0x7fbf929ca020 submit cmd buffer DONE <---------- Queue::submitQueue after Cast(...)
=== SWS: task 0x7fbf929ca020 submission done (signal fence) <---------- Queue::submitQueue at the bottom (*)
=== SWS: CountedEvent 0x606000130178 0x606000130188 done <--------- Fence is signaled
=== SWS: event shared 0x6120001f5340 signal

... (ANGLE continues to draw, then makes another submission. It then checks the fence of submission 27)
Submit
...
=== SWS: event 0x606000130188 signaled? 1
 - Batch 27 (0x6030001c8ca8) finished (status: 0) <------- Submission 27 is done, 0 == VK_SUCCESS (vkGetFenceStatus)
 Clean up garbage for: 27 <--------- ANGLE does clean up of resources used in submission 27 and released since
...
 -- Destroy (garbage) 0x61e0000e1090 <------------ pipeline is destroyed
 Submit done (28)
=== SWS: Draw with 0x61e0000e1090 <------------ CmdDrawBase::draw() starts to use the pipeline (**)
```

ANGLE makes use of the pipeline in submission 27, then queues the pipeline for garbage collection. In (*), SwiftShader signals the fence. A little while later ANGLE notices that the fence is signaled, and duly cleans up the garbage. In (**) SwiftShader starts apparently working on submission 27, after it has already signaled it complete.

I noticed this TODO at the end of Queue:submitQueue that may or may not be related:

```
	if(task.events)
	{
		// TODO: fix renderer signaling so that work submitted separately from (but before) a fence
		// is guaranteed complete by the time the fence signals.
		renderer->synchronize();
		task.events->done();
	}
```

### [Deleted User] (2022-07-18)

sugoi: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### su...@chromium.org (2022-08-04)

Investigated the issue with syoussefi@ and this turned out to be an ANGLE issue.
syoussefi@ will write a fix, so delegating the issue to him.

### su...@chromium.org (2022-08-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/928c5016b64d3a6cde7b5c7d135fc35cf8f86162

commit 928c5016b64d3a6cde7b5c7d135fc35cf8f86162
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Aug 04 16:28:12 2022

Vulkan: Fix garbage collection vs outside-RP-only flush

In https://chromium-review.googlesource.com/c/angle/angle/+/3379231, an
optimization was implemented such that the excessive recorded texture
uploads would get flushed early and submitted.  This caused a
use-after-free bug in the following situation:

* Draw with pipeline A
* Delete A <--- this puts A in the Context garbage list
* Upload a lot of data

At this point, the flush threshold could pass and the commands recorded
outside of the render pass up to this point would be submitted.
Associated with this submission was the current garbage, including
pipeline A.  However, the render pass that uses pipeline A is still not
submitted.

Now if after some time the render pass is still open, but the "completed
commands" are checked (another set of uploads causing another
submission, a query status check, etc), the garbage can be cleaned up.

When the render pass closes next and is submitted, the implementation
attempts to use the pipeline, which is already deleted.

In this change, outside-render-pass-only submissions no longer reference
the current garbage.  This has the side effect that the temporary
buffers used for uploading texture data won't be released early.  A
future optimization may want to separate the garbage list in ContextVk
to render pass and outside render pass garbage.

Bug: chromium:1337538
Change-Id: I4d31edc53916785d44420f4d6b4b2578ca3996e2
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3812555
Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Charlie Lao <cclao@google.com>
Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com>
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/928c5016b64d3a6cde7b5c7d135fc35cf8f86162/src/libANGLE/renderer/vulkan/ContextVk.h
[modify] https://crrev.com/928c5016b64d3a6cde7b5c7d135fc35cf8f86162/src/tests/gl_tests/VulkanPerformanceCounterTest.cpp
[modify] https://crrev.com/928c5016b64d3a6cde7b5c7d135fc35cf8f86162/src/libANGLE/renderer/vulkan/ContextVk.cpp


### gi...@appspot.gserviceaccount.com (2022-08-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/213836beb840d883aaf960c258a0f6414b311f2d

commit 213836beb840d883aaf960c258a0f6414b311f2d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Aug 06 01:11:47 2022

Roll ANGLE from 9e3e203278ee to 928c5016b64d (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/9e3e203278ee..928c5016b64d

2022-08-05 syoussefi@chromium.org Vulkan: Fix garbage collection vs outside-RP-only flush
2022-08-05 syoussefi@chromium.org Test for ARM bug with dynamic stencil write mask
2022-08-05 jmadill@chromium.org run_perf_tests: Allow passing flags to the test.

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
Bug: chromium:1337538
Tbr: jmadill@google.com
Change-Id: If0e5944fe4c4112dd6ca73062cff6fd02e33b03f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3812453
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1032206}

[modify] https://crrev.com/213836beb840d883aaf960c258a0f6414b311f2d/DEPS


### sy...@chromium.org (2022-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-06)

Requesting merge to stable M104 because latest trunk commit (1032206) appears to be after stable branch point (1012729).

Requesting merge to beta M105 because latest trunk commit (1032206) appears to be after beta branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-06)

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-06)

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

### sy...@chromium.org (2022-08-07)

1. Security fix
2. https://chromium-review.googlesource.com/c/angle/angle/+/3812555
3. Change is in Chromium since Aug 5
4. No
5. N/A
6. N/A

### am...@chromium.org (2022-08-09)

M105 merge approved, please merge this fix to branch 5195 ASAP so this fix can be included in tomorrow's M105/beta 

M104 merge approved, please merge this fix to branch 5112 at your earliest convenience so this fix can be in the next M104/stable respin -- thank you! 

### sy...@chromium.org (2022-08-09)

Done

### gi...@appspot.gserviceaccount.com (2022-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/4a65a669e11bd7bfa9d77cbf7001836379ec29b5

commit 4a65a669e11bd7bfa9d77cbf7001836379ec29b5
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Aug 04 16:28:12 2022

M104: Vulkan: Fix garbage collection vs outside-RP-only flush

In https://chromium-review.googlesource.com/c/angle/angle/+/3379231, an
optimization was implemented such that the excessive recorded texture
uploads would get flushed early and submitted.  This caused a
use-after-free bug in the following situation:

* Draw with pipeline A
* Delete A <--- this puts A in the Context garbage list
* Upload a lot of data

At this point, the flush threshold could pass and the commands recorded
outside of the render pass up to this point would be submitted.
Associated with this submission was the current garbage, including
pipeline A.  However, the render pass that uses pipeline A is still not
submitted.

Now if after some time the render pass is still open, but the "completed
commands" are checked (another set of uploads causing another
submission, a query status check, etc), the garbage can be cleaned up.

When the render pass closes next and is submitted, the implementation
attempts to use the pipeline, which is already deleted.

In this change, outside-render-pass-only submissions no longer reference
the current garbage.  This has the side effect that the temporary
buffers used for uploading texture data won't be released early.  A
future optimization may want to separate the garbage list in ContextVk
to render pass and outside render pass garbage.

Bug: chromium:1337538
Change-Id: Ibfc11f2b0d166b0c325fced725f23d6b9328ff98
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3821371
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/4a65a669e11bd7bfa9d77cbf7001836379ec29b5/src/libANGLE/renderer/vulkan/ContextVk.h
[modify] https://crrev.com/4a65a669e11bd7bfa9d77cbf7001836379ec29b5/src/tests/gl_tests/VulkanPerformanceCounterTest.cpp
[modify] https://crrev.com/4a65a669e11bd7bfa9d77cbf7001836379ec29b5/src/libANGLE/renderer/vulkan/ContextVk.cpp


### gi...@appspot.gserviceaccount.com (2022-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/a5a086d4d42bfc4e276482315a8a8546282f0de2

commit a5a086d4d42bfc4e276482315a8a8546282f0de2
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Aug 04 16:28:12 2022

M105: Vulkan: Fix garbage collection vs outside-RP-only flush

In https://chromium-review.googlesource.com/c/angle/angle/+/3379231, an
optimization was implemented such that the excessive recorded texture
uploads would get flushed early and submitted.  This caused a
use-after-free bug in the following situation:

* Draw with pipeline A
* Delete A <--- this puts A in the Context garbage list
* Upload a lot of data

At this point, the flush threshold could pass and the commands recorded
outside of the render pass up to this point would be submitted.
Associated with this submission was the current garbage, including
pipeline A.  However, the render pass that uses pipeline A is still not
submitted.

Now if after some time the render pass is still open, but the "completed
commands" are checked (another set of uploads causing another
submission, a query status check, etc), the garbage can be cleaned up.

When the render pass closes next and is submitted, the implementation
attempts to use the pipeline, which is already deleted.

In this change, outside-render-pass-only submissions no longer reference
the current garbage.  This has the side effect that the temporary
buffers used for uploading texture data won't be released early.  A
future optimization may want to separate the garbage list in ContextVk
to render pass and outside render pass garbage.

Bug: chromium:1337538
Change-Id: I069554dd8d98d1aef5d24172b1b49fae99fc6185
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3821369
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/a5a086d4d42bfc4e276482315a8a8546282f0de2/src/libANGLE/renderer/vulkan/ContextVk.h
[modify] https://crrev.com/a5a086d4d42bfc4e276482315a8a8546282f0de2/src/tests/gl_tests/VulkanPerformanceCounterTest.cpp
[modify] https://crrev.com/a5a086d4d42bfc4e276482315a8a8546282f0de2/src/libANGLE/renderer/vulkan/ContextVk.cpp


### am...@google.com (2022-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-11)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and nice work! 

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/9a25828113d57cf95b0c9f583e904af151a2edde

commit 9a25828113d57cf95b0c9f583e904af151a2edde
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Wed Aug 17 21:47:22 2022

Fix submit-count perf counter test on ARM

On ARM, the preferSubmitAtFBOBoundary feature causes extra submissions
that need to be taken into account.

Bug: chromium:1337538
Change-Id: Id545ee3e65fc943aff51ea3721e9c19bc0afd4a5
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3835168
Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Yuxin Hu <yuxinhu@google.com>
Commit-Queue: Yuxin Hu <yuxinhu@google.com>

[modify] https://crrev.com/9a25828113d57cf95b0c9f583e904af151a2edde/src/tests/gl_tests/VulkanPerformanceCounterTest.cpp


### gi...@appspot.gserviceaccount.com (2022-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/78e0072dec108b74762c87e10cf232287c7f6548

commit 78e0072dec108b74762c87e10cf232287c7f6548
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Aug 19 22:48:39 2022

Roll ANGLE from 4330a827bac7 to 9a25828113d5 (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/4330a827bac7..9a25828113d5

2022-08-19 syoussefi@chromium.org Fix submit-count perf counter test on ARM

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC syoussefi@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1337538
Tbr: syoussefi@google.com
Change-Id: I8988d4062c3522119f429e35472601dd4f2be3a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3843189
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1037293}

[modify] https://crrev.com/78e0072dec108b74762c87e10cf232287c7f6548/DEPS


### gm...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-12)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-12)

gmpritchard, the bot isn't adding the questionnaire for this one, but here are the answers:

1. Just https://crrev.com/c/3891371
2. Low, there were conflicts with the introduced tests, and the author suggested to validate if the ASAN crash was fixed and forego the test. I validated locally and removed the changes in the tests. The other tests are passing locally, and the ASAN issue isn't reproducible after applying the patch.
3. 104, 105
4. Yes

### ce...@google.com (2022-09-12)

Bot didn't flag this one bc the OS list doesn't include Chrome (for ChromeOS)

### gm...@google.com (2022-09-12)

The OS doesn't include ChromeOs. 

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1337538?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1349278]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060000)*
