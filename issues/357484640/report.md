#  GPU process crash via WebGL2 shader - dynamic-stack-buffer-overflow in hash_phi

| Field | Value |
|-------|-------|
| **Issue ID** | [357484640](https://issues.chromium.org/issues/357484640) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>WebGL, Blink>WebGPU |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | wg...@gmail.com |
| **Assignee** | ms...@google.com |
| **Created** | 2024-08-05 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

Chromium on Linux translates WebGL2 shaders to SPIR-V (if the Vulkan backend is enabled). These SPIR-V shaders are passed to Mesa. The Vulkan backend of Mesa first searches for an available device, instantiates the device and hands over the shader to the vendor-specific driver. This vendor-specific driver utilizes the SPIR-V shader optimization passes provided by the Mesa framework. This bug report is about a memory safety violation in `libvulkan_intel.so`, reachable via a crafted WebGL2 shader. The bug itself doesn't seem to be in an Intel-specific source file, so GPUs from other vendors might be affected as well.

##### VERSION

Chrome Version: Pre-compiled ASAN Chromium 129.0.6639.0 (Developer Build) (64-bit)   

Operating System: Ubuntu 24.04 LTS   

Mesa: mesa 24.1.1

##### ADDITIONAL INFORMATION

There is no upstream bug yet, if you'd like me to create on let me know.   

The shader triggering the bug looks a bit like the one from [bug 350528343](https://issues.chromium.org/issues/350528343) (infinite loops and nested switches), so they *might* be related. The asserts triggering in debug builds of Mesa of the respective issues are different though.

##### REPRODUCTION CASE

Attached is a .html file containing 2 WebGL2 shaders. The issue stems from the vertex shader; the fragment shader is just boilerplate. Opening the html file when using an ASAN build of Mesa (with Intel GPU): `VK_DRIVER_FILES=mesa/buildASAN/src/intel/vulkan/intel_icd.x86_64.json ./chrome --use-angle=vulkan --enable-features=Vulkan --disable-gpu-watchdog --no-sandbox` triggers an ASAN violation in the the GPU process. I verified that the crash reproduces on a 10th Gen GPUs (tested on i7-10510U).

```
ASAN_OPTIONS=external_symbolizer_path=/usr/lib/llvm-18/bin/llvm-symbolizer VK_DRIVER_FILES=mesa/buildASAN/src/intel/vulkan/intel_icd.x86_64.json ./chrome --use-angle=vulkan --enable-features=Vulkan --disable-gpu-watchdog --no-sandbox                                
[273889:273904:0805/124933.091418:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.Notifications.GetCapabilities: object_path= /org/freedesktop/Notifications: org.freedesktop.DBus.Error.NoReply: Message recipient disconnected from message bus without replying
================================================================= 
==273921==ERROR: AddressSanitizer: dynamic-stack-buffer-overflow on address 0x7ffc2a580c28 at pc 0x714b985b2269 bp 0x7ffc2a580bf0 sp 0x7ffc2a580be8
WRITE of size 8 at 0x7ffc2a580c28 thread T0 (chrome)
    #0 0x714b985b2268 in hash_phi mesa/buildASAN/../src/compiler/nir/nir_instr_set.c:196:17
    #1 0x714b97f12efd in _mesa_set_search_or_add mesa/buildASAN/../src/util/set.c:525:34
    #2 0x714b985b1843 in nir_instr_set_add_or_rewrite mesa/buildASAN/../src/compiler/nir/nir_instr_set.c:759:26
    #3 0x714b98417002 in nir_opt_cse_impl mesa/buildASAN/../src/compiler/nir/nir_opt_cse.c:48:22
    #4 0x714b98417002 in nir_opt_cse mesa/buildASAN/../src/compiler/nir/nir_opt_cse.c:68:19
    #5 0x714b98773711 in brw_nir_optimize mesa/buildASAN/../src/intel/compiler/brw_nir.c:762:7
    #6 0x714b98773fd7 in brw_preprocess_nir mesa/buildASAN/../src/intel/compiler/brw_nir.c:1059:4
    #7 0x714b9779fdee in anv_pipeline_nir_preprocess mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2093:4
    #8 0x714b977a7973 in anv_graphics_pipeline_compile mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2307:7
    #9 0x714b97795f6c in anv_graphics_lib_pipeline_create mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:3155:16
    #10 0x714b97795f6c in anv_CreateGraphicsPipelines mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:3339:16
    #11 0x714b9abecb67 in initGraphics third_party/angle/src/libANGLE/renderer/vulkan/vk_wrapper.h:1838:12
    #12 0x714b9abecb67 in createGraphicsPipeline third_party/angle/src/libANGLE/renderer/vulkan/vk_cache_utils.cpp:7025:25
    #13 0x714b9abecb67 in rx::vk::GraphicsPipelineDesc::initializePipeline(rx::vk::Context*, rx::vk::PipelineCacheAccess*, rx::vk::GraphicsPipelineSubset, rx::vk::RenderPass const&, rx::vk::PipelineLayout const&, angle::PackedEnumMap<gl::ShaderType, rx::vk::BindingPointer<rx::vk::ShaderModule, rx::vk::RefCounted<rx::vk::ShaderModule>>, 6ul> const&, rx::vk::SpecializationConstants const&, rx::vk::Pipeline*, rx::vk::CacheLookUpFeedback*) const third_party/angle/src/libANGLE/renderer/vulkan/vk_cache_utils.cpp:3580:38
    #14 0x714b9abeee2f in rx::GraphicsPipelineCache<rx::GraphicsPipelineDescShadersHash>::createPipeline(rx::vk::Context*, rx::vk::PipelineCacheAccess*, rx::vk::RenderPass const&, rx::vk::PipelineLayout const&, angle::PackedEnumMap<gl::ShaderType, rx::vk::BindingPointer<rx::vk::ShaderModule, rx::vk::RefCounted<rx::vk::ShaderModule>>, 6ul> const&, rx::vk::SpecializationConstants const&, rx::PipelineSource, rx::vk::GraphicsPipelineDesc const&, rx::vk::GraphicsPipelineDesc const**, rx::vk::PipelineHelper**) third_party/angle/src/libANGLE/renderer/vulkan/vk_cache_utils.cpp:7879:9
    #15 0x714b9aaeb641 in createGraphicsPipeline<rx::GraphicsPipelineDescShadersHash> third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.h:3631:35
    #16 0x714b9aaeb641 in createGraphicsPipelineImpl third_party/angle/src/libANGLE/renderer/vulkan/ProgramExecutableVk.cpp:1601:47
    #17 0x714b9aaeb641 in initProgramThenCreateGraphicsPipeline third_party/angle/src/libANGLE/renderer/vulkan/ProgramExecutableVk.cpp:1553:12
    #18 0x714b9aaeb641 in rx::ProgramExecutableVk::createGraphicsPipeline(rx::ContextVk*, rx::vk::GraphicsPipelineSubset, rx::vk::PipelineCacheAccess*, rx::PipelineSource, rx::vk::GraphicsPipelineDesc const&, rx::vk::GraphicsPipelineDesc const**, rx::vk::PipelineHelper**) third_party/angle/src/libANGLE/renderer/vulkan/ProgramExecutableVk.cpp:1665:5
    #19 0x714b9aa6ea11 in rx::ContextVk::createGraphicsPipeline() third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:2153:25
    #20 0x714b9aa54949 in rx::ContextVk::handleDirtyGraphicsPipelineDesc(angle::BitSetT<42ul, unsigned long, unsigned long>::Iterator*, angle::BitSetT<42ul, unsigned long, unsigned long>) third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:2248:9
    #21 0x714b9aa6a099 in rx::ContextVk::setupDraw(gl::Context const*, gl::PrimitiveMode, int, int, int, gl::DrawElementsType, void const*, angle::BitSetT<42ul, unsigned long, unsigned long>) third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:1600:13 
    #22 0x714b9aa77888 in rx::ContextVk::drawArrays(gl::Context const*, gl::PrimitiveMode, int, int) third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:4077:9
    #23 0x714b9a9e4aba in drawArrays third_party/angle/src/libANGLE/Context.inl.h:152:5
    #24 0x714b9a9e4aba in GL_DrawArrays third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:1260:22
    #25 0x5fc086fc98b4 in gl::RealGLApi::glDrawArraysFn(unsigned int, int, int) ui/gl/gl_gl_api_implementation.cc:397:16
    #26 0x5fc08ad8ead6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(unsigned int, int, int) gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1226:10
    #27 0x5fc08ad2f7ed in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:723:20
    #28 0x5fc08b2968f7 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:231:35
    #29 0x5fc08b286e10 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:502:22
    #30 0x5fc08b286393 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:153:7
    #31 0x5fc08b2a2351 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long) gpu/ipc/service/gpu_channel.cc:932:13
    #32 0x5fc08b2b17a8 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&) base/functional/bind_internal.h:738:12
    #33 0x5fc08b2b1570 in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long> > base/functional/bind_internal.h:954:5
    #34 0x5fc08b2b1570 in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1067:14
    #35 0x5fc08b2b1570 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #36 0x5fc087e08280 in Run base/functional/callback.h:156:12
    #37 0x5fc087e08280 in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler_dfs.cc:600:24
    #38 0x5fc087e05e88 in gpu::SchedulerDfs::RunNextTask() gpu/command_buffer/service/scheduler_dfs.cc:524:3
    #39 0x5fc087e09d04 in Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs *> base/functional/bind_internal.h:738:12
    #40 0x5fc087e09d04 in MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:930:12
    #41 0x5fc087e09d04 in RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1067:14
    #42 0x5fc087e09d04 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #43 0x5fc082c1fe84 in Run base/functional/callback.h:156:12
    #44 0x5fc082c1fe84 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #45 0x5fc082c87416 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> base/task/common/task_annotator.h:90:5
    #46 0x5fc082c87416 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #47 0x5fc082c86330 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #48 0x5fc082c8815a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #49 0x5fc082deceb2 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:649:46
    #50 0x5fc082defd98 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:274:43
    #51 0x714ba34d85b4  (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5d5b4) (BuildId: 9753724b85d60f97b5d5663181ef7f4e69a62131)
    #52 0x714ba3537716  (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0xbc716) (BuildId: 9753724b85d60f97b5d5663181ef7f4e69a62131)
    #53 0x714ba34d7a52 in g_main_context_iteration (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5ca52) (BuildId: 9753724b85d60f97b5d5663181ef7f4e69a62131)
    #54 0x5fc082ded4df in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:683:30
    #55 0x5fc082c88dc6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #56 0x5fc082baeb0f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #57 0x5fc099700e33 in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:431:14
    #58 0x5fc08042590e in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:703:14
    #59 0x5fc08042680d in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:807:12
    #60 0x5fc0804290a7 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1175:10
    #61 0x5fc080423d1a in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:333:36
    #62 0x5fc08042430b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:346:10
    #63 0x5fc06f88b9b3 in ChromeMain chrome/app/chrome_main.cc:230:12
    #64 0x714ba202a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #65 0x714ba202a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #66 0x5fc06f7b7029 in _start (/home/user/Downloads/linuxasan/chrome+0xf414029) (BuildId: 7e6cd0981f549e28)

Address 0x7ffc2a580c28 is located in stack of thread T0 (chrome)
SUMMARY: AddressSanitizer: dynamic-stack-buffer-overflow mesa/buildASAN/../src/compiler/nir/nir_instr_set.c:196:17 in hash_phi
Shadow bytes around the buggy address:
  0x7ffc2a580980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ffc2a580a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ffc2a580a80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ffc2a580b00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ffc2a580b80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ffc2a580c00: ca ca ca ca 00[cb]cb cb cb cb cb cb 00 00 00 00
  0x7ffc2a580c80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ffc2a580d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ffc2a580d80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ffc2a580e00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ffc2a580e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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

==273921==ADDITIONAL INFO

==273921==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5fc087e06395 in gpu::SchedulerDfs::RunNextTask() gpu/command_buffer/service/scheduler_dfs.cc:540:27
    #1 0x5fc087e06395 in gpu::SchedulerDfs::RunNextTask() gpu/command_buffer/service/scheduler_dfs.cc:540:27
    #2 0x5fc087e06395 in gpu::SchedulerDfs::RunNextTask() gpu/command_buffer/service/scheduler_dfs.cc:540:27
    #3 0x5fc087e06395 in gpu::SchedulerDfs::RunNextTask() gpu/command_buffer/service/scheduler_dfs.cc:540:27
Command line: `/proc/self/exe --type=gpu-process --no-sandbox --use-angle=vulkan --crashpad-handler-pid=273891 --enable-crash-reporter=, --no-subproc-heap-profiling --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAoAAAEAAAAAAAAAAAAAAAAAABgAAIAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,297518018745375511,4054440614369228451,262144 --field-trial-handle=3,i,3754390240110945565,8215912292913097726,262144 --enable-features=Vulkan --disable-features=EyeDropper --variations-seed-version`


==273921==END OF ADDITIONAL INFO
==273921==ABORTING
[273965:273989:0805/124944.141714:ERROR:command_buffer_proxy_impl.cc(324)] GPU state invalid after WaitForGetOffsetInRange.

```

This OOB didn't look *that* scary as its just slightly OOB into an area that may not contain interesting data. If I create a workaround for the above OOB in `src/compiler/nir/nir_instr_set.c:195` (terminating the loop in function `hash_phi` created by the macro `nir_foreach_phi_src` s.t. it respects buffer boundaries), the broked IR creates another OOB further down the line:

```
==283328==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x51f000190294 at pc 0x7cd7f3bc4a2c bp 0x7ffceb7cc750 sp 0x7ffceb7cc748
READ of size 1 at 0x51f000190294 thread T0 (chrome)
    #0 0x7cd7f3bc4a2b in compute_induction_information mesa/buildASAN/../src/compiler/nir/nir_loop_analyze.c:362:23
    #1 0x7cd7f3bc4a2b in get_loop_info mesa/buildASAN/../src/compiler/nir/nir_loop_analyze.c:1495:9
    #2 0x7cd7f3bc4a2b in process_loops mesa/buildASAN/../src/compiler/nir/nir_loop_analyze.c:1575:4
    #3 0x7cd7f3bbd60d in process_loops mesa/buildASAN/../src/compiler/nir/nir_loop_analyze.c:1560:10
    #4 0x7cd7f3bbd3bc in nir_loop_analyze_impl mesa/buildASAN/../src/compiler/nir/nir_loop_analyze.c:1587:7
    #5 0x7cd7f3a0f212 in nir_metadata_require mesa/buildASAN/../src/compiler/nir/nir_metadata.c:52:7
    #6 0x7cd7f3a1ca90 in opt_gcm_impl mesa/buildASAN/../src/compiler/nir/nir_opt_gcm.c:802:4
    #7 0x7cd7f3a1ca90 in nir_opt_gcm mesa/buildASAN/../src/compiler/nir/nir_opt_gcm.c:875:19
    #8 0x7cd7f3d73add in brw_nir_optimize mesa/buildASAN/../src/intel/compiler/brw_nir.c:820:7
    #9 0x7cd7f3d73fe7 in brw_preprocess_nir mesa/buildASAN/../src/intel/compiler/brw_nir.c:1059:4
    #10 0x7cd7f2d9fdee in anv_pipeline_nir_preprocess mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2093:4
    #11 0x7cd7f2da7973 in anv_graphics_pipeline_compile mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:2307:7
    #12 0x7cd7f2d95f6c in anv_graphics_lib_pipeline_create mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:3155:16
    #13 0x7cd7f2d95f6c in anv_CreateGraphicsPipelines mesa/buildASAN/../src/intel/vulkan/anv_pipeline.c:3339:16
    #14 0x7cd7f61ecb67 in initGraphics third_party/angle/src/libANGLE/renderer/vulkan/vk_wrapper.h:1838:12
    #15 0x7cd7f61ecb67 in createGraphicsPipeline third_party/angle/src/libANGLE/renderer/vulkan/vk_cache_utils.cpp:7025:25
    #16 0x7cd7f61ecb67 in rx::vk::GraphicsPipelineDesc::initializePipeline(rx::vk::Context*, rx::vk::PipelineCacheAccess*, rx::vk::GraphicsPipelineSubset, rx::vk::RenderPass const&, rx::vk::PipelineLayout const&, angle::PackedEnumMap<gl::ShaderType, rx::vk::BindingPointer<rx::vk::ShaderModule, rx::vk::RefCounted<rx::vk::ShaderModule>>, 6ul> const&, rx::vk::SpecializationConstants const&, rx::vk::Pipeline*, rx::vk::CacheLookUpFeedback*) const third_party/angle/src/libANGLE/renderer/vulkan/vk_cache_utils.cpp:3580:38
    #17 0x7cd7f61eee2f in rx::GraphicsPipelineCache<rx::GraphicsPipelineDescShadersHash>::createPipeline(rx::vk::Context*, rx::vk::PipelineCacheAccess*, rx::vk::RenderPass const&, rx::vk::PipelineLayout const&, angle::PackedEnumMap<gl::ShaderType, rx::vk::BindingPointer<rx::vk::ShaderModule, rx::vk::RefCounted<rx::vk::ShaderModule>>, 6ul> const&, rx::vk::SpecializationConstants const&, rx::PipelineSource, rx::vk::GraphicsPipelineDesc const&, rx::vk::GraphicsPipelineDesc const**, rx::vk::PipelineHelper**) third_party/angle/src/libANGLE/renderer/vulkan/vk_cache_utils.cpp:7879:9
    #18 0x7cd7f60eb641 in createGraphicsPipeline<rx::GraphicsPipelineDescShadersHash> third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.h:3631:35
    #19 0x7cd7f60eb641 in createGraphicsPipelineImpl third_party/angle/src/libANGLE/renderer/vulkan/ProgramExecutableVk.cpp:1601:47
    #20 0x7cd7f60eb641 in initProgramThenCreateGraphicsPipeline third_party/angle/src/libANGLE/renderer/vulkan/ProgramExecutableVk.cpp:1553:12
    #21 0x7cd7f60eb641 in rx::ProgramExecutableVk::createGraphicsPipeline(rx::ContextVk*, rx::vk::GraphicsPipelineSubset, rx::vk::PipelineCacheAccess*, rx::PipelineSource, rx::vk::GraphicsPipelineDesc const&, rx::vk::GraphicsPipelineDesc const**, rx::vk::PipelineHelper**) third_party/angle/src/libANGLE/renderer/vulkan/ProgramExecutableVk.cpp:1665:5
    #22 0x7cd7f606ea11 in rx::ContextVk::createGraphicsPipeline() third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:2153:25
    #23 0x7cd7f6054949 in rx::ContextVk::handleDirtyGraphicsPipelineDesc(angle::BitSetT<42ul, unsigned long, unsigned long>::Iterator*, angle::BitSetT<42ul, unsigned long, unsigned long>) third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:2248:9
    #24 0x7cd7f606a099 in rx::ContextVk::setupDraw(gl::Context const*, gl::PrimitiveMode, int, int, int, gl::DrawElementsType, void const*, angle::BitSetT<42ul, unsigned long, unsigned long>) third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:1600:13
    #25 0x7cd7f6077888 in rx::ContextVk::drawArrays(gl::Context const*, gl::PrimitiveMode, int, int) third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:4077:9
    #26 0x7cd7f5fe4aba in drawArrays third_party/angle/src/libANGLE/Context.inl.h:152:5
    #27 0x7cd7f5fe4aba in GL_DrawArrays third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:1260:22
    #28 0x591d05f708b4 in gl::RealGLApi::glDrawArraysFn(unsigned int, int, int) ui/gl/gl_gl_api_implementation.cc:397:16
    #29 0x591d09d35ad6 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(unsigned int, int, int) gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1226:10
    #30 0x591d09cd67ed in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:723:20
    #31 0x591d0a23d8f7 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:231:35
    #32 0x591d0a22de10 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:502:22
    #33 0x591d0a22d393 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc:153:7
    #34 0x591d0a249351 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long) gpu/ipc/service/gpu_channel.cc:932:13
    #35 0x591d0a2587a8 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&) base/functional/bind_internal.h:738:12
    #36 0x591d0a258570 in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long> > base/functional/bind_internal.h:954:5
    #37 0x591d0a258570 in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1067:14
    #38 0x591d0a258570 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #39 0x591d06daf280 in Run base/functional/callback.h:156:12
    #40 0x591d06daf280 in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler_dfs.cc:600:24
    #41 0x591d06dace88 in gpu::SchedulerDfs::RunNextTask() gpu/command_buffer/service/scheduler_dfs.cc:524:3
    #42 0x591d06db0d04 in Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs *> base/functional/bind_internal.h:738:12
    #43 0x591d06db0d04 in MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:930:12
    #44 0x591d06db0d04 in RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1067:14
    #45 0x591d06db0d04 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:980:12
    #46 0x591d01bc6e84 in Run base/functional/callback.h:156:12
    #47 0x591d01bc6e84 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:203:34
    #48 0x591d01c2e416 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> base/task/common/task_annotator.h:90:5
    #49 0x591d01c2e416 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #50 0x591d01c2d330 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #51 0x591d01c2f15a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #52 0x591d01d947e9 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:694:48
    #53 0x591d01c2fdc6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #54 0x591d01b55b0f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #55 0x591d186a7e33 in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:431:14
    #56 0x591cff3cc90e in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:703:14
    #57 0x591cff3cd80d in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:807:12
    #58 0x591cff3d00a7 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1175:10
    #59 0x591cff3cad1a in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:333:36
    #60 0x591cff3cb30b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:346:10
    #61 0x591cee8329b3 in ChromeMain chrome/app/chrome_main.cc:230:12
    #62 0x7cd7fd42a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #63 0x7cd7fd42a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #64 0x591cee75e029 in _start (/home/user/Downloads/linuxasan/chrome+0xf414029) (BuildId: 7e6cd0981f549e28)
Address 0x51f000190294 is a wild pointer inside of access range of size 0x000000000001.
SUMMARY: AddressSanitizer: heap-buffer-overflow mesa/buildASAN/../src/compiler/nir/nir_loop_analyze.c:362:23 in compute_induction_information
Shadow bytes around the buggy address:
  0x51f000190000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51f000190080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51f000190100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51f000190180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51f000190200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x51f000190280: fa fa[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51f000190300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51f000190380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51f000190400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51f000190480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51f000190500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==283328==ADDITIONAL INFO

==283328==Note: Please include this section with the ASan report.
Task trace:
    #0 0x591d06dad395 in gpu::SchedulerDfs::RunNextTask() gpu/command_buffer/service/scheduler_dfs.cc:540:27
    #1 0x591d06da8849 in gpu::SchedulerDfs::TryScheduleSequence(gpu::SchedulerDfs::Sequence*) gpu/command_buffer/service/scheduler_dfs.cc:342:11


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --use-angle=vulkan --crashpad-handler-pid=283283 --enable-crash-reporter=, --no-subproc-heap-profiling --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAoAAAEAAAAAAAAAAAAAAAAAABgAAIAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,16956414611577899132,17729580326589353017,262144 --field-trial-handle=3,i,15522175942107645994,7985500702686805221,262144 --enable-features=Vulkan --disable-features=EyeDropper --variations-seed-version`


==283328==END OF ADDITIONAL INFO
==283328==ABORTING
[283281:283281:0805/125645.248118:ERROR:gpu_process_host.cc(1007)] GPU process exited unexpectedly: exit_code=256

```

When enabling asserts in Mesa, the following assert triggers: `error: state->nr_tagged_srcs == 0 (../src/compiler/nir/nir_validate.c:1630)`
I attached a full output of Mesa debug output, as it contains the IR code of the function triggering the issue.

## Attachments

- [mesa_assert_output](attachments/mesa_assert_output) (application/octet-stream, 13.4 KB)
- [triggerInduction.html](attachments/triggerInduction.html) (text/html, 4.8 KB)

## Timeline

### wg...@gmail.com (2024-08-05)

I'm aware this isn't the best place to ask but: are you also interested in Mesa bugs reachable via WebGPU on Linux? This is currently not enabled by default and requires `--enable-unsafe-webgpu`.

### kr...@google.com (2024-08-06)

kbr@ can you take a look as this looks similar to [b/350528343](https://issues.chromium.org/issues/350528343)

### kb...@chromium.org (2024-08-06)

Shabi: could you please take this bug as well? I think that minimally, your workaround for [Issue 350528343](https://issues.chromium.org/issues/350528343) will catch and reject these shaders, too, even though it's a crash in a different part of Mesa.

### sy...@chromium.org (2024-08-06)

The infinite-loop-detection code is not detecting this shader as infinite loop because there's a `return` in the middle, so the workaround (neither the one that has already landed, nor the one that hasn't) is unable to prune/reject this shader.

### pe...@google.com (2024-08-06)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-08-06)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### kb...@chromium.org (2024-08-06)

I don't think P0 is warranted and am downgrading this to P1 to match [Issue 350528343](https://issues.chromium.org/issues/350528343).

### ms...@google.com (2024-08-06)

I'll have a look.

### kb...@chromium.org (2024-08-06)

Matt (msturner@), per your excellent analysis on [Issue 350528343](https://issues.chromium.org/issues/350528343) - would you be able to see whether the Mesa fixes you've identified also fix this issue? The control flow constructs are a little more complex here, but there are still fairly easily identifiable infinite loops which we think are the cause of the problem.

### ms...@google.com (2024-08-06)

Yeah, will do. Thanks for roping me in!

### ar...@chromium.org (2024-08-08)

Hello [msturner@chromium.org](mailto:msturner@chromium.org)

Would you have any updates about this critical vulnerability?

*Secondary security shepherd.*

### ms...@google.com (2024-08-08)

I'm OOO until Monday. I'll investigate as soon as I return.

### ms...@google.com (2024-08-12)

I need a direct reproducer outside of the browser.

### ms...@google.com (2024-08-12)

Extracting the VS from triggerInduction.html and using the steps from [b/350528343#comment110](https://issues.chromium.org/issues/350528343#comment110) I can reproduce the failure on ToT mesa commit `37d0cdc36f6 ("nak: special case PhiDsts as not uniform"`.

### ms...@google.com (2024-08-12)

NIR validation fails after a call to `nir_opt_if` in `brw_nir.c`.

### ms...@google.com (2024-08-12)

redacted

### ms...@google.com (2024-08-12)

(I posted this in comment 17, but must have done something wrong, because it's listed as "Restricted". Reposting here)

The validation errors are

```
block b13:  // preds: b12
            32    %59 = phi b12: %18, b11: %87
error: exec_list_length(&instr->srcs) == state->block->predecessors->entries (../src/compiler/nir/nir_validate.c:1036)

            32    %60 = phi b12: %19, b11: %88
error: exec_list_length(&instr->srcs) == state->block->predecessors->entries (../src/compiler/nir/nir_validate.c:1036)

            32    %61 = phi b12: %20, b11: %89
error: exec_list_length(&instr->srcs) == state->block->predecessors->entries (../src/compiler/nir/nir_validate.c:1036)

            32    %62 = phi b12: %21, b11: %90
error: exec_list_length(&instr->srcs) == state->block->predecessors->entries (../src/compiler/nir/nir_validate.c:1036)

            32    %63 = phi b12: %83, b11: %91
error: exec_list_length(&instr->srcs) == state->block->predecessors->entries (../src/compiler/nir/nir_validate.c:1036)

            1     %64 = phi b12: %23, b11: %92
error: exec_list_length(&instr->srcs) == state->block->predecessors->entries (../src/compiler/nir/nir_validate.c:1036)

            1     %85 = iand %16, %0 (false)
                        // succs: b2 
        }
[...]
1 additional errors:
error: state->nr_tagged_srcs == 0 (../src/compiler/nir/nir_validate.c:1664)

```

And the before-after diff of the NIR is

```
  -            block b16:  // preds: b15                                                                                                                                                                             
  -            32    %59 = phi b15: %18                                                                                                                                                                              
  -            32    %60 = phi b15: %19                                                                                                                                                                              
  -            32    %61 = phi b15: %20                                                                                                                                                                              
  -            32    %62 = phi b15: %21                                                                                                                                                                              
  -            32    %63 = phi b15: %24                                                                                                                                                                              
  -            1     %64 = phi b15: %23                                                                                                                                                                              
  +            block b13:  // preds: b12                                                                                                                                                                             
  +            32    %59 = phi b12: %18, b11: %87                                                                                                                                                                    
  +            32    %60 = phi b12: %19, b11: %88                                                                                                                                                                    
  +            32    %61 = phi b12: %20, b11: %89                                                                                                                                                                    
  +            32    %62 = phi b12: %21, b11: %90                                                                                                                                                                    
  +            32    %63 = phi b12: %83, b11: %91                                                                                                                                                                    
  +            1     %64 = phi b12: %23, b11: %92                                                                                                                                                                    
  +            1     %85 = iand %16, %0 (false)                                                                                                                                                                      
                           // succs: b2

```

so we can see that the phi nodes are gaining an input from block `b11` despite `b11` not being a predecessor.

### ms...@google.com (2024-08-12)

Okay, I think I understand what's going on. `nir_opt_if` is combining:

```
if %16 {
    [then-block-1]
} else {
    [else-block-1]
}

if %16 {
    [then-block-2]
} else {
    [else-block-2]
}

```

into

```
if %16 {
    [them-block-combined]
} else {
    [else-block-combined]
}

```

The block following the if-then-else control flow is `block b16` (before) and `block b13` (after) in the above diff. `nir_opt_if` assumes that when it combines the if-then-else control flow that it needs to update the subsequent phi nodes, but because of the infinite loop in `else-block-2`, `else-block-combined` does not flow into the block containing the phis.

### ms...@google.com (2024-08-12)

This fixes it:

```
diff --git a/src/compiler/nir/nir_opt_if.c b/src/compiler/nir/nir_opt_if.c
index 57bb9e869c8..e561023e2ba 100644
--- a/src/compiler/nir/nir_opt_if.c
+++ b/src/compiler/nir/nir_opt_if.c
@@ -1161,7 +1161,9 @@ opt_if_merge(nir_if *nif)
        * opt_if_evaluate_condition_use will optimize it later.
        */
       if (nir_block_ends_in_jump(nir_if_last_then_block(nif)) ||
-          nir_block_ends_in_jump(nir_if_last_else_block(nif)))
+          nir_block_ends_in_jump(nir_if_last_else_block(nif)) ||
+          nir_block_ends_in_jump(nir_if_last_then_block(next_if)) ||
+          nir_block_ends_in_jump(nir_if_last_else_block(next_if)))
          return false;
 
       simple_merge_if(nif, next_if, true, true);

```

I'll write a commit message and make an upstream merge request. I'll also try to create a piglit test for this case.

### ms...@google.com (2024-08-12)

I've made an upstream merge request: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/30629>

I tried for a bit to create a piglit test, but I couldn't craft something that hit the appropriate condition even when using the vertex shader from this report as a base. It seems you'd have to craft some pretty specific code that avoids other optimization passes in order to get the appropriate control flow and conditions in `nir_opt_if`.

### ms...@google.com (2024-08-12)

Confirmed that triggerInduction.html does not crash the browser/GPU process with my patch.

### kb...@chromium.org (2024-08-13)

Thanks very much Matt for tracking this down and fixing it! Now that we know the root cause it'll hopefully be easier to reject these shaders at the ANGLE level.

### ms...@google.com (2024-08-15)

Glad to get the opportunity to help!

I've addressed the feedback on the upstream MR and added unit tests that provoke the bug reported here. I expect the MR to land today or tomorrow and then I'll immediately cherry-pick the fix into ChromeOS's `mesa-iris` package and mark this as fixed.

### ms...@google.com (2024-08-16)

Patch landed upstream. Backport CL made here: [crrev/c/5793632](https://crrev.com/c/5793632).

### ap...@google.com (2024-08-16)

Project: chromiumos/third_party/mesa
Branch: chromeos-iris

commit ab9ad2e2f1306c2d2e2f36b10e2a284797d440b3
Author: Matt Turner <mattst88@gmail.com>
Date:   Mon Aug 12 15:26:57 2024

    UPSTREAM: nir: Skip opt_if_merge when next_if has block ending in a jump
    
    Similar to commit 6cef8040672 ("nir/opt_if: fix opt_if_merge when
    destination branch has a jump"), we shouldn't combine if statements when
    the second if-then-else has a block that ends in a jump.
    
    This fixes a case where opt_if_merge combines
    
        if (cond) {
            [then-block-1]
        } else {
            [else-block-1]
        }
    
        if (cond) {
            [then-block-2]
        } else {
            [else-block-2]
        }
    
    where `then-block-2` or `else-block-2` ends in a jump. The phi nodes
    following the control flow will be incorrectly updated to have an input
    from a block that is not a predecessor.
    
    Fixes: 4d3f6cb9739 ("nir: merge some basic consecutive ifs")
    Reviewed-by: Rhys Perry <pendingchaos02@gmail.com>
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/30629>
    (cherry picked from commit d2e6be94aebf20c9220e53e9f9dd9c0386b27676
     https://gitlab.freedesktop.org/mesa/mesa.git main)
    
    BUG=b:357484640
    TEST=Run crafted SPIR-V shader without crashing
    
    Change-Id: I30ec4738a14ed72bb52cd4976e98ec91a601d81f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5793632
    Reviewed-by: Sean Paul <sean@poorly.run>
    Reviewed-by: Prahlad Kilambi <prahladk@google.com>
    Commit-Queue: Matt Turner <msturner@google.com>
    Auto-Submit: Matt Turner <msturner@google.com>
    Tested-by: Matt Turner <msturner@google.com>

M       src/compiler/nir/nir_opt_if.c

https://chromium-review.googlesource.com/5793632


### ms...@google.com (2024-08-19)

Backported to mesa-iris. I think we're done here. Thanks!

### pe...@google.com (2024-08-19)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### kb...@chromium.org (2024-08-20)

Thank you Matt for diagnosing and driving this tricky fix!

### sp...@google.com (2024-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in the GPU process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-29)

Congratulations! Thank you for your efforts and reporting this issue to us!

### ap...@google.com (2024-09-17)

Project: chromiumos/third_party/mesa
Branch: chromeos-iris

commit a4bfafac68c3b54777fffd6e546250c5c2657039
Author: Matt Turner <mattst88@gmail.com>
Date:   Mon Aug 12 15:26:57 2024

    UPSTREAM: nir: Skip opt_if_merge when next_if has block ending in a jump
    
    Similar to commit 6cef8040672 ("nir/opt_if: fix opt_if_merge when
    destination branch has a jump"), we shouldn't combine if statements when
    the second if-then-else has a block that ends in a jump.
    
    This fixes a case where opt_if_merge combines
    
        if (cond) {
            [then-block-1]
        } else {
            [else-block-1]
        }
    
        if (cond) {
            [then-block-2]
        } else {
            [else-block-2]
        }
    
    where `then-block-2` or `else-block-2` ends in a jump. The phi nodes
    following the control flow will be incorrectly updated to have an input
    from a block that is not a predecessor.
    
    Fixes: 4d3f6cb9739 ("nir: merge some basic consecutive ifs")
    Reviewed-by: Rhys Perry <pendingchaos02@gmail.com>
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/30629>
    (cherry picked from commit d2e6be94aebf20c9220e53e9f9dd9c0386b27676
     https://gitlab.freedesktop.org/mesa/mesa.git main)
    
    BUG=b:357484640, b:360875983
    TEST=Run crafted SPIR-V shader without crashing
    
    Change-Id: I739067e1475386e0ffca020d9a415f19a865f002
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5797927
    Reviewed-by: Lina Versace <linyaa@google.com>
    Commit-Queue: Matt Turner <msturner@google.com>
    Reviewed-by: Sean Paul <sean@poorly.run>
    Tested-by: Matt Turner <msturner@google.com>
    Auto-Submit: Matt Turner <msturner@google.com>

M       src/compiler/nir/nir_opt_if.c

https://chromium-review.googlesource.com/5797927


### ap...@google.com (2024-09-19)

Project: chromiumos/third_party/mesa
Branch: chromeos-iris

commit 1d9898b043a2fdaf5ab541125bee9b0d0dd69a3b
Author: Jim Pollock <jmpollock@chromium.org>
Date:   Thu Sep 19 05:54:07 2024

    Revert "UPSTREAM: nir: Skip opt_if_merge when next_if has block ending in a jump"
    
    This reverts commit a4bfafac68c3b54777fffd6e546250c5c2657039.
    
    Reason for revert: b/367853536
    
    Original change's description:
    > UPSTREAM: nir: Skip opt_if_merge when next_if has block ending in a jump
    >
    > Similar to commit 6cef8040672 ("nir/opt_if: fix opt_if_merge when
    > destination branch has a jump"), we shouldn't combine if statements when
    > the second if-then-else has a block that ends in a jump.
    >
    > This fixes a case where opt_if_merge combines
    >
    >     if (cond) {
    >         [then-block-1]
    >     } else {
    >         [else-block-1]
    >     }
    >
    >     if (cond) {
    >         [then-block-2]
    >     } else {
    >         [else-block-2]
    >     }
    >
    > where `then-block-2` or `else-block-2` ends in a jump. The phi nodes
    > following the control flow will be incorrectly updated to have an input
    > from a block that is not a predecessor.
    >
    > Fixes: 4d3f6cb9739 ("nir: merge some basic consecutive ifs")
    > Reviewed-by: Rhys Perry <pendingchaos02@gmail.com>
    > Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/30629>
    > (cherry picked from commit d2e6be94aebf20c9220e53e9f9dd9c0386b27676
    >  https://gitlab.freedesktop.org/mesa/mesa.git main)
    >
    > BUG=b:357484640, b:360875983
    > TEST=Run crafted SPIR-V shader without crashing
    >
    > Change-Id: I739067e1475386e0ffca020d9a415f19a865f002
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5797927
    > Reviewed-by: Lina Versace <linyaa@google.com>
    > Commit-Queue: Matt Turner <msturner@google.com>
    > Reviewed-by: Sean Paul <sean@poorly.run>
    > Tested-by: Matt Turner <msturner@google.com>
    > Auto-Submit: Matt Turner <msturner@google.com>
    
    BUG=b:357484640, b:360875983, b:367853536
    
    Change-Id: Ie490c196e6546b0d1f5f194ae287868104a9e393
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5872308
    Tested-by: Matt Turner <msturner@google.com>
    Reviewed-by: Madhav <madhavadas@google.com>
    Owners-Override: Madhav <madhavadas@google.com>
    Reviewed-by: Jonathon Murphy <jpmurphy@google.com>

M       src/compiler/nir/nir_opt_if.c

https://chromium-review.googlesource.com/5872308


### qk...@google.com (2024-09-20)

The fix was reverted because it made a lot of failure on the bot with "stablize_dut_failed"[1]. So I marked LTS-NotApplicable-120, LTS-NotApplicable-126 labels to this bug for now. 

[1] https://b.corp.google.com/issues/367853536#comment1

### ms...@google.com (2024-09-20)

[Comment #32](https://issues.chromium.org/issues/357484640#comment32) is showing the patch cherry-picked after the mesa-iris uprev. [Comment #33](https://issues.chromium.org/issues/357484640#comment33) is showing that patch reverted as a part of reverting the mesa-iris uprev.

The original fix (in [comment #26](https://issues.chromium.org/issues/357484640#comment26)) is still in place.

### ms...@google.com (2024-09-20)

(The problem with "stabilize\_dut\_failed" was unrelated to this patch)

### kb...@chromium.org (2024-09-20)

Reopening because the CL chain in Mesa fixing this had to be reverted due to regressions on ChromeOS.

### pe...@google.com (2024-09-21)

We commit ourselves to a 30 day deadline for fixing for s0 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ms...@google.com (2024-09-23)

> Reopening because the CL chain in Mesa fixing this had to be reverted due to regressions on ChromeOS.

No, the patch is still applied and shipping.

In [comment #35](https://issues.chromium.org/issues/357484640#comment35), I was explaining that after updating the mesa-iris package that the patch applies to, I reapplied the patch. So in order to revert the update to mesa-iris I had to revert the patch (that had been reapplied on top of the update).

But the original fix is still in the current branch and is still shipping.

### kb...@chromium.org (2024-09-23)

Thanks Matt for clarifying - I still don't fully understand the state of things on ChromeOS. If any comments can be added to [Bug 367853536](https://issues.chromium.org/issues/367853536) describing the current state, I think that would help. (What was the root cause of the stabilize\_dut\_failed failures?)

### ms...@google.com (2024-09-23)

Good idea. I'll write up exactly what happened and link to it here.

### ms...@google.com (2024-09-23)

Posted here: [b/367853536#comment52](https://issues.chromium.org/issues/367853536#comment52)

### pe...@google.com (2024-09-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-09-27)

1. https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5894196/ and https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5894400
2. Low, no conflicts
3. No
4. The author thinks the bug can happen on M126. Although the fix was reverted, he told(#comment39) that the patch is still applied and shipping. But, the fix caused a few tests to begin timing out in Android CTS though, the regression was fixed by https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5894400. So, I think it would be good to merge the 2 patches together to M126.

### gm...@google.com (2024-09-27)

This has been merged to 129 and 130. Delaying LTS approval.

### gm...@google.com (2024-10-08)

Agree with both patches, Approving for 126.

### ap...@google.com (2024-10-10)

Project: chromiumos/third\_party/mesa  

Branch: release-R126-15886.B-chromeos-iris  

Author: Matt Turner <[mattst88@gmail.com](mailto:mattst88@gmail.com)>  

Link:      <https://chromium-review.googlesource.com/5894196>

[M126-LTS] UPSTREAM: nir: Skip opt\_if\_merge when next\_if has block ending in a jump

---


Expand for full commit details
```
[M126-LTS] UPSTREAM: nir: Skip opt_if_merge when next_if has block ending in a jump

Similar to commit 6cef8040672 ("nir/opt_if: fix opt_if_merge when
destination branch has a jump"), we shouldn't combine if statements when
the second if-then-else has a block that ends in a jump.

This fixes a case where opt_if_merge combines

    if (cond) {
        [then-block-1]
    } else {
        [else-block-1]
    }

    if (cond) {
        [then-block-2]
    } else {
        [else-block-2]
    }

where `then-block-2` or `else-block-2` ends in a jump. The phi nodes
following the control flow will be incorrectly updated to have an input
from a block that is not a predecessor.

Fixes: 4d3f6cb9739 ("nir: merge some basic consecutive ifs")
Reviewed-by: Rhys Perry <pendingchaos02@gmail.com>
Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/30629>
(cherry picked from commit d2e6be94aebf20c9220e53e9f9dd9c0386b27676
 https://gitlab.freedesktop.org/mesa/mesa.git main)

BUG=b:357484640, b:360875983
TEST=Run crafted SPIR-V shader without crashing

Change-Id: I739067e1475386e0ffca020d9a415f19a865f002
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5797927
Reviewed-by: Lina Versace <linyaa@google.com>
Commit-Queue: Matt Turner <msturner@google.com>
Reviewed-by: Sean Paul <sean@poorly.run>
Tested-by: Matt Turner <msturner@google.com>
Auto-Submit: Matt Turner <msturner@google.com>
(cherry picked from commit a4bfafac68c3b54777fffd6e546250c5c2657039)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/5894196
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Matt Turner <msturner@google.com>
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Tested-by: Gyuyoung Kim (xWF) <qkim@google.com>

```

---

Files:

- M `src/compiler/nir/nir_opt_if.c`

---

Hash: 346dfe65983e2af261d3d3bb2d5ef8babea94bbd  

Date:  Mon Aug 12 15:26:57 2024


---

### pe...@google.com (2024-12-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/357484640)*
