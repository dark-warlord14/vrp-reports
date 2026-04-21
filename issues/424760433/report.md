# GPU process crash via WebGPU shader - heap-use-after-free in Mesa brw_live_variables::setup_one_read

| Field | Value |
|-------|-------|
| **Issue ID** | [424760433](https://issues.chromium.org/issues/424760433) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | a7...@gmail.com |
| **Assignee** | pe...@google.com |
| **Created** | 2025-06-13 |
| **Bounty** | $11,000.00 |

## Description

#### VULNERABILITY DETAILS

This report is about a heap-use-after-free in the Mesa shader compiler, reachable via WebGPU shaders emitted by dawn/tint. I will also upload this report upstream, i.e., the Mesa project, and post the link below. The offending shader looks as follows:

```
enable subgroups;

@group(0) @binding(0)
var<storage, read_write> g2: vec4<f32>;

@compute @workgroup_size(1)
fn main(@builtin(subgroup_invocation_id) l: u32) {
    var h: array<vec4<f32>, 4>;
    var i = 111008u;
    let r = subgroupShuffle(vec2<f32>(f32(l)), i);
    g2 = h[i32(r.y)];
}

```

While I don't understand the root cause it seems to be related to the subgroupShuffle operation; the fuzzer crashes Mesa all over the place with samples containing this operation. I suspect the issue is an Intel-specific code-path as the fuzzer is not finding similar crashes when using the ACO backend (AMD GPU).

#### VERSION

Chrome Version: Version 139.0.7237.0 (Developer Build) (64-bit) (ASAN build)   

Operating System: Ubuntu 25.05   

Mesa: mesa-25.1.3 commit ba95e69

#### REPRODUCTION

There are two means of reproduction, standalone and via Chrome. In either case you'll need an ASAN build of Mesa:

1. `git clone https://chromium.googlesource.com/chromiumos/third_party/mesa; cd mesa; checkout ba95e69`
2. `mkdir buildASAN; cd buildASAN`
3. `LLVM_CONFIG=/usr/bin/llvm-config-18 CC=clang-18 CXX=clang++-18 meson .. ; meson configure -Db_sanitize=address -Db_lundef=false -Db_ndebug=true` configures mesa for ASAN
4. `ASAN_OPTIONS=detect_leaks=0 LLVM_CONFIG=/usr/bin/llvm-config-18 ninja src/intel/vulkan/libvulkan_intel.so build libvulkan_intel.so`
5. `ninja src/intel/vulkan/intel_icd.x86_64.json`
6. inside the json from step 5, update the path s.t. it points to the absolute path of libvulkan\_intel.so from step 4

##### Standalone

Standalone reproduction happens via gfxrecon-replay. The attached .gfxr allows to reproduce outside of chrome as follows: `LD_PRELOAD=/usr/lib/llvm-18/lib/clang/18/lib/linux/libclang_rt.asan-x86_64.so VK_DRIVER_FILES=~/src/intel/vulkan/intel_icd.x86_64.json ASAN_OPTIONS=detect_leaks=0,abort_on_error=1 ~/gfxreconstruct/build/linux/x64/output/bin/gfxrecon-replay gfxrecon_capture_20250613T172703.gfxr`

##### Chrome

Reproducing the issue in Chrome requires an ASAN build of Mesa as well as an ASAN build of Chromium. Note that the issue seems to be in an Intel-specific code path + the device needs to support the subgroups feature. The crash in Chrome has been observed using a Intel BMG G21 device. Opening the attached html file should trigger the UAF in the Chrome GPU process.
Start chrome and run it with the ASAN version of mesa (adapt paths as needed): `ASAN_OPTIONS=external_symbolizer_path=/usr/lib/llvm-18/bin/llvm-symbolizer VK_DRIVER_FILES=/path/to/src/intel/vulkan/intel_icd.x86_64.json ./chrome --user-data-dir=/tmp/deleteme --use-angle=vulkan --enable-features=Vulkan --disable-gpu-watchdog --no-sandbox --enable-unsafe-webgpu` and open the attached html:

```
==9181==ERROR: AddressSanitizer: heap-use-after-free on address 0x7b23ede84ff0 at pc 0x7953d6538b37 bp 0x7ffe79fe2520 sp 0x7ffe79fe2518
READ of size 8 at 0x7b23ede84ff0 thread T0 (chrome)
    #0 0x7953d6538b36 in brw_live_variables::setup_one_read(brw_live_variables::block_data*, int, brw_reg const&) /home/user/mesa/buildASAN/../src/intel/compiler/brw_analysis_liveness.cpp:60:28
    #1 0x7953d6538b36 in brw_live_variables::setup_def_use() /home/user/mesa/buildASAN/../src/intel/compiler/brw_analysis_liveness.cpp:120:16
    #2 0x7953d653ad15 in brw_live_variables::brw_live_variables(brw_shader const*) /home/user/mesa/buildASAN/../src/intel/compiler/brw_analysis_liveness.cpp:288:4
    #3 0x7953d66c6a90 in brw_analysis<brw_live_variables, brw_shader>::require() /home/user/mesa/buildASAN/../src/intel/compiler/brw_analysis.h:146:18
    #4 0x7953d66c6a90 in brw_opt_dead_code_eliminate(brw_shader&) /home/user/mesa/buildASAN/../src/intel/compiler/brw_opt_dead_code_eliminate.cpp:104:58
    #5 0x7953d666521c in brw_optimize(brw_shader&) /home/user/mesa/buildASAN/../src/intel/compiler/brw_opt.cpp:80:7
    #6 0x7953d647388c in run_cs(brw_shader&, bool) /home/user/mesa/buildASAN/../src/intel/compiler/brw_compile_cs.cpp:77:4
    #7 0x7953d647388c in brw_compile_cs /home/user/mesa/buildASAN/../src/intel/compiler/brw_compile_cs.cpp:196:11
    #8 0x7953d54bf59d in anv_pipeline_compile_cs /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2657:20
    #9 0x7953d54bf59d in anv_compute_pipeline_create /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2761:13
    #10 0x7953d54bf59d in anv_CreateComputePipelines /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2794:22
    #11 0x618288a1392f in dawn::native::vulkan::ComputePipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/ComputePipelineVk.cpp:124:5
    #12 0x6182887ebdf7 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:383:5
    #13 0x618288704278 in dawn::native::DeviceBase::CreateComputePipeline(dawn::native::ComputePipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1952:52
    #14 0x618288703c78 in dawn::native::DeviceBase::APICreateComputePipeline(dawn::native::ComputePipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1270:26
    #15 0x6182a49489af in dawn::wire::server::Server::DoDeviceCreateComputePipeline(WGPUDeviceImpl*, WGPUComputePipelineDescriptor const*, WGPUComputePipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:243:9
    #16 0x6182a493825c in dawn::wire::server::Server::HandleDeviceCreateComputePipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:466:9
    #17 0x6182a49433c4 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1644:30
    #18 0x6182a48fd900 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1061:33
    #19 0x6182a48fdd93 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2002:22
    #20 0x6182a48effd1 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1947:18
    #21 0x6182a413d377 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:265:35
    #22 0x6182a411cbb7 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:506:22
    #23 0x6182a411bd8a in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:162:7
    #24 0x6182a41493ad in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:886:13
    #25 0x6182a4158727 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:731:12
    #26 0x6182a415850f in MakeItSo<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:947:5
    #27 0x6182a415850f in RunImpl<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #28 0x6182a415850f in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:973:12
    #29 0x6182a2a80545 in Run base/functional/callback.h:156:12
    #30 0x6182a2a80545 in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:806:49
    #31 0x6182a2a80545 in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #32 0x6182a2a80545 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1060:14
    #33 0x6182a2a5adec in Run base/functional/callback.h:156:12
    #34 0x6182a2a5adec in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:672:29
    #35 0x6182a2a58a4c in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:594:3
    #36 0x6182a2a5cf73 in Invoke<void (Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:731:12
    #37 0x6182a2a5cf73 in MakeItSo<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #38 0x6182a2a5cf73 in RunImpl<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1060:14
    #39 0x6182a2a5cf73 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #40 0x61829b75cf66 in Run base/functional/callback.h:156:12
    #41 0x61829b75cf66 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:207:34
    #42 0x61829b7cfa57 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:104:5
    #43 0x61829b7cfa57 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #44 0x61829b7ce93c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #45 0x61829b7d054a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #46 0x61829b623d03 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #47 0x61829b7d1104 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #48 0x61829b6dc06f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #49 0x6182a5e22571 in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:454:14
    #50 0x6182982fffac in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:702:14
    #51 0x618298300f7c in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:804:12
    #52 0x618298303931 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1198:10
    #53 0x6182982fdce9 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:362:36
    #54 0x6182982fe20b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:375:10
    #55 0x6182855e4f27 in ChromeMain chrome/app/chrome_main.cc:222:12
    #56 0x7d53ef62a337 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #57 0x7d53ef62a3fa in __libc_start_main csu/../csu/libc-start.c:360:3
    #58 0x618285509029 in _start (/home/user/Downloads/linux-1473520/chrome+0xfbbf029) (BuildId: 836701a81112c94a)

0x7b23ede84ff0 is located 368 bytes inside of 2128-byte region [0x7b23ede84e80,0x7b23ede856d0)
freed by thread T0 (chrome) here:
    #0 0x6182855aa396 in free /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:51:3
    #1 0x7953d5d5a4d0 in unsafe_free /home/user/mesa/buildASAN/../src/util/ralloc.c:319:7
    #2 0x7953d65735a9 in nir_opt_combine_stores /home/user/mesa/buildASAN/../src/compiler/nir/nir_opt_combine_stores.c:425:4
    #3 0x7953d65411ae in brw_nir_optimize /home/user/mesa/buildASAN/../src/intel/compiler/brw_nir.c:863:7
    #4 0x7953d65437de in brw_postprocess_nir /home/user/mesa/buildASAN/../src/intel/compiler/brw_nir.c:1823:4
    #5 0x7953d6473633 in brw_compile_cs /home/user/mesa/buildASAN/../src/intel/compiler/brw_compile_cs.cpp:175:7
    #6 0x7953d54bf59d in anv_pipeline_compile_cs /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2657:20
    #7 0x7953d54bf59d in anv_compute_pipeline_create /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2761:13
    #8 0x7953d54bf59d in anv_CreateComputePipelines /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2794:22
    #9 0x618288a1392f in dawn::native::vulkan::ComputePipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/ComputePipelineVk.cpp:124:5
    #10 0x6182887ebdf7 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:383:5
    #11 0x618288704278 in dawn::native::DeviceBase::CreateComputePipeline(dawn::native::ComputePipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1952:52
    #12 0x618288703c78 in dawn::native::DeviceBase::APICreateComputePipeline(dawn::native::ComputePipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1270:26
    #13 0x6182a49489af in dawn::wire::server::Server::DoDeviceCreateComputePipeline(WGPUDeviceImpl*, WGPUComputePipelineDescriptor const*, WGPUComputePipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:243:9
    #14 0x6182a493825c in dawn::wire::server::Server::HandleDeviceCreateComputePipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:466:9
    #15 0x6182a49433c4 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1644:30
    #16 0x6182a48fd900 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1061:33
    #17 0x6182a48fdd93 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2002:22
    #18 0x6182a48effd1 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1947:18
    #19 0x6182a413d377 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:265:35
    #20 0x6182a411cbb7 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:506:22
    #21 0x6182a411bd8a in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:162:7
    #22 0x6182a41493ad in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:886:13
    #23 0x6182a4158727 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:731:12
    #24 0x6182a415850f in MakeItSo<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:947:5
    #25 0x6182a415850f in RunImpl<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #26 0x6182a415850f in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:973:12
    #27 0x6182a2a80545 in Run base/functional/callback.h:156:12
    #28 0x6182a2a80545 in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:806:49
    #29 0x6182a2a80545 in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #30 0x6182a2a80545 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1060:14
    #31 0x6182a2a5adec in Run base/functional/callback.h:156:12
    #32 0x6182a2a5adec in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:672:29
    #33 0x6182a2a58a4c in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:594:3
    #34 0x6182a2a5cf73 in Invoke<void (Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:731:12
    #35 0x6182a2a5cf73 in MakeItSo<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #36 0x6182a2a5cf73 in RunImpl<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1060:14
    #37 0x6182a2a5cf73 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #38 0x61829b75cf66 in Run base/functional/callback.h:156:12
    #39 0x61829b75cf66 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:207:34
    #40 0x61829b7cfa57 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:104:5
    #41 0x61829b7cfa57 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #42 0x61829b7ce93c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40

previously allocated by thread T0 (chrome) here:
    #0 0x6182855aa634 in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:67:3
    #1 0x7953d5d5e52c in ralloc_size /home/user/mesa/buildASAN/../src/util/ralloc.c:118:18
    #2 0x7953d5d5e52c in linear_context_with_opts /home/user/mesa/buildASAN/../src/util/ralloc.c:1134:10
    #3 0x7953d5d5e52c in linear_context /home/user/mesa/buildASAN/../src/util/ralloc.c:1113:11
    #4 0x7953d6570e0b in nir_opt_combine_stores /home/user/mesa/buildASAN/../src/compiler/nir/nir_opt_combine_stores.c:413:18
    #5 0x7953d65411ae in brw_nir_optimize /home/user/mesa/buildASAN/../src/intel/compiler/brw_nir.c:863:7
    #6 0x7953d65437de in brw_postprocess_nir /home/user/mesa/buildASAN/../src/intel/compiler/brw_nir.c:1823:4
    #7 0x7953d6473633 in brw_compile_cs /home/user/mesa/buildASAN/../src/intel/compiler/brw_compile_cs.cpp:175:7
    #8 0x7953d54bf59d in anv_pipeline_compile_cs /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2657:20
    #9 0x7953d54bf59d in anv_compute_pipeline_create /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2761:13
    #10 0x7953d54bf59d in anv_CreateComputePipelines /home/user/mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2794:22
    #11 0x618288a1392f in dawn::native::vulkan::ComputePipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/ComputePipelineVk.cpp:124:5
    #12 0x6182887ebdf7 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:383:5
    #13 0x618288704278 in dawn::native::DeviceBase::CreateComputePipeline(dawn::native::ComputePipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1952:52
    #14 0x618288703c78 in dawn::native::DeviceBase::APICreateComputePipeline(dawn::native::ComputePipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1270:26
    #15 0x6182a49489af in dawn::wire::server::Server::DoDeviceCreateComputePipeline(WGPUDeviceImpl*, WGPUComputePipelineDescriptor const*, WGPUComputePipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:243:9
    #16 0x6182a493825c in dawn::wire::server::Server::HandleDeviceCreateComputePipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:466:9
    #17 0x6182a49433c4 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1644:30
    #18 0x6182a48fd900 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1061:33
    #19 0x6182a48fdd93 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2002:22
    #20 0x6182a48effd1 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1947:18
    #21 0x6182a413d377 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:265:35
    #22 0x6182a411cbb7 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:506:22
    #23 0x6182a411bd8a in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:162:7
    #24 0x6182a41493ad in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:886:13
    #25 0x6182a4158727 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:731:12
    #26 0x6182a415850f in MakeItSo<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:947:5
    #27 0x6182a415850f in RunImpl<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #28 0x6182a415850f in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:973:12
    #29 0x6182a2a80545 in Run base/functional/callback.h:156:12
    #30 0x6182a2a80545 in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:806:49
    #31 0x6182a2a80545 in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #32 0x6182a2a80545 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1060:14
    #33 0x6182a2a5adec in Run base/functional/callback.h:156:12
    #34 0x6182a2a5adec in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:672:29
    #35 0x6182a2a58a4c in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:594:3
    #36 0x6182a2a5cf73 in Invoke<void (Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:731:12
    #37 0x6182a2a5cf73 in MakeItSo<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #38 0x6182a2a5cf73 in RunImpl<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1060:14
    #39 0x6182a2a5cf73 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #40 0x61829b75cf66 in Run base/functional/callback.h:156:12
    #41 0x61829b75cf66 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:207:34
    #42 0x61829b7cfa57 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:104:5
    #43 0x61829b7cfa57 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #44 0x61829b7ce93c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40

SUMMARY: AddressSanitizer: heap-use-after-free /home/user/mesa/buildASAN/../src/intel/compiler/brw_analysis_liveness.cpp:60:28 in brw_live_variables::setup_one_read(brw_live_variables::block_data*, int, brw_reg const&)
Shadow bytes around the buggy address:
  0x7b23ede84d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b23ede84d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7b23ede84e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x7b23ede84e80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7b23ede84f00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x7b23ede84f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd
  0x7b23ede85000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7b23ede85080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7b23ede85100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7b23ede85180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7b23ede85200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==9181==ADDITIONAL INFO

==9181==Note: Please include this section with the ASan report.
Task trace:
    #0 0x6182a2a54b7d in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*) gpu/command_buffer/service/scheduler.cc:412:29


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --ozone-platform=wayland --use-angle=vulkan --crashpad-handler-pid=9141 --enable-crash-reporter=, --user-data-dir=/tmp/deleteme --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAoAQAIAAAAAAAAAAAAAMAAAgAAAAIAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,264296500998255206,10634279736296973902,262144 --field-trial-handle=3,i,18144936422692879596,12846175919730523972,262144 --enable-features=Vulkan --disable-features=EyeDropper --variations-seed-version`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==9181==END OF ADDITIONAL INFO
==9181==ABORTING

```

## Attachments

- subgroup.html (text/html, 2.8 KB)
- gfxrecon_capture_20250613T172703.gfxr (application/octet-stream, 10.5 KB)
- Dockerfile (application/octet-stream, 2.0 KB)

## Timeline

### a7...@gmail.com (2025-06-13)

Upstream report <https://gitlab.freedesktop.org/mesa/mesa/-/issues/13351>

### dr...@chromium.org (2025-06-13)

[security triage] Thanks for reporting upstream! I'm still fighting a little to get a Mesa build setup working, so adding provisional security labels in the meantime.

+kbr@ and +syoussefi@ to see if there's a workaround to reject these shaders and +msturner@ for the underlying Mesa fix.

### dr...@chromium.org (2025-06-13)

Unfortunately even after I build Mesa I'm getting some failures to initialize the GPU driver that I suspect is a problem with my setup. Reporter and GPU folks - any input you have about when this bug was introduced would be very helpful.

### ch...@google.com (2025-06-14)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### a7...@gmail.com (2025-06-14)

Are you attempting to reproduce the issue standalone or via Chrome? And how does this failure to initialize the GPU driver manifest? Regarding your question when this bug was introduced: I'll attempt to bisect Mesa.

### a7...@gmail.com (2025-06-14)

Bisecting identifies the first bad commit as 5336cbff:

```
commit 5336cbff3bd0ac73cb03915bb2dad102f15d58a0 (HEAD)
Author: Ian Romanick <ian.d.romanick@intel.com>
Date:   Wed Jun 7 10:57:47 2023 -0700

    intel/fs: Constant propagate into SHADER_OPCODE_SHUFFLE

```

I still would like to solve the problems around reproducing the issue, in particular because there are some more Mesa issues lined up.

### a7...@gmail.com (2025-06-15)

[dr...@chromium.org](mailto:dr...@chromium.org): Since there are problems with reproducing the issue, attached is a Dockerfile that allows for standalone reproduction within a container:

1. Place the `Dockerfile` and `gfxrecon_capture_20250613T172703.gfxr` in new directory
2. Inside this directory: `docker build -t mesarepo .`
3. Once built, switch into the container: `docker run -it mesarepo /bin/bash`
4. Inside the container, run: `LD_PRELOAD="/usr/lib/llvm-20/lib/clang/20/lib/linux/libclang_rt.asan-x86_64.so /mesa/buildASAN/src/intel/tools/libintel_noop_drm_shim.so" VK_DRIVER_FILES=/mesa/buildASAN/src/intel/vulkan/intel_icd.x86_64.json /gfxreconstruct/build/tools/replay/gfxrecon-replay /gfxrecon_capture_20250613T172703.gfxr`

### dr...@chromium.org (2025-06-16)

Reporter - at startup I get some log messages:

```
[3894101:3894101:0613/145622.320565:ERROR:ui/gl/angle_platform_impl.cc:49] Display.cpp:1079 (initialize): ANGLE Display::initialize error 0: Internal Vulkan error (-3): Initialization of an object could not be completed for implementation-specific reasons, in ../../third
_party/angle/src/libANGLE/renderer/vulkan/vk_renderer.cpp, initialize:2396.                                                                                                                                                                                                    
ERR: Display.cpp:1079 (initialize): ANGLE Display::initialize error 0: Internal Vulkan error (-3): Initialization of an object could not be completed for implementation-specific reasons, in ../../third_party/angle/src/libANGLE/renderer/vulkan/vk_renderer.cpp, initialize:
2396.                                                                                                                                                                                                                                                                          
[3894101:3894101:0613/145622.321071:ERROR:ui/gl/egl_util.cc:92] EGL Driver message (Critical) eglInitialize: Internal Vulkan error (-3): Initialization of an object could not be completed for implementation-specific reasons, in ../../third_party/angle/src/libANGLE/render
er/vulkan/vk_renderer.cpp, initialize:2396.                                                                                                                                                                                                                                    
[3894101:3894101:0613/145622.321266:ERROR:ui/gl/gl_display.cc:637] eglInitialize Vulkan failed with error EGL_NOT_INITIALIZED                                                                                                                                                  
[3894101:3894101:0613/145622.321440:ERROR:ui/gl/gl_display.cc:672] Initialization of all EGL display types failed.                                                                                                                                                             
[3894101:3894101:0613/145622.321611:ERROR:ui/ozone/common/gl_ozone_egl.cc:26] GLDisplayEGL::Initialize failed.                                                                                                                                                                 

```

Before I ever even load the PoC. But our reproduction environment is historically bad at GPU bugs, so I'm going to trust your biesct and let the graphics folks take a look. <https://gitlab.freedesktop.org/mesa/mesa/-/commit/5336cbff3bd0ac73cb03915bb2dad102f15d58a0> is quite old, so I think we can safely say this impacts Stable.

### a7...@gmail.com (2025-06-16)

Can you verify:

1. The `VK_DRIVER_FILES` json you set as environment variable contains a path. Is this path pointing to the .so you built?
2. The Chrome version you're starting is an ASAN build? Otherwise the Mesa .so attempts to import some ASAN symbols (exported only by ASAN builds of Chrome), fails to do so and hence results in startup errors.

If both of these are affirmative I don't know why you can't start Chrome with ASAN-Mesa.

### ch...@google.com (2025-06-17)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-07-01)

cwallez: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-16)

cwallez: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### an...@chromium.org (2025-07-29)

[security shepherd]: cwallez@, have you had a chance to look into this issue? Could you please provide an update or re-route to someone if necessary? Thanks!

### kb...@chromium.org (2025-07-29)

David - does anyone on your team work extensively on Linux and if so could they help confirming that this bug reproduces?

Ultimately we'll need a fix in Mesa but there's a question of whether we could work around this bug in Tint.

### ds...@chromium.org (2025-07-29)

I believe Peter has a tested on mesa devices previously?

### pe...@google.com (2025-07-29)

Question for reporter: Is this sensitive to the constant shuffle value
for example we have 111008u but does this happen for values smaller than subgroupsize-1?

### a7...@gmail.com (2025-07-29)

Yes, this is sensitive to this value. Values < 256 don't trigger the issue.

### pe...@google.com (2025-07-29)

Thank you. This is quite interesting. Seems like a lack of sanitation of constants.

### pe...@google.com (2025-08-05)

Public bug [crbug.com/435246627](https://crbug.com/435246627)
Likely fix <https://dawn-review.googlesource.com/c/dawn/+/255322>

### ch...@google.com (2025-08-13)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ms...@google.com (2025-08-14)

I've reproduced the issue on upstream Mesa and am investigating.

### ms...@google.com (2025-08-14)

Upstream fix is here: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/36779>

### ms...@google.com (2025-08-18)

The upstream CI is having problems (it's evidently a known issue and is being worked on), so I haven't been able to land my fixes today.

I'm on vacation until Sept 2. Anyone should feel free to assign the MR upstream to `@Marge-Bot` and cherry pick the patches to `mesa-iris` downstream. Otherwise I'll handle it when I return.

### ch...@google.com (2025-08-20)

petermcneeley: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### a7...@gmail.com (2025-08-23)

The tint workaround seems incomplete as some shuffle opcodes remain unprotected, e.g., `subgroupShuffleDown`.

### pe...@google.com (2025-08-23)

Do you think these other functions are vulnerable in the same way?

### a7...@gmail.com (2025-08-25)

When testing the below shader against tint (with workarounds) against Mesa 25.2 (without the patch) results in an ASAN violation. Cherry-picking the Mesa patch makes the crash disappear. Upon investigating why the workaround in tint is insufficient I noticed that there are separate IR instructions for `subgroupShuffle`, `subgroupShuffleDown`, ... . So yes, I believe the functions are vulnerable in the same way.

```
enable subgroups;
diagnostic(off, subgroup_uniformity);

@group(0) @binding(0)
var<storage, read_write> d: atomic<i32>;

@fragment fn e(@builtin(sample_index) k: u32, @builtin(position) f: vec4<f32>, @builtin(subgroup_invocation_id) g: u32) -> @builtin(sample_mask) u32 {

    if (g != 65536) { return 0; }

    let i = subgroupShuffleDown(f.zzzz, 1);
    loop {
        atomicStore(&d, 1);
        if (0 > i[0]) { break; }
    }
    return 0;
}

```

### a7...@gmail.com (2025-08-25)

With the Mesa fix applied the fuzzers haven't been finding any ASAN violations in 48 hours (mesa-iris). So definitively improving.

### pe...@google.com (2025-08-25)

Thank you. I will make the same fix for all subgroup operations.

### pe...@google.com (2025-08-26)

This CL fixes subgroupShuffleDown, subgroupShuffleUp, and SubgroupShuffleXor
https://dawn-review.googlesource.com/c/dawn/+/259014

### ms...@google.com (2025-09-03)

Cherry pick of the Mesa fix is here: <https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6908131>

Just waiting for review.

### dx...@google.com (2025-09-04)

Project: chromiumos/third\_party/mesa  

Branch:  chromeos-iris  

Author:  Matt Turner [mattst88@gmail.com](mailto:mattst88@gmail.com)  

Link:    <https://chromium-review.googlesource.com/6908131>

BACKPORT: UPSTREAM: brw/algebraic: Protect SHUFFLE from OOB indices

---


Expand for full commit details
```
     
    Akin to b67230de635 ("intel/fs: Protect opt_algebraic from OOB BROADCAST 
    indices"), we need to protect SHUFFLE as well. 
     
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/13351 
    Reviewed-by: Sagar Ghuge <sagar.ghuge@intel.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/36779> 
     
    (cherry picked from commit b4b692c486ca8e12332d3493f4362de8a1562026 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    Conflicts: 
       src/intel/compiler/brw_opt_algebraic.cpp 
     
    BUG=b:424760433 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I01f8eb1fa3168a14b7dc42784c8c3122ac50c3f2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6908131 
    Reviewed-by: Juston Li <justonli@google.com> 
    Tested-by: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Commit-Queue: Matt Turner <msturner@google.com>

```

---

Files:

- M `src/intel/compiler/brw_fs_opt_algebraic.cpp`

---

Hash: [fc5ec52e423c3a598ab5eb64092d952ce742b63b](https://chromiumdash.appspot.com/commit/fc5ec52e423c3a598ab5eb64092d952ce742b63b)  

Date: Thu Aug 14 17:44:48 2025


---

### ms...@google.com (2025-09-04)

Upstream fix cherry picked to mesa-iris.

Marking as fixed.

### pe...@google.com (2025-09-04)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ms...@google.com (2025-09-04)

> Was this issue a regression for the milestone it was found in?

No.

> Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### pe...@google.com (2025-09-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-09-10)

1. https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6918319
2. Low - There was no conflict.
3. `chromeos-iris` branch
4. yes, it looks like the issue has existed for a long time. And M132 contains the suspected CL[1].

[1] intel/fs: Protect opt_algebraic from OOB BROADCAST indices

### pe...@google.com (2025-09-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-09-10)

1. https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6918503
2. Low - There was no conflict.
3. `chromeos-iris` branch
4. yes, it looks like the issue has existed for a long time. And M138 contains the suspected CL[1].

[1] intel/fs: Protect opt_algebraic from OOB BROADCAST indices


### sp...@google.com (2025-09-10)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
Baseline memory Corruption in a highly privileged process (GPU) with a bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2025-09-18)

Project: chromiumos/third\_party/mesa  

Branch:  release-R138-16295.B-chromeos-iris  

Author:  Matt Turner [mattst88@gmail.com](mailto:mattst88@gmail.com)  

Link:    <https://chromium-review.googlesource.com/6918503>

[M138-LTS] BACKPORT: UPSTREAM: brw/algebraic: Protect SHUFFLE from OOB indices

---


Expand for full commit details
```
     
    Akin to b67230de635 ("intel/fs: Protect opt_algebraic from OOB BROADCAST 
    indices"), we need to protect SHUFFLE as well. 
     
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/13351 
    Reviewed-by: Sagar Ghuge <sagar.ghuge@intel.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/36779> 
     
    (cherry picked from commit b4b692c486ca8e12332d3493f4362de8a1562026 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    Conflicts: 
       src/intel/compiler/brw_opt_algebraic.cpp 
     
    BUG=b:424760433 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I01f8eb1fa3168a14b7dc42784c8c3122ac50c3f2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6908131 
    Reviewed-by: Juston Li <justonli@google.com> 
    Tested-by: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Commit-Queue: Matt Turner <msturner@google.com> 
    (cherry picked from commit fc5ec52e423c3a598ab5eb64092d952ce742b63b) 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6918503 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Tested-by: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Matt Turner <msturner@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>

```

---

Files:

- M `src/intel/compiler/brw_fs_opt_algebraic.cpp`

---

Hash: [2ffa9f17d6929a80d330009cd9949b35c525da22](https://chromiumdash.appspot.com/commit/2ffa9f17d6929a80d330009cd9949b35c525da22)  

Date: Thu Aug 14 17:44:48 2025


---

### ch...@google.com (2025-12-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline memory Corruption in a highly privileged process (GPU) with a bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/424760433)*
