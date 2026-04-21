# GPU process crash via WebGPU shader - UAF in RecursivelyDeleteTriviallyDeadInstructions at Transforms\Utils\Local.cpp:368

| Field | Value |
|-------|-------|
| **Issue ID** | [345993680](https://issues.chromium.org/issues/345993680) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint, Internals>GPU>Dawn |
| **Platforms** | Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | dn...@google.com |
| **Created** | 2024-06-09 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this triggers an UAF inside the hlsl compiler.

##### VERSION

Chrome Version: Pre-compiled ASAN Chromium 127.0.6528.0 (Developer Build) (64-bit)   

Operating System: Win10 Build 19045.4291

##### REPRODUCTION CASE

Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process. Note that the crash may NOT manifest on machines which support the 6.6 shader model.

Reproducing the issue stand-alone on Linux also possible:

1. Compile the standalone.wgsl with tint (commit d9c2ed367198c08e7c56d5eeb93dcea25f5ef0d5) to hlsl via `./tint standalone.wgsl -o standalone.hlsl`. I also attached standalone.hlsl, but you should get the very same file when compiling standalone.wgsl yourself
2. Compile the hlsl with dxc (commit 1d196655b615fdb15afcd457c1466d9094947b02): `./dxc-3.7 standalone.hlsl -T ps_6_2 -HV 2018`. This should trigger an ASAN violation. Setting the shader model to `ps_6_6` prevents the UAF.

I verified this bug is not fixed by the upstream patches for [bug 344639860](https://issues.chromium.org/issues/344639860) and [bug 342545100](https://issues.chromium.org/issues/342545100).

##### Attached:

- html that triggers an ASAN violation in chromium
- wgsl for producing the hlsl shader
- the hlsl shader
- asan log file

```
[5960:1376:0608/235645.836:WARNING:chrome_main_delegate.cc(743)] This is Chrome version 127.0.6528.0 (not a warning)
[5960:5696:0608/235646.226:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[5960:6188:0608/235646.305:ERROR:sandbox_win.cc(840)] Sandbox cannot access executable. Check filesystem permissions are valid. See https://bit.ly/31yqMJR.: Access is denied. (0x5)
[5960:1376:0608/235646.445:WARNING:account_consistency_mode_manager.cc(77)] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
[5960:1376:0608/235646.524:WARNING:browser_management_service.cc(128)] EnterpriseLogoUrl fetch failed with error code -1 and MIME type 
=================================================================
==3936==ERROR: AddressSanitizer: heap-use-after-free on address 0x12701f464cc0 at pc 0x7ffc75a2c76e bp 0x0072d47fb7c0 sp 0x0072d47fb808
WRITE of size 8 at 0x12701f464cc0 thread T0
==3936==WARNING: Failed to use and restart external symbolizer!
==3936==*** WARNING: Failed to initialize DbgHelp!              ***
==3936==*** Most likely this means that the app is already      *** 
==3936==*** using DbgHelp, possibly with incompatible flags.    *** 
==3936==*** Due to technical reasons, symbolization might crash *** 
==3936==*** or produce wrong results.                           ***
    #0 0x7ffc75a2c76d in llvm::RecursivelyDeleteTriviallyDeadInstructions C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\Local.cpp:368
    #1 0x7ffc75a2d1e0 in llvm::RecursivelyDeleteDeadPHINode C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\Local.cpp:422
    #2 0x7ffc75ac4cae in llvm::DeleteDeadPHIs C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\BasicBlockUtils.cpp:103
    #3 0x7ffc75090926 in `anonymous namespace'::IndVarSimplify::runOnLoop C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\IndVarSimplify.cpp:2090
    #4 0x7ffc75c68d5b in llvm::LPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\LoopPass.cpp:251
    #5 0x7ffc73e28084 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #6 0x7ffc75a8fe5c in `anonymous namespace'::CGPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\IPA\CallGraphSCCPass.cpp:491
    #7 0x7ffc73e297d5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #8 0x7ffc73e32b6c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:781
    #9 0x7ffc73840921 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #10 0x7ffc73f5e5c1 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #11 0x7ffc7383b612 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #12 0x7ffc73848de3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #13 0x7ffc73726c13 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #14 0x7ffc7948231a in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #15 0x7ffc794e57ee in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #16 0x7ffc795872ad in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:377
    #17 0x7ffc79570dc5 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:365
    #18 0x7ffc7939cb70 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #19 0x7ffc792f1897 in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2191
    #20 0x7ffc792f127a in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1510
    #21 0x7ffc9bc1b63d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #22 0x7ffc9b67deb4 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606    
    #23 0x7ffc9b682d91 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #24 0x7ffc97879782 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1031
    #25 0x7ffc97879bd5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1938
    #26 0x7ffc9786df01 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1883
    #27 0x7ffc8ba10d63 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:231
    #28 0x7ffc87f4e96c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:506
    #29 0x7ffc87f4d413 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:154
    #30 0x7ffc8ba2ec5a in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:930
    #31 0x7ffc8ba3fd3a in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&,unsigned long long &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams>,unsigned long long>,void ()>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams>,unsigned long long>,0,1,2> C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1067
    #32 0x7ffc8b0b634d in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:730
    #33 0x7ffc8b0b4718 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:655
    #34 0x7ffc8b0b78a5 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #35 0x7ffc85dec820 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #36 0x7ffc89eda95e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:484
    #37 0x7ffc89ed984a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346
    #38 0x7ffc89f0f40e in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #39 0x7ffc89edc59c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:654
    #40 0x7ffc85e362a0 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #41 0x7ffc88feffa9 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:430
    #42 0x7ffc8455a162 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:784
    #43 0x7ffc8455c910 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1156
    #44 0x7ffc845580fd in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #45 0x7ffc84558bed in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #46 0x7ffc76d61601 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #47 0x7ff6626d43a5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #48 0x7ff6626d1db2 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #49 0x7ff662ac3b63 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #50 0x7ffcf9517343 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017343)
    #51 0x7ffcfa8a26b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)

0x12701f464cc0 is located 64 bytes inside of 120-byte region [0x12701f464c80,0x12701f464cf8)
freed by thread T0 here:
    #0 0x7ff6627ad26d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffc73a68c3b in llvm::ICmpInst::~ICmpInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:1093
    #2 0x7ffc74ccd8b1 in llvm::iplist<llvm::Instruction,llvm::ilist_traits<llvm::Instruction> >::clear C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\ADT\ilist.h:563
    #3 0x7ffc74ccd352 in llvm::BasicBlock::~BasicBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:91
    #4 0x7ffc74cd11ef in llvm::BasicBlock::~BasicBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:70
    #5 0x7ffc74ccdce8 in llvm::BasicBlock::eraseFromParent C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:104
    #6 0x7ffc750ede21 in `anonymous namespace'::LoopDeletion::runOnLoop C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\LoopDeletion.cpp:251
    #7 0x7ffc75c68d5b in llvm::LPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\LoopPass.cpp:251
    #8 0x7ffc73e28084 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #9 0x7ffc75a8fe5c in `anonymous namespace'::CGPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\IPA\CallGraphSCCPass.cpp:491
    #10 0x7ffc73e297d5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #11 0x7ffc73e32b6c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:781
    #12 0x7ffc73840921 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #13 0x7ffc73f5e5c1 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #14 0x7ffc7383b612 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #15 0x7ffc73848de3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #16 0x7ffc73726c13 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #17 0x7ffc7948231a in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #18 0x7ffc794e57ee in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #19 0x7ffc795872ad in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:377
    #20 0x7ffc79570dc5 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:365
    #21 0x7ffc7939cb70 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #22 0x7ffc792f1897 in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2191
    #23 0x7ffc792f127a in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1510
    #24 0x7ffc9bc1b63d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #25 0x7ffc9b67deb4 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #26 0x7ffc9b682d91 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #27 0x7ffc97879782 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1031

previously allocated by thread T0 here:
    #0 0x7ff6627ad36d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffc7624655e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffc74ccc411 in llvm::User::operator new C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:96
    #3 0x7ffc74c05b22 in llvm::BinaryOperator::cloneImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Instructions.cpp:3460
    #4 0x7ffc74c0f052 in llvm::Instruction::clone C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Instruction.cpp:543
    #5 0x7ffc74f21a11 in `anonymous namespace'::PruningFunctionCloner::CloneBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\CloneFunction.cpp:349
    #6 0x7ffc74f1e2c6 in llvm::CloneAndPruneIntoFromInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\CloneFunction.cpp:511
    #7 0x7ffc74f23b85 in llvm::CloneAndPruneFunctionInto C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\CloneFunction.cpp:720
    #8 0x7ffc7618fb54 in llvm::InlineFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\InlineFunction.cpp:1046
    #9 0x7ffc75a89b2b in llvm::Inliner::runOnSCC C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\IPO\Inliner.cpp:574
    #10 0x7ffc75a900af in `anonymous namespace'::CGPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\IPA\CallGraphSCCPass.cpp:491
    #11 0x7ffc73e297d5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #12 0x7ffc73e32b6c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:781
    #13 0x7ffc73840921 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #14 0x7ffc73f5e5c1 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #15 0x7ffc7383b612 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #16 0x7ffc73848de3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #17 0x7ffc73726c13 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #18 0x7ffc7948231a in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #19 0x7ffc794e57ee in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #20 0x7ffc795872ad in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:377
    #21 0x7ffc79570dc5 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:365
    #22 0x7ffc7939cb70 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #23 0x7ffc792f1897 in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2191
    #24 0x7ffc792f127a in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1510
    #25 0x7ffc9bc1b63d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #26 0x7ffc9b67deb4 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #27 0x7ffc9b682d91 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\Local.cpp:368 in llvm::RecursivelyDeleteTriviallyDeadInstructions
Shadow bytes around the buggy address:
  0x12701f464a00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x12701f464a80: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
  0x12701f464b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12701f464b80: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x12701f464c00: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
=>0x12701f464c80: fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fa
  0x12701f464d00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x12701f464d80: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
  0x12701f464e00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12701f464e80: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x12701f464f00: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
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

==3936==ADDITIONAL INFO

==3936==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffc8b0b489a in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:671
    #1 0x7ffc8b0b489a in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:671
    #2 0x7ffc8b0b489a in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:671
    #3 0x7ffc8b0aded0 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:473


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==3936==END OF ADDITIONAL INFO
==3936==ABORTING
[5960:1376:0609/000547.600:ERROR:gpu_process_host.cc(1007)] GPU process exited unexpectedly: exit_code=1
[5960:1376:0609/000547.616:WARNING:gpu_process_host.cc(1443)] The GPU process has crashed 1 time(s)
[5960:1376:0609/000547.648:INFO:CONSOLE(0)] "A valid external Instance reference no longer exists.", source: file://vboxsvr/shared/indexComputeExitCountExhaustively.html (0)
[5960:1376:0609/000548.351:WARNING:gpu_process_host.cc(1029)] Reinitialized the GPU process after a crash. The reported initialization time was 197 ms

```

## Attachments

- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 1.1 KB)
- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 955 B)
- [asanComputeExitCountExhaustively](attachments/asanComputeExitCountExhaustively) (application/octet-stream, 22.6 KB)
- [indexComputeExitCountExhaustively.html](attachments/indexComputeExitCountExhaustively.html) (text/html, 3.9 KB)

## Timeline

### pe...@google.com (2024-06-11)

Setting milestone because of s0/s1 severity.

### am...@google.com (2024-06-11)

Reproduced ASAN fauilure on ToT (1c7cb4ffb89107ce2aea583b2387f88225a4a634). As specified, does not reproduce with `-T ps_6_6`, but does with any shader model less than 6.5.

In a debug build, we get the following assert:

```
dxc: /home/amaiorano/src/external/DirectXShaderCompiler/lib/Transforms/Scalar/IndVarSimplify.cpp:2093: virtual bool (anonymous namespace)::IndVarSimplify::runOnLoop(Loop *, LPPassManager &): Assertion `L->isLCSSAForm(*DT) && "Indvars did not leave the loop in lcssa form!"' failed.
Aborted

```

Needs further investigation.

### dn...@google.com (2024-06-13)

Filed a PR upstream: <https://github.com/microsoft/DirectXShaderCompiler/pull/6695>

Induction variable simplification (indvars) tries to rewrite exit values; these appear as phi nodes in loop exit blocks. If the replacement for the phi is still in the loop, then that would break the LCSSA property. Don't do that.

### dn...@google.com (2024-06-13)

With the fix, the compilation of the original HLSL sample errors out with "no break from loop"

### dn...@google.com (2024-06-18)

Fix landed upstream.

That rolled into Dawn with: <https://dawn.googlesource.com/dawn/+/9ab81a997039106f60a1589fbd9b477cb263548a>

### dn...@google.com (2024-06-18)

That Dawn commit rolled into Chromium with: <https://dawn.googlesource.com/dawn/+/refs/heads/chromium/6544>

### dn...@google.com (2024-06-18)

Confirmed broken in an asan Win build 128.0.6543.0

Confirmed fixed in an asan Win build 128.0.6544.0

### pe...@google.com (2024-06-19)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### dn...@google.com (2024-06-19)

1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://dawn-review.googlesource.com/c/dawn/+/194002>

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes

3. Does this fix pose any potential non-verifiable stability risks?

No

4. Does this fix pose any known compatibility risks?

No

5. Does it require manual verification by the test team? If so, please describe required testing.

Yes. In Chrome, open indexComputeExitCountExhaustively.html attached to this bug.
If the bug is present, the Chrome tab will flash black, in response to crashing the GPU process.
If the bug is absent, the tab will remain white.

### am...@chromium.org (2024-06-20)

merges approved for <https://dawn-review.googlesource.com/c/dawn/+/194002>; please merge this fix to M127 (beta) / branch 6533 and M126 Stable / branch 6478 as soon as possible, by before 10am Pacific tomorrow so this fix can be included next week's M126 Stable update

### ap...@google.com (2024-06-20)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6533

commit 2bdff357219e92e086ec95b6e7d8e3a1fc9f9825
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Jun 20 14:04:42 2024

    indvars: don't replace a phi when that breaks LCSSA (#6695)
    
    Induction variable simplification (indvars) tries to rewrite exit
    values; these appear as phi nodes in loop exit blocks. If the
    replacement for the phi is still in the loop, then that would break the
    LCSSA property. Don't do that.
    
    Add a test for this.
    
    Bug: chromium:345993680
    Change-Id: I3d81eca072e7e170e13ca89e09d046015788335d
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5645926
    Reviewed-by: dan sinclair <dsinclair@google.com>
    Reviewed-by: James Price <jrprice@google.com>

M       lib/Transforms/Scalar/IndVarSimplify.cpp
A       test/HLSL/passes/indvars/preserve-phi-when-replacement-is-in-loop.ll

https://chromium-review.googlesource.com/5645926


### ap...@google.com (2024-06-20)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6478

commit 771e74ab497dcaa82b67c60bee605fe44a318de0
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Jun 20 14:02:42 2024

    indvars: don't replace a phi when that breaks LCSSA (#6695)
    
    Induction variable simplification (indvars) tries to rewrite exit
    values; these appear as phi nodes in loop exit blocks. If the
    replacement for the phi is still in the loop, then that would break the
    LCSSA property. Don't do that.
    
    Add a test for this.
    
    Bug: chromium:345993680
    Change-Id: Ib2330afa3c6f47373cb4336cfd00e851044fea3a
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5645925
    Reviewed-by: dan sinclair <dsinclair@chromium.org>
    Reviewed-by: James Price <jrprice@google.com>

M       lib/Transforms/Scalar/IndVarSimplify.cpp
A       test/HLSL/passes/indvars/preserve-phi-when-replacement-is-in-loop.ll

https://chromium-review.googlesource.com/5645925


### ap...@google.com (2024-06-20)

Project: dawn
Branch: chromium/6533

commit cabde7e7b03dd21f672c6b92b17ea7915648e6f6
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Jun 20 18:29:51 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:345993680
    Change-Id: I71f984ba28d26b4d1f43a9a11b96f119e5c34f60
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/194995
    Reviewed-by: James Price <jrprice@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/194995


### ap...@google.com (2024-06-20)

Project: dawn
Branch: chromium/6478

commit 46813578fd64e9e89aac914be3f371306f2cc7b8
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Jun 20 18:29:26 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:345993680
    Change-Id: I98923c71d6e3a44cb061f582a80ba18a6075a6d6
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/194994
    Reviewed-by: dan sinclair <dsinclair@chromium.org>
    Reviewed-by: James Price <jrprice@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/194994


### am...@google.com (2024-06-20)

Fix has been merged into Chromium:

- [M126](https://chromium.googlesource.com/chromium/src.git/+/97616db5cf7eaa1c68e78b6d2112a0b45078b662)
- [M127](https://chromium.googlesource.com/chromium/src.git/+/08785c2dc830354b67faba03c5cbae7c101bbfda)

### sp...@google.com (2024-06-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
memory corruption in the GPU process 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-26)

Congratulations on another one! Thanks for your fuzzing efforts and reporting this issue to us -- great work!

### pe...@google.com (2024-09-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> memory corruption in the GPU process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/345993680)*
