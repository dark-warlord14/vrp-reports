# UAF write in Dawn wire server: BufferUpdateMappedData writes to freed GPU memory after DeviceDestroy

| Field | Value |
|-------|-------|
| **Issue ID** | [492139412](https://issues.chromium.org/issues/492139412) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Wire |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | cw...@google.com |
| **Created** | 2026-03-12 |
| **Bounty** | $36,000.00 |

## Description

## Summary

A use-after-free write exists in the Dawn wire server running in the GPU process. When a compromised renderer sends a DeviceDestroy wire command followed by BufferUpdateMappedData for a buffer that was created with `mappedAtCreation`, the server performs a `memcpy` into GPU buffer memory that has already been freed during device destruction. The dangling pointer is a raw `uint8_t*` stored in the wire server's WriteHandle, which is not protected by `raw_ptr`, MiraclePtr, or any other mitigation. The attacker controls the write content (sourced from shared memory), offset, and size. This affects all platforms with WebGPU support.

## Bisect

Introducing Commit: `f93fa6acd96d77df9ef48f8f5ff78ea72cebf5ae` (Dawn)

- Date: 2020-07-29
- Author: Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)
- Review: <https://dawn-review.googlesource.com/c/dawn/+/25981>

This commit implemented `mappedAtCreation` in the Dawn wire server by calling `writeHandle->SetTarget(mapping, descriptor->size)` inside `DoDeviceCreateBuffer`. The raw pointer stored via `SetTarget` was never invalidated on the DeviceDestroy path, creating the dangling pointer condition. A later commit (`6e680fc56f`, 2021-07-08) extended WriteHandle lifetime to persist across map/unmap cycles, widening the exploitable window, but the root gap has existed since this original commit.

## Root Cause

Chromium's WebGPU implementation uses the Dawn wire protocol to relay GPU commands from the renderer process to the GPU process. When a renderer creates a buffer with `mappedAtCreation=true`, the wire server obtains a pointer to the native mapped memory and stores it in a `WriteHandle` via `SetTarget`:

```
// third_party/dawn/src/dawn/wire/server/ServerBuffer.cpp
writeHandle->SetTarget(mapping);
buffer->mapWriteState = BufferMapWriteState::Mapped;

```

`SetTarget` stores this as a bare `uint8_t*`:

```
// third_party/dawn/src/dawn/wire/WireServer.cpp
void MemoryTransferService::WriteHandle::SetTarget(void* data) {
    mTargetData = static_cast<uint8_t*>(data);
}

```

The field declaration confirms it is not wrapped in `raw_ptr` or any other safety abstraction:

```
// third_party/dawn/include/dawn/wire/WireServer.h
uint8_t* mTargetData = nullptr;
size_t mDataLength = 0;

```

When the renderer later sends a DeviceDestroy command, the wire server delegates directly to the native layer without cleaning up any per-buffer state:

```
// (auto-generated) third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp
WireResult Server::DoDeviceDestroy(WGPUDevice self) {
    mProcs->deviceDestroy(self);
    return WireResult::Success;
}

```

The native layer destroys all device-owned objects, including buffers. On Vulkan, this frees the underlying memory through the FencedDeleter:

```
// third_party/dawn/src/dawn/native/vulkan/BufferVk.cpp
void Buffer::DestroyImpl(DestroyReason reason) {
    BufferBase::DestroyImpl(reason);
    ToBackend(GetDevice())->GetResourceMemoryAllocator()->Deallocate(&mMemoryAllocation);
    if (mHandle != VK_NULL_HANDLE) {
        ToBackend(GetDevice())->GetFencedDeleter()->DeleteWhenUnused(mHandle);
        mHandle = VK_NULL_HANDLE;
    }
}

```

