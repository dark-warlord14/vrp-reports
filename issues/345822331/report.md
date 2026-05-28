#  AddressSanitizer: heap-use-after-free on Dawn

| Field | Value |
|-------|-------|
| **Issue ID** | [345822331](https://issues.chromium.org/issues/345822331) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-06-08 |
| **Bounty** | $10,000.00 |

## Description

## Reproduce

1. Download Dawn
   <https://dawn.googlesource.com/dawn/+/HEAD/docs/building.md>
2. Build tint:
   `gn gen out/test --args="is_debug=false is_asan=true dcheck_always_on=false" && ninja -C out/test tint`
3. run: `out/test/tint --format "hlsl" poc.wgsl --dxc out/dxc_harness/libdxcompiler.so"`

I test commit here:

```
commit d9c2ed367198c08e7c56d5eeb93dcea25f5ef0d5 (HEAD -> main, origin/main, origin/HEAD)
Author: Dawn Autoroller <dawn-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Sat Jun 8 04:31:03 2024 +0000

    Roll Depot Tools from e6d8f67fae6c to 954a8d771345 (7 revisions)
    
    https://chromium.googlesource.com/chromium/tools/depot_tools.git/+log/e6d8f67fae6c..954a8d771345
    
    2024-06-08 yiwzhang@google.com error if roll-dep command is called in Cog environment
    2024-06-07 yiwzhang@google.com error if repo command is called in Cog environment
    2024-06-07 jojwang@google.com Fix google-java-format/cipd exists check.
    2024-06-07 yiwzhang@google.com fail gracefully if gclient-new-workdir.py is called in non-git env
    2024-06-07 yiwzhang@google.com fail if fetch command is called in Cog
    2024-06-07 jojwang@google.com Support new third_party/google-java-format/cipd/ path.
    2024-06-07 recipe-mega-autoroller@chops-service-accounts.iam.gserviceaccount.com Roll recipe dependencies (trivial).
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/depot-tools-dawn
    Please CC dsinclair@google.com,webgpu-developers@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Bug: None
    Tbr: dsinclair@google.com
    Change-Id: I903c65a89d2e7345aa7054ecf58a797e3df6f965
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/192247
    Bot-Commit: Dawn Autoroller <dawn-autoroll@skia-public.iam.gserviceaccount.com>
    Commit-Queue: Dawn Autoroller <dawn-autoroll@skia-public.iam.gserviceaccount.com>

```
## CRASH LOG

see asan.txt

## Other

The complete root cause and reproduction on chromium will be released soon.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 13.3 KB)
- [poc.wgsl](attachments/poc.wgsl) (application/octet-stream, 5.8 KB)
- [index.html](attachments/index.html) (text/html, 10.0 KB)

## Timeline

### de...@gmail.com (2024-06-08)

## Reproduce

1. build chromium in windows: <https://chromium.googlesource.com/chromium/src/+/master/docs/windows_build_instructions.md>

- I test commit here:

```
commit 033c53d0fced230d7085f5e9fe5222b6797c3b32 (HEAD -> main, origin/main, origin/HEAD)
Author: David Pennington <dpenning@chromium.org>
Date:   Sat Jun 8 06:48:42 2024 +0000

    [SaveTabGroupsV2] Add a learn more link to the intro IPH.

    Image of Learn More link in bug.

    Bug: 342028422
    Change-Id: I3110a42afe900d24679e47a1d1b2db8d27883de5
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5605535
    Commit-Queue: David Pennington <dpenning@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Darryl James <dljames@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1312401}

```

- args.gn

```
    
is_asan = true
is_debug = false
dcheck_always_on = false
target_cpu = "x64"
is_component_build = true

```

2. Run index.html, The flag `--no-sandbox` is only used for ASAN output.

```
 .\out\asan-release\chrome.exe --no-sandbox http://127.0.0.1:8000

```
## ASAN LOG

