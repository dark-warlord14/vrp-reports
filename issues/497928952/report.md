# Heap-buffer-overflow in VertexArrayGL::streamAttributes via shiftInstancedArrayDataWithOffset

| Field | Value |
|-------|-------|
| **Issue ID** | [497928952](https://issues.chromium.org/issues/497928952) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, ChromeOS |
| **Chrome Version** | 148.0.7762.0 |
| **Reporter** | ca...@gmail.com |
| **Assignee** | sh...@google.com |
| **Created** | 2026-03-30 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

```
ASAN_OPTIONS=detect_leaks=0:halt_on_error=1:print_stacktrace=1 \
out/asan/chrome \
  --no-sandbox \
  --headless=new \
  --use-angle=gl \
  --ozone-platform=headless \
  --no-first-run \
  --disable-background-networking \
  --disable-sync \
  --disable-extensions \
  --ignore-gpu-blocklist \
  --enable-angle-features=shiftInstancedArrayDataWithOffset \
  --virtual-time-budget=20000 \
  poc.html

```
# Problem Description

## Summary

`VertexArrayGL::streamAttributes()` in ANGLE's GL backend allocates a streaming vertex buffer based on `ComputeVertexBindingElementCount()`, then the `shiftInstancedArrayDataWithOffset` workaround **increases** `streamedVertexCount` after allocation. The slow-path memcpy loop writes past the buffer end. This is a heap-buffer-overflow in the GPU process, reachable from WebGL via `drawArraysInstanced` with `first > 0`.

- **File:** `third_party/angle/src/libANGLE/renderer/gl/VertexArrayGL.cpp`
- **Bug lines:** 492-496 (count increased), 548-554 (writes with increased count)
- **Process:** GPU process
- **Tested:** Chromium 148.0.7762.0 (commit `371e35b061`)
- **Platform:** macOS Intel (non-Haswell) by default; reproducible on any platform with `--enable-angle-features=shiftInstancedArrayDataWithOffset`

## Root Cause

Line 415: `computeStreamingAttributeSizes()` computes `streamingDataSize` using the original vertex count from `ComputeVertexBindingElementCount()`.

Line 438: Buffer allocated with original size: `bufferData(GL_ARRAY_BUFFER, requiredBufferSize, ...)`.

Lines 495-496: Workaround **increases** the vertex count:

```
streamedVertexCount = (instanceCount + indexRange.start() + adjustedDivisor - 1u) / adjustedDivisor;

```

Lines 548-554: Slow-path copy loop uses the **increased** count:

```
for (size_t vertexIdx = 0; vertexIdx < streamedVertexCount; vertexIdx++) {
    uint8_t *out = bufferPointer + curBufferOffset + (destStride * vertexIdx);
    const uint8_t *in = inputPointer + sourceStride * (vertexIdx + firstIndexForSeparateCopy);
    memcpy(out, in, destStride);
}

```

With `first=100, instanceCount=1024, divisor=1`: original count = 1024, new count = 1124. Buffer sized for 1024 vertices, loop writes 1124. **Overflow = 100 \* destStride bytes.**

The slow path is taken when `sourceStride != destStride` (e.g., vertex attribute with stride=20 for vec4 which packs to 16).

## Suggested Fix

In `streamAttributes()`, after the workaround modifies `streamedVertexCount` at line 495-496, recompute `batchMemcpySize` and ensure the buffer allocation at line 438 accounts for the maximum possible vertex count.

# Summary

Heap-buffer-overflow in VertexArrayGL::streamAttributes via shiftInstancedArrayDataWithOffset

# Custom Questions

#### Type of crash:

GPU process crash

#### Crash state:

```
==500925==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7186c57fd230 at pc 0x631b84c7600b bp 0x7ffc2b03d690 sp 0x7ffc2b03ce50
READ of size 16 at 0x7186c57fd230 thread T0 (chrome)
    #0 0x631b84c7600a in __asan_memcpy (/home/calysteon/chromium/src/out/asan/chrome+0x196e900a) (BuildId: 330ba48cdf0bd5aa)
    #1 0x6ee6ba61f271 in rx::VertexArrayGL::streamAttributes(gl::Context const*, angle::BitSetT<16ul, unsigned long, unsigned long> const&, int, gl::IndexRange const&, bool) const third_party/angle/src/libANGLE/renderer/gl/VertexArrayGL.cpp:553:21
    #2 0x6ee6ba61beb5 in rx::VertexArrayGL::syncDrawState(gl::Context const*, angle::BitSetT<16ul, unsigned long, unsigned long> const&, int, int, gl::DrawElementsType, void const*, int, bool, void const**) const third_party/angle/src/libANGLE/renderer/gl/VertexArrayGL.cpp:264:27
    #3 0x6ee6ba61b6de in rx::VertexArrayGL::syncClientSideData(gl::Context const*, angle::BitSetT<16ul, unsigned long, unsigned long> const&, int, int, int) const third_party/angle/src/libANGLE/renderer/gl/VertexArrayGL.cpp:180:12
    #4 0x6ee6ba4e5453 in rx::ContextGL::drawArraysInstanced(gl::Context const*, gl::PrimitiveMode, int, int, int) third_party/angle/src/libANGLE/renderer/gl/ContextGL.cpp:266:26
    #5 0x6ee6b9f7c6d8 in gl::Context::drawArraysInstanced(gl::PrimitiveMode, int, int, int) third_party/angle/src/libANGLE/Context.cpp:2961:26
    #6 0x6ee6b9779072 in GL_DrawArraysInstanced third_party/angle/src/libGLESv2/entry_points_gles_3_0_autogen.cpp:1132:22
    #7 0x631bad5b541d in gpu::gles2::GLES2DecoderImpl::HandleDrawArraysInstancedANGLE(unsigned int, void const volatile*) gpu/command_buffer/service/<gles2_cmd_decoder.cc:9429>:18
    #8 0x631bad5fbd19 in gpu::error::Error gpu::gles2::GLES2DecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/<gles2_cmd_decoder.cc:4766>:18
    #9 0x631b93ed348d in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/<command_buffer_service.cc:267>:35
    #10 0x631bad49be45 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/<command_buffer_stub.cc:504>:22
    #11 0x631bad49ae36 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/<command_buffer_stub.cc:173>:7
    #12 0x631bad4c5a1b in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/<gpu_channel.cc:833>:13
    #13 0x631bad4d3f17 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #14 0x631bad4d3cf9 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #15 0x631b93f20bb8 in base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>::Run(gpu::FenceSyncReleaseDelegate*) && base/functional/callback.h:155:12
    #16 0x631b93f2092a in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:815:49
    #17 0x631b85572945 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
    #18 0x631b93eee378 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) gpu/command_buffer/service/<scheduler.cc:707>:29
    #19 0x631b93eeba79 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/<scheduler.cc:625>:3
    #20 0x631b93ef0af1 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #21 0x631b85572945 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
    #22 0x631ba309a7d7 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/<task_annotator.cc:229>:34
    #23 0x631ba314a045 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #24 0x631ba31483ed in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/<thread_controller_with_message_pump_impl.cc:340>:40
    #25 0x631ba2f19d33 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/<message_pump_default.cc:42>:55
    #26 0x631ba314c442 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/<thread_controller_with_message_pump_impl.cc:644>:12
    #27 0x631ba2ffc654 in base::RunLoop::Run(base::Location const&) base/<run_loop.cc:135>:14
    #28 0x631bafca9c53 in content::GpuMain(content::MainFunctionParams) content/gpu/<gpu_main.cc:484>:14
    #29 0x631b9e44968a in content::RunZygote(content::ContentMainDelegate*) content/app/<content_main_runner_impl.cc:664>:14
    #30 0x631b9e44ad86 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/<content_main_runner_impl.cc:771>:12
    #31 0x631b9e44e0cc in content::ContentMainRunnerImpl::Run() content/app/<content_main_runner_impl.cc:1152>:10
    #32 0x631b9e447241 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/<content_main.cc:358>:36
    #33 0x631b9e44783c in content::ContentMain(content::ContentMainParams) content/app/<content_main.cc:371>:10
    #34 0x631b84cb2b38 in ChromeMain chrome/app/<chrome_main.cc:191>:12
    #35 0x72e6c722a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #36 0x72e6c722a28a in __libc_start_main csu/../csu/libc-start.c:360:3

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/calysteon/chromium/src/out/asan/chrome+0x196e900a) (BuildId: 330ba48cdf0bd5aa) in __asan_memcpy

```
#### Reporter credit:

Nathaniel Oh (@calysteon)

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A \

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.8 KB)
- [poc-controlled-write.html](attachments/poc-controlled-write.html) (text/html, 5.7 KB)

