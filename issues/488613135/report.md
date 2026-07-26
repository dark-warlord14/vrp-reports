# Use-after-free in Dawn wire server buffer map callback due to spontaneous callback race condition

| Field | Value |
|-------|-------|
| **Issue ID** | [488613135](https://issues.chromium.org/issues/488613135) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Mac, iOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | lo...@google.com |
| **Created** | 2026-03-01 |
| **Bounty** | $16,000.00 |

## Description

## Summary

When Dawn's spontaneous wire server mode is enabled (the default on platforms where WebGPU is active), the GPU process's wire server processes incoming commands on the scheduler thread without holding the server mutex, while asynchronous callbacks from GPU completion handlers fire on separate threads and do acquire the mutex. This single-sided locking provides no mutual exclusion. A renderer can issue a buffer map request followed by a buffer destroy, causing the scheduler thread to free the ReadHandle object via `PreHandleBufferDestroy` while a Metal GPU completion callback thread is concurrently dereferencing the same ReadHandle inside `OnBufferMapAsyncCallback`. This results in a heap use-after-free in the GPU process, which constitutes a sandbox escape since the crash occurs outside the renderer sandbox. This vulnerability does not require a compromised renderer: the PoC uses only standard WebGPU JavaScript APIs (`createBuffer`, `mapAsync`, `destroy`, `setTimeout`) that are available to any web page on platforms where WebGPU is enabled. The vulnerability is specific to the Metal GPU backend and therefore affects macOS and iOS; no specific GPU model is required, any Metal-capable GPU is sufficient.

## Bisect

The vulnerability was introduced by a series of commits that added the spontaneous wire server mode to Dawn and wired it into Chromium.

Introducing Commit (Dawn): `7c133fa8ce744ac73d0ec4b960b919d9db7bc250`

- Date: 2025-09-03
- Author: Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)
- Review: <https://dawn-review.googlesource.com/c/dawn/+/237777>

Introducing Commit (Chromium, feature flag): `821883aea1cdecc988290dc976614d783199486c`

- Date: 2025-10-20
- Author: Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/7050205>

Introducing Commit (Chromium, wiring): `47978f61eaf56f03fb140b1eaa73de53e630c921`

- Date: 2025-10-22
- Author: Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/6918406>

## Root Cause