```
 .\out\asan-release\chrome.exe --no-sandbox http://127.0.0.1:8000
=================================================================
==24148==ERROR: AddressSanitizer: heap-use-after-free on address 0x11beda54a638 at pc 0x7ffd299db31b bp 0x004b547e9e70 sp 0x004b547e9eb8
WRITE of size 8 at 0x11beda54a638 thread T0
==24148==*** WARNING: Failed to initialize DbgHelp!              ***
==24148==*** Most likely this means that the app is already      ***
==24148==*** using DbgHelp, possibly with incompatible flags.    ***
==24148==*** Due to technical reasons, symbolization might crash ***
==24148==*** or produce wrong results.                           ***
    #0 0x7ffd299db31a in llvm::Use::zap D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\Use.cpp:89
    #1 0x7ffd2995b140 in llvm::User::operator delete D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:133
    #2 0x7ffd29854a9b in llvm::BinaryOperator::~BinaryOperator D:\chromium\src\third_party\dawn\third_party\dxc\include\llvm\IR\InstrTypes.h:134
    #3 0x7ffd2a9e7cc6 in llvm::DeleteDeadBlock D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\BasicBlockUtils.cpp:57
    #4 0x7ffd2aa06afd in llvm::SimplifyCFG D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\SimplifyCFG.cpp:4743
    #5 0x7ffd29bd96af in simplifyFunctionCFG D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\SimplifyCFGPass.cpp:157
    #6 0x7ffd287c5734 in llvm::FPPassManager::runOnFunction D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #7 0x7ffd287c61ce in llvm::FPPassManager::runOnModule D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #8 0x7ffd287c6e85 in llvm::legacy::PassManagerImpl::run D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #9 0x7ffd287d542c in clang::EmitBackendOutput D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:781
    #10 0x7ffd280e44e1 in clang::BackendConsumer::HandleTranslationUnit D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #11 0x7ffd289759d1 in clang::ParseAST D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #12 0x7ffd280de8f2 in clang::CodeGenAction::ExecuteAction D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #13 0x7ffd280ef113 in clang::FrontendAction::Execute D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #14 0x7ffd280480aa in DxcCompiler::Compile D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #15 0x7ffd36a473f2 in dawn::native::d3d::CompileShader D:\chromium\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #16 0x7ffd36abad92 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> D:\chromium\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #17 0x7ffd36b69361 in dawn::native::d3d12::ShaderModule::Compile D:\chromium\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:377
    #18 0x7ffd36b500fb in dawn::native::d3d12::RenderPipeline::InitializeImpl D:\chromium\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:365
    #19 0x7ffd36942b50 in dawn::native::PipelineBase::Initialize D:\chromium\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #20 0x7ffd36876a17 in dawn::native::DeviceBase::CreateRenderPipeline D:\chromium\src\third_party\dawn\src\dawn\native\Device.cpp:2191
    #21 0x7ffd368763f0 in dawn::native::DeviceBase::APICreateRenderPipeline D:\chromium\src\third_party\dawn\src\dawn\native\Device.cpp:1510
    #22 0x7ffd3b2c4c7d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline D:\chromium\src\out\asan-release\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #23 0x7ffd3b2d77d6 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline D:\chromium\src\out\asan-release\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #24 0x7ffd3b2e4df3 in dawn::wire::server::Server::HandleCommandsImpl D:\chromium\src\out\asan-release\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #25 0x7ffd449c5933 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1031
    #26 0x7ffd449c5d96 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1938
    #27 0x7ffd449b72f1 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1883
    #28 0x7ffdd37f6185 in gpu::CommandBufferService::Flush D:\chromium\src\gpu\command_buffer\service\command_buffer_service.cc:231
    #29 0x7ffd4446550e in gpu::CommandBufferStub::OnAsyncFlush D:\chromium\src\gpu\ipc\service\command_buffer_stub.cc:506
    #30 0x7ffd44463f85 in gpu::CommandBufferStub::ExecuteDeferredRequest D:\chromium\src\gpu\ipc\service\command_buffer_stub.cc:154
    #31 0x7ffd44485ce5 in gpu::GpuChannel::ExecuteDeferredRequest D:\chromium\src\gpu\ipc\service\gpu_channel.cc:930
    #32 0x7ffd4449820d in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&,unsigned long long &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams>,unsigned long long>,void ()>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long long),std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams>,unsigned long long>,0,1,2> D:\chromium\src\base\functional\bind_internal.h:1067
    #33 0x7ffdd3832325 in gpu::SchedulerDfs::ExecuteSequence D:\chromium\src\gpu\command_buffer\service\scheduler_dfs.cc:730
    #34 0x7ffdd38306ca in gpu::SchedulerDfs::RunNextTask D:\chromium\src\gpu\command_buffer\service\scheduler_dfs.cc:655
    #35 0x7ffdd3833b56 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(),gpu::SchedulerDfs *>,base::internal::BindState<1,1,0,void (gpu::SchedulerDfs::*)(),base::internal::UnretainedWrapper<gpu::SchedulerDfs,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce D:\chromium\src\base\functional\bind_internal.h:980
    #36 0x7ffddf8464c0 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task_annotator.cc:203
    #37 0x7ffddf8bc82e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:484
    #38 0x7ffddf8bb71a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346
    #39 0x7ffddf70f94e in base::MessagePumpDefault::Run D:\chromium\src\base\message_loop\message_pump_default.cc:40
    #40 0x7ffddf8be4bc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:654
    #41 0x7ffddf7c75f0 in base::RunLoop::Run D:\chromium\src\base\run_loop.cc:134
    #42 0x7ffd864e8c60 in content::GpuMain D:\chromium\src\content\gpu\gpu_main.cc:430
    #43 0x7ffd8ad5aa6a in content::RunOtherNamedProcessTypeMain D:\chromium\src\content\app\content_main_runner_impl.cc:784
    #44 0x7ffd8ad5d485 in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content_main_runner_impl.cc:1156
    #45 0x7ffd8ad58720 in content::RunContentProcess D:\chromium\src\content\app\content_main.cc:332
    #46 0x7ffd8ad591e0 in content::ContentMain D:\chromium\src\content\app\content_main.cc:345
    #47 0x7ffd8e1616a1 in ChromeMain D:\chromium\src\chrome\app\chrome_main.cc:192
    #48 0x7ff6d4ad3bd3 in MainDllLoader::Launch D:\chromium\src\chrome\app\main_dll_loader_win.cc:181
    #49 0x7ff6d4ad1d85 in main D:\chromium\src\chrome\app\chrome_exe_main_win.cc:350
    #50 0x7ff6d4c6c263 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #51 0x7ffe0c407033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #52 0x7ffe0e3e2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x11beda54a638 is located 24 bytes inside of 88-byte region [0x11beda54a620,0x11beda54a678)
freed by thread T0 here:
    #0 0x7ffdde432d0d in operator delete+0x8d (D:\chromium\src\out\asan-release\clang_rt.asan_dynamic-x86_64.dll+0x180052d0d)
    #1 0x7ffd287aa3cb in llvm::PHINode::~PHINode D:\chromium\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:2296
    #2 0x7ffd2995c6a1 in llvm::iplist<llvm::Instruction,llvm::ilist_traits<llvm::Instruction> >::clear D:\chromium\src\third_party\dawn\third_party\dxc\include\llvm\ADT\ilist.h:563
    #3 0x7ffd2995c142 in llvm::BasicBlock::~BasicBlock D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:91
    #4 0x7ffd299602ff in llvm::BasicBlock::~BasicBlock D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\BasicBlock.cpp:70
    #5 0x7ffd2a9438f1 in llvm::removeUnreachableBlocks D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\Local.cpp:1306
    #6 0x7ffd29bd8b3d in simplifyFunctionCFG D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\SimplifyCFGPass.cpp:155
    #7 0x7ffd287c5734 in llvm::FPPassManager::runOnFunction D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #8 0x7ffd287c61ce in llvm::FPPassManager::runOnModule D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #9 0x7ffd287c6e85 in llvm::legacy::PassManagerImpl::run D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #10 0x7ffd287d542c in clang::EmitBackendOutput D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:781
    #11 0x7ffd280e44e1 in clang::BackendConsumer::HandleTranslationUnit D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #12 0x7ffd289759d1 in clang::ParseAST D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #13 0x7ffd280de8f2 in clang::CodeGenAction::ExecuteAction D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #14 0x7ffd280ef113 in clang::FrontendAction::Execute D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #15 0x7ffd280480aa in DxcCompiler::Compile D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #16 0x7ffd36a473f2 in dawn::native::d3d::CompileShader D:\chromium\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #17 0x7ffd36abad92 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> D:\chromium\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #18 0x7ffd36b69361 in dawn::native::d3d12::ShaderModule::Compile D:\chromium\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:377
    #19 0x7ffd36b500fb in dawn::native::d3d12::RenderPipeline::InitializeImpl D:\chromium\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:365
    #20 0x7ffd36942b50 in dawn::native::PipelineBase::Initialize D:\chromium\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #21 0x7ffd36876a17 in dawn::native::DeviceBase::CreateRenderPipeline D:\chromium\src\third_party\dawn\src\dawn\native\Device.cpp:2191
    #22 0x7ffd368763f0 in dawn::native::DeviceBase::APICreateRenderPipeline D:\chromium\src\third_party\dawn\src\dawn\native\Device.cpp:1510
    #23 0x7ffd3b2c4c7d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline D:\chromium\src\out\asan-release\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #24 0x7ffd3b2d77d6 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline D:\chromium\src\out\asan-release\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #25 0x7ffd3b2e4df3 in dawn::wire::server::Server::HandleCommandsImpl D:\chromium\src\out\asan-release\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #26 0x7ffd449c5933 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1031
    #27 0x7ffd449c5d96 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1938

previously allocated by thread T0 here:
    #0 0x7ffdde4324ed in operator new+0x8d (D:\chromium\src\out\asan-release\clang_rt.asan_dynamic-x86_64.dll+0x1800524ed)
    #1 0x7ffd2995b044 in llvm::User::operator new D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\User.cpp:108
    #2 0x7ffd287a8326 in llvm::PHINode::Create D:\chromium\src\third_party\dawn\third_party\dxc\include\llvm\IR\Instructions.h:2340
    #3 0x7ffd2a9b9dbf in `anonymous namespace'::PromoteMem2Reg::run D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\PromoteMemoryToRegister.cpp:669
    #4 0x7ffd2a9b6103 in llvm::PromoteMemToReg D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Utils\PromoteMemoryToRegister.cpp:1086
    #5 0x7ffd29c62f77 in DxilConditionalMem2Reg::runOnFunction D:\chromium\src\third_party\dawn\third_party\dxc\lib\Transforms\Scalar\DxilConditionalMem2Reg.cpp:504
    #6 0x7ffd287c5734 in llvm::FPPassManager::runOnFunction D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1587
    #7 0x7ffd287c61ce in llvm::FPPassManager::runOnModule D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1609
    #8 0x7ffd287c6e85 in llvm::legacy::PassManagerImpl::run D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\LegacyPassManager.cpp:1771
    #9 0x7ffd287d542c in clang::EmitBackendOutput D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:781
    #10 0x7ffd280e44e1 in clang::BackendConsumer::HandleTranslationUnit D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:191
    #11 0x7ffd289759d1 in clang::ParseAST D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\Parse\ParseAST.cpp:164
    #12 0x7ffd280de8f2 in clang::CodeGenAction::ExecuteAction D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\CodeGenAction.cpp:807
    #13 0x7ffd280ef113 in clang::FrontendAction::Execute D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\lib\Frontend\FrontendAction.cpp:455
    #14 0x7ffd280480aa in DxcCompiler::Compile D:\chromium\src\third_party\dawn\third_party\dxc\tools\clang\tools\dxcompiler\dxcompilerobj.cpp:984
    #15 0x7ffd36a473f2 in dawn::native::d3d::CompileShader D:\chromium\src\third_party\dawn\src\dawn\native\d3d\ShaderUtils.cpp:355
    #16 0x7ffd36abad92 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (*)(dawn::native::d3d::D3DCompilationRequest)> D:\chromium\src\third_party\dawn\src\dawn\native\CacheRequest.h:154
    #17 0x7ffd36b69361 in dawn::native::d3d12::ShaderModule::Compile D:\chromium\src\third_party\dawn\src\dawn\native\d3d12\ShaderModuleD3D12.cpp:377
    #18 0x7ffd36b500fb in dawn::native::d3d12::RenderPipeline::InitializeImpl D:\chromium\src\third_party\dawn\src\dawn\native\d3d12\RenderPipelineD3D12.cpp:365
    #19 0x7ffd36942b50 in dawn::native::PipelineBase::Initialize D:\chromium\src\third_party\dawn\src\dawn\native\Pipeline.cpp:371
    #20 0x7ffd36876a17 in dawn::native::DeviceBase::CreateRenderPipeline D:\chromium\src\third_party\dawn\src\dawn\native\Device.cpp:2191
    #21 0x7ffd368763f0 in dawn::native::DeviceBase::APICreateRenderPipeline D:\chromium\src\third_party\dawn\src\dawn\native\Device.cpp:1510
    #22 0x7ffd3b2c4c7d in dawn::wire::server::Server::DoDeviceCreateRenderPipeline D:\chromium\src\out\asan-release\gen\third_party\dawn\src\dawn\wire\server\ServerDoers_autogen.cpp:314
    #23 0x7ffd3b2d77d6 in dawn::wire::server::Server::HandleDeviceCreateRenderPipeline D:\chromium\src\out\asan-release\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:606
    #24 0x7ffd3b2e4df3 in dawn::wire::server::Server::HandleCommandsImpl D:\chromium\src\out\asan-release\gen\third_party\dawn\src\dawn\wire\server\ServerHandlers_autogen.cpp:1682
    #25 0x7ffd449c5933 in gpu::webgpu::`anonymous namespace'::DawnWireServer::HandleCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1031
    #26 0x7ffd449c5d96 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::HandleDawnCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1938
    #27 0x7ffd449b72f1 in gpu::webgpu::`anonymous namespace'::WebGPUDecoderImpl::DoCommands D:\chromium\src\gpu\command_buffer\service\webgpu_decoder_impl.cc:1883

