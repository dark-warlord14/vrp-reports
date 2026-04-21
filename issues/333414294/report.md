# GPU process crash via WebGPU shader - SimplifyInstruction in InstructionSimplify.cpp

| Field | Value |
|-------|-------|
| **Issue ID** | [333414294](https://issues.chromium.org/issues/333414294) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU, Internals>GPU>Dawn, Internals>GPU>Tint |
| **Platforms** | Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-04-09 |
| **Bounty** | $10,000.00 |

## Description

VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this might trigger a heap UAF insider the hlsl compiler.

VERSION
Chrome Version: Pre-compiled ASAN Chromium 125.0.6406.0 (Developer Build) (64-bit)
Operating System: Win10 Build 19045

REPRODUCTION CASE
Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process.
The problematic wgsl shader (for standalone compilation) is:

```
var<private> g: array<i32, 10>;
var<private> g_1: array<i32, 10>;
var<private> g_3: vec4<f32>;

@group(0) @binding(0)
var<storage> g_2: u32;

fn f_1() {
    var l_5: i32;
    var l_6: i32;
    var l_7: f32;
    var l_8: bool = true;

    l_5 = 0;
    l_6 = 0;

    loop {
        let x_133_ = (l_6 < 10);
        let x_135_ = g_2;

        if !((x_135_ <= 1)) {
            l_7 = 0.0;
        } else {
            return;
        }
        if x_133_ {
        } else {
            break;
        }
        let x_140_ = l_6;
        let x_141_ = l_6;
        let x_143_ = g[x_141_];
        g_1[x_140_] = x_143_;
        continuing {
            let x_145_ = l_6;
            l_6 = (x_145_ + 1);
        }
    }
    l_7 = f32(g[0]);
    g_3 = vec4<f32>(l_7, 0.0, 0.0, 0.0);
}
@fragment
fn main() -> @location(0) vec4<f32> {
    f_1();

    let _e9 = false;
    loop {
        continuing {
            break if _e9;
        }
    }

    let _e5 = g;
    g = _e5;
    f_1();
    return g_3;
}

```
```
==5408==ERROR: AddressSanitizer: heap-use-after-free on address 0x1241883fbc60 at pc 0x7ff9d7bd16f0 bp 0x0044881fc2a0 sp 0x0044881fc2e8
READ of size 1 at 0x1241883fbc60 thread T0
==5408==WARNING: Failed to use and restart external symbolizer!
==5408==*** WARNING: Failed to initialize DbgHelp!              ***
==5408==*** Most likely this means that the app is already      *** 
==5408==*** using DbgHelp, possibly with incompatible flags.    *** 
==5408==*** Due to technical reasons, symbolization might crash *** 
==5408==*** or produce wrong results.                           ***
    #0 0x7ff9d7bd16ef in llvm::ConstantFoldInstruction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\ConstantFolding.cpp:930
    #1 0x7ff9d79a6668 in llvm::SimplifyInstruction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\InstructionSimplify.cpp:4280
    #2 0x7ff9d79a98fd in replaceAndRecursivelySimplifyImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\InstructionSimplify.cpp:4474
    #3 0x7ff9d79a9438 in llvm::recursivelySimplifyInstruction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\InstructionSimplify.cpp:4501
    #4 0x7ff9d79876d3 in llvm::SimplifyInstructionsInBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\Local.cpp:451
    #5 0x7ff9d6d693b9 in `anonymous namespace'::SimplifyInst::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\DxilPreparePasses.cpp:126
    #6 0x7ff9d5d92fc4 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #7 0x7ff9d5d93a5e in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #8 0x7ff9d5d94715 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #9 0x7ff9d5d9da2c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #10 0x7ff9d57b0801 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #11 0x7ff9d5ec9511 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #12 0x7ff9d57ab4f2 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #13 0x7ff9d57b8c23 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #14 0x7ff9d5696b56 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #15 0x7ff9dd860a75 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #16 0x7ff9dd8c0f7e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #17 0x7ff9dd9692e4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:379
    #18 0x7ff9dd952b10 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:383
    #19 0x7ff9dd78ac50 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #20 0x7ff9dd6e4c7e in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2049
    #21 0x7ff9dd6e4681 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1363
    #22 0x7ff9ff786bad in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #23 0x7ff9ff182584 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606    
    #24 0x7ff9ff1878ac in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1642
    #25 0x7ff9fad5bdc2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:999
    #26 0x7ff9fad5c215 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1908
    #27 0x7ff9fad50041 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1853
    #28 0x7ff9eeb0e273 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #29 0x7ff9eb75fddc in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:507
    #30 0x7ff9eb75e883 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:155
    #31 0x7ff9eeb2c1c5 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:888
    #32 0x7ff9eeb3c52a in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #33 0x7ff9ee1554bc in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:740
    #34 0x7ff9ee1537e8 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:665
    #35 0x7ff9ee156b68 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #36 0x7ff9e96809e0 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #37 0x7ff9ecf85426 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #38 0x7ff9ecf84349 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #39 0x7ff9ecfba26e in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #40 0x7ff9ecf8715c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:641
    #41 0x7ff9e96cb7f0 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #42 0x7ff9ec4b2f7b in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:436
    #43 0x7ff9e7f950e2 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:771
    #44 0x7ff9e7f97663 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1146
    #45 0x7ff9e7f931aa in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:329
    #46 0x7ff9e7f93b6d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:342
    #47 0x7ff9db2016c3 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #48 0x7ff6bc4a43c6 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:180
    #49 0x7ff6bc4a1dc0 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #50 0x7ff6bc883913 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #51 0x7ffa35a37613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)
    #52 0x7ffa36d826a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x1241883fbc60 is located 96 bytes inside of 160-byte region [0x1241883fbc00,0x1241883fbca0)
freed by thread T0 here:
    #0 0x7ff6bc57f03d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ff9d59d3cbb in llvm::ICmpInst::~ICmpInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:1093
    #2 0x7ff9d6c291a1 in llvm::iplist<llvm::Instruction,llvm::ilist_traits<llvm::Instruction> >::clear C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\ADT\ilist.h:563
    #3 0x7ff9d6c28c42 in llvm::BasicBlock::~BasicBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:91
    #4 0x7ff9d6c2cadf in llvm::BasicBlock::~BasicBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:70
    #5 0x7ff9d798f1f1 in llvm::removeUnreachableBlocks C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\Local.cpp:1306
    #6 0x7ff9d6e5151d in simplifyFunctionCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\SimplifyCFGPass.cpp:155
    #7 0x7ff9d5d92fc4 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #8 0x7ff9d5d93a5e in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #9 0x7ff9d5d94715 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #10 0x7ff9d5d9da2c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #11 0x7ff9d57b0801 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #12 0x7ff9d5ec9511 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #13 0x7ff9d57ab4f2 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #14 0x7ff9d57b8c23 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #15 0x7ff9d5696b56 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #16 0x7ff9dd860a75 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #17 0x7ff9dd8c0f7e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #18 0x7ff9dd9692e4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:379
    #19 0x7ff9dd952b10 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:383
    #20 0x7ff9dd78ac50 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #21 0x7ff9dd6e4c7e in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2049
    #22 0x7ff9dd6e4681 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1363
    #23 0x7ff9ff786bad in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #24 0x7ff9ff182584 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #25 0x7ff9ff1878ac in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1642
    #26 0x7ff9fad5bdc2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:999
    #27 0x7ff9fad5c215 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1908

previously allocated by thread T0 here:
    #0 0x7ff6bc57f13d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ff9d81a51ce in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ff9d6c27d01 in llvm::User::operator new C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:96
    #3 0x7ff9d5bd0b3c in llvm::GetElementPtrInst::Create C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:866
    #4 0x7ff9d6b38198 in llvm::ConstantExpr::getAsInstruction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Constants.cpp:3065
    #5 0x7ff9d6dff0eb in ReplaceConstantWithInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:3288
    #6 0x7ff9d6dfc60e in ReplaceMemcpy C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:3534
    #7 0x7ff9d6df5543 in `anonymous namespace'::SROA_Helper::LowerMemcpy C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:3987
    #8 0x7ff9d6dd97e7 in `anonymous namespace'::SROAGlobalAndAllocas C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:1939
    #9 0x7ff9d6dc88c5 in `anonymous namespace'::SROA_Parameter_HLSL::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\ScalarReplAggregatesHLSL.cpp:4291
    #10 0x7ff9d5d94715 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #11 0x7ff9d5d9da2c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #12 0x7ff9d57b0801 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #13 0x7ff9d5ec9511 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #14 0x7ff9d57ab4f2 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #15 0x7ff9d57b8c23 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #16 0x7ff9d5696b56 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #17 0x7ff9dd860a75 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #18 0x7ff9dd8c0f7e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #19 0x7ff9dd9692e4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:379
    #20 0x7ff9dd952b10 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:383
    #21 0x7ff9dd78ac50 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #22 0x7ff9dd6e4c7e in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2049
    #23 0x7ff9dd6e4681 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1363
    #24 0x7ff9ff786bad in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #25 0x7ff9ff182584 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #26 0x7ff9ff1878ac in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1642
    #27 0x7ff9fad5bdc2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:999

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\ConstantFolding.cpp:930 in llvm::ConstantFoldInstruction
Shadow bytes around the buggy address:
  0x1241883fb980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1241883fba00: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00
  0x1241883fba80: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa
  0x1241883fbb00: fa fa f7 fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x1241883fbb80: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa f7 fa
=>0x1241883fbc00: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd
  0x1241883fbc80: fd fd fd fd fa fa fa fa fa fa f7 fa fd fd fd fd
  0x1241883fbd00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x1241883fbd80: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x1241883fbe00: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x1241883fbe80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
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

==5408==ADDITIONAL INFO

==5408==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ff9ee15398e in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:681
    #1 0x7ff9ee14c8e5 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:480


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==5408==END OF ADDITIONAL INFO
==5408==ABORTING
win32u!NtGdiDdDDIWaitForVerticalBlankEvent+0x14:
00007ffa`34d65cc4 c3              ret

```

## Attachments

- [indexSimplifyInst.html](attachments/indexSimplifyInst.html) (text/html, 3.9 KB)
- [Mon Apr 15 2024 10:09:14 GMT-0400 (Eastern Daylight Time).png](attachments/Mon Apr 15 2024 10_09_14 GMT-0400 (Eastern Daylight Time).png) (image/png, 88.8 KB)
- [x.patch](attachments/x.patch) (text/x-diff, 2.9 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-04-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5103977822617600.

### an...@chromium.org (2024-04-09)

Hi @amaiorano, I've kicked off a clusterfuzz run but am assigning to you in parallel because of similarities w/ <https://issues.chromium.org/331123811>. I've also set Severity and Priority based on that bug. Please feel free to re-route as necessary.

### an...@chromium.org (2024-04-09)

Setting FoundIn provisionally as M122 based on commit dates in SimplifyInstruction within InstructionSimplify.cpp.
@am...@google.com, please modify if this is incorrect. Thanks!

### dn...@google.com (2024-04-09)

I can't reproduce with DXC on Linux.
I've tried both debug and release builds, both with is\_asan=true

### wg...@gmail.com (2024-04-09)

Urgh I uploaded a wgsl shader instead of a hlsl for standalone reproducing.
So I compiled the above standalone wgsl shader via `./tint a.wgsl -o a.hlsl` and got the following hlsl file. Compiling this hlsl via `./dxc-3.7 a.hlsl -T ps_6_2` trigger should trigger the ASAN violation.

```
static int g[10] = (int[10])0;
static int g_1[10] = (int[10])0;
static float4 g_3 = float4(0.0f, 0.0f, 0.0f, 0.0f);
ByteAddressBuffer g_2 : register(t0);

void f_1() {
  int l_5 = 0;
  int l_6 = 0;
  float l_7 = 0.0f;
  bool l_8 = true;
  l_5 = 0;
  l_6 = 0;
  while (true) {
    bool x_133_ = (l_6 < 10);
    uint x_135_ = g_2.Load(0u);
    if (!((x_135_ <= 1u))) {
      l_7 = 0.0f;
    } else {
      return;
    }
    if (x_133_) {
    } else {
      break;
    }
    int x_140_ = l_6;
    int x_141_ = l_6;
    int x_143_ = g[x_141_];
    g_1[x_140_] = x_143_;
    {
      int x_145_ = l_6;
      l_6 = (x_145_ + 1);
    }
  }
  l_7 = float(g[0]);
  g_3 = float4(l_7, 0.0f, 0.0f, 0.0f);
}

struct tint_symbol {
  float4 value : SV_Target0;
};

float4 main_inner() {
  f_1();
  bool _e9 = false;
  while (true) {
    {
      if (_e9) { break; }
    }
  }
  int _e5[10] = g;
  g = _e5;
  f_1();
  return g_3;
}

tint_symbol main() {
  float4 inner_result = main_inner();
  tint_symbol wrapper_result = (tint_symbol)0;
  wrapper_result.value = inner_result;
  return wrapper_result;
}

```

### dn...@google.com (2024-04-09)

Ok, thanks.
I can reproduce now. The compilation succeeds when compiling the vertex shader
But when compiling the fragment shader, -T ps\_6\_0 is sufficent, then an assert fails

xc: ../../third\_party/dxc/lib/IR/Constants.cpp:1379: static ConstantAggregateZero \*llvm::ConstantAggregateZero::get(Type \*): Assertion `(Ty->isStructTy() || Ty->isArrayTy() || Ty->isVectorTy()) && "Cannot create an aggregate zero of non-aggregate type!"' failed.
Aborted

This reproduces on Linux.

### dn...@google.com (2024-04-09)

Here's a reduced HLSL case. The trouble looks like it's around the assignment from and to `g`.

```
static int g[10] = (int[10])0;
static int g_1[10] = (int[10])0;
static float4 g_3 = float4(0.0f, 0.0f, 0.0f, 0.0f);
ByteAddressBuffer g_2 : register(t0);

struct tint_symbol {
  float4 value : SV_Target0;
};

float4 frag_main_inner() {
  for (int i = 0; i < 10; i++) {
    g_1[i] = g[i];
  }
  int _e5[10] = g;
  g = _e5;
  return g_3;
}

tint_symbol frag_main() {
  float4 inner_result = frag_main_inner();
  tint_symbol wrapper_result = (tint_symbol)0;
  wrapper_result.value = inner_result;
  return wrapper_result;
}

```

### dn...@google.com (2024-04-09)

Stack trace:

```
#0  __pthread_kill_implementation (threadid=<optimized out>, signo=signo@entry=6, no_tid=no_tid@entry=0) at ./nptl/pthread_kill.c:44
#1  0x00007ffff796c1cf in __pthread_kill_internal (signo=6, threadid=<optimized out>) at ./nptl/pthread_kill.c:78
#2  0x00007ffff791e472 in __GI_raise (sig=sig@entry=6) at ../sysdeps/posix/raise.c:26
#3  0x00007ffff79084b2 in __GI_abort () at ./stdlib/abort.c:79
#4  0x00007ffff79083d5 in __assert_fail_base (fmt=0x7ffff7a7cdc8 "%s%s%s:%u: %s%sAssertion `%s' failed.\n%n", 
    assertion=assertion@entry=0x7fffed11ec40 <str> "(Ty->isStructTy() || Ty->isArrayTy() || Ty->isVectorTy()) && \"Cannot create an aggregate zero of non-aggregate type!\"", file=file@entry=0x7fffed11cd80 <str> "../../third_party/dxc/lib/IR/Constants.cpp", line=line@entry=1379, 
    function=function@entry=0x7fffed11ece0 <__PRETTY_FUNCTION__._ZN4llvm21ConstantAggregateZero3getEPNS_4TypeE> "static ConstantAggregateZero *llvm::ConstantAggregateZero::get(Type *)") at ./assert/assert.c:92
#5  0x00007ffff79173a2 in __assert_fail (
    assertion=0x7fffed11ec40 <str> "(Ty->isStructTy() || Ty->isArrayTy() || Ty->isVectorTy()) && \"Cannot create an aggregate zero of non-aggregate type!\"", file=0x7fffed11cd80 <str> "../../third_party/dxc/lib/IR/Constants.cpp", line=1379, 
    function=0x7fffed11ece0 <__PRETTY_FUNCTION__._ZN4llvm21ConstantAggregateZero3getEPNS_4TypeE> "static ConstantAggregateZero *llvm::ConstantAggregateZero::get(Type *)") at ./assert/assert.c:101
