# heap-use-after-free cc\tiles\gpu_image_decode_cache.cc:2469 in cc::GpuImageDecodeCache::DecodeImageIfNecessary

| Field | Value |
|-------|-------|
| **Issue ID** | [368222741](https://issues.chromium.org/issues/368222741) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Compositing |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2024-09-19 |
| **Bounty** | $4,000.00 |

## Description

#Summary
heap-use-after-free cc\tiles\gpu_image_decode_cache.cc:2469 in cc::GpuImageDecodeCache::DecodeImageIfNecessary

#Reproduce
asan-win32-release_x64-1353186
This issue occurred unintentionally while I was browsing a normal page.
I attempted some analysis to identify the root cause of the vulnerability, but ultimately, I was unable to reproduce it.
I will share some of the work I did during this process.


#Analysis
ImageData is a RefCountedThreadSafe object. The GetTaskForImageAndRefInternal function calls CreateImageData to create a new ImageData object, which is then stored in both the PersistentCache[2] and InUseCacheKey[3].

The InUseCacheKey reference count is decreased by the UnrefImage call from the Compositor thread. Meanwhile, the PersistentCache reference count is decreased during memory pressure in the ThreadPoolForegroundWorker thread when DecodeImageIfNecessary calls GpuImageDecodeCache::ClearCache.

Both UnrefImage in the Compositor thread and DecodeImageIfNecessary in the ThreadPoolForegroundWorker thread acquire base::AutoLock lock(lock_);. The DecodeImageIfNecessary function receives ImageData* image_data[6] as a raw pointer without increasing the reference count. Within this function, base::AutoUnlock unlock(lock_)[7] is used to temporarily release the lock.

Thus, there's a potential timing issue where the ThreadPoolForegroundWorker thread releases the lock in DecodeImageIfNecessary and calls ClearCache, reducing the reference count in PersistentCache. At this point, the Compositor thread might execute UnrefImage, which further reduces the reference count through UnrefImageInternal, potentially freeing the image_data memory.

Subsequently, when the ThreadPoolForegroundWorker thread resumes execution of the remaining code in DecodeImageIfNecessary, it can lead to a use-after-free (UAF). This was identified as a possible root cause based on crash ASAN logs and my debugging analysis.

During my analysis, I confirmed that UnrefImage and ClearCache can indeed decrease the image_data reference count from different threads. However, I was unable to reproduce the issue by getting UnrefImage to execute immediately after ClearCache in DecodeImageIfNecessary.

[1] https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/gpu_image_decode_cache.cc;drc=a150b50c0ff706af12c449c7fccd3cf2745e2061;l=1310
[2] https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/gpu_image_decode_cache.cc;drc=a150b50c0ff706af12c449c7fccd3cf2745e2061;l=1397
[3] https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/gpu_image_decode_cache.cc;drc=a150b50c0ff706af12c449c7fccd3cf2745e2061;l=1401
[4] https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/gpu_image_decode_cache.cc;drc=a150b50c0ff706af12c449c7fccd3cf2745e2061;l=2151
[5] https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/gpu_image_decode_cache.cc;drc=a150b50c0ff706af12c449c7fccd3cf2745e2061;l=2425
[6] https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/gpu_image_decode_cache.cc;drc=a150b50c0ff706af12c449c7fccd3cf2745e2061;l=2359
[7] https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/gpu_image_decode_cache.cc;drc=a150b50c0ff706af12c449c7fccd3cf2745e2061;l=2407

#Asan
=================================================================
==1472==ERROR: AddressSanitizer: heap-use-after-free on address 0x11fe92769910 at pc 0x7ffd6dc08248 bp 0x003a3b5fe960 sp 0x003a3b5fe9a8
READ of size 8 at 0x11fe92769910 thread T4
    #0 0x7ffd6dc08247 in cc::GpuImageDecodeCache::DecodeImageIfNecessary C:\b\s\w\ir\cache\builder\src\cc\tiles\gpu_image_decode_cache.cc:2469
    #1 0x7ffd6dbf699b in cc::GpuImageDecodeCache::DecodeImageAndGenerateDarkModeFilterIfNecessary C:\b\s\w\ir\cache\builder\src\cc\tiles\gpu_image_decode_cache.cc:2351
    #2 0x7ffd6dc000e9 in cc::GpuImageDecodeCache::DecodeImageInTask C:\b\s\w\ir\cache\builder\src\cc\tiles\gpu_image_decode_cache.cc:1939
    #3 0x7ffd6dc17e1c in cc::GpuImageDecodeTaskImpl::RunOnWorkerThread C:\b\s\w\ir\cache\builder\src\cc\tiles\gpu_image_decode_cache.cc:616
    #4 0x7ffd76f7bc26 in cc::ImageController::ProcessNextImageDecodeOnWorkerThread C:\b\s\w\ir\cache\builder\src\cc\tiles\image_controller.cc:309
    #5 0x7ffd76f7d517 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(cc::ImageController::WorkerState *),cc::ImageController::WorkerState *>,base::internal::BindState<0,1,0,void (*)(cc::ImageController::WorkerState *),base::internal::UnretainedWrapper<cc::ImageController::WorkerState,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #6 0x7ffd682757a0 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #7 0x7ffd713ecb2a in base::internal::TaskTracker::RunContinueOnShutdown C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:655
    #8 0x7ffd713ec169 in base::internal::TaskTracker::RunTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:521
    #9 0x7ffd713eb23e in base::internal::TaskTracker::RunAndPopNextTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:416
    #10 0x7ffd76730c24 in base::internal::WorkerThread::RunWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:493
    #11 0x7ffd7672fa2f in base::internal::WorkerThread::RunPooledWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:379
    #12 0x7ffd6819ce45 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:131
    #13 0x7ff73039533d in asan_thread_start C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:147
    #14 0x7ffdcc44257c in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x18001257c)
    #15 0x7ffdcd62af27 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005af27)

0x11fe92769910 is located 656 bytes inside of 1232-byte region [0x11fe92769680,0x11fe92769b50)
freed by thread T9 here:
    #0 0x7ff7303a181d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffd6dbf4d93 in cc::GpuImageDecodeCache::UnrefImageInternal C:\b\s\w\ir\cache\builder\src\cc\tiles\gpu_image_decode_cache.cc:2151
    #2 0x7ffd6dbf4911 in cc::GpuImageDecodeCache::UnrefImage C:\b\s\w\ir\cache\builder\src\cc\tiles\gpu_image_decode_cache.cc:1441
    #3 0x7ffd76f7ae15 in cc::ImageController::UnlockImageDecode C:\b\s\w\ir\cache\builder\src\cc\tiles\image_controller.cc:261
    #4 0x7ffd723cb24d in std::__Cr::__destroy_at<std::__Cr::pair<int,std::__Cr::unique_ptr<cc::DecodedImageTracker::ImageLock,std::__Cr::default_delete<cc::DecodedImageTracker::ImageLock> > >,0> C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\construct_at.h:67
    #5 0x7ffd723c8d5b in cc::DecodedImageTracker::UnlockAllImages C:\b\s\w\ir\cache\builder\src\cc\tiles\decoded_image_tracker.cc:62
    #6 0x7ffd6dc8362c in cc::LayerTreeHostImpl::SetVisible C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:3822
    #7 0x7ffd72306d4b in cc::ProxyImpl::SetVisibleOnImpl C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_impl.cc:274
    #8 0x7ffd6dc3ea88 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::ProxyImpl::*&&)(bool),cc::ProxyImpl *,bool &&>,base::internal::BindState<1,1,0,void (cc::ProxyImpl::*)(bool),base::internal::UnretainedWrapper<cc::ProxyImpl,base::unretained_traits::MayNotDangle,0>,bool>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #9 0x7ffd682757a0 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #10 0x7ffd6c9bedcd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:470
    #11 0x7ffd6c9bdb79 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:332
    #12 0x7ffd6ca025ce in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #13 0x7ffd6c9c0a9f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:640
    #14 0x7ffd682cf96e in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #15 0x7ffd65bc4ef9 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\non_main_thread_impl.cc:188
    #16 0x7ffd6819ce45 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:131
    #17 0x7ff73039533d in asan_thread_start C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:147
    #18 0x7ffdcc44257c in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x18001257c)
    #19 0x7ffdcd62af27 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005af27)

previously allocated by thread T9 here:
    #0 0x7ff7303a191d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffd7f22286e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffd6dbef4dd in cc::GpuImageDecodeCache::CreateImageData C:\b\s\w\ir\cache\builder\src\cc\tiles\gpu_image_decode_cache.cc:2986
    #3 0x7ffd6dbebef9 in cc::GpuImageDecodeCache::GetTaskForImageAndRefInternal C:\b\s\w\ir\cache\builder\src\cc\tiles\gpu_image_decode_cache.cc:1310
    #4 0x7ffd6dbedb0e in cc::GpuImageDecodeCache::GetOutOfRasterDecodeTaskForImageAndRef C:\b\s\w\ir\cache\builder\src\cc\tiles\gpu_image_decode_cache.cc:1280
    #5 0x7ffd76f78332 in cc::ImageController::GenerateTasksForOrphanedRequests C:\b\s\w\ir\cache\builder\src\cc\tiles\image_controller.cc:382
    #6 0x7ffd76f77c7b in cc::ImageController::SetImageDecodeCache C:\b\s\w\ir\cache\builder\src\cc\tiles\image_controller.cc:148
    #7 0x7ffd72353ba4 in cc::TileManager::SetResources C:\b\s\w\ir\cache\builder\src\cc\tiles\tile_manager.cc:628
    #8 0x7ffd6dc70151 in cc::LayerTreeHostImpl::CreateTileManagerResources C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:3926
    #9 0x7ffd6dc86ee9 in cc::LayerTreeHostImpl::InitializeFrameSink C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:4217
    #10 0x7ffd72305dbc in cc::ProxyImpl::InitializeLayerTreeFrameSinkOnImpl C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_impl.cc:193
    #11 0x7ffd6dc3e4d1 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::ProxyImpl::*&&)(cc::LayerTreeFrameSink *, base::WeakPtr<cc::ProxyMain>),cc::ProxyImpl *,cc::LayerTreeFrameSink *&&,base::WeakPtr<cc::ProxyMain> &&>,base::internal::BindState<1,1,0,void (cc::ProxyImpl::*)(cc::LayerTreeFrameSink *, base::WeakPtr<cc::ProxyMain>),base::internal::UnretainedWrapper<cc::ProxyImpl,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<cc::LayerTreeFrameSink,base::unretained_traits::MayNotDangle,0>,base::WeakPtr<cc::ProxyMain> >,void ()>::RunImpl<void (cc::ProxyImpl::*)(cc::LayerTreeFrameSink *, base::WeakPtr<cc::ProxyMain>),std::__Cr::tuple<base::internal::UnretainedWrapper<cc::ProxyImpl,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<cc::LayerTreeFrameSink,base::unretained_traits::MayNotDangle,0>,base::WeakPtr<cc::ProxyMain> >,0,1,2> C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1067
    #12 0x7ffd682757a0 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #13 0x7ffd6c9bedcd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:470
    #14 0x7ffd6c9bdb79 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:332
    #15 0x7ffd6ca025ce in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #16 0x7ffd6c9c0a9f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:640
    #17 0x7ffd682cf96e in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #18 0x7ffd65bc4ef9 in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\non_main_thread_impl.cc:188
    #19 0x7ffd6819ce45 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:131
    #20 0x7ff73039533d in asan_thread_start C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:147
    #21 0x7ffdcc44257c in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x18001257c)
    #22 0x7ffdcd62af27 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005af27)

Thread T4 created by T0 here:
    #0 0x7ff730395252 in CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:158
    #1 0x7ffd6819be97 in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:196
    #2 0x7ffd7672e258 in base::internal::WorkerThread::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:207
    #3 0x7ffd713e2bf5 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group.cc:93
    #4 0x7ffd713e262d in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group.cc:84
    #5 0x7ffd713ff8a2 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:49
    #6 0x7ffd713ff5be in base::internal::ThreadGroupImpl::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:248
    #7 0x7ffd6c98d9b8 in base::internal::ThreadPoolImpl::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_pool_impl.cc:190
    #8 0x7ffd6b75f97a in content::ChildProcess::ChildProcess C:\b\s\w\ir\cache\builder\src\content\child\child_process.cc:102
    #9 0x7ffd75c05848 in content::RenderProcess::RenderProcess C:\b\s\w\ir\cache\builder\src\content\renderer\render_process.cc:18
    #10 0x7ffd7052c8ea in content::RenderProcessImpl::RenderProcessImpl C:\b\s\w\ir\cache\builder\src\content\renderer\render_process_impl.cc:113
    #11 0x7ffd7052cfe5 in content::RenderProcessImpl::Create C:\b\s\w\ir\cache\builder\src\content\renderer\render_process_impl.cc:228
    #12 0x7ffd6bd87092 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:289
    #13 0x7ffd66675dd1 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:795
    #14 0x7ffd6667802f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1164
    #15 0x7ffd6666c635 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:356
    #16 0x7ffd6666d1dd in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:369
    #17 0x7ffd57f916b0 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:231
    #18 0x7ff7302c43ed in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201
    #19 0x7ff7302c200c in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351
    #20 0x7ff7306e68cb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #21 0x7ffdcc44257c in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x18001257c)
    #22 0x7ffdcd62af27 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005af27)

Thread T9 created by T0 here:
    #0 0x7ff730395252 in CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:158
    #1 0x7ffd6819be97 in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:196
    #2 0x7ffd6823672e in base::SimpleThread::StartAsync C:\b\s\w\ir\cache\builder\src\base\threading\simple_thread.cc:55
    #3 0x7ffd65b16c88 in blink::Thread::CreateAndSetCompositorThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\common\thread.cc:84
    #4 0x7ffd705376d4 in content::RenderThreadImpl::InitializeCompositorThread C:\b\s\w\ir\cache\builder\src\content\renderer\render_thread_impl.cc:837
    #5 0x7ffd7053361b in content::RenderThreadImpl::InitializeWebKit C:\b\s\w\ir\cache\builder\src\content\renderer\render_thread_impl.cc:872
    #6 0x7ffd7052ff01 in content::RenderThreadImpl::Init C:\b\s\w\ir\cache\builder\src\content\renderer\render_thread_impl.cc:564
    #7 0x7ffd70532b8d in content::RenderThreadImpl::RenderThreadImpl C:\b\s\w\ir\cache\builder\src\content\renderer\render_thread_impl.cc:518
    #8 0x7ffd6bd87103 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:293
    #9 0x7ffd66675dd1 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:795
    #10 0x7ffd6667802f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1164
    #11 0x7ffd6666c635 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:356
    #12 0x7ffd6666d1dd in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:369
    #13 0x7ffd57f916b0 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:231
    #14 0x7ff7302c43ed in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201
    #15 0x7ff7302c200c in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351
    #16 0x7ff7306e68cb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #17 0x7ffdcc44257c in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x18001257c)
    #18 0x7ffdcd62af27 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005af27)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\cc\tiles\gpu_image_decode_cache.cc:2469 in cc::GpuImageDecodeCache::DecodeImageIfNecessary
Shadow bytes around the buggy address:
  0x11fe92769680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11fe92769700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11fe92769780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11fe92769800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11fe92769880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x11fe92769900: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11fe92769980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11fe92769a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11fe92769a80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x11fe92769b00: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x11fe92769b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==1472==ADDITIONAL INFO

==1472==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffd76f7a874 in cc::ImageController::ScheduleImageDecodeOnWorkerIfNeeded C:\b\s\w\ir\cache\builder\src\cc\tiles\image_controller.cc:402
    #1 0x7ffd6dc2e877 in cc::ProxyMain::SetLayerTreeFrameSink C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_main.cc:542
    #2 0x7ffd72310385 in cc::ProxyImpl::ScheduledActionBeginLayerTreeFrameSinkCreation C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_impl.cc:877
    #3 0x7ffd6dc2c1c5 in cc::ProxyMain::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_main.cc:468


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1472==END OF ADDITIONAL INFO
==1472==ABORTING

## Attachments

- [001-expected.png](attachments/001-expected.png) (image/png, 132.6 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 17.8 KB)
- [debug.patch](attachments/debug.patch) (text/x-diff, 4.6 KB)
- [test.html](attachments/test.html) (text/html, 483 B)

## Timeline

### ma...@google.com (2024-09-19)

Setting labels provisionally in lack of a clear repro case.

vmiura@, could you PTAL and decide if the analysis in the report is sufficiently actionable? Alternatively, if you aren't a good owner for this, please help me route this issue. Thank you!

### pe...@google.com (2024-09-20)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-09-20)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-10-04)

vmiura: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### m....@gmail.com (2024-10-07)

I saw a CL that might fix the issue, but I'm not sure because this CL is not associated with any bugid."

<https://chromium-review.googlesource.com/c/chromium/src/+/5893986>

### pe...@google.com (2024-10-19)

vmiura: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### an...@chromium.org (2024-10-25)

[security shepherd] CCing szager@ as well as they are the author of the CL mentioned in [c#6](https://issues.chromium.org/u/2/issues/368222741#comment6).

szager@ - Was this change a result of a specific bug? Do you think it addresses this issue?

vmpstr@ - As reviewer of the CL, can you PTAL to see if the CL can address the reported issue?

vmiura@ (or anyone else CC'd) - Can you PTAL or help re-route? Thanks!

I've also reached out directly to vmpstr@, vmiura@ (code owners).

### vm...@chromium.org (2024-10-25)

Stefan, it's possible that the work that you are doing to unify the image decode paths addressed this. If not, you likely have the most context right now about the work needed to fix the problem as described by OP.

Can you take a look?

### sz...@chromium.org (2024-11-04)

Sorry for the delay, this fell off my radar.

The analysis in [comment #1](https://issues.chromium.org/issues/368222741#comment1) sounds entirely plausible to me. Note that there are other places in the code where we make the same mistake (this is from auditing gpu\_image\_decode\_cache.cc for instances of base::AutoUnlock):

<https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/gpu_image_decode_cache.cc;l=2765-2788;drc=a45502c46d75f210c783e07384138379ea1e46e4;bpv=0;bpt=1>

<https://source.chromium.org/chromium/chromium/src/+/main:cc/tiles/gpu_image_decode_cache.cc;l=2853-2866;drc=a45502c46d75f210c783e07384138379ea1e46e4;bpv=0;bpt=1>

We should be holding scoped\_refptr<ImageData> anywhere there's a base::AutoUnlock. I'll put up a patch.

### ap...@google.com (2024-11-06)

Project: chromium/src  

Branch: main  

Author: Stefan Zager <[szager@chromium.org](mailto:szager@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5990752>

Prevent ImageData from being reclaimed while in use

---


Expand for full commit details
```
Prevent ImageData from being reclaimed while in use 
 
Bug: chromium:368222741 
Change-Id: If6b11492b01920306af042e001a65eb0d4b07f50 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5990752 
Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
Commit-Queue: Stefan Zager <szager@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1379290}

```

---

Files:

- M `cc/tiles/gpu_image_decode_cache.cc`

---

Hash: e65f06b6dc4792fe27c6872dbc7a1d185912cc48  

Date:  Wed Nov 06 22:26:50 2024


---

### ca...@chromium.org (2024-11-15)

[secondary shepherd Hi szager, did crrev.com/c/5990752 fix this or is there still work left?

### pe...@google.com (2024-11-19)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### sz...@chromium.org (2024-11-19)

Since there is no crash report or reliable reproduction, it's hard to say with certainty that the issue is fixed. This query *might* correspond to this issue:

<https://crash.corp.google.com/browse?q=product_name%3D%22Chrome%22+AND+STRPOS%28expanded_custom_data.ChromeCrashProto.magic_signature_1.name%2C+%27cc%3A%3AGpuImageDecodeCache%3A%3ADecodeImageIfNecessary%27%29+%3E+0>

Since the great bulk of crash reports is in stable channel, we may not know for certain whether the crash is fixed until the CL from [comment #11](https://issues.chromium.org/issues/368222741#comment11) reaches stable (it first appears in M132).

### th...@chromium.org (2024-12-11)

[secondary shepherd] From discussions with other security folks, I'm marking this bug as Fixed. In cases where we don't have a reliable repro to validate the fix, we geneally close the bug once the speculative fix is landed. This allows merge automation to kick in if relevant.

### pe...@google.com (2024-12-12)

Security Merge Request Consideration: Requesting merge to extended stable (M130) because latest trunk commit (1379290) appears to be after extended stable branch point (1356013).
Security Merge Request Consideration: Requesting merge to stable (M131) because latest trunk commit (1379290) appears to be after stable branch point (1368529).
Security Merge Request Consideration: Not requesting merge to beta (M132) because latest trunk commit (1379290) appears to be prior to beta branch point (1381561). If this is incorrect please remove NA-132 from the 'Merge' field and add 132 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request - Manual Review: Merge review required: M130 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M131 is already shipping to stable.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [130, 131].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2024-12-12)

This seems potentially mitigated by race, so it's unclear if high severity and backmerge to Stable / Extended Stable is fully warranted here. 
However this fix was landed on Canary so there is sufficient data from Canary, Dev, and Beta to confirm there should be no issues here, so I'm leaning toward backmerge to Stable and Extended Stable so this fix can fully ship sooner and prevent any potentially exploitable issues we may not know about yet from the other three areas where this was resolved in this CL. 

https://crrev.com/c/5990752 approved for merges to M131 Stable and M130 Extended Stable, please merge to branches 6778 and 6723 by 10am PT tomorrow so this fix an be included in next week's updates before the forthcoming holiday release freeze. Thank you.


### ap...@google.com (2024-12-14)

Project: chromium/src  

Branch: refs/branch-heads/6723  

Author: Stefan Zager <[szager@chromium.org](mailto:szager@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6093379>

[M130] Prevent ImageData from being reclaimed while in use

---


Expand for full commit details
```
[M130] Prevent ImageData from being reclaimed while in use 
 
Cherry-picked from: 
  https://chromium-review.googlesource.com/c/chromium/src/+/5990752 
 
Bug: chromium:368222741 
Change-Id: If830b19287fd7c4aa07137044f23a14f8ce6912d 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6093379 
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com> 
Owners-Override: Prudhvikumar Bommana <pbommana@google.com> 
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com> 
Cr-Commit-Position: refs/branch-heads/6723@{#2713} 
Cr-Branched-From: 985f2961df230630f9cbd75bd6fe463009855a11-refs/heads/main@{#1356013}

```

---

Files:

- M `cc/tiles/gpu_image_decode_cache.cc`

---

Hash: 3a6ff45cc3f48a359772f81c512c512b4f2d2643  

Date:  Sat Dec 14 11:06:00 2024


---

### pe...@google.com (2024-12-14)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ap...@google.com (2024-12-14)

Project: chromium/src  

Branch: refs/branch-heads/6778  

Author: Stefan Zager <[szager@chromium.org](mailto:szager@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6094731>

[M131] Prevent ImageData from being reclaimed while in use

---


Expand for full commit details
```
[M131] Prevent ImageData from being reclaimed while in use 
 
Cherry-picked from: 
  https://chromium-review.googlesource.com/c/chromium/src/+/5990752 
 
Bug: chromium:368222741 
Change-Id: Idcef7864100ba53143c3c809ae16b5988b8a3dbd 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6094731 
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com> 
Owners-Override: Prudhvikumar Bommana <pbommana@google.com> 
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com> 
Cr-Commit-Position: refs/branch-heads/6778@{#3025} 
Cr-Branched-From: b21671ca172dcfd1566d41a770b2808e7fa7cd88-refs/heads/main@{#1368529}

```

---

Files:

- M `cc/tiles/gpu_image_decode_cache.cc`

---

Hash: 72e3ee416f51703a649229ef753b55459d9036e8  

Date:  Sat Dec 14 11:25:51 2024


---

### pe...@google.com (2024-12-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-12-16)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6088725
2. Low - There was no conflict.
3. 130 and 131
4. Yes. although it's difficult to make sure that the issue could happen on M126 through the comments and the description, M126 looks have the same issue when checking the code base.


### sp...@google.com (2024-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
moderately mitigated security bug in the GPU process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-19)

Congratulations! Thank you for your efforts and reporting this issue to us.

### ap...@google.com (2025-01-29)

Project: chromium/src  

Branch: refs/branch-heads/6478  

Author: Stefan Zager <[szager@chromium.org](mailto:szager@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6088725>

[M126-LTS] Prevent ImageData from being reclaimed while in use

---


Expand for full commit details
```
[M126-LTS] Prevent ImageData from being reclaimed while in use 
 
(cherry picked from commit e65f06b6dc4792fe27c6872dbc7a1d185912cc48) 
 
Bug: chromium:368222741 
Change-Id: If6b11492b01920306af042e001a65eb0d4b07f50 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5990752 
Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
Commit-Queue: Stefan Zager <szager@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1379290} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6088725 
Reviewed-by: Fahad Mansoor <fahadmansoor@google.com> 
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
Cr-Commit-Position: refs/branch-heads/6478@{#2025} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `cc/tiles/gpu_image_decode_cache.cc`

---

Hash: ca2e751dc46a605232ba18b6a6d5b33c0604a523  

Date:  Tue Jan 28 19:18:20 2025


---

### ch...@google.com (2025-03-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/368222741)*