The Dawn wire server uses a split architecture where the renderer process serializes WebGPU commands into a command buffer, and the GPU process deserializes and executes them via `Server::HandleCommands`. When the spontaneous callback feature is enabled, asynchronous callbacks from the GPU backend (such as Metal's command buffer completion handlers) fire on arbitrary threads and are routed through `ForwardToServerHelper::Callback`, which acquires the server's `mMutex` via `GetGuard()` before invoking the callback handler. However, the main command processing path through `Server::HandleCommands` intentionally does not acquire this same mutex. This asymmetric locking design was chosen to avoid potential deadlocks with `Device::Destroy`, but it means the mutex provides zero mutual exclusion between the two threads.

The relevant callback dispatch code in `Server.h` shows the locking on the callback side:

```
// third_party/dawn/src/dawn/wire/server/Server.h
static void Callback(Args... args, void* userdata, void*) {
    std::unique_ptr<Userdata> data(static_cast<Userdata*>(userdata));
    auto server = data->server.lock();
    if (!server) { return; }
    {
        auto serverGuard = server.get()->GetGuard();  // Acquires mMutex
        (server.get()->*F)(data.get(), std::forward<Args>(args)...);
    }
    server.get()->Flush();
}

```

The `PreHandleBufferDestroy` function runs on the scheduler thread without any lock and directly resets the `readHandle` and `writeHandle` unique pointers, destroying the underlying `ReadHandleImpl` and `WriteHandleImpl` objects:

```
// third_party/dawn/src/dawn/wire/server/ServerBuffer.cpp
WireResult Server::PreHandleBufferDestroy(const BufferDestroyCmd& cmd) {
    Known<WGPUBuffer> buffer;
    WIRE_TRY(Get(cmd.selfId, &buffer));

    // The buffer was destroyed. Clear the Read/WriteHandle.
    buffer->readHandle = nullptr;   // Frees ReadHandle -- NO LOCK HELD
    buffer->writeHandle = nullptr;
    buffer->mapWriteState = BufferMapWriteState::Unmapped;

    return WireResult::Success;
}

```

Concurrently, `OnBufferMapAsyncCallback` runs on the Metal completion handler thread (holding `mMutex`) and dereferences the same `readHandle` unique pointer to access the `ReadHandleImpl` object:

```
// third_party/dawn/src/dawn/wire/server/ServerBuffer.cpp
void Server::OnBufferMapAsyncCallback(MapUserdata* data,
                                      WGPUMapAsyncStatus status,
                                      WGPUStringView message) {
    Known<WGPUBuffer> buffer;
    if (Get(data->buffer.id, &buffer) != WireResult::Success ||
        buffer->generation != data->buffer.generation) {
        return;
    }

    bool isRead = (data->mode & WGPUMapMode_Read) != 0u;
    bool isSuccess = status == WGPUMapAsyncStatus_Success;

    if (isSuccess && isRead) {
        readDataUpdateInfoLength =
            buffer->readHandle->SizeOfSerializeDataUpdate(data->offset, data->size);
            // Dereferences readHandle -- holds mMutex but main thread doesn't use it
    }
}

```

The `ReadHandleImpl` object is allocated in `DawnServiceMemoryTransferService::DeserializeReadHandle` during buffer creation and stored as a `std::unique_ptr` in the buffer's `ObjectData`. When the scheduler thread processes a `BufferDestroy` command, the unique pointer reset destroys the `ReadHandleImpl`. If the callback thread has already loaded the raw pointer from the unique pointer (via `operator->()`) but has not yet completed its method call, the `this` pointer inside the `ReadHandleImpl` method becomes dangling, and any subsequent member access constitutes a use-after-free.

After `OnBufferMapAsyncCallback` calls `SizeOfSerializeDataUpdate`, it proceeds to invoke `SerializeCommand` with a `CommandExtension` callback that calls `SerializeDataUpdate`. The `ReadHandleImpl::SerializeDataUpdate` in Chromium's `dawn_service_memory_transfer_service.cc` accesses freed memory through `this->buffer_data_view_`:

```
// gpu/command_buffer/service/dawn_service_memory_transfer_service.cc
void SerializeDataUpdate(const void* data, size_t offset, size_t size,
                         void* serializePointer) override {
    CHECK_LE(offset, buffer_data_view_.size());            // UAF: accesses freed this->buffer_data_view_
    CHECK_LE(size, buffer_data_view_.size() - offset);     // UAF: accesses freed this->buffer_data_view_
    memcpy(buffer_data_view_.data() + offset, data, size); // UAF: accesses freed this->buffer_data_view_
}

```

This is the concrete use-after-free point: when the `ReadHandleImpl` has been freed by `PreHandleBufferDestroy` on the scheduler thread, the `buffer_data_view_` member access in `SerializeDataUpdate` dereferences a dangling `this` pointer. If an attacker can reclaim the freed 32-byte `ReadHandleImpl` region with controlled data, the `buffer_data_view_` fields (a pointer at offset 16 and a size at offset 24) become attacker-controlled, and the `memcpy` in `SerializeDataUpdate` writes attacker-controlled content (the GPU buffer data, filled via `queue.writeBuffer`) to an attacker-controlled destination address. This yields an arbitrary write primitive in the GPU process.

The spontaneous callback mode is enabled by default in Chromium. The feature flag `kWebGPUSpontaneousWireServer` in `gpu/config/gpu_finch_features.cc` has a default value of `true`:

```
// gpu/config/gpu_finch_features.cc
const base::FeatureParam<bool> kWebGPUSpontaneousWireServer{
    &kWebGPUService, "DawnSpontaneousWireServer", true};

```

The race is only triggerable on the Metal backend (macOS and iOS). Metal's `Queue::SubmitPendingCommandBuffer` registers a completion handler via `[MTLCommandBuffer addCompletedHandler:]`, which the OS invokes on a Metal-owned background thread when GPU work finishes. This background thread calls `UpdateCompletedSerialToInternal`, which in turn calls `EventManager::SetFutureReady`, completing the map async event and invoking the wire server callback — all from the Metal thread. Other backends (Vulkan, D3D12, D3D11, OpenGL) check completion by polling fence values on the calling thread (`vkGetFenceStatus`, `ID3D12Fence::GetCompletedValue`, `eglClientWaitSync`), so the callback is never invoked spontaneously from a background thread and the race does not exist on those platforms.

## Reproduce

Tested on macOS (Apple Silicon) with Chromium commit `3633b670e86af329be8ecfe3d73ba9f927f48bb3` (2026-03-01, version 147.0.7710.0). WebGPU is enabled by default on macOS, so no special flags are needed. A source code modification is used to widen the race window for reliable reproduction: adding a 500ms sleep at the beginning of `ReadHandleImpl::SerializeDataUpdate` causes the callback thread to hold the `this` pointer long enough for the scheduler thread to process the destroy command and free the object. The sleep is not strictly necessary for the vulnerability to exist; without it the race can still be triggered naturally, though it requires more iterations due to the narrow window.

To reproduce:

```
git apply patch.diff
ninja -C out/asan/ chrome
./out/asan/Chromium.app/Contents/MacOS/Chromium --user-data-dir=./userdata poc.html

```

ASAN output:

```
=================================================================
==7848==ERROR: AddressSanitizer: heap-use-after-free on address 0x6030001fe208 at pc 0x000361dbeda0 bp 0x00016e5294d0 sp 0x00016e5294c8
READ of size 8 at 0x6030001fe208 thread T3
==7848==WARNING: invalid path to external symbolizer!
==7848==WARNING: Failed to use and restart external symbolizer!
    #0 0x000361dbed9c in gpu::webgpu::(anonymous namespace)::ReadHandleImpl::SerializeDataUpdate(void const*, unsigned long, unsigned long, void*)+0x350 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x185aed9c)
    #1 0x000361d80d78 in void dawn::wire::ChunkedCommandSerializer::SerializeCommandImpl<dawn::wire::ReturnBufferMapAsyncCallbackCmd, void dawn::wire::ChunkedCommandSerializer::SerializeCommand<dawn::wire::ReturnBufferMapAsyncCallbackCmd>(dawn::wire::ReturnBufferMapAsyncCallbackCmd const&, dawn::wire::CommandExtension&&)::'lambda'(dawn::wire::ReturnBufferMapAsyncCallbackCmd const&, unsigned long, dawn::wire::SerializeBuffer*), dawn::wire::CommandExtension>(dawn::wire::ReturnBufferMapAsyncCallbackCmd const&, void dawn::wire::ChunkedCommandSerializer::SerializeCommand<dawn::wire::ReturnBufferMapAsyncCallbackCmd>(dawn::wire::ReturnBufferMapAsyncCallbackCmd const&, dawn::wire::CommandExtension&&)::'lambda'(dawn::wire::ReturnBufferMapAsyncCallbackCmd const&, unsigned long, dawn::wire::SerializeBuffer*)&&, dawn::wire::CommandExtension&&)+0x3a8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x18570d78)
    #2 0x000361d80404 in void dawn::wire::server::Server::SerializeCommand<dawn::wire::ReturnBufferMapAsyncCallbackCmd, dawn::wire::CommandExtension>(dawn::wire::ReturnBufferMapAsyncCallbackCmd const&, dawn::wire::CommandExtension&&)+0x130 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x18570404)
    #3 0x000361d7f458 in dawn::wire::server::Server::OnBufferMapAsyncCallback(dawn::wire::server::MapUserdata*, WGPUMapAsyncStatus, WGPUStringView)+0x624 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x1856f458)
    #4 0x000361d80584 in dawn::wire::server::ForwardToServerHelper<&dawn::wire::server::Server::OnBufferMapAsyncCallback(dawn::wire::server::MapUserdata*, WGPUMapAsyncStatus, WGPUStringView), void (dawn::wire::server::Server::*)(dawn::wire::server::MapUserdata*, WGPUMapAsyncStatus, WGPUStringView)>::Callback(WGPUMapAsyncStatus, WGPUStringView, void*, void*)+0x94 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x18570584)
    #5 0x00034b967068 in dawn::native::BufferBase::MapAsyncEvent::RunCallback(WGPUMapAsyncStatus, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)+0x25c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x2157068)
    #6 0x00034b966a24 in dawn::native::BufferBase::MapAsyncEvent::Complete(dawn::EventCompletionType)+0x47c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x2156a24)
    #7 0x0003714f991c in std::__Cr::__call_once(unsigned long volatile&, void*, void (*)(void*))+0x16c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x27ce991c)
    #8 0x00034ba20b18 in dawn::native::EventManager::SetFutureReady(dawn::native::EventManager::TrackedEvent*)+0x1b4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x2210b18)
    #9 0x00034ba35040 in dawn::native::ExecutionQueueBase::UpdateCompletedSerialToInternal(unsigned long long, bool)+0x400 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x2225040)
    #10 0x00034bbf1b78 in invocation function for block in dawn::native::metal::Queue::SubmitPendingCommandBuffer()+0xf4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x23e1b78)
    #11 0x0001a75fbe9c in MTLDispatchListApply+0x30 (/System/Library/Frameworks/Metal.framework/Versions/A/Metal:arm64e+0x15e9c)
    #12 0x0001a77b2744 in -[_MTLCommandBuffer didCompleteWithStartTime:endTime:error:]+0x260 (/System/Library/Frameworks/Metal.framework/Versions/A/Metal:arm64e+0x1cc744)
    #13 0x0001bfa75224 in -[IOGPUMetalCommandBuffer didCompleteWithStartTime:endTime:error:]+0xd8 (/System/Library/PrivateFrameworks/IOGPU.framework/Versions/A/IOGPU:arm64e+0x3224)
    #14 0x0001a77b5fa8 in -[_MTLCommandQueue commandBufferDidComplete:startTime:completionTime:error:]+0x68 (/System/Library/Frameworks/Metal.framework/Versions/A/Metal:arm64e+0x1cffa8)
    #15 0x0001bfa81668 in IOGPUNotificationQueueDispatchAvailableCompletionNotifications+0x84 (/System/Library/PrivateFrameworks/IOGPU.framework/Versions/A/IOGPU:arm64e+0xf668)
    #16 0x0001bfa81778 in __IOGPUNotificationQueueSetDispatchQueue_block_invoke+0x3c (/System/Library/PrivateFrameworks/IOGPU.framework/Versions/A/IOGPU:arm64e+0xf778)
    #17 0x000102544780 in __asan_memmove+0x2790 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x54780)
    #18 0x00019b112b18 in _dispatch_client_callout4+0xc (/usr/lib/system/libdispatch.dylib:arm64e+0x1bb18)
    #19 0x00019b115398 in _dispatch_mach_msg_invoke+0x1cc (/usr/lib/system/libdispatch.dylib:arm64e+0x1e398)
    #20 0x00019b10134c in _dispatch_lane_serial_drain+0x148 (/usr/lib/system/libdispatch.dylib:arm64e+0xa34c)
    #21 0x00019b116100 in _dispatch_mach_invoke+0x1d4 (/usr/lib/system/libdispatch.dylib:arm64e+0x1f100)
    #22 0x00019b10134c in _dispatch_lane_serial_drain+0x148 (/usr/lib/system/libdispatch.dylib:arm64e+0xa34c)
    #23 0x00019b101ff4 in _dispatch_lane_invoke+0x1b4 (/usr/lib/system/libdispatch.dylib:arm64e+0xaff4)
    #24 0x00019b10134c in _dispatch_lane_serial_drain+0x148 (/usr/lib/system/libdispatch.dylib:arm64e+0xa34c)
    #25 0x00019b101fc0 in _dispatch_lane_invoke+0x180 (/usr/lib/system/libdispatch.dylib:arm64e+0xafc0)
    #26 0x00019b10c470 in _dispatch_root_queue_drain_deferred_wlh+0x120 (/usr/lib/system/libdispatch.dylib:arm64e+0x15470)
    #27 0x00019b10bd68 in _dispatch_workloop_worker_thread+0x2b0 (/usr/lib/system/libdispatch.dylib:arm64e+0x14d68)
    #28 0x00019b2b1e48 in _pthread_wqthread+0x120 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x2e48)
    #29 0x00019b2b0b98 in start_wqthread+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1b98)

0x6030001fe208 is located 24 bytes inside of 32-byte region [0x6030001fe1f0,0x6030001fe210)
freed by thread T0 here:
    #0 0x0001025450ac in __asan_memmove+0x30bc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x550ac)
    #1 0x000361d7e7b0 in dawn::wire::server::Server::PreHandleBufferDestroy(dawn::wire::BufferDestroyCmd const&)+0x178 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x1856e7b0)
    #2 0x000361d97b64 in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long)+0x2154 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x18587b64)
    #3 0x000361dcb758 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long)+0x154 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x185bb758)
    #4 0x000361dcbb5c in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*)+0x2e8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x185bbb5c)
    #5 0x000361dc1af0 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*)+0x200 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x185b1af0)
    #6 0x0003515a7340 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x4bc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x7d97340)
    #7 0x000361cd5f9c in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)+0x450 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x184c5f9c)
    #8 0x000361cd511c in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)+0x468 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x184c511c)
    #9 0x000361cf3934 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x184e3934)
    #10 0x000361cff5ec in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)+0x144 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x184ef5ec)
    #11 0x000361cff404 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)+0x118 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x184ef404)
    #12 0x0003515e0160 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x7dd0160)
    #13 0x0003515bac40 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x634 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x7daac40)
    #14 0x0003515b92d8 in gpu::Scheduler::RunNextTask()+0x27c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x7da92d8)
    #15 0x0003515bc674 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x7dac674)
    #16 0x00035bb2bfb0 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x1231bfb0)
    #17 0x00035bb9449c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x1238449c)
    #18 0x00035bb93848 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x12383848)
    #19 0x00035bcb4fc8 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x124a4fc8)
    #20 0x00035bca6678 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x12496678)
    #21 0x00035bcb3400 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x124a3400)
    #22 0x00019b3549f4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f9f4)
    #23 0x00019b354988 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f988)
    #24 0x00019b3546f4 in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f6f4)
    #25 0x00019b353384 in __CFRunLoopRun+0x330 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5e384)
    #26 0x00019b40de30 in _CFRunLoopRunSpecificWithOptions+0x210 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x118e30)
    #27 0x00019d5a2960 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd0 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:arm64e+0xa5b960)
    #28 0x00035bcb6118 in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xc8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x124a6118)
    #29 0x00035bcb2158 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x124a2158)

previously allocated by thread T0 here:
    #0 0x000102544fc0 in __asan_memmove+0x2fd0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x54fc0)
    #1 0x0003720b7d0c in operator new(unsigned long)+0x18 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x288a7d0c)
    #2 0x000361dbd870 in gpu::webgpu::DawnServiceMemoryTransferService::DeserializeReadHandle(void const*, unsigned long, dawn::wire::server::MemoryTransferService::ReadHandle**)+0x164 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x185ad870)
    #3 0x000361d7fc90 in dawn::wire::server::Server::DoDeviceCreateBuffer(dawn::wire::server::Known<WGPUDeviceImpl*>, WGPUBufferDescriptor const*, dawn::wire::ObjectHandle, unsigned long long, unsigned char const*, unsigned long long, unsigned char const*)+0x588 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x1856fc90)
    #4 0x000361d8f730 in dawn::wire::server::Server::HandleDeviceCreateBuffer(dawn::wire::DeserializeBuffer*)+0x22c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x1857f730)
    #5 0x000361d963a8 in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long)+0x998 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x185863a8)
    #6 0x000361dcb758 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long)+0x154 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x185bb758)
    #7 0x000361dcbb5c in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*)+0x2e8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x185bbb5c)
    #8 0x000361dc1af0 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*)+0x200 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x185b1af0)
    #9 0x0003515a7340 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x4bc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x7d97340)
    #10 0x000361cd5f9c in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)+0x450 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x184c5f9c)
    #11 0x000361cd511c in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)+0x468 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x184c511c)
    #12 0x000361cf3934 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x184e3934)
    #13 0x000361cff5ec in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)+0x144 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x184ef5ec)
    #14 0x000361cff404 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)+0x118 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x184ef404)
    #15 0x0003515e0160 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x7dd0160)
    #16 0x0003515bac40 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x634 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x7daac40)
    #17 0x0003515b92d8 in gpu::Scheduler::RunNextTask()+0x27c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x7da92d8)
    #18 0x0003515bc674 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x7dac674)
    #19 0x00035bb2bfb0 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x1231bfb0)
    #20 0x00035bb9449c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x1238449c)
    #21 0x00035bb93848 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x12383848)
    #22 0x00035bcb4fc8 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x124a4fc8)
    #23 0x00035bca6678 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x12496678)
    #24 0x00035bcb3400 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x124a3400)
    #25 0x00019b3549f4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f9f4)
    #26 0x00019b354988 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f988)
    #27 0x00019b3546f4 in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f6f4)
    #28 0x00019b353384 in __CFRunLoopRun+0x330 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5e384)
    #29 0x00019b40de30 in _CFRunLoopRunSpecificWithOptions+0x210 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x118e30)

Thread T3 created by T0 here:
    <empty stack>

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Chromium Framework:arm64+0x185aed9c) in gpu::webgpu::(anonymous namespace)::ReadHandleImpl::SerializeDataUpdate(void const*, unsigned long, unsigned long, void*)+0x350
Shadow bytes around the buggy address:
  0x6030001fdf80: fd fd fd fa f7 fa fd fd fd fd f7 fa 00 00 00 fa
  0x6030001fe000: f7 fa fd fd fd fa f7 fa fd fd fd fa f7 fa fd fd
  0x6030001fe080: fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa
  0x6030001fe100: fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd fd fa
  0x6030001fe180: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd
=>0x6030001fe200: fd[fd]f7 fa fd fd fd fd f7 fa 00 00 00 00 f7 fa
  0x6030001fe280: 00 00 00 00 f7 fa fd fd fd fd f7 fa 00 00 00 00
  0x6030001fe300: f7 fa 00 00 00 00 f7 fa 00 00 00 00 f7 fa 00 00
  0x6030001fe380: 00 00 f7 fa 00 00 00 00 f7 fa fd fd fd fa f7 fa
  0x6030001fe400: fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd
  0x6030001fe480: f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa fd fd
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

==7848==ADDITIONAL INFO

==7848==Note: Please include this section with the ASan report.
Task trace:


Command line: `/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7710.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper --type=gpu-process --user-data-dir=./userdata --start-stack-profiler --gpu-preferences=SAAAAAAAAAAgAQAEAAAAAAAAAAAAAMAAAwAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAA== --shared-files --metrics-shmem-handle=1752395122,r,8357134903701969152,10452187502410134878,262144 --field-trial-handle=1718379636,r,17980659783760999744,16137671430171451269,262144 --variations-seed-version --pseudonymization-salt-handle=1935764596,r,14948782399246895129,18320638700896022104,4 --trace-process-track-uuid=3190708988185955192 --seatbelt-client=25 --user-data-dir=/Users/test/Library/Application Support/Chromium`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==7848==END OF ADDITIONAL INFO

==7848==ABORTING

```
## Credit

86ac1f1587b71893ed2ad792cd7dde32

## Attachments

- [patch.diff](attachments/patch.diff) (text/x-diff, 1.1 KB)
- [poc.html](attachments/poc.html) (text/html, 3.4 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4670057997074432.

### mp...@google.com (2026-03-03)

I haven't reproduced but this looks real to me. There's also the `writeHandle` that's also freed as far as I can tell.

The feature was landed with a Killswitch, rather than an off-by-default Finch flag, so has security impact.

### 24...@project.gserviceaccount.com (2026-03-03)

Testcase 4670057997074432 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4670057997074432.

### se...@gmail.com (2026-03-04)

Hi! I think you may need to use `macOS` to reproduce it.

### ch...@google.com (2026-03-07)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-07)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-10)

Project: dawn  

Branch:  main  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/295217>

[dawn][wire] Adds a lock to the server-side buffer object.

---


Expand for full commit details
```
     
    - The lock is necessary now since the server's callbacks are allowed 
      to be spontaneous which means it may be run on different threads. 
      The lock ensures that if the main server thread processing commands 
      from the client is running an Unmap or Destroy operation on a 
      buffer, that it is protected against a race with a thread calling 
      the spontaneous callback that may update the mapping state. 
    - Also adds and updates MutexProtected/MutexRefProtected to allow for 
      copy/move constructors and assignment when it makes sense. This was 
      necessary because we needed to be able to move assign the wire 
      server data fields. 
     
    Bug: 488613135 
    Change-Id: I6c2eae3324fa6c551f2c2bb0e6eacf5371284dad 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/295217 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org>

```

---

Files:

- M `src/dawn/common/MutexProtected.h`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/ServerBuffer.cpp`

---

Hash: b2a0c4eb105fa5dfc7335280613c882699a87b9a  

Date: Tue Mar 10 22:30:49 2026


---

### lo...@google.com (2026-03-10)

The fix above should fix the issue. Do we feel like we need to merge this fix back?

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7658937>

Roll Dawn from b2cbf25a0364 to ad824e2cb346 (45 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/b2cbf25a0364..ad824e2cb346 
     
    2026-03-12 bsheedy@google.com Generate .pyl files from Starlark 
    2026-03-11 kainino@chromium.org [cts] Skip an OOM crash on Pixel 6, triage related expectations 
    2026-03-11 kainino@chromium.org Revert "[dawn][native] Add support filteringness attributes to GetBindGroupLayout" 
    2026-03-11 jrprice@google.com [ir] Clone explicit template parameters on builtin calls 
    2026-03-11 beaufort.francois@gmail.com Sync webgpu.h changes and remove "compat" tag 
    2026-03-11 petermcneeley@google.com [tint] Minor metal validation bug for relaxed math 
    2026-03-11 bajones@chromium.org Return a span for WriteHandle Source 
    2026-03-11 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 87e7333c9482 to 8d43dd57d980 (676 revisions) 
    2026-03-11 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from 29b36dd0b852 to 41b52b413169 (10 revisions) 
    2026-03-11 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll DirectX Shader Compiler from e9be4c440ce8 to 4f398bffdbba (5 revisions) 
    2026-03-11 shaoboyan@microsoft.com vulkan: Fix descriptor set rebinding on push constant range change 
    2026-03-11 jiawei.shao@intel.com Enable SharedBufferMemoryTests.BeginAccessInitialization on WARP 
    2026-03-11 bsheedy@google.com Remove Linux/TSan infra/specs entries 
    2026-03-10 bsheedy@google.com Migrate Linux/TSan to Starlark 
    2026-03-10 lokokung@google.com [dawn][wire] Adds a lock to the server-side buffer object. 
    2026-03-10 bsheedy@google.com Make dawn_end2end_tests definitions more generic 
    2026-03-10 bsheedy@google.com Fix clusterfuzz corpus args 
    2026-03-10 bajones@chromium.org Restrict Vulkan Dynamic Rendering on Mali-G68 GPUs 
    2026-03-10 chrome-branch-day@chops-service-accounts.iam.gserviceaccount.com Activate dawn M147 
    2026-03-10 petermcneeley@google.com [dawn] Minor triage of pixel 10 cts bugs 
    2026-03-10 jrprice@google.com [tint] Remove TINT_REFLECT_EQUALS macro 
    2026-03-10 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 9117cef67a60 to b55a0e69f29d (11 revisions) 
    2026-03-10 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from cdd0b0ea31d7 to 87e7333c9482 (692 revisions) 
    2026-03-10 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from b1b19492e609 to 29b36dd0b852 (13 revisions) 
    2026-03-10 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll DirectX Shader Compiler from 2888a8764a33 to e9be4c440ce8 (7 revisions) 
    2026-03-10 jiawei.shao@intel.com Define shared buffer memory d3d12 file handle descriptor in dawn.json 
    2026-03-10 bsheedy@google.com Remove Win/MSVC/dbg infra/specs entries 
    2026-03-09 bsheedy@google.com Migrate Win/MSVC/dbg to Starlark 
    2026-03-09 bsheedy@google.com Remove Linux/clusterfuzz infra/specs entries 
    2026-03-09 jrprice@google.com [msl] Run CanGenerate() from Generate() 
    2026-03-09 bsheedy@google.com Migrate Linux/clusterfuzz to Starlark 
    2026-03-09 jrprice@google.com [msl] Use Result for Validate*() and test helpers 
    2026-03-09 kainino@chromium.org [dawn][metal] Fix robustness issues around buffer lengths being u32 
    2026-03-09 jrprice@google.com [tint] Remove dead code for textureStore clamping 
    2026-03-09 cwallez@chromium.org [dawn][native] Add support filteringness attributes to GetBindGroupLayout 
    2026-03-09 jrprice@google.com [msl] Simplify vertex pulling entry point check 
    2026-03-09 bsheedy@google.com Remove Win/MSVC/rel infra/specs entries 
    2026-03-09 bsheedy@google.com Migrate missed Win/ASan test exceptions 
    2026-03-09 amaiorano@google.com Fix validation on nullptr color attachment 
    2026-03-09 senorblanco@chromium.org GL: fix multithreaded buffer mapping tests. 
    2026-03-09 bsheedy@google.com Migrate Win/MSVC/rel to Starlark 
    2026-03-09 kylechar@google.com Add RenderPassRenderArea feature 
    2026-03-09 bsheedy@google.com Swap Win/ARM64 mirrored builder 
    2026-03-09 amaiorano@google.com [dawn] Add samplers to ResourceTableTests.HasResourceCompatibilityAllTypes test 
    2026-03-09 cwallez@chromium.org [YUV AHB] Add test checking RGB of Vulkan YCbCr sampler 
     
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
    Bug: chromium:386255678,chromium:407748576,chromium:421288698,chromium:451928481,chromium:452840618,chromium:468988322,chromium:470014334,chromium:473354063,chromium:479233871,chromium:485816035,chromium:486441214,chromium:486866985,chromium:487522152,chromium:487593147,chromium:488613135,chromium:489152883,chromium:490378523,chromium:491869936,chromium:491881355 
    Tbr: gman@google.com 
    Test: Test: MetalBufferRobustnessTest.* 
    Change-Id: I46a192df2c7fb6305a7bc2d10d35b0bc7139fcc8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7658937 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1598189}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [c6d422798c9dfbb3ea5453a55744ad9296e4e772](https://chromiumdash.appspot.com/commit/c6d422798c9dfbb3ea5453a55744ad9296e4e772)  

Date: Thu Mar 12 03:42:35 2026


---

### ch...@google.com (2026-03-12)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-13)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1598189) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1598189) appears to be after beta branch point (1596535).
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

### lo...@google.com (2026-03-13)

This Dawn CL needs to be backmerged: <https://dawn-review.googlesource.com/c/dawn/+/295217>

### dr...@chromium.org (2026-03-15)

No crashes in Canary, approved to merge to M146 and M147.

### dr...@chromium.org (2026-03-18)

Friendly ping on the merge to M146!

### go...@google.com (2026-03-19)

Please merge your change to M147 by 2:00 PM PT today so we can take it in for tomorrow's M147 beta release. Thank you.

### ch...@google.com (2026-03-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-20)

Project: dawn  

Branch:  chromium/7727  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/298398>

[M147] [dawn][wire] Adds a lock to the server-side buffer object.

---


Expand for full commit details
```
     
    - The lock is necessary now since the server's callbacks are allowed 
      to be spontaneous which means it may be run on different threads. 
      The lock ensures that if the main server thread processing commands 
      from the client is running an Unmap or Destroy operation on a 
      buffer, that it is protected against a race with a thread calling 
      the spontaneous callback that may update the mapping state. 
    - Also adds and updates MutexProtected/MutexRefProtected to allow for 
      copy/move constructors and assignment when it makes sense. This was 
      necessary because we needed to be able to move assign the wire 
      server data fields. 
     
    Bug: 488613135 
    Change-Id: I6c2eae3324fa6c551f2c2bb0e6eacf5371284dad 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/295217 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/298398 
    Commit-Queue: Loko Kung <lokokung@google.com>

```

---

Files:

- M `src/dawn/common/MutexProtected.h`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/ServerBuffer.cpp`

---

Hash: f028ddea62c6e6ad3080771658ce8c0fb8b7336e  

Date: Fri Mar 20 18:26:35 2026


---

### dx...@google.com (2026-03-20)

Project: dawn  

Branch:  chromium/7680  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/298396>

[M146] [dawn][wire] Adds a lock to the server-side buffer object.

---


Expand for full commit details
```
     
    - The lock is necessary now since the server's callbacks are allowed 
      to be spontaneous which means it may be run on different threads. 
      The lock ensures that if the main server thread processing commands 
      from the client is running an Unmap or Destroy operation on a 
      buffer, that it is protected against a race with a thread calling 
      the spontaneous callback that may update the mapping state. 
    - Also adds and updates MutexProtected/MutexRefProtected to allow for 
      copy/move constructors and assignment when it makes sense. This was 
      necessary because we needed to be able to move assign the wire 
      server data fields. 
     
    Bug: 488613135 
    Change-Id: I6c2eae3324fa6c551f2c2bb0e6eacf5371284dad 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/295217 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/298396 
    Commit-Queue: Loko Kung <lokokung@google.com>

```

---

Files:

- M `src/dawn/common/MutexProtected.h`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/ServerBuffer.cpp`

---

Hash: 2fd2d5e3839c1812521d7cddbfd46f109f6d667a  

Date: Fri Mar 20 18:43:52 2026


---

### sp...@google.com (2026-04-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $16000.00 for this report.

Rationale for this decision:
High quality with bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488613135)*
