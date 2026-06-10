# Heap-buffer-overflow in Skia PathStencilCoverOp via AtlasPathRenderer integer overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [484983991](https://issues.chromium.org/issues/484983991) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | si...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2026-02-17 |
| **Bounty** | $32,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

VULNERABILITY DETAILS

Component: Skia Ganesh GPU backend — `AtlasPathRenderer` / `PathStencilCoverOp` (Canvas 2D fill path)

An integer overflow in `AtlasRenderTask::AtlasPathList::add()` allows a user to trigger a heap-buffer-overflow write in `PathStencilCoverOp::onPrepare()` via the HTML Canvas 2D API. The attacker controls the data written past the buffer (path vertex coordinates).

`AtlasRenderTask.h:98` accumulates path verb counts with no overflow check:

```
fTotalCombinedPathVerbCnt += path.countVerbs();  // int32, no overflow check

```

The atlas only validates path **pixel bounds** (must fit in 2048x2048), not verb count.

This overflowed count is passed to `PathStencilCoverOp` (`AtlasRenderTask.cpp:120`), which uses it to allocate a single contiguous fan triangle buffer (`GrEagerDynamicVertexAllocator`):

```
// PathStencilCoverOp.cpp:277-280
int maxTrianglesInFans = std::max(fTotalCombinedPathVerbCnt - 2, 0);
vertexAlloc.lockWriter(sizeof(SkPoint), maxTrianglesInFans * 3);  // undersized!

```

The fan triangle write loop (`PathStencilCoverOp.cpp:281-289`) then iterates all actual paths with no runtime bounds checking (`VertexWriter::validate()` is gated on `SK_DEBUG`, which is off in official builds):

```
for (auto [pathMatrix, path, color] : *fPathDrawList) {
    for (tess::PathMiddleOutFanIter it(path); !it.done();) {
        for (auto [p0, p1, p2] : it.nextStack()) {
            triangleVertexWriter << m.map2Points(p0, p1) << m.mapPoint(p2);  // OOB write
        }
    }
}

```

VERSION
Chrome Version: Chrome 147.0.7691.0 ASAN, Windows stable

Operating System: Windows 11 Version 24H2, OS Build 26100.7840

REPRODUCTION CASE

The following flags were used: `chrome.exe --disable-gpu-sandbox --enable-gpu-rasterization --disable-features=SkiaGraphite --disable-gpu-watchdog --disable-gpu-driver-bug-workarounds --use-angle=vulkan --user-data-dir="%TEMP%\chrome-test-profile" --no-first-run --no-default-browser-check skia_atlas_overflow_poc.html`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser

