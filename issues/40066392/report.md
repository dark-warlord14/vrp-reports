# Security: [ANGLE] metal : Out-of-bounds memory can be accessed on DrawCmd

| Field | Value |
|-------|-------|
| **Issue ID** | [40066392](https://issues.chromium.org/issues/40066392) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | ne...@nesk.kr |
| **Assignee** | kb...@chromium.org |
| **Created** | 2023-06-26 |
| **Bounty** | $10,000.00 |

## Description

# **VULNERABILITY DETAILS** AddressSanitizer:DEADLYSIGNAL

==37564==ERROR: AddressSanitizer: SEGV on unknown address 0x0005ed394c8c (pc 0x0001ed05dd20 bp 0x00028f600970 sp 0x00028f600920 T26)  

==37564==The signal is caused by a READ memory access.  

==37564==WARNING: invalid path to external symbolizer!  

==37564==WARNING: Failed to use and restart external symbolizer!  

#0 0x1ed05dd20 in -[AGXG14XFamilyRenderContext drawPrimitives:vertexStart:vertexCount:]+0xc8 (/System/Library/Extensions/AGXMetalG14X.bundle/Contents/MacOS/AGXMetalG14X:arm64+0x41fd20) (BuildId: 247dee6890793f328bcbdecebfb6c3ad32000000200000000100000000040d00)  

#1 0xad6d00029965e714 (<unknown module>)  

#2 0x29965cf28 in rx::mtl::RenderCommandEncoder::endEncodingImpl(bool)+0x424 (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/116.0.5840.0/Libraries/libGLESv2.dylib:arm64+0x9e0f28) (BuildId: 4c4c446f55553144a1accd4debf6e07b32000000200000000100000000000b00)  

#3 0x2995b26e0 in rx::ContextMtl::endEncoding(bool)+0x14c (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/116.0.5840.0/Libraries/libGLESv2.dylib:arm64+0x9366e0) (BuildId: 4c4c446f55553144a1accd4debf6e07b32000000200000000100000000000b00)  

#4 0x2995b4d4c in rx::ContextMtl::onDrawFrameBufferChangedState(gl::Context const\*, rx::FramebufferMtl\*, bool)+0x2f0 (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/116.0.5840.0/Libraries/libGLESv2.dylib:arm64+0x938d4c) (BuildId: 4c4c446f55553144a1accd4debf6e07b32000000200000000100000000000b00)  

#5 0x2995afa68 in rx::ContextMtl::syncState(gl::Context const\*, angle::BitSetT<64ul, unsigned long long, unsigned long> const&, angle::BitSetT<64ul, unsigned long long, unsigned long> const&, angle::BitSetT<11ul, unsigned int, unsigned long> const&, angle::BitSetT<11ul, unsigned int, unsigned long> const&, gl::Command)+0xa2c (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/116.0.5840.0/Libraries/libGLESv2.dylib:arm64+0x933a68) (BuildId: 4c4c446f55553144a1accd4debf6e07b32000000200000000100000000000b00)  

#6 0x299097680 in gl::Context::invalidateFramebuffer(unsigned int, int, unsigned int const\*)+0x26c (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/116.0.5840.0/Libraries/libGLESv2.dylib:arm64+0x41b680) (BuildId: 4c4c446f55553144a1accd4debf6e07b32000000200000000100000000000b00)  

#7 0x13f65fd14 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDiscardFramebufferEXT(unsigned int, int, unsigned int const volatile\*)+0x270 (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_gles2.dylib:arm64+0x107d14) (BuildId: 4c4c447f55553144a182475a1f98430032000000200000000100000000000b00)  

#8 0x13f5f99ec in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile\*, int, int\*)+0x1b4 (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_gles2.dylib:arm64+0xa19ec) (BuildId: 4c4c447f55553144a182475a1f98430032000000200000000100000000000b00)  

#9 0x10aab29c8 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface\*)+0x490 (/Users/nesk/chromium/src/out/AsanRelease/libgpu.dylib:arm64+0x4e9c8) (BuildId: 4c4c442655553144a162b1ca7c9d0b6f32000000200000000100000000000b00)  

#10 0x13bf89d54 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::\_\_Cr::vector<gpu::SyncToken, std::\_\_Cr::allocator[gpu::SyncToken](javascript:void(0);)> const&)+0x2a0 (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_ipc\_service.dylib:arm64+0x5d54) (BuildId: 4c4c442e55553144a122eb630926bb3f32000000200000000100000000000b00)  

#11 0x13bf88c44 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&)+0x1cc (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_ipc\_service.dylib:arm64+0x4c44) (BuildId: 4c4c442e55553144a122eb630926bb3f32000000200000000100000000000b00)  

#12 0x13bfa2e28 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);))+0x3d0 (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_ipc\_service.dylib:arm64+0x1ee28) (BuildId: 4c4c442e55553144a122eb630926bb3f32000000200000000100000000000b00)  

#13 0x13bfb2704 in void base::internal::FunctorTraits<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), void>::Invoke<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);) const&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)>(void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);) const&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&)+0x14c (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_ipc\_service.dylib:arm64+0x2e704) (BuildId: 4c4c442e55553144a122eb630926bb3f32000000200000000100000000000b00)  

#14 0x10aae3f98 in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x720 (/Users/nesk/chromium/src/out/AsanRelease/libgpu.dylib:arm64+0x7ff98) (BuildId: 4c4c442655553144a162b1ca7c9d0b6f32000000200000000100000000000b00)  

#15 0x10aae23d4 in gpu::SchedulerDfs::RunNextTask()+0x170 (/Users/nesk/chromium/src/out/AsanRelease/libgpu.dylib:arm64+0x7e3d4) (BuildId: 4c4c442655553144a162b1ca7c9d0b6f32000000200000000100000000000b00)  

#16 0x1068379dc in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x1bf9dc) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#17 0x106890f90 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0x7a8 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x218f90) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#18 0x106890408 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x130 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x218408) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#19 0x106a9f568 in base::MessagePumpCFRunLoopBase::RunWork()+0x1d4 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x427568) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#20 0x106a0acbc in base::mac::CallWithEHFrame(void () block\_pointer)+0xc (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x392cbc) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#21 0x106a9d490 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x13c (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x425490) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#22 0x186ef2638 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f638) (BuildId: 203e44018c2e3157a24b92f52551d43e32000000200000000100000000040d00)  

#23 0xad47000186ef25cc (<unknown module>)  

#24 0xe415800186ef233c (<unknown module>)  

#25 0x6a7c800186ef0f44 (<unknown module>)  

#26 0xbe0e000186ef04b4 (<unknown module>)  

#27 0x8a79000187e69fc8 (<unknown module>)  

#28 0xa87a800106aa10bc (<unknown module>)  

#29 0x106a9c030 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*)+0x23c (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x424030) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#30 0x106892b0c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x354 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x21ab0c) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#31 0x1067aaf8c in base::RunLoop::Run(base::Location const&)+0x430 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x132f8c) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#32 0x10691b4c0 in base::Thread::Run(base::RunLoop\*)+0xdc (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x2a34c0) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#33 0x10691b910 in base::Thread::ThreadMain()+0x3c8 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x2a3910) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#34 0x10697afac in base::(anonymous namespace)::ThreadFunc(void\*)+0xe0 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x302fac) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#35 0x10524d6e4 in \_\_sanitizer\_weak\_hook\_memcmp+0x349c8 (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x4d6e4) (BuildId: 4c4c443e55553144a1400716444dd55532000000200000000100000000000b00)  

#36 0x186e13fa4 in \_pthread\_start+0x90 (/usr/lib/system/libsystem\_pthread.dylib:arm64+0x6fa4) (BuildId: 46d35233a0513f4fbba4ba56dddc4d1a32000000200000000100000000040d00)  

#37 0x254f800186e0ed9c (<unknown module>)

==37564==Register values:  

x[0] = 0x000000028f600618 x[1] = 0x000063200039a954 x[2] = 0x0000000000000208 x[3] = 0x0000000000000041  

x[4] = 0x0000001501648b80 x[5] = 0x0000000000000002 x[6] = 0x0000000000000000 x[7] = 0x0000000000000000  

x[8] = 0x00000001ed394c90 x[9] = 0x0000000172ce8058 x[10] = 0x0000000172ce8060 x[11] = 0x0000000345884008  

x[12] = 0x0000000172d4c060 x[13] = 0x00000015008a90f0 x[14] = 0x000000034ff31118 x[15] = 0x3f80000000000000  

x[16] = 0x000010700001ffff x[17] = 0x00000002263159c8 x[18] = 0x0000000000000000 x[19] = 0x000060d0001ce060  

x[20] = 0x0000632000390800 x[21] = 0x0000000000008866 x[22] = 0xffffffffffffffff x[23] = 0x0000000000000000  

x[24] = 0x0000000000000078 x[25] = 0x000063200039b438 x[26] = 0x000063200039b068 x[27] = 0x0000000000000258  

x[28] = 0x00006110003fcb80 fp = 0x000000028f600970 lr = 0x08498001ed05dd18 sp = 0x000000028f600920  

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (/System/Library/Extensions/AGXMetalG14X.bundle/Contents/MacOS/AGXMetalG14X:arm64+0x41fd20) (BuildId: 247dee6890793f328bcbdecebfb6c3ad32000000200000000100000000040d00) in -[AGXG14XFamilyRenderContext drawPrimitives:vertexStart:vertexCount:]+0xc8  

Thread T26 created by T0 here:  

#0 0x1052487cc in \_\_sanitizer\_weak\_hook\_memcmp+0x2fab0 (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x487cc) (BuildId: 4c4c443e55553144a1400716444dd55532000000200000000100000000000b00)  

#1 0x10697a4cc in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadType, base::MessagePumpType)+0x1d8 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x3024cc) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#2 0x10691a200 in base::Thread::StartWithOptions(base::Thread::Options)+0x47c (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x2a2200) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#3 0x111cc7de0 in content::GpuProcessHost::Init()+0x44c (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1463de0) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#4 0x111cc77dc in content::GpuProcessHost::Get(content::GpuProcessKind, bool)+0x140 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x14637dc) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#5 0x111c96204 in content::BrowserGpuChannelHostFactory::EstablishRequest::Establish(bool)+0xd8 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1432204) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#6 0x111c95fec in content::BrowserGpuChannelHostFactory::EstablishRequest::Create(int, unsigned long long, bool, std::\_\_Cr::vector<base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>, std::\_\_Cr::allocator<base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>>>)+0x20c (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1431fec) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#7 0x111c98df4 in content::BrowserGpuChannelHostFactory::EstablishGpuChannel(base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>, bool)+0x8e8 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1434df4) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#8 0x111c98450 in content::BrowserGpuChannelHostFactory::EstablishGpuChannel(base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>)+0x114 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1434450) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#9 0x111c97970 in content::BrowserGpuChannelHostFactory::Initialize(bool)+0x1f4 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1433970) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#10 0x1115fcd20 in content::BrowserMainLoop::PostCreateThreadsImpl()+0x32c (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd98d20) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#11 0x1115fbed0 in content::BrowserMainLoop::PostCreateThreads()+0xf0 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd97ed0) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#12 0x112c8f920 in content::StartupTaskRunner::RunAllTasksNow()+0x148 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x242b920) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#13 0x1115fb4ec in content::BrowserMainLoop::CreateStartupTasks()+0x6cc (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd974ec) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#14 0x1116036d8 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams)+0x158 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd9f6d8) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#15 0x1115f7e58 in content::BrowserMain(content::MainFunctionParams)+0x174 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd93e58) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#16 0x113b353fc in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*)+0x210 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32d13fc) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#17 0x113b37bdc in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x378 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32d3bdc) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#18 0x113b37578 in content::ContentMainRunnerImpl::Run()+0x5bc (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32d3578) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#19 0x113b334d4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*)+0x9ec (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32cf4d4) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#20 0x113b339f0 in content::ContentMain(content::ContentMainParams)+0x144 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32cf9f0) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#21 0x119e16908 in ChromeMain+0x424 (/Users/nesk/chromium/src/out/AsanRelease/libchrome\_dll.dylib:arm64+0xa908) (BuildId: 4c4c44d955553144a14eb5b18d3feb4c32000000200000000100000000000b00)  

#22 0x104ac4bb4 in main+0x22c (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000bb4) (BuildId: 4c4c44a755553144a1708036cdec4a1432000000200000000100000000000b00)  

#23 0x186abbf24 (<unknown module>)  

#24 0xa373fffffffffffc (<unknown module>)

==37564==ADDITIONAL INFO

==37564==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x10aada854 in gpu::SchedulerDfs::TryScheduleSequence(gpu::SchedulerDfs::Sequence\*)+0x544 (/Users/nesk/chromium/src/out/AsanRelease/libgpu.dylib:arm64+0x76854) (BuildId: 4c4c442655553144a162b1ca7c9d0b6f32000000200000000100000000000b00)  

#1 0x1060ad914 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x29c (/Users/nesk/chromium/src/out/AsanRelease/libmojo\_public\_system\_cpp.dylib:arm64+0x19914) (BuildId: 4c4c442155553144a1be8c5f8846060032000000200000000100000000000b00)  

#2 0x106439fe8 in mojo::(anonymous namespace)::ThreadSafeInterfaceEndpointClientProxy::SendMessage(mojo::Message&)+0x108 (/Users/nesk/chromium/src/out/AsanRelease/libmojo\_public\_cpp\_bindings.dylib:arm64+0x29fe8) (BuildId: 4c4c446355553144a174cd99a9e91f4e32000000200000000100000000000b00)  

#3 0x108d56480 in cc::Scheduler::ScheduleBeginImplFrameDeadline()+0x4fc (/Users/nesk/chromium/src/out/AsanRelease/libcc.dylib:arm64+0x1f6480) (BuildId: 4c4c447055553144a1b0aee4d3a1543032000000200000000100000000000b00)

==37564==END OF ADDITIONAL INFO  

==37564==ABORTING  

[0626/154312.747780:WARNING:process\_memory\_mac.cc(93)] mach\_vm\_read(0x104b10000, 0x8000): (os/kern) invalid address (1)  

[0626/154312.749199:WARNING:process\_memory\_mac.cc(93)] mach\_vm\_read(0x104b10000, 0x8000): (os/kern) invalid address (1)  

[0626/154312.750349:WARNING:process\_memory\_mac.cc(93)] mach\_vm\_read(0x104b10000, 0x8000): (os/kern) invalid address (1)  

[0626/154312.750720:WARNING:process\_memory\_mac.cc(93)] mach\_vm\_read(0x104b10000, 0x8000): (os/kern) invalid address (1)  

[0626/154312.751472:WARNING:process\_memory\_mac.cc(93)] mach\_vm\_read(0x104b10000, 0x8000): (os/kern) invalid address (1)  

[0626/154312.770358:WARNING:in\_range\_cast.h(38)] value -634136515 out of range  

[0626/154312.792243:WARNING:crash\_report\_exception\_handler.cc(235)] UniversalExceptionRaise: (os/kern) failure (5)  

zsh: abort ./out/AsanRelease/Chromium.app/Contents/MacOS/Chromium --no-sandbox

**REPRODUCTION CASE**  

I am trying to minimize testcase will upload it later.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: GPU Process  

Crash State: See asan.log

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 18.3 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.4 KB)

