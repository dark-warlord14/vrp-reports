#  GPU process crash via WebGPU shader - stack-buffer-overflow in Mesa nir_extract_bits 

| Field | Value |
|-------|-------|
| **Issue ID** | [408364839](https://issues.chromium.org/issues/408364839) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | a7...@gmail.com |
| **Assignee** | cw...@chromium.org |
| **Created** | 2025-04-04 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

This report is about a stack-buffer-overflow in Mesa, reachable via WebGPU shaders emitted by dawn/tint. I will also upload this report upstream, i.e., the Mesa project, and post the link below.

##### VERSION

Chrome Version: 137.0.7108.0 (Developer Build) (64-bit) (ASAN build)   

Operating System: Ubuntu 24.04   

Mesa: mesa-25.0.3 commit ff386eb

##### REPRODUCTION CASE

The bug is provoked by compiling the following shader, first with tint to SPIR-V and then later with Mesa:

```
@group(0) @binding(0)
var<storage, read_write> e: array<f32>;

fn f(g: u32) {
  e[g] = 0;
}

@compute @workgroup_size(1)
fn comp(@builtin(local_invocation_id) k: vec3<u32>, @builtin(global_invocation_id) l: vec3<u32>) {
  let n = l.y * 4;
  if (n == 3) {
    f(k[n]);
    f(1);
    f(l.y);
  }
}

```

There are two means of reproduction, first the standalone reproduction via gfxrecon-replay.
The attached .gfxr allows to reproduce outside of chrome as follows:   

`LD_PRELOAD=/usr/lib/llvm-18/lib/clang/18/lib/linux/libclang_rt.asan-x86_64.so VK_DRIVER_FILES=~/src/intel/vulkan/intel_icd.x86_64.json ASAN_OPTIONS=detect_leaks=0,abort_on_error=1 ~/gfxrecon-replay gfxrecon_capture_20250404T174811.gfxr`

Reproducing the issue in Chrome requires an ASAN build of Mesa as well as an ASAN build of Chromium. Opening the attached html file should trigger the OOB in the Chrome GPU process:

```
=================================================================
==28082==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x79ab771ccd08 at pc 0x79ab6e74d06a bp 0x7ffc16030af0 sp 0x7ffc16030ae8
READ of size 8 at 0x79ab771ccd08 thread T0 (chrome)
    #0 0x79ab6e74d069 in nir_extract_bits /home/user/chromeosMesaOrg/buildASAN/../src/compiler/nir/nir_builder.h:1363:25
    #1 0x79ab6e742376 in vectorize_stores /home/user/chromeosMesaOrg/buildASAN/../src/compiler/nir/nir_opt_load_store_vectorize.c
    #2 0x79ab6e742376 in try_vectorize /home/user/chromeosMesaOrg/buildASAN/../src/compiler/nir/nir_opt_load_store_vectorize.c:1233:7
    #3 0x79ab6e742376 in vectorize_sorted_entries /home/user/chromeosMesaOrg/buildASAN/../src/compiler/nir/nir_opt_load_store_vectorize.c:1365:17
    #4 0x79ab6e742376 in vectorize_entries /home/user/chromeosMesaOrg/buildASAN/../src/compiler/nir/nir_opt_load_store_vectorize.c:1395:14
    #5 0x79ab6e73d3ec in process_block /home/user/chromeosMesaOrg/buildASAN/../src/compiler/nir/nir_opt_load_store_vectorize.c:1547:19
    #6 0x79ab6e73d3ec in nir_opt_load_store_vectorize /home/user/chromeosMesaOrg/buildASAN/../src/compiler/nir/nir_opt_load_store_vectorize.c:1569:22
    #7 0x79ab6ea1a499 in brw_vectorize_lower_mem_access /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_nir.c:1655:4
    #8 0x79ab6ea1a499 in brw_postprocess_nir /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_nir.c:1774:4
    #9 0x79ab6e92d633 in brw_compile_cs /home/user/chromeosMesaOrg/buildASAN/../src/intel/compiler/brw_compile_cs.cpp:188:7
    #10 0x79ab6d75cd15 in anv_pipeline_compile_cs /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:2610:20
    #11 0x79ab6d75cd15 in anv_compute_pipeline_create /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:2715:13
    #12 0x79ab6d75cd15 in anv_CreateComputePipelines /home/user/chromeosMesaOrg/buildASAN/../src/intel/vulkan/anv_pipeline.c:2748:22
    #13 0x577df69a117c in dawn::native::vulkan::ComputePipeline::InitializeImpl() third_party/dawn/src/dawn/native/vulkan/ComputePipelineVk.cpp:125:9
    #14 0x577df67bec27 in dawn::native::PipelineBase::Initialize(std::__Cr::optional<dawn::native::PerStage<dawn::native::APIRef<dawn::native::ShaderModuleBase>>>) third_party/dawn/src/dawn/native/Pipeline.cpp:383:5 
    #15 0x577df66ee028 in dawn::native::DeviceBase::CreateComputePipeline(dawn::native::ComputePipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:2027:52
    #16 0x577df66eda38 in dawn::native::DeviceBase::APICreateComputePipeline(dawn::native::ComputePipelineDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1299:26
    #17 0x577e12271cdf in dawn::wire::server::Server::DoDeviceCreateComputePipeline(WGPUDeviceImpl*, WGPUComputePipelineDescriptor const*, WGPUComputePipelineImpl**) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:243:9 
    #18 0x577e1226157c in dawn::wire::server::Server::HandleDeviceCreateComputePipeline(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:466:9
    #19 0x577e1226c6d4 in dawn::wire::server::Server::HandleCommandsImpl(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1644:30
    #20 0x577e12227790 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:1040:33
    #21 0x577e12227c23 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1967:22
    #22 0x577e12219f31 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1912:18
    #23 0x577e11a8aa37 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:263:35
    #24 0x577e11a69c4b in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:507:22
    #25 0x577e11a68e1a in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:163:7
    #26 0x577e11a95e0d in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:958:13
    #27 0x577e11aa5177 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:731:12
    #28 0x577e11aa4f5f in MakeItSo<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:947:5
    #29 0x577e11aa4f5f in RunImpl<void (GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> base/functional/bind_internal.h:1060:14
    #30 0x577e11aa4f5f in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:973:12
    #31 0x577e0e27b7c5 in Run base/functional/callback.h:156:12
    #32 0x577e0e27b7c5 in Invoke<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, gpu::FenceSyncReleaseDelegate *> base/functional/bind_internal.h:806:49
    #33 0x577e0e27b7c5 in MakeItSo<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #34 0x577e0e27b7c5 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1060:14
    #35 0x577e0e2564a4 in Run base/functional/callback.h:156:12
    #36 0x577e0e2564a4 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/scheduler.cc:672:29
    #37 0x577e0e25410c in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:594:3
    #38 0x577e0e258593 in Invoke<void (Scheduler::*)(), gpu::Scheduler *> base/functional/bind_internal.h:731:12
    #39 0x577e0e258593 in MakeItSo<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > base/functional/bind_internal.h:923:12
    #40 0x577e0e258593 in RunImpl<void (Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1060:14
    #41 0x577e0e258593 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:973:12
    #42 0x577e08a3cbe6 in Run base/functional/callback.h:156:12
    #43 0x577e08a3cbe6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:209:34
    #44 0x577e08aae5a8 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> base/task/common/task_annotator.h:106:5
    #45 0x577e08aae5a8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #46 0x577e08aad48c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #47 0x577e08aaf2da in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #48 0x577e08908223 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #49 0x577e08aafe8b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #50 0x577e089c07ef in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #51 0x577e1fe4e5bb in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:443:14
    #52 0x577e057a98e0 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:686:14
    #53 0x577e057aa85f in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:790:12
    #54 0x577e057ad0e5 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1155:10
    #55 0x577e057a76ab in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:359:36
    #56 0x577e057a7bcb in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:372:10
    #57 0x577df33e393f in ChromeMain chrome/app/chrome_main.cc:222:12
    #58 0x7dab8642a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #59 0x7dab8642a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #60 0x577df3308029 in _start (/home/user/Downloads/linux-release-1442635/chrome+0xf6ad029) (BuildId: c898030b07605a10)

Address 0x79ab771ccd08 is located in stack of thread T0 (chrome) at offset 264 in frame
    #0 0x79ab6e73fa1f in vectorize_entries /home/user/chromeosMesaOrg/buildASAN/../src/compiler/nir/nir_opt_load_store_vectorize.c:1381

  This frame has 11 object(s):
    [32, 40) 'src.addr.i134'
    [64, 72) 'src.addr.i126'
    [96, 104) 'src.addr.i74'
    [128, 136) 'src.addr.i'
    [160, 176) '.compoundliteral.i.i.i' (line 246)
    [192, 208) '.compoundliteral28.i.i.i' (line 246)
    [224, 232) 'low_val.i.i.i' (line 886)
    [256, 264) 'high_val.i.i.i' (line 887) <== Memory access at offset 264 overflows this variable
    [288, 416) 'data_channels.i.i.i' (line 892)
    [448, 488) 'b.i149.i' (line 1230)
    [528, 568) 'b.i.i' (line 1281)
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /home/user/chromeosMesaOrg/buildASAN/../src/compiler/nir/nir_builder.h:1363:25 in nir_extract_bits
Shadow bytes around the buggy address:
  0x79ab771cca80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x79ab771ccb00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x79ab771ccb80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x79ab771ccc00: f1 f1 f1 f1 f8 f2 f2 f2 f8 f2 f2 f2 f8 f2 f2 f2
  0x79ab771ccc80: f8 f2 f2 f2 f8 f8 f2 f2 f8 f8 f2 f2 00 f2 f2 f2
=>0x79ab771ccd00: 00[f2]f2 f2 00 00 00 00 00 00 00 00 00 00 00 00
  0x79ab771ccd80: 00 00 00 00 f2 f2 f2 f2 00 00 00 00 00 f2 f2 f2
  0x79ab771cce00: f2 f2 f8 f8 f8 f8 f8 f3 f3 f3 f3 f3 00 00 00 00
  0x79ab771cce80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79ab771ccf00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x79ab771ccf80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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

==28082==ADDITIONAL INFO

==28082==Note: Please include this section with the ASan report.
Task trace:
    #0 0x577e0e254659 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:610:27
    #1 0x577e0e254659 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:610:27
    #2 0x577e0e254659 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:610:27
    #3 0x577e0e254659 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:610:27


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --ozone-platform=wayland --use-angle=vulkan --crashpad-handler-pid=28048 --enable-crash-reporter=, --user-data-dir=/tmp/deleteme --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAoAQAEAAAAAAAAAAAAAAAAAADAAAIAAAACAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,17863684130055059328,1264872595161525766,262144 --field-trial-handle=3,i,17874687443381050132,4301968298168889399,262144 --enable-features=Vulkan --disable-features=EyeDropper --variations-seed-version`


==28082==END OF ADDITIONAL INFO
==28082==ABORTING

```

## Attachments

- [gfxrecon_capture_20250404T174811.gfxr](attachments/gfxrecon_capture_20250404T174811.gfxr) (application/octet-stream, 10.4 KB)
- [nir_extract_bits.html](attachments/nir_extract_bits.html) (text/html, 2.8 KB)

## Timeline

### a7...@gmail.com (2025-04-04)

Upstream report: <https://gitlab.freedesktop.org/mesa/mesa/-/issues/12946>

### ah...@google.com (2025-04-04)

[Primary Security Shepherd]

Thanks for the report!

Assigning to [cwallez@chromium.org](mailto:cwallez@chromium.org)

Setting severity to critical (S0) (Memory corruption in an unsandboxed GPU process when it is reachable directly from web content without compromising the renderer.)

I am assuming this only affects Linux and setting the OS accordingly.

Setting FoundIn to the current extended stable 135.

### am...@chromium.org (2025-04-05)

The vulnerability itself is in the Mesa driver, so I have marked this as an external dependency.
There is the potential a workaround could be made in Chrome, however, it would be more ideal if the vulnerability could be directly addressed in the driver.

I've updated the found-in to 134 since that is the current oldest active release channel in Chrome. However, this is completely moot if the fix is landed the driver. In the case that this is addressed in workaround in shader code, than we would need this reflected.

### a7...@gmail.com (2025-04-05)

Maybe this can be downgraded to S1? On Linux, WebGPU is not enabled by default and on ChromeOS the GPU process is (weakly) sandboxed.

### ch...@google.com (2025-04-05)

Setting milestone because of s0/s1 severity.

### am...@chromium.org (2025-04-05)

Yeah, that's correct. This doesn't really need to be set as P1 since it's on desktop / ChromeOS platform.

### ms...@google.com (2025-04-07)

Caio at Intel has confirmed the issue with a new unit test for the optimization pass, so definitely looks like a Mesa issue. See <https://gitlab.freedesktop.org/mesa/mesa/-/issues/12946#note_2854984>

### ms...@google.com (2025-04-11)

Intel has provided a fix here: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/34414>

I've reviewed it and tested to confirm that it resolves the issue. I'll cherry pick the patch as soon as it's upstream.

### ms...@google.com (2025-04-15)

CL uploaded: [crrev/c/6458319](https://crrev.com/c/6458319)

### dx...@google.com (2025-04-15)

Project: chromiumos/third\_party/mesa  

Branch: chromeos-iris  

Author: Caio Oliveira [caio.oliveira@intel.com](mailto:caio.oliveira@intel.com)  

Link:      <https://chromium-review.googlesource.com/6458319>

UPSTREAM: nir/load\_store\_vectorize: Skip new bit-sizes that are unaligned with high\_offset

---


Expand for full commit details
```
     
    Otherwise this would require combining two values to produce a single 
    (new bit-size) channel, which vectorize_stores() don't handle.  The pass 
    can still keep trying smaller bit-sizes. 
     
    Closes: https://gitlab.freedesktop.org/mesa/mesa/-/issues/12946 
    Fixes: ce9205c03bd ("nir: add a load/store vectorization pass") 
    Reviewed-by: Rhys Perry <pendingchaos02@gmail.com> 
    Part-of: <https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/34414> 
    (cherry picked from commit 2ed79f80ba894bba0d340708c326ac9d59d5795e 
     https://gitlab.freedesktop.org/mesa/mesa.git main) 
     
    BUG=b:408364839 
    TEST=Run crafted WebGPU shader without crashing 
     
    Change-Id: I497ae08a7e8a681bba5c64af34d8bbb589718082 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/mesa/+/6458319 
    Reviewed-by: Sean Paul <sean@poorly.run> 
    Commit-Queue: Juston Li <justonli@google.com> 
    Commit-Queue: Matt Turner <msturner@google.com> 
    Reviewed-by: Juston Li <justonli@google.com> 
    Auto-Submit: Matt Turner <msturner@google.com> 
    Tested-by: Matt Turner <msturner@google.com>

```

---

Files:

- M `src/compiler/nir/nir_opt_load_store_vectorize.c`
- M `src/compiler/nir/tests/load_store_vectorizer_tests.cpp`

---

Hash: 4f45223e101d05cbc6dd3330df6ea50a8c8ad2f4  

Date:  Mon Apr 7 15:18:14 2025


---

### sp...@google.com (2025-04-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in a highly-privileged process 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-18)

Congratulations! Thank you for your efforts and reporting this Mesa driver issue to us -- great work!

### ch...@google.com (2025-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a highly-privileged process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/408364839)*
