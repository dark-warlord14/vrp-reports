# uaf in rx::vk::CommandBufferHelper::bufferWrite

| Field | Value |
|-------|-------|
| **Issue ID** | [40058051](https://issues.chromium.org/issues/40058051) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>Vulkan |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | em...@gmail.com |
| **Assignee** | ab...@google.com |
| **Created** | 2021-11-28 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36

Steps to reproduce the problem:
Ubunt 20.04

Chrome version
Version Chromium 98.0.4710.4 (Developer Build) (64-bit) with asan build
Chromium 98.0.4733.0 (Developer Build) (64-bit) gs://chromium-browser-asan/linux-release/asan-linux-release-945734.zip

./chrome http://localhost:8000/crash.html

What is the expected behavior?

What went wrong?
==563433==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b000036c28 at pc 0x7f29cfeaa66d bp 0x7fff10f832d0 sp 0x7fff10f832c8
READ of size 8 at 0x60b000036c28 thread T0 (chrome)
==563433==WARNING: invalid path to external symbolizer!
==563433==WARNING: Failed to use and restart external symbolizer!
    #0 0x7f29cfeaa66c in rx::vk::CommandBufferHelper::bufferWrite(rx::ContextVk*, unsigned int, rx::vk::PipelineStage, rx::vk::AliasingMode, rx::vk::BufferHelper*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/ResourceVk.h:83
    #1 0x7f29cfeaa66c in add ./../../third_party/angle/src/libANGLE/renderer/vulkan/ResourceVk.h:157
    #2 0x7f29cfeaa66c in retainReadWrite ./../../third_party/angle/src/libANGLE/renderer/vulkan/ResourceVk.h:268
    #3 0x7f29cfeaa66c in bufferWrite ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:1045
    #4 0x7f29cfeaa66c in ?? ??:0
    #5 0x7f29cfd1216b in rx::ContextVk::handleDirtyGraphicsTransformFeedbackBuffersEmulation(angle::BitSetT<18ul, unsigned long, unsigned long>::Iterator*, angle::BitSetT<18ul, unsigned long, unsigned long>) ./../../third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:2002
    #6 0x7f29cfd1216b in ?? ??:0
    #7 0x7f29cfd1b72a in rx::ContextVk::setupDraw(gl::Context const*, gl::PrimitiveMode, int, int, int, gl::DrawElementsType, void const*, angle::BitSetT<18ul, unsigned long, unsigned long>) ./../../third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:1010
    #8 0x7f29cfd1b72a in ?? ??:0
    #9 0x7f29cfd246d0 in rx::ContextVk::drawArrays(gl::Context const*, gl::PrimitiveMode, int, int) ./../../third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:2659
    #10 0x7f29cfd246d0 in ?? ??:0
    #11 0x7f29cf661290 in GL_DrawArrays ./../../third_party/angle/src/libANGLE/Context.inl.h:133
    #12 0x7f29cf661290 in GL_DrawArrays ./../../third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:1109
    #13 0x7f29cf661290 in ?? ??:0
    #14 0x55ede788d269 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(unsigned int, int, int) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1216
    #15 0x55ede788d269 in ?? ??:0
    #16 0x55ede785b92f in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858
    #17 0x55ede785b92f in ?? ??:0
    #18 0x55ede7cda385 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:70
    #19 0x55ede7cda385 in ?? ??:0
    #20 0x55ede7ccdeaf in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) ./../../gpu/ipc/service/command_buffer_stub.cc:499
    #21 0x55ede7ccdeaf in ?? ??:0
    #22 0x55ede7ccd459 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command_buffer_stub.cc:151
    #23 0x55ede7ccd459 in ?? ??:0
    #24 0x55ede7ce0e62 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) ./../../gpu/ipc/service/gpu_channel.cc:666
    #25 0x55ede7ce0e62 in ?? ??:0
    #26 0x55ede7ced7f6 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) ./../../base/bind_internal.h:535
    #27 0x55ede7ced7f6 in ?? ??:0
    #28 0x55ede66cee87 in gpu::Scheduler::RunNextTask() ./../../base/callback.h:142
    #29 0x55ede66cee87 in RunNextTask ./../../gpu/command_buffer/service/scheduler.cc:685
    #30 0x55ede66cee87 in ?? ??:0
    #31 0x55ede205cc33 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/callback.h:142
    #32 0x55ede205cc33 in RunTaskImpl ./../../base/task/common/task_annotator.cc:135
    #33 0x55ede205cc33 in ?? ??:0
    #34 0x55ede20975c3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/common/task_annotator.h:73
    #35 0x55ede20975c3 in DoWorkImpl ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356
    #36 0x55ede20975c3 in ?? ??:0
    #37 0x55ede2096dd7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261
    #38 0x55ede2096dd7 in ?? ??:0
    #39 0x55ede2098191 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread_controller_with_message_pump_impl.cc:?
    #40 0x55ede2098191 in ?? ??:0
    #41 0x55ede1f54039 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:375
    #42 0x55ede1f54039 in WorkSourceDispatch ./../../base/message_loop/message_pump_glib.cc:125
    #43 0x55ede1f54039 in ?? ??:0
    #44 0x7f29d879317c in g_main_context_dispatch ??:?
    #45 0x7f29d879317c in ?? ??:0

0x60b000036c28 is located 8 bytes inside of 112-byte region [0x60b000036c20,0x60b000036c90)
freed by thread T0 (chrome) here:
    #0 0x55edd3e0b6dd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152
    #1 0x55edd3e0b6dd in ?? ??:0
    #2 0x7f29cfce4ee9 in rx::BufferVk::release(rx::ContextVk*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/BufferVk.cpp:241
    #3 0x7f29cfce4ee9 in ?? ??:0
    #4 0x7f29cfce5775 in rx::BufferVk::setDataWithMemoryType(gl::Context const*, gl::BufferBinding, void const*, unsigned long, unsigned int, bool, gl::BufferUsage) ./../../third_party/angle/src/libANGLE/renderer/vulkan/BufferVk.cpp:436
    #5 0x7f29cfce5775 in ?? ??:0
    #6 0x7f29cfce5436 in rx::BufferVk::setDataWithUsageFlags(gl::Context const*, gl::BufferBinding, void*, void const*, unsigned long, gl::BufferUsage, unsigned int) ./../../third_party/angle/src/libANGLE/renderer/vulkan/BufferVk.cpp:393
    #7 0x7f29cfce5436 in ?? ??:0
    #8 0x7f29cf6a601a in gl::Buffer::bufferDataImpl(gl::Context*, gl::BufferBinding, void const*, long, gl::BufferUsage, unsigned int) ./../../third_party/angle/src/libANGLE/Buffer.cpp:136
    #9 0x7f29cf6a601a in ?? ??:0
    #10 0x7f29cf6a6413 in gl::Buffer::bufferData(gl::Context*, gl::BufferBinding, void const*, long, gl::BufferUsage) ./../../third_party/angle/src/libANGLE/Buffer.cpp:100
    #11 0x7f29cf6a6413 in ?? ??:0
    #12 0x7f29cf65ee5f in GL_BufferData ./../../third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:355
    #13 0x7f29cf65ee5f in ?? ??:0
    #14 0x55ede788380a in gpu::gles2::GLES2DecoderPassthroughImpl::DoBufferData(unsigned int, long, void const*, unsigned int) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:657
    #15 0x55ede788380a in ?? ??:0
    #16 0x55ede785b92f in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858
    #17 0x55ede785b92f in ?? ??:0
    #18 0x55ede7cda385 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:70
    #19 0x55ede7cda385 in ?? ??:0
    #20 0x55ede7ccdeaf in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) ./../../gpu/ipc/service/command_buffer_stub.cc:499
    #21 0x55ede7ccdeaf in ?? ??:0
    #22 0x55ede7ccd459 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command_buffer_stub.cc:151
    #23 0x55ede7ccd459 in ?? ??:0
    #24 0x55ede7ce0e62 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) ./../../gpu/ipc/service/gpu_channel.cc:666
    #25 0x55ede7ce0e62 in ?? ??:0
    #26 0x55ede7ced7f6 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) ./../../base/bind_internal.h:535
    #27 0x55ede7ced7f6 in ?? ??:0
    #28 0x55ede66cee87 in Run ./../../base/callback.h:142
    #29 0x55ede66cee87 in RunNextTask ./../../gpu/command_buffer/service/scheduler.cc:685
    #30 0x55ede66cee87 in ?? ??:0
    #31 0x55ede205cc33 in Run ./../../base/callback.h:142
    #32 0x55ede205cc33 in RunTaskImpl ./../../base/task/common/task_annotator.cc:135
    #33 0x55ede205cc33 in ?? ??:0
    #34 0x55ede20975c3 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> ./../../base/task/common/task_annotator.h:73
    #35 0x55ede20975c3 in DoWorkImpl ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356
    #36 0x55ede20975c3 in ?? ??:0
    #37 0x55ede2096dd7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261
    #38 0x55ede2096dd7 in ?? ??:0
    #39 0x55ede2098191 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:?
    #40 0x55ede2098191 in ?? ??:0
    #41 0x55ede1f54039 in HandleDispatch ./../../base/message_loop/message_pump_glib.cc:375
    #42 0x55ede1f54039 in WorkSourceDispatch ./../../base/message_loop/message_pump_glib.cc:125
    #43 0x55ede1f54039 in ?? ??:0
    #44 0x7f29d879317c in g_main_context_dispatch ??:?
    #45 0x7f29d879317c in ?? ??:0

previously allocated by thread T0 (chrome) here:
    #0 0x55edd3e0ae7d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95
    #1 0x55edd3e0ae7d in ?? ??:0
    #2 0x7f29cfeb5294 in rx::vk::DynamicBuffer::allocateNewBuffer(rx::ContextVk*) ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725
    #3 0x7f29cfeb5294 in allocateNewBuffer ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:2165
    #4 0x7f29cfeb5294 in ?? ??:0
    #5 0x7f29cfeb6668 in rx::vk::DynamicBuffer::allocateWithAlignment(rx::ContextVk*, unsigned long, unsigned long, unsigned char**, VkBuffer_T**, unsigned long*, bool*) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:2247
    #6 0x7f29cfeb6668 in ?? ??:0
    #7 0x7f29cfce5941 in rx::BufferVk::setDataWithMemoryType(gl::Context const*, gl::BufferBinding, void const*, unsigned long, unsigned int, bool, gl::BufferUsage) ./../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.h:127
    #8 0x7f29cfce5941 in acquireBufferHelper ./../../third_party/angle/src/libANGLE/renderer/vulkan/BufferVk.cpp:1183
    #9 0x7f29cfce5941 in rx::BufferVk::setDataWithMemoryType(gl::Context const*, gl::BufferBinding, void const*, unsigned long, unsigned int, bool, gl::BufferUsage) ./../../third_party/angle/src/libANGLE/renderer/vulkan/BufferVk.cpp:460
    #10 0x7f29cfce5941 in ?? ??:0
    #11 0x7f29cfce5436 in rx::BufferVk::setDataWithUsageFlags(gl::Context const*, gl::BufferBinding, void*, void const*, unsigned long, gl::BufferUsage, unsigned int) ./../../third_party/angle/src/libANGLE/renderer/vulkan/BufferVk.cpp:393
    #12 0x7f29cfce5436 in ?? ??:0
    #13 0x7f29cf6a601a in gl::Buffer::bufferDataImpl(gl::Context*, gl::BufferBinding, void const*, long, gl::BufferUsage, unsigned int) ./../../third_party/angle/src/libANGLE/Buffer.cpp:136
    #14 0x7f29cf6a601a in ?? ??:0
    #15 0x7f29cf6a6413 in gl::Buffer::bufferData(gl::Context*, gl::BufferBinding, void const*, long, gl::BufferUsage) ./../../third_party/angle/src/libANGLE/Buffer.cpp:100
    #16 0x7f29cf6a6413 in ?? ??:0
    #17 0x7f29cf65ee5f in GL_BufferData ./../../third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:355
    #18 0x7f29cf65ee5f in ?? ??:0
    #19 0x55ede788380a in gpu::gles2::GLES2DecoderPassthroughImpl::DoBufferData(unsigned int, long, void const*, unsigned int) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:657
    #20 0x55ede788380a in ?? ??:0
    #21 0x55ede785b92f in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858
    #22 0x55ede785b92f in ?? ??:0
    #23 0x55ede7cda385 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:70
    #24 0x55ede7cda385 in ?? ??:0
    #25 0x55ede7ccdeaf in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) ./../../gpu/ipc/service/command_buffer_stub.cc:499
    #26 0x55ede7ccdeaf in ?? ??:0
    #27 0x55ede7ccd459 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command_buffer_stub.cc:151
    #28 0x55ede7ccd459 in ?? ??:0
    #29 0x55ede7ce0e62 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) ./../../gpu/ipc/service/gpu_channel.cc:666
    #30 0x55ede7ce0e62 in ?? ??:0
    #31 0x55ede7ced7f6 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) ./../../base/bind_internal.h:535
    #32 0x55ede7ced7f6 in ?? ??:0
    #33 0x55ede66cee87 in Run ./../../base/callback.h:142
    #34 0x55ede66cee87 in RunNextTask ./../../gpu/command_buffer/service/scheduler.cc:685
    #35 0x55ede66cee87 in ?? ??:0
    #36 0x55ede205cc33 in Run ./../../base/callback.h:142
    #37 0x55ede205cc33 in RunTaskImpl ./../../base/task/common/task_annotator.cc:135
    #38 0x55ede205cc33 in ?? ??:0
    #39 0x55ede20975c3 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> ./../../base/task/common/task_annotator.h:73
    #40 0x55ede20975c3 in DoWorkImpl ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356
    #41 0x55ede20975c3 in ?? ??:0
    #42 0x55ede2096dd7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261
    #43 0x55ede2096dd7 in ?? ??:0
    #44 0x55ede2098191 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:?
    #45 0x55ede2098191 in ?? ??:0
    #46 0x55ede1f54039 in HandleDispatch ./../../base/message_loop/message_pump_glib.cc:375
    #47 0x55ede1f54039 in WorkSourceDispatch ./../../base/message_loop/message_pump_glib.cc:125
    #48 0x55ede1f54039 in ?? ??:0
    #49 0x7f29d879317c in g_main_context_dispatch ??:?
    #50 0x7f29d879317c in ?? ??:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/exp11/asan-linux-release/libGLESv2.so+0x102f66c)
Shadow bytes around the buggy address:
  0x0c167fffed30: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x0c167fffed40: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c167fffed50: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c167fffed60: fd fd fd fd fd fa fa fa fa fa fa fa fa fa 00 00
  0x0c167fffed70: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa
=>0x0c167fffed80: fa fa fa fa fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x0c167fffed90: fd fd fa fa fa fa fa fa fa fa 00 00 00 00 00 00
  0x0c167fffeda0: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
  0x0c167fffedb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa
  0x0c167fffedc0: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00
  0x0c167fffedd0: 00 00 00 00 fa fa fa fa fa fa fa fa 00 00 00 00
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
==563433==ABORTING

Did this work before? N/A 

Chrome version:  98.0.4710.4   Channel: dev
OS Version: 20.04

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.3 KB)

