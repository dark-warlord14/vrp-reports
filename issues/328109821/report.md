# heap-buffer-overflow in vk::Image::copy

| Field | Value |
|-------|-------|
| **Issue ID** | [328109821](https://issues.chromium.org/issues/328109821) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ab...@google.com |
| **Created** | 2024-03-05 |
| **Bounty** | $2,000.00 |

## Description

tested os:
ubuntu 22.04
tested chrome version:
stable & dev

repro steps:
./chrome   --user-data-dir=/tmp/xx7 --disable-gpu http://localhost:8000/crash.html 

==1598117==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7efd9d6f3917 at pc 0x5589cea51a62 bp 0x7efd7c161f70 sp 0x7efd7c161730
READ of size 2336 at 0x7efd9d6f3917 thread T17
    #0 0x5589cea51a61 in __asan_memcpy _asan_rtl_:3
    #1 0x7efda5896041 in vk::Image::copy(void const*, void*, unsigned int, unsigned int, VkImageSubresourceLayers const&, VkOffset3D const&, VkExtent3D const&) ./../../third_party/swiftshader/src/Vulkan/VkImage.cpp:659:5
    #2 0x7efda58966cc in vk::Image::copyFrom(vk::Buffer*, VkBufferImageCopy2 const&) ./../../third_party/swiftshader/src/Vulkan/VkImage.cpp:684:2
    #3 0x7efda585bd72 in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) ./../../third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:2383:12
    #4 0x7efda58b5e4f in vk::Queue::submitQueue(vk::Queue::Task const&) ./../../third_party/swiftshader/src/Vulkan/VkQueue.cpp:104:42
    #5 0x7efda58b4fe0 in vk::Queue::taskLoop(marl::Scheduler*) ./../../third_party/swiftshader/src/Vulkan/VkQueue.cpp:156:4
    #6 0x7efda58b8985 in __invoke<void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *, void> ./../../third_party/libc++/src/include/__type_traits/invoke.h:118:25
    #7 0x7efda58b8985 in __thread_execute<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct> >, void (vk::Queue::*)(marl::Scheduler *), vk::Queue *, marl::Scheduler *, 2UL, 3UL> ./../../third_party/libc++/src/include/__thread/thread.h:193:3
    #8 0x7efda58b8985 in void* std::__Cr::__thread_proxy<std::__Cr::tuple<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct>>, void (vk::Queue::*)(marl::Scheduler*), vk::Queue*, marl::Scheduler*>>(void*) ./../../third_party/libc++/src/include/__thread/thread.h:202:3
    #9 0x5589cea516a8 in asan_thread_start(void*) _asan_rtl_:28

0x7efd9d6f3917 is located 0 bytes after 4194583-byte region [0x7efd9d2f3800,0x7efd9d6f3917)
allocated by thread T0 (chrome) here:
    #0 0x5589cea53b0f in __interceptor_malloc _asan_rtl_:3
    #1 0x7efda5d543fd in allocate ./../../third_party/swiftshader/src/System/Memory.cpp:81:42
    #2 0x7efda5d543fd in sw::allocateZeroOrPoison(unsigned long, unsigned long) ./../../third_party/swiftshader/src/System/Memory.cpp:110:9
    #3 0x7efda587c9a2 in vk::DeviceMemory::allocateBuffer() ./../../third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:342:11
    #4 0x7efda587b5d6 in allocate ./../../third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:275:12
    #5 0x7efda587b5d6 in vk::DeviceMemory::Allocate(VkAllocationCallbacks const*, VkMemoryAllocateInfo const*, VkNonDispatchableHandle<VkDeviceMemory_T*>*, vk::Device*) ./../../third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:103:29
    #6 0x7efda58d21b2 in vkAllocateMemory ./../../third_party/swiftshader/src/Vulkan/libVulkan.cpp:1382:20
    #7 0x7efdb1ee8637 in allocate ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_wrapper.h:1497:12
    #8 0x7efdb1ee8637 in rx::(anonymous namespace)::FindAndAllocateCompatibleMemory(rx::vk::Context*, rx::vk::MemoryAllocationType, rx::vk::MemoryProperties const&, unsigned int, unsigned int*, VkMemoryRequirements const&, void const*, unsigned int*, rx::vk::DeviceMemory*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:112:40
    #9 0x7efdb1ee4d9d in AllocateAndBindBufferOrImageMemory<rx::vk::Buffer> ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:188:5
    #10 0x7efdb1ee4d9d in AllocateBufferOrImageMemory<rx::vk::Buffer> ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:212:5
    #11 0x7efdb1ee4d9d in rx::vk::AllocateBufferMemory(rx::vk::Context*, rx::vk::MemoryAllocationType, unsigned int, unsigned int*, void const*, rx::vk::Buffer*, unsigned int*, rx::vk::DeviceMemory*, unsigned long*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:562:12
    #12 0x7efdb1e782d7 in rx::vk::BufferPool::allocateNewBuffer(rx::vk::Context*, unsigned long) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:3426:5
    #13 0x7efdb1e78f36 in rx::vk::BufferPool::allocateBuffer(rx::vk::Context*, unsigned long, unsigned long, rx::vk::BufferSuballocation*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:3547:5
    #14 0x7efdb1e8b6ad in rx::vk::BufferHelper::initSuballocation(rx::vk::Context*, unsigned int, unsigned long, unsigned long, rx::BufferUsageType, rx::vk::BufferPool*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:4934:5
    #15 0x7efdb1c40663 in rx::ContextVk::initBufferAllocation(rx::vk::BufferHelper*, unsigned int, unsigned long, unsigned long, rx::BufferUsageType) ./../../third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:7124:42
    #16 0x7efdb1bd89ef in acquireBufferHelper ./../../third_party/angle/src/libANGLE/renderer/vulkan/BufferVk.cpp:1209:5
    #17 0x7efdb1bd89ef in rx::BufferVk::setDataWithMemoryType(gl::Context const*, gl::BufferBinding, void const*, unsigned long, unsigned int, gl::BufferUsage) ./../../third_party/angle/src/libANGLE/renderer/vulkan/BufferVk.cpp:469:9
    #18 0x7efdb1bd7ff1 in rx::BufferVk::setDataWithUsageFlags(gl::Context const*, gl::BufferBinding, void*, void const*, unsigned long, gl::BufferUsage, unsigned int) ./../../third_party/angle/src/libANGLE/renderer/vulkan/BufferVk.cpp:423:12
    #19 0x7efdb1fc792b in gl::Buffer::bufferDataImpl(gl::Context*, gl::BufferBinding, void const*, long, gl::BufferUsage, unsigned int) ./../../third_party/angle/src/libANGLE/Buffer.cpp:159:16
    #20 0x7efdb1fc7d39 in gl::Buffer::bufferData(gl::Context*, gl::BufferBinding, void const*, long, gl::BufferUsage) ./../../third_party/angle/src/libANGLE/Buffer.cpp:123:12
    #21 0x5589e8198737 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBufferData(unsigned int, long, void const*, unsigned int) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:666:10
    #22 0x5589e814908d in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:737:20
    #23 0x5589e86675bb in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:232:35
    #24 0x5589e8656b33 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) ./../../gpu/ipc/service/command_buffer_stub.cc:507:22
    #25 0x5589e8656009 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command_buffer_stub.cc:155:7
    #26 0x5589e86728d1 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) ./../../gpu/ipc/service/gpu_channel.cc:874:13
    #27 0x5589e8682066 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) ./../../base/functional/bind_internal.h:738:12
    #28 0x5589e8681e4c in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> > > ./../../base/functional/bind_internal.h:954:5
    #29 0x5589e8681e4c in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:1067:14
    #30 0x5589e8681e4c in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #31 0x5589e5472d2d in Run ./../../base/functional/callback.h:156:12
    #32 0x5589e5472d2d in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) ./../../gpu/command_buffer/service/scheduler_dfs.cc:740:24
    #33 0x5589e5470c42 in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command_buffer/service/scheduler_dfs.cc:665:3
    #34 0x5589e5474833 in Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs *> ./../../base/functional/bind_internal.h:738:12
    #35 0x5589e5474833 in MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:930:12
    #36 0x5589e5474833 in RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #37 0x5589e5474833 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #38 0x5589e04d8834 in Run ./../../base/functional/callback.h:156:12
    #39 0x5589e04d8834 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #40 0x5589e053a11f in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #41 0x5589e053a11f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #42 0x5589e0539109 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #43 0x5589e053aeda in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0

Thread T17 created by T0 (chrome) here:
    #0 0x5589cea39981 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x7efda58b522e in __libcpp_thread_create ./../../third_party/libc++/src/include/__thread/support/pthread.h:181:10
    #2 0x7efda58b522e in std::__Cr::thread::thread<void (vk::Queue::*)(marl::Scheduler*), vk::Queue*, marl::Scheduler*&, 0>(void (vk::Queue::*&&)(marl::Scheduler*), vk::Queue*&&, marl::Scheduler*&) ./../../third_party/libc++/src/include/__thread/thread.h:212:14
    #3 0x7efda58b4e7b in vk::Queue::Queue(vk::Device*, marl::Scheduler*) ./../../third_party/swiftshader/src/Vulkan/VkQueue.cpp:38:16
    #4 0x7efda586e7ac in vk::Device::Device(VkDeviceCreateInfo const*, void*, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__Cr::shared_ptr<marl::Scheduler> const&) ./../../third_party/swiftshader/src/Vulkan/VkDevice.cpp:139:26
    #5 0x7efda58cf925 in DispatchableObject<const VkDeviceCreateInfo *, void *, vk::PhysicalDevice *, const VkPhysicalDeviceFeatures *, std::__Cr::shared_ptr<marl::Scheduler> > ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:127:8
    #6 0x7efda58cf925 in Create<vk::DispatchableObject<vk::Device, VkDevice_T *>, VkDevice_T *, VkDeviceCreateInfo, vk::PhysicalDevice *, const VkPhysicalDeviceFeatures *, std::__Cr::shared_ptr<marl::Scheduler> > ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:65:34
    #7 0x7efda58cf925 in VkResult vk::DispatchableObject<vk::Device, VkDevice_T*>::Create<VkDeviceCreateInfo, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__Cr::shared_ptr<marl::Scheduler>>(VkAllocationCallbacks const*, VkDeviceCreateInfo const*, VkDevice_T**, vk::PhysicalDevice*, VkPhysicalDeviceFeatures const*, std::__Cr::shared_ptr<marl::Scheduler>) ./../../third_party/swiftshader/src/Vulkan/VkObject.hpp:147:10
    #8 0x7efda58cf275 in vkCreateDevice ./../../third_party/swiftshader/src/Vulkan/libVulkan.cpp:1264:9
    #9 0x7efd9e92d81a in terminator_CreateDevice ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:5833:11
    #10 0x7efd9e930dc5 in loader_create_device_chain ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4937:15
    #11 0x7efd9e92f3d6 in loader_layer_create_device ./../../third_party/vulkan-deps/vulkan-loader/src/loader/loader.c:4317:11
    #12 0x7efd9e944818 in vkCreateDevice ./../../third_party/vulkan-deps/vulkan-loader/src/loader/trampoline.c:1005:20
    #13 0x7efdb1cd475f in rx::RendererVk::createDeviceAndQueue(rx::DisplayVk*, unsigned int) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:3490:5
    #14 0x7efdb1ccfc97 in rx::RendererVk::initialize(rx::DisplayVk*, egl::Display*, char const*, char const*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:1978:5
    #15 0x7efdb1c598a2 in rx::DisplayVk::initialize(egl::Display*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/DisplayVk.cpp:110:39
    #16 0x7efdb1ef49d6 in rx::DisplayVkXcb::initialize(egl::Display*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/linux/xcb/DisplayVkXcb.cpp:64:23
    #17 0x7efdb2082e1b in egl::Display::initialize() ./../../third_party/angle/src/libANGLE/Display.cpp:1066:36
    #18 0x7efdb1b7a7ef in egl::Initialize(egl::Thread*, egl::Display*, int*, int*) ./../../third_party/angle/src/libGLESv2/egl_stubs.cpp:514:5
    #19 0x7efdb1b817eb in EGL_Initialize ./../../third_party/angle/src/libGLESv2/entry_points_egl_autogen.cpp:478:27
    #20 0x5589e46a02dc in gl::GLDisplayEGL::InitializeDisplay(bool, std::__Cr::vector<gl::DisplayType, std::__Cr::allocator<gl::DisplayType>>, gl::EGLDisplayPlatform, gl::GLDisplayEGL*) ./../../ui/gl/gl_display.cc:783:10
    #21 0x5589e469e96f in gl::GLDisplayEGL::Initialize(bool, std::__Cr::vector<gl::DisplayType, std::__Cr::allocator<gl::DisplayType>>, gl::EGLDisplayPlatform) ./../../ui/gl/gl_display.cc:673:8
    #22 0x5589d0db7189 in ui::GLOzoneEGL::InitializeGLOneOffPlatform(bool, std::__Cr::vector<gl::DisplayType, std::__Cr::allocator<gl::DisplayType>>, gl::GpuPreference) ./../../ui/ozone/common/gl_ozone_egl.cc:25:17
    #23 0x5589e86976c7 in gl::init::InitializeGLOneOffPlatform(gl::GpuPreference) ./../../ui/gl/init/gl_initializer_ozone.cc:27:26
    #24 0x5589e8695ddb in gl::init::InitializeGLOneOffPlatformImplementation(bool, bool, bool, gl::GpuPreference) ./../../ui/gl/init/gl_factory.cc:211:24
    #25 0x5589e8695771 in gl::init::(anonymous namespace)::InitializeGLOneOffPlatformHelper(bool, gl::GpuPreference) ./../../ui/gl/init/gl_factory.cc:135:10
    #26 0x5589e8695b0f in gl::init::InitializeGLNoExtensionsOneOff(bool, gl::GpuPreference) ./../../ui/gl/init/gl_factory.cc:166:10
    #27 0x5589e86f74d2 in gpu::GpuInit::InitializeAndStartSandbox(base::CommandLine*, gpu::GpuPreferences const&) ./../../gpu/ipc/service/gpu_init.cc:443:18
    #28 0x5589f6e36f28 in content::GpuMain(content::MainFunctionParams) ./../../content/gpu/gpu_main.cc:357:39
    #29 0x5589ddbf8f98 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #30 0x5589ddbfa4c1 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #31 0x5589ddbfceff in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1146:10
    #32 0x5589ddbf72f0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:333:36
    #33 0x5589ddbf796b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:346:10
    #34 0x5589df0d3c4f in HeadlessChildMain ./../../headless/app/headless_shell.cc:195:12
    #35 0x5589df0d3c4f in headless::HeadlessShellMain(content::ContentMainParams) ./../../headless/app/headless_shell.cc:256:5
    #36 0x5589cea89da5 in ChromeMain ./../../chrome/app/chrome_main.cc:178:14
    #37 0x7efdb9029d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/pwn11/asan-linux-release/chrome+0xe55aa61) (BuildId: e96457291d9dde52)
Shadow bytes around the buggy address:
  0x7efd9d6f3680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7efd9d6f3700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7efd9d6f3780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7efd9d6f3800: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7efd9d6f3880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7efd9d6f3900: 00 00[07]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7efd9d6f3980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7efd9d6f3a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7efd9d6f3a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7efd9d6f3b00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7efd9d6f3b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==1598117==ADDITIONAL INFO

==1598117==Note: Please include this section with the ASan report.
Task trace:


==1598117==END OF ADDITIONAL INFO
==1598117==ABORTING

## Attachments

- [crash.html](attachments/crash.html) (text/html, 2.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 18.5 KB)
- [launcher.sh](attachments/launcher.sh) (text/x-sh, 519 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-03-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5112568707743744.

### ad...@chromium.org (2024-03-05)

ClusterFuzz was unable to reproduce this - I'll try locally.

### ad...@chromium.org (2024-03-05)

I also can't reproduce this with a local ASAN build - please let me know the exact version numbers you reproduced this with, and I'll try on them.

### em...@gmail.com (2024-03-05)


I believe that both very old versions (like Chromium 115.0.5744.0) and the latest versions should consistently reproduce the issue. I just downloaded the latest asan-build of Chrome, and I can also reproduce it.
Chromium 124.0.6340.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1268379.zip)
Chromium 115.0.5744.0

### ad...@chromium.org (2024-03-05)

Yep - reproduced with gs://chromium-browser-asan/linux-release/asan-linux-release-1268379.zip, thanks.

Setting severity: this is a buffer overflow read in the GPU process. OOB reads are usually medium severity if the result can be passed back to a compromised renderer process (which isn't known in this case, but as we seem to be copying into an image buffer it seems reasonably likely); this requires Swiftshader which is a further impediment - medium or low sounds right - I'll err on the side of caution and rate it medium severity. I'll test on some other release branches to set FoundIn.

### ad...@chromium.org (2024-03-05)

Reproduced also with asan-linux-release-1250580.zip, which corresponds to the M122 branch point, so setting FoundIn.

### pe...@google.com (2024-03-05)

Setting milestone because of s2 severity.

### pe...@google.com (2024-03-05)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ad...@chromium.org (2024-03-06)

I'm not sure what platforms Swiftshader is on, but assuming all desktop platforms.

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

### pe...@google.com (2024-03-20)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### em...@gmail.com (2024-04-02)

Hi,Is there any progress?


### pe...@google.com (2024-04-04)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### em...@gmail.com (2024-04-25)

Friendly ping, any updates on this issue? Just checking.

### ge...@chromium.org (2024-10-21)

Shabi: You may want to take a look at this. Looks like a possibly incorrect buffer size calculation when initializing a RGB8\_ETC2 texture.

### sy...@chromium.org (2024-10-21)

Amirali agreed to take a look at this, thanks!

### ab...@google.com (2024-10-28)

Hello,

I have been unable to repro this on local Linux (Release/ASAN). I build Chromium locally and ran this:

- `./out/Test/chrome --user-data-dir=/tmp/xx7 --disable-gpu http://localhost:8000/crash.html`

Should the error occur when Chrome is launched? Or does it occur after a certain event?

### em...@gmail.com (2024-10-28)

I have just tested the latest version, and the reproduction method mentioned above should be sufficient without requiring any special actions.

Alternatively, try adding the --enable-unsafe-swiftshader flag.

Tested version: asan-linux-release-1374142.zip

### ab...@google.com (2024-10-28)

After syncing, I tried building and running the same command. However, I was still unable to repro. I also tried `--enable-unsafe-swiftshader`, but no success.

- `./out/Test/chrome --user-data-dir=/tmp/xx7 --disable-gpu --enable-unsafe-swiftshader http://localhost:8000/crash.html`

Which GN args did you use? I tried using the following:

```
use_remoteexec = true
is_component_build = false
is_debug = false
is_asan = true

```

### em...@gmail.com (2024-10-28)

Here is my args.gn, but I feel the issue should be unrelated to this.

Could you please download this version and see if you can reproduce the issue on your machine?
gsutil cp gs://chromium-browser-asan/linux-release/asan-linux-release-1374142.zip .

args.gn

```
is_asan = true
is_debug = false
enable_nacl = false
treat_warnings_as_errors = false
is_component_build=false
dcheck_always_on = false

```

### ab...@google.com (2024-11-06)

I downloaded the package from the comment above using the following: `gsutil cp gs://chromium-browser-asan/linux-release/asan-linux-release-1374142.zip .`

Then I tried running `chrome` using the flags from before.

Unfortunately, I am still unable to reproduce the issue locally. (I also tried `--enable-unsafe-swiftshader`.)

### em...@gmail.com (2024-11-06)

Thank you for your reply; perhaps differences between machines are affecting reproduction.
I have uploaded the auto-run script; could you please try again?
Usage:
arg1: Browser path
arg2: Test page
arg3: Number of browsers

```
./launch.sh ./chrome http://localhost:8880/crash.html 5

```

### ab...@google.com (2024-11-09)

Thank you for sharing the script.

I tried running it locally as stated for some time. Unfortunately, it is still not reproducing the issue. I also increased the execution count to 10, but to no avail.

The only logs I see are a variation of the messages below:

```
[871344:871344:1108/170301.930391:ERROR:zygote_communication_linux.cc(296)] Failed to send GetTerminationStatus message to zygote
Error: unrecognized flag --no-expose-wasm
Try --help for options
Fontconfig error: Cannot load default config file: No such file: (null)

```

Perhaps it is indeed due to the differences between the machines.

### ma...@chromium.org (2024-12-23)

[Security shepherd] Security issues must have an assignee. Re-assigning to previous assignee.

### ab...@google.com (2026-03-05)

Hello,

I was able to repro the issue locally on Linux (ASAN Release). The reason for no repro from [comment #24](https://issues.chromium.org/issues/328109821#comment24) seems to have been the file `crash.html` (from [comment #1](https://issues.chromium.org/issues/328109821#comment1)) not being present at the right location.

The following GN args were used to build `chrome`:

```
is_asan = true
is_debug = false
enable_nacl = false
treat_warnings_as_errors = false
is_component_build=false
dcheck_always_on = false
use_remoteexec = true

```

After running the HTTP server in the location of `crash.html` (`python3 -m http.server 8000`), the following command was used to run Chrome, which resulted in the crash:

```
./out/Test/chrome --user-data-dir=/tmp/xx7 --disable-gpu --enable-unsafe-swiftshader http://localhost:8000/crash.html

```

The issue is indeed related to the incorrect buffer size used for a compressed 2D array texture.

The function `computeCompressedImageSize()` in `ImageHelper::stageResourceClearWithFormat()` uses a modified `glExtents` where the depth is set to 1 for the array texture types beforehand (in `stageRobustResourceClearWithFormat()`). This results in a smaller buffer than needed for image copy, leading to errors later. After using the layer count for such images to compute the size, the error no longer occurs.

A draft change has now been uploaded to fix the issue: <https://chromium-review.git.corp.google.com/c/angle/angle/+/7636098>

### dx...@google.com (2026-03-09)

Project: angle/angle  

Branch:  main  

Author:  Amirali Abdolrashidi [abdolrashidi@google.com](mailto:abdolrashidi@google.com)  

Link:    <https://chromium-review.googlesource.com/7636098>

Vulkan: Fix array compressed tex size for copy

---


Expand for full commit details
```
     
      In ImageHelper::stageResourceClearWithFormat(), the required size for 
    image copy is determined by computeCompressedImageSize(), which takes a 
    glExtents arg. However, in stageRobustResourceClearWithFormat(), which 
    calls this function, the glExtents arg is modified for array textures, 
    so that the layer count is set to the input depth instead and the depth 
    is set to 1. This results in a smaller buffer than needed, leading to 
    memory access errors later. 
     
    This change will make sure that the compressed image size uses the 
    layer count for the array textures. 
     
    * Updated ImageHelper::stageResourceClearWithFormat() so the buffer 
      size computation for an array compressed texture will use the layer 
      count instead of the depth. 
      * (computeCompressedImageSize()) 
      * (Depth is set to 1 in stageRobustResourceClearWithFormat() for 
        such textures.) 
     
    * Added the following unit tests to RobustResourceInitTestES3: 
      * LargeCompressedImage2DArray 
        * It makes sure that the proper robust resource clear path is 
          applied to the whole image and there is no crash due to an 
          incorrect buffer size and copying beyond its bounds. 
      * LargeImage2DArray 
        * Similar test for a non-compressed texture type. 
     
    Bug: chromium:328109821 
    Change-Id: I4ccbc0287ff6f1b1185e40a4c2cde3d6fffa3b80 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7636098 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Charlie Lao <cclao@google.com> 
    Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/vk_helpers.cpp`
- M `src/tests/gl_tests/RobustResourceInitTest.cpp`

---

Hash: [b1dd8daac2a6b3e8d7ddc38c3e501fbb80baf6d5](https://chromiumdash.appspot.com/commit/b1dd8daac2a6b3e8d7ddc38c3e501fbb80baf6d5)  

Date: Thu Mar 5 01:17:47 2026


---

### ab...@google.com (2026-03-09)

After the [change above](https://chromium-review.git.corp.google.com/c/angle/angle/+/7636098), the issue should no longer occur.

I will mark this issue as resolved. Please feel free to re-open in case of further questions or concerns.

Thank you.

### dx...@google.com (2026-03-10)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7647847>

Roll ANGLE from f5d25e4e8937 to 0989237c8802 (6 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/f5d25e4e8937..0989237c8802 
     
    2026-03-09 lexa.knyazev@gmail.com Simplify compressed format validation for TEXTURE_3D 
    2026-03-09 bsheedy@chromium.org Promote src-side Win/x64/rel to CQ 
    2026-03-09 syoussefi@chromium.org Translator: Remove sh::InterfaceBlock::isRowMajorLayout 
    2026-03-09 yuxinhu@google.com IR Validation: call on_error() when the register is double declared 
    2026-03-09 abdolrashidi@google.com Vulkan: Fix array compressed tex size for copy 
    2026-03-09 bsheedy@chromium.org Add src-side win-test equivalents 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,cnorthrop@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:328109821 
    Tbr: cnorthrop@google.com 
    Change-Id: I2874a1e6cb10492bc6c704b91f32aba8dfb94aaf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7647847 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1596763}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [7c355505d843a735b2a5a83cb74788bdb36905ff](https://chromiumdash.appspot.com/commit/7c355505d843a735b2a5a83cb74788bdb36905ff)  

Date: Tue Mar 10 01:30:55 2026


---

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/328109821)*