## Timeline

### ja...@google.com (2026-03-31)

Reproduced as described. Here's my ASAN output:

```
~/chrome_binaries$ ASAN_OPTIONS=detect_leaks=0:halt_on_error=1:print_stacktrace=1 ./chromium-148/chrome-wrapper   --no-sandbox   --headless=new   --use-angle=gl   --ozone-platform=headless   --no-first-run   --disable-background-networking   --disable-sync   --disable-extensions   --ignore-gpu-blocklist   --enable-angle-features=shiftInstancedArrayDataWithOffset   --virtual-time-budget=20000   --user-data-dir=`mktemp -d`   poc.html
ASAN_OPTIONS=detect_leaks=0:halt_on_error=1:print_stacktrace=1 ./chromium-148/chrome-wrapper   --no-sandbox    --use-angle=gl      --no-first-run   --disable-background-networking   --disable-sync   --disable-extensions   --ignore-gpu-blocklist   --enable-angle-features=shiftInstancedArrayDataWithOffset   --virtual-time-budget=20000   --user-data-dir=`mktemp -d`   localhost:8080/

[332165:332220:0330/171214.461710:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
[332165:332220:0330/171237.414510:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
=================================================================
==332248==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7e5e17153230 at pc 0x55779962100b bp 0x7ffeee167c20 sp 0x7ffeee1673e0
READ of size 16 at 0x7e5e17153230 thread T0 (chrome)
==332248==WARNING: invalid path to external symbolizer!
==332248==WARNING: Failed to use and restart external symbolizer!
    #0 0x55779962100a  (/.../chrome_binaries/chromium-148/chrome+0x10eb400a) (BuildId: 2f7458a0c5934b1f)
    #1 0x7bbe0c129551  (/.../chrome_binaries/chromium-148/libGLESv2.so+0x1929551) (BuildId: 52944c0ee0782d06)
    #2 0x7bbe0c1279a4  (/.../chrome_binaries/chromium-148/libGLESv2.so+0x19279a4) (BuildId: 52944c0ee0782d06)
    #3 0x7bbe0c12756e  (/.../chrome_binaries/chromium-148/libGLESv2.so+0x192756e) (BuildId: 52944c0ee0782d06)
    #4 0x7bbe0c013cfe  (/.../chrome_binaries/chromium-148/libGLESv2.so+0x1813cfe) (BuildId: 52944c0ee0782d06)
    #5 0x7bbe0bc73757  (/.../chrome_binaries/chromium-148/libGLESv2.so+0x1473757) (BuildId: 52944c0ee0782d06)
    #6 0x5577bb116c71  (/.../chrome_binaries/chromium-148/chrome+0x329a9c71) (BuildId: 2f7458a0c5934b1f)
    #7 0x5577bb09faa5  (/.../chrome_binaries/chromium-148/chrome+0x32932aa5) (BuildId: 2f7458a0c5934b1f)
    #8 0x5577a481d804  (/.../chrome_binaries/chromium-148/chrome+0x1c0b0804) (BuildId: 2f7458a0c5934b1f)
    #9 0x5577bab6c46b  (/.../chrome_binaries/chromium-148/chrome+0x323ff46b) (BuildId: 2f7458a0c5934b1f)
    #10 0x5577bab6b6d1  (/.../chrome_binaries/chromium-148/chrome+0x323fe6d1) (BuildId: 2f7458a0c5934b1f)
    #11 0x5577bab8e7ec  (/.../chrome_binaries/chromium-148/chrome+0x324217ec) (BuildId: 2f7458a0c5934b1f)
    #12 0x5577bab9c7d7  (/.../chrome_binaries/chromium-148/chrome+0x3242f7d7) (BuildId: 2f7458a0c5934b1f)
    #13 0x5577bab9c5b9  (/.../chrome_binaries/chromium-148/chrome+0x3242f5b9) (BuildId: 2f7458a0c5934b1f)
    #14 0x5577a4860201  (/.../chrome_binaries/chromium-148/chrome+0x1c0f3201) (BuildId: 2f7458a0c5934b1f)
    #15 0x5577a4834947  (/.../chrome_binaries/chromium-148/chrome+0x1c0c7947) (BuildId: 2f7458a0c5934b1f)
    #16 0x5577a4832978  (/.../chrome_binaries/chromium-148/chrome+0x1c0c5978) (BuildId: 2f7458a0c5934b1f)
    #17 0x5577a4836561  (/.../chrome_binaries/chromium-148/chrome+0x1c0c9561) (BuildId: 2f7458a0c5934b1f)
    #18 0x5577b169c396  (/.../chrome_binaries/chromium-148/chrome+0x28f2f396) (BuildId: 2f7458a0c5934b1f)
    #19 0x5577b1713a39  (/.../chrome_binaries/chromium-148/chrome+0x28fa6a39) (BuildId: 2f7458a0c5934b1f)
    #20 0x5577b17128aa  (/.../chrome_binaries/chromium-148/chrome+0x28fa58aa) (BuildId: 2f7458a0c5934b1f)
    #21 0x5577b18c17c8  (/.../chrome_binaries/chromium-148/chrome+0x291547c8) (BuildId: 2f7458a0c5934b1f)
    #22 0x5577b18c4d88  (/.../chrome_binaries/chromium-148/chrome+0x29157d88) (BuildId: 2f7458a0c5934b1f)
    #23 0x7fbe1a2f85ed  (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5c5ed) (BuildId: 58c462e4231d8ea78b160c5f95ce06e6661433e9)

0x7e5e17153230 is located 0 bytes after 20528-byte region [0x7e5e1714e200,0x7e5e17153230)
allocated by thread T0 (chrome) here:
    #0 0x557799623de7  (/.../chrome_binaries/chromium-148/chrome+0x10eb6de7) (BuildId: 2f7458a0c5934b1f)
    #1 0x7bbdfd6e2f62  (/usr/lib/x86_64-linux-gnu/libgallium-25.2.3-1.so+0x8e2f62) (BuildId: 16e9242790ec84f12ec6327f06ccbee5d52b063b)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/.../chrome_binaries/chromium-148/chrome+0x10eb400a) (BuildId: 2f7458a0c5934b1f) 
Shadow bytes around the buggy address:
  0x7e5e17152f80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e5e17153000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e5e17153080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e5e17153100: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e5e17153180: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7e5e17153200: 00 00 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa
  0x7e5e17153280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e5e17153300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e5e17153380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e5e17153400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e5e17153480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==332248==ADDITIONAL INFO

==332248==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5577a482dba6  (/.../chrome_binaries/chromium-148/chrome+0x1c0c0ba6) (BuildId: 2f7458a0c5934b1f)


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --enable-angle-features=shiftInstancedArrayDataWithOffset --ozone-platform=x11 --use-angle=gl --crashpad-handler-pid=332207 --enable-crash-reporter=,custom --user-data-dir=/tmp/tmp.Q6b88o4jNe --disable-breakpad --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAgAQAMAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAQAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,17852744006664348466,12935391031790563866,262144 --field-trial-handle=3,i,7238709560158101175,11966663169659200045,262144 --variations-seed-version --pseudonymization-salt-handle=7,i,7820969401879994256,3335429764655363607,4 --trace-process-track-uuid=3190708988185955192`


