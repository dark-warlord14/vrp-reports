# UAF in vk::Buffer::getOffsetPointer

| Field | Value |
|-------|-------|
| **Issue ID** | [327807820](https://issues.chromium.org/issues/327807820) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2024-03-03 |
| **Bounty** | $10,000.00 |

## Description

tested os:
ubuntu 22.04
tested chrome version:
Chromium 124.0.6315.2
repro steps:
chrome --incognito --user-data-dir=/tmp/xxx http://localhost:8000/crash.html --disable-gpu

==210209==ERROR: AddressSanitizer: heap-use-after-free on address 0x50700011b748 at pc 0x7f61b285445b bp 0x7f6197280f40 sp 0x7f6197280f38
READ of size 8 at 0x50700011b748 thread T18
    #0 0x7f61b285445a in vk::Buffer::getOffsetPointer(unsigned long) const ./../../third_party/swiftshader/src/Vulkan/VkBuffer.cpp:151:37
    #1 0x7f61b29542af in vk::Inputs::bindVertexInputs(int) ./../../third_party/swiftshader/src/Device/Context.cpp:382:61
    #2 0x7f61b286230d in (anonymous namespace)::CmdDrawBase::draw(vk::CommandBuffer::ExecutionState&, bool, unsigned int, unsigned int, unsigned int, int, unsigned int) ./../../third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:976:10
    #3 0x7f61b2862121 in (anonymous namespace)::CmdDraw::execute(vk::CommandBuffer::ExecutionState&) ./../../third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:1028:3
    #4 0x7f61b285aa02 in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) ./../../third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:2383:12
    #5 0x7f61b28b4acf in vk::Queue::submitQueue(vk::Queue::Task const&) ./../../third_party/swiftshader/src/Vulkan/VkQueue.cpp:104:42
    #6 0x7f61b28b3c60 in vk::Queue::taskLoop(marl::Scheduler*) ./../../third_party/swiftshader/src/Vulkan/VkQueue.cpp:156:4
    #7 0x7f61b28b7605 in __invoke<void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *, void> ./../../third_party/libc++/src/include/__type_traits/invoke.h:312:25
    #8 0x7f61b28b7605 in __thread_execute<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct> >, void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *, 2UL, 3UL> ./../../third_party/libc++/src/include/__thread/thread.h:193:3
    #9 0x7f61b28b7605 in void* std::__Cr::__thread_proxy<std::__Cr::tuple<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct>>, void (vk::Queue::*)(marl::Scheduler*), vk::Queue*, marl::Scheduler*>>(void*) ./../../third_party/libc++/src/include/__thread/thread.h:202:3
    #10 0x560728f0c6a8 in asan_thread_start(void*) _asan_rtl_:28

0x50700011b748 is located 8 bytes inside of 80-byte region [0x50700011b740,0x50700011b790)
freed by thread T0 (chrome) here:
    #0 0x560728f0e876 in __interceptor_free _asan_rtl_:3
    #1 0x7f61bdf21c77 in destroy ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_wrapper.h:1660:9
    #2 0x7f61bdf21c77 in rx::vk::BufferSuballocationGarbage::destroyIfComplete(rx::RendererVk*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/Suballocation.cpp:190:17
    #3 0x7f61be0ce5cd in rx::vk::SharedGarbageList<rx::vk::BufferSuballocationGarbage>::add(rx::RendererVk*, rx::vk::BufferSuballocationGarbage&&) ./../../third_party/angle/src/libANGLE/renderer/vulkan/ResourceVk.h:195:21
    #4 0x7f61be08b06b in rx::RendererVk::collectSuballocationGarbage(rx::vk::ResourceUse const&, rx::vk::BufferSuballocation&&, rx::vk::Buffer&&) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.h:325:35
    #5 0x7f61be08b428 in release ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:5085:19
    #6 0x7f61be08b428 in rx::vk::BufferHelper::releaseBufferAndDescriptorSetCache(rx::RendererVk*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:5110:5
    #7 0x7f61bde41979 in rx::ContextVk::releaseBufferAllocation(rx::vk::BufferHelper*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:7318:19
    #8 0x7f61bddd7cc4 in rx::BufferVk::release(rx::ContextVk*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/BufferVk.cpp:339:9
    #9 0x7f61be3847b3 in release ./../../third_party/angle/src/libANGLE/RefCountObject.h:45:13
    #10 0x7f61be3847b3 in DeleteObject ./../../third_party/angle/src/libANGLE/ResourceManager.cpp:122:13
    #11 0x7f61be3847b3 in gl::TypedResourceManager<gl::Buffer, gl::BufferManager, gl::BufferID>::deleteObject(gl::Context const*, gl::BufferID) ./../../third_party/angle/src/libANGLE/ResourceManager.cpp:96:9
    #12 0x7f61be232302 in deleteBuffer ./../../third_party/angle/src/libANGLE/Context.cpp:1128:28
    #13 0x7f61be232302 in gl::Context::deleteBuffers(int, gl::BufferID const*) ./../../third_party/angle/src/libANGLE/Context.cpp:6738:9
    #14 0x5607425c6bc3 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDeleteBuffers(int, unsigned int const volatile*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1020:10
    #15 0x56074257404d in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:737:20
    #16 0x560742a8b41b in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:232:35
    #17 0x560742a7a8a3 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) ./../../gpu/ipc/service/command_buffer_stub.cc:507:22
    #18 0x560742a79d79 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command_buffer_stub.cc:155:7
    #19 0x560742a96731 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) ./../../gpu/ipc/service/gpu_channel.cc:874:13
    #20 0x560742aa5e56 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) ./../../base/functional/bind_internal.h:737:12
    #21 0x560742aa5c3c in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> > > ./../../base/functional/bind_internal.h:953:5
    #22 0x560742aa5c3c in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:1066:14
    #23 0x560742aa5c3c in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:979:12
    #24 0x56073f89708d in Run ./../../base/functional/callback.h:156:12
    #25 0x56073f89708d in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) ./../../gpu/command_buffer/service/scheduler_dfs.cc:740:24
    #26 0x56073f894fa2 in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command_buffer/service/scheduler_dfs.cc:665:3
    #27 0x56073f898b93 in Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs *> ./../../base/functional/bind_internal.h:737:12
    #28 0x56073f898b93 in MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:929:12
    #29 0x56073f898b93 in RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:1066:14
    #30 0x56073f898b93 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:979:12
    #31 0x56073a91e224 in Run ./../../base/functional/callback.h:156:12
    #32 0x56073a91e224 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #33 0x56073a97fb0f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #34 0x56073a97fb0f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #35 0x56073a97eaf9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #36 0x56073a9808ca in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #37 0x56073aae7cf2 in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:646:46
    #38 0x56073aaeabb8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:274:43
    #39 0x7f61c76ffd3a in g_main_context_dispatch ??:0:0

previously allocated by thread T0 (chrome) here:
    #0 0x560728f0eb0f in __interceptor_malloc _asan_rtl_:3
    #1 0x7f61b2d4f10d in allocate ./../../third_party/swiftshader/src/System/Memory.cpp:81:42
    #2 0x7f61b2d4f10d in sw::allocateZeroOrPoison(unsigned long, unsigned long) ./../../third_party/swiftshader/src/System/Memory.cpp:110:9
    #3 0x7f61b28d36df in Create<vk::Buffer, VkNonDispatchableHandle<VkBuffer_T *>, VkBufferCreateInfo> ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:58:23
    #4 0x7f61b28d36df in VkResult vk::ObjectBase<vk::Buffer, VkNonDispatchableHandle<VkBuffer_T*>>::Create<VkBufferCreateInfo>(VkAllocationCallbacks const*, VkBufferCreateInfo const*, VkNonDispatchableHandle<VkBuffer_T*>*) ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:92:10
    #5 0x7f61b28d35cd in vkCreateBuffer ./../../third_party/swiftshader/src/Vulkan/libVulkan.cpp:1958:9
    #6 0x7f61be08a78a in init ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_wrapper.h:1668:12
    #7 0x7f61be08a78a in rx::vk::BufferHelper::getBufferForVertexArray(rx::ContextVk*, unsigned long, unsigned long*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:5026:29
    #8 0x7f61bdfac2b5 in rx::VertexArrayVk::syncDirtyAttrib(rx::ContextVk*, gl::VertexAttribute const&, gl::VertexBinding const&, unsigned long, bool) ./../../third_party/angle/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp:862:30
    #9 0x7f61bdfa475e in rx::VertexArrayVk::syncState(gl::Context const*, angle::BitSetT<51ul, unsigned long, unsigned long> const&, std::__Cr::array<angle::BitSetT<5ul, unsigned long, unsigned long>, 16ul>*, std::__Cr::array<angle::BitSetT<4ul, unsigned long, unsigned long>, 16ul>*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp:646:17
    #10 0x7f61be416d92 in gl::VertexArray::syncState(gl::Context const*) ./../../third_party/angle/src/libANGLE/VertexArray.cpp:641:9
    #11 0x7f61be20d368 in syncDirtyObjects ./../../third_party/angle/src/libANGLE/State.h:1612:9
    #12 0x7f61be20d368 in syncDirtyObjects ./../../third_party/angle/src/libANGLE/Context.inl.h:126:19
    #13 0x7f61be20d368 in prepareForDraw ./../../third_party/angle/src/libANGLE/Context.inl.h:136:5
    #14 0x7f61be20d368 in gl::Context::drawArraysInstanced(gl::PrimitiveMode, int, int, int) ./../../third_party/angle/src/libANGLE/Context.cpp:2776:5
    #15 0x560742603321 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArraysInstancedANGLE(unsigned int, int, int, int) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:4785:10
    #16 0x56074257404d in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:737:20
    #17 0x560742a8b41b in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:232:35
    #18 0x560742a7a8a3 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) ./../../gpu/ipc/service/command_buffer_stub.cc:507:22
    #19 0x560742a79d79 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command_buffer_stub.cc:155:7
    #20 0x560742a96731 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) ./../../gpu/ipc/service/gpu_channel.cc:874:13
    #21 0x560742aa5e56 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) ./../../base/functional/bind_internal.h:737:12
    #22 0x560742aa5c3c in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> > > ./../../base/functional/bind_internal.h:953:5
    #23 0x560742aa5c3c in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:1066:14
    #24 0x560742aa5c3c in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:979:12
    #25 0x56073f89708d in Run ./../../base/functional/callback.h:156:12
    #26 0x56073f89708d in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) ./../../gpu/command_buffer/service/scheduler_dfs.cc:740:24
    #27 0x56073f894fa2 in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command_buffer/service/scheduler_dfs.cc:665:3
    #28 0x56073f898b93 in Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs *> ./../../base/functional/bind_internal.h:737:12
    #29 0x56073f898b93 in MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:929:12
    #30 0x56073f898b93 in RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:1066:14
    #31 0x56073f898b93 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:979:12
    #32 0x56073a91e224 in Run ./../../base/functional/callback.h:156:12
    #33 0x56073a91e224 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #34 0x56073a97fb0f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #35 0x56073a97fb0f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #36 0x56073a97eaf9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #37 0x56073a9808ca in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #38 0x56073aae7cf2 in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:646:46
    #39 0x56073aaeabb8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:274:43
    #40 0x7f61c76ffd3a in g_main_context_dispatch ??:0:0

Thread T18 created by T0 (chrome) here:
    #0 0x560728ef4981 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x7f61b28b3eae in __libcpp_thread_create ./../../third_party/libc++/src/include/__thread/support/pthread.h:181:10
    #2 0x7f61b28b3eae in std::__Cr::thread::thread<void (vk::Queue::*)(marl::Scheduler*), vk::Queue*, marl::Scheduler*&, 0>(void (vk::Queue::*&&)(marl::Scheduler*), vk::Queue*&&, marl::Scheduler*&) ./../../third_party/libc++/src/include/__thread/thread.h:212:14
    #3 0x7f61b28b3afb in vk::Queue::Queue(vk::Device*, marl::Scheduler*) ./../../third_party/swiftshader/src/Vulkan/VkQueue.cpp:38:16
    #4 0x7f61b286d432 in vk::Device::Device(VkDeviceCreateInfo const*, void*, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__Cr::shared_ptr<marl::Scheduler> const&) ./../../third_party/swiftshader/src/Vulkan/VkDevice.cpp:139:26
    #5 0x7f61b28ce3b5 in DispatchableObject<const VkDeviceCreateInfo *, void *, vk::PhysicalDevice *, const VkPhysicalDeviceFeatures *, std::__Cr::shared_ptr<marl::Scheduler> > ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:127:8
    #6 0x7f61b28ce3b5 in Create<vk::DispatchableObject<vk::Device, VkDevice_T *>, VkDevice_T *, VkDeviceCreateInfo, vk::PhysicalDevice *, const VkPhysicalDeviceFeatures *, std::__Cr::shared_ptr<marl::Scheduler> > ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:65:34
    #7 0x7f61b28ce3b5 in VkResult vk::DispatchableObject<vk::Device, VkDevice_T*>::Create<VkDeviceCreateInfo, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__Cr::shared_ptr<marl::Scheduler>>(VkAllocationCallbacks const*, VkDeviceCreateInfo const*, VkDevice_T**, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__Cr::shared_ptr<marl::Scheduler>) ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:147:10
    #8 0x7f61b28cdd05 in vkCreateDevice ./../../third_party/swiftshader/src/Vulkan/libVulkan.cpp:1264:9
    #9 0x7f61bcf2d81a in terminator_CreateDevice ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:5833:11
    #10 0x7f61bcf30dc5 in loader_create_device_chain ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4937:15
    #11 0x7f61bcf2f3d6 in loader_layer_create_device ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4317:11
    #12 0x7f61bcf44818 in vkCreateDevice ./../../third_party/vulkan-deps/vulkan-loader/src/loader/trampoline.c:1005:20
    #13 0x7f61bded3fdf in rx::RendererVk::createDeviceAndQueue(rx::DisplayVk*, unsigned int) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:3487:5
    #14 0x7f61bdecf517 in rx::RendererVk::initialize(rx::DisplayVk*, egl::Display*, char const*, char const*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:1980:5
    #15 0x7f61bde59022 in rx::DisplayVk::initialize(egl::Display*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/DisplayVk.cpp:110:39
    #16 0x7f61be0f0a56 in rx::DisplayVkXcb::initialize(egl::Display*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/linux/xcb/DisplayVkXcb.cpp:64:23
    #17 0x7f61be27f5cb in egl::Display::initialize() ./../../third_party/angle/src/libANGLE/Display.cpp:1066:36
    #18 0x7f61bdd7a7df in egl::Initialize(egl::Thread*, egl::Display*, int*, int*) ./../../third_party/angle/src/libGLESv2/egl_stubs.cpp:514:5
    #19 0x7f61bdd817db in EGL_Initialize ./../../third_party/angle/src/libGLESv2/entry_points_egl_autogen.cpp:478:27
    #20 0x56073eae6e3c in gl::GLDisplayEGL::InitializeDisplay(bool, std::__Cr::vector<gl::DisplayType, std::__Cr::allocator<gl::DisplayType>>, gl::EGLDisplayPlatform, gl::GLDisplayEGL*) ./../../ui/gl/gl_display.cc:783:10
    #21 0x56073eae54cf in gl::GLDisplayEGL::Initialize(bool, std::__Cr::vector<gl::DisplayType, std::__Cr::allocator<gl::DisplayType>>, gl::EGLDisplayPlatform) ./../../ui/gl/gl_display.cc:673:8
    #22 0x56072b262c29 in ui::GLOzoneEGL::InitializeGLOneOffPlatform(bool, std::__Cr::vector<gl::DisplayType, std::__Cr::allocator<gl::DisplayType>>, gl::GpuPreference) ./../../ui/ozone/common/gl_ozone_egl.cc:25:17
    #23 0x560742abb347 in gl::init::InitializeGLOneOffPlatform(gl::GpuPreference) ./../../ui/gl/init/gl_initializer_ozone.cc:27:26
    #24 0x560742ab9a5b in gl::init::InitializeGLOneOffPlatformImplementation(bool, bool, bool, gl::GpuPreference) ./../../ui/gl/init/gl_factory.cc:211:24
    #25 0x560742ab93f1 in gl::init::(anonymous namespace)::InitializeGLOneOffPlatformHelper(bool, gl::GpuPreference) ./../../ui/gl/init/gl_factory.cc:135:10
    #26 0x560742ab978f in gl::init::InitializeGLNoExtensionsOneOff(bool, gl::GpuPreference) ./../../ui/gl/init/gl_factory.cc:166:10
    #27 0x560742b1b152 in gpu::GpuInit::InitializeAndStartSandbox(base::CommandLine*, gpu::GpuPreferences const&) ./../../gpu/ipc/service/gpu_init.cc:443:18
    #28 0x56075129dec8 in content::GpuMain(content::MainFunctionParams) ./../../content/gpu/gpu_main.cc:357:39
    #29 0x560738025888 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #30 0x560738026db1 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #31 0x5607380297ef in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1146:10
    #32 0x560738023be0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:335:36
    #33 0x56073802425b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:348:10
    #34 0x560728f44de8 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #35 0x7f61c6429d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwn11/asan-linux-release/././libvk_swiftshader.so+0x45445a) (BuildId: 7b83c3575abf9e76)
Shadow bytes around the buggy address:
  0x50700011b480: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fa fa
  0x50700011b500: f7 fa fd fd fd fd fd fd fd fd fd fd fa fa f7 fa
  0x50700011b580: fd fd fd fd fd fd fd fd fd fa fa fa f7 fa fd fd
  0x50700011b600: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
  0x50700011b680: fd fd fd fd fd fd fa fa f7 fa fd fd fd fd fd fd
=>0x50700011b700: fd fd fd fd fa fa f7 fa fd[fd]fd fd fd fd fd fd
  0x50700011b780: fd fd fa fa f7 fa fd fd fd fd fd fd fd fd fd fd
  0x50700011b800: fa fa f7 fa fd fd fd fd fd fd fd fd fd fa fa fa
  0x50700011b880: f7 fa fd fd fd fd fd fd fd fd fd fd fa fa f7 fa
  0x50700011b900: fd fd fd fd fd fd fd fd fd fa fa fa f7 fa fd fd
  0x50700011b980: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
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

==210209==ADDITIONAL INFO

==210209==Note: Please include this section with the ASan report.
Task trace:


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==210209==END OF ADDITIONAL INFO
==210209==ABORTING


## Attachments

- [crash.html](attachments/crash.html) (text/html, 1.8 KB)
- [debug.log](attachments/debug.log) (text/plain, 6.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 25.3 KB)
- [webgl-test-utils.js](attachments/webgl-test-utils.js) (text/javascript, 112.4 KB)
- crash.html (text/html, 114.0 KB)

## Timeline

### pa...@chromium.org (2024-03-04)

[security shepherd] I can reproduce this issue. As per <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md#toc-critical-severity>, setting severity to S0 since it is a UaF in the GPU process, but feel to re-assess if we should lower this.

### cl...@appspot.gserviceaccount.com (2024-03-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4936467045875712.

### pa...@chromium.org (2024-03-04)

[security shepherd] launched CF on this to get the impact.

### pa...@chromium.org (2024-03-05)

Attaching the file I used to run CF.

### ad...@chromium.org (2024-03-05)

The minimize task is taking a while here, which is why we don't yet have a regression range from ClusterFuzz. I'll test manually.

### ad...@chromium.org (2024-03-05)

Reproduced using `asan-linux-release-1268379.zip` and `DISPLAY=:20 ./chrome --user-data-dir=/tmp/xx7 --disable-gpu http://localhost:8000/crash9.html`

Does not reproduce using `asan-linux-release-1250580.zip` (122 equivalent)

Does reproduce with `asan-linux-release-1262506.zip` (123 equivalent)

Setting FoundIn 123.

### pe...@google.com (2024-03-05)

Setting milestone because of s0/s1 severity.

### ad...@chromium.org (2024-03-06)

I'm not sure what platforms Swiftshader is on, but assuming all desktop platforms.

### ge...@chromium.org (2024-03-07)

I'm investigating. I have reproduced locally and I'm reducing the test case to debug.

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### es...@chromium.org (2024-03-13)

[secondary security shepherd] geofflang, could you provide an update please? Thanks!

### ge...@chromium.org (2024-03-14)

Have a good local repro. Fix is in progress.

### ap...@google.com (2024-03-14)

Project: angle/angle
Branch: main

commit e5cb7f1f5ca2110bed014fc076da47ba7adb6063
Author: Geoff Lang <geofflang@chromium.org>
Date:   Tue Mar 12 16:06:37 2024

    Vulkan: Fix access to inactive attributes
    
    ... within range of active ones.  Since a buffer is bound for inactive
    attributes, it must be considered accessed.
    
    Ultimately, the nullDescriptor feature could be used to avoid binding a
    buffer for inactive attributes.
    
    Bug: chromium:327807820
    Change-Id: Ieceea9442310c23568c47cef7357b4094b7ebbb4
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5369336
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

M       src/libANGLE/renderer/vulkan/ContextVk.cpp
M       src/tests/gl_tests/VertexAttributeTest.cpp

https://chromium-review.googlesource.com/5369336


### ap...@google.com (2024-03-14)

Project: chromium/src
Branch: main

commit 1dc53b230f87772387fc4bf59513d25bffe7a58b
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Thu Mar 14 19:57:53 2024

    Roll ANGLE from 533fa5cedc61 to e5cb7f1f5ca2 (1 revision)
    
    https://chromium.googlesource.com/angle/angle.git/+log/533fa5cedc61..e5cb7f1f5ca2
    
    2024-03-14 geofflang@chromium.org Vulkan: Fix access to inactive attributes
    
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
    Bug: chromium:327807820
    Tbr: abdolrashidi@google.com
    Change-Id: I21bcc6e2bfd0d69b8c06a9d406de46d35644b11a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5372877
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1273006}