#6  0x00007ffff2d608b1 in llvm::ConstantAggregateZero::get(llvm::Type*) () at ../../third_party/dxc/lib/IR/Constants.cpp:1378
#7  0x00007ffff3b3b99c in ReplaceUseOfZeroInit(llvm::Instruction*, llvm::Value*, llvm::DominatorTree&, llvm::SmallPtrSet<llvm::BasicBlock*, 8u>&) () at ../../third_party/dxc/lib/Transforms/Scalar/ScalarReplAggregatesHLSL.cpp:3696
#8  0x00007ffff3b3b93b in ReplaceUseOfZeroInit(llvm::Instruction*, llvm::Value*, llvm::DominatorTree&, llvm::SmallPtrSet<llvm::BasicBlock*, 8u>&) () at ../../third_party/dxc/lib/Transforms/Scalar/ScalarReplAggregatesHLSL.cpp:3693
#9  0x00007ffff3b392fa in ReplaceUseOfZeroInitBeforeDef(llvm::Instruction*, llvm::GlobalVariable*) ()
    at ../../third_party/dxc/lib/Transforms/Scalar/ScalarReplAggregatesHLSL.cpp:3733
#10 0x00007ffff3b32ccd in (anonymous namespace)::SROA_Helper::LowerMemcpy(llvm::Value*, hlsl::DxilFieldAnnotation*, hlsl::DxilTypeSystem&, llvm::DataLayout const&, llvm::DominatorTree*, bool) () at ../../third_party/dxc/lib/Transforms/Scalar/ScalarReplAggregatesHLSL.cpp:3934
#11 0x00007ffff3b223ac in (anonymous namespace)::SROAGlobalAndAllocas(hlsl::HLModule&, bool) ()
    at ../../third_party/dxc/lib/Transforms/Scalar/ScalarReplAggregatesHLSL.cpp:1939
