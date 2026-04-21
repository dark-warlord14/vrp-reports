# GPU process crash via WebGPU shader - UAF in ConstantFoldTerminator at Transforms\Utils\Local.cpp:93

| Field | Value |
|-------|-------|
| **Issue ID** | [339171223](https://issues.chromium.org/issues/339171223) |
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

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this triggers an UAF inside the hlsl compiler.

##### VERSION

Chrome Version: Pre-compiled ASAN Chromium 126.0.6465.0 (Developer Build) (64-bit)
Operating System: Win10 Build 19045.4291

##### REPRODUCTION CASE

Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process.

Reproducing the issue stand-alone on Linux also possible:

1. Compile the standalone.wgsl with tint (commit 5976efe6b4b72c822085cf7ee08ad00036888ab5) to hlsl via `./tint standalone.wgsl -o standalone.hlsl`. I also attached standalone.hlsl, but you should get the very same file when compiling standalone.wgsl yourself
2. Compile the hlsl with dxc (commit 773b01272719e07ea369bc17f5ddfce248751c7a): `./dxc-3.7 standalone.hlsl -T ps_6_2`. This should trigger an ASAN violation.

##### Attached:

- html that triggers an ASAN violation in chromium
- wgsl for producing the hlsl shader
- the hlsl shader
- asan log file

```
[9052:7868:0507/063454.505:WARNING:chrome_main_delegate.cc(742)] This is Chrome version 126.0.6465.0 (not a warning)
[9052:3332:0507/063454.735:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[9052:2156:0507/063454.909:ERROR:sandbox_win.cc(913)] Sandbox cannot access executable. Check filesystem permissions are valid. See https://bit.ly/31yqMJR.: Access is denied. (0x5)
[9052:7868:0507/063454.948:WARNING:account_consistency_mode_manager.cc(77)] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
[9052:7868:0507/063455.162:WARNING:browser_management_service.cc(128)] EnterpriseLogoUrl fetch failed with error code -1 and MIME type 
[9052:7868:0507/063456.916:ERROR:network_service_instance_impl.cc(600)] Network service crashed, restarting service.
[9052:7868:0507/063456.943:WARNING:external_registry_loader_win.cc(232)] Error observing HKLM: 5
[9052:1800:0507/063459.325:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[8784:7296:0507/063459.972:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[8784:7296:0507/063512.196:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[9052:4052:0507/063512.364:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[8784:7084:0507/063521.593:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[9052:8844:0507/063532.085:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[8784:2628:0507/063543.246:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[9052:2156:0507/063803.323:ERROR:sandbox_win.cc(913)] Sandbox cannot access executable. Check filesystem permissions are valid. See https://bit.ly/31yqMJR.: Access is denied. (0x5)
[9052:7868:0507/063930.775:INFO:CONSOLE(20)] "[object GPUDevice]", source: file://vboxsvr/shared/indexCanPropagatePredecessorsForPHIs.html (20)
[9052:7868:0507/063930.799:INFO:CONSOLE(107)] "[object GPURenderPipeline]", source: file://vboxsvr/shared/indexCanPropagatePredecessorsForPHIs.html (107)
=================================================================
==7368==ERROR: AddressSanitizer: heap-use-after-free on address 0x122d458c3318 at pc 0x7ffed63ec804 bp 0x008564bfba00 sp 0x008564bfba48
WRITE of size 8 at 0x122d458c3318 thread T0
==7368==WARNING: Failed to use and restart external symbolizer!
==7368==*** WARNING: Failed to initialize DbgHelp!              ***
==7368==*** Most likely this means that the app is already      *** 
==7368==*** using DbgHelp, possibly with incompatible flags.    *** 
==7368==*** Due to technical reasons, symbolization might crash *** 
==7368==*** or produce wrong results.                           ***
    #0 0x7ffed63ec803 in llvm::PHINode::removeIncomingValue C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Instructions.cpp:106
    #1 0x7ffed64cf19c in llvm::BasicBlock::removePredecessor C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:320
    #2 0x7ffed72268a5 in llvm::ConstantFoldTerminator C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\Local.cpp:93
    #3 0x7ffed72d096e in llvm::SimplifyCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\SimplifyCFG.cpp:4740
    #4 0x7ffed66f58cf in simplifyFunctionCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\SimplifyCFGPass.cpp:157
    #5 0x7ffed5627f54 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #6 0x7ffed56289ee in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #7 0x7ffed56296a5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #8 0x7ffed56329cc in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #9 0x7ffed50408c1 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #10 0x7ffed575e431 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #11 0x7ffed503b5b2 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #12 0x7ffed5048d83 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #13 0x7ffed4f26b73 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #14 0x7ffedd881fb5 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #15 0x7ffedd8e954e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #16 0x7ffedd9911b4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #17 0x7ffedd97a933 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:385
    #18 0x7ffedd79bec0 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #19 0x7ffedd6ee081 in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2125
    #20 0x7ffedd6eda67 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1456
    #21 0x7ffeffb8c0bd in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #22 0x7ffeff592dd4 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606    
    #23 0x7ffeff597c81 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #24 0x7ffefb14a692 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:992
    #25 0x7ffefb14aae5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1888
    #26 0x7ffefb13ee71 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1833
    #27 0x7ffeeee28863 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #28 0x7ffeeb9daf1c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:506
    #29 0x7ffeeb9d99c3 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:154
    #30 0x7ffeeee4669a in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:936
    #31 0x7ffeeee579ba in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #32 0x7ffeee4abf4d in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:743
    #33 0x7ffeee4aa2a8 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:668
    #34 0x7ffeee4ad5d8 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #35 0x7ffee98ebf20 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #36 0x7ffeed2c8d6e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #37 0x7ffeed2c7c79 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #38 0x7ffeed2fd27e in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #39 0x7ffeed2ca9bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:645
    #40 0x7ffee9936430 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #41 0x7ffeec77e15d in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:438
    #42 0x7ffee81d8232 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:780
    #43 0x7ffee81da7b3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1156
    #44 0x7ffee81d61cd in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #45 0x7ffee81d6cbd in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #46 0x7ffedb1b16b1 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #47 0x7ff698ed43a5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #48 0x7ff698ed1db2 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #49 0x7ff6992b0143 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #50 0x7fff52017343 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017343)
    #51 0x7fff527426b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)

0x122d458c3318 is located 88 bytes inside of 160-byte region [0x122d458c32c0,0x122d458c3360)
freed by thread T0 here:
    #0 0x7ff698faca0d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffed52efc5b in llvm::CallInst::~CallInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:1438
    #2 0x7ffed64cd0d1 in llvm::iplist<llvm::Instruction,llvm::ilist_traits<llvm::Instruction> >::clear C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\ADT\ilist.h:563
    #3 0x7ffed64ccb72 in llvm::BasicBlock::~BasicBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:91
    #4 0x7ffed64d0a0f in llvm::BasicBlock::~BasicBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:70
    #5 0x7ffed72323b1 in llvm::removeUnreachableBlocks C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\Local.cpp:1306
    #6 0x7ffed66f4d5d in simplifyFunctionCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\SimplifyCFGPass.cpp:155
    #7 0x7ffed5627f54 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #8 0x7ffed56289ee in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #9 0x7ffed56296a5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #10 0x7ffed56329cc in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #11 0x7ffed50408c1 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #12 0x7ffed575e431 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #13 0x7ffed503b5b2 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #14 0x7ffed5048d83 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #15 0x7ffed4f26b73 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #16 0x7ffedd881fb5 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #17 0x7ffedd8e954e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #18 0x7ffedd9911b4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #19 0x7ffedd97a933 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:385
    #20 0x7ffedd79bec0 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #21 0x7ffedd6ee081 in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2125
    #22 0x7ffedd6eda67 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1456
    #23 0x7ffeffb8c0bd in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #24 0x7ffeff592dd4 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #25 0x7ffeff597c81 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #26 0x7ffefb14a692 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:992
    #27 0x7ffefb14aae5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1888

previously allocated by thread T0 here:
    #0 0x7ff698facb0d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffed7a42f5e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffed64cbc31 in llvm::User::operator new C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:96
    #3 0x7ffed52ef950 in llvm::CallInst::Create C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:1401
    #4 0x7ffed7436839 in `anonymous namespace'::TrivialDxilOperation C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLOperationLower.cpp:462
    #5 0x7ffed740eee9 in `anonymous namespace'::TrivialUnaryOperation C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLOperationLower.cpp:546
    #6 0x7ffed73db6ec in TranslateHLBuiltinOperation C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLOperationLower.cpp:9244
    #7 0x7ffed73de4bd in hlsl::TranslateBuiltinOperations C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLOperationLower.cpp:9426
    #8 0x7ffed6790863 in `anonymous namespace'::DxilGenerationPass::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\DxilGenerationPass.cpp:253
    #9 0x7ffed56296a5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #10 0x7ffed56329cc in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #11 0x7ffed50408c1 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #12 0x7ffed575e431 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #13 0x7ffed503b5b2 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #14 0x7ffed5048d83 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #15 0x7ffed4f26b73 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #16 0x7ffedd881fb5 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #17 0x7ffedd8e954e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #18 0x7ffedd9911b4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #19 0x7ffedd97a933 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:385
    #20 0x7ffedd79bec0 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #21 0x7ffedd6ee081 in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2125
    #22 0x7ffedd6eda67 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1456
    #23 0x7ffeffb8c0bd in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #24 0x7ffeff592dd4 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #25 0x7ffeff597c81 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #26 0x7ffefb14a692 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:992
    #27 0x7ffefb14aae5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1888

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Instructions.cpp:106 in llvm::PHINode::removeIncomingValue
Shadow bytes around the buggy address:
  0x122d458c3080: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
  0x122d458c3100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x122d458c3180: fd fd fd fd fa fa fa fa fa fa f7 fa fd fd fd fd
  0x122d458c3200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x122d458c3280: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
=>0x122d458c3300: fd fd fd[fd]fd fd fd fd fd fd fd fd fa fa fa fa
  0x122d458c3380: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x122d458c3400: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa
  0x122d458c3480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x122d458c3500: fd fd fd fa fa fa fa fa fa fa f7 fa fd fd fd fd
  0x122d458c3580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
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

==7368==ADDITIONAL INFO

==7368==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffeee4aa44e in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684
    #1 0x7ffeee4a34a5 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:483


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==7368==END OF ADDITIONAL INFO
==7368==ABORTING
[9052:7868:0507/063938.469:ERROR:gpu_process_host.cc(1002)] GPU process exited unexpectedly: exit_code=1
[9052:7868:0507/063938.504:WARNING:gpu_process_host.cc(1436)] The GPU process has crashed 1 time(s)

```

## Attachments

- [asanlogconstantfold](attachments/asanlogconstantfold) (application/octet-stream, 23.4 KB)
- [indexCanPropagatePredecessorsForPHIs.html](attachments/indexCanPropagatePredecessorsForPHIs.html) (text/html, 3.9 KB)
- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 1.1 KB)
- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 1.0 KB)
- [s2.hlsl](attachments/s2.hlsl) (application/octet-stream, 867 B)
- [bad.ll](attachments/bad.ll) (application/octet-stream, 13.7 KB)
- [good.ll](attachments/good.ll) (application/octet-stream, 8.5 KB)
- [RemoveUnstructuredExits b_339171223.png](attachments/RemoveUnstructuredExits b_339171223.png) (image/png, 122.0 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-05-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5927228794667008.

### 24...@project.gserviceaccount.com (2024-05-07)

Testcase 5927228794667008 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5927228794667008.

### pe...@google.com (2024-05-09)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ad...@google.com (2024-05-10)

Reproduced on Linux in the dawn repo by building dxc with asan, on dawn branch origin/chromium/6367, so labeling as FoundIn-124.

### pe...@google.com (2024-05-10)

Setting milestone because of s0/s1 severity.

### dn...@google.com (2024-05-13)

I've reduced the test case slightly, attaching as s2.hlsl.

Things that make the bug go away include:

- Removing the l\_2 variable from the f function
- changing \_e8 to be a scalar variable
- Changing g to e a scalar variable

In a debug build with ASAN turned on, the error symptom is the following, which occurs during a simplifycfg pass:

```
While deleting: float %DerivFineX
Use still stuck around after Def is destroyed:  %g.i.1.i0 = phi float [ %DerivFineX, %dx.struct_exit.cond_end ], [ 0.000000e+00, %for.cond.i.32.i ]
dxc: /usr/local/google/home/dneto/project/dxc/lib/IR/Value.cpp:83: virtual llvm::Value::~Value(): Assertion `use_empty() && "Uses remain when a value is destroyed!"' failed.

```

### dn...@google.com (2024-05-13)

The last time the simplifycfg pass runs on the module, it does two simplification iterations over the 'main' function. By that time the helper functions have been inlined into 'main'.

I'm attaching two copies of the module:

- 3.ll is the module before that first iteration.
- 4.ll is the module before the second iteraiton.

If I run LLVM's `opt 3.ll` it passes, so the module is self-consistent.
If I run `opt 4.ll` it immediately detects an error:

```
$ ../build/bin/opt 4.ll
Instruction does not dominate all uses!
  %DerivFineX = call float @dx.op.unary.f32(i32 85, float 0.000000e+00), !dbg !16
  %g.i.1.i0 = phi float [ %DerivFineX, %dx.struct_exit.cond_end ], [ 0.000000e+00, %for.cond.i.32.i ]
Instruction does not dominate all uses!
  %DerivFineX1 = call float @dx.op.unary.f32(i32 85, float 0.000000e+00), !dbg !16
  %g.i.1.i1 = phi float [ %DerivFineX1, %dx.struct_exit.cond_end ], [ 0.000000e+00, %for.cond.i.32.i ]
Instruction does not dominate all uses!
  %DerivFineX2 = call float @dx.op.unary.f32(i32 85, float 0.000000e+00), !dbg !16
  %g.i.1.i2 = phi float [ %DerivFineX2, %dx.struct_exit.cond_end ], [ 0.000000e+00, %for.cond.i.32.i ]
Instruction does not dominate all uses!
  %DerivFineX3 = call float @dx.op.unary.f32(i32 85, float 0.000000e+00), !dbg !16
  %g.i.1.i3 = phi float [ %DerivFineX3, %dx.struct_exit.cond_end ], [ 0.000000e+00, %for.cond.i.32.i ]
../build/bin/opt: 4.ll: error: input module is broken!

```

### dn...@google.com (2024-05-16)

This is the stack trace in a debug build:

```
#5  0x00007ffff7a533a2 in __assert_fail (assertion=0x7ffff5f601b0 "use_empty() && \"Uses remain when a value is destroyed!\"", 
    file=0x7ffff5f5ffc8 "/usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/IR/Value.cpp", line=83, 
    function=0x7ffff5f6018f "virtual llvm::Value::~Value()") at ./assert/assert.c:101
#6  0x00007ffff3d2e240 in llvm::Value::~Value (this=0x555555a8f668, __in_chrg=<optimized out>)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/IR/Value.cpp:83
#7  0x00007ffff3c5caf0 in llvm::User::~User (this=0x555555a8f668, __in_chrg=<optimized out>)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/include/llvm/IR/User.h:76
#8  0x00007ffff3cc1c0d in llvm::Instruction::~Instruction (this=0x555555a8f668, __in_chrg=<optimized out>)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/IR/Instruction.cpp:50
#9  0x00007ffff3cc753e in llvm::CallInst::~CallInst (this=0x555555a8f668, __in_chrg=<optimized out>)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/IR/Instructions.cpp:223
#10 0x00007ffff3cc755a in llvm::CallInst::~CallInst (this=0x555555a8f668, __in_chrg=<optimized out>)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/IR/Instructions.cpp:223
#11 0x00007ffff3c4d500 in llvm::ilist_node_traits<llvm::Instruction>::deleteNode (V=0x555555a8f668)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/include/llvm/ADT/ilist.h:113
#12 0x00007ffff3c4cac9 in llvm::iplist<llvm::Instruction, llvm::ilist_traits<llvm::Instruction> >::erase (this=0x555555b11c60, where=...)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/include/llvm/ADT/ilist.h:479
#13 0x00007ffff3c4c2b5 in llvm::iplist<llvm::Instruction, llvm::ilist_traits<llvm::Instruction> >::erase (this=0x555555b11c60, first=..., 
    last=...) at /usr/local/google/home/dneto/project/DirectXShaderCompiler/include/llvm/ADT/ilist.h:559
#14 0x00007ffff3c4b786 in llvm::iplist<llvm::Instruction, llvm::ilist_traits<llvm::Instruction> >::clear (this=0x555555b11c60)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/include/llvm/ADT/ilist.h:563
#15 0x00007ffff3c48f3c in llvm::BasicBlock::~BasicBlock (this=0x555555b11c30, __in_chrg=<optimized out>)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/IR/BasicBlock.cpp:91
#16 0x00007ffff3c48f78 in llvm::BasicBlock::~BasicBlock (this=0x555555b11c30, __in_chrg=<optimized out>)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/IR/BasicBlock.cpp:92
#17 0x00007ffff3c4c436 in llvm::ilist_node_traits<llvm::BasicBlock>::deleteNode (V=0x555555b11c30)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/include/llvm/ADT/ilist.h:113
#18 0x00007ffff3c4b989 in llvm::iplist<llvm::BasicBlock, llvm::ilist_traits<llvm::BasicBlock> >::erase (this=0x555555a8a160, where=...)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/include/llvm/ADT/ilist.h:479
#19 0x00007ffff436030b in llvm::removeUnreachableBlocks (F=...)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/Transforms/Utils/Local.cpp:1306
#20 0x00007ffff42b5541 in simplifyFunctionCFG (F=..., TTI=..., AC=0x555555a8f050, BonusInstThreshold=1)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/Transforms/Scalar/SimplifyCFGPass.cpp:166
#21 0x00007ffff42b5914 in (anonymous namespace)::CFGSimplifyPass::runOnFunction (this=0x555555ac48a0, F=...)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/Transforms/Scalar/SimplifyCFGPass.cpp:232
#22 0x00007ffff5a52746 in llvm::FPPassManager::runOnFunction (this=0x555555ab5220, F=...)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/IR/LegacyPassManager.cpp:1587
#23 0x00007ffff5a529ae in llvm::FPPassManager::runOnModule (this=0x555555ab5220, M=...)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/IR/LegacyPassManager.cpp:1609
#24 0x00007ffff5a52e12 in (anonymous namespace)::MPPassManager::runOnModule (this=0x555555a0ef50, M=...)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/IR/LegacyPassManager.cpp:1669
#25 0x00007ffff5a535bd in llvm::legacy::PassManagerImpl::run (this=0x555555a9bdc0, M=...)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/IR/LegacyPassManager.cpp:1771
#26 0x00007ffff5a5392c in llvm::legacy::PassManager::run (this=0x555555a9bd30, M=...)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/IR/LegacyPassManager.cpp:1814
#27 0x00007ffff43f6288 in (anonymous namespace)::EmitAssemblyHelper::EmitAssembly (this=0x7fffffff9760, Action=clang::Backend_EmitBC, 
    OS=0x555555a1a8c0) at /usr/local/google/home/dneto/project/DirectXShaderCompiler/tools/clang/lib/CodeGen/BackendUtil.cpp:756
#28 0x00007ffff43f646d in clang::EmitBackendOutput (Diags=..., CGOpts=..., TOpts=..., LOpts=..., TDesc=..., M=0x555555a1b4d0, 
    Action=clang::Backend_EmitBC, OS=0x555555a1a8c0)


```

The relevant part is likely at #18, #19, #20 where the removeUnreachableBlocks code is erasing a block.

```
#18 0x00007ffff3c4b989 in llvm::iplist<llvm::BasicBlock, llvm::ilist_traits<llvm::BasicBlock> >::erase (this=0x555555a8a160, where=...)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/include/llvm/ADT/ilist.h:479
#19 0x00007ffff436030b in llvm::removeUnreachableBlocks (F=...)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/Transforms/Utils/Local.cpp:1306
#20 0x00007ffff42b5541 in simplifyFunctionCFG (F=..., TTI=..., AC=0x555555a8f050, BonusInstThreshold=1)
    at /usr/local/google/home/dneto/project/DirectXShaderCompiler/lib/Transforms/Scalar/SimplifyCFGPass.cpp:166

```

Cleary one of the instructions in the block being erased defines the value `%DerivFineX` but it's used in a phi in another block.

### dn...@google.com (2024-05-16)

I dug into the history of the removeUnreachableBlocks function, and found that the block erasure pattern was added in 2013 with this patch:

<https://github.com/llvm/llvm-project/commit/2a066afce50be640103c36932fd88eefe69d9dde#diff-260cb3f00c79bee922ae9d3c19da751208997ad5c919d5cdf412c2259e0445ebR994>

```
  for (Function::iterator I = llvm::next(F.begin()), E=F.end(); I != E;)
    if (!Reachable.count(I))
      I = F.getBasicBlockList().erase(I);
    else
      ++I;

```

That pattern was changed in 2019 with this patch:

<https://github.com/llvm/llvm-project/commit/167b0529be766a85db3c0811607ac60f821670ff>

The new snippet looks like this:

```
    for (auto *BB : DeadBlockSet)
      BB->eraseFromParent();

```

Then deletion code was removed from removeUnreachableBlocks and now calls an existing DeleteDeadBlocks() function, via this patch in 2021:

<https://github.com/llvm/llvm-project/commit/b0bb2149b3711d5d7c4fd3182a7eac3f8fc17341>

### dn...@google.com (2024-05-16)

I should mention my current theory is that the removal code in DXC is an old version that didn't handle the edge case we have, and that newer LLVM code has fixed this problem. So I'm digging through history to see if I can spot the fix, or find suitable code to use instead.

### dn...@google.com (2024-05-16)

DXC has its own dead block deletion utility, which pays attention to metadata marking explicit breaks.
See <https://github.com/microsoft/DirectXShaderCompiler/blob/fd7e54bcd527daeb0e400c200aab4f66730525e6/lib/Transforms/Scalar/DxilRemoveDeadBlocks.cpp#L91>

### dn...@google.com (2024-05-16)

Top of tree LLVM's unreachable block deletion calls DeleteDeadBlocks which bottoms out llvm::detachDeadBlocks
herer: <https://github.com/llvm/llvm-project/blob/e5e562361555fc96c768b1dd3dd99f403f500838/llvm/lib/Transforms/Utils/BasicBlockUtils.cpp#L62>

It has code that scans the instructions inside the block, and replaces their uses with poison (we can settle for undef).

That's exactly the thing that should be happening, but isn't.

Note that even the DXC-era code has this utility:
<https://github.com/microsoft/DirectXShaderCompiler/blob/fd7e54bcd527daeb0e400c200aab4f66730525e6/lib/Transforms/Utils/BasicBlockUtils.cpp#L36>
That older version of the code also erases the block from its parent.

### dn...@google.com (2024-05-16)

The deleteDeadBlocks function requires that all the blocks to not have predecessors.
Looking at BasicBlock::removePredecessor, it seems to do exactly what we need it to do: its whole action is to remove a given Pred block as an incoming (block,value) pair from the target block's Phi nodes.

That suggests that we can tweak the existing code to call removePredecessors on all the dead blocks before trying to erase them.

### dn...@google.com (2024-05-16)

It's not that simple. Here's what's going on. The problem occurs with a pattern of 3 blocks:

```
dx.struct_exit.cond_body:                         ; No predecessors!
  %DerivFineX = call float @dx.op.unary.f32(i32 85, float 0.000000e+00), !dbg !16

...
dx.struct_exit.cond_end:                          ; preds = %"\01?f@@YAXXZ.exit.i", %dx.struct_exit.cond_body
  %10 = phi i1 [ false, %"\01?f@@YAXXZ.exit.i" ], [ %cmp6.i, %dx.struct_exit.cond_body ]
  %11 = phi float [ 0.000000e+00, %"\01?f@@YAXXZ.exit.i" ], [ %DerivFineX3, %dx.struct_exit.cond_body ]
...
  br i1 %10, label %if.end.i, label %for.cond.i.32.i, !dbg !18


if.end.i:                                         ; preds = %for.cond.i.32.i, %dx.struct_exit.cond_end
  %g.i.1.i0 = phi float [ %DerivFineX, %dx.struct_exit.cond_end ], [ 0.000000e+00, %for.cond.i.32.i ]

```

Now, `dx.struct_exit.cond_body` is dead, and should be removed.
The other two blocks are live, and won't be removed.
Block `dx.struct_exit.cond_end` is live and has the dead block as predecessor.
Block `if.end.i` is live and has `dx.struct_exit.cond_end` as a predecessor, at least if we ignore the condition.

But `if.end.i` uses `%DerivFineX` as the incoming value when branching from *live* predecessor `dx.struct_exit.cond_end`.

When we erase the dead block, `%DerivFineX` is deleted! Removing the dead block from its succesors is only removing it from its *immediate* succesors, and so it ends up missing the use of `%DerivFineX` in the far away live block. And then things go boom because there's an orphaned use.

This explains the additional work that llvm::detatchDeadBlocks does to replace used values by poison/undef, here: <https://github.com/llvm/llvm-project/blob/e5e562361555fc96c768b1dd3dd99f403f500838/llvm/lib/Transforms/Utils/BasicBlockUtils.cpp#L79>

The comment explains it well:

```
    // Zap all the instructions in the block.
    while (!BB->empty()) {
      Instruction &I = BB->back();
      // If this instruction is used, replace uses with an arbitrary value.
      // Because control flow can't get here, we don't care what we replace the
      // value with.  Note that since this block is unreachable, and all values
      // contained within it must dominate their uses, that all uses will
      // eventually be removed (they are themselves dead).
      if (!I.use_empty())
        I.replaceAllUsesWith(PoisonValue::get(I.getType()));
      BB->back().eraseFromParent();
    }

```

### dn...@google.com (2024-05-16)

Note that for efficiency's sake, it works from the end of the block backward. That's because the common case is for an early instruction in a basic block to be used by a later instruction in the same basic block. Going backwards causes the replacements to occur far less frequently.

### dn...@google.com (2024-05-17)

Ok, calling DeleteDeadBlocks gets us much further, then we run into this situation:

```
==remove dead blocks in Function  
; Function Attrs: nounwind
define void @main(<4 x float>* noalias) #0 {
entry: 
  br label %while.cond.i.23.i
  
while.cond.i.i:                                   ; preds = %1, %while.cond.i.i
  br label %while.cond.i.i, !dbg !3               
  
while.cond.i.23.i:                                ; preds = %entry, %while.cond.i.23.i
  br label %while.cond.i.23.i, !dbg !12           
   
; <label>:1                                               ; No predecessors!
  br i1 false, label %while.cond.i.i, label %2    
  
; <label>:2                                       ; preds = %1
  ret void, !dbg !14                              
} 


```

Blocks `while.cond.i.i` and `%1` and `%2` are dead.
The first one we try to delete is `while.cond.i.i`, but it has two predecessors: itself, and `%1`.

The `DeleteDeadBlock` code as it is in the DXC-era codebase asserts that the block you are deleting either has no predecessors, or only has itself as a predecessor.
When we try to delete `while.cond.i.i`, that assertion fails.

The top-of-tree version of LLVM has refactored that code to remove that assumption. See
<https://github.com/llvm/llvm-project/blob/e5e562361555fc96c768b1dd3dd99f403f500838/llvm/lib/Transforms/Utils/BasicBlockUtils.cpp#L101>

We should backport that code.

### dn...@google.com (2024-05-17)

Backporting that code fixes the remaining issue.
I'll make some targeted tests and post a PR

### dn...@google.com (2024-05-17)

When trying to make a simplifycfg test for this, I found that the module was always invalid.

Example:

```
define i32 @test1(i1 %cond, i32 %a) {
if0:
  br i1 false, label %then0, label %if1

then0:        ; a dead block
  %sum = add i32 0, 0   ;  used in phi in a block that is not a successor
  br label %if1

if1:
  %c2 = phi i1 [ false, %if0 ], [true, %then0 ]
  br i1 %c2, label %end, label %then1

then1:
  br label %end

end:
  %b = phi i32 [ %a, %if1 ], [ %sum, %then1 ]; not a successor of dead block
  ret i32 %b
}

```

LLVM complains:

```
Instruction does not dominate all uses!
  %sum = add i32 0, 0
  %b = phi i32 [ %a, %if1 ], [ %sum, %then1 ]
opt: unreachable-distant-phi.ll: error: input module is broken!

```

### dn...@google.com (2024-05-17)

It appears the loop-unroll pass breaks the module.

### dn...@google.com (2024-05-17)

Per amaiorano@ and bclayton@'s advice, I tried `-opt-disable structurize-loop-exits-for-unroll` which disables some DXC's custom code, and the problem goes away.

Similar to [b/339169163](https://issues.chromium.org/issues/339169163)

### dn...@google.com (2024-05-17)

Well, not so similar.
In this case, the loop structurizer produces an invalid module, and the flow continues until asserting out in simplifycfg.

I'm attaching good.ll and bad.ll which are the module before and after the structurizer runs, respectively.

### dn...@google.com (2024-05-17)

For good.ll, the loop info (dumped with `opt good.ll -passes='print<loops>'`) is:

```
Loop at depth 1 containing: %while.cond.i.i<header><latch>
Loop at depth 1 containing: %while.cond.i.23.i<header><latch>
Loop at depth 1 containing: %while.cond.i.37.i<header><latch>
Loop at depth 1 containing: %do.body.i<header>,%for.cond.i.i<exiting>,%"\01?f@@YAXXZ.exit.i",%for.cond.i.32.i<exiting>,%if.end.i,%sw.bb.10.i,%sw.default.i,%for.cond.i.18.i<exiting>,%do.cond.i<latch><exiting>

```

### dn...@google.com (2024-05-17)

I'm attaching a CFG dump with loop analysis annotations, and additionally the names of the basic blocks.

Block \*YAXXZ defines value %DerivFineX, and that's used in phis blocks %if.end.i and %for.cond.i.18.i
The %for.cond.i.18.i is a loop-exiting block.

From the description of the "RemoveUnstructuredExits" code [here](https://github.com/microsoft/DirectXShaderCompiler/blob/1658b068b50012e41eaf012db0761edbee76a1ea/lib/Transforms/Scalar/DxilRemoveUnstructuredLoopExits.cpp#L13) it tries to move logic in an exiting bock to after the loop exit. To do this it captures the exit condition, moves the logic int he exiting block to after the loop, and then conditions the moved code by the exit condition.

Unfortunately in the test case, the moved code includes an OpPhi that uses a value defined in a switch blcok inside the loop. By the time we move the code to after the loop, the dominance relation is broken on the incoming edge for the phi. That's the bug.

Inspecting the transform around the \*YAZZZ block ("\01?f@@YAXXZ.exit.i"), the before picture is this:

```
; this block defines the values
"\01?f@@YAXXZ.exit.i":                            ; preds = %for.cond.i.i
  %DerivFineX = call float @dx.op.unary.f32(i32 85, float %g.i.0.i0), !dbg !17
  %DerivFineX1 = call float @dx.op.unary.f32(i32 85, float %g.i.0.i1), !dbg !17
  %DerivFineX2 = call float @dx.op.unary.f32(i32 85, float %g.i.0.i2), !dbg !17
  %DerivFineX3 = call float @dx.op.unary.f32(i32 85, float %g.i.0.i3), !dbg !17
  %6 = getelementptr inbounds [2 x i32], [2 x i32]* %1, i32 0, i32 0, !dbg !18
  %7 = load i32, i32* %6, align 4, !dbg !18
  %8 = getelementptr [2 x i32], [2 x i32]* %1, i32 0, i32 %7, !dbg !19
  %9 = load i32, i32* %8, !dbg !19, !tbaa !20
  %cmp6.i = icmp eq i32 %9, 2, !dbg !24
  br i1 %cmp6.i, label %if.end.i, label %for.cond.i.32.i, !dbg !19

; this is an exiting block, because it branches to %while.cond.i37.i.preheader
; which is outside the loop.  
for.cond.i.32.i:                                  ; preds = %"\01?f@@YAXXZ.exit.i"
  br i1 true, label %while.cond.i.37.i.preheader, label %if.end.i, !dbg !25


```

Here's the same part, after the transform:

```
"\01?f@@YAXXZ.exit.i":                            ; preds = %for.cond.i.i
  %dx.struct_exit.prop = phi i1 [ true, %for.cond.i.i ]
  br i1 %dx.struct_exit.prop, label %dx.struct_exit.cond_end, label %dx.struct_exit.cond_body
  
dx.struct_exit.cond_body:                         ; preds = %"\01?f@@YAXXZ.exit.i"
  %DerivFineX = call float @dx.op.unary.f32(i32 85, float %g.i.0.i0), !dbg !16
  %DerivFineX1 = call float @dx.op.unary.f32(i32 85, float %g.i.0.i1), !dbg !16
  %DerivFineX2 = call float @dx.op.unary.f32(i32 85, float %g.i.0.i2), !dbg !16
  %DerivFineX3 = call float @dx.op.unary.f32(i32 85, float %g.i.0.i3), !dbg !16
  %6 = getelementptr inbounds [2 x i32], [2 x i32]* %1, i32 0, i32 0, !dbg !17
  %7 = load i32, i32* %6, align 4, !dbg !17
  %8 = getelementptr [2 x i32], [2 x i32]* %1, i32 0, i32 %7, !dbg !18
  %9 = load i32, i32* %8, !dbg !18, !tbaa !19
  %cmp6.i = icmp eq i32 %9, 2, !dbg !23
  br label %dx.struct_exit.cond_end, !dbg !18     
  
dx.struct_exit.cond_end:                          ; preds = %"\01?f@@YAXXZ.exit.i", %dx.struct_exit.cond_body
  %10 = phi i1 [ false, %"\01?f@@YAXXZ.exit.i" ], [ %cmp6.i, %dx.struct_exit.cond_body ]
  %11 = phi float [ 0.000000e+00, %"\01?f@@YAXXZ.exit.i" ], [ %DerivFineX3, %dx.struct_exit.cond_body ]
  %12 = phi float [ 0.000000e+00, %"\01?f@@YAXXZ.exit.i" ], [ %DerivFineX2, %dx.struct_exit.cond_body ]
  %13 = phi float [ 0.000000e+00, %"\01?f@@YAXXZ.exit.i" ], [ %DerivFineX1, %dx.struct_exit.cond_body ]
  %14 = phi float [ 0.000000e+00, %"\01?f@@YAXXZ.exit.i" ], [ %DerivFineX, %dx.struct_exit.cond_body ]
  br i1 %10, label %if.end.i, label %for.cond.i.32.i, !dbg !18
    
for.cond.i.32.i:                                  ; preds = %dx.struct_exit.cond_end
  %dx.struct_exit.prop9 = phi i1 [ %dx.struct_exit.prop, %dx.struct_exit.cond_end ]
  br label %if.end.i 

```

So we see that:

- Block "\01?f@@YAXXZ.exit.i" has been split:
- All its old core logic moved to new block dx.struct\_exit.cond\_body
  - Crucially this includes the definitions of values used later on in phis in distant nodes that the new node longer dominates!
- The only thing left is logic that decides whether to execute the new nested block. This is intrinsic to the purpose of this pass.
- Now that the definitions of %DerivFineX\* are tucked away in a conditionally executed block, they no longer dominate downstream blocks that need them. And hence the module is broken.

### dn...@google.com (2024-05-17)

I'm attaching a closeup of a portion of the post-transform PNG. I have a red arrow pointing at the block that now defines the value. It's conditionally executed, and therefore doesn't dominate the downstream blocks as needed.

### dn...@google.com (2024-05-17)

Inspecting the ReplaceUnstructuredLoopExits there looks like an iteration bug in the SkipBlockWithBranch function.

It is replacing uses of a value while it is iterating through those uses.
<https://github.com/microsoft/DirectXShaderCompiler/blob/1658b068b50012e41eaf012db0761edbee76a1ea/lib/Transforms/Scalar/DxilRemoveUnstructuredLoopExits.cpp#L330>

I rewrote the code to be simpler: collect the relevant uses, then change them. That fixed the bug.

### dn...@google.com (2024-05-17)

The patch to apply is at <https://paste.googleplex.com/6449676966690816>

### dn...@google.com (2024-05-22)

I posted a PR upstream which has the fix and a focusecd test.
<https://github.com/microsoft/DirectXShaderCompiler/pull/6644>

### dn...@google.com (2024-05-23)

The fix landed in upstream main.

Handing the rest of the shepherding to Antonio.

### am...@google.com (2024-05-30)

Am testing this to validate that it is indeed fixed.

- Testing on an official build, `Version 125.0.6422.78 (Official Build) (64-bit)` by opening the attached `indexCanPropagatePredecessorsForPHIs.html` does not reproduce the failure. This was only reproduced with an ASAN build of chromium.
- Testing on an ASAN build, `Version 126.0.6465.0 (Developer Build) (64-bit)`, opening `indexCanPropagatePredecessorsForPHIs.html` does reproduce the GPU process crash, as reported by OP.
- Testing on an ASAN build, `Version 127.0.6510.0 (Developer Build) (64-bit)`, opening `indexCanPropagatePredecessorsForPHIs.html` does **not** crash the GPU process, and in the developer window, we get the expected failure to compile output:

```
DXC compile failed with: hlsl.hlsl:36:43: warning: equality comparison with extraneous parentheses [-Wparentheses-equality]
      if ((tint_symbol_7[tint_symbol_7.x] == 2u)) {
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~
hlsl.hlsl:36:43: note: remove extraneous parentheses around the comparison to silence this warning
      if ((tint_symbol_7[tint_symbol_7.x] == 2u)) {
          ~                               ^    ~
hlsl.hlsl:36:43: note: use '=' to turn this equality comparison into an assignment
      if ((tint_symbol_7[tint_symbol_7.x] == 2u)) {
                                          ^~
                                          =
warning: Declared output SV_Target0 not fully written in shader. [-Winline-asm]
error: validation errors
hlsl.hlsl:63: error: Loop must have break.
Validation failed.


 - While calling [Device].CreateRenderPipeline([RenderPipelineDescriptor "render pipeline"]).

```

Since latest Canary is the same version as the ASAN build I tested above, `Version 127.0.6510.0 (Official Build) canary (64-bit)`, we can say that this is fixed in latest Canary.

- The upstream fix: <https://github.com/microsoft/DirectXShaderCompiler/pull/6644>
- DXC with fix roll into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/189760>
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

- The upstream fix: <https://github.com/microsoft/DirectXShaderCompiler/pull/6644>
- DXC with fix roll into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/189760>
- Dawn with fix roll into Chrome: <https://chromium-review.googlesource.com/c/chromium/src/+/5567994>

Note that the DXC fix will be cherry-picked to a custom branch in our DXC mirror, then updated in a Dawn custom branch for Chrome release.

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes.

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

Yes. As per [#comment30](https://issues.chromium.org/issues/339171223#comment30), test in the latest ASAN build of Chrome to see that the GPU process does not crash anymore.

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

Congratulations wgslfuzz! Thank you for your efforts in discovering yet another report of DXC GPU bug and reporting this issue to us!

### pe...@google.com (2024-06-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-06-10)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6478

commit 33051b084850a9b6b52f195651fab8f61843a4e2
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Mon Jun 10 10:52:30 2024

    Loop exit restructurizer: don't iterate over uses while mutating them (#6644)
    
    The SkipBlockWithBranch function does the following:
    - Splits the block into three blocks with an if-then-endif structure.
    - Moves most instructions from the original block into the "then" block
    - If any of those values are used outside the original block, they are
    propagated through newly-constructed phis in the 'endif' block.
    
    This algorithm had a bug where the uses of a value were being scanned
    while the uses were also being updated. In some cases a downstream
    out-of-block use could be skipped. That results in an invalid module
    because now the original definition is now in the 'then' block, which
    does not dominate the downstream out-of-block use.
    
    Add a test that demonstrates the problem.
    
    Bug: chromium:339171223
    Change-Id: Ia34fd7a2fe84de635289f7499772d11866a28e24
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5615350
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: dan sinclair <dsinclair@google.com>

M       lib/Transforms/Scalar/DxilRemoveUnstructuredLoopExits.cpp
A       tools/clang/test/DXC/Passes/DxilRemoveUnstructuredLoopExits/struct_exit_wrap_value_iteration_bug.ll

https://chromium-review.googlesource.com/5615350


### ap...@google.com (2024-06-10)

Project: dawn
Branch: chromium/6478

commit c68406f94723e5ef8f541900899ca9e0ef70f1b7
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Mon Jun 10 16:17:43 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:339171223
    Change-Id: I7478a66c95765593fe71c91bbb8ed1d567749088
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/192682
    Reviewed-by: James Price <jrprice@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/192682


### am...@google.com (2024-06-10)

This has been [merged to M126](https://chromium.googlesource.com/chromium/src.git/+/2b6450ea972086f5c69b9f4472ad641d4a792c02).

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


### pe...@google.com (2024-09-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in the GPU process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339171223)*