```
chrome.exe --disable-gpu-sandbox --enable-gpu-rasterization --disable-features=SkiaGraphite --disable-gpu-watchdog --disable-gpu-driver-bug-workarounds --use-angle=vulkan --user-data-dir="%TEMP%\chrome-test-profile" --no-first-run --no-default-browser-check skia_atlas_overflow_poc.html
=================================================================
==46964==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x11acaa5d1820 at pc 0x7fff153543db bp 0x001237ffd540 sp 0x001237ffd588
WRITE of size 16 at 0x11acaa5d1820 thread T0
    #0 0x7fff153543da in skgpu::BufferWriter::write C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\BufferWriter.h:92
    #1 0x7fff153543da in skgpu::operator<< C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\BufferWriter.h:321
    #2 0x7fff153543da in skgpu::ganesh::PathStencilCoverOp::onPrepare(class GrOpFlushState *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\ops\PathStencilCoverOp.cpp:285:46
    #3 0x7fff15116c04 in GrOp::prepare(class GrOpFlushState *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\ops\GrOp.cpp:59:11
    #4 0x7fff1511e412 in skgpu::ganesh::OpsTask::onPrepare(class GrOpFlushState *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\ops\OpsTask.cpp:548:27
    #5 0x7fff15284653 in GrRenderTask::prepare(class GrOpFlushState *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrRenderTask.cpp:111:11
    #6 0x7fff153ec37a in GrDrawingManager::executeRenderTasks(class GrOpFlushState *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:266:21
    #7 0x7fff153ea19a in GrDrawingManager::flush(class SkSpan<class GrSurfaceProxy *>, enum SkSurfaces::BackendSurfaceAccess, struct GrFlushInfo const &, class skgpu::MutableTextureState const *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:209:34
    #8 0x7fff153ed7cd in GrDrawingManager::flushSurfaces(class SkSpan<class GrSurfaceProxy *>, enum SkSurfaces::BackendSurfaceAccess, struct GrFlushInfo const &, class skgpu::MutableTextureState const *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:540:27
    #9 0x7fff1540584b in GrDirectContextPriv::flushSurfaces(class SkSpan<class GrSurfaceProxy *>, enum SkSurfaces::BackendSurfaceAccess, struct GrFlushInfo const &, class skgpu::MutableTextureState const *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDirectContextPriv.cpp:92:47
    #10 0x7fff1541794a in GrDirectContextPriv::flushSurface C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDirectContextPriv.h:106
    #11 0x7fff1541794a in GrDirectContext::flush(class SkSurface *, struct GrFlushInfo const &, class skgpu::MutableTextureState const *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDirectContext.cpp:520:25
    #12 0x7fff150c88ed in skgpu::ganesh::Flush(class SkSurface *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\surface\SkSurface_Ganesh.cpp:759:45
    #13 0x7fff1937ff06 in gpu::SharedContextState::FlushWriteAccess(class gpu::SkiaImageRepresentation::ScopedWriteAccess *) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_context_state.cc:869:9
    #14 0x7fff19627512 in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM(void) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\raster_decoder.cc:3099:30
    #15 0x7fff19622078 in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile *) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\raster_decoder_autogen.h:151:3
    #16 0x7fff1962c03d in gpu::raster::RasterDecoderImpl::DoCommandsImpl<0>(unsigned int, void const volatile *, int, int *) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\raster_decoder.cc:1526:18
    #17 0x7fff035de36b in gpu::CommandBufferService::Flush(int, class gpu::AsyncAPIInterface *) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:267:35
    #18 0x7fff196e36e1 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, class std::__Cr::vector<struct gpu::SyncToken, class std::__Cr::allocator<struct gpu::SyncToken>> const &) C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:504:22
    #19 0x7fff196e25f3 in gpu::CommandBufferStub::ExecuteDeferredRequest(class gpu::mojom::DeferredCommandBufferRequestParams &, class gpu::FenceSyncReleaseDelegate *) C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:173:7
    #20 0x7fff196af4a1 in gpu::GpuChannel::ExecuteDeferredRequest(class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>, class gpu::FenceSyncReleaseDelegate *) C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:833:13
    #21 0x7fff196bf4cf in base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:740
    #22 0x7fff196bf4cf in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:956
    #23 0x7fff196bf4cf in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void (gpu::FenceSyncReleaseDelegate *)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069
    #24 0x7fff196bf4cf in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl gpu::GpuChannel::*&&)(class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>, class gpu::FenceSyncReleaseDelegate *), class base::WeakPtr<class gpu::GpuChannel> &&, class mojo::StructPtr<class gpu::mojom::DeferredRequestParams> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl gpu::GpuChannel::*)(class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>, class gpu::FenceSyncReleaseDelegate *), class base::WeakPtr<class gpu::GpuChannel>, class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>>, (class gpu::FenceSyncReleaseDelegate *)>::RunOnce(class base::internal::BindStateBase *, class gpu::FenceSyncReleaseDelegate *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982:12
    #25 0x7fff036204cb in base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #26 0x7fff036204cb in base::internal::DecayedFunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>,gpu::FenceSyncReleaseDelegate *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:815
    #27 0x7fff036204cb in base::internal::InvokeHelper<0,base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)> &&,gpu::FenceSyncReleaseDelegate *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932
    #28 0x7fff036204cb in base::internal::Invoker<struct base::internal::FunctorTraits<class base::OnceCallback<(class gpu::FenceSyncReleaseDelegate *)> &&, class gpu::FenceSyncReleaseDelegate *>, struct base::internal::BindState<0, 1, 1, class base::OnceCallback<(class gpu::FenceSyncReleaseDelegate *)>, class base::internal::UnretainedWrapper<class gpu::FenceSyncReleaseDelegate, struct base::unretained_traits::MayNotDangle, 0>>, (void)>::RunImpl<class base::OnceCallback<(class gpu::FenceSyncReleaseDelegate *)>, class std::__Cr::tuple<class base::internal::UnretainedWrapper<class gpu::FenceSyncReleaseDelegate, struct base::unretained_traits::MayNotDangle, 0>>, 0>(class base::OnceCallback<(class gpu::FenceSyncReleaseDelegate *)> &&, class std::__Cr::tuple<class base::internal::UnretainedWrapper<class gpu::FenceSyncReleaseDelegate, struct base::unretained_traits::MayNotDangle, 0>> &&, struct std::__Cr::integer_sequence<unsigned __int64, 0>) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069:14
    #29 0x7fff035f42f2 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #30 0x7fff035f42f2 in gpu::Scheduler::ExecuteSequence(class base::IdType<class gpu::SyncPointOrderData, unsigned int, 0, 1>) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:707:29
    #31 0x7fff035f2420 in gpu::Scheduler::RunNextTask(void) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:625:3
    #32 0x7fff035f6fa4 in base::internal::DecayedFunctorTraits<void (gpu::Scheduler::*)(),gpu::Scheduler *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:740
    #33 0x7fff035f6fa4 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(),gpu::Scheduler *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932
    #34 0x7fff035f6fa4 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(),gpu::Scheduler *>,base::internal::BindState<1,1,0,void (gpu::Scheduler::*)(),base::internal::UnretainedWrapper<gpu::Scheduler,base::unretained_traits::MayNotDangle,0> >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069
    #35 0x7fff035f6fa4 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl gpu::Scheduler::*&&)(void), class gpu::Scheduler *>, struct base::internal::BindState<1, 1, 0, void (__cdecl gpu::Scheduler::*)(void), class base::internal::UnretainedWrapper<class gpu::Scheduler, struct base::unretained_traits::MayNotDangle, 0>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982:12
    #36 0x7fff1434a988 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #37 0x7fff1434a988 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:229:34
    #38 0x7fff1431add1 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:112
    #39 0x7fff1431add1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475:23
    #40 0x7fff14319c33 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346:40
    #41 0x7fff14484b10 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #42 0x7fff1431cb1f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650:12
    #43 0x7fff143c25ac in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:135:14
    #44 0x7fff1deb4f03 in content::GpuMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc:479:14
    #45 0x7fff0ff97536 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:762:14
    #46 0x7fff0ff99bcb in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1147:10
    #47 0x7fff0ff8da9f in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:358:36
    #48 0x7fff0ff8e242 in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:371:10
    #49 0x7ffefff02b06 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:191:12
    #50 0x7ff7bac44807 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:204:12
    #51 0x7ff7bac42074 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351:20
    #52 0x7ff7bb13c83f in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #53 0x7ff7bb13c83f in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #54 0x7ff84e4be8d6  (C:\Windows\System32\KERNEL32.DLL+0x18002e8d6)
    #55 0x7ff84f06c40b  (C:\Windows\SYSTEM32\ntdll.dll+0x18008c40b)

0x11acaa5d1820 is located 0 bytes after 1572896-byte region [0x11acaa451800,0x11acaa5d1820)
allocated by thread T0 here:
    #0 0x7fff6924e51f  (C:\Users\symeon\Desktop\chromium-147.0.7691.0-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005e51f)
    #1 0x7fff15436d32 in GrCpuBuffer::Make C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrCpuBuffer.h:29
    #2 0x7fff15436d32 in GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned __int64, bool) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrBufferAllocPool.cpp:56:30
    #3 0x7fff15437fc7 in GrBufferAllocPool::resetCpuData(unsigned __int64) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrBufferAllocPool.cpp:389:60
    #4 0x7fff15439cd1 in GrBufferAllocPool::createBlock(unsigned __int64) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrBufferAllocPool.cpp:362:15
    #5 0x7fff15438fce in GrBufferAllocPool::makeSpace(unsigned __int64, unsigned __int64, class sk_sp<class GrBuffer const> *, unsigned __int64 *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrBufferAllocPool.cpp:229:16
    #6 0x7fff1543b8c0 in GrVertexBufferAllocPool::makeSpace(unsigned __int64, int, class sk_sp<class GrBuffer const> *, int *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrBufferAllocPool.cpp:445:28
    #7 0x7fff15349b27 in GrEagerDynamicVertexAllocator::lock(unsigned __int64, int) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrEagerVertexAllocator.cpp:20:31
    #8 0x7fff153528b8 in GrEagerVertexAllocator::lockWriter C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrEagerVertexAllocator.h:39
    #9 0x7fff153528b8 in skgpu::ganesh::PathStencilCoverOp::onPrepare(class GrOpFlushState *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\ops\PathStencilCoverOp.cpp:280:33
    #10 0x7fff15116c04 in GrOp::prepare(class GrOpFlushState *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\ops\GrOp.cpp:59:11
    #11 0x7fff1511e412 in skgpu::ganesh::OpsTask::onPrepare(class GrOpFlushState *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\ops\OpsTask.cpp:548:27
    #12 0x7fff15284653 in GrRenderTask::prepare(class GrOpFlushState *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrRenderTask.cpp:111:11
    #13 0x7fff153ec37a in GrDrawingManager::executeRenderTasks(class GrOpFlushState *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:266:21
    #14 0x7fff153ea19a in GrDrawingManager::flush(class SkSpan<class GrSurfaceProxy *>, enum SkSurfaces::BackendSurfaceAccess, struct GrFlushInfo const &, class skgpu::MutableTextureState const *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:209:34
    #15 0x7fff153ed7cd in GrDrawingManager::flushSurfaces(class SkSpan<class GrSurfaceProxy *>, enum SkSurfaces::BackendSurfaceAccess, struct GrFlushInfo const &, class skgpu::MutableTextureState const *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:540:27
    #16 0x7fff1540584b in GrDirectContextPriv::flushSurfaces(class SkSpan<class GrSurfaceProxy *>, enum SkSurfaces::BackendSurfaceAccess, struct GrFlushInfo const &, class skgpu::MutableTextureState const *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDirectContextPriv.cpp:92:47
    #17 0x7fff1541794a in GrDirectContextPriv::flushSurface C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDirectContextPriv.h:106
    #18 0x7fff1541794a in GrDirectContext::flush(class SkSurface *, struct GrFlushInfo const &, class skgpu::MutableTextureState const *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\GrDirectContext.cpp:520:25
    #19 0x7fff150c88ed in skgpu::ganesh::Flush(class SkSurface *) C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\ganesh\surface\SkSurface_Ganesh.cpp:759:45
    #20 0x7fff1937ff06 in gpu::SharedContextState::FlushWriteAccess(class gpu::SkiaImageRepresentation::ScopedWriteAccess *) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\shared_context_state.cc:869:9
    #21 0x7fff19627512 in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM(void) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\raster_decoder.cc:3099:30
    #22 0x7fff19622078 in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile *) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\raster_decoder_autogen.h:151:3
    #23 0x7fff1962c03d in gpu::raster::RasterDecoderImpl::DoCommandsImpl<0>(unsigned int, void const volatile *, int, int *) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\raster_decoder.cc:1526:18
    #24 0x7fff035de36b in gpu::CommandBufferService::Flush(int, class gpu::AsyncAPIInterface *) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc:267:35
    #25 0x7fff196e36e1 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, class std::__Cr::vector<struct gpu::SyncToken, class std::__Cr::allocator<struct gpu::SyncToken>> const &) C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:504:22
    #26 0x7fff196e25f3 in gpu::CommandBufferStub::ExecuteDeferredRequest(class gpu::mojom::DeferredCommandBufferRequestParams &, class gpu::FenceSyncReleaseDelegate *) C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc:173:7
    #27 0x7fff196af4a1 in gpu::GpuChannel::ExecuteDeferredRequest(class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>, class gpu::FenceSyncReleaseDelegate *) C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc:833:13
    #28 0x7fff196bf4cf in base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:740
    #29 0x7fff196bf4cf in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:956
    #30 0x7fff196bf4cf in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void (gpu::FenceSyncReleaseDelegate *)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069
    #31 0x7fff196bf4cf in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl gpu::GpuChannel::*&&)(class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>, class gpu::FenceSyncReleaseDelegate *), class base::WeakPtr<class gpu::GpuChannel> &&, class mojo::StructPtr<class gpu::mojom::DeferredRequestParams> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl gpu::GpuChannel::*)(class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>, class gpu::FenceSyncReleaseDelegate *), class base::WeakPtr<class gpu::GpuChannel>, class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>>, (class gpu::FenceSyncReleaseDelegate *)>::RunOnce(class base::internal::BindStateBase *, class gpu::FenceSyncReleaseDelegate *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982:12
    #32 0x7fff036204cb in base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #33 0x7fff036204cb in base::internal::DecayedFunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>,gpu::FenceSyncReleaseDelegate *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:815
    #34 0x7fff036204cb in base::internal::InvokeHelper<0,base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)> &&,gpu::FenceSyncReleaseDelegate *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932
    #35 0x7fff036204cb in base::internal::Invoker<struct base::internal::FunctorTraits<class base::OnceCallback<(class gpu::FenceSyncReleaseDelegate *)> &&, class gpu::FenceSyncReleaseDelegate *>, struct base::internal::BindState<0, 1, 1, class base::OnceCallback<(class gpu::FenceSyncReleaseDelegate *)>, class base::internal::UnretainedWrapper<class gpu::FenceSyncReleaseDelegate, struct base::unretained_traits::MayNotDangle, 0>>, (void)>::RunImpl<class base::OnceCallback<(class gpu::FenceSyncReleaseDelegate *)>, class std::__Cr::tuple<class base::internal::UnretainedWrapper<class gpu::FenceSyncReleaseDelegate, struct base::unretained_traits::MayNotDangle, 0>>, 0>(class base::OnceCallback<(class gpu::FenceSyncReleaseDelegate *)> &&, class std::__Cr::tuple<class base::internal::UnretainedWrapper<class gpu::FenceSyncReleaseDelegate, struct base::unretained_traits::MayNotDangle, 0>> &&, struct std::__Cr::integer_sequence<unsigned __int64, 0>) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069:14
    #36 0x7fff035f42f2 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #37 0x7fff035f42f2 in gpu::Scheduler::ExecuteSequence(class base::IdType<class gpu::SyncPointOrderData, unsigned int, 0, 1>) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:707:29

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\skia\src\gpu\BufferWriter.h:92 in skgpu::BufferWriter::write
Shadow bytes around the buggy address:
  0x11acaa5d1580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11acaa5d1600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11acaa5d1680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11acaa5d1700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11acaa5d1780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x11acaa5d1800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x11acaa5d1880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11acaa5d1900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11acaa5d1980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11acaa5d1a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11acaa5d1a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==46964==ADDITIONAL INFO

==46964==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7fff035f28a3 in gpu::Scheduler::RunNextTask(void) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:647:27
    #1 0x7fff035f28a3 in gpu::Scheduler::RunNextTask(void) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:647:27
    #2 0x7fff035f28a3 in gpu::Scheduler::RunNextTask(void) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:647:27
    #3 0x7fff035f28a3 in gpu::Scheduler::RunNextTask(void) C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc:647:27


Command line: `"C:\Users\symeon\Desktop\chromium-147.0.7691.0-win64-asan\chrome.exe" --type=gpu-process --disable-gpu-sandbox --enable-gpu-rasterization --disable-gpu-driver-bug-workarounds --use-angle=vulkan --user-data-dir="C:\Users\symeon\AppData\Local\Temp\chrome-test-profile" --no-pre-read-main-dll --start-stack-profiler --gpu-preferences=SAAAAAAAAADoAQAEAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAA== --metrics-shmem-handle=2020,i,2711572133984203719,598222915878074520,262144 --field-trial-handle=2184,i,4859281458461868149,12462582824067425576,262144 --disable-features=SkiaGraphite --variations-seed-version --pseudonymization-salt-handle=2188,i,1596115968977333280,2659678181742721290,4 --trace-process-track-uuid=3190708988185955192 --mojo-platform-channel-handle=2180 /prefetch:2`


==46964==END OF ADDITIONAL INFO

==46964==ABORTING
[47764:48420:0217/095337.032:ERROR:content\browser\gpu\gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=1
[47764:48420:0217/095344.320:ERROR:components\device_event_log\device_event_log_impl.cc:202] [09:53:44.319] USB: usb_service_win.cc:108 SetupDiGetDeviceProperty({{A45C254E-DF1C-4EFD-8020-67D146A850E0}, 6}) failed: Element not found. (0x490)
[47764:47488:0217/095344.506:ERROR:google_apis\gcm\engine\connection_factory_impl.cc:434] Failed to connect to MCS endpoint with error -105
[47764:47488:0217/095344.508:ERROR:google_apis\gcm\engine\registration_request.cc:275] Registration URL fetching failed.

```

