# GPU process crash via WebGPU shader (Linux): OOB in mark_src_live mesa/src/compiler/nir/nir_opt_dce.c:39:9

| Field | Value |
|-------|-------|
| **Issue ID** | [359909532](https://issues.chromium.org/issues/359909532) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>WebGPU |
| **Platforms** | Linux |
| **Reporter** | wg...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2024-08-15 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

The following vulnerabilitiy describes an issue in Mesa, reachable via WebGPU shaders on Linux. I'm aware that WebGPU is not yet enabled by default on Linux, so just let me know if this type of issue is not yet in scope. If such issues are in scope but only on some specific version of Mesa I'm happy to fuzz this version instead.

While the attached testcase reproduces in Chromium, reproducing outside the browser is non-trivial. If you don't yet have a proper setup for investigating such issues I can provide a variant of my fuzzing harness (patched dawn + patched mesa). These patches have *not* been applied when reproducing the issue in chromium.

##### VERSION

Chrome Version 129.0.6659.0 (Developer Build) (64-bit) (precompiled ASAN)   

Operating System: Ubuntu 24.04   

Mesa: TOT (commit a1a06f386e8a317e02b430ff3860ee21f6c4149b)

##### REPRODUCTION CASE

Start an ASAN build of Chromium which uses an ASAN build of Mesa. There are a couple of non-standard flags (in particular, enabling WebGPU on Ubuntu):

`VK_DRIVER_FILES=mesa/buildASAN/src/intel/vulkan/intel_icd.x86_64.json ./chrome --use-angle=vulkan --enable-features=Vulkan --disable-gpu-watchdog --no-sandbox --enable-unsafe-webgpu`

Opening the attached html triggers an OOB access. The fragment shader is the interesting one, the vertex shader is just part of the surrounding html.

```
[4009473:4009500:0815/100238.659469:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.Notifications.GetCapabilities: object_path= /org/freedesktop/Notifications: org.freedesktop.DBus.Error.NoReply: Message recipient disconnected from message bus without replying
=================================================================
==4009577==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x506000246840 at pc 0x711af527ccee bp 0x7fffe6511f30 sp 0x7fffe6511f28
READ of size 4 at 0x506000246840 thread T0 (chrome)
    #0 0x711af527cced in mark_src_live mesa/buildASAN/../src/compiler/nir/nir_opt_dce.c:39:9
    #1 0x711af527cced in dce_cf_list mesa/buildASAN/../src/compiler/nir/nir_opt_dce.c:165:10
    #2 0x711af527c48f in dce_cf_list mesa/buildASAN/../src/compiler/nir/nir_opt_dce.c:164:22
    #3 0x711af527c620 in dce_cf_list mesa/buildASAN/../src/compiler/nir/nir_opt_dce.c:191:13
    #4 0x711af527c476 in dce_cf_list mesa/buildASAN/../src/compiler/nir/nir_opt_dce.c:163:22
    #5 0x711af527b0f9 in nir_opt_dce_impl mesa/buildASAN/../src/compiler/nir/nir_opt_dce.c:234:20
    #6 0x711af527b0f9 in nir_opt_dce mesa/buildASAN/../src/compiler/nir/nir_opt_dce.c:254:11
    #7 0x711af561fac1 in brw_nir_optimize mesa/buildASAN/../src/intel/compiler/brw_nir.c:831:10
    #8 0x711af5620146 in brw_preprocess_nir mesa/buildASAN/../src/intel/compiler/brw_nir.c:1084:4
    #9 0x711af451ee0f in anv_pipeline_nir_preprocess mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2111:4
    #10 0x711af4526ec9 in anv_graphics_pipeline_compile mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2329:7
    #11 0x711af45155cd in anv_graphics_pipeline_create mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:3282:13
    #12 0x711af45155cd in anv_CreateGraphicsPipelines mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:3342:16
    #13 0x6164268473af in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:587:9
    #14 0x616426607a00 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:371:12
    #15 0x616426543697 in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2245:51
    #16 0x6164265430dc in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1556:26
    #17 0x61643ef9dd8f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:469:9
    #18 0x61643ef8e7ac in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:716:9
    #19 0x61643ef9535f in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:2056:30
    #20 0x61643ef575d0 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1043:33
    #21 0x61643ef57a63 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1948:22
    #22 0x61643ef49673 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1893:18
    #23 0x61643ee65087 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:231:35
    #24 0x61643ee55390 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:502:22
    #25 0x61643ee54913 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:153:7
    #26 0x61643ee70af1 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long) gpu/ipc/service/gpu_channel.cc:932:13
    #27 0x61643ee7ff18 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&) base/functional/bind_internal.h:738:12
    #28 0x61643ee7fce0 in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long> > base/functional/bind_internal.h:954:5
    #29 0x61643ee7fce0 in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1067:14
    #30 0x61643ee7fce0 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #31 0x61643ba24680 in Run base/functional/callback.h:156:12
    #32 0x61643ba24680 in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler_dfs.cc:598:24
    #33 0x61643ba22288 in gpu::SchedulerDfs::RunNextTask() gpu/command_buffer/service/scheduler_dfs.cc:522:3
    #34 0x61643ba26104 in Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs *> base/functional/bind_internal.h:738:12
    #35 0x61643ba26104 in MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:930:12
    #36 0x61643ba26104 in RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1067:14
    #37 0x61643ba26104 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #38 0x6164367ba7d4 in Run base/functional/callback.h:156:12
    #39 0x6164367ba7d4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #40 0x6164368228e6 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> base/task/common/task_annotator.h:90:5
    #41 0x6164368228e6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #42 0x61643682167a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #43 0x61643682364a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #44 0x616436989a89 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:694:48
    #45 0x61643682429a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #46 0x6164367495cf in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #47 0x61644d2b8cc3 in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:431:14
    #48 0x616433dba92e in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:703:14
    #49 0x616433dbb82d in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:807:12
    #50 0x616433dbe0c7 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1175:10
    #51 0x616433db8d3a in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:333:36
    #52 0x616433db932b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:346:10
    #53 0x616423257203 in ChromeMain chrome/app/chrome_main.cc:230:12
    #54 0x711aff42a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #55 0x711aff42a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #56 0x616423182029 in _start (/home/user/Downloads/linuxasan1342140/chrome+0xf514029) (BuildId: 8e8d1dc1bb334b1d)

0x506000246840 is located 0 bytes after 64-byte region [0x506000246800,0x506000246840)
allocated by thread T0 (chrome) here:
    #0 0x61642321e1af in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:68:3
    #1 0x711af4dfa77f in ralloc_size mesa/buildASAN/../src/util/ralloc.c:118:18
    #2 0x711af4dfa77f in rzalloc_size mesa/buildASAN/../src/util/ralloc.c:152:16
    #3 0x711af4dfa77f in rzalloc_array_size mesa/buildASAN/../src/util/ralloc.c:232:11
    #4 0x711af527b08a in nir_opt_dce_impl mesa/buildASAN/../src/compiler/nir/nir_opt_dce.c:226:29
    #5 0x711af527b08a in nir_opt_dce mesa/buildASAN/../src/compiler/nir/nir_opt_dce.c:254:11
    #6 0x711af561fac1 in brw_nir_optimize mesa/buildASAN/../src/intel/compiler/brw_nir.c:831:10
    #7 0x711af5620146 in brw_preprocess_nir mesa/buildASAN/../src/intel/compiler/brw_nir.c:1084:4
    #8 0x711af451ee0f in anv_pipeline_nir_preprocess mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2111:4
    #9 0x711af4526ec9 in anv_graphics_pipeline_compile mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2329:7
    #10 0x711af45155cd in anv_graphics_pipeline_create mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:3282:13
    #11 0x711af45155cd in anv_CreateGraphicsPipelines mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:3342:16
    #12 0x6164268473af in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:587:9
    #13 0x616426607a00 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:371:12
    #14 0x616426543697 in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2245:51
    #15 0x6164265430dc in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1556:26
    #16 0x61643ef9dd8f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:469:9
    #17 0x61643ef8e7ac in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:716:9
    #18 0x61643ef9535f in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:2056:30
    #19 0x61643ef575d0 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1043:33
    #20 0x61643ef57a63 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1948:22
    #21 0x61643ef49673 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1893:18
    #22 0x61643ee65087 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:231:35
    #23 0x61643ee55390 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:502:22
    #24 0x61643ee54913 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:153:7
    #25 0x61643ee70af1 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long) gpu/ipc/service/gpu_channel.cc:932:13
    #26 0x61643ee7ff18 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&) base/functional/bind_internal.h:738:12
    #27 0x61643ee7fce0 in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long> > base/functional/bind_internal.h:954:5
    #28 0x61643ee7fce0 in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1067:14
    #29 0x61643ee7fce0 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #30 0x61643ba24680 in Run base/functional/callback.h:156:12
    #31 0x61643ba24680 in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler_dfs.cc:598:24
    #32 0x61643ba22288 in gpu::SchedulerDfs::RunNextTask() gpu/command_buffer/service/scheduler_dfs.cc:522:3
    #33 0x61643ba26104 in Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs *> base/functional/bind_internal.h:738:12
    #34 0x61643ba26104 in MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:930:12
    #35 0x61643ba26104 in RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1067:14
    #36 0x61643ba26104 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #37 0x6164367ba7d4 in Run base/functional/callback.h:156:12
    #38 0x6164367ba7d4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #39 0x6164368228e6 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> base/task/common/task_annotator.h:90:5
    #40 0x6164368228e6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #41 0x61643682167a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40

SUMMARY: AddressSanitizer: heap-buffer-overflow mesa/buildASAN/../src/compiler/nir/nir_opt_dce.c:39:9 in mark_src_live
Shadow bytes around the buggy address:
  0x506000246580: fd fd fd fd fa fa f7 fa 00 00 00 00 00 00 00 00
  0x506000246600: fa fa f7 fa 00 00 00 00 00 00 00 00 fa fa f7 fa
  0x506000246680: 00 00 00 00 00 00 00 00 fa fa f7 fa 00 00 00 00
  0x506000246700: 00 00 00 00 fa fa f7 fa fd fd fd fd fd fd fd fd
  0x506000246780: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
=>0x506000246800: 00 00 00 00 00 00 00 00[fa]fa fa fa fa fa fa fa
  0x506000246880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x506000246900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x506000246980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x506000246a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x506000246a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==4009577==ADDITIONAL INFO

==4009577==Note: Please include this section with the ASan report.
Task trace:
    #0 0x61643ba22795 in gpu::SchedulerDfs::RunNextTask() gpu/command_buffer/service/scheduler_dfs.cc:538:27
    #1 0x61643ba1dc49 in gpu::SchedulerDfs::TryScheduleSequence(gpu::SchedulerDfs::Sequence*) gpu/command_buffer/service/scheduler_dfs.cc:340:11


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --use-angle=vulkan --string-annotations --crashpad-handler-pid=4009475 --enable-crash-reporter=, --no-subproc-heap-profiling --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAoAAAEAAAAAAAAAAAAAAAAAABgAAIAAAACAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,17237863391721455418,1904573532517946590,262144 --field-trial-handle=3,i,16993049197961748657,9709463668740412786,262144 --enable-features=Vulkan --disable-features=EyeDropper --variations-seed-version`


==4009577==END OF ADDITIONAL INFO
==4009577==ABORTING

```

When enabling assers in Mesa, the following is triggered instead of reaching the ASAN violation: `chrome: ../src/compiler/nir/nir_control_flow.c:592: nir_cursor stitch_blocks(nir_block *, nir_block *): Assertion` exec\_list\_is\_empty(&after->instr\_list)' failed.`

## Attachments

- [exec_list_is_empty.html](attachments/exec_list_is_empty.html) (text/html, 3.0 KB)
- [Dockerfile](attachments/Dockerfile) (application/octet-stream, 1.4 KB)
- [gfxrecon_capture_20240815T130508.gfxr](attachments/gfxrecon_capture_20240815T130508.gfxr) (application/octet-stream, 326.4 KB)

## Timeline

### wg...@gmail.com (2024-08-15)

Forgot to upload the reproducer

### ad...@google.com (2024-08-15)

Thanks.

Security shepherd here: I'm tagging this with `Security_Impact-None` because it doesn't yet affect production Chrome. We [don't consider the GPU process sandboxed on Linux](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/process-sandboxes-by-platform.md) which means this is a straight-from-web-content-to-sandbox-escape bug, i.e. S0.

### ad...@google.com (2024-08-15)

NB I haven't attempted to:

- upload this to ClusterFuzz, because we don't have a mesa ASAN build up there
- reproduce this locally, because I don't know how to build an ASAN build of mesa. I'm sure I could figure it out, but I have little doubt that this is a real bug, so I'm not sure it adds much value for me to reproduce this.

Reporter, if you wouldn't mind listing the steps by which you built your ASAN mesa build, that might save us a bit of time. Thanks!

### wg...@gmail.com (2024-08-15)

Attached a Dockerfile, copy it to an otherwise empyt directoy, cd into the directory and build with `docker build -t dockermesa .`

The image contains `/build/mesa/buildASAN/src/intel/vulkan/libvulkan_intel.so` and `/build/mesa/buildASAN/src/intel/vulkan/intel_icd.x86_64.json`. Now copy these two files to the host system. You have to modify the `intel_icd.x86_64.json` s.t. the path the `libvulkan_intel.so` is correct. You can now start an ASAN build of chromium with the ASAN Mesa if you set the environment variable `VK_DRIVER_FILES=/path/to/intel_icd.x86_64.json`. Note that you cannot use a non-ASAN build of chromium because `libvulkan_intel.so` requires the ASAN symbols (exported by ASAN chromium).

Assuming you're on a device with an Intel GPU, opening the above html should trigger the ASAN violation.

### wg...@gmail.com (2024-08-15)

Quick question: is the code path WebGPU -> Mesa reachable on ChromeOS? I don't have such a device for testing; but its based on Linux and according to <https://github.com/gpuweb/gpuweb/wiki/Implementation-Status> WebGPU is enabled by default.

### ad...@google.com (2024-08-15)

That is a good question. amaiorano@ do you know? If so I'm afraid we have to remove `Security_Impact-None` from this, although as we [trust the ChromeOS sandbox](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/process-sandboxes-by-platform.md) we'd probably bump it down to S1 at the same time (probably. It's a slightly weird situation).

### am...@google.com (2024-08-15)

Am less familiar with WebGPU on ChromeOS. jrprice@ might know.

### jr...@google.com (2024-08-15)

Yes, WebGPU is used in production on ChromeOS and I believe Mesa is the only GPU driver used on ChromeOS. We'd need to do some investigation to figure out if the issue is present in a version of Mesa that has been shipped.

### wg...@gmail.com (2024-08-15)

While you're at it, could you let me know the most interesting Mesa version to fuzz (from a ChromeOS perspective)? Neither do I want to waste your time reporting bugs in outdated versions nor by reporting bugs in commits not yet been shipped to ChromeOS.

### ro...@google.com (2024-08-15)

So, `exec_list_is_empty(&after->instr_list)` is maybe unrelated. I can reproduce that on a non-intel driver. I have not been able to reproduce the out of bounds access in `mark_src_live()`.. I'm on different hw, but it is an opt pass shared by all the mesa drivers.

gfxreconstruct which reproduces this is attached. (But it is hit or miss whether a gfxreconstruct trace captured on one driver can replay on another.)

edit: I can reproduce the OOB now. It may be fallout from the unhandled case in nir\_flow\_control after all

### ro...@google.com (2024-08-16)

upstream fix: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/30702>

### ro...@google.com (2024-08-16)

- olv for mesa-radv
- msturner for mesa-iris

The commit which introduced the bug landed after 24.1 branchpoint so AMD and intel are not currently affected. But you should ensure the fix has landed in 24.2 branch before uprev'ing.

The commit which introduced the bug is currently in mesa-freedreno, I will cherry-pick the fix once it has been reviewed and merged upstream.

### ol...@google.com (2024-08-16)

Thanks for the heads up. Should the fix have a `Fixes` tag so that it can cherry-picked to 24.2?

### ro...@google.com (2024-08-16)

> Should the fix have a Fixes tag so that it can cherry-picked to 24.2?

yeah, I added one and re-pushed but didn't update the MR description

### wg...@gmail.com (2024-08-17)

So the most relevant mesa version (for fuzzing) is the one in chromiumos/third\_party/mesa on branch chromeos-iris, as this is the version that is used by chromeos with WebGPU enabled?

### ro...@google.com (2024-08-19)

> So the most relevant mesa version (for fuzzing) is the one in chromiumos/third\_party/mesa on branch chromeos-iris, as this is the version that is used by chromeos with WebGPU enabled?

correct, or chromeos-radv for AMD

### ap...@google.com (2024-08-19)

Project: chromiumos/third_party/mesa
Branch: chromeos-freedreno

commit 0c091bcc8b419ea60868153a8647773d27ecd2b6
Author: Rob Clark <robdclark@chromium.org>
Date:   Fri Aug 16 14:15:49 2024

    UPSTREAM: nir/opt_loop: Don't peel initial break if loop ends in break
    
    A loop that looks like:
    
       loop {
          do_work_1();
          if (cond) {
             break;
          } else {
          }
          do_work_2();
          break;
       }
    
    We can't pull that break ahead of do_work_1() after hoisting the initial
    do_work_1() out of the loop.  So bail in this case.
    
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/11711
    Fixes: 6b4b04473986 ("nir/opt_loop: add loop peeling optimization")
    Signed-off-by: Rob Clark <robdclark@chromium.org>
    Reviewed-by: Alyssa Rosenzweig <alyssa@rosenzweig.io>
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/30702>
    (cherry picked from commit 563ec4754aef34f8707cccbb01ec8dac29a0c0e3)
    
    BUG=b:359909532
    TEST=boot wormdingler
    
    Change-Id: Iea9a0979c394ebace7b6b8b385ae9b9bf56e62c5
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5797842
    Reviewed-by: Sean Paul <sean@poorly.run>
    Reviewed-by: Chia-I Wu <olv@google.com>
    Commit-Queue: Chia-I Wu <olv@google.com>
    Auto-Submit: Rob Clark <robdclark@chromium.org>
    Commit-Queue: Rob Clark <robdclark@chromium.org>
    Tested-by: Rob Clark <robdclark@chromium.org>

M       src/compiler/nir/nir_opt_loop.c

https://chromium-review.googlesource.com/5797842


### ap...@google.com (2024-08-19)

Project: chromiumos/third_party/mesa
Branch: chromeos-iris

commit 51ef6de2af3f5e5bb926d462ad40a86ecda5c8aa
Author: Rob Clark <robdclark@chromium.org>
Date:   Fri Aug 16 14:15:49 2024

    UPSTREAM: nir/opt_loop: Don't peel initial break if loop ends in break
    
    A loop that looks like:
    
       loop {
          do_work_1();
          if (cond) {
             break;
          } else {
          }
          do_work_2();
          break;
       }
    
    We can't pull that break ahead of do_work_1() after hoisting the initial
    do_work_1() out of the loop.  So bail in this case.
    
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/11711
    Fixes: 6b4b04473986 ("nir/opt_loop: add loop peeling optimization")
    Signed-off-by: Rob Clark <robdclark@chromium.org>
    Reviewed-by: Alyssa Rosenzweig <alyssa@rosenzweig.io>
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/30702>
    (cherry picked from commit 563ec4754aef34f8707cccbb01ec8dac29a0c0e3
     https://gitlab.freedesktop.org/mesa/mesa.git main)
    
    BUG=b:359909532
    TEST=Run crafted SPIR-V shader without crashing
    
    Change-Id: I01e36bfa38500b6fc34854e55112cf1e52f5efa1
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5796383
    Tested-by: Matt Turner <msturner@google.com>
    Reviewed-by: Sean Paul <sean@poorly.run>
    Reviewed-by: Chia-I Wu <olv@google.com>
    Commit-Queue: Matt Turner <msturner@google.com>
    Auto-Submit: Matt Turner <msturner@google.com>
    Commit-Queue: Chia-I Wu <olv@google.com>

M       src/compiler/nir/nir_opt_loop.c

https://chromium-review.googlesource.com/5796383


### ro...@google.com (2024-08-28)

fixes are in ToT everywhere that they were needed, I believe

### sp...@google.com (2024-09-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
baseline report of memory corruption a highly-privileged process (GPU)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-04)

Congratulations! Thank you for your efforts and reporting this issue to us!

### ap...@google.com (2024-09-17)

Project: chromiumos/third_party/mesa
Branch: chromeos-iris

commit cd8abccde6f03a1da369575168d40307744b3c4d
Author: Rob Clark <robdclark@chromium.org>
Date:   Fri Aug 16 14:15:49 2024

    UPSTREAM: nir/opt_loop: Don't peel initial break if loop ends in break
    
    A loop that looks like:
    
       loop {
          do_work_1();
          if (cond) {
             break;
          } else {
          }
          do_work_2();
          break;
       }
    
    We can't pull that break ahead of do_work_1() after hoisting the initial
    do_work_1() out of the loop.  So bail in this case.
    
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/11711
    Fixes: 6b4b04473986 ("nir/opt_loop: add loop peeling optimization")
    Signed-off-by: Rob Clark <robdclark@chromium.org>
    Reviewed-by: Alyssa Rosenzweig <alyssa@rosenzweig.io>
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/30702>
    (cherry picked from commit 563ec4754aef34f8707cccbb01ec8dac29a0c0e3
     https://gitlab.freedesktop.org/mesa/mesa.git main)
    
    BUG=b:359909532, b:360875983
    TEST=Run crafted SPIR-V shader without crashing
    
    Change-Id: I8c8f0e0f7aacd31d85ba530e4410c277fb0f2bfa
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5797928
    Auto-Submit: Matt Turner <msturner@google.com>
    Commit-Queue: Matt Turner <msturner@google.com>
    Tested-by: Matt Turner <msturner@google.com>
    Reviewed-by: Lina Versace <linyaa@google.com>
    Reviewed-by: Rob Clark <robdclark@chromium.org>
    Reviewed-by: Sean Paul <sean@poorly.run>

M       src/compiler/nir/nir_opt_loop.c

https://chromium-review.googlesource.com/5797928


### ap...@google.com (2024-09-19)

Project: chromiumos/third_party/mesa
Branch: chromeos-iris

commit f447fe37fbc0bb5ff05c57feebf5d1e888f5361e
Author: Jim Pollock <jmpollock@chromium.org>
Date:   Thu Sep 19 05:53:04 2024

    Revert "UPSTREAM: nir/opt_loop: Don't peel initial break if loop ends in break"
    
    This reverts commit cd8abccde6f03a1da369575168d40307744b3c4d.
    
    Reason for revert: b/367853536
    
    Original change's description:
    > UPSTREAM: nir/opt_loop: Don't peel initial break if loop ends in break
    >
    > A loop that looks like:
    >
    >    loop {
    >       do_work_1();
    >       if (cond) {
    >          break;
    >       } else {
    >       }
    >       do_work_2();
    >       break;
    >    }
    >
    > We can't pull that break ahead of do_work_1() after hoisting the initial
    > do_work_1() out of the loop.  So bail in this case.
    >
    > Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/11711
    > Fixes: 6b4b04473986 ("nir/opt_loop: add loop peeling optimization")
    > Signed-off-by: Rob Clark <robdclark@chromium.org>
    > Reviewed-by: Alyssa Rosenzweig <alyssa@rosenzweig.io>
    > Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/30702>
    > (cherry picked from commit 563ec4754aef34f8707cccbb01ec8dac29a0c0e3
    >  https://gitlab.freedesktop.org/mesa/mesa.git main)
    >
    > BUG=b:359909532, b:360875983
    > TEST=Run crafted SPIR-V shader without crashing
    >
    > Change-Id: I8c8f0e0f7aacd31d85ba530e4410c277fb0f2bfa
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5797928
    > Auto-Submit: Matt Turner <msturner@google.com>
    > Commit-Queue: Matt Turner <msturner@google.com>
    > Tested-by: Matt Turner <msturner@google.com>
    > Reviewed-by: Lina Versace <linyaa@google.com>
    > Reviewed-by: Rob Clark <robdclark@chromium.org>
    > Reviewed-by: Sean Paul <sean@poorly.run>
    
    BUG=b:359909532, b:360875983, b:367853536
    
    Change-Id: I3005a768b3c6b608c66f5ad447da48b21744df60
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5872307
    Reviewed-by: Jonathon Murphy <jpmurphy@google.com>
    Owners-Override: Madhav <madhavadas@google.com>
    Tested-by: Matt Turner <msturner@google.com>
    Reviewed-by: Madhav <madhavadas@google.com>

M       src/compiler/nir/nir_opt_loop.c

https://chromium-review.googlesource.com/5872307


### pe...@google.com (2024-12-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> baseline report of memory corruption a highly-privileged process (GPU)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/359909532)*
