# Use-After-Free in AsyncTaskManager::WaitAllPendingTasks Due to Early Task Destruction in GPU Process

| Field | Value |
|-------|-------|
| **Issue ID** | [492735369](https://issues.chromium.org/issues/492735369) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2026-5286 |
| **Reporter** | se...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-03-14 |
| **Bounty** | $11,000.00 |

## Description

## Summary

A race condition between `AsyncTaskManager::WaitAllPendingTasks` and worker threads executing `AsyncTaskManager::RunTask` in Dawn's native backend causes a heap use-after-free in the GPU process. The bug is triggered from the renderer via the Dawn wire protocol by creating asynchronous compute pipelines and immediately destroying the device. When `AsyncTask::Run()` clears `mWaitableEvent` before `RunTask` has finished executing, the concurrent `WaitAllPendingTasks` call skips waiting, destructs the pending task set, and frees the `WaitableTask` objects while worker threads still hold raw pointers to them. The vulnerability affects all platforms with WebGPU support (Windows, macOS, Linux, ChromeOS, Android) and requires no specific GPU hardware.

## Bisect

Introducing Commit: `bbfecec2b0979e30be689f83de1155995719d9db`

- Date: 2025-09-30
- Author: Geoff Lang ([geofflang@chromium.org](mailto:geofflang@chromium.org))
- Review: <https://dawn-review.googlesource.com/c/dawn/+/263714>

## Root Cause

Dawn's `AsyncTaskManager` manages asynchronous pipeline compilation by posting tasks to a worker thread pool. Each task is wrapped in a `WaitableTask` struct stored in `mPendingTasks`, and the worker thread pool receives a raw `void*` pointer to the `WaitableTask` as userdata for its callback.

```
// dawn/native/AsyncTask.h
struct WaitableTask : NonCopyable {
    Ref<AsyncTask> asyncTask;
    raw_ptr<AsyncTaskManager> taskManager;
};

```

When a task completes on a worker thread, `AsyncTaskManager::RunTask` is invoked with the `WaitableTask*` as userdata:

```
// dawn/native/AsyncTask.cpp:174-178
void AsyncTaskManager::RunTask(void* task) {
    WaitableTask* waitableTask = static_cast<WaitableTask*>(task);
    waitableTask->asyncTask->Run();
    waitableTask->taskManager->HandleTaskCompletion(waitableTask);
}

```

Inside `AsyncTask::Run()`, the method clears `mWaitableEvent` under a mutex lock after marking the task as completed:

```
// dawn/native/AsyncTask.cpp:76-83
{
    std::scoped_lock<std::mutex> lock(mMutex);
    AsyncTaskState prevState = mState.exchange(AsyncTaskState::Completed);
    DAWN_ASSERT(prevState == AsyncTaskState::Running);
    completionCallbacks = std::move(mCompletionCallbacks);
    mCompletionCallbacks.clear();
    mWaitableEvent = nullptr;
}

```

The `Wait()` method, used by `WaitAllPendingTasks`, moves `mWaitableEvent` out and only blocks if it is non-null:

```
// dawn/native/AsyncTask.cpp:38-48
void AsyncTask::Wait() {
    std::unique_ptr<dawn::platform::WaitableEvent> waitableEvent;
    {
        std::scoped_lock<std::mutex> lock(mMutex);
        waitableEvent = std::move(mWaitableEvent);
    }
    if (waitableEvent) {
        waitableEvent->Wait();
    }
}

```

When `DeviceBase::Destroy` is called, it invokes `WaitAllPendingTasks`, which atomically swaps all pending tasks into a local set, calls `Wait()` on each, and then lets the local set destruct:

```
// dawn/native/AsyncTask.cpp:160-168
void AsyncTaskManager::WaitAllPendingTasks() {
    PendingTasksSet allPendingTasks;
    mPendingTasks.Use(
        [&allPendingTasks](auto pendingTasks) { allPendingTasks.swap(*pendingTasks); });
    for (auto& task : allPendingTasks) {
        task->asyncTask->Wait();
    }
}

```

The race occurs when `Run()` has already set `mWaitableEvent` to nullptr (making the task appear completed to `Wait()`), but `RunTask` has not yet returned. In this window, `WaitAllPendingTasks` finds `mWaitableEvent` null, skips waiting, finishes iterating, and destructs `allPendingTasks`, which frees all `WaitableTask` objects via `unique_ptr` destructors. The worker thread then returns from `Run()` and attempts to dereference the freed `waitableTask` pointer to call `HandleTaskCompletion`, producing a heap use-after-free.

In Chromium's GPU process, the platform `WaitableEvent` (backed by `base::WaitableEvent` in `dawn_platform.cc`) is only signaled after the callback returns. This means the race is not mitigated by the platform layer; it is purely a Dawn-internal lifetime management issue where `AsyncTask::Run()` prematurely advertises task completion by clearing `mWaitableEvent` before `RunTask` has finished.

The `WaitableTask` struct contains a `raw_ptr<AsyncTaskManager> taskManager` field, and the ASAN crash location at `raw_ptr.h:1012` confirms the UAF triggers when dereferencing this `raw_ptr`. However, MiraclePtr does not prevent this crash. The `WaitableTask` object is freed first, which destroys the `raw_ptr` and its associated BRP ref count metadata. An attacker who reclaims the freed 16-byte `WaitableTask` region via heap spraying can overwrite the `raw_ptr` field with arbitrary content, at which point MiraclePtr has no surviving bookkeeping to detect the dangling access. The ASAN report marks this as "MANUAL ANALYSIS REQUIRED" because the "use" and "free" occur on different threads; the manual conclusion is that MiraclePtr is ineffective here since the container object is freed before the pointer is dereferenced.

## Reproduce

This issue reproduces a heap-use-after-free in Dawn's AsyncTaskManager, where WaitAllPendingTasks races with worker threads still executing RunTask. The bug manifests in the GPU process and can be triggered from a compromised renderer via the Dawn wire protocol.

Tested at commit `45a2cb21a2a229660d9df813e554ac3a4f0cadc6` on macOS and Linux.

Build asan chromium(`is_asan = true; is_debug = false; dcheck_always_on = false`):

```
git apply patch.diff
autoninja -C out/asan chrome

```

The patch adds a 200ms sleep in AsyncTaskManager::RunTask between the call to AsyncTask::Run() and the subsequent access to the WaitableTask pointer. This widens the natural race window.

Launch Chrome:

```
# macOS
./out/asan/Chromium.app/Contents/MacOS/Chromium --user-data-dir=./userdata --enable-logging=stderr poc.html

# Linux
./out/asan/chrome --user-data-dir=./userdata --enable-logging=stderr --enable-unsafe-webgpu poc.html

```

ASAN log:

```
=================================================================
==942717==ERROR: AddressSanitizer: heap-use-after-free on address 0x79771828b6f8 at pc 0x61e65be05ea8 bp 0x7955815cb550 sp 0x7955815cb548
READ of size 8 at 0x79771828b6f8 thread T324 (ThreadPoolForeg)
    #0 0x61e65be05ea7 in dawn::native::AsyncTaskManager::RunTask(void*) base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:1012:48
    #1 0x61e67ae92333 in gpu::webgpu::(anonymous namespace)::AsyncWorkerTaskPool::RunWorkerTask(void (*)(void*), void*, gl::ProgressReporter*, scoped_refptr<gpu::webgpu::(anonymous namespace)::AsyncWaitableEventImpl>) gpu/command_buffer/service/dawn_platform.cc:124:5
    #2 0x61e67ae92c1a in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(void (*)(void*), void*, gl::ProgressReporter*, scoped_refptr<gpu::webgpu::(anonymous namespace)::AsyncWaitableEventImpl>), void (*&&)(void*), void*&&, base::raw_ptr<gl::ProgressReporter, (partition_alloc::internal::RawPtrTraits)0>&&, scoped_refptr<gpu::webgpu::(anonymous namespace)::AsyncWaitableEventImpl>&&>, base::internal::BindState<false, true, false, void (*)(void (*)(void*), void*, gl::ProgressReporter*, scoped_refptr<gpu::webgpu::(anonymous namespace)::AsyncWaitableEventImpl>), base::internal::UnretainedWrapper<void (void*), base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<void, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<gl::ProgressReporter, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<gpu::webgpu::(anonymous namespace)::AsyncWaitableEventImpl>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:673:12
    #3 0x61e671903cf6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #4 0x61e6719a29c2 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/common/task_annotator.h:112:5
    #5 0x61e6719a2c0c in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:676:3
    #6 0x61e6719a11f9 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType) base/task/thread_pool/task_tracker.cc:706:7
    #7 0x61e6719a0482 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:394:5
    #8 0x61e6719e51b3 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:473:36
    #9 0x61e6719e42f4 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #10 0x61e6719e3d5b in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #11 0x61e671a6d26e in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #12 0x61e65a09bc46 in asan_thread_start(void*) asan_interceptors.cpp

0x79771828b6f8 is located 8 bytes inside of 16-byte region [0x79771828b6f0,0x79771828b700)
freed by thread T0 (chrome) here:
    #0 0x61e65a0d8002 in operator delete(void*, unsigned long) (/home/test/Desktop/chromium/src/out/asan/chrome+0x10ed1002) (BuildId: 562837dd080b5dc4)
    #1 0x61e65a19ec1c in absl::container_internal::IterateOverFullSlots(absl::container_internal::CommonFields const&, unsigned long, absl::FunctionRef<void (absl::container_internal::ctrl_t const*, void*)>) third_party/abseil-cpp/absl/functional/function_ref.h:165:12
    #2 0x61e65be08d75 in absl::container_internal::raw_hash_set<absl::container_internal::FlatHashSetPolicy<std::__Cr::unique_ptr<dawn::native::AsyncTaskManager::WaitableTask, std::__Cr::default_delete<dawn::native::AsyncTaskManager::WaitableTask>>>>::destructor_impl() third_party/abseil-cpp/absl/container/internal/raw_hash_set.h:3074:7
    #3 0x61e65be04e4a in dawn::native::AsyncTaskManager::WaitAllPendingTasks() third_party/abseil-cpp/absl/container/internal/raw_hash_set.h:2348:5
    #4 0x61e65bef9316 in dawn::native::DeviceBase::Destroy(dawn::native::DestroyReason) third_party/dawn/src/dawn/native/Device.cpp:662:28
    #5 0x61e65bd93f72 in dawn::native::NativeDeviceDestroy(WGPUDeviceImpl*) gen/third_party/dawn/src/dawn/native/ProcTable.cpp:946:15
    #6 0x61e67b7c67bd in dawn::wire::server::Server::DoDeviceDestroy(WGPUDeviceImpl*) gen/third_party/dawn/src/dawn/wire/server/ServerDoers_autogen.cpp:494:9
    #7 0x61e67b7bb0cb in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:692:18
    #8 0x61e67b7741a7 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:155:33
    #9 0x61e67b77461d in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2001:22
    #10 0x61e67b768512 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1946:18
    #11 0x61e664cdd814 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:267:35
    #12 0x61e67aea006b in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:504:22
    #13 0x61e67ae9f2d1 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:173:7
    #14 0x61e67aec23bc in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:833:13
    #15 0x61e67aed03a7 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #16 0x61e67aed0189 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #17 0x61e664d20211 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/callback.h:155:12
    #18 0x61e664cf4957 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) base/functional/callback.h:155:12
    #19 0x61e664cf2988 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:625:3
    #20 0x61e664cf6571 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #21 0x61e671903cf6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #22 0x61e67197b509 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #23 0x61e67197a37a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #24 0x61e671b28fe4 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:782:48
    #25 0x61e67197cc17 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #26 0x61e67187f290 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #27 0x61e67d25b41c in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:479:14
    #28 0x61e66d57619f in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #29 0x61e66d5774cf in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12

previously allocated by thread T0 (chrome) here:
    #0 0x61e65a0d73fd in operator new(unsigned long) (/home/test/Desktop/chromium/src/out/asan/chrome+0x10ed03fd) (BuildId: 562837dd080b5dc4)
    #1 0x61e65be0513c in dawn::native::AsyncTaskManager::PostConstructedTask(dawn::Ref<dawn::native::AsyncTask>) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:26
    #2 0x61e65beee722 in dawn::Ref<dawn::native::AsyncTask> dawn::native::AsyncTaskManager::PostTask<dawn::native::AsyncTask, dawn::native::CreatePipelineAsyncEvent<dawn::native::ComputePipelineBase, WGPUCreateComputePipelineAsyncCallbackInfo>::InitializeAsync()::'lambda'()>(dawn::native::CreatePipelineAsyncEvent<dawn::native::ComputePipelineBase, WGPUCreateComputePipelineAsyncCallbackInfo>::InitializeAsync()::'lambda'()&&) third_party/dawn/src/dawn/native/AsyncTask.h:117:9
    #3 0x61e65beee46f in dawn::native::CreatePipelineAsyncEvent<dawn::native::ComputePipelineBase, WGPUCreateComputePipelineAsyncCallbackInfo>::InitializeAsync() third_party/dawn/src/dawn/native/CreatePipelineAsyncEvent.cpp:177:36
    #4 0x61e65bf06b1b in dawn::native::DeviceBase::APICreateComputePipelineAsync(dawn::native::ComputePipelineDescriptor const*, WGPUCreateComputePipelineAsyncCallbackInfo const&) third_party/dawn/src/dawn/native/Device.cpp:1450:5
    #5 0x61e65bd92dbf in dawn::native::NativeDeviceCreateComputePipelineAsync(WGPUDeviceImpl*, WGPUComputePipelineDescriptor const*, WGPUCreateComputePipelineAsyncCallbackInfo) gen/third_party/dawn/src/dawn/native/ProcTable.cpp:786:36
    #6 0x61e67b7a9a05 in dawn::wire::server::Server::DoDeviceCreateComputePipelineAsync(dawn::wire::server::Known<WGPUDeviceImpl*>, dawn::wire::ObjectHandle, WGPUFuture, dawn::wire::ObjectHandle, WGPUComputePipelineDescriptor const*) third_party/dawn/src/dawn/wire/server/ServerDevice.cpp:111:5
    #7 0x61e67b7b0bf4 in dawn::wire::server::Server::HandleDeviceCreateComputePipelineAsync(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:501:18
    #8 0x61e67b7b8325 in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1787:30
    #9 0x61e67b7741a7 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:155:33
    #10 0x61e67b77461d in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2001:22
    #11 0x61e67b768512 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1946:18
    #12 0x61e664cdd814 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:267:35
    #13 0x61e67aea006b in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:504:22
    #14 0x61e67ae9f2d1 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:173:7
    #15 0x61e67aec23bc in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:833:13
    #16 0x61e67aed03a7 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #17 0x61e67aed0189 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #18 0x61e664d20211 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/callback.h:155:12
    #19 0x61e664cf4957 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) base/functional/callback.h:155:12
    #20 0x61e664cf2988 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:625:3
    #21 0x61e664cf6571 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #22 0x61e671903cf6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #23 0x61e67197b509 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #24 0x61e67197a37a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #25 0x61e671b286a8 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:736:46
    #26 0x61e671b2bc68 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:355:43
    #27 0x7d571b2cad3a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x55d3a) (BuildId: 6b4f160dbc5397c2f502dc4f08a8cff259917926)

Thread T324 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x61e65a081a71 in pthread_create (/home/test/Desktop/chromium/src/out/asan/chrome+0x10e7aa71) (BuildId: 562837dd080b5dc4)
    #1 0x61e671a6c8c2 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x61e6719e2aa4 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:185:3
    #3 0x61e6719da095 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() base/task/thread_pool/thread_group.cc:65:13
    #4 0x61e6719d9d50 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() base/task/thread_pool/thread_group.cc:56:3
    #5 0x61e6719d0558 in base::internal::ThreadGroupImpl::PushTaskSourceAndWakeUpWorkers(base::internal::RegisteredTaskSourceAndTransaction) base/task/thread_pool/thread_group_impl.cc:71:3
    #6 0x61e6719ae86b in base::internal::ThreadPoolImpl::PostTaskWithSequenceNow(base::internal::Task, scoped_refptr<base::internal::Sequence>) base/task/thread_pool/thread_pool_impl.cc:569:11
    #7 0x61e6719aee6a in base::internal::ThreadPoolImpl::PostTaskWithSequence(base::internal::Task, scoped_refptr<base::internal::Sequence>) base/task/thread_pool/thread_pool_impl.cc:599:12
    #8 0x61e6719aa09e in base::internal::ThreadPoolImpl::PostDelayedTask(base::Location const&, base::TaskTraits const&, base::OnceCallback<void ()>, base::TimeDelta) base/task/thread_pool/thread_pool_impl.cc:331:10
    #9 0x61e671996f6e in base::ThreadPool::PostTask(base::Location const&, base::TaskTraits const&, base::OnceCallback<void ()>) base/task/thread_pool.cc:66:31
    #10 0x61e67ae91bbc in gpu::webgpu::(anonymous namespace)::AsyncWorkerTaskPool::PostWorkerTask(void (*)(void*), void*) gpu/command_buffer/service/dawn_platform.cc:99:5
    #11 0x61e65be05427 in dawn::native::AsyncTaskManager::PostConstructedTask(dawn::Ref<dawn::native::AsyncTask>) third_party/dawn/src/dawn/native/AsyncTask.cpp:151:51
    #12 0x61e65beee722 in dawn::Ref<dawn::native::AsyncTask> dawn::native::AsyncTaskManager::PostTask<dawn::native::AsyncTask, dawn::native::CreatePipelineAsyncEvent<dawn::native::ComputePipelineBase, WGPUCreateComputePipelineAsyncCallbackInfo>::InitializeAsync()::'lambda'()>(dawn::native::CreatePipelineAsyncEvent<dawn::native::ComputePipelineBase, WGPUCreateComputePipelineAsyncCallbackInfo>::InitializeAsync()::'lambda'()&&) third_party/dawn/src/dawn/native/AsyncTask.h:117:9
    #13 0x61e65beee46f in dawn::native::CreatePipelineAsyncEvent<dawn::native::ComputePipelineBase, WGPUCreateComputePipelineAsyncCallbackInfo>::InitializeAsync() third_party/dawn/src/dawn/native/CreatePipelineAsyncEvent.cpp:177:36
    #14 0x61e65bf06b1b in dawn::native::DeviceBase::APICreateComputePipelineAsync(dawn::native::ComputePipelineDescriptor const*, WGPUCreateComputePipelineAsyncCallbackInfo const&) third_party/dawn/src/dawn/native/Device.cpp:1450:5
    #15 0x61e65bd92dbf in dawn::native::NativeDeviceCreateComputePipelineAsync(WGPUDeviceImpl*, WGPUComputePipelineDescriptor const*, WGPUCreateComputePipelineAsyncCallbackInfo) gen/third_party/dawn/src/dawn/native/ProcTable.cpp:786:36
    #16 0x61e67b7a9a05 in dawn::wire::server::Server::DoDeviceCreateComputePipelineAsync(dawn::wire::server::Known<WGPUDeviceImpl*>, dawn::wire::ObjectHandle, WGPUFuture, dawn::wire::ObjectHandle, WGPUComputePipelineDescriptor const*) third_party/dawn/src/dawn/wire/server/ServerDevice.cpp:111:5
    #17 0x61e67b7b0bf4 in dawn::wire::server::Server::HandleDeviceCreateComputePipelineAsync(dawn::wire::DeserializeBuffer*) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:501:18
    #18 0x61e67b7b8325 in dawn::wire::server::Server::HandleCommands(char const volatile*, unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1787:30
    #19 0x61e67b7741a7 in gpu::webgpu::(anonymous namespace)::DawnWireServer::HandleCommands(char const volatile*, unsigned long) gpu/command_buffer/service/webgpu_decoder_impl.cc:155:33
    #20 0x61e67b77461d in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::HandleDawnCommands(unsigned int, void const volatile*) gpu/command_buffer/service/webgpu_decoder_impl.cc:2001:22
    #21 0x61e67b768512 in gpu::webgpu::(anonymous namespace)::WebGPUDecoderImpl::DoCommands(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/webgpu_decoder_impl.cc:1946:18
    #22 0x61e664cdd814 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:267:35
    #23 0x61e67aea006b in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:504:22
    #24 0x61e67ae9f2d1 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:173:7
    #25 0x61e67aec23bc in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:833:13
    #26 0x61e67aed03a7 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #27 0x61e67aed0189 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #28 0x61e664d20211 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/callback.h:155:12
    #29 0x61e664cf4957 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) base/functional/callback.h:155:12
    #30 0x61e664cf2988 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:625:3
    #31 0x61e664cf6571 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #32 0x61e671903cf6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #33 0x61e67197b509 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #34 0x61e67197a37a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #35 0x61e671b286a8 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:736:46
    #36 0x61e671b2bc68 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:355:43
    #37 0x7d571b2cad3a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x55d3a) (BuildId: 6b4f160dbc5397c2f502dc4f08a8cff259917926)

SUMMARY: AddressSanitizer: heap-use-after-free base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:1012:48 in dawn::native::AsyncTaskManager::RunTask(void*)
Shadow bytes around the buggy address:
  0x79771828b400: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa fd fd
  0x79771828b480: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fa
  0x79771828b500: f7 fa fd fa f7 fa fd fd f7 fa fd fd f7 fa fd fa
  0x79771828b580: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x79771828b600: f7 fa fd fd f7 fa fd fd f7 fa fd fa f7 fa fd fd
=>0x79771828b680: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd[fd]
  0x79771828b700: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x79771828b780: f7 fa fd fa f7 fa 00 00 f7 fa 00 00 f7 fa fd fa
  0x79771828b800: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x79771828b880: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x79771828b900: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
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

==942717==ADDITIONAL INFO

==942717==Note: Please include this section with the ASan report.
Task trace:
    #0 0x61e67ae9194d in gpu::webgpu::(anonymous namespace)::AsyncWorkerTaskPool::PostWorkerTask(void (*)(void*), void*) gpu/command_buffer/service/dawn_platform.cc:100:9
    #1 0x61e664cf2e62 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #2 0x61e664cf2e62 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #3 0x61e664cf2e62 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27

MiraclePtr Status: MANUAL ANALYSIS REQUIRED
This crash occurred inside a callback where a raw_ptr<T> pointing to the same region was bound to one of the arguments.
The "use" and "free" threads don't match. This crash is likely to have been caused by a race condition that is mislabeled as a use-after-free. Make sure that the "free" is sequenced after the "use" (e.g. both are on the same sequence, or the "free" is in a task posted after the "use"). Otherwise, the crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==942717==END OF ADDITIONAL INFO

==942717==ABORTING
[942681:942681:0314/231704.217466:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256

```
## References

- [dawn/native/AsyncTask.cpp (Run, WaitAllPendingTasks, RunTask)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/AsyncTask.cpp;l=62-178)
- [dawn/native/AsyncTask.h (WaitableTask struct)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/AsyncTask.h;l=125-128)
- [dawn/native/Device.cpp (Destroy calling WaitAllPendingTasks)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/Device.cpp;l=662)
- [gpu/command\_buffer/service/dawn\_platform.cc (Chromium WorkerTaskPool)](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/dawn_platform.cc;l=88-144)
- [dawn/native/CreatePipelineAsyncEvent.cpp (InitializeAsync posting tasks)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/CreatePipelineAsyncEvent.cpp;l=170-178)

## Credit

Please use 86ac1f1587b71893ed2ad792cd7dde32 as the credit for this vulnerability. Thank you.

## Attachments

- [patch.diff](attachments/patch.diff) (text/x-diff, 575 B)
- [poc.html](attachments/poc.html) (text/html, 2.0 KB)

## Timeline

### ke...@chromium.org (2026-03-17)

Thanks for the report.

This is a crash so I'm passing it to geofflang@, but I don't think it's a vulnerability so I have converted it to a bug.

In particular, this doesn't match what ASAN is reporting:

> The WaitableTask object is freed first, which destroys the raw\_ptr and its associated BRP ref count metadata. An attacker who reclaims the freed 16-byte WaitableTask region via heap spraying can overwrite the raw\_ptr field with arbitrary content, at which point MiraclePtr has no surviving bookkeeping to detect the dangling access.

If the `WaitableTask` was freed and then its memory was being accessed, ASAN would flag that as the UaF. But it is flagging access to the `raw_ptr<AsyncTaskManager>` as the UaF, which is protected by MiraclePtr.

MiraclePtr saying "MANUAL ANALYSIS NEEDED" means there was a raw pointer taken from the `raw_ptr` at some point, and it can't say for sure that it isn't dangling. There is no evidence of such a pointer being dereferenced.

### se...@gmail.com (2026-04-01)

Hi Chrome Security Team,

I'm writing regarding [Issue 493900619](https://issues.chromium.org/issues/493900619) — [High] CVE-2026-5286: Use after free in Dawn, which was reported by sweetchip on 2026-03-18 and has since been fixed.

I reported the same vulnerability earlier in [Issue 492735369](https://issues.chromium.org/issues/492735369). However, my report was downgraded to a non-security bug at the time. I didn't follow up on this immediately, but I recently reviewed the patch and noticed that this UAF is not protected by MiraclePtr. This means the vulnerability is exploitable and should not have been classified as a non-security bug.

Given that:

1. My report predates sweetchip's report ([Issue 493900619](https://issues.chromium.org/issues/493900619)).
2. The UAF is not mitigated by MiraclePtr, confirming it is a genuine security vulnerability.
3. Google has already patched the issue and assigned CVE-2026-5286 with a High severity rating.

I'd like to request the following:

- Duplicate [Issue 493900619](https://issues.chromium.org/issues/493900619) to my original report ([Issue 492735369](https://issues.chromium.org/issues/492735369)).
- Reclassify [Issue 492735369](https://issues.chromium.org/issues/492735369) as a security vulnerability (Type: vulnerability) rather than a regular bug.
- Evaluate the VRP reward accordingly, as my report was the first to identify this vulnerability.

Happy to provide any additional details if needed. Thank you for your time.

### se...@gmail.com (2026-04-16)

Hi, any update?

### lo...@google.com (2026-04-21)

Hi, yea this does in fact seem like an earlier report of symptoms that have the same root cause as [b/493900619](https://issues.chromium.org/issues/493900619) which I have since fixed. It might make sense to re-evaluate the two bugs as suggested in [comment#3](https://issues.chromium.org/issues/492735369#comment3).

### aj...@google.com (2026-04-23)

panel: see comment 3

### ns...@chromium.org (2026-05-04)

> Hi, yea this does in fact seem like an earlier report of symptoms that have the same root cause as [b/493900619](https://issues.chromium.org/issues/493900619) which I have since fixed. It might make sense to re-evaluate the two bugs as suggested in [comment#3](https://issues.chromium.org/issues/492735369#comment3).

@lo...@google.com I've copied the missing metadata from [b/493900619](https://issues.chromium.org/issues/493900619) into this one. Should this be marked as fixed then?

### ge...@google.com (2026-05-05)

Yes, let's mark this as fixed.

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
Mildly mitigated (sandboxed/renderer)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492735369)*