CREDIT INFORMATION
Reporter credit: Symeon Paraschoudis

## Attachments

- [skia_atlas_overflow_poc.html](attachments/skia_atlas_overflow_poc.html) (text/html, 1.1 KB)

## Timeline

### si...@gmail.com (2026-02-17)

Output with UBAsan compiled flags....

```
[48108:35780:0217/103301.909:FATAL:third_party\skia\src\gpu\BufferWriter.h:140] check(!fEnd || Mark(fPtr, bytesToWrite) <= fEnd)
        chrome!base::debug::CollectStackTrace [0x7fff08ad554a+3a] (C:\Users\symeon\Desktop\chromium\src\base\debug\stack_trace_win.cc:383)
        chrome!base::debug::StackTrace::StackTrace [0x7fff08affe37+257] (C:\Users\symeon\Desktop\chromium\src\base\debug\stack_trace.cc:280)
        chrome!logging::LogMessage::Flush [0x7fff08d2a68a+2fa] (C:\Users\symeon\Desktop\chromium\src\base\logging.cc:706)
        chrome!logging::LogMessage::~LogMessage [0x7fff08d2a229+39] (C:\Users\symeon\Desktop\chromium\src\base\logging.cc:696)
        chrome!SkAbort_FileLine [0x7fff094980b1+1a1] (C:\Users\symeon\Desktop\chromium\src\skia\ext\google_logging.cc:83)
        chrome!skgpu::ganesh::PathStencilCoverOp::onPrepare [0x7fff202749aa+266a] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\ops\PathStencilCoverOp.cpp:292)
        chrome!GrOp::prepare [0x7fff1b9364e5+2a5] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\ops\GrOp.cpp:59)
        chrome!skgpu::ganesh::OpsTask::onPrepare [0x7fff14e13a8e+73e] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\ops\OpsTask.cpp:548)
        chrome!GrRenderTask::prepare [0x7fff14dd7144+1c4] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrRenderTask.cpp:111)
        chrome!GrDrawingManager::executeRenderTasks [0x7fff0f26d6bc+1bc] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:266)
        chrome!GrDrawingManager::flush [0x7fff0f26a9e5+f15] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:209)
        chrome!GrDrawingManager::flushSurfaces [0x7fff0f26f824+2d4] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:540)
        chrome!GrDirectContextPriv::flushSurfaces [0x7fff0f2a8cfb+62b] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDirectContextPriv.cpp:92)
        chrome!GrDirectContext::flush [0x7fff0938e905+2a5] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDirectContext.cpp:520)
        chrome!skgpu::ganesh::Flush [0x7fff0f229c6e+5e] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\surface\SkSurface_Ganesh.cpp:759)
        chrome!gpu::SharedContextState::FlushWriteAccess [0x7fff0a52019c+2dc] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\shared_context_state.cc:869)
        chrome!gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM [0x7fff1c257d30+7a0] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\raster_decoder.cc:3099)
        chrome!gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM [0x7fff1c251f39+9] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\raster_decoder_autogen.h:152)
        chrome!gpu::raster::RasterDecoderImpl::DoCommandsImpl<0> [0x7fff1c260fe0+370] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\raster_decoder.cc:1526)
        chrome!gpu::CommandBufferService::Flush [0x7ffef4e6f680+780] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\command_buffer_service.cc:267)
        chrome!gpu::CommandBufferStub::OnAsyncFlush [0x7fff0a541f46+736] (C:\Users\symeon\Desktop\chromium\src\gpu\ipc\service\command_buffer_stub.cc:504)
        chrome!gpu::CommandBufferStub::ExecuteDeferredRequest [0x7fff0a540d39+5a9] (C:\Users\symeon\Desktop\chromium\src\gpu\ipc\service\command_buffer_stub.cc:173)
        chrome!gpu::GpuChannel::ExecuteDeferredRequest [0x7fff105a2d4c+7cc] (C:\Users\symeon\Desktop\chromium\src\gpu\ipc\service\gpu_channel.cc:836)
        chrome!base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&> [0x7fff105b3050+1c0] (C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h:982)
        chrome!base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>::Run [0x7ffef4ebe6f8+1e8] (C:\Users\symeon\Desktop\chromium\src\base\functional\callback.h:156)
        chrome!base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)> &&,gpu::FenceSyncReleaseDelegate *>,base::internal::BindState<0,1,1,base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>,base::internal: [0x7ffef4ebe419+229] (C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h:1069)
        chrome!base::OnceCallback<void ()>::Run [0x7ffef192fcc3+1e3] (C:\Users\symeon\Desktop\chromium\src\base\functional\callback.h:156)
        chrome!gpu::Scheduler::ExecuteSequence [0x7ffef4e89cd6+be6] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:707)
        chrome!gpu::Scheduler::RunNextTask [0x7ffef4e87316+876] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:629)
        chrome!base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(),gpu::Scheduler *>,base::internal::BindState<1,1,0,void (gpu::Scheduler::*)(),base::internal::UnretainedWrapper<gpu::Scheduler,base::unretained_traits::MayNotDangle,0> >,voi [0x7ffef4e8d595+1a5] (C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h:982)
        chrome!base::OnceCallback<void ()>::Run [0x7ffef192fcc3+1e3] (C:\Users\symeon\Desktop\chromium\src\base\functional\callback.h:156)
        chrome!base::TaskAnnotator::RunTaskImpl [0x7fff08bcbb0b+32b] (C:\Users\symeon\Desktop\chromium\src\base\task\common\task_annotator.cc:229)
        chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x7fff0ed52874+1544] (C:\Users\symeon\Desktop\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475)
        chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x7fff0ed50b2a+40a] (C:\Users\symeon\Desktop\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346)
        chrome!base::MessagePumpDefault::Run [0x7fff0edb8411+321] (C:\Users\symeon\Desktop\chromium\src\base\message_loop\message_pump_default.cc:42)
        chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x7fff0ed55554+934] (C:\Users\symeon\Desktop\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650)
        chrome!base::RunLoop::Run [0x7fff08c535fa+65a] (C:\Users\symeon\Desktop\chromium\src\base\run_loop.cc:135)
        chrome!content::GpuMain [0x7fff0c78861b+110b] (C:\Users\symeon\Desktop\chromium\src\content\gpu\gpu_main.cc:479)
        chrome!content::RunOtherNamedProcessTypeMain [0x7fff051141b9+419] (C:\Users\symeon\Desktop\chromium\src\content\app\content_main_runner_impl.cc:762)
        chrome!content::ContentMainRunnerImpl::Run [0x7fff051170bb+9cb] (C:\Users\symeon\Desktop\chromium\src\content\app\content_main_runner_impl.cc:1147)
        chrome!content::RunContentProcess [0x7fff0510a4e1+a81] (C:\Users\symeon\Desktop\chromium\src\content\app\content_main.cc:358)
        chrome!content::ContentMain [0x7fff0510ac53+1d3] (C:\Users\symeon\Desktop\chromium\src\content\app\content_main.cc:371)
        chrome!ChromeMain [0x7ffef1142a96+566] (C:\Users\symeon\Desktop\chromium\src\chrome\app\chrome_main.cc:191)
        chrome!MainDllLoader::Launch [0x7ff7638a4d39+9c9] (C:\Users\symeon\Desktop\chromium\src\chrome\app\main_dll_loader_win.cc:204)
        chrome!main [0x7ff7638a2425+13b5] (C:\Users\symeon\Desktop\chromium\src\chrome\app\chrome_exe_main_win.cc:351)
        chrome!__scrt_common_main_seh [0x7ff763e68594+10c] (D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288)
        KERNEL32!BaseThreadInitThunk [0x7ff84e4be8d7+17]
        ntdll!RtlUserThreadStart [0x7ff84f06c40c+2c]
Task trace:
        chrome!gpu::Scheduler::RunNextTask [0x7ffef4e87844+da4] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:647)
        chrome!gpu::Scheduler::RunNextTask [0x7ffef4e87844+da4] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:647)
        chrome!gpu::Scheduler::RunNextTask [0x7ffef4e87844+da4] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:647)
        chrome!gpu::Scheduler::RunNextTask [0x7ffef4e87844+da4] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:647)
        chrome!gpu::Scheduler::RunNextTask [0x7ffef4e87844+da4] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:647)
Task trace buffer limit hit, update PendingTask::kTaskBacktraceLength to increase.
Crash keys:
  "gpu-gl-context-is-virtual" = "0"
  "gpu-url-chunk-chrome" = "chrome://gpu/RenderThreadImpl::CreateOffscreenContext/RendererMainThread"
  "variations" = "a66dbd64-71c38a98,102166ac-3f4a17df,8d24eeea-3f4a17df,b516dd81-3f4a17df,a66fd611-3f4a17df,148c69c8-77850c6f,8f80c10-78198108,7550b1c4-2aa7fdc8,ea815280-3f4a17df,ae727645-d13781e7,cad2b12b-8ef57898,d6ad7f9a-a9080253,bcb58f65-3f4a17df,4dc2f223-3f4a17df,1632add8-90563727,fc1790de-3f4a17df,35c106c9-3f4a17df,57d26b38-3f4a17df,f6f5c542-3f4a17df,5e05ef36-3f4a17df,3779be93-3f4a17df,9d5ecd8d-ca7d8d80,3e15bfc6-3f4a17df,e1d656a5-3f4a17df,7e6af697-b5e01f69,7ffaf59b-26f21c65,3e672fd9-e109e63f,4ab30a87-c9361ef3,6ddea229-6ddea229,d4daab79-3f4a17df,acf2401-ec6cb59a,81d334bc-e3e32dbb,e9844d40-3f4a17df,d1ae5bf4-3f4a17df,5e3a236d-59e286d0,3dbad317-3f4a17df,ba449693-695908d9,4af38a69-3c635604,b602fc3f-3f4a17df,54be7848-3f4a17df,da493d3c-3f4a17df,72bafd3e-cdb4c186,f3ed486d-3f4a17df,81c84cff-e4e4c9a,4076100b-3f4a17df,284b7c58-80f9a33e,6c6d8c51-3f4a17df,f390dfc4-f8de9cfd,8f418b04-299bae22,4fa4e3b8-3f4a17df,44fe0078-3f4a17df,c92d2cc4-3f4a17df,ea0d881d-fd860968,89bba52e-174ae9a8,5e2ea1a-3f4a17df,e2d2a641-33bf6d2e,94b88ba6-7e2e67c9,f3dbf5bd-faff9ce0,db59f83a-3f4a17df,33956e74-dd411bc1,30cf4980-61673e6,797fe373-3f4a17df,6f27bc8a-3f4a17df,e5c8270a-3f4a17df,c297985a-3f4a17df,5870a003-3f4a17df,1da56142-3f4a17df,951dcd0c-3f4a17df,b357b792-3f4a17df,a983f698-8e9cac75,9481ce98-3d47f4f4,2a426c03-3d47f4f4,70678518-dee66fa8,be338734-dee66fa8,5f9907a9-206f6a6e,8eeccb9a-c35b209e,2b465683-dee66fa8,52fc7926-ee3d6169,bc9b361d-dee66fa8,a41a7188-dee66fa8,ff71bfdc-dee66fa8,251fc742-dee66fa8,2159dd0c-dee66fa8,e7cc79d5-dee66fa8,4b935545-bb2d3403,9a38bae3-3d47f4f4,41ad04e1-e4065f40,2d1e43a3-3d47f4f4,386dc267-3d47f4f4,d69d967d-3695c92e,3c8f75a1-42ae4bee,a4406b35-1657e2d6,408da146-1657e2d6,"
  "num-experiments" = "93"
  "gr-context-type" = "GaneshGL"
  "egl-display-type" = "angle:Vulkan"
  "gpu-generation-intel" = "12"
  "gpu-vsver" = "3.00"
  "gpu-psver" = "3.00"
  "gpu-driver" = "31.0.15.5274"
  "gpu-rev" = "161"
  "gpu-subid" = "0x1611103c"
  "gpu_count" = "2"
  "gpu-devid" = "0x2571"
  "gpu-venid" = "0x10de"
  "chrome-trace-id" = "14756645943848589678"
  "reentry_guard_tls_slot" = "unused"
  "switch-13" = "--mojo-platform-channel-handle=2160"
  "switch-12" = "--trace-process-track-uuid=2772445969238945468"
  "switch-11" = "--pseudonymization-salt-handle=2204,i,12699387937323480726,42565"
  "switch-10" = "--variations-seed-version"
  "switch-9" = "--field-trial-handle=2164,i,5907722396211644557,3429537694544772"
  "switch-8" = "--metrics-shmem-handle=2024,i,11083858985161257643,1071278954013"
  "switch-7" = "--start-stack-profiler"
  "switch-6" = "--no-pre-read-main-dll"
  "switch-5" = "--user-data-dir=C:\Users\symeon\AppData\Local\Temp\chrome-test-p"
  "switch-4" = "--use-angle=vulkan"
  "switch-3" = "--disable-gpu-driver-bug-workarounds"
  "switch-2" = "--enable-gpu-rasterization"
  "switch-1" = "--disable-gpu-sandbox"
  "num-switches" = "17"
  "commandline-disabled-feature-1" = "SkiaGraphite"

Received fatal exception EXCEPTION_BREAKPOINT
        chrome!logging::LogMessage::HandleFatal [0x7fff08d2c0bf+63f] (C:\Users\symeon\Desktop\chromium\src\base\logging.cc:1045)
        chrome!logging::LogMessage::Flush [0x7fff08d2b288+ef8] (C:\Users\symeon\Desktop\chromium\src\base\logging.cc:924)
        chrome!logging::LogMessage::~LogMessage [0x7fff08d2a229+39] (C:\Users\symeon\Desktop\chromium\src\base\logging.cc:696)
        chrome!SkAbort_FileLine [0x7fff094980b1+1a1] (C:\Users\symeon\Desktop\chromium\src\skia\ext\google_logging.cc:83)
        chrome!skgpu::ganesh::PathStencilCoverOp::onPrepare [0x7fff202749aa+266a] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\ops\PathStencilCoverOp.cpp:292)
        chrome!GrOp::prepare [0x7fff1b9364e5+2a5] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\ops\GrOp.cpp:59)
        chrome!skgpu::ganesh::OpsTask::onPrepare [0x7fff14e13a8e+73e] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\ops\OpsTask.cpp:548)
        chrome!GrRenderTask::prepare [0x7fff14dd7144+1c4] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrRenderTask.cpp:111)
        chrome!GrDrawingManager::executeRenderTasks [0x7fff0f26d6bc+1bc] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:266)
        chrome!GrDrawingManager::flush [0x7fff0f26a9e5+f15] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:209)
        chrome!GrDrawingManager::flushSurfaces [0x7fff0f26f824+2d4] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:540)
        chrome!GrDirectContextPriv::flushSurfaces [0x7fff0f2a8cfb+62b] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDirectContextPriv.cpp:92)
        chrome!GrDirectContext::flush [0x7fff0938e905+2a5] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDirectContext.cpp:520)
        chrome!skgpu::ganesh::Flush [0x7fff0f229c6e+5e] (C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\surface\SkSurface_Ganesh.cpp:759)
        chrome!gpu::SharedContextState::FlushWriteAccess [0x7fff0a52019c+2dc] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\shared_context_state.cc:869)
        chrome!gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM [0x7fff1c257d30+7a0] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\raster_decoder.cc:3099)
        chrome!gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM [0x7fff1c251f39+9] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\raster_decoder_autogen.h:152)
        chrome!gpu::raster::RasterDecoderImpl::DoCommandsImpl<0> [0x7fff1c260fe0+370] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\raster_decoder.cc:1526)
        chrome!gpu::CommandBufferService::Flush [0x7ffef4e6f680+780] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\command_buffer_service.cc:267)
        chrome!gpu::CommandBufferStub::OnAsyncFlush [0x7fff0a541f46+736] (C:\Users\symeon\Desktop\chromium\src\gpu\ipc\service\command_buffer_stub.cc:504)
        chrome!gpu::CommandBufferStub::ExecuteDeferredRequest [0x7fff0a540d39+5a9] (C:\Users\symeon\Desktop\chromium\src\gpu\ipc\service\command_buffer_stub.cc:173)
        chrome!gpu::GpuChannel::ExecuteDeferredRequest [0x7fff105a2d4c+7cc] (C:\Users\symeon\Desktop\chromium\src\gpu\ipc\service\gpu_channel.cc:836)
        chrome!base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&> [0x7fff105b3050+1c0] (C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h:982)
        chrome!base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>::Run [0x7ffef4ebe6f8+1e8] (C:\Users\symeon\Desktop\chromium\src\base\functional\callback.h:156)
        chrome!base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)> &&,gpu::FenceSyncReleaseDelegate *>,base::internal::BindState<0,1,1,base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>,base::internal: [0x7ffef4ebe419+229] (C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h:1069)
        chrome!base::OnceCallback<void ()>::Run [0x7ffef192fcc3+1e3] (C:\Users\symeon\Desktop\chromium\src\base\functional\callback.h:156)
        chrome!gpu::Scheduler::ExecuteSequence [0x7ffef4e89cd6+be6] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:707)
        chrome!gpu::Scheduler::RunNextTask [0x7ffef4e87316+876] (C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:629)
        chrome!base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(),gpu::Scheduler *>,base::internal::BindState<1,1,0,void (gpu::Scheduler::*)(),base::internal::UnretainedWrapper<gpu::Scheduler,base::unretained_traits::MayNotDangle,0> >,voi [0x7ffef4e8d595+1a5] (C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h:982)
        chrome!base::OnceCallback<void ()>::Run [0x7ffef192fcc3+1e3] (C:\Users\symeon\Desktop\chromium\src\base\functional\callback.h:156)
        chrome!base::TaskAnnotator::RunTaskImpl [0x7fff08bcbb0b+32b] (C:\Users\symeon\Desktop\chromium\src\base\task\common\task_annotator.cc:229)
        chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x7fff0ed52874+1544] (C:\Users\symeon\Desktop\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475)
        chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x7fff0ed50b2a+40a] (C:\Users\symeon\Desktop\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346)
        chrome!base::MessagePumpDefault::Run [0x7fff0edb8411+321] (C:\Users\symeon\Desktop\chromium\src\base\message_loop\message_pump_default.cc:42)
        chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x7fff0ed55554+934] (C:\Users\symeon\Desktop\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650)
        chrome!base::RunLoop::Run [0x7fff08c535fa+65a] (C:\Users\symeon\Desktop\chromium\src\base\run_loop.cc:135)
        chrome!content::GpuMain [0x7fff0c78861b+110b] (C:\Users\symeon\Desktop\chromium\src\content\gpu\gpu_main.cc:479)
        chrome!content::RunOtherNamedProcessTypeMain [0x7fff051141b9+419] (C:\Users\symeon\Desktop\chromium\src\content\app\content_main_runner_impl.cc:762)
        chrome!content::ContentMainRunnerImpl::Run [0x7fff051170bb+9cb] (C:\Users\symeon\Desktop\chromium\src\content\app\content_main_runner_impl.cc:1147)
        chrome!content::RunContentProcess [0x7fff0510a4e1+a81] (C:\Users\symeon\Desktop\chromium\src\content\app\content_main.cc:358)
        chrome!content::ContentMain [0x7fff0510ac53+1d3] (C:\Users\symeon\Desktop\chromium\src\content\app\content_main.cc:371)
        chrome!ChromeMain [0x7ffef1142a96+566] (C:\Users\symeon\Desktop\chromium\src\chrome\app\chrome_main.cc:191)
        chrome!MainDllLoader::Launch [0x7ff7638a4d39+9c9] (C:\Users\symeon\Desktop\chromium\src\chrome\app\main_dll_loader_win.cc:204)
        chrome!main [0x7ff7638a2425+13b5] (C:\Users\symeon\Desktop\chromium\src\chrome\app\chrome_exe_main_win.cc:351)
        chrome!__scrt_common_main_seh [0x7ff763e68594+10c] (D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288)
        KERNEL32!BaseThreadInitThunk [0x7ff84e4be8d7+17]
        ntdll!RtlUserThreadStart [0x7ff84f06c40c+2c]
=================================================================
==48108==ERROR: AddressSanitizer: breakpoint on unknown address 0x7fff08d2c0bf (pc 0x7fff08d2c0bf bp 0x00ad499fcf20 sp 0x00ad499fcea0 T0)
==48108==*** WARNING: Failed to initialize DbgHelp!              ***
==48108==*** Most likely this means that the app is already      ***
==48108==*** using DbgHelp, possibly with incompatible flags.    ***
==48108==*** Due to technical reasons, symbolization might crash ***
==48108==*** or produce wrong results.                           ***
    #0 0x7fff08d2c0be in logging::LogMessage::HandleFatal C:\Users\symeon\Desktop\chromium\src\base\logging.cc:1022
    #1 0x7fff08d2b287 in logging::LogMessage::Flush C:\Users\symeon\Desktop\chromium\src\base\logging.cc:924
    #2 0x7fff08d2a228 in logging::LogMessage::~LogMessage C:\Users\symeon\Desktop\chromium\src\base\logging.cc:695
    #3 0x7fff094980b0 in SkAbort_FileLine C:\Users\symeon\Desktop\chromium\src\skia\ext\google_logging.cc:83
    #4 0x7fff202749a9 in skgpu::ganesh::PathStencilCoverOp::onPrepare C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\ops\PathStencilCoverOp.cpp:333
    #5 0x7fff1b9364e4 in GrOp::prepare C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\ops\GrOp.cpp:59
    #6 0x7fff14e13a8d in skgpu::ganesh::OpsTask::onPrepare C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\ops\OpsTask.cpp:548
    #7 0x7fff14dd7143 in GrRenderTask::prepare C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrRenderTask.cpp:111
    #8 0x7fff0f26d6bb in GrDrawingManager::executeRenderTasks C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:266
    #9 0x7fff0f26a9e4 in GrDrawingManager::flush C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:209
    #10 0x7fff0f26f823 in GrDrawingManager::flushSurfaces C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp:540
    #11 0x7fff0f2a8cfa in GrDirectContextPriv::flushSurfaces C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDirectContextPriv.cpp:92
    #12 0x7fff0938e904 in GrDirectContext::flush C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDirectContext.cpp:520
    #13 0x7fff0f229c6d in skgpu::ganesh::Flush C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\surface\SkSurface_Ganesh.cpp:759
    #14 0x7fff0a52019b in gpu::SharedContextState::FlushWriteAccess C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\shared_context_state.cc:869
    #15 0x7fff1c257d2f in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\raster_decoder.cc:3099
    #16 0x7fff1c251f38 in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\raster_decoder_autogen.h:151
    #17 0x7fff1c260fdf in gpu::raster::RasterDecoderImpl::DoCommandsImpl<0> C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\raster_decoder.cc:1526
    #18 0x7ffef4e6f67f in gpu::CommandBufferService::Flush C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\command_buffer_service.cc:267
    #19 0x7fff0a541f45 in gpu::CommandBufferStub::OnAsyncFlush C:\Users\symeon\Desktop\chromium\src\gpu\ipc\service\command_buffer_stub.cc:504
    #20 0x7fff0a540d38 in gpu::CommandBufferStub::ExecuteDeferredRequest C:\Users\symeon\Desktop\chromium\src\gpu\ipc\service\command_buffer_stub.cc:173
    #21 0x7fff105a2d4b in gpu::GpuChannel::ExecuteDeferredRequest C:\Users\symeon\Desktop\chromium\src\gpu\ipc\service\gpu_channel.cc:833
    #22 0x7fff105b304f in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel> &&,mojo::StructPtr<gpu::mojom::DeferredRequestParams> &&>,base::internal::BindState<1,1,0,void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate *),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void (gpu::FenceSyncReleaseDelegate *)>::RunOnce C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h:982
    #23 0x7ffef4ebe6f7 in base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>::Run C:\Users\symeon\Desktop\chromium\src\base\functional\callback.h:155
    #24 0x7ffef4ebe418 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)> &&,gpu::FenceSyncReleaseDelegate *>,base::internal::BindState<0,1,1,base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>,base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate,base::unretained_traits::MayNotDangle,0> >,void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>,std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate,base::unretained_traits::MayNotDangle,0> >,0> C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h:1069
    #25 0x7ffef192fcc2 in base::OnceCallback<void ()>::Run C:\Users\symeon\Desktop\chromium\src\base\functional\callback.h:155
    #26 0x7ffef4e89cd5 in gpu::Scheduler::ExecuteSequence C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:707
    #27 0x7ffef4e87315 in gpu::Scheduler::RunNextTask C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:625
    #28 0x7ffef4e8d594 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(),gpu::Scheduler *>,base::internal::BindState<1,1,0,void (gpu::Scheduler::*)(),base::internal::UnretainedWrapper<gpu::Scheduler,base::unretained_traits::MayNotDangle,0> >,void ()>::RunOnce C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h:982
    #29 0x7ffef192fcc2 in base::OnceCallback<void ()>::Run C:\Users\symeon\Desktop\chromium\src\base\functional\callback.h:155
    #30 0x7fff08bcbb0a in base::TaskAnnotator::RunTaskImpl C:\Users\symeon\Desktop\chromium\src\base\task\common\task_annotator.cc:229
    #31 0x7fff0ed52873 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\Users\symeon\Desktop\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:475
    #32 0x7fff0ed50b29 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\Users\symeon\Desktop\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346
    #33 0x7fff0edb8410 in base::MessagePumpDefault::Run C:\Users\symeon\Desktop\chromium\src\base\message_loop\message_pump_default.cc:42
    #34 0x7fff0ed55553 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\Users\symeon\Desktop\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650
    #35 0x7fff08c535f9 in base::RunLoop::Run C:\Users\symeon\Desktop\chromium\src\base\run_loop.cc:135
    #36 0x7fff0c78861a in content::GpuMain C:\Users\symeon\Desktop\chromium\src\content\gpu\gpu_main.cc:479
    #37 0x7fff051141b8 in content::RunOtherNamedProcessTypeMain C:\Users\symeon\Desktop\chromium\src\content\app\content_main_runner_impl.cc:762
    #38 0x7fff051170ba in content::ContentMainRunnerImpl::Run C:\Users\symeon\Desktop\chromium\src\content\app\content_main_runner_impl.cc:1147
    #39 0x7fff0510a4e0 in content::RunContentProcess C:\Users\symeon\Desktop\chromium\src\content\app\content_main.cc:358
    #40 0x7fff0510ac52 in content::ContentMain C:\Users\symeon\Desktop\chromium\src\content\app\content_main.cc:371
    #41 0x7ffef1142a95 in ChromeMain C:\Users\symeon\Desktop\chromium\src\chrome\app\chrome_main.cc:191
    #42 0x7ff7638a4d38 in MainDllLoader::Launch C:\Users\symeon\Desktop\chromium\src\chrome\app\main_dll_loader_win.cc:204
    #43 0x7ff7638a2424 in main C:\Users\symeon\Desktop\chromium\src\chrome\app\chrome_exe_main_win.cc:351
    #44 0x7ff763e68593 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #45 0x7ff84e4be8d6 in BaseThreadInitThunk+0x16 (C:\Windows\System32\KERNEL32.DLL+0x18002e8d6)
    #46 0x7ff84f06c40b in RtlUserThreadStart+0x2b (C:\Windows\SYSTEM32\ntdll.dll+0x18008c40b)

==48108==Register values:
rax = 0  rbx = 80  rcx = 7fff3c967cf0  rdx = 0
rdi = 21fa7b80000  rsi = 15a933f9dc  rbp = ad499fcf20  rsp = ad499fcea0
r8  = 7fff3c967cf0  r9  = 0  r10 = 7ff84c360000  r11 = 0
r12 = f2f2f2f2f2f2f2f2  r13 = 21fa7b80000  r14 = 21f81a05330  r15 = ad499fcfe0
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: breakpoint C:\Users\symeon\Desktop\chromium\src\base\logging.cc:1022 in logging::LogMessage::HandleFatal

==48108==ADDITIONAL INFO

==48108==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffef4e87843 in gpu::Scheduler::RunNextTask C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:647
    #1 0x7ffef4e87843 in gpu::Scheduler::RunNextTask C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:647
    #2 0x7ffef4e87843 in gpu::Scheduler::RunNextTask C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:647
    #3 0x7ffef4e87843 in gpu::Scheduler::RunNextTask C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\scheduler.cc:647


Command line: `"C:\Users\symeon\Desktop\chromium\src\out\asan\chrome.exe" --type=gpu-process --disable-gpu-sandbox --enable-gpu-rasterization --disable-gpu-driver-bug-workarounds --use-angle=vulkan --user-data-dir="C:\Users\symeon\AppData\Local\Temp\chrome-test-profile" --no-pre-read-main-dll --start-stack-profiler --gpu-preferences=SAAAAAAAAADoAQAEAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAA== --metrics-shmem-handle=2024,i,11083858985161257643,10712789540137715944,262144 --field-trial-handle=2164,i,5907722396211644557,3429537694544772943,262144 --disable-features=SkiaGraphite --variations-seed-version --pseudonymization-salt-handle=2204,i,12699387937323480726,4256573035488019492,4 --trace-process-track-uuid=2772445969238945468 --mojo-platform-channel-handle=2160 /prefetch:2`


==48108==END OF ADDITIONAL INFO

==48108==ABORTING
[32008:41628:0217/103327.855:ERROR:content\browser\gpu\gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=1

```