M       DEPS
M       third_party/angle

https://chromium-review.googlesource.com/5372877


### es...@google.com (2024-03-15)

Thank you geofflang@! Looks like a CL landed, should this be marked Fixed now or is there more to do?

### ge...@chromium.org (2024-03-15)

I believe it is fixed. It fixes the local test case I made, I still need to confirm the original test case.

### 24...@project.gserviceaccount.com (2024-03-15)

ClusterFuzz testcase 4936467045875712 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1273002:1273011

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### pe...@google.com (2024-03-16)

Requesting merge to stable (M123) because latest trunk commit (1273006) appears to be after stable branch point (1262506).
Merge review required: a commit with DEPS changes was detected.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [123].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### sy...@chromium.org (2024-03-19)

1. https://chromium-review.googlesource.com/c/angle/angle/+/5369336
2. It's been verified by ClusterFuzz
3. No
4. No
5. No

### am...@chromium.org (2024-03-20)

<https://crrev.com/c/5369336> approved for merge to M123, please merge this fix to branch 6312 at your earliest convenience and before EOD Thursday, 21 March so this fix can be included in the first M123 Stable update

### ap...@google.com (2024-03-22)

Project: angle/angle
Branch: chromium/6312

commit bbf1e1ea6bcf61e5e8e403870fd88df4e5e3a892
Author: Geoff Lang <geofflang@chromium.org>
Date:   Tue Mar 12 16:06:37 2024

    M123: Vulkan: Fix access to inactive attributes
    
    ... within range of active ones.  Since a buffer is bound for inactive
    attributes, it must be considered accessed.
    
    Ultimately, the nullDescriptor feature could be used to avoid binding a
    buffer for inactive attributes.
    
    Bug: chromium:327807820
    Change-Id: I953b419d8ec51760e8848409024cad5083888fa2
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5386431
    Reviewed-by: Shahbaz Youssefi <syoussefi@google.com>

M       src/libANGLE/renderer/vulkan/ContextVk.cpp
M       src/tests/gl_tests/VertexAttributeTest.cpp

https://chromium-review.googlesource.com/5386431


### pe...@google.com (2024-03-22)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### am...@google.com (2024-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-22)

Congratulations, Cassidy Kim! The Chrome VRP has decided to award you $10,000 for this report of memory corruption in the GPU process. Thank you for your efforts in discovering and reporting this issue to us -- nicely done and much appreciated!

### vo...@google.com (2024-03-25)

Wasn't able to reproduce in M120, according to [comment #7](https://issues.chromium.org/issues/327807820#comment7) seems like it's a regression in M123. So I'm marking this as not applicable to M120 LTS.

### pe...@google.com (2024-06-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/327807820)*