## Timeline

### [Deleted User] (2021-11-28)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5956867505061888.

### cl...@chromium.org (2021-11-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-29)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-29)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>Vulkan]

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-30)

Detailed Report: https://clusterfuzz.com/testcase?key=5956867505061888

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60f000038ed8
Crash State:
  rx::vk::CommandBufferHelper::bufferWrite
  rx::ContextVk::handleDirtyGraphicsTransformFeedbackBuffersEmulation
  rx::ContextVk::setupDraw
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=769545:769546

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5956867505061888

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### rs...@chromium.org (2021-11-30)

Clusterfuzz’s identified regression window indicates https://chromium.googlesource.com/angle/angle.git/+/8270ebbd627d24eb87c61fde1282f52a6e085653.

### cl...@chromium.org (2021-11-30)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2021-11-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2021-11-30)

Amirali, could you help me implement the fix for this use-after-free in ANGLE's Vulkan back-end? It's a serious security issue that affects the shipping implementation. I've implemented an integration test here: https://chromium-review.googlesource.com/c/angle/angle/+/3309101 . The test will crash in the Vulkan back-end, as well as producing VVL errors and ASAN errors when run under ASAN.

The bug is that a "BufferData" call creates the vk::BufferHelper storage after we call BeginTransformFeedback. The XFB object then has stale Buffer handles in its internal cache.

