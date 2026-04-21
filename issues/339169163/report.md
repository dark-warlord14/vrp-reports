# GPU process crash via WebGPU shader - OOB in ComputeExitLimit at

| Field | Value |
|-------|-------|
| **Issue ID** | [339169163](https://issues.chromium.org/issues/339169163) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-05-07 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this triggers an OOB inside the hlsl compiler. Standalone reproducing on linux triggers a UAF instead.

##### VERSION

Chrome Version: Pre-compiled ASAN Chromium 126.0.6465.0 (Developer Build) (64-bit)  

Operating System: Win10 Build 19045.4291

##### REPRODUCTION CASE

Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process.

Reproducing the issue stand-alone on Linux also possible, this triggers a UAF instead of an OOB:

1. Compile the standalone.wgsl with tint (commit 5976efe6b4b72c822085cf7ee08ad00036888ab5) to hlsl via `./tint standalone.wgsl -o standalone.hlsl`. I also attached standalone.hlsl, but you should get the very same file when compiling standalone.wgsl yourself
2. Compile the hlsl with dxc (commit 773b01272719e07ea369bc17f5ddfce248751c7a): `./dxc-3.7 standalone.hlsl -T cs_6_2`. This should trigger an ASAN violation.

##### Attached:

- html that triggers an ASAN violation in chromium
- wgsl for producing the hlsl shader
- the hlsl shader
- asan log file

```
[6692:7064:0507/074000.582:WARNING:chrome_main_delegate.cc(742)] This is Chrome version 126.0.6465.0 (not a warning)
[6692:5068:0507/074001.205:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[6692:9024:0507/074001.440:ERROR:sandbox_win.cc(913)] Sandbox cannot access executable. Check filesystem permissions are valid. See https://bit.ly/31yqMJR.: Access is denied. (0x5)
[6692:7064:0507/074001.721:WARNING:account_consistency_mode_manager.cc(77)] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
[6692:7064:0507/074002.268:WARNING:browser_management_service.cc(128)] EnterpriseLogoUrl fetch failed with error code -1 and MIME type 
[6692:7064:0507/074004.924:ERROR:network_service_instance_impl.cc(600)] Network service crashed, restarting service.
[6692:7064:0507/074005.111:WARNING:external_registry_loader_win.cc(232)] Error observing HKLM: 5
[6692:3440:0507/074009.806:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[3896:1988:0507/074010.587:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[3896:3148:0507/074016.083:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[6692:1216:0507/074021.929:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[3896:4800:0507/074026.099:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[6692:6224:0507/074041.952:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[3896:3148:0507/074046.143:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[6692:7064:0507/074147.240:INFO:CONSOLE(20)] "[object GPUDevice]", source: file://vboxsvr/shared/indexComputeExitLimit.html (20)
=================================================================
==5716==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x11f6a1ef6c08 at pc 0x7ffed72203f3 bp 0x006a465fba90 sp 0x006a465fbad8
READ of size 8 at 0x11f6a1ef6c08 thread T0
==5716==WARNING: Failed to use and restart external symbolizer!
==5716==*** WARNING: Failed to initialize DbgHelp!              ***
==5716==*** Most likely this means that the app is already      *** 
==5716==*** using DbgHelp, possibly with incompatible flags.    *** 
==5716==*** Due to technical reasons, symbolization might crash *** 
==5716==*** or produce wrong results.                           ***
    #0 0x7ffed72203f2 in llvm::ScalarEvolution::ComputeExitLimit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\ScalarEvolution.cpp:4988
    #1 0x7ffed721da66 in llvm::ScalarEvolution::ComputeBackedgeTakenCount C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\ScalarEvolution.cpp:4875
    #2 0x7ffed721c714 in llvm::ScalarEvolution::getBackedgeTakenInfo C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\ScalarEvolution.cpp:4624
    #3 0x7ffed721bc7e in llvm::ScalarEvolution::getSmallConstantTripCount C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\ScalarEvolution.cpp:4500
    #4 0x7ffed67fae9d in `anonymous namespace'::LoopUnroll::runOnLoop C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\LoopUnrollPass.cpp:814
    #5 0x7ffed73359bb in llvm::LPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\LoopPass.cpp:251
    #6 0x7ffed54f7f54 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #7 0x7ffed54f89ee in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #8 0x7ffed54f96a5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #9 0x7ffed55029cc in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #10 0x7ffed4f108c1 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #11 0x7ffed562e431 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #12 0x7ffed4f0b5b2 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #13 0x7ffed4f18d83 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #14 0x7ffed4df6b73 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #15 0x7ffedd531fb5 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #16 0x7ffedd59954e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #17 0x7ffedd6411b4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #18 0x7ffedd60467c in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:87
    #19 0x7ffedd44bec0 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #20 0x7ffedd398841 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1996
    #21 0x7ffedd398227 in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1299
    #22 0x7ffeff83bd5d in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #23 0x7ffeff240714 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477   
    #24 0x7ffeff2491ed in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1652
    #25 0x7ffefadfa692 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:992
    #26 0x7ffefadfaae5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1888
    #26 0x7ffefadfaae5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1888
    #27 0x7ffefadeee71 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1833
    #28 0x7ffeeead8863 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #29 0x7ffeeb68af1c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:506
    #30 0x7ffeeb6899c3 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:154
    #31 0x7ffeeeaf669a in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:936
    #32 0x7ffeeeb079ba in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #33 0x7ffeee15bf4d in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:743
    #34 0x7ffeee15a2a8 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:668
    #35 0x7ffeee15d5d8 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #36 0x7ffee959bf20 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #37 0x7ffeecf78d6e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #38 0x7ffeecf77c79 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #39 0x7ffeecfad27e in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #40 0x7ffeecf7a9bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:645
    #41 0x7ffee95e6430 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #42 0x7ffeec42e15d in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:438
    #43 0x7ffee7e88232 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:780
    #44 0x7ffee7e8a7b3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1156
    #45 0x7ffee7e861cd in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #46 0x7ffee7e86cbd in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #47 0x7ffedae616b1 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #48 0x7ff698ed43a5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #49 0x7ff698ed1db2 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #50 0x7ff6992b0143 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #51 0x7fff52017343 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017343)
    #52 0x7fff527426b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)

0x11f6a1ef6c08 is located 24 bytes before 96-byte region [0x11f6a1ef6c20,0x11f6a1ef6c80)
allocated by thread T0 here:
    #0 0x7ff698facb0d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffed7912f5e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffed639bc31 in llvm::User::operator new C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:96
    #3 0x7ffed71947f2 in llvm::SplitBlockPredecessors C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\BasicBlockUtils.cpp:496
    #4 0x7ffed731d6a6 in llvm::InsertPreheaderForLoop C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\LoopSimplify.cpp:145
    #5 0x7ffed731f0bd in llvm::simplifyLoop C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\LoopSimplify.cpp:740
    #6 0x7ffed7323e12 in LoopSimplify::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\LoopSimplify.cpp:790
    #7 0x7ffed54f7f54 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #8 0x7ffed54f89ee in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #9 0x7ffed54f96a5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #10 0x7ffed55029cc in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #11 0x7ffed4f108c1 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #12 0x7ffed562e431 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #13 0x7ffed4f0b5b2 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #14 0x7ffed4f18d83 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #15 0x7ffed4df6b73 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #16 0x7ffedd531fb5 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #17 0x7ffedd59954e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #18 0x7ffedd6411b4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #19 0x7ffedd60467c in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:87
    #20 0x7ffedd44bec0 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #21 0x7ffedd398841 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1996
    #22 0x7ffedd398227 in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1299
    #23 0x7ffeff83bd5d in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #24 0x7ffeff240714 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477
    #25 0x7ffeff2491ed in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1652
    #26 0x7ffefadfa692 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:992
    #27 0x7ffefadfaae5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1888

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\ScalarEvolution.cpp:4988 in llvm::ScalarEvolution::ComputeExitLimit
Shadow bytes around the buggy address:
  0x11f6a1ef6980: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x11f6a1ef6a00: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x11f6a1ef6a80: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x11f6a1ef6b00: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x11f6a1ef6b80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
=>0x11f6a1ef6c00: fa[fa]f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x11f6a1ef6c80: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x11f6a1ef6d00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x11f6a1ef6d80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11f6a1ef6e00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11f6a1ef6e80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
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


==5716==ADDITIONAL INFO

==5716==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffeee1534a5 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:483


==5716==END OF ADDITIONAL INFO
==5716==ABORTING
[6692:7064:0507/074158.199:ERROR:gpu_process_host.cc(1002)] GPU process exited unexpectedly: exit_code=1
[6692:7064:0507/074158.199:WARNING:gpu_process_host.cc(1436)] The GPU process has crashed 1 time(s)

```

## Attachments

- [asancomputeexit](attachments/asancomputeexit) (application/octet-stream, 18.4 KB)
- [indexComputeExitLimit.html](attachments/indexComputeExitLimit.html) (text/html, 3.1 KB)
- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 754 B)
- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 881 B)
- [rule-0-post.dot](attachments/rule-0-post.dot) (application/msword, 8.5 KB)
- [rule-0-post.png](attachments/rule-0-post.png) (image/png, 665.6 KB)
- [rule-0-pre.dot](attachments/rule-0-pre.dot) (application/msword, 7.6 KB)
- [rule-0-pre.png](attachments/rule-0-pre.png) (image/png, 547.3 KB)
- [DumpLoopCFG.cpp](attachments/DumpLoopCFG.cpp) (text/x-c++src, 3.6 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-05-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5999026018123776.

### ca...@chromium.org (2024-05-08)

amaiorano: Can you help further triage this? This didn't repro in CF, but seems like a legitimate crash. Thanks

### ca...@chromium.org (2024-05-08)

(same for crbug.com/339171223 and crbug.com/339332638)

### pe...@google.com (2024-05-09)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ad...@google.com (2024-05-10)

Reproduced on Linux with dxc on Dawn branch origin/chromium/6367 so I think this can safely be labeled FoundIn-124.

### pe...@google.com (2024-05-10)

Setting milestone because of s0/s1 severity.

### bc...@google.com (2024-05-16)

I've done some investigation, and I believe that the `RemoveUnstructuredLoopExitsIteration` transform is breaking flow control rules for loops.

Using the HLSL provided by the reporter of this bug and [some custom CFG annotations](https://gist.github.com/ben-clayton/77975d5bdcb88529ec0682d5c500de86), we can see the CFG pre and post `RemoveUnstructuredLoopExitsIteration()` on the first iteration of the loop in [`hlsl::RemoveUnstructuredLoopExits()`](https://github.com/microsoft/DirectXShaderCompiler/blob/fd7e54bcd527daeb0e400c200aab4f66730525e6/lib/Transforms/Scalar/DxilRemoveUnstructuredLoopExits.cpp#L609-L612).  

See the attached files for graphs pre / post call to `RemoveUnstructuredLoopExitsIteration()`.

The first call to `RemoveUnstructuredLoopExitsIteration()` is passed with the inner-most loop, and the local variables at the top of the function are:

- `latch` is `while.body.7.i.backedge` owned by the **inner loop**.
- `exit_block` is `while.body.2.i.loopexit` owned by the **middle loop**.
- `latch_exit` is `while.body.i.loopexit` owned by the **outer loop**.

[At the very end of `RemoveUnstructuredLoopExitsIteration()`](https://github.com/microsoft/DirectXShaderCompiler/blob/fd7e54bcd527daeb0e400c200aab4f66730525e6/lib/Transforms/Scalar/DxilRemoveUnstructuredLoopExits.cpp#L550-L554) a conditional branch is created from `latch_exit` to either `exit_block` or `post_exit_location`:

```
    // 5. Take the first half of latch_exit and branch it to the exit_block
    // based on the propagated exit condition.
    latch_exit->getTerminator()->eraseFromParent();
    BranchInst::Create(exit_block, post_exit_location, exit_cond_lcssa,
                       latch_exit);

```

`latch_exit` (`while.body.i.loopexit`) is in the outer loop, while `exit_block` (`while.body.2.i.loopexit`) is in the middle loop and **is not the loop header**.   

The middle loop now has two edges from outside the loop into two different blocks of the loop, which violates property 2 of LLVM's [Loop Definition](https://llvm.org/docs/LoopTerminology.html#loop-definition).   

Subsequent passes of `RemoveUnstructuredLoopExitsIteration()` further corrupts the loop and [the final call to `llvm::UnrollLoop()`](https://github.com/microsoft/DirectXShaderCompiler/blob/fd7e54bcd527daeb0e400c200aab4f66730525e6/lib/Transforms/Scalar/LoopUnrollPass.cpp#L957-L960) ends up asserting / crashing due to the invalid state.

We can confirm that `RemoveUnstructuredLoopExitsIteration()` is the cause of the corruption by adding the following to `hlsl::RemoveUnstructuredLoopExits()` immediately [after the call](https://github.com/microsoft/DirectXShaderCompiler/blob/fd7e54bcd527daeb0e400c200aab4f66730525e6/lib/Transforms/Scalar/DxilRemoveUnstructuredLoopExits.cpp#L611-L612):

```
      local_changed =
          RemoveUnstructuredLoopExitsIteration(exiting_block, L, LI, DT);

      // Ensure that this loop and all ancestor loops are still valid
      for (auto *loop = L; loop; loop = loop->getParentLoop()) {
        loop->verifyLoop(); // Fails validation on the second iteration (middle loop).
      }

```

Unfortunately due to the complexity here, I'm uncertain what the correct fix is for this transform. Until a fix can be provided by Microsoft, I would advise disabling this transform (`-opt-disable structurize-loop-exits-for-unroll`). With this flag, DXC does not assert or crash, but the shader is rejected with:

```
error: validation errors
test.hlsl:32: error: Loop must have break.
Validation failed.

```

This is because of the infinite loop in the shader's `main()`, and is expected.

Re-assigning back to amaiorano@ to lead discussions for a fix with the DXC team.

### dn...@google.com (2024-05-17)

Attaching Ben's cfg dumper code

### am...@google.com (2024-05-24)

Did some investigation as well, and have sent an email to Microsoft DXC folks with details about this.

### dn...@google.com (2024-05-28)

I've read the pass pretty closely now.
I think it assumes that any exit block is in the immediately surrounding loop, if it's in any loop at all.
The CFG dumps show that the initial conditions don't match that.

So the fix would be: if any exit block is in a loop that is not the immediately surrounding loop, then split it, and put the front half in the surrounding loop; and maintain the LCSSA property.

### dn...@google.com (2024-05-30)

I am working on the fix.
It gets interesting because I want to handle the case where the exit block may have other predecessors. In this case teh exit edge is "critical" in standard CFG terms.
Fortunately LLVM has a SplitEdge utility I can use.

Running all DXC's tests I have some failures.
One of them is tools/clang/test/DXC/loop\_structurize\_exit\_inner\_latch\_regression.ll
where the loop structure is:

```
Loop at depth 1 containing: %while.body.3.preheader.lr.ph<header>,%while.body.3.preheader,%while.body.3,%land.lhs.true<exiting>,%if.end,%for.inc,%while.body.3.preheader.lr.ph.loopexit<latch>
    Loop at depth 2 containing: %while.body.3.preheader<header>,%while.body.3,%land.lhs.true<exiting>,%if.end,%for.inc<latch><exiting>
        Loop at depth 3 containing: %while.body.3<header>,%land.lhs.true<exiting>,%if.end<latch><exiting>

```

The `%land.lhs.true` block is exiting because it branches to block `if.then` which does ret void.

So a return from inside a loop is an intersting case to watch for.

The failure occurs when running the pass on the inner loop at depth 2, `land.lhs.true` is also an exiting block for that middle loop, but the "getLoopFor" that block answers loop 3 rather than current loop 2. This trips an assertion I added.

I have to see if my modification natuarally generalizes.

### dn...@google.com (2024-05-31)

It got interesting. I had to learn about splitting critical edges.

I've posted a fix upstream, including regression cases, and two basic reduced test cases.
<https://github.com/microsoft/DirectXShaderCompiler/pull/6668>

### dn...@google.com (2024-06-03)

Some of the CI bots failed upstream.
<https://github.com/microsoft/DirectXShaderCompiler/pull/6668/checks?check_run_id=25674659921>

new test multi-level-exit-from-latch.ll

```
Script:
--
/home/vsts/work/1/s/build/./bin/opt /home/vsts/work/1/s/test/HLSL/passes/dxil_remove_unstructured_loop_exits/multi-level-exit-from-latch.ll -analyze -loops | /home/vsts/work/1/s/build/./bin/FileCheck -check-prefix=LOOPBEFORE /home/vsts/work/1/s/test/HLSL/passes/dxil_remove_unstructured_loop_exits/multi-level-exit-from-latch.ll
/home/vsts/work/1/s/build/./bin/opt /home/vsts/work/1/s/test/HLSL/passes/dxil_remove_unstructured_loop_exits/multi-level-exit-from-latch.ll -dxil-remove-unstructured-loop-exits -o /home/vsts/work/1/s/build/test/HLSL/passes/dxil_remove_unstructured_loop_exits/Output/multi-level-exit-from-latch.ll.tmp.bc
/home/vsts/work/1/s/build/./bin/opt /home/vsts/work/1/s/build/test/HLSL/passes/dxil_remove_unstructured_loop_exits/Output/multi-level-exit-from-latch.ll.tmp.bc -S | /home/vsts/work/1/s/build/./bin/FileCheck /home/vsts/work/1/s/test/HLSL/passes/dxil_remove_unstructured_loop_exits/multi-level-exit-from-latch.ll
/home/vsts/work/1/s/build/./bin/opt /home/vsts/work/1/s/build/test/HLSL/passes/dxil_remove_unstructured_loop_exits/Output/multi-level-exit-from-latch.ll.tmp.bc -analyze -loops | /home/vsts/work/1/s/build/./bin/FileCheck -check-prefix=LOOPAFTER /home/vsts/work/1/s/test/HLSL/passes/dxil_remove_unstructured_loop_exits/multi-level-exit-from-latch.ll
--
Exit Code: 1

Command Output (stderr):
--
=================================================================
==17631==ERROR: AddressSanitizer: heap-use-after-free on address 0x608000000740 at pc 0x5633603a179a bp 0x7ffe0ccb2ae0 sp 0x7ffe0ccb2ad8
READ of size 8 at 0x608000000740 thread T0
    #0 0x5633603a1799 in llvm::Value::getContext() const /home/vsts/work/1/s/lib/IR/Value.cpp:528:49
    #1 0x563360d6b6ac in EnsureSingleLevelExit(llvm::Loop*, llvm::LoopInfo*, llvm::DominatorTree*, llvm::BasicBlock*) /home/vsts/work/1/s/lib/Transforms/Scalar/DxilRemoveUnstructuredLoopExits.cpp:519:51
    #2 0x563360d65c74 in RemoveUnstructuredLoopExitsIteration(llvm::BasicBlock*, llvm::Loop*, llvm::LoopInfo*, llvm::DominatorTree*) /home/vsts/work/1/s/lib/Transforms/Scalar/DxilRemoveUnstructuredLoopExits.cpp:544:7
    #3 0x563360d655be in hlsl::RemoveUnstructuredLoopExits(llvm::Loop*, llvm::LoopInfo*, llvm::DominatorTree*, std::__1::unordered_set<llvm::BasicBlock*, std::__1::hash<llvm::BasicBlock*>, std::__1::equal_to<llvm::BasicBlock*>, std::__1::allocator<llvm::BasicBlock*> >*) /home/vsts/work/1/s/lib/Transforms/Scalar/DxilRemoveUnstructuredLoopExits.cpp:789:11
    #4 0x56335ffd2c96 in llvm::LPPassManager::runOnFunction(llvm::Function&) /home/vsts/work/1/s/lib/Analysis/LoopPass.cpp:251:23
    #5 0x563360338da8 in llvm::FPPassManager::runOnFunction(llvm::Function&) /home/vsts/work/1/s/lib/IR/LegacyPassManager.cpp:1587:27
    #6 0x563360339433 in llvm::FPPassManager::runOnModule(llvm::Module&) /home/vsts/work/1/s/lib/IR/LegacyPassManager.cpp:1609:16
    #7 0x563360339fd7 in runOnModule /home/vsts/work/1/s/lib/IR/LegacyPassManager.cpp:1669:27
    #8 0x563360339fd7 in llvm::legacy::PassManagerImpl::run(llvm::Module&) /home/vsts/work/1/s/lib/IR/LegacyPassManager.cpp:1771:44
    #9 0x56335fe072dd in main /home/vsts/work/1/s/tools/opt/opt.cpp:651:12
    #10 0x7efe68229d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f) (BuildId: 962015aa9d133c6cbcfb31ec300596d7f44d3348)
    #11 0x7efe68229e3f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x29e3f) (BuildId: 962015aa9d133c6cbcfb31ec300596d7f44d3348)
    #12 0x56335fd17d94 in _start (/home/vsts/work/1/s/build/bin/opt+0x974d94) (BuildId: 06dda16ea477b0b1)

0x608000000740 is located 32 bytes inside of 88-byte region [0x608000000720,0x608000000778)
freed by thread T0 here:
    #0 0x56335fdd628d in operator delete(void*) (/home/vsts/work/1/s/build/bin/opt+0xa3328d) (BuildId: 06dda16ea477b0b1)
    #1 0x5633602dc9ef in deleteNode /home/vsts/work/1/s/include/llvm/ADT/ilist.h:113:39
    #2 0x5633602dc9ef in erase /home/vsts/work/1/s/include/llvm/ADT/ilist.h:479:5
    #3 0x5633602dc9ef in llvm::Instruction::eraseFromParent() 

```

### dn...@google.com (2024-06-03)

I pushed a fix to my branch. The upstream CI bots are running again.

### dn...@google.com (2024-06-04)

The PR includes two reduced test cases:

- an exit edge escapes two levels of nesting, and leaves from a block that does not dominate its latch block. the exit block is in a loop.
- an exit edge escapes two levels of nesting, and leaves from the latch block. it lands in a loop. the exit block is in a loop.

It could also have

- the above two cases, where the exit block is not in a loop.
- the exit block is the header for an entirely unrelated loop

### dn...@google.com (2024-06-06)

The bugfix PR landed upstream <https://github.com/microsoft/DirectXShaderCompiler/pull/6668>

Reassigning to Antonio to shepherd the patch into Chromium

### ts...@google.com (2024-06-10)

Antonio, has the fix been pulled into Chromium yet? If so then this can be closed.  Thanks heaps!

### am...@google.com (2024-06-10)

Yes, I'll be testing this today.

### am...@google.com (2024-06-10)

- Tested by opening the attached `indexComputeExitLimit.html` in Chrome `Version 125.0.6422.114 (Official Build) (64-bit)`, and the GPU process crashes.
- Tested by opening the attached `indexComputeExitLimit.html` in Canary `Version 127.0.6531.0 (Official Build) canary (64-bit)`, and the GPU process no longer crashes. The console output correctly displays the following error:

```
DXC compile failed with: error: validation errors
hlsl.hlsl:38: error: Loop must have break.
Validation failed.

```

Links:

- Fix in DXC: <https://github.com/microsoft/DirectXShaderCompiler/pull/6668>
- Roll of DXC to Dawn with the fix: <https://dawn-review.googlesource.com/c/dawn/+/192165>
- Roll of Dawn into Chromium with fix: <https://chromium-review.googlesource.com/c/chromium/src/+/5606688>

### am...@google.com (2024-06-10)

As per chouinard@, the new bug [b/345988921](https://issues.chromium.org/issues/345988921) is caused by the [upstream fix](https://github.com/microsoft/DirectXShaderCompiler/pull/6668) that is now in Canary.

### am...@google.com (2024-06-10)

It also looks like [b/345822331](https://issues.chromium.org/issues/345822331) is caused by the same upstream fix. Note that the fix has not yet landed in any official Chrome release.

### da...@chromium.org (2024-06-11)

What are the next steps here then? Was the previous fix rolled back?

### am...@google.com (2024-06-11)

Yep, I just put up a revert PR: <https://github.com/microsoft/DirectXShaderCompiler/pull/6685>
And have reached out to DXC folks to ask for approvals ASAP.

### am...@google.com (2024-06-11)

Upstream revert has been approved, and should land in the next hour. It will make its way into Dawn, then into Chromium.

In the meantime, we are considering disabling the buggy pass altogether ([CL](https://dawn-review.googlesource.com/c/dawn/+/184422)).

### ap...@google.com (2024-06-12)

Project: dawn
Branch: main

commit cb79ddf448252ae8d25b8f0cb4e3dc4d7b8f54fe
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Wed Jun 12 00:37:29 2024

    dawn/dxc: disable DXC pass 'structurize-loop-exits-for-unroll'
    
    Multiple security bugs have been reported related to this optimization pass, and after careful consideration, we have decided to disable it.
    
    Bug: chromium:333508731
    Bug: chromium:339171223
    Bug: chromium:339169163
    Bug: chromium:346595893
    Change-Id: I5c9d7180ed09e7417c120595937bcb1013b6ce66
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/184422
    Commit-Queue: Antonio Maiorano <amaiorano@google.com>
    Reviewed-by: Natalie Chouinard <chouinard@google.com>
    Reviewed-by: Austin Eng <enga@chromium.org>

M       src/dawn/native/d3d/ShaderUtils.cpp

https://dawn-review.googlesource.com/184422


### ap...@google.com (2024-06-12)

Project: chromium/src
Branch: main

commit 7cb330156dcffbf97c3eda1aba1fb3606641e42b
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Wed Jun 12 10:08:47 2024

    Roll Dawn from 6f5358203435 to 236295367f2e (16 revisions)
    
    https://dawn.googlesource.com/dawn.git/+log/6f5358203435..236295367f2e
    
    2024-06-12 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll DirectX Shader Compiler from 0b9acdb75e17 to a44c88e2b803 (4 revisions)
    2024-06-12 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll Depot Tools from e30d8fac3437 to fd8560139886 (6 revisions)
    2024-06-12 dsinclair@chromium.org [hlsl] Start emitting types and constants.
    2024-06-12 jrprice@google.com [tint] Remove clamping for textureStore
    2024-06-12 jrprice@google.com [msl] Emit `abs()` builtin
    2024-06-12 jrprice@google.com [msl] Add polyfill for textureStore()
    2024-06-12 jrprice@google.com [msl] Add polyfill for textureLoad()
    2024-06-12 hao.x.li@intel.com Add Intel Arrowlake and Battlemage device IDs
    2024-06-12 jiawei.shao@intel.com Disallow using `@blend_src` on a non-struct fragment output
    2024-06-12 dneto@google.com .gitignore: Ignore local files written by pyenv
    2024-06-12 amaiorano@google.com dawn/dxc: disable DXC pass 'structurize-loop-exits-for-unroll'
    2024-06-12 enga@chromium.org Remove obsolete TODO about future tracking
    2024-06-11 senorblanco@chromium.org CTS: widen some expectations on Linux.
    2024-06-11 dsinclair@chromium.org Cleanup clang-tidy issues in src/tint/api
    2024-06-11 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from 81452425d73f to 544b108a1f77 (12 revisions)
    2024-06-11 dsinclair@chromium.org Update name of the disassembler
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/dawn-chromium-autoroll
    Please CC cwallez@google.com,senorblanco@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64
    Bug: chromium:333508731,chromium:339169163,chromium:339171223,chromium:341973423,chromium:345480299,chromium:346595893,chromium:42251016,chromium:42251305
    Tbr: senorblanco@google.com
    Test: Test: tint_unittests
    Include-Ci-Only-Tests: true
    Change-Id: I0c94717b662d22ad005beb9e3fb1d86f4425cbd4
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5625269
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1313905}

M       DEPS
M       third_party/dawn

https://chromium-review.googlesource.com/5625269


### am...@google.com (2024-06-12)

CL to disable the `structurize-loop-exits-for-unroll` pass has [landed in Dawn](https://dawn-review.googlesource.com/c/dawn/+/184422). Waiting for it to roll into Chromium to test in Canary.

Note that this should fix the following bugs: [b/339169163](https://issues.chromium.org/issues/339169163) (this one), and [b/345822331](https://issues.chromium.org/issues/345822331) (also [b/345988921](https://issues.chromium.org/issues/345988921), but this is a dupe of [b/345822331](https://issues.chromium.org/issues/345822331)).

### da...@chromium.org (2024-06-12)

Thanks amaiorano!

### am...@google.com (2024-06-12)

Tested in Canary, `Version 128.0.6535.0 (Official Build) canary (64-bit)`, by opening the attached `indexComputeExitLimit.html` and it no longer crashes the GPU process. The console output displays the expected compilation error:

```
DXC compile failed with: error: validation errors
hlsl.hlsl:38: error: Loop must have break.
Validation failed.

```

- Fix in Dawn: <https://dawn-review.googlesource.com/c/dawn/+/184422>
- Dawn roll into Chromium with fix: <https://chromium-review.googlesource.com/c/chromium/src/+/5625269>

### pe...@google.com (2024-06-13)

Requesting merge to stable (M126) because latest trunk commit (1313905) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1313905) appears to be after beta branch point (1313161).
Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### ch...@google.com (2024-06-13)

1. Which CLs should be backmerged? (Please include Gerrit links.)

- Fix into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/184422>
- Dawn rolled into Chromium: <https://chromium-review.googlesource.com/c/chromium/src/+/5625269>

The fix will be cherry-picked into a Dawn custom branch for Chrome release. Note that this is the same fix as <https://crbug.com/345822331> so they will be cherry-picked together.

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes

3. Does this fix pose any potential non-verifiable stability risks?

No

4. Does this fix pose any known compatibility risks?

No

5. Does it require manual verification by the test team? If so, please describe required testing.

Yes. Test by opening indexComputeExitLimit.html in Canary, and note that the GPU process does not crash. The console output does not show any errors, as expected, but simply outputs the GPUDevice and GPURenderPipeline state.

### am...@chromium.org (2024-06-14)

<https://dawn-review.googlesource.com/c/dawn/+/184422> approved for CP and merge to M127 Beta and M126 Stable
Please merge this fix to branch 6533 and 6478 respectively as soon as possible.

Please note that M126 Stable respin RC is scheduled to be cut tomorrow. If this fix can be CPed to be included in next week's Stable update, that would be ideal; otherwise this can be picked up for the following week's respin.

### am...@chromium.org (2024-06-14)

deleted

### pe...@google.com (2024-06-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sr...@google.com (2024-06-17)

Chatting with Amy and Antonio, we are good to proceed to merge to m126 today 

please complete your merge asap to m126

### am...@chromium.org (2024-06-17)

Apologies for any confusion from my c#34 (that comment was meant for another GPU bug [crbug.com/40942995](https://crbug.com/40942995) -- the fix for which was landed on 13 June)

Please go ahead and follow the the approval in c#33 and merge this fix at soonest, so this fix can be included in this week's update of Stable M126.
Thank you!

### am...@google.com (2024-06-17)

No problem. Will get this merged ASAP.

### ap...@google.com (2024-06-17)

Project: dawn
Branch: chromium/6533

commit 41d4bdf93cbc8783699cc6f9d6a1b04fa056b662
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Mon Jun 17 18:34:01 2024

    dawn/dxc: disable DXC pass 'structurize-loop-exits-for-unroll'
    
    Multiple security bugs have been reported related to this optimization pass, and after careful consideration, we have decided to disable it.
    
    Bug: chromium:333508731
    Bug: chromium:339171223
    Bug: chromium:339169163
    Bug: chromium:346595893
    Change-Id: I5c9d7180ed09e7417c120595937bcb1013b6ce66
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/184422
    Commit-Queue: Antonio Maiorano <amaiorano@google.com>
    Reviewed-by: Natalie Chouinard <chouinard@google.com>
    Reviewed-by: Austin Eng <enga@chromium.org>
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/193646
    Reviewed-by: dan sinclair <dsinclair@chromium.org>

M       src/dawn/native/d3d/ShaderUtils.cpp

https://dawn-review.googlesource.com/193646


### ap...@google.com (2024-06-17)

Project: dawn
Branch: chromium/6478

commit 9c6534f82db39148f29f0bb5e64fdcc7c2a4f372
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Mon Jun 17 18:33:47 2024

    dawn/dxc: disable DXC pass 'structurize-loop-exits-for-unroll'
    
    Multiple security bugs have been reported related to this optimization pass, and after careful consideration, we have decided to disable it.
    
    Bug: chromium:333508731
    Bug: chromium:339171223
    Bug: chromium:339169163
    Bug: chromium:346595893
    Change-Id: I5c9d7180ed09e7417c120595937bcb1013b6ce66
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/184422
    Commit-Queue: Antonio Maiorano <amaiorano@google.com>
    Reviewed-by: Natalie Chouinard <chouinard@google.com>
    Reviewed-by: Austin Eng <enga@chromium.org>
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/194160
    Reviewed-by: dan sinclair <dsinclair@chromium.org>

M       src/dawn/native/d3d/ShaderUtils.cpp

https://dawn-review.googlesource.com/194160


### am...@google.com (2024-06-17)

Fix has rolled into [6478](https://chromium.googlesource.com/chromium/src.git/+/089ca00b134be8edb76bc24ff76424b6b476b0ed) and [6533](https://chromium.googlesource.com/chromium/src.git/+/00cdbc010823bd134d4d20e46358757ff8a2f731).

### sp...@google.com (2024-06-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in the GPU process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-21)

Congratulations! Thank you for your ongoing fuzzing efforts and reporting this issue to us!

### pe...@google.com (2024-09-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in the GPU process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339169163)*
