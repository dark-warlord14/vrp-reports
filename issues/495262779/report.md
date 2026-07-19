# Security: heap-use-after-free in gpu::SyncToken::operator=(gpu::SyncToken const&)

| Field | Value |
|-------|-------|
| **Issue ID** | [495262779](https://issues.chromium.org/issues/495262779) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Mac |
| **Chrome Version** | 146.0.0.0 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | il...@chromium.org |
| **Created** | 2026-03-23 |
| **Bounty** | $7,000.00 |

## Description

# Steps to reproduce the problem

1. compile arm mac asan chromium:

```
git checkout da5e37a96774daad7538cb4cf11761571080d2b3 
gn gen out/asan-0323 --args="is_component_build=true is_debug=false is_asan=true symbol_level=2 dcheck_always_on=false treat_warnings_as_errors=false"

```

2. run asan chromium:

```
./out/asan-0323/Chromium.app/Contents/MacOS/Chromium --no-sandbox --user-data-dir=/tmp/userdata/t1 --enable-features=WebMachineLearningNeuralNetwork,WebrtcAcceleratedScaling --enable-unsafe-webgpu --js-flags=--expose-gc --enable-logging --v=1 http://127.0.0.1:8088/poc.html?senders=3&rounds=32&hold_ms=4000

```
# Problem Description

RCA and Bisect coming soon!

# Summary

Security: heap-use-after-free in gpu::SyncToken::operator=(gpu::SyncToken const&)

# Custom Questions

#### Type of crash:

--type=renderer

#### Crash state:

```
=================================================================
[1m[31m==34992==ERROR: AddressSanitizer: heap-use-after-free on address 0x6040001e6b68 at pc 0x000103c19c84 bp 0x0003bb1be710 sp 0x0003bb1bdec0
[1m[0m[1m[34mREAD of size 24 at 0x6040001e6b68 thread T33[1m[0m
==34992==WARNING: invalid path to external symbolizer!
==34992==WARNING: Failed to use and restart external symbolizer!
    #0 0x000103c19c80 in __asan_memcpy+0x3e4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51c80)
    #1 0x0001054a8250 in gpu::SyncToken::operator=(gpu::SyncToken const&)+0x14 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libgpu_command_buffer_common.dylib:arm64+0x14250)
    #2 0x00014cf0f68c in blink::(anonymous namespace)::Context::DestroySharedImage(gpu::SyncToken const&, scoped_refptr<gpu::ClientSharedImage>)+0xf0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libblink_platform.dylib:arm64+0x8c768c)
    #3 0x0001128f86a8 in std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>::reset(media::(anonymous namespace)::FrameResources*)+0x168 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmedia.dylib:arm64+0x6dc6a8)
    #4 0x0001128f8024 in std::__Cr::list<std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, std::__Cr::allocator<std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>>>::pop_front()+0xb8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmedia.dylib:arm64+0x6dc024)
    #5 0x0001128f81d4 in media::(anonymous namespace)::InternalRefCountedPool::OnVideoFrameDestroyed(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool)+0x118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmedia.dylib:arm64+0x6dc1d4)
    #6 0x0001128f8ff8 in base::internal::Invoker<base::internal::FunctorTraits<void (media::(anonymous namespace)::InternalRefCountedPool::*&&)(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool), media::(anonymous namespace)::InternalRefCountedPool*&&, std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>&&>, base::internal::BindState<true, true, false, void (media::(anonymous namespace)::InternalRefCountedPool::*)(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool), scoped_refptr<media::(anonymous namespace)::InternalRefCountedPool>, std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>>, void (gpu::SyncToken const&, bool)>::RunOnce(base::internal::BindStateBase*, gpu::SyncToken const&, bool)+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmedia.dylib:arm64+0x6dcff8)
    #7 0x0001128f9b6c in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::SyncToken const&, bool)>&&, gpu::SyncToken&&, bool&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::SyncToken const&, bool)>, gpu::SyncToken, bool>, void ()>::RunOnce(base::internal::BindStateBase*)+0x16c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmedia.dylib:arm64+0x6ddb6c)
    #8 0x000105a13674 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x1ff674)
    #9 0x000105ad9880 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c5880)
    #10 0x000105ad9acc in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c5acc)
    #11 0x000105ad822c in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType)+0x3fc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c422c)
    #12 0x000105ad74f4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x548 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c34f4)
    #13 0x000105afd974 in base::internal::WorkerThread::RunWorker()+0x834 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e9974)
    #14 0x000105afce2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e8e2c)
    #15 0x000105afc7e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e87e4)
    #16 0x000105b9e2d8 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x38a2d8)
    #17 0x000103c19870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #18 0x00010308d088 in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0x1088)
    #19 0x000103096f4c in thread_start+0x4 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0xaf4c)

[1m[32m0x6040001e6b68 is located 24 bytes inside of 48-byte region [0x6040001e6b50,0x6040001e6b80)
[1m[0m[1m[35mfreed by thread T8 here:[1m[0m
    #0 0x000103c2d7b4 in __sanitizer_finish_switch_fiber+0xa14 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libclang_rt.asan_osx_dynamic.dylib:arm64+0x657b4)
    #1 0x0001128f8760 in std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>::reset(media::(anonymous namespace)::FrameResources*)+0x220 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmedia.dylib:arm64+0x6dc760)
    #2 0x0001128f8024 in std::__Cr::list<std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, std::__Cr::allocator<std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>>>::pop_front()+0xb8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmedia.dylib:arm64+0x6dc024)
    #3 0x0001128f81d4 in media::(anonymous namespace)::InternalRefCountedPool::OnVideoFrameDestroyed(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool)+0x118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmedia.dylib:arm64+0x6dc1d4)
    #4 0x0001128f8ff8 in base::internal::Invoker<base::internal::FunctorTraits<void (media::(anonymous namespace)::InternalRefCountedPool::*&&)(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool), media::(anonymous namespace)::InternalRefCountedPool*&&, std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>&&>, base::internal::BindState<true, true, false, void (media::(anonymous namespace)::InternalRefCountedPool::*)(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool), scoped_refptr<media::(anonymous namespace)::InternalRefCountedPool>, std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>>, void (gpu::SyncToken const&, bool)>::RunOnce(base::internal::BindStateBase*, gpu::SyncToken const&, bool)+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmedia.dylib:arm64+0x6dcff8)
    #5 0x0001128f9b6c in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::SyncToken const&, bool)>&&, gpu::SyncToken&&, bool&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::SyncToken const&, bool)>, gpu::SyncToken, bool>, void ()>::RunOnce(base::internal::BindStateBase*)+0x16c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmedia.dylib:arm64+0x6ddb6c)
    #6 0x000105a13674 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x1ff674)
    #7 0x000105ad9880 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c5880)
    #8 0x000105ad9acc in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c5acc)
    #9 0x000105ad822c in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType)+0x3fc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c422c)
    #10 0x000105ad74f4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x548 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c34f4)
    #11 0x000105afd974 in base::internal::WorkerThread::RunWorker()+0x834 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e9974)
    #12 0x000105afce2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e8e2c)
    #13 0x000105afc7e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e87e4)
    #14 0x000105b9e2d8 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x38a2d8)
    #15 0x000103c19870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #16 0x00010308d088 in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0x1088)
    #17 0x000103096f4c in thread_start+0x4 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0xaf4c)

[1m[35mpreviously allocated by thread T33 here:[1m[0m
    #0 0x000103c2d3bc in __sanitizer_finish_switch_fiber+0x61c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libclang_rt.asan_osx_dynamic.dylib:arm64+0x653bc)
    #1 0x0001128f6dc0 in media::(anonymous namespace)::RenderableMappableSharedImageVideoFramePoolImpl::MaybeCreateVideoFrame(gfx::Size const&, gfx::ColorSpace const&)+0x2c4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmedia.dylib:arm64+0x6dadc0)
    #2 0x00014cf05d80 in blink::WebRtcVideoFrameAdapter::SharedResources::ScaleAndMapFrameAsync(scoped_refptr<media::VideoFrame>, base::OnceCallback<void (scoped_refptr<media::VideoFrame>)>)+0x86c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libblink_platform.dylib:arm64+0x8bdd80)
    #3 0x00014cf0e6a0 in blink::WebRtcVideoFrameAdapter::PrepareMappedBufferAsync(unsigned long, unsigned long, webrtc::scoped_refptr<webrtc::VideoFrameBuffer::PreparedFrameHandler>, unsigned long)+0x378 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libblink_platform.dylib:arm64+0x8c66a0)
    #4 0x00013460ff14 in webrtc::VideoStreamEncoder::MaybePrepareVideoFrame(webrtc::VideoFrame const&, long long)+0x544 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xabbf14)
    #5 0x00013460f414 in webrtc::VideoStreamEncoder::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&)+0x688 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xabb414)
    #6 0x000133b761cc in blink::WebRtcTaskQueue::RunTask(absl::AnyInvocable<void () &&>)+0x118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x221cc)
    #7 0x000133b777e0 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WebRtcTaskQueue::*&&)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue*, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x237e0)
    #8 0x000105a13674 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x1ff674)
    #9 0x000105ad9880 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c5880)
    #10 0x000105ad9acc in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c5acc)
    #11 0x000105ad822c in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType)+0x3fc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c422c)
    #12 0x000105ad74f4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x548 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c34f4)
    #13 0x000105afd974 in base::internal::WorkerThread::RunWorker()+0x834 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e9974)
    #14 0x000105afce2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e8e2c)
    #15 0x000105afc7e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e87e4)
    #16 0x000105b9e2d8 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x38a2d8)
    #17 0x000103c19870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #18 0x00010308d088 in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0x1088)
    #19 0x000103096f4c in thread_start+0x4 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0xaf4c)

Thread T33 created by T8 here:
    #0 0x000103c1395c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x000105b9d89c in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x38989c)
    #2 0x000105afb568 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x27c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e7568)
    #3 0x000105adc128 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x244 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c8128)
    #4 0x000105adbe84 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x44 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c7e84)
    #5 0x000105ae6850 in base::internal::ThreadGroupImpl::WorkerDelegate::SwapProcessedTask(base::internal::RegisteredTaskSource, base::internal::WorkerThread*)+0x640 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2d2850)
    #6 0x000105afda4c in base::internal::WorkerThread::RunWorker()+0x90c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e9a4c)
    #7 0x000105afce2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e8e2c)
    #8 0x000105afc7e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e87e4)
    #9 0x000105b9e2d8 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x38a2d8)
    #10 0x000103c19870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #11 0x00010308d088 in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0x1088)
    #12 0x000103096f4c in thread_start+0x4 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0xaf4c)

Thread T8 created by T0 here:
    #0 0x000103c1395c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x000105b9d89c in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x38989c)
    #2 0x000105afb568 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x27c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2e7568)
    #3 0x000105adc128 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x244 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c8128)
    #4 0x000105adbe84 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x44 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2c7e84)
    #5 0x000105ae30a4 in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>)+0x3b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2cf0a4)
    #6 0x000105aef45c in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*)+0x125c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libbase.dylib:arm64+0x2db45c)
    #7 0x00013e67571c in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>, bool)+0x314 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libcontent.dylib:arm64+0xb971c)
    #8 0x00014215ac80 in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>)+0x24 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libcontent.dylib:arm64+0x3b9ec80)
    #9 0x00014215ad30 in content::RenderProcessImpl::RenderProcessImpl()+0x4c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libcontent.dylib:arm64+0x3b9ed30)
    #10 0x00014218936c in content::RendererMain(content::MainFunctionParams)+0x5ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libcontent.dylib:arm64+0x3bcd36c)
    #11 0x0001423caec4 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libcontent.dylib:arm64+0x3e0eec4)
    #12 0x0001423cd044 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libcontent.dylib:arm64+0x3e11044)
    #13 0x0001423c8954 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libcontent.dylib:arm64+0x3e0c954)
    #14 0x0001423c8e44 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libcontent.dylib:arm64+0x3e0ce44)
    #15 0x00011b8077b4 in ChromeMain+0x490 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libchrome_dll.dylib:arm64+0xb7b4)
    #16 0x000102ff0b94 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7749.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000b94)
    #17 0x00018a24dd50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libgpu_command_buffer_common.dylib:arm64+0x14250) in gpu::SyncToken::operator=(gpu::SyncToken const&)+0x14
Shadow bytes around the buggy address:
  0x6040001e6880: [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
  0x6040001e6900: [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
  0x6040001e6980: [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[31mfa[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m
  0x6040001e6a00: [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
  0x6040001e6a80: [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
=>0x6040001e6b00: [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m[[1m[35mfd[1m[0m][1m[35mfd[1m[0m [1m[35mfd[1m[0m
  0x6040001e6b80: [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[31mfa[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[31mfa[1m[0m
  0x6040001e6c00: [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
  0x6040001e6c80: [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m
  0x6040001e6d00: [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[35mfd[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m
  0x6040001e6d80: [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[34mf7[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m [1m[31mfa[1m[0m
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           [1m[0m00[1m[0m
  Partially addressable: [1m[0m01[1m[0m [1m[0m02[1m[0m [1m[0m03[1m[0m [1m[0m04[1m[0m [1m[0m05[1m[0m [1m[0m06[1m[0m [1m[0m07[1m[0m 
  Heap left redzone:       [1m[31mfa[1m[0m
  Freed heap region:       [1m[35mfd[1m[0m
  Stack left redzone:      [1m[31mf1[1m[0m
  Stack mid redzone:       [1m[31mf2[1m[0m
  Stack right redzone:     [1m[31mf3[1m[0m
  Stack after return:      [1m[35mf5[1m[0m
  Stack use after scope:   [1m[35mf8[1m[0m
  Global redzone:          [1m[31mf9[1m[0m
  Global init order:       [1m[36mf6[1m[0m
  Poisoned by user:        [1m[34mf7[1m[0m
  Container overflow:      [1m[34mfc[1m[0m
  Array cookie:            [1m[31mac[1m[0m
  Intra object redzone:    [1m[33mbb[1m[0m
  ASan internal:           [1m[33mfe[1m[0m
  Left alloca redzone:     [1m[34mca[1m[0m
  Right alloca redzone:    [1m[34mcb[1m[0m

==34992==ADDITIONAL INFO

==34992==Note: Please include this section with the ASan report.
Task trace:
    #0 0x0001128f75c4 in media::(anonymous namespace)::RenderableMappableSharedImageVideoFramePoolImpl::MaybeCreateVideoFrame(gfx::Size const&, gfx::ColorSpace const&)+0xac8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmedia.dylib:arm64+0x6db5c4)
    #1 0x0001345ffc34 in webrtc::VideoStreamEncoder::OnFramePrepared(unsigned long)+0x120 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xaabc34)
    #2 0x000103730268 in mojo::internal::MultiplexRouter::MaybePostToProcessTasks(base::SequencedTaskRunner*)+0x134 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmojo_public_cpp_bindings.dylib:arm64+0x4c268)
    #3 0x000103473178 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x230 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0323/libmojo_public_system_cpp.dylib:arm64+0x1b178)


```
# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 27.4 KB)
- [poc.html](attachments/poc.html) (text/html, 4.0 KB)

## Timeline

### sk...@google.com (2026-03-23)

Cannot reproduce on Mac, setting to medium severity

### ch...@google.com (2026-03-24)

Setting milestone because of s2 severity.

### ge...@chromium.org (2026-03-24)

Ilya: Sorry to send you another, looks WebRTC related. Let me know if there is someone more direct to send it to.

### il...@chromium.org (2026-03-25)

That seems to be the same as <https://crbug.com/494823867>. Caused by using a single-threaded `RenderableMappableSharedImageVideoFramePool` being used from multiple threads.

### il...@chromium.org (2026-03-25)

Again, this is in an experimental code, and I've just removed it yesterday: <https://crrev.com/c/7679176>

It still may be able to trigger this in a similar code with `--disable-features=BreakoutBoxConversionWithoutSinkSignal` and capturing from the canvas.

I'm working on fixing it.

### il...@chromium.org (2026-04-07)

I think this was fixed last week.

### il...@chromium.org (2026-04-07)

The remaining similar issue is tracked on <https://crbug.com/494823867>

### ch...@google.com (2026-04-07)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### il...@chromium.org (2026-04-07)

Fixed by <https://crrev.com/c/7679176>.

### ch...@google.com (2026-04-07)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### aj...@google.com (2026-06-25)

-> S1 as this is a renderer UAF.

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
High Quality. Renderer RCE / memory corruption in a sandboxed process.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/495262779)*
