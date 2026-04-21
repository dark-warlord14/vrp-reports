# GPU process crash via WebGPU shader

| Field | Value |
|-------|-------|
| **Issue ID** | [328958020](https://issues.chromium.org/issues/328958020) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn, Internals>GPU>Dawn |
| **Platforms** | Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-03-11 |
| **Bounty** | $10,000.00 |

## Description

VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this might trigger a heap UAF insider the hlsl compiler.

VERSION
Chrome Version: Pre-compiled ASAN Chromium 124.0.6350.0 (Developer Build) (64-bit)
Operating System: Win10 Build 19045

REPRODUCTION CASE
Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: GPU
Crash State:
=================================================================
==2156==ERROR: AddressSanitizer: heap-use-after-free on address 0x126e221e9f70 at pc 0x7fff5ca9ca87 bp 0x006fed5fc3c0 sp 0x006fed5fc408
READ of size 1 at 0x126e221e9f70 thread T0
==2156==WARNING: Failed to use and restart external symbolizer!
==2156==*** WARNING: Failed to initialize DbgHelp!              ***
==2156==*** Most likely this means that the app is already      *** 
==2156==*** using DbgHelp, possibly with incompatible flags.    *** 
==2156==*** Due to technical reasons, symbolization might crash *** 
==2156==*** or produce wrong results.                           ***
ModLoad: 00007fff`b7c40000 00007fff`b7cef000   C:\Windows\System32\ADVAPI32.dll
ModLoad: 00007fff`b6cb0000 00007fff`b6d4c000   C:\Windows\System32\sechost.dll
ModLoad: 00007fff`b65e0000 00007fff`b6706000   C:\Windows\System32\RPCRT4.dll
ModLoad: 00007fff`b7560000 00007fff`b760d000   C:\Windows\System32\shcore.dll
ModLoad: 00007fff`b6170000 00007fff`b64c4000   C:\Windows\System32\combase.dll
ModLoad: 00007fff`b5970000 00007fff`b5a70000   C:\Windows\System32\ucrtbase.dll
ModLoad: 00007fff`66820000 00007fff`93985000   C:\Users\user\Desktop\win32-release_x64_asan-win32-release_x64-1270692\chrome.dll
ModLoad: 00007fff`b7610000 00007fff`b767b000   C:\Windows\System32\WS2_32.dll
ModLoad: 00007fff`b6710000 00007fff`b67dd000   C:\Windows\System32\OLEAUT32.dll
ModLoad: 00007fff`b5d70000 00007fff`b5e0d000   C:\Windows\System32\msvcp_win.dll
ModLoad: 00007fff`b5970000 00007fff`b5a70000   C:\Windows\System32\ucrtbase.dll
ModLoad: 00007fff`b6170000 00007fff`b64c4000   C:\Windows\System32\combase.dll
ModLoad: 00007fff`b5f50000 00007fff`b5fb7000   C:\Windows\System32\WINTRUST.dll
ModLoad: 00007fff`b5810000 00007fff`b596e000   C:\Windows\System32\CRYPT32.dll
ModLoad: 00007fff`9ded0000 00007fff`9def7000   C:\Windows\SYSTEM32\WINMM.dll
ModLoad: 00007fff`665f0000 00007fff`6681d000   C:\Users\user\Desktop\win32-release_x64_asan-win32-release_x64-1270692\dbghelp.dll
ModLoad: 00007fff`b4b60000 00007fff`b4b9c000   C:\Windows\SYSTEM32\IPHLPAPI.DLL
ModLoad: 00007fff`b5650000 00007fff`b567e000   C:\Windows\SYSTEM32\USERENV.dll
ModLoad: 00007fff`ae540000 00007fff`ae54c000   C:\Windows\SYSTEM32\Secur32.dll
ModLoad: 00007fff`ae580000 00007fff`ae68a000   C:\Windows\SYSTEM32\WINHTTP.dll
ModLoad: 00007fff`a2b20000 00007fff`a2d9f000   C:\Windows\SYSTEM32\DWrite.dll
ModLoad: 00007fff`9dbb0000 00007fff`9dc48000   C:\Windows\SYSTEM32\WINSPOOL.DRV
ModLoad: 00007fff`aeb40000 00007fff`aeb5d000   C:\Windows\SYSTEM32\dhcpcsvc.DLL
ModLoad: 00007fff`b5680000 00007fff`b56b2000   C:\Windows\SYSTEM32\SSPICLI.DLL
ModLoad: 00007fff`b52a0000 00007fff`b52b2000   C:\Windows\System32\MSASN1.dll
ModLoad: 00007fff`b5ec0000 00007fff`b5f42000   C:\Windows\System32\bcryptPrimitives.dll
ModLoad: 00007fff`b7560000 00007fff`b760d000   C:\Windows\System32\shcore.dll
#0 0x7fff5ca9ca86 in `anonymous namespace'::GlobalDCE::GlobalIsNeeded C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\IPO\GlobalDCE.cpp:244
    #1 0x7fff5ca9b52a in `anonymous namespace'::GlobalDCE::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\IPO\GlobalDCE.cpp:100
    #2 0x7fff5bea3c3e in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #3 0x7fff5beab484 in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #4 0x7fff5ba3755c in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #5 0x7fff5bf89477 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #6 0x7fff5ba31d9f in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #7 0x7fff5ba3f325 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #8 0x7fff5b969f07 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #9 0x7fff6883a396 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #10 0x7fff68891d53 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #11 0x7fff689281fa in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #12 0x7fff688f12ff in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:85
    #13 0x7fff6877cf0d in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #14 0x7fff686f8213 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1871
    #15 0x7fff686f7cfc in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1212
    #16 0x7fff85c96889 in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #17 0x7fff857d4d83 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477
    #18 0x7fff857e15c9 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1612
    #19 0x7fff821b97bc in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:999
    #20 0x7fff821b9c4e in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1883
    #21 0x7fff821aee7b in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1828
    #22 0x7fff77502a14 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #23 0x7fff74981036 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:507
    #24 0x7fff749801e4 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:155
    #25 0x7fff7751b1ba in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:873
    #26 0x7fff775276d1 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #27 0x7fff66b20c6e in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #28 0x7fff76dc3879 in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:740
    #29 0x7fff76dc1f2c in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:665
    #30 0x7fff76dc4a83 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #31 0x7fff72d1d912 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:202
    #32 0x7fff75d9517b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #33 0x7fff75d940a4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #34 0x7fff75dbc93a in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #35 0x7fff75d96eca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:641
    #36 0x7fff72d6a150 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #37 0x7fff754716f9 in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:431
    #38 0x7fff719a387c in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:771
    #39 0x7fff719a5b96 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1146
    #40 0x7fff719a1cac in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:333
    #41 0x7fff719a248e in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:346
    #42 0x7fff6682169b in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #43 0x7ff7ec425133 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #44 0x7ff7ec422522 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:401
    #45 0x7ff7ec7ac7d3 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #46 0x7fffb6d67613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)
    #47 0x7fffb81026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x126e221e9f70 is located 48 bytes inside of 200-byte region [0x126e221e9f40,0x126e221ea008)
freed by thread T0 here:
    #0 0x7ff7ec4d115d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7fff5c8528d9 in llvm::Function::~Function C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Function.cpp:275
    #2 0x7fff5bc7acb7 in llvm::iplist<llvm::Function,llvm::ilist_traits<llvm::Function> >::erase C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\ADT\ilist.h:479
    #3 0x7fff5c84a73f in llvm::Function::eraseFromParent C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Function.cpp:244
    #4 0x7fff5cb97e7c in `anonymous namespace'::TempOverloadPool::~TempOverloadPool C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLMatrixLowerPass.cpp:63
    #5 0x7fff5cb97315 in `anonymous namespace'::HLMatrixLowerPass::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLMatrixLowerPass.cpp:258
    #6 0x7fff5bea3c3e in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #7 0x7fff5beab484 in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #8 0x7fff5ba3755c in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #9 0x7fff5bf89477 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #10 0x7fff5ba31d9f in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #11 0x7fff5ba3f325 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #12 0x7fff5b969f07 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #13 0x7fff6883a396 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #14 0x7fff68891d53 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #15 0x7fff689281fa in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #16 0x7fff688f12ff in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:85
    #17 0x7fff6877cf0d in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #18 0x7fff686f8213 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1871
    #19 0x7fff686f7cfc in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1212
    #20 0x7fff85c96889 in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #21 0x7fff857d4d83 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477
    #22 0x7fff857e15c9 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1612
    #23 0x7fff821b97bc in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:999
    #24 0x7fff821b9c4e in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1883
    #25 0x7fff821aee7b in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1828
    #26 0x7fff77502a14 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #27 0x7fff74981036 in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:507
previously allocated by thread T0 here:
    #0 0x7ff7ec4d125d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7fff5d8c6956 in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7fff5c91c847 in llvm::User::operator new C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:96
    #3 0x7fff5bc32284 in llvm::Function::Create C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\IR\Function.h:123
    #4 0x7fff5bc76057 in llvm::Module::getOrInsertFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Module.cpp:129
    #5 0x7fff5bc76231 in llvm::Module::getOrInsertFunction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\Module.cpp:147
    #6 0x7fff5cb9a2e9 in `anonymous namespace'::TempOverloadPool::get C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLMatrixLowerPass.cpp:88
    #7 0x7fff5cba2458 in `anonymous namespace'::HLMatrixLowerPass::getLoweredByValOperand C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLMatrixLowerPass.cpp:427
    #8 0x7fff5cb9cda6 in `anonymous namespace'::HLMatrixLowerPass::lowerHLOperation C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLMatrixLowerPass.cpp:899
    #9 0x7fff5cb96488 in `anonymous namespace'::HLMatrixLowerPass::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLMatrixLowerPass.cpp:243
    #10 0x7fff5bea3c3e in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #11 0x7fff5beab484 in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #12 0x7fff5ba3755c in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #13 0x7fff5bf89477 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #14 0x7fff5ba31d9f in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #15 0x7fff5ba3f325 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #16 0x7fff5b969f07 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #17 0x7fff6883a396 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #18 0x7fff68891d53 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #19 0x7fff689281fa in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #20 0x7fff688f12ff in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:85
    #21 0x7fff6877cf0d in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #22 0x7fff686f8213 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1871
    #23 0x7fff686f7cfc in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1212
    #24 0x7fff85c96889 in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #25 0x7fff857d4d83 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477
    #26 0x7fff857e15c9 in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1612
    #27 0x7fff821b97bc in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:999

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Transforms\IPO\GlobalDCE.cpp:244 in `anonymous namespace'::GlobalDCE::GlobalIsNeeded
Shadow bytes around the buggy address:
  0x126e221e9c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x126e221e9d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x126e221e9d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x126e221e9e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x126e221e9e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x126e221e9f00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd[fd]fd
  0x126e221e9f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x126e221ea000: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x126e221ea080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x126e221ea100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x126e221ea180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==2156==ADDITIONAL INFO

==2156==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7fff76dbdbc9 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:481


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==2156==END OF ADDITIONAL INFO
==2156==ABORTING


CREDIT INFORMATION
Reporter credit: wgslfuzz

## Attachments

- [index.html](attachments/index.html) (text/html, 1.8 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-03-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6505539726409728.

### ja...@chromium.org (2024-03-12)

ClusterFuzz hasn't been able to reproduce this issue yet, and my guess is because it needs the D3D12 backend that was mentioned in the bug report. I tried reproducing this as well, but my Windows virtual machine fails on calling `navigator.gpu.requestAdapter()` because a GPUAdapter is not returned.

I'm going to add a component and some potential owners based on previous bugs and see if they can help with reproducing the issue.

### ja...@chromium.org (2024-03-12)

Adding bclayton, dneto and amaiorano who worked on [issue 41485642](https://issues.chromium.org/issues/41485642), which seems similar.

### ja...@chromium.org (2024-03-12)

Hi bclayton, from the bug description, this seems like it could either be a problem with how Chrome is generating the hlsl, or with how dxcompiler.dll is processing it.

Can you take a look?

### ja...@chromium.org (2024-03-14)

Assigning to bclayton so there's a clear owner.

### am...@google.com (2024-03-14)

I will investigate this.

### ja...@chromium.org (2024-03-14)

Thanks for taking a look amaiorano!

### am...@google.com (2024-03-14)

Extracted the WGSL from the HTML file:

```
fn f3822906348_() -> mat4x2<f32> {
    loop {
        continuing {
            break if false;
        }
    }
    return mat4x2<f32>();
}

@compute @workgroup_size(1, 1, 1)
fn computeSomething() {
    let _e1 = f3822906348_();
    return;
}

```

Note that it contains an infinite loop. Compiled it with Tint to produce the HLSL:

```
float4x2 f3822906348_() {
  while (true) {
    {
      if (false) { break; }
    }
  }
  return float4x2((0.0f).xx, (0.0f).xx, (0.0f).xx, (0.0f).xx);
}

[numthreads(1, 1, 1)]
void computeSomething() {
  float4x2 _e1 = f3822906348_();
  return;
}

```

Running an asan-build dxc.exe against this HLSL rerproduces the ASAN failure. Will debug this now.

### ja...@chromium.org (2024-03-14)

Following from <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-critical-severity>, I'm going to add Severity S0 provisionally as it looks like "memory corruption in the GPU process when it is reachable directly from web content without compromising the renderer.

This may change as we learn more about the issue.

### ja...@chromium.org (2024-03-14)

Adding affected OS: Windows.

### ja...@chromium.org (2024-03-15)

I'm setting foundin to extended stable for now. amaiorano, if you narrow down when this was introduced to something more recent, we can update the foundin.

### pe...@google.com (2024-03-15)

Setting milestone because of s0/s1 severity.

### am...@google.com (2024-03-15)

Update: I've spent the day debugging this. I created [this issue on the DXC GitHub](https://github.com/microsoft/DirectXShaderCompiler/issues/6423) and hope to get some guidance from Microsoft. I will continue to look at this on Monday.

### 24...@project.gserviceaccount.com (2024-03-19)

Detailed Report: https://clusterfuzz.com/testcase?key=6505539726409728

Fuzzer: None
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: UNKNOWN
Crash Address: 0x7ffff26e90fc
Crash State:
  C:\Windows\SYSTEM32\ntdll.dll
  C:\Windows\SYSTEM32\ntdll.dll
  C:\Windows\SYSTEM32\ntdll.dll
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&revision=1271142

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6505539726409728



************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### am...@google.com (2024-03-20)

Update on the plan moving forward:

- Find a fix
- Land it in our [Chrome mirror of DXC](https://chromium.googlesource.com/external/github.com/microsoft/DirectXShaderCompiler/) (stop auto-roller, land on patch branch, point to patch branch in Dawn's DEPS/submodules).
- Cherry-pick the Dawn DEPS change to other Chrome release branches.
- Once rolled out, get this patch into DXC, going via [their security procedure](https://github.com/microsoft/DirectXShaderCompiler/blob/main/SECURITY.md)

### ad...@google.com (2024-03-20)

We had a bit of a discussion in the security team on the severity level here. Cross-platform GPU process bugs are S0 since we do not believe in the strength of the GPU process sandbox on all platforms, but as this is Windows-only, and we believe in the strength of the GPU process sandbox on Windows, we consider this to be "memory corruption within a sandboxed process" and that means S1 not S0. Adjusting appropriately.

### am...@google.com (2024-03-20)

A fix for this crash has been sent to Microsoft. We are also working on setting up a patch branch in our mirror of DXC. So this fix will either land in upstream DXC, then roll into Dawn (and into Chrome); or we will land the patch in our mirror temporarily.

### ap...@google.com (2024-03-20)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/b328958020

commit 701a2b1da0387ac6abf73bdbaf7864b9615db033
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Wed Mar 20 17:15:40 2024

    Fix HLMatrixLowerPass leaving call to dangling FunctionVal
    
    When lowering an hl.cast, when the operand was an undef matrix, the pass would insert a call to a mat2vec stub, but since the undef value is not
    an alloca, it never gets handled, and the call to the temporary stub
    remains. Since the stub FunctionVal gets deleted, when the instruction
    is accessed in a future pass, it reads a dangling pointer.
    
    The fix is to handle undef similarly to how constant 0 is handled, and
    to return an undef vector from lowerHLCast.
    
    Bug: chromium:328958020
    Change-Id: Id31e3aa326d9cb9f03ea97139f14dc5292cd6f7b
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5383595
    Reviewed-by: Ben Clayton <bclayton@chromium.org>
    Reviewed-by: David Neto <dneto@google.com>
    Reviewed-by: Kenneth Russell <kbr@chromium.org>

M       lib/HLSL/HLMatrixLowerPass.cpp

https://chromium-review.googlesource.com/5383595


### bc...@google.com (2024-03-20)

Update:

- [amaiorano@'s fix for DXC has landed in a new branch as `refs/branch-heads/patches/b328958020`](https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5383595)
- [Autoroller for DirectXShaderCompiler -> Dawn has been stopped](https://autoroll.skia.org/r/directx-shader-compiler-dawn).
- [We've created a Dawn CL to use the fix in the new branch](https://dawn-review.googlesource.com/c/dawn/+/179706).

Once this lands, and then rolls into Chromium, we'll test the fix works as expected and start the merge request process.

### ap...@google.com (2024-03-21)

Project: chromium/src
Branch: main

commit 4602b454c56c4f0771baeaef257d53d4965ccd40
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Thu Mar 21 02:47:52 2024

    Roll Dawn from cc21b87a9865 to d654129e99a7 (11 revisions)
    
    https://dawn.googlesource.com/dawn.git/+log/cc21b87a9865..d654129e99a7
    
    2024-03-20 bclayton@google.com DEPS: Update DXC to patched branch
    2024-03-20 bclayton@google.com [tools][cts] Add seat belts to prevent commits of rolls from external repos
    2024-03-20 dsinclair@chromium.org Mark dp4a methods as `@const` in core.def.
    2024-03-20 dsinclair@chromium.org Re-enable disabled test.
    2024-03-20 dsinclair@chromium.org Change emitted name for `StageAttribute`.
    2024-03-20 bclayton@chromium.org [tools][perfmon]: Bump CL delta thresholds
    2024-03-20 bclayton@chromium.org [tools][perfmon] Chunk results by month
    2024-03-20 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 1e3bacded3cb to f2e0306307e4 (5 revisions)
    2024-03-20 bclayton@google.com [cts] Triage macOS + AMD + f16 failures
    2024-03-20 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll Depot Tools from 03ee6d950d4c to 13d20527ff69 (2 revisions)
    2024-03-20 dsinclair@chromium.org Add FoldConstants transform
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/dawn-chromium-autoroll
    Please CC cwallez@google.com,jrprice@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64
    Bug: chromium:328958020
    Tbr: jrprice@google.com
    Include-Ci-Only-Tests: true
    Change-Id: Id2b9850e69139f6871bd96eee89baf2c1001fb4f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5383167
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1276010}

M       DEPS
M       third_party/dawn

https://chromium-review.googlesource.com/5383167


### pe...@google.com (2024-03-22)

Merge review required: a commit with DEPS changes was detected.

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

### am...@google.com (2024-03-22)

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

This fixes a crash in the GPU process. This only affects Windows.

2. What changes specifically would you like to merge? Please link to Gerrit.

This is the specific Gerrit change that landed in Dawn: <https://dawn-review.googlesource.com/c/dawn/+/179706>
Which was then rolled into Chrome with: <https://dawn.googlesource.com/dawn.git/+log/cc21b87a9865..d654129e99a7>

3. Have the changes been released and tested on canary?

Yes, I tested this in Version 125.0.6372.0 (Official Build) canary (64-bit) on Windows. We no longer crash the GPU process.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative?
   <https://goto.google.com/cros-engprodcomponents>

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Not sure if it's major, but it's easy enough to test by downloading the "index.html" file attached to this bug, and opening it in Stable vs Canary. In Stable, the GPU process crashes, and in the Dev Console it says that the GPU device was lost. In Canary, we get the expected compilation failure from DXC:

```
DXC compile failed with: error: validation errors
hlsl.hlsl:11: error: Loop must have break.
Validation failed.

```

### am...@chromium.org (2024-03-22)

Thanks for your work on this. I've closed this as Fixed, based on the CL and merge request. Please re-open if there is additional work to be done.
Closing security bugs as Fixed, allows blintz to update the bug with the appropriate merge labels.
Since there has already been human intervention here, I've gone ahead and added a review label for M122.

### am...@chromium.org (2024-03-22)

sorry -- the new tracker makes a bit too easy to make unintentional atomic changes when trying to view metadata fields

### am...@chromium.org (2024-03-22)

merge approved for this fix <https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5383595> rolled into chromium via Dawn roll <https://crrev.com/c/5383167> to M124 Beta / branch 6367, M123 Stable / branch 6312, and M122 Extended Stable / branch 6261.

Please complete these merges ASAP, for the M123 Stable merge, please complete this merge ASAP before Monday 25 March at 10am PST so this fix can be included in the next M123 Stable security update -- thank you.

### am...@google.com (2024-03-25)

Patch has been merged into M122, M123, and M124:

M122: <https://chromium.googlesource.com/chromium/src.git/+/09fa1e778a70b32b302b3a0042acab3c48aca322>
M123: <https://chromium.googlesource.com/chromium/src.git/+/decc6b5b07bac496f8bad9629b812c72e9b61dfd>
M124: <https://chromium.googlesource.com/chromium/src.git/+/31aef484ef509af19ec458262d3dfd9ea207379e>

### am...@google.com (2024-03-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-27)

Congratulations wgslfuzz! The Chrome VRP Panel has decided to award you $10,000 for this report of memory corruption in a highly privileged process. A member of the Google p2p-vrp finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work!

### pe...@google.com (2024-06-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/328958020)*