#12 0x00007ffff3b16874 in (anonymous namespace)::SROA_Parameter_HLSL::runOnModule(llvm::Module&) ()
    at ../../third_party/dxc/lib/Transforms/Scalar/ScalarReplAggregatesHLSL.cpp:4291
#13 0x00007ffff2fad714 in (anonymous namespace)::MPPassManager::runOnModule(llvm::Module&) ()
    at ../../third_party/dxc/lib/IR/LegacyPassManager.cpp:1669
#14 0x00007ffff2facb94 in llvm::legacy::PassManagerImpl::run(llvm::Module&) () at ../../third_party/dxc/lib/IR/LegacyPassManager.cpp:1771
#15 0x00007ffff2fae7a6 in llvm::legacy::PassManager::run(llvm::Module&) () at ../../third_party/dxc/lib/IR/LegacyPassManager.cpp:1814
#16 0x00007fffef26f6c2 in (anonymous namespace)::EmitAssemblyHelper::EmitAssembly(clang::BackendAction, llvm::raw_pwrite_stream*) ()
    at ../../third_party/dxc/tools/clang/lib/CodeGen/BackendUtil.cpp:756

```

### dn...@google.com (2024-04-09)

I've made good progress.
The bug is in DXC-specific pass ScalarReplAggregatesHLSL.cpp

The relevant part of the modules are:

1. a global array @g:

```
@g = internal global [10 x i32] zeroinitializer, align 4