SUMMARY: AddressSanitizer: heap-use-after-free D:\chromium\src\third_party\dawn\third_party\dxc\lib\IR\Use.cpp:89 in llvm::Use::zap
Shadow bytes around the buggy address:
  0x11beda54a380: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11beda54a400: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11beda54a480: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11beda54a500: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11beda54a580: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
=>0x11beda54a600: fa fa f7 fa fd fd fd[fd]fd fd fd fd fd fd fd fa
  0x11beda54a680: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11beda54a700: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11beda54a780: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11beda54a800: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x11beda54a880: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
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

==24148==ADDITIONAL INFO

==24148==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffdd3830851 in gpu::SchedulerDfs::RunNextTask D:\chromium\src\gpu\command_buffer\service\scheduler_dfs.cc:671
    #1 0x7ffdd3828847 in gpu::SchedulerDfs::TryScheduleSequence D:\chromium\src\gpu\command_buffer\service\scheduler_dfs.cc:473


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==24148==END OF ADDITIONAL INFO
==24148==ABORTING
[23564:4256:0608/161528.911:ERROR:gpu_process_host.cc(1007)] GPU process exited unexpectedly: exit_code=1

```

### de...@gmail.com (2024-06-08)

Please CC [amaiorano@google.com](mailto:amaiorano@google.com). I believe you are the owner of this issue.

### de...@gmail.com (2024-06-10)

## Minimize poc(hlsl)

run: `out/tint/dxc -T ps_6_0 -HV 2018 /Zpr /Gis poc.hlsl`

```
static float4 gl_FragCoord = float4(0.0f, 0.0f, 0.0f, 0.0f);

