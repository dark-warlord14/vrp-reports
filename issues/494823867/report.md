# Security: double-free in blink::WebRtcVideoFrameAdapter::SharedResources::ScaleAndMapFrameAsync

| Field | Value |
|-------|-------|
| **Issue ID** | [494823867](https://issues.chromium.org/issues/494823867) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 146.0.0.0 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | il...@chromium.org |
| **Created** | 2026-03-21 |
| **Bounty** | $11,000.00 |

## Description

# Steps to reproduce the problem

git checkout d9b172d77d035686b97163805763270e2790866e
gn gen out/asan-0321 --args="is\_component\_build=true is\_debug=false is\_asan=true symbol\_level=2 dcheck\_always\_on=false treat\_warnings\_as\_errors=false"
./out/asan-0321/Chromium.app/Contents/MacOS/Chromium --no-sandbox --user-data-dir=/tmp/userdata/t1 --enable-features=WebMachineLearningNeuralNetwork,WebrtcAcceleratedScaling --enable-unsafe-webgpu --js-flags=--expose-gc --enable-logging --v=1 <http://127.0.0.1/poc.html?senders=3&rounds=32&hold_ms=4000> <http://127.0.0.1/poc.html?senders=3&rounds=32&hold_ms=4000> <http://127.0.0.1/poc.html?senders=3&rounds=32&hold_ms=4000> <http://127.0.0.1/poc.html?senders=3&rounds=32&hold_ms=4000> --autoplay-policy=no-user-gesture-required

# Problem Description

RCA and Bisect coming soon!

# Summary

Security: double-free in blink::WebRtcVideoFrameAdapter::SharedResources::ScaleAndMapFrameAsync

# Custom Questions

#### Type of crash:

--type=renderer

#### Crash state:

```
=================================================================
[1m[31m==95002==ERROR: AddressSanitizer: attempting double-free on 0x60300048d690 in thread T8:
[1m[0m==95002==WARNING: invalid path to external symbolizer!
==95002==WARNING: Failed to use and restart external symbolizer!
    #0 0x000102c5d7b4 in __sanitizer_finish_switch_fiber+0xa14 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x657b4)
    #1 0x000111ad6c80 in media::(anonymous namespace)::RenderableMappableSharedImageVideoFramePoolImpl::MaybeCreateVideoFrame(gfx::Size const&, gfx::ColorSpace const&)+0x1c0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dac80)
    #2 0x00014beede9c in blink::WebRtcVideoFrameAdapter::SharedResources::ScaleAndMapFrameAsync(scoped_refptr<media::VideoFrame>, base::OnceCallback<void (scoped_refptr<media::VideoFrame>)>)+0x86c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_platform.dylib:arm64+0x8b9e9c)
    #3 0x00014bef67bc in blink::WebRtcVideoFrameAdapter::PrepareMappedBufferAsync(unsigned long, unsigned long, webrtc::scoped_refptr<webrtc::VideoFrameBuffer::PreparedFrameHandler>, unsigned long)+0x378 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_platform.dylib:arm64+0x8c27bc)
    #4 0x00013360bf14 in webrtc::VideoStreamEncoder::MaybePrepareVideoFrame(webrtc::VideoFrame const&, long long)+0x544 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xabbf14)
    #5 0x00013360b414 in webrtc::VideoStreamEncoder::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&)+0x688 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xabb414)
    #6 0x000132b721cc in blink::WebRtcTaskQueue::RunTask(absl::AnyInvocable<void () &&>)+0x118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x221cc)
    #7 0x000132b737e0 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WebRtcTaskQueue::*&&)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue*, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x237e0)
    #8 0x000104bfb674 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x1ff674)
    #9 0x000104cc1880 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c5880)
    #10 0x000104cc1acc in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c5acc)
    #11 0x000104cc022c in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType)+0x3fc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c422c)
    #12 0x000104cbf4f4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x548 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c34f4)
    #13 0x000104ce5974 in base::internal::WorkerThread::RunWorker()+0x834 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e9974)
    #14 0x000104ce4e2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e8e2c)
    #15 0x000104ce47e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e87e4)
    #16 0x000104d86284 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x38a284)
    #17 0x000102c49870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #18 0x00010235d088 in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0x1088)
    #19 0x000102366f4c in thread_start+0x4 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0xaf4c)

[1m[32m0x60300048d690 is located 0 bytes inside of 24-byte region [0x60300048d690,0x60300048d6a8)
[1m[0m[1m[35mfreed by thread T29 here:[1m[0m
    #0 0x000102c5d7b4 in __sanitizer_finish_switch_fiber+0xa14 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x657b4)
    #1 0x000111ad8198 in media::(anonymous namespace)::InternalRefCountedPool::OnVideoFrameDestroyed(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool)+0x118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dc198)
    #2 0x000111ad8fbc in base::internal::Invoker<base::internal::FunctorTraits<void (media::(anonymous namespace)::InternalRefCountedPool::*&&)(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool), media::(anonymous namespace)::InternalRefCountedPool*&&, std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>&&>, base::internal::BindState<true, true, false, void (media::(anonymous namespace)::InternalRefCountedPool::*)(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool), scoped_refptr<media::(anonymous namespace)::InternalRefCountedPool>, std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>>, void (gpu::SyncToken const&, bool)>::RunOnce(base::internal::BindStateBase*, gpu::SyncToken const&, bool)+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dcfbc)
    #3 0x000111ad9b30 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::SyncToken const&, bool)>&&, gpu::SyncToken&&, bool&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::SyncToken const&, bool)>, gpu::SyncToken, bool>, void ()>::RunOnce(base::internal::BindStateBase*)+0x16c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6ddb30)
    #4 0x000104bfb674 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x1ff674)
    #5 0x000104cc1880 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c5880)
    #6 0x000104cc1acc in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c5acc)
    #7 0x000104cc022c in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType)+0x3fc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c422c)
    #8 0x000104cbf4f4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x548 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c34f4)
    #9 0x000104ce5974 in base::internal::WorkerThread::RunWorker()+0x834 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e9974)
    #10 0x000104ce4e2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e8e2c)
    #11 0x000104ce47e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e87e4)
    #12 0x000104d86284 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x38a284)
    #13 0x000102c49870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #14 0x00010235d088 in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0x1088)
    #15 0x000102366f4c in thread_start+0x4 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0xaf4c)

[1m[35mpreviously allocated by thread T28 here:[1m[0m
    #0 0x000102c5d3bc in __sanitizer_finish_switch_fiber+0x61c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x653bc)
    #1 0x000111ad80ec in media::(anonymous namespace)::InternalRefCountedPool::OnVideoFrameDestroyed(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool)+0x6c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dc0ec)
    #2 0x000111ad8fbc in base::internal::Invoker<base::internal::FunctorTraits<void (media::(anonymous namespace)::InternalRefCountedPool::*&&)(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool), media::(anonymous namespace)::InternalRefCountedPool*&&, std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>&&>, base::internal::BindState<true, true, false, void (media::(anonymous namespace)::InternalRefCountedPool::*)(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool), scoped_refptr<media::(anonymous namespace)::InternalRefCountedPool>, std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>>, void (gpu::SyncToken const&, bool)>::RunOnce(base::internal::BindStateBase*, gpu::SyncToken const&, bool)+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dcfbc)
    #3 0x000111ad9b30 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::SyncToken const&, bool)>&&, gpu::SyncToken&&, bool&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::SyncToken const&, bool)>, gpu::SyncToken, bool>, void ()>::RunOnce(base::internal::BindStateBase*)+0x16c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6ddb30)
    #4 0x000104bfb674 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x1ff674)
    #5 0x000104cc1880 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c5880)
    #6 0x000104cc1acc in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c5acc)
    #7 0x000104cc022c in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType)+0x3fc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c422c)
    #8 0x000104cbf4f4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x548 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c34f4)
    #9 0x000104ce5974 in base::internal::WorkerThread::RunWorker()+0x834 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e9974)
    #10 0x000104ce4e2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e8e2c)
    #11 0x000104ce47e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e87e4)
    #12 0x000104d86284 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x38a284)
    #13 0x000102c49870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #14 0x00010235d088 in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0x1088)
    #15 0x000102366f4c in thread_start+0x4 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0xaf4c)

Thread T8 created by T0 here:
    #0 0x000102c4395c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x000104d85848 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x389848)
    #2 0x000104ce3568 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x27c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e7568)
    #3 0x000104cc4128 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x244 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c8128)
    #4 0x000104cc3e84 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x44 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c7e84)
    #5 0x000104ccb0a4 in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>)+0x3b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2cf0a4)
    #6 0x000104cd745c in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*)+0x125c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2db45c)
    #7 0x00013d67171c in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>, bool)+0x314 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0xb971c)
    #8 0x000141156504 in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>)+0x24 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3b9e504)
    #9 0x0001411565b4 in content::RenderProcessImpl::RenderProcessImpl()+0x4c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3b9e5b4)
    #10 0x000141184bf0 in content::RendererMain(content::MainFunctionParams)+0x5ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3bccbf0)
    #11 0x0001413c6748 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3e0e748)
    #12 0x0001413c88c8 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3e108c8)
    #13 0x0001413c41d8 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3e0c1d8)
    #14 0x0001413c46c8 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3e0c6c8)
    #15 0x00011a81f7b4 in ChromeMain+0x490 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libchrome_dll.dylib:arm64+0xb7b4)
    #16 0x0001022c0b94 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7745.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000b94)
    #17 0x00019f3e1d50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

Thread T29 created by T25 here:
    #0 0x000102c4395c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x000104d85848 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x389848)
    #2 0x000104ce3568 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x27c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e7568)
    #3 0x000104cc4128 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x244 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c8128)
    #4 0x000104cc3e84 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x44 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c7e84)
    #5 0x000104ccb99c in base::internal::ThreadGroupImpl::PushTaskSourceAndWakeUpWorkers(base::internal::RegisteredTaskSourceAndTransaction)+0x18c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2cf99c)
    #6 0x000104cdca88 in base::internal::ThreadPoolImpl::PostTaskWithSequenceNow(base::internal::Task, scoped_refptr<base::internal::Sequence>)+0x358 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e0a88)
    #7 0x000104cdd228 in base::internal::ThreadPoolImpl::PostTaskWithSequence(base::internal::Task, scoped_refptr<base::internal::Sequence>)+0x4dc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e1228)
    #8 0x000104ca36dc in base::internal::PooledSequencedTaskRunner::PostDelayedTask(base::Location const&, base::OnceCallback<void ()>, base::TimeDelta)+0x290 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2a76dc)
    #9 0x000104c91440 in base::TaskRunner::PostTask(base::Location const&, base::OnceCallback<void ()>)+0x130 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x295440)
    #10 0x000132b72584 in blink::WebRtcTaskQueue::PostTaskImpl(absl::AnyInvocable<void () &&>, webrtc::TaskQueueBase::PostTaskTraits const&, base::Location const&)+0x2a8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x22584)
    #11 0x0001335cfb88 in webrtc::(anonymous namespace)::FrameCadenceAdapterImpl::OnFrame(webrtc::VideoFrame const&)+0x31c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xa7fb88)
    #12 0x00013321ca5c in webrtc::VideoBroadcaster::OnFrame(webrtc::VideoFrame const&)+0x4e4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x6cca5c)
    #13 0x000133214fb0 in webrtc::AdaptedVideoTrackSource::OnFrame(webrtc::VideoFrame const&)+0x2b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x6c4fb0)
    #14 0x00014be07150 in blink::WebRtcVideoTrackSource::DeliverFrame(scoped_refptr<media::VideoFrame>, std::__Cr::optional<gfx::Rect>, long long, std::__Cr::optional<webrtc::Timestamp>, std::__Cr::optional<webrtc::Timestamp>)+0x93c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_platform.dylib:arm64+0x7d3150)
    #15 0x00014be05cfc in blink::WebRtcVideoTrackSource::ComputeMetadataAndDeliverFrame(scoped_refptr<media::VideoFrame>, long long)+0xd28 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_platform.dylib:arm64+0x7d1cfc)
    #16 0x00014be04d9c in blink::WebRtcVideoTrackSource::TryProcessPendingFrames()+0x214 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_platform.dylib:arm64+0x7d0d9c)
    #17 0x00014be03b3c in blink::WebRtcVideoTrackSource::OnFrameCaptured(scoped_refptr<media::VideoFrame>)+0x9b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_platform.dylib:arm64+0x7cfb3c)
    #18 0x00017002421c in blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter::OnVideoFrameOnNetworkThread(scoped_refptr<media::VideoFrame>)+0x134 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_modules.dylib:arm64+0x24e421c)
    #19 0x0001700275c0 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter::*&&)(scoped_refptr<media::VideoFrame>), scoped_refptr<blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter>&&, scoped_refptr<media::VideoFrame>&&>, base::internal::BindState<true, true, false, void (blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter::*)(scoped_refptr<media::VideoFrame>), scoped_refptr<blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter>, scoped_refptr<media::VideoFrame>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x160 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_modules.dylib:arm64+0x24e75c0)
    #20 0x000104bfb674 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x1ff674)
    #21 0x000104c791ac in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x27d1ac)
    #22 0x000104c78564 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x27c564)
    #23 0x000104a9cab4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x228 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0xa0ab4)
    #24 0x000104c7a568 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x27e568)
    #25 0x000104b669e4 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x16a9e4)
    #26 0x000104d13a3c in base::Thread::Run(base::RunLoop*)+0xd8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x317a3c)
    #27 0x000104d13e9c in base::Thread::ThreadMain()+0x3d8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x317e9c)
    #28 0x000104d86284 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x38a284)
    #29 0x000102c49870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #30 0x00010235d088 in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0x1088)
    #31 0x000102366f4c in thread_start+0x4 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0xaf4c)

Thread T25 created by T0 here:
    #0 0x000102c4395c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x000104d85848 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x389848)
    #2 0x000104d1271c in base::Thread::StartWithOptions(base::Thread::Options)+0x498 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x31671c)
    #3 0x00017002c408 in blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory()+0x33c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_modules.dylib:arm64+0x24ec408)
    #4 0x00017002c014 in blink::PeerConnectionDependencyFactory::GetPcFactory()+0xc8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_modules.dylib:arm64+0x24ec014)
    #5 0x00017003360c in blink::PeerConnectionDependencyFactory::CreatePeerConnection(webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, webrtc::PeerConnectionObserver*, blink::ExceptionState&)+0x124 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_modules.dylib:arm64+0x24f360c)
    #6 0x0001701027b4 in blink::RTCPeerConnectionHandler::Initialize(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, blink::ExceptionState&)+0x600 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_modules.dylib:arm64+0x25c27b4)
    #7 0x0001700bf0c0 in blink::RTCPeerConnection::RTCPeerConnection(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::ExceptionState&)+0x794 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_modules.dylib:arm64+0x257f0c0)
    #8 0x0001700be7c0 in blink::RTCPeerConnection* blink::MakeGarbageCollected<blink::RTCPeerConnection, blink::ExecutionContext*&, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::ExceptionState&>(blink::ExecutionContext*&, webrtc::PeerConnectionInterface::RTCConfiguration&&, bool&&, blink::ExceptionState&)+0x1a8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_modules.dylib:arm64+0x257e7c0)
    #9 0x0001700bc5bc in blink::RTCPeerConnection::Create(blink::ExecutionContext*, blink::RTCConfiguration const*, blink::ExceptionState&)+0x46c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_modules.dylib:arm64+0x257c5bc)
    #10 0x00016e842520 in blink::(anonymous namespace)::v8_rtc_peer_connection::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&)+0x3ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_modules.dylib:arm64+0xd02520)
    #11 0x000160fafb24 in v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool)+0x284 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libv8.dylib:arm64+0x353b24)
    #12 0x000160fac840 in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*)+0x76c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libv8.dylib:arm64+0x350840)
    #13 0x0003233fb5e8  (<unknown module>)
    #14 0x00032334ede0  (<unknown module>)
    #15 0x0003234fcfb0  (<unknown module>)
    #16 0x00032334e33c  (<unknown module>)
    #17 0x00032334e33c  (<unknown module>)
    #18 0x00032334e33c  (<unknown module>)
    #19 0x00032334b340  (<unknown module>)
    #20 0x00032334b038  (<unknown module>)
    #21 0x000161299d54 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)+0x1c7c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libv8.dylib:arm64+0x63dd54)
    #22 0x00016129b448 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>)+0x204 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libv8.dylib:arm64+0x63f448)
    #23 0x000160e83e88 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>)+0x5a4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libv8.dylib:arm64+0x227e88)
    #24 0x0001504b6b84 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, v8::Local<v8::Data>, blink::ExecutionContext*)+0x628 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x19ab84)
    #25 0x0001504b7f84 in blink::V8ScriptRunner::CompileAndRunScript(blink::ScriptState*, blink::ClassicScript*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption)+0x8e4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x19bf84)
    #26 0x00015374e85c in blink::ClassicScript::RunScriptOnScriptStateAndReturnValue(blink::ScriptState*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption)+0x1a0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x343285c)
    #27 0x0001537a937c in blink::Script::RunScriptOnScriptState(blink::ScriptState*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption)+0x1f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x348d37c)
    #28 0x0001537a9760 in blink::Script::RunScript(blink::LocalDOMWindow*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption)+0x140 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x348d760)
    #29 0x0001537a8864 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool)+0x420 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x348c864)
    #30 0x0001537a78bc in blink::PendingScript::ExecuteScriptBlock()+0xb94 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x348b8bc)
    #31 0x0001537aeb44 in blink::ScriptLoader::PrepareScript(blink::ScriptLoader::ParserBlockingInlineOption, blink::TextPosition const&)+0x2c70 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x3492b44)
    #32 0x000153760aa4 in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, blink::TextPosition const&)+0x3ec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x3444aa4)
    #33 0x0001537603fc in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, blink::TextPosition const&)+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x34443fc)
    #34 0x000154281d1c in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder()+0x1a4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x3f65d1c)
    #35 0x00015427e9a8 in blink::HTMLDocumentParser::PumpTokenizer()+0x5e8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x3f629a8)
    #36 0x00015427d1ec in blink::HTMLDocumentParser::PumpTokenizerIfPossible()+0x350 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x3f611ec)
    #37 0x0001542866c0 in blink::HTMLDocumentParser::FinishAppend()+0x134 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x3f6a6c0)
    #38 0x000154286cf0 in blink::HTMLDocumentParser::CommitPreloadedData()+0x1c4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x3f6acf0)
    #39 0x00015308f180 in blink::DocumentLoader::StartLoadingResponse()+0x4c4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x2d73180)
    #40 0x00015309be90 in blink::DocumentLoader::CommitNavigation()+0x1b98 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x2d7fe90)
    #41 0x0001530f857c in blink::FrameLoader::CommitDocumentLoader(blink::DocumentLoader*, blink::HistoryItem*, blink::CommitReason)+0x508 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x2ddc57c)
    #42 0x00015310214c in blink::FrameLoader::CommitNavigation(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>, std::__Cr::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__Cr::default_delete<blink::WebDocumentLoader::ExtraData>>, blink::CommitReason)+0x13b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x2de614c)
    #43 0x000151c0e0dc in blink::WebLocalFrameImpl::CommitNavigation(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>, std::__Cr::unique_ptr<blink::WebDocumentLoader::ExtraData, std::__Cr::default_delete<blink::WebDocumentLoader::ExtraData>>)+0x4f4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_core.dylib:arm64+0x18f20dc)
    #44 0x0001410ecdb8 in content::RenderFrameImpl::CommitNavigationWithParams(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>)+0xe24 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3b34db8)
    #45 0x000141139550 in void base::internal::DecayedFunctorTraits<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl>&&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::StructPtr<content::mojom::CookieManagerInfo>&&, mojo::StructPtr<content::mojom::StorageInfo>&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>&&>::Invoke<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl> const&, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>>(void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl> const&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::StructPtr<content::mojom::CookieManagerInfo>&&, mojo::StructPtr<content::mojom::StorageInfo>&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>&&, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>&&)+0x384 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3b81550)
    #46 0x000141139120 in base::internal::Invoker<base::internal::FunctorTraits<void (content::RenderFrameImpl::*&&)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl>&&, mojo::StructPtr<blink::mojom::CommonNavigationParams>&&, mojo::StructPtr<blink::mojom::CommitNavigationParams>&&, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>&&, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>&&, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>&&, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingRemote<network::mojom::URLLoaderFactory>&&, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::PendingRemote<blink::mojom::CodeCacheHost>&&, mojo::StructPtr<content::mojom::CookieManagerInfo>&&, mojo::StructPtr<content::mojom::StorageInfo>&&, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>&&>, base::internal::BindState<true, true, false, void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>), base::WeakPtr<content::RenderFrameImpl>, mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__Cr::unique_ptr<content::DocumentState, std::__Cr::default_delete<content::DocumentState>>>, void (std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>)>::RunOnce(base::internal::BindStateBase*, std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>&&)+0x164 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3b81120)
    #47 0x0001410edbe8 in base::OnceCallback<void (std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>)>::Run(std::__Cr::unique_ptr<blink::WebNavigationParams, std::__Cr::default_delete<blink::WebNavigationParams>>) &&+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3b35be8)
    #48 0x0001410e86cc in content::RenderFrameImpl::CommitNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken const&, base::Uuid const&, mojo::StructPtr<blink::mojom::PolicyContainer>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>)+0x2960 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3b306cc)
    #49 0x0001410c8860 in content::NavigationClient::CommitNavigation(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, mojo::StructPtr<network::mojom::URLLoaderClientEndpoints>, std::__Cr::unique_ptr<blink::PendingURLLoaderFactoryBundle, std::__Cr::default_delete<blink::PendingURLLoaderFactoryBundle>>, std::__Cr::optional<std::__Cr::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>, std::__Cr::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader>>>>, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingAssociatedRemote<blink::mojom::FetchLaterLoaderFactory>, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken const&, base::Uuid const&, mojo::StructPtr<blink::mojom::PolicyContainer>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, base::OnceCallback<void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>)+0x510 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3b10860)
    #50 0x00013dbaf708 in content::mojom::NavigationClientStubDispatch::AcceptWithResponder(content::mojom::NavigationClient*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>)+0xe28 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x5f7708)
    #51 0x000102745de0 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8b8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmojo_public_cpp_bindings.dylib:arm64+0x25de0)
    #52 0x00010275c090 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmojo_public_cpp_bindings.dylib:arm64+0x3c090)
    #53 0x00010274b018 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmojo_public_cpp_bindings.dylib:arm64+0x2b018)
    #54 0x0001093e9c80 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)+0x3e8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libipc.dylib:arm64+0x39c80)
    #55 0x0001093ebcf8 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1b8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libipc.dylib:arm64+0x3bcf8)
    #56 0x000104bfb674 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x1ff674)
    #57 0x000104c791ac in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x88c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x27d1ac)
    #58 0x000104c78564 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x27c564)
    #59 0x000104a9cab4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x228 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0xa0ab4)
    #60 0x000104c7a568 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x27e568)
    #61 0x000104b669e4 in base::RunLoop::Run(base::Location const&)+0x430 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x16a9e4)
    #62 0x000141184ed0 in content::RendererMain(content::MainFunctionParams)+0x88c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3bcced0)
    #63 0x0001413c6748 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3e0e748)
    #64 0x0001413c88c8 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3e108c8)
    #65 0x0001413c41d8 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3e0c1d8)
    #66 0x0001413c46c8 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3e0c6c8)
    #67 0x00011a81f7b4 in ChromeMain+0x490 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libchrome_dll.dylib:arm64+0xb7b4)
    #68 0x0001022c0b94 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7745.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000b94)
    #69 0x00019f3e1d50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

Thread T28 created by T8 here:
    #0 0x000102c4395c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x000104d85848 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x389848)
    #2 0x000104ce3568 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x27c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e7568)
    #3 0x000104cc4128 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x244 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c8128)
    #4 0x000104cc3e84 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x44 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c7e84)
    #5 0x000104ccd9c8 in base::internal::ThreadGroupImpl::WorkerDelegate::GetWork(base::internal::WorkerThread*)+0x2cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2d19c8)
    #6 0x000104ce5838 in base::internal::WorkerThread::RunWorker()+0x6f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e9838)
    #7 0x000104ce4e2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e8e2c)
    #8 0x000104ce47e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e87e4)
    #9 0x000104d86284 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x38a284)
    #10 0x000102c49870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #11 0x00010235d088 in _pthread_start+0x84 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0x1088)
    #12 0x000102366f4c in thread_start+0x4 (/usr/lib/system/introspection/libsystem_pthread.dylib:arm64e+0xaf4c)

SUMMARY: AddressSanitizer: double-free (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dac80) in media::(anonymous namespace)::RenderableMappableSharedImageVideoFramePoolImpl::MaybeCreateVideoFrame(gfx::Size const&, gfx::ColorSpace const&)+0x1c0

==95002==ADDITIONAL INFO

==95002==Note: Please include this section with the ASan report.
Task trace:
    #0 0x0001335db918 in webrtc::(anonymous namespace)::VSyncEncodeAdapterMode::EncodeAllEnqueuedFrames()+0x4ec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xa8b918)
    #1 0x0001335dac14 in webrtc::(anonymous namespace)::VSyncEncodeAdapterMode::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&)+0x278 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xa8ac14)
    #2 0x0001335cfb2c in webrtc::(anonymous namespace)::FrameCadenceAdapterImpl::OnFrame(webrtc::VideoFrame const&)+0x2c0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xa7fb2c)
    #3 0x000170023b3c in blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter::OnVideoFrameOnIO(scoped_refptr<media::VideoFrame>, base::TimeTicks)+0x12c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_modules.dylib:arm64+0x24e3b3c)

```
# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [double_free_asan.txt](attachments/double_free_asan.txt) (text/plain, 57.3 KB)
- [poc.html](attachments/poc.html) (text/html, 4.0 KB)
- [poc2.html](attachments/poc2.html) (text/html, 5.5 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 165.7 MB)

## Timeline

### zh...@gmail.com (2026-03-21)

Update another `poc2.html`, which can trigger UAF, I think the double-free and this UAF is the same root cause.

```
./out/asan-0321/Chromium.app/Contents/MacOS/Chromium --no-sandbox --user-data-dir=/tmp/userdata/t1 --enable-features=WebMachineLearningNeuralNetwork,WebrtcAcceleratedScaling --enable-unsafe-webgpu --js-flags=--expose-gc --enable-logging --v=1 http://127.0.0.1/poc2.html?senders=3&layers=3&rounds=48&hold_ms=4000&width=1280&height=720&fps=60 --autoplay-policy=no-user-gesture-required

```

- asan:

```
=================================================================
==47124==ERROR: AddressSanitizer: heap-use-after-free on address 0x6040001b57e0 at pc 0x00011455c7c0 bp 0x0003039667b0 sp 0x0003039667a8
READ of size 8 at 0x6040001b57e0 thread T8
==47124==WARNING: invalid path to external symbolizer!
==47124==WARNING: Failed to use and restart external symbolizer!
    #0 0x00011455c7bc in std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>::reset(media::(anonymous namespace)::FrameResources*)+0x2b8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dc7bc)
    #1 0x00011455bfe8 in std::__Cr::list<std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, std::__Cr::allocator<std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>>>::pop_front()+0xb8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dbfe8)
    #2 0x00011455c198 in media::(anonymous namespace)::InternalRefCountedPool::OnVideoFrameDestroyed(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool)+0x118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dc198)
    #3 0x00011455cfbc in base::internal::Invoker<base::internal::FunctorTraits<void (media::(anonymous namespace)::InternalRefCountedPool::*&&)(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool), media::(anonymous namespace)::InternalRefCountedPool*&&, std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>&&>, base::internal::BindState<true, true, false, void (media::(anonymous namespace)::InternalRefCountedPool::*)(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool), scoped_refptr<media::(anonymous namespace)::InternalRefCountedPool>, std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>>, void (gpu::SyncToken const&, bool)>::RunOnce(base::internal::BindStateBase*, gpu::SyncToken const&, bool)+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dcfbc)
    #4 0x00011455db30 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::SyncToken const&, bool)>&&, gpu::SyncToken&&, bool&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::SyncToken const&, bool)>, gpu::SyncToken, bool>, void ()>::RunOnce(base::internal::BindStateBase*)+0x16c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6ddb30)
    #5 0x00010738f674 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x1ff674)
    #6 0x000107455880 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c5880)
    #7 0x000107455acc in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c5acc)
    #8 0x00010745422c in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType)+0x3fc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c422c)
    #9 0x0001074534f4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x548 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c34f4)
    #10 0x000107479974 in base::internal::WorkerThread::RunWorker()+0x834 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e9974)
    #11 0x000107478e2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e8e2c)
    #12 0x0001074787e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e87e4)
    #13 0x00010751a284 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x38a284)
    #14 0x0001056b1870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #15 0x00019f7abc04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #16 0x00019f7a6ba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

0x6040001b57e0 is located 16 bytes inside of 48-byte region [0x6040001b57d0,0x6040001b5800)
freed by thread T23 here:
    #0 0x0001056c57b4 in __sanitizer_finish_switch_fiber+0xa14 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x657b4)
    #1 0x00011455c724 in std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>::reset(media::(anonymous namespace)::FrameResources*)+0x220 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dc724)
    #2 0x00011455bfe8 in std::__Cr::list<std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, std::__Cr::allocator<std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>>>::pop_front()+0xb8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dbfe8)
    #3 0x00011455c198 in media::(anonymous namespace)::InternalRefCountedPool::OnVideoFrameDestroyed(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool)+0x118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dc198)
    #4 0x00011455cfbc in base::internal::Invoker<base::internal::FunctorTraits<void (media::(anonymous namespace)::InternalRefCountedPool::*&&)(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool), media::(anonymous namespace)::InternalRefCountedPool*&&, std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>&&>, base::internal::BindState<true, true, false, void (media::(anonymous namespace)::InternalRefCountedPool::*)(std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>, gpu::SyncToken const&, bool), scoped_refptr<media::(anonymous namespace)::InternalRefCountedPool>, std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>>, void (gpu::SyncToken const&, bool)>::RunOnce(base::internal::BindStateBase*, gpu::SyncToken const&, bool)+0x148 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dcfbc)
    #5 0x00011455db30 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::SyncToken const&, bool)>&&, gpu::SyncToken&&, bool&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::SyncToken const&, bool)>, gpu::SyncToken, bool>, void ()>::RunOnce(base::internal::BindStateBase*)+0x16c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6ddb30)
    #6 0x00010738f674 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x1ff674)
    #7 0x000107455880 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c5880)
    #8 0x000107455acc in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c5acc)
    #9 0x00010745422c in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType)+0x3fc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c422c)
    #10 0x0001074534f4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x548 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c34f4)
    #11 0x000107479974 in base::internal::WorkerThread::RunWorker()+0x834 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e9974)
    #12 0x000107478e2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e8e2c)
    #13 0x0001074787e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e87e4)
    #14 0x00010751a284 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x38a284)
    #15 0x0001056b1870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #16 0x00019f7abc04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #17 0x00019f7a6ba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

previously allocated by thread T22 here:
    #0 0x0001056c53bc in __sanitizer_finish_switch_fiber+0x61c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x653bc)
    #1 0x00011455ad84 in media::(anonymous namespace)::RenderableMappableSharedImageVideoFramePoolImpl::MaybeCreateVideoFrame(gfx::Size const&, gfx::ColorSpace const&)+0x2c4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dad84)
    #2 0x00014e955e9c in blink::WebRtcVideoFrameAdapter::SharedResources::ScaleAndMapFrameAsync(scoped_refptr<media::VideoFrame>, base::OnceCallback<void (scoped_refptr<media::VideoFrame>)>)+0x86c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_platform.dylib:arm64+0x8b9e9c)
    #3 0x00014e95e7bc in blink::WebRtcVideoFrameAdapter::PrepareMappedBufferAsync(unsigned long, unsigned long, webrtc::scoped_refptr<webrtc::VideoFrameBuffer::PreparedFrameHandler>, unsigned long)+0x378 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libblink_platform.dylib:arm64+0x8c27bc)
    #4 0x000136073f14 in webrtc::VideoStreamEncoder::MaybePrepareVideoFrame(webrtc::VideoFrame const&, long long)+0x544 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xabbf14)
    #5 0x000136073414 in webrtc::VideoStreamEncoder::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&)+0x688 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xabb414)
    #6 0x0001355da1cc in blink::WebRtcTaskQueue::RunTask(absl::AnyInvocable<void () &&>)+0x118 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x221cc)
    #7 0x0001355db7e0 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WebRtcTaskQueue::*&&)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue*, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0x237e0)
    #8 0x00010738f674 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x1ff674)
    #9 0x000107455880 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1f0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c5880)
    #10 0x000107455acc in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xec (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c5acc)
    #11 0x00010745422c in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType)+0x3fc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c422c)
    #12 0x0001074534f4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x548 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c34f4)
    #13 0x000107479974 in base::internal::WorkerThread::RunWorker()+0x834 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e9974)
    #14 0x000107478e2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e8e2c)
    #15 0x0001074787e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e87e4)
    #16 0x00010751a284 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x38a284)
    #17 0x0001056b1870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #18 0x00019f7abc04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #19 0x00019f7a6ba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

Thread T8 created by T0 here:
    #0 0x0001056ab95c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x000107519848 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x389848)
    #2 0x000107477568 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x27c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e7568)
    #3 0x000107458128 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x244 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c8128)
    #4 0x000107457e84 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x44 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c7e84)
    #5 0x00010745f0a4 in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>)+0x3b0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2cf0a4)
    #6 0x00010746b45c in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*)+0x125c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2db45c)
    #7 0x0001400d971c in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>, bool)+0x314 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0xb971c)
    #8 0x000143bbe504 in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>)+0x24 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3b9e504)
    #9 0x000143bbe5b4 in content::RenderProcessImpl::RenderProcessImpl()+0x4c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3b9e5b4)
    #10 0x000143becbf0 in content::RendererMain(content::MainFunctionParams)+0x5ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3bccbf0)
    #11 0x000143e2e748 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x420 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3e0e748)
    #12 0x000143e308c8 in content::ContentMainRunnerImpl::Run()+0x53c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3e108c8)
    #13 0x000143e2c1d8 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x858 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3e0c1d8)
    #14 0x000143e2c6c8 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libcontent.dylib:arm64+0x3e0c6c8)
    #15 0x00011d2877b4 in ChromeMain+0x490 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libchrome_dll.dylib:arm64+0xb7b4)
    #16 0x000104db8b94 in main+0x254 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7745.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000b94)
    #17 0x00019f3e1d50 in start+0x1c0c (/usr/lib/dyld:arm64e+0x8d50)

Thread T23 created by T8 here:
    #0 0x0001056ab95c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x000107519848 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x389848)
    #2 0x000107477568 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x27c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e7568)
    #3 0x000107458128 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x244 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c8128)
    #4 0x000107457e84 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x44 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c7e84)
    #5 0x0001074619c8 in base::internal::ThreadGroupImpl::WorkerDelegate::GetWork(base::internal::WorkerThread*)+0x2cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2d19c8)
    #6 0x000107479838 in base::internal::WorkerThread::RunWorker()+0x6f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e9838)
    #7 0x000107478e2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e8e2c)
    #8 0x0001074787e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e87e4)
    #9 0x00010751a284 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x38a284)
    #10 0x0001056b1870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #11 0x00019f7abc04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #12 0x00019f7a6ba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

Thread T22 created by T8 here:
    #0 0x0001056ab95c in __sanitizer_weak_hook_memcmp+0x3083c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4b95c)
    #1 0x000107519848 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x389848)
    #2 0x000107477568 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x27c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e7568)
    #3 0x000107458128 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x244 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c8128)
    #4 0x000107457e84 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x44 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2c7e84)
    #5 0x0001074619c8 in base::internal::ThreadGroupImpl::WorkerDelegate::GetWork(base::internal::WorkerThread*)+0x2cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2d19c8)
    #6 0x000107479838 in base::internal::WorkerThread::RunWorker()+0x6f8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e9838)
    #7 0x000107478e2c in base::internal::WorkerThread::RunPooledWorker()+0xac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e8e2c)
    #8 0x0001074787e4 in base::internal::WorkerThread::ThreadMain()+0x1e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x2e87e4)
    #9 0x00010751a284 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libbase.dylib:arm64+0x38a284)
    #10 0x0001056b1870 in __sanitizer_weak_hook_memcmp+0x36750 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51870)
    #11 0x00019f7abc04 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c04)
    #12 0x00019f7a6ba4 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1ba4)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6dc7bc) in std::__Cr::unique_ptr<media::(anonymous namespace)::FrameResources, std::__Cr::default_delete<media::(anonymous namespace)::FrameResources>>::reset(media::(anonymous namespace)::FrameResources*)+0x2b8
Shadow bytes around the buggy address:
  0x6040001b5500: f7 fa fa fa fa fa fa fa f7 fa fa fa fa fa fa fa
  0x6040001b5580: f7 fa fa fa fa fa fa fa f7 fa fa fa fa fa fa fa
  0x6040001b5600: f7 fa fa fa fa fa fa fa f7 fa fa fa fa fa fa fa
  0x6040001b5680: f7 fa 00 00 00 00 00 fa f7 fa fa fa fa fa fa fa
  0x6040001b5700: f7 fa fa fa fa fa fa fa f7 fa fa fa fa fa fa fa
=>0x6040001b5780: f7 fa fa fa fa fa fa fa f7 fa fd fd[fd]fd fd fd
  0x6040001b5800: f7 fa fa fa fa fa fa fa f7 fa fd fd fd fd fd fd
  0x6040001b5880: f7 fa fd fd fd fd fd fd f7 fa fa fa fa fa fa fa
  0x6040001b5900: f7 fa fa fa fa fa fa fa f7 fa fa fa fa fa fa fa
  0x6040001b5980: f7 fa fa fa fa fa fa fa f7 fa fa fa fa fa fa fa
  0x6040001b5a00: f7 fa fa fa fa fa fa fa f7 fa fa fa fa fa fa fa
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

==47124==ADDITIONAL INFO

==47124==Note: Please include this section with the ASan report.
Task trace:
    #0 0x00011455b588 in media::(anonymous namespace)::RenderableMappableSharedImageVideoFramePoolImpl::MaybeCreateVideoFrame(gfx::Size const&, gfx::ColorSpace const&)+0xac8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmedia.dylib:arm64+0x6db588)
    #1 0x000136063c34 in webrtc::VideoStreamEncoder::OnFramePrepared(unsigned long)+0x120 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libthird_party_webrtc_overrides_webrtc_component.dylib:arm64+0xaabc34)
    #2 0x000105010268 in mojo::internal::MultiplexRouter::MaybePostToProcessTasks(base::SequencedTaskRunner*)+0x134 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmojo_public_cpp_bindings.dylib:arm64+0x4c268)
    #3 0x000105227178 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x230 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/libmojo_public_system_cpp.dylib:arm64+0x1b178)


Command line: `/Users/zh1x1an1221/xcode-chromium/src/out/asan-0321/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7745.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer) --type=renderer --user-data-dir=/tmp/userdata/t1 --enable-isolated-web-apps-in-renderer --no-sandbox --autoplay-policy=no-user-gesture-required --enable-unsafe-webgpu --js-flags=--expose-gc --lang=zh-CN --touch-selection-strategy=direction --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=14 --time-ticks-at-unix-epoch=-1774021302066554 --launch-time-ticks=81240210628 --shared-files --metrics-shmem-handle=1752395122,r,17752569440243381764,3527914974393709823,2097152 --field-trial-handle=1718379636,r,6272212639987267535,16891183168796593781,262144 --enable-features=WebMachineLearningNeuralNetwork,WebrtcAcceleratedScaling  --variations-seed-version --pseudonymization-salt-handle=1935764596,r,10145022558413320499,14659108321754050920,4 --trace-process-track-uuid=3190708999430457380 --enable-logging --v=1`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==47124==END OF ADDITIONAL INFO

==47124==ABORTING

```