## Timeline

### [Deleted User] (2023-06-26)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2023-06-26)

VERSION
Chrome Version: [116.0.5840.0] + [Dev build & Asan]
Operating System: macOS Ventura 13.4 (Apple M2 Pro)

GPU INFO
GL_RENDERER : ANGLE (Apple, Apple M2 Pro, OpenGL 4.1 Metal - 83.1)
GL_VERSION : OpenGL ES 2.0.0 (ANGLE 2.1.21313 git hash: 24f4007b93e0)

Chromium Build Flags (args.gn)
```
is_debug=false
symbol_level=1
is_asan=true
is_component_build = true
dcheck_always_on = false
enable_nacl = false
is_ubsan=false
```

REPRODUCTION CASE
I've attached a minimized testcase. 

The following parameters are required to enable the Metal backend

```
./Chromium.app/Contents/MacOS/Chromium --no-sandbox --incognito --disable-in-process-stack-traces --use-gl=angle --use-angle=metal poc.html
```

### cl...@chromium.org (2023-06-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4993078328492032.

### cl...@chromium.org (2023-06-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5273116772859904.

### pa...@chromium.org (2023-06-27)

I was able to reproduce the issue on ToT macos build. Setting this as severity high for now until owner changes it. I'll try to check whether this is reproducible before 116.

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2023-06-27)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-06-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@nesk.kr (2023-06-27)

