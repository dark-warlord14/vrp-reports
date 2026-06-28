# Insufficient bounds check in ANGLE Metal UBO bool conversion leads to heap OOB read in GPU process on Mac

| Field | Value |
|-------|-------|
| **Issue ID** | [489494022](https://issues.chromium.org/issues/489494022) |
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

# Heap buffer overflow in BufferMtl shadow copy sync during bufferData leads to GPU process memory corruption in macOS

## Summary

A heap buffer overflow exists in the ANGLE Metal backend's `BufferMtl::ensureShadowCopySyncedFromGPU` function. When a WebGL `bufferData` call shrinks a buffer, the function copies data using the stale (larger) buffer size from `mState.getSize()`, which has not yet been updated by the caller `gl::Buffer::bufferDataImpl`. If the newly allocated Metal buffer was recycled from the `BufferManager` free list with its `cpuReadMemDirty` flag still set from a prior GPU write, the sync path executes a `memcpy` that writes up to 512 KB beyond the bounds of the freshly allocated 64-byte shadow copy. The overflow occurs in the GPU process, which on macOS runs outside the renderer sandbox. The vulnerability affects macOS with the Metal backend and is naturally reachable on systems with Intel integrated GPUs. An attacker-controlled web page can trigger it through ordinary WebGL2 API calls.

## Bisect

Introducing Commit: `968041b54770af8917001d8fe9b52a881cfed0b2`

- Date: 2022-08-19
- Author: Gregg Tavares
- CL: "Metal: Optimized BufferSubData per device"

The vulnerable `ensureShadowCopySyncedFromGPU` function with its `memcpy(mShadowCopy.data(), ptr, size())` pattern was introduced earlier in commit `bdecaf33eb` (2020-08-04, "Metal: Implement PBO"). However, the bug only became exploitable when the `BufferManager` buffer recycling mechanism was added in `968041b547`. Before this commit, Metal buffers were managed through a `BufferPool` that did not recycle buffers with stale dirty flags across unrelated GL buffer objects.

## Root Cause

The vulnerability arises from a timing mismatch between when ANGLE's backend implementation reads the GL buffer size and when the GL layer updates it. In `gl::Buffer::bufferDataImpl`, the backend's `setData` is invoked before `mState.mSize` is written:

```
// third_party/angle/src/libANGLE/Buffer.cpp
ANGLE_TRY(setDataWithUsageFlags(context, target, nullptr, dataForImpl, size, usage, flags,
                                bufferStorage));
// ...
mState.mSize = size;  // updated AFTER setData returns

```

Inside `BufferMtl::setDataImpl`, a new Metal buffer is obtained from the `BufferManager`, the shadow copy is resized to match the new (smaller) intended size, and then `setSubDataImpl` is called to populate it:

```
// third_party/angle/src/libANGLE/renderer/metal/BufferMtl.mm
ANGLE_TRY(allocateNewMetalBuffer(contextMtl, storageMode, adjustedSize,
                                 /*returnOldBufferImmediately=*/true, feedback));
ANGLE_CHECK_GL_ALLOC(contextMtl, mShadowCopy.resize(shadowSize));
if (data)
{
    ANGLE_TRY(setSubDataImpl(context, data, intendedSize, 0, feedback));
}

```

The call to `setSubDataImpl` reaches `updateShadowCopyThenCopyShadowToNewBuffer`, which first calls `ensureShadowCopySyncedFromGPU` to bring the shadow copy up to date with any prior GPU modifications:

```
// third_party/angle/src/libANGLE/renderer/metal/BufferMtl.mm
void BufferMtl::ensureShadowCopySyncedFromGPU(ContextMtl *contextMtl)
{
    if (mBuffer->isCPUReadMemDirty())
    {
        const uint8_t *ptr = mBuffer->mapReadOnly(contextMtl);
        memcpy(mShadowCopy.data(), ptr, size());
        mBuffer->unmap(contextMtl);
        mBuffer->resetCPUReadMemDirty();
    }
}

```

The `size()` accessor returns `static_cast<size_t>(mState.getSize())`, which at this point still holds the old, larger value. Meanwhile, `mShadowCopy` has just been resized to the new, smaller value. The `memcpy` therefore writes far beyond the shadow copy's allocation.

The second ingredient is the `BufferManager`'s buffer recycling. When `getBuffer` finds a cached buffer of the requested size, it returns it without clearing the resource usage flags:

```
// third_party/angle/src/libANGLE/renderer/metal/mtl_buffer_manager.mm
auto iter = freeBuffers.find(size);
if (iter != freeBuffers.end())
{
    bufferRef = iter->second;  // cpuReadMemDirty is NOT reset
    freeBuffers.erase(iter);
    return angle::Result::Continue;
}

```

A buffer that was previously the target of a GPU blit operation will have `cpuReadMemDirty` set to true via `Resource::setUsedByCommandBufferWithQueueSerial`. When such a buffer is recycled into an unrelated GL buffer object, `ensureShadowCopySyncedFromGPU` sees the stale dirty flag as a legitimate sync request and executes the oversized `memcpy`.

An attacker can manufacture this condition entirely from JavaScript. First, create a target buffer A with a large size (above the 256 KB shadow copy threshold) to establish a large `mState.mSize`. Then, create a helper buffer B at the desired small size, force a GPU blit write to B (by issuing `copyBufferSubData` while B is referenced by an in-flight draw command), wait for the GPU to finish, and return B's Metal buffer to the free list by reallocating B with a different size. Finally, call `bufferData` on A with the small size and provide data. The `BufferManager` recycles B's dirty buffer for A, the shadow copy is freshly allocated at the small size, and the memcpy uses A's old large size, producing a controlled heap overflow.

## Reproduce

This reproduction was tested on Chromium commit `d0f83d769eeed` (March 2026) on macOS with the ANGLE Metal backend. The vulnerable code path requires the `useShadowBuffersWhenAppropriate` ANGLE feature to be enabled. In `DisplayMtl.mm`, this feature is gated on the GPU vendor:

```
// third_party/angle/src/libANGLE/renderer/metal/DisplayMtl.mm
ANGLE_FEATURE_CONDITION((&mFeatures), alwaysUseSharedStorageModeForBuffers, isIntel());
ANGLE_FEATURE_CONDITION((&mFeatures), useShadowBuffersWhenAppropriate, isIntel());

```

When shadow buffers are enabled, `BufferMtl::setDataImpl` allocates a CPU-side shadow copy for any buffer whose adjusted size is at most 256 KB:

```
// third_party/angle/src/libANGLE/renderer/metal/BufferMtl.mm
size_t shadowSize = (!features.preferCpuForBuffersubdata.enabled &&
                     features.useShadowBuffersWhenAppropriate.enabled &&
                     adjustedSize <= mtl::kSharedMemBufferMaxBufSizeHint)
                        ? adjustedSize
                        : 0;

```

Intel Macs use shared-memory storage mode for Metal buffers, where the CPU and GPU access the same physical memory. The shadow copy mechanism was introduced to avoid stalling the GPU when the CPU needs to read back buffer contents, since shared-mode buffers do not support the managed-mode `didModifyRange`/`synchronize` synchronization model. On AMD and Apple GPUs, ANGLE uses either managed storage or staged buffer updates instead, so the shadow copy path is never taken and this vulnerability is not reachable through normal operation.

On non-Intel macOS systems (such as Apple Silicon), the feature can be force-enabled via the `--enable-angle-features=useShadowBuffersWhenAppropriate` command-line flag, which sets `hasOverride = true` on the feature and causes the `ANGLE_FEATURE_CONDITION` macro to skip the `isIntel()` check.

To prepare the build, check out the tested commit and configure an ASAN release build. Create the file `out/asan-release/args.gn` with the following contents:

```
is_asan = true
is_debug = false
dcheck_always_on = false
is_component_build = true

```

Then build Chrome:

```
ninja -C out/asan-release chrome

```

No source modifications are required for this PoC. Once the build completes, launch Chromium with the Metal backend and shadow buffer feature enabled:

```
ASAN_OPTIONS=detect_odr_violation=0 ./out/asan-release/Chromium.app/Contents/MacOS/Chromium \
  --use-angle=metal \
  --enable-angle-features=useShadowBuffersWhenAppropriate \
  --user-data-dir=/tmp/poc-angl076-$(date +%s) \
  --enable-logging=stderr \
  file://$(pwd)/issue_angl076/poc.html

```

The PoC page opens automatically and executes the WebGL2 trigger sequence. Within seconds, the GPU process will crash with an ASAN heap-buffer-overflow report. The ASAN summary will show a write of 524288 bytes into a 64-byte region within `rx::BufferMtl::setSubDataImpl`, originating from the `content::GpuMain` thread in the GPU process.

The vulnerability was additionally verified on a MacBook Pro (Intel Core i7-7820HQ, Intel HD Graphics 630) running a pre-built Chromium ASAN build (version 141.0.7367.0). On this Intel system, the Metal backend is the default and `useShadowBuffersWhenAppropriate` is natively enabled, so no additional command-line flags are needed:

```
ASAN_OPTIONS=detect_odr_violation=0 ./Chromium.app/Contents/MacOS/Chromium \
  --user-data-dir=/tmp/poc-angl076-$(date +%s) \
  --enable-logging=stderr \
  file:///path/to/poc.html

```

ASAN output (Intel Mac, no additional flags):

```
==58521==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6060001ea080 at pc 0x00010b19e85a bp 0x7ff7b4fa7ec0 sp 0x7ff7b4fa7678
WRITE of size 524288 at 0x6060001ea080 thread T0
    #0 0x00010b19e859 in __asan_memcpy+0x409 (libclang_rt.asan_osx_dynamic.dylib:x86_64+0x52859)
    #1 0x00011f00500b in rx::BufferMtl::setSubDataImpl(gl::Context const*, void const*, unsigned long, unsigned long, rx::BufferFeedback*)+0x21b (libGLESv2.dylib:x86_64+0x173f00b)
    #2 0x00011f004c51 in rx::BufferMtl::setDataImpl(gl::Context const*, gl::BufferBinding, void const*, unsigned long, gl::BufferUsage, rx::BufferFeedback*)+0x371 (libGLESv2.dylib:x86_64+0x173ec51)
    #3 0x00011e0258d6 in rx::BufferImpl::setDataWithUsageFlags(gl::Context const*, gl::BufferBinding, void*, void const*, unsigned long, gl::BufferUsage, unsigned int, gl::BufferStorage, rx::BufferFeedback*)+0x56 (libGLESv2.dylib:x86_64+0x75f8d6)
    #4 0x00011dd6ae50 in gl::Buffer::setDataWithUsageFlags(gl::Context const*, gl::BufferBinding, void*, void const*, unsigned long, gl::BufferUsage, unsigned int, gl::BufferStorage)+0x140 (libGLESv2.dylib:x86_64+0x4a4e50)
    #5 0x00011dd6a812 in gl::Buffer::bufferDataImpl(gl::Context*, gl::BufferBinding, void const*, long, gl::BufferUsage, unsigned int, gl::BufferStorage)+0x1f2 (libGLESv2.dylib:x86_64+0x4a4812)
    #6 0x00011dd6acff in gl::Buffer::bufferData(gl::Context*, gl::BufferBinding, void const*, long, gl::BufferUsage)+0xf (libGLESv2.dylib:x86_64+0x4a4cff)
    #7 0x0001700e0e32 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBufferData(unsigned int, long, void const*, unsigned int)+0xb2 (Chromium Framework:x86_64+0x1ac51e32)
    #8 0x000170153943 in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)+0x1b3 (Chromium Framework:x86_64+0x1acc4943)
    #9 0x00015def21c6 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x576 (Chromium Framework:x86_64+0x8a631c6)
    #10 0x00017029bfaa in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)+0x59a (Chromium Framework:x86_64+0x1ae0cfaa)
    ...
    #36 0x000173328560 in content::GpuMain(content::MainFunctionParams)+0xc10 (Chromium Framework:x86_64+0x1de99560)

0x6060001ea080 is located 0 bytes after 64-byte region [0x6060001ea040,0x6060001ea080)
allocated by thread T0 here:
    #0 0x00010b1a16b2 in __asan_memmove+0x2c22 (libclang_rt.asan_osx_dynamic.dylib:x86_64+0x556b2)
    #1 0x00011f15585a in angle::MemoryBuffer::resize(unsigned long)+0x4a (libGLESv2.dylib:x86_64+0x188f85a)
    #2 0x00011f004c2e in rx::BufferMtl::setDataImpl(gl::Context const*, gl::BufferBinding, void const*, unsigned long, gl::BufferUsage, rx::BufferFeedback*)+0x34e (libGLESv2.dylib:x86_64+0x173ec2e)
    ...

SUMMARY: AddressSanitizer: heap-buffer-overflow (libGLESv2.dylib:x86_64+0x173f00b) in rx::BufferMtl::setSubDataImpl+0x21b

```

The complete untruncated ASAN logs are provided in `asan.log` (Apple Silicon with feature flag) and `asan-intel.log` (Intel Mac, default configuration).

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 26.8 KB)
- [asan-intel.log](attachments/asan-intel.log) (text/plain, 32.1 KB)
- [readme.md](attachments/readme.md) (text/markdown, 3.4 KB)
- [poc.html](attachments/poc.html) (text/html, 8.5 KB)
- [exploit_writeup.md](attachments/exploit_writeup.md) (text/markdown, 21.9 KB)
- [exploit_pc_hijack.html](attachments/exploit_pc_hijack.html) (text/html, 6.2 KB)
- deleted (application/octet-stream, 0 B)
- [exploit_pc_hijack.html](attachments/exploit_pc_hijack_75310436.html) (text/html, 5.1 KB)
- [asan.log](attachments/asan_76136585.log) (text/plain, 17.2 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5621273530925056.

### me...@google.com (2026-03-07)

Thanks for the report. Reproed locally with `--use-angle=metal --enable-angle-features=useShadowBuffersWhenAppropriate`

geofflang@: Could you PTAL?

### 24...@project.gserviceaccount.com (2026-03-07)

Testcase 5621273530925056 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5621273530925056.

### ch...@google.com (2026-03-07)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-03-12)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7656589>

Metal: Use the mtl::Buffer's size when syncing shadow data.

---


Expand for full commit details
```
     
    When syncing data to the shadow copy during a buffer resize calculation, 
    BufferMtl::size will return the previous size of the buffer since it 
    queries the buffer's frontend state. 
     
    Use the size of the actual internal buffer and assert that the shadow 
    buffer has been updated to match already. 
     
    Bug: chromium:489494022 
    Change-Id: Ica3763a3f3ca8e78150295794679b51bba863ca8 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7656589 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Kenneth Russell <kbr@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/BufferMtl.mm`

---

Hash: [7a68f0166454119af163c1e08cd3a6c9e61bc6ee](https://chromiumdash.appspot.com/commit/7a68f0166454119af163c1e08cd3a6c9e61bc6ee)  

Date: Wed Mar 11 19:24:33 2026


---

### dx...@google.com (2026-03-12)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7662487>

Revert "Metal: Use the mtl::Buffer's size when syncing shadow data."

---


Expand for full commit details
```
     
    This reverts commit 7a68f0166454119af163c1e08cd3a6c9e61bc6ee. 
     
    Reason for revert: Assertion failure 
     
    Original change's description: 
    > Metal: Use the mtl::Buffer's size when syncing shadow data. 
    > 
    > When syncing data to the shadow copy during a buffer resize calculation, 
    > BufferMtl::size will return the previous size of the buffer since it 
    > queries the buffer's frontend state. 
    > 
    > Use the size of the actual internal buffer and assert that the shadow 
    > buffer has been updated to match already. 
    > 
    > Bug: chromium:489494022 
    > Change-Id: Ica3763a3f3ca8e78150295794679b51bba863ca8 
    > Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7656589 
    > Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    > Reviewed-by: Kenneth Russell <kbr@chromium.org> 
     
    Bug: chromium:489494022 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I4d367a2fa99aa63eae1c1a9100acb72b951ad240 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7662487 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/BufferMtl.mm`

---

Hash: [1210ebe5f0d393b1abfcb7b67f1af967f0fadb83](https://chromiumdash.appspot.com/commit/1210ebe5f0d393b1abfcb7b67f1af967f0fadb83)  

Date: Thu Mar 12 19:03:56 2026


---

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7663029>

Roll ANGLE from 69360e45f63e to 7a68f0166454 (1 revision)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/69360e45f63e..7a68f0166454 
     
    2026-03-12 geofflang@chromium.org Metal: Use the mtl::Buffer's size when syncing shadow data. 
     
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
    Bug: chromium:489494022 
    Tbr: cnorthrop@google.com 
    Change-Id: I7a2c6cd0b3fb28377d420027f5f73093d9a7e87f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7663029 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1598612}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [c5ee8a8b1a281e37f65c8b4c465988bf557ee531](https://chromiumdash.appspot.com/commit/c5ee8a8b1a281e37f65c8b4c465988bf557ee531)  

Date: Thu Mar 12 19:34:19 2026


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

### dx...@google.com (2026-03-16)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7665314>

Reland "Metal: Use the mtl::Buffer's size when syncing shadow data."

---


Expand for full commit details
```
     
    Move buffer size rounding logic to the common allocation code so that 
    shadow data always matches the size of the Metal buffer. 
     
    This reverts commit 1210ebe5f0d393b1abfcb7b67f1af967f0fadb83. 
     
    Original change's description: 
    > Revert "Metal: Use the mtl::Buffer's size when syncing shadow data." 
    > 
    > This reverts commit 7a68f0166454119af163c1e08cd3a6c9e61bc6ee. 
    > 
    > Reason for revert: Assertion failure 
    > 
    > Original change's description: 
    > > Metal: Use the mtl::Buffer's size when syncing shadow data. 
    > > 
    > > When syncing data to the shadow copy during a buffer resize calculation, 
    > > BufferMtl::size will return the previous size of the buffer since it 
    > > queries the buffer's frontend state. 
    > > 
    > > Use the size of the actual internal buffer and assert that the shadow 
    > > buffer has been updated to match already. 
    > > 
    > > Bug: chromium:489494022 
    > > Change-Id: Ica3763a3f3ca8e78150295794679b51bba863ca8 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7656589 
    > > Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    > > Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    > 
    > Bug: chromium:489494022 
    > No-Presubmit: true 
    > No-Tree-Checks: true 
    > No-Try: true 
    > Change-Id: I4d367a2fa99aa63eae1c1a9100acb72b951ad240 
    > Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7662487 
    > Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    > Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    > Commit-Queue: Geoff Lang <geofflang@chromium.org> 
     
    Bug: chromium:489494022 
    Change-Id: Id1057d578ee80f66c51deae3ceadb511911a3b7f 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7665314 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/BufferMtl.mm`

---

Hash: [74b9ebf704200aeec307b729ae396764638730c9](https://chromiumdash.appspot.com/commit/74b9ebf704200aeec307b729ae396764638730c9)  

Date: Mon Mar 16 14:19:14 2026


---

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7670454>

Roll ANGLE from 8fb26b5fa9d5 to 74b9ebf70420 (4 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/8fb26b5fa9d5..74b9ebf70420 
     
    2026-03-16 geofflang@chromium.org Reland "Metal: Use the mtl::Buffer's size when syncing shadow data." 
    2026-03-16 ynovikov@chromium.org Revert "Suppress regressed dEQP-GLES2 test on Pixel 10 and Galaxy S24" 
    2026-03-16 ynovikov@chromium.org Suppress regressed dEQP-GLES2 test on Pixel 10 and Galaxy S24 
    2026-03-16 lexa.knyazev@gmail.com Vulkan: Allow S3TC formats without the device feature 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC abdolrashidi@google.com,angle-team@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:489494022 
    Tbr: abdolrashidi@google.com 
    Change-Id: I6af51e7bd64f340360d1568a581805cc3ff7c649 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7670454 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1600103}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [6ce4bd42be49f50fd61435137b0bcd486969e0c6](https://chromiumdash.appspot.com/commit/6ce4bd42be49f50fd61435137b0bcd486969e0c6)  

Date: Mon Mar 16 21:01:34 2026


---

### ch...@google.com (2026-03-18)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1600103) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1600103) appears to be after beta branch point (1596535).
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

### ge...@chromium.org (2026-03-18)

> Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/7665314>

> Has this fix been verified on Canary to not pose any stability regressions?

One canary release so far.

> Does this fix pose any potential non-verifiable stability risks?

No

> Does this fix pose any known compatibility risks?

No

> Does it require manual verification by the test team? If so, please describe required testing.

No

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

Link:    <https://chromium-review.googlesource.com/7696623>

M147: Reland "Metal: Use the mtl::Buffer's size when syncing shadow data."

---


Expand for full commit details
```
     
    Move buffer size rounding logic to the common allocation code so that 
    shadow data always matches the size of the Metal buffer. 
     
    This reverts commit 1210ebe5f0d393b1abfcb7b67f1af967f0fadb83. 
     
    Original change's description: 
    > Revert "Metal: Use the mtl::Buffer's size when syncing shadow data." 
    > 
    > This reverts commit 7a68f0166454119af163c1e08cd3a6c9e61bc6ee. 
    > 
    > Reason for revert: Assertion failure 
    > 
    > Original change's description: 
    > > Metal: Use the mtl::Buffer's size when syncing shadow data. 
    > > 
    > > When syncing data to the shadow copy during a buffer resize calculation, 
    > > BufferMtl::size will return the previous size of the buffer since it 
    > > queries the buffer's frontend state. 
    > > 
    > > Use the size of the actual internal buffer and assert that the shadow 
    > > buffer has been updated to match already. 
    > > 
    > > Bug: chromium:489494022 
    > > Change-Id: Ica3763a3f3ca8e78150295794679b51bba863ca8 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7656589 
    > > Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    > > Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    > 
    > Bug: chromium:489494022 
    > No-Presubmit: true 
    > No-Tree-Checks: true 
    > No-Try: true 
    > Change-Id: I4d367a2fa99aa63eae1c1a9100acb72b951ad240 
    > Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7662487 
    > Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    > Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    > Commit-Queue: Geoff Lang <geofflang@chromium.org> 
     
    Bug: chromium:489494022 
    Change-Id: Id1057d578ee80f66c51deae3ceadb511911a3b7f 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7665314 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit 74b9ebf704200aeec307b729ae396764638730c9) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7696623 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

```

---

Files:

- M `src/libANGLE/renderer/metal/BufferMtl.mm`

---

Hash: [1ca27145c44e618dcbff83babd6b6542ce82e5ad](https://chromiumdash.appspot.com/commit/1ca27145c44e618dcbff83babd6b6542ce82e5ad)  

Date: Mon Mar 16 14:19:14 2026


---

### dx...@google.com (2026-03-24)

Project: angle/angle  

Branch:  chromium/7680  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7696622>

M146: Reland "Metal: Use the mtl::Buffer's size when syncing shadow data."

---


Expand for full commit details
```
     
    Move buffer size rounding logic to the common allocation code so that 
    shadow data always matches the size of the Metal buffer. 
     
    This reverts commit 1210ebe5f0d393b1abfcb7b67f1af967f0fadb83. 
     
    Original change's description: 
    > Revert "Metal: Use the mtl::Buffer's size when syncing shadow data." 
    > 
    > This reverts commit 7a68f0166454119af163c1e08cd3a6c9e61bc6ee. 
    > 
    > Reason for revert: Assertion failure 
    > 
    > Original change's description: 
    > > Metal: Use the mtl::Buffer's size when syncing shadow data. 
    > > 
    > > When syncing data to the shadow copy during a buffer resize calculation, 
    > > BufferMtl::size will return the previous size of the buffer since it 
    > > queries the buffer's frontend state. 
    > > 
    > > Use the size of the actual internal buffer and assert that the shadow 
    > > buffer has been updated to match already. 
    > > 
    > > Bug: chromium:489494022 
    > > Change-Id: Ica3763a3f3ca8e78150295794679b51bba863ca8 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7656589 
    > > Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    > > Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    > 
    > Bug: chromium:489494022 
    > No-Presubmit: true 
    > No-Tree-Checks: true 
    > No-Try: true 
    > Change-Id: I4d367a2fa99aa63eae1c1a9100acb72b951ad240 
    > Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7662487 
    > Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    > Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    > Commit-Queue: Geoff Lang <geofflang@chromium.org> 
     
    Bug: chromium:489494022 
    Change-Id: Id1057d578ee80f66c51deae3ceadb511911a3b7f 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7665314 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit 74b9ebf704200aeec307b729ae396764638730c9) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7696622 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

```

---

Files:

- M `src/libANGLE/renderer/metal/BufferMtl.mm`

---

Hash: [5ea435e34885c1eb991c594c378310c98d8cdc53](https://chromiumdash.appspot.com/commit/5ea435e34885c1eb991c594c378310c98d8cdc53)  

Date: Mon Mar 16 14:19:14 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### je...@gmail.com (2026-03-29)

To Chrome VRP:

# Exploitation of BufferMtl Shadow Copy Heap Overflow to PC Hijack in macOS GPU Process

## Summary

The heap buffer overflow in the ANGLE Metal backend's shadow copy synchronization path can be escalated from a memory corruption primitive to a program counter hijack in the GPU process. On macOS the GPU process runs outside the renderer sandbox, so controlling the instruction pointer in this process is equivalent to unsandboxed code execution. The exploit uses only standard WebGL2 API calls from a single HTML page and requires no renderer or browser process code modifications. On the tested configuration (macOS ARM64, Chromium Release build), the exploit overwrites `gl::Buffer` objects with the attacker-controlled pattern `0x4141414141414141`, causing a `SEGV_ACCERR` at address `0x41414141414150` when the GPU process dereferences a corrupted pointer during virtual method dispatch. The GPU process crashes on every attempt; approximately 20-40% of runs produce the controlled-address crash.

## Exploit Primitive

The vulnerability provides a linear heap overflow whose size and content are both attacker-controlled. The overflow destination is the PartitionAlloc heap (where `MemoryBuffer::reserve` calls `malloc`), and the overflow source is Metal's unified memory (the `MTLBuffer` mapped pointer returned by `mapReadOnly`). The vulnerable memcpy in `ensureShadowCopySyncedFromGPU` copies `size()` bytes, which returns the stale `mState.mSize` value from the GL frontend, into the freshly resized `mShadowCopy` buffer:

```
// third_party/angle/src/libANGLE/renderer/metal/BufferMtl.mm
void BufferMtl::ensureShadowCopySyncedFromGPU(ContextMtl *contextMtl)
{
    if (mBuffer->isCPUReadMemDirty())
    {
        const uint8_t *ptr = mBuffer->mapReadOnly(contextMtl);
        memcpy(mShadowCopy.data(), ptr, size());  // size() returns stale mState.mSize
        ...
    }
}

```

At this point `mShadowCopy` has been resized to the new (smaller) `adjustedSize` by `setDataImpl`, but `mState.mSize` still holds the old (larger) value because `gl::Buffer::bufferDataImpl` updates it only after `setDataImpl` returns:

```
// third_party/angle/src/libANGLE/Buffer.cpp
ANGLE_TRY(setDataWithUsageFlags(context, target, nullptr, dataForImpl, size, usage, flags,
                                bufferStorage));
// ...
mState.mSize = size;  // updated AFTER setData returns

```

The overflow writes `mState.mSize - adjustedSize` bytes beyond the shadow copy allocation. Because the shadow copy is allocated via `malloc` inside `MemoryBuffer::reserve`, the overflow corrupts adjacent objects in the PartitionAlloc heap.

## Stage 1: Controlling Overflow Content via Metal Sub-Allocation Heap Spray

The attacker does not directly control the bytes written beyond the Metal buffer's size. The content that overflows past the shadow copy comes from whatever occupies the virtual memory immediately following the source Metal buffer. Controlling this content is the first challenge.

Metal's buffer allocator on Apple Silicon exhibits size-dependent allocation granularity. For allocations below 464 bytes, each `MTLBuffer` created via `[device newBufferWithLength:options:]` receives a dedicated VM page (16 KB on ARM64 macOS); the trailing bytes within that page are zero-filled. For allocations of 464 bytes or larger, Metal sub-allocates multiple buffers within shared pages, placing them at consecutive addresses separated by a 32-byte internal header. This threshold was determined empirically by testing buffer sizes from 256 to 512 in 16-byte increments.

The exploit creates 200 WebGL buffers of 480 bytes, each filled with the pattern `0x4141414141414141` via `gl.bufferData`. Each `bufferData` call reaches `BufferMtl::setDataImpl`, which calls `allocateNewMetalBuffer`:

```
// third_party/angle/src/libANGLE/renderer/metal/BufferMtl.mm
ANGLE_TRY(allocateNewMetalBuffer(contextMtl, storageMode, adjustedSize,
                                 /*returnOldBufferImmediately=*/true, feedback));

```

Inside `allocateNewMetalBuffer`, the `BufferManager::getBuffer` call either reuses a cached buffer from the free list or creates a new `MTLBuffer` via `Buffer::MakeBufferWithStorageMode`. For 480-byte buffers, Metal sub-allocates them within shared pages, producing a layout of consecutive 480-byte data regions separated by 32-byte headers:

```
Metal heap page (16 KB):
  [spray[0] data: 480B of 0x41][header: 32B][spray[1] data: 480B of 0x41][header: 32B]...

```

When one of these spray buffers is later recycled as the trigger's Metal buffer, reading beyond its 480-byte boundary with `mapReadOnly` returns the 32-byte header followed by the adjacent spray buffer's data, both of which reside within the same mapped page. The attacker's `0x4141414141414141` pattern appears in the overflow source starting at offset `480 + 32 = 512` from the Metal buffer's base.

## Stage 2: Making the Recycled Metal Buffer Dirty

The overflow path is gated on `mBuffer->isCPUReadMemDirty()`. This flag is set when a Metal buffer is the target of a GPU write operation. The `Resource::setUsedByCommandBufferWithQueueSerial` method sets it during blit encoding:

```
// third_party/angle/src/libANGLE/renderer/metal/mtl_resources.mm
void Resource::setUsedByCommandBufferWithQueueSerial(uint64_t serial, bool writing, ...)
{
    if (writing)
    {
        mUsageRef->cpuReadMemNeedSync = true;
        mUsageRef->cpuReadMemDirty    = true;
    }
    ...
}

```

The exploit creates this condition by binding a spray buffer as a vertex buffer, issuing a draw call (which marks it as referenced by the render encoder), then calling `gl.copyBufferSubData` to copy data into it. Because the buffer is being used by the GPU when the copy is requested, ANGLE takes the blit path, encoding a `MTLBlitCommandEncoder::copyFromBuffer` that writes to the buffer and sets `cpuReadMemDirty = true`.

After the blit, the exploit must ensure the Metal buffer is no longer considered in-use by the GPU before returning it to the `BufferManager` free list. `BufferManager::returnBuffer` checks `isBeingUsedByGPU` and routes the buffer accordingly:

```
// third_party/angle/src/libANGLE/renderer/metal/mtl_buffer_manager.mm
void BufferManager::returnBuffer(ContextMtl *contextMtl, BufferRef &bufferRef)
{
    ...
    if (bufferRef->isBeingUsedByGPU(contextMtl))
    {
        mInUseBuffers.push_back(bufferRef);   // NOT immediately available
    }
    else
    {
        addBufferRefToFreeLists(bufferRef);   // available for recycling
    }
}

```

If the buffer goes to `mInUseBuffers`, it will not be found by `getBuffer` until a later `freeUnusedBuffers` call moves it. The exploit calls `gl.finish()` followed by `gl.readPixels()` to force all GPU command buffers to complete and update the completion serial. This ensures that `isBeingUsedByGPU` returns false at the time of `returnBuffer`, placing the dirty buffer directly into `mFreeBuffers` where it is indexed by size for exact-match lookup:

```
// third_party/angle/src/libANGLE/renderer/metal/mtl_buffer_manager.mm
void BufferManager::addBufferRefToFreeLists(mtl::BufferRef &bufferRef)
{
    int cacheIndex = storageModeToCacheIndex(bufferRef->storageMode());
    mFreeBuffers[cacheIndex].insert(BufferMap::value_type(bufferRef->size(), bufferRef));
}

```

The resize operation that follows (`gl.bufferData(poisonBuf, 1, gl.STATIC_DRAW)`) triggers `allocateNewMetalBuffer` inside `setDataImpl`, which calls `returnBuffer` on the old 480-byte dirty buffer and then allocates a new 16-byte buffer. The dirty 480-byte buffer now sits in the free list, retaining its `cpuReadMemDirty = true` flag because neither `returnBuffer` nor `addBufferRefToFreeLists` calls `resetCPUReadMemDirty`.

## Stage 3: Fresh Shadow Copy Allocation via Capacity Reset

The overflow magnitude equals `size() - mShadowCopy.size()`. A large overflow requires a fresh `malloc` for the shadow copy (so the allocation is small) while `mState.mSize` retains a large value from a previous `bufferData` call. The `MemoryBuffer::reserve` function only allocates new memory when the requested capacity exceeds the current capacity:

```
// third_party/angle/src/common/MemoryBuffer.cpp
bool MemoryBuffer::reserve(size_t newCapacity)
{
    if (newCapacity <= mCapacity)
    {
        return true;  // no reallocation
    }
    uint8_t *newMemory = static_cast<uint8_t *>(malloc(newCapacity));
    ...
}

```

If the trigger buffer previously held a shadow copy (from an earlier `bufferData` with a small size), the capacity would already be large enough to accommodate the new size, and no fresh `malloc` would occur. The exploit avoids this by making the trigger buffer's first `bufferData` call large enough to disable shadow copies entirely.

The shadow copy is disabled when `adjustedSize > kSharedMemBufferMaxBufSizeHint` (262144 bytes). The exploit calls `bufferData(trigger, 262145)`, producing `adjustedSize = roundUpPow2(262145, 16) = 262160 > 262144`. The shadow size computation in `setDataImpl` yields zero:

```
// third_party/angle/src/libANGLE/renderer/metal/BufferMtl.mm
size_t shadowSize = (!features.preferCpuForBuffersubdata.enabled &&
                     features.useShadowBuffersWhenAppropriate.enabled &&
                     adjustedSize <= mtl::kSharedMemBufferMaxBufSizeHint)
                        ? adjustedSize
                        : 0;  // disabled: adjustedSize (262160) > 262144
ANGLE_CHECK_GL_ALLOC(contextMtl, mShadowCopy.resize(shadowSize));  // resize(0)

```

The `resize(0)` call sets `mSize = 0` but does not free the underlying buffer or reset `mCapacity`. Because the trigger buffer was freshly created (never had a shadow copy), `mCapacity` is still its initial value of zero. When the subsequent `bufferData(trigger, new Uint8Array(480))` enables the shadow copy, `reserve(480)` finds `480 > 0` and executes a fresh `malloc(480)`. Meanwhile, `size()` returns `mState.mSize = 262145` from the previous call, producing an overflow of `262145 - 480 = 261665` bytes.

## Stage 4: PartitionAlloc Bucket Collision and Heap Feng Shui

PartitionAlloc-Everywhere, the default allocator in Chromium Release builds, segregates allocations by size class into slot spans. Objects in different size classes reside in physically separate memory regions, so the overflow from a 480-byte shadow copy can only corrupt objects in the same PA bucket. In PA-Everywhere mode, both `malloc` (used by `MemoryBuffer::reserve`) and `operator new` (used to create `gl::Buffer` instances) route through the same partition root, so allocations of the same size class share slot spans regardless of the allocation API.

The target victim object is `gl::Buffer`, which is 456 bytes on ARM64. PA groups both 456-byte and 480-byte allocations into the same bucket (the exponential distribution for order 9 produces bucket boundaries at 448 and 480; both sizes fall at or below the 480 boundary). Each WebGL `gl.createBuffer()` followed by `gl.bufferData(480B)` produces two allocations in the same bucket: the `gl::Buffer` instance (456 bytes via `operator new` inside the GL layer) and the shadow copy data (480 bytes via `malloc` inside `MemoryBuffer::reserve`). These interleave within the same slot span:

```
PA slot span (bucket 480):
  [gl::Buffer_0 (456B)][ShadowData_0 (480B)][gl::Buffer_1][ShadowData_1]...

```

The exploit creates 300 filler buffers to populate several slot spans with these interleaved pairs, then deletes `filler[150]`. The deletion frees both the filler's `gl::Buffer` (via `operator delete`) and its shadow copy data (via `free` inside `MemoryBuffer::destroy`). Both freed slots enter the PA thread-local cache, which returns slots in LIFO order. The trigger's subsequent `malloc(480)` inside `mShadowCopy.resize` pops one of these freed slots, placing the trigger's shadow copy data at a position surrounded by live `gl::Buffer` objects in the filled slot span.

## Stage 5: Overflow and vtable Corruption

When the trigger's `bufferData(new Uint8Array(480))` reaches `setSubDataImpl`, the code path enters `updateShadowCopyThenCopyShadowToNewBuffer`, which calls `ensureShadowCopySyncedFromGPU`:

```
// third_party/angle/src/libANGLE/renderer/metal/BufferMtl.mm
angle::Result BufferMtl::updateShadowCopyThenCopyShadowToNewBuffer(...)
{
    ensureShadowCopySyncedFromGPU(contextMtl);        // overflow happens here
    std::copy(srcPtr, srcPtr + sizeToCopy, ...);       // write client data
    return commitShadowCopy(contextMtl, feedback);     // copy to new Metal buffer
}

```

Inside `ensureShadowCopySyncedFromGPU`, the recycled Metal buffer's `cpuReadMemDirty` flag is true, so the memcpy executes with `size() = 262145` and `mShadowCopy.size() = 480`. The 261665 bytes of overflow blast through hundreds of adjacent PA slots. The overflow content, sourced from the Metal sub-allocation heap spray, consists of alternating 32-byte Metal headers (zeros) and 480-byte spray buffer data (`0x4141414141414141`).

When the overflow reaches a live `gl::Buffer` object in the same slot span, the first 8 bytes of the object (the vtable pointer, inherited from `angle::Subject`) are overwritten. If the vtable offset aligns with a spray data region rather than a Metal header, the vtable pointer becomes `0x4141414141414141`. If it aligns with a Metal header, the vtable pointer becomes zero (NULL).

## Stage 6: Crash via Corrupted Object Dereference

The 261665-byte overflow writes attacker-controlled `0x4141414141414141` data across hundreds of adjacent PA slots. These slots contain a mixture of shadow copy data buffers and `gl::Buffer` C++ objects whose member fields include vtable pointers (from `angle::Subject`), `mImpl` pointers (type `rx::BufferImpl*`), reference counts, and observer lists. The overflow replaces all of these fields with the `0x41` pattern.

The crash does not require a separate trigger step. The overflow occurs inside `ensureShadowCopySyncedFromGPU`, which is called from `updateShadowCopyThenCopyShadowToNewBuffer`. After the memcpy returns, this function continues to `commitShadowCopy`, which calls `allocateNewMetalBuffer` and interacts with the `BufferManager`. These operations traverse data structures in the same PA heap region that was just corrupted. When any code path dereferences a pointer field of a corrupted `gl::Buffer` (whether the vtable pointer at offset 0, the `mImpl` pointer, or an internal observer list entry), the CPU attempts to load from an address derived from the `0x4141414141414141` pattern:

```
Received signal 11 SEGV_ACCERR 41414141414150

```

The crash address `0x41414141414150` is characteristic of a pointer dereference chain through `0x41`-filled memory. The entire `gl::Buffer` object has been overwritten, so any member access produces an address within the `0x4141414141414141` region. The specific offset (`0x50 - 0x41 = 0xF`) depends on which member pointer is dereferenced first and at what struct offset; this varies between runs based on PA slot alignment.

The exploit additionally iterates remaining filler buffers via `gl.bufferSubData` to increase the probability of hitting a corrupted object. In `gl::Buffer::bufferSubData`, the call `mImpl->setSubData()` dereferences the corrupted `mImpl` pointer, which also triggers a fault at an attacker-derived address.

Across 20 test runs, six (30%) crashed at `0x41414141414150`, confirming that the attacker-controlled pattern was present at the faulting address. The remaining runs crashed at NULL+offset (vtable zeroed by Metal header bytes), at PA guard pages (memcpy reached slot span boundary), or at other partially corrupted addresses.

## Reliability

A 32-byte Metal allocator header separates sub-allocated buffers within a shared page. When this header aligns with the `gl::Buffer` vtable offset in the overflow stream, the vtable is overwritten with zeros rather than the spray pattern, producing a NULL dereference (crash at method offset, such as `0x10` or `0x50`) instead of the controlled-address crash. This alignment depends on Metal's internal heap state and varies between runs. Across test runs on macOS ARM64 (Apple M3 Max) in the default multi-process configuration, approximately 20-40% produce `SEGV at 0x41414141414150` (PC hijack), and the remainder crash at NULL+offset or hit the PartitionAlloc guard page. The GPU process crashes on every run.

## Reproduce

Tested on Chromium at commit `d0f83d769eeed` (March 2026) on macOS ARM64. The vulnerability was fixed in ANGLE commit `74b9ebf704` ("Reland: Metal: Use the mtl::Buffer's size when syncing shadow data"), which replaced the stale `size()` call with `mBuffer->size()` and moved the buffer size rounding logic into `allocateNewMetalBuffer` to ensure the shadow copy size always matches the Metal buffer size. The exploit requires reverting this fix:

Release build configuration (`out/release/args.gn`):

```
is_debug = false
dcheck_always_on = false
target_cpu = "arm64"

```
```
cd ~/chromium/src/third_party/angle
git revert --no-commit 74b9ebf704
cd ~/chromium/src
ninja -C out/release chrome

```
```
./out/release/Chromium.app/Contents/MacOS/Chromium \
  --use-angle=metal \
  --enable-angle-features=useShadowBuffersWhenAppropriate,alwaysUseSharedStorageModeForBuffers \
  --user-data-dir=/tmp/exploit-$(date +%s) \
  --enable-logging=stderr --no-first-run --disable-default-apps \
  "file://$(pwd)/issue_angl076/exploit_pc_hijack.html" \
  2>&1 | grep -E "Received signal|GPU process"

```

The GPU process crashes within seconds of page load. On Intel Macs where `useShadowBuffersWhenAppropriate` is natively enabled, the `--enable-angle-features` flag is unnecessary.

Release multi-process output (PC hijack in GPU process):

```
Received signal 11 SEGV_ACCERR 41414141414150
 [0x00012061b338]
 [0x00012060e290]
 [0x00012061b28c]
 [0x00019a9396a4]
 [0x00010638f4b8]
 [0x000106357f08]
 [0x000105e02070]
 [0x0001223da9f8]
 [0x0001223f9a38]
 [0x00011d6c660c]
 [0x00012245a6d8]
 [0x00012245a390]
 [0x00012246301c]
 [0x000122465dcc]
 [0x000122465d58]
 [0x00011ba429f0]
 [0x00011d6cbf18]
 [0x00011d6cb600]
 [0x0001205b7de4]
 [0x0001205d44b0]
 [0x0001205d4074]
 [0x000120626208]
 [0x0001206216b8]
 [0x000120625964]
 [0x00019a9eab14]
[end of stack trace]

GPU process exited unexpectedly: exit_code=11
The GPU process has crashed 1 time(s)
WebGL: CONTEXT_LOST_WEBGL: loseContext: context lost

```
## Path to Full RCE

### Intel Mac: direct exploitation without mitigations

On Intel Macs, the vulnerability is natively reachable without any command-line flags. `DisplayMtl.mm` gates `useShadowBuffersWhenAppropriate` on `isIntel()`, which returns true for all Intel integrated GPUs. The Metal backend is the default ANGLE backend on these systems. The shadow copy code path executes on every `bufferData` call for buffers up to 256 KB, making the vulnerability trivially triggerable from any webpage that uses WebGL.

Intel Macs lack Pointer Authentication (PAC), which is an ARM64-only feature. With PAC absent, neither return addresses on the stack nor function pointers in data structures carry authentication codes. Once the vtable pointer of a `gl::Buffer` is overwritten, the corrupted virtual dispatch jumps directly to the attacker-specified address without any integrity check. This eliminates the need for a PAC bypass and reduces the exploit to a straightforward vtable hijack.

Furthermore, on x86-64 macOS, all processes within the same user session share the same ASLR slide for a given dylib. The renderer process (which the attacker controls in the compromised-renderer threat model, or from which the attacker can read arbitrary memory via a separate renderer bug) loads the same `libGLESv2.dylib` at the same base address as the GPU process. The attacker reads the library base from the renderer's own address space, computes the absolute addresses of gadgets and API functions, and embeds them directly into the spray payload. When the spray data overwrites the victim `gl::Buffer` in the GPU process, the fake vtable entries already contain correct absolute addresses.

The Intel Mac exploit path therefore proceeds as follows. The attacker uses `gl.bufferSubData` to write a fake vtable into a Metal buffer whose virtual address is known (Metal shared-storage buffers are CPU-addressable; the attacker can determine the address by correlating the `MTLBuffer` pointer with the buffer's GPU-visible address, or by spraying fake vtables across many buffers and accepting a probabilistic hit). The fake vtable's method entries point to a stack-pivot gadget in `libGLESv2.dylib` or `Chromium Framework`. The stack pivot redirects `rsp` to a second Metal buffer containing a ROP chain. The ROP chain calls `system("open -a Calculator")` or equivalent via `dlsym`-resolved libc addresses. Because the GPU process on macOS is not sandboxed, `system()` executes with full user privileges.

### ARM64 Mac: additional steps required

On ARM64, PAC signs return addresses stored on the stack, preventing conventional ROP without a PAC bypass or a signing oracle. The vtable pointer itself is not PAC-protected in standard Chromium builds (ANGLE is compiled without `-fptrauth-vtable-pointer-*`), so the initial vtable hijack works identically to Intel. The challenge is executing a useful code sequence after gaining control of a single indirect call.

Converting the single indirect call to arbitrary code execution on ARM64 requires one of the following approaches. A JOP (Jump-Oriented Programming) chain constructed entirely from indirect branches avoids the need to forge PAC-signed return addresses. Alternatively, a PAC signing gadget within the Chromium binary (a code sequence that signs an attacker-supplied pointer using a predictable key/context) can be used to forge valid return addresses, enabling a conventional ROP chain. The `paciza` instruction with a zero-context modifier is sometimes present in large binaries and acts as an unconditional signing oracle.

ASLR bypass on ARM64 macOS follows the same approach as Intel: the overflow corrupts adjacent shadow copy data in the same PA slot span, and the corrupted data can be read back to the renderer via `gl.getBufferSubData`. If the corrupted region overlaps with a freed `gl::Buffer` whose memory has been partially reclaimed (containing heap metadata or vtable pointers from a prior occupant), the read-back reveals code-segment addresses from which the library base can be computed.

### gm...@google.com (2026-04-03)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-04-03)

1. Two CLs: <https://chromium-review.git.corp.google.com/c/angle/angle/+/7727162> (this one as a dependency of the other - which is also being tracked in <https://buganizer.corp.google.com/issues/489585044>) and <https://chromium-review.git.corp.google.com/c/angle/angle/+/7726650> (this is the actual fix)
2. Low - there are no conflicts
3. 146 and 147 (note that the first CL is tracked
4. Yes. This is relevant, specially since the introducing commit `968041b547` dates back 2022.

### an...@google.com (2026-04-03)

Merge approved for LTS-138

### je...@gmail.com (2026-04-08)

deleted

### je...@gmail.com (2026-04-08)

I was testing an exploit for another vulnerability, so I tried the exploit on cdd1f63c02a65c37ccdb85e85b25dbec456c9914.

The current test success rate is approximately between 30% and 50%.

## Environment

- **Chromium commit**: `cdd1f63c02a65` (Roll ANGLE from a8b99447d3bd to f187d4338681)
- **ANGLE commit**: `f187d4338681` (Refactor GetProgramivRobust validation)
- **OS**: macOS ARM64 (Apple Silicon)
- **Build**: Release

## args.gn

```
is_debug = false
dcheck_always_on = false

```
## Build

```
ninja -C out/release chrome

```
## Reproduce

```
./out/release/Chromium.app/Contents/MacOS/Chromium \
  --use-angle=metal \
  --enable-angle-features=useShadowBuffersWhenAppropriate,alwaysUseSharedStorageModeForBuffers \
  --user-data-dir=/tmp/exploit-$(date +%s) \
  --enable-logging=stderr --no-first-run --disable-default-apps \
  "file://$(pwd)/issue_angl076/exploit_pc_hijack.html" \
  2>&1 | grep -E "Received signal|GPU process"

```
## Expected Output

GPU process crashes within seconds. Approximately 90% crash rate, ~50% with attacker-controlled PC:

```
Received signal 11 SEGV_ACCERR 41414141414150
GPU process exited unexpectedly: exit_code=11
The GPU process has crashed 1 time(s)
WebGL: CONTEXT_LOST_WEBGL: loseContext: context lost

```

Crash address `0x41414141414150` is derived from the attacker-controlled vtable pointer `0x4141414141414141`.

## Notes

- The vulnerability exists in ANGLE's Metal backend at this commit — the fix (`74b9ebf704`) has not been rolled into Chromium yet, so no revert is needed.
- `useShadowBuffersWhenAppropriate` is enabled by default on Intel Macs (`isIntel()` check in `DisplayMtl.mm`). On Apple Silicon it must be enabled via `--enable-angle-features`.
- The GPU process on macOS runs outside the renderer sandbox.

### sp...@google.com (2026-04-10)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $16000.00 for this report.

Rationale for this decision:
High quality with bisect. Sandbox escape / Memory corruption in a non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### aj...@chromium.org (2026-04-11)

Sending back to panel as an exploit was added in comment 25.

### dx...@google.com (2026-04-14)

Project: angle/angle  

Branch:  chromium/7204  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7726650>

[M138-LTS] Reland "Metal: Use the mtl::Buffer's size when syncing shadow data."

---


Expand for full commit details
```
     
    Move buffer size rounding logic to the common allocation code so that 
    shadow data always matches the size of the Metal buffer. 
     
    This reverts commit 1210ebe5f0d393b1abfcb7b67f1af967f0fadb83. 
     
    Original change's description: 
    > Revert "Metal: Use the mtl::Buffer's size when syncing shadow data." 
    > 
    > This reverts commit 7a68f0166454119af163c1e08cd3a6c9e61bc6ee. 
    > 
    > Reason for revert: Assertion failure 
    > 
    > Original change's description: 
    > > Metal: Use the mtl::Buffer's size when syncing shadow data. 
    > > 
    > > When syncing data to the shadow copy during a buffer resize calculation, 
    > > BufferMtl::size will return the previous size of the buffer since it 
    > > queries the buffer's frontend state. 
    > > 
    > > Use the size of the actual internal buffer and assert that the shadow 
    > > buffer has been updated to match already. 
    > > 
    > > Bug: chromium:489494022 
    > > Change-Id: Ica3763a3f3ca8e78150295794679b51bba863ca8 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7656589 
    > > Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    > > Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    > 
    > Bug: chromium:489494022 
    > No-Presubmit: true 
    > No-Tree-Checks: true 
    > No-Try: true 
    > Change-Id: I4d367a2fa99aa63eae1c1a9100acb72b951ad240 
    > Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7662487 
    > Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    > Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    > Commit-Queue: Geoff Lang <geofflang@chromium.org> 
     
    Bug: chromium:489494022 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7665314 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit 74b9ebf704200aeec307b729ae396764638730c9) 
    Change-Id: I654d054e493399120e0d2446414e291083ad8e65 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7726650 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com>

```

---

Files:

- M `src/libANGLE/renderer/metal/BufferMtl.mm`

---

Hash: [4664989d810d3614c0af32933ba28e10a949b420](https://chromiumdash.appspot.com/commit/4664989d810d3614c0af32933ba28e10a949b420)  

Date: Mon Mar 16 14:19:14 2026


---

### el...@google.com (2026-04-29)

PoC from #25 at Chromium d0f83d769eeed0b61ffc7d3c15172b2c257acf4e on macOS 26.4:

```
$ out/rel/Chromium.app/Contents/MacOS/Chromium --use-angle=metal --enable-angle-features=useShadowBuffersWhenAppropriate,alwaysUseSharedStorageModeForBuffers --enable-logging=stderr

```

results in a GPU process ASAN crash with an OOB write so I can confirm this exploit works. ASAN dump attached.

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $61000.00 for this report.

Rationale for this decision:
GPU controlled write + renderer bonus, does not demonstrate functional exploit. Sorry we missed things the first time!


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### vi...@google.com (2026-05-06)

(manually posting and adjusting label to `LTS-Merge-Review-144` as the bot didn't seem to caught my request)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-06)

1. <https://chromium-review.git.corp.google.com/c/angle/angle/+/7808513> and <https://chromium-review.git.corp.google.com/c/angle/angle/+/7819074>
2. Low - there are no conflicts
3. 138, 146 and 147
4. Yes

### dx...@google.com (2026-05-13)

Project: angle/angle  

Branch:  chromium/7559  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7819074>

[M144-LTS] Reland "Metal: Use the mtl::Buffer's size when..."

---


Expand for full commit details
```
     
    Move buffer size rounding logic to the common allocation code so that 
    shadow data always matches the size of the Metal buffer. 
     
    This reverts commit 1210ebe5f0d393b1abfcb7b67f1af967f0fadb83. 
     
    Original change's description: 
    > Revert "Metal: Use the mtl::Buffer's size when syncing shadow data." 
    > 
    > This reverts commit 7a68f0166454119af163c1e08cd3a6c9e61bc6ee. 
    > 
    > Reason for revert: Assertion failure 
    > 
    > Original change's description: 
    > > Metal: Use the mtl::Buffer's size when syncing shadow data. 
    > > 
    > > When syncing data to the shadow copy during a buffer resize calculation, 
    > > BufferMtl::size will return the previous size of the buffer since it 
    > > queries the buffer's frontend state. 
    > > 
    > > Use the size of the actual internal buffer and assert that the shadow 
    > > buffer has been updated to match already. 
    > > 
    > > Bug: chromium:489494022 
    > > Change-Id: Ica3763a3f3ca8e78150295794679b51bba863ca8 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7656589 
    > > Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    > > Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    > 
    > Bug: chromium:489494022 
    > No-Presubmit: true 
    > No-Tree-Checks: true 
    > No-Try: true 
    > Change-Id: I4d367a2fa99aa63eae1c1a9100acb72b951ad240 
    > Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7662487 
    > Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    > Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    > Commit-Queue: Geoff Lang <geofflang@chromium.org> 
     
    Bug: chromium:489494022 
    Reviewed-on: 
    https://chromium-review.googlesource.com/c/angle/angle/+/7665314 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    (cherry picked from commit 74b9ebf704200aeec307b729ae396764638730c9) 
    Change-Id: I08460ccd5d876f7d4be9bddae330e07de362b197 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7819074 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/BufferMtl.mm`

---

Hash: [83f72efb014066929bfced84d02220a86af0b514](https://chromiumdash.appspot.com/commit/83f72efb014066929bfced84d02220a86af0b514)  

Date: Mon Mar 16 14:19:14 2026


---

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489494022)*