void drawShape_vf2_() {
  int GLF_live4_looplimiter5 = 0;
  int GLF_live7cols = 0;
  int GLF_live7rows = 0;
  int GLF_live7_looplimiter2 = 0;
  int GLF_live7_looplimiter1 = 0;
  int GLF_live7c = 0;
  int GLF_live7r = 0;
  int GLF_live7_looplimiter7 = 0;
  int GLF_live7_looplimiter3 = 0;
  while (true) {
    if ((GLF_live4_looplimiter5 >= 2)) { // 0-7
      break;
    }
    GLF_live4_looplimiter5++;
    GLF_live7cols = 3;
    while (true) {
      if ((GLF_live7cols <= 4)) { // 3-4
      } else {
        break;
      }
      if ((GLF_live7_looplimiter3 >= 2)) {
        break;
      }
      GLF_live7_looplimiter3++;
      GLF_live7rows = 3;
      while (true) {
        if ((GLF_live7rows <= 4)) { // 3-4
        } else { // >=5
          break;
        }
        if ((GLF_live7rows > 7)) { // unreachable
          break;
        }
        GLF_live7_looplimiter2++;
        GLF_live7_looplimiter1 = 0;
        GLF_live7c = 0;
        while (true) {
          if ((GLF_live7_looplimiter1 >= 7)) {
            break;
          }
        }
        {
          GLF_live7rows++;
        }
      }
      {
        GLF_live7cols++;
      }
    }
    while (true) {
      if ((GLF_live7_looplimiter7 >= 7)) {
        break;
      }
      GLF_live7_looplimiter7++;
    }
  }
  return;
}

