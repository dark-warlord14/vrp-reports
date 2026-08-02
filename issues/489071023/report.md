# Transform Feedback OOB Write via Multi-Draw Cumulative Overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [489071023](https://issues.chromium.org/issues/489071023) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-03-02 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

Transform Feedback OOB Write via Multi-Draw Cumulative Overflow

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

ANGLE's `ValidateMultiDrawArraysANGLE()` checks each sub-draw's transform feedback (XFB) buffer space against a stale `mVerticesDrawn` counter that is never updated between validation iterations. Sub-draws that individually fit within the XFB buffer but collectively exceed its capacity all pass validation. The backend then executes all sub-draws sequentially, writing past the XFB buffer boundary.

## Root Cause

### The Bug: Stale Accumulator in Multi-Draw Validation Loop

The root cause is a **stale accumulator** leading to **cumulative overflow** — the validation loop reads `mVerticesDrawn` without advancing it between iterations, so every sub-draw is checked against the same base offset. This gap is **deterministic and single-threaded**: the validation phase simply never updates the counter that the execution phase later advances correctly. Each sub-draw individually fits within the buffer, but their cumulative writes exceed its capacity.

```
// validationES2.cpp — ValidateMultiDrawArraysANGLE
bool ValidateMultiDrawArraysANGLE(const Context *context,
                                   angle::EntryPoint entryPoint,
                                   PrimitiveMode mode,
                                   const GLint *firsts,
                                   const GLsizei *counts,
                                   GLsizei drawcount)
{
    if (drawcount < 0) { ... return false; }
    for (GLsizei drawID = 0; drawID < drawcount; ++drawID)
    {
        if (!ValidateDrawArrays(context, entryPoint, mode,
                                firsts[drawID], counts[drawID]))
            return false;
        // *** BUG: mVerticesDrawn NOT updated between iterations ***
        // Each sub-draw validates against the same stale counter
    }
    return true;
}

```

The same stale-accumulator pattern exists in all multi-draw validation functions — each loops over sub-draws calling per-draw validation without advancing `mVerticesDrawn` between iterations:

```
// validationES2.cpp — ValidateMultiDrawElementsANGLE (same pattern)
for (GLsizei drawID = 0; drawID < drawcount; ++drawID)
{
    if (!ValidateDrawElements(context, entryPoint, mode, counts[drawID], type, indices[drawID]))
        return false;
    // BUG: mVerticesDrawn not updated between iterations
}

```
```
// validationES3.cpp — ValidateMultiDrawArraysInstancedANGLE (same pattern)
for (GLsizei drawID = 0; drawID < drawcount; ++drawID)
{
    if (!ValidateDrawArraysInstancedBase(context, entryPoint, mode, firsts[drawID],
                                         counts[drawID], instanceCounts[drawID], 0))
        return false;
    // BUG: mVerticesDrawn not updated — instanceCounts amplifies overflow
}

```
```
// validationES3.cpp — ValidateMultiDrawElementsInstancedANGLE (same pattern)
for (GLsizei drawID = 0; drawID < drawcount; ++drawID)
{
    if (!ValidateDrawElementsInstancedBase(context, entryPoint, mode, counts[drawID], type,
                                           indices[drawID], instanceCounts[drawID], 0))
        return false;
    // BUG: mVerticesDrawn not updated — instanceCounts amplifies overflow
}

```
### The XFB Space Check (called per sub-draw via ValidateDrawArraysCommon)

```
// validationES.h — inside ValidateDrawArraysCommon
if (ANGLE_UNLIKELY(context->getStateCache().isTransformFeedbackActiveUnpaused()) &&
    ANGLE_UNLIKELY(!context->supportsGeometryOrTesselation()))
{
    const State &state = context->getState();
    TransformFeedback *curTransformFeedback = state.getCurrentTransformFeedback();
    if (!curTransformFeedback->checkBufferSpaceForDraw(count, primcount))
    {
        ANGLE_VALIDATION_ERROR(GL_INVALID_OPERATION, err::kTransformFeedbackBufferTooSmall);
        return false;
    }
}

```
### The Counter Check (reads stale mVerticesDrawn)

