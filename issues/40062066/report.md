# UAF in GpuChannel

| Field | Value |
|-------|-------|
| **Issue ID** | [40062066](https://issues.chromium.org/issues/40062066) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU |
| **Platforms** | Mac |
| **Reporter** | he...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2022-12-06 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

Will attach details soon

**Problem Description:**  

UAF in GPU

**Additional Comments:**

\*\*Chrome version: \*\* 110.0.5458.0 \*\*Channel: \*\* Canary

**OS:** Mac OS

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 25.6 KB)
- [repro.sh](attachments/repro.sh) (text/plain, 33.1 KB)

## Timeline

### he...@gmail.com (2022-12-06)

During the reproduction of the previous report https://crbug.com/chromium/1396212, I find another UAF. Due to the stack trace is quite different, I choose to report it separately.

Tested on the 110.0.5461.0 MacOS chromium with M1 chip.

I attached a script which contains the features which my fuzzer used. (need to change the path to chromium in the script). Just launch chromium with that features and wait for several seconds, the UAF occurs. It may not related with my fuzzer generated web contents, since without the generated web page, it still repros.

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-07)

Unlike https://crbug.com/chromium/1396212, I can't reproduce this on my Intel Mac. But just like that previous issue, the GPU process has odd behavior with all of those extra flags (not least, nothing actually gets displayed in the window) so I am confident that this is a side-effect of one of those flags and I am therefore marking this Security_Impact-None. As a GPU process UaF this would be High severity.

Geoff, you might want to just mark this as a duplicate of the other issue if you think they are symptoms of the same root cause. We ask our VRP reporters to file bugs separately just in case they turn out to be different root causes (it's easier to merge bugs than split them apart).

[Monorail components: Internals>GPU]

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-12-15)

security marshal note: pinged Geoff by email and asked him to add an update when he is back next Tuesday.

### ge...@chromium.org (2023-01-03)

Jonah, can you take a look at this too? May be M1 specific.

### jo...@google.com (2023-01-30)

Hi reporter, can you still reproduce this issue? Or has it been fixed like https://crbug.com/chromium/1396212?

### he...@gmail.com (2023-01-31)

Like the previous issue, I couldn't reproduce this on the ToT chromium any more. Feel free to mark it as fixed.

### th...@chromium.org (2023-03-10)

Security marshal here. In https://bugs.chromium.org/p/chromium/issues/detail?id=1396212#c15 (in the other issue), I'm seeing the stack trace in the description of this issue match the asan1.txt stack trace. So, I don't think this issue is fixed, since that comment is saying this was reproducible on March 2nd.

jonahr@, if it's found that the root cause for this issue is the same as the other one, this can be closed as a duplicate of the other.

### pa...@chromium.org (2023-05-11)

[secondary security shepherd] Hello @jonahr@google.com, just a friendly ping for https://crbug.com/chromium/1396304#c9.

### he...@gmail.com (2023-05-31)

Hello, I could still reproduce this on the ToT chromium in my fuzzing machine. I'm not sure whether this issue could be updated.

