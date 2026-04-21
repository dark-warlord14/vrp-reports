# GPU process crash via WebGPU shader - unknown-crash at fs_nir_emit_alu in brw_fs_nir.cpp

| Field | Value |
|-------|-------|
| **Issue ID** | [377321465](https://issues.chromium.org/issues/377321465) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | wg...@gmail.com |
| **Assignee** | ms...@google.com |
| **Created** | 2024-11-04 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

This report is about a vulnerability in Mesa reachable via WebGPU shaders. The Mesa version is the one used by ChromeOS (which, in contrast to other versions of Linux, enables WebGPU). The bug reproducer was tested on an Ubuntu machine, which should not influence whether the bug is reachable on ChromeOS.

##### DISCLAIMER

1. I wanted to file this issue in the ChromeOS tracker directly but it seems I can't create non-public bugs there? (sorry [am...@chromium.org](mailto:am...@chromium.org))
2. I suspect the root cause of this issue to be identical to [issue 350528343](https://issues.chromium.org/issues/350528343). The fix is a workaround in the ANGLE front-end which prevents reaching the actual root-cause via WebGL shaders. Obviously this workaround is ineffective for WebGPU shaders (which are processed by tint instead of ANGLE).
3. The upsteam issue is <https://gitlab.freedesktop.org/mesa/mesa/-/issues/11449> The issue seems to be deep down in the intel-specific part of Mesa (the backtrace is somewhere in the intel-specific code, entered via brw\_compile\_fs)

##### VERSION

Chrome Version: 132.0.6819.0 (Developer Build) (64-bit) (ASAN build)  

Operating System: Ubuntu  

Mesa: branch chromeos-iris, commit 05bc211c0764b02c63f467c8823580041a723c9a

##### REPRODUCTION CASE

Attached is a html file that triggers an ASAN violation when opened in an ASAN version of Mesa (assuming Mesa has been built with ASAN enabled) and using an Intel GPU (tested on the integrated GPU of an i7-10510U).

ASAN report:

```
==84219==ERROR: AddressSanitizer: unknown-crash on address 0x761719bcb7f5 at pc 0x734710e129ee bp 0x7ffe4c236f30 sp 0x7ffe4c236f28
READ of size 8 at 0x761719bcb7f5 thread T0 (chrome)
    #0 0x734710e129ed in fs_nir_emit_alu(nir_to_brw_state&, nir_alu_instr*, bool) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs_nir.cpp:912:55
    #1 0x734710e021f3 in fs_nir_emit_instr(nir_to_brw_state&, nir_instr*) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs_nir.cpp:8779:7
    #2 0x734710e021f3 in fs_nir_emit_block(nir_to_brw_state&, nir_block*) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs_nir.cpp:484:7
    #3 0x734710dffedb in fs_nir_emit_cf_list(nir_to_brw_state&, exec_list*) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs_nir.cpp:418:10
    #4 0x734710dfbc70 in fs_nir_emit_impl(nir_to_brw_state&, nir_function_impl*) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs_nir.cpp:400:4
    #5 0x734710dfbc70 in nir_to_brw(fs_visitor*) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs_nir.cpp:8982:4
    #6 0x734710dbfe4e in fs_visitor::run_fs(bool, bool) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs.cpp:3276:7
    #7 0x734710dc37d4 in brw_compile_fs /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs.cpp:3873:16
    #8 0x73470ff2875f in anv_pipeline_compile_fs /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:1616:21
    #9 0x73470ff2875f in anv_graphics_pipeline_compile /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:2495:10
    #10 0x73470ff1421d in anv_graphics_pipeline_create /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:3253:13
    #11 0x73470ff1421d in anv_CreateGraphicsPipelines /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:3313:16
    #12 0x64d78cee75ec in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:590:9
    #13 0x64d78ccbafba in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:380:5
    #14 0x64d78cbee099 in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2256:51
    #15 0x64d78cbeda9a in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1566:26
    #16 0x64d7a66c6d4f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:306:9
    #17 0x64d7a66b984c in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:583:9
    #18 0x64d7a66bf022 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1635:30
    #19 0x64d7a6680e60 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1067:33
    #20 0x64d7a66812f3 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1997:22
    #21 0x64d7a6672cc3 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1942:18
    #22 0x64d7a6593497 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:263:35
    #23 0x64d7a6582e1a in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:496:22
    #24 0x64d7a65822bd in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:160:7
    #25 0x64d7a659eed5 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:967:13
    #26 0x64d7a65ae308 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:738:12
    #27 0x64d7a65ae0cf in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:954:5
    #28 0x64d7a65ae0cf in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1067:14
    #29 0x64d7a65ae0cf in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:980:12
    #30 0x64d7a3594c03 in Run base/functional/callback.h:156:12
    #31 0x64d7a3594c03 in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:813:49
    #32 0x64d7a3594c03 in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:930:12
    #33 0x64d7a3594c03 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1067:14
    #34 0x64d7a3570d3a in Run base/functional/callback.h:156:12
    #35 0x64d7a3570d3a in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:676:29
    #36 0x64d7a356ea07 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:600:3
    #37 0x64d7a35724e3 in Invoke<void (gpu::Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:738:12
    #38 0x64d7a35724e3 in MakeItSo<void (gpu::Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:930:12
    #39 0x64d7a35724e3 in RunImpl<void (gpu::Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1067:14
    #40 0x64d7a35724e3 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #41 0x64d79da45da4 in Run base/functional/callback.h:156:12
    #42 0x64d79da45da4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:202:34
    #43 0x64d79daaef88 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:11)> base/task/common/task_annotator.h:98:5
    #44 0x64d79daaef88 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:471:23
    #45 0x64d79daadd2a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332:40
    #46 0x64d79daafcba in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #47 0x64d79dc08552 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:649:46
    #48 0x64d79dc0b348 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:274:43
    #49 0x77471c71d5b4  (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5d5b4) (BuildId: 9753724b85d60f97b5d5663181ef7f4e69a62131)
    #50 0x77471c77c716  (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0xbc716) (BuildId: 9753724b85d60f97b5d5663181ef7f4e69a62131)
    #51 0x77471c71ca52 in g_main_context_iteration (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5ca52) (BuildId: 9753724b85d60f97b5d5663181ef7f4e69a62131)
    #52 0x64d79dc08b7f in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:683:30
    #53 0x64d79dab08aa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #54 0x64d79d9d70cf in base::RunLoop::Run(base::Location const&) base/run_loop.cc:133:14
    #55 0x64d7b45d552e in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:444:14
    #56 0x64d79ab78653 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:699:14
    #57 0x64d79ab7951d in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:803:12
    #58 0x64d79ab7bc8b in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1163:10
    #59 0x64d79ab769b5 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:356:36
    #60 0x64d79ab76fcb in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:369:10
    #61 0x64d789a2ef9a in ChromeMain chrome/app/chrome_main.cc:223:12
    #62 0x77471b22a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #63 0x77471b22a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #64 0x64d789954029 in _start (/home/user/Downloads/linux-release-1377742/chrome+0xf23e029) (BuildId: 650d66fb9a165cd2)

0x761719bcb7f5 is located 13301 bytes inside of 32752-byte region [0x761719bc8400,0x761719bd03f0)
allocated by thread T0 (chrome) here:
    #0 0x64d7899f2c94 in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:67:3
    #1 0x7347106f851d in ralloc_size /home/user/chromeosMesaOrg/buildASAN/../src/util/ralloc.c:118:18
    #2 0x7347106f851d in create_slab /home/user/chromeosMesaOrg/buildASAN/../src/util/ralloc.c:801:20
    #3 0x7347106f851d in gc_alloc_size /home/user/chromeosMesaOrg/buildASAN/../src/util/ralloc.c:840:61
    #4 0x7347106f8bee in gc_zalloc_size /home/user/chromeosMesaOrg/buildASAN/../src/util/ralloc.c:868:16
    #5 0x734710ad9dee in nir_deref_instr_create /home/user/chromeosMesaOrg/buildASAN/../src/compiler/nir/nir.c:695:29
    #6 0x734711072381 in nir_build_deref_var /home/user/chromeosMesaOrg/buildASAN/../src/compiler/nir/nir_builder.h:1447:7
    #7 0x734711072381 in vtn_pointer_dereference /home/user/chromeosMesaOrg/buildASAN/../src/compiler/spirv/vtn_variables.c:446:14
    #8 0x73471107582d in vtn_pointer_to_deref /home/user/chromeosMesaOrg/buildASAN/../src/compiler/spirv/vtn_variables.c:509:13
    #9 0x73471107582d in _vtn_variable_load_store /home/user/chromeosMesaOrg/buildASAN/../src/compiler/spirv/vtn_variables.c:706:35
    #10 0x73471107b4c5 in vtn_variable_load /home/user/chromeosMesaOrg/buildASAN/../src/compiler/spirv/vtn_variables.c:764:4
    #11 0x73471107b4c5 in vtn_handle_variables /home/user/chromeosMesaOrg/buildASAN/../src/compiler/spirv/vtn_variables.c:2813:35
    #12 0x734711019c0a in vtn_handle_body_instruction /home/user/chromeosMesaOrg/buildASAN/../src/compiler/spirv/spirv_to_nir.c:6128:7
    #13 0x7347110095b7 in vtn_foreach_instruction /home/user/chromeosMesaOrg/buildASAN/../src/compiler/spirv/spirv_to_nir.c:777:15
    #14 0x734711067b10 in vtn_emit_block /home/user/chromeosMesaOrg/buildASAN/../src/compiler/spirv/vtn_structured_cfg.c:1349:4
    #15 0x734711067b10 in vtn_emit_cf_func_structured /home/user/chromeosMesaOrg/buildASAN/../src/compiler/spirv/vtn_structured_cfg.c:1738:7
    #16 0x7347110496ee in vtn_function_emit /home/user/chromeosMesaOrg/buildASAN/../src/compiler/spirv/vtn_cfg.c:720:7
    #17 0x73471100e1e0 in spirv_to_nir /home/user/chromeosMesaOrg/buildASAN/../src/compiler/spirv/spirv_to_nir.c:6928:13
    #18 0x73471053cac7 in vk_spirv_to_nir /home/user/chromeosMesaOrg/buildASAN/../src/vulkan/runtime/vk_nir.c:144:22
    #19 0x7347105421de in vk_pipeline_shader_stage_to_nir /home/user/chromeosMesaOrg/buildASAN/../src/vulkan/runtime/vk_pipeline.c:185:22
    #20 0x73470ff1d2f2 in anv_shader_stage_to_nir /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:163:7
    #21 0x73470ff1d2f2 in anv_pipeline_stage_get_nir /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:817:17
    #22 0x73470ff25627 in anv_graphics_pipeline_load_nir /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:2053:28
    #23 0x73470ff25627 in anv_graphics_pipeline_compile /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:2288:13
    #24 0x73470ff1421d in anv_graphics_pipeline_create /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:3253:13
    #25 0x73470ff1421d in anv_CreateGraphicsPipelines /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:3313:16
    #26 0x64d78cee75ec in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:590:9
    #27 0x64d78ccbafba in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:380:5
    #28 0x64d78cbee099 in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2256:51
    #29 0x64d78cbeda9a in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1566:26
    #30 0x64d7a66c6d4f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:306:9
    #31 0x64d7a66b984c in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:583:9
    #32 0x64d7a66bf022 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1635:30
    #33 0x64d7a6680e60 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1067:33
    #34 0x64d7a66812f3 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1997:22
    #35 0x64d7a6672cc3 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1942:18
    #36 0x64d7a6593497 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:263:35
    #37 0x64d7a6582e1a in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:496:22
    #38 0x64d7a65822bd in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:160:7

SUMMARY: AddressSanitizer: unknown-crash /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs_nir.cpp:912:55 in fs_nir_emit_alu(nir_to_brw_state&, nir_alu_instr*, bool)
Shadow bytes around the buggy address:
  0x761719bcb500: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x761719bcb580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x761719bcb600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x761719bcb680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x761719bcb700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x761719bcb780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00[00]00
  0x761719bcb800: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x761719bcb880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x761719bcb900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x761719bcb980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x761719bcba00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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

==84219==ADDITIONAL INFO

==84219==Note: Please include this section with the ASan report.
Task trace:
    #0 0x64d7a356eedb in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:616:27
    #1 0x64d7a356eedb in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:616:27
    #2 0x64d7a356eedb in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:616:27
    #3 0x64d7a356eedb in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:616:27


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --use-angle=vulkan --string-annotations --crashpad-handler-pid=84172 --enable-crash-reporter=, --user-data-dir=/tmp/deleteme --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAoAAAEAAAAAAAAAAAAAAAAAADAAAIAAAACAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAAAQAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,6635664808008298280,12340487920340548454,262144 --field-trial-handle=3,i,12055010269265570720,12512237865393580235,262144 --enable-features=Vulkan --disable-features=EyeDropper --variations-seed-version`


==84219==END OF ADDITIONAL INFO
==84219==ABORTING

```

## Attachments

- [nir_src_comp_as_uint.html](attachments/nir_src_comp_as_uint.html) (text/html, 3.7 KB)

## Timeline

### pg...@google.com (2024-11-04)

Setting sev=s0 for oob read in the GPU process  

setting foundin to soon-to-be extended stable 130 (i do not have access to the mesa bug)  

Setting OS to be ChromeOS, but im not sure if this is triggerable elsewhere\

msturner@ can you take a look?

### am...@chromium.org (2024-11-04)

S1 / P1 due to OOB read in GPU (rather than write), while I'm not ruling out the potential a write could be achieved, setting this as S1 in the interim rather than S0 until there is more information that demonstrates this should be elevated.

### kb...@chromium.org (2024-11-04)

Fixes were made upstream in Mesa for [Issue 350528343](https://issues.chromium.org/issues/350528343) which should have addressed the root cause. Submitter, are you saying that even with those fixes applied in Mesa, this GPU process crash can still happen with WebGPU shaders?

### wg...@gmail.com (2024-11-05)

Well, the issue reported here is reachable as of yesterday. I *believe* the root cause to be identical as the one in [issue 350528343](https://issues.chromium.org/issues/350528343) because:

1. in debug builds of Mesa, both issues trigger the same assert `chrome: ../src/compiler/nir/nir.h:2807: uint64_t nir_src_comp_as_uint(nir_src, unsigned int): Assertion nir_src_is_const(src) failed.`
2. in both cases, the crash occurs in intel-specific code path somehow related to register allocation, entered via `brw_compile_*`

The fixes in [issue 350528343](https://issues.chromium.org/issues/350528343) attempt to work around the issue by changing ANGLE s.t. it becomes more difficult to trigger the bug via WebGL. AFAICT, the actual root cause has never been determined. Yes, there are some changes to Mesa back-porting a loop optimization (which also makes it harder for the fuzzer to find the bug via a WebGL shader). Still, I believe the root cause remains.

In the end, it makes no difference for me whether the root cause is identical or not but it might help the investigation.

### pe...@google.com (2024-11-05)

Setting milestone because of s0/s1 severity.

### ms...@google.com (2024-11-05)

Lionel from Intel is actively debugging this issue, per <https://gitlab.freedesktop.org/mesa/mesa/-/issues/11449#note_2623082>

### ms...@google.com (2024-11-13)

I don't see more activity from Lionel in the last few days on this issue, and the discussion was on a closed issue.

Could you file a new issue upstream so it isnt't forgotten upstream?

### wg...@gmail.com (2024-11-14)

I created <https://gitlab.freedesktop.org/mesa/mesa/-/issues/12153> and hope its getting more traction this time.

### ms...@google.com (2024-11-14)

Thank you!

### pe...@google.com (2024-11-29)

msturner: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ms...@google.com (2024-12-02)

The issue doesn't exist on the upstream main branch. An upstream commit avoids the problem by accident. It has been cherry picked to the 24.2 stable branch in <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/32367>, but this isn't a fix for the underlying problem.

I'll apply these patches to our branch.

### ap...@google.com (2024-12-03)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Georg Lehmann <[dadschoorse@gmail.com](mailto:dadschoorse@gmail.com)>  

Link:      <https://chromium-review.googlesource.com/6063368>

UPSTREAM: nir/opt\_remove\_phis: rematerialize constants

---


Expand for full commit details
```
UPSTREAM: nir/opt_remove_phis: rematerialize constants 
 
Foz-DB Navi31: 
Totals from 749 (0.94% of 79395) affected shaders: 
Instrs: 1224359 -> 1223722 (-0.05%); split: -0.07%, +0.02% 
CodeSize: 6468392 -> 6466296 (-0.03%); split: -0.06%, +0.03% 
Latency: 9764410 -> 9766457 (+0.02%); split: -0.01%, +0.03% 
InvThroughput: 1017401 -> 1017380 (-0.00%); split: -0.03%, +0.03% 
VClause: 19902 -> 19873 (-0.15%); split: -0.16%, +0.02% 
SClause: 38441 -> 38424 (-0.04%); split: -0.05%, +0.01% 
Copies: 86880 -> 86304 (-0.66%); split: -0.73%, +0.06% 
Branches: 34206 -> 34159 (-0.14%); split: -0.14%, +0.01% 
PreSGPRs: 45557 -> 45527 (-0.07%); split: -0.08%, +0.01% 
PreVGPRs: 32406 -> 32408 (+0.01%) 
VALU: 671633 -> 671533 (-0.01%); split: -0.02%, +0.01% 
SALU: 155284 -> 154675 (-0.39%); split: -0.40%, +0.00% 
VMEM: 27303 -> 27271 (-0.12%) 
SMEM: 67490 -> 67455 (-0.05%) 
 
Reviewed-by: Daniel Schürmann <daniel@schuermann.dev> 
Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/31031> 
(cherry picked from commit 60776f87c38f69507d60591b46b3ea2efba8e188 
 https://gitlab.freedesktop.org/mesa/mesa.git main) 
 
BUG=b:377321465 
TEST=Run crafted SPIR-V shader without crashing 
 
Change-Id: Ie822710b1a754568658a117b6e3917ed30c42f93 
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6063368 
Reviewed-by: Sean Paul <sean@poorly.run> 
Reviewed-by: Lina Versace <linyaa@google.com> 
Commit-Queue: Matt Turner <msturner@google.com> 
Auto-Submit: Matt Turner <msturner@google.com> 
Tested-by: Matt Turner <msturner@google.com>

```

---

Files:

- M `src/compiler/nir/nir_opt_remove_phis.c`

---

Hash: fbafe5697750b35984bfa327147ad2a362a70ea5  

Date:  Wed Sep 04 18:33:59 2024


---

### ap...@google.com (2024-12-03)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Georg Lehmann <[dadschoorse@gmail.com](mailto:dadschoorse@gmail.com)>  

Link:      <https://chromium-review.googlesource.com/6063367>

UPSTREAM: nir: make nir\_instr\_clone usable with load\_const and undef

---


Expand for full commit details
```
UPSTREAM: nir: make nir_instr_clone usable with load_const and undef 
 
Reviewed-by: Daniel Schürmann <daniel@schuermann.dev> 
Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/31031> 
(cherry picked from commit 40fc85c15b464fba75f13f5fba054c46ef5d26bf 
 https://gitlab.freedesktop.org/mesa/mesa.git main) 
 
BUG=b:377321465 
TEST=Run crafted SPIR-V shader without crashing 
 
Change-Id: I4d537873e22622e1acc11747e5b891e09368f229 
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6063367 
Reviewed-by: Sean Paul <sean@poorly.run> 
Auto-Submit: Matt Turner <msturner@google.com> 
Tested-by: Matt Turner <msturner@google.com> 
Reviewed-by: Lina Versace <linyaa@google.com> 
Commit-Queue: Matt Turner <msturner@google.com>

```

---

Files:

- M `src/compiler/nir/nir_clone.c`

---

Hash: 5ed2f2821dcb48886cf7c88f8f04729ecc0305f3  

Date:  Wed Sep 04 18:33:20 2024


---

### ap...@google.com (2024-12-03)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Georg Lehmann <[dadschoorse@gmail.com](mailto:dadschoorse@gmail.com)>  

Link:      <https://chromium-review.googlesource.com/6063366>

UPSTREAM: nir: replace nir\_opt\_remove\_phis\_block with a single source version

---


Expand for full commit details
```
UPSTREAM: nir: replace nir_opt_remove_phis_block with a single source version 
 
This is what callers actually want, and it simplifies nir_opt_remove_phis 
because we can assume dominance meta data is valid. 
 
Reviewed-by: Daniel Schürmann <daniel@schuermann.dev> 
Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/31031> 
(cherry picked from commit a9f80892403aaa07d134898c5a2931b26ff40702 
 https://gitlab.freedesktop.org/mesa/mesa.git main) 
 
BUG=b:377321465 
TEST=Run crafted SPIR-V shader without crashing 
 
Change-Id: Iec6f4c81ce0d646a52f7786e4872694ba48e45a5 
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6063366 
Reviewed-by: Sean Paul <sean@poorly.run> 
Commit-Queue: Matt Turner <msturner@google.com> 
Reviewed-by: Lina Versace <linyaa@google.com> 
Tested-by: Matt Turner <msturner@google.com> 
Auto-Submit: Matt Turner <msturner@google.com>

```

---

Files:

- M `src/amd/compiler/aco_instruction_selection_setup.cpp`
- M `src/compiler/nir/nir.h`
- M `src/compiler/nir/nir_opt_if.c`
- M `src/compiler/nir/nir_opt_loop.c`
- M `src/compiler/nir/nir_opt_remove_phis.c`

---

Hash: 2d0c7de8a30b6f9e53e8492fe788ac4cede00737  

Date:  Fri Sep 06 14:01:30 2024


---

### ms...@google.com (2024-12-03)

Patches to fix the crash by eliminating the invalid code have landed.

I'd still like to investigate the underlying cause of the invalid code. Marking as P2 to do that.

### th...@chromium.org (2024-12-11)

[secondary shepherd]

msturner@: could you confirm that the security bug has been fixed? That is: will the followup investigation mentioned in [#comment16](https://issues.chromium.org/issues/377321465#comment16) have a security impact (i.e. more CLs that have security behavior change), or is that just for understanding the code better?

amyressler@: if based on the answer to ^, the security bug has been fixed, should we security embargo + close out this bug and file a followup for the remaining investigation? Or do you recommend we keep this issue open until the remaining investigation is complete?

### ar...@chromium.org (2024-12-16)

**(secondary security shepherd)**

msturner@ Gentle ping for comment 11.

I will ping on chat as well.

### ms...@google.com (2024-12-16)

> msturner@: could you confirm that the security bug has been fixed? That is: will the followup investigation mentioned in [#comment16](https://issues.chromium.org/issues/377321465#comment16) have a security impact (i.e. more CLs that have security behavior change), or is that just for understanding the code better?

Yes, the trigger as originally reported is fixed.

I will close this and make a separate note to investigate the potential underlying issue.

### pe...@google.com (2024-12-16)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2024-12-19)

Labeling as LTS-NotApplicable-126 because one[1] of the 3 fixes generates a conflict, so it looks like it's not safe to merge back to M126. Besides I think the fixes just came from the upstream without clear investigation about the root cause. So I'm not sure if we can merge back the 3 fixes to M126 without any side effect.

[1] https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6063366

### pe...@google.com (2025-01-02)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pe...@google.com (2025-01-02)

msturner: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2025-01-04)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### pe...@google.com (2025-01-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pg...@google.com (2025-01-18)

Hi Matt, the bug was opened per [comment #25](https://issues.chromium.org/issues/377321465#comment25) - the "Fixed By Code Changes" field is requested for bugs that do not have single CL fixes!

I've added the three that youve landed in Mesa, assuming all three are required. If some are not required for this to be considered fixed, please remove those.

### pe...@google.com (2025-01-18)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pe...@google.com (2025-01-18)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2025-02-18)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2025-02-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-02-19)

1. https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6277904, https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6276247, and https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6277905
2. Low - There was no conflict.
3. No
4. Yes. it was difficult to find the suspected CL which caused this bug, but the bug happened on the mesa CL[1] that M132 contained. Thus, I think we need to merge them to M132.

[1] https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5939484

### sp...@google.com (2025-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in a highly-privileged process (GPU)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-20)

Congratulations! Thank you for your efforts and reporting this issue to us -- nice work!

### dx...@google.com (2025-04-24)

Project: chromiumos/third\_party/mesa  

Branch: release-R132-16093.B-chromeos-iris  

Author: Georg Lehmann [dadschoorse@gmail.com](mailto:dadschoorse@gmail.com)  

Link:      <https://chromium-review.googlesource.com/6277904>

[M132-LTS] UPSTREAM: nir: replace nir\_opt\_remove\_phis\_block with a single source version

---


Expand for full commit details
```
     
    This is what callers actually want, and it simplifies nir_opt_remove_phis 
    because we can assume dominance meta data is valid. 
     
    Reviewed-by: Daniel Schürmann <daniel@schuermann.dev> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/31031> 
    (cherry picked from commit a9f80892403aaa07d134898c5a2931b26ff40702 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    BUG=b:377321465 
    TEST=Run crafted SPIR-V shader without crashing 
     
    Change-Id: Iec6f4c81ce0d646a52f7786e4872694ba48e45a5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6063366 
    Reviewed-by: Sean Paul <sean@poorly.run> 
    Commit-Queue: Matt Turner <msturner@google.com> 
    Reviewed-by: Lina Versace <linyaa@google.com> 
    Tested-by: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    (cherry picked from commit 2d0c7de8a30b6f9e53e8492fe788ac4cede00737) 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6277904 
    Reviewed-by: Matt Turner <msturner@google.com> 
    Tested-by: Gyuyoung Kim (xWF) <qkim@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com>

```

---

Files:

- M `src/amd/compiler/aco_instruction_selection_setup.cpp`
- M `src/compiler/nir/nir.h`
- M `src/compiler/nir/nir_opt_if.c`
- M `src/compiler/nir/nir_opt_loop.c`
- M `src/compiler/nir/nir_opt_remove_phis.c`

---

Hash: b65a8adfeaa4e222f43e2564468483b6a8de3d80  

Date:  Fri Sep 6 12:01:30 2024


---

### dx...@google.com (2025-04-24)

Project: chromiumos/third\_party/mesa  

Branch: release-R132-16093.B-chromeos-iris  

Author: Georg Lehmann [dadschoorse@gmail.com](mailto:dadschoorse@gmail.com)  

Link:      <https://chromium-review.googlesource.com/6276247>

[M132-LTS] UPSTREAM: nir: make nir\_instr\_clone usable with load\_const and undef

---


Expand for full commit details
```
     
    Reviewed-by: Daniel Schürmann <daniel@schuermann.dev> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/31031> 
    (cherry picked from commit 40fc85c15b464fba75f13f5fba054c46ef5d26bf 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    BUG=b:377321465 
    TEST=Run crafted SPIR-V shader without crashing 
     
    Change-Id: I4d537873e22622e1acc11747e5b891e09368f229 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6063367 
    Reviewed-by: Sean Paul <sean@poorly.run> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Tested-by: Matt Turner <msturner@google.com> 
    Reviewed-by: Lina Versace <linyaa@google.com> 
    Commit-Queue: Matt Turner <msturner@google.com> 
    (cherry picked from commit 5ed2f2821dcb48886cf7c88f8f04729ecc0305f3) 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6276247 
    Reviewed-by: Matt Turner <msturner@google.com> 
    Tested-by: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>

```

---

Files:

- M `src/compiler/nir/nir_clone.c`

---

Hash: 9b9b9fdba436b581b6454651cb0f343b702786e8  

Date:  Wed Sep 4 16:33:20 2024


---

### dx...@google.com (2025-04-24)

Project: chromiumos/third\_party/mesa  

Branch: release-R132-16093.B-chromeos-iris  

Author: Georg Lehmann [dadschoorse@gmail.com](mailto:dadschoorse@gmail.com)  

Link:      <https://chromium-review.googlesource.com/6277905>

[M132-LTS] UPSTREAM: nir/opt\_remove\_phis: rematerialize constants

---


Expand for full commit details
```
     
    Foz-DB Navi31: 
    Totals from 749 (0.94% of 79395) affected shaders: 
    Instrs: 1224359 -> 1223722 (-0.05%); split: -0.07%, +0.02% 
    CodeSize: 6468392 -> 6466296 (-0.03%); split: -0.06%, +0.03% 
    Latency: 9764410 -> 9766457 (+0.02%); split: -0.01%, +0.03% 
    InvThroughput: 1017401 -> 1017380 (-0.00%); split: -0.03%, +0.03% 
    VClause: 19902 -> 19873 (-0.15%); split: -0.16%, +0.02% 
    SClause: 38441 -> 38424 (-0.04%); split: -0.05%, +0.01% 
    Copies: 86880 -> 86304 (-0.66%); split: -0.73%, +0.06% 
    Branches: 34206 -> 34159 (-0.14%); split: -0.14%, +0.01% 
    PreSGPRs: 45557 -> 45527 (-0.07%); split: -0.08%, +0.01% 
    PreVGPRs: 32406 -> 32408 (+0.01%) 
    VALU: 671633 -> 671533 (-0.01%); split: -0.02%, +0.01% 
    SALU: 155284 -> 154675 (-0.39%); split: -0.40%, +0.00% 
    VMEM: 27303 -> 27271 (-0.12%) 
    SMEM: 67490 -> 67455 (-0.05%) 
     
    Reviewed-by: Daniel Schürmann <daniel@schuermann.dev> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/31031> 
    (cherry picked from commit 60776f87c38f69507d60591b46b3ea2efba8e188 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    BUG=b:377321465 
    TEST=Run crafted SPIR-V shader without crashing 
     
    Change-Id: Ie822710b1a754568658a117b6e3917ed30c42f93 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6063368 
    Reviewed-by: Sean Paul <sean@poorly.run> 
    Reviewed-by: Lina Versace <linyaa@google.com> 
    Commit-Queue: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Tested-by: Matt Turner <msturner@google.com> 
    (cherry picked from commit fbafe5697750b35984bfa327147ad2a362a70ea5) 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6277905 
    Reviewed-by: Matt Turner <msturner@google.com> 
    Tested-by: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>

```

---

Files:

- M `src/compiler/nir/nir_opt_remove_phis.c`

---

Hash: a889f777673622593ebb28f3ecad58ea364357b5  

Date:  Wed Sep 4 16:33:59 2024


---

### ch...@google.com (2025-04-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a highly-privileged process (GPU)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/377321465)*
