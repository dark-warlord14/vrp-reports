# GPU process crash via WebGPU shader - UAF in GetIfCondition at BasicBlockUtils.cpp:810

| Field | Value |
|-------|-------|
| **Issue ID** | [340196361](https://issues.chromium.org/issues/340196361) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-05-13 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this triggers an UAF inside the hlsl compiler.

##### VERSION

Chrome Version: Pre-compiled ASAN Chromium 126.0.6478.0 (Developer Build) (64-bit)   

Operating System: Win10 Build 19045.4291

##### REPRODUCTION CASE

Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process.

Reproducing the issue stand-alone on Linux also possible:

1. Compile the standalone.wgsl with tint (commit cabf62259d57b046b38d305cceac1d84893d3329) to hlsl via `./tint standalone.wgsl -o standalone.hlsl`. I also attached standalone.hlsl, but you should get the very same file when compiling standalone.wgsl yourself
2. Compile the hlsl with dxc (commit 01007bcd7f95fc32cbdf33ec8bcd9de4906926a5): `./dxc-3.7 -T ps_6_2 -HV 2018 standalone.hlsl`. This should trigger an ASAN violation. The command line arguments `-HV 2018` is necessary to trigger the bug; dawn is adding it under Windows.

##### Attached:

Nothing yet, I'm getting upload errors but will reply in a comment.

```
[5188:8084:0513/113003.906:WARNING:chrome_main_delegate.cc(742)] This is Chrome version 126.0.6478.0 (not a warning)
[5188:7744:0513/113004.266:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[5188:5536:0513/113004.328:ERROR:sandbox_win.cc(913)] Sandbox cannot access executable. Check filesystem permissions are valid. See https://bit.ly/31yqMJR.: Access is denied. (0x5)
[5188:8084:0513/113004.500:WARNING:account_consistency_mode_manager.cc(77)] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
[5188:8084:0513/113004.750:WARNING:browser_management_service.cc(128)] EnterpriseLogoUrl fetch failed with error code -1 and MIME type 
[5188:8084:0513/113006.515:ERROR:network_service_instance_impl.cc(600)] Network service crashed, restarting service.
[5188:8084:0513/113006.593:WARNING:external_registry_loader_win.cc(232)] Error observing HKLM: 5
[5188:5468:0513/113009.307:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[2140:3808:0513/113009.902:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[2140:7596:0513/113018.845:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[5188:5700:0513/113020.212:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[2140:3808:0513/113028.863:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[5188:5700:0513/113040.220:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[5188:8084:0513/113048.339:INFO:CONSOLE(20)] "[object GPUDevice]", source: file://vboxsvr/shared/index_FoldTwoEntryPHINode.html (20)
[5188:8084:0513/113048.434:INFO:CONSOLE(109)] "[object GPURenderPipeline]", source: file://vboxsvr/shared/index_FoldTwoEntryPHINode.html (109)
[2140:7596:0513/113048.885:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
=================================================================
==4316==ERROR: AddressSanitizer: heap-use-after-free on address 0x12be01fb4668 at pc 0x7ffe2e3adb9e bp 0x00c4f91fbdb0 sp 0x00c4f91fbdf8
READ of size 8 at 0x12be01fb4668 thread T0
==4316==WARNING: Failed to use and restart external symbolizer!
==4316==*** WARNING: Failed to initialize DbgHelp!              ***
==4316==*** Most likely this means that the app is already      *** 
==4316==*** using DbgHelp, possibly with incompatible flags.    *** 
==4316==*** Due to technical reasons, symbolization might crash *** 
==4316==*** or produce wrong results.                           ***
    #0 0x7ffe2e3adb9d in llvm::BasicBlock::getTerminator C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:131
    #1 0x7ffe2f1a96da in llvm::GetIfCondition C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\BasicBlockUtils.cpp:810
    #2 0x7ffe2f1b1942 in llvm::SimplifyCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\SimplifyCFG.cpp:4740
    #3 0x7ffe2e5d5d4f in simplifyFunctionCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\SimplifyCFGPass.cpp:157
    #4 0x7ffe2d507f54 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #5 0x7ffe2d5070e5 in llvm::legacy::FunctionPassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1528
    #6 0x7ffe2d506d6a in llvm::legacy::FunctionPassManager::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1452
    #7 0x7ffe2e687217 in `anonymous namespace'::DxilLoopDeletion::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\DxilLoopDeletion.cpp:70
    #8 0x7ffe2d507f54 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #9 0x7ffe2d5089ee in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #10 0x7ffe2d5096a5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #11 0x7ffe2d5129cc in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #12 0x7ffe2cf208c1 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #13 0x7ffe2d63e431 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #14 0x7ffe2cf1b5b2 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #15 0x7ffe2cf28d83 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #16 0x7ffe2ce06b73 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #17 0x7ffe35b65b79 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #18 0x7ffe35bccc9e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #19 0x7ffe35c72dc4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #20 0x7ffe35c5c543 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:385
    #21 0x7ffe35a80330 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #22 0x7ffe359d02e1 in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2126
    #23 0x7ffe359cfcc7 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1456
    #24 0x7ffe57f9774d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #25 0x7ffe5799e3c4 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #26 0x7ffe579a32a1 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #27 0x7ffe534f5f72 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:992
    #28 0x7ffe534f63c5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1887
    #29 0x7ffe534ea761 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1832
    #30 0x7ffe471957f3 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #31 0x7ffe43d2058c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:506
    #32 0x7ffe43d1f033 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:154
    #33 0x7ffe471b369a in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:930
    #34 0x7ffe471c477a in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&,unsigned long long &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams>,unsigned long long>,void ()>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams>,unsigned long long>,0,1,2> C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1067
    #35 0x7ffe4680e16d in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:743
    #36 0x7ffe4680c4c8 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:668
    #37 0x7ffe4680f7f8 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #38 0x7ffe41c317a0 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #39 0x7ffe456323fe in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #40 0x7ffe45631309 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #41 0x7ffe4566760e in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #42 0x7ffe4563404c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:645
    #43 0x7ffe41c7bc50 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #44 0x7ffe44ae02cd in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:438
    #45 0x7ffe4051af62 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:780
    #46 0x7ffe4051d4e3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1156
    #47 0x7ffe40518efd in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #48 0x7ffe405199ed in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #49 0x7ffe33491601 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #50 0x7ff6856f43a5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #51 0x7ff6856f1db2 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #52 0x7ff685ad0583 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #53 0x7ffea8a27343 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017343)
    #54 0x7ffea9a626b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)

0x12be01fb4668 is located 72 bytes inside of 88-byte region [0x12be01fb4620,0x12be01fb4678)
freed by thread T0 here:
    #0 0x7ff6857cca0d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffe2e3b0c2b in llvm::BasicBlock::~BasicBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:70
    #2 0x7ffe2e3ad718 in llvm::BasicBlock::eraseFromParent C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:104
    #3 0x7ffe2e7cd945 in `anonymous namespace'::LoopDeletion::runOnLoop C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\LoopDeletion.cpp:237
    #4 0x7ffe2f345efb in llvm::LPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\LoopPass.cpp:251
    #5 0x7ffe2d507f54 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #6 0x7ffe2d5070e5 in llvm::legacy::FunctionPassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1528
    #7 0x7ffe2d506d6a in llvm::legacy::FunctionPassManager::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1452
    #8 0x7ffe2e6871ff in `anonymous namespace'::DxilLoopDeletion::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\DxilLoopDeletion.cpp:67
    #9 0x7ffe2d507f54 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #10 0x7ffe2d5089ee in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #11 0x7ffe2d5096a5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #12 0x7ffe2d5129cc in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #13 0x7ffe2cf208c1 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #14 0x7ffe2d63e431 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #15 0x7ffe2cf1b5b2 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #16 0x7ffe2cf28d83 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #17 0x7ffe2ce06b73 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #18 0x7ffe35b65b79 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #19 0x7ffe35bccc9e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #20 0x7ffe35c72dc4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #21 0x7ffe35c5c543 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:385
    #22 0x7ffe35a80330 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #23 0x7ffe359d02e1 in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2126
    #24 0x7ffe359cfcc7 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1456
    #25 0x7ffe57f9774d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #26 0x7ffe5799e3c4 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #27 0x7ffe579a32a1 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682

previously allocated by thread T0 here:
    #0 0x7ff6857ccb0d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffe2f92371e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffe2e60107c in `anonymous namespace'::PruningFunctionCloner::CloneBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\CloneFunction.cpp:307
    #3 0x7ffe2e5fdd76 in llvm::CloneAndPruneIntoFromInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\CloneFunction.cpp:511
    #4 0x7ffe2e603635 in llvm::CloneAndPruneFunctionInto C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\CloneFunction.cpp:720
    #5 0x7ffe2f86cd24 in llvm::InlineFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\InlineFunction.cpp:1046
    #6 0x7ffe2f16746b in llvm::Inliner::runOnSCC C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\IPO\Inliner.cpp:574
    #7 0x7ffe2f16d9ef in `anonymous namespace'::CGPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\IPA\CallGraphSCCPass.cpp:491
    #8 0x7ffe2d5096a5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #9 0x7ffe2d5129cc in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #10 0x7ffe2cf208c1 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #11 0x7ffe2d63e431 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #12 0x7ffe2cf1b5b2 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #13 0x7ffe2cf28d83 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #14 0x7ffe2ce06b73 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #15 0x7ffe35b65b79 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #16 0x7ffe35bccc9e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #17 0x7ffe35c72dc4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #18 0x7ffe35c5c543 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:385
    #19 0x7ffe35a80330 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #20 0x7ffe359d02e1 in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2126
    #21 0x7ffe359cfcc7 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1456
    #22 0x7ffe57f9774d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #23 0x7ffe5799e3c4 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #24 0x7ffe579a32a1 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #25 0x7ffe534f5f72 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:992
    #26 0x7ffe534f63c5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1887
    #27 0x7ffe534ea761 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1832

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:131 in llvm::BasicBlock::getTerminator
Shadow bytes around the buggy address:
  0x12be01fb4380: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x12be01fb4400: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x12be01fb4480: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x12be01fb4500: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x12be01fb4580: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
=>0x12be01fb4600: fa fa f7 fa fd fd fd fd fd fd fd fd fd[fd]fd fa
  0x12be01fb4680: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x12be01fb4700: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x12be01fb4780: fa fa f7 fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12be01fb4800: fa fa f7 fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12be01fb4880: fa fa f7 fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==4316==ADDITIONAL INFO

==4316==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffe4680c66e in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684
    #1 0x7ffe468056c5 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:483


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==4316==END OF ADDITIONAL INFO
==4316==ABORTING
[5188:8084:0513/113059.736:ERROR:gpu_process_host.cc(1002)] GPU process exited unexpectedly: exit_code=1
[5188:8084:0513/113059.750:WARNING:gpu_process_host.cc(1436)] The GPU process has crashed 1 time(s)

```

## Attachments

- [index_FoldTwoEntryPHINode.html](attachments/index_FoldTwoEntryPHINode.html) (text/html, 4.1 KB)
- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 1.2 KB)
- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 1.3 KB)
- [asanlogfold](attachments/asanlogfold) (application/octet-stream, 23.4 KB)

## Timeline

### wg...@gmail.com (2024-05-13)

I'm not really sure what going on with the upload function; the browser console logs:

```
GET https://people-pa.clients6.google.com/v2/people/rankedTargets?affinity.type=CONTACT_STORE_DEFAULT_AFFINITY&context.clientVersion.clientAgent=CONTACT_STORE&context.clientVersion.clientType=BUGANIZER&context.clientVersion.clientVersion=contact_store_336195648&pagingOptions.pageSize=500&requestMask.includeContainer=CONTACT&requestMask.includeContainer=PROFILE&requestMask.includeContainer=DOMAIN_CONTACT&requestMask.includeContainer=DOMAIN_PROFILE&requestMask.includeContainer=AFFINITY&requestMask.includeField=person.name%2Cperson.photo%2Cperson.email%2Cperson.phone%2Cperson.email.certificate%2Cperson.metadata&mergedPersonSourceOptions.includedProfileStates=CORE_ID&mergedPersonSourceOptions.personModelParams.personModel=CONTACT_CENTRIC&extensionSet.extensionNames=FILTER_TO_PRIMARY&key=REMOVEDBYWGSLFUZZ

401 (Unauthorized)

```

Once the upload is fixed I'll upload the html file + standalone hlsl file. The standalone wgsl code should be enough for starting to investigate:

```
struct t {
    m: vec2<f32>,
}

@group(0) @binding(0)
var<uniform> g: t;

var<private> g_1: vec4<f32>;

fn f() {
    var l: i32 = 0;
    var l_1: i32 = 0;

    loop {
        let x_35_ = g.m.y;
        let _e13 = i32(x_35_);
        let _e14 = (l_1 < _e13);
        if (l_1 >= _e13) {
            break;
        }
        let _e16 = (l > 0); 
        if _e16 {
            break;
        } else {
            let _e28 = vec3(_e14);
            if _e28[l] {
                switch l { 
                    case 0: {
                        return;
                    }
                    case -1: {
                        return;
                    }
                    default: {
                    }
                }
                if _e16 {
                    loop {
                        continuing {
                            break if _e28[l];
                        }
                    }
                }
            } else {
                g_1 = vec4<f32>(0.0, 0.0, 0.0, x_35_);
            }
        }
        l = l_1;
        continuing {
            l_1 = (l_1 + 1); 
        }
    }   
    g_1 = vec4<f32>(0.0, 0.0, 0.0, 0.0);
}

@fragment
fn main() -> @location(0) vec4<f32> {
    f();
    return g_1;
}

```

### ad...@google.com (2024-05-13)

Thanks, there's an upload problem with our bug tracker today - it's being worked on. Sorry about that. Is the hlsl short enough that you could paste it inline too?

### wg...@gmail.com (2024-05-14)

standalone hlsl:

```
int tint_ftoi(float v) {
  return ((v < 2147483520.0f) ? ((v < -2147483648.0f) ? -2147483648 : int(v)) : 2147483647);
}

cbuffer cbuffer_g : register(b0) {
  uint4 g[1];
};
static float4 g_1 = float4(0.0f, 0.0f, 0.0f, 0.0f);

void f() {
  int l = 0;
  int l_1 = 0;
  while (true) {
    float x_35_ = asfloat(g[0].y);
    int _e13 = tint_ftoi(x_35_);
    bool _e14 = (l_1 < _e13);
    if ((l_1 >= _e13)) {
      break;
    }   
    bool _e16 = (l > 0); 
    if (_e16) {
      break;
    } else {
      bool3 _e28 = bool3((_e14).xxx);
      if (_e28[l]) {
        switch(l) {
          case 0: {
            return;
            break;
          }
          case -1: {
            return;
            break;
          }
          default: {
            break;
          }
        }
        if (_e16) {
          while (true) {
            {
              if (_e28[l]) { break; }
            }
          }
        }
      } else {
        g_1 = float4(0.0f, 0.0f, 0.0f, x_35_);
      }   
    } 
    l = l_1;
    {   
      l_1 = (l_1 + 1); 
    }   
  }
  g_1 = (0.0f).xxxx;
}

struct tint_symbol {
  float4 value : SV_Target0;
};

float4 main_inner() {
  f();
  return g_1;
}

tint_symbol main() {
  float4 inner_result = main_inner();
  tint_symbol wrapper_result = (tint_symbol)0;
  wrapper_result.value = inner_result;
  return wrapper_result;
}

```

### ad...@google.com (2024-05-14)

I don't have access to a physical Windows machine (and I assume that's necessary) so I'm unable to test out the WGSL. However, with Dawn revision 2ea615d914b17fa882c0bb50eab29216edb5075e, building the `dxc` binary under ASAN and using `out/test/dxc -T ps_6_2 -HV 2018 poc-340196361.hlsl` does indeed result in the UaF above.

I assume that the wgsl shader achieves the same result. As this is Windows-only, we consider the GPU process sandboxed, and I'll rate this as S1.

### ad...@google.com (2024-05-14)

That dawn revision corresponds to M124, so labeling appropriately.

### ad...@google.com (2024-05-14)

This still happens on the latest dawn revision 4c8379a4ab2ad42a02eb8528ad01c15c879da803.

### pe...@google.com (2024-05-14)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-14)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### am...@google.com (2024-05-17)

Investigation started yesterday, see [doc](https://docs.google.com/document/d/10uQcKBy4ICItAdDIsn1iQN0YlyA97g0U85SS5hylSrI/edit?usp=sharing&resourcekey=0-sdHSqPYE9zcCNlURN6klDA).

### am...@google.com (2024-05-22)

Figured out the bug, and have put up a fix: <https://github.com/microsoft/DirectXShaderCompiler/pull/6643>

Waiting on Microsoft to review.

### am...@google.com (2024-05-23)

Upstream [PR has been approved and merged](https://github.com/microsoft/DirectXShaderCompiler/pull/6643). Waiting for it to roll into Dawn, then into Chromium, so that I can test on Canary.

### am...@google.com (2024-05-30)

This has been fixed in latest Canary:

- I tested opening the attached `index_FoldTwoEntryPHINode.html` in Chrome `Version 125.0.6422.78 (Official Build) (64-bit)`, and the GPU process crashes.
- I tested opening the same file in Canary, `Version 127.0.6511.0 (Official Build) canary (64-bit)`, and the GPU process no longer crashes. The console output does not show any errors, as expected, but simply outputs the GPUDevice and GPURenderPipeline state.
- Upstream fix: <https://github.com/microsoft/DirectXShaderCompiler/pull/6643>
- Roll of DXC with fix to Dawn: <https://dawn-review.googlesource.com/c/dawn/+/189760>
- Dawn with fix roll into Chrome: <https://chromium-review.googlesource.com/c/chromium/src/+/5567994>

### pe...@google.com (2024-05-31)

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


### pg...@google.com (2024-06-04)

There are no more scheduled releases for M124/M125 - removing label

### am...@google.com (2024-06-04)

1. Which CLs should be backmerged? (Please include Gerrit links.)

- Upstream fix: <https://github.com/microsoft/DirectXShaderCompiler/pull/6643>
- Roll of DXC with fix to Dawn: <https://dawn-review.googlesource.com/c/dawn/+/189760>
- Dawn with fix roll into Chrome: <https://chromium-review.googlesource.com/c/chromium/src/+/5567994>

Note that the DXC fix will be cherry-picked to a custom branch in our DXC mirror, then updated in a Dawn custom branch for Chrome release.

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes.

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

Yes. Test by opening `index_FoldTwoEntryPHINode.html` in Canary, and note that the GPU proces does not crash. The console output does not show any errors, as expected, but simply outputs the GPUDevice and GPURenderPipeline state.

### pg...@google.com (2024-06-05)

Thank you for your patience here!

The fix landed May 24th and hence has gotten plenty of canary data with nothing of note

Merge approved for M126 - please cherry pick the fix to branch 6478 by next Thursday June 13th EOD MTV time to get this fix into the next stable respin!

### sp...@google.com (2024-06-05)

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

### am...@chromium.org (2024-06-05)

Congratulations on another one, wgslfuzz! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-06-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-06-10)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6478

commit b845fed991110a834225be67aeb89e0e205689dd
Author: Natalie Chouinard <chouinard@google.com>
Date:   Mon Jun 10 18:21:40 2024

    Fix LoopDeletion incorrectly updating PHI with multiple duplicate inputs (#6643)
    
    LoopDeletion was incorrectly updating PHI nodes in the target block when
    it had duplicate input edges. This happens, for example, when deleting a
    loop that uses a switch with multiple cases that exit the same way.
    
    After determining that this was the bug, I found this fix in LLVM:
    https://reviews.llvm.org/D34516 and applied it here.
    
    Bug: 340196361
    Change-Id: I98b150bb9a164466eb84dd3d46f720d5d92ef909
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5616791
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>
    Reviewed-by: dan sinclair <dsinclair@chromium.org>

M       lib/Transforms/Scalar/LoopDeletion.cpp
A       tools/clang/test/DXC/Passes/DxilLoopDeletion/dxil-loop-deletion-phi-with-duplicate-preds.ll

https://chromium-review.googlesource.com/5616791


### ap...@google.com (2024-06-10)

Project: dawn
Branch: chromium/6478

commit b44f52d869cb1cbfca7484b109285f99f73983c7
Author: Natalie Chouinard <chouinard@google.com>
Date:   Mon Jun 10 19:04:31 2024

    DEPS: Update DXC to patched branch
    
    Bug: 340196361
    Change-Id: I3e69809cc11bc8761ad929080c7f463f1cfce263
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/192761
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/192761


### ch...@google.com (2024-06-10)

This has been merged to M126: <https://chromium.googlesource.com/chromium/src.git/+/bdcac3e9514768c40445e621721228c830992191>

### pe...@google.com (2024-09-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in the GPU process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/340196361)*