==2101==WARNING: Failed to use and restart external symbolizer!
    #0 0x13ec15088 in gpu::raster::RasterDecoderImpl::Initialize(scoped_refptr<gl::GLSurface> const&, scoped_refptr<gl::GLContext> const&, bool, gpu::gles2::DisallowedFeatures const&, gpu::ContextCreationAttribs const&)+0x750 (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x1ed088) (BuildId: 4c4c44ca55553144a12e2065b122d44332000000200000000100000000000b00)
    #1 0x13b4d9738 in gpu::RasterCommandBufferStub::Initialize(gpu::CommandBufferStub*, gpu::mojom::CreateCommandBufferParams const&, base::UnsafeSharedMemoryRegion)+0x8fc (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x61738) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #2 0x13b49a074 in gpu::GpuChannel::CreateCommandBuffer(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>)+0x1148 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x22074) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #3 0x13b4a92a0 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>&&, int&&, base::UnsafeSharedMemoryRegion&&, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>&&, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>&&, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>&&)+0x25c (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x312a0) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #4 0x13b4a9010 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x90 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x31010) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #5 0x10688425c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x1bc25c) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #6 0x1068dd31c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7a8 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x21531c) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #7 0x1068dc794 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x130 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x214794) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #8 0x106a6e908 in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3a6908) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #9 0x106a5f8f0 in base::mac::CallWithEHFrame(void () block_pointer)+0xc (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3978f0) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #10 0x106a6c984 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x13c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3a4984) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #11 0x182cda638 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f638) (BuildId: 203e44018c2e3157a24b92f52551d43e32000000200000000100000000040d00)
    #12 0x8478800182cda5cc  (<unknown module>)
    #13 0x4128800182cda33c  (<unknown module>)
    #14 0xf045000182cd8f44  (<unknown module>)
    #15 0x557b000182cd84b4  (<unknown module>)
    #16 0xc47a000183c51fc8  (<unknown module>)
    #17 0x7f4f000106a702b0  (<unknown module>)
    #18 0x106a6b7d8 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x23c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3a37d8) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #19 0x1068dee98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x354 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x216e98) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #20 0x1067f81e0 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x1301e0) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #21 0x110749bbc in content::GpuMain(content::MainFunctionParams)+0x918 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0xdbbc) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)
    #22 0x11396f0b4 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x3cc (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x32330b4) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)
    #23 0x113970cd0 in content::ContentMainRunnerImpl::Run()+0x560 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x3234cd0) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)
    #24 0x11396cc80 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x9ec (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x3230c80) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)
    #25 0x11396d19c in content::ContentMain(content::ContentMainParams)+0x144 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x323119c) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)
    #26 0x1189e670c in ChromeMain+0x424 (/Users/happy/source/chromium/src/out/asan/libchrome_dll.dylib:arm64+0xa70c) (BuildId: 4c4c447555553144a12d8409386a838832000000200000000100000000000b00)
    #27 0x10478cd34 in main+0x2a4 (/Users/happy/source/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/116.0.5800.0/Helpers/Chromium Helper (GPU).app/Contents/MacOS/Chromium Helper (GPU):arm64+0x100000d34) (BuildId: 4c4c443b55553144a1630807f2d6a6b732000000200000000100000000000b00)
    #28 0x1828a3f24  (<unknown module>)
    #29 0x80bfffffffffffc  (<unknown module>)

0x60300027a9f0 is located 0 bytes inside of 24-byte region [0x60300027a9f0,0x60300027aa08)
freed by thread T0 here:
    #0 0x1052bea2c in __sanitizer_finish_switch_fiber+0xb68 (/Users/happy/source/chromium/src/out/asan/libclang_rt.asan_osx_dynamic.dylib:arm64+0x5ea2c) (BuildId: 4c4c443e55553144a1400716444dd55532000000200000000100000000000b00)
    #1 0x109d36228 in gl::GLContext::~GLContext()+0x314 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0x76228) (BuildId: 4c4c44ab55553144a106a0e0f2e9039d32000000200000000100000000000b00)
    #2 0x109da8808 in gl::GLContextEGL::~GLContextEGL()+0x40 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0xe8808) (BuildId: 4c4c44ab55553144a106a0e0f2e9039d32000000200000000100000000000b00)
    #3 0x13ead6a64 in gpu::gles2::GLES2DecoderPassthroughImpl::Destroy(bool)+0x249c (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0xaea64) (BuildId: 4c4c44ca55553144a12e2065b122d44332000000200000000100000000000b00)
    #4 0x13b47bef0 in gpu::CommandBufferStub::Destroy()+0xd1c (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x3ef0) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #5 0x13b47ab40 in gpu::CommandBufferStub::~CommandBufferStub()+0x78 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x2b40) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #6 0x13b48eb60 in gpu::GLES2CommandBufferStub::~GLES2CommandBufferStub()+0x8 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x16b60) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #7 0x13b49ba80 in gpu::GpuChannel::DestroyCommandBuffer(int)+0x370 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x23a80) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #8 0x13b4a9848 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(int), base::WeakPtr<gpu::GpuChannel>, int>, void ()>::RunOnce(base::internal::BindStateBase*)+0x17c (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x31848) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #9 0x106955234 in base::(anonymous namespace)::PostTaskAndReplyRelay::RunTaskAndPostReply(base::(anonymous namespace)::PostTaskAndReplyRelay)+0x12c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x28d234) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #10 0x106955c20 in base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase*)+0x188 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x28dc20) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #11 0x10688425c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x1bc25c) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #12 0x1068dd31c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7a8 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x21531c) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #13 0x1068dc794 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x130 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x214794) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #14 0x106a6e908 in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3a6908) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #15 0x106a5f8f0 in base::mac::CallWithEHFrame(void () block_pointer)+0xc (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3978f0) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #16 0x106a6c984 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x13c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3a4984) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #17 0x182cda638 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f638) (BuildId: 203e44018c2e3157a24b92f52551d43e32000000200000000100000000040d00)
    #18 0x8478800182cda5cc  (<unknown module>)
    #19 0x4128800182cda33c  (<unknown module>)
    #20 0xf045000182cd8f44  (<unknown module>)
    #21 0x557b000182cd84b4  (<unknown module>)
    #22 0xc47a000183c51fc8  (<unknown module>)
    #23 0x7f4f000106a702b0  (<unknown module>)
    #24 0x106a6b7d8 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x23c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3a37d8) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #25 0x1068dee98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x354 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x216e98) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #26 0x1067f81e0 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x1301e0) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #27 0x110749bbc in content::GpuMain(content::MainFunctionParams)+0x918 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0xdbbc) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)
    #28 0x11396f0b4 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x3cc (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x32330b4) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)
    #29 0x113970cd0 in content::ContentMainRunnerImpl::Run()+0x560 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x3234cd0) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)