void main_1() {
  drawShape_vf2_();
  return;
}

void main() {
  main_1();
  return;
}

```
## Root Cause

In dxc, the SimplifyCFGPass is used to optimize the Control Flow Graph (CFG) by simplifying some control structures and basic blocks. The CFGSimplifyPass::runOnFunction function calls the simplifyFunctionCFG function at point [0]:

```
bool runOnFunction(Function &F) override {
    if (PredicateFtor && !PredicateFtor(F))
        return false;

    if (skipOptnoneFunction(F))
        return false;

    AssumptionCache *AC =
        &getAnalysis<AssumptionCacheTracker>().getAssumptionCache(F);
    const TargetTransformInfo &TTI =
        getAnalysis<TargetTransformInfoWrapperPass>().getTTI(F);
    return simplifyFunctionCFG(F, TTI, AC, BonusInstThreshold); // <------------- [0]
}

```

The simplifyFunctionCFG function eventually calls the removeUnreachableBlocks function, which is where the use-after-free (UAF) issue arises.

The removeUnreachableBlocks function removes unreachable basic blocks from the code.

At point [0], it iterates through all the basic blocks and skips reachable blocks at point [1].

At point [2], it iterates through all unreachable basic blocks and removes the references to these blocks from their predecessor blocks.

At point [3], it deletes the unreachable basic blocks, but it does not remove references to the instructions within the deleted basic blocks from other basic blocks. This can cause a use-after-free if other basic blocks reference instructions from the deleted unreachable basic blocks.

```
/// removeUnreachableBlocksFromFn - Remove blocks that are not reachable, even
/// if they are in a dead cycle.  Return true if a change was made, false
/// otherwise.
bool llvm::removeUnreachableBlocks(Function &F) {
    SmallPtrSet<BasicBlock*, 128> Reachable;
    bool Changed = markAliveBlocks(F, Reachable);

    // If there are unreachable blocks in the CFG...
    if (Reachable.size() == F.size())
        return Changed;

    assert(Reachable.size() < F.size());
    NumRemoved += F.size()-Reachable.size();

    // Loop over all of the basic blocks that are not reachable, dropping all of
    // their internal references...
    for (Function::iterator BB = ++F.begin(),  // <----------------------- [0]
         E = F.end(); BB != E; ++BB) {
        if (Reachable.count(BB)) // <----------------------- [1]
            continue;

        for (succ_iterator SI = succ_begin(BB),  // <----------------------- [2]
             SE = succ_end(BB); SI != SE; ++SI)
            if (Reachable.count(*SI))
                (*SI)->removePredecessor(BB); // <----------------------- [2]
        BB->dropAllReferences();
    }

    for (Function::iterator I = ++F.begin(); I != F.end();)
        if (!Reachable.count(I)) // <----------------------- [3]
            I = F.getBasicBlockList().erase(I); // <----------------------- [3]
        else
            ++I;

    return true;
}

