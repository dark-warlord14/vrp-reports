# GPU process crash via WebGPU shader - UAF in ScalarizePreciseVectorAlloca at DxilConditionalMem2Reg.cpp:275

| Field | Value |
|-------|-------|
| **Issue ID** | [365254285](https://issues.chromium.org/issues/365254285) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Windows |
| **Reporter** | a7...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-09-08 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this triggers an UAF inside the hlsl compiler.

##### VERSION

Chrome Version: Pre-compiled ASAN Chromium 130.0.6706.0 (Developer Build) (64-bit)   

Operating System: Win11 Build 22631

##### REPRODUCTION CASE

Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process. The corresponding ASAN crash is generated:

```
[10524:6416:0908/153414.580:WARNING:chrome_main_delegate.cc(743)] This is Chrome version 130.0.6706.0 (not a warning)
[10524:14008:0908/153414.764:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
=================================================================
==2848==ERROR: AddressSanitizer: heap-use-after-free on address 0x1219260ecfe8 at pc 0x7ffbe7f647d7 bp 0x0065eb7fbb80 sp 0x0065eb7fbbc8
READ of size 8 at 0x1219260ecfe8 thread T0
==2848==WARNING: Failed to use and restart external symbolizer!
==2848==*** WARNING: Failed to initialize DbgHelp!              ***
==2848==*** Most likely this means that the app is already      ***
==2848==*** using DbgHelp, possibly with incompatible flags.    ***
==2848==*** Due to technical reasons, symbolization might crash ***
==2848==*** or produce wrong results.                           ***
    #0 0x7ffbe7f647d6 in DxilConditionalMem2Reg::ScalarizePreciseVectorAlloca C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilConditionalMem2Reg.cpp:275
    #1 0x7ffbe7f5f696 in DxilConditionalMem2Reg::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilConditionalMem2Reg.cpp:503
    #2 0x7ffbe6c50229 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #3 0x7ffbe6c50dbe in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #4 0x7ffbe6c51ded in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #5 0x7ffbe6c5b8ec in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:783
    #6 0x7ffbe65c55fb in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:192
    #7 0x7ffbe6d9b9d1 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #8 0x7ffbe65bff31 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:808
    #9 0x7ffbe65ce64c in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #10 0x7ffbe64a8030 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:974
    #11 0x7ffbef15e3b7 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:370
    #12 0x7ffbef1c9669 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #13 0x7ffbef275291 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:385
    #14 0x7ffbef25f723 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:365
    #15 0x7ffbef06aaa0 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #16 0x7ffbeefb9c9b in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2244
    #17 0x7ffbeefb9687 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1556
    #18 0x7ffc1352037d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:469
    #19 0x7ffc12f0ee64 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:716
    #20 0x7ffc12f1574c in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:2056
    #21 0x7ffc0f0cd552 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1043
    #22 0x7ffc0f0cd9b2 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1950
    #23 0x7ffc0f0c1901 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1895
    #24 0x7ffc02e07ac3 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:263
    #25 0x7ffbfed3401a in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:497
    #26 0x7ffbfed32f0f in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:153
    #27 0x7ffc02e25d7e in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:942
    #28 0x7ffc02e36fa0 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void (gpu::FenceSyncReleaseDelegate *)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #29 0x7ffc02408811 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)> &&,gpu::FenceSyncReleaseDelegate *>,base::internal::BindState<0,1,1,base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>,base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate,base::unretained_traits::MayNotDangle,0> >,void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>,std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate,base::unretained_traits::MayNotDangle,0> >,0> C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1067
    #30 0x7ffbfe034a03 in gpu::Scheduler::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:667
    #31 0x7ffbfe032735 in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:591
    #32 0x7ffbfe035378 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::Sequence::*const &)(),gpu::Scheduler::Sequence *>,base::internal::BindState<1,1,0,void (gpu::Scheduler::Sequence::*)(),base::internal::UnretainedWrapper<gpu::Scheduler::Sequence,base::unretained_traits::MayNotDangle,0> >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:987
    #33 0x7ffbfc9b6ec0 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #34 0x7ffc010d445d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:470
    #35 0x7ffc010d3209 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:332
    #36 0x7ffc01117c5e in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #37 0x7ffc010d612f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:640
    #38 0x7ffbfca1106e in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #39 0x7ffc0004412b in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:434
    #40 0x7ffbfade7271 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:795
    #41 0x7ffbfade94cf in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1160
    #42 0x7ffbfadddad5 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:356
    #43 0x7ffbfadde67d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:369
    #44 0x7ffbec7216b0 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:231
    #45 0x7ff7d48743ed in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201
    #46 0x7ff7d487200c in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351
    #47 0x7ff7d4c968cb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #48 0x7ffc8fef257c in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x18001257c)
    #49 0x7ffc90f4af27 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005af27)

0x1219260ecfe8 is located 72 bytes inside of 96-byte region [0x1219260ecfa0,0x1219260ed000)
freed by thread T0 here:
    #0 0x7ff7d495181d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffbe688c71b in llvm::ICmpInst::~ICmpInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:1093
    #2 0x7ffbe7b70df2 in llvm::Instruction::eraseFromParent C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Instruction.cpp:71
    #3 0x7ffbe7f63ebe in DxilConditionalMem2Reg::ScalarizePreciseVectorAlloca C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilConditionalMem2Reg.cpp:325
    #4 0x7ffbe7f5f696 in DxilConditionalMem2Reg::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilConditionalMem2Reg.cpp:503
    #5 0x7ffbe6c50229 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #6 0x7ffbe6c50dbe in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #7 0x7ffbe6c51ded in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #8 0x7ffbe6c5b8ec in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:783
    #9 0x7ffbe65c55fb in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:192
    #10 0x7ffbe6d9b9d1 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #11 0x7ffbe65bff31 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:808
    #12 0x7ffbe65ce64c in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #13 0x7ffbe64a8030 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:974
    #14 0x7ffbef15e3b7 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:370
    #15 0x7ffbef1c9669 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #16 0x7ffbef275291 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:385
    #17 0x7ffbef25f723 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:365
    #18 0x7ffbef06aaa0 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #19 0x7ffbeefb9c9b in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2244
    #20 0x7ffbeefb9687 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1556
    #21 0x7ffc1352037d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:469
    #22 0x7ffc12f0ee64 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:716
    #23 0x7ffc12f1574c in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:2056
    #24 0x7ffc0f0cd552 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1043
    #25 0x7ffc0f0cd9b2 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1950
    #26 0x7ffc0f0c1901 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1895
    #27 0x7ffc02e07ac3 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:263

previously allocated by thread T0 here:
    #0 0x7ff7d495191d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffbe943d62e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffbe7da3506 in llvm::User::operator new C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:96
    #3 0x7ffbe7b601cb in llvm::CastInst::Create C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Instructions.cpp:2271
    #4 0x7ffbe688c942 in llvm::IRBuilder<1,llvm::ConstantFolder,llvm::IRBuilderDefaultInserter<1> >::CreateCast C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\IRBuilder.h:1336
    #5 0x7ffbe7e75dfc in `anonymous namespace'::SROA_Helper::RewriteForScalarRepl C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:2899
    #6 0x7ffbe7e658d7 in `anonymous namespace'::SROA_Helper::DoScalarReplacement C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:3060
    #7 0x7ffbe7e48bca in `anonymous namespace'::SROAGlobalAndAllocas C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:1879
    #8 0x7ffbe7e34ba1 in `anonymous namespace'::SROA_Parameter_HLSL::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:4372
    #9 0x7ffbe6c51ded in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #10 0x7ffbe6c5b8ec in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:783
    #11 0x7ffbe65c55fb in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:192
    #12 0x7ffbe6d9b9d1 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #13 0x7ffbe65bff31 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:808
    #14 0x7ffbe65ce64c in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #15 0x7ffbe64a8030 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:974
    #16 0x7ffbef15e3b7 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:370
    #17 0x7ffbef1c9669 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #18 0x7ffbef275291 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:385
    #19 0x7ffbef25f723 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:365
    #20 0x7ffbef06aaa0 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #21 0x7ffbeefb9c9b in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2244
    #22 0x7ffbeefb9687 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1556
    #23 0x7ffc1352037d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:469
    #24 0x7ffc12f0ee64 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:716
    #25 0x7ffc12f1574c in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:2056
    #26 0x7ffc0f0cd552 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1043
    #27 0x7ffc0f0cd9b2 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1950

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilConditionalMem2Reg.cpp:275 in DxilConditionalMem2Reg::ScalarizePreciseVectorAlloca
Shadow bytes around the buggy address:
  0x1219260ecd00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1219260ecd80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1219260ece00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1219260ece80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1219260ecf00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
=>0x1219260ecf80: fa fa f7 fa fd fd fd fd fd fd fd fd fd[fd]fd fd
  0x1219260ed000: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1219260ed080: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1219260ed100: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x1219260ed180: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x1219260ed200: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
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

==2848==ADDITIONAL INFO

==2848==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffbfe032c9c in gpu::Scheduler::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:607
    #1 0x7ffbfe02e295 in gpu::Scheduler::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:409


Command line: `"C:\Users\user\Desktop\chrome\chrome.exe" --type=gpu-process --string-annotations=is-enterprise-managed=no --no-pre-read-main-dll --start-stack-profiler --gpu-preferences=UAAAAAAAAADgAAAEAAAAAAAAAAAAAAAAAABgAAMAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --metrics-shmem-handle=1960,i,9350606658359399770,7748648325109262653,262144 --field-trial-handle=2072,i,9048101244650392040,14828032373139287594,262144 --variations-seed-version --enable-logging=handle --log-file=2076 --mojo-platform-channel-handle=1904 /prefetch:2`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==2848==END OF ADDITIONAL INFO
==2848==ABORTING
[10524:6416:0908/153811.998:ERROR:gpu_process_host.cc(982)] GPU process exited unexpectedly: exit_code=1
[10524:6416:0908/153811.998:WARNING:gpu_process_host.cc(1416)] The GPU process has crashed 1 time(s)

```

Reproducing the issue stand-alone on Linux also possible:

1. Compile the standalone.wgsl with tint (commit 40cf7fd7bc06f871fc5e482338dffa3a8ba3acfb) to hlsl via `./tint standalone.wgsl -o standalone.hlsl`. I also attached standalone.hlsl, but you should get the very same file when compiling standalone.wgsl yourself
2. Compile the hlsl with dxc (commit 937c8c88112398b0628c53c1ca4148954a11f7fd): `./dxc-3.7 standalone.hlsl -T vs_6_2 -opt-disable structurize-loop-exits-for-unroll -HV 2018`.

##### Attached:

- html that triggers an ASAN violation in chromium
- standalone.wgsl for producing the hlsl shader
- standalone.hlsl for reproducing the crash in dxc

## Attachments

- [indexScalarizePreciseVectorAlloca.html](attachments/indexScalarizePreciseVectorAlloca.html) (text/html, 2.6 KB)
- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 147 B)
- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 349 B)

## Timeline

### a7...@gmail.com (2024-09-08)

I'm in contact with a person at MSFT working on GPU security, if you don't mind I'd like to add him to the issue.

### aj...@google.com (2024-09-08)

Yes, please CC them to this issue.

### aj...@google.com (2024-09-08)

I'm not able to repro this myself but passing to the webgpu team for further investigation:-

```
[15236:14232:0908/130451.354:ERROR:gpu_process_host.cc(982)] GPU process exited unexpectedly: exit_code=1
Created TensorFlow Lite XNNPACK delegate for CPU.
Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#141 is a dynamic-sized tensor).
[15236:14232:0908/130514.896:ERROR:gpu_process_host.cc(982)] GPU process exited unexpectedly: exit_code=1
[21292:17032:0908/130526.042:ERROR:command_buffer_proxy_impl.cc(131)] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.
[15236:14232:0908/130526.095:ERROR:gpu_process_host.cc(982)] GPU process exited unexpectedly: exit_code=1

```

### aj...@google.com (2024-09-08)

Apologies - this does repro and the log goes into the logfile:-

```
[21808:22176:0908/131027.432:VERBOSE1:first_party_sets_component_installer.cc(44)] Received Related Website Sets
    #0 0x7ffd88b159a7 in DxilConditionalMem2Reg::ScalarizePreciseVectorAlloca D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilConditionalMem2Reg.cpp:275
    #1 0x7ffd88b0f2cc in DxilConditionalMem2Reg::runOnFunction D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilConditionalMem2Reg.cpp:503
    #2 0x7ffd8703399e in llvm::FPPassManager::runOnFunction D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #3 0x7ffd8703459e in llvm::FPPassManager::runOnModule D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #4 0x7ffd8703596d in llvm::legacy::PassManagerImpl::run D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #5 0x7ffd870dd0a2 in clang::EmitBackendOutput D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:783
    #6 0x7ffd867d0dc1 in clang::BackendConsumer::HandleTranslationUnit D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:192
    #7 0x7ffd872946fe in clang::ParseAST D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #8 0x7ffd867c9d51 in clang::CodeGenAction::ExecuteAction D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:808
    #9 0x7ffd867dcc43 in clang::FrontendAction::Execute D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #10 0x7ffd8665a129 in DxcCompiler::Compile D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:974
    #11 0x7ffd9e579bd9 in dawn::native::d3d::CompileShader D:\chromium\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:370
    #12 0x7ffd9e61b562 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> D:\chromium\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #13 0x7ffd9e706078 in dawn::native::d3d12::ShaderModule::Compile D:\chromium\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:385
    #14 0x7ffd9e6e6856 in dawn::native::d3d12::RenderPipeline::InitializeImpl D:\chromium\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:365
    #15 0x7ffd9e4225ab in dawn::native::PipelineBase::Initialize D:\chromium\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #16 0x7ffd9e33cef3 in dawn::native::DeviceBase::CreateRenderPipeline D:\chromium\src\third_party\dawn\src\dawn\native\Device.cpp:2244
    #17 0x7ffd9e33c6a4 in dawn::native::DeviceBase::APICreateRenderPipeline D:\chromium\src\third_party\dawn\src\dawn\native\Device.cpp:1556
    #18 0x7ffdccdd34b9 in dawn::wire::server::Server::DoDeviceCreateRenderPipeline D:\chromium\src\out\asan\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:469
    #19 0x7ffdcc63cd42 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline D:\chromium\src\out\asan\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:716
    #20 0x7ffdcc6462c8 in dawn::wire::server::Server::HandleCommandsImpl D:\chromium\src\out\asan\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:2056
    #21 0x7ffdc791398f in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1043
    #22 0x7ffdc7913e5f in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1950
    #23 0x7ffdc790437a in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1895
    #24 0x7ffdb7dd5f40 in gpu::CommandBufferService::Flush D:\chromium\src\gpu\command_buffer\service\command_buffer_service.cc:263
    #25 0x7ffdb2d88d85 in gpu::CommandBufferStub::OnAsyncFlush D:\chromium\src\gpu\ipc\service\command_buffer_stub.cc:497
    #26 0x7ffdb2d87e81 in gpu::CommandBufferStub::ExecuteDeferredRequest D:\chromium\src\gpu\ipc\service\command_buffer_stub.cc:153
    #27 0x7ffdb7dfbb3e in gpu::GpuChannel::ExecuteDeferredRequest D:\chromium\src\gpu\ipc\service\gpu_channel.cc:942
    #28 0x7ffdb7e0f3b9 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void (gpu::FenceSyncReleaseDelegate *)>::RunOnce D:\chromium\src\base\functional\bind_internal.h:980
    #29 0x7ffdb7248b66 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)> &&,gpu::FenceSyncReleaseDelegate *>,base::internal::BindState<0,1,1,base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>,base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate,base::unretained_traits::MayNotDangle,0> >,void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>,std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate,base::unretained_traits::MayNotDangle,0> >,0> D:\chromium\src\base\functional\bind_internal.h:1067
    #30 0x7ffdb1f5da8c in gpu::Scheduler::ExecuteSequence D:\chromium\src\gpu\command_buffer\service\scheduler.cc:667
    #31 0x7ffdb1f5b0bc in gpu::Scheduler::RunNextTask D:\chromium\src\gpu\command_buffer\service\scheduler.cc:591
    #32 0x7ffdb1f5f679 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(),gpu::Scheduler *>,base::internal::BindState<1,1,0,void (gpu::Scheduler::*)(),base::internal::UnretainedWrapper<gpu::Scheduler,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce D:\chromium\src\base\functional\bind_internal.h:980
    #33 0x7ffdb0298b50 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task_annotator.cc:203
    #34 0x7ffdb59d1240 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:470
    #35 0x7ffdb59cfa9a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:332
    #36 0x7ffdb5a2733f in base::MessagePumpDefault::Run D:\chromium\src\base\message_loop\message_pump_default.cc:40
    #37 0x7ffdb59d3393 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:640
    #38 0x7ffdb032a259 in base::RunLoop::Run D:\chromium\src\base\run_loop.cc:134
    #39 0x7ffdb44e17db in content::GpuMain D:\chromium\src\content\gpu\gpu_main.cc:434
    #40 0x7ffdade39c48 in content::RunOtherNamedProcessTypeMain D:\chromium\src\content\app\content_main_runner_impl.cc:795
    #41 0x7ffdade3cd08 in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content_main_runner_impl.cc:1160
    #42 0x7ffdade2dd7c in content::RunContentProcess D:\chromium\src\content\app\content_main.cc:331
    #43 0x7ffdade2e4ce in content::ContentMain D:\chromium\src\content\app\content_main.cc:344
    #44 0x7ffd9ad417f1 in ChromeMain D:\chromium\src\chrome\app\chrome_main.cc:231
    #45 0x7ff677804ade in MainDllLoader::Launch D:\chromium\src\chrome\app\main_dll_loader_win.cc:201
    #46 0x7ff67780242b in main D:\chromium\src\chrome\app\chrome_exe_main_win.cc:351
    #47 0x7ff677d5852b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #48 0x7ffe3f0b257c in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x18001257c)
    #49 0x7ffe3f6aaf27 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005af27)

0x12530f65c6a0 is located 96 bytes inside of 120-byte region [0x12530f65c640,0x12530f65c6b8)
freed by thread T0 here:
    #0 0x7ff67791d12d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffd88575c30 in llvm::StoreInst::~StoreInst D:\chromium\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:316
    #2 0x7ffd885772d3 in llvm::Instruction::eraseFromParent D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\Instruction.cpp:71
    #3 0x7ffd88b1565f in DxilConditionalMem2Reg::ScalarizePreciseVectorAlloca D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilConditionalMem2Reg.cpp:316
    #4 0x7ffd88b0f2cc in DxilConditionalMem2Reg::runOnFunction D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilConditionalMem2Reg.cpp:503
    #5 0x7ffd8703399e in llvm::FPPassManager::runOnFunction D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #6 0x7ffd8703459e in llvm::FPPassManager::runOnModule D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #7 0x7ffd8703596d in llvm::legacy::PassManagerImpl::run D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #8 0x7ffd870dd0a2 in clang::EmitBackendOutput D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:783
    #9 0x7ffd867d0dc1 in clang::BackendConsumer::HandleTranslationUnit D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:192
    #10 0x7ffd872946fe in clang::ParseAST D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #11 0x7ffd867c9d51 in clang::CodeGenAction::ExecuteAction D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:808
    #12 0x7ffd867dcc43 in clang::FrontendAction::Execute D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #13 0x7ffd8665a129 in DxcCompiler::Compile D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:974
    #14 0x7ffd9e579bd9 in dawn::native::d3d::CompileShader D:\chromium\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:370
    #15 0x7ffd9e61b562 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> D:\chromium\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #16 0x7ffd9e706078 in dawn::native::d3d12::ShaderModule::Compile D:\chromium\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:385
    #17 0x7ffd9e6e6856 in dawn::native::d3d12::RenderPipeline::InitializeImpl D:\chromium\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:365
    #18 0x7ffd9e4225ab in dawn::native::PipelineBase::Initialize D:\chromium\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #19 0x7ffd9e33cef3 in dawn::native::DeviceBase::CreateRenderPipeline D:\chromium\src\third_party\dawn\src\dawn\native\Device.cpp:2244
    #20 0x7ffd9e33c6a4 in dawn::native::DeviceBase::APICreateRenderPipeline D:\chromium\src\third_party\dawn\src\dawn\native\Device.cpp:1556
    #21 0x7ffdccdd34b9 in dawn::wire::server::Server::DoDeviceCreateRenderPipeline D:\chromium\src\out\asan\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:469
    #22 0x7ffdcc63cd42 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline D:\chromium\src\out\asan\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:716
    #23 0x7ffdcc6462c8 in dawn::wire::server::Server::HandleCommandsImpl D:\chromium\src\out\asan\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:2056
    #24 0x7ffdc791398f in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1043
    #25 0x7ffdc7913e5f in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1950
    #26 0x7ffdc790437a in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1895
    #27 0x7ffdb7dd5f40 in gpu::CommandBufferService::Flush D:\chromium\src\gpu\command_buffer\service\command_buffer_service.cc:263

previously allocated by thread T0 here:
    #0 0x7ff67791d22d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffd8a6e1176 in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffd888aee54 in llvm::User::operator new D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:96
    #3 0x7ffd87f05134 in llvm::IRBuilder<1,llvm::ConstantFolder,clang::CodeGen::CGBuilderInserter<1> >::CreateStore D:\chromium\src\third_party\dawn\third_party\dxc\include\llvm\IR\IRBuilder.h:1015
    #4 0x7ffd87f120db in SimpleFlatValCopy D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGHLSLMS.cpp:6058
    #5 0x7ffd87f1796f in `anonymous namespace'::CGMSHLSLRuntime::EmitHLSLSplat D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGHLSLMS.cpp:6151
    #6 0x7ffd87f17dd7 in `anonymous namespace'::CGMSHLSLRuntime::EmitHLSLSplat D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGHLSLMS.cpp:6129
    #7 0x7ffd87eb90c7 in `anonymous namespace'::CGMSHLSLRuntime::EmitHLSLFlatConversion D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGHLSLMS.cpp:6167
    #8 0x7ffd89a6ef53 in `anonymous namespace'::AggExprEmitter::VisitCastExpr D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExprAgg.cpp:722
    #9 0x7ffd89a6cc8c in `anonymous namespace'::AggExprEmitter::VisitCastExpr D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExprAgg.cpp:708
    #10 0x7ffd89a58ec1 in clang::CodeGen::CodeGenFunction::EmitAggExpr D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExprAgg.cpp:1505
    #11 0x7ffd89a3cff0 in clang::CodeGen::CodeGenFunction::EmitExprAsInit D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGDecl.cpp:1283
    #12 0x7ffd89a391ab in clang::CodeGen::CodeGenFunction::EmitAutoVarInit D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGDecl.cpp:1174
    #13 0x7ffd89a30cec in clang::CodeGen::CodeGenFunction::EmitVarDecl D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGDecl.cpp:165
    #14 0x7ffd8a2ec8fd in clang::CodeGen::CodeGenFunction::EmitDeclStmt D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGStmt.cpp:1208
    #15 0x7ffd8a2e0112 in clang::CodeGen::CodeGenFunction::EmitSimpleStmt D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGStmt.cpp:264
    #16 0x7ffd8a2df232 in clang::CodeGen::CodeGenFunction::EmitStmt D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGStmt.cpp:52
    #17 0x7ffd8a2ef3ff in clang::CodeGen::CodeGenFunction::EmitCompoundStmtWithoutScope D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGStmt.cpp:305
    #18 0x7ffd89a2038c in clang::CodeGen::CodeGenFunction::EmitFunctionBody D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenFunction.cpp:811
    #19 0x7ffd89a21d29 in clang::CodeGen::CodeGenFunction::GenerateCode D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenFunction.cpp:932
    #20 0x7ffd88fde120 in clang::CodeGen::CodeGenModule::EmitGlobalFunctionDefinition D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenModule.cpp:2620
    #21 0x7ffd88fd0d55 in clang::CodeGen::CodeGenModule::EmitGlobalDefinition D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenModule.cpp:1603
    #22 0x7ffd88fda7f9 in clang::CodeGen::CodeGenModule::EmitGlobal D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenModule.cpp:1451
    #23 0x7ffd88fe5b0c in clang::CodeGen::CodeGenModule::EmitTopLevelDecl D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenModule.cpp:3392
    #24 0x7ffd8701672a in `anonymous namespace'::CodeGeneratorImpl::HandleTopLevelDecl D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\ModuleBuilder.cpp:134
    #25 0x7ffd867d0185 in clang::BackendConsumer::HandleTopLevelDecl D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:120
    #26 0x7ffd87294573 in clang::ParseAST D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:148
    #27 0x7ffd867c9d51 in clang::CodeGenAction::ExecuteAction D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:808

SUMMARY: AddressSanitizer: heap-use-after-free D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilConditionalMem2Reg.cpp:275 in DxilConditionalMem2Reg::ScalarizePreciseVectorAlloca
Shadow bytes around the buggy address:
  0x12530f65c400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12530f65c480: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x12530f65c500: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa
  0x12530f65c580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x12530f65c600: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
=>0x12530f65c680: fd fd fd fd[fd]fd fd fa fa fa fa fa fa fa f7 fa
  0x12530f65c700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x12530f65c780: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x12530f65c800: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa
  0x12530f65c880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x12530f65c900: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
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

==20116==ADDITIONAL INFO

==20116==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffdb1f5b6d2 in gpu::Scheduler::RunNextTask D:\chromium\src\gpu\command_buffer\service\scheduler.cc:607
    #1 0x7ffdb1f5b6d2 in gpu::Scheduler::RunNextTask D:\chromium\src\gpu\command_buffer\service\scheduler.cc:607
    #2 0x7ffdb1f55cda in gpu::Scheduler::TryScheduleSequence D:\chromium\src\gpu\command_buffer\service\scheduler.cc:409
    #3 0x7ffdc080620e in viz::DisplayScheduler::ScheduleBeginFrameDeadline D:\chromium\src\components\viz\service\display\display_scheduler.cc:497

```

### pe...@google.com (2024-09-09)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-09-09)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dn...@google.com (2024-09-09)

I'm at a conference. Reassigning.

### am...@google.com (2024-09-11)

Was able to reproduce the ASAN UAF using ASAN Chromium build `Version 130.0.6711.0 (Developer Build) (64-bit)` and opening `indexScalarizePreciseVectorAlloca.html`. Does not result in a crash on latest Canary `Version 130.0.6711.0 (Official Build) canary (64-bit)`; however, UAFs do not always result in crashes in release builds.

I determined the reason for the UAF, and have put up a fix on upstream: <https://github.com/microsoft/DirectXShaderCompiler/pull/6910>

### am...@google.com (2024-09-11)

Upstream fix has landed. Waiting for it to roll into Dawn, then into Chrome, for testing.

### am...@google.com (2024-09-16)

This is fixed. Issue no longer reproduces in latest ASAN build of Chromium: `Version 130.0.6720.0 (Developer Build) (64-bit)`. Opening `indexScalarizePreciseVectorAlloca.html.` does not result in a GPU process crash anymore.

- Upstream fix landed: <https://github.com/microsoft/DirectXShaderCompiler/pull/6910>
- Fix manually rolled into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/206394>
- Fix rolled into Chromium: <https://dawn.googlesource.com/dawn.git/+log/9b2cd683aca7..4ad4b1457bf1>

### pe...@google.com (2024-09-16)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128, 129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@google.com (2024-09-17)

1. Which CLs should be backmerged? (Please include Gerrit links.)

- Upstream fix landed: <https://github.com/microsoft/DirectXShaderCompiler/pull/6910>
- Fix manually rolled into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/206394>
- Fix rolled into Chromium: <https://dawn.googlesource.com/dawn.git/+log/9b2cd683aca7..4ad4b1457bf1>

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes.

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

No, but can be tested by opening `indexScalarizePreciseVectorAlloca.html` in latest ASAN Chromium and verifying that the GPU process does not crash.

### pe...@google.com (2024-09-17)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128, 129, 130].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2024-09-17)

Change landed and rolled into Chromium on 130 on 12 September; no 130 merge review needed
No issues related to this fix since it was rolled into Chromium (<https://crrev.com/c/5858740>)
M129 Stable and M128 Extended Stable merges approved; please merge this fix to branches 6668 and 6613 respectively at your earliest convenience, before EOD Thursday, 19 September so this fix can be included in the next updates for each

### ap...@google.com (2024-09-18)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6613

commit ee5422d3f33c0bfd8643ce7782eb3a216cf15dea
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Tue Sep 17 18:15:03 2024

    Fix ASAN UAF in DxilConditionalMem2Reg (#6910)
    
    ScalarizePreciseVectorAlloca would iterate over all instructions, then
    for each instruction use, would iterate and potentially erase the
    instruction. If the erased instruction was the immediate next
    instruction after the alloca, this would invalidate the outer
    instruction iterator. Fixed by collecting the allocas in a vector first.
    
    Bug: 365254285
    Change-Id: I551455295c600e49354beae665275bc80ce186e4
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5870863
    Reviewed-by: dan sinclair <dsinclair@chromium.org>
    Reviewed-by: James Price <jrprice@google.com>

M       lib/Transforms/Scalar/DxilConditionalMem2Reg.cpp
A       tools/clang/test/DXC/Passes/DxilConditionalMem2Reg/precise-vector-alloca-followed-by-use.hlsl

https://chromium-review.googlesource.com/5870863


### ap...@google.com (2024-09-18)

Project: dawn
Branch: chromium/6613

commit 65fc64fce1c8b05c34d03ce7eb4304d471c971b3
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Wed Sep 18 13:18:04 2024

    DEPS: Update DXC to patched branch
    
    Bug: 365254285
    Change-Id: Iec877cfdc6e89a47c9f0ac43df464b4271b16460
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/207014
    Reviewed-by: James Price <jrprice@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/207014


### ap...@google.com (2024-09-18)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6668

commit 29eccb23f9845403821d1ce0e2b6ca33d963c2ab
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Wed Sep 18 09:19:46 2024

    Fix ASAN UAF in DxilConditionalMem2Reg (#6910)
    
    ScalarizePreciseVectorAlloca would iterate over all instructions, then
    for each instruction use, would iterate and potentially erase the
    instruction. If the erased instruction was the immediate next
    instruction after the alloca, this would invalidate the outer
    instruction iterator. Fixed by collecting the allocas in a vector first.
    
    Bug: 365254285
    Change-Id: I70b59f417e62fd499284e41b2d73be858561dcb3
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5873360
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: dan sinclair <dsinclair@chromium.org>

M       lib/Transforms/Scalar/DxilConditionalMem2Reg.cpp
A       tools/clang/test/DXC/Passes/DxilConditionalMem2Reg/precise-vector-alloca-followed-by-use.hlsl

https://chromium-review.googlesource.com/5873360


### ap...@google.com (2024-09-18)

Project: dawn
Branch: chromium/6668

commit 46428fd238c00f1637a56446b6910e92c2a1160f
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Wed Sep 18 13:35:31 2024

    DEPS: Update DXC to patched branch
    
    Bug: 365254285
    Change-Id: Id213f64b7ddff4d9985052b82ff0ba32205eb259
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/207034
    Reviewed-by: James Price <jrprice@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/207034


### am...@google.com (2024-09-18)

- M128/6613
  - [Cherry-pick to DXC](https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5870863)
  - [DXC to Dawn](https://dawn-review.googlesource.com/c/dawn/+/207014)
  - [Dawn to Chromium](https://chromium.googlesource.com/chromium/src.git/+/06522ad5978a89c0523d627ea1bd22c474207947)
- M129/6668
  - [Cherry-pick to DXC](https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5873360)
  - [DXC to Dawn](https://dawn-review.googlesource.com/c/dawn/+/207034)
  - [Dawn to Chromium](https://chromium.googlesource.com/chromium/src.git/+/66d3730a26f21a49d2ad08118c2acdaaf21375c5)

### sp...@google.com (2024-09-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in a highly privileged process (GPU)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-19)

Congratulations! Thank you for your efforts and reporting this issue to us.
Please let us know if there is a particular name or handle/tag we should use in acknowledging you for this issue.

### a7...@gmail.com (2024-09-19)

Thanks am...@chromium.org. No particular handle/tag should receive credit; i.e., anonymous is fine.

### ti...@chromium.org (2024-09-24)

CC-ing bookholt@ per offline request by reporter - see also [comment #2](https://issues.chromium.org/issues/365254285#comment2).

### pe...@google.com (2024-12-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a highly privileged process (GPU)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/365254285)*