The FencedDeleter flushes all pending deletions during device teardown, calling `vkFreeMemory` which ultimately calls `free()` on the underlying heap allocation (in SwiftShader's case via `sw::freeMemory`).

After the memory is freed, the wire server's `buffer->writeHandle` still holds the stale `mTargetData` pointer, and `buffer->mapWriteState` is still `BufferMapWriteState::Mapped`. A subsequent BufferUpdateMappedData command passes all validation checks and reaches the `memcpy`:

```
// gpu/command_buffer/service/dawn_service_memory_transfer_service.cc
bool WriteHandleImpl::DeserializeDataUpdate(const void* deserialize_pointer,
                                            size_t deserialize_size,
                                            size_t offset,
                                            size_t size) {
    // ...bounds checks against targetData and buffer_data_view_...
    UNSAFE_TODO(memcpy(static_cast<uint8_t*>(targetData.data()) + offset,
                       buffer_data_view_.data() + offset, size));
    return true;
}

```

The `targetData` comes from `GetTarget()`, which returns a span over `mTargetData`, the now-dangling pointer. The source data (`buffer_data_view_`) points into renderer-controlled shared memory.

The gap exists because `PreHandleBufferDestroy` does clean up the WriteHandle on individual buffer destruction, but `DoDeviceDestroy` does not invoke equivalent cleanup for each buffer owned by the device. There is no iteration over associated buffers, no clearing of `writeHandle`, and no resetting of `mapWriteState`.

A compromised renderer exploits this by reordering the wire commands. In normal Blink code, `GPUDevice::destroy()` calls `UnmapAllMappableBuffers()` (which sends BufferUpdateMappedData) before `GetHandle().Destroy()` (which sends DeviceDestroy). By reversing this order, the renderer ensures DeviceDestroy frees the memory before BufferUpdateMappedData writes to it.

## Reproduce

Tested on commit `3484f09b1620f6b7198fda97caf21b822d3df8ff` on macOS and Ubuntu 22.04. This vulnerability exists on all platforms that support WebGPU (Windows, macOS, Linux, ChromeOS, Android).

Configure an ASAN build. A minimal `args.gn` for `out/asan`:

```
is_asan = true
is_debug = false
is_component_build = false

```

Build Chrome:

```
git apply patch.diff
autoninja -C out/asan chrome

```

Run Chrome:

```
# macOS
out/asan/Chromium.app/Contents/MacOS/Chromium --user-data-dir=./userdata poc.html

# Linux
out/asan/chrome --enable-unsafe-webgpu --user-data-dir=./userdata poc.html

```

On macOS, the native Metal backend allocates GPU buffer memory through `vm_allocate`/IOKit mapped memory, which lives outside the heap regions that ASAN instruments. When the buffer is destroyed and the VM pages are reclaimed by the OS, the subsequent `memcpy` hits unmapped virtual memory and produces a SEGV rather than an ASAN report. On Linux, `--enable-unsafe-webgpu` selects SwiftShader as the Vulkan backend. SwiftShader allocates GPU buffer memory via `malloc` (through `sw::allocateZeroOrPoison`), which ASAN fully instruments, so the dangling write produces a proper heap-use-after-free report. To obtain an ASAN report on macOS, pass `--use-webgpu-adapter=swiftshader --enable-unsafe-webgpu` to force the SwiftShader backend.

SEGV on macOS (native Metal backend):

```
Received signal 11 SEGV_ACCERR 0001341f4000
 [0x00035c2633c8]
 [0x00035c237198]
 [0x00035c2631fc]
 [0x000180743744]
 [0x000104a41994]
 [0x0003623fe9dc]
 [0x0003623c0ee0]
 [0x0003623cd95c]
 [0x0003623d712c]
 [0x00036240ada4]
 [0x00036240b1a8]
 [0x000362401144]
 [0x000351a5af0c]
 [0x000362316cc0]
 [0x000362315e10]
 [0x00036233470c]
 [0x0003623403ac]
 [0x0003623401c4]
 [0x000351a93d5c]
 [0x000351a6e83c]
 [0x000351a6ced4]
 [0x000351a70270]
 [0x00035c0fb574]
 [0x00035c163318]
 [0x00035c1626d0]
 [0x00035c284a8c]
 [0x00035c2761d8]
 [0x00035c282edc]
 [0x0001807d89f8]
 [0x0001807d898c]
 [0x0001807d86f8]
 [0x0001807d7388]
 [0x000180891e34]
 [0x000182a26964]
 [0x00035c285bdc]
 [0x00035c281c44]
 [0x00035c164678]
 [0x00035c089820]
 [0x00036546ae9c]
 [0x0003587c9b64]
 [0x0003587cbce4]
 [0x0003587c7854]
 [0x0003587c7d44]
 [0x000349c4dcb8]
 [0x000104640c98]
 [0x000180371d54]
[end of stack trace]

```

ASAN output on Linux (SwiftShader backend via `--enable-unsafe-webgpu`):

```
=================================================================
==154737==ERROR: AddressSanitizer: heap-use-after-free on address 0x71787d175900 at pc 0x5eec4ca260ae bp 0x7ffe523cc350 sp 0x7ffe523cbb10
WRITE of size 16777216 at 0x71787d175900 thread T0 (chrome)
    #0 0x5eec4ca260ad in __asan_memcpy (/home/test/Desktop/chromium/src/out/asan/chrome+0x10e810ad) (BuildId: 285b4624b4b2a3a5)
    #1 0x5eec6e07c0a4 in gpu::webgpu::(anonymous namespace)::WriteHandleImpl::DeserializeDataUpdate(void const*, unsigned long, unsigned long, unsigned long) gpu/command_buffer/service/dawn_service_memory_transfer_service.cc:123:17
    #2 0x5eec6e0c9709 in dawn::wire::server::Server::DoBufferUpdateMappedData(dawn::wire::server::Known<WGPUBufferImpl*>, unsigned long, unsigned char const*, unsigned long, unsigned long) third_party/dawn/src/dawn/wire/server/ServerBuffer.cpp:248:37
    #3 0x5eec6e0a68eb in dawn::wire::server::Server::HandleBufferUpdateMappedData(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:101:18
    #4 0x5eec6e0b1c8a in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1676:30
    #5 0x5eec6e06c317 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:155:33
    #6 0x5eec6e06c78d in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1988:22
    #7 0x5eec6e060682 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1933:18
    #8 0x5eec5763b814 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:267:35
    #9 0x5eec6d79a62b in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:504:22
    #10 0x5eec6d799891 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:173:7
    #11 0x5eec6d7bc97c in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:833:13
    #12 0x5eec6d7ca967 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #13 0x5eec6d7ca749 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #14 0x5eec5767e211 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/callback.h:155:12
    #15 0x5eec57652957 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) base/functional/callback.h:155:12
    #16 0x5eec57650988 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:625:3
    #17 0x5eec57654571 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #18 0x5eec64210c76 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #19 0x5eec64288459 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #20 0x5eec642872ca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #21 0x5eec64435e74 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:782:48
    #22 0x5eec64289b67 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #23 0x5eec6418c210 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #24 0x5eec6fb5379c in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:479:14
    #25 0x5eec5fe67e3f in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #26 0x5eec5fe6916f in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #27 0x5eec5fe6be78 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #28 0x5eec5fe65851 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #29 0x5eec5fe65e4c in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #30 0x5eec4ca62b39 in ChromeMain chrome/app/chrome_main.cc:191:12
    #31 0x757a1a229d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x71787d175900 is located 256 bytes inside of 16777495-byte region [0x71787d175800,0x71787e175917)
freed by thread T0 (chrome) here:
    #0 0x5eec4ca28086 in free (/home/test/Desktop/chromium/src/out/asan/chrome+0x10e83086) (BuildId: 285b4624b4b2a3a5)
    #1 0x71789987f42c in vk::DeviceMemory::freeBuffer() third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:354:2
    #2 0x71789987f1f8 in vk::DeviceMemory::destroy(VkAllocationCallbacks const*) third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:162:3
    #3 0x7178998d37af in vkFreeMemory third_party/swiftshader/src/Vulkan/VkDestroy.hpp:61:11
    #4 0x5eec4ec44fcf in dawn::native::vulkan::FencedDeleter::UpdateCompletedSerialTo(unsigned long) third_party/dawn/src/dawn/native/vulkan/FencedDeleter.cpp:88:30
    #5 0x5eec4e8fd68f in dawn::native::ExecutionQueueBase::WaitForIdleForDestruction() third_party/dawn/src/dawn/native/ExecutionQueue.cpp:184:24
    #6 0x5eec4e883c05 in dawn::native::DeviceBase::Destroy(dawn::native::DestroyReason) third_party/dawn/src/dawn/native/Device.cpp:681:34
    #7 0x5eec4e71e8a2 in dawn::native::NativeDeviceDestroy(WGPUDeviceImpl*) gen/third_party/dawn/src/dawn/native/ProcTable.cpp:946:15
    #8 0x5eec6e0be92d in dawn::wire::server::Server::DoDeviceDestroy(WGPUDeviceImpl*) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:494:9
    #9 0x5eec6e0b323b in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:692:18
    #10 0x5eec6e06c317 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:155:33
    #11 0x5eec6e06c78d in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1988:22
    #12 0x5eec6e060682 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1933:18
    #13 0x5eec5763b814 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:267:35
    #14 0x5eec6d79a62b in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:504:22
    #15 0x5eec6d799891 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:173:7
    #16 0x5eec6d7bc97c in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:833:13
    #17 0x5eec6d7ca967 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #18 0x5eec6d7ca749 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #19 0x5eec5767e211 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/callback.h:155:12
    #20 0x5eec57652957 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) base/functional/callback.h:155:12
    #21 0x5eec57650988 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:625:3
    #22 0x5eec57654571 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #23 0x5eec64210c76 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #24 0x5eec64288459 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #25 0x5eec642872ca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #26 0x5eec64435538 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:736:46
    #27 0x5eec64438af8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:355:43
    #28 0x757a1b72dd3a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x55d3a) (BuildId: 6b4f160dbc5397c2f502dc4f08a8cff259917926)

previously allocated by thread T0 (chrome) here:
    #0 0x5eec4ca28324 in malloc (/home/test/Desktop/chromium/src/out/asan/chrome+0x10e83324) (BuildId: 285b4624b4b2a3a5)
    #1 0x717899d6bf1d in sw::allocateZeroOrPoison(unsigned long, unsigned long) third_party/swiftshader/src/System/Memory.cpp:81:42
    #2 0x71789987f3c4 in vk::DeviceMemory::allocateBuffer() third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:342:11
    #3 0x71789987e024 in vk::DeviceMemory::Allocate(VkAllocationCallbacks const*, VkMemoryAllocateInfo const*, VkNonDispatchableHandle<VkDeviceMemory_T*>*, vk::Device*) third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:275:12
    #4 0x7178998d36a7 in vkAllocateMemory third_party/swiftshader/src/Vulkan/libVulkan.cpp:1421:20
    #5 0x5eec4eca20a9 in dawn::native::vulkan::ResourceMemoryAllocator::SingleTypeAllocator::AllocateResourceHeap(unsigned long) third_party/dawn/src/dawn/native/vulkan/ResourceMemoryAllocatorVk.cpp:113:35
    #6 0x5eec4ec9ebfa in dawn::native::vulkan::ResourceMemoryAllocator::Allocate(VkMemoryRequirements const&, dawn::native::vulkan::MemoryKind, bool) third_party/dawn/src/dawn/native/vulkan/ResourceMemoryAllocatorVk.cpp:241:67
    #7 0x5eec4ec03eb2 in dawn::native::vulkan::Buffer::Initialize(bool) third_party/dawn/src/dawn/native/vulkan/BufferVk.cpp:293:59
    #8 0x5eec4ec02ca6 in dawn::native::vulkan::Buffer::Create(dawn::native::vulkan::Device*, dawn::native::UnpackedPtr<dawn::native::BufferDescriptor> const&) third_party/dawn/src/dawn/native/vulkan/BufferVk.cpp:219:26
    #9 0x5eec4ec316b7 in dawn::native::vulkan::Device::CreateBufferImpl(dawn::native::UnpackedPtr<dawn::native::BufferDescriptor> const&) third_party/dawn/src/dawn/native/vulkan/DeviceVk.cpp:213:12
    #10 0x5eec4e88e50b in dawn::native::DeviceBase::APICreateBuffer(dawn::native::BufferDescriptor const*) third_party/dawn/src/dawn/native/Device.cpp:1339:20
    #11 0x5eec6e0c8c2c in dawn::wire::server::Server::DoDeviceCreateBuffer(dawn::wire::server::Known<WGPUDeviceImpl*>, WGPUBufferDescriptor const*, dawn::wire::ObjectHandle, unsigned long, unsigned char const*, unsigned long, unsigned char const*) third_party/dawn/src/dawn/wire/server/ServerBuffer.cpp:142:22
    #12 0x5eec6e0a831c in dawn::wire::server::Server::HandleDeviceCreateBuffer(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:463:18
    #13 0x5eec6e0b0648 in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1778:30
    #14 0x5eec6e06c317 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:155:33
    #15 0x5eec6e06c78d in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1988:22
    #16 0x5eec6e060682 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1933:18
    #17 0x5eec5763b814 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:267:35
    #18 0x5eec6d79a62b in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:504:22
    #19 0x5eec6d799891 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:173:7
    #20 0x5eec6d7bc97c in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:833:13
    #21 0x5eec6d7ca967 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #22 0x5eec6d7ca749 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #23 0x5eec5767e211 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/callback.h:155:12
    #24 0x5eec57652957 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) base/functional/callback.h:155:12
    #25 0x5eec57650988 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:625:3
    #26 0x5eec57654571 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #27 0x5eec64210c76 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #28 0x5eec64288459 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #29 0x5eec642872ca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40

SUMMARY: AddressSanitizer: heap-use-after-free (/home/test/Desktop/chromium/src/out/asan/chrome+0x10e810ad) (BuildId: 285b4624b4b2a3a5) in __asan_memcpy
Shadow bytes around the buggy address:
  0x71787d175680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71787d175700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x71787d175780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x71787d175800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71787d175880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x71787d175900:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71787d175980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71787d175a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71787d175a80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71787d175b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x71787d175b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==154737==ADDITIONAL INFO

==154737==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5eec57650e62 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #1 0x5eec57650e62 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #2 0x5eec57650e62 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #3 0x5eec57650e62 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==154737==END OF ADDITIONAL INFO

==154737==ABORTING
[154700:154700:0312/225514.129998:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256

```
## Credit

Please use 86ac1f1587b71893ed2ad792cd7dde32 as the credit for this vulnerability. Thank you.

## Attachments

- [patch.diff](attachments/patch.diff) (text/x-diff, 893 B)
- [poc.html](attachments/poc.html) (text/html, 2.1 KB)

## Timeline

### ch...@google.com (2026-03-13)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-13)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### cw...@chromium.org (2026-03-13)

Loko, I'm taking this to help lighten the load since you've been handling a lot of wire security reports lately.

### dx...@google.com (2026-03-15)

Project: dawn  

Branch:  main  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://dawn-review.googlesource.com/297055>

[dawn] Add more tests of buffer mapping and device loss/destroy

---


Expand for full commit details
```
     
    Bug: 42240407, 492139412 
    Change-Id: Ifef5b6a0e0219c7833a364b629d03b357ed42b89 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297055 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org>

```

---

Files:

- M `src/dawn/tests/end2end/DeviceLostTests.cpp`
- M `src/dawn/tests/unittests/validation/BufferValidationTests.cpp`
- M `src/dawn/tests/unittests/validation/CommandBufferValidationTests.cpp`

---

Hash: 851ba3e50c354ef66d16c518d4341c01ed6828cc  

Date: Sun Mar 15 14:14:08 2026


---

### dx...@google.com (2026-03-15)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7668790>

Roll Dawn from b97879f37cc8 to 851ba3e50c35 (1 revision)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/b97879f37cc8..851ba3e50c35 
     
    2026-03-15 cwallez@chromium.org [dawn] Add more tests of buffer mapping and device loss/destroy 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,gman@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:42240407,chromium:492139412 
    Tbr: gman@google.com 
    Change-Id: I49fa86ab14b619b9b9a8c6e09c51b69a1b85a890 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7668790 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1599616}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [463b27830193ed972008920b8102b10801baa812](https://chromiumdash.appspot.com/commit/463b27830193ed972008920b8102b10801baa812)  

Date: Sun Mar 15 16:54:32 2026


---

### dx...@google.com (2026-03-20)

Project: dawn  

Branch:  main  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://dawn-review.googlesource.com/297036>

[dawn][wire] Put most of the wire in a source\_set.

---


Expand for full commit details
```
     
    And change dawn_unittests to use the static version of dawn_wire, such 
    that in a follow-up CL it can test using its internals directly instead 
    of having to only rely on the public interface. 
     
    Bug: 492139412 
    Change-Id: I43a26073382545d7502b8765c78525ea040812c3 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297036 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Loko Kung <lokokung@google.com>

```

---

Files:

- M `generator/templates/dawn/wire/client/ApiProcs.cpp`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/utils/BUILD.gn`
- M `src/dawn/wire/BUILD.gn`
- M `src/dawn/wire/WireClient.cpp`

---

Hash: a703d864e29f6765f7dfcea0a2531afea02bee70  

Date: Fri Mar 20 11:25:32 2026


---

### dx...@google.com (2026-03-22)

Project: dawn  

Branch:  main  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://dawn-review.googlesource.com/296817>

[dawn][wire] Check that buffer is mapped in DeserializeDataUpdate.

---


Expand for full commit details
```
     
    Previously the target of the WriteHandle for a buffer was set as soon as 
    the buffer is mapped. Between the time it was first mapped and the time 
    DeserializeDataUpdate was called (right before Unmap), the buffer could 
    be implicitly unmapped by a call to Device::Destroy. 
     
     - Instead check for the buffer being mapped directly in 
       DeserializeDataUpdate, which remove the need to track a mapWriteState 
       on the ObjectData<WGPUBuffer>. 
     - Update the change detecting WireTests to account to GetMappedRange 
       being done in a different place now for writable buffers. 
     - Add a new test that allows injecting WireCmds directly for even more 
       precise but even more change detecting tests. 
     - Add necessary backdoors to WireClient and WireTest need for the new 
       tests. 
     - Link dawn::wire statically in dawn_unittests as we now need to use 
       some of its internals directly. 
     
    Bug: 492139412 
    Change-Id: Ibe9ab95ae7456c6629434d4978f439ebfe41c4d1 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/296817 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org>

```

---

Files:

- M `include/dawn/wire/WireClient.h`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/tests/unittests/wire/WireBufferMappingTests.cpp`
- M `src/dawn/tests/unittests/wire/WireMemoryTransferServiceTests.cpp`
- A `src/dawn/tests/unittests/wire/WireSpecificCommandTests.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/wire/WireClient.cpp`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/ServerBuffer.cpp`

---

Hash: e0a5e719c91ae3b60b3fc3d6d407b55e19337be4  

Date: Sun Mar 22 19:04:12 2026


---

### dx...@google.com (2026-03-23)

Project: dawn  

Branch:  main  

Author:  James Price [jrprice@google.com](mailto:jrprice@google.com)  

Link:    <https://dawn-review.googlesource.com/298815>

Revert "[dawn][wire] Check that buffer is mapped in DeserializeDataUpdate."

---


Expand for full commit details
```
     
    This reverts commit e0a5e719c91ae3b60b3fc3d6d407b55e19337be4. 
     
    Reason for revert: parent change is breaking Dawn->Chromium roll 
     
    Original change's description: 
    > [dawn][wire] Check that buffer is mapped in DeserializeDataUpdate. 
    > 
    > Previously the target of the WriteHandle for a buffer was set as soon as 
    > the buffer is mapped. Between the time it was first mapped and the time 
    > DeserializeDataUpdate was called (right before Unmap), the buffer could 
    > be implicitly unmapped by a call to Device::Destroy. 
    > 
    >  - Instead check for the buffer being mapped directly in 
    >    DeserializeDataUpdate, which remove the need to track a mapWriteState 
    >    on the ObjectData<WGPUBuffer>. 
    >  - Update the change detecting WireTests to account to GetMappedRange 
    >    being done in a different place now for writable buffers. 
    >  - Add a new test that allows injecting WireCmds directly for even more 
    >    precise but even more change detecting tests. 
    >  - Add necessary backdoors to WireClient and WireTest need for the new 
    >    tests. 
    >  - Link dawn::wire statically in dawn_unittests as we now need to use 
    >    some of its internals directly. 
    > 
    > Bug: 492139412 
    > Change-Id: Ibe9ab95ae7456c6629434d4978f439ebfe41c4d1 
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/296817 
    > Reviewed-by: Loko Kung <lokokung@google.com> 
    > Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
     
    TBR=cwallez@chromium.org,amaiorano@google.com,dawn-scoped@luci-project-accounts.iam.gserviceaccount.com,lokokung@google.com 
     
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Bug: 492139412 
    Change-Id: I0424b5ca40aae5836d5019a7a03b1855e5fdb5a7 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/298815 
    Reviewed-by: James Price <jrprice@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Commit-Queue: James Price <jrprice@google.com>

```

---

Files:

- M `include/dawn/wire/WireClient.h`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/tests/unittests/wire/WireBufferMappingTests.cpp`
- M `src/dawn/tests/unittests/wire/WireMemoryTransferServiceTests.cpp`
- D `src/dawn/tests/unittests/wire/WireSpecificCommandTests.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/wire/WireClient.cpp`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/ServerBuffer.cpp`

---

Hash: 05fe218e6d78ac6ed8b7159079f1623c1eb2d4f5  

Date: Mon Mar 23 15:11:43 2026


---

### dx...@google.com (2026-03-23)

Project: dawn  

Branch:  main  

Author:  James Price [jrprice@google.com](mailto:jrprice@google.com)  

Link:    <https://dawn-review.googlesource.com/298835>

Revert "[dawn][wire] Put most of the wire in a source\_set."

---


Expand for full commit details
```
     
    This reverts commit a703d864e29f6765f7dfcea0a2531afea02bee70. 
     
    Reason for revert: breaking Dawn->Chromium roll 
     
    Original change's description: 
    > [dawn][wire] Put most of the wire in a source_set. 
    > 
    > And change dawn_unittests to use the static version of dawn_wire, such 
    > that in a follow-up CL it can test using its internals directly instead 
    > of having to only rely on the public interface. 
    > 
    > Bug: 492139412 
    > Change-Id: I43a26073382545d7502b8765c78525ea040812c3 
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297036 
    > Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    > Reviewed-by: Loko Kung <lokokung@google.com> 
     
    # Not skipping CQ checks because original CL landed > 1 day ago. 
     
    Bug: 492139412 
    Change-Id: I7d39f1d9570cc502140cbc5c4765ba7d69c2f1a0 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/298835 
    Reviewed-by: James Price <jrprice@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Commit-Queue: James Price <jrprice@google.com>

```

---

Files:

- M `generator/templates/dawn/wire/client/ApiProcs.cpp`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/utils/BUILD.gn`
- M `src/dawn/wire/BUILD.gn`
- M `src/dawn/wire/WireClient.cpp`

---

Hash: eeff706d177ccc2a4db6ce3e91e61f2a70bdf785  

Date: Mon Mar 23 17:54:07 2026


---

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7694813>

Roll Dawn from 7d5e33062472 to 7f10515939a5 (31 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/7d5e33062472..7f10515939a5 
     
    2026-03-23 petermcneeley@google.com [tint] Remove duplicate lowering 
    2026-03-23 chouinard@google.com [hlsl] Use Result for new var_let_test tests 
    2026-03-23 jrprice@google.com Revert "[dawn][wire] Put most of the wire in a source_set." 
    2026-03-23 lokokung@google.com [dawn][native] Make EventManager::SetFutureReady take Ref<TrackedEvent>. 
    2026-03-23 jrprice@google.com [hlsl] Run CanGenerate() from Generate() 
    2026-03-23 jrprice@google.com [hlsl] Use Result for writer test helpers 
    2026-03-23 dawn-automated-expectations@chops-service-accounts.iam.gserviceaccount.com Roll third_party/webgpu-cts/ e135cc01e..9726cfe28 (3 commits) 
    2026-03-23 shanxing.mei@intel.com Add u16 in HLSL to fix WebGPU CTS memory_layout non-atomic issue 
    2026-03-23 jrprice@google.com Revert "[dawn][wire] Check that buffer is mapped in DeserializeDataUpdate." 
    2026-03-23 jrprice@google.com [hlsl] Rework binding options validation 
    2026-03-23 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 7d3330d9ed24 to 2cb8be8f2979 (851 revisions) 
    2026-03-23 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 0d2e0efef5f2 to f9b475aa7134 (16 revisions) 
    2026-03-23 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from 8715c233439f to d05ec6ac7d97 (16 revisions) 
    2026-03-22 cwallez@chromium.org [dawn][wire] Check that buffer is mapped in DeserializeDataUpdate. 
    2026-03-22 alanbaker@google.com [wgsl] Add inter-function bufferView checks 
    2026-03-21 chrome-automated-expectation@chops-service-accounts.iam.gserviceaccount.com Remove stale WebGPU Compat CTS expectations 
    2026-03-21 alanbaker@google.com [wgsl] Add bufferArrayView builtin function 
    2026-03-21 lokokung@google.com [dawn][native] Tighten MapMode validation to check for values. 
    2026-03-20 cwallez@chromium.org [YUV AHB] Add a BGL getter for the expected BGDesc entry count. 
    2026-03-20 cwallez@chromium.org [bindless] Suppress ResourceTableTests on Swiftshader 
    2026-03-20 cwallez@chromium.org [YUV AHB] Make vulkan::BGL return the full TextureToStaticSamplerMap 
    2026-03-20 cwallez@chromium.org [YUV AHB] Make GetNoopRGBColorSpaceConversionInfo support YUV 
    2026-03-20 cwallez@chromium.org [YUV AHB] Fix STMAHB test errors on Pixel 10. 
    2026-03-20 chouinard@google.com Disable HostMappedPointer on AMD 
    2026-03-20 dawn-automated-expectations@chops-service-accounts.iam.gserviceaccount.com Roll third_party/webgpu-cts/ 5ca78e551..e135cc01e (1 commit) 
    2026-03-20 cwallez@chromium.org [dawn][wire] Put most of the wire in a source_set. 
    2026-03-20 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from e65fb3bf6dc6 to 0d2e0efef5f2 (14 revisions) 
    2026-03-20 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from aef03d88aba5 to 8715c233439f (13 revisions) 
    2026-03-20 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll DirectX Shader Compiler from 21f060b7138e to 54afd2c6a5f1 (4 revisions) 
    2026-03-20 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 82da30b07f25 to 7d3330d9ed24 (654 revisions) 
    2026-03-20 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 313545f85af7 to 89556131bf9d (1 revision) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,jrprice@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:0000,chromium:341991439,chromium:458102548,chromium:467330780,chromium:468988322,chromium:474820386,chromium:487349982,chromium:491515775,chromium:492139412,chromium:492403441,chromium:494566064 
    Tbr: jrprice@google.com 
    Change-Id: I669d8a387e6a91ee10afbbb3ea0ce3c14d007802 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7694813 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1603812}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [9a9288746a0534deea815fdc3523b0651517a072](https://chromiumdash.appspot.com/commit/9a9288746a0534deea815fdc3523b0651517a072)  

Date: Tue Mar 24 00:31:55 2026


---

### dx...@google.com (2026-03-24)

Project: dawn  

Branch:  main  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://dawn-review.googlesource.com/299075>

Reland "[dawn][wire] Put most of the wire in a source\_set."

---


Expand for full commit details
```
     
    This is a reland of commit a703d864e29f6765f7dfcea0a2531afea02bee70 
     
    Instead of special-casing GetProc from ApiProcs_autogen.cpp to be 
    exported, make that whole file part of the exported API (by making it a 
    .inc that's inlined in WireClient.cpp). 
     
    Original change's description: 
    > [dawn][wire] Put most of the wire in a source_set. 
    > 
    > And change dawn_unittests to use the static version of dawn_wire, such 
    > that in a follow-up CL it can test using its internals directly instead 
    > of having to only rely on the public interface. 
    > 
    > Bug: 492139412 
    > Change-Id: I43a26073382545d7502b8765c78525ea040812c3 
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297036 
    > Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    > Reviewed-by: Loko Kung <lokokung@google.com> 
     
    Bug: 492139412 
    Change-Id: I9b99bcc46685b99ab2a9248f9d81cdb914bc945d 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299075 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com> 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org>

```

---

Files:

- M `generator/dawn_json_generator.py`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/utils/BUILD.gn`
- M `src/dawn/wire/BUILD.gn`
- M `src/dawn/wire/WireClient.cpp`

---

Hash: baea44be7bedb6309d9c6ee3f5ff1ee6b2b093f7  

Date: Tue Mar 24 11:18:55 2026


---

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7695896>

Roll Dawn from 0fe2d0a6b84c to baea44be7bed (5 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/0fe2d0a6b84c..baea44be7bed 
     
    2026-03-24 cwallez@chromium.org Reland "[dawn][wire] Put most of the wire in a source_set." 
    2026-03-24 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from f9b475aa7134 to eb9aff58b383 (10 revisions) 
    2026-03-24 cwallez@chromium.org [YUV AHB] STMAHB: Set YCbCrInfo so that it gets in the STMContents 
    2026-03-24 cwallez@chromium.org [YUV AHB] Rework CreateSamplerYCbCrConversion interface 
    2026-03-24 cwallez@chromium.org [YUV AHB] Fix ExternalTextureTests quad drawing. 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,jrprice@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:468988322,chromium:489325170,chromium:492139412 
    Tbr: jrprice@google.com 
    Change-Id: Id0a4302823077036053ef3e7aba62f8c66eb3e94 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7695896 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1604052}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [f4ca5d2f5c6c8666dbf2ce465c6d0c0f4105b049](https://chromiumdash.appspot.com/commit/f4ca5d2f5c6c8666dbf2ce465c6d0c0f4105b049)  

Date: Tue Mar 24 12:57:24 2026


---

### dx...@google.com (2026-03-24)

Project: dawn  

Branch:  main  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://dawn-review.googlesource.com/299215>

Reland "[dawn][wire] Check that buffer is mapped in DeserializeDataUpdate."

---


Expand for full commit details
```
     
    This is a reland of commit e0a5e719c91ae3b60b3fc3d6d407b55e19337be4 
     
    Original change's description: 
    > [dawn][wire] Check that buffer is mapped in DeserializeDataUpdate. 
    > 
    > Previously the target of the WriteHandle for a buffer was set as soon as 
    > the buffer is mapped. Between the time it was first mapped and the time 
    > DeserializeDataUpdate was called (right before Unmap), the buffer could 
    > be implicitly unmapped by a call to Device::Destroy. 
    > 
    >  - Instead check for the buffer being mapped directly in 
    >    DeserializeDataUpdate, which remove the need to track a mapWriteState 
    >    on the ObjectData<WGPUBuffer>. 
    >  - Update the change detecting WireTests to account to GetMappedRange 
    >    being done in a different place now for writable buffers. 
    >  - Add a new test that allows injecting WireCmds directly for even more 
    >    precise but even more change detecting tests. 
    >  - Add necessary backdoors to WireClient and WireTest need for the new 
    >    tests. 
    >  - Link dawn::wire statically in dawn_unittests as we now need to use 
    >    some of its internals directly. 
    > 
    > Bug: 492139412 
    > Change-Id: Ibe9ab95ae7456c6629434d4978f439ebfe41c4d1 
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/296817 
    > Reviewed-by: Loko Kung <lokokung@google.com> 
    > Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
     
    Bug: 492139412 
    Change-Id: Ie60fe8d418299335fb2ec13d673be0a4776c32be 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299215 
    Auto-Submit: Corentin Wallez <cwallez@chromium.org> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com> 
    Commit-Queue: Antonio Maiorano <amaiorano@google.com>

```

---

Files:

- M `include/dawn/wire/WireClient.h`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/tests/unittests/wire/WireBufferMappingTests.cpp`
- M `src/dawn/tests/unittests/wire/WireMemoryTransferServiceTests.cpp`
- A `src/dawn/tests/unittests/wire/WireSpecificCommandTests.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/wire/WireClient.cpp`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/ServerBuffer.cpp`

---

Hash: 4ba836a41006884c55731c72a1ba730d76cfb993  

Date: Tue Mar 24 14:55:36 2026


---

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7695689>

Roll Dawn from baea44be7bed to 5e0b99b59ef8 (4 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/baea44be7bed..5e0b99b59ef8 
     
    2026-03-24 dsinclair@chromium.org Add configuration data for third_party/webgpu-headers. 
    2026-03-24 cwallez@chromium.org Reland "[dawn][wire] Check that buffer is mapped in DeserializeDataUpdate." 
    2026-03-24 dsinclair@chromium.org Move GLFW to the standard 3p layout 
    2026-03-24 mridulgoyal@google.com [WebGPU][Kotlin] Simplify generated enum code 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,jrprice@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:492139412,chromium:493761823,chromium:493762911 
    Tbr: jrprice@google.com 
    Change-Id: Id7074a7c8cefec319efcd0629a240f7a59642a89 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7695689 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1604296}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [384ff0c56ccc7afd716ffd086baabfe5fb330373](https://chromiumdash.appspot.com/commit/384ff0c56ccc7afd716ffd086baabfe5fb330373)  

Date: Tue Mar 24 19:24:14 2026


---

### 24...@project.gserviceaccount.com (2026-03-25)

ClusterFuzz testcase 6625811285180416 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan_debug&range=1604292:1604344

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-03-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### cw...@chromium.org (2026-03-25)

Waiting until tomorrow to ask for the merge to see how Canary is doing.

### ch...@google.com (2026-03-27)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-27)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### cw...@chromium.org (2026-03-27)

Re #19

1. This is an important security issue.
2. <https://dawn-review.googlesource.com/299075> and <https://dawn-review.googlesource.com/299215>
3. Yes, 3 days ago
4. No
5. N/A
6. No

Re #20

1. This is an important security issue.
2. <https://dawn-review.googlesource.com/299075> and <https://dawn-review.googlesource.com/299215>
3. Yes, 3 days ago
4. No
5. N/A
6. No

### dr...@chromium.org (2026-03-27)

No crashes in Canary after 24 hours. Approved to merge to M146 and M147. Our release cut for M146 is Monday at 11am Pacific time, so please try to land by then.

### dx...@google.com (2026-03-27)

Project: dawn  

Branch:  chromium/7680  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://dawn-review.googlesource.com/299995>

[M146] Reland "[dawn][wire] Put most of the wire in a source\_set."

---


Expand for full commit details
```
     
    This is a reland of commit a703d864e29f6765f7dfcea0a2531afea02bee70 
     
    Instead of special-casing GetProc from ApiProcs_autogen.cpp to be 
    exported, make that whole file part of the exported API (by making it a 
    .inc that's inlined in WireClient.cpp). 
     
    Original change's description: 
    > [dawn][wire] Put most of the wire in a source_set. 
    > 
    > And change dawn_unittests to use the static version of dawn_wire, such 
    > that in a follow-up CL it can test using its internals directly instead 
    > of having to only rely on the public interface. 
    > 
    > Bug: 492139412 
    > Change-Id: I43a26073382545d7502b8765c78525ea040812c3 
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297036 
    > Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    > Reviewed-by: Loko Kung <lokokung@google.com> 
     
    Bug: 492139412 
    Change-Id: I9b99bcc46685b99ab2a9248f9d81cdb914bc945d 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299075 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com> 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    (cherry picked from commit baea44be7bedb6309d9c6ee3f5ff1ee6b2b093f7) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299995

```

---

Files:

- M `generator/dawn_json_generator.py`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/utils/BUILD.gn`
- M `src/dawn/wire/BUILD.gn`
- M `src/dawn/wire/WireClient.cpp`

---

Hash: f11011937c1b00c58d92454a9a322108f8b8ba68  

Date: Fri Mar 27 21:57:24 2026


---

### dx...@google.com (2026-03-27)

Project: dawn  

Branch:  chromium/7727  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://dawn-review.googlesource.com/300015>

[M147] Reland "[dawn][wire] Put most of the wire in a source\_set."

---


Expand for full commit details
```
     
    This is a reland of commit a703d864e29f6765f7dfcea0a2531afea02bee70 
     
    Instead of special-casing GetProc from ApiProcs_autogen.cpp to be 
    exported, make that whole file part of the exported API (by making it a 
    .inc that's inlined in WireClient.cpp). 
     
    Original change's description: 
    > [dawn][wire] Put most of the wire in a source_set. 
    > 
    > And change dawn_unittests to use the static version of dawn_wire, such 
    > that in a follow-up CL it can test using its internals directly instead 
    > of having to only rely on the public interface. 
    > 
    > Bug: 492139412 
    > Change-Id: I43a26073382545d7502b8765c78525ea040812c3 
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297036 
    > Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    > Reviewed-by: Loko Kung <lokokung@google.com> 
     
    Bug: 492139412 
    Change-Id: I9b99bcc46685b99ab2a9248f9d81cdb914bc945d 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299075 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com> 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    (cherry picked from commit baea44be7bedb6309d9c6ee3f5ff1ee6b2b093f7) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/300015

```

---

Files:

- M `generator/dawn_json_generator.py`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/utils/BUILD.gn`
- M `src/dawn/wire/BUILD.gn`
- M `src/dawn/wire/WireClient.cpp`

---

Hash: c2dc6235ad86e5973184ce0d2919d98312f7d980  

Date: Fri Mar 27 21:57:33 2026


---

### dx...@google.com (2026-03-28)

Project: dawn  

Branch:  chromium/7680  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://dawn-review.googlesource.com/299997>

[M146] Reland "[dawn][wire] Check that buffer is mapped in DeserializeDataUpdate."

---


Expand for full commit details
```
     
    This is a reland of commit e0a5e719c91ae3b60b3fc3d6d407b55e19337be4 
     
    Original change's description: 
    > [dawn][wire] Check that buffer is mapped in DeserializeDataUpdate. 
    > 
    > Previously the target of the WriteHandle for a buffer was set as soon as 
    > the buffer is mapped. Between the time it was first mapped and the time 
    > DeserializeDataUpdate was called (right before Unmap), the buffer could 
    > be implicitly unmapped by a call to Device::Destroy. 
    > 
    >  - Instead check for the buffer being mapped directly in 
    >    DeserializeDataUpdate, which remove the need to track a mapWriteState 
    >    on the ObjectData<WGPUBuffer>. 
    >  - Update the change detecting WireTests to account to GetMappedRange 
    >    being done in a different place now for writable buffers. 
    >  - Add a new test that allows injecting WireCmds directly for even more 
    >    precise but even more change detecting tests. 
    >  - Add necessary backdoors to WireClient and WireTest need for the new 
    >    tests. 
    >  - Link dawn::wire statically in dawn_unittests as we now need to use 
    >    some of its internals directly. 
    > 
    > Bug: 492139412 
    > Change-Id: Ibe9ab95ae7456c6629434d4978f439ebfe41c4d1 
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/296817 
    > Reviewed-by: Loko Kung <lokokung@google.com> 
    > Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
     
    Bug: 492139412 
    Change-Id: Ie60fe8d418299335fb2ec13d673be0a4776c32be 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299215 
    Auto-Submit: Corentin Wallez <cwallez@chromium.org> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com> 
    Commit-Queue: Antonio Maiorano <amaiorano@google.com> 
    (cherry picked from commit 4ba836a41006884c55731c72a1ba730d76cfb993) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299997 
    Reviewed-by: Loko Kung <lokokung@google.com>

```

---

Files:

- M `include/dawn/wire/WireClient.h`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/tests/unittests/wire/WireBufferMappingTests.cpp`
- M `src/dawn/tests/unittests/wire/WireMemoryTransferServiceTests.cpp`
- A `src/dawn/tests/unittests/wire/WireSpecificCommandTests.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/wire/WireClient.cpp`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/ServerBuffer.cpp`

---

Hash: 7c1377424ea94d1b15d6fd3d1bf3356617d1c228  

Date: Sat Mar 28 15:00:42 2026


---

### dx...@google.com (2026-03-28)

Project: dawn  

Branch:  chromium/7727  

Author:  Corentin Wallez [cwallez@chromium.org](mailto:cwallez@chromium.org)  

Link:    <https://dawn-review.googlesource.com/299998>

[M147] Reland "[dawn][wire] Check that buffer is mapped in DeserializeDataUpdate."

---


Expand for full commit details
```
     
    This is a reland of commit e0a5e719c91ae3b60b3fc3d6d407b55e19337be4 
     
    Original change's description: 
    > [dawn][wire] Check that buffer is mapped in DeserializeDataUpdate. 
    > 
    > Previously the target of the WriteHandle for a buffer was set as soon as 
    > the buffer is mapped. Between the time it was first mapped and the time 
    > DeserializeDataUpdate was called (right before Unmap), the buffer could 
    > be implicitly unmapped by a call to Device::Destroy. 
    > 
    >  - Instead check for the buffer being mapped directly in 
    >    DeserializeDataUpdate, which remove the need to track a mapWriteState 
    >    on the ObjectData<WGPUBuffer>. 
    >  - Update the change detecting WireTests to account to GetMappedRange 
    >    being done in a different place now for writable buffers. 
    >  - Add a new test that allows injecting WireCmds directly for even more 
    >    precise but even more change detecting tests. 
    >  - Add necessary backdoors to WireClient and WireTest need for the new 
    >    tests. 
    >  - Link dawn::wire statically in dawn_unittests as we now need to use 
    >    some of its internals directly. 
    > 
    > Bug: 492139412 
    > Change-Id: Ibe9ab95ae7456c6629434d4978f439ebfe41c4d1 
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/296817 
    > Reviewed-by: Loko Kung <lokokung@google.com> 
    > Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
     
    Bug: 492139412 
    Change-Id: Ie60fe8d418299335fb2ec13d673be0a4776c32be 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299215 
    Auto-Submit: Corentin Wallez <cwallez@chromium.org> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Antonio Maiorano <amaiorano@google.com> 
    Commit-Queue: Antonio Maiorano <amaiorano@google.com> 
    (cherry picked from commit 4ba836a41006884c55731c72a1ba730d76cfb993) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299998 
    Reviewed-by: Loko Kung <lokokung@google.com>

```

---

Files:

- M `include/dawn/wire/WireClient.h`
- M `src/dawn/tests/BUILD.gn`
- M `src/dawn/tests/unittests/wire/WireBufferMappingTests.cpp`
- M `src/dawn/tests/unittests/wire/WireMemoryTransferServiceTests.cpp`
- A `src/dawn/tests/unittests/wire/WireSpecificCommandTests.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/wire/WireClient.cpp`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/ServerBuffer.cpp`

---

Hash: 484c8f67f53a6eb8bc8eddcd894b15983b2e8117  

Date: Sat Mar 28 15:00:47 2026


---

### pe...@google.com (2026-03-28)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### cw...@chromium.org (2026-03-28)

1. Not sure but years ago, so way befor M144
2. No

### vi...@google.com (2026-03-31)

For M138 LTS, CL <https://dawn-review.git.corp.google.com/c/dawn/+/299075> has a single conflict simple to solve. But CL <https://dawn-review.git.corp.google.com/c/dawn/+/299215> requires a large number of dependent CLs to resolve. Given that this dependency chain is unsafe to merge into LTS, I’m labeling it as not applicable for the M138 LTS.

### vi...@google.com (2026-05-08)

Likewise to [#comment29](https://issues.chromium.org/issues/492139412#comment29), the first CL applied nicely but the second (<https://dawn-review.git.corp.google.com/c/dawn/+/299215>) would require a larger modification that'd bring instability for M144 LTS. Labeling as LTS-NotApplicable-144

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $36000.00 for this report.

Rationale for this decision:
High quality with bisect. Memory Corruption / RCE in a highly privileged process (e.g. GPU or network)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492139412)*