Here's my sketch of a fix:

- make TransformFeedbackVk inherit from angle::ObserverInterface, and add a vector of angle::ObserverBindings representing each buffer binding point. You'll need to initialize these.
- connect the ObserverBindings with BufferVk objects either in TransformFeedbackVk::begin or in TransformFeedbackVk::initializeXFBBuffersDesc. Deconnect them if necessary in ::end() (not sure when/if necessary)
- in BufferVk::acquireBufferHelper, if updateType == StorageChanged, send a new message like angle::SubjectMessage::BufferVkStorageChanged
- add TransformFeedbackVk::onSubjectStateChange, and handle this message there. The handling will be to update the Buffer caches in TransformFeedbackVk.

Look over the code & let me know if that makes sense. It should fix the test I added above. Frank, FYI.


### ab...@google.com (2021-11-30)

Hello Jamie,
Sure, I'll be happy to help.

### ab...@google.com (2021-11-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f84dc44fd9242c4a5f6d726f084be4b5feb39832

commit f84dc44fd9242c4a5f6d726f084be4b5feb39832
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Nov 30 17:22:21 2021

Add a test for changing an XFB buffer after Begin.

Bug: chromium:1274316
Change-Id: I4ba240ff4cc383b157a64a0c92e8ce8ab2d8061e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3309101
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/f84dc44fd9242c4a5f6d726f084be4b5feb39832/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/f84dc44fd9242c4a5f6d726f084be4b5feb39832/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/f84dc44fd9242c4a5f6d726f084be4b5feb39832/src/tests/capture_replay_tests/capture_replay_expectations.txt