```

2.
Before the end of the loop there is only one read from @g. Here %3 gets the value `g[i]`.
Since g is zero initialized, and there are no possible intervening stores to g, then the value of %3 should be i32 0.
This pass means to replace uses of %3 with i32 0.

```
for.body.i:                                       ; preds = %for.cond.i
  %2 = load i32, i32* %i.i, align 4, !dbg !18, !tbaa !10 ; line:12 col:16
  %arrayidx.i = getelementptr inbounds [10 x i32], [10 x i32]* @g, i32 0, i32 %2, !dbg !19 ; line:12 col:14
  %3 = load i32, i32* %arrayidx.i, align 4, !dbg !19, !tbaa !10 ; line:12 col:14

```

3. There's a third relevant part of the module. In the last block of the function we have:

```
"\01?frag_main_inner@@YA?AV?$vector@M$03@@XZ.exit": ; preds = %for.cond.i
  %6 = bitcast [10 x i32]* %_e5.i to i8*, !dbg !24 ; line:14 col:17
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %6, i8* bitcast ([10 x i32]* @g to i8*), i64 40, i32 1, i1 false) #0, !dbg !24 ; line:14 col:17
  %7 = bitcast [10 x i32]* %_e5.i to i8*, !dbg !25 ; line:15 col:7
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* bitcast ([10 x i32]* @g to i8*), i8* %7, i64 40, i32 1, i1 false) #0, !dbg !25 ; line:15 col:7
...

```

That second memcpy uses @g as the source of the memcpy. The HLSL replacement-of-aggregates pass spots that, sees that @g is zero-initialized, and starts traversing all uses of `@g` in the function, looking for opportunities to replace those uses with zeros.
That's how it finds that initial use of @g in section 1 noted above.

The traversal occurs by a call to ReplaceUsesOfZerInit(I, V, ...) where I is the initial memcpy instruction triggering the search, V is the globalValue that is @g's declaration.

This is the code, around line 3669 of ScalarReplAggregatesHLSL.cpp:

```
// If a V user is dominated by memcpy (I),
//    skip it - memcpy dest can simply alias to src for this user.
// If the V user may follow the memcpy (I),
//    return false - memcpy dest not safe to replace with src.
// Otherwise,
//    replace use with zeroinitializer.
static bool ReplaceUseOfZeroInit(Instruction *I, Value *V, DominatorTree &DT,
                                 SmallPtrSet<BasicBlock *, 8> &Reachable) {
  BasicBlock *BB = I->getParent();
  Function *F = I->getParent()->getParent();
  for (auto U = V->user_begin(); U != V->user_end();) {
    Instruction *UI = dyn_cast<Instruction>(*(U++));
    if (!UI || UI == I)
      continue;
    if (UI->getParent()->getParent() != F)
      continue;

    // Skip properly dominated users
    if (DT.properlyDominates(BB, UI->getParent()))
      continue;

    // If user is found in memcpy successor list
    // then the user is not safe to replace with zeroinitializer.
    if (Reachable.count(UI->getParent()))
      return false;

    // Remaining cases are where I:
    // - is at the end of the same block
    // - does not precede UI on any path
    if (isa<GetElementPtrInst>(UI) || isa<BitCastInst>(UI)) {
      if (ReplaceUseOfZeroInit(I, UI, DT, Reachable))
        continue;
    } else if (LoadInst *LI = dyn_cast<LoadInst>(UI)) {
      LI->replaceAllUsesWith(ConstantAggregateZero::get(LI->getType())); /// problem is HERE!
      LI->eraseFromParent();
      continue;
    }
    return false;
  }
  return true;
}


