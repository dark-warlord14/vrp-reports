# GPU process crash via WebGPU shader - heap-buffer-overflow in Mesa build_interference_graph

| Field | Value |
|-------|-------|
| **Issue ID** | [419939693](https://issues.chromium.org/issues/419939693) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | a7...@gmail.com |
| **Assignee** | ms...@google.com |
| **Created** | 2025-05-24 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

This report is about a heap-buffer-overflow in Mesa, reachable via WebGPU shaders emitted by dawn/tint. I will also upload this report upstream, i.e., the Mesa project, and post the link below.

##### VERSION

Chrome Version 137.0.7140.0 (Developer Build) (64-bit)   

Operating System: Ubuntu   

Mesa: mesa-25.1.1, commit 7485541cc3a8a4f60ef66e02265048aadf14b3ed

##### REPRODUCTION CASE

The bug is provoked by compiling the following shader, first with tint to SPIR-V and then later with Mesa:

```
@group(0) @binding(0)
var<storage, read_write> d: array<vec4<f32>, 8>;

@fragment fn frag_main(@builtin(position) f: vec4<f32>) -> @location(0) vec4<f32> {
    var q: array<vec4<f32>, 8>;
    var r: vec4<f32>;
    var g: i32;
    var h: array<vec4<f32>, 16>;

    loop {
        loop {
            q = d;
            continuing {
                break if any(f <= f);
            }
        }
        if g < 9 {
            d = d;
            break;
        }
        r = q[g];
        g = 9;
    }
    let n = i32(r.x);
    return h[n];
}

```

There are two means of reproduction, first the standalone reproduction via gfxrecon-replay. The attached .gfxr allows to reproduce outside of chrome as follows:
`LD_PRELOAD=/usr/lib/llvm-18/lib/clang/18/lib/linux/libclang_rt.asan-x86_64.so VK_DRIVER_FILES=~/src/intel/vulkan/intel_icd.x86_64.json ASAN_OPTIONS=detect_leaks=0,abort_on_error=1 ~/gfxrecon-replay gfxrecon_capture_20250524T090556.gfxr`

When enabling assertions, the shader trigger: `assertion size <= ARRAY_SIZE(compiler->reg_set.classes) && "Register allocation relies on split_virtual_grfs()" ../src/intel/compiler/brw_reg_allocate.cpp 661 void brw_reg_alloc::build_interference_graph(bool)`

Reproducing the issue in Chrome requires an ASAN build of Mesa as well as an ASAN build of Chromium. Opening the attached html file should trigger the UAF in the Chrome GPU process:

```
==13643==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x70e761903b30 at pc 0x6f1756a4c81a bp 0x7fffaea50660 sp 0x7fffaea50658
READ of size 8 at 0x70e761903b30 thread T0 (chrome)
[13606:13624:0523/140012.314921:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
    #0 0x6f1756a4c819 in brw_reg_alloc::build_interference_graph(bool) /home/user/buildASAN/../src/intel/compiler/brw_reg_allocate.cpp:665:25
    #1 0x6f1756a51ffe in brw_reg_alloc::assign_regs(bool, bool) /home/user/buildASAN/../src/intel/compiler/brw_reg_allocate.cpp:1263:4
    #2 0x6f1756a52c28 in brw_assign_regs(brw_shader&, bool, bool) /home/user/buildASAN/../src/intel/compiler/brw_reg_allocate.cpp:1339:25
    #3 0x6f1756a5e614 in brw_allocate_registers(brw_shader&, bool) /home/user/buildASAN/../src/intel/compiler/brw_shader.cpp:1114:19
    #4 0x6f175690281d in run_fs(brw_shader&, bool, bool) /home/user/buildASAN/../src/intel/compiler/brw_compile_fs.cpp:1468:7
    #5 0x6f17568fb642 in brw_compile_fs /home/user/buildASAN/../src/intel/compiler/brw_compile_fs.cpp:1729:15
    #6 0x6f175578580d in anv_pipeline_compile_fs /home/user/buildASAN/../src/intel/vulkan/anv_pipeline.c:1586:21
    #7 0x6f175578580d in anv_graphics_pipeline_compile /home/user/buildASAN/../src/intel/vulkan/anv_pipeline.c:2465:10
    #8 0x6f175576f532 in anv_graphics_pipeline_create /home/user/buildASAN/../src/intel/vulkan/anv_pipeline.c:3264:13
    #9 0x6f175576f532 in anv_CreateGraphicsPipelines /home/user/buildASAN/../src/intel/vulkan/anv_pipeline.c:3324:16
    #10 0x59bfebe6bae4 in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:624:9
    #11 0x59bfebc077a7 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:383:5
    #12 0x59bfebb30c09 in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2092:51
    #13 0x59bfebb305fa in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1375:26
    #14 0x59c007e3b71f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:307:9
    #15 0x59c007e2e62c in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:595:9
    #16 0x59c007e356c7 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1674:30
    #17 0x59c007df0880 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1062:33
    #18 0x59c007df0d13 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2000:22
    #19 0x59c007de2e41 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1945:18
    #20 0x59c00764e5a7 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:263:35
    #21 0x59c00762d54b in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:507:22
    #22 0x59c00762c71a in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:163:7
    #23 0x59c007659b0d in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:958:13
    #24 0x59c007668f17 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:731:12
    #25 0x59c007668cff in MakeItSo<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:947:5
    #26 0x59c007668cff in RunImpl<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #27 0x59c007668cff in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:973:12
    #28 0x59c003da3325 in Run base/functional/callback.h:156:12
    #29 0x59c003da3325 in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:806:49
    #30 0x59c003da3325 in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #31 0x59c003da3325 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1060:14
    #32 0x59c003d7dcec in Run base/functional/callback.h:156:12
    #33 0x59c003d7dcec in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:672:29
    #34 0x59c003d7b94c in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:594:3
    #35 0x59c003d7fe73 in Invoke<void (Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:731:12
    #36 0x59c003d7fe73 in MakeItSo<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #37 0x59c003d7fe73 in RunImpl<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1060:14
    #38 0x59c003d7fe73 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #39 0x59bffe4dc746 in Run base/functional/callback.h:156:12
    #40 0x59bffe4dc746 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:209:34
    #41 0x59bffe54da48 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:106:5
    #42 0x59bffe54da48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #43 0x59bffe54c8fc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #44 0x59bffe54e79a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #45 0x59bffe3a5f33 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #46 0x59bffe54f34b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #47 0x59bffe45faaf in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #48 0x59c015b07381 in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:443:14
    #49 0x59bffb1a9553 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:686:14
    #50 0x59bffb1aa4ef in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:790:12
    #51 0x59bffb1acdc5 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1155:10
    #52 0x59bffb1a72f9 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:359:36
    #53 0x59bffb1a781b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:372:10
    #54 0x59bfe87bf957 in ChromeMain chrome/app/chrome_main.cc:222:12
    #55 0x73176e42a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #56 0x73176e42a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #57 0x59bfe86e4029 in _start (/home/user/Downloads/linux-release-1449920/chrome+0xfb87029) (BuildId: ea1a4345215ab1ef)

0x70e761903b30 is located 160 bytes after 2064-byte region [0x70e761903280,0x70e761903a90)
allocated by thread T0 (chrome) here:
    #0 0x59bfe8784234 in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:67:3
    #1 0x6f175619415c in ralloc_size /home/user/buildASAN/../src/util/ralloc.c:118:18
    #2 0x6f175619415c in rzalloc_size /home/user/buildASAN/../src/util/ralloc.c:152:16
    #3 0x6f175691b3dd in brw_compiler_create /home/user/buildASAN/../src/intel/compiler/brw_compiler.c:91:36
    #4 0x6f175575c178 in anv_physical_device_try_create /home/user/buildASAN/../src/intel/vulkan/anv_physical_device.c:2666:23
    #5 0x6f1755feeae4 in enumerate_drm_physical_devices_locked /home/user/buildASAN/../src/vulkan/runtime/vk_instance.c:422:16
    #6 0x6f1755feeae4 in enumerate_physical_devices_locked /home/user/buildASAN/../src/vulkan/runtime/vk_instance.c:453:16
    #7 0x6f1755feeae4 in enumerate_physical_devices /home/user/buildASAN/../src/vulkan/runtime/vk_instance.c:470:16
    #8 0x6f1755fee6dc in vk_common_EnumeratePhysicalDevices /home/user/buildASAN/../src/vulkan/runtime/vk_instance.c:486:22
    #9 0x6f175a745f03 in setup_loader_term_phys_devs third_party/vulkan-loader/src/loader/loader.c:6418:15
    #10 0x6f175a72399e in terminator_EnumeratePhysicalDevices third_party/vulkan-loader/src/loader/loader.c:6752:11
    #11 0x6f175a365ab4  (/lib/x86_64-linux-gnu/libVkLayer_MESA_device_select.so+0x3ab4) (BuildId: ca030a18db9de07434591bb63d5e42d455783298)
    #12 0x6f175a7552b6 in vkEnumeratePhysicalDevices third_party/vulkan-loader/src/loader/trampoline.c:855:11
    #13 0x59bfebf05e8e in dawn::native::vulkan::GatherPhysicalDevices(VkInstance_T*, dawn::native::vulkan::VulkanFunctions const&) third_party/dawn/src/dawn/native/vulkan/VulkanInfo.cpp:146:30
    #14 0x59bfebdcc908 in dawn::native::vulkan::VulkanInstance::Initialize(dawn::native::InstanceBase const*, dawn::native::vulkan::ICD) third_party/dawn/src/dawn/native/vulkan/BackendVk.cpp:425:5
    #15 0x59bfebdcb8f3 in dawn::native::vulkan::VulkanInstance::Create(dawn::native::InstanceBase const*, dawn::native::vulkan::ICD) third_party/dawn/src/dawn/native/vulkan/BackendVk.cpp:341:5
    #16 0x59bfebdd18d4 in operator() third_party/dawn/src/dawn/native/vulkan/BackendVk.cpp:594:25
    #17 0x59bfebdd18d4 in dawn::native::vulkan::Backend::DiscoverPhysicalDevices(dawn::native::UnpackedPtr<dawn::native::RequestAdapterOptions> const&) third_party/dawn/src/dawn/native/vulkan/BackendVk.cpp:593:56
    #18 0x59bfebbcbea3 in dawn::native::InstanceBase::EnumeratePhysicalDevices(dawn::native::UnpackedPtr<dawn::native::RequestAdapterOptions> const&) third_party/dawn/src/dawn/native/Instance.cpp:466:31
    #19 0x59bfebbcb367 in dawn::native::InstanceBase::EnumerateAdapters(dawn::native::RequestAdapterOptions const*) third_party/dawn/src/dawn/native/Instance.cpp:365:39
    #20 0x59c00308fc6c in dawn::native::Instance::EnumerateAdapters(WGPURequestAdapterOptions const*) const third_party/dawn/src/dawn/native/DawnNative.cpp:164:51
    #21 0x59c00308ff53 in dawn::native::Instance::EnumerateAdapters(wgpu::RequestAdapterOptions const*) const third_party/dawn/src/dawn/native/DawnNative.cpp:171:12
    #22 0x59c007de8821 in CreatePreferredAdapter gpu/command_buffer/service/webgpu_decoder_impl.cc:1867:26
    #23 0x59c007de8821 in RequestAdapterImpl<WGPURequestAdapterCallbackInfo> gpu/command_buffer/service/webgpu_decoder_impl.cc:1352:27
    #24 0x59c007de8821 in operator()<WGPUInstanceImpl *, const WGPURequestAdapterOptions *, WGPURequestAdapterCallbackInfo> gpu/command_buffer/service/webgpu_decoder_impl.cc:1177:28
    #25 0x59c007de8821 in _ZZN3gpu6webgpu12_GLOBAL__N_117WebGPUDecoderImplC1EPNS_13DecoderClientEPNS_24CommandBufferServiceBaseEPNS_18SharedImageManagerEPNS_13MemoryTrackerEPNS_5gles29OutputterERKNS_14GpuPreferencesE13scoped_refptrINS_18SharedContextStateEENSt4__Cr10unique_ptrINS0_20DawnCachingInterfaceENSK_14default_deleteISM_EEEEPNS_20IsolationKeyProviderEEN3$_08__invokeIJP16WGPUInstanceImplPK25WGPURequestAdapterOptions30WGPURequestAdapterCallbackInfoEEEDaDpT_ gpu/command_buffer/service/webgpu_decoder_impl.cc:1175:39
    #26 0x59c007e45008 in dawn::wire::server::Server::DoInstanceRequestAdapter(dawn::wire::server::Known<WGPUInstanceImpl*>, dawn::wire::ObjectHandle, WGPUFuture, dawn::wire::ObjectHandle, WGPURequestAdapterOptions const*) third_party/dawn/src/dawn/wire/server/ServerInstance.cpp:51:5
    #27 0x59c007e30717 in dawn::wire::server::Server::HandleInstanceRequestAdapter(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:803:9
    #28 0x59c007e34803 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1731:30
    #29 0x59c007df0880 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1062:33
    #30 0x59c007df0d13 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2000:22
    #31 0x59c007de2e41 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1945:18
    #32 0x59c00764e5a7 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:263:35
    #33 0x59c00762d54b in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:507:22
    #34 0x59c00762c71a in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:163:7
    #35 0x59c007659b0d in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:958:13
    #36 0x59c007668f17 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:731:12

SUMMARY: AddressSanitizer: heap-buffer-overflow /home/user/buildASAN/../src/intel/compiler/brw_reg_allocate.cpp:665:25 in brw_reg_alloc::build_interference_graph(bool)
Shadow bytes around the buggy address:
  0x70e761903880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x70e761903900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x70e761903980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x70e761903a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x70e761903a80: 00 00 fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x70e761903b00: fa fa fa fa fa fa[fa]fa fa fa fa fa fa fa fa fa
  0x70e761903b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x70e761903c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x70e761903c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70e761903d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70e761903d80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==13643==ADDITIONAL INFO


==13643==Note: Please include this section with the ASan report.
Task trace:
    #0 0x59c003d7be99 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:610:27
    #1 0x59c003d7be99 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:610:27
    #2 0x59c003d77a7d in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*) gpu/command_buffer/service/scheduler.cc:412:29


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --ozone-platform=wayland --use-angle=vulkan --crashpad-handler-pid=13609 --enable-crash-reporter=, --user-data-dir=/tmp/deleteme --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAoAQAEAAAAAAAAAAAAAAAAAADAAAIAAAACAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,16493178375242726520,12357933776801490915,262144 --field-trial-handle=3,i,7721872578303244053,14662520769333236388,262144 --enable-features=Vulkan --disable-features=EyeDropper --variations-seed-version`


==13643==END OF ADDITIONAL INFO
==13643==ABORTING

```

## Attachments

- gfxrecon_capture_20250524T090556.gfxr (application/octet-stream, 12.6 KB)
- build_interference_graph.html (text/html, 3.2 KB)

## Timeline

### a7...@gmail.com (2025-05-24)

Upstream report: <https://gitlab.freedesktop.org/mesa/mesa/-/issues/13239>

### pa...@chromium.org (2025-05-26)

[cwallez@chromium.org](mailto:cwallez@chromium.org) can you PTAL? It's a bug in Mesa, but setting critical severity since it's HBO in the GPU process. [cwallez@chromium.org](mailto:cwallez@chromium.org), maybe we can also have a workaround in Chrome not to emit the problematic shader(s) ? Setting impact as extended stable.

### pa...@chromium.org (2025-05-26)

Note that the bug report for Mesa doesn't work for me. Reporter, is there an issue with the report?

### ch...@google.com (2025-05-26)

Setting milestone because of s0/s1 severity.

### a7...@gmail.com (2025-05-26)

P0/S0 is probably to high as ChromeOS GPU process is sandboxed and Linux doesn't enable WebGPU by default.  

[pa...@chromium.org](mailto:pa...@chromium.org) Are you reproducing with a full Chrome or with the gfxr file? Also, do you have an Intel GPU? It might be specific to the intel-backend of Mesa.

### ds...@chromium.org (2025-05-26)

The shader itself is pretty simple, we'll need to know the root cause from the Mesa people and an idea of what needs to be worked around.

### pr...@google.com (2025-05-28)

Matt, could you take a look at the shader in <https://gitlab.freedesktop.org/mesa/mesa/-/issues/13239> and respond to [comment#7](https://issues.chromium.org/issues/419939693#comment7)?

### ms...@google.com (2025-05-28)

Sure, will do.

### ch...@google.com (2025-06-12)

msturner: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ms...@google.com (2025-06-12)

I investigated a bit (I was hoping Intel would fix this without me). This is very similar to issue <https://gitlab.freedesktop.org/mesa/mesa/-/issues/12324> / [b/384531062](https://issues.chromium.org/issues/384531062). I've noted this on the upstream issue and CC'd the author of the fix for the older issue.

### ch...@google.com (2025-07-10)

msturner: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ms...@google.com (2025-07-17)

Upstream MR from Intel that should fix this: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/36202>

### ms...@google.com (2025-07-18)

MR landed upstream. Doesn't cherry pick cleanly. I'm investigating.

### ms...@google.com (2025-07-18)

CLs uploaded:

- [crrev/c/6771097](https://crrev.com/c/6771097)
- [crrev/c/6771098](https://crrev.com/c/6771098)

Still need to deploy to a device and confirm that the backported patches fix the reported issue.

### ms...@google.com (2025-07-18)

> Still need to deploy to a device and confirm that the backported patches fix the reported issue.

Yep, build\_interference\_graph.html doesn't crash with the backported patches.

### dx...@google.com (2025-07-18)

Project: chromiumos/third\_party/mesa  

Branch:  chromeos-iris  

Author:  Ian Romanick [ian.d.romanick@intel.com](mailto:ian.d.romanick@intel.com)  

Link:    <https://chromium-review.googlesource.com/6771097>

BACKPORT: UPSTREAM: brw/reg\_allocate: Don't access out of bounds in non-debug builds

---


Expand for full commit details
```
     
    In debug builds, the assertion should be preferred as it will highlight 
    the actual problem. In non-debug builds, it is possible to fail register 
    allocation more gracefully. If the problem only occurs in, for example, 
    a SIMD32 version of a shader, the application may even continue to 
    function. 
     
    Closes: #13239 
    Reviewed-by: Caio Oliveira <caio.oliveira@intel.com> 
    Reviewed-by: Matt Turner <mattst88@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/36202> 
     
    (cherry picked from commit f6da6399d7d46f86890b1a5f37d85df1f5487a01 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    Conflicts: 
       src/intel/compiler/brw_fs_reg_allocate.cpp 
     
    BUG=b:419939693 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I68411f74e6a63ea2bde29353951c06b76488b202 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6771097 
    Tested-by: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Commit-Queue: Matt Turner <msturner@google.com> 
    Reviewed-by: Prahlad Kilambi <prahladk@google.com>

```

---

Files:

- M `src/intel/compiler/brw_fs_reg_allocate.cpp`

---

Hash: [83d5cd7f13e1a88926ff013b76fbb07c5e317c9e](http://crrev.com/83d5cd7f13e1a88926ff013b76fbb07c5e317c9e)  

Date: Wed Jul 16 17:11:51 2025


---

### dx...@google.com (2025-07-18)

Project: chromiumos/third\_party/mesa  

Branch:  chromeos-iris  

Author:  Ian Romanick [ian.d.romanick@intel.com](mailto:ian.d.romanick@intel.com)  

Link:    <https://chromium-review.googlesource.com/6771098>

BACKPORT: UPSTREAM: brw: Split virtual GRFs again at the end of optimizations

---


Expand for full commit details
```
     
    Logical sends and load_payload can have large VGRFs that cannot be 
    split. Once all of the lowering passes and optimization passes that 
    might eliminate any of those instructions have completed, try to split 
    larger VGRFs one last time. 
     
    Register allocation can only handle VGRFs up to a certain size, so this 
    is the last opportunity to prevent later failures due to VGRFs that are 
    too large. 
     
    Closes: #13239 
     
    shader-db: 
     
    Lunar Lake, Meteor Lake, DG2, and Tiger Lake had similar results. (Lunar Lake shown) 
    total instructions in shared programs: 17114494 -> 17114496 (<.01%) 
    instructions in affected programs: 2790 -> 2792 (0.07%) 
    helped: 2 / HURT: 4 
     
    total cycles in shared programs: 886617364 -> 886315282 (-0.03%) 
    cycles in affected programs: 4067540 -> 3765458 (-7.43%) 
    helped: 48 / HURT: 9 
     
    Ice Lake and Skylake had similar restuls. (Ice Lake shown) 
    total instructions in shared programs: 20799801 -> 20799691 (<.01%) 
    instructions in affected programs: 1210 -> 1100 (-9.09%) 
    helped: 1 / HURT: 0 
     
    total cycles in shared programs: 865495386 -> 865498990 (<.01%) 
    cycles in affected programs: 60132 -> 63736 (5.99%) 
    helped: 2 / HURT: 1 
     
    total spills in shared programs: 3987 -> 3981 (-0.15%) 
    spills in affected programs: 24 -> 18 (-25.00%) 
    helped: 1 / HURT: 0 
     
    total fills in shared programs: 3535 -> 3519 (-0.45%) 
    fills in affected programs: 36 -> 20 (-44.44%) 
    helped: 1 / HURT: 0 
     
    fossil-db: 
     
    All Intel platforms had similar results. (Lunar Lake shown) 
    Totals: 
    Instrs: 208647246 -> 208646499 (-0.00%); split: -0.00%, +0.00% 
    Cycle count: 31257819536 -> 31263957016 (+0.02%); split: -0.02%, +0.04% 
    Max live registers: 66160877 -> 66155728 (-0.01%) 
     
    Totals from 34703 (4.91% of 707053) affected shaders: 
    Instrs: 13766639 -> 13765892 (-0.01%); split: -0.02%, +0.01% 
    Cycle count: 3693572086 -> 3699709566 (+0.17%); split: -0.15%, +0.32% 
    Max live registers: 4843852 -> 4838703 (-0.11%) 
     
    Reviewed-by: Caio Oliveira <caio.oliveira@intel.com> 
    Reviewed-by: Matt Turner <mattst88@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/36202> 
     
    (cherry picked from commit 2594fcadd436f991d99f73ff0e2893298017a69c 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    Conflicts: 
       src/intel/compiler/brw_opt.cpp 
     
    BUG=b:419939693 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I6115e5b4f0f9f1d7640ebb8bd3f3155586bd24b1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6771098 
    Commit-Queue: Matt Turner <msturner@google.com> 
    Tested-by: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Reviewed-by: Prahlad Kilambi <prahladk@google.com>

```

---

Files:

- M `src/intel/compiler/brw_fs_opt.cpp`

---

Hash: [91b5b5a92e030f6b722dc0d27206893fe631df07](http://crrev.com/91b5b5a92e030f6b722dc0d27206893fe631df07)  

Date: Wed Jul 16 17:14:45 2025


---

### pe...@google.com (2025-07-21)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2025-07-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in a highly privileged process 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-07-24)

Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2025-09-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2025-09-25)

1.

For 132: <https://crrev.com/c/6816957>, <https://crrev.com/c/6816958/1>

For 138: <https://crrev.com/c/6954345>, <https://crrev.com/c/6954346/1>

2. Low, no conflicts
3. 140, 141
4. Yes

### dx...@google.com (2025-10-09)

Project: chromiumos/third\_party/mesa  

Branch:  release-R138-16295.B-chromeos-iris  

Author:  Ian Romanick [ian.d.romanick@intel.com](mailto:ian.d.romanick@intel.com)  

Link:    <https://chromium-review.googlesource.com/6954345>

[M138-LTS] BACKPORT: UPSTREAM: brw/reg\_allocate: Don't access out of bounds in non-debug builds

---


Expand for full commit details
```
     
    In debug builds, the assertion should be preferred as it will highlight 
    the actual problem. In non-debug builds, it is possible to fail register 
    allocation more gracefully. If the problem only occurs in, for example, 
    a SIMD32 version of a shader, the application may even continue to 
    function. 
     
    Closes: #13239 
    Reviewed-by: Caio Oliveira <caio.oliveira@intel.com> 
    Reviewed-by: Matt Turner <mattst88@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/36202> 
     
    (cherry picked from commit f6da6399d7d46f86890b1a5f37d85df1f5487a01 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    Conflicts: 
       src/intel/compiler/brw_fs_reg_allocate.cpp 
     
    BUG=b:419939693 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I68411f74e6a63ea2bde29353951c06b76488b202 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6771097 
    Tested-by: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Commit-Queue: Matt Turner <msturner@google.com> 
    (cherry picked from commit 83d5cd7f13e1a88926ff013b76fbb07c5e317c9e) 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6954345 
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
    Tested-by: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
    Owners-Override: Achuith Bhandarkar <achuith@chromium.org> 
    Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>

```

---

Files:

- M `src/intel/compiler/brw_fs_reg_allocate.cpp`

---

Hash: [0617f1b855c38d4c693d2b3bbe398f008a2667d0](https://chromiumdash.appspot.com/commit/0617f1b855c38d4c693d2b3bbe398f008a2667d0)  

Date: Wed Jul 16 17:11:51 2025


---

### dx...@google.com (2025-10-09)

Project: chromiumos/third\_party/mesa  

Branch:  release-R138-16295.B-chromeos-iris  

Author:  Ian Romanick [ian.d.romanick@intel.com](mailto:ian.d.romanick@intel.com)  

Link:    <https://chromium-review.googlesource.com/6954346>

[M138-LTS] BACKPORT: UPSTREAM: brw: Split virtual GRFs again at the end of optimizations

---


Expand for full commit details
```
     
    Logical sends and load_payload can have large VGRFs that cannot be 
    split. Once all of the lowering passes and optimization passes that 
    might eliminate any of those instructions have completed, try to split 
    larger VGRFs one last time. 
     
    Register allocation can only handle VGRFs up to a certain size, so this 
    is the last opportunity to prevent later failures due to VGRFs that are 
    too large. 
     
    Closes: #13239 
     
    shader-db: 
     
    Lunar Lake, Meteor Lake, DG2, and Tiger Lake had similar results. (Lunar Lake shown) 
    total instructions in shared programs: 17114494 -> 17114496 (<.01%) 
    instructions in affected programs: 2790 -> 2792 (0.07%) 
    helped: 2 / HURT: 4 
     
    total cycles in shared programs: 886617364 -> 886315282 (-0.03%) 
    cycles in affected programs: 4067540 -> 3765458 (-7.43%) 
    helped: 48 / HURT: 9 
     
    Ice Lake and Skylake had similar restuls. (Ice Lake shown) 
    total instructions in shared programs: 20799801 -> 20799691 (<.01%) 
    instructions in affected programs: 1210 -> 1100 (-9.09%) 
    helped: 1 / HURT: 0 
     
    total cycles in shared programs: 865495386 -> 865498990 (<.01%) 
    cycles in affected programs: 60132 -> 63736 (5.99%) 
    helped: 2 / HURT: 1 
     
    total spills in shared programs: 3987 -> 3981 (-0.15%) 
    spills in affected programs: 24 -> 18 (-25.00%) 
    helped: 1 / HURT: 0 
     
    total fills in shared programs: 3535 -> 3519 (-0.45%) 
    fills in affected programs: 36 -> 20 (-44.44%) 
    helped: 1 / HURT: 0 
     
    fossil-db: 
     
    All Intel platforms had similar results. (Lunar Lake shown) 
    Totals: 
    Instrs: 208647246 -> 208646499 (-0.00%); split: -0.00%, +0.00% 
    Cycle count: 31257819536 -> 31263957016 (+0.02%); split: -0.02%, +0.04% 
    Max live registers: 66160877 -> 66155728 (-0.01%) 
     
    Totals from 34703 (4.91% of 707053) affected shaders: 
    Instrs: 13766639 -> 13765892 (-0.01%); split: -0.02%, +0.01% 
    Cycle count: 3693572086 -> 3699709566 (+0.17%); split: -0.15%, +0.32% 
    Max live registers: 4843852 -> 4838703 (-0.11%) 
     
    Reviewed-by: Caio Oliveira <caio.oliveira@intel.com> 
    Reviewed-by: Matt Turner <mattst88@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/36202> 
     
    (cherry picked from commit 2594fcadd436f991d99f73ff0e2893298017a69c 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    Conflicts: 
       src/intel/compiler/brw_opt.cpp 
     
    BUG=b:419939693 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I6115e5b4f0f9f1d7640ebb8bd3f3155586bd24b1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6771098 
    Commit-Queue: Matt Turner <msturner@google.com> 
    Tested-by: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    (cherry picked from commit 91b5b5a92e030f6b722dc0d27206893fe631df07) 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6954346 
    Reviewed-by: Achuith Bhandarkar <achuith@chromium.org> 
    Owners-Override: Achuith Bhandarkar <achuith@chromium.org> 
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
    Tested-by: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>

```

---

Files:

- M `src/intel/compiler/brw_fs_opt.cpp`

---

Hash: [cf76e8b603c740c9016412c49fe5229c53e4edcc](https://chromiumdash.appspot.com/commit/cf76e8b603c740c9016412c49fe5229c53e4edcc)  

Date: Wed Jul 16 17:14:45 2025


---

### ch...@google.com (2025-10-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a highly privileged process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/419939693)*