### ma...@google.com (2026-02-17)

Security shepherd: Skia folks, PTAL?

### ma...@google.com (2026-02-17)

Actually, OOB write in the GPU process should be Critical/S0.

### ch...@google.com (2026-02-18)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-18)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2026-02-20)

Project: skia  

Branch:  main  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1169977>

[ganesh] Guard verb counts in tessellation accumulation against overflow

---


Expand for full commit details
```
     
    Rejects adding a path if the total verb count would overflow. 
    Rejects merging ops if their total verb counts would overflow. 
    Clamps the min allocation size in the GrVertexChunkArray to prevent 
    overflow. 
    Clamps the preallocation verb count parameter to avoid overflow in their 
    intermediate calculations. 
     
    Bug: b/484983991 
    Change-Id: I32359cf10a996baf46b023a6cb8c608834942e0b 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1169977 
    Commit-Queue: Michael Ludwig <michaelludwig@google.com> 
    Reviewed-by: Thomas Smith <thomsmit@google.com>

```

---

Files:

- M `src/gpu/ganesh/GrVertexChunkArray.cpp`
- M `src/gpu/ganesh/ops/AtlasRenderTask.cpp`
- M `src/gpu/ganesh/ops/AtlasRenderTask.h`
- M `src/gpu/ganesh/ops/PathTessellateOp.cpp`
- M `src/gpu/tessellate/FixedCountBufferUtils.h`