```

The bug occurs because, while walking the users of V (a.k.a. @G), it finds the array index calculation:

```
  %arrayidx.i = getelementptr inbounds [10 x i32], [10 x i32]* @g, i32 0, i32 %2, !dbg !19 ; line:12 col:14

```

It sees it's a GEP, and takes the recursion path, calling ReplaceUsesOfZeroInit(the memcpy, the gep, ...)
Then it traverses the uses of %arrayidx.i, and finds the load instruction on the next line:

```
  %3 = load i32, i32* %arrayidx.i, align 4, !dbg !19, !tbaa !10 ; line:12 col:14

```

And then it tries to create a ConstantAggregateZero of the result type of the load, but that's i32, and CAZ isn't allowed to create a scalar type. So the assert fails.

The fix

### dn...@google.com (2024-04-09)

I've posted a fix upstream: <https://github.com/microsoft/DirectXShaderCompiler/pull/6516>

### pe...@google.com (2024-04-10)

Setting milestone because of s0/s1 severity.

### am...@google.com (2024-04-15)

dneto@ I tested opening the originally attached file `indexSimplifyInst.html` in latest Canary `Version 125.0.6420.0 (Official Build) canary (64-bit)`, and unfortunately the GPU process crash still reproduces. I verified, and Canary includes your fix: [this is the 6420 branch in Dawn](https://dawn.googlesource.com/dawn/+log/refs/heads/chromium/6420), and it includes [this roll of DXC](https://dawn.googlesource.com/dawn/+/0e14373fbbebb5feaa83a5584e96dd818aba7b7f) that includes your fix.

### am...@google.com (2024-04-15)

Using the latest precompiled asan build of Chrome `chromium-125.0.6420.0-win64-asan` and opening `indexSimplifyInst.html`, I get the exact call stack in the bug description, which is not the same as the one shared in [#comment9](https://issues.chromium.org/issues/333414294#comment9), which probably means a different bug was fixed.

Here's as slightly more detailed callstack from Visual Studio that includes inlined frames:

```
 	chrome.exe!__sanitizer::internal__exit(int exitcode=1) Line 843	C++
 	chrome.exe!__sanitizer::Die() Line 59	C++
 	chrome.exe!__asan::ScopedInErrorReport::~ScopedInErrorReport() Line 193	C++
 	chrome.exe!__asan::ReportGenericError(unsigned __int64 pc, unsigned __int64 bp, unsigned __int64 sp, unsigned __int64 addr, bool is_write, unsigned __int64 access_size=1, unsigned int fatal, bool) Line 498	C++
 	chrome.exe!__asan_report_load1(unsigned __int64 addr) Line 128	C++
 	[Inline Frame] dxcompiler.dll!llvm::Value::getValueID() Line 374	C++
 	[Inline Frame] dxcompiler.dll!llvm::isa_impl<llvm::Constant,llvm::Value,void>::doit(const llvm::Value &) Line 655	C++
 	[Inline Frame] dxcompiler.dll!llvm::isa_impl_cl<llvm::Constant,llvm::Value *>::doit() Line 83	C++
 	[Inline Frame] dxcompiler.dll!llvm::isa_impl_wrap<llvm::Constant,llvm::Value *,llvm::Value *>::doit(llvm::Value * const &) Line 123	C++
 	[Inline Frame] dxcompiler.dll!llvm::isa_impl_wrap<llvm::Constant,const llvm::Use,llvm::Value *>::doit(const llvm::Use &) Line 113	C++
 	[Inline Frame] dxcompiler.dll!llvm::isa(const llvm::Use &) Line 134	C++
 	[Inline Frame] dxcompiler.dll!llvm::dyn_cast(llvm::Use &) Line 294	C++
>	dxcompiler.dll!llvm::ConstantFoldInstruction(llvm::Instruction *) Line 935	C++
 	dxcompiler.dll!llvm::SimplifyInstruction(llvm::Instruction *) Line 4280	C++
 	dxcompiler.dll!replaceAndRecursivelySimplifyImpl(llvm::Instruction *) Line 4474	C++
 	dxcompiler.dll!llvm::recursivelySimplifyInstruction(llvm::Instruction *) Line 4501	C++
 	dxcompiler.dll!llvm::SimplifyInstructionsInBlock(llvm::BasicBlock *) Line 451	C++
 	dxcompiler.dll!`anonymous namespace'::SimplifyInst::runOnFunction(llvm::Function &) Line 124	C++
 	dxcompiler.dll!llvm::FPPassManager::runOnFunction(llvm::Function &) Line 1587	C++
 	dxcompiler.dll!llvm::FPPassManager::runOnModule(llvm::Module &) Line 1609	C++
 	[Inline Frame] dxcompiler.dll!`anonymous namespace'::MPPassManager::runOnModule(llvm::Module &) Line 1669	C++
 	dxcompiler.dll!llvm::legacy::PassManagerImpl::run(llvm::Module &) Line 1771	C++
 	[Inline Frame] dxcompiler.dll!`anonymous namespace'::EmitAssemblyHelper::EmitAssembly(clang::BackendAction) Line 756	C++
 	dxcompiler.dll!clang::EmitBackendOutput(clang::DiagnosticsEngine &) Line 779	C++
 	dxcompiler.dll!clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext &) Line 195	C++
 	dxcompiler.dll!clang::ParseAST(clang::Sema &) Line 164	C++
 	dxcompiler.dll!clang::CodeGenAction::ExecuteAction() Line 807	C++
 	dxcompiler.dll!clang::FrontendAction::Execute() Line 468	C++
 	dxcompiler.dll!DxcCompiler::Compile(const DxcBuffer *) Line 982	C++
 	[Inline Frame] chrome.dll!dawn::native::d3d::`anonymous namespace'::CompileShaderDXC(const dawn::native::d3d::D3DBytecodeCompilationRequest &) Line 155	C++
 	chrome.dll!dawn::native::d3d::CompileShader(dawn::native::d3d::D3DCompilationRequest) Line 355	C++