### gi...@appspot.gserviceaccount.com (2021-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/531e47db7393b331895ae58d24b9e33c63671728

commit 531e47db7393b331895ae58d24b9e33c63671728
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Dec 01 16:59:25 2021

Roll ANGLE from 5f67a941ff1e to 9d91064d6c8b (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/5f67a941ff1e..9d91064d6c8b

2021-12-01 ynovikov@chromium.org Document using Rubber Stamper for test expectations CLs
2021-12-01 jmadill@chromium.org Add a test for changing an XFB buffer after Begin.
2021-12-01 gert.wollny@collabora.com Capture/Replay: eliminate redundant parameters in GenOnBind

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1274316
Tbr: ynovikov@google.com
Change-Id: I4223b222e9bfaedcdc23e9f478db492590e6ff23
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3310714
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#947056}

[modify] https://crrev.com/531e47db7393b331895ae58d24b9e33c63671728/DEPS


### gi...@appspot.gserviceaccount.com (2021-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/89e11878b275b15735eaf273ababfa6fd43a2e3d

commit 89e11878b275b15735eaf273ababfa6fd43a2e3d
Author: Amirali Abdolrashidi <abdolrashidi@google.com>
Date: Mon Dec 06 17:42:46 2021

Vulkan: Fix the UAF issue with BufferData

* Fixed the use-after-free issue with stale buffer handles
after calling BeginTransformFeedback.
  * Added an observer for TransformFeedbackVk to update the
buffer handles when buffer's storage is changed and the buffer
update type is StorageRedefined.
* Added a function to TransformFeedbackVk::onDestroy() to
release the counter buffers in order to avoid crash due to
TransformFeedbackVk::end() not being called, e.g., as a
result of no glEndTransformFeedback() calls.

Bug: chromium:1274316
Change-Id: I8ed477f36e6ff89dd4764bb59af564c69efe33e2
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3321789
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/89e11878b275b15735eaf273ababfa6fd43a2e3d/src/libANGLE/Buffer.cpp
[modify] https://crrev.com/89e11878b275b15735eaf273ababfa6fd43a2e3d/src/libANGLE/renderer/vulkan/TransformFeedbackVk.cpp
[modify] https://crrev.com/89e11878b275b15735eaf273ababfa6fd43a2e3d/src/libANGLE/renderer/vulkan/TransformFeedbackVk.h
[modify] https://crrev.com/89e11878b275b15735eaf273ababfa6fd43a2e3d/src/libANGLE/Texture.cpp
[modify] https://crrev.com/89e11878b275b15735eaf273ababfa6fd43a2e3d/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/89e11878b275b15735eaf273ababfa6fd43a2e3d/src/libANGLE/VertexArray.cpp
[modify] https://crrev.com/89e11878b275b15735eaf273ababfa6fd43a2e3d/src/libANGLE/Observer.h
[modify] https://crrev.com/89e11878b275b15735eaf273ababfa6fd43a2e3d/src/tests/capture_replay_tests/capture_replay_expectations.txt
[modify] https://crrev.com/89e11878b275b15735eaf273ababfa6fd43a2e3d/src/libANGLE/renderer/vulkan/BufferVk.cpp


### gi...@appspot.gserviceaccount.com (2021-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e0282162cdf5021d1f4ec58addfd516fdc7e8bd1

commit e0282162cdf5021d1f4ec58addfd516fdc7e8bd1
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Dec 16 02:06:35 2021

Roll ANGLE from 26fa0fe68b92 to 89e11878b275 (4 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/26fa0fe68b92..89e11878b275

2021-12-15 abdolrashidi@google.com Vulkan: Fix the UAF issue with BufferData
2021-12-15 gman@chromium.org Metal: Integrate Metal Binary Shader generation
2021-12-15 kpiddington@apple.com Metal: Fix macOS ANGLE build on Catalina (10.15) SDK
2021-12-15 abdolrashidi@google.com Vulkan: Set content undefined on eglSwapBuffers

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC timvp@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1274316
Tbr: timvp@google.com
Change-Id: I331c7a333e69d8b3d76b4d3543f27a086e71cbe5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3343606
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#952205}

[modify] https://crrev.com/e0282162cdf5021d1f4ec58addfd516fdc7e8bd1/DEPS


### [Deleted User] (2021-12-16)

jmadill: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2021-12-16)

[Empty comment from Monorail migration]

### jm...@chromium.org (2021-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-16)

Requesting merge to stable M96 because latest trunk commit (952205) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (952205) appears to be after beta branch point (938553).

Requesting merge to dev M98 because latest trunk commit (952205) appears to be after dev branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-16)