previously allocated by thread T0 here:
    #0 0x1052be60c in __sanitizer_finish_switch_fiber+0x748 (/Users/happy/source/chromium/src/out/asan/libclang_rt.asan_osx_dynamic.dylib:arm64+0x5e60c) (BuildId: 4c4c443e55553144a1400716444dd55532000000200000000100000000000b00)
    #1 0x109d36c64 in gl::GLContext::GetCurrentGL()+0x1d8 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0x76c64) (BuildId: 4c4c44ab55553144a106a0e0f2e9039d32000000200000000100000000000b00)
    #2 0x109d39a7c in gl::GLContext::BindGLApi()+0x8 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0x79a7c) (BuildId: 4c4c44ab55553144a106a0e0f2e9039d32000000200000000100000000000b00)
    #3 0x109da7608 in gl::GLContextEGL::MakeCurrentImpl(gl::GLSurface*)+0x3b4 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0xe7608) (BuildId: 4c4c44ab55553144a106a0e0f2e9039d32000000200000000100000000000b00)
    #4 0x109d3675c in gl::GLContext::MakeCurrent(gl::GLSurface*)+0x1b0 (/Users/happy/source/chromium/src/out/asan/libgl_wrapper.dylib:arm64+0x7675c) (BuildId: 4c4c44ab55553144a106a0e0f2e9039d32000000200000000100000000000b00)
    #5 0x13b4910b4 in gpu::GLES2CommandBufferStub::Initialize(gpu::CommandBufferStub*, gpu::mojom::CreateCommandBufferParams const&, base::UnsafeSharedMemoryRegion)+0x2500 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x190b4) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #6 0x13b49a074 in gpu::GpuChannel::CreateCommandBuffer(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>)+0x1148 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x22074) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #7 0x13b4a92a0 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>&&, int&&, base::UnsafeSharedMemoryRegion&&, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>&&, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>&&, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>&&)+0x25c (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x312a0) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #8 0x13b4a9010 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x90 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x31010) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)
    #9 0x10688425c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x1bc25c) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #10 0x1068dd31c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7a8 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x21531c) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #11 0x1068dc794 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x130 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x214794) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #12 0x106a6e908 in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3a6908) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #13 0x106a5f8f0 in base::mac::CallWithEHFrame(void () block_pointer)+0xc (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3978f0) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #14 0x106a6c984 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x13c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3a4984) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #15 0x182cda638 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f638) (BuildId: 203e44018c2e3157a24b92f52551d43e32000000200000000100000000040d00)
    #16 0x8478800182cda5cc  (<unknown module>)
    #17 0x4128800182cda33c  (<unknown module>)
    #18 0xf045000182cd8f44  (<unknown module>)
    #19 0x557b000182cd84b4  (<unknown module>)
    #20 0xc47a000183c51fc8  (<unknown module>)
    #21 0x7f4f000106a702b0  (<unknown module>)
    #22 0x106a6b7d8 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x23c (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x3a37d8) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #23 0x1068dee98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x354 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x216e98) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #24 0x1067f81e0 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/happy/source/chromium/src/out/asan/libbase.dylib:arm64+0x1301e0) (BuildId: 4c4c44f355553144a12b11cf8c88210d32000000200000000100000000000b00)
    #25 0x110749bbc in content::GpuMain(content::MainFunctionParams)+0x918 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0xdbbc) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)
    #26 0x11396f0b4 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x3cc (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x32330b4) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)
    #27 0x113970cd0 in content::ContentMainRunnerImpl::Run()+0x560 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x3234cd0) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)
    #28 0x11396cc80 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x9ec (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x3230c80) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)
    #29 0x11396d19c in content::ContentMain(content::ContentMainParams)+0x144 (/Users/happy/source/chromium/src/out/asan/libcontent.dylib:arm64+0x323119c) (BuildId: 4c4c44a355553144a14d07686318472e32000000200000000100000000000b00)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/happy/source/chromium/src/out/asan/libgpu_gles2.dylib:arm64+0x1ed088) (BuildId: 4c4c44ca55553144a12e2065b122d44332000000200000000100000000000b00) in gpu::raster::RasterDecoderImpl::Initialize(scoped_refptr<gl::GLSurface> const&, scoped_refptr<gl::GLContext> const&, bool, gpu::gles2::DisallowedFeatures const&, gpu::ContextCreationAttribs const&)+0x750