```

### am...@google.com (2024-04-19)

Update: investigated this today, and am getting closer to understanding the root cause. See [investigation doc here](https://docs.google.com/document/d/1J4OnAHxNIRs24cigJtDcOpL2q6Plt69SvOKGSQ0tQS8/edit?usp=sharing).

### dn...@google.com (2024-04-20)

I have a fix. I've attached a patch to the DXC sources.

The bug is in ReplaceConstantWIthInst(Constant \*C, Value \*V, Builder..)

Here's the relevant IR:

```
while.end.i:                                      ; preds = %while.body.i
  %10 = bitcast [10 x i32]* %arr1_copy.i to i8*, !dbg !33
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %10, i8* bitcast ([10 x i32]* @arr1 to i8*), i64 40, i32 1, i1 false) #0, !dbg !33
  %11 = bitcast [10 x i32]* %arr1_copy.i to i8*, !dbg !34
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* bitcast ([10 x i32]* @arr1 to i8*), i8* %11, i64 40, i32 1, i1 false) #0, !dbg !34
  store i32 0, i32* %i.i.1.i, align 4, !dbg !35, !tbaa !12
  %12 = load %struct.ByteAddressBuffer, %struct.ByteAddressBuffer* @"\01?buff@@3UByteAddressBuffer@@A", !dbg !37

```

There are two memcpys. (dest is first arg, src is second arg)

- ReplaceMemcpy(Value=@arr1,Src=%11) tries to replace the second memcpy:
  roughly memcpy(@arr1, %11)
  a.k.a. memcpy(@arr1, %arr1\_copy.i), where %arr1\_copy.i is the function-local array variable.
- It sees that Value is a constant (because its the address of global var @arr)
- It sees that Src is not a constant, because it's the result of an alloca (a.k.a. stack variable address)
- So it falls into the code path with the comment  `// Replace Constant with a non-Constant.` and calls ReplaceConstantWithInst

Now let's enter ReplaceConstantWithInst(C=@arr, V=%arr1\_copy.i).
Its job is to replace uses of C, in the current function, with the value V.
It traverses the uses of C, skipping over any that aren't in the current function (i.e. the function containing the instruction that generates V).
If such a use C is an instruction I, then it replaces uses of C in I with V.
Remember C=@arr, and one of the uses is the *first* memcpy: memcpy(bitcast of %arr1\_copy.i, bitcast of @arr).

After these replacements, the first part of that basic block is this:

```
while.end.i:                                      ; preds = %while.body.i
  %10 = bitcast [10 x i32]* %arr1_copy.i to i8*, !dbg !32
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %10, i8* %12, i64 40, i32 1, i1 false) #0, !dbg !32
  %11 = bitcast [10 x i32]* %arr1_copy.i to i8*, !dbg !33
  %12 = bitcast [10 x i32]* %arr1_copy.i to i8*, !dbg !33
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %12, i8* %11, i64 40, i32 1, i1 false) #0, !dbg !33
  store i32 0, i32* %i.i.1.i, align 4, !dbg !34, !tbaa !12

```

We see that %12 is in the first memcpy, but defined two instructions later. That's bad.

The bug is in this statement: If such a use C is an instruction I, then it replaces uses of C in I with V.
That's only safe to do if V dominates I.

So the fix uses a big hammer: compute the dominator tree so we can guard the replacement with that dominance check.

Now, it could be heavyweight to recompute the dominator tree repeatedly, but it's the safe thing to do.

Earlier in the code it says

> ```
>  // SROA_Parameter_HLSL has no access to a domtree, if one is needed, it'll
>  // be generated
> 
> ```

So it seems in the spirit to compute the dominator tree on demand in this pass.

Note that early in ReplaceMemcpy, it has a promising comment and mechanism to early-out:

```
  // If the source of the memcpy (Src) doesn't dominate all users of dest (V),
  // full replacement isn't possible without complicated PHI insertion
  // This will likely replace with ld/st which will be replaced in mem2reg
  if (Instruction *SrcI = dyn_cast<Instruction>(Src))
    if (!DominateAllUsers(SrcI, V, DT))
      return false;

```

But DominateAllUsers doesn't quite do the job for us. It calls DominateAllUsersDom (where it has a dominator tree), and it does this code:

```
// Use `DT` to trace all users and make sure `I`'s BB dominates them all
static bool DominateAllUsersDom(Instruction *I, Value *V, DominatorTree *DT) {
  BasicBlock *BB = I->getParent();
  Function *F = I->getParent()->getParent();
  for (auto U = V->user_begin(); U != V->user_end();) {
    Instruction *UI = dyn_cast<Instruction>(*(U++));
    // If not an instruction or from a differnt function, nothing to check, move
    // along.
    if (!UI || UI->getParent()->getParent() != F)
      continue;

    if (!DT->dominates(BB, UI->getParent()))
      return false;
      
    if (isa<GetElementPtrInst>(UI) || isa<BitCastInst>(UI)) {
      if (!DominateAllUsersDom(I, UI, DT))
        return false;
    }
  }
  return true;
}

```