### zh...@gmail.com (2026-03-21)

## BISECT COMMIT

<https://chromium-review.googlesource.com/c/chromium/src/+/6890771>

### zh...@gmail.com (2026-03-21)

By the way, I recommend triggering it on a arm Mac as I described. This vulnerability cannot be triggered on Linux or Windows at this time.

### zh...@gmail.com (2026-03-21)

## RCA HERE

These two ASANs are essentially two manifestations of the same concurrency root cause: the same `RenderableMappableSharedImageVideoFramePool` is accessed simultaneously by multiple WebRTC encoding threads, while its internal `freelist` is not synchronized at all.

The key path is:

The same track source will share the same `adapter_resources_` with multiple senders. <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/peerconnection/webrtc_video_track_source.cc;l=482-484>

```
  webrtc::scoped_refptr<webrtc::VideoFrameBuffer> frame_adapter(
      new webrtc::RefCountedObject<WebRtcVideoFrameAdapter>(
          frame, adapter_resources_));

```

`adapter_resources_` holds a shared [accelerated\_frame\_pool\_](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/webrtc/webrtc_video_frame_adapter.h;l=138-139?q=third_party%2Fblink%2Frenderer%2Fplatform%2Fwebrtc%2Fwebrtc_video_frame_adapter.h)

```
    std::unique_ptr<media::RenderableMappableSharedImageVideoFramePool>
        accelerated_frame_pool_;

```

