#  GPU process crash via WebGPU shader - UAF in GlobalIsNeeded at GlobalDCE.cpp:244

| Field | Value |
|-------|-------|
| **Issue ID** | [342428008](https://issues.chromium.org/issues/342428008) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU, Dawn>Tint |
| **Platforms** | Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-05-23 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this triggers a UAF inside the hlsl compiler.

##### VERSION

Chrome Version: Pre-compiled ASAN Chromium 127.0.6497.0 (Developer Build) (64-bit)  

Operating System: Win11 Build 22631.3447

##### REPRODUCTION CASE

Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process.

Reproducing the issue stand-alone on Linux also possible:

1. Compile the standalone.wgsl with tint (commit 143523a12f42d663bc0473cf5d8468559d4eb192) to hlsl via `./tint standalone.wgsl -o standalone.hlsl`. I also attached standalone.hlsl, but you should get the very same file when compiling standalone.wgsl yourself
2. Compile the hlsl with dxc (commit a1b945c1a3e0866b409c00d7ff2ed077060f5a57): `./dxc-3.7 -T cs_6_2 -HV 2018 standalone.hlsl`. This should trigger an ASAN violation.

##### Attached:

- html that triggers an ASAN violation in chromium
- wgsl for producing the hlsl shader
- the hlsl shader
- asan log file

```
[13380:9656:0523/073333.826:WARNING:chrome_main_delegate.cc(742)] This is Chrome version 127.0.6497.0 (not a warning)
[13380:13940:0523/073334.014:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[13380:14912:0523/073334.077:ERROR:sandbox_win.cc(913)] Sandbox cannot access executable. Check filesystem permissions are valid. See https://bit.ly/31yqMJR.: Access is denied. (0x5)
[13380:9656:0523/073334.249:WARNING:account_consistency_mode_manager.cc(77)] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
[13380:9656:0523/073334.469:WARNING:browser_management_service.cc(128)] EnterpriseLogoUrl fetch failed with error code -1 and MIME type
[13380:9656:0523/073335.190:ERROR:network_service_instance_impl.cc(600)] Network service crashed, restarting service.
[13380:9656:0523/073335.237:WARNING:external_registry_loader_win.cc(232)] Error observing HKLM: 5
[10096:8564:0523/073335.300:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[13380:8984:0523/073339.025:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[10096:8564:0523/073340.309:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
=================================================================
==15112==ERROR: AddressSanitizer: heap-use-after-free on address 0x11dbb0bca240 at pc 0x7ffb676bbbbc bp 0x00bcfedfc6a0 sp 0x00bcfedfc6e8
READ of size 1 at 0x11dbb0bca240 thread T0
==15112==WARNING: Failed to use and restart external symbolizer!
==15112==*** WARNING: Failed to initialize DbgHelp!              ***
==15112==*** Most likely this means that the app is already      *** 
==15112==*** using DbgHelp, possibly with incompatible flags.    *** 
==15112==*** Due to technical reasons, symbolization might crash *** 
==15112==*** or produce wrong results.                           ***
    #0 0x7ffb676bbbbb in `anonymous namespace'::GlobalDCE::GlobalIsNeeded C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\IPO\GlobalDCE.cpp:244
    #1 0x7ffb676b92cf in `anonymous namespace'::GlobalDCE::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\IPO\GlobalDCE.cpp:100
    #2 0x7ffb665e97b5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #3 0x7ffb665f2b4c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:781
    #4 0x7ffb66000921 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #5 0x7ffb6671e5a1 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #6 0x7ffb65ffb612 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #7 0x7ffb66008de3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #8 0x7ffb65ee6c13 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #9 0x7ffb1114a139 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #10 0x7ffb111ada5e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #11 0x7ffb1124f374 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #12 0x7ffb11213bdc in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:87
    #13 0x7ffb11065550 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #14 0x7ffb10fb6781 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1987
    #15 0x7ffb10fb6167 in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1300
    #16 0x7ffb335603ad in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #17 0x7ffb32fb0354 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477   
    #18 0x7ffb32fb869d in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1652
    #19 0x7ffb2eaef6f2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1020
    #20 0x7ffb2eaefb45 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1924
    #21 0x7ffb2eae3e71 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1869
    #22 0x7ffb22778c23 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #23 0x7ffb1f32526c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:506
    #24 0x7ffb1f323d13 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:154
    #25 0x7ffb22796aca in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:930
    #26 0x7ffb227a7baa in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&,unsigned long long &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams>,unsigned long long>,void ()>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams>,unsigned long long>,0,1,2> C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1067
    #27 0x7ffb21dddc9d in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:743
    #28 0x7ffb21ddc068 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:668
    #29 0x7ffb21ddf1f5 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #30 0x7ffb1d280ad0 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #31 0x7ffb20c02dae in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473 
    #32 0x7ffb20c01cb9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #33 0x7ffb20c380ce in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #34 0x7ffb20c049fc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:645
    #35 0x7ffb1d2ca760 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #36 0x7ffb2010bdc9 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:438
    #37 0x7ffb1bbb39e2 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:780
    #38 0x7ffb1bbb5f63 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1156
    #39 0x7ffb1bbb197d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #40 0x7ffb1bbb246d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #41 0x7ffb0ea51601 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #42 0x7ff7bec243a5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #43 0x7ff7bec21db2 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #44 0x7ff7bf000ac3 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #45 0x7ffbc73c257c in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x18001257c)
    #46 0x7ffbc83eaa47 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005aa47)

0x11dbb0bca240 is located 96 bytes inside of 160-byte region [0x11dbb0bca1e0,0x11dbb0bca280)
freed by thread T0 here:
    #0 0x7ff7becfcc4d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffb66228c3b in llvm::ICmpInst::~ICmpInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:1093
    #2 0x7ffb673caf7d in llvm::Instruction::eraseFromParent C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Instruction.cpp:71
    #3 0x7ffb6768019a in `anonymous namespace'::DeleteDeadInstructions C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:1196
    #4 0x7ffb67640b08 in `anonymous namespace'::SROAGlobalAndAllocas C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:2012
    #5 0x7ffb6762c6e5 in `anonymous namespace'::SROA_Parameter_HLSL::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:4316
    #6 0x7ffb665e97b5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #7 0x7ffb665f2b4c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:781
    #8 0x7ffb66000921 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #9 0x7ffb6671e5a1 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #10 0x7ffb65ffb612 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #11 0x7ffb66008de3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #12 0x7ffb65ee6c13 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #13 0x7ffb1114a139 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #14 0x7ffb111ada5e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #15 0x7ffb1124f374 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #16 0x7ffb11213bdc in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:87
    #17 0x7ffb11065550 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #18 0x7ffb10fb6781 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1987
    #19 0x7ffb10fb6167 in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1300
    #20 0x7ffb335603ad in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #21 0x7ffb32fb0354 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477
    #22 0x7ffb32fb869d in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1652
    #23 0x7ffb2eaef6f2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1020
    #24 0x7ffb2eaefb45 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1924
    #25 0x7ffb2eae3e71 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1869
    #26 0x7ffb22778c23 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #27 0x7ffb1f32526c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:506


previously allocated by thread T0 here:
    #0 0x7ff7becfcd4d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffb68a05b9e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffb6748c3f1 in llvm::User::operator new C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:96
    #3 0x7ffb66425aac in llvm::GetElementPtrInst::Create C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:866
    #4 0x7ffb6812d5a9 in llvm::IRBuilder<0,llvm::ConstantFolder,clang::CodeGen::CGBuilderInserter<0> >::CreateGEP C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\IRBuilder.h:1077
    #5 0x7ffb688af7a7 in clang::CodeGen::CodeGenFunction::EmitCXXMemberOrOperatorMemberCallExpr C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExprCXX.cpp:270
    #6 0x7ffb688b0b58 in clang::CodeGen::CodeGenFunction::EmitCXXOperatorMemberCallExpr C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExprCXX.cpp:500
    #7 0x7ffb68126dd1 in clang::CodeGen::CodeGenFunction::EmitCallExpr C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExpr.cpp:3662
    #8 0x7ffb681065e3 in clang::CodeGen::CodeGenFunction::EmitCallExprLValue C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExpr.cpp:3772
    #9 0x7ffb680f484d in clang::CodeGen::CodeGenFunction::EmitLValue C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExpr.cpp:861
    #10 0x7ffb681035f4 in clang::CodeGen::CodeGenFunction::EmitCheckedLValue C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExpr.cpp:813
    #11 0x7ffb680d082e in `anonymous namespace'::ScalarExprEmitter::VisitCallExpr C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExprScalar.cpp:361
    #12 0x7ffb680b7061 in `anonymous namespace'::ScalarExprEmitter::Visit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExprScalar.cpp:230
    #13 0x7ffb680e3630 in `anonymous namespace'::ScalarExprEmitter::VisitCastExpr C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExprScalar.cpp:1528
    #14 0x7ffb680b6da6 in `anonymous namespace'::ScalarExprEmitter::Visit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExprScalar.cpp:230
    #15 0x7ffb680b589f in clang::CodeGen::CodeGenFunction::EmitScalarExpr C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGExprScalar.cpp:3926
    #16 0x7ffb681464ab in clang::CodeGen::CodeGenFunction::EmitScalarInit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGDecl.cpp:624
    #17 0x7ffb6814b209 in clang::CodeGen::CodeGenFunction::EmitExprAsInit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGDecl.cpp:1269
    #18 0x7ffb68148b20 in clang::CodeGen::CodeGenFunction::EmitAutoVarInit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGDecl.cpp:1174
    #19 0x7ffb6814327b in clang::CodeGen::CodeGenFunction::EmitVarDecl C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGDecl.cpp:165
    #20 0x7ffb687176a9 in clang::CodeGen::CodeGenFunction::EmitSimpleStmt C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGStmt.cpp:264
    #21 0x7ffb68716ac3 in clang::CodeGen::CodeGenFunction::EmitStmt C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGStmt.cpp:52
    #22 0x7ffb6872507a in clang::CodeGen::CodeGenFunction::EmitCompoundStmtWithoutScope C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CGStmt.cpp:305
    #23 0x7ffb68137324 in clang::CodeGen::CodeGenFunction::EmitFunctionBody C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenFunction.cpp:811
    #24 0x7ffb68138743 in clang::CodeGen::CodeGenFunction::GenerateCode C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenFunction.cpp:932
    #25 0x7ffb67a51206 in clang::CodeGen::CodeGenModule::EmitGlobalFunctionDefinition C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenModule.cpp:2620
    #26 0x7ffb67a4715d in clang::CodeGen::CodeGenModule::EmitGlobalDefinition C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenModule.cpp:1603
    #27 0x7ffb67a4e993 in clang::CodeGen::CodeGenModule::EmitGlobal C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenModule.cpp:1451

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\IPO\GlobalDCE.cpp:244 in `anonymous namespace'::GlobalDCE::GlobalIsNeeded
Shadow bytes around the buggy address:
  0x11dbb0bc9f80: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa
  0x11dbb0bca000: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x11dbb0bca080: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa f7 fa
  0x11dbb0bca100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11dbb0bca180: fd fd fd fd fa fa fa fa fa fa f7 fa fd fd fd fd
=>0x11dbb0bca200: fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd
  0x11dbb0bca280: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x11dbb0bca300: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x11dbb0bca380: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x11dbb0bca400: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa
  0x11dbb0bca480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==15112==ADDITIONAL INFO

==15112==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffb21ddc1ea in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684
    #1 0x7ffb21ddc1ea in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684
    #2 0x7ffb21ddc1ea in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684
    #3 0x7ffb21ddc1ea in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==15112==END OF ADDITIONAL INFO
==15112==ABORTING
[13380:9656:0523/073419.480:ERROR:gpu_process_host.cc(1002)] GPU process exited unexpectedly: exit_code=1
[13380:9656:0523/073419.480:WARNING:gpu_process_host.cc(1436)] The GPU process has crashed 1 time(s)

```

## Attachments

- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 204 B)
- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 226 B)
- [asanglobalisneeded](attachments/asanglobalisneeded) (application/octet-stream, 21.0 KB)
- [indexGlobalIsNeeded.html](attachments/indexGlobalIsNeeded.html) (text/html, 2.1 KB)