Merge review required: a commit with DEPS changes was detected.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-16)

Merge review required: a commit with DEPS changes was detected.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-16)

Merge review required: a commit with DEPS changes was detected.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2021-12-17)

ClusterFuzz testcase 5956867505061888 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=952204:952208

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### sr...@google.com (2021-12-22)

Pls help answer the https://crbug.com/chromium/1274316#c27 for merge review ( pls answer if this merge is needed for all 3 branches requested here)

### ab...@google.com (2021-12-29)

Hello,

1. It is a security fix.
2. Link: https://crrev.com/c/3321789
3. Yes. It is already merged to main and rolled in Chromium.
4. No, it is not a new feature.
5. N/A
6. No, security fix tests are automated.

### am...@chromium.org (2022-01-04)

Merge approved to M98, please merge to branch 4758 as soon as possible so this fix can be included this afternoon's beta cut. Thank you! 

### am...@chromium.org (2022-01-04)

Merge approved for M97, please merge to branch 4692 so this fix can be included in the next M97 stable security refresh. 
Merge also approved for M96, please merge to branch 4664 so this fix can be included in M96 now that it is in Extended support. Thank you! 

### gi...@appspot.gserviceaccount.com (2022-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/36386cd79b45c2d7140ad7992454e58ea9f9addd

