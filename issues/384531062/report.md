# GPU process crash via WebGPU shader - heap-buffer-overflow in Mesa brw_fs_opt_register_coalesce

| Field | Value |
|-------|-------|
| **Issue ID** | [384531062](https://issues.chromium.org/issues/384531062) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | a7...@gmail.com |
| **Assignee** | ms...@google.com |
| **Created** | 2024-12-17 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

This report is about a vulnerability in Mesa reachable via WebGPU shaders. The Mesa version is the one used by ChromeOS (which, in contrast to other versions of Linux, enables WebGPU). The bug reproducer was tested on an Ubuntu machine, which should not influence whether the bug is reachable on ChromeOS. I will also upload this report upstream, i.e., the Mesa project, and post the link below.

##### VERSION

Chrome Version: 133.0.6902.0 (Developer Build) (64-bit) (ASAN build)   

Operating System: Ubuntu   

Mesa: branch chromeos-iris, commit fbafe5697750b35984bfa327147ad2a362a70ea5

##### REPRODUCTION CASE

Attached is a html file that triggers a heap OOB when opened in an ASAN version of mesa.

```
==13824==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x767c067175a0 at pc 0x759bfe29dd67 bp 0x7ffce9dde9f0 sp 0x7ffce9dde9e8
READ of size 8 at 0x767c067175a0 thread T0 (chrome)
    #0 0x759bfe29dd66 in brw_fs_opt_register_coalesce(fs_visitor&) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs_register_coalesce.cpp:275:14
    #1 0x759bfe284e52 in brw_fs_optimize(fs_visitor&) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs_opt.cpp:117:7
    #2 0x759bfe1bfbff in fs_visitor::run_fs(bool, bool) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs.cpp:3285:7
    #3 0x759bfe1c4290 in brw_compile_fs /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs.cpp:3944:17
    #4 0x759bfd3289af in anv_pipeline_compile_fs /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:1636:21
    #5 0x759bfd3289af in anv_graphics_pipeline_compile /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:2515:10
    #6 0x759bfd3141fd in anv_graphics_pipeline_create /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:3273:13
    #7 0x759bfd3141fd in anv_CreateGraphicsPipelines /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:3333:16
    #8 0x59cb6173f31c in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:609:9
    #9 0x59cb6150196a in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:395:5
    #10 0x59cb614340e9 in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2180:51
    #11 0x59cb61433aea in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1473:26
    #12 0x59cb7c33822f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:306:9
    #13 0x59cb7c32acbc in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:583:9
    #14 0x59cb7c330492 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1635:30
    #15 0x59cb7c2f2070 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1067:33
    #16 0x59cb7c2f2503 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2010:22
    #17 0x59cb7c2e43b3 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1955:18
    #18 0x59cb7c200f77 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:263:35
    #19 0x59cb7c1f047a in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:489:22
    #20 0x59cb7c1efcb4 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:157:7
    #21 0x59cb7c20c91b in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:958:13
    #22 0x59cb7c21c48e in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:738:12
    #23 0x59cb7c21c25f in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:954:5
    #24 0x59cb7c21c25f in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1067:14
    #25 0x59cb7c21c25f in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:980:12
    #26 0x59cb787b9c7d in Run base/functional/callback.h:156:12
    #27 0x59cb787b9c7d in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:813:49
    #28 0x59cb787b9c7d in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:930:12
    #29 0x59cb787b9c7d in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1067:14
    #30 0x59cb78796708 in Run base/functional/callback.h:156:12
    #31 0x59cb78796708 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:675:29
    #32 0x59cb78794877 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:599:3
    #33 0x59cb78798073 in Invoke<void (gpu::Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:738:12
    #34 0x59cb78798073 in MakeItSo<void (gpu::Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:930:12
    #35 0x59cb78798073 in RunImpl<void (gpu::Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1067:14
    #36 0x59cb78798073 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #37 0x59cb72ba3432 in Run base/functional/callback.h:156:12
    #38 0x59cb72ba3432 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:208:34
    #39 0x59cb72c10478 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:11)> base/task/common/task_annotator.h:106:5
    #40 0x59cb72c10478 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:471:23
    #41 0x59cb72c0f21a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332:40
    #42 0x59cb72c111aa in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #43 0x59cb72d7c6fc in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:694:48
    #44 0x59cb72c11d6c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #45 0x59cb72b2b0af in base::RunLoop::Run(base::Location const&) base/run_loop.cc:133:14
    #46 0x59cb89dbd265 in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:456:14
    #47 0x59cb6fbffaf4 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:699:14
    #48 0x59cb6fc009bd in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:803:12
    #49 0x59cb6fc03255 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1163:10
    #50 0x59cb6fbfd8b7 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:354:36
    #51 0x59cb6fbfdddb in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:367:10
    #52 0x59cb5e0c0a0a in ChromeMain chrome/app/chrome_main.cc:222:12
    #53 0x799c0862a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #54 0x799c0862a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #55 0x59cb5dfe5029 in _start (/home/user/Downloads/linux-release-1397153/chrome+0xedf6029) (BuildId: c16d633d3fb88166)

0x767c067175a0 is located 0 bytes after 160-byte region [0x767c06717500,0x767c067175a0)
allocated by thread T0 (chrome) here:
    #0 0x59cb5e0be2ed in operator new[](unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x759bfe29a5f4 in brw_fs_opt_register_coalesce(fs_visitor&) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs_register_coalesce.cpp:238:20
    #2 0x759bfe284e52 in brw_fs_optimize(fs_visitor&) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs_opt.cpp:117:7
    #3 0x759bfe1bfbff in fs_visitor::run_fs(bool, bool) /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs.cpp:3285:7
    #4 0x759bfe1c4290 in brw_compile_fs /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs.cpp:3944:17
    #5 0x759bfd3289af in anv_pipeline_compile_fs /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:1636:21
    #6 0x759bfd3289af in anv_graphics_pipeline_compile /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:2515:10
    #7 0x759bfd3141fd in anv_graphics_pipeline_create /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:3273:13
    #8 0x759bfd3141fd in anv_CreateGraphicsPipelines /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:3333:16
    #9 0x59cb6173f31c in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:609:9
    #10 0x59cb6150196a in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:395:5
    #11 0x59cb614340e9 in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2180:51
    #12 0x59cb61433aea in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1473:26
    #13 0x59cb7c33822f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:306:9
    #14 0x59cb7c32acbc in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:583:9
    #15 0x59cb7c330492 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1635:30
    #16 0x59cb7c2f2070 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1067:33
    #17 0x59cb7c2f2503 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2010:22
    #18 0x59cb7c2e43b3 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1955:18
    #19 0x59cb7c200f77 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:263:35
    #20 0x59cb7c1f047a in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:489:22
    #21 0x59cb7c1efcb4 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:157:7
    #22 0x59cb7c20c91b in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:958:13
    #23 0x59cb7c21c48e in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:738:12
    #24 0x59cb7c21c25f in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:954:5
    #25 0x59cb7c21c25f in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1067:14
    #26 0x59cb7c21c25f in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:980:12
    #27 0x59cb787b9c7d in Run base/functional/callback.h:156:12
    #28 0x59cb787b9c7d in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:813:49
    #29 0x59cb787b9c7d in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:930:12
    #30 0x59cb787b9c7d in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1067:14
    #31 0x59cb78796708 in Run base/functional/callback.h:156:12
    #32 0x59cb78796708 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:675:29
    #33 0x59cb78794877 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:599:3
    #34 0x59cb78798073 in Invoke<void (gpu::Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:738:12
    #35 0x59cb78798073 in MakeItSo<void (gpu::Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:930:12
    #36 0x59cb78798073 in RunImpl<void (gpu::Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1067:14
    #37 0x59cb78798073 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #38 0x59cb72ba3432 in Run base/functional/callback.h:156:12
    #39 0x59cb72ba3432 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:208:34
    #40 0x59cb72c10478 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:11)> base/task/common/task_annotator.h:106:5
    #41 0x59cb72c10478 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:471:23
    #42 0x59cb72c0f21a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332:40

SUMMARY: AddressSanitizer: heap-buffer-overflow /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_fs_register_coalesce.cpp:275:14 in brw_fs_opt_register_coalesce(fs_visitor&)
Shadow bytes around the buggy address:
  0x767c06717300: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x767c06717380: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x767c06717400: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x767c06717480: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
  0x767c06717500: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x767c06717580: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x767c06717600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x767c06717680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x767c06717700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x767c06717780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x767c06717800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==13824==ADDITIONAL INFO

==13824==Note: Please include this section with the ASan report.
Task trace:
    #0 0x59cb78794cb6 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:615:27
    #1 0x59cb78790072 in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*) gpu/command_buffer/service/scheduler.cc:417:29

Command line: `/proc/self/exe --type=gpu-process --no-sandbox --use-angle=vulkan --string-annotations --crashpad-handler-pid=13781 --enable-crash-reporter=, --user-data-dir=/tmp/deleteme --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAoAAAEAAAAAAAAAAAAAAAAAADAAAIAAAACAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAAAQAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,7355950764304781472,8327999700532085311,262144 --field-trial-handle=3,i,8161328738629070096,17794170914092561336,262144 --enable-features=Vulkan --disable-features=EyeDropper --variations-seed-version`

==13824==END OF ADDITIONAL INFO

```

When running with debug asserts enabled, the shader compilation instead aborts with `../src/intel/compiler/brw_fs_opt_virtual_grfs.cpp:128: bool brw_fs_opt_split_virtual_grfs(fs_visitor &): Assertion offset <= MAX_VGRF_SIZE(s.devinfo) failed.`

The gfxrecon capture can be replayed with:
`INTEL_STUB_GPU_PLATFORM=cml VK_DRIVER_FILES=~/chromeosMesaOrg/buildAsserts/src/intel/vulkan/intel_icd.x86_64.json ~/gfxreconstruct/build/linux/x64/output/bin/gfxrecon-replay gfxrecon_capture_20241217T142120.gfxr`

## Attachments

- [brw_fs_opt_split_virtual_grfs.html](attachments/brw_fs_opt_split_virtual_grfs.html) (text/html, 3.6 KB)
- [gfxrecon_capture_20241217T134513.gfxr](attachments/gfxrecon_capture_20241217T134513.gfxr) (application/octet-stream, 8.0 KB)
- [gfxrecon_capture_20250322T211754.gfxr](attachments/gfxrecon_capture_20250322T211754.gfxr) (application/octet-stream, 12.7 KB)

## Timeline

### a7...@gmail.com (2024-12-17)

Upstream report: <https://gitlab.freedesktop.org/mesa/mesa/-/issues/12324>

### dc...@chromium.org (2024-12-18)

I am tentatively tagging this as CrOS-only based off:

> The Mesa version is the one used by ChromeOS (which, in contrast to other versions of Linux, enables WebGPU).

But I don't know how true this statement is, nor if there's some workaround we could land in Chrome.

### pe...@google.com (2025-01-01)

cwallez: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ds...@chromium.org (2025-01-06)

@msturner, are you the correct person to send these Mesa issues too?

### ms...@google.com (2025-01-06)

Yes. I'll have a look.

### ms...@google.com (2025-01-17)

I haven't been able to reproduce this from the gfxreconstruct trace.

I've tried on RPL and WHL (essentially the same as CML):

```
00:02.0 VGA compatible controller [0300]: Intel Corporation Raptor Lake-P [Iris Xe Graphics] [8086:a7a0] (rev 04)

```
```
00:02.0 VGA compatible controller [0300]: Intel Corporation WhiskeyLake-U GT2 [UHD Graphics 620] [8086:3ea0] (rev 02)

```

On my WHL system:

```
$ INTEL_DEBUG=fs,vs,cs MESA_SHADER_CACHE_DISABLE=1 ASAN_OPTIONS=detect_leaks=0,abort_on_error=1 mesa-debug-asan gfxrecon-replay gfxrecon_capture_20241217T134513.gfxr
[gfxrecon] WARNING - Skipping unrecognized meta-data block with type 32
../src/intel/vulkan/anv_device.c:3070:37: runtime error: member access within null pointer of type 'struct anv_instance'
../src/intel/perf/intel_perf.c:1550:4: runtime error: null pointer passed as argument 1, which is declared to never be null
[gfxrecon] WARNING - Incomplete block at end of file
File did not contain any frames

```

If the trace compiled any shaders, I'd expect to see them printed with `INTEL_DEBUG=fs,vs,cs` set. And if I run it under gdb and set a breakpoint on `brw_compact_instructions`, it's never hit.

Can you reproduce the issue with this trace?

### pe...@google.com (2025-02-07)

a72827312: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ph...@google.com (2025-02-17)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### am...@chromium.org (2025-03-04)

Hi msturner@ I'm going to have to temporarily assign this issue back to you because it can't be assigned to the external reporter.

I am however applying a needs-feedback tag and a next action date.
OP, while we appreciate the report here, there are some issues with getting this reproduced and we're unable to make any headway. Can you pease provide any additional information here?
If this can't be reproduced by us, given the amount of time this has been open without a successful production, we'll probably need to close this out as a WontFix without further information.

This is unfortunately, because by all measures this does seem to be a valid issue, but if we're unable to reproduce, there's not much more we can do.

### pe...@google.com (2025-03-19)

The NextAction date has arrived: 2025-03-19
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### a7...@gmail.com (2025-03-23)

I'm so sorry it took so long for me to respond; I missed the question in [comment #7](https://issues.chromium.org/issues/384531062#comment7) and had plenty of other things going on. I finally found some time yesterday to investigate and would like to share the results: \

For whatever reason, I can't get the `.gfxr` from [comment #1](https://issues.chromium.org/issues/384531062#comment1) to reproduce on the indicated commit (fbafe569775) anymore. So, at least we're seeing consistent results... Anyways, the fuzzers are still regularly finding the crash, even on the most current version of Mesa (25.0.2). Hence, I created a new `.gfxr` record. I tested this trace with both Mesa 25.0.2 (commit 06631a88764) and the commit initially reported (fbafe569775). On both versions of Mesa, this should, depending on your compile options, result in an ASAN violation or assertion violation. The shader is not yet minimized; assuming you can replay it, I'll promptly provide another trace with a minimized shader.

### pe...@google.com (2025-03-23)

Thank you for providing more feedback. Adding the requester to the CC list.

### ms...@google.com (2025-04-01)

Thanks, I'll have another look.

### ms...@google.com (2025-04-03)

I can reproduce an assertion failure with this trace. Thank you!

```
mattst88@framework ~ $ MESA_SHADER_CACHE_DISABLE=1 ASAN_OPTIONS=detect_leaks=0,abort_on_error=1 mesa-debug-asan gfxrecon-replay gfxrecon_capture_20250322T211754.gfxr
[gfxrecon] WARNING - The replay device differs from the original capture device; replay may fail due to device incompatibilities:
[gfxrecon] WARNING -   Capture device info:     [vendorID = 0x8086, deviceId = 0x9b41, deviceName = Intel(R) UHD Graphics (CML GT2)]
[gfxrecon] WARNING -   Replay device info:      [vendorID = 0x8086, deviceId = 0xa7a0, deviceName = Intel(R) Iris(R) Xe Graphics (RPL-P)]
SPIR-V WARNING:
    In file ../src/compiler/spirv/spirv_to_nir.c:4974
    Unsupported SPIR-V capability: SpvCapabilityShader (1)
    20 bytes into the SPIR-V binary
gfxrecon-replay: ../src/intel/compiler/brw_opt_virtual_grfs.cpp:129: bool brw_opt_split_virtual_grfs(brw_shader&): Assertion `offset <= MAX_VGRF_SIZE(s.devinfo)' failed.
[1]    1002735 IOT instruction (core dumped)  MESA_SHADER_CACHE_DISABLE=1 ASAN_OPTIONS=detect_leaks=0,abort_on_error=1

```

### ms...@google.com (2025-04-03)

The assertion failure doesn't happen with `INTEL_DEBUG=no32`. The program is compiled to SIMD8 and SIMD16 successfully.

### ms...@google.com (2025-04-08)

I posted the new gfxreconstruct trace up on the upstream gitlab and Caio from Intel understands what's wrong and is investigating possible solutions (<https://gitlab.freedesktop.org/mesa/mesa/-/issues/12324>).

### ms...@google.com (2025-04-11)

Intel has provided a fix here: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/34461>

I've reviewed it and tested to confirm that it resolves the issue. I'll cherry pick the patches as soon as they're upstream.

### ms...@google.com (2025-04-15)

4 CLs opened, starting with [crrev/c/6457668](https://crrev.com/c/6457668)

### dx...@google.com (2025-04-16)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Kenneth Graunke [kenneth@whitecape.org](mailto:kenneth@whitecape.org)  

Link:      <https://chromium-review.googlesource.com/6457668>

BACKPORT: brw: Track the largest VGRF size in liveness analysis

---


Expand for full commit details
```
     
    We're already looking at this data to calculate the per-component 
    vars_from_vgrf[] and vgrf_from_vars[] mappings, so just record the 
    largest VGRF size while we're here.  This will allow passes to size 
    arrays based on the actual size needed, rather than hardcoding some 
    fixed size.  In many cases, MAX_VGRF_SIZE(devinfo) is larger than 
    necessary, because e.g. vec5 sparse sampling results aren't used. 
    Not hardcoding this means we can also temporarily handle very large 
    VGRFs which we know will be split eventually, without having to 
    increase the maximum which is ultimately used for RA classes. 
     
    Cc: mesa-stable 
    Reviewed-by: Matt Turner <mattst88@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/34461> 
     
    (cherry picked from commit ea468412f672b07d498af9a910bf5047106f6d84 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    Conflicts: 
       src/intel/compiler/brw_analysis.h 
     
    BUG=b:384531062 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I97ed11ba6abc185b648abe0b14155686f4907523 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6457668 
    Tested-by: Matt Turner <msturner@google.com> 
    Reviewed-by: Juston Li <justonli@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Commit-Queue: Matt Turner <msturner@google.com>

```

---

Files:

- M `src/intel/compiler/brw_fs_live_variables.cpp`
- M `src/intel/compiler/brw_fs_live_variables.h`

---

Hash: 3ed720c0eb8116e18f561c130ca63466ab73e4bd  

Date:  Wed Apr 9 23:02:25 2025


---

### dx...@google.com (2025-04-16)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Kenneth Graunke [kenneth@whitecape.org](mailto:kenneth@whitecape.org)  

Link:      <https://chromium-review.googlesource.com/6457669>

BACKPORT: brw: Use live->max\_vgrf\_size in register coalescing

---


Expand for full commit details
```
     
    We already require liveness, so just use the actual maximum size we saw 
    instead of a hardcoded pessimal size. 
     
    Cc: mesa-stable 
    Reviewed-by: Matt Turner <mattst88@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/34461> 
     
    (cherry picked from commit 4b27b5895c9ef8a597c061e3b5fdf15e1424cc22 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    Conflicts: 
       src/intel/compiler/brw_fs_register_coalesce.cpp 
     
    BUG=b:384531062 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: Ibb255af19fd746a1fc281f8e4acfc13bb22d2610 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6457669 
    Reviewed-by: Juston Li <justonli@google.com> 
    Commit-Queue: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Tested-by: Matt Turner <msturner@google.com>

```

---

Files:

- M `src/intel/compiler/brw_fs_register_coalesce.cpp`

---

Hash: 1114d26473f548a9f4f878b8aeefef49750c7287  

Date:  Wed Apr 9 23:03:47 2025


---

### dx...@google.com (2025-04-16)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Kenneth Graunke [kenneth@whitecape.org](mailto:kenneth@whitecape.org)  

Link:      <https://chromium-review.googlesource.com/6457670>

BACKPORT: brw: Use live->max\_vgrf\_size in pre-RA scheduling

---


Expand for full commit details
```
     
    Post-RA scheduling doesn't use liveness analysis, so we continue using 
    MAX_VGRF_SIZE(devinfo).  But for pre-RA scheduling, we now use 
    live->max_vgrf_size. 
     
    This helps get us to a place where we can emit arbitrarily large VGRFs 
    early on in compilation, but which will be split and cleaned up prior to 
    register allocation.  It may also allocate smaller arrays in practice 
    since MAX_VGRF_SIZE(devinfo) assumes the worst case scenario for things 
    we actually could need to allocate. 
     
    Cc: mesa-stable 
    Reviewed-by: Matt Turner <mattst88@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/34461> 
     
    (cherry picked from commit a45583f07812015fdcd83257645cb17b2285a456 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    Conflicts: 
       src/intel/compiler/brw_schedule_instructions.cpp 
     
    BUG=b:384531062 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I031629771d191d44c63a276e8b363e675de8b9e4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6457670 
    Reviewed-by: Juston Li <justonli@google.com> 
    Tested-by: Matt Turner <msturner@google.com> 
    Commit-Queue: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com>

```

---

Files:

- M `src/intel/compiler/brw_schedule_instructions.cpp`

---

Hash: dec4ccb84abd0a302c7bfc2f3f2c42a80cdc6e6f  

Date:  Wed Apr 9 23:04:26 2025


---

### dx...@google.com (2025-04-16)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Kenneth Graunke [kenneth@whitecape.org](mailto:kenneth@whitecape.org)  

Link:      <https://chromium-review.googlesource.com/6457671>

BACKPORT: brw: Don't assert about MAX\_VGRF\_SIZE in brw\_opt\_split\_virtual\_grfs()

---


Expand for full commit details
```
     
    This allows us to create temporary VGRFs that are larger than 
    MAX_VGRF_SIZE(devinfo), which will be split eventually.  They may not 
    be split on the initial pass, because we may need LOAD_PAYLOAD lowering, 
    copy propagation, and so on to occur first.  So we allow registers to 
    exceed that size initially. 
     
    The "Register allocation relies on split_virtual_grfs()" assertion in 
    brw_reg_allocate.cpp still asserts that all VGRFs which reach the 
    register allocator have been properly split. 
     
    One case where this is useful is for vectorizing convergent block loads. 
    We create temporaries to splat the SIMD1 values out to SIMD(N), which 
    can lead to some very large temporaries.  However, copy propagation and 
    so on ultimately eliminate these and they'll get split down to proper 
    sizes or elided entirely in the end. 
     
    (Note: both this and the prior commits from this merge request are 
     needed to close the linked issue.) 
     
    Cc: mesa-stable 
    Reviewed-by: Matt Turner <mattst88@gmail.com> 
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/12324 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/34461> 
     
    (cherry picked from commit eb1ec9cf8e6f62f0664bb9886ac6c35b35cebc6b 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    Conflicts: 
       src/intel/compiler/brw_fs_opt_virtual_grfs.cpp 
     
    BUG=b:384531062 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: Ifa7aaa9e72514b590cdf33ad50c62f043cc5d962 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6457671 
    Reviewed-by: Juston Li <justonli@google.com> 
    Commit-Queue: Matt Turner <msturner@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Tested-by: Matt Turner <msturner@google.com>

```

---

Files:

- M `src/intel/compiler/brw_fs_opt_virtual_grfs.cpp`

---

Hash: 590b5a90021e5ab06df5e44fa65f6ed1aaae209e  

Date:  Wed Apr 9 23:19:18 2025


---

### ch...@google.com (2025-04-16)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ms...@google.com (2025-04-16)

I am unsure how to handle that request. Assigning to Amy.

### ms...@google.com (2025-04-16)

Oh, looking at [b/408364839](https://issues.chromium.org/issues/408364839) `Found In` appears to simply be what version this issue was originally discovered in.

### sp...@google.com (2025-05-28)

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

### am...@chromium.org (2025-05-28)

Apologies for letting this one fall though the cracks and the delay in rewarding it. Since it was tagged as CrOS, it slipped though our automation. Thank you for your patience!

### ch...@google.com (2025-07-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a highly privileged process (GPU)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/384531062)*