```
## Fix

When deleting unreachable basic blocks, because references to instructions within the unreachable basic blocks are not removed from other basic blocks, a use-after-free (UAF) can occur if other basic blocks reference instructions from the deleted unreachable basic blocks.

Therefore, we need to remove all references from other basic blocks to instructions within the unreachable basic blocks before deleting the unreachable basic blocks.

```
diff --git a/lib/Transforms/Utils/Local.cpp b/lib/Transforms/Utils/Local.cpp
index 1b97d5669..b71e36182 100644
--- a/lib/Transforms/Utils/Local.cpp
+++ b/lib/Transforms/Utils/Local.cpp
@@ -1303,7 +1303,16 @@ bool llvm::removeUnreachableBlocks(Function &F) {
 
   for (Function::iterator I = ++F.begin(); I != F.end();)
     if (!Reachable.count(I))
+    {
+      while (!I->empty()) {
+        Instruction &Inst = I->back();
+        if (!Inst.use_empty()) {
+          Inst.replaceAllUsesWith(UndefValue::get(Inst.getType()));
+        }
+        I->getInstList().pop_back();
+      }
       I = F.getBasicBlockList().erase(I);
+    }
     else
       ++I;
 
@@ -1383,4 +1392,4 @@ unsigned llvm::replaceDominatedUsesWith(Value *From, Value *To,
     }
   }
   return Count;
