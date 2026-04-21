#  GPU process crash via WebGPU shader - heap-use-after-free in Mesa aco:do_pack_2x16 

| Field | Value |
|-------|-------|
| **Issue ID** | [428515091](https://issues.chromium.org/issues/428515091) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | a7...@gmail.com |
| **Assignee** | ol...@google.com |
| **Created** | 2025-06-29 |
| **Bounty** | $10,000.00 |

## Description

#### VULNERABILITY DETAILS

This report is about a heap-use-after-free in the Mesa shader compiler, reachable via WebGPU shaders emitted by dawn/tint. The offending shader looks as follows:

```
enable f16;
enable subgroups;
diagnostic(off, subgroup_uniformity);

@group(0) @binding(0)
var<storage, read_write> a: vec4<f16>;

@fragment
fn frag_main() -> @location(0) vec4<f32> {
    let j = subgroupExclusiveMul(vec4(1));
    let e = i32(j.z);
    switch e {
        case 1 {
            discard;
        }
        default{
            loop {
                switch e {
                    case 8 { return vec4<f32>(); }
                    case 9 { return vec4<f32>(); }
                    default { }
                }
                if u32(j.x) == 0 { return vec4<f32>(); }
            }
        }
    }
    a = subgroupExclusiveMul(vec4(1h));
    return vec4<f32>();
}

```

The code-path indicates an AMD-specific issue. Bisecting did not a recent regressor; versions as early as mesa-22.3.0 are affected. Earlier versions couldn't be tested because they fail to recognize my GPU.

#### VERSION

Chrome Version: Version 140.0.7267.0 (Developer Build) (64-bit)   

Operating System: Ubuntu 25.04   

Mesa: mesa-25.1.4

#### REPRODUCTION

There are two means of reproduction, standalone and via Chrome. In either case you'll need an ASAN build of Mesa. Precise built instructions depend on the distro, a complete example for Ubuntu is part of the Dockerfile file of the standalone reproducer.

##### Standalone

- Place the `Dockerfile` and the `.gfxr` in a new directory
- Inside this directory: `docker build -t mesarepo .`
- Once built, switch into the container: `docker run -it mesarepo /bin/bash`
- Inside the container, run: `LD_PRELOAD="/usr/lib/llvm-20/lib/clang/20/lib/linux/libclang_rt.asan-x86_64.so /mesa/buildASAN/src/amd/drm-shim/libamdgpu_noop_drm_shim.so" VK_DRIVER_FILES=/mesa/buildASAN/src/amd/vulkan/radeon_icd.x86_64.json /gfxreconstruct/build/tools/replay/gfxrecon-replay /gfxrecon.gfxr`

##### Chrome

Reproducing the issue in Chrome requires an ASAN build of Mesa as well as an ASAN build of Chromium. Note that the issue seems to be in an AMD-specific code path, requiring an AMD GPU for reproduction. The crash in Chrome has been observed using an AMD RX 7600. Opening the attached html file should trigger a heap-use-after-free ASAN violation in the Chrome GPU process. Start chrome and run it with the ASAN version of mesa (adapt paths as needed): `ASAN_OPTIONS=external_symbolizer_path=/usr/lib/llvm-20/bin/llvm-symbolizer VK_DRIVER_FILES=/path/to/src/amd/vulkan/radeon_icd.x86_64.json ./chrome --user-data-dir=/tmp/deleteme --use-angle=vulkan --enable-features=Vulkan --disable-gpu-watchdog --no-sandbox --enable-unsafe-webgpu` and open the attached html:

```
=================================================================
==174342==ERROR: AddressSanitizer: heap-use-after-free on address 0x70d1888d1260 at pc 0x6ea16957e036 bp 0x7fff34069fd0 sp 0x7fff34069fc8
READ of size 1 at 0x70d1888d1260 thread T0 (chrome)
[174284:174312:0629/145806.258848:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
    #0 0x6ea16957e035 in aco::(anonymous namespace)::do_pack_2x16(aco::(anonymous namespace)::lower_context*, aco::Builder&, aco::Definition, aco::Operand, aco::Operand) /home/user/mesa/buildASAN/../src/amd/compiler/aco_lower_to_hw_instr.cpp:1580:45
    #1 0x6ea16957e035 in aco::(anonymous namespace)::handle_operands(std::map<aco::PhysReg, aco::(anonymous namespace)::copy_operation, std::less<aco::PhysReg>, std::allocator<std::pair<aco::PhysReg const, aco::(anonymous namespace)::copy_operation>>>&, aco::(anonymous namespace)::lower_context*, amd_gfx_level, aco::Pseudo_instruction*) /home/user/mesa/buildASAN/../src/amd/compiler/aco_lower_to_hw_instr.cpp:1832:16
    #2 0x6ea169557d6d in aco::lower_to_hw_instr(aco::Program*) /home/user/mesa/buildASAN/../src/amd/compiler/aco_lower_to_hw_instr.cpp:2348:16
    #3 0x6ea1694605c3 in (anonymous namespace)::aco_postprocess_shader[abi:cxx11](aco_compiler_options const*, std::unique_ptr<aco::Program, std::default_delete<aco::Program>>&) /home/user/mesa/buildASAN/../src/amd/compiler/aco_interface.cpp:149:4
    #4 0x6ea16945f4a7 in aco_compile_shader /home/user/mesa/buildASAN/../src/amd/compiler/aco_interface.cpp:242:26
    #5 0x6ea168ab0a8e in shader_compile /home/user/mesa/buildASAN/../src/amd/vulkan/radv_shader.c:3114:7
    #6 0x6ea168ab0a8e in radv_shader_nir_to_asm /home/user/mesa/buildASAN/../src/amd/vulkan/radv_shader.c:3145:7
    #7 0x6ea168a56457 in radv_graphics_shaders_nir_to_asm /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:2390:21
    #8 0x6ea168a56457 in radv_graphics_shaders_compile /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:2815:4
    #9 0x6ea168a67e65 in radv_graphics_pipeline_compile /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3057:4
    #10 0x6ea168a5e68c in radv_graphics_pipeline_init /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3452:13
    #11 0x6ea168a5e68c in radv_graphics_pipeline_create /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3513:13
    #12 0x6ea168a5e68c in radv_CreateGraphicsPipelines /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3668:14
    #13 0x5e6512e4e3e8 in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:615:5
    #14 0x5e6512bba567 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:383:5
    #15 0x5e6512a88239 in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2086:51
    #16 0x5e6512a87c2a in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1416:26
    #17 0x5e652f366c6f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:307:9
    #18 0x5e652f35983c in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:595:9
    #19 0x5e652f3608d3 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1674:30
    #20 0x5e652f31b570 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:156:33
    #21 0x5e652f31ba03 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1941:22
    #22 0x5e652f30fa51 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1886:18
    #23 0x5e6519d1af27 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:265:35
    #24 0x5e652eb4f417 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:495:22
    #25 0x5e652eb4e661 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:162:7
    #26 0x5e652eb70a1d in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:886:13
    #27 0x5e652eb7fd97 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:731:12
    #28 0x5e652eb7fb7f in MakeItSo<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:947:5
    #29 0x5e652eb7fb7f in RunImpl<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #30 0x5e652eb7fb7f in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:973:12
    #31 0x5e6519d5cdf5 in Run base/functional/callback.h:156:12
    #32 0x5e6519d5cdf5 in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:806:49
    #33 0x5e6519d5cdf5 in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #34 0x5e6519d5cdf5 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1060:14
    #35 0x5e6519d3008c in Run base/functional/callback.h:156:12
    #36 0x5e6519d3008c in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:672:29
    #37 0x5e6519d2dcec in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:594:3
    #38 0x5e6519d343c3 in Invoke<void (Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:731:12
    #39 0x5e6519d343c3 in MakeItSo<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #40 0x5e6519d343c3 in RunImpl<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1060:14
    #41 0x5e6519d343c3 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #42 0x5e6525ac2f06 in Run base/functional/callback.h:156:12
    #43 0x5e6525ac2f06 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:207:34
    #44 0x5e6525b35947 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:104:5
    #45 0x5e6525b35947 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #46 0x5e6525b3482c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #47 0x5e6525b3643a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #48 0x5e6525989343 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #49 0x5e6525b36ff4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #50 0x5e6525a416ef in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #51 0x5e6530920a21 in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:454:14
    #52 0x5e652264a37c in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:665:14
    #53 0x5e652264b34c in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:764:12
    #54 0x5e652264dd01 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1158:10
    #55 0x5e65226480be in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:361:36
    #56 0x5e65226485eb in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:374:10
    #57 0x5e651003a277 in ChromeMain chrome/app/chrome_main.cc:222:12
    #58 0x72a18a22a337 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #59 0x72a18a22a3fa in __libc_start_main csu/../csu/libc-start.c:360:3
    #60 0x5e650ff5e029 in _start (/home/user/Downloads/linux-1480243/chrome+0xfc61029) (BuildId: 370cecd94f166502)

0x70d1888d1260 is located 5472 bytes inside of 6384-byte region [0x70d1888cfd00,0x70d1888d15f0)
freed by thread T0 (chrome) here:
    #0 0x5e65100391ad in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:143:3
    #1 0x6ea16946505d in std::__new_allocator<aco::Block>::deallocate(aco::Block*, unsigned long) ../../include/c++/14/bits/new_allocator.h:172:2
    #2 0x6ea16946505d in std::allocator_traits<std::allocator<aco::Block>>::deallocate(std::allocator<aco::Block>&, aco::Block*, unsigned long) ../../include/c++/14/bits/alloc_traits.h:550:13
    #3 0x6ea16946505d in void std::vector<aco::Block, std::allocator<aco::Block>>::_M_realloc_append<aco::Block>(aco::Block&&)::_Guard::~_Guard() ../../include/c++/14/bits/vector.tcc:615:6
    #4 0x6ea16946505d in void std::vector<aco::Block, std::allocator<aco::Block>>::_M_realloc_append<aco::Block>(aco::Block&&) ../../include/c++/14/bits/vector.tcc:688:7
    #5 0x6ea16948ed1e in aco::Block& std::vector<aco::Block, std::allocator<aco::Block>>::emplace_back<aco::Block>(aco::Block&&) ../../include/c++/14/bits/vector.tcc:123:4
    #6 0x6ea16948ed1e in aco::Program::insert_block(aco::Block&&) /home/user/mesa/buildASAN/../src/amd/compiler/aco_ir.h:2218:14
    #7 0x6ea16948ed1e in aco::Program::create_and_insert_block() /home/user/mesa/buildASAN/../src/amd/compiler/aco_ir.h:2208:14
    #8 0x6ea16956616a in aco::lower_to_hw_instr(aco::Program*) /home/user/mesa/buildASAN/../src/amd/compiler/aco_lower_to_hw_instr.cpp:2422:44
    #9 0x6ea1694605c3 in (anonymous namespace)::aco_postprocess_shader[abi:cxx11](aco_compiler_options const*, std::unique_ptr<aco::Program, std::default_delete<aco::Program>>&) /home/user/mesa/buildASAN/../src/amd/compiler/aco_interface.cpp:149:4
    #10 0x6ea16945f4a7 in aco_compile_shader /home/user/mesa/buildASAN/../src/amd/compiler/aco_interface.cpp:242:26
    #11 0x6ea168ab0a8e in shader_compile /home/user/mesa/buildASAN/../src/amd/vulkan/radv_shader.c:3114:7
    #12 0x6ea168ab0a8e in radv_shader_nir_to_asm /home/user/mesa/buildASAN/../src/amd/vulkan/radv_shader.c:3145:7
    #13 0x6ea168a56457 in radv_graphics_shaders_nir_to_asm /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:2390:21
    #14 0x6ea168a56457 in radv_graphics_shaders_compile /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:2815:4
    #15 0x6ea168a67e65 in radv_graphics_pipeline_compile /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3057:4
    #16 0x6ea168a5e68c in radv_graphics_pipeline_init /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3452:13
    #17 0x6ea168a5e68c in radv_graphics_pipeline_create /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3513:13
    #18 0x6ea168a5e68c in radv_CreateGraphicsPipelines /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3668:14
    #19 0x5e6512e4e3e8 in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:615:5
    #20 0x5e6512bba567 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:383:5
    #21 0x5e6512a88239 in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2086:51
    #22 0x5e6512a87c2a in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1416:26
    #23 0x5e652f366c6f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:307:9
    #24 0x5e652f35983c in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:595:9
    #25 0x5e652f3608d3 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1674:30
    #26 0x5e652f31b570 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:156:33
    #27 0x5e652f31ba03 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1941:22
    #28 0x5e652f30fa51 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1886:18
    #29 0x5e6519d1af27 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:265:35
    #30 0x5e652eb4f417 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:495:22
    #31 0x5e652eb4e661 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:162:7
    #32 0x5e652eb70a1d in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:886:13
    #33 0x5e652eb7fd97 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:731:12
    #34 0x5e652eb7fb7f in MakeItSo<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:947:5
    #35 0x5e652eb7fb7f in RunImpl<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #36 0x5e652eb7fb7f in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:973:12
    #37 0x5e6519d5cdf5 in Run base/functional/callback.h:156:12
    #38 0x5e6519d5cdf5 in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:806:49
    #39 0x5e6519d5cdf5 in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #40 0x5e6519d5cdf5 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1060:14
    #41 0x5e6519d3008c in Run base/functional/callback.h:156:12
    #42 0x5e6519d3008c in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:672:29
    #43 0x5e6519d2dcec in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:594:3
    #44 0x5e6519d343c3 in Invoke<void (Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:731:12
    #45 0x5e6519d343c3 in MakeItSo<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #46 0x5e6519d343c3 in RunImpl<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1060:14
    #47 0x5e6519d343c3 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12

previously allocated by thread T0 (chrome) here:
    #0 0x5e651003894d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x6ea169727d89 in std::__new_allocator<aco::Block>::allocate(unsigned long, void const*) ../../include/c++/14/bits/new_allocator.h:151:27
    #2 0x6ea169727d89 in std::allocator_traits<std::allocator<aco::Block>>::allocate(std::allocator<aco::Block>&, unsigned long) ../../include/c++/14/bits/alloc_traits.h:515:20
    #3 0x6ea169727d89 in std::_Vector_base<aco::Block, std::allocator<aco::Block>>::_M_allocate(unsigned long) ../../include/c++/14/bits/stl_vector.h:380:20
    #4 0x6ea169727d89 in std::vector<aco::Block, std::allocator<aco::Block>>::reserve(unsigned long) ../../include/c++/14/bits/vector.tcc:79:22
    #5 0x6ea169727d89 in aco::setup_isel_context(aco::Program*, unsigned int, nir_shader* const*, ac_shader_config*, aco_compiler_options const*, aco_shader_info const*, ac_shader_args const*, aco::SWStage) /home/user/mesa/buildASAN/../src/amd/compiler/instruction_selection/aco_isel_setup.cpp:772:24
    #6 0x6ea1696823aa in aco::select_program(aco::Program*, unsigned int, nir_shader* const*, ac_shader_config*, aco_compiler_options const*, aco_shader_info const*, ac_shader_args const*) /home/user/mesa/buildASAN/../src/amd/compiler/instruction_selection/aco_select_nir.cpp:1426:7
    #7 0x6ea16945f483 in aco_compile_shader /home/user/mesa/buildASAN/../src/amd/compiler/aco_interface.cpp:240:4
    #8 0x6ea168ab0a8e in shader_compile /home/user/mesa/buildASAN/../src/amd/vulkan/radv_shader.c:3114:7
    #9 0x6ea168ab0a8e in radv_shader_nir_to_asm /home/user/mesa/buildASAN/../src/amd/vulkan/radv_shader.c:3145:7
    #10 0x6ea168a56457 in radv_graphics_shaders_nir_to_asm /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:2390:21
    #11 0x6ea168a56457 in radv_graphics_shaders_compile /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:2815:4
    #12 0x6ea168a67e65 in radv_graphics_pipeline_compile /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3057:4
    #13 0x6ea168a5e68c in radv_graphics_pipeline_init /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3452:13
    #14 0x6ea168a5e68c in radv_graphics_pipeline_create /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3513:13
    #15 0x6ea168a5e68c in radv_CreateGraphicsPipelines /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_graphics.c:3668:14
    #16 0x5e6512e4e3e8 in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:615:5
    #17 0x5e6512bba567 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:383:5
    #18 0x5e6512a88239 in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2086:51
    #19 0x5e6512a87c2a in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1416:26
    #20 0x5e652f366c6f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:307:9
    #21 0x5e652f35983c in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:595:9
    #22 0x5e652f3608d3 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1674:30
    #23 0x5e652f31b570 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:156:33
    #24 0x5e652f31ba03 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1941:22
    #25 0x5e652f30fa51 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1886:18
    #26 0x5e6519d1af27 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:265:35
    #27 0x5e652eb4f417 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:495:22
    #28 0x5e652eb4e661 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:162:7
    #29 0x5e652eb70a1d in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:886:13
    #30 0x5e652eb7fd97 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:731:12
    #31 0x5e652eb7fb7f in MakeItSo<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:947:5
    #32 0x5e652eb7fb7f in RunImpl<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #33 0x5e652eb7fb7f in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:973:12
    #34 0x5e6519d5cdf5 in Run base/functional/callback.h:156:12
    #35 0x5e6519d5cdf5 in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:806:49
    #36 0x5e6519d5cdf5 in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #37 0x5e6519d5cdf5 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1060:14
    #38 0x5e6519d3008c in Run base/functional/callback.h:156:12
    #39 0x5e6519d3008c in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:672:29
    #40 0x5e6519d2dcec in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:594:3
    #41 0x5e6519d343c3 in Invoke<void (Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:731:12
    #42 0x5e6519d343c3 in MakeItSo<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #43 0x5e6519d343c3 in RunImpl<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1060:14
    #44 0x5e6519d343c3 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #45 0x5e6525ac2f06 in Run base/functional/callback.h:156:12
    #46 0x5e6525ac2f06 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:207:34
    #47 0x5e6525b35947 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:104:5
    #48 0x5e6525b35947 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23

SUMMARY: AddressSanitizer: heap-use-after-free /home/user/mesa/buildASAN/../src/amd/compiler/aco_lower_to_hw_instr.cpp:1580:45 in aco::(anonymous namespace)::do_pack_2x16(aco::(anonymous namespace)::lower_context*, aco::Builder&, aco::Definition, aco::Operand, aco::Operand)
Shadow bytes around the buggy address:
  0x70d1888d0f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70d1888d1000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70d1888d1080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70d1888d1100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70d1888d1180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x70d1888d1200: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd
  0x70d1888d1280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70d1888d1300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70d1888d1380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70d1888d1400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x70d1888d1480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==174342==ADDITIONAL INFO

==174342==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5e6519d2e239 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:610:27
    #1 0x5e6519d2e239 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:610:27
    #2 0x5e6519d29e1d in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*) gpu/command_buffer/service/scheduler.cc:412:29


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --ozone-platform=wayland --render-node-override=/dev/dri/renderD128 --use-angle=vulkan --crashpad-handler-pid=174291 --enable-crash-reporter=, --user-data-dir=/tmp/deleteme --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAoAQAIAAAAAAAAAAAAAMAAAgAAAAIAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,11408805778871955108,14110357538963709261,262144 --field-trial-handle=3,i,10760395712238912777,1379634972567036274,262144 --enable-features=Vulkan --disable-features=EyeDropper --variations-seed-version`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==174342==END OF ADDITIONAL INFO
==174342==ABORTING

```

## Attachments

- gfxrecon_capture_do_pack_2x16.gfxr (application/octet-stream, 11.9 KB)
- radv_do_pack_2x16.html (text/html, 3.4 KB)
- Dockerfile (application/octet-stream, 2.0 KB)

## Timeline

### a7...@gmail.com (2025-06-29)

Upstream report: <https://gitlab.freedesktop.org/mesa/mesa/-/issues/13432>

### dc...@chromium.org (2025-06-30)

enga@, is there any workaround we should be adding for this issue in Chrome?

### cw...@chromium.org (2025-07-01)

Austin no longer works on Chromium, reassigning.

### a7...@gmail.com (2025-07-01)

Upstream fix <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/35833>

### ch...@google.com (2025-07-01)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-07-01)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-07-17)

jrprice: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### jr...@google.com (2025-07-18)

We're trying to figure out what our process is for AMD Mesa bugs. Will update when we have a plan of action.

### pr...@google.com (2025-07-21)

This seems to have a fix upstream. To olv@ to CP this in our branch.

From a process standpoint, for AMD issues, please file a gitlab issue upstream and CC olv@ and basni@ in buganizer always.

### ch...@google.com (2025-08-05)

olv: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ol...@google.com (2025-08-11)

Thanks for the report!

<https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6838012> cherry-picks the upstream fix to our Mesa driver.

### dx...@google.com (2025-08-12)

Project: chromiumos/third\_party/mesa  

Branch:  chromeos-radv  

Author:  Rhys Perry [pendingchaos02@gmail.com](mailto:pendingchaos02@gmail.com)  

Link:    <https://chromium-review.googlesource.com/6838012>

UPSTREAM: aco: update ctx.block when inserting discard block

---


Expand for full commit details
```
     
    Signed-off-by: Rhys Perry <pendingchaos02@gmail.com> 
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/13432 
    Backport-to: 25.1 
    Reviewed-by: Georg Lehmann <dadschoorse@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/35833> 
    (cherry picked from commit 21c4400278edffb24c71c0d2483b4d76c0aa6dbb) 
     
    BUG=b:428515091 
    TEST=gfxreconstruct with asan build 
     
    Change-Id: I6eb8e83028acd9202a115c14f6dfea3c2626816a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6838012 
    Reviewed-by: Prahlad Kilambi <prahladk@google.com> 
    Tested-by: Chia-I Wu <olv@google.com> 
    Commit-Queue: Chia-I Wu <olv@google.com>

```

---

Files:

- M `src/amd/compiler/aco_lower_to_hw_instr.cpp`

---

Hash: [3db75399ea5bdf6a86aca82d90fbf04801e41c01](https://chromiumdash.appspot.com/commit/3db75399ea5bdf6a86aca82d90fbf04801e41c01)  

Date: Mon Jun 30 13:25:17 2025


---

### pe...@google.com (2025-08-12)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ol...@google.com (2025-08-12)

1. Was this issue a regression for the milestone it was found in?
   
   No, it is a pre-existing issue.
2. Is this issue related to a change or feature merged after the latest LTS Milestone?
   
   No.

### ol...@google.com (2025-08-12)

1. Explain how/why your merge fits within the Merge Decision Guidelines?
   
   Security fix
2. Links to the CLs you are requesting to merge.
   
   <https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6842215>
3. Has the change landed and been verified on ToT? If so, explain what testing has been done to limit the risk of regressio
   ns.
   
   Yes, the fix has been verified manually. There is also no test regression on ToT.
4. Does this change need to be merged into other active release branches (M-1, M+1)?
   
   It affects all milestones. But I think merging to M140 is enough, unless the security team disagrees.
5. Has your Eng Prod Representative approved (in any form) that testing for this change can be accommodated? (if this merge would change/add to the required testing)
   
   N/A
6. Why are these changes required in this milestone after branch?
   
   Security fix
7. Is this a new/unlaunched/in-development feature or a bug fix related to a new/unlaunched/in-development feature in any way?
   
   No
8. Does this change have the potential to impact released devices? If the request is specific to an unreleased device, but the cherry-pick is not going to land in a model-specific directory, please CC a member of the SIE team to LGTM that the change will not impact any released devices.
   
   Yes, but it is a one-line fix that is deemed low risk.

### lm...@google.com (2025-08-12)

Merge approved for M140

### dx...@google.com (2025-08-13)

Project: chromiumos/third\_party/mesa  

Branch:  release-R140-16371.B-chromeos-radv  

Author:  Rhys Perry [pendingchaos02@gmail.com](mailto:pendingchaos02@gmail.com)  

Link:    <https://chromium-review.googlesource.com/6842215>

UPSTREAM: aco: update ctx.block when inserting discard block

---


Expand for full commit details
```
     
    Signed-off-by: Rhys Perry <pendingchaos02@gmail.com> 
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/13432 
    Backport-to: 25.1 
    Reviewed-by: Georg Lehmann <dadschoorse@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/35833> 
    (cherry picked from commit 21c4400278edffb24c71c0d2483b4d76c0aa6dbb) 
     
    BUG=b:428515091 
    TEST=gfxreconstruct with asan build 
     
    Change-Id: I6eb8e83028acd9202a115c14f6dfea3c2626816a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6838012 
    Reviewed-by: Prahlad Kilambi <prahladk@google.com> 
    Tested-by: Chia-I Wu <olv@google.com> 
    Commit-Queue: Chia-I Wu <olv@google.com> 
    (cherry picked from commit 3db75399ea5bdf6a86aca82d90fbf04801e41c01) 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6842215

```

---

Files:

- M `src/amd/compiler/aco_lower_to_hw_instr.cpp`

---

Hash: [46e69e286086ff617156f197a77e9809cd2c286f](https://chromiumdash.appspot.com/commit/46e69e286086ff617156f197a77e9809cd2c286f)  

Date: Mon Jun 30 13:25:17 2025


---

### sp...@google.com (2025-08-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
Report of memory corruption in a highly-privileged process (GPU)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2025-09-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### pe...@google.com (2025-09-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2025-09-16)

1 <https://crrev.com/c/6938777>
2 Low, no conflicts
3 140
4 Yes

### pe...@google.com (2025-09-17)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### rz...@google.com (2025-09-18)

Requesting merge for LTS-132:

1. <https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6873303>
2. Low, no conflicts
3. 140
4. Yes

### dx...@google.com (2025-10-06)

Project: chromiumos/third\_party/mesa  

Branch:  release-R138-16295.B-chromeos-radv  

Author:  Rhys Perry [pendingchaos02@gmail.com](mailto:pendingchaos02@gmail.com)  

Link:    <https://chromium-review.googlesource.com/6938777>

[M138-LTS] UPSTREAM: aco: update ctx.block when inserting discard block

---


Expand for full commit details
```
     
    Signed-off-by: Rhys Perry <pendingchaos02@gmail.com> 
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/13432 
    Backport-to: 25.1 
    Reviewed-by: Georg Lehmann <dadschoorse@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/35833> 
    (cherry picked from commit 21c4400278edffb24c71c0d2483b4d76c0aa6dbb) 
     
    BUG=b:428515091 
    TEST=gfxreconstruct with asan build 
     
    Change-Id: I6eb8e83028acd9202a115c14f6dfea3c2626816a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6838012 
    Tested-by: Chia-I Wu <olv@google.com> 
    Commit-Queue: Chia-I Wu <olv@google.com> 
    (cherry picked from commit 3db75399ea5bdf6a86aca82d90fbf04801e41c01) 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6938777 
    Tested-by: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
    Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com>

```

---

Files:

- M `src/amd/compiler/aco_lower_to_hw_instr.cpp`

---

Hash: [570cab4a8b79abf5979c5fcc36189c8035afffa3](https://chromiumdash.appspot.com/commit/570cab4a8b79abf5979c5fcc36189c8035afffa3)  

Date: Mon Jun 30 13:25:17 2025


---

### ch...@google.com (2025-11-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Report of memory corruption in a highly-privileged process (GPU)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/428515091)*
