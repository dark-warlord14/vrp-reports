# GPU process crash via WebGPU shader - global-buffer-overflow in Mesa lower_mem_store

| Field | Value |
|-------|-------|
| **Issue ID** | [425271170](https://issues.chromium.org/issues/425271170) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | a7...@gmail.com |
| **Assignee** | pg...@google.com |
| **Created** | 2025-06-16 |
| **Bounty** | $1,000.00 |

## Description

#### VULNERABILITY DETAILS

This report is about a global-buffer-overflow in the Mesa shader compiler, reachable via WebGPU shaders emitted by dawn/tint. The offending shader looks as follows:

```
@group(0) @binding(0)
var<storage, read_write> g: array<f32>;

@compute @workgroup_size(1)
fn main(@builtin(global_invocation_id) l_1: vec3<u32>) {
    let l_2 = l_1.y * 4;
    if (l_2 == 1u) {
        g[l_1.y] = 0;
    }
}

```

I suspect the issue is an AMD-specific code-path as the fuzzer is not finding similar crashes when using the Intel backend. This is corroborated by the bisect which points to Mesa commit 8fdc5d7. The commit adds the AMD-specific function `nir_lower_mem_access_bit_sizes`.

#### VERSION

Chrome Version: Version 139.0.7237.0 (Developer Build) (64-bit) (ASAN build)   

Operating System: Ubuntu 25.04   

Mesa: mesa-25.1.3 commit ba95e69

#### REPRODUCTION

There are two means of reproduction, standalone and via Chrome. In either case you'll need an ASAN build of Mesa. Precise built instructions depend on the distro, a complete example for Ubuntu is part of the Dockerfile file of the standalone reproducer.

##### Standalone

1. Place the Dockerfile and the `.gfxr` in a new directory
2. Inside this directory: `docker build -t mesarepo .`
3. Once built, switch into the container: `docker run -it mesarepo /bin/bash`
4. Inside the container, run: `LD_PRELOAD="/usr/lib/llvm-20/lib/clang/20/lib/linux/libclang_rt.asan-x86_64.so /mesa/buildASAN/src/amd/drm-shim/libamdgpu_noop_drm_shim.so" VK_DRIVER_FILES=/mesa/buildASAN/src/amd/vulkan/radeon_icd.x86_64.json /gfxreconstruct/build/tools/replay/gfxrecon-replay /gfxrecon.gfxr`

##### Chrome

Reproducing the issue in Chrome requires an ASAN build of Mesa as well as an ASAN build of Chromium. Note that the issue seems to be in an AMD-specific code path, requiring an AMD GPU for reproduction. The crash in Chrome has been observed using an AMD RX 7600. Opening the attached html file should trigger a global-buffer-overflow ASAN violation in the Chrome GPU process. Start chrome and run it with the ASAN version of mesa (adapt paths as needed): `ASAN_OPTIONS=external_symbolizer_path=/usr/lib/llvm-20/bin/llvm-symbolizer VK_DRIVER_FILES=/path/to/src/amd/vulkan/radeon_icd.x86_64.json ./chrome --user-data-dir=/tmp/deleteme --use-angle=vulkan --enable-features=Vulkan --disable-gpu-watchdog --no-sandbox --enable-unsafe-webgpu` and open the attached html:

```
=================================================================
==4229==ERROR: AddressSanitizer: global-buffer-overflow on address 0x6fe27c17e37c at pc 0x6fe27cbbb6ad bp 0x7ffc59eaff20 sp 0x7ffc59eaff18
READ of size 4 at 0x6fe27c17e37c thread T0 (chrome)
    #0 0x6fe27cbbb6ac in nir_op_vec /home/user/mesa/buildASAN/../src/compiler/nir/nir.c:2950:4
    #1 0x6fe27cc701a1 in nir_vec /home/user/mesa/buildASAN/../src/compiler/nir/nir_builder.h:683:40
    #2 0x6fe27cc701a1 in nir_extract_bits /home/user/mesa/buildASAN/../src/compiler/nir/nir_builder.h:1448:14
    #3 0x6fe27cc6cae9 in lower_mem_store /home/user/mesa/buildASAN/../src/compiler/nir/nir_lower_mem_access_bit_sizes.c:448:28
    #4 0x6fe27cc6cae9 in lower_mem_access_instr /home/user/mesa/buildASAN/../src/compiler/nir/nir_lower_mem_access_bit_sizes.c:543:14
    #5 0x6fe27cc69b18 in nir_function_instructions_pass /home/user/mesa/buildASAN/../src/compiler/nir/nir_builder.h:108:22
    #6 0x6fe27cc69b18 in nir_shader_instructions_pass /home/user/mesa/buildASAN/../src/compiler/nir/nir_builder.h:134:19
    #7 0x6fe27cc69b18 in nir_lower_mem_access_bit_sizes /home/user/mesa/buildASAN/../src/compiler/nir/nir_lower_mem_access_bit_sizes.c:555:11
    #8 0x6fe27c8af2b1 in ac_nir_lower_mem_access_bit_sizes /home/user/mesa/buildASAN/../src/amd/common/nir/ac_nir_lower_mem_access_bit_sizes.c:143:11
    #9 0x6fe27c57541e in radv_postprocess_nir /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline.c:374:4
    #10 0x6fe27c58317f in radv_compile_cs /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_compute.c:119:4
    #11 0x6fe27c58400b in radv_compute_pipeline_compile /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_compute.c:218:7
    #12 0x6fe27c58400b in radv_compute_pipeline_create /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_compute.c:299:16
    #13 0x6fe27c58464a in radv_create_compute_pipelines /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_compute.c:327:11
    #14 0x6fe27c58464a in radv_CreateComputePipelines /home/user/mesa/buildASAN/../src/amd/vulkan/radv_pipeline_compute.c:356:11
    #15 0x63aef56bf92f in dawn::native::vulkan::ComputePipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/ComputePipelineVk.cpp:124:5
    #16 0x63aef5497df7 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:383:5
    #17 0x63aef53b0278 in dawn::native::DeviceBase::CreateComputePipeline(dawn::native::ComputePipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1952:52
    #18 0x63aef53afc78 in dawn::native::DeviceBase::APICreateComputePipeline(dawn::native::ComputePipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1270:26
    #19 0x63af115f49af in dawn::wire::server::Server::DoDeviceCreateComputePipeline(WGPUDeviceImpl*, WGPUComputePipelineDescriptor const*, WGPUComputePipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:243:9
    #20 0x63af115e425c in dawn::wire::server::Server::HandleDeviceCreateComputePipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:466:9
    #21 0x63af115ef3c4 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1644:30
    #22 0x63af115a9900 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1061:33
    #23 0x63af115a9d93 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2002:22
    #24 0x63af1159bfd1 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1947:18
    #25 0x63af10de9377 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:265:35
    #26 0x63af10dc8bb7 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:506:22
    #27 0x63af10dc7d8a in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:162:7
    #28 0x63af10df53ad in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:886:13
    #29 0x63af10e04727 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:731:12
    #30 0x63af10e0450f in MakeItSo<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:947:5
    #31 0x63af10e0450f in RunImpl<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #32 0x63af10e0450f in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:973:12
    #33 0x63af0f72c545 in Run base/functional/callback.h:156:12
    #34 0x63af0f72c545 in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:806:49
    #35 0x63af0f72c545 in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #36 0x63af0f72c545 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1060:14
    #37 0x63af0f706dec in Run base/functional/callback.h:156:12
    #38 0x63af0f706dec in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:672:29
    #39 0x63af0f704a4c in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:594:3
    #40 0x63af0f708f73 in Invoke<void (Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:731:12
    #41 0x63af0f708f73 in MakeItSo<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #42 0x63af0f708f73 in RunImpl<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1060:14
    #43 0x63af0f708f73 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #44 0x63af08408f66 in Run base/functional/callback.h:156:12
    #45 0x63af08408f66 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:207:34
    #46 0x63af0847ba57 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:104:5
    #47 0x63af0847ba57 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #48 0x63af0847a93c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #49 0x63af0847c54a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #50 0x63af082cfd03 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #51 0x63af0847d104 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #52 0x63af0838806f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #53 0x63af12ace571 in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:454:14
    #54 0x63af04fabfac in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:702:14
    #55 0x63af04facf7c in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:804:12
    #56 0x63af04faf931 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1198:10
    #57 0x63af04fa9ce9 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:362:36
    #58 0x63af04faa20b in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:375:10
    #59 0x63aef2290f27 in ChromeMain chrome/app/chrome_main.cc:222:12
    #60 0x73e28622a337 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #61 0x73e28622a3fa in __libc_start_main csu/../csu/libc-start.c:360:3
    #62 0x63aef21b5029 in _start (/home/user/Downloads/linux-1473520/chrome+0xfbbf029) (BuildId: 836701a81112c94a)

0x6fe27c17e37c is located 4 bytes before global variable 'switch.table.nir_op_vec' defined in '../src/compiler/nir/nir.c' (0x6fe27c17e380) of size 64
0x6fe27c17e37c is located 37 bytes after global variable 'switch.table.nir_get_nir_type_for_glsl_base_type' defined in '../src/compiler/nir/nir.c' (0x6fe27c17e340) of size 23
0x6fe27c17e37c is located 4 bytes before global variable 'switch.table.nir_op_vec' defined in '../src/compiler/nir/nir.c' (0x6fe27c17e380) of size 64
0x6fe27c17e37c is located 37 bytes after global variable 'switch.table.nir_get_nir_type_for_glsl_base_type' defined in '../src/compiler/nir/nir.c' (0x6fe27c17e340) of size 23
SUMMARY: AddressSanitizer: global-buffer-overflow /home/user/mesa/buildASAN/../src/compiler/nir/nir.c:2950:4 in nir_op_vec
Shadow bytes around the buggy address:
  0x6fe27c17e080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fe27c17e100: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fe27c17e180: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fe27c17e200: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x6fe27c17e280: 00 00 00 00 00 00 00 00 04 f9 f9 f9 f9 f9 f9 f9
=>0x6fe27c17e300: f9 f9 f9 f9 f9 f9 f9 f9 00 00 07 f9 f9 f9 f9[f9]
  0x6fe27c17e380: 00 00 00 00 00 00 00 00 f9 f9 f9 f9 00 00 07 f9
  0x6fe27c17e400: f9 f9 f9 f9 00 00 07 f9 f9 f9 f9 f9 00 00 00 00
  0x6fe27c17e480: 00 f9 f9 f9 f9 f9 f9 f9 00 06 f9 f9 00 00 00 00
  0x6fe27c17e500: 00 00 00 00 04 f9 f9 f9 f9 f9 f9 f9 00 00 00 00
  0x6fe27c17e580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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

==4229==ADDITIONAL INFO

==4229==Note: Please include this section with the ASan report.
Task trace:
    #0 0x63af0f700b7d in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*) gpu/command_buffer/service/scheduler.cc:412:29


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --ozone-platform=wayland --use-angle=vulkan --crashpad-handler-pid=4185 --enable-crash-reporter=, --user-data-dir=/tmp/deleteme --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAoAQAIAAAAAAAAAAAAAMAAAgAAAAIAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,5323047306905283140,3680587412988863138,262144 --field-trial-handle=3,i,13885978254897881502,8627082155501245184,262144 --enable-features=Vulkan --disable-features=EyeDropper --variations-seed-version`

==4229==END OF ADDITIONAL INFO
==4229==ABORTING

```

## Attachments

- [radv_nir_op_vec.html](attachments/radv_nir_op_vec.html) (text/html, 2.7 KB)
- [gfxrecon_capture_radv_nir_op_vec.gfxr](attachments/gfxrecon_capture_radv_nir_op_vec.gfxr) (application/octet-stream, 7.9 KB)
- [Dockerfile](attachments/Dockerfile) (application/octet-stream, 2.0 KB)

## Timeline

### a7...@gmail.com (2025-06-16)

Upstream report <https://gitlab.freedesktop.org/mesa/mesa/-/issues/13362>

### pg...@google.com (2025-06-16)

I have not been able to reproduce, but this seems legitimate.

Setting S1 - Memory corruption on GPU would be S0, but on Linux WebGPU is not enabled by default and on ChromeOS the GPU process is somewhat sandboxed.
Setting foundin to the current extended to be safe, since I cant tell how far back the issue goes - hoping the GPU folks can help answer that question!

Bug seems to be within mesa driver, so setting external dependency hotlist, but perhaps Chrome can have a mitigation on our end? 
cc'ing some GPU folks to take a look!

### ch...@google.com (2025-06-17)

Setting milestone because of s0/s1 severity.

### a7...@gmail.com (2025-06-17)

This issue was already fixed in the `main` branch of upstream one month ago, see <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/34976>   

Due to the report Mesa is backporting the fix to the current release branch, see <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/35575>

### ms...@google.com (2025-06-24)

This is specific to AMD, reassigning to olv@.

### ol...@google.com (2025-06-24)

Our Mesa driver does not have the [offending commit](https://gitlab.freedesktop.org/mesa/mesa/-/commit/8fdc5d7f9f853dcea6d8934239a3a63ad8e87ff9). Let me check if I can repro.

### ol...@google.com (2025-06-24)

Neither `radv_nir_op_vec.html` nor `gfxrecon_capture_radv_nir_op_vec.gfxr` reproduces on amd chromeos with stock mesa.

Furthermore, I can confirm that `gfxrecon_capture_radv_nir_op_vec.gfxr` crashes with mesa 25.1.3 but is fine with 25.1.4.

### pg...@google.com (2025-06-25)

Hi @reporter - we were unable to reproduce on our side ([comment #8](https://issues.chromium.org/issues/425271170#comment8)) and see that the offending commit is not in the Mesa driver that Chrome uses ([comment #7](https://issues.chromium.org/issues/425271170#comment7)) - could you provide more details on how you were able to reproduce this from Chrome using radv\_nir\_op\_vec.html - im assuming then this is Ubuntu specific?

but if it does repro on Ubuntu, sounds like getting the mesa driver used to 25.1.4 is the way forward

### a7...@gmail.com (2025-06-26)

I did reproduce the issue on Ubuntu with the ASAN version of Mesa 25.1.3 + ASAN version of Chromium; the exact command line flags are part of the initial report. The issue per se isn't Ubuntu-specific; but since the fix was already part of `main` and is now backported to the latest released version (25.1.4) I think this issue can be closed.

### pe...@google.com (2025-06-26)

Thank you for providing more feedback. Adding the requester to the CC list.

### ch...@google.com (2025-06-26)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-06-27)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M138. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [138, 139].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sp...@google.com (2025-07-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Thank you reward for report that result in backmerges of GPU driver change upstream 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-07-02)

Thank you for your report to us and upstream that resulted in the fix for this issue landed prior to this report being backmerged upstream by AMD.
 

### ch...@google.com (2025-10-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/425271170)*