commit 36386cd79b45c2d7140ad7992454e58ea9f9addd
Author: Amirali Abdolrashidi <abdolrashidi@google.com>
Date: Mon Dec 06 17:42:46 2021

[M98] Vulkan: Fix the UAF issue with BufferData

* Fixed the use-after-free issue with stale buffer handles
after calling BeginTransformFeedback.
  * Added an observer for TransformFeedbackVk to update the
buffer handles when buffer's storage is changed and the buffer
update type is StorageRedefined.
* Added a function to TransformFeedbackVk::onDestroy() to
release the counter buffers in order to avoid crash due to
TransformFeedbackVk::end() not being called, e.g., as a
result of no glEndTransformFeedback() calls.

Bug: chromium:1274316
Change-Id: I8ed477f36e6ff89dd4764bb59af564c69efe33e2
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3321789
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com>
(cherry picked from commit 89e11878b275b15735eaf273ababfa6fd43a2e3d)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3366997
Reviewed-by: Charlie Lao <cclao@google.com>

[modify] https://crrev.com/36386cd79b45c2d7140ad7992454e58ea9f9addd/src/libANGLE/Buffer.cpp
[modify] https://crrev.com/36386cd79b45c2d7140ad7992454e58ea9f9addd/src/libANGLE/renderer/vulkan/TransformFeedbackVk.cpp
[modify] https://crrev.com/36386cd79b45c2d7140ad7992454e58ea9f9addd/src/libANGLE/renderer/vulkan/TransformFeedbackVk.h
[modify] https://crrev.com/36386cd79b45c2d7140ad7992454e58ea9f9addd/src/libANGLE/Texture.cpp
[modify] https://crrev.com/36386cd79b45c2d7140ad7992454e58ea9f9addd/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/36386cd79b45c2d7140ad7992454e58ea9f9addd/src/libANGLE/VertexArray.cpp
[modify] https://crrev.com/36386cd79b45c2d7140ad7992454e58ea9f9addd/src/libANGLE/Observer.h
[modify] https://crrev.com/36386cd79b45c2d7140ad7992454e58ea9f9addd/src/tests/capture_replay_tests/capture_replay_expectations.txt
[modify] https://crrev.com/36386cd79b45c2d7140ad7992454e58ea9f9addd/src/libANGLE/renderer/vulkan/BufferVk.cpp