First, in our case value V is a constant (`@arr`), and its use in the first memcpy is `i8* bitcast ([10 x i32]* @arr1 to i8*` which is itself an llvm::Constant. So it early outs because UI here is null because that llvm::Constant is not an instruction. So I think it returns true, and that's why we get into trouble later.

One local fix here could be if the use is a constant, then recurse and follow the users of that enclosing constant, until you hit an instruction. This has a problem that it could blow up the search.

And even if you got out far enough to reach an instruction you would get to the first memcpy.
And then the test `if (!DT->dominates(BB, UI->getParent()))` only compares at a basic block level. But both memcpys are in the same basic block, and a node always dominates itself. So again it would decide incorrectly. You have to check dominance on an instruction level.

So all told I think computing the patch does a correct and safe thing. We could go with this.

When you apply the patch, we end up with DXC emitting the error that a loop doesn't have a break. That's true after all the constant folding occurs, and a safe result.

### dn...@google.com (2024-04-20)

With the patch, this is the error:

```
$ dxc x.hlsl -E main -T ps_6_0
warning: Declared output SV_Target0 not fully written in shader. [-Winline-asm]
warning: DXIL signing library (dxil.dll,libdxil.so) not found.  Resulting DXIL will not be signed for use in release environments.

error: validation errors
x.hlsl:32: error: Loop must have break.
Validation failed.

```

### am...@google.com (2024-04-22)

I tested David's patch, and made some two changes:

1. Lazily compute the dominator tree only when absolutely necessary
2. Correctly return `bReplacedAll` when recursing in `ReplaceConstantWithInst`.

I also wrote two tests. I've put up the PR for this upstream: <https://github.com/microsoft/DirectXShaderCompiler/pull/6556>

### am...@google.com (2024-04-29)

