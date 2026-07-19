# Integer truncation in ANGLE D3D11 VertexDataManager leads to heap OOB read from compromised renderer on Windows

| Field | Value |
|-------|-------|
| **Issue ID** | [489369089](https://issues.chromium.org/issues/489369089) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | je...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2026-03-04 |
| **Bounty** | $3,000.00 |

## Description

# Integer truncation in ANGLE D3D11 VertexDataManager leads to heap OOB read from compromised renderer on Windows

## Summary

ANGLE's D3D11 backend truncates a 64-bit vertex attribute offset to a 32-bit signed integer when performing CPU-side vertex format conversion. When a compromised renderer supplies an offset of 0x80000000 or larger, the truncation produces a negative value that shifts the source data pointer backward past the buffer allocation. The subsequent copy reads heap memory preceding the buffer. The crash occurs in the GPU process on the GPU scheduler thread. Platform: Windows only (requires the D3D11 ANGLE backend).

## Bisect

Introducing Commit: `2597fb6469a315f4942b867727c074e78bf2233a` (ANGLE repo)

- Date: 2016-12-09
- Author: Jiawei Shao ([jiawei.shao@intel.com](mailto:jiawei.shao@intel.com))
- Review: <https://chromium-review.googlesource.com/418880>

The commit refactored vertex array handling for ES 3.1 Vertex Attrib Binding support. It replaced direct field accesses with calls to `ComputeVertexAttributeOffset`, which returns a `GLintptr` (64-bit), but stored the result in a plain `int` (32-bit). Before this commit the offset was computed inline from narrower fields that could not exceed 32-bit range.

## Root Cause

When a WebGL page calls `gl.vertexAttribPointer` with a vertex format that requires CPU-side conversion on the D3D11 backend, the draw path reaches `VertexDataManager::StoreStaticAttrib`. This function retrieves the attribute's byte offset through `ComputeVertexAttributeOffset`, which returns a `GLintptr`, and immediately truncates it to `int`:

```
// third_party/angle/src/libANGLE/renderer/d3d/VertexDataManager.cpp
const int offset = static_cast<int>(ComputeVertexAttributeOffset(attrib, binding));

```

The truncated value is then added to the system-memory copy of the vertex buffer:

```
ANGLE_TRY(bufferD3D->getData(context, &sourceData));
if (sourceData)
{
    sourceData += offset;
}

```

When the original offset is 0x80000000 (2,147,483,648), `static_cast<int>` wraps it to -2,147,483,648. Adding this negative value to `sourceData` moves the pointer two gigabytes backward. However, the pointer does not land a full two gigabytes away from the buffer because `storeVertexAttributes` subsequently applies a compensating forward adjustment derived from `startIndex`:

```
int startIndex = offset / static_cast<int>(ComputeVertexAttributeStride(attrib, binding));

```

In `VertexBuffer11::storeVertexAttributes`, the `start` parameter (which is `-startIndex`) is multiplied by the stride and added to the input pointer:

```
// third_party/angle/src/libANGLE/renderer/d3d/d3d11/VertexBuffer11.cpp
const uint8_t *input = sourceData;
if (instances == 0 || binding.getDivisor() == 0)
{
    input += inputStride * start;
}

```

For offset 0x80000000 and stride 3, the arithmetic works out as follows. The truncated offset is -2,147,483,648. The start index is -2,147,483,648 divided by 3, which C++ truncates toward zero to -715,827,882. The negated start index, 715,827,882, is multiplied by stride 3 to give 2,147,483,646. The net displacement is -2,147,483,648 plus 2,147,483,646, which equals -2. The copy function therefore reads starting two bytes before the 256-byte buffer allocation, and ASAN reports a heap-buffer-overflow at exactly that location.

Only vertex formats that require CPU-side conversion reach `StoreStaticAttrib`. On D3D11 Feature Level 10.0 and above, `GL_BYTE` normalized with four components maps to `DXGI_FORMAT_R8G8B8A8_SNORM` and uses direct storage with no CPU copy. With three components, however, the format maps to `R8G8B8_SNORM`, which has no native D3D11 equivalent and is tagged `VERTEX_CONVERT_CPU`. This forces the attribute through the static conversion path where the truncation occurs.

Two renderer-side checks ordinarily reject offsets above INT\_MAX before they reach the GPU process. `WebGLRenderingContextBase::ValidateValueFitNonNegInt32` in the Blink layer rejects values exceeding `std::numeric_limits<int>::max()`, and `GLES2Implementation::ValidateOffset` in the GPU command buffer client performs the same check using `base::IsValueInRangeForNumericType<int32_t>`. Both checks execute exclusively in the renderer process. `ValidateValueFitNonNegInt32` resides under `third_party/blink/renderer/`, which is Blink rendering engine code that runs in the renderer. `ValidateOffset` resides under `gpu/command_buffer/client/`, which is the client half of Chromium's GPU command buffer architecture; the client serializes GL calls into shared-memory command buffers within the renderer process, while the service half under `gpu/command_buffer/service/` deserializes and executes them in the GPU process. Neither patched function is linked into or invoked by the GPU process. Under the compromised-renderer threat model these checks carry no security weight, and the attached `patch.diff` removes them to demonstrate the bug.

A natural question is whether ANGLE's own draw-time validation catches the oversized offset before `StoreStaticAttrib` runs. The answer is no. ANGLE's element-limit validation, which compares the vertex buffer's byte size against the attribute offset to determine how many elements can be fetched, is gated on `mBufferAccessValidationEnabled`. On the D3D11 backend this flag is unconditionally false because `renderer11_utils.cpp` sets `robustBufferAccessBehaviorKHR` to true:

```
// third_party/angle/src/libANGLE/renderer/d3d/d3d11/renderer11_utils.cpp
// Direct3D guarantees to return zero for any resource that is accessed out of bounds.
extensions->robustBufferAccessBehaviorKHR = true;

```

The resulting computation in `Context.cpp` disables the validation:

```
mBufferAccessValidationEnabled =
    !mSupportedExtensions.robustBufferAccessBehaviorKHR && mRequiresRobustBehavior;

```

D3D11's out-of-bounds guarantee covers GPU-side resource reads, but it does not protect the CPU-side `memcpy` that ANGLE performs in its vertex format conversion routines. The validation gap allows the truncated offset to pass through unchecked on every Windows system with a D3D11 GPU.

## Reproduce

This issue was tested on Chromium commit `cdd1f63c02` on Windows 10 x64 with an ASAN build. The bug requires the D3D11 ANGLE backend, so it applies only to Windows.

Because the vulnerable code path in the GPU process is guarded by two renderer-side range checks that reject offsets above INT\_MAX, reproducing the bug requires simulating a compromised renderer. The attached `patch.diff` removes the upper-bound check from `GLES2Implementation::ValidateOffset` in the GPU command buffer client and from `WebGLRenderingContextBase::ValidateValueFitNonNegInt32` in the Blink WebGL layer. Both functions reside in the renderer process, so modifying them is consistent with the compromised-renderer threat model. No GPU-process code is changed.

To begin, check out the tested revision and apply the patch.

```
cd D:\chromium\src
git checkout cdd1f63c02
git apply patch.diff

```

Configure an ASAN build by creating `out/asan-release/args.gn` with the following content.

```
is_asan = true
is_debug = false
is_component_build = true
symbol_level = 1
dcheck_always_on = false

```

Then build Chrome.

```
autoninja -C out/asan-release chrome

```

Launch Chrome and open the PoC.

```
set ASAN_OPTIONS=detect_odr_violation=0
out\asan-release\chrome.exe --enable-logging=stderr --no-first-run --no-default-browser-check --user-data-dir=%TEMP%\poc file:///D:/chromium/src/poc.html

```

The GPU process will print an AddressSanitizer heap-buffer-overflow report to stderr and abort. The browser process will log "GPU process exited unexpectedly." The expected ASAN summary line is:

```
SUMMARY: AddressSanitizer: heap-buffer-overflow copyvertex.inc.h:102
  in rx::CopyNativeVertexData<signed char,3,4,127>

```

After reproducing, restore the tree with `git checkout -- .` to undo the renderer patch.

### ASAN log

```
==31140==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x11cdfac6447e at pc 0x7ff8e74db30c bp 0x004c03bfd2d0 sp 0x004c03bfd318
READ of size 3 at 0x11cdfac6447e thread T0
    #0 0x7ff8e74db30b in _asan_memcpy+0x25b (D:\chromium\src\out\asan-release\clang_rt.asan_dynamic-x86_64.dll+0x18004b30b)
    #1 0x7ff819469c24 in rx::CopyNativeVertexData<signed char,3,4,127> D:\chromium\src\third_party\angle\src\libANGLE\renderer\copyvertex.inc.h:102
    #2 0x7ff819bc3c8f in rx::VertexBuffer11::storeVertexAttributes D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexBuffer11.cpp:133
    #3 0x7ff819c96530 in rx::StaticVertexBufferInterface::storeStaticAttribute D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\VertexBuffer.cpp:299
    #4 0x7ff819c9a233 in rx::VertexDataManager::StoreStaticAttrib D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\VertexDataManager.cpp:406
    #5 0x7ff819bc2059 in rx::VertexArray11::updateDirtyAttribs D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexArray11.cpp:277
    #6 0x7ff819bc162c in rx::VertexArray11::syncStateForDraw D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\VertexArray11.cpp:151
    #7 0x7ff819b6680a in rx::StateManager11::updateState D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\StateManager11.cpp:2001
    #8 0x7ff819adc11d in rx::Context11::drawArrays D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Context11.cpp:285
    #9 0x7ff819165dc0 in GL_DrawArrays D:\chromium\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:1819
    #10 0x7ff8dd51de75 in gl::RealGLApi::glDrawArraysFn D:\chromium\src\ui\gl\gl_gl_api_implementation.cc:390
    #11 0x7ff835f7dc6f in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays D:\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:1155
    #12 0x7ff835f4235c in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0> D:\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:742
    #13 0x7ff8347fc37d in gpu::CommandBufferService::Flush D:\chromium\src\gpu\command_buffer\service\command_buffer_service.cc:267
    #14 0x7ff835ca6b54 in gpu::CommandBufferStub::OnAsyncFlush D:\chromium\src\gpu\ipc\service\command_buffer_stub.cc:504
    #15 0x7ff835ca5a1e in gpu::CommandBufferStub::ExecuteDeferredRequest D:\chromium\src\gpu\ipc\service\command_buffer_stub.cc:173
    #16 0x7ff835cd21ff in gpu::GpuChannel::ExecuteDeferredRequest D:\chromium\src\gpu\ipc\service\gpu_channel.cc:833
    #17 0x7ff835ce30c2 in base::internal::Invoker<...>::RunOnce D:\chromium\src\base\functional\bind_internal.h:982
    #18 0x7ff83484a66f in base::internal::Invoker<...>::RunImpl<...> D:\chromium\src\base\functional\bind_internal.h:1069
    #19 0x7ff8348197ef in gpu::Scheduler::ExecuteSequence D:\chromium\src\gpu\command_buffer\service\scheduler.cc:707
    #20 0x7ff834817915 in gpu::Scheduler::RunNextTask D:\chromium\src\gpu\command_buffer\service\scheduler.cc:625
    #21 0x7ff83481cc18 in base::internal::Invoker<...>::RunOnce D:\chromium\src\base\functional\bind_internal.h:982
    #22 0x7ff8e8a420d8 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task_annotator.cc:229
    #23 0x7ff8e8ad6471 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475
    #24 0x7ff8e8ad52d3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346
    #25 0x7ff8e88a5060 in base::MessagePumpDefault::Run D:\chromium\src\base\message_loop\message_pump_default.cc:42
    #26 0x7ff8e8ad820f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650
    #27 0x7ff8e8993cbd in base::RunLoop::Run D:\chromium\src\base\run_loop.cc:135
    #28 0x7ff8ad0dbdb9 in content::GpuMain D:\chromium\src\content\gpu\gpu_main.cc:479

0x11cdfac6447e is located 2 bytes before 256-byte region [0x11cdfac64480,0x11cdfac64580)
allocated by thread T0 here:
    #0 0x7ff8e74dc8df in _asan_wrap_memcpy+0x73f (D:\chromium\src\out\asan-release\clang_rt.asan_dynamic-x86_64.dll+0x18004c8df)
    #1 0x7ff819f99bcd in angle::MemoryBuffer::resize D:\chromium\src\third_party\angle\src\common\MemoryBuffer.cpp:40
    #2 0x7ff819ad0a24 in rx::Buffer11::SystemMemoryStorage::resize D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:1691
    #3 0x7ff819ac2e34 in rx::Buffer11::getData D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Buffer11.cpp:375
    #4 0x7ff819c99c00 in rx::VertexDataManager::StoreStaticAttrib D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\VertexDataManager.cpp:375

SUMMARY: AddressSanitizer: heap-buffer-overflow D:\chromium\src\third_party\angle\src\libANGLE\renderer\copyvertex.inc.h:102 in rx::CopyNativeVertexData<signed char,3,4,127>
Shadow bytes around the buggy address:
  0x11cdfac64180: fd fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x11cdfac64200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11cdfac64280: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x11cdfac64300: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x11cdfac64380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x11cdfac64400: fd fa fa fa fa fa fa fa fa fa fa fa fa fa f7[fa]
  0x11cdfac64480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11cdfac64500: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11cdfac64580: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x11cdfac64600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11cdfac64680: fd fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.8 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 1.9 KB)
- [asan.log](attachments/asan.log) (text/plain, 13.8 KB)
- [readme.md](attachments/readme.md) (text/markdown, 1.8 KB)

## Timeline

### jd...@chromium.org (2026-03-09)

Due to a significant influx in vulnerability reports to Chrome, I have not been able to fully investigate this report, but I've set flags assuming it is valid.

geofflang@: would you please take a look? Thanks very much.

### ch...@google.com (2026-03-10)

Setting milestone because of s2 severity.

### ch...@google.com (2026-03-10)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-09)

Project: angle/angle  

Branch:  main  

Author:  Antonio Maiorano [amaiorano@google.com](mailto:amaiorano@google.com)  

Link:    <https://chromium-review.googlesource.com/7736785>

D3D11: Fix potential OOB read in StoreStaticAttrib

---


Expand for full commit details
```
     
    Bug: b/489369089 
    Change-Id: Ieda5e911ed0b122af49af15f52eb938787346143 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7736785 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Antonio Maiorano <amaiorano@google.com>

```

---

Files:

- M `src/libANGLE/renderer/d3d/VertexDataManager.cpp`
- M `src/tests/angle_end2end_tests_expectations.txt`
- M `src/tests/gl_tests/VertexAttributeTest.cpp`

---

Hash: [641c0d0e1bbd7d7220f797887fa28a1f17bfeb7d](https://chromiumdash.appspot.com/commit/641c0d0e1bbd7d7220f797887fa28a1f17bfeb7d)  

Date: Tue Apr 7 20:03:19 2026


---

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489369089)*
