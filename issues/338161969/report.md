#  GPU process crash via WebGPU shader - OOB in WriteInstruction at BitcodeWriter.cpp:1720

| Field | Value |
|-------|-------|
| **Issue ID** | [338161969](https://issues.chromium.org/issues/338161969) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU, Dawn>Tint, Internals>GPU>Dawn, Internals>GPU>Tint |
| **Platforms** | Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-05-01 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this triggers an OOB inside the hlsl compiler.

##### VERSION

Chrome Version: Pre-compiled ASAN Chromium 126.0.6451.0 (Developer Build) (64-bit)   

Operating System: Win11 Build 22631.2861

##### REPRODUCTION CASE

Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process. Note that the shader compiler only crashes if the DirectX back-end supports shader model 6.6. Inspecting the shader model is possible with a Microsoft tool called dxcapsviewer. The UI on my machine shows:

```
NVIDIA GeForce RTX 3090
    Direct3D 12
        Shader Model 6.6

```

Reproducing the issue stand-alone on Linux also possible.

1. Compile the standalone.wgsl with tint (commit 1488c9c94dea5d9bb158870717ebaf2f7d161f57) to hlsl via `./tint standalone.wgsl -o standalone.hlsl`. I also attached standalone.hlsl, but you should get the very same file when compiling standalone.wgsl yourself
2. Compile the hlsl with dxc (commit e7b78ff9c99c19a6a0c98256db9794e0af4eb59d): `./dxc-3.7 standalone.hlsl -T cs_6_6`. This should trigger an ASAN violation.

##### Attached:

- html that should trigger an ASAN violation in chromium (if the native back-end support shader-model 6.6)
- wgsl for producing the hlsl shader
- the hlsl shader
- asan log file

```
[10824:10828:0501/023933.139:WARNING:chrome_main_delegate.cc(742)] This is Chrome version 126.0.6451.0 (not a warning)
[10824:7736:0501/023933.358:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[10824:10828:0501/023933.405:INFO:chrome_browser_cloud_management_controller.cc(161)] Cloud management controller initialization aborted as CBCM is not enabled. Please use the `--enable-chrome-browser-cloud-management` command line flag to enable it if you are not using the official Google Chrome build.
[10824:10752:0501/023933.421:ERROR:sandbox_win.cc(911)] Sandbox cannot access executable. Check filesystem permissions are valid. See https://bit.ly/31yqMJR.: Access is denied. (0x5)
[10824:10828:0501/023933.561:WARNING:account_consistency_mode_manager.cc(77)] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
[10824:10828:0501/023933.749:WARNING:browser_management_service.cc(128)] EnterpriseLogoUrl fetch failed with error code -1 and MIME type 
[10824:10828:0501/023935.125:ERROR:network_service_instance_impl.cc(600)] Network service crashed, restarting service.
[10824:10828:0501/023935.171:WARNING:external_registry_loader_win.cc(232)] Error observing HKLM: 5
[8424:5960:0501/023935.421:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[10824:7724:0501/023938.375:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[8424:6128:0501/023940.427:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[10824:7736:0501/023948.382:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[8424:892:0501/023950.430:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[10824:10828:0501/023957.315:INFO:CONSOLE(20)] "[object GPUDevice]", source: file:///E:/indexValueEnumeratorOOB.html (20)
[10328:3004:0501/023957.459:ERROR:gpu_device.cc(302)] GPUDevice: Entry point "computeSomething" doesn't exist in the shader module [ShaderModule "doubling compute module"].
 - While validating compute stage ([ShaderModule "doubling compute module"], entryPoint: computeSomething).
 - While calling [Device].CreateComputePipeline([ComputePipelineDescriptor "doubling compute pipeline"]).

[10328:3004:0501/023957.459:ERROR:gpu_device.cc(302)] GPUDevice: [Invalid ComputePipeline "doubling compute pipeline"] is invalid.
 - While encoding [ComputePassEncoder "doubling compute pass"].SetPipeline([Invalid ComputePipeline "doubling compute pipeline"]).

[10824:10828:0501/023957.459:INFO:CONSOLE(0)] "Entry point "computeSomething" doesn't exist in the shader module [ShaderModule "doubling compute module"].
 - While validating compute stage ([ShaderModule "doubling compute module"], entryPoint: computeSomething).
 - While calling [Device].CreateComputePipeline([ComputePipelineDescriptor "doubling compute pipeline"]).
", source: file:///E:/indexValueEnumeratorOOB.html (0) 
[10328:3004:0501/023957.459:ERROR:gpu_device.cc(302)] GPUDevice: [Invalid CommandBuffer from CommandEncoder "doubling encoder"] is invalid.
 - While calling [Queue].Submit([[Invalid CommandBuffer from CommandEncoder "doubling encoder"]])

[10824:10828:0501/023957.459:INFO:CONSOLE(0)] "[Invalid ComputePipeline "doubling compute pipeline"] is invalid.
 - While encoding [ComputePassEncoder "doubling compute pass"].SetPipeline([Invalid ComputePipeline "doubling compute pipeline"]).
", source: file:///E:/indexValueEnumeratorOOB.html (0) 
[10824:10828:0501/023957.459:INFO:CONSOLE(0)] "[Invalid CommandBuffer from CommandEncoder "doubling encoder"] is invalid.
 - While calling [Queue].Submit([[Invalid CommandBuffer from CommandEncoder "doubling encoder"]])
", source: file:///E:/indexValueEnumeratorOOB.html (0) 
[10824:7708:0501/024008.389:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[8424:6128:0501/024010.446:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[10824:10828:0501/024037.828:INFO:CONSOLE(20)] "[object GPUDevice]", source: file:///E:/indexValueEnumeratorOOB.html (20)
=================================================================
==7644==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x11a6989f2a88 at pc 0x7ffb3b7e9278 bp 0x00130e9fbe60 sp 0x00130e9fbea8
READ of size 4 at 0x11a6989f2a88 thread T0
==7644==WARNING: Failed to use and restart external symbolizer!
==7644==*** WARNING: Failed to initialize DbgHelp!              ***
==7644==*** Most likely this means that the app is already      *** 
==7644==*** using DbgHelp, possibly with incompatible flags.    *** 
==7644==*** Due to technical reasons, symbolization might crash *** 
==7644==*** or produce wrong results.                           ***
    #0 0x7ffb3b7e9277 in WriteInstruction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Bitcode\Writer\BitcodeWriter.cpp:1720
    #1 0x7ffb3b7a935b in WriteModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Bitcode\Writer\BitcodeWriter.cpp:2419
    #2 0x7ffb3b7996dc in llvm::WriteBitcodeToFile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Bitcode\Writer\BitcodeWriter.cpp:2520
    #3 0x7ffb3d0a0934 in `anonymous namespace'::WriteBitcodePass::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Bitcode\Writer\BitcodeWriterPass.cpp:40
    #4 0x7ffb3bbc9405 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #5 0x7ffb3bbd272c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #6 0x7ffb3b5e0811 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #7 0x7ffb3bcfe191 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #8 0x7ffb3b5db502 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #9 0x7ffb3b5e8cd3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #10 0x7ffb3b4c6b05 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #11 0x7ffb47aa9405 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #12 0x7ffb47b0930e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #13 0x7ffb47bb0b54 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #14 0x7ffb47b7431c in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:87
    #15 0x7ffb479bfc30 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #16 0x7ffb4790ee71 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1996
    #17 0x7ffb4790e857 in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1299
    #18 0x7ffb69cacfad in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #19 0x7ffb696b2e04 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477
    #20 0x7ffb696bb8dd in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1652
    #21 0x7ffb6533f7b2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:982
    #22 0x7ffb6533fc05 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1880
    #23 0x7ffb65334021 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1825
    #24 0x7ffb59056013 in gpu::CommandBufferService::Flush C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:232
    #25 0x7ffb55bbcbcc in gpu::CommandBufferStub::OnAsyncFlush C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:506
    #26 0x7ffb55bbb673 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:154
    #27 0x7ffb59073e4a in gpu::GpuChannel::ExecuteDeferredRequest C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:895
    #28 0x7ffb5908414a in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #29 0x7ffb586765dd in gpu::SchedulerDfs::ExecuteSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:743
    #30 0x7ffb58674938 in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:668
    #31 0x7ffb58677c68 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #32 0x7ffb53aaca20 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #33 0x7ffb57496c66 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #34 0x7ffb57495b89 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #35 0x7ffb574ca37e in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #36 0x7ffb574988ac in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:645
    #37 0x7ffb53af6f30 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #38 0x7ffb5695c71b in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:437
    #39 0x7ffb5239f5d2 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:773
    #40 0x7ffb523a1b53 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1155
    #41 0x7ffb5239d56d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #42 0x7ffb5239e05d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #43 0x7ffb453e16b1 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #44 0x7ff640f243a5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #45 0x7ff640f21db2 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #46 0x7ff6412fd943 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #47 0x7ffbc73c257c in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x18001257c)
    #48 0x7ffbc83eaa47 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005aa47)

0x11a6989f2a88 is located 8 bytes after 1024-byte region [0x11a6989f2680,0x11a6989f2a80)
allocated by thread T0 here:
    #0 0x7ff640ffcb0d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffb3dfd396e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffb3b6c09db in llvm::DenseMapBase<llvm::DenseMap<const clang::TypeDecl *,unsigned int,llvm::DenseMapInfo<const clang::TypeDecl *>,llvm::detail::DenseMapPair<const clang::TypeDecl *,unsigned int> >,const clang::TypeDecl *,unsigned int,llvm::DenseMapInfo<const clang::TypeDecl *>,llvm::detail::DenseMapPair<const clang::TypeDecl *,unsigned int> >::grow C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\ADT\DenseMap.h:427
    #3 0x7ffb3b6c0716 in llvm::DenseMapBase<llvm::DenseMap<clang::RecordDecl *,unsigned int,llvm::DenseMapInfo<clang::RecordDecl *>,llvm::detail::DenseMapPair<clang::RecordDecl *,unsigned int> >,clang::RecordDecl *,unsigned int,llvm::DenseMapInfo<clang::RecordDecl *>,llvm::detail::DenseMapPair<clang::RecordDecl *,unsigned int> >::FindAndConstruct C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\include\llvm\ADT\DenseMap.h:265
    #4 0x7ffb3c91bb1d in llvm::ValueEnumerator::EnumerateType C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Bitcode\Writer\ValueEnumerator.cpp:635
    #5 0x7ffb3c91b092 in llvm::ValueEnumerator::EnumerateValue C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Bitcode\Writer\ValueEnumerator.cpp:601
    #6 0x7ffb3c918b48 in llvm::ValueEnumerator::ValueEnumerator C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Bitcode\Writer\ValueEnumerator.cpp:300
    #7 0x7ffb3b79c2ea in WriteModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Bitcode\Writer\BitcodeWriter.cpp:2380
    #8 0x7ffb3b7996dc in llvm::WriteBitcodeToFile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Bitcode\Writer\BitcodeWriter.cpp:2520
    #9 0x7ffb3d0a0934 in `anonymous namespace'::WriteBitcodePass::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Bitcode\Writer\BitcodeWriterPass.cpp:40
    #10 0x7ffb3bbc9405 in llvm::legacy::PassManagerImpl::run C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #11 0x7ffb3bbd272c in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:779
    #12 0x7ffb3b5e0811 in clang::BackendConsumer::HandleTranslationUnit C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #13 0x7ffb3bcfe191 in clang::ParseAST C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #14 0x7ffb3b5db502 in clang::CodeGenAction::ExecuteAction C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #15 0x7ffb3b5e8cd3 in clang::FrontendAction::Execute C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #16 0x7ffb3b4c6b05 in DxcCompiler::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:982
    #17 0x7ffb47aa9405 in dawn::native::d3d::CompileShader C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #18 0x7ffb47b0930e in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #19 0x7ffb47bb0b54 in dawn::native::d3d12::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:378
    #20 0x7ffb47b7431c in dawn::native::d3d12::ComputePipeline::InitializeImpl C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d12\ComputePipelineD3D12.cpp:87
    #21 0x7ffb479bfc30 in dawn::native::PipelineBase::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #22 0x7ffb4790ee71 in dawn::native::DeviceBase::CreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1996
    #23 0x7ffb4790e857 in dawn::native::DeviceBase::APICreateComputePipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1299
    #24 0x7ffb69cacfad in dawn::wire::server::Server::DoDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:250
    #25 0x7ffb696b2e04 in dawn::wire::server::Server::HandleDeviceCreateComputePipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:477
    #26 0x7ffb696bb8dd in dawn::wire::server::Server::HandleCommandsImpl C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1652
    #27 0x7ffb6533f7b2 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:982


SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\Bitcode\Writer\BitcodeWriter.cpp:1720 in WriteInstruction
Shadow bytes around the buggy address:
  0x11a6989f2800: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11a6989f2880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11a6989f2900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11a6989f2980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11a6989f2a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x11a6989f2a80: fa[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11a6989f2b00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x11a6989f2b80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11a6989f2c00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11a6989f2c80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11a6989f2d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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

==7644==ADDITIONAL INFO

==7644==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffb58674ade in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684
    #1 0x7ffb58674ade in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684
    #2 0x7ffb58674ade in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684
    #3 0x7ffb58674ade in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:684


==7644==END OF ADDITIONAL INFO
==7644==ABORTING
[10824:10828:0501/024125.457:ERROR:gpu_process_host.cc(1002)] GPU process exited unexpectedly: exit_code=1
[10824:10828:0501/024125.457:WARNING:gpu_process_host.cc(1436)] The GPU process has crashed 1 time(s)
[10824:10828:0501/024125.814:WARNING:gpu_process_host.cc(1024)] Reinitialized the GPU process after a crash. The reported initialization time was 256 ms

```

## Attachments

- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 925 B)
- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 916 B)
- [indexDIXLUaf.html](attachments/indexDIXLUaf.html) (text/html, 3.8 KB)
- [asanoob](attachments/asanoob) (application/octet-stream, 20.7 KB)
- [indexValueEnumeratorOOB.html](attachments/indexValueEnumeratorOOB.html) (text/html, 3.1 KB)
- [standalone_reduced.hlsl](attachments/standalone_reduced.hlsl) (application/octet-stream, 536 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-05-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6318625582415872.

### th...@chromium.org (2024-05-01)

It doesn't look like ClusterFuzz is having luck with this. Triaging this speculatively, matching the high severity from <https://crbug.com/328958020>.

I'm also setting the FoundIn speculatively to extended stable (M124).

amaiorano@: This looks similar to some other issues you've looked into recently. Could you PTAL at this issue? Note I am tagging you on two other similar ones as well. Could you please update the FoundIn if you learn that this was introduced more recently than M124?

### pe...@google.com (2024-05-02)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-02)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### am...@google.com (2024-05-03)

[wgslfuzz@gmail.com](mailto:wgslfuzz@gmail.com) the WGSL in the attached `indexDIXLUaf.html` does not match the `standalone.wgsl` and `standalone.hlsl` that you included. Please can you provide the right html file?

In the meantime, I did test our gn build of dxc with asan enabled against `standalone.hlsl`, and I got the same heap-buffer-overflow with the same call stack when passing `-T cs_6_6`. However, I also got the same ASAN failure with a slightly different call stack when passing in `-T cs_6_5` to `-T cs_6_0`, so this does not seem only related to Shader Model 6.6.

Requires further investigation.

### wg...@gmail.com (2024-05-03)

My bad, I accidentally uploaded the same html file as in bug 338071106.
The correct html is attached; just the name of the entry point differs.

### am...@google.com (2024-05-03)

Since this one affects all shader models, will look into this one first.

### am...@google.com (2024-05-03)

I tested opening `indexValueEnumeratorOOB.html` from [comment #7](https://issues.chromium.org/issues/338161969#comment7) in `Version 126.0.6456.0 (Official Build) canary (64-bit)` on my Windows system with an GPU that supports SM 6.5, and I get intermittent GPU process crashes. Sometimes it doesn't crash, and the console output is:

```
DXC compile failed with: Internal Compiler error: 
 - While calling [Device].CreateComputePipeline([ComputePipelineDescriptor "doubling compute pipeline"]).

indexValueEnumeratorOOB.html:1 [Invalid ComputePipeline "doubling compute pipeline"] is invalid.
 - While encoding [ComputePassEncoder "doubling compute pass"].SetPipeline([Invalid ComputePipeline "doubling compute pipeline"]).

indexValueEnumeratorOOB.html:1 [Invalid CommandBuffer from CommandEncoder "doubling encoder"] is invalid.
 - While calling [Queue].Submit([[Invalid CommandBuffer from CommandEncoder "doubling encoder"]])

```

The ASAN failure is 100% reproducible, though.

### am...@google.com (2024-05-03)

I've reduced the `standalone.hlsl` code that still reproduces the ASAN failure to:

```
cbuffer cbuffer_global_uint4 : register(b0) {
  uint4 global_uint4[1];
};

[numthreads(1, 1, 1)]
void main() {
  const bool4 v_bool4 = bool4(true, true, true, true);
  const uint gx = global_uint4[0].x;
  while (true) {
    if (gx == 0u) {
      if (v_bool4.zw[gx] == v_bool4.zy[gx]) {
        GroupMemoryBarrierWithGroupSync();
      }
      return;
    } else {
      bool2 v_bool2 = v_bool4.yy;
      while (true) {
        GroupMemoryBarrierWithGroupSync();
        if (v_bool2[gx]) {
          break;
        }
      }
    }
  }
}

```

### am...@google.com (2024-05-03)

Compiling the reduced hlsl file using different optimization levels reveals some potentially useful info:

With `-O0`:

```
:~/src/dawn$ out/asan/dxc -T cs_6_5 -O0 /mnt/c/Users/amaiorano/Downloads/338161969/standalone_reduced.hlsl
warning: DXIL signing library (dxil.dll,libdxil.so) not found.  Resulting DXIL will not be signed for use in release environments.

error: validation errors
error: Module bitcode is invalid.
error: Stored value type does not match pointer operand type!
  store i32 1, i1* %14
 i1Stored value type does not match pointer operand type!
  store i32 1, i1* %16
 i1Stored value type does not match pointer operand type!
  store i32 1, i1* %22
 i1Stored value type does not match pointer operand type!
  store i32 1, i1* %24
 i1
Validation failed.

```

With `-O1`:

```
~/src/dawn$ out/asan/dxc -T cs_6_5 -O1 /mnt/c/Users/amaiorano/Downloads/338161969/standalone_reduced.hlsl
warning: DXIL signing library (dxil.dll,libdxil.so) not found.  Resulting DXIL will not be signed for use in release environments.

error: validation errors
error: Module bitcode is invalid.
error: Global variable initializer type does not match global variable type!
[2 x i1]* @.hca
Global variable initializer type does not match global variable type!
[2 x i1]* @.hca.1

Validation failed.

```

At `-O2` and `-O3`, the ASAN failure emerges.

The error output for `-O0` and `-O1` indicate that DXC has detected invalid Module bitcode. The ASAN failure is during the `WriteBitcodePass`, so the error comes before that. The specific error is `Stored value type does not match pointer operand type!` and displays some IR. I will dump the full Module IR and see which part it's referring to.

### am...@google.com (2024-05-03)

Spent the day on this, and figured out the problem. It happens when *indexing a swizzled bool vector*. I've put up a fix for it upstream: <https://github.com/microsoft/DirectXShaderCompiler/pull/6582>

### am...@google.com (2024-05-10)

The [fix landed upstream](https://github.com/microsoft/DirectXShaderCompiler/pull/6582) yesterday. Waiting until it's in Canary to test again.

### am...@google.com (2024-05-13)

Tested in Canary Version 126.0.6476.0 (Official Build) canary (64-bit) by opening `indexValueEnumeratorOOB.html` from [comment #7](https://issues.chromium.org/issues/338161969#comment7), and we no longer crash. Instead, as expected since the shader may result in an infinite loop, and does based on the shader inputs, we get the following warning in the Console:

```
ID3D12Device::GetDeviceRemovedReason failed with DXGI_ERROR_DEVICE_HUNG (0x887A0006)
 - While handling unexpected error type Internal when allowed errors are (Validation|DeviceLost).
    at CheckHRESULTImpl (..\..\third_party\dawn\src\dawn\native\d3d\D3DError.cpp:119)

Backend messages:
 * Device removed reason: DXGI_ERROR_DEVICE_HUNG (0x887A0006)

```

Reloading 2 more times, we get the same error, and then we get:

```
Error: No appropriate GPUAdapter found.

```

As expected.

The DXC -> Dawn roll that includes my fix: <https://dawn-review.googlesource.com/c/dawn/+/187586>
The Dawn -> Chromium roll that includes my fix: <https://chromium-review.googlesource.com/c/chromium/src/+/5531126>

### pe...@google.com (2024-05-14)

This is sufficiently serious that it should be merged to extended stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M124. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
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


### am...@google.com (2024-05-14)

1. Which CLs should be backmerged? (Please include Gerrit links.)

The DXC -> Dawn roll that includes my fix: <https://dawn-review.googlesource.com/c/dawn/+/187586>
The Dawn -> Chromium roll that includes my fix: <https://chromium-review.googlesource.com/c/chromium/src/+/5531126>

Note that these will not be backmerged as-is. Rather, we'd cherry-pick the DXC fix directly into Dawn's Chrome release branches.

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes.

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

Yes. Please see my [#comment14](https://issues.chromium.org/issues/338161969#comment14) for how to test this fix.

### pe...@google.com (2024-05-15)

This is sufficiently serious that it should be merged to extended stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M124. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to dev. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
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


### ad...@google.com (2024-05-16)

Please see the answers in [#comment16](https://issues.chromium.org/issues/338161969#comment16).

### am...@chromium.org (2024-05-16)

I've reviewed Canary data for Canary since the Dawn->Chromium ( <https://chromium-review.googlesource.com/c/chromium/src/+/5531126>) roll was for this fix, I don't see any issues related to the upstream fix (<https://github.com/microsoft/DirectXShaderCompiler/pull/6582/files>). Since the goal is to CP this fix onto Dawn Chromium branches, approving for merge to M125 and M124.
Please CP and merge this fix to M125 branch 6422 and M126 branch 6367 at soonest (ideally by 10am PT tomorrow) so this fix can be included in the next M125 and M124 updates.

The roll with the fix was landed on 126, so CP is not needed for 126.

### ap...@google.com (2024-05-16)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6367

commit 867c1001637e9156f13e852e80ce2038fe5c7ca2
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu May 16 14:24:27 2024

    Fix invalid module bitcode when indexing a swizzled bool vector (#6582)
    
    When indexing a swizzled bool vector, some HLSL-specific code in
    EmitCXXMemberOrOperatorMemberCallExpr kicks in to handle the
    HLSLVecType. In this case, we’re dealing with an ExtVectorElt because of
    the swizzle, so this function creates a GEP, Load, and Store on the
    vector. However, boolean scalars are returned as type i11 while the
    store is storing to a bool, which is an i32, so we need to insert a cast
    before the store.
    
    Bug: chromium:338161969
    Change-Id: I45f8ec383be49210a10f725d8266b66fd30c34be
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5545820
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: dan sinclair <dsinclair@google.com>

M       tools/clang/lib/CodeGen/CGExpr.cpp
M       tools/clang/lib/CodeGen/CGExprCXX.cpp
A       tools/clang/test/CodeGenDXIL/operators/swizzle/indexSwizzledBoolVec.hlsl

https://chromium-review.googlesource.com/5545820


### ap...@google.com (2024-05-16)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6422

commit 7679d3a0a821bccbd9c7c33fe2d3aafb48e97af0
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu May 16 14:21:19 2024

    Fix invalid module bitcode when indexing a swizzled bool vector (#6582)
    
    When indexing a swizzled bool vector, some HLSL-specific code in
    EmitCXXMemberOrOperatorMemberCallExpr kicks in to handle the
    HLSLVecType. In this case, we’re dealing with an ExtVectorElt because of
    the swizzle, so this function creates a GEP, Load, and Store on the
    vector. However, boolean scalars are returned as type i11 while the
    store is storing to a bool, which is an i32, so we need to insert a cast
    before the store.
    
    Bug: chromium:338161969
    Change-Id: I5a695989f464391374b46d4dcda0f4e132efa361
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5545819
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: dan sinclair <dsinclair@google.com>

M       tools/clang/lib/CodeGen/CGExpr.cpp
M       tools/clang/lib/CodeGen/CGExprCXX.cpp
A       tools/clang/test/CodeGenDXIL/operators/swizzle/indexSwizzledBoolVec.hlsl

https://chromium-review.googlesource.com/5545819


### ap...@google.com (2024-05-17)

Project: dawn
Branch: chromium/6422

commit bfe28e306e60e986c73adf25cacfc3d246fd1d10
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Fri May 17 00:27:20 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:338161969
    Change-Id: Icea14b79b0e89d26a1656e71180b80f63d654150
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/188661
    Commit-Queue: Antonio Maiorano <amaiorano@google.com>
    Reviewed-by: dan sinclair <dsinclair@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/188661


### ap...@google.com (2024-05-17)

Project: dawn
Branch: chromium/6367

commit c01092832e200d0d784df38e8ce07998f983c38c
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Fri May 17 00:35:41 2024

    DEPS: Update DXC to patched branch
    
    Bug: chromium:338161969
    Change-Id: Iabf855a40672838e040c558c843f8e6e6c1b700e
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/188660
    Reviewed-by: dan sinclair <dsinclair@google.com>
    Reviewed-by: James Price <jrprice@google.com>
    Commit-Queue: Antonio Maiorano <amaiorano@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/188660


### am...@google.com (2024-05-17)

The fix has been cherry-picked to [M124/6367](https://chromium.googlesource.com/chromium/src.git/+/c74a729245b5f06ee937094852369b1ba4ccb313) and [M125/6422](https://chromium.googlesource.com/chromium/src.git/+/67791e3c5758f08fb7e56cd20bb95aa9ac39e6c2).

### sp...@google.com (2024-05-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
OOB write / memory corruption in the GPU process 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are not already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-22)

Thank you for your continued WebGPU research and fuzzing discoveries -- and reporting these issues to us -- great work!

### pe...@google.com (2024-08-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> OOB write / memory corruption in the GPU process 
> 
> Thank you for your efforts and helping us make Chrome more secure for all users!
> 
> Cheers,
> Chrome VRP Panel Bot
> 
> 
> P.S. Two other things we'd like to mention:
> 
> * Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this 

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/338161969)*