Shadow bytes around the buggy address:
  0x60300027a700: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa
  0x60300027a780: fd fd fd fd fa fa fd fd fd fa fa fa fd fd fd fd
  0x60300027a800: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd
  0x60300027a880: fd fa fa fa fd fd fd fa fa fa fd fd fd fd fa fa
  0x60300027a900: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fd
=>0x60300027a980: fa fa fd fd fd fa fa fa fd fd fd fd fa fa[fd]fd
  0x60300027aa00: fd fa fa fa fd fd fd fd fa fa fd fd fd fd fa fa
  0x60300027aa80: fd fd fd fd fa fa fd fd fd fa fa fa fd fd fd fd
  0x60300027ab00: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd
  0x60300027ab80: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa
  0x60300027ac00: fd fd fd fd fa fa fd fd fd fd fa fa fd fd fd fd
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

==2101==ADDITIONAL INFO

==2101==Note: Please include this section with the ASan report.
Task trace:
    #0 0x13b4989b4 in gpu::GpuChannelMessageFilter::CreateCommandBuffer(mojo::StructPtr<gpu::mojom::CreateCommandBufferParams>, int, base::UnsafeSharedMemoryRegion, mojo::PendingAssociatedReceiver<gpu::mojom::CommandBuffer>, mojo::PendingAssociatedRemote<gpu::mojom::CommandBufferClient>, base::OnceCallback<void (gpu::ContextResult, gpu::Capabilities const&)>)+0x1b4 (/Users/happy/source/chromium/src/out/asan/libgpu_ipc_service.dylib:arm64+0x209b4) (BuildId: 4c4c44aa55553144a1f5cfb74cf63d9e32000000200000000100000000000b00)


==2101==END OF ADDITIONAL INFO

### he...@gmail.com (2023-05-31)

Additional note: on the macOS Chrome 116.0.5800.0

### aj...@google.com (2023-06-08)

[Empty comment from Monorail migration]

### he...@gmail.com (2023-06-25)

friendly ping - 

### ts...@chromium.org (2023-07-11)

Re-assigning - geoff, is there someone who might have cycles to look in to this again bug? thanks!

### he...@gmail.com (2023-07-13)

After digging it deeper, I find that the root cause of this UAF is clear:

## RCA

When a GpuChannel's CommandBuffer is requested to be created via mojo ipc |CreateCommandBuffer| [1], |GpuChannelMessageFilter::CreateCommandBuffer| will post the `gpu::GpuChannel::CreateCommandBuffer` [2] to the main_task_runner. The |main_task_runner| is originated from the `task_runner_` of `GpuChannelManager` [3]. That `task_runner_` is actually on the GpuService thread [4].

