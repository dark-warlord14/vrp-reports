# GPU process crash via WebGPU shader - UAF in SimplifyTerminatorOnSelect at SimplifyCFG.cpp:2637

| Field | Value |
|-------|-------|
| **Issue ID** | [338103465](https://issues.chromium.org/issues/338103465) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU, Dawn>Tint, Internals>GPU>Dawn, Internals>GPU>Tint |
| **Platforms** | Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-05-01 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this triggers an UAF inside the hlsl compiler.

##### VERSION

Chrome Version: Pre-compiled ASAN Chromium 126.0.6451.0 (Developer Build) (64-bit)   

Operating System: Win11 Build 22631.2861

##### REPRODUCTION CASE

Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process. Note that the shader compiler only crashes if the DirectX back-end supports shader model 6.6. Inspecting the shader model is possible with a Microsoft tool called dxcapsviewer. The UI on my machine shows:

```
NVIDIA GeForce RTX 3090
    Direct3D 12
        Shader Model 6.6

```

Reproducing the issue stand-alone on Linux also possible:

1. Compile the standalone.wgsl with tint (commit 1488c9c94dea5d9bb158870717ebaf2f7d161f57) to hlsl via `./tint standalone.wgsl -o standalone.hlsl`. I also attached standalone.hlsl, but you should get the very same file when compiling standalone.wgsl yourself
2. Compile the hlsl with dxc (commit e7b78ff9c99c19a6a0c98256db9794e0af4eb59d): `./dxc-3.7 standalone.hlsl -T cs_6_6`. This should trigger an ASAN violation.

##### Attached:

- html that should trigger an ASAN violation in chromium (if the native back-end support shader-model 6.6)
- wgsl for producing the hlsl shader
- the hlsl shader
- asan log file

I have a bunch of more crashes but I don't want to spam the bug tracker. Do you prefer that I (1) report them all or (2) wait for the current dxcompiler issues to be fixed, check which crashes remain and report the ones still reproducing?

```
[8636:10396:0501/050229.559:WARNING:chrome_main_delegate.cc(742)] This is Chrome version 126.0.6451.0 (not a warning)
[8636:9132:0501/050229.700:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[8636:10396:0501/050229.731:INFO:chrome_browser_cloud_management_controller.cc(161)] Cloud management controller initialization aborted as CBCM is not enabled. Please use the `--enable-chrome-browser-cloud-management` command line flag to enable it if you are not using the official Google Chrome build.
[8636:1056:0501/050229.747:ERROR:sandbox_win.cc(911)] Sandbox cannot access executable. Check filesystem permissions are valid. See https://bit.ly/31yqMJR.: Access is denied. (0x5)
[8636:10396:0501/050229.857:WARNING:account_consistency_mode_manager.cc(77)] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
[8636:10396:0501/050230.029:WARNING:browser_management_service.cc(128)] EnterpriseLogoUrl fetch failed with error code -1 and MIME type 
[8636:10396:0501/050230.826:ERROR:network_service_instance_impl.cc(600)] Network service crashed, restarting service.
[8636:10396:0501/050230.872:WARNING:external_registry_loader_win.cc(232)] Error observing HKLM: 5
[9360:9024:0501/050230.935:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[8636:8980:0501/050234.707:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[9360:9372:0501/050235.942:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[8636:9992:0501/050244.712:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[9360:10548:0501/050245.944:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[8636:10396:0501/050248.482:INFO:CONSOLE(20)] "[object GPUDevice]", source: file:///E:/indexAddToListUAF.html (20)
=================================================================
==10192==ERROR: AddressSanitizer: heap-use-after-free on address 0x1215ce251138 at pc 0x7ffb6ee93c24 bp 0x007e09bfbfb0 sp 0x007e09bfbff8
READ of size 8 at 0x1215ce251138 thread T0
==10192==WARNING: Failed to use and restart external symbolizer!
==10192==*** WARNING: Failed to initialize DbgHelp!              ***
==10192==*** Most likely this means that the app is already      *** 
==10192==*** using DbgHelp, possibly with incompatible flags.    *** 
==10192==*** Due to technical reasons, symbolization might crash *** 
==10192==*** or produce wrong results.                           ***
    #0 0x7ffb6ee93c23 in llvm::BranchInst::BranchInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Instructions.cpp:723
    #1 0x7ffb6fd9a5d4 in SimplifyTerminatorOnSelect C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\SimplifyCFG.cpp:2637
    #2 0x7ffb6fd812dd in `anonymous namespace'::SimplifyCFGOpt::SimplifySwitch C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\SimplifyCFG.cpp:4320
    #3 0x7ffb6fd7389b in llvm::SimplifyCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\SimplifyCFG.cpp:4740
    #4 0x7ffb6f19637f in simplifyFunctionCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\SimplifyCFGPass.cpp:157
    #5 0x7ffb6e0d7cb4 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #6 0x7ffb6e0d874e in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #7 0x7ffb6e0d9405 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #8 0x7ffb6e0e272c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #9 0x7ffb6daf0811 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #10 0x7ffb6e20e191 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #11 0x7ffb6daeb502 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #12 0x7ffb6daf8cd3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #13 0x7ffb6d9d6b05 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #14 0x7ffb114d9405 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #15 0x7ffb1153930e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #16 0x7ffb115e0b54 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #17 0x7ffb115a431c in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:87
    #18 0x7ffb113efc30 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #19 0x7ffb1133ee71 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1996
    #20 0x7ffb1133e857 in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1299
    #21 0x7ffb336dcfad in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #22 0x7ffb330e2e04 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477   
    #23 0x7ffb330eb8dd in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1652
    #24 0x7ffb2ed6f7b2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:982
    #25 0x7ffb2ed6fc05 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1880
    #26 0x7ffb2ed64021 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1825
    #27 0x7ffb22a86013 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #28 0x7ffb1f5ecbcc in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:506
    #29 0x7ffb1f5eb673 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:154
    #30 0x7ffb22aa3e4a in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:895
    #31 0x7ffb22ab414a in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #32 0x7ffb220a65dd in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:743
    #33 0x7ffb220a4938 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:668
    #34 0x7ffb220a7c68 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #35 0x7ffb1d4dca20 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #36 0x7ffb20ec6c66 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #37 0x7ffb20ec5b89 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #38 0x7ffb20efa37e in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #39 0x7ffb20ec88ac in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:645
    #40 0x7ffb1d526f30 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #41 0x7ffb2038c71b in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:437
    #42 0x7ffb1bdcf5d2 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:773
    #43 0x7ffb1bdd1b53 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1155
    #44 0x7ffb1bdcd56d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #45 0x7ffb1bdce05d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #46 0x7ffb0ee116b1 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #47 0x7ff640f243a5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #48 0x7ff640f21db2 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #49 0x7ff6412fd943 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #50 0x7ffbc73c257c in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x18001257c)
    #51 0x7ffbc83eaa47 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005aa47)

0x1215ce251138 is located 24 bytes inside of 88-byte region [0x1215ce251120,0x1215ce251178)
freed by thread T0 here:
    #0 0x7ff640ffca0d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffb6dd18b1b in llvm::ICmpInst::~ICmpInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:1093
    #2 0x7ffb6ef6fed2 in llvm::BasicBlock::removePredecessor C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:329
    #3 0x7ffb6fd9a40f in SimplifyTerminatorOnSelect C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\SimplifyCFG.cpp:2622
    #4 0x7ffb6fd812dd in `anonymous namespace'::SimplifyCFGOpt::SimplifySwitch C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\SimplifyCFG.cpp:4320
    #5 0x7ffb6fd7389b in llvm::SimplifyCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\SimplifyCFG.cpp:4740
    #6 0x7ffb6f19637f in simplifyFunctionCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\SimplifyCFGPass.cpp:157
    #7 0x7ffb6e0d7cb4 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #8 0x7ffb6e0d874e in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #9 0x7ffb6e0d9405 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #10 0x7ffb6e0e272c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #11 0x7ffb6daf0811 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #12 0x7ffb6e20e191 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #13 0x7ffb6daeb502 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #14 0x7ffb6daf8cd3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #15 0x7ffb6d9d6b05 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #16 0x7ffb114d9405 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #17 0x7ffb1153930e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #18 0x7ffb115e0b54 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #19 0x7ffb115a431c in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:87
    #20 0x7ffb113efc30 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #21 0x7ffb1133ee71 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1996
    #22 0x7ffb1133e857 in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1299
    #23 0x7ffb336dcfad in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #24 0x7ffb330e2e04 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477
    #25 0x7ffb330eb8dd in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1652
    #26 0x7ffb2ed6f7b2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:982
    #27 0x7ffb2ed6fc05 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1880

previously allocated by thread T0 here:
    #0 0x7ff640ffcb0d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffb704e396e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffb6ef6c784 in llvm::User::operator new C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:108
    #3 0x7ffb6e0bd516 in llvm::PHINode::Create C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:2340
    #4 0x7ffb6fd79763 in llvm::SimplifyCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\SimplifyCFG.cpp:4740
    #5 0x7ffb6f19637f in simplifyFunctionCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\SimplifyCFGPass.cpp:157
    #6 0x7ffb6e0d7cb4 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #7 0x7ffb6e0d874e in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #8 0x7ffb6e0d9405 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #9 0x7ffb6e0e272c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #10 0x7ffb6daf0811 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #11 0x7ffb6e20e191 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #12 0x7ffb6daeb502 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #13 0x7ffb6daf8cd3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #14 0x7ffb6d9d6b05 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #15 0x7ffb114d9405 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #16 0x7ffb1153930e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #17 0x7ffb115e0b54 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #18 0x7ffb115a431c in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:87
    #19 0x7ffb113efc30 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #20 0x7ffb1133ee71 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1996
    #21 0x7ffb1133e857 in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1299
    #22 0x7ffb336dcfad in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #23 0x7ffb330e2e04 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477
    #24 0x7ffb330eb8dd in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1652
    #25 0x7ffb2ed6f7b2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:982
    #26 0x7ffb2ed6fc05 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1880
    #27 0x7ffb2ed64021 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1825
SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Instructions.cpp:723 in llvm::BranchInst::BranchInst

Shadow bytes around the buggy address:
  0x1215ce250e80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1215ce250f00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1215ce250f80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1215ce251000: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1215ce251080: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
=>0x1215ce251100: fa fa f7 fa fd fd fd[fd]fd fd fd fd fd fd fd fa
  0x1215ce251180: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x1215ce251200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1215ce251280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1215ce251300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1215ce251380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==10192==ADDITIONAL INFO

==10192==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffb220a4ade in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684
    #1 0x7ffb220a4ade in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684
    #2 0x7ffb220a4ade in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684
    #3 0x7ffb220a4ade in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==10192==END OF ADDITIONAL INFO
==10192==ABORTING
[8636:10396:0501/050250.174:ERROR:gpu_process_host.cc(1002)] GPU process exited unexpectedly: exit_code=1
[8636:10396:0501/050250.174:WARNING:gpu_process_host.cc(1436)] The GPU process has crashed 1 time(s)

```

## Attachments

- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 1.3 KB)
- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 1.9 KB)
- [indexAddToListUAF.html](attachments/indexAddToListUAF.html) (text/html, 4.3 KB)
- [asanuselistUaf](attachments/asanuselistUaf) (application/octet-stream, 23.6 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-05-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5095831112712192.

### th...@chromium.org (2024-05-01)

It doesn't look like ClusterFuzz is having luck with this. Triaging this speculatively, matching the high severity from <https://crbug.com/328958020>.

I'm also setting the FoundIn speculatively to extended stable (M124).

amaiorano@: This looks similar to some other issues you've looked into recently. Could you PTAL at this issue? Note I am tagging you on two other similar ones as well. Could you please update the FoundIn if you learn that this was introduced more recently than M124?

### 24...@project.gserviceaccount.com (2024-05-01)

Testcase 5095831112712192 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5095831112712192.

### pe...@google.com (2024-05-02)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-02)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### am...@google.com (2024-05-03)

- Cannot reproduce the crash when opening the attached `indexAddToListUAF.html` in Chrome; however, as the bug states, this is likely because my GPU does not support Shader Model 6.6 - mine supports SM 6.5.
- I am able to reproduce the ASAN failure when running an asan build of dxc against the attached `standalone.hlsl` and get a similar ASAN output with `-T cs_6_6`, but dxc succeeds when compiling with `-T cs_6_5` (or less), so this is specific to the SM 6.6 path in DXC.
- From my ASAN output, we're hitting a heap-use-after-free on an allocation of a `PHINode` that was created in `SimplifyCFG` in `SimplifyCondBranchToCondBranch`, then later deleted in `SimplifyCFG` in `SimplifyTerminatorOnSelect`, and then accessed in the same function. So this all happens in `SimplifyCFG`, with the delete and use-after-free happening in `SimplifyTerminatorOnSelect`.

Needs more investigation.

### am...@google.com (2024-05-03)

Potential workaround: as we don't currently use any shader model 6.6 features yet, Dawn could limit the shader model to 6.5.

### am...@google.com (2024-05-13)

In attempting to simplify the `standalone.hlsl` file, very few changes are required to make the ASAN error disappear, but instead emit an assertion. Assuming the assert is related, I've reduced the code to a bare minimum that still reproduces the assertion:

```
[numthreads(1, 1, 1)]
void main() {
  int i = 0;
  while (true) {
    for (i = 0; i < 2; i++) {
      while (true) {
        int unused = 0;
        while (true) {
          if (i < 2) {
            return;
          } else {
            break;
          }
        }
        if (i < 2) { break; }
      }
    }
  }
}

```

And the error:

```
$ ./bin/dxc -T cs_6_6 standalone_reduced.hlsl 
dxc: /home/amaiorano/src/external/DirectXShaderCompiler/include/llvm/IR/CFG.h:216: Self &llvm::SuccIterator<llvm::TerminatorInst *, llvm::BasicBlock>::operator+=(int) [Term_ = llvm::TerminatorInst *, BB_ = llvm::BasicBlock]: Assertion `index_is_valid(new_idx) && "Iterator index out of bound"' failed.
Aborted

```

### am...@google.com (2024-05-14)

It looks like the assertion I mention in [#comment9](https://issues.chromium.org/issues/338103465#comment9) is a false positive. I'm putting together a patch to fix this false positive. This means that my code reduction does not reproduce the ASAN failure, and I'll have to try again.

### am...@google.com (2024-05-15)

Fix for false-positive assert (which does NOT address this ASAN failure): [Fix false positive assert in SuccIterator::operator+= by amaiorano · Pull Request #6623 · microsoft/DirectXShaderCompiler](https://github.com/microsoft/DirectXShaderCompiler/pull/6623)

### am...@google.com (2024-05-15)

Okay, figured out the bug, and put up a fix upstream: <https://github.com/microsoft/DirectXShaderCompiler/pull/6628>

### am...@google.com (2024-05-17)

Upstream fix was [approved and should land shortly](https://github.com/microsoft/DirectXShaderCompiler/pull/6628). Once it lands, will wait for DXC to roll into Dawn, and Dawn into Chromium so that I can test the fix on Canary.

### am...@google.com (2024-05-21)

I tested this on my personal PC since I needed a machine with a GPU that supports Shader Model 6.6.

- I tested using regular Chrome, Version 124.0.6367.208 (Official Build) (64-bit), and reproduced the GPU process crash when opening the attached `indexAddToListUAF.html`, as expected.
- I tested using latest Canary, Version 127.0.6492.0 (Official Build) canary (64-bit), and the crash no longer reproduces when opening the attached `indexAddToListUAF.html`.

This is the upstream fix in our DXC mirror: <https://chromium.googlesource.com/external/github.com/microsoft/DirectXShaderCompiler.git/+/348040254ed77c00dc4bae16678a38d77187abbb>

This is the roll of DXC with that fix into Dawn: <https://dawn.googlesource.com/dawn/+/f22e61ff624c0c4b9b8961a49680ff0073960cfe>

This is the roll of Dawn with that fix into Chrome: <https://chromium.googlesource.com/chromium/src/+/7b04aa204072b5be4904a48f13bfb34056d26023>

### pe...@google.com (2024-05-22)

This is sufficiently serious that it should be merged to extended stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M124. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125, 126].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@google.com (2024-05-22)

1. Which CLs should be backmerged? (Please include Gerrit links.)

This is the DXC -> Dawn CL that rolls in the fix: <https://dawn-review.googlesource.com/c/dawn/+/188646>

This is the Dawn -> Chromium CL: <https://chromium-review.googlesource.com/c/chromium/src/+/5545744>

But we cannot cherry-pick these. I will need to manually cherry-pick the fix from the DXC mirror into Dawn's chromium release branches.

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes.

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

Can be tested on latest Canary on a Windows machine with a GPU that supports Shader Model 6.6 by opening the attached `indexAddToListUAF.html` and ensuring that the GPU process does not crash.

### sr...@google.com (2024-05-23)

[Bulk update] I will be reviewing all the merge requests today and expect to make a comment before EOD today, Please make sure you answer merge questions so i can review/approve later today

### am...@chromium.org (2024-05-23)

I've review data on Canary on which this roll was landed: <https://chromium-review.googlesource.com/c/chromium/src/+/5545744>
Fixes approved for merge into Dawn's Chromium release branches, please merge this fix to:

- M126 Beta / branch 6478
- M125 Stable / branch 6422
- M124 Extended Stable / branch 6367

as soon as possible, before 10am Pacific Time on Tuesday, 28 May (reminder that Monday is a US holiday, so merge by EOD tomorrow / Friday is preferred)

### ap...@google.com (2024-05-27)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6478

commit 6a6ff9dafe27caebfc47bace6c3a029bb42007f3
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Mon May 27 15:43:52 2024

    Fix use-after-free in SimplifyCFG (#6628)
    
    When SimplifySwitchOnSelect calls SimplifyTerminatorOnSelect, it holds
    onto the select's condition value to use for the conditional branch it
    replaces the switch with. When removing the switch's unused
    predecessors, it must make sure not to delete PHIs in case one of them
    is used by the condition value, otherwise the condition value itself may
    get deleted, resulting in an use-after-free.
    
    Note that this was fixed in LLVM as well:
    
    https://github.com/llvm/llvm-project/commit/dc3b67b4cad5c18a687edfabd50779c3c656c620
    
    Bug: chromium:338103465
    Change-Id: I0f1870f1f84b2ce14a1bc883e3d2f6086ee14013
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570019
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: Natalie Chouinard <chouinard@chromium.org>

M       lib/Transforms/Utils/SimplifyCFG.cpp
A       tools/clang/test/DXC/Passes/SimplifyCFG/simplifycfg-uaf-select-condition.ll

https://chromium-review.googlesource.com/5570019


### ap...@google.com (2024-05-27)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6422

commit e3dec39021a438ef070a1f7dbbef8760f358cb33
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Mon May 27 15:43:03 2024

    Fix use-after-free in SimplifyCFG (#6628)
    
    When SimplifySwitchOnSelect calls SimplifyTerminatorOnSelect, it holds
    onto the select's condition value to use for the conditional branch it
    replaces the switch with. When removing the switch's unused
    predecessors, it must make sure not to delete PHIs in case one of them
    is used by the condition value, otherwise the condition value itself may
    get deleted, resulting in an use-after-free.
    
    Note that this was fixed in LLVM as well:
    
    https://github.com/llvm/llvm-project/commit/dc3b67b4cad5c18a687edfabd50779c3c656c620
    
    Bug: chromium:338103465
    Change-Id: I06521a6ef02774c81cfebcc9d5a0610c0c95e7b5
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570610
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: Natalie Chouinard <chouinard@chromium.org>

M       lib/Transforms/Utils/SimplifyCFG.cpp
A       tools/clang/test/DXC/Passes/SimplifyCFG/simplifycfg-uaf-select-condition.ll

https://chromium-review.googlesource.com/5570610


### ap...@google.com (2024-05-27)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6367

commit 511cfef8e0509d172fbfa156be8a97ed2b42590b
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Mon May 27 15:41:40 2024

    Fix use-after-free in SimplifyCFG (#6628)
    
    When SimplifySwitchOnSelect calls SimplifyTerminatorOnSelect, it holds
    onto the select's condition value to use for the conditional branch it
    replaces the switch with. When removing the switch's unused
    predecessors, it must make sure not to delete PHIs in case one of them
    is used by the condition value, otherwise the condition value itself may
    get deleted, resulting in an use-after-free.
    
    Note that this was fixed in LLVM as well:
    
    https://github.com/llvm/llvm-project/commit/dc3b67b4cad5c18a687edfabd50779c3c656c620
    
    Bug: chromium:338103465
    Change-Id: Iff5d5f2e3ecf38a3fb22bbc65e7c33ad0de659fb
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570018
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: Natalie Chouinard <chouinard@chromium.org>

M       lib/Transforms/Utils/SimplifyCFG.cpp
A       tools/clang/test/DXC/Passes/SimplifyCFG/simplifycfg-uaf-select-condition.ll

https://chromium-review.googlesource.com/5570018


### ap...@google.com (2024-05-27)

Project: dawn
Branch: chromium/6478

commit 4c6214625c4fd6d38b1604af39ce64395358ca55
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Mon May 27 20:28:52 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:338103465
    Change-Id: I1372195c5f52e5e632dc7a34ec1c9f14e3fa1078
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/190162
    Reviewed-by: Natalie Chouinard <chouinard@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/190162


### ap...@google.com (2024-05-27)

Project: dawn
Branch: chromium/6422

commit fe3821ae5458d9a1a67c2e6a0f19aee8d6f90322
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Mon May 27 20:28:46 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:338103465
    Change-Id: Ie421f0cbfaf07fb87869c7965aed9579175f12db
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/190161
    Reviewed-by: Natalie Chouinard <chouinard@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/190161


### ap...@google.com (2024-05-27)

Project: dawn
Branch: chromium/6367

commit e04b03f714994b7a747b5472da4ffae9e6e38938
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Mon May 27 20:28:40 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:338103465
    Change-Id: Ibc3677e42a81892c6f2f58bac7ee12409a7c6ae9
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/190222
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: Natalie Chouinard <chouinard@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/190222


### am...@google.com (2024-05-27)

Fix has been merged to M124, M125, and M126:

- Cherry-picked DXC fix: [M126/6478](https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570019), [M125/6422](https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570610), [M124/6367](https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570018).
- Updated Dawn DEPS: [M126/6478](https://dawn-review.googlesource.com/c/dawn/+/190222), [M125/6422](https://dawn-review.googlesource.com/c/dawn/+/190161), [M124/6367](https://dawn-review.googlesource.com/c/dawn/+/190162).
- Dawn into Chrome: [M126/6478](https://chromium.googlesource.com/chromium/src.git/+/b1c14f3cb44a8738e11960deadd87a2aaf57db19), [M125/6422](https://chromium.googlesource.com/chromium/src.git/+/11ddce057b8221f772a85ca2dd3bf9c64fedc14d), [M124/6367](https://chromium.googlesource.com/chromium/src.git/+/1c5bd031dde27caae5fbdd35961c726651f8c516).

### sp...@google.com (2024-05-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
memory corruption in the GPU process 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are not already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-30)

Congratulations on yet another one, wgslfuzz! Thanks your for your efforts in GPU fuzzing and reporting these issues to us -- great work!

### pe...@google.com (2024-08-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> memory corruption in the GPU process 
> 
> Thank you for your efforts and helping us make Chrome more secure for all users!
> 
> Cheers,
> Chrome VRP Panel Bot
> 
> 
> P.S. Two other things we'd like to mention:
> 
> * Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information 

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/338103465)*
