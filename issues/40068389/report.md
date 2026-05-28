# Security: stack-use-after-return in tint::wgsl::writer::ASTPrinter::EmitStructType

| Field | Value |
|-------|-------|
| **Issue ID** | [40068389](https://issues.chromium.org/issues/40068389) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | bc...@google.com |
| **Created** | 2023-07-30 |
| **Bounty** | $11,000.00 |

## Description

**VULNERABILITY DETAILS**  

Setting a `rotate` and a `filter` style with the "Skia Graphite" experiment enabled results in stack-use-after-return in the GPU process.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/flag_descriptions.cc;l=3120;drc=aeb76145fe766a359f2e2b7432c207cc135113b6>

**VERSION**  

Chrome Version: 117.0.5917.0  

Operating System: Windows 11

BISECT  

r1176848..r1176860  

<https://chromium.googlesource.com/chromium/src/+log/05fe514b0eab74338558fb0c8baf43e732cdc55c..fd5519a4c16ac2eee81674c9c7d4dfb753fd36cf?pretty=fuller&n=10000>

Based on this commit range, this is most likely caused by Skia roll commit fd5519a4c16ac2eee81674c9c7d4dfb753fd36cf

**REPRODUCTION CASE**  

chrome --no-sandbox --enable-features=SkiaGraphite "data:text/html,<style>\*{ rotate: 1deg 1 1 1; filter: saturate(1); }</style>"

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU Crash State:

==25804==ERROR: AddressSanitizer: stack-use-after-return on address 0x12881b244890 at pc 0x7ffbf7795c70 bp 0x0066793fc070 sp 0x0066793fc0b8  

READ of size 8 at 0x12881b244890 thread T12  

==25804==WARNING: Failed to use and restart external symbolizer!  

==25804==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==25804==\*\*\* Most likely this means that the app is already \*\*\*  

==25804==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==25804==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==25804==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffbf7795c6f in std::\_\_Cr::\_\_murmur2\_or\_cityhash<unsigned long long,64>::\_\_hash\_len\_0\_to\_16 C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_functional\hash.h:175  

#1 0x7ffbfa6853aa in tint::HashmapBase<std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> >,void,8,tint::Hasher<std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> > >,std::\_\_Cr::equal\_to<std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> > > >::Put<0,std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> >,NoValue> C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\tint\utils\containers\hashmap\_base.h:477  

#2 0x7ffbfa68450f in tint::HashmapBase<std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> >,void,8,tint::Hasher<std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> > >,std::\_\_Cr::equal\_to<std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> > > >::Reserve C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\tint\utils\containers\hashmap\_base.h:402  

#3 0x7ffbfa683619 in tint::HashmapBase<std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> >,void,8,tint::Hasher<std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> > >,std::\_\_Cr::equal\_to<std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> > > >::Put<0,std::\_\_Cr::basic\_string<char,std::\_\_Cr::char\_traits<char>,std::\_\_Cr::allocator<char> > &,NoValue> C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\tint\utils\containers\hashmap\_base.h:474  

#4 0x7ffbfa67c419 in tint::wgsl::writer::ASTPrinter::EmitStructType C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\tint\lang\wgsl\writer\ast\_printer\ast\_printer.cc:365  

#5 0x7ffbfa677266 in tint::wgsl::writer::ASTPrinter::EmitTypeDecl C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\tint\lang\wgsl\writer\ast\_printer\ast\_printer.cc:137  

#6 0x7ffbfa67638c in tint::wgsl::writer::ASTPrinter::Generate C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\tint\lang\wgsl\writer\ast\_printer\ast\_printer.cc:106  

#7 0x7ffbfa68761e in tint::wgsl::writer::Generate C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\tint\lang\wgsl\writer\writer.cc:51  

#8 0x7ffbf9c3e97c in dawn::native::stream::Stream[tint::Program,void](javascript:void(0);)::Write C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\StreamImplTint.cpp:36  

#9 0x7ffbf9cd6310 in dawn::native::stream::StreamIn<const tint::Program \*,std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> >,dawn::native::SingleShaderStage,unsigned int,unsigned int,dawn::native::d3d::Compiler,unsigned long long,std::\_\_Cr::basic\_string\_view<wchar\_t,std::\_\_Cr::char\_traits<wchar\_t> >,std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> >,long (\*)(const void \*, unsigned long long, const char \*, const \_D3D\_SHADER\_MACRO \*, ID3DInclude \*, const char \*, const char \*, unsigned int, unsigned int, ID3D10Blob \*\*, ID3D10Blob \*\*),IDxcLibrary \*,IDxcCompiler \*,unsigned int,unsigned int,bool,unsigned int,unsigned int,tint::ExternalTextureOptions,tint::ArrayLengthFromUniformOptions,tint::BindingRemapperOptions,std::\_\_Cr::optional[tint::ast::transform::SubstituteOverride::Config](javascript:void(0);),std::\_\_Cr::bitset<16>,dawn::native::LimitsForCompilationRequest,bool,bool,bool,bool,bool,std::\_\_Cr::vector<tint::BindingPoint,std::\_\_Cr::allocator[tint::BindingPoint](javascript:void(0);) > > C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\dawn\native\stream\Stream.h:72  

#10 0x7ffbf9cd6199 in dawn::native::d3d::HlslCompilationRequest\_\_Contents::VisitAll<`lambda at ..\..\third_party\dawn\src\dawn\native\Serializable.h:33:21'> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d\D3DCompilationRequest.h:88 #11 0x7ffbf9cd5e31 in dawn::native::stream::StreamIn<dawn::native::d3d::HlslCompilationRequest,dawn::native::d3d::D3DBytecodeCompilationRequest,dawn::native::CacheKey::UnsafeUnkeyedValue<dawn::platform::Platform \*> > C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\stream\Stream.h:73 #12 0x7ffbf9cd51d7 in dawn::native::CacheRequestImpl<dawn::native::d3d::D3DCompilationRequest>::CreateCacheKey C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:84 #13 0x7ffbf9cd35d9 in dawn::native::LoadOrRun<dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (\*)(dawn::native::Blob),dawn::Result<dawn::native::d3d::CompiledShader,dawn::native::ErrorData> (\*)(dawn::native::d3d::D3DCompilationRequest)> C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\CacheRequest.h:114 #14 0x7ffbf9cd15ba in dawn::native::d3d11::ShaderModule::Compile C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d11\ShaderModuleD3D11.cpp:192 #15 0x7ffbf9cca152 in dawn::native::d3d11::RenderPipeline::InitializeShaders C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d11\RenderPipelineD3D11.cpp:443 #16 0x7ffbf9cc81f5 in dawn::native::d3d11::RenderPipeline::Initialize C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\d3d11\RenderPipelineD3D11.cpp:207 #17 0x7ffbf9b4671d in dawn::native::DeviceBase::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1708 #18 0x7ffbf9b45f77 in dawn::native::DeviceBase::APICreateRenderPipeline C:\b\s\w\ir\cache\builder\src\third_party\dawn\src\dawn\native\Device.cpp:1210 #19 0x7ffbf9a33d7d in dawn::native::NativeDeviceCreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\native\ProcTable.cpp:813 #20 0x7ffbf82f6549 in wgpu::Device::CreateRenderPipeline C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\dawn\src\dawn\webgpu_cpp.cpp:2338 #21 0x7ffbf8a75d45 in skgpu::graphite::DawnGraphicsPipeline::Make C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\graphite\dawn\DawnGraphicsPipeline.cpp:529 #22 0x7ffbf8a7b723 in skgpu::graphite::DawnResourceProvider::createGraphicsPipeline C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\graphite\dawn\DawnResourceProvider.cpp:193 #23 0x7ffbf89d2f6d in skgpu::graphite::ResourceProvider::findOrCreateGraphicsPipeline C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\graphite\ResourceProvider.cpp:54 #24 0x7ffbf897c855 in skgpu::graphite::DrawPass::prepareResources C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\graphite\DrawPass.cpp:651 #25 0x7ffbf89c2f97 in skgpu::graphite::RenderPassTask::prepareResources C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\graphite\RenderPassTask.cpp:52 #26 0x7ffbf89f2165 in skgpu::graphite::TaskGraph::prepareResources C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\graphite\TaskGraph.cpp:26 #27 0x7ffbf89ba3c6 in skgpu::graphite::Recorder::snap C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\graphite\Recorder.cpp:159 #28 0x7ffc0bd2547d in viz::SkiaOutputSurfaceImpl::EndPaint C:\b\s\w\ir\cache\builder\src\components\viz\service\display_embedder\skia_output_surface_impl.cc:898 #29 0x7ffc151a8589 in viz::SkiaRenderer::EndPaint C:\b\s\w\ir\cache\builder\src\components\viz\service\display\skia_renderer.cc:3824 #30 0x7ffc151a74c6 in viz::SkiaRenderer::FinishDrawingRenderPass C:\b\s\w\ir\cache\builder\src\components\viz\service\display\skia_renderer.cc:3227 #31 0x7ffc151dad59 in viz::DirectRenderer::DrawRenderPass C:\b\s\w\ir\cache\builder\src\components\viz\service\display\direct_renderer.cc:772 #32 0x7ffc151d59bc in viz::DirectRenderer::DrawRenderPassAndExecuteCopyRequests C:\b\s\w\ir\cache\builder\src\components\viz\service\display\direct_renderer.cc:603 #33 0x7ffc151d2281 in viz::DirectRenderer::DrawFrame C:\b\s\w\ir\cache\builder\src\components\viz\service\display\direct_renderer.cc:415 #34 0x7ffc10b47d9d in viz::Display::DrawAndSwap C:\b\s\w\ir\cache\builder\src\components\viz\service\display\display.cc:915 #35 0x7ffc10b37737 in viz::DisplayScheduler::DrawAndSwap C:\b\s\w\ir\cache\builder\src\components\viz\service\display\display_scheduler.cc:224 #36 0x7ffc10b34594 in viz::DisplayScheduler::OnBeginFrameDeadline C:\b\s\w\ir\cache\builder\src\components\viz\service\display\display_scheduler.cc:542 #37 0x7ffc10b3aed1 in base::internal::Invoker<base::internal::BindState<void (viz::DisplayScheduler::\*)(),base::WeakPtr<viz::DisplayScheduler> >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:957 #38 0x7ffc0555c877 in base::DeadlineTimer::OnScheduledTaskInvoked C:\b\s\w\ir\cache\builder\src\base\timer\timer.cc:305 #39 0x7ffc0555ddcc in base::internal::Invoker<base::internal::BindState<void (base::MetronomeTimer::\*)(),base::internal::UnretainedWrapper<base::MetronomeTimer,base::unretained_traits::MayNotDangle,0> >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:957 #40 0x7ffc055a7f46 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:201 #41 0x7ffc08d45d62 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:480 #42 0x7ffc08d44aef in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:345 #43 0x7ffc08d7d663 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40 #44 0x7ffc08d4848f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:645 #45 0x7ffc056128e7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134 #46 0x7ffc0556675d in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:337 #47 0x7ffc05566c12 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:409 #48 0x7ffc054c0f31 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:133  

#49 0x7ff7383cdc65 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:291  

#50 0x7ffd157c26ac in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x1800126ac)  

#51 0x7ffd1742aa67 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005aa67)

Address 0x12881b244890 is located in stack of thread T12 at offset 144 in frame  

#0 0x7ffbfa683457 in tint::HashmapBase<std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> >,void,8,tint::Hasher<std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> > >,std::\_\_Cr::equal\_to<std::\_\_Cr::basic\_string\_view<char,std::\_\_Cr::char\_traits<char> > > >::Put<0,std::\_\_Cr::basic\_string<char,std::\_\_Cr::char\_traits<char>,std::\_\_Cr::allocator<char> > &,NoValue> C:\b\s\w\ir\cache\builder\src\third\_party\dawn\src\tint\utils\containers\hashmap\_base.h:471

This frame has 7 object(s):  

[32, 72) '\_\_t.i'  

[112, 128) 'hash' (line 477)  

[144, 168) 'ref.tmp' (line 493) <== Memory access at offset 144 is inside this variable  

[208, 248) 'evicted' (line 518)  

[288, 312) 'ref.tmp34' (line 518)  

[352, 384) 'diags' (line 533)  

[416, 728) 'ref.tmp60' (line 534)  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork  

(longjmp, SEH and C++ exceptions \*are\* supported)  

Thread T12 created by T0 here:  

#0 0x7ff7383cc7a2 in CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffc054bfc8f in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:198  

#2 0x7ffc05565910 in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:210  

#3 0x7ffc03704ebe in viz::VizCompositorThreadRunnerImpl::VizCompositorThreadRunnerImpl C:\b\s\w\ir\cache\builder\src\components\viz\service\main\viz\_compositor\_thread\_runner\_impl.cc:90  

#4 0x7ffc0370afeb in viz::VizMainImpl::VizMainImpl C:\b\s\w\ir\cache\builder\src\components\viz\service\main\viz\_main\_impl.cc:90  

#5 0x7ffc0bc43163 in content::GpuChildThread::GpuChildThread C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_child\_thread.cc:124  

#6 0x7ffc0bc422dd in content::GpuChildThread::GpuChildThread C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_child\_thread.cc:110  

#7 0x7ffc083397bd in content::GpuMain C:\b\s\w\ir\cache\builder\src\content\gpu\gpu\_main.cc:372  

#8 0x7ffc03c78387 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:745  

#9 0x7ffc03c7b197 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1118  

#10 0x7ffc03c75e04 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:326  

#11 0x7ffc03c76a91 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:343  

#12 0x7ffbf7751722 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:187  

#13 0x7ff738316084 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#14 0x7ff738312a9c in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#15 0x7ff73874d6db in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#16 0x7ffd157c26ac in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x1800126ac)  

#17 0x7ffd1742aa67 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005aa67)

SUMMARY: AddressSanitizer: stack-use-after-return C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_functional\hash.h:175 in std::\_\_Cr::\_\_murmur2\_or\_cityhash<unsigned long long,64>::\_\_hash\_len\_0\_to\_16  

Shadow bytes around the buggy address:  

0x12881b244600: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x12881b244680: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x12881b244700: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x12881b244780: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x12881b244800: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

=>0x12881b244880: f5 f5[f5]f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x12881b244900: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x12881b244980: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x12881b244a00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x12881b244a80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x12881b244b00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb

==25804==ADDITIONAL INFO

==25804==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x7ffc10b3a16a in viz::DisplayScheduler::ScheduleBeginFrameDeadline C:\b\s\w\ir\cache\builder\src\components\viz\service\display\display\_scheduler.cc:509  

#1 0x7ffc05d89929 in mojo::SimpleWatcher::Context::Notify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:102

==25804==END OF ADDITIONAL INFO  

==25804==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [buggy-spirv.txt](attachments/buggy-spirv.txt) (text/plain, 56.1 KB)

## Timeline

### [Deleted User] (2023-07-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-31)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5101520351330304.

### th...@chromium.org (2023-07-31)

I am not able to reproduce this on Linux tip of tree and ClusterFuzz also found it unreproducible (on Windows). Are you still able to reproduce this on tip of tree?

And just to confirm: There are no specific gestures needed to reproduce once the chrome tab has loaded, right?

### st...@gmail.com (2023-07-31)

I am able to reproduce this on ToT on Windows. Yup, there is no user interaction.

Looking at the ClusterFuzz logs, it seems that it fails to use Skia Graphite. I don't see the same error on my machine -- maybe it's a VM limitation?

https://clusterfuzz.com/testcase-detail/5101520351330304#:~:text=083045.531%3AERROR%3Ashared_context_state.cc(409)%5D-,Skia%20Graphite%20disabled,-%3A%20Graphite%20Context%20creation%20failed.

### [Deleted User] (2023-07-31)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2023-07-31)

Thanks for those details. I'm able to reproduce this on Mac (not on a VM). I can reproduce this on M117 but not M116. Setting severity as high because this is a stack-use-after-return in the GPU process. Setting security impact none because this is behind SkiaGraphite, which does not have a field trial enabled.

sunnyps@: Could you PTAL?

(Speculatively setting OS to Desktop platforms.)

[Monorail components: Internals>GPU>Internals]

### su...@chromium.org (2023-07-31)

We plan to start finching SkiaGraphite in the next couple of months so this report is timely.

dneto: Who's the best person on the tint team to look into this? The repro seems to be pretty simple, but since the crash occurs deep in tint code, it's unlikely anyone on our side will be able to make much progress on it so any help is much appreciated.

[Monorail components: -Internals>GPU>Internals Internals>GPU>Tint]

### cw...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### bc...@google.com (2023-08-02)

I'd investigate, but I'm on vacation until next week.
Dan or James, can you spare a moment to look into this please?

### ds...@google.com (2023-08-02)

Is it possible to get SkiaGraphite to dump out the shader it's generating before sending to Dawn? This looks like it's gone to Dawn, we've converted to a Program and we're now attempting to re-create the WGSL to cache the file.

If you can get me the shader as output by SkiaGraphite I can try to dig deeper. (My chrome tree is months out of date so may take a while to get up and running again)

### ds...@google.com (2023-08-02)

Turns out, SkiaGraphite isn't available on linux. So, I'm unable to dump the Shader. Sunny, if you can dump the generated shader and attach to the issue please assign back to me and I can push along further.

### bl...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

### jo...@google.com (2023-08-03)

Added dneto@ to triage since this appears to be a security bug inside Tint.

### jo...@google.com (2023-08-03)

Oh never mind, I see Dan Sinclair is already on it! 

### su...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

### su...@chromium.org (2023-08-03)

I was able to reproduce this on Windows with an ASAN build. Got tint to disassemble and print the SPIRV just before the crash - attached it.

### bc...@google.com (2023-08-07)

I see what's going on. Fix incoming.

### bc...@google.com (2023-08-14)

Should be fixed with https://dawn-review.googlesource.com/c/dawn/+/145260

### [Deleted User] (2023-08-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a718258062ba755770e409f9df9712c2fc578500

commit a718258062ba755770e409f9df9712c2fc578500
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Aug 23 20:52:18 2023

Roll Dawn from 092f3f12f369 to 415eb24e0b6c (22 revisions)

https://dawn.googlesource.com/dawn.git/+log/092f3f12f369..415eb24e0b6c

2023-08-23 sunnyps@chromium.org graphite: Dump SPIR-V disassembly with DumpShaders toggle
2023-08-23 dsinclair@chromium.org [eval] Make a TransformTernaryElements
2023-08-23 dsinclair@chromium.org [eval] Add a TransformUnaryElement method
2023-08-23 dsinclair@chromium.org [eval] Make a un-templated TransformBinaryElement
2023-08-23 enga@chromium.org Fix CTS roller swarming build request parent run id
2023-08-23 bclayton@google.com Add tools/OWNERS
2023-08-23 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from 0ef565c50e04 to 711db27554bc (9 revisions)
2023-08-23 dsinclair@chromium.org [eval] Remove template param from TransformBinaryDifferingArityElements
2023-08-23 shrekshao@google.com Raise suppression for a cts test on win intel
2023-08-23 dsinclair@chromium.org [eval] Rename method for clarity
2023-08-23 rharrison@chromium.org Update run-cts error from '--dawn-node' to '--bin'
2023-08-23 bclayton@google.com [tint][resolver] Fix use after free, causing UA to be ignored.
2023-08-23 nexa@google.com Updated the CMakeLists to use Dawn on Android.
2023-08-23 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from ceb93445a393 to d2ca5166ee7c (11 revisions)
2023-08-23 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll DirectX Shader Compiler from 104604638f69 to f9219a906eff (1 revision)
2023-08-23 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from aaeeea0c42a8 to 0ef565c50e04 (14 revisions)
2023-08-23 cwallez@chromium.org Validate T2T copy ranges before common restrictions.
2023-08-23 shrekshao@google.com Use TextureBuiltinFromUniform transform in dawn
2023-08-23 gman@chromium.org Add buffer to more bind messages
2023-08-23 jiawei.shao@intel.com Implement read-only storage texture on D3D12, Vulkan and Metal
2023-08-22 bsheedy@google.com Remove duplicate Android expectation
2023-08-22 shrekshao@google.com Suppress cts flakes

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/dawn-chromium-autoroll
Please CC cwallez@google.com,shrekshao@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel
Bug: chromium:1462375,chromium:1468848,chromium:1469851,chromium:1474717
Tbr: shrekshao@google.com
Test: Test: dawn_end2end_tests
Change-Id: Icf9d846784ee87334d372c4a223c6b6ab4084263
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4808452
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1187484}

[modify] https://crrev.com/a718258062ba755770e409f9df9712c2fc578500/third_party/dawn
[modify] https://crrev.com/a718258062ba755770e409f9df9712c2fc578500/DEPS


### am...@google.com (2023-09-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-07)

Congratulations Thomas! The VRP Panel has decided to award you $10,000 for this report of a memory corruption bug in the GPU process + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-20)

This issue was migrated from crbug.com/chromium/1468848?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068389)*
