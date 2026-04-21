# GPU process crash via WebGPU shader - DeleteMemcpy in ScalarReplAggregatesHLSL.cpp

| Field | Value |
|-------|-------|
| **Issue ID** | [331123811](https://issues.chromium.org/issues/331123811) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU, Internals>GPU>Dawn |
| **Platforms** | Android, Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-03-25 |
| **Bounty** | $10,000.00 |

## Description

VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this might trigger a heap UAF insider the hlsl compiler.

VERSION
Chrome Version: Pre-compiled ASAN Chromium 125.0.6375.0 (Developer Build) (64-bit)
Operating System: Win10 Build 19045

REPRODUCTION CASE
Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process.
The problematic wgsl shader is:

```
struct S2596889757_ {
    @builtin(front_facing) m0_: bool,
}

var<private> G2178370774_: S2596889757_;

@fragment
fn fragment_main() -> @location(0) vec4<f32> {
    {
        G2178370774_ = G2178370774_;
    }
    return vec4<f32>(0.0, 0.0, 0.0, 0.0);
}
```


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: GPU
Crash State:

4:134> g
    #0 0x7ffec1a98674 in `anonymous namespace'::MemcpySplitter::SplitMemCpy C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:1118
    #1 0x7ffec1aa5ebc in `anonymous namespace'::SROA_Helper::LowerMemcpy C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:4025
    #2 0x7ffec1a8d2c7 in `anonymous namespace'::SROAGlobalAndAllocas C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:1937
    #3 0x7ffec1a7ede5 in `anonymous namespace'::SROA_Parameter_HLSL::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:4289
    #4 0x7ffec0adaa2d in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #5 0x7ffec0ae3b11 in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #6 0x7ffec05231a1 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #7 0x7ffec0c04b41 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #8 0x7ffec051e02a in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #9 0x7ffec052b2b3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #10 0x7ffec041ef57 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #11 0x7ffe67bda760 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #12 0x7ffe67c38c10 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #13 0x7ffe67cddf54 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:379
    #14 0x7ffe67cc8420 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:383
    #15 0x7ffe67b0a320 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #16 0x7ffe67a699ce in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2032
    #17 0x7ffe67a693d1 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1347
    #18 0x7ffe8982c0ad in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #19 0x7ffe8921b214 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #20 0x7ffe8922054c in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1642
    #21 0x7ffe84e50d82 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:999
    #22 0x7ffe84e511d5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1894
    #23 0x7ffe84e45021 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1839
    #24 0x7ffe78d25543 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #25 0x7ffe759aadae in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:507
    #26 0x7ffe759a9853 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:155
    #27 0x7ffe78d434b5 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:873
    #28 0x7ffe78d5371a in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #29 0x7ffe7836aa09 in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:740
    #30 0x7ffe78368a84 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:665
    #31 0x7ffe7836c128 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #32 0x7ffe738d0070 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #33 0x7ffe771b895b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #34 0x7ffe771b7884 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #35 0x7ffe771e2d1a in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #36 0x7ffe771ba6aa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:641
    #37 0x7ffe7391a3d0 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #38 0x7ffe766ec3eb in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:434
    #39 0x7ffe721f37d2 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:771
    #40 0x7ffe721f5d31 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1146
    #41 0x7ffe721f18a7 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:328
    #42 0x7ffe721f225d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:341
    #43 0x7ffe655b16c3 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #44 0x7ff6072e4386 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:180
    #45 0x7ff6072e1da0 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #46 0x7ff6076bc7b3 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #47 0x7ffef3b27613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)
    #48 0x7ffef43426a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x1242774bd9d0 is located 48 bytes inside of 96-byte region [0x1242774bd9a0,0x1242774bda00)
freed by thread T0 here:
    #0 0x7ff6073baa5d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffec073784b in llvm::ICmpInst::~ICmpInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:1093
    #2 0x7ffec182effd in llvm::Instruction::eraseFromParent C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Instruction.cpp:71
    #3 0x7ffec1a97f0f in `anonymous namespace'::MemcpySplitter::SplitMemCpy C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:1118
    #4 0x7ffec1aa5ebc in `anonymous namespace'::SROA_Helper::LowerMemcpy C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:4025
    #5 0x7ffec1a8d2c7 in `anonymous namespace'::SROAGlobalAndAllocas C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:1937
    #6 0x7ffec1a7ede5 in `anonymous namespace'::SROA_Parameter_HLSL::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:4289
    #7 0x7ffec0adaa2d in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #8 0x7ffec0ae3b11 in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #9 0x7ffec05231a1 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #10 0x7ffec0c04b41 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #11 0x7ffec051e02a in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #12 0x7ffec052b2b3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #13 0x7ffec041ef57 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #14 0x7ffe67bda760 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #15 0x7ffe67c38c10 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #16 0x7ffe67cddf54 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:379
    #17 0x7ffe67cc8420 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:383
    #18 0x7ffe67b0a320 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #19 0x7ffe67a699ce in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2032
    #20 0x7ffe67a693d1 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1347
    #21 0x7ffe8982c0ad in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #22 0x7ffe8921b214 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #23 0x7ffe8922054c in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1642
    #24 0x7ffe84e50d82 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:999
    #25 0x7ffe84e511d5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1894
    #26 0x7ffe84e45021 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1839
    #27 0x7ffe78d25543 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232

previously allocated by thread T0 here:
    #0 0x7ff6073bab5d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffec2d9d41e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffec18e9e51 in llvm::User::operator new C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:96
    #3 0x7ffec182145a in llvm::CastInst::Create C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Instructions.cpp:2271
    #4 0x7ffec1a939e4 in `anonymous namespace'::PatchZeroIdxGEP C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:929
    #5 0x7ffec1a7c3de in `anonymous namespace'::SROA_Parameter_HLSL::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:4195
    #6 0x7ffec0adaa2d in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #7 0x7ffec0ae3b11 in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #8 0x7ffec05231a1 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #9 0x7ffec0c04b41 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #10 0x7ffec051e02a in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #11 0x7ffec052b2b3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #12 0x7ffec041ef57 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #13 0x7ffe67bda760 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #14 0x7ffe67c38c10 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #15 0x7ffe67cddf54 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:379
    #16 0x7ffe67cc8420 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:383
    #17 0x7ffe67b0a320 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #18 0x7ffe67a699ce in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2032
    #19 0x7ffe67a693d1 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1347
    #20 0x7ffe8982c0ad in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #21 0x7ffe8921b214 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #22 0x7ffe8922054c in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1642
    #23 0x7ffe84e50d82 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:999
    #24 0x7ffe84e511d5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1894
    #25 0x7ffe84e45021 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1839
    #26 0x7ffe78d25543 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #27 0x7ffe759aadae in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:507

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:1118 in `anonymous namespace'::MemcpySplitter::SplitMemCpy
Shadow bytes around the buggy address:
  0x1242774bd700: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1242774bd780: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x1242774bd800: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1242774bd880: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x1242774bd900: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
=>0x1242774bd980: fa fa f7 fa fd fd fd fd fd fd[fd]fd fd fd fd fd
  0x1242774bda00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1242774bda80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x1242774bdb00: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x1242774bdb80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1242774bdc00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==4148==ADDITIONAL INFO

==4148==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffe78368fe0 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:681
    #1 0x7ffe78368fe0 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:681
    #2 0x7ffe78368fe0 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:681
    #3 0x7ffe783621e3 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:481


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==4148==END OF ADDITIONAL INFO
==4148==ABORTING
win32u!NtGdiDdDDIWaitForVerticalBlankEvent+0x14:
00007ffe`f2215cc4 c3              ret

## Attachments

- [index2.html](attachments/index2.html) (text/html, 2.4 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-03-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6248113924145152.

### xi...@chromium.org (2024-03-26)

While the ClusterFuzz is still running, looping in amaiorano@ early in case this is a duplicate or follow up of <https://issues.chromium.org/issues/328958020>.

### pe...@google.com (2024-03-26)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-26)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cl...@appspot.gserviceaccount.com (2024-03-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5091575096344576.

### am...@google.com (2024-03-26)

Reproduces with locally GN-compiled dxc with `is_asan = true`. Reduced to a simpler test case, now as a compute shader:

```
struct MyStruct {
  int m0;
};

static MyStruct s;

void foo() {
  s = s;
}

[numthreads(1, 1, 1)]
void main() {
  foo();
}

```

### am...@google.com (2024-03-27)

I landed a fix upstream: <https://github.com/microsoft/DirectXShaderCompiler/pull/6466>

And this has rolled into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/180984>

### pe...@google.com (2024-03-27)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-03-27)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-03-27)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

### am...@google.com (2024-03-27)

1. Why does your merge fit within the merge criteria for these milestones?

This fixes a crash in the GPU process. This only affects Windows.

2. What changes specifically would you like to merge? Please link to Gerrit.

<https://dawn-review.googlesource.com/c/dawn/+/180984>

3. Have the changes been released and tested on canary?

Not yet. Waiting for Dawn to roll into Chromium.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Open the index2.html file attached to this bug and verify in the dev console that the GPU device was not lost.

### am...@chromium.org (2024-03-27)

Thanks for the work on this one, amaiorano@. Since this fix just landed and hasn't rolled into Chromium as of yet, I'll revisit in ~ 48 hours to ensure there's been sufficient Canary bake time before making merge decisions.

### pe...@google.com (2024-03-28)

Setting milestone because of s0/s1 severity.

### wg...@gmail.com (2024-03-28)

Forgot to add a credit info when creating the issue:

CREDIT INFORMATION
Reporter credit: wgslfuzz

### am...@chromium.org (2024-03-28)

Hi -- no worries about adding credit each time; we have your credit info in our database now which will use going forward.
You only need to let us know in the future if you want to change what credit / ack data you would like us to use.

### am...@chromium.org (2024-03-28)

hi amaiorano@ -- I can't review this for backmerge yet as it appears there is an issue with the Dawn into Chromium autoroller and the roll in c#12 (<https://dawn-review.googlesource.com/c/dawn/+/180984>) has not been landed on Chromium as of yet. I've reached out to the webgpu gardener for assistance.

### am...@chromium.org (2024-03-28)

p0 bug for autoroller filed earlier today but webgpu gardener: [crbug.com/331775413](https://crbug.com/331775413)

### am...@chromium.org (2024-03-29)

autoroller issue was resolved earlier today, so the roll with this fix is now finally on Canary; I'll revisit this issue for merge review early next week

### am...@google.com (2024-04-02)

Works on latest Canary: Version 125.0.6394.0 (Official Build) canary (64-bit)

[amyressler@chromium.org](mailto:amyressler@chromium.org) please let me know which Milestones branches we want this patch to go so that I can cherry-pick the fix to them.

### am...@chromium.org (2024-04-03)

despite looking at the upstream fix I'm not confident in my assessment to sort out any issues/impact on Canary, please confirm there are not stability risks or issues before merging; please let me know if there are any issues here

tentatively approving merge to M124 Beta / branch 6376 and M123 Stable / branch 6312, please merge this fix to the respective branches by EOD tomorrow / Thursday so this fix can be included in the next M123 Stable update and M124 Beta update and impending Stable RC -- thank you

### am...@google.com (2024-04-03)

> despite looking at the upstream fix I'm not confident in my assessment to sort out any issues/impact on Canary, please confirm there are not stability risks or issues before merging; please let me know if there are any issues here

Cherry-picking the specific fix I made on DXC will not introduce any stability risks. In order to cherry-pick just that fix for the two release branches, I've made a [request to get patch branches made on our mirror of DXC](https://g-issues.chromium.org/issues/332735132). As soon as these are created, I will push the fix and get them landed.

### ap...@google.com (2024-04-03)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6312

commit a65e511a14b4bffda1b24052732b09ca130359d1
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Wed Apr 03 15:58:51 2024

    Fix ASAN use-after-free on unreferenced self-assignment of struct instance (#6466)
    
    When deleting an unused memcpy, ScalarReplAggregatesHLSL was attempting
    to delete both the target and the source of the memcpy without first
    checking if they were both same, resulting in a double-delete.
    
    Bug: chromium:331123811
    Change-Id: Idaef95a06b10a7fb6f0ca2e662972a44ec662fbc
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5419225
    Reviewed-by: David Neto <dneto@google.com>
    Reviewed-by: dan sinclair <dsinclair@chromium.org>
    Reviewed-by: Ben Clayton <bclayton@chromium.org>

M       lib/Transforms/Scalar/ScalarReplAggregatesHLSL.cpp
A       tools/clang/test/DXC/unreferenced_struct_selft_assignment_crash.hlsl

https://chromium-review.googlesource.com/5419225


### am...@google.com (2024-04-04)

The fix has been pulled into the two Chrome release branches:

M123: <https://chromium.googlesource.com/chromium/src.git/+/6b9d9ec2581aa1a4f3d8a9fc597bf23d7e3a0ad8>

M123: <https://chromium.googlesource.com/chromium/src.git/+/a06dc4e8e17502595195e89b5d203b0b64aff865>

### am...@google.com (2024-04-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-04)

Congratulations wgslfuzz! The Chrome VRP Panel has decided to aware you $10,000 for this report of GPU process memory corruption. Thank you for your efforts in discovering and reporting this issue to us -- nice work!

### pe...@google.com (2024-04-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### am...@chromium.org (2024-04-08)

The second merge line in c#24 should read M124, as that reflects the M124 roll with the fixes (<https://crrev.com/c/c5421670>); updating merge labels accordingly

### pe...@google.com (2024-07-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/331123811)*