---

Hash: 03d405099043409a7925e54d7cfad73a9c5ad8db  

Date: Thu Feb 19 21:29:16 2026


---

### mi...@google.com (2026-02-23)

This was difficult to reproduce so "fixed" is tentative.

With Graphite, this repro html quickly uses a large amount of memory and is then killed by the hang watchdog. The thread that is "hung" is busy writing many vertices, which is what I'd expect for this type of content.

On canary with graphite disabled, the browser became unresponsive and slowly increased memory usage. After many minutes I noticed that the browser was responsive again, but given the timeline it was difficult to see if there was a hang reset. There was not a clear crash report recorded for that time.

On stable with graphite disabled, had similar behavior and the crash report eventually complained of an OOM from PartitionAlloc while writing vertices in GrVertexChunkArray.

### si...@gmail.com (2026-02-24)

`This was difficult to reproduce so "fixed" is tentative.`

Edit: I'm sorry you were having issues repro'ing it. In my case, it took literally 2-3 seconds to trigger this crash on my computer as well as on 2 different machines that I've tried. That is with the flags I mentioned earlier.
On top of that, on a Release version it crashes on a straight memcpy() as seen below:

```
0:000> g
(7608.b840): Access violation - code c0000005 (!!! second chance !!!)
chrome!skgpu::BufferWriter::write [inlined in chrome!skgpu::ganesh::PathStencilCoverOp::onPrepare+0x45a]:
00007fff`03c7955a 0f113b          movups  xmmword ptr [rbx],xmm7 ds:00003dbc`002c9ff8=????????????????????????????????
0:000> r
rax=0000000000000010 rbx=00003dbc002c9ff8 rcx=000000a66c5fb098
rdx=000000a66c5fb0a4 rsi=00003dbc00571790 rdi=00007fff05e39390
rip=00007fff03c7955a rsp=000000a66c5fafd0 rbp=00007fff0773b0b8
 r8=000000a66c5fb0bc  r9=4348400043340000 r10=4348400043340000
r11=00007fff05daa49b r12=00003dbc014ebc00 r13=00000000000006a7
r14=000000a66c5fb060 r15=00003dbc014ebc28
iopl=0         nv up ei pl nz na pe cy
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010201
chrome!skgpu::BufferWriter::write [inlined in chrome!skgpu::ganesh::PathStencilCoverOp::onPrepare+0x45a]:
00007fff`03c7955a 0f113b          movups  xmmword ptr [rbx],xmm7 ds:00003dbc`002c9ff8=????????????????????????????????
0:000> dqs rbx-0x20 
00003dbc`002c9fd8  44e8a800`441976fa
00003dbc`002c9fe0  44e8a800`441976fa
00003dbc`002c9fe8  44e89800`441976fa
00003dbc`002c9ff0  44e8a800`441976fa
00003dbc`002c9ff8  00000000`00000000
00003dbc`002ca000  ????????`????????
00003dbc`002ca008  ????????`????????
00003dbc`002ca010  ????????`????????
00003dbc`002ca018  ????????`????????
00003dbc`002ca020  ????????`????????
00003dbc`002ca028  ????????`????????
00003dbc`002ca030  ????????`????????
00003dbc`002ca038  ????????`????????
00003dbc`002ca040  ????????`????????
00003dbc`002ca048  ????????`????????
00003dbc`002ca050  ????????`????????

0:000> k
 # Child-SP          RetAddr               Call Site
00 (Inline Function) --------`--------     chrome!skgpu::BufferWriter::write [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\BufferWriter.h @ 92] 
01 (Inline Function) --------`--------     chrome!skgpu::operator<< [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\BufferWriter.h @ 321] 
02 000000a6`6c5fafd0 00007fff`02a11eee     chrome!skgpu::ganesh::PathStencilCoverOp::onPrepare+0x45a [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\ops\PathStencilCoverOp.cpp @ 285] 
03 000000a6`6c5fb2f0 00007fff`0105c9fc     chrome!GrOp::prepare+0x11e [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\ops\GrOp.cpp @ 60] 
04 000000a6`6c5fb3a0 00007fff`0104f1a7     chrome!skgpu::ganesh::OpsTask::onPrepare+0x37c [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\ops\OpsTask.cpp @ 549] 
05 000000a6`6c5fb500 00007ffe`ff5e3577     chrome!GrRenderTask::prepare+0x67 [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrRenderTask.cpp @ 111] 
06 000000a6`6c5fb560 00007ffe`ff5e2f1c     chrome!GrDrawingManager::executeRenderTasks+0x67 [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp @ 266] 
07 000000a6`6c5fb600 00007ffe`ff5e3988     chrome!GrDrawingManager::flush+0x88c [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp @ 208] 
08 000000a6`6c5fd140 00007ffe`ff5f41ad     chrome!GrDrawingManager::flushSurfaces+0xb8 [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDrawingManager.cpp @ 540] 
09 000000a6`6c5fd200 00007ffe`fd8a24b0     chrome!GrDirectContextPriv::flushSurfaces+0x1ad [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDirectContextPriv.cpp @ 92] 
0a (Inline Function) --------`--------     chrome!GrDirectContextPriv::flushSurface+0x36 [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDirectContextPriv.h @ 106] 
0b 000000a6`6c5fd2d0 00007ffe`ff5d33e0     chrome!GrDirectContext::flush+0xa0 [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\GrDirectContext.cpp @ 520] 
0c 000000a6`6c5fd350 00007ffe`fde5efa1     chrome!skgpu::ganesh::Flush+0x40 [C:\Users\symeon\Desktop\chromium\src\third_party\skia\src\gpu\ganesh\surface\SkSurface_Ganesh.cpp @ 759] 
0d 000000a6`6c5fd390 00007fff`02d94848     chrome!gpu::SharedContextState::FlushWriteAccess+0xd1 [C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\shared_context_state.cc @ 866] 
0e 000000a6`6c5fd3f0 00007fff`02d92ef9     chrome!gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM+0xe8 [C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\raster_decoder.cc @ 3103] 
0f 000000a6`6c5fd4a0 00007fff`02d95e4e     chrome!gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM+0x9 [C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\raster_decoder_autogen.h @ 152] 
10 000000a6`6c5fd4d0 00007ffe`f833bdbd     chrome!gpu::raster::RasterDecoderImpl::DoCommandsImpl<0>+0x10e [C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\raster_decoder.cc @ 1526] 
11 000000a6`6c5fd680 00007ffe`fde686f5     chrome!gpu::CommandBufferService::Flush+0x1ed [C:\Users\symeon\Desktop\chromium\src\gpu\command_buffer\service\command_buffer_service.cc @ 267] 
12 000000a6`6c5fd860 00007ffe`fde68167     chrome!gpu::CommandBufferStub::OnAsyncFlush+0x155 [C:\Users\symeon\Desktop\chromium\src\gpu\ipc\service\command_buffer_stub.cc @ 505] 
13 000000a6`6c5fd950 00007ffe`ffc10e14     chrome!gpu::CommandBufferStub::ExecuteDeferredRequest+0x167 [C:\Users\symeon\Desktop\chromium\src\gpu\ipc\service\command_buffer_stub.cc @ 173] 
14 000000a6`6c5fda10 00007ffe`f9f6e575     chrome!gpu::GpuChannel::ExecuteDeferredRequest+0x114 [C:\Users\symeon\Desktop\chromium\src\gpu\ipc\service\gpu_channel.cc @ 836] 
15 (Inline Function) --------`--------     chrome!base::internal::DecayedFunctorTraits<void (optimization_guide::HintsManager::*)(base::OnceCallback<void ()>, const optimization_guide::proto::Hint *),base::WeakPtr<optimization_guide::HintsManager> &&,base::OnceCallback<void ()> &&>::Invoke+0x38 [C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h @ 740] 
16 (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (optimization_guide::HintsManager::*&&)(base::OnceCallback<void ()>, const optimization_guide::proto::Hint *) const,base::WeakPtr<optimization_guide::HintsManager> &&,base::OnceCallback<void ()> &&>,void,0,1>::MakeItSo+0x52 [C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h @ 956] 
17 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (optimization_guide::HintsManager::*&&)(base::OnceCallback<void ()>, const optimization_guide::proto::Hint *) const,base::WeakPtr<optimization_guide::HintsManager> &&,base::OnceCallback<void ()> &&>,base::internal::BindState<1,1,0,void (optimization_guide::HintsManager::*)(base::OnceCallback<void ()>, const optimization_guide::proto::Hint *) const,base::WeakPtr<optimization_guide::HintsManager>,base::OnceCallback<void ()> >,void (const optimization_guide::proto::Hint *)>::RunImpl+0x52 [C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h @ 1069] 
18 000000a6`6c5fdaa0 00007ffe`f835050c     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (optimization_guide::HintsManager::*&&)(base::OnceCallback<void ()>, const optimization_guide::proto::Hint *) const,base::WeakPtr<optimization_guide::HintsManager> &&,base::OnceCallback<void ()> &&>,base::internal::BindState<1,1,0,void (optimization_guide::HintsManager::*)(base::OnceCallback<void ()>, const optimization_guide::proto::Hint *) const,base::WeakPtr<optimization_guide::HintsManager>,base::OnceCallback<void ()> >,void (const optimization_guide::proto::Hint *)>::RunOnce+0x75 [C:\Users\symeon\Desktop\chromium\src\base\functional\bind_internal.h @ 982] 
19 (Inline Function) --------`--------     chrome!base::OnceCallback<void (gpu::FenceSyncReleaseDelegate *)>::Run+0x3c [C:\Users\symeon\Desktop\chromium\src\base\functional\callback.h @ 155] 