### gi...@appspot.gserviceaccount.com (2022-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa

commit 06187cbdaf533f2f0f8cdc59ff8296dc4c658efa
Author: Amirali Abdolrashidi <abdolrashidi@google.com>
Date: Mon Dec 06 17:42:46 2021

[M96] Vulkan: Fix the UAF issue with BufferData

* Fixed the use-after-free issue with stale buffer handles
after calling BeginTransformFeedback.
  * Added an observer for TransformFeedbackVk to update the
buffer handles when buffer's storage is changed and the buffer
update type is StorageRedefined.
* Added a function to TransformFeedbackVk::onDestroy() to
release the counter buffers in order to avoid crash due to
TransformFeedbackVk::end() not being called, e.g., as a
result of no glEndTransformFeedback() calls.

Bug: chromium:1274316
Change-Id: I8ed477f36e6ff89dd4764bb59af564c69efe33e2
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3321789
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com>
(cherry picked from commit 89e11878b275b15735eaf273ababfa6fd43a2e3d)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3366999
Reviewed-by: Charlie Lao <cclao@google.com>

[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/Buffer.cpp
[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/renderer/vulkan/TransformFeedbackVk.cpp
[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/renderer/vulkan/TransformFeedbackVk.h
[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/Texture.cpp
[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/VertexArray.cpp
[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/Observer.h
[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/renderer/vulkan/BufferVk.cpp


### gi...@appspot.gserviceaccount.com (2022-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/907d2234409b3507bbcf15f30177692f9204afaa

commit 907d2234409b3507bbcf15f30177692f9204afaa
Author: Amirali Abdolrashidi <abdolrashidi@google.com>
Date: Mon Dec 06 17:42:46 2021

[M97] Vulkan: Fix the UAF issue with BufferData

* Fixed the use-after-free issue with stale buffer handles
after calling BeginTransformFeedback.
  * Added an observer for TransformFeedbackVk to update the
buffer handles when buffer's storage is changed and the buffer
update type is StorageRedefined.
* Added a function to TransformFeedbackVk::onDestroy() to
release the counter buffers in order to avoid crash due to
TransformFeedbackVk::end() not being called, e.g., as a
result of no glEndTransformFeedback() calls.

Bug: chromium:1274316
Change-Id: I8ed477f36e6ff89dd4764bb59af564c69efe33e2
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3321789
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com>
(cherry picked from commit 89e11878b275b15735eaf273ababfa6fd43a2e3d)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3366998
Reviewed-by: Charlie Lao <cclao@google.com>

[modify] https://crrev.com/907d2234409b3507bbcf15f30177692f9204afaa/src/libANGLE/Buffer.cpp
[modify] https://crrev.com/907d2234409b3507bbcf15f30177692f9204afaa/src/libANGLE/renderer/vulkan/TransformFeedbackVk.cpp
[modify] https://crrev.com/907d2234409b3507bbcf15f30177692f9204afaa/src/libANGLE/renderer/vulkan/TransformFeedbackVk.h
[modify] https://crrev.com/907d2234409b3507bbcf15f30177692f9204afaa/src/libANGLE/Texture.cpp
[modify] https://crrev.com/907d2234409b3507bbcf15f30177692f9204afaa/src/libANGLE/VertexArray.cpp
[modify] https://crrev.com/907d2234409b3507bbcf15f30177692f9204afaa/src/libANGLE/Observer.h
[modify] https://crrev.com/907d2234409b3507bbcf15f30177692f9204afaa/src/libANGLE/renderer/vulkan/BufferVk.cpp


### gi...@appspot.gserviceaccount.com (2022-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa

commit 06187cbdaf533f2f0f8cdc59ff8296dc4c658efa
Author: Amirali Abdolrashidi <abdolrashidi@google.com>
Date: Mon Dec 06 17:42:46 2021

[M96] Vulkan: Fix the UAF issue with BufferData

* Fixed the use-after-free issue with stale buffer handles
after calling BeginTransformFeedback.
  * Added an observer for TransformFeedbackVk to update the
buffer handles when buffer's storage is changed and the buffer
update type is StorageRedefined.
* Added a function to TransformFeedbackVk::onDestroy() to
release the counter buffers in order to avoid crash due to
TransformFeedbackVk::end() not being called, e.g., as a
result of no glEndTransformFeedback() calls.

Bug: chromium:1274316
Change-Id: I8ed477f36e6ff89dd4764bb59af564c69efe33e2
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3321789
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com>
(cherry picked from commit 89e11878b275b15735eaf273ababfa6fd43a2e3d)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3366999
Reviewed-by: Charlie Lao <cclao@google.com>

[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/Buffer.cpp
[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/renderer/vulkan/TransformFeedbackVk.cpp
[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/renderer/vulkan/TransformFeedbackVk.h
[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/Texture.cpp
[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/VertexArray.cpp
[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/Observer.h
[modify] https://crrev.com/06187cbdaf533f2f0f8cdc59ff8296dc4c658efa/src/libANGLE/renderer/vulkan/BufferVk.cpp


### am...@google.com (2022-01-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-06)

And another one! Nice work, Cassidy Kim. The VRP Panel has decided to award you $5,000 for this report. Thank you for reporting this issue to us. 

### am...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1274316?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>GPU>ANGLE, Internals>GPU>Vulkan]
[Monorail mergedwith: crbug.com/chromium/1274317]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058051)*
