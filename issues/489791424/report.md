# Integer overflow in ANGLE D3D11 streaming vertex buffer leads to massive heap OOB write in the GPU process on Windows

| Field | Value |
|-------|-------|
| **Issue ID** | [489791424](https://issues.chromium.org/issues/489791424) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | je...@gmail.com |
| **Assignee** | sh...@google.com |
| **Created** | 2026-03-05 |
| **Bounty** | $3,000.00 |

## Description

# Integer overflow in ANGLE D3D11 streaming vertex buffer leads to massive heap OOB write in the GPU process

## Summary

ANGLE's D3D11 backend computes the space to reserve in a streaming vertex buffer and the number of elements to copy using two inconsistent formulas when processing instanced draw calls with a non-zero `baseInstance`. By choosing a `baseInstance` close to 2^32, an attacker can cause unsigned 32-bit wrap in the reservation path while the copy path operates on a 64-bit accumulator, resulting in a heap buffer overflow of approximately 64 GB past a 768-byte allocation. A secondary defense in `VertexDataManager::reserveSpaceForAttrib` that validates the source buffer size is also defeated through an unsigned-to-signed truncation of the same `baseInstance` value. The crash occurs in the GPU process on Windows with the D3D11 backend (the default ANGLE backend on Windows), reachable from a compromised renderer via the `WEBGL_draw_instanced_base_vertex_base_instance` WebGL2 extension. The extension is gated behind a draft extension check in the renderer process, but since the vulnerability is in the GPU process, a compromised renderer can trivially bypass this gate.

## Bisect

Introducing Commit: `e61245008e7b1a152b31a1ee34f631203130d384`

- Date: 2020-06-15
- Author: shrekshao ([shrekshao@google.com](mailto:shrekshao@google.com))
- Review: <https://chromium-review.googlesource.com/c/angle/angle/+/2227022>

## Root Cause

Three integer arithmetic errors combine to produce this vulnerability. They all stem from the same commit that added `baseInstance` support to ANGLE's D3D11 streaming vertex translation path.

The first error is in `Renderer11::getVertexSpaceRequired`, which computes how many bytes to reserve in the streaming vertex buffer. For instanced attributes, the element count is calculated as:

```
// src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp
elementCount =
    UnsignedCeilDivide(static_cast<unsigned int>(instances + baseInstance), divisor);

```

Both `instances` (a `GLsizei`, i.e. signed 32-bit) and `baseInstance` (a `GLuint`, i.e. unsigned 32-bit) are added together and the result is truncated to `unsigned int` before the division. When `baseInstance` is 0xFFFFFF00 and `instances` is 300, the sum is 0x10000002C, which wraps to 44 after truncation. The function therefore reports that only 44 elements (704 bytes for `vec4` floats) need to be reserved.

The second error is in `StreamingVertexBufferInterface::storeDynamicAttribute`, which computes how many elements to actually copy into that buffer:

```
// src/libANGLE/renderer/d3d/VertexBuffer.cpp
size_t adjustedCount = count;
GLuint divisor       = binding.getDivisor();

if (instances != 0 && divisor != 0)
{
    adjustedCount += UnsignedCeilDivide(baseInstance, divisor);
}

```

Here `adjustedCount` is a `size_t` (64-bit on x64), and `UnsignedCeilDivide(0xFFFFFF00, 1)` returns 0xFFFFFF00, so `adjustedCount` becomes 300 + 4,294,967,040 = 4,294,967,340. The subsequent call to `VertexBuffer11::storeVertexAttributes` passes this count to `CopyNativeVertexData`, which runs a memcpy-based loop that immediately overflows the 704-byte reservation.

The third error is in `VertexDataManager::reserveSpaceForAttrib`, which attempts to validate the source buffer before copying. It computes the first vertex index for instanced attributes:

```
// src/libANGLE/renderer/d3d/VertexDataManager.cpp
GLint firstVertexIndex = binding.getDivisor() > 0
                             ? UnsignedCeilDivide(baseInstance, binding.getDivisor())
                             : start;
int64_t maxVertexCount =
    static_cast<int64_t>(firstVertexIndex) + static_cast<int64_t>(totalCount);

```

`UnsignedCeilDivide` returns `GLuint` (unsigned 32-bit), but the result is stored in `GLint` (signed 32-bit). When `baseInstance` is 0xFFFFFF00 and `divisor` is 1, the return value 0xFFFFFF00 is reinterpreted as -256 in the signed domain. This makes `maxVertexCount` equal to -256 + 300 = 44, and the subsequent `maxByte <= bufferSize` check passes trivially when the source buffer has at least 44 elements.

A potential validation exists in `ValidateDrawInstancedAttribs` in `validationES.h`, which checks whether `baseInstance` exceeds the instanced vertex element limit. However, this validation is gated on `context->isBufferAccessValidationEnabled()`, which is set to false when the backend supports `GL_KHR_robust_buffer_access_behavior`. The D3D11 backend advertises this extension, so the validation is skipped entirely. The hardware-level robust access only guards D3D11 GPU reads, not ANGLE's CPU-side streaming buffer copies that precede the actual draw call.

## Reproduce

This vulnerability affects Windows systems using the ANGLE D3D11 backend (the default on Windows). It crashes the GPU process via an integer overflow in ANGLE's streaming vertex buffer translation, triggered through the `WEBGL_draw_instanced_base_vertex_base_instance` WebGL2 extension. The extension is gated behind a draft extension check in the renderer process; since the bug is in the GPU process, the attached `patch.diff` removes this renderer-side gate under the compromised renderer threat model.

Tested on commit `4e910e2277470c4576177b37937569fa4151abdc`.

### Build

Check out the tested commit and apply the renderer patch:

```
cd D:\chromium\src
git checkout 4e910e2277470c4576177b37937569fa4151abdc
git apply patch.diff

```

Configure an ASAN build by placing the following in `D:\chromium\src\out\asan-release\args.gn`:

```
is_asan = true
is_debug = false
is_component_build = false
symbol_level = 1
dcheck_always_on = false
use_remoteexec = true

```

Then build Chrome:

```
autoninja -C D:\chromium\src\out\asan-release chrome

```
### Run

Set the ASAN options environment variable and launch Chrome, pointing it at the attached `poc.html`:

```
set ASAN_OPTIONS=detect_odr_violation=0
D:\chromium\src\out\asan-release\chrome.exe --enable-logging=stderr --no-first-run --user-data-dir=%TEMP%\poc-angl008 poc.html

```

The GPU process will crash within seconds. ASAN reports a `heap-buffer-overflow` in `rx::CopyNativeVertexData<float,4,4,0>` at `copyvertex.inc.h`, with a read of approximately 64 GB past the end of a 768-byte heap buffer. The full ASAN trace is provided in `asan.log`.

### ASAN Output

```
=================================================================
==1944==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x116a3688ca00 at pc 0x7ffaf208b36c bp 0x0032075fd4b0 sp 0x0032075fd4f8
READ of size 68719477440 at 0x116a3688ca00 thread T0
    #0 0x7ffaf208b36b in _asan_memcpy+0x25b (D:\chromium\src\out\asan-release\clang_rt.asan_dynamic-x86_64.dll+0x18004b36b)
    #1 0x7ffaee711956 in rx::CopyNativeVertexData<float,4,4,0> D:\chromium\src\third_party\angle\src\libANGLE\renderer\copyvertex.inc.h:69
    #2 0x7ffaeed4efcf in rx::VertexBuffer11::storeVertexAttributes D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexBuffer11.cpp:133
    #3 0x7ffaeee0bd9f in rx::StreamingVertexBufferInterface::storeDynamicAttribute D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\VertexBuffer.cpp:202
    #4 0x7ffaeee11c81 in rx::VertexDataManager::storeDynamicAttrib D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\VertexDataManager.cpp:587
    #5 0x7ffaeee1117f in rx::VertexDataManager::storeDynamicAttribs D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\VertexDataManager.cpp:466
    #6 0x7ffaeed4e1c9 in rx::VertexArray11::updateDynamicAttribs D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexArray11.cpp:330
    #7 0x7ffaeed4d072 in rx::VertexArray11::syncStateForDraw D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexArray11.cpp:163
    #8 0x7ffaeecf97aa in rx::StateManager11::updateState D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\StateManager11.cpp:2001
    #9 0x7ffaeec7dd87 in rx::Context11::drawArraysInstancedBaseInstance D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Context11.cpp:311
    #10 0x7ffaee94b013 in gl::Context::drawArraysInstancedBaseInstance D:\chromium\src\third_party\angle\src\libANGLE\Context.cpp:6946
    #11 0x7ffaee4a97f8 in GL_DrawArraysInstancedBaseInstanceANGLE D:\chromium\src\third_party\angle\src\libGLESv2\entry_points_gles_ext_autogen.cpp:616
    #12 0x7ffac9c2a10c in gl::GLApiBase::glDrawArraysInstancedBaseInstanceANGLEFn D:\chromium\src\ui\gl\gl_bindings_autogen_gl.cc:2679
    #13 0x7ffaceba2304 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArraysInstancedBaseInstanceANGLE D:\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:4525
    #14 0x7ffacebce8aa in gpu::gles2::GLES2DecoderPassthroughImpl::HandleDrawArraysInstancedBaseInstanceANGLE D:\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_handlers.cc:1645
    #15 0x7ffaca02ae8c in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> D:\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:742
    #16 0x7ffaae4277fb in gpu::CommandBufferService::Flush D:\chromium\src\gpu\command_buffer\service\command_buffer_service.cc:267
    #17 0x7ffabfc389e1 in gpu::CommandBufferStub::OnAsyncFlush D:\chromium\src\gpu\ipc\service\command_buffer_stub.cc:504
    #18 0x7ffabfc378f3 in gpu::CommandBufferStub::ExecuteDeferredRequest D:\chromium\src\gpu\ipc\service\command_buffer_stub.cc:173
    #19 0x7ffac530d8a1 in gpu::GpuChannel::ExecuteDeferredRequest D:\chromium\src\gpu\ipc\service\gpu_channel.cc:833
    #20 0x7ffac531d40f in base::internal::Invoker<...>::RunOnce D:\chromium\src\base\functional\bind_internal.h:982
    #21 0x7ffaae46996b in base::internal::Invoker<...>::RunImpl D:\chromium\src\base\functional\bind_internal.h:1069
    #22 0x7ffaae43d792 in gpu::Scheduler::ExecuteSequence D:\chromium\src\gpu\command_buffer\service\scheduler.cc:707
    #23 0x7ffaae43b8c0 in gpu::Scheduler::RunNextTask D:\chromium\src\gpu\command_buffer\service\scheduler.cc:625
    #24 0x7ffaae440444 in base::internal::Invoker<...>::RunOnce D:\chromium\src\base\functional\bind_internal.h:982
    #25 0x7ffabe4ccc98 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task_annotator.cc:229
    #26 0x7ffac3c1b9f1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475
    #27 0x7ffac3c1a853 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346
    #28 0x7ffac3c630f7 in base::MessagePumpDefault::Run D:\chromium\src\base\message_loop\message_pump_default.cc:42
    #29 0x7ffac3c1d73f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650
    #30 0x7ffabe53fd0c in base::RunLoop::Run D:\chromium\src\base\run_loop.cc:135
    #31 0x7ffac1a78e13 in content::GpuMain D:\chromium\src\content\gpu\gpu_main.cc:479
    #32 0x7ffabae8899f in content::RunOtherNamedProcessTypeMain D:\chromium\src\content\app\content_main_runner_impl.cc:762
    #33 0x7ffabae8b10b in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content_main_runner_impl.cc:1152
    #34 0x7ffabae7eeff in content::RunContentProcess D:\chromium\src\content\app\content_main.cc:358
    #35 0x7ffabae7f6a2 in content::ContentMain D:\chromium\src\content\app\content_main.cc:371
    #36 0x7ffaaace2b06 in ChromeMain D:\chromium\src\chrome\app\chrome_main.cc:191
    #37 0x7ff7e0db4807 in MainDllLoader::Launch D:\chromium\src\chrome\app\main_dll_loader_win.cc:204
    #38 0x7ff7e0db2074 in main D:\chromium\src\chrome\app\chrome_exe_main_win.cc:351

0x116a3688ca00 is located 0 bytes after 768-byte region [0x116a3688c700,0x116a3688ca00)
allocated by thread T0 here:
    #0 0x7ffaf208c93f in _asan_wrap_memcpy+0x73f
    #1 0x7ffaee4423c3 in _malloc_base
    #2 0x7ffaf0050c2c in angle::MemoryBuffer::resize D:\chromium\src\third_party\angle\src\common\MemoryBuffer.cpp:40
    #3 0x7ffaeec73564 in rx::Buffer11::SystemMemoryStorage::resize D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:1691
    #4 0x7ffaeec6a0a7 in rx::Buffer11::setSubData D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:443
    #5 0x7ffaeec68bd4 in rx::Buffer11::setData D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:359
    #6 0x7ffaeeb81d0a in rx::BufferImpl::setDataWithUsageFlags D:\chromium\src\third_party\angle\src\libANGLE\renderer\BufferImpl.cpp:33
    #7 0x7ffaee8dc21a in gl::Buffer::setDataWithUsageFlags D:\chromium\src\third_party\angle\src\libANGLE\Buffer.cpp:186
    #8 0x7ffaee8dbb7c in gl::Buffer::bufferDataImpl D:\chromium\src\third_party\angle\src\libANGLE\Buffer.cpp:237
    #9 0x7ffaee8dc0aa in gl::Buffer::bufferData D:\chromium\src\third_party\angle\src\libANGLE\Buffer.cpp:173
    #10 0x7ffaee9450cf in gl::Context::bufferData D:\chromium\src\third_party\angle\src\libANGLE\Context.cpp:6434
    #11 0x7ffaee476a89 in GL_BufferData D:\chromium\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:589

SUMMARY: AddressSanitizer: heap-buffer-overflow D:\chromium\src\third_party\angle\src\libANGLE\renderer\copyvertex.inc.h:69 in rx::CopyNativeVertexData<float,4,4,0>

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## References

- [Renderer11::getVertexSpaceRequired](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp;l=4103-4104)
- [StreamingVertexBufferInterface::storeDynamicAttribute](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/d3d/VertexBuffer.cpp;l=191-199)
- [VertexDataManager::reserveSpaceForAttrib](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/d3d/VertexDataManager.cpp;l=525-527)
- [UnsignedCeilDivide](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/common/mathutil.h;l=1535-1539)
- [ValidateDrawInstancedAttribs (skipped validation)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/validationES.h;l=885-906)
- [Introducing CL](https://chromium-review.googlesource.com/c/angle/angle/+/2227022)

## Attachments

- [poc.html](attachments/poc.html) (text/html, 6.2 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 771 B)
- [asan.log](attachments/asan.log) (text/plain, 14.7 KB)

## Timeline

### me...@google.com (2026-03-07)

shrekshao@: Could you PTAL? Unfortunately I don't have a Windows setup to test the patch. Thanks.

Setting tentative severity and foundin labels.

### ch...@google.com (2026-03-07)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-03-20)

Project: angle/angle  

Branch:  main  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7675790>

Fix D3D11 integer overflows in streaming vertex buffer path

---


Expand for full commit details
```
     
    The D3D11 backend's streaming vertex buffer path had several integer 
    arithmetic errors that could lead to under-reservation or out-of-bounds 
    memory access when using large base instance values. 
     
    Key changes: 
    - mathutil.h: Added UnsignedCeilDivide64 to handle 64-bit values safely. 
    - Renderer11/Renderer9: Updated getVertexSpaceRequired to use size_t and 
    CheckedNumeric for instance calculations, preventing 32-bit truncation. 
    - VertexBuffer: Updated storeDynamicAttribute to use CheckedNumeric when 
    calculating adjustedCount for instanced attributes with a base instance. 
    - VertexDataManager: Changed firstVertexIndex from GLint to size_t to 
    prevent negative index wrapping and added overflow checks for vertex 
    buffer size validation. 
    - Added a regression test (D3D11OverflowTest.cpp) to verify that large 
    baseInstance values do not cause crashes in the D3D11 backend. 
     
    This is a Gemini generated CL with manual modifications. 
     
    Bug: chromium:489791424 
    Change-Id: I86d13594ee6da6238d8c6583c5268b4bd2ee2658 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7675790 
    Auto-Submit: Shrek Shao <shrekshao@google.com> 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `src/common/mathutil.h`
- M `src/common/mathutil_unittest.cpp`
- M `src/libANGLE/renderer/d3d/RendererD3D.h`
- M `src/libANGLE/renderer/d3d/VertexBuffer.cpp`
- M `src/libANGLE/renderer/d3d/VertexBuffer.h`
- M `src/libANGLE/renderer/d3d/VertexDataManager.cpp`
- M `src/libANGLE/renderer/d3d/VertexDataManager.h`
- M `src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp`
- M `src/libANGLE/renderer/d3d/d3d11/Renderer11.h`
- M `src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp`
- M `src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.h`
- M `src/libANGLE/renderer/d3d/d3d9/Renderer9.cpp`
- M `src/libANGLE/renderer/d3d/d3d9/Renderer9.h`
- M `src/libANGLE/renderer/d3d/d3d9/VertexBuffer9.cpp`
- M `src/libANGLE/renderer/d3d/d3d9/VertexBuffer9.h`
- M `src/tests/angle_end2end_tests.gni`
- M `src/tests/angle_end2end_tests_expectations.txt`
- A `src/tests/gl_tests/BaseInstanceOverflowTest.cpp`
- M `src/tests/perf_tests/IndexDataManagerTest.cpp`

---

Hash: [f4c4aaf00cd981baf98fd81d37823d1032582d12](https://chromiumdash.appspot.com/commit/f4c4aaf00cd981baf98fd81d37823d1032582d12)  

Date: Tue Mar 17 21:04:32 2026


---

### dx...@google.com (2026-03-20)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7686874>

Roll ANGLE from 477f6af8fbe6 to ab0ff0f644fb (2 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/477f6af8fbe6..ab0ff0f644fb 
     
    2026-03-20 lexa.knyazev@gmail.com PLS: Implicitly disable PLS on all ReadPixels variants 
    2026-03-20 shrekshao@google.com Fix D3D11 integer overflows in streaming vertex buffer path 
     
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
    Bug: chromium:489791424 
    Tbr: abdolrashidi@google.com 
    Change-Id: Ie2e2a0497376240848c5639aa8ae43ba9c9ce43b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686874 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1602410}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [d03b084341dedc85615750145c8f4fce4f852fe8](https://chromiumdash.appspot.com/commit/d03b084341dedc85615750145c8f4fce4f852fe8)  

Date: Fri Mar 20 03:16:19 2026


---

### ch...@google.com (2026-03-20)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1602410) appears to be after stable branch point (1582197).

Merge review required: a commit with DEPS changes was detected.

Requesting merge to beta (M147) because latest trunk commit (1602410) appears to be after beta branch point (1596535).

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-23)

No crashes in Canary, approved to merge to M146 and M147.

### dx...@google.com (2026-03-23)

Project: angle/angle  

Branch:  chromium/7680  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7693459>

[M146] Fix D3D11 integer overflows in streaming vertex buffer path

---


Expand for full commit details
```
     
    The D3D11 backend's streaming vertex buffer path had several integer 
    arithmetic errors that could lead to under-reservation or out-of-bounds 
    memory access when using large base instance values. 
     
    Key changes: 
    - mathutil.h: Added UnsignedCeilDivide64 to handle 64-bit values safely. 
    - Renderer11/Renderer9: Updated getVertexSpaceRequired to use size_t and 
    CheckedNumeric for instance calculations, preventing 32-bit truncation. 
    - VertexBuffer: Updated storeDynamicAttribute to use CheckedNumeric when 
    calculating adjustedCount for instanced attributes with a base instance. 
    - VertexDataManager: Changed firstVertexIndex from GLint to size_t to 
    prevent negative index wrapping and added overflow checks for vertex 
    buffer size validation. 
    - Added a regression test (D3D11OverflowTest.cpp) to verify that large 
    baseInstance values do not cause crashes in the D3D11 backend. 
     
    This is a Gemini generated CL with manual modifications. 
     
    Bug: chromium:489791424 
    Change-Id: I86d13594ee6da6238d8c6583c5268b4bd2ee2658 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7675790 
    Auto-Submit: Shrek Shao <shrekshao@google.com> 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    (cherry picked from commit f4c4aaf00cd981baf98fd81d37823d1032582d12) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7693459 
    Commit-Queue: Shrek Shao <shrekshao@google.com>

```

---

Files:

- M `src/common/mathutil.h`
- M `src/common/mathutil_unittest.cpp`
- M `src/libANGLE/renderer/d3d/RendererD3D.h`
- M `src/libANGLE/renderer/d3d/VertexBuffer.cpp`
- M `src/libANGLE/renderer/d3d/VertexBuffer.h`
- M `src/libANGLE/renderer/d3d/VertexDataManager.cpp`
- M `src/libANGLE/renderer/d3d/VertexDataManager.h`
- M `src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp`
- M `src/libANGLE/renderer/d3d/d3d11/Renderer11.h`
- M `src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp`
- M `src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.h`
- M `src/libANGLE/renderer/d3d/d3d9/Renderer9.cpp`
- M `src/libANGLE/renderer/d3d/d3d9/Renderer9.h`
- M `src/libANGLE/renderer/d3d/d3d9/VertexBuffer9.cpp`
- M `src/libANGLE/renderer/d3d/d3d9/VertexBuffer9.h`
- M `src/tests/angle_end2end_tests.gni`
- M `src/tests/angle_end2end_tests_expectations.txt`
- A `src/tests/gl_tests/BaseInstanceOverflowTest.cpp`
- M `src/tests/perf_tests/IndexDataManagerTest.cpp`

---

Hash: [d1057840b8daa9eaec0e3d676fbbb1223ec034a1](https://chromiumdash.appspot.com/commit/d1057840b8daa9eaec0e3d676fbbb1223ec034a1)  

Date: Tue Mar 17 21:04:32 2026


---

### dx...@google.com (2026-03-23)

Project: angle/angle  

Branch:  chromium/7727  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7694117>

[M147] Fix D3D11 integer overflows in streaming vertex buffer path

---


Expand for full commit details
```
     
    The D3D11 backend's streaming vertex buffer path had several integer 
    arithmetic errors that could lead to under-reservation or out-of-bounds 
    memory access when using large base instance values. 
     
    Key changes: 
    - mathutil.h: Added UnsignedCeilDivide64 to handle 64-bit values safely. 
    - Renderer11/Renderer9: Updated getVertexSpaceRequired to use size_t and 
    CheckedNumeric for instance calculations, preventing 32-bit truncation. 
    - VertexBuffer: Updated storeDynamicAttribute to use CheckedNumeric when 
    calculating adjustedCount for instanced attributes with a base instance. 
    - VertexDataManager: Changed firstVertexIndex from GLint to size_t to 
    prevent negative index wrapping and added overflow checks for vertex 
    buffer size validation. 
    - Added a regression test (D3D11OverflowTest.cpp) to verify that large 
    baseInstance values do not cause crashes in the D3D11 backend. 
     
    This is a Gemini generated CL with manual modifications. 
     
    Bug: chromium:489791424 
    Change-Id: I86d13594ee6da6238d8c6583c5268b4bd2ee2658 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7675790 
    Auto-Submit: Shrek Shao <shrekshao@google.com> 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    (cherry picked from commit f4c4aaf00cd981baf98fd81d37823d1032582d12) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7694117 
    Commit-Queue: Shrek Shao <shrekshao@google.com>

```

---

Files:

- M `src/common/mathutil.h`
- M `src/common/mathutil_unittest.cpp`
- M `src/libANGLE/renderer/d3d/RendererD3D.h`
- M `src/libANGLE/renderer/d3d/VertexBuffer.cpp`
- M `src/libANGLE/renderer/d3d/VertexBuffer.h`
- M `src/libANGLE/renderer/d3d/VertexDataManager.cpp`
- M `src/libANGLE/renderer/d3d/VertexDataManager.h`
- M `src/libANGLE/renderer/d3d/d3d11/Renderer11.cpp`
- M `src/libANGLE/renderer/d3d/d3d11/Renderer11.h`
- M `src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp`
- M `src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.h`
- M `src/libANGLE/renderer/d3d/d3d9/Renderer9.cpp`
- M `src/libANGLE/renderer/d3d/d3d9/Renderer9.h`
- M `src/libANGLE/renderer/d3d/d3d9/VertexBuffer9.cpp`
- M `src/libANGLE/renderer/d3d/d3d9/VertexBuffer9.h`
- M `src/tests/angle_end2end_tests.gni`
- M `src/tests/angle_end2end_tests_expectations.txt`
- A `src/tests/gl_tests/BaseInstanceOverflowTest.cpp`
- M `src/tests/perf_tests/IndexDataManagerTest.cpp`

---

Hash: [949bb97ac07572f7f8ae44e38541cc6e8ca95f93](https://chromiumdash.appspot.com/commit/949bb97ac07572f7f8ae44e38541cc6e8ca95f93)  

Date: Tue Mar 17 21:04:32 2026


---

### sp...@google.com (2026-04-10)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489791424)*