The issue can also be reproduced on version 114.0.5735.133 (stable, arm64)

```
(lldb) r --single-process --no-sandbox --use-gl=angle --use-angle=metal poc.html
Process 38056 launched: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' (arm64)
Process 38056 stopped
* thread #24, name = 'Chrome_InProcGpuThread', stop reason = EXC_BAD_ACCESS (code=1, address=0x5ed394c8c)
    frame #0: 0x00000001ed05dd20 AGXMetalG14X`-[AGXG14XFamilyRenderContext drawPrimitives:vertexStart:vertexCount:] + 200
AGXMetalG14X`-[AGXG14XFamilyRenderContext drawPrimitives:vertexStart:vertexCount:]:
->  0x1ed05dd20 <+200>: ldr    w8, [x8, w22, uxtw #2]
    0x1ed05dd24 <+204>: and    w8, w8, #0xfffeffff
    0x1ed05dd28 <+208>: stp    w8, w21, [sp]
    0x1ed05dd2c <+212>: mov    w8, #0x1
Target 0: (Google Chrome) stopped.

(lldb) register read 
General Purpose Registers:
        x0 = 0x00000001789c84b8
        x1 = 0x00000118090aa33c
        x2 = 0x0000000000000000
        x3 = 0x00000001789c8680
        x4 = 0x00000116906e1c9c
        x5 = 0x0000000000000008
        x6 = 0x0000000000000000
        x7 = 0x0000000000000000
        x8 = 0x00000001ed394c90  AGXMetalG14X`AGX::VDMEncoderGen4<AGX::G14X::ESLEncoder, AGX::G14X::DeviceConstants, AGX::G14X::VsStateConfig>::PrimitiveTypeToVDMCTRLTypeNonIndexedDraw
        x9 = 0x0000000110ee4058
       x10 = 0x0000000110ee4060
       x11 = 0x0000000113678008
       x12 = 0x0000000111700060
       x13 = 0x0000001501db10f0
       x14 = 0x0000000115499118
       x15 = 0x3f80000000000000
       x16 = 0x0000000186e42640  libsystem_platform.dylib`_platform_memmove
       x17 = 0x00000002263159c8
       x18 = 0x0000000000000000
       x19 = 0x000001181015b860
       x20 = 0x00000118090a0000
       x21 = 0x0000000000008866
       x22 = 0xffffffffffffffff
       x23 = 0x0000000000000000
       x24 = 0x0000000000000078
       x25 = 0x00000118090aac38
       x26 = 0x00000118090aa868
       x27 = 0x0000000000000001
       x28 = 0x00000001d66ee710  
        fp = 0x00000001789c8810
        lr = 0x00000001ed05dd18  AGXMetalG14X`-[AGXG14XFamilyRenderContext drawPrimitives:vertexStart:vertexCount:] + 192
        sp = 0x00000001789c87c0
        pc = 0x00000001ed05dd20  AGXMetalG14X`-[AGXG14XFamilyRenderContext drawPrimitives:vertexStart:vertexCount:] + 200
      cpsr = 0x60001000

(lldb) bt
* thread #24, name = 'Chrome_InProcGpuThread', stop reason = EXC_BAD_ACCESS (code=1, address=0x5ed394c8c)
  * frame #0: 0x00000001ed05dd20 AGXMetalG14X`-[AGXG14XFamilyRenderContext drawPrimitives:vertexStart:vertexCount:] + 200
    frame #1: 0x00000001085c6ce4 libGLESv2.dylib`___lldb_unnamed_symbol2269 + 42168
    frame #2: 0x00000001085c619c libGLESv2.dylib`___lldb_unnamed_symbol2269 + 39280
    frame #3: 0x0000000108594420 libGLESv2.dylib`ANGLEResetDisplayPlatform + 1562792
    frame #4: 0x00000001085928b8 libGLESv2.dylib`ANGLEResetDisplayPlatform + 1555776
    frame #5: 0x00000001083d82bc libGLESv2.dylib`glShadingRateQCOM + 1095520
    frame #6: 0x000000011d06b2ac Google Chrome Framework`___lldb_unnamed_symbol5040 + 202848