Update: the [PR](https://github.com/microsoft/DirectXShaderCompiler/pull/6556) is still in progress. Greg Roth from Microsoft has asked for some clarification, which I provided, and he is still evaluating the change.

### am...@google.com (2024-05-06)

Discussed with Microsoft in a meeting today. Greg Roth said he would approve the PR, so this should land soon. Then this will roll into Dawn, then Dawn into Chromium, where we can test Canary.

### am...@google.com (2024-05-06)

The [upstream PR has been merged](https://github.com/microsoft/DirectXShaderCompiler/pull/6556). Now waiting for roll into Dawn, then Dawn into Chromium, to test the fix in Canary.

### am...@google.com (2024-05-08)

Tested Canary Version 126.0.6466.0 (Official Build) canary (64-bit) by opening `indexSimplifyInst.html` and it now no longer crashes.

Dawn CL that has rolled into Chromium: <https://dawn.googlesource.com/dawn.git/+/a35bac7ac6186eefd258ec15b4d29945485d0352>

### pe...@google.com (2024-05-08)

This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M124. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@google.com (2024-05-08)

1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://dawn-review.googlesource.com/c/dawn/+/187301>

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes

3. Does this fix pose any potential non-verifiable stability risks?

No

4. Does this fix pose any known compatibility risks?

No

5. Does it require manual verification by the test team? If so, please describe required testing.

Yes. Open `indexSimplifyInst.html` attached to this bug.

### ap...@google.com (2024-05-08)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6422

commit 18584a7628918724949cce6d4f879c3d34a5d722
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Wed May 08 13:41:43 2024

    Fix invalid IR from scalarrepl-param-hlsl in ReplaceConstantWithInst (#6556)
    
    ReplaceConstantWithInst(C, V) replaces uses of C in the current function
    with V. If such a use C is an instruction I, the it replaces uses of C
    in I with V. However, this function did not make sure to only perform
    this replacement if V dominates I. As a result, it may end up replacing
    uses of C in instructions before the definition of V.
    
    The fix is to lazily compute the dominator tree in
    ReplaceConstantWithInst so that we can guard the replacement with that
    dominance check.
    
    Bug: chromium:333414294
    Change-Id: I010e63d93a92a6e3eee637a0827ab9821eaf9745
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5526975
    Reviewed-by: dan sinclair <dsinclair@google.com>
    Reviewed-by: James Price <jrprice@google.com>

M       lib/Transforms/Scalar/ScalarReplAggregatesHLSL.cpp
A       tools/clang/test/DXC/Passes/ScalarReplHLSL/scalarrepl-param-hlsl-const-to-local-and-back.hlsl
A       tools/clang/test/DXC/Passes/ScalarReplHLSL/scalarrepl-param-hlsl-const-to-local-and-back.ll
M       tools/clang/test/DXC/Passes/ScalarReplHLSL/scalarrepl-param-hlsl-replace-zero-recurse-to-float.ll
M       tools/clang/test/DXC/Passes/ScalarReplHLSL/scalarrepl-param-hlsl-replace-zero-recurse-to-int.ll

https://chromium-review.googlesource.com/5526975


### ap...@google.com (2024-05-08)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6367

commit 2a434fd0af6bbcaa6da648f51b696a33a6bcdd04
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Wed May 08 13:38:38 2024

    Fix invalid IR from scalarrepl-param-hlsl in ReplaceConstantWithInst (#6556)
    
    ReplaceConstantWithInst(C, V) replaces uses of C in the current function
    with V. If such a use C is an instruction I, the it replaces uses of C
    in I with V. However, this function did not make sure to only perform
    this replacement if V dominates I. As a result, it may end up replacing
    uses of C in instructions before the definition of V.
    
    The fix is to lazily compute the dominator tree in
    ReplaceConstantWithInst so that we can guard the replacement with that
    dominance check.
    
    Bug: chromium:333414294
    Change-Id: I2a8bf64094298b49a1887cc7c1334e91a745c396
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5525429
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: dan sinclair <dsinclair@google.com>

M       lib/Transforms/Scalar/ScalarReplAggregatesHLSL.cpp
A       tools/clang/test/DXC/Passes/ScalarReplHLSL/scalarrepl-param-hlsl-const-to-local-and-back.hlsl
A       tools/clang/test/DXC/Passes/ScalarReplHLSL/scalarrepl-param-hlsl-const-to-local-and-back.ll

https://chromium-review.googlesource.com/5525429


### am...@chromium.org (2024-05-09)

Hi amaiorano@ -- I've reached out to you directly about the backports for this fix based on the minimal bake time of the Dawn -> Chromium roll with the fix on Canary and lacking review/approval.

### am...@google.com (2024-05-09)

Hi Amy, as discussed offline, I've reverted the [CL for M124](https://dawn-review.googlesource.com/c/dawn/+/187600). Sorry about that. Let me know if we need to do the same for M125.

In the meantime, I will wait for you, or someone from your team, to let me know when we can merge this fix into Chromium.

### pg...@google.com (2024-05-14)

deleted

### am...@chromium.org (2024-05-14)

Hi Antonio -- since there do not appear to be any issues in 125 since the merge or 126 Canary or Dev since the original fix was rolled into Chromium, and is in and will be shipped tomorrow in 125, you are free to reland <https://dawn-review.googlesource.com/c/dawn/+/187600> to 6367 whenever you are ready. Thank you!

### ap...@google.com (2024-05-15)

Project: dawn
Branch: chromium/6367

commit 2ea615d914b17fa882c0bb50eab29216edb5075e
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu May 09 02:01:27 2024

    Revert "DEPS: Update DXC to patched branch"
    
    This reverts commit 65b347768990e33267382a584405c5c12e2f56e7.
    
    Reason for revert: Needs approval from Chrome security team.
    
    Original change's description:
    > DEPS: Update DXC to patched branch
    >
    > Bug: chromium:333414294
    > Change-Id: Ib44b9623aaec8b836a31c0a89c2800d476ee6700
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/187481
    > Reviewed-by: dan sinclair <dsinclair@google.com>
    > Commit-Queue: Antonio Maiorano <amaiorano@google.com>
    
    TBR=dsinclair@chromium.org,bclayton@google.com,jrprice@google.com,amaiorano@google.com,dawn-scoped@luci-project-accounts.iam.gserviceaccount.com,dsinclair@google.com
    
    Change-Id: Ic960cba4bbe0d3495e3c06bd3bae615016baf522
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Bug: chromium:333414294
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/187600
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>
    Commit-Queue: Antonio Maiorano <amaiorano@google.com>
    Reviewed-by: James Price <jrprice@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/187600


### sp...@google.com (2024-05-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
$10,000 for this report of memory corruption in the GPU process 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### ap...@google.com (2024-05-16)

Project: dawn
Branch: chromium/6367

commit fd7470f7565fd49ea470a7a93a21c6b3ef3fb0d8
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu May 16 00:27:50 2024

    Reland "DEPS: Update DXC to patched branch"
    
    This reverts commit 2ea615d914b17fa882c0bb50eab29216edb5075e.
    
    Reason for revert: Chrome Security team has given the thumbs up to reland this.
    
    Original change's description:
    > Revert "DEPS: Update DXC to patched branch"
    >
    > This reverts commit 65b347768990e33267382a584405c5c12e2f56e7.
    >
    > Reason for revert: Needs approval from Chrome security team.
    >
    > Original change's description:
    > > DEPS: Update DXC to patched branch
    > >
    > > Bug: chromium:333414294
    > > Change-Id: Ib44b9623aaec8b836a31c0a89c2800d476ee6700
    > > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/187481
    > > Reviewed-by: dan sinclair <dsinclair@google.com>
    > > Commit-Queue: Antonio Maiorano <amaiorano@google.com>
    >
    > TBR=dsinclair@chromium.org,bclayton@google.com,jrprice@google.com,amaiorano@google.com,dawn-scoped@luci-project-accounts.iam.gserviceaccount.com,dsinclair@google.com
    >
    > Change-Id: Ic960cba4bbe0d3495e3c06bd3bae615016baf522
    > No-Presubmit: true
    > No-Tree-Checks: true
    > No-Try: true
    > Bug: chromium:333414294
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/187600
    > Reviewed-by: Antonio Maiorano <amaiorano@google.com>
    > Commit-Queue: Antonio Maiorano <amaiorano@google.com>
    > Reviewed-by: James Price <jrprice@google.com>
    
    # Not skipping CQ checks because original CL landed > 1 day ago.
    
    Bug: chromium:333414294
    Change-Id: Iae0cdddee59d155aa2982d9f689a4ff922a3bf61
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/188461
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>
    Commit-Queue: Antonio Maiorano <amaiorano@google.com>
    Reviewed-by: James Price <jrprice@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/188461


### am...@google.com (2024-05-16)

Hi [amyressler@chromium.org](mailto:amyressler@chromium.org), I've [relanded the patch to Dawn's 6367 branch](https://dawn-review.googlesource.com/c/dawn/+/188461) and it has been [merged into chromium's 6367 branch](https://chromium.googlesource.com/chromium/src.git/+/c42f4eb4280d1b8fdc6853635c12307254820679).

### pe...@google.com (2024-08-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $10,000 for this report of memory corruption in the GPU process 
> 
> Thank you for your efforts and helping us make Chrome more secure for all users!
> 
> Cheers,
> Chrome VRP Panel Bot
> 
> 
> P.S. Two other things we'd like to mention:
> 
> * Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do 

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/333414294)*