```
// TransformFeedback.cpp — checkBufferSpaceForDraw
bool TransformFeedback::checkBufferSpaceForDraw(GLsizei count, GLsizei primcount) const
{
    auto vertices = mState.mVerticesDrawn +  // <-- STALE: never advanced during validation
        GetVerticesNeededForDraw(mState.mPrimitiveMode, count, primcount);
    return vertices.IsValid() && vertices.ValueOrDie() <= mState.mVertexCapacity;
}

```
### The Counter Update (only called AFTER execution, not during validation)

```
// TransformFeedback.cpp — onVerticesDrawn
void TransformFeedback::onVerticesDrawn(const Context *context, GLsizei count, GLsizei primcount)
{
    ASSERT(mState.mActive && !mState.mPaused);
    mState.mVerticesDrawn =
        (mState.mVerticesDrawn + GetVerticesNeededForDraw(mState.mPrimitiveMode, count, primcount))
            .ValueOrDie();
    // ...
}

```
### Execution Flow

```
Validation phase (all pass — stale mVerticesDrawn = 0):
  Sub-draw 0: checkBufferSpaceForDraw(400,1) → 0+400 <= 1024 ✓
  Sub-draw 1: checkBufferSpaceForDraw(400,1) → 0+400 <= 1024 ✓ (STALE!)
  ... (all 10 sub-draws pass)

Execution phase (MULTI_DRAW_BLOCK macro in renderer_utils.cpp):
  Sub-draw 0: writes 400 vertices at offset 0,     mVerticesDrawn = 400
  Sub-draw 1: writes 400 vertices at offset 1600,   mVerticesDrawn = 800
  Sub-draw 2: writes 400 vertices at offset 3200,   mVerticesDrawn = 1200 ← OVERFLOW START
  Sub-draw 3: writes 400 vertices at offset 4800,   mVerticesDrawn = 1600
  ...
  Sub-draw 9: writes 400 vertices at offset 14400,  mVerticesDrawn = 4000
  → 2976 vertices × 4 bytes = 11,904 bytes OOB write

```
## Reproduction Steps

### Cross-Tab Rendering Corruption

This PoC demonstrates that an attacker webpage can corrupt the GPU buffer data of a victim webpage open in a separate tab. Both tabs share Chrome's GPU process.

