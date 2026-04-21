#  GPU process crash via WebGPU shader - UAF in combineInstructionsOverFunction at InstructionCombining.cpp:3008

| Field | Value |
|-------|-------|
| **Issue ID** | [342545100](https://issues.chromium.org/issues/342545100) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2024-05-24 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this triggers an UAF inside the hlsl compiler.

##### VERSION

Chrome Version: Pre-compiled ASAN Chromium 127.0.6500.0 (Developer Build) (64-bit)  

Operating System: Win10 Build 19045.4291

##### REPRODUCTION CASE

Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process. Note that the crash does NOT manifest on machines which support the 6.6 shader model.

Reproducing the issue stand-alone on Linux also possible:

- Compile the standalone.wgsl with tint (commit 06b3046a76049cf638a11e791b2b727df47e5a04) to hlsl via `./tint standalone.wgsl -o standalone.hlsl`. I also attached standalone.hlsl, but you should get the very same file when compiling standalone.wgsl yourself
- Compile the hlsl with dxc (commit cdc56031b562359967ea440060a110a388d8f782): `./dxc-3.7 standalone.hlsl -T cs_6_2`. This should trigger an ASAN violation. Setting the shader model to `cs_6_6` prevents the UAF.

##### Attached:

- html that triggers an ASAN violation in chromium
- wgsl for producing the hlsl shader
- the hlsl shader
- asan log file

```
[7248:2100:0524/135757.672:INFO:CONSOLE(20)] "[object GPUDevice]", source: file://vboxsvr/shared/indexAddReachableCodeToWorklist.html (20)
=================================================================
==3768==ERROR: AddressSanitizer: heap-use-after-free on address 0x11927a004348 at pc 0x7ffca73114a0 bp 0x0042685fc0c0 sp 0x0042685fc108
READ of size 1 at 0x11927a004348 thread T0
==3768==WARNING: Failed to use and restart external symbolizer!
==3768==*** WARNING: Failed to initialize DbgHelp!              ***
==3768==*** Most likely this means that the app is already      *** 
==3768==*** using DbgHelp, possibly with incompatible flags.    *** 
==3768==*** Due to technical reasons, symbolization might crash *** 
==3768==*** or produce wrong results.                           ***
    #0 0x7ffca731149f in combineInstructionsOverFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\InstCombine\InstructionCombining.cpp:3008
    #1 0x7ffca7313678 in `anonymous namespace'::InstructionCombiningPass::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\InstCombine\InstructionCombining.cpp:3104
    #2 0x7ffca6078064 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #3 0x7ffca6078afe in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #4 0x7ffca60797b5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #5 0x7ffca6082b4c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:781
    #6 0x7ffca5a90921 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #7 0x7ffca61ae5a1 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #8 0x7ffca5a8b612 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #9 0x7ffca5a98de3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #10 0x7ffca5976c13 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #11 0x7ffcae33c559 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #12 0x7ffcae39fe7e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #13 0x7ffcae441794 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #14 0x7ffcae405ffc in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:87
    #15 0x7ffcae257330 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #16 0x7ffcae1a7da1 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2035
    #17 0x7ffcae1a7787 in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1300
    #18 0x7ffcd076567d in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #19 0x7ffcd01b5494 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477   
    #20 0x7ffcd01bd7dd in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1652
    #21 0x7ffccbccc572 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1020
    #22 0x7ffccbccc9c5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1924
    #23 0x7ffccbcc0cf1 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1869
    #24 0x7ffcbf970fc3 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #25 0x7ffcbc52109c in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:506
    #26 0x7ffcbc51fb43 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:154
    #27 0x7ffcbf98ee6a in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:930
    #28 0x7ffcbf99ff4a in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&,unsigned long long &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams>,unsigned long long>,void ()>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams>,unsigned long long>,0,1,2> C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1067
    #29 0x7ffcbefd5e2d in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:743
    #30 0x7ffcbefd41f8 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:668
    #31 0x7ffcbefd7385 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #32 0x7ffcba47ef10 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #33 0x7ffcbddfb9ce in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #34 0x7ffcbddfa8d9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #35 0x7ffcbde2ffde in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #36 0x7ffcbddfd61c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:645
    #37 0x7ffcba4c8ac0 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #38 0x7ffcbd304299 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:438
    #39 0x7ffcb8db2b32 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:780
    #40 0x7ffcb8db50b3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1156
    #41 0x7ffcb8db0acd in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #42 0x7ffcb8db15bd in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #43 0x7ffcabc41601 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #44 0x7ff7fe5b43a5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #45 0x7ff7fe5b1db2 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #46 0x7ff7fe98e8c3 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #47 0x7ffd21af7343 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017343)
    #48 0x7ffd22f426b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)

0x11927a004348 is located 72 bytes inside of 120-byte region [0x11927a004300,0x11927a004378)
freed by thread T0 here:
    #0 0x7ff7fe68cbfd in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffca5cb8c3b in llvm::ICmpInst::~ICmpInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:1093
    #2 0x7ffca6f1d891 in llvm::iplist<llvm::Instruction,llvm::ilist_traits<llvm::Instruction> >::clear C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\ADT\ilist.h:563
    #3 0x7ffca6f1d332 in llvm::BasicBlock::~BasicBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:91
    #4 0x7ffca6f211cf in llvm::BasicBlock::~BasicBlock C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:70
    #5 0x7ffca7c84f81 in llvm::removeUnreachableBlocks C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\Local.cpp:1306
    #6 0x7ffca71456ed in simplifyFunctionCFG C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\SimplifyCFGPass.cpp:155
    #7 0x7ffca6078064 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #8 0x7ffca6078afe in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #9 0x7ffca60797b5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #10 0x7ffca6082b4c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:781
    #11 0x7ffca5a90921 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #12 0x7ffca61ae5a1 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #13 0x7ffca5a8b612 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #14 0x7ffca5a98de3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #15 0x7ffca5976c13 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #16 0x7ffcae33c559 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #17 0x7ffcae39fe7e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #18 0x7ffcae441794 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #19 0x7ffcae405ffc in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:87
    #20 0x7ffcae257330 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #21 0x7ffcae1a7da1 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2035
    #22 0x7ffcae1a7787 in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1300
    #23 0x7ffcd076567d in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #24 0x7ffcd01b5494 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477
    #25 0x7ffcd01bd7dd in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1652
    #26 0x7ffccbccc572 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1020
    #27 0x7ffccbccc9c5 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1924

previously allocated by thread T0 here:
    #0 0x7ff7fe68ccfd in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffca849592e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffca6f1c3f1 in llvm::User::operator new C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:96
    #3 0x7ffca6e4b4d9 in llvm::BinaryOperator::Create C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Instructions.cpp:1701
    #4 0x7ffca7f9bbda in llvm::InstCombiner::OptimizeOverflowCheck C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\InstCombine\InstCombineCompares.cpp:2159
    #5 0x7ffca7fa4dcd in llvm::InstCombiner::visitICmpInst C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\InstCombine\InstCombineCompares.cpp:3527
    #6 0x7ffca730e25b in llvm::InstCombiner::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\InstCombine\InstructionCombining.cpp:2766
    #7 0x7ffca73112c6 in combineInstructionsOverFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\InstCombine\InstructionCombining.cpp:3014
    #8 0x7ffca7313678 in `anonymous namespace'::InstructionCombiningPass::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\InstCombine\InstructionCombining.cpp:3104
    #9 0x7ffca6078064 in llvm::FPPassManager::runOnFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #10 0x7ffca6078afe in llvm::FPPassManager::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #11 0x7ffca60797b5 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #12 0x7ffca6082b4c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:781
    #13 0x7ffca5a90921 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #14 0x7ffca61ae5a1 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #15 0x7ffca5a8b612 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #16 0x7ffca5a98de3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #17 0x7ffca5976c13 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #18 0x7ffcae33c559 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #19 0x7ffcae39fe7e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #20 0x7ffcae441794 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #21 0x7ffcae405ffc in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:87
    #22 0x7ffcae257330 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #23 0x7ffcae1a7da1 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:2035
    #24 0x7ffcae1a7787 in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1300
    #25 0x7ffcd076567d in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #26 0x7ffcd01b5494 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477
    #27 0x7ffcd01bd7dd in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1652

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\InstCombine\InstructionCombining.cpp:3008 in combineInstructionsOverFunction
Shadow bytes around the buggy address:
  0x11927a004080: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00
  0x11927a004100: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa f7 fa
  0x11927a004180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x11927a004200: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x11927a004280: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa
=>0x11927a004300: fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fa
  0x11927a004380: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x11927a004400: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
  0x11927a004480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11927a004500: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x11927a004580: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
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

==3768==ADDITIONAL INFO

==3768==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffcbefcd5b0 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:483


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==3768==END OF ADDITIONAL INFO
==3768==ABORTING
[7248:2100:0524/135808.046:ERROR:gpu_process_host.cc(1002)] GPU process exited unexpectedly: exit_code=1
[7248:2100:0524/135808.046:WARNING:gpu_process_host.cc(1436)] The GPU process has crashed 1 time(s)

```

## Attachments

- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 667 B)
- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 807 B)
- [asanAddReachable](attachments/asanAddReachable) (application/octet-stream, 23.0 KB)
- [indexAddReachableCodeToWorklist.html](attachments/indexAddReachableCodeToWorklist.html) (text/html, 2.9 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-05-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5077990110068736.

### cl...@appspot.gserviceaccount.com (2024-05-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4836462724841472.

### mp...@google.com (2024-05-28)

We appreciate this report given this code is exposed to the web in Chromium. Given dxc is a microsoft product and they have vulnerability rewards program for this product (<https://github.com/microsoft/DirectXShaderCompiler/blob/main/SECURITY.md>), why not report it to microsoft directly?

Assigning to enga@ and CC'ing dneto@.

### mp...@google.com (2024-05-28)

I was able to reproduce on the current extended stable (M124) with a similar stack trace:

```
=================================================================
==3386344==ERROR: AddressSanitizer: heap-use-after-free on address 0x50b000001aa8 at pc 0x7f029bdf13b6 bp 0x7fff8a00e3d0 sp 0x7fff8a00e3c8
READ of size 1 at 0x50b000001aa8 thread T0
    #0 0x7f029bdf13b5 in getValueID third_party/dxc/include/llvm/IR/Value.h:374:12
    #1 0x7f029bdf13b5 in doit third_party/dxc/include/llvm/IR/Value.h:655:16
    #2 0x7f029bdf13b5 in doit third_party/dxc/include/llvm/Support/Casting.h:97:12
    #3 0x7f029bdf13b5 in doit third_party/dxc/include/llvm/Support/Casting.h:123:12
    #4 0x7f029bdf13b5 in doit third_party/dxc/include/llvm/Support/Casting.h:113:12
    #5 0x7f029bdf13b5 in isa<llvm::Constant, llvm::Value *> third_party/dxc/include/llvm/Support/Casting.h:134:10
    #6 0x7f029bdf13b5 in AddReachableCodeToWorklist third_party/dxc/lib/Transforms/InstCombine/InstructionCombining.cpp:2860:43
    #7 0x7f029bdf13b5 in prepareICWorklistFromFunction third_party/dxc/lib/Transforms/InstCombine/InstructionCombining.cpp:2949:7
    #8 0x7f029bdf13b5 in combineInstructionsOverFunction(llvm::Function&, llvm::InstCombineWorklist&, bool, llvm::AliasAnalysis*, llvm::AssumptionCache&, llvm::TargetLibraryInfo&, llvm::DominatorTree&, llvm::LoopInfo*) third_party/dxc/lib/Transforms/InstCombine/InstructionCombining.cpp:3008:9
    #9 0x7f029bdf4057 in (anonymous namespace)::InstructionCombiningPass::runOnFunction(llvm::Function&) third_party/dxc/lib/Transforms/InstCombine/InstructionCombining.cpp:3104:10
    #10 0x7f029ba9cd3d in llvm::FPPassManager::runOnFunction(llvm::Function&) third_party/dxc/lib/IR/LegacyPassManager.cpp:1587:27
    #11 0x7f029ba9d45a in llvm::FPPassManager::runOnModule(llvm::Module&) third_party/dxc/lib/IR/LegacyPassManager.cpp:1609:16
    #12 0x7f029ba9df69 in runOnModule third_party/dxc/lib/IR/LegacyPassManager.cpp:1669:27
    #13 0x7f029ba9df69 in llvm::legacy::PassManagerImpl::run(llvm::Module&) third_party/dxc/lib/IR/LegacyPassManager.cpp:1771:44
    #14 0x7f0299990e2c in EmitAssembly third_party/dxc/tools/clang/lib/CodeGen/BackendUtil.cpp:756:22
    #15 0x7f0299990e2c in clang::EmitBackendOutput(clang::DiagnosticsEngine&, clang::CodeGenOptions const&, clang::TargetOptions const&, clang::LangOptions const&, llvm::StringRef, llvm::Module*, clang::BackendAction, llvm::raw_pwrite_stream*) third_party/dxc/tools/clang/lib/CodeGen/BackendUtil.cpp:779:15
    #16 0x7f0299c2058f in clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext&) third_party/dxc/tools/clang/lib/CodeGen/CodeGenAction.cpp:191:7
    #17 0x7f029a0ea73c in clang::ParseAST(clang::Sema&, bool, bool) third_party/dxc/tools/clang/lib/Parse/ParseAST.cpp:164:13
    #18 0x7f0299c1ddee in clang::CodeGenAction::ExecuteAction() third_party/dxc/tools/clang/lib/CodeGen/CodeGenAction.cpp:807:28
    #19 0x7f0299f67b64 in clang::FrontendAction::Execute() third_party/dxc/tools/clang/lib/Frontend/FrontendAction.cpp:455:8
    #20 0x7f029929173b in DxcCompiler::Compile(DxcBuffer const*, wchar_t const**, unsigned int, IDxcIncludeHandler*, _GUID const&, void**) third_party/dxc/tools/clang/tools/dxcompiler/dxcompilerobj.cpp:982:18
    #21 0x7f0299288418 in hlsl::DxcCompilerAdapter::WrapCompile(bool, IDxcBlob*, wchar_t const*, wchar_t const*, wchar_t const*, wchar_t const**, unsigned int, DxcDefine const*, unsigned int, IDxcIncludeHandler*, IDxcOperationResult**, wchar_t**, IDxcBlob**) third_party/dxc/tools/clang/tools/dxcompiler/dxcompilerobj.cpp:1845:5
    #22 0x7f029928ae20 in hlsl::DxcCompilerAdapter::CompileWithDebug(IDxcBlob*, wchar_t const*, wchar_t const*, wchar_t const*, wchar_t const**, unsigned int, DxcDefine const*, unsigned int, IDxcIncludeHandler*, IDxcOperationResult**, wchar_t**, IDxcBlob**) third_party/dxc/tools/clang/tools/dxcompiler/dxcompilerobj.cpp:1748:10
    #23 0x7f029928b798 in hlsl::DxcCompilerAdapter::Compile(IDxcBlob*, wchar_t const*, wchar_t const*, wchar_t const*, wchar_t const**, unsigned int, DxcDefine const*, unsigned int, IDxcIncludeHandler*, IDxcOperationResult**) third_party/dxc/tools/clang/tools/dxcompiler/dxcompileradapter.h:75:12
    #24 0x55689b8484ac in DxcContext::Compile() third_party/dxc/tools/clang/tools/dxclib/dxc.cpp:873:9
    #25 0x55689b851e0d in dxc::main(int, char const**) third_party/dxc/tools/clang/tools/dxclib/dxc.cpp:1501:24
    #26 0x7f029f5a96c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x50b000001aa8 is located 72 bytes inside of 112-byte region [0x50b000001a60,0x50b000001ad0)
freed by thread T0 here:
    #0 0x55689b83a63d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:143:3
    #1 0x7f029b988193 in deleteNode third_party/dxc/include/llvm/ADT/ilist.h:113:39
    #2 0x7f029b988193 in erase third_party/dxc/include/llvm/ADT/ilist.h:479:5
    #3 0x7f029b988193 in erase third_party/dxc/include/llvm/ADT/ilist.h:559:15
    #4 0x7f029b988193 in llvm::iplist<llvm::Instruction, llvm::ilist_traits<llvm::Instruction>>::clear() third_party/dxc/include/llvm/ADT/ilist.h:563:28
    #5 0x7f029b987ce3 in llvm::BasicBlock::~BasicBlock() third_party/dxc/lib/IR/BasicBlock.cpp:91:12
    #6 0x7f029b98821d in llvm::BasicBlock::~BasicBlock() third_party/dxc/lib/IR/BasicBlock.cpp:70:27
    #7 0x7f029c123e34 in deleteNode third_party/dxc/include/llvm/ADT/ilist.h:113:39
    #8 0x7f029c123e34 in erase third_party/dxc/include/llvm/ADT/ilist.h:479:5
    #9 0x7f029c123e34 in llvm::removeUnreachableBlocks(llvm::Function&) third_party/dxc/lib/Transforms/Utils/Local.cpp:1306:33
    #10 0x7f029c0a7d35 in simplifyFunctionCFG(llvm::Function&, llvm::TargetTransformInfo const&, llvm::AssumptionCache*, int) third_party/dxc/lib/Transforms/Scalar/SimplifyCFGPass.cpp:155:22
    #11 0x7f029ba9cd3d in llvm::FPPassManager::runOnFunction(llvm::Function&) third_party/dxc/lib/IR/LegacyPassManager.cpp:1587:27
    #12 0x7f029ba9d45a in llvm::FPPassManager::runOnModule(llvm::Module&) third_party/dxc/lib/IR/LegacyPassManager.cpp:1609:16
    #13 0x7f029ba9df69 in runOnModule third_party/dxc/lib/IR/LegacyPassManager.cpp:1669:27
    #14 0x7f029ba9df69 in llvm::legacy::PassManagerImpl::run(llvm::Module&) third_party/dxc/lib/IR/LegacyPassManager.cpp:1771:44
    #15 0x7f0299990e2c in EmitAssembly third_party/dxc/tools/clang/lib/CodeGen/BackendUtil.cpp:756:22
    #16 0x7f0299990e2c in clang::EmitBackendOutput(clang::DiagnosticsEngine&, clang::CodeGenOptions const&, clang::TargetOptions const&, clang::LangOptions const&, llvm::StringRef, llvm::Module*, clang::BackendAction, llvm::raw_pwrite_stream*) third_party/dxc/tools/clang/lib/CodeGen/BackendUtil.cpp:779:15
    #17 0x7f0299c2058f in clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext&) third_party/dxc/tools/clang/lib/CodeGen/CodeGenAction.cpp:191:7
    #18 0x7f029a0ea73c in clang::ParseAST(clang::Sema&, bool, bool) third_party/dxc/tools/clang/lib/Parse/ParseAST.cpp:164:13
    #19 0x7f0299c1ddee in clang::CodeGenAction::ExecuteAction() third_party/dxc/tools/clang/lib/CodeGen/CodeGenAction.cpp:807:28
    #20 0x7f0299f67b64 in clang::FrontendAction::Execute() third_party/dxc/tools/clang/lib/Frontend/FrontendAction.cpp:455:8
    #21 0x7f029929173b in DxcCompiler::Compile(DxcBuffer const*, wchar_t const**, unsigned int, IDxcIncludeHandler*, _GUID const&, void**) third_party/dxc/tools/clang/tools/dxcompiler/dxcompilerobj.cpp:982:18
    #22 0x7f0299288418 in hlsl::DxcCompilerAdapter::WrapCompile(bool, IDxcBlob*, wchar_t const*, wchar_t const*, wchar_t const*, wchar_t const**, unsigned int, DxcDefine const*, unsigned int, IDxcIncludeHandler*, IDxcOperationResult**, wchar_t**, IDxcBlob**) third_party/dxc/tools/clang/tools/dxcompiler/dxcompilerobj.cpp:1845:5
    #23 0x7f029928ae20 in hlsl::DxcCompilerAdapter::CompileWithDebug(IDxcBlob*, wchar_t const*, wchar_t const*, wchar_t const*, wchar_t const**, unsigned int, DxcDefine const*, unsigned int, IDxcIncludeHandler*, IDxcOperationResult**, wchar_t**, IDxcBlob**) third_party/dxc/tools/clang/tools/dxcompiler/dxcompilerobj.cpp:1748:10
    #24 0x7f029928b798 in hlsl::DxcCompilerAdapter::Compile(IDxcBlob*, wchar_t const*, wchar_t const*, wchar_t const*, wchar_t const**, unsigned int, DxcDefine const*, unsigned int, IDxcIncludeHandler*, IDxcOperationResult**) third_party/dxc/tools/clang/tools/dxcompiler/dxcompileradapter.h:75:12
    #25 0x55689b8484ac in DxcContext::Compile() third_party/dxc/tools/clang/tools/dxclib/dxc.cpp:873:9
    #26 0x55689b851e0d in dxc::main(int, char const**) third_party/dxc/tools/clang/tools/dxclib/dxc.cpp:1501:24
    #27 0x7f029f5a96c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

previously allocated by thread T0 here:
    #0 0x55689b839ddd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x7f029baf63bb in llvm::User::operator new(unsigned long, unsigned int) third_party/dxc/lib/IR/User.cpp:96:19
    #2 0x7f029ba6d71f in operator new third_party/dxc/include/llvm/IR/InstrTypes.h:150:12
    #3 0x7f029ba6d71f in llvm::BinaryOperator::Create(llvm::Instruction::BinaryOps, llvm::Value*, llvm::Value*, llvm::Twine const&, llvm::Instruction*) third_party/dxc/lib/IR/Instructions.cpp:1701:10
    #4 0x7f029bcdd2a4 in CreateInsertNUWNSWBinOp third_party/dxc/include/llvm/IR/IRBuilder.h:694:33
    #5 0x7f029bcdd2a4 in llvm::IRBuilder<true, llvm::TargetFolder, llvm::InstCombineIRInserter>::CreateAdd(llvm::Value*, llvm::Value*, llvm::Twine const&, bool, bool) third_party/dxc/include/llvm/IR/IRBuilder.h:717:12
    #6 0x7f029bd58863 in llvm::InstCombiner::OptimizeOverflowCheck(llvm::OverflowCheckFlavor, llvm::Value*, llvm::Value*, llvm::Instruction&, llvm::Value*&, llvm::Constant*&) third_party/dxc/lib/Transforms/InstCombine/InstCombineCompares.cpp:2159:33
    #7 0x7f029bd5d811 in llvm::InstCombiner::visitICmpInst(llvm::ICmpInst&) third_party/dxc/lib/Transforms/InstCombine/InstCombineCompares.cpp:3527:11
    #8 0x7f029bdee89f in llvm::InstCombiner::run() third_party/dxc/lib/Transforms/InstCombine/InstructionCombining.cpp:2766:31
    #9 0x7f029bdf121c in combineInstructionsOverFunction(llvm::Function&, llvm::InstCombineWorklist&, bool, llvm::AliasAnalysis*, llvm::AssumptionCache&, llvm::TargetLibraryInfo&, llvm::DominatorTree&, llvm::LoopInfo*) third_party/dxc/lib/Transforms/InstCombine/InstructionCombining.cpp:3014:12
    #10 0x7f029bdf4057 in (anonymous namespace)::InstructionCombiningPass::runOnFunction(llvm::Function&) third_party/dxc/lib/Transforms/InstCombine/InstructionCombining.cpp:3104:10
    #11 0x7f029ba9cd3d in llvm::FPPassManager::runOnFunction(llvm::Function&) third_party/dxc/lib/IR/LegacyPassManager.cpp:1587:27
    #12 0x7f029ba9d45a in llvm::FPPassManager::runOnModule(llvm::Module&) third_party/dxc/lib/IR/LegacyPassManager.cpp:1609:16
    #13 0x7f029ba9df69 in runOnModule third_party/dxc/lib/IR/LegacyPassManager.cpp:1669:27
    #14 0x7f029ba9df69 in llvm::legacy::PassManagerImpl::run(llvm::Module&) third_party/dxc/lib/IR/LegacyPassManager.cpp:1771:44
    #15 0x7f0299990e2c in EmitAssembly third_party/dxc/tools/clang/lib/CodeGen/BackendUtil.cpp:756:22
    #16 0x7f0299990e2c in clang::EmitBackendOutput(clang::DiagnosticsEngine&, clang::CodeGenOptions const&, clang::TargetOptions const&, clang::LangOptions const&, llvm::StringRef, llvm::Module*, clang::BackendAction, llvm::raw_pwrite_stream*) third_party/dxc/tools/clang/lib/CodeGen/BackendUtil.cpp:779:15
    #17 0x7f0299c2058f in clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext&) third_party/dxc/tools/clang/lib/CodeGen/CodeGenAction.cpp:191:7
    #18 0x7f029a0ea73c in clang::ParseAST(clang::Sema&, bool, bool) third_party/dxc/tools/clang/lib/Parse/ParseAST.cpp:164:13
    #19 0x7f0299c1ddee in clang::CodeGenAction::ExecuteAction() third_party/dxc/tools/clang/lib/CodeGen/CodeGenAction.cpp:807:28
    #20 0x7f0299f67b64 in clang::FrontendAction::Execute() third_party/dxc/tools/clang/lib/Frontend/FrontendAction.cpp:455:8
    #21 0x7f029929173b in DxcCompiler::Compile(DxcBuffer const*, wchar_t const**, unsigned int, IDxcIncludeHandler*, _GUID const&, void**) third_party/dxc/tools/clang/tools/dxcompiler/dxcompilerobj.cpp:982:18
    #22 0x7f0299288418 in hlsl::DxcCompilerAdapter::WrapCompile(bool, IDxcBlob*, wchar_t const*, wchar_t const*, wchar_t const*, wchar_t const**, unsigned int, DxcDefine const*, unsigned int, IDxcIncludeHandler*, IDxcOperationResult**, wchar_t**, IDxcBlob**) third_party/dxc/tools/clang/tools/dxcompiler/dxcompilerobj.cpp:1845:5
    #23 0x7f029928ae20 in hlsl::DxcCompilerAdapter::CompileWithDebug(IDxcBlob*, wchar_t const*, wchar_t const*, wchar_t const*, wchar_t const**, unsigned int, DxcDefine const*, unsigned int, IDxcIncludeHandler*, IDxcOperationResult**, wchar_t**, IDxcBlob**) third_party/dxc/tools/clang/tools/dxcompiler/dxcompilerobj.cpp:1748:10
    #24 0x7f029928b798 in hlsl::DxcCompilerAdapter::Compile(IDxcBlob*, wchar_t const*, wchar_t const*, wchar_t const*, wchar_t const**, unsigned int, DxcDefine const*, unsigned int, IDxcIncludeHandler*, IDxcOperationResult**) third_party/dxc/tools/clang/tools/dxcompiler/dxcompileradapter.h:75:12
    #25 0x55689b8484ac in DxcContext::Compile() third_party/dxc/tools/clang/tools/dxclib/dxc.cpp:873:9
    #26 0x55689b851e0d in dxc::main(int, char const**) third_party/dxc/tools/clang/tools/dxclib/dxc.cpp:1501:24
    #27 0x7f029f5a96c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free third_party/dxc/include/llvm/IR/Value.h:374:12 in getValueID
Shadow bytes around the buggy address:
  0x50b000001800: fd fd fa fa fa fa fa fa fa fa 00 00 00 00 00 00
  0x50b000001880: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
  0x50b000001900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
  0x50b000001980: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x50b000001a00: fd fd fd fd fa fa fa fa fa fa fa fa fd fd fd fd
=>0x50b000001a80: fd fd fd fd fd[fd]fd fd fd fd fa fa fa fa fa fa
  0x50b000001b00: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x50b000001b80: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x50b000001c00: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fd fd
  0x50b000001c80: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x50b000001d00: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
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
==3386344==ABORTING

```

### wg...@gmail.com (2024-05-29)

@ [mp...@google.com](mailto:mp...@google.com):

AFAICT, the Microsoft VRP does not cover dxc. While there is a [bounty program](https://www.microsoft.com/en-us/msrc/bounty-new-edge) for Edge it explicitly excludes bugs if they're reachable via Chrome.

> Identify a previously unreported vulnerability that is unique to Microsoft Edge based on Chromium, in the Dev, Beta, or Stable channels, and which does not reproduce on the equivalent channel of Google Chrome.

While I don't agree with this policy (especially as the bug is in Microsoft code), it looks like these dxc bugs are only eligible for the Google VRP.

Furthermore, some [memory corruption bugs](https://github.com/microsoft/DirectXShaderCompiler/issues/6115) are not getting fixed even if Microsoft is aware of them.

### pe...@google.com (2024-05-29)

Setting milestone because of s0/s1 severity.

### am...@google.com (2024-05-31)

Opened the attached `indexAddReachableCodeToWorklist.html` in Canary, Version 127.0.6512.0 (Official Build) canary (64-bit), and the GPU process crashes.

I will investigate further.

### am...@google.com (2024-06-07)

Figured out the bug, and pushed an upstream patch: <https://github.com/microsoft/DirectXShaderCompiler/pull/6679>

### ch...@google.com (2024-06-14)

Fix rolled into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/192928>

Dawn rolled into Chromium: <https://chromium-review.googlesource.com/c/chromium/src/+/5625269>

Landed in 128.0.6535.0: <https://chromiumdash.appspot.com/commit/7cb330156dcffbf97c3eda1aba1fb3606641e42b>

dneto@: Can you verify the fix on a Windows ASAN Chromium build of Canary 128.0.6535.0?

### dn...@google.com (2024-06-17)

I don't have ssh or remote desktop access to my windows machines. I will be back in the office tomorrow to verify the fix.

### dn...@google.com (2024-06-18)

I've confirmed the problem in a developer ASAN build of 127.0.6533.0.

I confirmed the problem is fixed in an ASAN build of 128.0.6543.0

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

### am...@google.com (2024-06-20)

1. Which CLs should be backmerged? (Please include Gerrit links.)

Fix rolled into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/192928>

Dawn rolled into Chromium: <https://chromium-review.googlesource.com/c/chromium/src/+/5625269>

Landed in 128.0.6535.0: <https://chromiumdash.appspot.com/commit/7cb330156dcffbf97c3eda1aba1fb3606641e42b>

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes.

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

Yes, open the attached `indexAddReachableCodeToWorklist.html` in latest Canary, and the GPU process will not crash anymore.

### am...@chromium.org (2024-06-20)

merges approved for <https://dawn-review.googlesource.com/c/dawn/+/192928>; please merge this fix to M127 Beta / branch 6533 and M126 Stable / branch 6478 as soon as possible/ before 10am Pacific tomorrow so this fix can be included in next week's Stable and Beta updates -- thanks!

### ap...@google.com (2024-06-20)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6533

commit bacb045ce3ea764405aa6d9f6da00064332cffb4
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Jun 20 15:40:30 2024

    Fix instcombine overflow check inserting inst at wrong place (#6679)
    
    When optimizing an overflow check of an add followed by a compare, the
    new instruction was being inserted at the compare, and the add removed.
    This produced invalid IR in cases where there were other uses of the
    former add between it and the compare. This fix makes sure to insert the
    new instruction at the old add location, rather than at the compare.
    
    Note that this was also fixed in LLVM:
    
    https://github.com/llvm/llvm-project/commit/6f5dca70ed1c030957a45ad91bd295921f17b18d
    
    Bug: chromium:342545100
    Change-Id: Ief0476021b0c9c27b7e673b0ba50f8c6c73b5691
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5644336
    Reviewed-by: Ryan Harrison <rharrison@chromium.org>
    Reviewed-by: dan sinclair <dsinclair@google.com>

M       lib/Transforms/InstCombine/InstCombineCompares.cpp
A       tools/clang/test/DXC/Passes/InstructionCombining/instcombine-opt-overflow-check-inserts-at-add.ll

https://chromium-review.googlesource.com/5644336


### ap...@google.com (2024-06-20)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6478

commit b3c64851765c411b7147ac0269df2a2ce23d6f89
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Jun 20 15:39:00 2024

    Fix instcombine overflow check inserting inst at wrong place (#6679)
    
    When optimizing an overflow check of an add followed by a compare, the
    new instruction was being inserted at the compare, and the add removed.
    This produced invalid IR in cases where there were other uses of the
    former add between it and the compare. This fix makes sure to insert the
    new instruction at the old add location, rather than at the compare.
    
    Note that this was also fixed in LLVM:
    
    https://github.com/llvm/llvm-project/commit/6f5dca70ed1c030957a45ad91bd295921f17b18d
    
    Bug: chromium:342545100
    Change-Id: Iecf758e4465b32371266bbe9879790328f363322
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5644335
    Reviewed-by: dan sinclair <dsinclair@google.com>
    Reviewed-by: Ryan Harrison <rharrison@chromium.org>

M       lib/Transforms/InstCombine/InstCombineCompares.cpp
A       tools/clang/test/DXC/Passes/InstructionCombining/instcombine-opt-overflow-check-inserts-at-add.ll

https://chromium-review.googlesource.com/5644335


### ap...@google.com (2024-06-20)

Project: dawn
Branch: chromium/6533

commit 4511fb32737b61e2502d3c933beea18159741dbd
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Jun 20 20:39:38 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:342545100
    Change-Id: Iacf6d9e5a932679766e02989495f78d248907617
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/194998
    Reviewed-by: dan sinclair <dsinclair@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/194998


### ap...@google.com (2024-06-20)

Project: dawn
Branch: chromium/6478

commit 13586d84cb6038b38bf769db815e59d3d152d474
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Jun 20 20:39:31 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:342545100
    Change-Id: I59149f3e1af146238efd6480c371f3dd2f4c4ce2
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/194997
    Reviewed-by: dan sinclair <dsinclair@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/194997


### am...@google.com (2024-06-21)

Merged to chromium: [M126](https://chromium.googlesource.com/chromium/src.git/+/e0c7ff08349ead4cd20051f0a875cb7c7760615c), [M127](https://chromium.googlesource.com/chromium/src.git/+/028deb95638845bd5e0e61b42c3edcb44a216777)

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

### am...@chromium.org (2024-06-27)

Congratulations on yet another one! Thank you for your efforts and reporting this issue to us -- nice work! 

### pe...@google.com (2024-09-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> memory corruption in the GPU process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/342545100)*
