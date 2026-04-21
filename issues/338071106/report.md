# GPU process crash via WebGPU shader - UAF in ProcessValue at DxilValueCache.cpp:555

| Field | Value |
|-------|-------|
| **Issue ID** | [338071106](https://issues.chromium.org/issues/338071106) |
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

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this might trigger a heap UAF insider the hlsl compiler.

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

Reproducing the issue stand-alone on Linux also possible.

1. Compile the standalone.wgsl with tint (commit 1488c9c94dea5d9bb158870717ebaf2f7d161f57) to hlsl via `./tint standalone.wgsl -o standalone.hlsl`. I also attached standalone.hlsl, but you should get the very same file when compiling standalone.wgsl yourself
2. Compile the hlsl with dxc (commit e7b78ff9c99c19a6a0c98256db9794e0af4eb59d): `./dxc-3.7 standalone.hlsl -T ps_6_6`. This should trigger an ASAN violation.

##### Attached:

- html that should trigger an ASAN violation in chromium (if the native back-end support shader-model 6.6)
- wgsl for producing the hlsl shader
- the hlsl shader
- asan log file

```
[12752:12836:0501/004239.044:WARNING:chrome_main_delegate.cc(742)] This is Chrome version 126.0.6451.0 (not a warning)
[12752:1904:0501/004239.185:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[12752:12836:0501/004239.216:INFO:chrome_browser_cloud_management_controller.cc(161)] Cloud management controller initialization aborted as CBCM is not enabled. Please use the `--enable-chrome-browser-cloud-management` command line flag to enable it if you are not using the official Google Chrome build.
[12752:4804:0501/004239.216:ERROR:sandbox_win.cc(911)] Sandbox cannot access executable. Check filesystem permissions are valid. See https://bit.ly/31yqMJR.: Access is denied. (0x5)
[12752:12836:0501/004239.342:WARNING:account_consistency_mode_manager.cc(77)] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
[12752:12836:0501/004239.514:WARNING:browser_management_service.cc(128)] EnterpriseLogoUrl fetch failed with error code -1 and MIME type 
[12752:12836:0501/004240.346:ERROR:network_service_instance_impl.cc(600)] Network service crashed, restarting service.
[12752:12836:0501/004240.393:WARNING:external_registry_loader_win.cc(232)] Error observing HKLM: 5
[13516:13424:0501/004240.455:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[12752:1904:0501/004244.189:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[13516:2924:0501/004245.468:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[12752:12836:0501/004247.307:INFO:CONSOLE(20)] "[object GPUDevice]", source: file:///E:/indexDIXLUaf.html (20)
[12752:12836:0501/004247.308:INFO:CONSOLE(100)] "[object GPURenderPipeline]", source: file:///E:/indexDIXLUaf.html (100)
=================================================================
==13136==ERROR: AddressSanitizer: heap-use-after-free on address 0x11b2604971e8 at pc 0x7ffe0390e43e bp 0x002f8d7fbdd0 sp 0x002f8d7fbe18
READ of size 8 at 0x11b2604971e8 thread T0
==13136==WARNING: Failed to use and restart external symbolizer!
==13136==*** WARNING: Failed to initialize DbgHelp!              ***
==13136==*** Most likely this means that the app is already      *** 
==13136==*** using DbgHelp, possibly with incompatible flags.    *** 
==13136==*** Due to technical reasons, symbolization might crash *** 
==13136==*** or produce wrong results.                           ***
    #0 0x7ffe0390e43d in llvm::BasicBlock::getTerminator C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:131
    #1 0x7ffe03c1c353 in llvm::DxilValueCache::ProcessValue C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\DxilValueCache.cpp:555
    #2 0x7ffe03c1d50e in llvm::DxilValueCache::GetConstValue C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\DxilValueCache.cpp:488
    #3 0x7ffe03c09c51 in `anonymous namespace'::DxilRemoveDeadBlocks::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilRemoveDeadBlocks.cpp:371
    #4 0x7ffe02a77cb4 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #5 0x7ffe02a7874e in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #6 0x7ffe02a79405 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #7 0x7ffe02a8272c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #8 0x7ffe02490811 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #9 0x7ffe02bae191 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #10 0x7ffe0248b502 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #11 0x7ffe02498cd3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #12 0x7ffe02376b05 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #13 0x7ffe096c9405 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #14 0x7ffe0972930e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #15 0x7ffe097d0b54 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #16 0x7ffe097ba563 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:385
    #17 0x7ffe095dfc30 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #18 0x7ffe095346b1 in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2125
    #19 0x7ffe09534097 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1456
    #20 0x7ffe2b8cd30d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #21 0x7ffe2b2d54c4 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606    
    #22 0x7ffe2b2da371 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #23 0x7ffe26f5f7b2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:982
    #24 0x7ffe26f5fc05 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1880
    #25 0x7ffe26f54021 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1825
    #26 0x7ffe1ac76013 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #27 0x7ffe177dcbcc in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:506
    #28 0x7ffe177db673 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:154
    #29 0x7ffe1ac93e4a in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:895
    #30 0x7ffe1aca414a in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #31 0x7ffe1a2965dd in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:743
    #32 0x7ffe1a294938 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:668
    #33 0x7ffe1a297c68 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #34 0x7ffe156cca20 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #35 0x7ffe190b6c66 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #36 0x7ffe190b5b89 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #37 0x7ffe190ea37e in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #38 0x7ffe190b88ac in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:645
    #39 0x7ffe15716f30 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #40 0x7ffe1857c71b in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:437
    #41 0x7ffe13fbf5d2 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:773
    #42 0x7ffe13fc1b53 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1155
    #43 0x7ffe13fbd56d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #44 0x7ffe13fbe05d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #45 0x7ffe070016b1 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #46 0x7ff6f58843a5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #47 0x7ff6f5881db2 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #48 0x7ff6f5c5d943 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #49 0x7ffe9237257c in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x18001257c)
    #50 0x7ffe92e0aa57 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005aa57)

0x11b2604971e8 is located 72 bytes inside of 88-byte region [0x11b2604971a0,0x11b2604971f8)
freed by thread T0 here:
    #0 0x7ff6f595ca0d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffe039114cb in llvm::BasicBlock::~BasicBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:70
    #2 0x7ffe0390dfb8 in llvm::BasicBlock::eraseFromParent C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:104
    #3 0x7ffe03c082fb in DeadBlockDeleter::Run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilRemoveDeadBlocks.cpp:188
    #4 0x7ffe03c096e8 in `anonymous namespace'::DxilRemoveDeadBlocks::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilRemoveDeadBlocks.cpp:370
    #5 0x7ffe02a77cb4 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #6 0x7ffe02a7874e in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #7 0x7ffe02a79405 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #8 0x7ffe02a8272c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #9 0x7ffe02490811 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #10 0x7ffe02bae191 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #11 0x7ffe0248b502 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #12 0x7ffe02498cd3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #13 0x7ffe02376b05 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #14 0x7ffe096c9405 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #15 0x7ffe0972930e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #16 0x7ffe097d0b54 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #17 0x7ffe097ba563 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:385
    #18 0x7ffe095dfc30 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #19 0x7ffe095346b1 in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2125
    #20 0x7ffe09534097 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1456
    #21 0x7ffe2b8cd30d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #22 0x7ffe2b2d54c4 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #23 0x7ffe2b2da371 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #24 0x7ffe26f5f7b2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:982
    #25 0x7ffe26f5fc05 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1880
    #26 0x7ffe26f54021 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1825
    #27 0x7ffe1ac76013 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232

previously allocated by thread T0 here:
    #0 0x7ff6f595cb0d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffe04e8396e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffe03b5ab71 in llvm::CloneBasicBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\CloneFunction.cpp:43
    #3 0x7ffe048956d9 in llvm::UnrollLoop C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\LoopUnroll.cpp:317
    #4 0x7ffe03d6c23a in `anonymous namespace'::LoopUnroll::runOnLoop C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\LoopUnrollPass.cpp:958
    #5 0x7ffe048a63cb in llvm::LPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\LoopPass.cpp:251
    #6 0x7ffe02a77cb4 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #7 0x7ffe02a7874e in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #8 0x7ffe02a79405 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #9 0x7ffe02a8272c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #10 0x7ffe02490811 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #11 0x7ffe02bae191 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #12 0x7ffe0248b502 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #13 0x7ffe02498cd3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #14 0x7ffe02376b05 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #15 0x7ffe096c9405 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #16 0x7ffe0972930e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #17 0x7ffe097d0b54 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #18 0x7ffe097ba563 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:385
    #19 0x7ffe095dfc30 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #20 0x7ffe095346b1 in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2125
    #21 0x7ffe09534097 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1456
    #22 0x7ffe2b8cd30d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #23 0x7ffe2b2d54c4 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #24 0x7ffe2b2da371 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #25 0x7ffe26f5f7b2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:982
    #26 0x7ffe26f5fc05 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1880
    #27 0x7ffe26f54021 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1825

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:131 in llvm::BasicBlock::getTerminator
Shadow bytes around the buggy address:
  0x11b260496f00: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x11b260496f80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11b260497000: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11b260497080: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11b260497100: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
=>0x11b260497180: fa fa f7 fa fd fd fd fd fd fd fd fd fd[fd]fd fa
  0x11b260497200: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11b260497280: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11b260497300: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x11b260497380: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x11b260497400: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
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

==13136==ADDITIONAL INFO

==13136==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffe1a294ade in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684
    #1 0x7ffe1a28db35 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:483


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==13136==END OF ADDITIONAL INFO
==13136==ABORTING
[12752:12836:0501/004248.874:ERROR:gpu_process_host.cc(1002)] GPU process exited unexpectedly: exit_code=1
[12752:12836:0501/004248.874:WARNING:gpu_process_host.cc(1436)] The GPU process has crashed 1 time(s)
[2244:14212:0501/004248.874:ERROR:command_buffer_proxy_impl.cc(131)] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.
[12752:12836:0501/004248.890:INFO:CONSOLE(0)] "A valid external Instance reference no longer exists.", source: file:///E:/indexDIXLUaf.html (0)
[12752:12836:0501/004249.204:WARNING:gpu_process_host.cc(1024)] Reinitialized the GPU process after a crash. The reported initialization time was 230 ms
[12752:12836:0501/004253.682:WARNING:pref_notifier_impl.cc(41)] Pref observer for media_router.cast_allow_all_ips found at shutdown.

```

## Attachments

- [indexDIXLUaf.html](attachments/indexDIXLUaf.html) (text/html, 3.8 KB)
- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 991 B)
- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 1.2 KB)
- [asan.log](attachments/asan.log) (text/plain, 23.0 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-05-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5475347811205120.

### th...@chromium.org (2024-05-01)

It doesn't look like ClusterFuzz is having luck with this. Triaging this speculatively, matching the high severity from <https://crbug.com/328958020>.

I'm also setting the FoundIn speculatively to extended stable (M124).

amaiorano@: This looks similar to some other issues you've looked into recently. Could you PTAL at this issue? Note I am tagging you on two other similar ones as well. Could you please update the FoundIn if you learn that this was introduced more recently than M124?

### 24...@project.gserviceaccount.com (2024-05-01)

Testcase 5475347811205120 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5475347811205120.

### pe...@google.com (2024-05-02)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-02)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### am...@google.com (2024-05-03)

- Cannot reproduce the crash when opening the attached `indexDIXLUaf.html` in Chrome; however, as the bug states, this is likely because my GPU does not support Shader Model 6.6 - mine supports SM 6.5.
- However, I am able to reproduce the crash using DXC from the commandline against the provided `standalone.hlsl` with `-T ps_6_6`. Note that running with `-T cs_6_5` does *not* reproduce the crash, and compiles successfully, so the crash is specific to the 6.6 codepath.
- When compiled with assertions enabled, DXC does not trip any assertions in the failure case (`-T cs_6_6`).
- Looking at the ASAN output, this looks like yet another errant `Instruction::eraseFromParent`. The instruction was allocated in the `UnrollLoop` pass, then later deleted in the `DxilRemoveDeadBlocks`, where the dangling pointer ends up getting accessed again in the `DxilValueCache`, triggering the ASAN `heap-use-after-free`.

This will require further investigation.

### am...@google.com (2024-05-03)

Potential workaround: as we don't currently use any shader model 6.6 features yet, Dawn could limit the shader model to 6.5.

### am...@google.com (2024-05-07)

More info after some investigation:

- Crash does NOT reproduce at optimization level `O2`, but does at `O3`. Comparing the passes between the two, the main difference are that the following passes are run at `O3`:

```
Canonicalize natural loops (loop-simplify)
Loop-Closed SSA Form Pass (lcssa)
Unroll loops (loop-unroll)

```

So it looks like another loop-related bug, like [this one](https://github.com/microsoft/DirectXShaderCompiler/commit/4242b576ed109e0bb6fd87f70823f8dd40f0fd2c) (though this recent patch doesn't address this specific bug).

### am...@google.com (2024-05-10)

I spent about 2 days on this. See my [investigation doc](https://docs.google.com/document/d/1zxF5WYHbU09Z1WCPqDbx4EF8A3_kXwHEvmAXXQ5QcSc/edit?usp=sharing).

Put up a fix PR: <https://github.com/microsoft/DirectXShaderCompiler/pull/6610>

### am...@google.com (2024-05-17)

[Upstream fix has landed](https://github.com/microsoft/DirectXShaderCompiler/pull/6610).
Waiting for DXC to roll into Dawn, and Dawn into Chromium so that I can test the fix on Canary.

### am...@google.com (2024-05-21)

Okay, I tested this. I had to use my personal PC since I needed a machine with a GPU that supports Shader Model 6.6.

- I tested using regular Chrome, Version 124.0.6367.208 (Official Build) (64-bit), and reproduced the GPU process crash when opening the attached `indexDIXLUaf.html`, as expected.
- I tested using latest Canary, Version 127.0.6492.0 (Official Build) canary (64-bit), and the crash no longer reproduces when opening the attached `indexDIXLUaf.html`.

This is the upstream fix in our DXC mirror: <https://chromium.googlesource.com/external/github.com/microsoft/DirectXShaderCompiler.git/+/cf566e1f3fec4fd1e3a7cd0ae6fad4c5864f9603>

This is the roll of DXC with that fix into Dawn: <https://dawn.googlesource.com/dawn/+/91c9b67a7dbd47e84aab9e63267d79fd594d73ce>

This is the roll of Dawn with that fix into Chrome: <https://chromium.googlesource.com/chromium/src/+/ac21ffb29c5eb7a18e3db2b8f8abe564e357bcef>

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

This is the DXC -> Dawn CL that rolls in the fix: <https://dawn-review.googlesource.com/c/dawn/+/188702>

This is the Dawn -> Chromium CL: <https://chromium-review.googlesource.com/c/chromium/src/+/5546473>

But we cannot cherry-pick these. I will need to manually cherry-pick the fix from the DXC mirror into Dawn's chromium release branches.

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes.

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

Can be tested on latest Canary on a Windows machine with a GPU that supports Shader Model 6.6 by opening the attached `indexDIXLUaf.html` and ensuring that the GPU process does not crash.

### sr...@google.com (2024-05-23)

[Bulk update] I will be reviewing all the merge requests today and expect to make a comment before EOD today, Please make sure you answer merge questions so i can review/approve later today

### am...@chromium.org (2024-05-24)

reviewed Canary data for Dawn -> Chromium roll with fix <https://chromium-review.googlesource.com/c/chromium/src/+/5546473>
approving merge to Dawn's Chromium release branches

please complete merges as soon as possible to ensure these fixes can be included in next week's updates (and a reminder that Monday is a US holiday :)

- M126 Beta / branch 6478
- M125 Stable / branch 6422
- M124 Extended Stable / branch 6367

### ap...@google.com (2024-05-24)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6367

commit 0b785e88fefa6d58508e937970fc288f223eda4e
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Fri May 24 15:51:26 2024

    Fix dxil-remove-dead-blocks removing switch with multiple same successor (#6610)
    
    Given a switch with a constant condition and all cases the same
    (branching to the same successor), dxil-remove-dead-blocks would
    incorrectly remove the switch when replacing it with a branch, by
    forgetting to remove the N-1 incoming values to the PHIs in the
    successor block.
    
    Bug: chromium:338071106
    Change-Id: Iaa2c42642f3e370afd19d88c96c81056c16349b6
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570270
    Reviewed-by: Ben Clayton <bclayton@chromium.org>
    Reviewed-by: James Price <jrprice@google.com>

M       lib/Transforms/Scalar/DxilRemoveDeadBlocks.cpp
A       tools/clang/test/DXC/Passes/DxilRemoveDeadBlocks/switch-with-multiple-same-successor.hlsl
A       tools/clang/test/DXC/Passes/DxilRemoveDeadBlocks/switch-with-multiple-same-successor.ll

https://chromium-review.googlesource.com/5570270


### ap...@google.com (2024-05-24)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6422

commit 97da97360f24cd7616636e79b17650eabfc4c68b
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Fri May 24 15:49:21 2024

    Fix dxil-remove-dead-blocks removing switch with multiple same successor (#6610)
    
    Given a switch with a constant condition and all cases the same
    (branching to the same successor), dxil-remove-dead-blocks would
    incorrectly remove the switch when replacing it with a branch, by
    forgetting to remove the N-1 incoming values to the PHIs in the
    successor block.
    
    Bug: chromium:338071106
    Change-Id: I8c1f1fb9da624a4793b96c0f167ea45e099cc8d0
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570864
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: Ben Clayton <bclayton@chromium.org>

M       lib/Transforms/Scalar/DxilRemoveDeadBlocks.cpp
A       tools/clang/test/DXC/Passes/DxilRemoveDeadBlocks/switch-with-multiple-same-successor.hlsl
A       tools/clang/test/DXC/Passes/DxilRemoveDeadBlocks/switch-with-multiple-same-successor.ll

https://chromium-review.googlesource.com/5570864


### ap...@google.com (2024-05-24)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6478

commit 3a3e07af1f03da19092a371eae8f44d1640c194b
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Fri May 24 15:44:52 2024

    Fix dxil-remove-dead-blocks removing switch with multiple same successor (#6610)
    
    Given a switch with a constant condition and all cases the same
    (branching to the same successor), dxil-remove-dead-blocks would
    incorrectly remove the switch when replacing it with a branch, by
    forgetting to remove the N-1 incoming values to the PHIs in the
    successor block.
    
    Bug: chromium:338071106
    Change-Id: Ibd4e372ec87d276e18569d458460da5cc1edbd6f
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570863
    Reviewed-by: Ben Clayton <bclayton@chromium.org>
    Reviewed-by: James Price <jrprice@google.com>

M       lib/Transforms/Scalar/DxilRemoveDeadBlocks.cpp
A       tools/clang/test/DXC/Passes/DxilRemoveDeadBlocks/switch-with-multiple-same-successor.hlsl
A       tools/clang/test/DXC/Passes/DxilRemoveDeadBlocks/switch-with-multiple-same-successor.ll

https://chromium-review.googlesource.com/5570863


### ap...@google.com (2024-05-25)

Project: dawn
Branch: chromium/6422

commit 6a1b17b8ce0fea77f08db558d5acff96a95f6111
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Sat May 25 01:28:40 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:338071106
    Change-Id: I1f0f2a247c3c6b4f7fef3bf1c09b4eb23803c537
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/189900
    Reviewed-by: James Price <jrprice@google.com>
    Commit-Queue: Antonio Maiorano <amaiorano@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/189900


### ap...@google.com (2024-05-27)

Project: dawn
Branch: chromium/6367

commit 7ecefb42aeabba4f18fa7e2a260b71a6dddec4c1
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Mon May 27 19:22:29 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:338071106
    Change-Id: I48f967da947d08c7a702630f5412e79ad46c3c55
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/189882
    Reviewed-by: James Price <jrprice@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/189882


### ap...@google.com (2024-05-27)

Project: dawn
Branch: chromium/6478

commit 73b2692dd71562b31168781be36732b2641cb8a5
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Mon May 27 19:22:38 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:338071106
    Change-Id: I47b54201cf74fa17b686ab0eda36d5f0864d18e0
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/189881
    Reviewed-by: James Price <jrprice@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/189881


### am...@google.com (2024-05-27)

The fix is now in M124, M125, and M126:

- Cherry-picked DXC fix: [M126/6478](https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570863), [M125/6422](https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570864), [M124/6367](https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5570270).
- Updated Dawn DEPS: [M126/6478](https://dawn-review.googlesource.com/c/dawn/+/189881), [M125/6422](https://dawn-review.googlesource.com/c/dawn/+/189900), [M124/6367](https://dawn-review.googlesource.com/c/dawn/+/189882).
- Dawn into Chrome: [M126/6478](https://chromium.googlesource.com/chromium/src.git/+/a28ba6a2f5cba315d9919ff42a17afe48a50681b), [M125/6422](https://chromium.googlesource.com/chromium/src.git/+/6f4a47bbc15b15519cf933f600a1e447c86b7fbe), [M124/6367](https://chromium.googlesource.com/chromium/src.git/+/239ca2c0428e2fcde1856d60b6245aaa6c10d6e2).

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

Congratulations on another one wgslfuzz -- great work and impressive fuzzing! Thanks for your effort in discovering and reporting this issue to us.

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
> * Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information w

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/338071106)*
