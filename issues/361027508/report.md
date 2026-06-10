# GPU process crash via WebGPU shader - UAF in mesa gcm_schedule_early_instr at src/compiler/nir/nir_opt_gcm.c:477

| Field | Value |
|-------|-------|
| **Issue ID** | [361027508](https://issues.chromium.org/issues/361027508) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU |
| **Platforms** | ChromeOS |
| **Reporter** | a7...@gmail.com |
| **Assignee** | ms...@google.com |
| **Created** | 2024-08-20 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

This report is about a vulnerability in Mesa reachable via WebGPU shaders. The Mesa version is the one used by ChromeOS (which, in contrast to other versions of Linux, enables WebGPU). The bug reproducer was tested on an Ubuntu machine, which *should* not influence whether the bug is reachable on ChromeOS.

##### VERSION

Chrome Version: 130.0.6669.0 (Developer Build) (64-bit) (ASAN build)   

Operating System: Ubuntu   

Mesa: branch chromeos-iris, commit 51ef6de2a

##### REPRODUCTION CASE

Attached is a html file that triggers a heap UAF when opened in an ASAN version of mesa.

```
==1428067==ERROR: AddressSanitizer: heap-use-after-free on address 0x52d0000052d0 at pc 0x7272b582121b bp 0x7ffed85f4140 sp 0x7ffed85f4138
READ of size 8 at 0x52d0000052d0 thread T0 (chrome)
    #0 0x7272b582121a in exec_node_is_tail_sentinel /home/me/chromeosMesaOrg/build/../src/compiler/glsl/list.h:197:14
    #1 0x7272b582121a in nir_foreach_src /home/me/chromeosMesaOrg/build/../src/compiler/nir/nir_inline_helpers.h:111:7
    #2 0x7272b582121a in gcm_schedule_early_instr /home/me/chromeosMesaOrg/build/../src/compiler/nir/nir_opt_gcm.c:477:4
    #3 0x7272b5820d86 in gcm_schedule_early_src /home/me/chromeosMesaOrg/build/../src/compiler/nir/nir_opt_gcm.c:420:4
    #4 0x7272b5820d86 in _nir_visit_src /home/me/chromeosMesaOrg/build/../src/compiler/nir/nir_inline_helpers.h:47:9
    #5 0x7272b5820d86 in nir_foreach_src /home/me/chromeosMesaOrg/build/../src/compiler/nir/nir_inline_helpers.h:112:15
    #6 0x7272b5820d86 in gcm_schedule_early_instr /home/me/chromeosMesaOrg/build/../src/compiler/nir/nir_opt_gcm.c:477:4
    #7 0x7272b581ff2a in gcm_schedule_early_src /home/me/chromeosMesaOrg/build/../src/compiler/nir/nir_opt_gcm.c:420:4
    #8 0x7272b581ff2a in _nir_visit_src /home/me/chromeosMesaOrg/build/../src/compiler/nir/nir_inline_helpers.h:47:9
    #9 0x7272b581ff2a in nir_foreach_src /home/me/chromeosMesaOrg/build/../src/compiler/nir/nir_inline_helpers.h:65:15
    #10 0x7272b581ff2a in gcm_schedule_early_instr /home/me/chromeosMesaOrg/build/../src/compiler/nir/nir_opt_gcm.c:477:4
    #11 0x7272b581eaaa in opt_gcm_impl /home/me/chromeosMesaOrg/build/../src/compiler/nir/nir_opt_gcm.c:848:7
    #12 0x7272b581eaaa in nir_opt_gcm /home/me/chromeosMesaOrg/build/../src/compiler/nir/nir_opt_gcm.c:875:19
    #13 0x7272b5b7489d in brw_nir_optimize /home/me/chromeosMesaOrg/build/../src/intel/compiler/brw_nir.c:820:7
    #14 0x7272b5b74da7 in brw_preprocess_nir /home/me/chromeosMesaOrg/build/../src/intel/compiler/brw_nir.c:1059:4
    #15 0x7272b4b9feee in anv_pipeline_nir_preprocess /home/me/chromeosMesaOrg/build/../src/intel/vulkan/anv_pipeline.c:2093:4
    #16 0x7272b4ba7a73 in anv_graphics_pipeline_compile /home/me/chromeosMesaOrg/build/../src/intel/vulkan/anv_pipeline.c:2307:7
    #17 0x7272b4b9615f in anv_graphics_pipeline_create /home/me/chromeosMesaOrg/build/../src/intel/vulkan/anv_pipeline.c:3284:13
    #18 0x7272b4b9615f in anv_CreateGraphicsPipelines /home/me/chromeosMesaOrg/build/../src/intel/vulkan/anv_pipeline.c:3344:16
    #19 0x6103e5d2d662 in dawn::native::vulkan::RenderPipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/RenderPipelineVk.cpp:587:9
    #20 0x6103e5aed940 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:371:12
    #21 0x6103e5a2746b in dawn::native::DeviceBase::CreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*, bool) third_party/dawn/src/dawn/native/Device.cpp:2241:51
    #22 0x6103e5a26ec6 in dawn::native::DeviceBase::APICreateRenderPipeline(dawn::native::RenderPipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1556:26
    #23 0x6103fe50a16f in dawn::wire::server::Server::DoDeviceCreateRenderPipeline(WGPUDeviceImpl*, WGPURenderPipelineDescriptor const*, WGPURenderPipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:469:9
    #24 0x6103fe4fab8c in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:716:9
    #25 0x6103fe50173f in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:2056:30
    #26 0x6103fe4c39b0 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1043:33
    #27 0x6103fe4c3e43 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1948:22
    #28 0x6103fe4b5753 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1893:18
    #29 0x6103fe3d1d27 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:231:35
    #30 0x6103fe3c2030 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:502:22
    #31 0x6103fe3c15b3 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:153:7
    #32 0x6103fe3dd781 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long) gpu/ipc/service/gpu_channel.cc:932:13
    #33 0x6103fe3ecba8 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&) base/functional/bind_internal.h:738:12
    #34 0x6103fe3ec970 in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long> > base/functional/bind_internal.h:954:5
    #35 0x6103fe3ec970 in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1067:14
    #36 0x6103fe3ec970 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #37 0x6103faf96790 in Run base/functional/callback.h:156:12
    #38 0x6103faf96790 in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler_dfs.cc:598:24
    #39 0x6103faf94398 in gpu::SchedulerDfs::RunNextTask() gpu/command_buffer/service/scheduler_dfs.cc:522:3
    #40 0x6103faf98214 in Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs *> base/functional/bind_internal.h:738:12
    #41 0x6103faf98214 in MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:930:12
    #42 0x6103faf98214 in RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1067:14
    #43 0x6103faf98214 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #44 0x6103f5d5cf74 in Run base/functional/callback.h:156:12
    #45 0x6103f5d5cf74 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #46 0x6103f5dc5086 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> base/task/common/task_annotator.h:90:5
    #47 0x6103f5dc5086 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #48 0x6103f5dc3e1a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #49 0x6103f5dc5dea in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #50 0x6103f5f227f9 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:694:48
    #51 0x6103f5dc6a3a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #52 0x6103f5cebeff in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #53 0x61040c8bf83e in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:433:14
    #54 0x6103f333fa5e in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:700:14
    #55 0x6103f334095d in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:804:12
    #56 0x6103f33430cb in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1160:10
    #57 0x6103f333e02a in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:331:36
    #58 0x6103f333e61b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:344:10
    #59 0x6103e27ac203 in ChromeMain chrome/app/chrome_main.cc:230:12
    #60 0x7272bf02a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #61 0x7272bf02a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #62 0x6103e26d7029 in _start (/home/me/chrome/chrome+0xf5c5029) (BuildId: d2d087a5bec42288)

0x52d0000052d0 is located 20176 bytes inside of 32832-byte region [0x52d000000400,0x52d000008440)
freed by thread T0 (chrome) here:
    #0 0x6103e27aa22d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:143:3
    #1 0x6103e27fd2b7 in __libcpp_operator_delete<void *> third_party/libc++/src/include/new:274:3
    #2 0x6103e27fd2b7 in __do_deallocate_handle_size<> third_party/libc++/src/include/new:296:10
    #3 0x6103e27fd2b7 in __libcpp_deallocate third_party/libc++/src/include/new:311:12
    #4 0x6103e27fd2b7 in deallocate third_party/libc++/src/include/__memory/allocator.h:118:7
    #5 0x6103e27fd2b7 in deallocate third_party/libc++/src/include/__memory/allocator_traits.h:312:9
    #6 0x6103e27fd2b7 in std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>::__grow_by(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) third_party/libc++/src/include/string:2545:5
    #7 0x6103f4880c9d in __grow_by_without_replace third_party/libc++/src/include/string:2560:3
    #8 0x6103f4880c9d in std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>::append(unsigned long, char) third_party/libc++/src/include/string:2862:7
    #9 0x6103f5ee085f in resize third_party/libc++/src/include/string:1303:84
    #10 0x6103f5ee085f in base::debug::ReadProcMaps(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>*) base/debug/proc_maps_linux.cc:60:16
    #11 0x6103f5edbd12 in CacheMemoryRegions base/debug/stack_trace_posix.cc:871:10
    #12 0x6103f5edbd12 in Init base/debug/stack_trace_posix.cc:934:9
    #13 0x6103f5edbd12 in SandboxSymbolizeHelper base/debug/stack_trace_posix.cc:687:5
    #14 0x6103f5edbd12 in New base/memory/singleton.h:47:16
    #15 0x6103f5edbd12 in CreatorFunc base/memory/singleton.h:263:61
    #16 0x6103f5edbd12 in GetOrCreateLazyPointer<base::debug::(anonymous namespace)::SandboxSymbolizeHelper> base/lazy_instance_helpers.h:82:46
    #17 0x6103f5edbd12 in get base/memory/singleton.h:240:12
    #18 0x6103f5edbd12 in base::debug::(anonymous namespace)::SandboxSymbolizeHelper::GetInstance() base/debug/stack_trace_posix.cc:675:12
    #19 0x6103f5edb8c5 in base::debug::EnableInProcessStackDumping() base/debug/stack_trace_posix.cc:976:3
    #20 0x6103f3341ada in content::ContentMainRunnerImpl::Initialize(content::ContentMainParams) content/app/content_main_runner_impl.cc:1019:5
    #21 0x6103f333dd97 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:299:38
    #22 0x6103f333e61b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:344:10
    #23 0x6103e27ac203 in ChromeMain chrome/app/chrome_main.cc:230:12
    #24 0x7272bf02a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #25 0x7272bf02a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #26 0x6103e26d7029 in _start (/home/me/chrome/chrome+0xf5c5029) (BuildId: d2d087a5bec42288)

previously allocated by thread T0 (chrome) here:
    #0 0x6103e27a99cd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x6103e27fd200 in __libcpp_operator_new<unsigned long> third_party/libc++/src/include/new:265:10
    #2 0x6103e27fd200 in __libcpp_allocate third_party/libc++/src/include/new:289:10
    #3 0x6103e27fd200 in allocate third_party/libc++/src/include/__memory/allocator.h:103:32
    #4 0x6103e27fd200 in __allocate_at_least<std::__Cr::allocator<char> > third_party/libc++/src/include/__memory/allocate_at_least.h:41:19
    #5 0x6103e27fd200 in std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>::__grow_by(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) third_party/libc++/src/include/string:2535:23
    #6 0x6103f4880c9d in __grow_by_without_replace third_party/libc++/src/include/string:2560:3
    #7 0x6103f4880c9d in std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>::append(unsigned long, char) third_party/libc++/src/include/string:2862:7
    #8 0x6103f5ee085f in resize third_party/libc++/src/include/string:1303:84
    #9 0x6103f5ee085f in base::debug::ReadProcMaps(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>*) base/debug/proc_maps_linux.cc:60:16
    #10 0x6103f5edbd12 in CacheMemoryRegions base/debug/stack_trace_posix.cc:871:10
    #11 0x6103f5edbd12 in Init base/debug/stack_trace_posix.cc:934:9
    #12 0x6103f5edbd12 in SandboxSymbolizeHelper base/debug/stack_trace_posix.cc:687:5
    #13 0x6103f5edbd12 in New base/memory/singleton.h:47:16
    #14 0x6103f5edbd12 in CreatorFunc base/memory/singleton.h:263:61
    #15 0x6103f5edbd12 in GetOrCreateLazyPointer<base::debug::(anonymous namespace)::SandboxSymbolizeHelper> base/lazy_instance_helpers.h:82:46
    #16 0x6103f5edbd12 in get base/memory/singleton.h:240:12
    #17 0x6103f5edbd12 in base::debug::(anonymous namespace)::SandboxSymbolizeHelper::GetInstance() base/debug/stack_trace_posix.cc:675:12
    #18 0x6103f5edb8c5 in base::debug::EnableInProcessStackDumping() base/debug/stack_trace_posix.cc:976:3
    #19 0x6103f3341ada in content::ContentMainRunnerImpl::Initialize(content::ContentMainParams) content/app/content_main_runner_impl.cc:1019:5
    #20 0x6103f333dd97 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:299:38
    #21 0x6103f333e61b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:344:10
    #22 0x6103e27ac203 in ChromeMain chrome/app/chrome_main.cc:230:12
    #23 0x7272bf02a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #24 0x7272bf02a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #25 0x6103e26d7029 in _start (/home/me/chrome/chrome+0xf5c5029) (BuildId: d2d087a5bec42288)
SUMMARY: AddressSanitizer: heap-use-after-free /home/me/chromeosMesaOrg/build/../src/compiler/glsl/list.h:197:14 in exec_node_is_tail_sentinel
Shadow bytes around the buggy address:
  0x52d000005000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x52d000005080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x52d000005100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x52d000005180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x52d000005200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x52d000005280: fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd
  0x52d000005300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x52d000005380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x52d000005400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x52d000005480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x52d000005500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==1428067==ADDITIONAL INFO

==1428067==Note: Please include this section with the ASan report.
Task trace:
    #0 0x6103faf948a5 in gpu::SchedulerDfs::RunNextTask() gpu/command_buffer/service/scheduler_dfs.cc:538:27
    #1 0x6103faf8fd59 in gpu::SchedulerDfs::TryScheduleSequence(gpu::SchedulerDfs::Sequence*) gpu/command_buffer/service/scheduler_dfs.cc:340:11


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --use-angle=vulkan --string-annotations --crashpad-handler-pid=1428038 --enable-crash-reporter=, --no-subproc-heap-profiling --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAoAAAEAAAAAAAAAAAAAAAAAABgAAIAAAACAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,7403204782531740081,2882334392781765968,262144 --field-trial-handle=3,i,4897725009369838748,5062799707588159629,262144 --enable-features=Vulkan --disable-features=EyeDropper --variations-seed-version`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1428067==END OF ADDITIONAL INFO

```
##### CREDIT INFORMATION

Reporter credit: anonymous

## Attachments

- [gcm_choose_block_for_instr.html](attachments/gcm_choose_block_for_instr.html) (text/html, 4.3 KB)

## Timeline

### am...@chromium.org (2024-08-20)

Hello -- thank you for the report. This seems to be an issue squarely in Mesa, so we'll need to send it over to the ChromeOS in their tracker.
Apologies for the noise while I adjust a bunch of the metadata to do this as cleanly as possible.
For issues in Mesa / ChromeOS, please report them directly to the ChromeOS team in the future.

### am...@chromium.org (2024-08-20)

adding msturner@ from the ChromeOS gpu team in the meantime

### bl...@google.com (2024-08-20)

Automated by Blunderbuss job chromeos_security_blunderbuss_autoassigner for config chromeos_security_blunderbuss_config for component 1335705.

### pr...@google.com (2024-08-20)

Matt, can you open a private mesa issue upstream for this and let Lionel and co comment on this?

### ms...@google.com (2024-08-20)

Sure, will do.

### ms...@google.com (2024-08-23)

Filed as <https://gitlab.freedesktop.org/mesa/mesa/-/issues/11770>

### a7...@gmail.com (2024-09-07)

Is there any kind of update from the Mesa project regarding a fix to this issue? Memory corruptions reachable from the web/via chrome are often fixed rather quickly + having this bug fixed would allow me to decide for all the other fuzzer crashes whether they're duplicates or distinct bugs.

### ms...@google.com (2024-09-09)

There hasn't :(

I'll ping people.

### ms...@google.com (2024-09-09)

What freedesktop gitlab account would you like me to Cc on the upstream issue?

### ms...@google.com (2024-09-10)

Upstream, the author of the optimization pass that is crashing is asking for a reproducer outside of the browser.

### a7...@gmail.com (2024-09-10)

Could you please add @a72827312 to the issue in the mesa repo? I'll provide a reproducer outside of the browser.

### ms...@google.com (2024-09-10)

Done, thanks!

### a7...@gmail.com (2024-09-10)

Hmm, I still can't open the issue nor got a e-mail notification.

### ms...@google.com (2024-09-10)

I've now set you as the assignee. Apparently the requirements for confidential issues are:

> Only project members with at least the Reporter role, the author, and assignees can view or be notified about this issue.

I think it makes sense for you to be the one to file issues upstream in the future. Not much point in me being the middleman.

### a7...@gmail.com (2024-09-30)

Just a heads up, other people are also working on harnessing Mesa in order to find bugs reachable via WebGPU (see <https://github.com/wgslfuzz/darthshader/issues/2#issuecomment-2383858307>)
Considering the pace of upstream in investigating reports, they'll uncover a multiplicity in bugs affecting ChromeOS via WebGPU shaders.

### ms...@google.com (2024-11-08)

I've pinged people upstream to try to get <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/31711> reviewed. I left a comment on the MR as well.

### ro...@google.com (2024-11-15)

> they'll uncover a multiplicity in bugs affecting ChromeOS via WebGPU shaders.

For these bugs to be considered vulnerabilities as part of our program, there would need to be a demonstrated security impact on ChromeOS. There is currently no PoC associated with this bug demonstrating any information being exfiltrated or arbitrary code execution.

Do you have a PoC on CrOS that demonstrates an attacker can actually do something with this bug beyond triggering a crash (which we don't consider a vulnerability)?

### a7...@gmail.com (2024-11-16)

Just to be clear, are you unconvinced that this UAF affects Chrome on CrOs or is the bar higher, as in "the program requires to demonstrate code execution or data exfiltration"?

### ro...@google.com (2024-11-18)

Please see our program rules for bugs we consider in scope
https://bughunters.google.com/about/rules/chrome-friends/4919474699501568/chromeos-vulnerability-reward-program-rules

We expect bugs reported to our program to manifest on a production version
of ChromeOS in the Stable channel booted in verified mode on a Chromebook.
Since ChromeOS is hardened and integrated with the hardware/firmware this
gets to reachability.

For a reachable bug to be considered a vulnerability, the bug must also
have a demonstrated security impact e.g. confidentiality or integrity
(since we don't consider availability a security impact).

We don't consider bugs that only cause a crash/denial of service to be
vulnerabilities. (In part, because we rely heavily on sandboxing and
toolchain hardening like FORTIFY_SOURCE so we may intentionally generate a
crash to prevent exploitation of a bug.)

Please see our security severity guidelines for more details
https://www.chromium.org/chromium-os/developer-library/guides/bugs/security-severity-guidelines/

Additionally this bug is not considered a vulnerability in Mesa since Mesa
does not maintain a security boundary. The security boundary is in the
browser. However, there are cases where a bug can't be fixed, or fully
fixed in the browser, and there's a need to push the fix to Mesa.

Hope this clarifies. That said, I think the attack surface in the browser
you are exploring is important because Mesa is not actually a security
boundary.



### a7...@gmail.com (2024-11-19)

> Additionally this bug is not considered a vulnerability in Mesa since Mesa does not maintain a security boundary. The security boundary is in the browser.

If Mesa is not ready to handle "untrusted but well-formed" inputs, exposing its shader compiler to the web is an interesting design choice. In fact, I don't see the browser at fault at all because the SPIR-V generated by tint is perfectly valid. The tint/dawn developers cannot prevent such issues (without prior knowledge regarding which IR patterns to avoid).

In the end, it doesn't matter as long as the bugs get fixed.

### ms...@google.com (2024-11-21)

CL created to cherry-pick the fix to `mesa-iris`: [crrev/c/6039380](https://crrev.com/c/6039380)

### ap...@google.com (2024-11-21)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Rhys Perry <[pendingchaos02@gmail.com](mailto:pendingchaos02@gmail.com)>  

Link:      <https://chromium-review.googlesource.com/6039380>

UPSTREAM: nir/lcssa: fix premature exit of loop after rematerializing derefs

---


Expand for full commit details
```
UPSTREAM: nir/lcssa: fix premature exit of loop after rematerializing derefs 
 
If we have NIR such as: 
 
32x4  %48 = @load_vulkan_descriptor (%47) (desc_type=SSBO) 
32x4  %76 = deref_cast (tint_symbol_11 *)%48 (ssbo tint_symbol_11)  (ptr_stride=0, align_mul=4, align_offset=0) 
32x4  %77 = deref_struct &%76->tint_symbol_10 (ssbo int)  // &((tint_symbol_11 *)%48)->tint_symbol_10 
 
A single nir_rematerialize_deref_in_use_blocks() will rematerialize the 
deref_struct and then it's deref_cast. However, 
nir_foreach_instr_reverse_safe is not safe if the next iteration's 
instruction is removed. This can result in the instruction loop exiting 
and the load_vulkan_descriptor never having an LCSSA phi. 
 
Signed-off-by: Rhys Perry <pendingchaos02@gmail.com> 
Reviewed-by: Ian Romanick <ian.d.romanick@intel.com> 
Fixes: 439e8c42cc4b ("nir/lcssa: Fix rematerializing derefs") 
Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/11770 
Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/32225> 
(cherry picked from commit 65a54b4ec41f4de33c770ceb1535358d008fbaad 
 https://gitlab.freedesktop.org/mesa/mesa.git main) 
 
BUG=b:361027508 
TEST=Run crafted SPIR-V shader without crashing 
 
Change-Id: I9fdd0e7620bccea8734e5fff0a3e8a42a587d623 
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6039380 
Tested-by: Matt Turner <msturner@google.com> 
Commit-Queue: Rob Clark <robdclark@chromium.org> 
Commit-Queue: Matt Turner <msturner@google.com> 
Reviewed-by: Rob Clark <robdclark@chromium.org> 
Reviewed-by: Prahlad Kilambi <prahladk@google.com> 
Auto-Submit: Matt Turner <msturner@google.com> 
Reviewed-by: Sean Paul <sean@poorly.run>

```

---

Files:

- M `src/compiler/nir/nir_to_lcssa.c`
- M `src/compiler/nir/tests/control_flow_tests.cpp`

---

Hash: 44e909eea09f692a682cb0e7b33c49cd1d7a7e29  

Date:  Thu Oct 17 10:21:47 2024


---

### sp...@google.com (2024-12-03)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Explained in b/361027508#comment20

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### pe...@google.com (2024-12-06)

This bug is now in the Chromium Tracker, and users should use Chromium’s custom fields going forward instead of ChromeOS hotlists.

### am...@chromium.org (2024-12-06)

Since this the time this issue was initially triaged, we have re-defined bug handling policies regarding user mode GPU driver security bugs[1], so I am moving this back to the Chromium tracker.

The ChromeOS VRP decision in c#24 was incorrectly associated with the Chrome VRP by the CrOS bot. So I am tagging this as reward-topanel so it can be considered by Chrome VRP, since this falls within our scope. [2]

[1] <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/shepherd.md#assign>
[2] <https://g.co/chrome/vrp#scope-of-program>

### sp...@google.com (2024-12-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
$10,000 for report of memory corruption in a highly-privileged process / GPU


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-12)

Congratulations -- thank you for your efforts and reporting this issue to us!

### ch...@google.com (2025-02-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/361027508)*
