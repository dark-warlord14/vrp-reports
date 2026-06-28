# Insufficient bounds check in ANGLE Metal UBO bool conversion leads to heap OOB read in GPU process on Mac

| Field | Value |
|-------|-------|
| **Issue ID** | [489585044](https://issues.chromium.org/issues/489585044) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-03-04 |
| **Bounty** | $3,000.00 |

## Description

## Insufficient bounds check in ANGLE Metal UBO bool conversion leads to heap OOB read in GPU process on Mac

### Summary

The ANGLE Metal backend's `ConvertUniformBufferData` function performs an insufficient bounds check when converting std140 boolean uniform values to Metal's 1-byte representation. The check validates only that the source pointer falls within the buffer, but does not account for the full 4-byte dereference that follows, allowing a 1 to 3 byte heap out-of-bounds read in the GPU process. The bug is reachable from any WebGL2 page on macOS using the Metal backend.

Platform: macOS (Metal backend). Affects both Intel and Apple Silicon Macs.

### Bisect

Introducing Commit: `b23bf47c9e999532a684beab9ac901552420b0b8`

- Date: Wed Jan 25 18:50:40 2023 -0800
- Author: Kyle Piddington
- Review: <https://chromium-review.googlesource.com/c/angle/angle/+/4209867>

A subsequent commit `f7d7be8d2ff0bbee438b6030419a0b13082de198` ("Metal: upstream 'UBO convert only whole block'") added the `srcBool < maxSrcPtr` bounds check to this code path, but the check is insufficient as described below.

### Root Cause

When a WebGL2 shader uses a uniform block containing a `bool` field, the ANGLE Metal backend must convert between the std140 layout (where bools occupy 4 bytes) and Metal's native layout (where bools occupy 1 byte). This conversion happens in `ConvertUniformBufferData`, called from `legalizeUniformBufferOffsets` at draw time.

The function computes `sizeToCopy` as the full buffer size minus the initial source offset, then divides by the block's std140 size to determine how many block instances to process:

```
// ProgramExecutableMtl.mm — legalizeUniformBufferOffsets
size_t sizeToCopy = bufferMtl->size() - conversion->initialSrcOffset();

// ProgramExecutableMtl.mm — ConvertUniformBufferData
const uint8_t *maxSrcPtr = sourceData + sizeToCopy;
size_t numBlocksToCopy =
    (sizeToCopy + blockConversionInfo.stdSize() - 1) / blockConversionInfo.stdSize();

```

This ceiling division means that if the buffer size is not an exact multiple of `stdSize`, the function will process a partial final block. When this partial block contains a boolean field, the following code runs:

```
// ProgramExecutableMtl.mm — ConvertUniformBufferData, bool branch
const uint8_t *srcBool =
    (sourceData + stdIterator->offset + stdArrayOffset +
     blockConversionInfo.stdSize() * i +
     gl::VariableComponentSize(GL_BOOL) * boolCol);
unsigned int srcValue =
    srcBool < maxSrcPtr ? *((unsigned int *)(srcBool)) : 0;

```

The guard `srcBool < maxSrcPtr` checks that the start of the 4-byte value is within bounds, but `*((unsigned int *)(srcBool))` reads 4 bytes starting at `srcBool`. When `srcBool` points to, say, the last byte of the buffer, the check passes (the pointer is less than `maxSrcPtr`) but the dereference reads 3 bytes past the end of the allocation.

To trigger the partial block, the buffer must be created with a size that is not a multiple of the block's std140 size. ANGLE's Metal backend rounds up buffer sizes to 16 bytes when the buffer is first created as `UNIFORM_BUFFER`, but this round-up does not apply when the buffer is initially created as `ARRAY_BUFFER` and later bound to a uniform buffer binding point. This is a known gap acknowledged in a TODO comment in `BufferMtl::setDataImpl`:

```
// BufferMtl.mm — setDataImpl
if (target == gl::BufferBinding::Uniform)
{
    // This doesn't work! A buffer can be allocated on ARRAY_BUFFER and used in UNIFORM_BUFFER
    // TODO(anglebug.com/42266052)
    adjustedSize = roundUpPow2(adjustedSize, (size_t)16);
}

```

When `useShadowBuffersWhenAppropriate` is enabled (default on Intel Macs, can be force-enabled elsewhere), `getBufferDataReadOnly` returns a pointer to a `malloc`-backed shadow copy whose size matches the exact buffer allocation. This makes the OOB read land on a precisely sized heap allocation where ASAN can detect it. Without shadow buffers, the read targets a Metal buffer mapping with driver-level alignment padding, so the OOB still occurs but may not trigger ASAN.

The concrete trigger sequence: a uniform block `layout(std140) uniform U { bool b; }` has `stdSize = 4`. A buffer created as `ARRAY_BUFFER` with 5 bytes, then bound via `bindBufferRange` to a uniform buffer binding, produces `sizeToCopy = 5`, `numBlocksToCopy = ceil(5/4) = 2`. The second block iteration sets `srcBool = sourceData + 4`. Since `4 < 5`, the check passes, but the 4-byte read at offset 4 reaches bytes `[4..7]`, overflowing the 5-byte allocation by 3 bytes.

### Reproduce

Tested on Chromium commit `d0f83d769eeed`, macOS with Metal backend. The ASAN build must have the `useShadowBuffersWhenAppropriate` ANGLE feature enabled at runtime so that UBO shadow copies go through `malloc`, which ASAN can track. Without this, Metal buffer mappings are used and the OOB read still occurs but escapes ASAN detection.

Build Chromium with ASAN enabled. A minimal `args.gn` for `out/asan-release`:

```
is_asan = true
is_debug = false
is_component_build = false
symbol_level = 1

```

Then build:

```
autoninja -C ~/chromium/src/out/asan-release chrome

```

Launch Chrome with the PoC, forcing the Metal backend and the shadow buffer feature:

```
ANGLE_FEATURE_OVERRIDES_ENABLED=useShadowBuffersWhenAppropriate \
ASAN_OPTIONS=detect_odr_violation=0 \
~/chromium/src/out/asan-release/Chromium.app/Contents/MacOS/Chromium \
  --no-sandbox --use-angle=metal \
  --user-data-dir=/tmp/poc-$(date +%s) \
  poc.html

```

The GPU process will report a heap-buffer-overflow in `rx::ProgramExecutableMtl::legalizeUniformBufferOffsets` with a READ of size 4. The shadow byte pattern `[05]` confirms a 5-byte allocation where a 4-byte read starting at offset 4 overflows by 3 bytes. On Intel Macs, `useShadowBuffersWhenAppropriate` is enabled by default, so the environment variable override is not needed.

ASAN output:

```
=================================================================
==11248==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000010014 at pc 0x000307933094 bp 0x00016bccbcb0 sp 0x00016bccbca8
READ of size 4 at 0x602000010014 thread T0
==11248==WARNING: invalid path to external symbolizer!
==11248==WARNING: Failed to use and restart external symbolizer!
    #0 0x000307933090 in rx::ProgramExecutableMtl::legalizeUniformBufferOffsets(rx::ContextMtl*)+0x1580 (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Libraries/libGLESv2.dylib:arm64+0x933090)
    #1 0x0003079308a4 in rx::ProgramExecutableMtl::updateUniformBuffers(rx::ContextMtl*, rx::mtl::RenderCommandEncoder*, rx::mtl::RenderPipelineDesc const&)+0x1a4 (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Libraries/libGLESv2.dylib:arm64+0x9308a4)
    #2 0x00030792ea94 in rx::ProgramExecutableMtl::setupDraw(gl::Context const*, rx::mtl::RenderCommandEncoder*, rx::mtl::RenderPipelineDesc const&, bool, bool, bool)+0x340 (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Libraries/libGLESv2.dylib:arm64+0x92ea94)
    #3 0x0003078fd4b0 in rx::ContextMtl::setupDrawImpl(gl::Context const*, gl::PrimitiveMode, int, int, int, gl::DrawElementsType, void const*, bool, bool*)+0xb28 (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Libraries/libGLESv2.dylib:arm64+0x8fd4b0)
    #4 0x0003078efbc0 in rx::ContextMtl::drawArraysImpl(gl::Context const*, gl::PrimitiveMode, int, int, int, unsigned int)+0x2cc (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Libraries/libGLESv2.dylib:arm64+0x8efbc0)
    #5 0x0003078f1ad4 in rx::ContextMtl::drawArrays(gl::Context const*, gl::PrimitiveMode, int, int)+0x158 (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Libraries/libGLESv2.dylib:arm64+0x8f1ad4)
    #6 0x000307033f3c in GL_DrawArrays+0x4f0 (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Libraries/libGLESv2.dylib:arm64+0x33f3c)
    #7 0x00010b06457c in gl::RealGLApi::glDrawArraysFn(unsigned int, int, int)+0x19c (/Users/user/chromium/src/out/asan-release/libgl_wrapper.dylib:arm64+0xc857c)
    #8 0x00014777ec50 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(unsigned int, int, int)+0x94 (/Users/user/chromium/src/out/asan-release/libgpu_gles2.dylib:arm64+0xd2c50)
    #9 0x0001477496cc in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)+0x1a4 (/Users/user/chromium/src/out/asan-release/libgpu_gles2.dylib:arm64+0x9d6cc)
    #10 0x00013e936b44 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x4bc (/Users/user/chromium/src/out/asan-release/libgpu_command_buffer_service.dylib:arm64+0xab44)
    #11 0x000142ee616c in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)+0x450 (/Users/user/chromium/src/out/asan-release/libgpu_ipc_service.dylib:arm64+0x616c)
    #12 0x000142ee52ec in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)+0x468 (/Users/user/chromium/src/out/asan-release/libgpu_ipc_service.dylib:arm64+0x52ec)
    #13 0x000142f099fc in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)+0x290 (/Users/user/chromium/src/out/asan-release/libgpu_ipc_service.dylib:arm64+0x299fc)
    #14 0x000142f15aa8 (/Users/user/chromium/src/out/asan-release/libgpu_ipc_service.dylib:arm64+0x35aa8)
    #15 0x000142f158c0 (/Users/user/chromium/src/out/asan-release/libgpu_ipc_service.dylib:arm64+0x358c0)
    #16 0x00013e97dafc (/Users/user/chromium/src/out/asan-release/libgpu_command_buffer_service.dylib:arm64+0x51afc)
    #17 0x00013e95200c in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x634 (/Users/user/chromium/src/out/asan-release/libgpu_command_buffer_service.dylib:arm64+0x2600c)
    #18 0x00013e9506a4 in gpu::Scheduler::RunNextTask()+0x27c (/Users/user/chromium/src/out/asan-release/libgpu_command_buffer_service.dylib:arm64+0x246a4)
    #19 0x00013e95484c (/Users/user/chromium/src/out/asan-release/libgpu_command_buffer_service.dylib:arm64+0x2884c)
    #20 0x00010670d804 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x1fd804)
    #21 0x00010678ae84 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x27ae84)
    #22 0x00010678a23c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x27a23c)
    #23 0x0001069163cc in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x4063cc)
    #24 0x000106900df8 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x3f0df8)
    #25 0x00010691475c in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x40475c)
    #26 0x00019c086b10 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7cb10)
    #27 0x00019c086aa4 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7caa4)
    #28 0x00019c086810 in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7c810)
    #29 0x00019c085464 in __CFRunLoopRun+0x344 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7b464)
    #30 0x00019c084a94 in CFRunLoopRunSpecific+0x238 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7aa94)
    #31 0x00019d654c74 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd0 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:arm64e+0x59c74)
    #32 0x000106917db8 in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xc8 (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x407db8)
    #33 0x000106913334 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290 (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x403334)
    #34 0x00010678c240 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x27c240)
    #35 0x000106678b08 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x168b08)
    #36 0x000134c6ca04 in content::GpuMain(content::MainFunctionParams)+0x8b4 (/Users/user/chromium/src/out/asan-release/libcontent.dylib:arm64+0x10a04)
    #37 0x0001389e4ac8 in content::RunOtherNamedProcessTypeMain(...)+0x420 (/Users/user/chromium/src/out/asan-release/libcontent.dylib:arm64+0x3d88ac8)
    #38 0x0001389e6c48 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/user/chromium/src/out/asan-release/libcontent.dylib:arm64+0x3d8ac48)
    #39 0x0001389e2558 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/user/chromium/src/out/asan-release/libcontent.dylib:arm64+0x3d86558)
    #40 0x0001389e2a48 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/user/chromium/src/out/asan-release/libcontent.dylib:arm64+0x3d86a48)
    #41 0x00011c79b724 in ChromeMain+0x490 (/Users/user/chromium/src/out/asan-release/libchrome_dll.dylib:arm64+0xb724)
    #42 0x000104130b94 in main+0x254 (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:arm64+0x100000b94)
    #43 0x00019bbfab94 in start+0x17b8 (/usr/lib/dyld:arm64e+0x6b94)

0x602000010015 is located 0 bytes after 5-byte region [0x602000010010,0x602000010015)
allocated by thread T0 here:
    #0 0x000104a3cdb8 in __asan_memmove+0x2fd8 (/Users/user/chromium/src/out/asan-release/libclang_rt.asan_osx_dynamic.dylib:arm64+0x54db8)
    #1 0x000307a05a60 in angle::MemoryBuffer::resize(unsigned long)+0x50 (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Libraries/libGLESv2.dylib:arm64+0xa05a60)
    #2 0x0003078e04b4 in rx::BufferMtl::setDataImpl(gl::Context const*, gl::BufferBinding, void const*, unsigned long, gl::BufferUsage, rx::BufferFeedback*)+0x29c (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Libraries/libGLESv2.dylib:arm64+0x8e04b4)
    #3 0x0003073eab88 in gl::Buffer::setDataWithUsageFlags(...)+0x130 (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Libraries/libGLESv2.dylib:arm64+0x3eab88)
    #4 0x0003073ea688 in gl::Buffer::bufferDataImpl(...)+0x1d0 (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Libraries/libGLESv2.dylib:arm64+0x3ea688)
    #5 0x000147778850 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBufferData(unsigned int, long, void const*, unsigned int)+0xb0 (/Users/user/chromium/src/out/asan-release/libgpu_gles2.dylib:arm64+0xcc850)
    #6 0x0001477496cc in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)+0x1a4 (/Users/user/chromium/src/out/asan-release/libgpu_gles2.dylib:arm64+0x9d6cc)
    #7 0x00013e936b44 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x4bc (/Users/user/chromium/src/out/asan-release/libgpu_command_buffer_service.dylib:arm64+0xab44)
    #8 0x000142ee616c in gpu::CommandBufferStub::OnAsyncFlush(...)+0x450 (/Users/user/chromium/src/out/asan-release/libgpu_ipc_service.dylib:arm64+0x616c)
    #9 0x000142ee52ec in gpu::CommandBufferStub::ExecuteDeferredRequest(...)+0x468 (/Users/user/chromium/src/out/asan-release/libgpu_ipc_service.dylib:arm64+0x52ec)
    #10 0x000142f099fc in gpu::GpuChannel::ExecuteDeferredRequest(...)+0x290 (/Users/user/chromium/src/out/asan-release/libgpu_ipc_service.dylib:arm64+0x299fc)
    #11 0x000142f15aa8 (/Users/user/chromium/src/out/asan-release/libgpu_ipc_service.dylib:arm64+0x35aa8)
    #12 0x000142f158c0 (/Users/user/chromium/src/out/asan-release/libgpu_ipc_service.dylib:arm64+0x358c0)
    #13 0x00013e97dafc (/Users/user/chromium/src/out/asan-release/libgpu_command_buffer_service.dylib:arm64+0x51afc)
    #14 0x00013e95200c in gpu::Scheduler::ExecuteSequence(...)+0x634 (/Users/user/chromium/src/out/asan-release/libgpu_command_buffer_service.dylib:arm64+0x2600c)
    #15 0x00013e9506a4 in gpu::Scheduler::RunNextTask()+0x27c (/Users/user/chromium/src/out/asan-release/libgpu_command_buffer_service.dylib:arm64+0x246a4)
    #16 0x00013e95484c (/Users/user/chromium/src/out/asan-release/libgpu_command_buffer_service.dylib:arm64+0x2884c)
    #17 0x00010670d804 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x1fd804)
    #18 0x00010678ae84 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x27ae84)
    #19 0x00010678a23c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x27a23c)
    #20 0x0001069163cc in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x4063cc)
    #21 0x000106900df8 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x3f0df8)
    #22 0x00010691475c in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/user/chromium/src/out/asan-release/libbase.dylib:arm64+0x40475c)
    #23 0x00019c086b10 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18
    #24 0x00019c086aa4 in __CFRunLoopDoSource0+0xa8
    #25 0x00019c086810 in __CFRunLoopDoSources0+0xe4
    #26 0x00019c085464 in __CFRunLoopRun+0x344
    #27 0x00019c084a94 in CFRunLoopRunSpecific+0x238
    #28 0x00019d654c74 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd0
    #29 0x000106917db8 in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xc8
    #30 0x000106913334 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290
    #31 0x00010678c240 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c
    #32 0x000106678b08 in base::RunLoop::Run(base::Location const&)+0x430
    #33 0x000134c6ca04 in content::GpuMain(content::MainFunctionParams)+0x8b4
    #34 0x0001389e4ac8 in content::RunOtherNamedProcessTypeMain(...)+0x420
    #35 0x0001389e6c48 in content::ContentMainRunnerImpl::Run()+0x53c
    #36 0x0001389e2558 in content::RunContentProcess(...)+0x858
    #37 0x0001389e2a48 in content::ContentMain(content::ContentMainParams)+0x190
    #38 0x00011c79b724 in ChromeMain+0x490
    #39 0x000104130b94 in main+0x254
    #40 0x00019bbfab94 in start+0x17b8

0x602000010015 is located 0 bytes after 5-byte region [0x602000010010,0x602000010015)
allocated by thread T0 here:
    #0 0x000104a3cdb8 in __asan_memmove+0x2fd8
    #1 0x000307a05a60 in angle::MemoryBuffer::resize(unsigned long)+0x50
    #2 0x0003078e04b4 in rx::BufferMtl::setDataImpl(...)+0x29c
    #3 0x0003073eab88 in gl::Buffer::setDataWithUsageFlags(...)+0x130
    #4 0x0003073ea688 in gl::Buffer::bufferDataImpl(...)+0x1d0
    #5 0x000147778850 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBufferData(...)+0xb0
    #6 0x0001477496cc in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(...)+0x1a4
    #7 0x00013e936b44 in gpu::CommandBufferService::Flush(...)+0x4bc
    #8 0x000142ee616c in gpu::CommandBufferStub::OnAsyncFlush(...)+0x450
    #9 0x000142ee52ec in gpu::CommandBufferStub::ExecuteDeferredRequest(...)+0x468
    #10 0x000142f099fc in gpu::GpuChannel::ExecuteDeferredRequest(...)+0x290

SUMMARY: AddressSanitizer: heap-buffer-overflow (/Users/user/chromium/src/out/asan-release/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7702.0/Libraries/libGLESv2.dylib:arm64+0x933090) in rx::ProgramExecutableMtl::legalizeUniformBufferOffsets(rx::ContextMtl*)+0x1580
Shadow bytes around the buggy address:
  0x60200000fd80: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x60200000fe00: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa 00 00
  0x60200000fe80: f7 fa fd fa f7 fa 00 00 f7 fa 00 00 f7 fa 00 00
  0x60200000ff00: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fa
  0x60200000ff80: f7 fa fd fd f7 fa fd fa f7 fa fd fd f7 fa fd fd
=>0x602000010000: f7 fa[05]fa f7 fa fd fa f7 fa fd fd f7 fa fd fa
  0x602000010080: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x602000010100: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fd
  0x602000010180: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fd
  0x602000010200: f7 fa fd fd f7 fa 00 00 f7 fa fd fa f7 fa fd fa
  0x602000010280: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa 00 00
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

==11248==ABORTING

```
### Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 4.2 KB)
- [readme.md](attachments/readme.md) (text/markdown, 1.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 21.4 KB)

## Timeline

### je...@gmail.com (2026-03-04)

"--no-sandbox --use-angle=metal " No need, it was a typo while copying.

### cl...@appspot.gserviceaccount.com (2026-03-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4717186002124800.

### me...@google.com (2026-03-07)

Reproed locally on stable with `ANGLE_FEATURE_OVERRIDES_ENABLED=useShadowBuffersWhenAppropriate Chromium.app/Contents/MacOS/Chromium --use-angle=metal --user-data-dir=/tmp/...`

### 24...@project.gserviceaccount.com (2026-03-07)

Testcase 4717186002124800 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4717186002124800.

### ch...@google.com (2026-03-07)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-03-12)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7657186>

Metal: Round up all buffer sizes to 16 bytes.

---


Expand for full commit details
```
     
    Uniform buffers used to be rounded up to 16 bytes but it's possible to 
    bind other buffer types as uniform buffers later. Do the rounding on all 
    buffer types. 
     
    Bug: angleproject:42266052, chromium:489585044 
    Change-Id: I9bca591cf1e58dde750085e7335fe83d44f00b03 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7657186 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/BufferMtl.mm`
- M `src/tests/gl_tests/UniformBufferTest.cpp`

---

Hash: [92108f0e6867f8e45fe124abb962b8eb87dace76](https://chromiumdash.appspot.com/commit/92108f0e6867f8e45fe124abb962b8eb87dace76)  

Date: Wed Mar 11 20:30:52 2026


---

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7662538>

Roll ANGLE from 7a68f0166454 to fc2e9d6218eb (4 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/7a68f0166454..fc2e9d6218eb 
     
    2026-03-12 bsheedy@chromium.org Remove win-exp-test Starlark definition 
    2026-03-12 geofflang@chromium.org Revert "Metal: Use the mtl::Buffer's size when syncing shadow data." 
    2026-03-12 bsheedy@chromium.org Add src-side win-exp-test equivalents 
    2026-03-12 geofflang@chromium.org Metal: Round up all buffer sizes to 16 bytes. 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,cnorthrop@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:489494022,chromium:489585044 
    Tbr: cnorthrop@google.com 
    Change-Id: I1e13aa960f42dbc6d2963c263c011872e1c477ef 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7662538 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1598759}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [4544a92d68644dbac5fe74cfa970ee63533e38ab](https://chromiumdash.appspot.com/commit/4544a92d68644dbac5fe74cfa970ee63533e38ab)  

Date: Thu Mar 12 23:15:53 2026


---

### ch...@google.com (2026-03-18)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1598759) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1598759) appears to be after beta branch point (1596535).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146, 147].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-18)

No crashes in Canary. Merge approved to M146 and M147.

### go...@google.com (2026-03-19)

Please merge your change to M147 by 2:00 PM PT today so we can take it in for tomorrow's M147 beta release. Thank you.

### ch...@google.com (2026-03-24)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-24)

Project: angle/angle  

Branch:  chromium/7727  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7696621>

M147: Metal: Round up all buffer sizes to 16 bytes.

---


Expand for full commit details
```
     
    Uniform buffers used to be rounded up to 16 bytes but it's possible to 
    bind other buffer types as uniform buffers later. Do the rounding on all 
    buffer types. 
     
    Bug: angleproject:42266052, chromium:489585044 
    Change-Id: I9bca591cf1e58dde750085e7335fe83d44f00b03 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7657186 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit 92108f0e6867f8e45fe124abb962b8eb87dace76) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7696621 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

```

---

Files:

- M `src/libANGLE/renderer/metal/BufferMtl.mm`
- M `src/tests/gl_tests/UniformBufferTest.cpp`

---

Hash: [3afa9f7ef657f16f648e2aef166917bc55323458](https://chromiumdash.appspot.com/commit/3afa9f7ef657f16f648e2aef166917bc55323458)  

Date: Wed Mar 11 20:30:52 2026


---

### dx...@google.com (2026-03-24)

Project: angle/angle  

Branch:  chromium/7680  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7696620>

M146: Metal: Round up all buffer sizes to 16 bytes.

---


Expand for full commit details
```
     
    Uniform buffers used to be rounded up to 16 bytes but it's possible to 
    bind other buffer types as uniform buffers later. Do the rounding on all 
    buffer types. 
     
    Bug: angleproject:42266052, chromium:489585044 
    Change-Id: I9bca591cf1e58dde750085e7335fe83d44f00b03 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7657186 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit 92108f0e6867f8e45fe124abb962b8eb87dace76) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7696620 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

```

---

Files:

- M `src/libANGLE/renderer/metal/BufferMtl.mm`
- M `src/tests/gl_tests/UniformBufferTest.cpp`

---

Hash: [6c2b57330ed3d7e7984bc670d54493975fb5634e](https://chromiumdash.appspot.com/commit/6c2b57330ed3d7e7984bc670d54493975fb5634e)  

Date: Wed Mar 11 20:30:52 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-04-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-04-01)

1. <https://chromium-review.git.corp.google.com/c/angle/angle/+/7722538>
2. Low - no conflicts
3. 146 and 147
4. Yes, specially as the description notes the bug exists since 2023

### an...@google.com (2026-04-03)

Merge approved for LTS-138.

### sp...@google.com (2026-04-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-04-14)

Project: angle/angle  

Branch:  chromium/7204  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7727162>

[M138-LTS] Metal: Round up all buffer sizes to 16 bytes.

---


Expand for full commit details
```
     
    Uniform buffers used to be rounded up to 16 bytes but it's possible to 
    bind other buffer types as uniform buffers later. Do the rounding on all buffer types. 
     
    Bug: angleproject:42266052, chromium:489585044 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7657186 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit 92108f0e6867f8e45fe124abb962b8eb87dace76) 
    Change-Id: Ia105f45db27018b69e9b6dd1e87d52ad61c3f41c 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7727162 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

```

---

Files:

- M `src/libANGLE/renderer/metal/BufferMtl.mm`
- M `src/tests/gl_tests/UniformBufferTest.cpp`

---

Hash: [aa51faff4110ce8d508b68af70995da0e0bc1d9b](https://chromiumdash.appspot.com/commit/aa51faff4110ce8d508b68af70995da0e0bc1d9b)  

Date: Wed Mar 11 20:30:52 2026


---

### pe...@google.com (2026-05-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-04)

1. <https://chromium-review.git.corp.google.com/c/angle/angle/+/7808513>
2. Low - no conflicts
3. 138, 146 and 147
4. Yes

### dx...@google.com (2026-05-13)

Project: angle/angle  

Branch:  chromium/7559  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7808513>

[M144-LTS] Metal: Round up all buffer sizes to 16 bytes.

---


Expand for full commit details
```
     
    Uniform buffers used to be rounded up to 16 bytes but it's possible to 
    bind other buffer types as uniform buffers later. Do the rounding on all 
    buffer types. 
     
    Bug: angleproject:42266052, chromium:489585044 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7657186 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit 92108f0e6867f8e45fe124abb962b8eb87dace76) 
     
    Change-Id: Ia1683f1236b3450039e8baa058231a24986da88c 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7808513 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/BufferMtl.mm`
- M `src/tests/gl_tests/UniformBufferTest.cpp`

---

Hash: [a4bd261b34962f2a21e52e9cdbd054dc20cb6f18](https://chromiumdash.appspot.com/commit/a4bd261b34962f2a21e52e9cdbd054dc20cb6f18)  

Date: Wed Mar 11 20:30:52 2026


---

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489585044)*