--- snip ---

0:000> !address 00003dbc`002c9fd8
                                     
Mapping file section regions...
Mapping module regions...
Mapping PEB regions...
Mapping TEB and stack regions...
Mapping heap regions...
Mapping page heap regions...
Mapping other regions...
Mapping stack trace database regions...
Mapping activation context regions...

Usage:                  <unknown>
Base Address:           00003dbc`002c0000
End Address:            00003dbc`002ca000
Region Size:            00000000`0000a000 (  40.000 kB)
State:                  00001000          MEM_COMMIT
Protect:                00000004          PAGE_READWRITE
Type:                   00020000          MEM_PRIVATE
Allocation Base:        00003db8`00000000
Allocation Protect:     00000001          PAGE_NOACCESS


Content source: 1 (target), length: 28


```

and the memcpy:

```
    void write(const void* src, size_t bytes) {
        auto s = this->slice(bytes);
        memcpy(s.data(), src, s.size_bytes());
    }

```

In any case, appreciate your time and the fix, thanks.

### ch...@google.com (2026-02-24)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M145. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### mi...@google.com (2026-02-24)

I was able to reproduce with a local asan build on linux and confirmed that with the CL above the verb count is no longer overflowing.

Questions for merge:

1. <https://skia-review.googlesource.com/1169977>
2. Released in 147.0.7701.0
3. No
4. No
5. No

