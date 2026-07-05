# Dawn: Heap Use-After-Free in AsyncTaskManager::RunTask via premature WaitableEvent nullification

| Field | Value |
|-------|-------|
| **Issue ID** | [493900619](https://issues.chromium.org/issues/493900619) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sw...@gmail.com |
| **Assignee** | lo...@google.com |
| **Created** | 2026-03-18 |
| **Bounty** | $10,000.00 |

## Description

---

### Report description

Dawn: Heap Use-After-Free in AsyncTaskManager::RunTask via premature WaitableEvent nullification

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

A race condition in `src/dawn/native/AsyncTask.cpp` causes a heap-use-after-free in the GPU process. `AsyncTask::Run()` sets `mWaitableEvent = nullptr` before `RunTask()` finishes, so `WaitAllPendingTasks()` frees the `WaitableTask` while the worker thread still accesses it. The freed `raw_ptr<AsyncTaskManager> taskManager` at offset 8 becomes a dangling `this` pointer for `HandleTaskCompletion()`, which can be exploited to hijack control flow in the GPU process if the 16-byte slot is reclaimed.

- **Tested on**: Chromium 147.0.7727.0 (Dawn `85424799f6`)
- **Still alive on remote HEAD**: Dawn `4a3266331c` (2026-03-19) — vulnerable code unchanged at `AsyncTask.cpp`

## Root Cause

`src/dawn/native/AsyncTask.cpp`:

```
void AsyncTask::Run() {
    {
        AsyncTaskState prevState = mState.exchange(AsyncTaskState::Running);
        DAWN_ASSERT(prevState == AsyncTaskState::Pending);
    }

    mTask();
    mTask = nullptr;

    std::vector<AsyncTaskCompletionCallback> completionCallbacks;
    {
        std::scoped_lock<std::mutex> lock(mMutex);
        AsyncTaskState prevState = mState.exchange(AsyncTaskState::Completed);
        DAWN_ASSERT(prevState == AsyncTaskState::Running);
        completionCallbacks = std::move(mCompletionCallbacks);
        mCompletionCallbacks.clear();
        mWaitableEvent = nullptr;                   // ← BUG: premature nullification
    }

    for (auto completionCallback : completionCallbacks) {
        completionCallback();
    }
}

void AsyncTaskManager::RunTask(void* task) {
    WaitableTask* waitableTask = static_cast<WaitableTask*>(task);
    waitableTask->asyncTask->Run();                  // Run() nullifies mWaitableEvent
    waitableTask->taskManager->HandleTaskCompletion(waitableTask);  // ← UAF here
}

void AsyncTask::Wait() {
    std::unique_ptr<dawn::platform::WaitableEvent> waitableEvent;
    {
        std::scoped_lock<std::mutex> lock(mMutex);
        waitableEvent = std::move(mWaitableEvent);   // nullptr after Run() → no wait
    }

    if (waitableEvent) {
        waitableEvent->Wait();
    }
    // Returns immediately when mWaitableEvent is nullptr
}

void AsyncTaskManager::WaitAllPendingTasks() {
    PendingTasksSet allPendingTasks;
    mPendingTasks.Use(
        [&allPendingTasks](auto pendingTasks) { allPendingTasks.swap(*pendingTasks); });

    for (auto& task : allPendingTasks) {
        task->asyncTask->Wait();                     // Returns early
    }
    // allPendingTasks destroyed → unique_ptr<WaitableTask> freed
    // while worker thread still holds raw pointer in RunTask()
}

```
## Reproduction Steps

### Environment

- **Hardware**: Apple MacBook Pro, M4 Pro chip, 48GB RAM
- **OS**: macOS
- **Build**: ASAN Chromium (arm64)
- **Backend**: Metal (default on macOS)
- **Important**: The PoC relies on `requestAnimationFrame` driving the event loop at full frame rate. Page rendering must be active and smooth in GUI (non-headless) mode for the race to trigger. The bug exists in platform-independent code (`AsyncTask.cpp`) and is theoretically triggerable on all backends, but this PoC has only been confirmed on macOS Metal due to its specific thread scheduling characteristics.

### Steps

```
# 1. Serve PoC
python3 -m http.server 8080 &

# 2. Option A - Run ASAN Chromium
ASAN_OPTIONS="detect_leaks=0:halt_on_error=1:abort_on_error=1:detect_odr_violation=0:print_stacktrace=1" \
/path/to/Chromium.app/Contents/MacOS/Chromium \
  --disable-gpu-sandbox \
  --no-sandbox \
  --no-first-run \
  --noerrdialogs \
  --disable-crashpad \
  --user-data-dir=/tmp/dawn-race-$$ \
  http://127.0.0.1:8080/poc_v7_throughput.html

# 2. Option B - Run ASAN Chromium
ASAN_OPTIONS="detect_leaks=0:halt_on_error=1:abort_on_error=1:detect_odr_violation=0:print_stacktrace=1" \
/path/to/Chromium.app/Contents/MacOS/Chromium \
  --disable-gpu-sandbox \
  --no-sandbox \
  --no-first-run \
  --noerrdialogs \
  --disable-crashpad \
  --user-data-dir=/tmp/dawn-race-$$ \
  http://127.0.0.1:8080/poc_v5_reliable.html

```

The ASAN crash typically occurs **between 6 seconds and 1 minute** after the page loads. If no crash occurs within 90 seconds, terminate Chromium and restart with a fresh `--user-data-dir` (e.g. `/tmp/dawn-race-$$` with a new PID). Reliability: **3/5 crashes at 90s timeout** across repeated test runs.

### Expected ASAN output

```
AGX: exceeded compiled variants footprint limit
[72172:1275402:0319/005211.912691:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
[72172:1275402:0319/005236.091116:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
=================================================================
==72180==ERROR: AddressSanitizer: heap-use-after-free on address 0x6020005cad58 at pc 0x00034b11a490 bp 0x0001751aa870 sp 0x0001751aa868
READ of size 8 at 0x6020005cad58 thread T19
==72180==WARNING: invalid path to external symbolizer!
==72180==WARNING: Failed to use and restart external symbolizer!
    #0 0x00034b11a48c in dawn::native::AsyncTaskManager::RunTask(void*)+0xb0 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x122248c)
    #1 0x0003625f1b40 in gpu::webgpu::(anonymous namespace)::AsyncWorkerTaskPool::RunWorkerTask(void (*)(void*), void*, gl::ProgressReporter*, scoped_refptr<gpu::webgpu::(anonymous namespace)::AsyncWaitableEventImpl>)+0x140 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x186f9b40)
    #2 0x0003625f22f0 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(void (*)(void*), void*, gl::ProgressReporter*, scoped_refptr<gpu::webgpu::(anonymous namespace)::AsyncWaitableEventImpl>), void (*&&)(void*), void*&&, base::raw_ptr<gl::ProgressReporter, (partition_alloc::internal::RawPtrTraits)0>&&, scoped_refptr<gpu::webgpu::(anonymous namespace)::AsyncWaitableEventImpl>&&>, base::internal::BindState<false, true, false, void (*)(void (*)(void*), void*, gl::ProgressReporter*, scoped_refptr<gpu::webgpu::(anonymous namespace)::AsyncWaitableEventImpl>), base::internal::UnretainedWrapper<void (void*), base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<void, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<gl::ProgressReporter, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<gpu::webgpu::(anonymous namespace)::AsyncWaitableEventImpl>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x22c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x186fa2f0)
    #3 0x00035c402a34 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1250aa34)
    #4 0x00035c48ad04 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1f0 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12592d04)
    #5 0x00035c48af50 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xec (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12592f50)
    #6 0x00035c48988c in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType)+0x3fc (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1259188c)
    #7 0x00035c488c54 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x548 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12590c54)
    #8 0x00035c4c53a0 in base::internal::WorkerThread::RunWorker()+0x834 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125cd3a0)
    #9 0x00035c4c4858 in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125cc858)
    #10 0x00035c4c4210 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125cc210)
    #11 0x00035c53835c in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1264035c)
    #12 0x000102a7d870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #13 0x00018251fc04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #14 0x00018251aba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

0x6020005cad58 is located 8 bytes inside of 16-byte region [0x6020005cad50,0x6020005cad60)
freed by thread T0 here:
    #0 0x000102a81074 in __asan_memmove+0x308c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x55074)
    #1 0x000349f998f8 in absl::container_internal::IterateOverFullSlots(absl::container_internal::CommonFields const&, unsigned long, absl::FunctionRef<void (absl::container_internal::ctrl_t const*, void*)>)+0x190 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0xa18f8)
    #2 0x00034b11ccbc in absl::container_internal::raw_hash_set<absl::container_internal::FlatHashSetPolicy<std::__Cr::unique_ptr<dawn::native::AsyncTaskManager::WaitableTask, std::__Cr::default_delete<dawn::native::AsyncTaskManager::WaitableTask>>>>::destructor_impl()+0x208 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1224cbc)
    #3 0x00034b119494 in dawn::native::AsyncTaskManager::WaitAllPendingTasks()+0x168 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1221494)
    #4 0x00034b1e72a4 in dawn::native::DeviceBase::Destroy(dawn::native::DestroyReason)+0x22c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12ef2a4)
    #5 0x00034b0bd59c in dawn::native::NativeDeviceDestroy(WGPUDeviceImpl*)+0xc8 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x11c559c)
    #6 0x0003626b7358 in dawn::wire::server::Server::DoDeviceDestroy(WGPUDeviceImpl*)+0x40 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x187bf358)
    #7 0x0003626d6cc8 in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long)+0x209c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x187decc8)
    #8 0x00036270a728 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long)+0x154 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x18812728)
    #9 0x00036270ab2c in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*)+0x2e8 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x18812b2c)
    #10 0x000362700ac8 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*)+0x200 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x18808ac8)
    #11 0x000351d8af30 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x4bc (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7e92f30)
    #12 0x000362616764 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)+0x450 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1871e764)
    #13 0x0003626158e4 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)+0x468 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1871d8e4)
    #14 0x0003626341ec in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)+0x290 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1873c1ec)
    #15 0x00036263fe8c in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)+0x144 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x18747e8c)
    #16 0x00036263fca4 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)+0x118 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x18747ca4)
    #17 0x000351dc3d80 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x1c8 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7ecbd80)
    #18 0x000351d9e860 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x634 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7ea6860)
    #19 0x000351d9cef8 in gpu::Scheduler::RunNextTask()+0x27c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7ea4ef8)
    #20 0x000351da0294 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7ea8294)
    #21 0x00035c402a34 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1250aa34)
    #22 0x00035c46a9e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125729e8)
    #23 0x00035c469da0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12571da0)
    #24 0x00035c58b61c in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1269361c)
    #25 0x00035c57cc9c in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12684c9c)
    #26 0x00035c589a48 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xe4 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12691a48)
    #27 0x0001825bea04 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5fa04)
    #28 0x0001825be998 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f998)
    #29 0x0001825be704 in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5f704)

previously allocated by thread T0 here:
    #0 0x000102a80f84 in __asan_memmove+0x2f9c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x54f84)
    #1 0x0003729e04dc in operator new(unsigned long)+0x18 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x28ae84dc)
    #2 0x00034b1199f8 in dawn::native::AsyncTaskManager::PostConstructedTask(dawn::Ref<dawn::native::AsyncTask>)+0x100 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12219f8)
    #3 0x00034b1de844 in dawn::Ref<dawn::native::AsyncTask> dawn::native::AsyncTaskManager::PostTask<dawn::native::AsyncTask, dawn::native::CreatePipelineAsyncEvent<dawn::native::ComputePipelineBase, WGPUCreateComputePipelineAsyncCallbackInfo>::InitializeAsync()::'lambda'()>(dawn::native::CreatePipelineAsyncEvent<dawn::native::ComputePipelineBase, WGPUCreateComputePipelineAsyncCallbackInfo>::InitializeAsync()::'lambda'()&&)+0x178 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12e6844)
    #4 0x00034b1de600 in dawn::native::CreatePipelineAsyncEvent<dawn::native::ComputePipelineBase, WGPUCreateComputePipelineAsyncCallbackInfo>::InitializeAsync()+0x1fc (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12e6600)
    #5 0x00034b1f20c0 in dawn::native::DeviceBase::APICreateComputePipelineAsync(dawn::native::ComputePipelineDescriptor const*, WGPUCreateComputePipelineAsyncCallbackInfo const&)+0x7c0 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12fa0c0)
    #6 0x00034b0bc5b0 in dawn::native::NativeDeviceCreateComputePipelineAsync(WGPUDeviceImpl*, WGPUComputePipelineDescriptor const*, WGPUCreateComputePipelineAsyncCallbackInfo)+0xe0 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x11c45b0)
    #7 0x0003626c37dc in dawn::wire::server::Server::DoDeviceCreateComputePipelineAsync(dawn::wire::server::Known<WGPUDeviceImpl*>, dawn::wire::ObjectHandle, WGPUFuture, dawn::wire::ObjectHandle, WGPUComputePipelineDescriptor const*)+0x2a8 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x187cb7dc)
    #8 0x0003626cf204 in dawn::wire::server::Server::HandleDeviceCreateComputePipelineAsync(dawn::wire::DeserializeBuffer*)+0x238 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x187d7204)
    #9 0x0003626d5434 in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long)+0x808 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x187dd434)
    #10 0x00036270a728 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long)+0x154 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x18812728)
    #11 0x00036270ab2c in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*)+0x2e8 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x18812b2c)
    #12 0x000362700ac8 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*)+0x200 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x18808ac8)
    #13 0x000351d8af30 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)+0x4bc (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7e92f30)
    #14 0x000362616764 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)+0x450 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1871e764)
    #15 0x0003626158e4 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)+0x468 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1871d8e4)
    #16 0x0003626341ec in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)+0x290 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1873c1ec)
    #17 0x00036263fe8c in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)+0x144 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x18747e8c)
    #18 0x00036263fca4 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)+0x118 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x18747ca4)
    #19 0x000351dc3d80 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x1c8 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7ecbd80)
    #20 0x000351d9e860 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)+0x634 (/Users/sweetchip/Deskto
                                                                                                                                                     p/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7ea6860)
    #21 0x000351d9cef8 in gpu::Scheduler::RunNextTask()+0x27c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7ea4ef8)
    #22 0x000351da0294 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7ea8294)
    #23 0x00035c402a34 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1250aa34)
    #24 0x00035c46a9e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125729e8)
    #25 0x00035c469da0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12571da0)
    #26 0x00035c58b61c in base::MessagePumpCFRunLoopBase::RunWork()+0x1c8 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1269361c)
    #27 0x00035c57cc9c in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12684c9c)
    #28 0x00035c589a48 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xe4 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12691a48)
    #29 0x0001825bea04 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x5fa04)

Thread T19 created by T13 here:
    #0 0x000102a7795c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x00035c5378fc in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1263f8fc)
    #2 0x00035c4c31d8 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x27c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125cb1d8)
    #3 0x00035c490488 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x244 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12598488)
    #4 0x00035c4901e4 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x44 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125981e4)
    #5 0x00035c49808c in base::internal::ThreadGroupImpl::WorkerDelegate::GetWork(base::internal::WorkerThread*)+0x2c4 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125a008c)
    #6 0x00035c4c5264 in base::internal::WorkerThread::RunWorker()+0x6f8 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125cd264)
    #7 0x00035c4c4858 in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125cc858)
    #8 0x00035c4c4210 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125cc210)
    #9 0x00035c53835c in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1264035c)
    #10 0x000102a7d870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #11 0x00018251fc04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #12 0x00018251aba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

Thread T13 created by T8 here:
    #0 0x000102a7795c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x00035c5378fc in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1263f8fc)
    #2 0x00035c4c31d8 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x27c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125cb1d8)
    #3 0x00035c490488 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x244 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12598488)
    #4 0x00035c4901e4 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x44 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125981e4)
    #5 0x00035c49808c in base::internal::ThreadGroupImpl::WorkerDelegate::GetWork(base::internal::WorkerThread*)+0x2c4 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125a008c)
    #6 0x00035c4c5264 in base::internal::WorkerThread::RunWorker()+0x6f8 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125cd264)
    #7 0x00035c4c4858 in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125cc858)
    #8 0x00035c4c4210 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125cc210)
    #9 0x00035c53835c in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1264035c)
    #10 0x000102a7d870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #11 0x00018251fc04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #12 0x00018251aba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

Thread T8 created by T0 here:
    #0 0x000102a7795c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x00035c5378fc in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1263f8fc)
    #2 0x00035c4c31d8 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x27c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125cb1d8)
    #3 0x00035c490488 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x244 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x12598488)
    #4 0x00035c4901e4 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x44 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125981e4)
    #5 0x00035c4963a4 in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>)+0x3a8 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1259e3a4)
    #6 0x00035c4b7630 in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*)+0x107c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125bf630)
    #7 0x00035c4c20f8 in base::ThreadPoolInstance::StartWithDefaultParams()+0x144 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x125ca0f8)
    #8 0x000365b270e8 in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>, bool)+0x338 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1bc2f0e8)
    #9 0x00036575e70c in content::GpuMain(content::MainFunctionParams)+0x710 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x1b86670c)
    #10 0x000358ae4298 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0xebec298)
    #11 0x000358ae6418 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0xebee418)
    #12 0x000358ae1f88 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0xebe9f88)
    #13 0x000358ae2478 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0xebea478)
    #14 0x000349efdcb4 in ChromeMain+0x490 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x5cb4)
    #15 0x0001026f8c94 in main+0x254 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Helpers/Chromium Helper.app/Contents/MacOS/Chromium Helper:arm64+0x100000c94)
    #16 0x000182155d50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x122248c) in dawn::native::AsyncTaskManager::RunTask(void*)+0xb0
Shadow bytes around the buggy address:
  0x6020005caa80: f7 fa fa fa f7 fa fd fa f7 fa fd fa f7 fa fd fd
  0x6020005cab00: f7 fa fd fa f7 fa fd fd f7 fa fd fd f7 fa fd fd
  0x6020005cab80: f7 fa fd fa f7 fa fa fa f7 fa fa fa f7 fa fd fd
  0x6020005cac00: f7 fa fd fa f7 fa fd fd f7 fa fd fd f7 fa fa fa
  0x6020005cac80: f7 fa fd fd f7 fa 00 00 f7 fa fd fd f7 fa fd fd
=>0x6020005cad00: f7 fa fd fd f7 fa fd fa f7 fa fd[fd]f7 fa fa fa
  0x6020005cad80: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fa fa
  0x6020005cae00: f7 fa fd fd f7 fa 00 00 f7 fa fd fd f7 fa fd fd
  0x6020005cae80: f7 fa fa fa f7 fa fa fa f7 fa fd fa f7 fa fa fa
  0x6020005caf00: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fd
  0x6020005caf80: f7 fa fa fa f7 fa fd fd f7 fa fd fa f7 fa fd fa
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

==72180==ADDITIONAL INFO

==72180==Note: Please include this section with the ASan report.
Task trace:
    #0 0x0003625f1260 in gpu::webgpu::(anonymous namespace)::AsyncWorkerTaskPool::PostWorkerTask(void (*)(void*), void*)+0x1e4 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x186f9260)
    #1 0x000351d9d0a0 in gpu::Scheduler::RunNextTask()+0x424 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7ea50a0)
    #2 0x000351d9d0a0 in gpu::Scheduler::RunNextTask()+0x424 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7ea50a0)
    #3 0x000351d9d0a0 in gpu::Scheduler::RunNextTask()+0x424 (/Users/sweetchip/Desktop/bug_finder/browser_artifact/mac-release-arm64_asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/147.0.7727.0/Chromium Framework:arm64+0x7ea50a0)
......


MiraclePtr Status: MANUAL ANALYSIS REQUIRED
This crash occurred inside a callback where a raw_ptr<T> pointing to the same region was bound to one of the arguments.
The "use" and "free" threads don't match. This crash is likely to have been caused by a race condition that is mislabeled as a use-after-free. Make sure that the "free" is sequenced after the "use" (e.g. both are on the same sequence, or the "free" is in a task posted after the "use"). Otherwise, the crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==72180==END OF ADDITIONAL INFO

==72180==ABORTING
[72172:1275285:0319/005256.254904:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256

```
#### Impact analysis

## Impact

The worker thread reads the freed `taskManager` pointer (offset 8 of 16-byte `WaitableTask`) and uses it as `this` for `HandleTaskCompletion()`, which acquires a mutex and performs a hash set erase at the attacker-influenced address — enabling potential control flow hijack in the GPU process. MiraclePtr may be ineffective because the use and free occur on different threads.

---

### The cause

#### What version of Chrome have you found the security issue in?

147.0.7727.0

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

sweetchip

## Attachments

- [poc_v5_reliable.html](attachments/poc_v5_reliable.html) (text/html, 6.2 KB)
- [poc_v7_throughput.html](attachments/poc_v7_throughput.html) (text/html, 9.9 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5830213757861888.

### ts...@google.com (2026-03-18)

CC'ing top-level owners.

### dx...@google.com (2026-03-25)

Project: dawn  

Branch:  main  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/299315>

[dawn][native] Updates AsyncTasks to remove need of WaitableEvent.

---


Expand for full commit details
```
     
    - Previously, the WaitableEvent and how it was being handled caused a 
      UAF as per the bug below. This change simplifies the logic in the 
      AsyncTasks to remove the WaitableEvent entirely, and get rid of the 
      need of the intermediate WaitableTask struct that we used to pair 
      the AsyncTask to it's manager. Since we know that the task's 
      manager must be the one that created it, we can track that 
      information at construction and use it directly later on. 
    - This change also updates the AsyncTask to use MutexCondVarProtected 
      for synchronization. 
     
    Bug: 493900619 
    Change-Id: I45da53638727ac86d60e9ffd317ad342fced3174 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299315 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Loko Kung <lokokung@google.com>

```

---

Files:

- M `src/dawn/native/AsyncTask.cpp`
- M `src/dawn/native/AsyncTask.h`
- M `src/dawn/native/Device.cpp`
- M `src/dawn/tests/unittests/AsyncTaskTests.cpp`

---

Hash: 6742999c0f402758e439277ac9d6787acd14d022  

Date: Wed Mar 25 22:47:12 2026


---

### dx...@google.com (2026-03-26)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7701847>

Roll Dawn from c5c579183723 to 6742999c0f40 (6 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/c5c579183723..6742999c0f40 
     
    2026-03-25 lokokung@google.com [dawn][native] Updates AsyncTasks to remove need of WaitableEvent. 
    2026-03-25 kim.brandwijk@gmail.com metal: Map iOS depth/disparity IOSurface formats in SharedTextureMemory 
    2026-03-25 rharrison@chromium.org Document remaining UBU suppressions 
    2026-03-25 rharrison@chromium.org Rework unicode handling to reduce UBUs 
    2026-03-25 ynovikov@chromium.org Target macOS 15 or 26 on CI and Try Mac ARM64 builders 
    2026-03-25 dsinclair@chromium.org Cleanup glfw folder. 
     
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
    Bug: chromium:408010433,chromium:493339350,chromium:493610839,chromium:493761823,chromium:493900619 
    Tbr: jrprice@google.com 
    Change-Id: I43c389b0824144b882ee04f32f1908471b522c68 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7701847 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1605248}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [753768f4908c03c70e11fcd72ef16dac6a9e9b40](https://chromiumdash.appspot.com/commit/753768f4908c03c70e11fcd72ef16dac6a9e9b40)  

Date: Thu Mar 26 02:40:46 2026


---

### ch...@google.com (2026-03-26)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-26)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dr...@chromium.org (2026-03-27)

No crashes in Canary after 24 hours. Approved to merge to M146 and M147. Our release cut for M146 is Monday at 11am Pacific time, so please try to land by then.

### dx...@google.com (2026-03-30)

Project: dawn  

Branch:  chromium/7680  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/299955>

[M146] [dawn][native] Updates AsyncTasks to remove need of WaitableEvent.

---


Expand for full commit details
```
     
    - Previously, the WaitableEvent and how it was being handled caused a 
      UAF as per the bug below. This change simplifies the logic in the 
      AsyncTasks to remove the WaitableEvent entirely, and get rid of the 
      need of the intermediate WaitableTask struct that we used to pair 
      the AsyncTask to it's manager. Since we know that the task's 
      manager must be the one that created it, we can track that 
      information at construction and use it directly later on. 
    - This change also updates the AsyncTask to use MutexCondVarProtected 
      for synchronization. 
     
    Bug: 493900619 
    Change-Id: I45da53638727ac86d60e9ffd317ad342fced3174 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299315 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299955 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/dawn/native/AsyncTask.cpp`
- M `src/dawn/native/AsyncTask.h`
- M `src/dawn/native/Device.cpp`
- M `src/dawn/tests/unittests/AsyncTaskTests.cpp`

---

Hash: 10fb89e3179bb7443e66911eb3c795c7aaf022e5  

Date: Mon Mar 30 18:50:53 2026


---

### pe...@google.com (2026-03-30)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-03-30)

Project: dawn  

Branch:  chromium/7727  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/299897>

[M147] [dawn][native] Updates AsyncTasks to remove need of WaitableEvent.

---


Expand for full commit details
```
     
    - Previously, the WaitableEvent and how it was being handled caused a 
      UAF as per the bug below. This change simplifies the logic in the 
      AsyncTasks to remove the WaitableEvent entirely, and get rid of the 
      need of the intermediate WaitableTask struct that we used to pair 
      the AsyncTask to it's manager. Since we know that the task's 
      manager must be the one that created it, we can track that 
      information at construction and use it directly later on. 
    - This change also updates the AsyncTask to use MutexCondVarProtected 
      for synchronization. 
     
    Bug: 493900619 
    Change-Id: I45da53638727ac86d60e9ffd317ad342fced3174 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299315 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/299897 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/dawn/native/AsyncTask.cpp`
- M `src/dawn/native/AsyncTask.h`
- M `src/dawn/native/Device.cpp`
- M `src/dawn/tests/unittests/AsyncTaskTests.cpp`

---

Hash: c03bd8974619bdbc792a0cb943df8c07886b56c9  

Date: Mon Mar 30 19:01:04 2026


---

### vi...@google.com (2026-03-31)

I’ve labeled it as LTS-NotApplicable-138 because the AsyncTask refactored code which possibly introduced this bug (See <https://dawn-review.git.corp.google.com/c/dawn/+/263714>) was not present in the M138 LTS Dawn branch.

### sp...@google.com (2026-04-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
Baseline. Mildly mitigated (non-sandboxed) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-05-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-12)

I’m actually suggesting to not go ahead with 144 merge, because the proposed fix is convoluted with the notify mode template changes (<https://dawn-review.git.corp.google.com/c/dawn/+/290375>) that got added after 144. Labeling as `LTS-NotApplicable-144`.

### ch...@google.com (2026-07-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493900619)*