In the `GpuChannel::CreateCommandBuffer` function, there's no thread-lock protection, neither the thread checker. It will initialize three types of stub (i.e., `CommandBufferStub`) [5], and if the context enables the raster command buffer, the `stub` becomes the `RasterCommandBufferStub` and then being initialized. However, since `CreateCommandBuffer` is not thread-safe, there exists TOCTOU bug after the stub created [6] and before it is initialized [5]. If the `GpuChannel` is freed/destroyed at that time, the stub will be freed [7]. Then when we initialize the freed stub, UAF happens in `RasterCommandBufferStub::Initialize` (if stub is `RasterCommandBufferStub` type. it could be other type and the UAF places vaires as well).

The key point here may lies in the concurrency execution of `CreateCommandBuffer` and `~GpuChannel`. We note that the normal |DestroyCommandBuffer| mojo call properly post the `DestroyCommandBuffer` to the same GpuService thread, which won't cause the UAF. However, `GpuChannelManager::RemoveChannel` may not runs on the proper thread (i.e., the gpu service thread), and could free the GpuChannel in [9]. There are many ways to trigger the `RemoveChannel` on the different thread, take two methods for example:

1. Through the `EstablishGpuChannel` mojo call [10], with the exising `client_id` of the GpuChannel [11].
2. The connected renderer could force crash itself, or DoS the renderer (which could be easily achived by the web page) to disconnect the IPC channel. This would trigger the `OnChannelError`, e.g., `BrowserChildProcessHostImpl::OnChannelError()`[12]/`ChildProcessHostImpl::OnDisconnectedFromChildProcess()`[13], etc.