```

### sy...@chromium.org (2023-06-27)

CC metal/ folks.

### es...@chromium.org (2023-06-28)

kbr can you please take a look or help triage?

### kb...@chromium.org (2023-06-29)

The test case issues a draw with no buffers bound. The draw call is conceptually legal at the OpenGL level. The vertex shader's attributes, vPosition and texCoord0, are supposed to be constant values in this case.

I'm not sure how the vertex shader is translated at the Metal level, and in particular how it handles the case of an attribute which is a constant value - not bound to a buffer. This seems to be where the bug is - vertex fetch is accessing memory it shouldn't.

CC'ing colleagues from Apple. Kyle, Kimmo, Dan - do you know how this is expected to work?

Shabi - is this governed by the ActiveDefaultAttribsMask in the StateCache, and associated dirty bits?
https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/Context.h;l=135?q=getActiveDefaultAttribsMask


[Monorail components: Blink>WebGL]

### le...@chromium.org (2023-06-29)

- This test case calls drawArray with mode=10 (first argument). This translates to mode=GL_LINES_ADJACENCY.
- The frontend passes primitive mode = LinesAdjacent to metal backend. I'm not sure why the frontend's validation didn't catch this before passing to metal backend. Since metal sure doesn't support LinesAdjacent.
- The metal backend then tried to convert primitive mode to MTLPrimitiveType, but because the primitive mode is not supported, it returned 0xffffffff instead [1]. 0xffffffff is not a primitive value supported by metal, it is a custom defined value in mtl_utils.h. I think this led to the crash inside Metal framework.

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/metal/mtl_utils.mm;drc=409bf13406dce692315050703df4a68558cc0008;l=1247

### le...@chromium.org (2023-06-30)

[Empty comment from Monorail migration]

### le...@chromium.org (2023-06-30)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-06-30)

Thanks Quyen for investigating and for your CL https://chromium-review.googlesource.com/c/angle/angle/+/4659980 . I think something is wrong with the validation; GL_LINES_ADJACENCY was only introduced in ES 3.2, and ANGLE should definitely not be accepting it as a valid enum for WebGL contexts. I'm looking into this now.


### kb...@chromium.org (2023-06-30)

In https://crbug.com/angleproject/5483 and https://crbug.com/chromium/1185267 maintenance of the StateCache's valid draw modes was revised. The new code needs to check for a client GLES context of version 3.2, or any of the geometry shader extensions, in order to advertise any of the _ADJACENCY modes for lines or triangles (GL_LINES_ADJACENCY, GL_LINE_STRIP_ADJACENCY, GL_TRIANGLES_ADJACENCY, GL_TRIANGLE_STRIP_ADJACENCY).


### ti...@google.com (2023-06-30)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-06-30)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-06-30)

https://chromium-review.googlesource.com/c/angle/angle/+/4661672 is up for review fixing the validation and adding assertions to the Metal backend rather than early-outs.


### gi...@appspot.gserviceaccount.com (2023-07-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/9d9ca90bf05f6219989ca00fa28c9e792c106673

commit 9d9ca90bf05f6219989ca00fa28c9e792c106673
Author: Kenneth Russell <kbr@chromium.org>
Date: Fri Jun 30 22:31:03 2023

Properly validate _ADJACENCY primitive modes.

After a refactoring in https://crbug.com/angleproject/5483 and Issue
chromium:1185267, the _ADJACENCY primitive modes were being validated
as legal in context versions where they were not supported.

Thanks to lehoangquyen@ for an initial version of this CL and one of
the two new tests. Verified locally on an ASAN build on macOS (by
manually disabling SwiftShader, where ASAN does not work) that the new
tests pass cleanly.

Test: SimpleOperationTest.PrimitiveModeLinesAdjacentNegativeTest
Test: SimpleOperationTest.DrawsWithNoAttributeData
Bug: chromium:1457840
Change-Id: Icb0945e0081ca6f97355dc60f75d60c3f4f68565
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4661672
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/9d9ca90bf05f6219989ca00fa28c9e792c106673/src/tests/gl_tests/SimpleOperationTest.cpp
[modify] https://crrev.com/9d9ca90bf05f6219989ca00fa28c9e792c106673/src/libANGLE/renderer/metal/mtl_command_buffer.mm
[modify] https://crrev.com/9d9ca90bf05f6219989ca00fa28c9e792c106673/src/libANGLE/Context.cpp


### kb...@chromium.org (2023-07-05)

Not completely sure in which Chrome release ANGLE's Metal backend is aimed to be enabled by default, but this fix must be merged back to that release. Requesting merge to M116.


### [Deleted User] (2023-07-05)

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2023-07-05)

1. High severity security issue, though not yet shipping to Stable.
2. https://chromium-review.googlesource.com/c/angle/angle/+/4661672
3. Not yet, but they have been thoroughly tested locally.
4. Yes, it's a new feature (ANGLE's Metal backend). It is behind a Finch flag and being experimented upon in Canary/Dev/Beta per:
https://source.corp.google.com/search?q=DefaultANGLEMetal
https://source.corp.google.com/piper///depot/google3/googledata/googleclient/chrome/finch/gcl_studies/Metal.gcl;l=118?q=DefaultANGLEMetal&sq=package:piper%20file:%2F%2Fdepot%2Fgoogle3%20-file:google3%2Fexperimental
5. N/A
6. Does not require manual verification. Crash is likely only observed in ASAN builds, though the out-of-bounds access occurred in product builds.


### kb...@chromium.org (2023-07-05)

Correction to #6: the GPU process crash can be seen in release builds with the supplied proof of concept. While manual verification is not required, it would be appreciated.


### gi...@appspot.gserviceaccount.com (2023-07-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/018481a73c0268351617d1cb4bbdf790c355f145

commit 018481a73c0268351617d1cb4bbdf790c355f145
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jul 05 21:46:42 2023

Roll ANGLE from 8a8c8fc280d7 to ec8fb51b69d2 (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/8a8c8fc280d7..ec8fb51b69d2

2023-07-05 cnorthrop@google.com Tests: Add Evony: The King's Return trace
2023-07-05 kbr@chromium.org Properly validate _ADJACENCY primitive modes.
2023-07-05 syoussefi@chromium.org Make glClearColor/Depth/Stencil entry points lockless

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,ianelliott@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1457840
Tbr: ianelliott@google.com
Test: Test: SimpleOperationTest.DrawsWithNoAttributeData
Test: Test: SimpleOperationTest.PrimitiveModeLinesAdjacentNegativeTest
Test: Test: angle_trace_tests --gtest_filter="*evony_the_kings_return*"
Change-Id: I940093251d4c1f3f8713fb6fb7811f8aedfa9575
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4667289
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1166169}

[modify] https://crrev.com/018481a73c0268351617d1cb4bbdf790c355f145/DEPS


### [Deleted User] (2023-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-06)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-07-06)

The fix is shipping in Canary as of 117.0.5874.0, and I've confirmed locally that the proof-of-concept no longer crashes the GPU process, but generates WebGL errors as expected.


### kb...@chromium.org (2023-07-06)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-07-06)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-07-07)

amyressler@ could you please approve this M116 security fix merge?


### gi...@appspot.gserviceaccount.com (2023-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e61c81d7bca633f86ca4edeebd16370e69437a84

commit e61c81d7bca633f86ca4edeebd16370e69437a84
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jul 10 12:34:35 2023

Manual roll ANGLE from 20cc4a9bc250 to 66c2e4fca248 (35 revisions)

Manual roll requested by ynovikov@google.com

https://chromium.googlesource.com/angle/angle.git/+log/20cc4a9bc250..66c2e4fca248

2023-07-07 aredulla@google.com [ssci] Added Shipped field to READMEs
2023-07-07 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from c421d230f1c1 to 869b279baef4 (3 revisions)
2023-07-07 syoussefi@chromium.org Make glIsEnabled* entry points lockless
2023-07-07 syoussefi@chromium.org Make pack/unpack and hint entry points lockless
2023-07-07 syoussefi@chromium.org Make glStencil* entry points lockless
2023-07-07 syoussefi@chromium.org Make glBlend* entry points lockless
2023-07-06 syoussefi@chromium.org Make various state setting entry points lockless
2023-07-06 syoussefi@chromium.org Make glEnable/Disable entry points lockless
2023-07-06 syoussefi@chromium.org Fix multi-draw's gl_DrawID in non-multi-draw draws
2023-07-06 syoussefi@chromium.org Vulkan: Optimize PBO download between RGBA and BGRA
2023-07-06 yuxinhu@google.com Update dEQP-GLES mustpass List
2023-07-06 syoussefi@chromium.org Make glColor/DepthMask entry points lockless
2023-07-06 syoussefi@chromium.org Revert "Cleanup multiview support"
2023-07-06 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from df22aa218f6a to c421d230f1c1 (7 revisions)
2023-07-06 ianelliott@google.com Mac: Suppress flaky/crashing test
2023-07-06 sunnyps@chromium.org gl: Handle copyTexSubImage2D failures manually
2023-07-05 syoussefi@chromium.org Workaround app bug with using ESSL 100 extension in ESSL 310
2023-07-05 cnorthrop@google.com Tests: Add Evony: The King's Return trace
2023-07-05 kbr@chromium.org Properly validate _ADJACENCY primitive modes.
2023-07-05 syoussefi@chromium.org Make glClearColor/Depth/Stencil entry points lockless
2023-07-05 ynovikov@chromium.org Roll chromium_revision ad19957265..e506ce09ba (1165395:1165897)
2023-07-05 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 222e07b368b1 to 3e73cce1c470 (1 revision)
2023-07-05 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 347306080b87 to df22aa218f6a (1 revision)
2023-07-04 angle-autoroll@skia-public.iam.gserviceaccount.com Manual roll vulkan-deps from e21365bc9170 to 347306080b87 (3 revisions)
2023-07-04 angle-autoroll@skia-public.iam.gserviceaccount.com Manual roll vulkan-deps from 2b2cba62bfea to e21365bc9170 (38 revisions)
2023-07-04 ynovikov@chromium.org Expand dEQP-EGL suppression
2023-07-04 ynovikov@chromium.org Roll chromium_revision 2e0371f07e..ad19957265 (1162850:1165395)
2023-07-04 lexa.knyazev@gmail.com Cleanup multiview support
2023-07-04 m.maiya@samsung.com Update ANGLEExtensionAvailability test expectation
2023-07-04 sunnyps@chromium.org gl: Use ANGLE_GL_TRY_ALWAYS_CHECK for CopyTexSubImage
2023-07-04 ianelliott@google.com Vulkan: Suppress VVL "VUID-vkCmdDraw-None-08608"
2023-07-03 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 14fa1a826dad to 2e0371f07e01 (1224 revisions)
2023-07-03 angle-autoroll@skia-public.iam.gserviceaccount.com Roll VK-GL-CTS from 12bc45af35d5 to e7b180ad5366 (12 revisions)
2023-07-03 angle-autoroll@skia-public.iam.gserviceaccount.com Manual roll vulkan-deps from 23a32754e715 to 2b2cba62bfea (29 revisions)
2023-06-30 i.nazarov@samsung.com Use compare_exchange_weak() in AllocateGlobalMutexImpl()

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,ianelliott@google.com,ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1456553,chromium:1457840,chromium:1457915,chromium:1458040,chromium:1462139,chromium:1462478,chromium:1462504,chromium:1462505,chromium:1462506,chromium:1462531
Tbr: ianelliott@google.com,ynovikov@google.com
Test: Test: ImageTest.ANGLEExtensionAvailability*
Test: Test: SimpleOperationTest.DrawsWithNoAttributeData
Test: Test: SimpleOperationTest.PrimitiveModeLinesAdjacentNegativeTest
Test: Test: angle_trace_tests --gtest_filter="*evony_the_kings_return*"
Change-Id: I95fcf52cc3511cba4bccb0e5b65662e42f2e06a7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4675508
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1168029}

[modify] https://crrev.com/e61c81d7bca633f86ca4edeebd16370e69437a84/DEPS


### am...@chromium.org (2023-07-10)

https://chromium-review.googlesource.com/c/angle/angle/+/4661672 approved for merge to M116 
please merge to branch 5845 at your earliest convenience, before 10am Pacific Friday, 13 July -- next M116 dev and the first release coming out of the two-week release freeze 

### am...@chromium.org (2023-07-10)

apologies -- the above merge deadline should read "10am Pacific Thursday, 13 July" 

### kb...@chromium.org (2023-07-10)

https://chromium-review.googlesource.com/c/angle/angle/+/4672003 up for review, merging to ANGLE's branch for Chromium M116 (chromium/5845 in the ANGLE repo).


### gi...@appspot.gserviceaccount.com (2023-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/70b0a25845f064f57793cc595f61801ac9045446

commit 70b0a25845f064f57793cc595f61801ac9045446
Author: Kenneth Russell <kbr@chromium.org>
Date: Fri Jun 30 22:31:03 2023

[M116] Properly validate _ADJACENCY primitive modes.

After a refactoring in https://crbug.com/angleproject/5483 and Issue
chromium:1185267, the _ADJACENCY primitive modes were being validated
as legal in context versions where they were not supported.

Thanks to lehoangquyen@ for an initial version of this CL and one of
the two new tests. Verified locally on an ASAN build on macOS (by
manually disabling SwiftShader, where ASAN does not work) that the new
tests pass cleanly.

Test: SimpleOperationTest.PrimitiveModeLinesAdjacentNegativeTest
Test: SimpleOperationTest.DrawsWithNoAttributeData
Bug: chromium:1457840
Change-Id: Icb0945e0081ca6f97355dc60f75d60c3f4f68565
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4661672
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 9d9ca90bf05f6219989ca00fa28c9e792c106673)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4672003

[modify] https://crrev.com/70b0a25845f064f57793cc595f61801ac9045446/src/tests/gl_tests/SimpleOperationTest.cpp
[modify] https://crrev.com/70b0a25845f064f57793cc595f61801ac9045446/src/libANGLE/renderer/metal/mtl_command_buffer.mm
[modify] https://crrev.com/70b0a25845f064f57793cc595f61801ac9045446/src/libANGLE/Context.cpp


### am...@google.com (2023-07-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-19)

Congratulations, n3sk! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1457840?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>ANGLE]
[Monorail blocked-on: crbug.com/angleproject/5483, crbug.com/chromium/1185267]
[Monorail blocking: crbug.com/chromium/1322521]
[Monorail mergedwith: crbug.com/angleproject/8240, crbug.com/angleproject/8241]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066392)*
