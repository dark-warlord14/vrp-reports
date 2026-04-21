# UAF in SharedImageManager of GPU

| Field | Value |
|-------|-------|
| **Issue ID** | [40062056](https://issues.chromium.org/issues/40062056) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU |
| **Platforms** | Mac |
| **Reporter** | he...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2022-12-06 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

Will attach details later

**Problem Description:**  

UAF in GPU

**Additional Comments:**

\*\*Chrome version: \*\* 110.0.5458.0 \*\*Channel: \*\* Canary

**OS:** Mac OS

## Attachments

- [repro.sh](attachments/repro.sh) (text/plain, 20.5 KB)
- [intel-repro.txt](attachments/intel-repro.txt) (text/plain, 43.3 KB)
- [asan0.txt](attachments/asan0.txt) (text/plain, 28.5 KB)
- [asan1.txt](attachments/asan1.txt) (text/plain, 26.4 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 25.6 KB)
- [1396212_test.html](attachments/1396212_test.html) (text/plain, 47.9 KB)

## Timeline

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### he...@gmail.com (2022-12-06)

The repro is a little bit tricky and I'm still minimizing the repro method. Tested on the 110.0.5461.0 MacOS chromium.

## initial RCA

The GPUChannel of the SharedImageBacking maybe somehow destroyed before the SharedImageManager::OnRepresentationDestroyed is called.

In `SharedImageManager::OnRepresentationDestroyed` [1], it would destroy the found `SharedImageBacking`. The destruction of `SharedImageBacking` will consequently called `IOSurfaceImageBacking::~IOSurfaceImageBacking` and `gles2::TexturePassthrough::~TexturePassthrough()`. 

Since the backing GPUChannel is freed, this would lead to the UAF when trying to delete the backing texture [2]. 


[1]https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/shared_image/shared_image_manager.cc;l=378;drc=e05f074ee710b56e2ff9c044e062808e754aebd2

[2]https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/texture_manager.cc;l=547;drc=6b4af5d8208398839e90c7adc2da22c0288d6b47

The RCA may not correct and I'm still trying to minimizing the reproduction method.

### he...@gmail.com (2022-12-06)

==79406==ERROR: AddressSanitizer: heap-use-after-free on address 0x603000139f00 at pc 0x000135ef5528 bp 0x00016fc3cdc0 sp 0x00016fc3cdb8
READ of size 8 at 0x603000139f00 thread T0
==79406==WARNING: invalid path to external symbolizer!
==79406==WARNING: Failed to use and restart external symbolizer!
    #0 0x135ef5524 in gpu::gles2::TexturePassthrough::~TexturePassthrough()+0x18c (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x315524) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #1 0x135f75494 in gpu::IOSurfaceImageBacking::ReleaseGLTexture(gpu::IOSurfaceBackingEGLState*, bool)+0x23c (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x395494) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #2 0x135f78eb0 in gpu::IOSurfaceImageBacking::IOSurfaceBackingEGLStateBeingDestroyed(gpu::IOSurfaceBackingEGLState*, bool)+0xd0 (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x398eb0) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #3 0x135f715c0 in gpu::IOSurfaceBackingEGLState::~IOSurfaceBackingEGLState()+0x88 (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x3915c0) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #4 0x135f74fdc in gpu::IOSurfaceImageBacking::~IOSurfaceImageBacking()+0xec (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x394fdc) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #5 0x135f7524c in gpu::IOSurfaceImageBacking::~IOSurfaceImageBacking()+0x8 (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x39524c) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #6 0x135ed3948 in base::internal::flat_tree<std::Cr::unique_ptr<gpu::SharedImageBacking, std::Cr::default_delete<gpu::SharedImageBacking> >, base::identity, std::Cr::less<void>, std::Cr::vector<std::Cr::unique_ptr<gpu::SharedImageBacking, std::Cr::default_delete<gpu::SharedImageBacking> >, std::Cr::allocator<std::Cr::unique_ptr<gpu::SharedImageBacking, std::Cr::default_delete<gpu::SharedImageBacking> > > > >::erase(std::Cr::__wrap_iter<std::Cr::unique_ptr<gpu::SharedImageBacking, std::Cr::default_delete<gpu::SharedImageBacking> >*>)+0x1a8 (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x2f3948) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #7 0x135ed36a0 in gpu::SharedImageManager::OnRepresentationDestroyed(gpu::Mailbox const&, gpu::SharedImageRepresentation*)+0x398 (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x2f36a0) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #8 0x135edb70c in gpu::SharedImageRepresentationFactoryRef::~SharedImageRepresentationFactoryRef()+0x19c (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x2fb70c) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #9 0x135edb874 in gpu::SharedImageRepresentationFactoryRef::~SharedImageRepresentationFactoryRef()+0x8 (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x2fb874) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #10 0x135ecd390 in base::internal::flat_tree<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef, std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> >, base::identity, std::Cr::less<void>, std::Cr::vector<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef, std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> >, std::Cr::allocator<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef, std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> > > > >::erase(std::Cr::__wrap_iter<std::Cr::unique_ptr<gpu::SharedImageRepresentationFactoryRef, std::Cr::default_delete<gpu::SharedImageRepresentationFactoryRef> >*>)+0x1a8 (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x2ed390) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #11 0x135ecd0a8 in gpu::SharedImageFactory::DestroySharedImage(gpu::Mailbox const&)+0x1e8 (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x2ed0a8) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #12 0x1337ca700 in gpu::SharedImageStub::OnDestroySharedImage(gpu::Mailbox const&)+0x148 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x5e700) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #13 0x1337c86bc in gpu::SharedImageStub::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredSharedImageRequest>)+0x3e4 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x5c6bc) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #14 0x13378785c in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>)+0x2dc (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x1b85c) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #15 0x133795abc in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&)+0x140 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x29abc) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #16 0x102f7ee0c in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x610 (/Users/happy/source/chromium/src/out/asan/libgpu.dylib:arm64+0x7ae0c) (BuildId: 4c4c44bf55553144a1a2a77b3ac2187232000000200000000100000000000b00)
    #17 0x102f7d4e4 in gpu::SchedulerDfs::RunNextTask()+0x154 (/Users/happy/source/chromium/src/out/asan/libgpu.dylib:arm64+0x794e4) (BuildId: 4c4c44bf55553144a1a2a77b3ac2187232000000200000000100000000000b00)
    #18 0x10227f204 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x304 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x1d7204) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #19 0x1022d2638 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x724 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x22a638) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #20 0x1022d1a2c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x150 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x229a2c) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #21 0x1023fb328 in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x353328) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #22 0x1023e2ad0 in base::mac::CallWithEHFrame(void () block_pointer)+0xc (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x33aad0) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #23 0x1023f93ec in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x13c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3513ec) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #24 0x1a8585a30 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x81a30) (BuildId: f4ff83fce62c30b4b3a9876c8a1fd59532000000200000000100000000000d00)
    #25 0xd66c0001a85859c4  (<unknown module>)
    #26 0x2a3e8001a8585734  (<unknown module>)
    #27 0x60410001a8584338  (<unknown module>)
    #28 0xb6610001a85838a0  (<unknown module>)
    #29 0x77730001a948be54  (<unknown module>)
    #30 0xc1040001023fd174  (<unknown module>)
    #31 0x1023f809c in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x270 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x35009c) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #32 0x1022d3fec in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x338 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x22bfec) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #33 0x1021fca80 in base::RunLoop::Run(base::Location const&)+0x3c0 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x154a80) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #34 0x10b5fba88 in content::GpuMain(content::MainFunctionParams)+0x880 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0xba88) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)
    #35 0x10e27dff0 in content::RunOtherNamedProcessTypeMain(std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x4cc (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x2c8dff0) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)
    #36 0x10e27f9b0 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x2c8f9b0) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)
    #37 0x10e27bb58 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0xf60 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x2c8bb58) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)
    #38 0x10e27c254 in content::ContentMain(content::ContentMainParams)+0x134 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x2c8c254) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)
    #39 0x1129f1694 in ChromeMain+0x1f4 (/Users/happy/source/chromium/src/out/asan/libchrome_dll.dylib:arm64+0x9694) (BuildId: 4c4c44f355553144a13149ec4b9fe4b832000000200000000100000000000b00)
    #40 0x1001b8d14 in main+0x2a4 (/Users/happy/source/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/110.0.5461.0/Helpers/Chromium Helper (GPU).app/Contents/MacOS/Chromium Helper (GPU):arm64+0x100000d14) (BuildId: 4c4c445a55553144a1ea884311501a4732000000200000000100000000000b00)
    #41 0x1a817be4c  (<unknown module>)
    #42 0x832a7ffffffffffc  (<unknown module>)

0x603000139f00 is located 0 bytes inside of 24-byte region [0x603000139f00,0x603000139f18)
freed by thread T0 here:
    #0 0x100cf36a4 in __sanitizer_finish_switch_fiber+0x584 (/Users/happy/source/chromium/src/out/asan/libclang_rt.asan_osx_dynamic.dylib:arm64+0x5b6a4) (BuildId: 4c4c448555553144a19c875a4f1bd18a32000000200000000100000000000b00)
    #1 0x105a97e94 in gl::GLContext::~GLContext()+0x25c (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0x73e94) (BuildId: 4c4c447a55553144a100e847e3aed8b032000000200000000100000000000b00)
    #2 0x105b0983c in gl::GLContextEGL::~GLContextEGL()+0x40 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0xe583c) (BuildId: 4c4c447a55553144a100e847e3aed8b032000000200000000100000000000b00)
    #3 0x135d43594 in gpu::gles2::GLES2DecoderPassthroughImpl::Destroy(bool)+0x22ac (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x163594) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00)
    #4 0x13376fdc8 in gpu::CommandBufferStub::Destroy()+0xcd0 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x3dc8) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #5 0x13376eae8 in gpu::CommandBufferStub::~CommandBufferStub()+0x78 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x2ae8) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #6 0x133780ab0 in gpu::GLES2CommandBufferStub::~GLES2CommandBufferStub()+0x8 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x14ab0) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #7 0x13378e138 in gpu::GpuChannel::~GpuChannel()+0xec (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x22138) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #8 0x13378e8a8 in gpu::GpuChannel::~GpuChannel()+0x8 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x228a8) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #9 0x1337a2124 in gpu::GpuChannelManager::RemoveChannel(int)+0x190 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x36124) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #10 0x10227f204 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x304 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x1d7204) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #11 0x1022d2638 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x724 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x22a638) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #12 0x1022d1a2c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x150 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x229a2c) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #13 0x1023fb328 in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x353328) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #14 0x1023e2ad0 in base::mac::CallWithEHFrame(void () block_pointer)+0xc (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x33aad0) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #15 0x1023f93ec in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x13c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3513ec) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #16 0x1a8585a30 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x81a30) (BuildId: f4ff83fce62c30b4b3a9876c8a1fd59532000000200000000100000000000d00)
    #17 0xd66c0001a85859c4  (<unknown module>)
    #18 0x2a3e8001a8585734  (<unknown module>)
    #19 0x60410001a8584338  (<unknown module>)
    #20 0xb6610001a85838a0  (<unknown module>)
    #21 0x77730001a948be54  (<unknown module>)
    #22 0xc1040001023fd174  (<unknown module>)
    #23 0x1023f809c in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x270 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x35009c) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #24 0x1022d3fec in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x338 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x22bfec) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #25 0x1021fca80 in base::RunLoop::Run(base::Location const&)+0x3c0 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x154a80) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #26 0x10b5fba88 in content::GpuMain(content::MainFunctionParams)+0x880 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0xba88) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)
    #27 0x10e27dff0 in content::RunOtherNamedProcessTypeMain(std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x4cc (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x2c8dff0) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)
    #28 0x10e27f9b0 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x2c8f9b0) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)
    #29 0x10e27bb58 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0xf60 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x2c8bb58) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)

previously allocated by thread T0 here:
    #0 0x100cf3284 in __sanitizer_finish_switch_fiber+0x164 (/Users/happy/source/chromium/src/out/asan/libclang_rt.asan_osx_dynamic.dylib:arm64+0x5b284) (BuildId: 4c4c448555553144a19c875a4f1bd18a32000000200000000100000000000b00)
    #1 0x105a98828 in gl::GLContext::GetCurrentGL()+0x1d8 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0x74828) (BuildId: 4c4c447a55553144a100e847e3aed8b032000000200000000100000000000b00)
    #2 0x105a9ad08 in gl::GLContext::BindGLApi()+0x8 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0x76d08) (BuildId: 4c4c447a55553144a100e847e3aed8b032000000200000000100000000000b00)
    #3 0x105b08570 in gl::GLContextEGL::MakeCurrentImpl(gl::GLSurface*)+0x3bc (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0xe4570) (BuildId: 4c4c447a55553144a100e847e3aed8b032000000200000000100000000000b00)
    #4 0x105a98338 in gl::GLContext::MakeCurrent(gl::GLSurface*)+0x1b0 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0x74338) (BuildId: 4c4c447a55553144a100e847e3aed8b032000000200000000100000000000b00)
    #5 0x133782748 in gpu::GLES2CommandBufferStub::Initialize(gpu::CommandBufferStub*, gpu::mojom::CreateCommandBufferParams const&, base::UnsafeSharedMemoryRegion)+0x1c44 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x16748) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #6 0x13378a0e8 in gpu::GpuChannel::CreateCommandBuffer(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>)+0xf8c (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x1e0e8) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #7 0x133797100 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>&&, int&&, base::UnsafeSharedMemoryRegion&&, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>&&, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>&&, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>&&)+0x218 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x2b100) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #8 0x133796eb4 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)> >, void ()>::RunOnce(base::internal::BindStateBase*)+0x90 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x2aeb4) (BuildId: 4c4c442e55553144a1b7c989e136d24332000000200000000100000000000b00)
    #9 0x10227f204 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x304 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x1d7204) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #10 0x1022d2638 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x724 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x22a638) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #11 0x1022d1a2c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x150 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x229a2c) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #12 0x1023fb328 in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x353328) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #13 0x1023e2ad0 in base::mac::CallWithEHFrame(void () block_pointer)+0xc (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x33aad0) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #14 0x1023f93ec in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x13c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3513ec) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #15 0x1a8585a30 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x81a30) (BuildId: f4ff83fce62c30b4b3a9876c8a1fd59532000000200000000100000000000d00)
    #16 0xd66c0001a85859c4  (<unknown module>)
    #17 0x2a3e8001a8585734  (<unknown module>)
    #18 0x60410001a8584338  (<unknown module>)
    #19 0xb6610001a85838a0  (<unknown module>)
    #20 0x77730001a948be54  (<unknown module>)
    #21 0xc1040001023fd174  (<unknown module>)
    #22 0x1023f809c in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x270 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x35009c) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #23 0x1022d3fec in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x338 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x22bfec) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #24 0x1021fca80 in base::RunLoop::Run(base::Location const&)+0x3c0 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x154a80) (BuildId: 4c4c449b55553144a12ab56582a50d0c32000000200000000100000000000b00)
    #25 0x10b5fba88 in content::GpuMain(content::MainFunctionParams)+0x880 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0xba88) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)
    #26 0x10e27dff0 in content::RunOtherNamedProcessTypeMain(std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x4cc (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x2c8dff0) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)
    #27 0x10e27f9b0 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x2c8f9b0) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)
    #28 0x10e27bb58 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0xf60 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x2c8bb58) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)
    #29 0x10e27c254 in content::ContentMain(content::ContentMainParams)+0x134 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x2c8c254) (BuildId: 4c4c443355553144a1c54c53c4b853c132000000200000000100000000000b00)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/happy/source/chromium/src/out/asan/libgles2.dylib:arm64+0x315524) (BuildId: 4c4c449355553144a1c7871cc42adae032000000200000000100000000000b00) in gpu::gles2::TexturePassthrough::~TexturePassthrough()+0x18c
Shadow bytes around the buggy address:
  0x603000139c80: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd
  0x603000139d00: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa
  0x603000139d80: fd fd fd fd fa fa fd fd fd fd fa fa fd fd fd fd
  0x603000139e00: fa fa fd fd fd fd fa fa fd fd fd fa fa fa fd fd
  0x603000139e80: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa
=>0x603000139f00:[fd]fd fd fa fa fa fd fd fd fd fa fa fd fd fd fd
  0x603000139f80: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd
  0x60300013a000: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa
  0x60300013a080: fd fd fd fd fa fa fd fd fd fd fa fa fd fd fd fd
  0x60300013a100: fa fa fd fd fd fd fa fa fd fd fd fa fa fa fd fd
  0x60300013a180: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa
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
==79406==ABORTING

### ad...@google.com (2022-12-06)

Thanks for the report. Let us know when you've succeeded, _or failed_ to produce a POC and we'll handle this appropriately. Setting Needs-Feedback for now.

If you can't come up with a POC, please provide more details about how you reproduced this - e.g. this was a Mac M1, right? Did you reach it via web content or manipulating the UI, or something else?

[Monorail components: Internals>GPU]

### he...@gmail.com (2022-12-06)

Yeah this is repro on the Mac M1.

It is not related with the UI manipulation or the web contents. Instead, it requires some features to be enabled. 

I attached a script which contains the features which my fuzzer used. (need to change the path to chromium in the script). Just launch chromium with that features and wait for several seconds, the UAF occurs. It may not related with my fuzzer generated web contents, since without the generated web page, it still repros.

I failed to minimize the required features. However, from the RCA, I suspect that it may related with the EarlyEstablishGpuChannel.

### ad...@google.com (2022-12-07)

I reproduced this on an Intel Mac using asan-mac-release-1079353. It seemed to happen only when I attempted to close the browser window.

### he...@gmail.com (2022-12-07)

Hello, thanks for the repro. Yeah it may need to close the browser window in my local fuzzing environment.

I found another UAF while I'm reproducing this one and filled the https://crbug.com/chromium/1396304. That UAF seems happen during the initialization of the web page without closing the window.

### ad...@google.com (2022-12-07)

(the build in the previous comment is 110)
I can't reproduce this with M109

So, as a GPU process UaF this rates as Security_Severity-High.

However, I can't reproduce this without all those non-default flags so I'm rating it Security_Impact-None.

Geoff, please take a look.

### an...@chromium.org (2022-12-15)

security marshal note: pinged Geoff by email and asked him to add an update when he is back next Tuesday.

### ge...@chromium.org (2023-01-03)

Jonah, Chris: Can you take a look? Likely a regression from the refactoring done here.

### he...@gmail.com (2023-01-28)

friendly ping - seems that this is fixed by the recent CL since I couldn't reproduce this on the ToT chromium any more. 

Feel free to mark it as fixed.

### jo...@google.com (2023-01-30)

 adetaylor can you comment on which flags lead you to rate it Security_Impact-None? Are any of these flags going to be launched eventually?

### ke...@chromium.org (2023-03-01)

re https://crbug.com/chromium/1396212#c12: adetaylor@ marked it Security_Impact-None because the repro script includes a very long list of flags, and nobody has been able to repro without them. It doesn't repro on a default configuration, but someone would have to go through that list to determine which flags are actually necessary to reproduce.

Even if this no longer reproduces, it might still be worth trying to figure out what is happening to here to be confident the UAF is really fixed.

### he...@gmail.com (2023-03-02)

Hello, I found that I could trigger the similar UAF in the GPU. (the Asan stack might be slightly different)

After the investigation, the reproduction needs both Metal and RendererAllocatesImages features enabled.

That's said, we need the following command to repro:

./chrome --no-sandbox --enable-features=Metal,RendererAllocatesImages google.com

### he...@gmail.com (2023-03-02)

I suspect that there's a schedule bug in the SchedulerDfs of command_buffer service. Since the WebGL task is still scheduled even the bound GPU instance is crashed from the asan stack.

The Asan stack is a little bit flaky, I attached all of them which are found during reproduction and minimization on the ToT macOS Chromium.
 

### th...@chromium.org (2023-03-10)

Security marshal here. jonahr@, are you able to reproduce?

(Note that there is also a similar ticket https://crbug.com/1396304. If the root cause of the two issues is the same, that issue can be closed as a duplicate of this one.)

### he...@gmail.com (2023-03-22)

Note that I could still sometimes reproduce it on the 113.0.5664.0 chromium via loading the fuzzer generated web-page.

### he...@gmail.com (2023-03-22)

==14182==ERROR: AddressSanitizer: heap-use-after-free on address 0x6030001e0be0 at pc 0x0001395a466c bp 0x00016f23eaf0 sp 0x00016f23eae8
READ of size 8 at 0x6030001e0be0 thread T0
==14182==WARNING: invalid path to external symbolizer!
==14182==WARNING: Failed to use and restart external symbolizer!
    #0 0x1395a4668 in gpu::IOSurfaceImageBacking::ReleaseGLTexture(gpu::IOSurfaceBackingEGLState*, bool)+0x524 (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x32c668) (BuildId: 4c4c44f655553144a17d9992812855df32000000200000000100000000000b00)
    #1 0x1395a9f34 in gpu::IOSurfaceImageBacking::IOSurfaceBackingEGLStateBeingDestroyed(gpu::IOSurfaceBackingEGLState*, bool)+0xd4 (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x331f34) (BuildId: 4c4c44f655553144a17d9992812855df32000000200000000100000000000b00)
    #2 0x1395ae21c in void base::RefCounted<gpu::IOSurfaceBackingEGLState, base::DefaultRefCountedTraits<gpu::IOSurfaceBackingEGLState> >::DeleteInternal<gpu::IOSurfaceBackingEGLState>(gpu::IOSurfaceBackingEGLState const*)+0x140 (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x33621c) (BuildId: 4c4c44f655553144a17d9992812855df32000000200000000100000000000b00)
    #3 0x1395a3ba8 in gpu::IOSurfaceImageBacking::~IOSurfaceImageBacking()+0x1c4 (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x32bba8) (BuildId: 4c4c44f655553144a17d9992812855df32000000200000000100000000000b00)
    #4 0x1395a4084 in gpu::IOSurfaceImageBacking::~IOSurfaceImageBacking()+0x8 (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x32c084) (BuildId: 4c4c44f655553144a17d9992812855df32000000200000000100000000000b00)
    #5 0x1394e1978 in base::internal::flat_tree<std::Cr::unique_ptr<gpu::SharedImageBacking, std::Cr::default_delete<gpu::SharedImageBacking> >, base::identity, std::Cr::less<void>, std::Cr::vector<std::Cr::unique_ptr<gpu::SharedImageBacking, std::Cr::default_delete<gpu::SharedImageBacking> >, std::Cr::allocator<std::Cr::unique_ptr<gpu::SharedImageBacking, std::Cr::default_delete<gpu::SharedImageBacking> > > > >::erase(std::Cr::__wrap_iter<std::Cr::unique_ptr<gpu::SharedImageBacking, std::Cr::default_delete<gpu::SharedImageBacking> >*>)+0x23c (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x269978) (BuildId: 4c4c44f655553144a17d9992812855df32000000200000000100000000000b00)
    #6 0x1394e163c in gpu::SharedImageManager::OnRepresentationDestroyed(gpu::Mailbox const&, gpu::SharedImageRepresentation*)+0x398 (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x26963c) (BuildId: 4c4c44f655553144a17d9992812855df32000000200000000100000000000b00)
    #7 0x1394e42bc in gpu::SharedImageRepresentation::~SharedImageRepresentation()+0x1c8 (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x26c2bc) (BuildId: 4c4c44f655553144a17d9992812855df32000000200000000100000000000b00)
    #8 0x1394e9f30 in gpu::SharedImageRepresentationFactoryRef::~SharedImageRepresentationFactoryRef()+0xac (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x271f30) (BuildId: 4c4c44f655553144a17d9992812855df32000000200000000100000000000b00)
    #9 0x1394d98d8 in gpu::SharedImageFactory::DestroyAllSharedImages(bool)+0x144 (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x2618d8) (BuildId: 4c4c44f655553144a17d9992812855df32000000200000000100000000000b00)
    #10 0x1360720a8 in gpu::SharedImageStub::~SharedImageStub()+0x108 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x6a0a8) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #11 0x136072570 in gpu::SharedImageStub::~SharedImageStub()+0x8 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x6a570) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #12 0x13602ee34 in gpu::GpuChannel::~GpuChannel()+0x2f4 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x26e34) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #13 0x13602f3f0 in gpu::GpuChannel::~GpuChannel()+0x8 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x273f0) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #14 0x136046690 in gpu::GpuChannelManager::RemoveChannel(int)+0x190 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x3e690) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #15 0x102e35600 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x338 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x1c5600) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #16 0x102e92114 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7dc (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x222114) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #17 0x102e91558 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x130 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x221558) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #18 0x10302ad88 in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3bad88) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #19 0x10301b584 in base::mac::CallWithEHFrame(void () block_pointer)+0xc (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3ab584) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #20 0x103028e04 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x13c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3b8e04) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #21 0x190f6cf90 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x84f90) (BuildId: fc3c193d0cdb35699f0ebd2507ca1dbb32000000200000000100000000060c00)
    #22 0x843d800190f6cedc  (<unknown module>)
    #23 0xa17a800190f6cbdc  (<unknown module>)
    #24 0x5534000190f6b55c  (<unknown module>)
    #25 0xc513000190f6aa80  (<unknown module>)
    #26 0xdd64800191e500bc  (<unknown module>)
    #27 0x2b3700010302c760  (<unknown module>)
    #28 0x103027c58 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x23c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3b7c58) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #29 0x102e93c9c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x338 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x223c9c) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #30 0x102da0ba0 in base::RunLoop::Run(base::Location const&)+0x42c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x130ba0) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #31 0x10c96903c in content::GpuMain(content::MainFunctionParams)+0x934 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0xd03c) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)
    #32 0x10fae9214 in content::RunOtherNamedProcessTypeMain(std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x4b8 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x318d214) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)
    #33 0x10faeac44 in content::ContentMainRunnerImpl::Run()+0x564 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x318ec44) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)
    #34 0x10fae6d58 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0xc74 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x318ad58) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)
    #35 0x10fae72b4 in content::ContentMain(content::ContentMainParams)+0x144 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x318b2b4) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)
    #36 0x1143e6468 in ChromeMain+0x410 (/Users/happy/source/chromium/src/out/asan/libchrome_dll.dylib:arm64+0xa468) (BuildId: 4c4c447455553144a1167dbdf083289932000000200000000100000000000b00)
    #37 0x100bbcd44 in main+0x2b4 (/Users/happy/source/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/113.0.5664.0/Helpers/Chromium Helper (GPU).app/Contents/MacOS/Chromium Helper (GPU):arm64+0x100000d44) (BuildId: 4c4c445355553144a11000968585514032000000200000000100000000000b00)
    #38 0x100d45088  (/usr/lib/dyld:arm64+0x5088) (BuildId: d7845cbce8ac3acb9f6c719e7f7c217632000000200000000100000000060c00)
    #39 0xdf67fffffffffffc  (<unknown module>)

0x6030001e0be0 is located 0 bytes inside of 24-byte region [0x6030001e0be0,0x6030001e0bf8)
freed by thread T0 here:
    #0 0x10188252c in __sanitizer_finish_switch_fiber+0xbb8 (/Users/happy/source/chromium/src/out/asan/libclang_rt.asan_osx_dynamic.dylib:arm64+0x5e52c) (BuildId: 4c4c447955553144a111e8a54c2ba45732000000200000000100000000000b00)
    #1 0x1055ed86c in gl::GLContext::~GLContext()+0x314 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0x7586c) (BuildId: 4c4c445b55553144a13aff8827b63abe32000000200000000100000000000b00)
    #2 0x105662204 in gl::GLContextEGL::~GLContextEGL()+0x40 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0xea204) (BuildId: 4c4c445b55553144a13aff8827b63abe32000000200000000100000000000b00)
    #3 0x13932576c in gpu::gles2::GLES2DecoderPassthroughImpl::Destroy(bool)+0x282c (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0xad76c) (BuildId: 4c4c44f655553144a17d9992812855df32000000200000000100000000000b00)
    #4 0x13600c0c0 in gpu::CommandBufferStub::Destroy()+0xd1c (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x40c0) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #5 0x13600ad10 in gpu::CommandBufferStub::~CommandBufferStub()+0x78 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x2d10) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #6 0x13601fe80 in gpu::GLES2CommandBufferStub::~GLES2CommandBufferStub()+0x8 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x17e80) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #7 0x13602ec2c in gpu::GpuChannel::~GpuChannel()+0xec (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x26c2c) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #8 0x13602f3f0 in gpu::GpuChannel::~GpuChannel()+0x8 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x273f0) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #9 0x136046690 in gpu::GpuChannelManager::RemoveChannel(int)+0x190 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x3e690) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #10 0x102e35600 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x338 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x1c5600) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #11 0x102e92114 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7dc (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x222114) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #12 0x102e91558 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x130 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x221558) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #13 0x10302ad88 in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3bad88) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #14 0x10301b584 in base::mac::CallWithEHFrame(void () block_pointer)+0xc (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3ab584) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #15 0x103028e04 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x13c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3b8e04) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #16 0x190f6cf90 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x84f90) (BuildId: fc3c193d0cdb35699f0ebd2507ca1dbb32000000200000000100000000060c00)
    #17 0x843d800190f6cedc  (<unknown module>)
    #18 0xa17a800190f6cbdc  (<unknown module>)
    #19 0x5534000190f6b55c  (<unknown module>)
    #20 0xc513000190f6aa80  (<unknown module>)
    #21 0xdd64800191e500bc  (<unknown module>)
    #22 0x2b3700010302c760  (<unknown module>)
    #23 0x103027c58 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x23c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3b7c58) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #24 0x102e93c9c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x338 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x223c9c) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #25 0x102da0ba0 in base::RunLoop::Run(base::Location const&)+0x42c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x130ba0) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #26 0x10c96903c in content::GpuMain(content::MainFunctionParams)+0x934 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0xd03c) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)
    #27 0x10fae9214 in content::RunOtherNamedProcessTypeMain(std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x4b8 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x318d214) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)
    #28 0x10faeac44 in content::ContentMainRunnerImpl::Run()+0x564 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x318ec44) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)
    #29 0x10fae6d58 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0xc74 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x318ad58) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)

previously allocated by thread T0 here:
    #0 0x10188210c in __sanitizer_finish_switch_fiber+0x798 (/Users/happy/source/chromium/src/out/asan/libclang_rt.asan_osx_dynamic.dylib:arm64+0x5e10c) (BuildId: 4c4c447955553144a111e8a54c2ba45732000000200000000100000000000b00)
    #1 0x1055ee2a8 in gl::GLContext::GetCurrentGL()+0x1d8 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0x762a8) (BuildId: 4c4c445b55553144a13aff8827b63abe32000000200000000100000000000b00)
    #2 0x1055f102c in gl::GLContext::BindGLApi()+0x8 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0x7902c) (BuildId: 4c4c445b55553144a13aff8827b63abe32000000200000000100000000000b00)
    #3 0x1056610d8 in gl::GLContextEGL::MakeCurrentImpl(gl::GLSurface*)+0x3b4 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0xe90d8) (BuildId: 4c4c445b55553144a13aff8827b63abe32000000200000000100000000000b00)
    #4 0x1055edda0 in gl::GLContext::MakeCurrent(gl::GLSurface*)+0x1b0 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0x75da0) (BuildId: 4c4c445b55553144a13aff8827b63abe32000000200000000100000000000b00)
    #5 0x136022448 in gpu::GLES2CommandBufferStub::Initialize(gpu::CommandBufferStub*, gpu::mojom::CreateCommandBufferParams const&, base::UnsafeSharedMemoryRegion)+0x2574 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x1a448) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #6 0x13602ab88 in gpu::GpuChannel::CreateCommandBuffer(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>)+0xf60 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x22b88) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #7 0x136039a58 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>&&, int&&, base::UnsafeSharedMemoryRegion&&, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>&&, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>&&, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>&&)+0x250 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x31a58) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #8 0x1360397d4 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)> >, void ()>::RunOnce(base::internal::BindStateBase*)+0x90 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x317d4) (BuildId: 4c4c443855553144a18de2f622b92a7c32000000200000000100000000000b00)
    #9 0x102e35600 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x338 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x1c5600) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #10 0x102e92114 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7dc (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x222114) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #11 0x102e91558 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x130 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x221558) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #12 0x10302ad88 in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3bad88) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #13 0x10301b584 in base::mac::CallWithEHFrame(void () block_pointer)+0xc (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3ab584) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #14 0x103028e04 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x13c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3b8e04) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #15 0x190f6cf90 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x84f90) (BuildId: fc3c193d0cdb35699f0ebd2507ca1dbb32000000200000000100000000060c00)
    #16 0x843d800190f6cedc  (<unknown module>)
    #17 0xa17a800190f6cbdc  (<unknown module>)
    #18 0x5534000190f6b55c  (<unknown module>)
    #19 0xc513000190f6aa80  (<unknown module>)
    #20 0xdd64800191e500bc  (<unknown module>)
    #21 0x2b3700010302c760  (<unknown module>)
    #22 0x103027c58 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x23c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3b7c58) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #23 0x102e93c9c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x338 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x223c9c) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #24 0x102da0ba0 in base::RunLoop::Run(base::Location const&)+0x42c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x130ba0) (BuildId: 4c4c443e55553144a19e430939ebcbce32000000200000000100000000000b00)
    #25 0x10c96903c in content::GpuMain(content::MainFunctionParams)+0x934 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0xd03c) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)
    #26 0x10fae9214 in content::RunOtherNamedProcessTypeMain(std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x4b8 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x318d214) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)
    #27 0x10faeac44 in content::ContentMainRunnerImpl::Run()+0x564 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x318ec44) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)
    #28 0x10fae6d58 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0xc74 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x318ad58) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)
    #29 0x10fae72b4 in content::ContentMain(content::ContentMainParams)+0x144 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x318b2b4) (BuildId: 4c4c44f155553144a1a33f843e3f885932000000200000000100000000000b00)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x32c668) (BuildId: 4c4c44f655553144a17d9992812855df32000000200000000100000000000b00) in gpu::IOSurfaceImageBacking::ReleaseGLTexture(gpu::IOSurfaceBackingEGLState*, bool)+0x524
Shadow bytes around the buggy address:
  0x6030001e0900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6030001e0980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6030001e0a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6030001e0a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6030001e0b00: fa fa fa fa fa fa fa fa fa fa fd fd fd fd fa fa
=>0x6030001e0b80: fd fd fd fd fa fa fd fd fd fd fa fa[fd]fd fd fa
  0x6030001e0c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6030001e0c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6030001e0d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6030001e0d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6030001e0e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==14182==ADDITIONAL INFO

==14182==Note: Please include this section with the ASan report.
Task trace:
    #0 0x1051e8e74 in IPC::ChannelProxy::Context::OnChannelError()+0x1b4 (/Users/happy/source/chromium/src/out/asan/libipc.dylib:arm64+0x20e74) (BuildId: 4c4c44a955553144a1d6319dd3c2573532000000200000000100000000000b00)


==14182==END OF ADDITIONAL INFO
==14182==ABORTING

### pa...@chromium.org (2023-05-11)

[secondary security shepherd] ping @jonahr@google.com, any updates on this?

### ts...@chromium.org (2023-07-11)

Re-assigning,. geofflang, is there someone else who can take a look at this report?


### ge...@chromium.org (2023-07-31)

Vasiliy: Do you have some time to look at this? Looks like a SharedImage being destroyed while Chrome thinks there is a context current but it's already been deleted. Send it back to me if you don't have time.

### va...@chromium.org (2023-07-31)

I'm a bit confused about this one. There is no Metal feature anymore (removed in 114 and it was never shipped) and looking at code, GLContext is question is now stored in IOSurfaceBackingEGLState.

Looking at stack traces, it looks like we access CurrentGL that triggers asan. It's stored in TLS and destruction of texture might use that TLS to get pointer to glDeleteTextures. But:
* GLContext is supposed to clear TLS if it's destroyed [1]
* Context supposed to be current is set here [2] and the ref to that context should be alive via SharedContextState (we have scoped_refptr to SharedContextState, SharedContextState has scoped_refptr to GLContext)

It is possible that we failed to make context current.  This should be plumbed through [3][4], but even if that plumbing fails, we shouldn't have dead context in a TLS.

More, IOSurfaceBackingEGLState will make context current again here [4]. GLContext there is refcounted, so the object should be alive. We don't check for context lost there and we should, but it should get us to UAF.

I don't have mac to repro, is it reproducible on newer chrome versions than 113?

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:ui/gl/gl_context.cc;drc=5cb22f99522203e552ff9de07dbc895f26a96dd4;l=82
[2] https://source.chromium.org/chromium/chromium/src/+/main:gpu/ipc/service/shared_image_stub.cc;l=57-58


[3] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:gpu/command_buffer/service/shared_image/shared_image_backing.cc;drc=5cb22f99522203e552ff9de07dbc895f26a96dd4;l=96
[4] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:gpu/command_buffer/service/shared_image/iosurface_image_backing.mm;drc=5cb22f99522203e552ff9de07dbc895f26a96dd4;l=177
[5] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:gpu/command_buffer/service/shared_image/iosurface_image_backing.mm;drc=5cb22f99522203e552ff9de07dbc895f26a96dd4;l=156

### ge...@chromium.org (2023-07-31)

Yea, I think there is a good chance this no longer repros or hit an edge case due to the combination of flags used. I'll take it back and try to repro when I have a chance.

### he...@gmail.com (2023-09-15)

Hello, seems that this issue is fixed by the commit https://chromium-review.googlesource.com/c/chromium/src/+/4847892

Feel free to mark it as fixed. Thank you very much.

### bo...@google.com (2023-11-06)

Thanks @hedonistsmith. 

Even with the tighter repro steps in https://crbug.com/chromium/1396212#c14 it's unclear to me whether the root cause was identified, meaning it's not obvious to me whether the subsequent changes addressed the issue or made it more difficult to reach. 

@geofflang, are you able to confirm whether crrev.com/c/4847892 fixes this issue to your satisfaction? 

### el...@chromium.org (2023-11-24)

Secondary shepherd here! Hi geofflang@ - is this fixed enough for you?

### ge...@chromium.org (2023-12-04)

Going to mark this as fixed. I have an item on my TODO list to try to repro. If it does (unlikely) I will re-open.

### ch...@chromium.org (2023-12-04)

[Comment Deleted]

### [Deleted User] (2023-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-04)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-07)

Congratulations! The Chrome VRP Panel has decided to award you $5,000 for this report. The reward amount was decided based report quality in that it didn't efficient provide the relevant information for us to reliably reproduce or work toward resolution of this issue. We do appreciate your efforts here and reporting this issue to us, but in the end it was the efforts in another issue that resulted in the potential resolution of this issue. 

### he...@gmail.com (2023-12-08)

Thank you very much :)

### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### is...@google.com (2023-12-08)

This issue was migrated from crbug.com/chromium/1396212?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062056)*