-}
+}

```

### li...@chromium.org (2024-06-10)

I'm wondering if this is similar to the fix landed a [few weeks ago](https://github.com/microsoft/DirectXShaderCompiler/pull/6628), but looks like the suggested fix is in llvm itself.

IIRC don't some shader compilers use a fork of LLVM? Might be that the fork needs to be updated if it's not in a newer version of the compiler.

### am...@google.com (2024-06-10)

Taking a look, thanks.

### pe...@google.com (2024-06-11)

Setting milestone because of s0/s1 severity.

### de...@gmail.com (2024-06-12)

hello, any update? Thanks :)

### pe...@google.com (2024-06-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### am...@google.com (2024-06-12)

Tested in ASAN Chromium build, `chromium-128.0.6535.0-win64-asan`, by opening the attached `index.html` and it no longer crashes the GPU process. Opening the same file in `chromium-127.0.6532.0-win64-asan` does crash the GPU process.

- Fix in Dawn: <https://dawn-review.googlesource.com/c/dawn/+/184422>
- Dawn roll into Chromium with fix: <https://chromium-review.googlesource.com/c/chromium/src/+/5625269>

### pe...@google.com (2024-06-13)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### ch...@google.com (2024-06-13)

1. Which CLs should be backmerged? (Please include Gerrit links.)

- Fix into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/184422>
- Dawn rolled into Chromium: <https://chromium-review.googlesource.com/c/chromium/src/+/5625269>

Note that fix will be cherry-picked into a Dawn custom branch for Chrome release.

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes

3. Does this fix pose any potential non-verifiable stability risks?

No

4. Does this fix pose any known compatibility risks?

No

5. Does it require manual verification by the test team? If so, please describe required testing.

Yes. Test by opening index.html from <https://g-issues.chromium.org/issues/345822331#comment2> in Canary, and note that the GPU process does not crash. The console output does not show any errors, as expected, but simply outputs the GPUDevice and GPURenderPipeline state.

### ch...@google.com (2024-06-13)

Note that this is the same fix as <https://crbug.com/339169163> so they will be cherry-picked together.

### am...@chromium.org (2024-06-14)

since this is the same upstream fix, fix in Dawn, and Chromium roll, merge reviews and approvals will be handled on [crbug.com/339169163](https://crbug.com/339169163) since all the changes and rolls were landed there

### pe...@google.com (2024-06-14)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

- M127, which branched on 2024-06-10 (Chromium branch: 6533, Chromium branch position: 1313161)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove TBD-## from the Merge field and replace it with NA-## (where ## corresponds to the milestone under evaluation). If a merge is necessary, the requested milestone(s) to the Merge-Request field. If you're not sure, reach out to the relevant release manager (can be found at <https://chromiumdash.appspot.com/schedule>).

To learn more about the merge process, including how to land any required merges, see <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>.

### am...@chromium.org (2024-06-17)

merges are being handled on [crbug.com/339169163](https://crbug.com/339169163)

### pe...@google.com (2024-06-18)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

- M127, which branched on 2024-06-10 (Chromium branch: 6533, Chromium branch position: 1313161)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove TBD-## from the Merge field and replace it with NA-## (where ## corresponds to the milestone under evaluation). If a merge is necessary, the requested milestone(s) to the Merge-Request field. If you're not sure, reach out to the relevant release manager (can be found at <https://chromiumdash.appspot.com/schedule>).

To learn more about the merge process, including how to land any required merges, see <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>.

### ch...@google.com (2024-06-18)

Merges to M126 and M127 have already been completed as part of <https://crbug.com/339169163>

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

Congratulations gelatin! Please let us know if you would be interested in submitting your fuzzer to the Chrome Fuzzing program. Thank you for your efforts and reporting this issue to us -- nice work!

### de...@gmail.com (2024-06-22)

I am currently further improving my fuzzer, and once it's completed, I will contact you regarding the Chrome Fuzzer Program. Additionally, I believe I have provided a detailed RCA and patch this time. Please let me know why this is not considered a high-quality report worth $15,000, and I will make improvements. :)

### pe...@google.com (2024-09-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/345822331)*