==332248==END OF ADDITIONAL INFO

==332248==ABORTING
[332485:332485:0330/171253.400849:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:488] GPU state invalid after WaitForGetOffsetInRange.
[332165:332165:0330/171253.404534:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256


```

### ja...@google.com (2026-03-31)

[security triage]
giving an initial severity of High (S1) for memory corruption in a sandboxed gpu process.

### ja...@google.com (2026-03-31)

with symbols:

```
~/chrome_binaries$ ASAN_OPTIONS=detect_leaks=0:halt_on_error=1:print_stacktrace=1 ./chromium-148/chrome-wrapper   --no-sandbox   --headless=new   --use-angle=gl   --ozone-platform=headless   --no-first-run   --disable-background-networking   --disable-sync   --disable-extensions   --ignore-gpu-blocklist   --enable-angle-features=shiftInstancedArrayDataWithOffset   --virtual-time-budget=20000   --user-data-dir=`mktemp -d`   poc.html
ASAN_OPTIONS=detect_leaks=0:halt_on_error=1:print_stacktrace=1 ./chromium-148/chrome-wrapper   --no-sandbox    --use-angle=gl      --no-first-run   --disable-background-networking   --disable-sync   --disable-extensions   --ignore-gpu-blocklist   --enable-angle-features=shiftInstancedArrayDataWithOffset   --virtual-time-budget=20000   --user-data-dir=`mktemp -d`   localhost:8080/

[332165:332220:0330/171214.461710:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
[332165:332220:0330/171237.414510:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
=================================================================
==332248==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7e5e17153230 at pc 0x55779962100b bp 0x7ffeee167c20 sp 0x7ffeee1673e0
READ of size 16 at 0x7e5e17153230 thread T0 (chrome)
==332248==WARNING: invalid path to external symbolizer!
==332248==WARNING: Failed to use and restart external symbolizer!
    #0 0x55779962100a in __asan_memcpy ??:0:0
    #1 0x7bbe0c129551 in rx::VertexArrayGL::streamAttributes(gl::Context const*, angle::BitSetT<16ul, unsigned long, unsigned long> const&, int, gl::IndexRange const&, bool) const ./../../third_party/angle/src/libANGLE/renderer/gl/VertexArrayGL.cpp:553:21
    #2 0x7bbe0c1279a4 in rx::VertexArrayGL::syncDrawState(gl::Context const*, angle::BitSetT<16ul, unsigned long, unsigned long> const&, int, int, gl::DrawElementsType, void const*, int, bool, void const**) const ./../../third_party/angle/src/libANGLE/renderer/gl/VertexArrayGL.cpp:264:27
    #3 0x7bbe0c12756e in rx::VertexArrayGL::syncClientSideData(gl::Context const*, angle::BitSetT<16ul, unsigned long, unsigned long> const&, int, int, int) const ./../../third_party/angle/src/libANGLE/renderer/gl/VertexArrayGL.cpp:180:12
    #4 0x7bbe0c013cfe in rx::ContextGL::drawArraysInstanced(gl::Context const*, gl::PrimitiveMode, int, int, int) ./../../third_party/angle/src/libANGLE/renderer/gl/ContextGL.cpp:266:26
    #5 0x7bbe0bc73757 in gl::Context::drawArraysInstanced(gl::PrimitiveMode, int, int, int) ./../../third_party/angle/src/libANGLE/Context.cpp:2961:26
    #6 0x5577bb116c71 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArraysInstancedANGLE(unsigned int, int, int, int) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:4509:10
    #7 0x5577bb09faa5 in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:742:20
    #8 0x5577a481d804 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:267:35
    #9 0x5577bab6c46b in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) ./../../gpu/ipc/service/command_buffer_stub.cc:504:22
    #10 0x5577bab6b6d1 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) ./../../gpu/ipc/service/command_buffer_stub.cc:173:7
    #11 0x5577bab8e7ec in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) ./../../gpu/ipc/service/gpu_channel.cc:833:13
    #12 0x5577bab9c7d7 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) ./../../base/functional/bind_internal.h:740:12
    #13 0x5577bab9c5b9 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) ./../../base/functional/bind_internal.h:956:5
    #14 0x5577a4860201 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) ./../../base/functional/callback.h:155:12
    #15 0x5577a4834947 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) ./../../base/functional/callback.h:155:12
    #16 0x5577a4832978 in gpu::Scheduler::RunNextTask() ./../../gpu/command_buffer/service/scheduler.cc:625:3
    #17 0x5577a4836561 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #18 0x5577b169c396 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #19 0x5577b1713a39 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #20 0x5577b17128aa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:340:40
    #21 0x5577b18c17c8 in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:736:46
    #22 0x5577b18c4d88 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:355:43
    #23 0x7fbe1a2f85ed in g_source_get_name ??:?

0x7e5e17153230 is located 0 bytes after 20528-byte region [0x7e5e1714e200,0x7e5e17153230)
allocated by thread T0 (chrome) here:
    #0 0x557799623de7 in ___interceptor_posix_memalign ??:0:0
    #1 0x7bbdfd6e2f62 in _mesa_glapi_set_dispatch ??:?

SUMMARY: AddressSanitizer: heap-buffer-overflow (/.../chrome_binaries/chromium-148/chrome+0x10eb400a) (BuildId: 2f7458a0c5934b1f)
Shadow bytes around the buggy address:
  0x7e5e17152f80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e5e17153000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e5e17153080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e5e17153100: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e5e17153180: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7e5e17153200: 00 00 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa
  0x7e5e17153280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e5e17153300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e5e17153380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e5e17153400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e5e17153480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==332248==ADDITIONAL INFO

==332248==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5577a482dba6 in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*) ./../../gpu/command_buffer/service/scheduler.cc:432:29


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --enable-angle-features=shiftInstancedArrayDataWithOffset --ozone-platform=x11 --use-angle=gl --crashpad-handler-pid=332207 --enable-crash-reporter=,custom --user-data-dir=/tmp/tmp.Q6b88o4jNe --disable-breakpad --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAgAQAMAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAQAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,17852744006664348466,12935391031790563866,262144 --field-trial-handle=3,i,7238709560158101175,11966663169659200045,262144 --variations-seed-version --pseudonymization-salt-handle=7,i,7820969401879994256,3335429764655363607,4 --trace-process-track-uuid=3190708988185955192`


==332248==END OF ADDITIONAL INFO

==332248==ABORTING
[332485:332485:0330/171253.400849:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:488] GPU state invalid after WaitForGetOffsetInRange.
[332165:332165:0330/171253.404534:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256


```

### ja...@google.com (2026-03-31)

Also reproduced on 146.0.7670.2

### ch...@google.com (2026-03-31)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-31)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ja...@google.com (2026-04-01)

[security triage]
All security issues need to be assigned to complete triage. Assigning to geofflang@

### ge...@chromium.org (2026-04-01)

Shrek: Could you look at this one?

### dx...@google.com (2026-04-07)

Project: angle/angle  

Branch:  main  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7728161>

GL: Fix heap-buffer-overflow in streamAttributes

---


Expand for full commit details
```
     
    When the shiftInstancedArrayDataWithOffset workaround is 
    enabled (primarily for Intel drivers on macOS), the number 
    of vertices to stream is increased to account for the first 
    parameter in drawArraysInstanced. 
     
    However, computeStreamingAttributeSizes was not aware of this 
    workaround, leading to an under-allocation of the streaming 
    buffer. Additionally, the copy loop in streamAttributes used 
    the increased vertex count to read from the source client 
    memory. 
    This resulted in a heap-buffer-overflow because the source 
    buffer might only contain enough data for the original instance 
    count, and the destination buffer was also too small for the 
    shifted layout. 
     
    This CL: 
    1. Updates computeStreamingAttributeSizes to accept an 
    applyExtraOffsetWorkaroundForInstancedAttributes flag and 
    correctly calculate the required buffer size when the 
    workaround is active. 
    2. Updates streamAttributes to only copy the original number 
    of vertices from the source memory in both fast and slow paths. 
    3. Ensures the destination buffer layout still respects the 
    increased vertex count for correct attribute spacing as required 
    by the workaround. 
    4. Adds a regression test 
    ShiftInstancedArrayDataWithOffsetSlowPath in 
    VertexAttributeTest.cpp that triggers the workaround 
    and the slow path copy loop. 
     
    Bug: b/497928952 
    Change-Id: I4b59ceec7cf9fc301eacb5b22faa4a3b2c2c863d 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7728161 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Shrek Shao <shrekshao@google.com> 
    Auto-Submit: Shrek Shao <shrekshao@google.com>

```

---

Files:

- M `src/libANGLE/renderer/gl/VertexArrayGL.cpp`
- M `src/libANGLE/renderer/gl/VertexArrayGL.h`
- M `src/tests/gl_tests/VertexAttributeTest.cpp`

---

Hash: [c0c3b52cec94593157bea7a5ecd9e1ab7b2ce802](https://chromiumdash.appspot.com/commit/c0c3b52cec94593157bea7a5ecd9e1ab7b2ce802)  

Date: Thu Apr 2 20:05:19 2026


---

### ch...@google.com (2026-04-08)

This is sufficiently serious that it should be merged to M146. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M147. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-04-08)

**M146** merge request created. **Please update [crbug/500599922](https://crbug.com/500599922) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M147** merge request created. **Please update [crbug/500599809](https://crbug.com/500599809) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500601251](https://crbug.com/500601251) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500600308](https://crbug.com/500600308) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500600739](https://crbug.com/500600739) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500600570](https://crbug.com/500600570) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500602637](https://crbug.com/500602637) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500602756](https://crbug.com/500602756) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500602892](https://crbug.com/500602892) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500602469](https://crbug.com/500602469) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500603871](https://crbug.com/500603871) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500603762](https://crbug.com/500603762) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500604296](https://crbug.com/500604296) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500603703](https://crbug.com/500603703) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500604489](https://crbug.com/500604489) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500603990](https://crbug.com/500603990) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500605896](https://crbug.com/500605896) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500605703](https://crbug.com/500605703) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500606616](https://crbug.com/500606616) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500606080](https://crbug.com/500606080) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500605784](https://crbug.com/500605784) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500606825](https://crbug.com/500606825) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500607299](https://crbug.com/500607299) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500608012](https://crbug.com/500608012) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500607542](https://crbug.com/500607542) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500608242](https://crbug.com/500608242) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500608659](https://crbug.com/500608659) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500609235](https://crbug.com/500609235) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500608902](https://crbug.com/500608902) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500609602](https://crbug.com/500609602) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500609822](https://crbug.com/500609822) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500609781](https://crbug.com/500609781) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500610003](https://crbug.com/500610003) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500609766](https://crbug.com/500609766) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500611267](https://crbug.com/500611267) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500611425](https://crbug.com/500611425) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500611211](https://crbug.com/500611211) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500611634](https://crbug.com/500611634) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500612149](https://crbug.com/500612149) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500612105](https://crbug.com/500612105) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500612512](https://crbug.com/500612512) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500613840](https://crbug.com/500613840) to have this merge reviewed.**

### ch...@google.com (2026-04-08)

**M148** merge request created. **Please update [crbug/500613386](https://crbug.com/500613386) to have this merge reviewed.**

### dr...@chromium.org (2026-04-08)

Sorry for the noise folks - we believe this is a novel edge case in our automation (https://crbug.com/500636350). I'll clean up the excess merges now.

### ca...@gmail.com (2026-04-08)

This is a follow-up demonstrating that the heap-buffer-overflow in `VertexArrayGL::streamAttributes()` is a **controlled write** of attacker-chosen data to GPU process heap memory, not merely a crash.

**Attached:** `poc-controlled-write.html`

## Controlled Write Primitive

The slow-path memcpy loop at `VertexArrayGL.cpp:548-554` copies vertex attribute data from the attacker's WebGL buffer into the overflowed heap region:

```cpp
for (size_t vertexIdx = 0; vertexIdx < streamedVertexCount; vertexIdx++) {
    uint8_t *out = bufferPointer + curBufferOffset + (destStride * vertexIdx);
    const uint8_t *in = inputPointer + sourceStride * (vertexIdx + firstIndexForSeparateCopy);
    memcpy(out, in, destStride);
}
```

The attacker controls all three dimensions of the write:

1. **Content**: The `in` pointer reads from the attacker's vertex buffer uploaded via `gl.bufferData()`. The PoC fills this buffer with `0xDEADBEEF 0xCAFEBABE 0x41414141 0x42424242` to demonstrate full byte-level control.

2. **Size**: The overflow size is `(streamedVertexCount - originalStreamedVertexCount) * destStride` bytes. The attacker controls the `first` parameter to `drawArraysInstanced`, which directly controls the overflow size. With `first=200`, `instanceCount=1024`, `divisor=1`: overflow = `200 * 16 = 3200 bytes`.

3. **Granularity**: Each loop iteration writes exactly `destStride` bytes (16 for vec4). The writes are contiguous, covering `[buffer + allocatedSize, buffer + allocatedSize + overflowSize)`.

## ASan Confirmation: WRITE of size 16

Running `poc-controlled-write.html` against the ASan build confirms a **WRITE** (not READ) overflow at the buffer boundary:

```
==6640==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x73bab280aeb0 at pc 0x631b84c7600b bp 0x7ffc2b03d690 sp 0x7ffc2b03ce50
WRITE of size 16 at 0x73bab280aeb0 thread T0 (chrome)
    #0 0x631b84c7600a in __asan_memcpy
    #1 0x6ee6ba61f271 in rx::VertexArrayGL::streamAttributes(...) third_party/angle/src/libANGLE/renderer/gl/VertexArrayGL.cpp:553:21
    #2 0x6ee6ba61beb5 in rx::VertexArrayGL::syncDrawState(...) VertexArrayGL.cpp:264:27
    #3 0x6ee6ba61b6de in rx::VertexArrayGL::syncClientSideData(...) VertexArrayGL.cpp:180:12
    #4 0x6ee6ba4e5453 in rx::ContextGL::drawArraysInstanced(...) ContextGL.cpp:266:26
    #5 0x6ee6b9f7c6d8 in gl::Context::drawArraysInstanced(...) Context.cpp:2961:26
    #6 0x6ee6b9779072 in GL_DrawArraysInstanced entry_points_gles_3_0_autogen.cpp:1132:22
    #7 0x631bad5b541d in gpu::gles2::GLES2DecoderImpl::HandleDrawArraysInstancedANGLE(...) gles2_cmd_decoder.cc:9429:18

0x73bab280aeb0 is located 0 bytes after 19632-byte region [0x73bab2806200,0x73bab280aeb0)
allocated by thread T0 (chrome) here:
    #0 posix_memalign
    ...
    #5 rx::VertexArrayGL::streamAttributes(...) VertexArrayGL.cpp:438:31

SUMMARY: AddressSanitizer: heap-buffer-overflow in __asan_memcpy
```

Key observations:
- **`WRITE of size 16`** - not a read. The overflow direction is write.
- **`0 bytes after 19632-byte region`** - the write hits exactly at the buffer boundary.
- Allocation at line 438 (`glBufferData`), overflow at line 553 (memcpy loop).

The original report showed `READ of size 16` because the source buffer was undersized. In `poc-controlled-write.html`, the source buffer is correctly sized to `(instanceCount + first) * srcStride`, ensuring the source side does not fault. ASan now catches the **destination-side** overflow.

## Proof: Attacker-Controlled Data at Buffer Boundary

Freezing the GPU process after the overflow loop completes and dumping heap memory with gdb shows the attacker's `0xDEADBEEF` pattern written right up to the buffer boundary:

```
--- LAST 64 BYTES INSIDE BUFFER ---
0x74729f1e7e70:  0xdeadbeef  0xcafebabe  0x41414141  0x42424242
0x74729f1e7e80:  0xdeadbeef  0xcafebabe  0x41414141  0x42424242
0x74729f1e7e90:  0xdeadbeef  0xcafebabe  0x41414141  0x42424242
0x74729f1e7ea0:  0xdeadbeef  0xcafebabe  0x41414141  0x42424242
```

The ASan redzone (at `0x74729f1e7eb0` onward) prevents the actual OOB write in the ASan build - this is expected. **In a release build there is no redzone.** The same memcpy loop continues for 200 more iterations past the boundary, writing the same attacker-controlled `0xDEADBEEF` pattern to contiguous heap addresses occupied by adjacent allocations.

## Overflow Calculation

```
originalStreamedVertexCount = ComputeVertexBindingElementCount(divisor=1, vertexCount=6, instanceCount=1024) = 1024
Buffer allocated: 1024 * 16 = 16384 bytes (actual alloc 19632 with alignment)

After shiftInstancedArrayDataWithOffset workaround (first=200):
  streamedVertexCount = (1024 + 200 + 1 - 1) / 1 = 1224
  Loop writes: 1224 * 16 = 19584 bytes

Overflow: (1224 - 1024) * 16 = 200 * 16 = 3200 bytes of attacker-controlled data
```

## Reproduction

```
ASAN_OPTIONS=detect_leaks=0:halt_on_error=1:print_stacktrace=1 \
out/asan/chrome \
  --no-sandbox \
  --headless=new \
  --use-angle=gl \
  --ozone-platform=headless \
  --no-first-run \
  --disable-background-networking \
  --disable-sync \
  --disable-extensions \
  --ignore-gpu-blocklist \
  --enable-angle-features=shiftInstancedArrayDataWithOffset \
  --virtual-time-budget=20000 \
  poc-controlled-write.html
```

## Exploitation Path

The GPU process is a highly privileged process (manages shared memory with the browser process, handles IPC). A controlled heap write of 3200 bytes in the GPU process enables:

- Overwriting function pointers or vtables in adjacent heap objects (GL context state, texture metadata, command buffer structures)
- Corrupting GPU command buffer metadata to redirect execution
- On Android, the GPU process is unsandboxed - this is a direct sandbox escape

The overflow size is fully controllable via the `first` parameter (up to `instanceCount * destStride` bytes), and the content is arbitrary byte data supplied through the WebGL vertex buffer.


### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

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

### dx...@google.com (2026-05-06)

Project: angle/angle  

Branch:  chromium/7778  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7817770>

[M148] GL: Fix heap-buffer-overflow in streamAttributes

---


Expand for full commit details
```
     
    When the shiftInstancedArrayDataWithOffset workaround is 
    enabled (primarily for Intel drivers on macOS), the number 
    of vertices to stream is increased to account for the first 
    parameter in drawArraysInstanced. 
     
    However, computeStreamingAttributeSizes was not aware of this 
    workaround, leading to an under-allocation of the streaming 
    buffer. Additionally, the copy loop in streamAttributes used 
    the increased vertex count to read from the source client 
    memory. 
    This resulted in a heap-buffer-overflow because the source 
    buffer might only contain enough data for the original instance 
    count, and the destination buffer was also too small for the 
    shifted layout. 
     
    This CL: 
    1. Updates computeStreamingAttributeSizes to accept an 
    applyExtraOffsetWorkaroundForInstancedAttributes flag and 
    correctly calculate the required buffer size when the 
    workaround is active. 
    2. Updates streamAttributes to only copy the original number 
    of vertices from the source memory in both fast and slow paths. 
    3. Ensures the destination buffer layout still respects the 
    increased vertex count for correct attribute spacing as required 
    by the workaround. 
    4. Adds a regression test 
    ShiftInstancedArrayDataWithOffsetSlowPath in 
    VertexAttributeTest.cpp that triggers the workaround 
    and the slow path copy loop. 
     
    Bug: b/497928952 
    Fixed: b/500613386 
    Change-Id: I4b59ceec7cf9fc301eacb5b22faa4a3b2c2c863d 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7728161 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Shrek Shao <shrekshao@google.com> 
    Auto-Submit: Shrek Shao <shrekshao@google.com> 
    (cherry picked from commit c0c3b52cec94593157bea7a5ecd9e1ab7b2ce802) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7817770

```

---

Files:

- M `src/libANGLE/renderer/gl/VertexArrayGL.cpp`
- M `src/libANGLE/renderer/gl/VertexArrayGL.h`
- M `src/tests/gl_tests/VertexAttributeTest.cpp`

---

Hash: [6c71c70ec7e838c5f1712974086c8bc33d07de14](https://chromiumdash.appspot.com/commit/6c71c70ec7e838c5f1712974086c8bc33d07de14)  

Date: Thu Apr 2 20:05:19 2026


---

### pe...@google.com (2026-05-06)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sh...@google.com (2026-05-14)

1 No
2 No

### pe...@google.com (2026-06-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-06-10)

1. https://chromium-review.git.corp.google.com/c/angle/angle/+/7902628
2. Low - There were a few conflicts.
3. 148
4. Yes.

### dx...@google.com (2026-06-11)

Project: angle/angle  

Branch:  chromium/7559  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7902628>

[M144-LTS] GL: Fix heap-buffer-overflow in streamAttributes

---


Expand for full commit details
```
     
    When the shiftInstancedArrayDataWithOffset workaround is 
    enabled (primarily for Intel drivers on macOS), the number 
    of vertices to stream is increased to account for the first 
    parameter in drawArraysInstanced. 
     
    However, computeStreamingAttributeSizes was not aware of this 
    workaround, leading to an under-allocation of the streaming 
    buffer. Additionally, the copy loop in streamAttributes used 
    the increased vertex count to read from the source client 
    memory. 
    This resulted in a heap-buffer-overflow because the source 
    buffer might only contain enough data for the original instance 
    count, and the destination buffer was also too small for the 
    shifted layout. 
     
    This CL: 
    1. Updates computeStreamingAttributeSizes to accept an 
    applyExtraOffsetWorkaroundForInstancedAttributes flag and 
    correctly calculate the required buffer size when the 
    workaround is active. 
    2. Updates streamAttributes to only copy the original number 
    of vertices from the source memory in both fast and slow paths. 
    3. Ensures the destination buffer layout still respects the 
    increased vertex count for correct attribute spacing as required 
    by the workaround. 
    4. Adds a regression test 
    ShiftInstancedArrayDataWithOffsetSlowPath in 
    VertexAttributeTest.cpp that triggers the workaround 
    and the slow path copy loop. 
     
    Bug: b/497928952 
    Change-Id: I4b59ceec7cf9fc301eacb5b22faa4a3b2c2c863d 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7728161 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Shrek Shao <shrekshao@google.com> 
    Auto-Submit: Shrek Shao <shrekshao@google.com> 
    (cherry picked from commit c0c3b52cec94593157bea7a5ecd9e1ab7b2ce802) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7902628 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/gl/VertexArrayGL.cpp`
- M `src/libANGLE/renderer/gl/VertexArrayGL.h`
- M `src/tests/gl_tests/VertexAttributeTest.cpp`

---

Hash: [4a20fc969c6987684356ce1875c58b4d9aae1fb2](https://chromiumdash.appspot.com/commit/4a20fc969c6987684356ce1875c58b4d9aae1fb2)  

Date: Thu Apr 2 20:05:19 2026


---

### ch...@google.com (2026-07-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/497928952)*