When multiple senders concurrently execute [PrepareMappedBufferAsync()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/webrtc/webrtc_video_frame_adapter.cc;l=800) and [ScaleAndMapFrameAsync()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/webrtc/webrtc_video_frame_adapter.cc;l=359), they will all enter the same pool.

The API for this pool itself states that it "must be accessed by the thread that created it".
<https://source.chromium.org/chromium/chromium/src/+/main:media/video/renderable_mappable_shared_image_video_frame_pool.h;l=38-39?q=media%2Fvideo%2Frenderable_mappable_shared_image_video_frame_pool.h>

```
// A video frame pool that returns MappableSharedImage-backed VideoFrames. All
// access to this class must be on the thread on which it was created.
class MEDIA_EXPORT RenderableMappableSharedImageVideoFramePool {

```

The real problem lies inside the pool:

[MaybeCreateVideoFrame()](https://source.chromium.org/chromium/chromium/src/+/main:media/video/renderable_mappable_shared_image_video_frame_pool.cc;l=307-345?q=media%2Fvideo%2Frenderable_mappable_shared_image_video_frame_pool.cc) will `pop_front()` from `available_frame_resources_` to retrieve reusable objects:

```
scoped_refptr<VideoFrame> InternalRefCountedPool::MaybeCreateVideoFrame(
    const gfx::Size& visible_size,
    const gfx::ColorSpace& color_space) {
  // Find or create a suitable FrameResources.
  std::unique_ptr<FrameResources> frame_resources;
  while (!available_frame_resources_.empty()) {
    frame_resources = std::move(available_frame_resources_.front());
    available_frame_resources_.pop_front();
    if (!frame_resources->IsCompatibleWith(visible_size, color_space)) {
      frame_resources = nullptr;
      continue;
    }
    break;
  }
  if (!frame_resources) {
    frame_resources = std::make_unique<FrameResources>(this, visible_size);
    if (!frame_resources->Initialize(format_, color_space,
                                     requires_cpu_access_)) {
      DLOG(ERROR) << "Failed to initialize frame resources.";
      return nullptr;
    }
  }
  DCHECK(frame_resources);

  // Create a VideoFrame from the FrameResources.
  auto video_frame = frame_resources->CreateVideoFrame();
  if (!video_frame) {
    DLOG(ERROR) << "Failed to create VideoFrame from FrameResources.";
    return nullptr;
  }

  // Set the ReleaseMailboxCB to return the FrameResources to the available
  // pool. Do this on the calling thread.
  auto callback = base::BindOnce(&InternalRefCountedPool::OnVideoFrameDestroyed,
                                 this, std::move(frame_resources));
  video_frame->SetReleaseMailboxCB(
      base::BindPostTaskToCurrentDefault(std::move(callback), FROM_HERE));
  return video_frame;
}

```

Each newly created VideoFrame will be bound to a release callback, returning to `OnVideoFrameDestroyed()`: <https://source.chromium.org/chromium/chromium/src/+/main:media/video/renderable_mappable_shared_image_video_frame_pool.cc;l=338-341?q=media%2Fvideo%2Frenderable_mappable_shared_image_video_frame_pool.cc>

```
  // Set the ReleaseMailboxCB to return the FrameResources to the available
  // pool. Do this on the calling thread.
  auto callback = base::BindOnce(&InternalRefCountedPool::OnVideoFrameDestroyed,
                                 this, std::move(frame_resources));

```

[OnVideoFrameDestroyed()](https://source.chromium.org/chromium/chromium/src/+/main:media/video/renderable_mappable_shared_image_video_frame_pool.cc;l=347-369?q=media%2Fvideo%2Frenderable_mappable_shared_image_video_frame_pool.cc) will push\_back() back to the freelist, and pop\_front() to evict old objects if necessary.

```
void InternalRefCountedPool::OnVideoFrameDestroyed(
    std::unique_ptr<FrameResources> frame_resources,
    const gpu::SyncToken& sync_token,
    bool lost_shared_image_resource) {
  frame_resources->SetSharedImageReleaseSyncToken(sync_token);

  // If the SharedImage within FrameResource is lost, we should not reuse it.
  if (lost_shared_image_resource) {
    return;
  }

  if (shutting_down_) {
    return;
  }

  // TODO(crbug.com/40174702): Determine if we can get away with just
  // having 1 available frame, or if that will cause flakey underruns.
  constexpr size_t kMaxAvailableFrames = 2;
  available_frame_resources_.push_back(std::move(frame_resources));
  while (available_frame_resources_.size() > kMaxAvailableFrames) {
    available_frame_resources_.pop_front();
  }
}

```

The problem here is that `available_frame_resources_` is a `std::list<std::unique_ptr<FrameResources>>`, but `MaybeCreateVideoFrame()`, `OnVideoFrameDestroyed()`, and `Shutdown()` are not locked.

Therefore, race conditions can occur as follows:

1. Thread T22 creates frame A and binds its release callback back to T22's current default sequence.
2. Thread T23 creates frame B and binds its release callback back to T23's current default sequence.
3. When A/B are destroyed, the two `OnVideoFrameDestroyed()` calls will concurrently modify the same `available_frame_resources_` in different threads.
4. At the same time, another thread might be retrieving nodes from the same list in `MaybeCreateVideoFrame()`.

This leads to three phenomena:

1. One thread has just called `pop_front()` and released a node, while another thread is still reading that node, resulting in the UAF
2. Both threads eventually reach the same `FrameResources` path for destruction, resulting in double-free.
3. The list structure is corrupted by concurrent modifications, manifesting as `list::pop_front()` being called with an empty list.

This is why I mentioned earlier that I believe UAF and double-free are the same root cause.

### zh...@gmail.com (2026-03-22)

Updated a `poc.mov` file, and verified stable triggering of double free and UAF.

### cl...@appspot.gserviceaccount.com (2026-03-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6425169136484352.

### sk...@google.com (2026-03-23)

Cannot repro on Mac, setting provisional severity and FoundIn

### zh...@gmail.com (2026-03-23)

I can repro this issue very stably on Mac, and I have submitted the rca and poc.mov.

### ch...@google.com (2026-03-24)

Setting milestone because of s2 severity.

### il...@chromium.org (2026-03-24)

Note, this is in a code behind a disabled, not rolled yet feature.
The mentioned accelrated pool itself is being removed by ongoing work, so the error will be fixed accidentally.

### zh...@gmail.com (2026-03-24)

Hmmmm, thank you for this feedback. However, we don't have access to information about your code development progress or plans. All I know is that the latest code can still be reliably fuzzed to trigger vulnerabilities.

### il...@chromium.org (2026-03-24)

Sorry for confusion. I didn't try to discredit your work. This is just information for severity analysis.

### il...@chromium.org (2026-03-24)

Thinking more about it, the same accelerated pool can be hit here: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/webrtc/webrtc_video_frame_adapter.cc;l=265;drc=d1b8e210f0c932906c1dd46f61d4a8be23e144a2>

This is not an experimental code.

To trigger it several things are required:

1. capture from a canvas, not from the camera.
2. `--disable-features=BreakoutBoxConversionWithoutSinkSignal` command line flag.

However, this flag is enabled on canary-dev-beta as part of an `WebrtcEncodeReadbackOptimization` experiment.

I'm not sure if this code has the same issue. It's very similar to the code in question.

I'll make a CL to remove that code just in case.

### ge...@google.com (2026-03-24)

I have no knowledge of this area of the code. Ilya, can you find an owner?

### il...@chromium.org (2026-03-25)

I'm the right owner to fix this.

### il...@chromium.org (2026-04-07)

The original issue should be fixed on ToT. I'm still working on fixing the `ConstructVideoFrameFromTexture` path.

I was OOO past week.

### il...@chromium.org (2026-04-07)

@da...@chromium.org WDYT about adding a lock to `RenderableMappableSharedImageVideoFramePool`? It will be one extra unneeded lock in WebCodec setting per frame, but it's very low cost. On the other hand we save a lot on eleminating extra memcopy on Mac. On windows it's basically the same.

Otherwise the fix is just to basically revert <https://crrev.com/c/3025855>

### da...@chromium.org (2026-04-07)

I think we should either add a lock or revert and add a thread checker. We can revert <https://crrev.com/c/3025855> if it doesn't seem like it's adding any value. ISTR tests showing it was more performant on macOS in some cases, but it probably needs retesting since so much has changed on the GPU side and around this code. Did you end up testing perf w/o it on the Meet test bench?

### il...@chromium.org (2026-04-08)

No, it does add a value. It removes a full copy operation. So it's preferable to leave it in if it's feasible to add locks ot the Pool.  

I didn't get to test it yet. Will try later this week.

### il...@chromium.org (2026-04-09)

I didn't see any difference in my local tests and after some investigation I found that this code is a backup-on-backup. It runs only for a few first frames before the feedback reaches the canvas and there the same accelerated\_pool is used: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/breakout_box/media_stream_video_track_underlying_sink.cc;l=231;drc=15be50893f87a32a6a12adea5051b701414e932f>

There it's done in a single thread, so it's fine.

I've kicked off some tests with all the features disabled just to force this code to execute, but I'm pretty sure we can just remove it.

### il...@chromium.org (2026-04-10)

I've observed no difference on Windows: <https://dashboards.corp.google.com/mq_testbed_ab_test_dashboard?f=ab_test_name:in:canvas-readback-test&f=ab_test_run_id:in:20260409_090914_21b04ed9-2dda-40df-9378-5b8b5f0c3f66>

Running on Mac now.

### il...@chromium.org (2026-04-14)

There's a small difference on Mac: <https://dashboards.corp.google.com/mq_testbed_ab_test_dashboard?f=ab_test_name:in:canvas-readback-test-mac&f=ab_test_run_id:in:20260413_084547_d8a7b5e9-cd82-483d-844a-c528cb9a714e> The power usage is increased by 1.6%. But that's in the artificial case where all the other code paths are disabled with flags, so it's the absolute upper bound for the regression, practically unreachable because the slower code is only supposed to be run for a negligeable subset of frames.

### dx...@google.com (2026-04-14)

Project: chromium/src  

Branch:  main  

Author:  Ilya Nikolaevskiy [ilnik@chromium.org](mailto:ilnik@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7748044>

Remove accelerated pool for RGB texture readback in webrtc.

---


Expand for full commit details
```
     
    That pool can't be used in multithreaded webrtc environment. 
    It's full of UAF, race conditions and other security issues. 
    The removal will not noticeably impact the performance because this 
    conversion here is a backup, happening only if feedback isn't acted upon 
    yet in the canvas capture, where the same accelerated pool performs 
    efficient conversion. 
     
    Bug: 494823867 
    Change-Id: I8895838bec35f089b363cb4179a204f55fdc3096 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7748044 
    Commit-Queue: Ilya Nikolaevskiy <ilnik@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1614335}

```

---

Files:

- M `third_party/blink/renderer/platform/webrtc/webrtc_video_frame_adapter.cc`

---

Hash: [71feade96b744446b818ef9687ffe1dfc04e357f](https://chromiumdash.appspot.com/commit/71feade96b744446b818ef9687ffe1dfc04e357f)  

Date: Tue Apr 14 09:38:52 2026


---

### il...@chromium.org (2026-04-14)

I don't think any merges are necessary, because the affected code is behind flags.

### aj...@google.com (2026-06-25)

-> S1 as this is renderer rce.

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High quailty. Renderer RCE / memory corruption in a sandboxed process with bisect.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-07-23)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494823867)*