### wf...@chromium.org (2026-02-25)

[vrp panel] michaelludwig - does this affect Android too?

### mi...@google.com (2026-02-25)

Yes, I think it could.

### dr...@chromium.org (2026-02-25)

No crashes in Canary, so approving merges.

### dx...@google.com (2026-02-27)

Project: skia  

Branch:  chrome/m146  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1176958>

[ganesh] Guard verb counts in tessellation accumulation against overflow

---


Expand for full commit details
```
     
    Rejects adding a path if the total verb count would overflow. 
    Rejects merging ops if their total verb counts would overflow. 
    Clamps the min allocation size in the GrVertexChunkArray to prevent 
    overflow. 
    Clamps the preallocation verb count parameter to avoid overflow in their 
    intermediate calculations. 
     
    Bug: b/484983991 
    Change-Id: I32359cf10a996baf46b023a6cb8c608834942e0b 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1169977 
    Commit-Queue: Michael Ludwig <michaelludwig@google.com> 
    Reviewed-by: Thomas Smith <thomsmit@google.com> 
    (cherry picked from commit 03d405099043409a7925e54d7cfad73a9c5ad8db) 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1176958 
    Commit-Queue: Thomas Smith <thomsmit@google.com> 
    Auto-Submit: Michael Ludwig <michaelludwig@google.com>

```