[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:gpu/ipc/common/gpu_channel.mojom;l=150-155;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188

  // CommandBufferStub is created.  If `params` provides a non-null
  // SurfaceHandle, |size| is ignored and it will render directly to the native
  // surface (only the browser process is allowed to create those). Otherwise it
  // will create an offscreen backbuffer of dimensions `size`.
  [Sync, NoInterrupt] CreateCommandBuffer(
      CreateCommandBufferParams params, int32 routing_id,
      mojo_base.mojom.UnsafeSharedMemoryRegion shared_state,
      pending_associated_receiver<CommandBuffer> receiver,
      pending_associated_remote<CommandBufferClient> client)
      => (ContextResult result, Capabilities capabilties);

[2] https://source.chromium.org/chromium/chromium/src/+/main:gpu/ipc/service/gpu_channel.cc;l=406-413;drc=26b5249d4959541063b6bb2d7c071d4f858be9b3

  main_task_runner_->PostTask(
      FROM_HERE,
      base::BindOnce(
          &gpu::GpuChannel::CreateCommandBuffer, gpu_channel_->AsWeakPtr(), // [2]
          std::move(params), routing_id, std::move(shared_state),
          std::move(receiver), std::move(client),
          base::BindPostTask(base::SingleThreadTaskRunner::GetCurrentDefault(),
                             std::move(callback))));


[3] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:gpu/ipc/service/gpu_channel_manager.cc;l=492;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188

  std::unique_ptr<GpuChannel> gpu_channel = GpuChannel::Create(
      this, channel_token, scheduler_, sync_point_manager_, share_group_,
      task_runner_, io_task_runner_, client_id, client_tracing_id, is_gpu_host, // [3]
      image_decode_accelerator_worker_);

[4] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/viz/service/gl/gpu_service_impl.cc;l=327;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188

    main_runner_(base::SingleThreadTaskRunner::GetCurrentDefault()),

[5][6] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:gpu/ipc/service/gpu_channel.cc;l=910-935;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188

  std::unique_ptr<CommandBufferStub> stub;
  if (init_params->attribs.context_type == CONTEXT_TYPE_WEBGPU) {
    if (!gpu_channel_manager_->gpu_preferences().enable_webgpu) {
      DLOG(ERROR) << "ContextResult::kFatalFailure: WebGPU not enabled";
      return;
    }

    stub = std::make_unique<WebGPUCommandBufferStub>(
        this, *init_params, command_buffer_id, sequence_id, stream_id,
        route_id);
  } else if (init_params->attribs.enable_raster_interface &&
             !init_params->attribs.enable_gles2_interface &&
             !init_params->attribs.enable_grcontext) {
    stub = std::make_unique<RasterCommandBufferStub>( // -------- [6] create stub
        this, *init_params, command_buffer_id, sequence_id, stream_id,
        route_id);
  } else {
    stub = std::make_unique<GLES2CommandBufferStub>(
        this, *init_params, command_buffer_id, sequence_id, stream_id,
        route_id);
  }

  stub->BindEndpoints(std::move(receiver), std::move(client), io_task_runner_);

  auto stub_result =
      stub->Initialize(share_group, *init_params, std::move(shared_state_shm)); // [5] initialize stub here

[7] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:gpu/ipc/service/gpu_channel.cc;l=563-565;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188

 GpuChannel::~GpuChannel() {
  // Clear stubs first because of dependencies.
  stubs_.clear(); // -------- [7] may free the just created stubs

[8] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:gpu/ipc/service/gpu_channel.cc;l=425-429;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188

void GpuChannelMessageFilter::DestroyCommandBuffer(
    int32_t routing_id,
    DestroyCommandBufferCallback callback) {
  base::AutoLock auto_lock(gpu_channel_lock_);
  if (!gpu_channel_) {
    receiver_.reset();
    return;
  }

  main_task_runner_->PostTaskAndReply(
      FROM_HERE,
      base::BindOnce(&gpu::GpuChannel::DestroyCommandBuffer,
                     gpu_channel_->AsWeakPtr(), routing_id),
      std::move(callback));
}

[9] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:gpu/ipc/service/gpu_channel_manager.cc;l=460-464;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188

void GpuChannelManager::RemoveChannel(int client_id) {
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);

  auto it = gpu_channels_.find(client_id);
  if (it == gpu_channels_.end())
    return;

  delegate_->DidDestroyChannel(client_id);

  // Erase the |gpu_channels_| entry before destroying the GpuChannel object to
  // avoid reentrancy problems from the GpuChannel destructor.
  std::unique_ptr<GpuChannel> channel = std::move(it->second);
  gpu_channels_.erase(it);
  channel.reset(); // [9]

  if (gpu_channels_.empty()) {
    delegate_->DidDestroyAllChannels();
  }
}

[10] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:services/viz/privileged/mojom/gl/gpu_service.mojom;l=51-56;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188

  [Sync, NoInterrupt]
  EstablishGpuChannel(int32 client_id,
                      uint64 client_tracing_id,
                      bool is_gpu_host)
      => (handle<message_pipe>? channel_handle,
          gpu.mojom.GpuInfo gpu_info,
          gpu.mojom.GpuFeatureInfo gpu_feature_info);

[11] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:gpu/ipc/service/gpu_channel_manager.cc;l=488;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188

[12] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/browser_child_process_host_impl.cc;l=434;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188

[13] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/child_process_host_impl.cc;l=268-273;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188



# BISECT

This UAF is introduced in https://chromium-review.googlesource.com/c/chromium/src/+/2881324

Hence it affect all Chromium stable/beta/dev/canary version. 

Since the affected version starts at 
    Canary 92 92.0.4507.0
    Dev 92 92.0.4512.3
    Beta 92 92.0.4515.40
    Stable 92 92.0.4515.107

### he...@gmail.com (2023-07-13)

# Patch suggestion

An easy to fix method is to turn `DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);` to the hard `CHECK`. However, this may affect the performance or the stability. A more friendly patch may related to control defer the destruction of stub in the `~GpuChannel()`.

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:gpu/ipc/service/gpu_channel_manager.cc;l=452;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188

# Reproduction

As mentioned in the RCA, this may trigger by the pure web page. However, to improve the repro success rate or the timing chance, another https://crbug.com/chromium/1450801 of mine describe another PoC to repro it flaky.  

# Additional note:

Note that the root cause of another similar https://crbug.com/chromium/1396212 is slightly differently than this one. Although they are both UAF caused in the stub, the trigger method and the concurrency thread context are different. I'll dig that one as soon as possible. 

Thank you very much.

### he...@gmail.com (2023-07-22)

FYI, I've made a possible patch to fix this issue directly, thank you.

diff --git a/gpu/ipc/service/gpu_channel_manager.cc b/gpu/ipc/service/gpu_channel_manager.cc
index c1d3e2128c2f3..bfa9f0fd1eaa0 100644
--- a/gpu/ipc/service/gpu_channel_manager.cc
+++ b/gpu/ipc/service/gpu_channel_manager.cc
@@ -376,7 +376,7 @@ GpuChannelManager::GpuChannelManager(
 }

 GpuChannelManager::~GpuChannelManager() {
-  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);
+  CHECK(thread_checker_.CalledOnValidThread());
   // Clear |gpu_channels_| first to prevent reentrancy problems from GpuChannel
   // destructor.
   auto gpu_channels = std::move(gpu_channels_);
@@ -449,7 +449,7 @@ gles2::ProgramCache* GpuChannelManager::program_cache() {
 }

 void GpuChannelManager::RemoveChannel(int client_id) {
-  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);
+  CHECK(thread_checker_.CalledOnValidThread());

   auto it = gpu_channels_.find(client_id);
   if (it == gpu_channels_.end())
@@ -480,7 +480,7 @@ GpuChannel* GpuChannelManager::EstablishChannel(
     int client_id,
     uint64_t client_tracing_id,
     bool is_gpu_host) {
-  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);
+  CHECK(thread_checker_.CalledOnValidThread());

   // Remove existing GPU channel with same client id before creating
   // new GPU channel. if not, new SyncPointClientState in SyncPointManager

### he...@gmail.com (2023-07-28)

friendly ping - @Geoff @jonahr

Not sure whether is issue buried in the working list. If there's anything unclear above, feel free to point it out. Moreover, I could submit the patch to the Gerrit if you could review/handle it.

Thank you very much.

### ge...@chromium.org (2023-07-31)

Hey, catching up on this now. Great writeup of the investigation.

I agree that these DCHECKs should be CHECKs but the underlying issue will still be present. Going through the call sites of GpuChannelManager::RemoveChannel, it looks like only GpuChannel::OnChannelError isn't making sure the call is happening on the correct thread, I think we need a PostTask.

### ge...@chromium.org (2023-07-31)

Ken: I'd like your opinions on this one since you've worked in the GPU channel IPC stuff before. How should we make sure that GpuChannel::OnChannelError propagates to GpuChannelManager::RemoveChannel on the correct thread?

### he...@gmail.com (2023-08-30)

friendly ping - 

In GpuChannelManager::RemoveChannel, maybe we could use | task_runner_ | to post a task which cleanup the gpu_channels_.

### he...@gmail.com (2023-09-11)

Hello Geoff,

Seems that Ken haven't online for a quite long time. Could you please CC another developer to fix it. Like @sunn which manages https://crbug.com/chromium/1478409.

### bo...@google.com (2023-11-06)

[Security shepherd update] I pinged @rockot & @geofflang via chat, which I'll paraphrase here for transparency. 

The repro script in https://crbug.com/chromium/1396304#c1 includes enablement of over 1200 features. Progress of analysis is blocked on having a reasonably sized list of features. 

@hedonistsmith, can you help by finding the minimum set of feature flags required to trigger this issue? 

Once we have a narrower scope for analysis then we can invite someone more familiar with GpuChannel, such as possibly jonross, to help diagnose the root cause. 

### am...@chromium.org (2023-11-14)

[security shepherd update] OP / reporter, friendly ping here -- can you please minimize the number of feature flags that need to be set to trigger this issue? 
RCA is currently blocked by this information.
Analysis may continue to stall without this sort of minimization which is an expected characteristic of VRP reports, even those at baseline report quality. 
Leaving this issue in a needs-feedback status. 




### he...@gmail.com (2023-11-21)

Hello, it only need **SkiaGraphite** feature to reproduce originally in that version. However, this couldn't be reproduced in my recent chromium build. 

There might have some code changes in recent month, since I haven't focus on investigating this UAF recently.

From the original ASAN stack, I thought that this may have the same root cause with the https://crbug.com/chromium/1396212 and is fixed by r4847892. Thank you very much.

### jo...@chromium.org (2023-11-22)

+blundell@ to take a look since the original repro seems to be tied to SkiaGraphite.

There has certainly been a lot of work on that project since this was identified. So this may have been mitigated since

### bl...@chromium.org (2023-11-22)

It's unclear what the relationship between the description of the issue in [1] and Graphite is? Maybe somehow Graphite was more likely to tickle the issue, but assuming that the description in [1] is correct, the issue predates and is more general than Graphite.

[1] https://bugs.chromium.org/p/chromium/issues/detail?id=1396304#c16

### bl...@chromium.org (2023-11-23)

hedonistasmith@: Can you link again to the CL that you think might have fixed this issue? The link you provided in https://crbug.com/chromium/1396304#c26 is broken.


### he...@gmail.com (2023-11-23)

perhaps https://chromium-review.googlesource.com/c/chromium/src/+/4847892

Moreover, I think only the above patch is not complete enough to fix this issue. Since https://crbug.com/chromium/1396304#c16 has analyzed the root cause, turning to a CHECK could be a temporary idea to completely fix it.


### bl...@chromium.org (2023-11-24)

Unless I'm missing something, https://chromium-review.googlesource.com/c/chromium/src/+/4847892 indeed doesn't seem related to the issue outlined in https://crbug.com/chromium/1396304#c16. Based on https://crbug.com/chromium/1396304#c16, Graphite also seems unrelated.

rockot@: Could you take a look at https://crbug.com/chromium/1396304#c16-#21 and give your judgment on the best approach to take here? Thanks!

### ah...@google.com (2023-12-22)

[secondary security shepherd] 

Hello @rockot@google.com, 
A friendly ping to check https://crbug.com/chromium/1396304#c31.

Thanks!

### ro...@google.com (2023-12-28)

The proposed fix in c#18 LGTM at least as an immediate way to address the UAFs. Then it's just a matter of following up on the new resulting CHECK failures to correct any wrong-thread accesses.

### he...@gmail.com (2023-12-28)

I would like propose/commit the patch in c#18 if you would like to review it. Thank you.

### he...@gmail.com (2023-12-28)

Proposed a candidate patch on https://chromium-review.googlesource.com/c/chromium/src/+/5154495

### bl...@chromium.org (2024-01-02)

Thanks for the contribution! Ensuring that we're getting it reviewed.

### ja...@chromium.org (2024-01-17)

Hello Bug Reporter! Thanks again for the changelist. It looks like the review is to you now.

Hello blundell@, if the changelist isn't updated soon, would it be useful if you copied the fix and got it reviewed/submitted yourself, so we can address the issue? 

[secondary security shepherd]

### bl...@chromium.org (2024-01-18)

Vasiliy pointed out that the approach in that CL doesn't actually work as ThreadChecker does validation only if DCHECKs are enabled: https://source.chromium.org/chromium/chromium/src/+/main:base/threading/thread_checker.h;drc=71f64d72a7ac8448e898857d29e34b93a5f3cff9;l=129

So the patch there won't actually hard-protect in production. I don't offhand have an alternative approach to suggest.

### he...@gmail.com (2024-01-19)

Thanks for the remind. I'll propose an alternative approach.

### gi...@appspot.gserviceaccount.com (2024-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bec5edb475fc49d80db7621cf07822f8400cf4f8

commit bec5edb475fc49d80db7621cf07822f8400cf4f8
Author: Smith Hedonist <hedonistsmith@gmail.com>
Date: Tue Jan 23 11:43:16 2024

Check GpuChannel thread consistency

GpuChannelManager::RemoveChannel() can be called on the wrong thread,
causing the UAF of GpuChannel object during thread racing. Avoid further
wrong-thread accesses by the sequence hard check.

Fixed: 1396304
Change-Id: I3a907a0a5cca6d58717ab7604ba57c623cc313a2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5154495
Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org>
Reviewed-by: Colin Blundell <blundell@chromium.org>
Commit-Queue: Colin Blundell <blundell@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1250743}

[modify] https://crrev.com/bec5edb475fc49d80db7621cf07822f8400cf4f8/gpu/ipc/service/gpu_channel_manager.cc
[modify] https://crrev.com/bec5edb475fc49d80db7621cf07822f8400cf4f8/AUTHORS


### [Deleted User] (2024-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-23)

[Empty comment from Monorail migration]

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations! The Chrome VRP Panel has decided to award you $5,000 for this report a GPU process memory corruption bug that is mitigated by race condition and for which no real reproducer to demonstrate real-world exploitability was provided. We did also reward you a $2,000 patch bonus -- thanks for your efforts in submitting a patch and committing it to Chromium directly. Thanks for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1396304?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1450801]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-05-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062066)*