1. Open Chrome.
2. Open `poc_render_verify_victim_min.html` in Tab 1 — it renders 3 colored triangles (red, green, blue), sprays 4096 × 4KB GPU buffers with tagged sentinel data, then starts a rendering integrity monitoring loop
3. Open `poc_render_verify_attacker_min.html` in Tab 2 — click "Attack (100 rounds)"
4. The attacker page will:
   - Force ANGLE BufferManager GC eviction (60 temporary contexts destroyed + 3×600 buffer spray/free cycles + 256MB allocation pressure)
   - Allocate a 4KB XFB buffer (same size class as victim's buffers)
   - Execute 100 XFB overflow rounds via `multiDrawArraysWEBGL(POINTS, ...)` with 10 sub-draws of 400 vertices each
   - Each sub-draw passes validation individually (400 < 1024) because `mVerticesDrawn` is never updated between iterations
   - Each round writes 12KB past the 4KB buffer boundary into adjacent GPU memory
5. Expected victim behavior (if no bug): Rendering stays identical, all buffers clean
6. Actual (confirmed on Apple M4 Pro, macOS, Metal backend): **"GPU RENDERING CORRUPTION DETECTED"** — victim tab's triangles disappear or move to wrong positions, spray buffer sentinel data overwritten

**Note**: The cross-tab attack relies on GPU heap status (GC eviction + buffer spray) to place victim and attacker buffers adjacently. (multiple attempts may be required)

**How it works:**

1. Both tabs share Chrome's single GPU process and Metal device
2. ANGLE's per-context `BufferManager` caches freed buffers; GC eviction returns them to Metal
3. Attacker triggers GC eviction (destroy 60 temp contexts + 3×600 spray/free + 256MB pressure)
4. Victim allocates 4096 × 4KB buffers → Metal reuses freed regions, placing them adjacent to attacker's XFB buffer
5. Attacker executes XFB overflow → writes 12KB past buffer boundary into victim's VBO/spray buffers
6. Victim's rendering loop detects pixel differences → **GPU rendering corruption confirmed**

**Cross-tab attack timeline:**

```
Tab 1 (Victim):  Allocate VBO → Render triangles → Monitor rendering
Tab 2 (Attacker): GC eviction → Allocate XFB buf → multiDrawArrays overflow
                                                      ↓
Tab 1 (Victim):  Re-render → readPixels → PIXEL DIFFS DETECTED
                              → "GPU RENDERING CORRUPTION DETECTED"

```
## Attached Files

| File | Description |
| --- | --- |
| `poc_render_verify_attacker_min.html` | **Cross-tab attack PoC** — executes XFB overflow after GC eviction to corrupt victim's GPU buffers (CSS-stripped minimal version) |
| `poc_render_verify_victim_min.html` | **Cross-tab victim PoC** — renders 3 triangles + 4096×4KB buffer spray, monitors rendering integrity (CSS-stripped minimal version) |

#### Impact analysis

## Impact

An attacker can corrputs GPU memory. (POC shows that an attacker page corrupts the rendering output of a victim page in a different tab.)

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7632.117 stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

sweetchip

## Attachments

- [poc_pre_execute.png](attachments/poc_pre_execute.png) (image/png, 92.7 KB)
- [poc_after_execute.png](attachments/poc_after_execute.png) (image/png, 358.3 KB)
- [poc_render_verify_attacker_min.html](attachments/poc_render_verify_attacker_min.html) (text/html, 8.1 KB)
- [poc_render_verify_victim_min.html](attachments/poc_render_verify_victim_min.html) (text/html, 9.2 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### sw...@gmail.com (2026-03-07)

More information to reproduce this issue. You can use swiftshader to check ASAN crash reports.

1. Open poc\_render\_verify\_victim\_min.html in one tab.
2. Open poc\_render\_verify\_attacker\_min.html in two or three additional tabs.
3. Click "Attack" in the Attacker tabs.
4. Check the ASAN LOG.

This vulnerability has been reproduced on a Mac.

```
export ASAN_OPTIONS="detect_leaks=0:abort_on_error=1:print_stacktrace=1:symbolize=1:handle_segv=1:handle_sigbus=1:handle_sigfpe=1:handle_sigill=1:handle_abort=1:allow_user_segv_handler=0:detect_stack_use_after_return=1:detect_stack_use_after_scope=1:check_malloc_usable_size=0:detect_odr_violation=0:allocator_may_return_null=1:print_scariness=1:strict_memcmp=1:redzone=256:quarantine_size_mb=256:fast_unwind_on_fatal=0:malloc_context_size=30:log_path=stderr"
export MallocNanoZone=0

```
```
./Chromium.app/Contents/MacOS/Chromium
--disable-gpu-sandbox \
--no-sandbox \
--in-process-gpu --enable-features=WebGPUSubgroupMatrix --enable-unsafe-webgpu --enable-dawn-features=allow_unsafe_apis \
--no-first-run \
--use-webgpu-adapter=swiftshader --use-unsafe-webgpu ./poc.html

```
```
==12547==ABORTING
[12552:35088468:0309/170326.192239:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:484] GPU state invalid after WaitForGetOffsetInRange.
[12567:35089583:0309/170326.192304:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:484] GPU state invalid after WaitForGetOffsetInRange.
[12539:35088329:0309/170326.249495:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256
WARNING: sanitizers are preventing signal handler installation. Trap handlers are disabled.
Chromium Helper(12572,0x1f127b240) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper(12577,0x1f127b240) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper(12579,0x1f127b240) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper(12580,0x1f127b240) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper(12581,0x1f127b240) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper(12585,0x1f127b240) malloc: nano zone abandoned due to inability to reserve vm space.
Chromium Helper(12589,0x1f127b240) malloc: nano zone abandoned due to inability to reserve vm space.
[12539:35088435:0309/170337.982654:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
AddressSanitizer:DEADLYSIGNAL
=================================================================
==12572==ERROR: AddressSanitizer: BUS on unknown address (pc 0x000118381188 bp 0x000171fd8110 sp 0x000171fd7d70 T16)
==12572==The signal is caused by a READ memory access.
==12572==Hint: this fault was caused by a dereference of a high value address (see register values below).  Disassemble the provided pc to learn which register was used.
SCARINESS: 20 (wild-addr-read)
==12572==WARNING: invalid path to external symbolizer!
==12572==WARNING: Failed to use and restart external symbolizer!
    #0 0x000118381188 in AGX::TextureGen4<(AGXTextureMemoryLayout)3, AGX::G14X::Encoders, AGX::G14X::Classes>::TextureGen4(AGX::G14X::Device*, bool, AGXHardwareTextureMemoryOrder, MTLTextureType, AGX::TextureFormat const*, MTLPixelFormat, unsigned long, MTLStorageMode, AGXTextureCompressionSettings, eAGXColorSpaceConversion, eAGXTextureRotation, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, unsigned long, unsigned int, MTLCPUCacheMode, __IOSurface*, unsigned int, unsigned int, __IOSurface*, unsigned int, unsigned int, bool, bool, bool, unsigned long long)+0x82c (/System/Library/Extensions/AGXMetalG14X.bundle/Contents/MacOS/AGXMetalG14X:arm64e+0x6a9188)
    #1 0x000118386c54 in AGX::Texture<(AGXTextureMemoryLayout)3, AGX::G14X::Encoders, AGX::G14X::Classes>::createTextureViewForBlit(AGX::G14X::Texture const*, MTLTextureType, MTLPixelFormat, unsigned long, AGXTextureCompressionSettings, eAGXColorSpaceConversion, eAGXTextureRotation, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, unsigned long, MTLCPUCacheMode, __IOSurface*, unsigned int, unsigned int, __IOSurface*, bool, bool)+0x288 (/System/Library/Extensions/AGXMetalG14X.bundle/Contents/MacOS/AGXMetalG14X:arm64e+0x6aec54)
    #2 0x000117f0d668 in AGX::BlitContext<AGX::G14X::Encoders, AGX::G14X::Classes, AGX::G14X::ObjClasses>::copyTextureToBuffer(IOGPUMetalResource const*, unsigned long, unsigned long, unsigned long, AGXG14XFamilyTexture*, unsigned int, unsigned int, MTLOrigin, MTLSize, unsigned long)+0x368 (/System/Library/Extensions/AGXMetalG14X.bundle/Contents/MacOS/AGXMetalG14X:arm64e+0x235668)
    #3 0x000117f0ff38 in -[AGXG14XFamilyBlitContext copyFromTexture:sourceSlice:sourceLevel:sourceOrigin:sourceSize:toBuffer:destinationOffset:destinationBytesPerRow:destinationBytesPerImage:options:]+0x84 (/System/Library/Extensions/AGXMetalG14X.bundle/Contents/MacOS/AGXMetalG14X:arm64e+0x237f38)
    #4 0x0003014e2f40 in dawn::native::metal::CommandBuffer::FillCommands(dawn::native::metal::CommandRecordingContext*)+0x25cc (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x14e2f40)
    #5 0x00030150dde4 in dawn::native::metal::Queue::SubmitImpl(unsigned int, dawn::native::CommandBufferBase* const*)+0x198 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x150dde4)
    #6 0x0003013d4a38 in dawn::native::QueueBase::SubmitInternal(unsigned int, dawn::native::CommandBufferBase* const*)+0x334 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x13d4a38)
    #7 0x0003013d451c in dawn::native::QueueBase::APISubmit(unsigned int, dawn::native::CommandBufferBase* const*)+0xc8 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x13d451c)
    #8 0x0003011c723c in dawn::native::NativeQueueSubmit(WGPUQueueImpl*, unsigned long, WGPUCommandBufferImpl* const*)+0xe0 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x11c723c)
    #9 0x000300b57b64 in skgpu::graphite::DawnQueueManager::onSubmitToGpu(skgpu::graphite::SubmitInfo const&)+0x110 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0xb57b64)
    #10 0x000300a655a0 in skgpu::graphite::QueueManager::submitToGpu(skgpu::graphite::SubmitInfo const&)+0x1f8 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0xa655a0)
    #11 0x0003009c0a8c in skgpu::graphite::Context::submit(skgpu::graphite::SubmitInfo)+0x148 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x9c0a8c)
    #12 0x0003184c0b58 in gpu::GraphiteSharedContext::submit(skgpu::graphite::SyncToCpu)+0x104 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x184c0b58)
    #13 0x00031b8b2140 in viz::SkiaOutputDevice::Submit(scoped_refptr<gpu::SharedContextState>, bool, base::OnceCallback<void ()>)+0x190 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1b8b2140)
    #14 0x00031b8d6e0c in viz::SkiaOutputSurfaceImplOnGpu::SwapBuffersInternal(std::__Cr::optional<viz::OutputSurfaceFrame>)+0x454 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1b8d6e0c)
    #15 0x00031b8d6868 in viz::SkiaOutputSurfaceImplOnGpu::SwapBuffers(viz::OutputSurfaceFrame)+0x14c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1b8d6868)
    #16 0x00031b8a7010 in void base::internal::Invoker<base::internal::FunctorTraits<void (viz::SkiaOutputSurfaceImplOnGpu::*&&)(viz::OutputSurfaceFrame), viz::SkiaOutputSurfaceImplOnGpu*, viz::OutputSurfaceFrame&&>, base::internal::BindState<true, true, false, void (viz::SkiaOutputSurfaceImplOnGpu::*)(viz::OutputSurfaceFrame), base::internal::UnretainedWrapper<viz::SkiaOutputSurfaceImplOnGpu, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, viz::OutputSurfaceFrame>, void ()>::RunImpl<void (viz::SkiaOutputSurfaceImplOnGpu::*)(viz::OutputSurfaceFrame), std::__Cr::tuple<base::internal::UnretainedWrapper<viz::SkiaOutputSurfaceImplOnGpu, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, viz::OutputSurfaceFrame>, 0ul, 1ul>(void (viz::SkiaOutputSurfaceImplOnGpu::*&&)(viz::OutputSurfaceFrame), std::__Cr::tuple<base::internal::UnretainedWrapper<viz::SkiaOutputSurfaceImplOnGpu, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, viz::OutputSurfaceFrame>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>)+0x1c8 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1b8a7010)
    #17 0x00031b8ac7b8 in base::internal::Invoker<base::internal::FunctorTraits<viz::SkiaOutputSurfaceImpl::FlushGpuTasksWithImpl(viz::SkiaOutputSurfaceImpl::SyncMode, viz::SkiaOutputSurfaceImplOnGpu*, gpu::SyncToken const&)::$_0&&, std::__Cr::vector<base::OnceCallback<void ()>, std::__Cr::allocator<base::OnceCallback<void ()>>>&&, viz::SkiaOutputSurfaceImpl::SyncMode&&, base::WaitableEvent*&&, viz::SkiaOutputSurfaceImplOnGpu*&&, bool&&, bool&&, base::TimeTicks&&>, base::internal::BindState<false, false, false, viz::SkiaOutputSurfaceImpl::FlushGpuTasksWithImpl(viz::SkiaOutputSurfaceImpl::SyncMode, viz::SkiaOutputSurfaceImplOnGpu*, gpu::SyncToken const&)::$_0, std::__Cr::vector<base::OnceCallback<void ()>, std::__Cr::allocator<base::OnceCallback<void ()>>>, viz::SkiaOutputSurfaceImpl::SyncMode, base::internal::UnretainedWrapper<base::WaitableEvent, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<viz::SkiaOutputSurfaceImplOnGpu, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, bool, bool, base::TimeTicks>, void ()>::RunOnce(base::internal::BindStateBase*)+0x420 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1b8ac7b8)
    #18 0x000307e82860 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x634 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x7e82860)
    #19 0x000307e80ef8 in gpu::Scheduler::RunNextTask()+0x27c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x7e80ef8)
    #20 0x000307e84294 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x7e84294)
    #21 0x0003124c4814 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x124c4814)
    #22 0x00031252c888 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1252c888)
    #23 0x00031252bc40 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1252bc40)
    #24 0x00031264d2ac in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1264d2ac)
    #25 0x00031263e980 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1263e980)
    #26 0x00031264b708 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xe4 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1264b708)
    #27 0x00018cc22410 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7e410)
    #28 0x00018cc223a4 in __CFRunLoopDoSource0+0xac (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7e3a4)
    #29 0x00018cc22108 in __CFRunLoopDoSources0+0xf0 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7e108)
    #30 0x00018cc20cf4 in __CFRunLoopRun+0x344 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7ccf4)
    #31 0x00018cc20330 in CFRunLoopRunSpecific+0x238 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7c330)
    #32 0x00018ddde914 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd0 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:arm64e+0x5a914)
    #33 0x00031264e3fc in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xc8 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1264e3fc)
    #34 0x00031264a470 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1264a470)
    #35 0x00031252dbe8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1252dbe8)
    #36 0x000312452808 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x12452808)
    #37 0x0003125a2dd0 in base::Thread::Run(base::RunLoop*)+0xd8 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x125a2dd0)
    #38 0x0003125a3228 in base::Thread::ThreadMain()+0x3d8 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x125a3228)
    #39 0x0003125fa01c in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x125fa01c)
    #40 0x0001049b9870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #41 0x00018cb3b2e0 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x72e0)
    #42 0x00018cb360f8 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x20f8)

==12572==Register values:
 x[0] = 0x000062400004f688   x[1] = 0x000062400004e100   x[2] = 0x0000000000000000   x[3] = 0x0000000000008103
 x[4] = 0x0000000000000002   x[5] = 0x00000001183b1f98   x[6] = 0x0000000000000049   x[7] = 0x0000000000000000
 x[8] = 0x00000000bf800000   x[9] = 0x000062400004f650  x[10] = 0x00000f3300000000  x[11] = 0x0000000000000018
x[12] = 0x0000000100000000  x[13] = 0x000000012bdb1000  x[14] = 0x00000011f4000000  x[15] = 0x0000000000000004
x[16] = 0x000000018cb6d630  x[17] = 0x0000000118404750  x[18] = 0x0000000000000000  x[19] = 0x0000000171fd8388
x[20] = 0x000062400004f688  x[21] = 0x000000011842b000  x[22] = 0x00000001183b4678  x[23] = 0x0000000000000000
x[24] = 0x00000001ef7e1db4  x[25] = 0x0000000000000000  x[26] = 0x0000000000000000  x[27] = 0x0000000000000002
x[28] = 0x0000000171fd84cc     fp = 0x0000000171fd8110     lr = 0x0000000118381150     sp = 0x0000000171fd7d70
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: BUS (/System/Library/Extensions/AGXMetalG14X.bundle/Contents/MacOS/AGXMetalG14X:arm64e+0x6a9188) in AGX::TextureGen4<(AGXTextureMemoryLayout)3, AGX::G14X::Encoders, AGX::G14X::Classes>::TextureGen4(AGX::G14X::Device*, bool, AGXHardwareTextureMemoryOrder, MTLTextureType, AGX::TextureFormat const*, MTLPixelFormat, unsigned long, MTLStorageMode, AGXTextureCompressionSettings, eAGXColorSpaceConversion, eAGXTextureRotation, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, unsigned long, unsigned int, MTLCPUCacheMode, __IOSurface*, unsigned int, unsigned int, __IOSurface*, unsigned int, unsigned int, bool, bool, bool, unsigned long long)+0x82c
Thread T16 created by T0 here:
    #0 0x0001049b395c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x0003125f95e0 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x125f95e0)
    #2 0x0003125a2108 in base::Thread::StartWithOptions(base::Thread::Options)+0x498 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x125a2108)
    #3 0x00031b874ecc in viz::CompositorGpuThread::Create(viz::CompositorGpuThread::CreateParams const&)+0x258 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1b874ecc)
    #4 0x00031bb016c4 in viz::GpuServiceImpl::InitializeWithHostInternal(mojo::PendingRemote<viz::mojom::GpuHost>, gpu::GpuProcessShmCount, scoped_refptr<gl::GLSurface>, mojo::InlinedStructPtr<viz::mojom::GpuServiceCreationParams>, gpu::SyncPointManager*, gpu::SharedImageManager*, gpu::Scheduler*, base::WaitableEvent*)+0xb4c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1bb016c4)
    #5 0x00031bb00678 in viz::GpuServiceImpl::InitializeWithHost(mojo::PendingRemote<viz::mojom::GpuHost>, gpu::GpuProcessShmCount, scoped_refptr<gl::GLSurface>, mojo::InlinedStructPtr<viz::mojom::GpuServiceCreationParams>, base::WaitableEvent*)+0x2bc (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1bb00678)
    #6 0x00030bb3f0d4 in viz::VizMainImpl::CreateGpuService(mojo::PendingReceiver<viz::mojom::GpuService>, mojo::PendingRemote<viz::mojom::GpuHost>, mojo::PendingRemote<viz::mojom::GpuLogging>, mojo::PendingRemote<discardable_memory::mojom::DiscardableSharedMemoryManager>, base::UnsafeSharedMemoryRegion, mojo::InlinedStructPtr<viz::mojom::GpuServiceCreationParams>)+0x88c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0xbb3f0d4)
    #7 0x00030825d350 in viz::mojom::VizMainStubDispatch::Accept(viz::mojom::VizMain*, mojo::Message*)+0x70c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x825d350)
    #8 0x0003122d0cd0 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8fc (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x122d0cd0)
    #9 0x0003122e5b20 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x122e5b20)
    #10 0x0003122d5ec4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x122d5ec4)
    #11 0x0003122f2cc0 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x624 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x122f2cc0)
    #12 0x0003122f1794 in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x55c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x122f1794)
    #13 0x0003122e5b20 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x122e5b20)
    #14 0x0003122c3e6c in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x37c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x122c3e6c)
    #15 0x0003122c539c in mojo::Connector::ReadAllAvailableMessages()+0x234 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x122c539c)
    #16 0x0003122c4ea4 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x122c4ea4)
    #17 0x0003122c6984 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x122c6984)
    #18 0x0003039867cc in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x148 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x39867cc)
    #19 0x0003039865a8 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x39865a8)
    #20 0x000312aabc68 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x154 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x12aabc68)
    #21 0x000312aab684 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x398 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x12aab684)
    #22 0x000312aac5c4 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x12aac5c4)
    #23 0x0003124c4814 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x124c4814)
    #24 0x00031252c888 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1252c888)
    #25 0x00031252bc40 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1252bc40)
    #26 0x00031264d2ac in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1264d2ac)
    #27 0x00031263e980 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1263e980)
    #28 0x00031264b708 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xe4 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1264b708)
    #29 0x00018cc22410 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7e410)
    #30 0x00018cc223a4 in __CFRunLoopDoSource0+0xac (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7e3a4)
    #31 0x00018cc22108 in __CFRunLoopDoSources0+0xf0 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7e108)
    #32 0x00018cc20cf4 in __CFRunLoopRun+0x344 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7ccf4)
    #33 0x00018cc20330 in CFRunLoopRunSpecific+0x238 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7c330)
    #34 0x00018ddde914 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd0 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:arm64e+0x5a914)
    #35 0x00031264e3fc in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xc8 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1264e3fc)
    #36 0x00031264a470 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1264a470)
    #37 0x00031252dbe8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1252dbe8)
    #38 0x000312452808 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x12452808)
    #39 0x00031b81876c in content::GpuMain(content::MainFunctionParams)+0x8b4 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1b81876c)
    #40 0x00030eba4d10 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0xeba4d10)
    #41 0x00030eba6e90 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0xeba6e90)
    #42 0x00030eba2a00 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0xeba2a00)
    #43 0x00030eba2ef0 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0xeba2ef0)
    #44 0x000300005cb4 in ChromeMain+0x490 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x5cb4)
    #45 0x0001047a0c94 in main+0x254 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:arm64+0x100000c94)
    #46 0x00018c7b8270 in start+0xb14 (/usr/lib/dyld:arm64e+0x6270)


==12572==ADDITIONAL INFO

==12572==Note: Please include this section with the ASan report.
Task trace:
    #0 0x000307e810a0 in gpu::Scheduler::RunNextTask()+0x424 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x7e810a0)
    #1 0x000307e7cb24 in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*)+0x48c (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x7e7cb24)
    #2 0x00031b9cd144 in viz::DisplayScheduler::ScheduleBeginFrameDeadline()+0x3e0 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x1b9cd144)
    #3 0x000312aac000 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x230 (/Users/chip/Desktop/chrome/mac-release-arm64_asan-mac-release-1596143_/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7726.0/Chromium Framework:arm64+0x12aac000)


```

### jd...@chromium.org (2026-03-09)

Due to a dramatic influx of security vulnerability reports, I have not tried to reproduce this. Triaging conservatively assuming the report is valid. It's possible that this is invalid, or a duplicate of an already submitted report.

kbr@: can you help further route this?

### ch...@google.com (2026-03-10)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-10)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-16)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7758139>

Validate TF buffer size for multidraw calls.

---


Expand for full commit details
```
     
    Validation for transform feedback output buffer size was done per draw 
    call and the space available was accumulated after the draw finished. 
    For multidraw calls, this did not correctly calculate the counts. 
     
    Refactor this validation out of the common draw call validation and do 
    it in the higher level validation functions which are aware of how many 
    draws will be submitted. 
     
    Bug: chromium:489071023 
    Change-Id: Id1976906235a174688cf3c586ef7af49ae81dff9 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7758139 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Kenneth Russell <kbr@chromium.org>

```

---

Files:

- M `src/libANGLE/TransformFeedback.cpp`
- M `src/libANGLE/TransformFeedback.h`
- M `src/libANGLE/capture/capture_gles_ext_params.cpp`
- M `src/libANGLE/validationES.cpp`
- M `src/libANGLE/validationES.h`
- M `src/libANGLE/validationES2.cpp`
- M `src/libANGLE/validationES2.h`
- M `src/libANGLE/validationES3.cpp`
- M `src/libANGLE/validationESEXT.cpp`
- M `src/tests/gl_tests/TransformFeedbackTest.cpp`

---

Hash: [31151bbc3505a9fe84e64529c7f105a7cd8c40a6](https://chromiumdash.appspot.com/commit/31151bbc3505a9fe84e64529c7f105a7cd8c40a6)  

Date: Mon Apr 13 18:48:57 2026


---

### dx...@google.com (2026-04-17)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7770151>

Roll ANGLE from 905918456461 to 6ee4d31c38d7 (2 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/905918456461..6ee4d31c38d7 
     
    2026-04-16 mark@lunarg.com Tests: Add Arena Breakout: Realistic FPS trace 
    2026-04-16 geofflang@chromium.org Validate TF buffer size for multidraw calls. 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,solti@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:489071023 
    Tbr: solti@google.com 
    Test: Test: angle_trace_tests --gtest_filter=*arena_breakout 
    Change-Id: I0032f3e9ea2f1b8b7ce3c26459201ebc36dc1986 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7770151 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1616272}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [fc5774772cc4ab2b9d50fd46086377f91b171538](https://chromiumdash.appspot.com/commit/fc5774772cc4ab2b9d50fd46086377f91b171538)  

Date: Fri Apr 17 02:05:35 2026


---

### ch...@google.com (2026-04-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-04-21)

Requesting merge to M146 because latest trunk commit (1616272) appears to be after M146 branch point (1582197).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M147 because latest trunk commit (1616272) appears to be after M147 branch point (1596535).

Requesting merge to M148 because latest trunk commit (1616272) appears to be after M148 branch point (1610480).

### ch...@google.com (2026-04-21)

**M146** merge request created. **Please update [crbug/504872921](https://crbug.com/504872921) to have this merge reviewed.**

### ch...@google.com (2026-04-21)

**M147** merge request created. **Please update [crbug/504873317](https://crbug.com/504873317) to have this merge reviewed.**

### ch...@google.com (2026-04-21)

**M148** merge request created. **Please update [crbug/504873397](https://crbug.com/504873397) to have this merge reviewed.**

### sp...@google.com (2026-05-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline || Lower Impact. User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### sw...@gmail.com (2026-05-21)

Hello, Would it be possible to have a CVE assigned (or to share the CVE ID once it's allocated)?

### ch...@google.com (2026-07-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489071023)*
