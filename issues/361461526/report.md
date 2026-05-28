# Integer overflow in Skia GrMeshDrawOp::PatternHelper::init leads to OOB write

| Field | Value |
|-------|-------|
| **Issue ID** | [361461526](https://issues.chromium.org/issues/361461526) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 129.0.6661.0 |
| **Reporter** | hy...@gmail.com |
| **Assignee** | ja...@google.com |
| **Created** | 2024-08-22 |
| **Bounty** | $15,000.00 |

## Description

# Steps to reproduce the problem

(Chromium)

1. Apply the chromium.diff renderer patch to chromium.
2. Run genskpic.py to generate drawable\_picture.skp.hh, then move the generated file to src/gpu/command\_buffer/client.
3. Build and start the browser.
4. Open index.html to trigger PoC.
5. GPU process will crash.

(Skia standalone)

1. Run genskpic.py to generate a .skp file.
2. You can now run it in skpbench using: ./out/asan/skpbench --src pic.skp --config gles.
3. UBSAN crash will happen.

# Problem Description

Creating a separate issue as per: <https://issues.chromium.org/issues/360758697#comment13>

Hi, while researching Skia for more bugs, I noticed that there's another hidden integer overflow there, `PatternHelper` (called from `RegionOpImpl::onPrepareDraws`) is also not checking against overflows when multiplying the amount of vertices per repetition with the number of quads to draw, so we can still overflow the vertex space even if `numRects` is a valid integer, see [1] [2] [3] below:

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/ops/RegionOp.cpp;l=150?q=RegionOp&ss=chromium%2Fchromium%2Fsrc>

```
    void onPrepareDraws(GrMeshDrawTarget* target) override {
        ...

        SkSafeMath safeMath;
        for (int i = 0; i < numRegions; i++) {
            numRects = safeMath.addInt(numRects, fRegions[i].fRegion.computeRegionComplexity());
        }
        if (!safeMath) {
            // This is a nonsensical draw, so we can just drop it.
            return;
        }

        if (!numRects) {
            return;
        }

        QuadHelper helper(target, fProgramInfo->geomProc().vertexStride(), numRects); // <-- [1]

        ...
    }

```

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/ops/GrMeshDrawOp.cpp;l=134>

```
GrMeshDrawOp::QuadHelper::QuadHelper(GrMeshDrawTarget* target,
                                     size_t vertexStride,
                                     int quadsToDraw) {
    ...
    this->init(target, GrPrimitiveType::kTriangles, vertexStride, std::move(indexBuffer),
               GrResourceProvider::NumVertsPerNonAAQuad(),
               GrResourceProvider::NumIndicesPerNonAAQuad(), quadsToDraw,
               GrResourceProvider::MaxNumNonAAQuads()); // <-- [2]
}

```

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/ops/GrMeshDrawOp.cpp;l=95;drc=82dff63dbf9db05e9274e11d9128af7b9f51ceaa>

```
void GrMeshDrawOp::PatternHelper::init(GrMeshDrawTarget* target, GrPrimitiveType primitiveType,
                                       size_t vertexStride, sk_sp<const GrBuffer> indexBuffer,
                                       int verticesPerRepetition, int indicesPerRepetition,
                                       int repeatCount, int maxRepetitions) {
    ...
    int vertexCount = verticesPerRepetition * repeatCount; // <-- [3] No checks are being made here against overflow.
    fVertices = target->makeVertexSpace(vertexStride, vertexCount, &vertexBuffer, &firstVertex);
    if (!fVertices) {
        SkDebugf("Vertices could not be allocated for patterned rendering.");
        return;
    }
    ...
}

```

(`indicesPerRepetition` should be validated as well).

`PatternHelper` is used in many operations other than `RegionOpImpl`, so checking for overflows here would be a cool thing to also mitigate attacks using other operations.

# Summary

Integer overflow in Skia GrMeshDrawOp::PatternHelper::init leads to OOB write

# Custom Questions

#### Type of crash:

gpu

#### Crash state:

```
=================================================================
==9095==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7d0890d2c820 at pc 0x7d090fe55493 bp 0x7ffde9e34b90 sp 0x7ffde9e34b88
WRITE of size 4 at 0x7d0890d2c820 thread T0 (chrome)
==9095==WARNING: invalid path to external symbolizer!
==9095==WARNING: Failed to use and restart external symbolizer!
    #0 0x7d090fe55492 in operator<<<float> ./../../third_party/skia/src/gpu/BufferWriter.h:280:5
    #1 0x7d090fe55492 in writeVertex ./../../third_party/skia/src/gpu/BufferWriter.h:0:0
    #2 0x7d090fe55492 in writeQuadVertex<1, skgpu::VertexWriter::TriStrip<float>, skgpu::VertexColor> ./../../third_party/skia/src/gpu/BufferWriter.h:262:14
    #3 0x7d090fe55492 in writeQuad<skgpu::VertexWriter::TriStrip<float>, skgpu::VertexColor> ./../../third_party/skia/src/gpu/BufferWriter.h:246:15
    #4 0x7d090fe55492 in skgpu::ganesh::RegionOp::(anonymous namespace)::RegionOpImpl::onPrepareDraws(GrMeshDrawTarget*) ./../../third_party/skia/src/gpu/ganesh/ops/RegionOp.cpp:170:26
    #5 0x7d090fe30ac0 in GrOp::prepare(GrOpFlushState*) ./../../third_party/skia/src/gpu/ganesh/ops/GrOp.h:197:15
    #6 0x7d090fe3033c in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) ./../../third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #7 0x7d090fc378d9 in GrRenderTask::prepare(GrOpFlushState*) ./../../third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #8 0x7d090fbdbe50 in GrDrawingManager::executeRenderTasks(GrOpFlushState*) ./../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:260:21
    #9 0x7d090fbda829 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) ./../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:203:34
    #10 0x7d090fbdcf7c in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) ./../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:530:27
    #11 0x7d090fbca9c9 in GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) ./../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:92:47
    #12 0x7d090fbbf607 in flushSurface ./../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
    #13 0x7d090fbbf607 in GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*) ./../../third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:516:25
    #14 0x7d090fe96e1b in skgpu::ganesh::Flush(SkSurface*) ./../../third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:782:45
    #15 0x7d08d9f90829 in gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*) ./../../gpu/command_buffer/service/shared_context_state.cc:789:9
    #16 0x7d08d9f4927b in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM() ./../../gpu/command_buffer/service/raster_decoder.cc:3197:30
    #17 0x7d08d9f43ac8 in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*) ./../../gpu/command_buffer/service/raster_decoder_autogen.h:151:3
    #18 0x7d08d9f4e321 in gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/raster_decoder.cc:1539:18
    #19 0x7d09046d3826 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:231:35
    #20 0x7d08dc128e5c in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) ./../../gpu/ipc/service/command_buffer_stub.cc:502:22
    #21 0x7d08dc128101 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command_buffer_stub.cc:153:7
    #22 0x7d08dc148655 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long) ./../../gpu/ipc/service/gpu_channel.cc:932:13
    #23 0x7d08dc156e8e in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&) ./../../base/functional/bind_internal.h:738:12
    #24 0x7d08dc156c74 in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long> > ./../../base/functional/bind_internal.h:954:5
    #25 0x7d08dc156c74 in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1067:14
    #26 0x7d08dc156c74 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #27 0x7d090471076e in Run ./../../base/functional/callback.h:156:12
    #28 0x7d090471076e in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) ./../../gpu/command_buffer/service/scheduler_dfs.cc:598:24
    #29 0x7d090470e155 in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command_buffer/service/scheduler_dfs.cc:522:3
    #30 0x7d0904711f40 in Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs *> ./../../base/functional/bind_internal.h:738:12
    #31 0x7d0904711f40 in MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:930:12
    #32 0x7d0904711f40 in RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #33 0x7d0904711f40 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #34 0x7d09139bee6a in Run ./../../base/functional/callback.h:156:12
    #35 0x7d09139bee6a in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #36 0x7d0913a30793 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> ./../../base/task/common/task_annotator.h:90:5
    #37 0x7d0913a30793 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #38 0x7d0913a2f69e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #39 0x7d0913a314b4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #40 0x7d0913bc2cb3 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:694:48
    #41 0x7d0913a32084 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #42 0x7d0913943a12 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #43 0x7d0907b71fdb in content::GpuMain(content::MainFunctionParams) ./../../content/gpu/gpu_main.cc:431:14
    #44 0x7d090b77ad5a in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:703:14
    #45 0x7d090b77bb29 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:807:12
    #46 0x7d090b77dfd2 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1175:10
    #47 0x7d090b77902c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:333:36
    #48 0x7d090b77985a in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:346:10
    #49 0x58d4249a28b5 in ChromeMain ./../../chrome/app/chrome_main.cc:230:12
    #50 0x7d08b3e29d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x7d0890d2c820 is located 0 bytes after 1048608-byte region [0x7d0890c2c800,0x7d0890d2c820)
allocated by thread T0 (chrome) here:
    #0 0x58d4249a00bd in operator new(unsigned long) _asan_rtl_:3
    #1 0x7d090fb9bc9d in Make ./../../third_party/skia/src/gpu/ganesh/GrCpuBuffer.h:29:20
    #2 0x7d090fb9bc9d in GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned long, bool) ./../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:56:30
    #3 0x7d090fb9cb9c in GrBufferAllocPool::resetCpuData(unsigned long) ./../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:389:60
    #4 0x7d090fb9e51a in GrBufferAllocPool::createBlock(unsigned long) ./../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:362:15
    #5 0x7d090fb9da01 in GrBufferAllocPool::makeSpace(unsigned long, unsigned long, sk_sp<GrBuffer const>*, unsigned long*) ./../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:229:16
    #6 0x7d090fb9fc02 in GrVertexBufferAllocPool::makeSpace(unsigned long, int, sk_sp<GrBuffer const>*, int*) ./../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:445:28
    #7 0x7d090fdf3eef in GrMeshDrawOp::PatternHelper::init(GrMeshDrawTarget*, GrPrimitiveType, unsigned long, sk_sp<GrBuffer const>, int, int, int, int) ./../../third_party/skia/src/gpu/ganesh/ops/GrMeshDrawOp.cpp:96:25
    #8 0x7d090fdf4500 in GrMeshDrawOp::QuadHelper::QuadHelper(GrMeshDrawTarget*, unsigned long, int) ./../../third_party/skia/src/gpu/ganesh/ops/GrMeshDrawOp.cpp:134:11
    #9 0x7d090fe542bf in skgpu::ganesh::RegionOp::(anonymous namespace)::RegionOpImpl::onPrepareDraws(GrMeshDrawTarget*) ./../../third_party/skia/src/gpu/ganesh/ops/RegionOp.cpp:157:20
    #10 0x7d090fe30ac0 in GrOp::prepare(GrOpFlushState*) ./../../third_party/skia/src/gpu/ganesh/ops/GrOp.h:197:15
    #11 0x7d090fe3033c in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) ./../../third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #12 0x7d090fc378d9 in GrRenderTask::prepare(GrOpFlushState*) ./../../third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #13 0x7d090fbdbe50 in GrDrawingManager::executeRenderTasks(GrOpFlushState*) ./../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:260:21
    #14 0x7d090fbda829 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) ./../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:203:34
    #15 0x7d090fbdcf7c in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) ./../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:530:27
    #16 0x7d090fbca9c9 in GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) ./../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:92:47
    #17 0x7d090fbbf607 in flushSurface ./../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
    #18 0x7d090fbbf607 in GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*) ./../../third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:516:25
    #19 0x7d090fe96e1b in skgpu::ganesh::Flush(SkSurface*) ./../../third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:782:45
    #20 0x7d08d9f90829 in gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*) ./../../gpu/command_buffer/service/shared_context_state.cc:789:9
    #21 0x7d08d9f4927b in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM() ./../../gpu/command_buffer/service/raster_decoder.cc:3197:30
    #22 0x7d08d9f43ac8 in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*) ./../../gpu/command_buffer/service/raster_decoder_autogen.h:151:3
    #23 0x7d08d9f4e321 in gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/raster_decoder.cc:1539:18
    #24 0x7d09046d3826 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:231:35
    #25 0x7d08dc128e5c in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) ./../../gpu/ipc/service/command_buffer_stub.cc:502:22
    #26 0x7d08dc128101 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command_buffer_stub.cc:153:7
    #27 0x7d08dc148655 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long) ./../../gpu/ipc/service/gpu_channel.cc:932:13
    #28 0x7d08dc156e8e in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&) ./../../base/functional/bind_internal.h:738:12
    #29 0x7d08dc156c74 in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long> > ./../../base/functional/bind_internal.h:954:5
    #30 0x7d08dc156c74 in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1067:14
    #31 0x7d08dc156c74 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #32 0x7d090471076e in Run ./../../base/functional/callback.h:156:12
    #33 0x7d090471076e in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) ./../../gpu/command_buffer/service/scheduler_dfs.cc:598:24
    #34 0x7d090470e155 in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command_buffer/service/scheduler_dfs.cc:522:3

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/hyhy100/chromium2/src/out/asan/libskia.so+0xc55492) (BuildId: 739a908ae5387373)
Shadow bytes around the buggy address:
  0x7d0890d2c580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d0890d2c600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d0890d2c680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d0890d2c700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7d0890d2c780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7d0890d2c800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x7d0890d2c880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d0890d2c900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d0890d2c980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d0890d2ca00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d0890d2ca80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==9095==ADDITIONAL INFO

==9095==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7d090470e73a in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command_buffer/service/scheduler_dfs.cc:538:27
    #1 0x7d090470e73a in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command_buffer/service/scheduler_dfs.cc:538:27
    #2 0x7d090470e73a in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command_buffer/service/scheduler_dfs.cc:538:27
    #3 0x7d090470e73a in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command_buffer/service/scheduler_dfs.cc:538:27

Command line: `/proc/self/exe --type=gpu-process --string-annotations --crashpad-handler-pid=9058 --enable-crash-reporter=, --no-subproc-heap-profiling --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAgAAAEAAAAAAAAAAAAAAAAAABgAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,7711159281679077118,5503874274070490124,262144 --field-trial-handle=3,i,8533360048761144999,15654948628870376523,262144 --variations-seed-version`

==9095==END OF ADDITIONAL INFO
==9095==ABORTING
[9053:9053:0822/110423.428241:ERROR:gpu_process_host.cc(980)] GPU process exited unexpectedly: exit_code=256

```
#### Reporter credit:

Renan Rios (@hyhy\_100)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: No

## Attachments

- [genskpic_POSTFIX.py](attachments/genskpic_POSTFIX.py) (text/x-python, 3.5 KB)
- [index.html](attachments/index.html) (text/html, 191 B)
- [chromium.diff](attachments/chromium.diff) (text/x-diff, 6.7 KB)

## Timeline

### am...@chromium.org (2024-08-22)

I didn't attempt to reproduce this based on the conversation in [crbug.com/360758697](https://crbug.com/360758697) and the plausibility of this issue based on the information provided.
Wanted to get visibility to the Skia folks sooner than later.
P1 since this is GPU process memory corruption with the precondition of a compromised renderer
Foundin-128, since 128 is current Stable / Extended Stable, but likely existing for some time

### mi...@google.com (2024-08-22)

Interestingly, the `maxRepetitions` parameter is not validated against `repeatCount` before attempting any math, and looking deeper into the implementation of `drawIndexPattern`, it's actually acceptable for the total repeatCount to be greater than this `maxRepetitions` value. The maximum represents how many pattern instances fit within the bound index buffer, and if more than that many instances are needed, multiple draw calls are issued with a shifted base vertex to start reading from a later part in the bound vertex buffer.

Here are the usages of `PatternHelper` that I found:

1. In `AAStrokeRectOp::onPrepareDraws`, which has a `verticesPerRepetition` set to either 16 or 24 depending on being mitered or not. `repeatCount` is equal to the number of stroked rects accumulated in the op. `onCombineIfPossible` has no logic that would limit the number of accumulated stroked rects. This op would need to be fixed.
2. In `EllipticalRRectOp::onPrepareDraws`, which has a `verticesPerRepetition` set to 16 and a `repeatCount` equal to the number of accumulated RRects. `onCombineIfPossible` has no logic to limit the number of accumulated rrects (all other batch-breaking state being equal).
3. In `AAHairLinePathRenderer::onPrepareDraws`, which has a `verticesPerRepetition` set to 6 and a `repeatCount` equal to the local variable `lineCount`. `lineCount` is the number of collected line points divided by 2, but there is a check before reaching the PatternHelper to ensure that `lineCount <= SK_MaxS32 / 6`. This should mean that the value in `PatternHelper::init()` won't overflow.

It seems reasonable to me to generalize the overflow check that is in `AAHairLinePathRenderer` and have it be in `PatternHelper`. The ops are already validating that the helper created a vertex buffer and exiting early if that failed, so if there would have been an overflow, `PatternHelper` can just skip allocating a buffer.

That said, given the low `verticesPerRepetition`, we would need to accumulate (2147483647 / 24) = ~89478486 rects to trigger an overflow. Each rect is 16 bytes so that's 1.3GB of data that would have to be directly held by the `AAStrokeRectOp` (and even higher amount for `EllipticalRRectOp` since its vertex count is 16 not 24). Are there limits in PartitionAlloc that would prevent such a thing from ever reaching that point?

### pe...@google.com (2024-08-23)

Setting milestone because of s0/s1 severity.

### hy...@gmail.com (2024-08-24)

A few more instances of `PatternHelper` being used via the subclass [QuadHelper](https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/ops/GrMeshDrawOp.h;l=96;bpv=1;bpt=1) (the same that I used here to trigger the overflow from `RegionOpImpl`).

- `DrawAtlasOpImpl::onPrepareDraws`, the overflow should be reachable in some machines, the process would consume a big amount of RAM in an hypothetical attack, but it's still doable here because we have memory swapping, and we can split all data between many smaller allocations with `N` quads(`sprites`) each to avoid the `PartitionAlloc` allocation limit from killing the process.
- `NonAALatticeOp::onPrepareDraws`, it would work (much cheaper than a `DrawAtlasOpImpl`), but I don't know if [the color space check](https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/ops/LatticeOp.cpp;l=399?q=LatticeOp&ss=chromium%2Fchromium%2Fsrc) in `NonAALatticeOp::onCombineIfPossible` here is intentional, because looks like ops are never going to be merged (shouldn't it be checking if they don't match instead?). So, assuming the if condition here is intentional and there's a world where `onCombineIfPossible` would return `kMerged`, it would be an alternative.
- `EllipseOp::onPrepareDraws` and `DIEllipseOp::onPrepareDraws`, both are using a `STArray` with no indirect allocations of `N` items per element, so it would end up being killed. Also, growing a `STArray` like this is very slow (every reallocation of the buffer would have to copy elements again).
- `RegionOpImpl::onPrepareDraws`, cheap, `N` items per array element, it had an overflow before even doing the `verticesPerRepetition * repeatCount` multiplication. Probably the best current operation to reach the given overflow up to my knowledge (after some debugging, a nice thing here is that all region ops are sharing the same buffer of `intervals`[subregions], so cost here is almost zero).
- `DashOpImpl::onPrepareDraws`, uses a `STArray`, slow and will be killed due to the huge amount of elements required to trigger the overflow.

`PartitionAlloc` will kill the process with any attempt to allocate a buffer with a size [bigger than 2GB](https://issues.chromium.org/issues/40055619#comment5) in order to mitigate some security bugs related to 32-bit integers (and it's working great for that, since it mitigated some other integer overflows I have in the context of chrome).

Integer overflows alone are not really vulnerabilities most of the time, but what happens after they overflow, I feel like presence of libcxx hardening is a bit weaker here (many C-like array pointers, no runtime checks when writing data to `BufferWriter`, etc), runtime checks are already being used in `STArray` to prevent out of bounds accesses for example, but not sure if there are performance implications related to using it in more places.

**Edit: Also, demonstrating further impact via an Android GPU process stacktrace (SBX):**

```
* thread #14, name = 'CrGpuMain', stop reason = signal SIGSEGV: address access protected (fault address: 0x7310a778a000)
  * frame #0: 0x000073117e2d6684 libskia.cr.so`skgpu::VertexWriter& skgpu::operator<<<float>(w=0x000073119c014ea0, val=0x000073119c014f0c) at BufferWriter.h:280:5
    frame #1: 0x000073117e321259 libskia.cr.so`std::__Cr::enable_if<is_quad<skgpu::VertexWriter::TriStrip<float>>::value, void>::type skgpu::VertexWriter::writeQuadVertex<1, skgpu::VertexWriter::TriStrip<float>, skgpu::VertexColor>(this=0x000073119c014ea0, quad=<unavailable>, remainder=0x000073119c014ee0) at BufferWriter.h:262:14
    frame #2: 0x000073117e3211f3 libskia.cr.so`void skgpu::VertexWriter::writeQuad<skgpu::VertexWriter::TriStrip<float>, skgpu::VertexColor>(this=0x000073119c014ea0, remainder=0x000073119c014f00, remainder=0x000073119c014ee0) at BufferWriter.h:246:15
    frame #3: 0x000073117e320fb3 libskia.cr.so`skgpu::ganesh::RegionOp::(anonymous namespace)::RegionOpImpl::onPrepareDraws(this=0x00007312bd4a95b0, target=<unavailable>) at RegionOp.cpp:140:26
    frame #4: 0x000073117e318409 libskia.cr.so`GrOp::prepare(this=0x00007312bd4a95b0, state=0x000073119c015190) at GrOp.h:187:15
    frame #5: 0x000073117e31825e libskia.cr.so`skgpu::ganesh::OpsTask::onPrepare(this=0x000073133d4ac4c0, flushState=0x000073119c015190) at OpsTask.cpp:531:27
    frame #6: 0x000073117e289464 libskia.cr.so`GrRenderTask::prepare(this=0x000073133d4ac4c0, flushState=0x000073119c015190) at GrRenderTask.cpp:111:11
    frame #7: 0x000073117e268631 libskia.cr.so`GrDrawingManager::executeRenderTasks(this=0x000073128d486850, flushState=0x000073119c015190) at GrDrawingManager.cpp:260:21
    frame #8: 0x000073117e267b76 libskia.cr.so`GrDrawingManager::flush(this=0x000073128d486850, proxies=SkSpan @ 0x000073119c015140, access=kNoAccess, info=0x000073117de87b48, newState=0x0000000000000000) at GrDrawingManager.cpp:203:34
    frame #9: 0x000073117e268f2e libskia.cr.so`GrDrawingManager::flushSurfaces(this=0x000073128d486850, proxies=SkSpan @ 0x000073119c016c48, access=kNoAccess, info=0x000073117de87b48, newState=0x0000000000000000) at GrDrawingManager.cpp:530:27
    frame #10: 0x000073117e261d42 libskia.cr.so`GrDirectContextPriv::flushSurfaces(this=0x000073119c016dc0, proxies=SkSpan @ 0x000073119c016cf8, access=kNoAccess, info=0x000073117de87b48, newState=0x0000000000000000) at GrDirectContextPriv.cpp:92:47
    frame #11: 0x000073117e25ee38 libskia.cr.so`GrDirectContextPriv::flushSurface(this=0x000073119c016dc0, proxy=0x00007312dd484250, access=kNoAccess, info=0x000073117de87b48, newState=0x0000000000000000) at GrDirectContextPriv.h:106:22
    frame #12: 0x000073117e25eecc libskia.cr.so`GrDirectContext::flush(this=0x00007312bd4a6f70, surface=0x000073125d48a530, info=0x000073117de87b48, newState=0x0000000000000000) at GrDirectContext.cpp:516:25
    frame #13: 0x000073117e3317d2 libskia.cr.so`skgpu::ganesh::Flush(surface=0x000073125d48a530) at SkSurface_Ganesh.cpp:782:45
    frame #14: 0x0000731163851442 libgpu_gles2.cr.so`gpu::SharedContextState::FlushWriteAccess(this=<unavailable>, access=0x000073126d4797e0) at shared_context_state.cc:798:9
    frame #15: 0x000073116383a529 libgpu_gles2.cr.so`gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM(this=0x00007312fd4992b0) at raster_decoder.cc:3128:30
    frame #16: 0x0000731163839158 libgpu_gles2.cr.so`gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(this=<unavailable>, immediate_data_size=<unavailable>, cmd_data=<unavailable>) at raster_decoder_autogen.h:162:3
    frame #17: 0x000073116383bb68 libgpu_gles2.cr.so`gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(this=0x00007312fd4992b0, num_commands=<unavailable>, buffer=<unavailable>, num_entries=111, entries_processed=0x000073119c0170d0) at raster_decoder.cc:1510:18
    frame #18: 0x0000731166c2bca6 libgpu.cr.so`gpu::CommandBufferService::Flush(this=0x000073127d4ba480, put_offset=<unavailable>, handler=0x00007312fd4992b0) at command_buffer_service.cc:231:35
    frame #19: 0x0000731140cc93c7 libgpu_ipc_service.cr.so`gpu::CommandBufferStub::OnAsyncFlush(this=0x00007312fd49bb50, put_offset=111, flush_id=4, sync_token_fences=<unavailable>) at command_buffer_stub.cc:503:22
    frame #20: 0x0000731140cc8fef libgpu_ipc_service.cr.so`gpu::CommandBufferStub::ExecuteDeferredRequest(this=0x00007312fd49bb50, params=0x000073121d484970) at command_buffer_stub.cc:154:7
    frame #21: 0x0000731140cd3790 libgpu_ipc_service.cr.so`gpu::GpuChannel::ExecuteDeferredRequest(this=0x00007312bd4b9f30, params=gpu::mojom::DeferredRequestParamsPtr @ 0x000073119c017578, release_count=1) at gpu_channel.cc:932:13
    frame #22: 0x0000731140cd732a libgpu_ipc_service.cr.so`void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(method=<unavailable>, receiver_ptr=<unavailable>, args=0x000073125d48a9f0, args=0x000073125d48a9f8) at bind_internal.h:738:12
    frame #23: 0x0000731166c3343d libgpu.cr.so`base::OnceCallback<void ()>::Run(this=0x000073119c017610) && at callback.h:156:12
    frame #24: 0x0000731166c3b544 libgpu.cr.so`gpu::SchedulerDfs::ExecuteSequence(this=0x000073125d487c50, sequence_id=gpu::SequenceId @ 0x000073119c017604) at scheduler_dfs.cc:600:24
    frame #25: 0x0000731166c3aaf7 libgpu.cr.so`gpu::SchedulerDfs::RunNextTask(this=0x000073125d487c50) at scheduler_dfs.cc:524:3
    frame #26: 0x000073118f5177c1 libbase.cr.so`base::OnceCallback<void ()>::Run(this=0x000073135d496378) && at callback.h:156:12
    frame #27: 0x000073118f5a4fce libbase.cr.so`base::TaskAnnotator::RunTaskImpl(this=<unavailable>, pending_task=<unavailable>) at task_annotator.cc:203:34
    frame #28: 0x000073118f5c883a libbase.cr.so`base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) [inlined] void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(this=0x000073130d51d088, event_name=<unavailable>, pending_task=0x000073135d496300, args=0x000073119c017bd0) at task_annotator.h:90:5
    frame #29: 0x000073118f5c8811 libbase.cr.so`base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(this=0x000073130d51cdc0, continuation_lazy_now=0x000073119c017c80) at thread_controller_with_message_pump_impl.cc:484:23
    frame #30: 0x000073118f5c82b1 libbase.cr.so`base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(this=0x000073130d51cdc0) at thread_controller_with_message_pump_impl.cc:346:40
    frame #31: 0x000073118f5c8c22 libbase.cr.so`non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() at thread_controller_with_message_pump_impl.cc:0
    frame #32: 0x000073118f540559 libbase.cr.so`base::MessagePumpDefault::Run(this=<unavailable>, delegate=0x000073130d51cdc0) at message_pump_default.cc:40:55
    frame #33: 0x000073118f5c8f23 libbase.cr.so`base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(this=0x000073130d51cdc0, application_tasks_allowed=true, timeout=<unavailable>) at thread_controller_with_message_pump_impl.cc:654:12
    frame #34: 0x000073118f57bbeb libbase.cr.so`base::RunLoop::Run(this=0x000073119c017f18, location=<unavailable>) at run_loop.cc:134:14
    frame #35: 0x00007310c1e493c7 libcontent.cr.so`content::GpuMain(parameters=<unavailable>) at gpu_main.cc:431:14
    frame #36: 0x00007310c398d4d7 libcontent.cr.so`content::RunOtherNamedProcessTypeMain(process_type="gpu-process", main_function_params=<unavailable>, delegate=<unavailable>) at content_main_runner_impl.cc:798:14
    frame #37: 0x00007310c398e0da libcontent.cr.so`content::ContentMainRunnerImpl::Run(this=0x000073126d472620) at content_main_runner_impl.cc:1175:10
    frame #38: 0x00007310c398bcb0 libcontent.cr.so`content::RunContentProcess(params=ContentMainParams @ 0x000073119c018520, content_main_runner=0x000073126d472620) at content_main.cc:333:36
    frame #39: 0x00007310c398cb67 libcontent.cr.so`::Java_org_jni_1zero_GEN_1JNI_org_1chromium_1content_1app_1ContentMain_1start(JNIEnv *, jclass, jboolean) [inlined] content::JNI_ContentMain_Start(env=<unavailable>, start_minimal_browser='\0') at content_main_android.cc:65:10
    frame #40: 0x00007310c398cae3 libcontent.cr.so`Java_org_jni_1zero_GEN_1JNI_org_1chromium_1content_1app_1ContentMain_1start(env=<unavailable>, jcaller=<unavailable>, startMinimalBrowser='\0') at ContentMain_jni.h:36:15
    frame #41: 0x000073120937d70c libart.so`art_quick_generic_jni_trampoline + 220
    frame #42: 0x0000731209368c96 libart.so`NterpCommonInvokeStatic + 131```

```

### ap...@google.com (2024-08-28)

Project: skia
Branch: main

commit 07fcb9a00233cace0b6cc19ed4bcec6770e0315f
Author: James Godfrey-Kittle <jamesgk@google.com>
Date:   Wed Aug 28 10:48:21 2024

    [ganesh] Avoid int overflow in PatternHelper
    
    The callers of PatternHelper which are not updated here pass in a TArray
    size as repeatCount, which already prevents overflow:
    https://crsrc.org/c/third_party/skia/include/private/base/SkTArray.h?q=kMaxCapacity
    
    Bug: b/361461526
    Change-Id: I86c494cb00223f0bb8d68540d33d7230b60c9486
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/893916
    Reviewed-by: Brian Osman <brianosman@google.com>
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>

M       src/gpu/ganesh/ops/DashOp.cpp
M       src/gpu/ganesh/ops/DrawAtlasOp.cpp
M       src/gpu/ganesh/ops/GrMeshDrawOp.cpp
M       src/gpu/ganesh/ops/LatticeOp.cpp
M       src/gpu/ganesh/ops/RegionOp.cpp

https://skia-review.googlesource.com/893916


### pe...@google.com (2024-08-29)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128, 129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ja...@google.com (2024-08-29)

1. <http://review.skia.org/893916>
2. This fix has been in Canary on Android and Mac since 130.0.6685.0, and doesn't seem to have caused any stability regressions
3. No
4. No
5. No

### am...@chromium.org (2024-08-29)

Thanks -- it looks like the roll just landed into Chromium with this fix yesterday afternoon / less than 24 hours ago; this should probably have at least one more day of bake time just to make sure there are no issues. Will revisit this then, but it may be safer to let this bake until Monday and consider for the next respin instead.

### pg...@google.com (2024-09-03)

This fix has been in Canary for a while, and I do not see any related stability regressions.

Merge approved for M128 - please merge by Thursday September 5th EOD MTV time to get this fix into the next M128 stable respin!  

Merge approved for M129 - please merge at your earliest convenience to get this fix into the next M129 beta release!

### sp...@google.com (2024-09-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $15000.00 for this report.

Rationale for this decision:
high-quality report of memory corruption in a highly privileged process (GPU)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-04)

Congratulations Renan! Thank you for your efforts and reporting this issue to us -- great work!

In assessment, it was determined this report was very high quality but the demonstrated impact was limited to memory corruption in the GPU / highly priviledged process.
Your stack trace added to c#5 did not demonstrate a sandbox escape, nor did it fully demonstrate exploitable memory corruption to the same degree on the Android process. Again, since it was mentioned in follow-up to other reports today, the requirements here are demonstrated memory corruption rather than just a segfault. We understand that is more work to do this rather than demonstrating the issue on desktop and pointing to the transitive impact of an issue on a given platform with a stack trace showing a segfault, but that is why the rewards for that category are so much higher.

### ap...@google.com (2024-09-04)

Project: skia
Branch: chrome/m128

commit 938144dd79c6e3664a3c0bbd019daedddf655ffa
Author: James Godfrey-Kittle <jamesgk@google.com>
Date:   Wed Aug 28 10:48:21 2024

    [ganesh] Avoid int overflow in PatternHelper
    
    The callers of PatternHelper which are not updated here pass in a TArray
    size as repeatCount, which already prevents overflow:
    https://crsrc.org/c/third_party/skia/include/private/base/SkTArray.h?q=kMaxCapacity
    
    Bug: b/361461526
    Change-Id: I86c494cb00223f0bb8d68540d33d7230b60c9486
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/893916
    Reviewed-by: Brian Osman <brianosman@google.com>
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>
    (cherry picked from commit 07fcb9a00233cace0b6cc19ed4bcec6770e0315f)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/896478

M       src/gpu/ganesh/ops/DashOp.cpp
M       src/gpu/ganesh/ops/DrawAtlasOp.cpp
M       src/gpu/ganesh/ops/GrMeshDrawOp.cpp
M       src/gpu/ganesh/ops/LatticeOp.cpp
M       src/gpu/ganesh/ops/RegionOp.cpp

https://skia-review.googlesource.com/896478


### ap...@google.com (2024-09-04)

Project: skia
Branch: chrome/m129

commit 07d7158eeabfa377f46f25f632f900a49b653e18
Author: James Godfrey-Kittle <jamesgk@google.com>
Date:   Wed Aug 28 10:48:21 2024

    [ganesh] Avoid int overflow in PatternHelper
    
    The callers of PatternHelper which are not updated here pass in a TArray
    size as repeatCount, which already prevents overflow:
    https://crsrc.org/c/third_party/skia/include/private/base/SkTArray.h?q=kMaxCapacity
    
    Bug: b/361461526
    Change-Id: I86c494cb00223f0bb8d68540d33d7230b60c9486
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/893916
    Reviewed-by: Brian Osman <brianosman@google.com>
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>
    (cherry picked from commit 07fcb9a00233cace0b6cc19ed4bcec6770e0315f)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/896479

M       src/gpu/ganesh/ops/DashOp.cpp
M       src/gpu/ganesh/ops/DrawAtlasOp.cpp
M       src/gpu/ganesh/ops/GrMeshDrawOp.cpp
M       src/gpu/ganesh/ops/LatticeOp.cpp
M       src/gpu/ganesh/ops/RegionOp.cpp

https://skia-review.googlesource.com/896479


### pe...@google.com (2024-09-04)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ja...@google.com (2024-09-04)

re: [comment #15](https://issues.chromium.org/issues/361461526#comment15)

1. No
2. No

### pe...@google.com (2024-09-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### ja...@google.com (2024-09-12)

1. <http://review.skia.org/898036> for 120
2. Low, only merge conflicts were in includes
3. 128, 129
4. Yes

### ap...@google.com (2024-09-12)

Project: skia
Branch: chrome/m120

commit cbb40e2aee54cd02f36b6f95f7f23a17c41d4728
Author: Gyuyoung Kim <qkim@google.com>
Date:   Thu Sep 12 14:17:34 2024

    [M120-LTS][ganesh] Avoid int overflow in PatternHelper
    
    The callers of PatternHelper which are not updated here pass in a TArray
    size as repeatCount, which already prevents overflow:
    https://crsrc.org/c/third_party/skia/include/private/base/SkTArray.h?q=kMaxCapacity
    
    Bug: b/361461526
    Change-Id: I86c494cb00223f0bb8d68540d33d7230b60c9486
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/893916
    Reviewed-by: Brian Osman <brianosman@google.com>
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>
    (cherry picked from commit 07fcb9a00233cace0b6cc19ed4bcec6770e0315f)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/898036
    Reviewed-by: James Godfrey-Kittle <jamesgk@google.com>

M       src/gpu/ganesh/ops/DashOp.cpp
M       src/gpu/ganesh/ops/DrawAtlasOp.cpp
M       src/gpu/ganesh/ops/GrMeshDrawOp.cpp
M       src/gpu/ganesh/ops/LatticeOp.cpp
M       src/gpu/ganesh/ops/RegionOp.cpp

https://skia-review.googlesource.com/898036


### hy...@gmail.com (2024-09-18)

Hi, thanks!

Proceeding with this bug, this is just another way of reaching the previous bug via a different overflow when repeating the geometry via `PatternHelper`, [crbug.com/360758697](https://crbug.com/360758697) was changed to a 'baseline report of memory corruption in a non sandboxed process', would the VRP mind changing this as well since Android is also affected?

Just like the previous bug, we are overflowing the vertex space (the allocation), and since an attacker has control over the complexity of each region, it's also possible to manipulate the overflow to make the allocation fall into a predictable memory layout, which also makes it doable to manipulate the write to happen in controlled memory.

The bug ends up in a wild copy when writing rectangles (composed of four 32bit attacker controlled floats) of all previously combined regions to the overflowed space in `VertexWriter::operator<<` [1], which eventually ends up hitting unmapped memory in the previous android stacktrace as more rectangles are copied, however, wild copy exploitation is not unrealistic [2][3][4] and modern browsers are multi threaded applications by nature, so there are multiple potential ways to exploit it.

```
template <typename T>
inline VertexWriter& operator<<(VertexWriter& w, const T& val) {
    static_assert(std::is_trivially_copyable<T>::value, "");
    w.validate(sizeof(T));
    memcpy(w.fPtr, &val, sizeof(T)); // <-- [1]
    w = w.makeOffset(sizeof(T));
    return w;
}

```

Note that `w.validate(sizeof(T))` calls are not really doing anything in release builds since checks are behind a SkASSERT:

```
void validate(size_t bytesToWrite) const {
    // If the buffer writer had an end marked, make sure we're not crossing it.
    // Ideally, all creators of BufferWriters mark the end, but a lot of legacy code is not set
    // up to easily do this.
    SkASSERT(fPtr || bytesToWrite == 0);
    SkASSERT(!fEnd || Mark(fPtr, bytesToWrite) <= fEnd);
}

```

Thanks.

Reference:

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/BufferWriter.h;l=280?q=BufferWriter.h:280&ss=chromium>

[2] <https://googleprojectzero.blogspot.com/2015/03/taming-wild-copy-parallel-thread.html>

[3] <https://blog.ret2.io/2022/05/19/pwn2own-2021-parallels-desktop-exploit/>

[4] <https://saaramar.github.io/IOMFB_integer_overflow_poc/#wildcopy-exploitation>

---

Android ARM ASAN stacktrace from logcat:

```
09-18 04:39:52.264 32307 32307 I wrap.sh : =================================================================
09-18 04:39:52.264 32307 32307 I wrap.sh : ==32308==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x007eb99c9820 at pc 0x005dad1012bc bp 0x005dc586e540 sp 0x005dc586e538
09-18 04:39:52.265 32307 32307 I wrap.sh : WRITE of size 4 at 0x007eb99c9820 thread T16 (CrGpuMain)
I 04:39:51.941  183.066s Main  Running: /home/hyhy100/chromium/src/third_party/android_platform/development/scripts/stack.py --output-directory /home/hyhy100/chromium/src/out/android-arm64-static --apks-directory /tmp/tmpchxy0qp6 --quiet /tmp/tmpthvgxg_g
09-18 04:39:52.308 32307 32307 I wrap.sh : 
09-18 04:39:52.308 32307 32307 I wrap.sh : Stack Trace:
09-18 04:39:52.308 32307 32307 I wrap.sh :   RELADDR   FUNCTION                                                                          FILE:LINE
09-18 04:39:52.309 32307 32307 I wrap.sh :   v------>  skgpu::VertexWriter& skgpu::operator<<<float>(skgpu::VertexWriter&, float const&)  ../../third_party/skia/src/gpu/BufferWriter.h:280:5
09-18 04:39:52.309 32307 32307 I wrap.sh :   24b692b8  skgpu::VertexWriter::TriStrip<float>::writeVertex(int, skgpu::VertexWriter&) const  ../../third_party/skia/src/gpu/BufferWriter.h:208:32
09-18 04:39:52.309 32307 32307 I wrap.sh :   v------>  std::__Cr::enable_if<is_quad<skgpu::VertexWriter::TriStrip<float>>::value, void>::type skgpu::VertexWriter::writeQuadVertex<1, skgpu::VertexWriter::TriStrip<float>, skgpu::VertexColor>(skgpu::VertexWriter::TriStrip<float> const&, skgpu::VertexColor const&)  ../../third_party/skia/src/gpu/BufferWriter.h:262:14
09-18 04:39:52.309 32307 32307 I wrap.sh :   v------>  void skgpu::VertexWriter::writeQuad<skgpu::VertexWriter::TriStrip<float>, skgpu::VertexColor>(skgpu::VertexWriter::TriStrip<float> const&, skgpu::VertexColor const&)  ../../third_party/skia/src/gpu/BufferWriter.h:246:15
09-18 04:39:52.309 32307 32307 I wrap.sh :   24bea230  skgpu::ganesh::RegionOp::(anonymous namespace)::RegionOpImpl::onPrepareDraws(GrMeshDrawTarget*)  ../../third_party/skia/src/gpu/ganesh/ops/RegionOp.cpp:142:26
09-18 04:39:52.309 32307 32307 I wrap.sh :   24bcba70  GrOp::prepare(GrOpFlushState*)                                                    ../../third_party/skia/src/gpu/ganesh/ops/GrOp.h:187:15
09-18 04:39:52.309 32307 32307 I wrap.sh :   24bcafb8  skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*)                                ../../third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:531:27
09-18 04:39:52.309 32307 32307 I wrap.sh :   249f40a0  GrRenderTask::prepare(GrOpFlushState*)                                            ../../third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
09-18 04:39:52.310 32307 32307 I wrap.sh :   2499ac30  GrDrawingManager::executeRenderTasks(GrOpFlushState*)                             ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:260:21
09-18 04:39:52.310 32307 32307 I wrap.sh :   24998d70  GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:203:34
09-18 04:39:52.310 32307 32307 I wrap.sh :   2499c8bc  GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:530:27
09-18 04:39:52.310 32307 32307 I wrap.sh :   2498af88  GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:92:47
09-18 04:39:52.310 32307 32307 I wrap.sh :   v------>  GrDirectContextPriv::flushSurface(GrSurfaceProxy*, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
09-18 04:39:52.310 32307 32307 I wrap.sh :   24983f98  GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:516:25
09-18 04:39:52.310 32307 32307 I wrap.sh :   24c22468  skgpu::ganesh::Flush(SkSurface*)                                                  ../../third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:782:45
09-18 04:39:52.310 32307 32307 I wrap.sh :   2a1cfad0  gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*)  ../../gpu/command_buffer/service/shared_context_state.cc:798:9
09-18 04:39:52.311 32307 32307 I wrap.sh :   2a184c78  gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM()                             ../../gpu/command_buffer/service/raster_decoder.cc:3128:30
09-18 04:39:52.311 32307 32307 I wrap.sh :   2a17f3ec  gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*)  ../../gpu/command_buffer/service/raster_decoder_autogen.h:162:3
09-18 04:39:52.311 32307 32307 I wrap.sh :   2a18e4ac  gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)  ../../gpu/command_buffer/service/raster_decoder.cc:1510:18
09-18 04:39:52.311 32307 32307 I wrap.sh :   2829ff40  gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)                    ../../gpu/command_buffer/service/command_buffer_service.cc:231:35
09-18 04:39:52.311 32307 32307 I wrap.sh :   2a467404  gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)  ../../gpu/ipc/service/command_buffer_stub.cc:503:22
09-18 04:39:52.311 32307 32307 I wrap.sh :   2a4662c8  gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&)  ../../gpu/ipc/service/command_buffer_stub.cc:154:7
09-18 04:39:52.311 32307 32307 I wrap.sh :   2a47ecd0  gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long)  ../../gpu/ipc/service/gpu_channel.cc:932:13
09-18 04:39:52.312 32307 32307 I wrap.sh :   v------>  void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&)  ../../base/functional/bind_internal.h:738:12
09-18 04:39:52.312 32307 32307 I wrap.sh :   2a48bfa8  void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, void, 0ul, 1ul, 2ul>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>&&)  ../../base/functional/bind_internal.h:954:5
09-18 04:39:52.312 32307 32307 I wrap.sh :   v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0ul, 1ul, 2ul>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>)  ../../base/functional/bind_internal.h:1067:14
09-18 04:39:52.312 32307 32307 I wrap.sh :   2a48bd8c  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:980:12
09-18 04:39:52.312 32307 32307 I wrap.sh :   138d1804  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:156:12
09-18 04:39:52.312 32307 32307 I wrap.sh :   282cf2dc  gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)  ../../gpu/command_buffer/service/scheduler_dfs.cc:600:24
09-18 04:39:52.312 32307 32307 I wrap.sh :   282cd2d0  gpu::SchedulerDfs::RunNextTask()                                                  ../../gpu/command_buffer/service/scheduler_dfs.cc:524:3
09-18 04:39:52.312 32307 32307 I wrap.sh :   v------>  void base::internal::DecayedFunctorTraits<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs*>::Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs*>(void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs*&&)  ../../base/functional/bind_internal.h:738:12
09-18 04:39:52.312 32307 32307 I wrap.sh :   v------>  void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, void, 0ul>::MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>>(void (gpu::SchedulerDfs::*&&)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&)  ../../base/functional/bind_internal.h:930:12
09-18 04:39:52.313 32307 32307 I wrap.sh :   v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(void (gpu::SchedulerDfs::*&&)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)  ../../base/functional/bind_internal.h:1067:14
09-18 04:39:52.313 32307 32307 I wrap.sh :   282d0af8  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:980:12
09-18 04:39:52.313 32307 32307 I wrap.sh :   138d1804  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:156:12
09-18 04:39:52.313 32307 32307 I wrap.sh :   22f457cc  base::TaskAnnotator::RunTaskImpl(base::PendingTask&)                              ../../base/task/common/task_annotator.cc:203:34
09-18 04:39:52.313 32307 32307 I wrap.sh :   v------>  void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&)  ../../base/task/common/task_annotator.h:90:5
09-18 04:39:52.313 32307 32307 I wrap.sh :   22fc3acc  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
09-18 04:39:52.313 32307 32307 I wrap.sh :   22fc28bc  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()   ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
09-18 04:39:52.313 32307 32307 I wrap.sh :   22e49990  base::MessagePumpDefault::Run(base::MessagePump::Delegate*)                       ../../base/message_loop/message_pump_default.cc:40:55
09-18 04:39:52.313 32307 32307 I wrap.sh :   22fc5930  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
09-18 04:39:52.313 32307 32307 I wrap.sh :   22ee07ec  base::RunLoop::Run(base::Location const&)                                         ../../base/run_loop.cc:134:14
09-18 04:39:52.313 32307 32307 I wrap.sh :   350715dc  content::GpuMain(content::MainFunctionParams)                                     ../../content/gpu/gpu_main.cc:431:14
09-18 04:39:52.313 32307 32307 I wrap.sh :   22006d70  content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)  ../../content/app/content_main_runner_impl.cc:798:14
09-18 04:39:52.313 32307 32307 I wrap.sh :   22008be0  content::ContentMainRunnerImpl::Run()                                             ../../content/app/content_main_runner_impl.cc:1175:10
09-18 04:39:52.313 32307 32307 I wrap.sh :   22003080  content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)  ../../content/app/content_main.cc:333:36
09-18 04:39:52.313 32307 32307 I wrap.sh :   v------>  content::JNI_ContentMain_Start(_JNIEnv*, unsigned char)                           ../../content/app/android/content_main_android.cc:65:10
09-18 04:39:52.313 32307 32307 I wrap.sh :   22005798  Java_org_1chromium_1content_1app_1ContentMain_1start                              gen/jni_headers/content/public/android/content_app_jni/ContentMain_jni.h:36:15
09-18 04:39:52.313 32307 32307 I wrap.sh : : 
09-18 04:39:52.313 32307 32307 I wrap.sh : 0x007eb99c9820 is located 0 bytes after 65568-byte region [0x007eb99b9800,0x007eb99c9820)
09-18 04:39:52.313 32307 32307 I wrap.sh : allocated by thread T16 (CrGpuMain) here:
I 04:39:54.879  186.005s Main  Running: /home/hyhy100/chromium/src/third_party/android_platform/development/scripts/stack.py --output-directory /home/hyhy100/chromium/src/out/android-arm64-static --apks-directory /tmp/tmpchxy0qp6 --quiet /tmp/tmpijtuae3h
09-18 04:39:52.313 32307 32307 I wrap.sh : 
09-18 04:39:52.314 32307 32307 I wrap.sh : Stack Trace:
09-18 04:39:52.314 32307 32307 I wrap.sh :   RELADDR   FUNCTION                                                                          FILE:LINE
09-18 04:39:52.314 32307 32307 I wrap.sh :   v------>  GrCpuBuffer::Make(unsigned long)                                                  ../../third_party/skia/src/gpu/ganesh/GrCpuBuffer.h:29:20
09-18 04:39:52.314 32307 32307 I wrap.sh :   24962ff0  GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned long, bool)                ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:56:30
09-18 04:39:52.314 32307 32307 I wrap.sh :   24964afc  GrBufferAllocPool::resetCpuData(unsigned long)                                    ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:389:60
09-18 04:39:52.314 32307 32307 I wrap.sh :   24966530  GrBufferAllocPool::createBlock(unsigned long)                                     ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:362:15
09-18 04:39:52.314 32307 32307 I wrap.sh :   24965a10  GrBufferAllocPool::makeSpace(unsigned long, unsigned long, sk_sp<GrBuffer const>*, unsigned long*)  ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:229:16
09-18 04:39:52.314 32307 32307 I wrap.sh :   24967b68  GrVertexBufferAllocPool::makeSpace(unsigned long, int, sk_sp<GrBuffer const>*, int*)  ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:445:28
09-18 04:39:52.315 32307 32307 I wrap.sh :   24b96ff8  GrMeshDrawOp::PatternHelper::init(GrMeshDrawTarget*, GrPrimitiveType, unsigned long, sk_sp<GrBuffer const>, int, int, int, int)  ../../third_party/skia/src/gpu/ganesh/ops/GrMeshDrawOp.cpp:87:25
09-18 04:39:52.315 32307 32307 I wrap.sh :   24b9738c  GrMeshDrawOp::QuadHelper::QuadHelper(GrMeshDrawTarget*, unsigned long, int)       ../../third_party/skia/src/gpu/ganesh/ops/GrMeshDrawOp.cpp:125:11
09-18 04:39:52.315 32307 32307 I wrap.sh :   24bea0b8  skgpu::ganesh::RegionOp::(anonymous namespace)::RegionOpImpl::onPrepareDraws(GrMeshDrawTarget*)  ../../third_party/skia/src/gpu/ganesh/ops/RegionOp.cpp:129:20
09-18 04:39:52.315 32307 32307 I wrap.sh :   24bcba70  GrOp::prepare(GrOpFlushState*)                                                    ../../third_party/skia/src/gpu/ganesh/ops/GrOp.h:187:15
09-18 04:39:52.315 32307 32307 I wrap.sh :   24bcafb8  skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*)                                ../../third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:531:27
09-18 04:39:52.315 32307 32307 I wrap.sh :   249f40a0  GrRenderTask::prepare(GrOpFlushState*)                                            ../../third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
09-18 04:39:52.315 32307 32307 I wrap.sh :   2499ac30  GrDrawingManager::executeRenderTasks(GrOpFlushState*)                             ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:260:21
09-18 04:39:52.315 32307 32307 I wrap.sh :   24998d70  GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:203:34
09-18 04:39:52.315 32307 32307 I wrap.sh :   2499c8bc  GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:530:27
09-18 04:39:52.316 32307 32307 I wrap.sh :   2498af88  GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:92:47
09-18 04:39:52.316 32307 32307 I wrap.sh :   v------>  GrDirectContextPriv::flushSurface(GrSurfaceProxy*, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
09-18 04:39:52.316 32307 32307 I wrap.sh :   24983f98  GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:516:25
09-18 04:39:52.316 32307 32307 I wrap.sh :   24c22468  skgpu::ganesh::Flush(SkSurface*)                                                  ../../third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:782:45
09-18 04:39:52.316 32307 32307 I wrap.sh :   2a1cfad0  gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*)  ../../gpu/command_buffer/service/shared_context_state.cc:798:9
09-18 04:39:52.316 32307 32307 I wrap.sh :   2a184c78  gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM()                             ../../gpu/command_buffer/service/raster_decoder.cc:3128:30
09-18 04:39:52.316 32307 32307 I wrap.sh :   2a17f3ec  gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*)  ../../gpu/command_buffer/service/raster_decoder_autogen.h:162:3
09-18 04:39:52.316 32307 32307 I wrap.sh :   2a18e4ac  gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)  ../../gpu/command_buffer/service/raster_decoder.cc:1510:18
09-18 04:39:52.316 32307 32307 I wrap.sh :   2829ff40  gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)                    ../../gpu/command_buffer/service/command_buffer_service.cc:231:35
09-18 04:39:52.316 32307 32307 I wrap.sh :   2a467404  gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)  ../../gpu/ipc/service/command_buffer_stub.cc:503:22
09-18 04:39:52.316 32307 32307 I wrap.sh :   2a4662c8  gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&)  ../../gpu/ipc/service/command_buffer_stub.cc:154:7
09-18 04:39:52.316 32307 32307 I wrap.sh :   2a47ecd0  gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long)  ../../gpu/ipc/service/gpu_channel.cc:932:13
09-18 04:39:52.316 32307 32307 I wrap.sh :   v------>  void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&)  ../../base/functional/bind_internal.h:738:12
09-18 04:39:52.316 32307 32307 I wrap.sh :   2a48bfa8  void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, void, 0ul, 1ul, 2ul>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>&&)  ../../base/functional/bind_internal.h:954:5
09-18 04:39:52.316 32307 32307 I wrap.sh :   v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0ul, 1ul, 2ul>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>)  ../../base/functional/bind_internal.h:1067:14
09-18 04:39:52.316 32307 32307 I wrap.sh :   2a48bd8c  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:980:12
09-18 04:39:52.316 32307 32307 I wrap.sh :   138d1804  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:156:12
09-18 04:39:52.316 32307 32307 I wrap.sh :   282cf2dc  gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)  ../../gpu/command_buffer/service/scheduler_dfs.cc:600:24
09-18 04:39:52.317 32307 32307 I wrap.sh : : 
09-18 04:39:52.317 32307 32307 I wrap.sh : Thread T16 (CrGpuMain) created by T0 (ileged_process3) here:
I 04:39:57.816  188.942s Main  Running: /home/hyhy100/chromium/src/third_party/android_platform/development/scripts/stack.py --output-directory /home/hyhy100/chromium/src/out/android-arm64-static --apks-directory /tmp/tmpchxy0qp6 --quiet /tmp/tmp8ekyvsmo
09-18 04:39:52.344 32307 32307 I wrap.sh : : 
09-18 04:39:52.344 32307 32307 I wrap.sh : SUMMARY: AddressSanitizer: heap-buffer-overflow (/data/app/~~bizbQQyWZVOUoyJ0gR-EoA==/org.chromium.chrome-R8eUu0gfp78N-oEzXQYU2Q==/lib/arm64/libchrome.so+0x24b692b8) (BuildId: 76ac9af45a50a079) 
09-18 04:39:52.345 32307 32307 I wrap.sh : Shadow bytes around the buggy address:
09-18 04:39:52.345 32307 32307 I wrap.sh :   0x007eb99c9580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-18 04:39:52.345 32307 32307 I wrap.sh :   0x007eb99c9600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-18 04:39:52.345 32307 32307 I wrap.sh :   0x007eb99c9680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-18 04:39:52.345 32307 32307 I wrap.sh :   0x007eb99c9700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-18 04:39:52.345 32307 32307 I wrap.sh :   0x007eb99c9780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-18 04:39:52.345 32307 32307 I wrap.sh : =>0x007eb99c9800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
09-18 04:39:52.345 32307 32307 I wrap.sh :   0x007eb99c9880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-18 04:39:52.345 32307 32307 I wrap.sh :   0x007eb99c9900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-18 04:39:52.345 32307 32307 I wrap.sh :   0x007eb99c9980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-18 04:39:52.345 32307 32307 I wrap.sh :   0x007eb99c9a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-18 04:39:52.345 32307 32307 I wrap.sh :   0x007eb99c9a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-18 04:39:52.345 32307 32307 I wrap.sh : Shadow byte legend (one shadow byte represents 8 application bytes):
09-18 04:39:52.346 32307 32307 I wrap.sh :   Addressable:           00
09-18 04:39:52.346 32307 32307 I wrap.sh :   Partially addressable: 01 02 03 04 05 06 07 
09-18 04:39:52.346 32307 32307 I wrap.sh :   Heap left redzone:       fa
09-18 04:39:52.346 32307 32307 I wrap.sh :   Freed heap region:       fd
09-18 04:39:52.346 32307 32307 I wrap.sh :   Stack left redzone:      f1
09-18 04:39:52.346 32307 32307 I wrap.sh :   Stack mid redzone:       f2
09-18 04:39:52.346 32307 32307 I wrap.sh :   Stack right redzone:     f3
09-18 04:39:52.346 32307 32307 I wrap.sh :   Stack after return:      f5
09-18 04:39:52.346 32307 32307 I wrap.sh :   Stack use after scope:   f8
09-18 04:39:52.346 32307 32307 I wrap.sh :   Global redzone:          f9
09-18 04:39:52.346 32307 32307 I wrap.sh :   Global init order:       f6
09-18 04:39:52.346 32307 32307 I wrap.sh :   Poisoned by user:        f7
09-18 04:39:52.346 32307 32307 I wrap.sh :   Container overflow:      fc
09-18 04:39:52.346 32307 32307 I wrap.sh :   Array cookie:            ac
09-18 04:39:52.346 32307 32307 I wrap.sh :   Intra object redzone:    bb
09-18 04:39:52.347  4159  4285 E Netd    : getNetworkForDns: getNetId from enterpriseCtrl is netid 0
09-18 04:39:52.347 32307 32307 I wrap.sh :   ASan internal:           fe
09-18 04:39:52.350 32307 32307 I wrap.sh :   Left alloca redzone:     ca
09-18 04:39:52.350 32307 32307 I wrap.sh :   Right alloca redzone:    cb
09-18 04:39:52.350 32307 32307 I wrap.sh : : 
09-18 04:39:52.350 32307 32307 I wrap.sh : ==32308==ADDITIONAL INFO
09-18 04:39:52.350 32307 32307 I wrap.sh : : 
09-18 04:39:52.350 32307 32307 I wrap.sh : ==32308==Note: Please include this section with the ASan report.
09-18 04:39:52.350 32307 32307 I wrap.sh : Task trace:
I 04:39:57.868  188.994s Main  Running: /home/hyhy100/chromium/src/third_party/android_platform/development/scripts/stack.py --output-directory /home/hyhy100/chromium/src/out/android-arm64-static --apks-directory /tmp/tmpchxy0qp6 --quiet /tmp/tmph61w72pz
09-18 04:39:52.350 32307 32307 I wrap.sh : 
09-18 04:39:52.350 32307 32307 I wrap.sh : Stack Trace:
09-18 04:39:52.350 32307 32307 I wrap.sh :   RELADDR   FUNCTION                                                                          FILE:LINE
09-18 04:39:52.350 32307 32307 I wrap.sh :   282cd644  gpu::SchedulerDfs::RunNextTask()                                                  ../../gpu/command_buffer/service/scheduler_dfs.cc:540:27
09-18 04:39:52.350 32307 32307 I wrap.sh :   282c828c  gpu::SchedulerDfs::TryScheduleSequence(gpu::SchedulerDfs::Sequence*)              ../../gpu/command_buffer/service/scheduler_dfs.cc:342:11
09-18 04:39:52.350 32307 32307 I wrap.sh :   23a4310c  mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)  ../../mojo/public/cpp/system/simple_watcher.cc:102:13
09-18 04:39:52.350 32307 32307 I wrap.sh : : 
09-18 04:39:52.350 32307 32307 I wrap.sh : : 
09-18 04:39:52.350 32307 32307 I wrap.sh : Command line: ` --type=gpu-process --enable-crash-reporter=,unknown --no-subproc-heap-profiling --gpu-preferences=UAAAAAAAAAAgAIAMAAAAAAAAAAAAAAAAAABgAAIAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=5,i,13654182554807572241,13573772251302674701,262144 --field-trial-handle=3,i,8799412926759861892,8198567582605599966,262144 --variations-seed-version --host-package-name=org.chromium.chrome --package-name=org.chromium.chrome --host-package-label=Chromium --host-version-code=661700004 --package-version-name=129.0.6617.0 --mojo-platform-channel-handle=binder:0 --enable-dom-distiller`
09-18 04:39:52.350 32307 32307 I wrap.sh : : 
09-18 04:39:52.350 32307 32307 I wrap.sh : : 
09-18 04:39:52.350 32307 32307 I wrap.sh : ==32308==END OF ADDITIONAL INFO
09-18 04:39:52.350 32307 32307 I wrap.sh : ==32308==ABORTING