## Timeline

### ps...@google.com (2024-05-23)

Thanks OP for the report!

I'm also setting the FoundIn speculatively to stable (M125).

amaiorano@: This looks similar to some other issues you've looked into recently that are marked as fixed. Setting severity to match those issues. Could you please take a look and see if the fix you landed will remediate these issues as well?

### am...@google.com (2024-05-24)

- Tested opening the attached `indexGlobalIsNeeded.html` in Canary `Version 127.0.6498.3 (Official Build) canary (64-bit)`, and the GPU process crashes.
- Am able to reproduce an ASAN heap-use-after-free when running dxc against the attached `standalone.hlsl`, although my call stack is different, failing `ScalarReplAggregatesHLSL`.

### pe...@google.com (2024-05-24)

Setting milestone because of s0/s1 severity.

### am...@google.com (2024-06-03)

Started investigating this last Friday (May 31st). See [investigation doc](https://docs.google.com/document/d/1M9DB8UiKMyw8ZtAMBmDtR9KNFuDp6B5MLTBopVNVPZk/edit?usp=sharing&resourcekey=0-jccWllxenpv-UZBVKyhXfQ).

I put up an upstream fix: [Fix crash in scalarrepl-param-hlsl when dynamically indexing a GEP of a constant indexed GEP by amaiorano · Pull Request #6670 · microsoft/DirectXShaderCompiler](https://github.com/microsoft/DirectXShaderCompiler/pull/6670/files)

Waiting for feedback from MS.

### am...@google.com (2024-06-11)

Fix landed, testing in Canary.

### am...@google.com (2024-06-11)

Tested by opening attached `indexGlobalIsNeeded.html` in Canary, `Version 127.0.6533.0 (Official Build) canary (64-bit)`, and the GPU process no longer crashes.

- Upstream fix: <https://github.com/microsoft/DirectXShaderCompiler/pull/6670>
- Roll of DXC with fix into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/192165>
- Roll of Dawn with fix into Chromium: <https://chromium-review.googlesource.com/c/chromium/src/+/5606688>

### am...@google.com (2024-06-19)

Hi [amyressler@google.com](mailto:amyressler@google.com), this was marked fixed over a week ago. Shouldn't the bot have updated this bug with the 5 questions by now?

### am...@chromium.org (2024-06-20)

It seems that a speculative foundin of 125 was set, which is Stable channel (rather than extended stable at the time of reporting) which resulted in milestone of M125. At the time this was fixed, M126 is Stable and there are no further releases of M125. The bot should have asked for a merge, but there is obviously some strange behavior with the blintz rules since the bot updated this issue as SI-Extended from SI-Stable, and M125 is not an Extended Stable support milestone.

I've gone ahead and set review labels here. I don't want to make any changes to the foundin- or SI at this time, because I'm noticing

In the future, please cc: me on issues if there is a question. I only have visibility to c#8 because there was also an email about this. I would have not seen this comment otherwise since there are hundreds of security bugs. Thanks!

### am...@chromium.org (2024-06-20)

The dawn roll landed on 127, no 127 merge needed

### am...@chromium.org (2024-06-20)

M126 merge approved for <https://chromium-review.googlesource.com/c/chromium/src/+/5606688>
please merge this fix to branch 6478 as soon as possible / by 10am pacific tomorrow, so this fix can be included in next week's M126 Stable udpate

### ap...@google.com (2024-06-20)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6478

commit 8f07d39227f6181d42fa8d42bc9c247c048bbd49
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Jun 20 14:49:58 2024

    Fix crash in scalarrepl-param-hlsl when dynamically indexing a GEP of a constant indexed GEP (#6670)
    
    When processing global values to determine when to flatten vectors, this
    pass was only checking the immdiate users of the value for non-dynamic
    indexing of the vector. But this would fail in the case of a dynamic
    indexed GEP of a constant indexed GEP (e.g. h[0][a]) because the first
    level GEP was constant indexed, but not the second. We fix this by
    checking the full User tree of the value in `hasDynamicVectorIndexing`.
    
    Bug: chromium:342428008
    Change-Id: Ibf2ae3a6528cfc9b50634058385c5a45aa1d3b75
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5645927
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: dan sinclair <dsinclair@chromium.org>

M       lib/Transforms/Scalar/ScalarReplAggregatesHLSL.cpp
A       tools/clang/test/DXC/Passes/ScalarReplHLSL/scalarrepl-param-hlsl-dyn-idx-gep-of-const-idx-gep.ll

https://chromium-review.googlesource.com/5645927


### ap...@google.com (2024-06-20)

Project: dawn
Branch: chromium/6478

commit b208b3aab58d2dda99ec9492ee007f150a08b805
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Jun 20 19:26:12 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:342428008
    Change-Id: Ide9ccf2903ab352b41c59dab1e0f97650b2f149c
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/195014
    Reviewed-by: dan sinclair <dsinclair@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/195014


### am...@google.com (2024-06-20)

Fix has been merged to [M126](https://chromium.googlesource.com/chromium/src.git/+/dac2df4a9fef60a29f14697509a18ae9212b29ed).

### sp...@google.com (2024-06-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
memory corruption in the GPU process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-21)

And another one -- congratulations! Thank you for your fuzzing efforts and reporting this issue to us -- nice work!

### pe...@google.com (2024-09-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> memory corruption in the GPU process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/342428008)*