---

Files:

- M `src/gpu/ganesh/GrVertexChunkArray.cpp`
- M `src/gpu/ganesh/ops/AtlasRenderTask.cpp`
- M `src/gpu/ganesh/ops/AtlasRenderTask.h`
- M `src/gpu/ganesh/ops/PathTessellateOp.cpp`
- M `src/gpu/tessellate/FixedCountBufferUtils.h`

---

Hash: 50841da4a7b7064b3cea8a851e60ef921c87a103  

Date: Thu Feb 19 21:29:16 2026


---

### dx...@google.com (2026-02-27)

Project: skia  

Branch:  chrome/m144  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1176956>

[ganesh] Guard verb counts in tessellation accumulation against overflow

---


Expand for full commit details
```
     
    Rejects adding a path if the total verb count would overflow. 
    Rejects merging ops if their total verb counts would overflow. 
    Clamps the min allocation size in the GrVertexChunkArray to prevent 
    overflow. 
    Clamps the preallocation verb count parameter to avoid overflow in their 
    intermediate calculations. 
     
    Bug: b/484983991 
    Change-Id: I32359cf10a996baf46b023a6cb8c608834942e0b 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1169977 
    Commit-Queue: Michael Ludwig <michaelludwig@google.com> 
    Reviewed-by: Thomas Smith <thomsmit@google.com> 
    (cherry picked from commit 03d405099043409a7925e54d7cfad73a9c5ad8db) 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1176956 
    Auto-Submit: Michael Ludwig <michaelludwig@google.com> 
    Commit-Queue: Thomas Smith <thomsmit@google.com>

```

---

Files:

- M `src/gpu/ganesh/GrVertexChunkArray.cpp`
- M `src/gpu/ganesh/ops/AtlasRenderTask.cpp`
- M `src/gpu/ganesh/ops/AtlasRenderTask.h`
- M `src/gpu/ganesh/ops/PathTessellateOp.cpp`
- M `src/gpu/tessellate/FixedCountBufferUtils.h`

---

Hash: 2708a1b1540e59b8e3407405b0c991a5c7b69523  

Date: Thu Feb 19 21:29:16 2026


---

### dx...@google.com (2026-02-27)

Project: skia  

Branch:  chrome/m145  

Author:  Michael Ludwig [michaelludwig@google.com](mailto:michaelludwig@google.com)  

Link:    <https://skia-review.googlesource.com/1176957>

[ganesh] Guard verb counts in tessellation accumulation against overflow

---


Expand for full commit details
```
     
    Rejects adding a path if the total verb count would overflow. 
    Rejects merging ops if their total verb counts would overflow. 
    Clamps the min allocation size in the GrVertexChunkArray to prevent 
    overflow. 
    Clamps the preallocation verb count parameter to avoid overflow in their 
    intermediate calculations. 
     
    Bug: b/484983991 
    Change-Id: I32359cf10a996baf46b023a6cb8c608834942e0b 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1169977 
    Commit-Queue: Michael Ludwig <michaelludwig@google.com> 
    Reviewed-by: Thomas Smith <thomsmit@google.com> 
    (cherry picked from commit 03d405099043409a7925e54d7cfad73a9c5ad8db) 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1176957 
    Commit-Queue: Thomas Smith <thomsmit@google.com> 
    Auto-Submit: Michael Ludwig <michaelludwig@google.com>

```

---

Files:

- M `src/gpu/ganesh/GrVertexChunkArray.cpp`
- M `src/gpu/ganesh/ops/AtlasRenderTask.cpp`
- M `src/gpu/ganesh/ops/AtlasRenderTask.h`
- M `src/gpu/ganesh/ops/PathTessellateOp.cpp`
- M `src/gpu/tessellate/FixedCountBufferUtils.h`

---

Hash: fba326b8829e469ac02e5a68a0d36982ef1975bc  

Date: Thu Feb 19 21:29:16 2026


---

### mi...@google.com (2026-02-27)

Merges are complete.

### sp...@google.com (2026-03-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $32000.00 for this report.

Rationale for this decision:
Baseline. Sandbox escape / Memory corruption in a non-sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### si...@gmail.com (2026-03-06)

Thank you so much team, *really* appreciate it 🖤. Haven't disclosed anything at all, thanks again.

### ch...@google.com (2026-06-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484983991)*