```

### am...@chromium.org (2024-09-19)

Hello Renan, thank you for reaching out with this updated information; however, as was conveyed in the other similar issues, such information should be provided in the original report or before fix and VRP reward decision.
While I understand this report was submitted before the new reward structure was launched, the VRP reward judgement was made on 4 September, a week after that. This information coming in two weeks after that and three weeks after the bug was fixed is a bit far outside of the timeline expectations for report components for resolution and reward decision. As such we cannot consider a change in reward amount for additional information provided at this time since.

### hy...@gmail.com (2024-09-19)

No problem! Thanks!

### ap...@google.com (2024-11-19)

Project: skia  

Branch: chrome/m126  

Author: Gyuyoung Kim <[qkim@google.com](mailto:qkim@google.com)>  

Link:      <https://skia-review.googlesource.com/913076>

[M126-LTS][ganesh] Avoid int overflow in PatternHelper

---


Expand for full commit details
```
[M126-LTS][ganesh] Avoid int overflow in PatternHelper 
 
The callers of PatternHelper which are not updated here pass in a TArray 
size as repeatCount, which already prevents overflow: 
https://crsrc.org/c/third_party/skia/include/private/base/SkTArray.h?q=kMaxCapacity 
 
Bug: b/361461526 
Change-Id: I86c494cb00223f0bb8d68540d33d7230b60c9486 
Commit-Queue: James Godfrey-Kittle <jamesgk@google.com> 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/898036 
(cherry picked from commit cbb40e2aee54cd02f36b6f95f7f23a17c41d4728) 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/913076 
Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
Reviewed-by: James Godfrey-Kittle <jamesgk@google.com>

```

---

Files:

- M `src/gpu/ganesh/ops/DashOp.cpp`
- M `src/gpu/ganesh/ops/DrawAtlasOp.cpp`
- M `src/gpu/ganesh/ops/GrMeshDrawOp.cpp`
- M `src/gpu/ganesh/ops/LatticeOp.cpp`
- M `src/gpu/ganesh/ops/RegionOp.cpp`

---

Hash: 2d8b452f1f6d6cc55e59da0910012fdd5d21fab6  

Date:  Thu Sep 12 14:17:34 2024


---

### pe...@google.com (2024-12-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/361461526)*
