# Integer overflow in Skia RegionOpImpl::onPrepareDraws leads to OOB write

| Field | Value |
|-------|-------|
| **Issue ID** | [360758697](https://issues.chromium.org/issues/360758697) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 129.0.6661.0 |
| **Reporter** | hy...@gmail.com |
| **Assignee** | ja...@google.com |
| **Created** | 2024-08-19 |
| **Bounty** | $15,000.00 |

## Description

# Steps to reproduce the problem

(Chromium)

1. Apply the `chromium.diff` renderer patch to chromium.
2. Run `genskpic.py` to generate `drawable_picture.skp.hh`, then move the generated file to `src/gpu/command_buffer/client`.
3. Build and start the browser.
4. Open `index.html` to trigger PoC.
5. GPU process will crash.

(Skia standalone)

1. Run `genskpic.py` to generate a `.skp` file.
2. You can now run it in skpbench using: `./out/asan/skpbench --src pic.skp --config gles`.
3. UBSAN crash will happen.

# Problem Description

In Skia Ganesh, when drawing a Skia Picture with a `DRAW_REGION` operation, a `RegionOpImpl` operation object will be created if anti-aliasing is disabled or not needed.

Each `DRAW_REGION` operation is serialized together with a `SkRegion`, and each `SkRegion` can take thousands of "intervals" where each "interval" is a subrectangle within the region.

If many `DRAW_REGION` operations are drawn on the same canvas, `RegionOpImpl::onCombineIfPossible` will be called to test how many `RegionOp` operation objects can be merged into a single one, and will merge region information of both operations if the test succeeds [1], this function is really small and does not make any relevant checks before combining operations:

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/ops/RegionOp.cpp;l=189?q=RegionOp&ss=chromium%2Fchromium%2Fsrc>

```
    CombineResult onCombineIfPossible(GrOp* t, SkArenaAlloc*, const GrCaps& caps) override {
        auto that = t->cast<RegionOpImpl>();
        if (!fHelper.isCompatible(that->fHelper, caps, this->bounds(), that->bounds())) {
            return CombineResult::kCannotCombine;
        }

        if (fViewMatrix != that->fViewMatrix) {
            return CombineResult::kCannotCombine;
        }

        fRegions.push_back_n(that->fRegions.size(), that->fRegions.begin()); // <-- [1]
        fWideColor |= that->fWideColor;
        return CombineResult::kMerged;
    }

```

Then, `RegionOpImpl::onPrepareDraws` will be called to sum the "complexity" of each region [2] in order to calculate how many rectangles are needed to draw all the combined regions:

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/ops/RegionOp.cpp;l=150?q=RegionOp&ss=chromium%2Fchromium%2Fsrc>

```
    void onPrepareDraws(GrMeshDrawTarget* target) override {
        ...

        int numRegions = fRegions.size();
        int numRects = 0;
        for (int i = 0; i < numRegions; i++) {
            numRects += fRegions[i].fRegion.computeRegionComplexity(); // <-- [2]
        }

        ...
    }

```

However, the complexity of each region can be given by how many `intervals` (subrectangles) they have [3] (which is `80000` per region in PoC):

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/core/SkRegion.cpp;l=176?q=computeRegionComplexity&ss=chromium%2Fchromium%2Fsrc>

```
int SkRegion::computeRegionComplexity() const {
  if (this->isEmpty()) {
    return 0;
  } else if (this->isRect()) {
    return 1;
  }
  return fRunHead->getIntervalCount(); // <-- [3]
}

```

Looking back to the previous for [2] in `RegionOpImpl::onPrepareDraws`, we can clearly see that, by previously combining many `DRAW_REGION` operations, `numRects` will eventually overflow.

Later, the function will try to **pre-allocate** enough vertices [4] [5] for all rectangles using the overflowed `numRects`, and will try to write a quad for each invidual region [6] to the vertex buffer, which ends up in an OOB write.

```
    void onPrepareDraws(GrMeshDrawTarget* target) override {
        ...

        QuadHelper helper(target, fProgramInfo->geomProc().vertexStride(), numRects); // <-- [4]

        VertexWriter vertices{helper.vertices()}; // <-- [5]
        if (!vertices) {
            SkDebugf("Could not allocate vertices\n");
            return;
        }

        for (int i = 0; i < numRegions; i++) {
            VertexColor color(fRegions[i].fColor, fWideColor);
            SkRegion::Iterator iter(fRegions[i].fRegion);
            while (!iter.done()) {
                SkRect rect = SkRect::Make(iter.rect());
                vertices.writeQuad(VertexWriter::TriStripFromRect(rect), color); // <-- [6]
                iter.next();
            }
        }

        fMesh = helper.mesh();
    }

```
# Summary

Integer overflow in Skia RegionOpImpl::onPrepareDraws leads to OOB write

# Custom Questions

#### Type of crash:

gpu

#### Crash state:

=================================================================
==126174==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f5282001820 at pc 0x7f530a855493 bp 0x7ffca376c130 sp 0x7ffca376c128
WRITE of size 4 at 0x7f5282001820 thread T0 (chrome)
==126174==WARNING: invalid path to external symbolizer!
==126174==WARNING: Failed to use and restart external symbolizer!
#0 0x7f530a855492 in operator<<<float> ./../../third\_party/skia/src/gpu/BufferWriter.h:280:5
#1 0x7f530a855492 in writeVertex ./../../third\_party/skia/src/gpu/BufferWriter.h:0:0
#2 0x7f530a855492 in writeQuadVertex<1, skgpu::VertexWriter::TriStrip<float>, skgpu::VertexColor> ./../../third\_party/skia/src/gpu/BufferWriter.h:262:14
#3 0x7f530a855492 in writeQuad<skgpu::VertexWriter::TriStrip<float>, skgpu::VertexColor> ./../../third\_party/skia/src/gpu/BufferWriter.h:246:15
#4 0x7f530a855492 in skgpu::ganesh::RegionOp::(anonymous namespace)::RegionOpImpl::onPrepareDraws(GrMeshDrawTarget\*) ./../../third\_party/skia/src/gpu/ganesh/ops/RegionOp.cpp:170:26
#5 0x7f530a830ac0 in GrOp::prepare(GrOpFlushState\*) ./../../third\_party/skia/src/gpu/ganesh/ops/GrOp.h:197:15
#6 0x7f530a83033c in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState\*) ./../../third\_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
#7 0x7f530a6378d9 in GrRenderTask::prepare(GrOpFlushState\*) ./../../third\_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
#8 0x7f530a5dbe50 in GrDrawingManager::executeRenderTasks(GrOpFlushState\*) ./../../third\_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:260:21
#9 0x7f530a5da829 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy\*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const\*) ./../../third\_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:203:34
#10 0x7f530a5dcf7c in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy\*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const\*) ./../../third\_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:530:27
#11 0x7f52d4990394 in flushAndSubmit ./../../third\_party/skia/include/gpu/GrDirectContext.h:333:15
#12 0x7f52d4990394 in gpu::SharedContextState::FlushAndSubmit(bool) ./../../gpu/command\_buffer/service/shared\_context\_state.cc:764:19
#13 0x7f52d494188c in DoFinish ./../../gpu/command\_buffer/service/raster\_decoder.cc:1846:26
#14 0x7f52d494188c in gpu::raster::RasterDecoderImpl::HandleFinish(unsigned int, void const volatile\*) ./../../gpu/command\_buffer/service/raster\_decoder\_autogen.h:22:3
#15 0x7f52d494e321 in gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile\*, int, int\*) ./../../gpu/command\_buffer/service/raster\_decoder.cc:1539:18
#16 0x7f52ff0d3826 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface\*) ./../../gpu/command\_buffer/service/command\_buffer\_service.cc:231:35
#17 0x7f52d6b28e5c in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::\_\_Cr::vector<gpu::SyncToken, std::\_\_Cr::allocator[gpu::SyncToken](javascript:void(0);)> const&) ./../../gpu/ipc/service/command\_buffer\_stub.cc:502:22
#18 0x7f52d6b28101 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command\_buffer\_stub.cc:153:7
#19 0x7f52d6b48655 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long) ./../../gpu/ipc/service/gpu\_channel.cc:932:13
#20 0x7f52d6b56e8e in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), base::WeakPtr[gpu::GpuChannel](javascript:void(0);)&&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), base::WeakPtr[gpu::GpuChannel](javascript:void(0);) const&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), base::WeakPtr[gpu::GpuChannel](javascript:void(0);) const&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&, unsigned long&&) ./../../base/functional/bind\_internal.h:738:12
#21 0x7f52d6b56c74 in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), std::\_\_Cr::tuple<base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long> > ./../../base/functional/bind\_internal.h:954:5
#22 0x7f52d6b56c74 in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), std::\_\_Cr::tuple<base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long>, 0UL, 1UL, 2UL> ./../../base/functional/bind\_internal.h:1067:14
#23 0x7f52d6b56c74 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), base::WeakPtr[gpu::GpuChannel](javascript:void(0);)&&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind\_internal.h:980:12
#24 0x7f52ff11076e in Run ./../../base/functional/callback.h:156:12
#25 0x7f52ff11076e in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) ./../../gpu/command\_buffer/service/scheduler\_dfs.cc:598:24
#26 0x7f52ff10e155 in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command\_buffer/service/scheduler\_dfs.cc:522:3
#27 0x7f52ff111f40 in Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs *> ./../../base/functional/bind\_internal.h:738:12
#28 0x7f52ff111f40 in MakeItSo<void (gpu::SchedulerDfs::*)(), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind\_internal.h:930:12
#29 0x7f52ff111f40 in RunImpl<void (gpu::SchedulerDfs::*)(), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind\_internal.h:1067:14
#30 0x7f52ff111f40 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind\_internal.h:980:12
#31 0x7f530e3bee6a in Run ./../../base/functional/callback.h:156:12
#32 0x7f530e3bee6a in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:203:34
#33 0x7f530e430793 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:11)> ./../../base/task/common/task\_annotator.h:90:5
#34 0x7f530e430793 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:484:23
#35 0x7f530e42f69e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:346:40
#36 0x7f530e4314b4 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0
#37 0x7f530e5c2411 in base::MessagePumpGlib::HandleDispatch() ./../../base/message\_loop/message\_pump\_glib.cc:649:46
#38 0x7f530e5c5472 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (*)(void*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:274:43
#39 0x7f52b531bd3a in g\_main\_context\_dispatch ??:0:0

0x7f5282001820 is located 0 bytes after 4194336-byte region [0x7f5281c01800,0x7f5282001820)
allocated by thread T0 (chrome) here:
#0 0x653362ca40bd in operator new(unsigned long) *asan\_rtl*:3
#1 0x7f530a59bc9d in Make ./../../third\_party/skia/src/gpu/ganesh/GrCpuBuffer.h:29:20
#2 0x7f530a59bc9d in GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned long, bool) ./../../third\_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:56:30
#3 0x7f530a59cb9c in GrBufferAllocPool::resetCpuData(unsigned long) ./../../third\_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:389:60
#4 0x7f530a59e51a in GrBufferAllocPool::createBlock(unsigned long) ./../../third\_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:362:15
#5 0x7f530a59da01 in GrBufferAllocPool::makeSpace(unsigned long, unsigned long, sk\_sp<GrBuffer const>*, unsigned long*) ./../../third\_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:229:16
#6 0x7f530a59fc02 in GrVertexBufferAllocPool::makeSpace(unsigned long, int, sk\_sp<GrBuffer const>*, int*) ./../../third\_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:445:28
#7 0x7f530a7f3eef in GrMeshDrawOp::PatternHelper::init(GrMeshDrawTarget\*, GrPrimitiveType, unsigned long, sk\_sp<GrBuffer const>, int, int, int, int) ./../../third\_party/skia/src/gpu/ganesh/ops/GrMeshDrawOp.cpp:96:25
#8 0x7f530a7f4500 in GrMeshDrawOp::QuadHelper::QuadHelper(GrMeshDrawTarget\*, unsigned long, int) ./../../third\_party/skia/src/gpu/ganesh/ops/GrMeshDrawOp.cpp:134:11
#9 0x7f530a8542bf in skgpu::ganesh::RegionOp::(anonymous namespace)::RegionOpImpl::onPrepareDraws(GrMeshDrawTarget\*) ./../../third\_party/skia/src/gpu/ganesh/ops/RegionOp.cpp:157:20
#10 0x7f530a830ac0 in GrOp::prepare(GrOpFlushState\*) ./../../third\_party/skia/src/gpu/ganesh/ops/GrOp.h:197:15
#11 0x7f530a83033c in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState\*) ./../../third\_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
#12 0x7f530a6378d9 in GrRenderTask::prepare(GrOpFlushState\*) ./../../third\_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
#13 0x7f530a5dbe50 in GrDrawingManager::executeRenderTasks(GrOpFlushState\*) ./../../third\_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:260:21
#14 0x7f530a5da829 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy\*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const\*) ./../../third\_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:203:34
#15 0x7f530a5dcf7c in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy\*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const\*) ./../../third\_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:530:27
#16 0x7f52d4990394 in flushAndSubmit ./../../third\_party/skia/include/gpu/GrDirectContext.h:333:15
#17 0x7f52d4990394 in gpu::SharedContextState::FlushAndSubmit(bool) ./../../gpu/command\_buffer/service/shared\_context\_state.cc:764:19
#18 0x7f52d494188c in DoFinish ./../../gpu/command\_buffer/service/raster\_decoder.cc:1846:26
#19 0x7f52d494188c in gpu::raster::RasterDecoderImpl::HandleFinish(unsigned int, void const volatile\*) ./../../gpu/command\_buffer/service/raster\_decoder\_autogen.h:22:3
#20 0x7f52d494e321 in gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile\*, int, int\*) ./../../gpu/command\_buffer/service/raster\_decoder.cc:1539:18
#21 0x7f52ff0d3826 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface\*) ./../../gpu/command\_buffer/service/command\_buffer\_service.cc:231:35
#22 0x7f52d6b28e5c in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::\_\_Cr::vector<gpu::SyncToken, std::\_\_Cr::allocator[gpu::SyncToken](javascript:void(0);)> const&) ./../../gpu/ipc/service/command\_buffer\_stub.cc:502:22
#23 0x7f52d6b28101 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command\_buffer\_stub.cc:153:7
#24 0x7f52d6b48655 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long) ./../../gpu/ipc/service/gpu\_channel.cc:932:13
#25 0x7f52d6b56e8e in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), base::WeakPtr[gpu::GpuChannel](javascript:void(0);)&&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), base::WeakPtr[gpu::GpuChannel](javascript:void(0);) const&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), base::WeakPtr[gpu::GpuChannel](javascript:void(0);) const&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&, unsigned long&&) ./../../base/functional/bind\_internal.h:738:12
#26 0x7f52d6b56c74 in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), std::\_\_Cr::tuple<base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long> > ./../../base/functional/bind\_internal.h:954:5
#27 0x7f52d6b56c74 in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), std::\_\_Cr::tuple<base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long>, 0UL, 1UL, 2UL> ./../../base/functional/bind\_internal.h:1067:14
#28 0x7f52d6b56c74 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), base::WeakPtr[gpu::GpuChannel](javascript:void(0);)&&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long), base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);), unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind\_internal.h:980:12
#29 0x7f52ff11076e in Run ./../../base/functional/callback.h:156:12
#30 0x7f52ff11076e in gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) ./../../gpu/command\_buffer/service/scheduler\_dfs.cc:598:24
#31 0x7f52ff10e155 in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command\_buffer/service/scheduler\_dfs.cc:522:3
#32 0x7f52ff111f40 in Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs *> ./../../base/functional/bind\_internal.h:738:12
#33 0x7f52ff111f40 in MakeItSo<void (gpu::SchedulerDfs::*)(), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind\_internal.h:930:12
#34 0x7f52ff111f40 in RunImpl<void (gpu::SchedulerDfs::*)(), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind\_internal.h:1067:14
#35 0x7f52ff111f40 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind\_internal.h:980:12
#36 0x7f530e3bee6a in Run ./../../base/functional/callback.h:156:12
#37 0x7f530e3bee6a in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:203:34
#38 0x7f530e430793 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:11)> ./../../base/task/common/task\_annotator.h:90:5
#39 0x7f530e430793 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:484:23
#40 0x7f530e42f69e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:346:40

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/hyhy100/chromium2/src/out/asan/libskia.so+0xc55492) (BuildId: 739a908ae5387373)
Shadow bytes around the buggy address:
0x7f5282001580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x7f5282001600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x7f5282001680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x7f5282001700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x7f5282001780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7f5282001800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
0x7f5282001880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7f5282001900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7f5282001980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7f5282001a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x7f5282001a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
Addressable: 00
Partially addressable: 01 02 03 04 05 06 07
Heap left redzone: fa
Freed heap region: fd
Stack left redzone: f1
Stack mid redzone: f2
Stack right redzone: f3
Stack after return: f5
Stack use after scope: f8
Global redzone: f9
Global init order: f6
Poisoned by user: f7
Container overflow: fc
Array cookie: ac
Intra object redzone: bb
ASan internal: fe
Left alloca redzone: ca
Right alloca redzone: cb

==126174==ADDITIONAL INFO

==126174==Note: Please include this section with the ASan report.
Task trace:
#0 0x7f52ff10e73a in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command\_buffer/service/scheduler\_dfs.cc:538:27
#1 0x7f52ff10e73a in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command\_buffer/service/scheduler\_dfs.cc:538:27
#2 0x7f52ff10e73a in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command\_buffer/service/scheduler\_dfs.cc:538:27
#3 0x7f52ff10e73a in gpu::SchedulerDfs::RunNextTask() ./../../gpu/command\_buffer/service/scheduler\_dfs.cc:538:27

Command line: `/proc/self/exe --type=gpu-process --string-annotations --crashpad-handler-pid=126139 --enable-crash-reporter=, --no-subproc-heap-profiling --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAgAAAEAAAAAAAAAAAAAAAAAABgAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,5938383281710132735,15970005224835835873,262144 --field-trial-handle=3,i,10774954344472323617,3888956267482362363,262144 --variations-seed-version`

==126174==END OF ADDITIONAL INFO
==126174==ABORTING

#### Reporter credit:

Renan Rios (@hyhy\_100)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: No

## Attachments

- [genskpic.py](attachments/genskpic.py) (text/x-python, 3.5 KB)
- [chromium.diff](attachments/chromium.diff) (text/x-diff, 6.7 KB)
- [index.html](attachments/index.html) (text/html, 191 B)
- [CHROME_ASAN_LOG.txt](attachments/CHROME_ASAN_LOG.txt) (text/plain, 18.8 KB)
- [genskpic_POSTFIX.py](attachments/genskpic_POSTFIX.py) (text/x-python, 3.5 KB)

## Timeline

### hy...@gmail.com (2024-08-19)

ASAN stacktrace is a mess with markdown enabled (sorry, there's no preview now for the final report when reporting bugs through <https://issues.chromium.org/issues/wizard> and I can´t edit them here :/).

I'll attach the stacktrace as a file here.

Also, this attack is only possible from a compromised renderer.

### xi...@chromium.org (2024-08-19)

Thanks for the report. +kjlubick@, could you take a look? Triaged the same way as <https://crbug.com/360265320>.

### kj...@google.com (2024-08-19)

Assigning to Skia's GPU gardener to take a look

### pe...@google.com (2024-08-20)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-08-20)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-08-21)

Project: skia
Branch: main

commit efd38e98b22e3335e4d2bb562c1d2a610990eaca
Author: James Godfrey-Kittle <jamesgk@google.com>
Date:   Tue Aug 20 14:35:00 2024

    [ganesh] Avoid int overflow when combining RegionOps
    
    Bug: b/360758697
    Change-Id: I46eb92ac6ed71646fb05a910f8d577ec851e3b3f
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/891636
    Reviewed-by: Brian Osman <brianosman@google.com>
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>

M       src/gpu/ganesh/ops/RegionOp.cpp

https://skia-review.googlesource.com/891636


### pe...@google.com (2024-08-21)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127, 128, 129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### br...@google.com (2024-08-21)

Amy, similar to [Issue 355465305](https://issues.chromium.org/issues/355465305), the automation is suggesting merges back to 126, but I assume (from your comments on the prior bug) that 126 and 127 aren't going to need (or get) any new merges? Should we just be targeting 128 and 129 now?

### am...@chromium.org (2024-08-21)

Hi Brian -- that's correct. The only applicable branches would be 129 and 128 for backmerge.
I've updated the labeling.
Since the fix just landed today, I'll review this for merge tomorrow or Friday.

### hy...@gmail.com (2024-08-22)

Hi, while researching Skia for more bugs, I noticed that there's another hidden integer overflow here, `PatternHelper` (called from `RegionOpImpl::onPrepareDraws`) is also not checking against overflows when multiplying the amount of vertices per repetition with the number of quads to draw, so we can still overflow the vertex space even if `numRects` is a valid integer, see [1] [2] [3] below:

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

### br...@google.com (2024-08-22)

Adding more GPU leads, for visibility into the vertex overflow issues described in [Comment #11](https://issues.chromium.org/issues/360758697#comment11)

### eg...@google.com (2024-08-22)

Hyhy100n would you mind filing a new bug for [comment#11](https://issues.chromium.org/issues/360758697#comment11)? That way this one can be used for tracking the cherry-picks of the original bug and fix.

### hy...@gmail.com (2024-08-22)

Ok

### hy...@gmail.com (2024-08-22)

done, <https://issues.chromium.org/issues/361461526>

### am...@chromium.org (2024-08-23)

<https://skia-review.googlesource.com/c/skia/+/891636> approved for merges to M129 Beta and M128 Stable
There appear to have been some issues with the Windows Canary build since the Skia -> Chromium roll, so I reviewed data for Android and Mac canary build and am not seeing any issues.
Please go ahead and merge this fix to branch 6668 / M129 and branch 6613 / M128 at your earliest convenience so this fix can be included in next updates

### ap...@google.com (2024-08-24)

Project: skia
Branch: chrome/m129

commit 501e9efaa2fc929ec67c44da6dbaf9335264b559
Author: James Godfrey-Kittle <jamesgk@google.com>
Date:   Tue Aug 20 14:35:00 2024

    [ganesh] Avoid int overflow when combining RegionOps
    
    Bug: b/360758697
    Change-Id: I46eb92ac6ed71646fb05a910f8d577ec851e3b3f
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/891636
    Reviewed-by: Brian Osman <brianosman@google.com>
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>
    (cherry picked from commit efd38e98b22e3335e4d2bb562c1d2a610990eaca)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/892601
    Reviewed-by: Michael Ludwig <michaelludwig@google.com>
    Auto-Submit: Brian Osman <brianosman@google.com>
    Commit-Queue: Michael Ludwig <michaelludwig@google.com>

M       src/gpu/ganesh/ops/RegionOp.cpp

https://skia-review.googlesource.com/892601


### ap...@google.com (2024-08-24)

Project: skia
Branch: chrome/m128

commit 8bd493b850f1a75482af8f30cb492cd70645498c
Author: James Godfrey-Kittle <jamesgk@google.com>
Date:   Tue Aug 20 14:35:00 2024

    [ganesh] Avoid int overflow when combining RegionOps
    
    Bug: b/360758697
    Change-Id: I46eb92ac6ed71646fb05a910f8d577ec851e3b3f
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/891636
    Reviewed-by: Brian Osman <brianosman@google.com>
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>
    (cherry picked from commit efd38e98b22e3335e4d2bb562c1d2a610990eaca)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/892184
    Commit-Queue: Michael Ludwig <michaelludwig@google.com>
    Auto-Submit: Brian Osman <brianosman@google.com>
    Reviewed-by: Michael Ludwig <michaelludwig@google.com>

M       src/gpu/ganesh/ops/RegionOp.cpp

https://skia-review.googlesource.com/892184


### ap...@google.com (2024-08-24)

Project: skia
Branch: chrome/m129

commit 501e9efaa2fc929ec67c44da6dbaf9335264b559
Author: James Godfrey-Kittle <jamesgk@google.com>
Date:   Tue Aug 20 14:35:00 2024

    [ganesh] Avoid int overflow when combining RegionOps
    
    Bug: b/360758697
    Change-Id: I46eb92ac6ed71646fb05a910f8d577ec851e3b3f
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/891636
    Reviewed-by: Brian Osman <brianosman@google.com>
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>
    (cherry picked from commit efd38e98b22e3335e4d2bb562c1d2a610990eaca)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/892601
    Reviewed-by: Michael Ludwig <michaelludwig@google.com>
    Auto-Submit: Brian Osman <brianosman@google.com>
    Commit-Queue: Michael Ludwig <michaelludwig@google.com>

M       src/gpu/ganesh/ops/RegionOp.cpp

https://skia-review.googlesource.com/892601


### pe...@google.com (2024-08-24)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### br...@google.com (2024-08-24)

re: LTS questions in [comment #20](https://issues.chromium.org/issues/360758697#comment20):

1. No, this is a pre-existing condition that has existed for numerous milestones.
2. No.

### sp...@google.com (2024-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $15000.00 for this report.

Rationale for this decision:
$15,000 for high-quality report of demonstrated memory corruption in a highly-privileged process (GPU)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-29)

Congratulations Renan! Thank you for your efforts and your high-quality report of this issue -- great work!

### hy...@gmail.com (2024-08-29)

Hi, as per [crbug.com/360265320](https://issues.chromium.org/issues/360265320#comment17):

Android stacktrace of this bug after attaching lldb to the GPU process on Android using `out/androidx86_64/bin/chrome_public_apk lldb --debug-process-name privileged_process0` (memory corruption has already been proven by the previous ASAN stacktrace, just proving Android reproducibility using an Android release build I have here):

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
    frame #42: 0x0000731209368c96 libart.so`NterpCommonInvokeStatic + 131

```

### am...@chromium.org (2024-08-29)

re c#24; (same response as on [crbug.com/360265320](https://crbug.com/360265320)) Since this was reported and not demonstrated before the new reward structure was announced, we'll need to take this under specific consideration to determine if a reward adjustment is appropriate here.

We do, however, greatly appreciate you going ahead and providing the requisite information up front, in tandem to your reassessment request. In the future, impact in a given process and platform will be expected to be demonstrated in the original report, not after reward decision.

We'll take a look at a future panel session, and will update here with a decision after that discussion has occurred.

### pe...@google.com (2024-08-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-08-30)

1. <http://review.skia.org/894936> for 120, <http://review.skia.org/894463> for 126
2. Low, only conflicts with includes
3. 128, 129
4. Yes

### am...@chromium.org (2024-09-04)

Following up on c#24 and c#25, while we appreciate you attempting to demonstrate this issue on Android, your stacktrace that you have provided only demonstrates a segfault. While this issue in Ganesh, and transitively Android is impacted, to be eligible for the memory corruption in a non-sandboxed process level rewards you would need to fully demonstrate that exploitable memory corruption on Android in the same manner as other platforms. This will be expected to be included as part of the original report in future reports.

### hy...@gmail.com (2024-09-05)

Hi, thanks for reviewing it and for answering my questions, let me clarify the situation here, maybe I have misunderstood the current VRP rules:

According to [1], vulnerabilities as "High-quality report of demonstrated memory corruption" in non-sandboxed process (e.g: GPU process in Android, according to
" Also includes the GPU process on Android. RCE in the Android GPU process is considered a sandbox escape since the GPU process is not sandboxed on the Android platform.") are eligible for 35k bounty.

Now, the Android stack trace provided, ends up with [2]

```
* thread #14, name = 'CrGpuMain', stop reason = signal SIGSEGV: address access protected (fault address: 0x7310a778a000)
  * frame #0: 0x000073117e2d6684 libskia.cr.so`skgpu::VertexWriter& skgpu::operator<<<float>(w=0x000073119c014ea0, val=0x000073119c014f0c) at BufferWriter.h:280:5

template <typename T>
inline VertexWriter& operator<<(VertexWriter& w, const T& val) {
    static_assert(std::is_trivially_copyable<T>::value, "");
    w.validate(sizeof(T));
    memcpy(w.fPtr, &val, sizeof(T));
    w = w.makeOffset(sizeof(T));
    return w;
}

```

This is a write into memory that is currently not mapped, as already explained by the bug writeup, an attacker can manipulate the allocation size and this write could be done in a controlled memory, furthermore,
PartitionAlloc does have predicable memory layout and memory allocations (unless chunk randomization was implemented or something similar that I'm currently not aware of),
that makes doable to manipulate the write to end up in controlled memory.

I do understand there are constraints over the for-loop size that may be a big value, however, wild-memcpy (and similar scenarios) exploitation isn't unrealistic as it has been done previously a few times, [3][4][5]
taking in consideration the multi-thread nature of modern browsers (we have IO/UI/Thread pool etc), there are potentially multiple way to exploit it.

Let me know what I may have misunderstood here and why this doesn't meet the bar, happy to follow-up with any extra information if needed!

Thanks.

Reference:

[1] <https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules#memory-corruption-vulnerabilities>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/BufferWriter.h;l=280?q=BufferWriter.h:280&ss=chromium>

[3] <https://googleprojectzero.blogspot.com/2015/03/taming-wild-copy-parallel-thread.html>

[4] <https://blog.ret2.io/2022/05/19/pwn2own-2021-parallels-desktop-exploit/>

[5] <https://saaramar.github.io/IOMFB_integer_overflow_poc/#wildcopy-exploitation>

### hy...@gmail.com (2024-09-11)

Following [c#29](https://issues.chromium.org/issues/360758697#comment29) and [crbug.com/360265320](https://crbug.com/360265320)#comment25, GPU process ASAN stacktrace on ARM64 Android from logcat:

```
09-11 00:38:14.438  9577  9577 I wrap.sh : =================================================================
09-11 00:38:14.438  9577  9577 I wrap.sh : ==9578==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x0073f71fe820 at pc 0x0074444b92e4 bp 0x00745cc8a560 sp 0x00745cc8a558
09-11 00:38:14.439  9577  9577 I wrap.sh : WRITE of size 4 at 0x0073f71fe820 thread T16 (CrGpuMain)
I 00:38:19.592  221.385s Main  Running: /home/hyhy100/chromium/src/third_party/android_platform/development/scripts/stack.py --output-directory /home/hyhy100/chromium/src/out/android-arm64-static --apks-directory /tmp/tmpzho364jg --quiet /tmp/tmpfqu6rzhf
09-11 00:38:14.476  9577  9577 I wrap.sh : 
09-11 00:38:14.476  9577  9577 I wrap.sh : Stack Trace:
09-11 00:38:14.476  9577  9577 I wrap.sh :   RELADDR   FUNCTION                                                                          FILE:LINE
09-11 00:38:14.476  9577  9577 I wrap.sh :   v------>  skgpu::VertexWriter& skgpu::operator<<<float>(skgpu::VertexWriter&, float const&)  ../../third_party/skia/src/gpu/BufferWriter.h:280:5
09-11 00:38:14.477  9577  9577 I wrap.sh :   24b692e0  skgpu::VertexWriter::TriStrip<float>::writeVertex(int, skgpu::VertexWriter&) const  ../../third_party/skia/src/gpu/BufferWriter.h:208:32
09-11 00:38:14.477  9577  9577 I wrap.sh :   v------>  std::__Cr::enable_if<is_quad<skgpu::VertexWriter::TriStrip<float>>::value, void>::type skgpu::VertexWriter::writeQuadVertex<1, skgpu::VertexWriter::TriStrip<float>, skgpu::VertexColor>(skgpu::VertexWriter::TriStrip<float> const&, skgpu::VertexColor const&)  ../../third_party/skia/src/gpu/BufferWriter.h:262:14
09-11 00:38:14.477  9577  9577 I wrap.sh :   v------>  void skgpu::VertexWriter::writeQuad<skgpu::VertexWriter::TriStrip<float>, skgpu::VertexColor>(skgpu::VertexWriter::TriStrip<float> const&, skgpu::VertexColor const&)  ../../third_party/skia/src/gpu/BufferWriter.h:246:15
09-11 00:38:14.477  9577  9577 I wrap.sh :   24bea1f0  skgpu::ganesh::RegionOp::(anonymous namespace)::RegionOpImpl::onPrepareDraws(GrMeshDrawTarget*)  ../../third_party/skia/src/gpu/ganesh/ops/RegionOp.cpp:140:26
09-11 00:38:14.477  9577  9577 I wrap.sh :   24bcba98  GrOp::prepare(GrOpFlushState*)                                                    ../../third_party/skia/src/gpu/ganesh/ops/GrOp.h:187:15
09-11 00:38:14.477  9577  9577 I wrap.sh :   24bcafe0  skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*)                                ../../third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:531:27
09-11 00:38:14.477  9577  9577 I wrap.sh :   249f40c8  GrRenderTask::prepare(GrOpFlushState*)                                            ../../third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
09-11 00:38:14.477  9577  9577 I wrap.sh :   2499ac58  GrDrawingManager::executeRenderTasks(GrOpFlushState*)                             ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:260:21
09-11 00:38:14.477  9577  9577 I wrap.sh :   24998d98  GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:203:34
09-11 00:38:14.477  9577  9577 I wrap.sh :   2499c8e4  GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:530:27
09-11 00:38:14.477  9577  9577 I wrap.sh :   2498afb0  GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:92:47
09-11 00:38:14.477  9577  9577 I wrap.sh :   v------>  GrDirectContextPriv::flushSurface(GrSurfaceProxy*, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
09-11 00:38:14.478  9577  9577 I wrap.sh :   24983fc0  GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:516:25
09-11 00:38:14.478  9577  9577 I wrap.sh :   24c22444  skgpu::ganesh::Flush(SkSurface*)                                                  ../../third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:782:45
09-11 00:38:14.478  9577  9577 I wrap.sh :   2a1cfaac  gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*)  ../../gpu/command_buffer/service/shared_context_state.cc:798:9
09-11 00:38:14.478  9577  9577 I wrap.sh :   2a184c54  gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM()                             ../../gpu/command_buffer/service/raster_decoder.cc:3128:30
09-11 00:38:14.478  9577  9577 I wrap.sh :   2a17f3c8  gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*)  ../../gpu/command_buffer/service/raster_decoder_autogen.h:162:3
09-11 00:38:14.478  9577  9577 I wrap.sh :   2a18e488  gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)  ../../gpu/command_buffer/service/raster_decoder.cc:1510:18
09-11 00:38:14.478  9577  9577 I wrap.sh :   2829ff1c  gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)                    ../../gpu/command_buffer/service/command_buffer_service.cc:231:35
09-11 00:38:14.478  9577  9577 I wrap.sh :   2a4673e0  gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)  ../../gpu/ipc/service/command_buffer_stub.cc:503:22
09-11 00:38:14.478  9577  9577 I wrap.sh :   2a4662a4  gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&)  ../../gpu/ipc/service/command_buffer_stub.cc:154:7
09-11 00:38:14.478  9577  9577 I wrap.sh :   2a47ecac  gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long)  ../../gpu/ipc/service/gpu_channel.cc:932:13
09-11 00:38:14.478  9577  9577 I wrap.sh :   v------>  void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&)  ../../base/functional/bind_internal.h:738:12
09-11 00:38:14.479  9577  9577 I wrap.sh :   2a48bf84  void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, void, 0ul, 1ul, 2ul>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>&&)  ../../base/functional/bind_internal.h:954:5
09-11 00:38:14.479  9577  9577 I wrap.sh :   v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0ul, 1ul, 2ul>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>)  ../../base/functional/bind_internal.h:1067:14
09-11 00:38:14.479  9577  9577 I wrap.sh :   2a48bd68  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:980:12
09-11 00:38:14.479  9577  9577 I wrap.sh :   138d1804  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:156:12
09-11 00:38:14.479  9577  9577 I wrap.sh :   282cf2b8  gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)  ../../gpu/command_buffer/service/scheduler_dfs.cc:600:24
09-11 00:38:14.479  9577  9577 I wrap.sh :   282cd2ac  gpu::SchedulerDfs::RunNextTask()                                                  ../../gpu/command_buffer/service/scheduler_dfs.cc:524:3
09-11 00:38:14.479  9577  9577 I wrap.sh :   v------>  void base::internal::DecayedFunctorTraits<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs*>::Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs*>(void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs*&&)  ../../base/functional/bind_internal.h:738:12
09-11 00:38:14.479  9577  9577 I wrap.sh :   v------>  void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, void, 0ul>::MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>>(void (gpu::SchedulerDfs::*&&)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&)  ../../base/functional/bind_internal.h:930:12
09-11 00:38:14.479  9577  9577 I wrap.sh :   v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(void (gpu::SchedulerDfs::*&&)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)  ../../base/functional/bind_internal.h:1067:14
09-11 00:38:14.479  9577  9577 I wrap.sh :   282d0ad4  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:980:12
09-11 00:38:14.479  9577  9577 I wrap.sh :   138d1804  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:156:12
09-11 00:38:14.479  9577  9577 I wrap.sh :   22f457cc  base::TaskAnnotator::RunTaskImpl(base::PendingTask&)                              ../../base/task/common/task_annotator.cc:203:34
09-11 00:38:14.479  9577  9577 I wrap.sh :   v------>  void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&)  ../../base/task/common/task_annotator.h:90:5
09-11 00:38:14.479  9577  9577 I wrap.sh :   22fc3acc  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
09-11 00:38:14.479  9577  9577 I wrap.sh :   22fc28bc  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()   ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
09-11 00:38:14.479  9577  9577 I wrap.sh :   22e49990  base::MessagePumpDefault::Run(base::MessagePump::Delegate*)                       ../../base/message_loop/message_pump_default.cc:40:55
09-11 00:38:14.479  9577  9577 I wrap.sh :   22fc5930  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
09-11 00:38:14.479  9577  9577 I wrap.sh :   22ee07ec  base::RunLoop::Run(base::Location const&)                                         ../../base/run_loop.cc:134:14
09-11 00:38:14.479  9577  9577 I wrap.sh :   35071528  content::GpuMain(content::MainFunctionParams)                                     ../../content/gpu/gpu_main.cc:431:14
09-11 00:38:14.479  9577  9577 I wrap.sh :   22006d70  content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)  ../../content/app/content_main_runner_impl.cc:798:14
09-11 00:38:14.479  9577  9577 I wrap.sh :   22008be0  content::ContentMainRunnerImpl::Run()                                             ../../content/app/content_main_runner_impl.cc:1175:10
09-11 00:38:14.479  9577  9577 I wrap.sh :   22003080  content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)  ../../content/app/content_main.cc:333:36
09-11 00:38:14.479  9577  9577 I wrap.sh :   v------>  content::JNI_ContentMain_Start(_JNIEnv*, unsigned char)                           ../../content/app/android/content_main_android.cc:65:10
09-11 00:38:14.479  9577  9577 I wrap.sh :   22005798  Java_org_1chromium_1content_1app_1ContentMain_1start                              gen/jni_headers/content/public/android/content_app_jni/ContentMain_jni.h:36:15
09-11 00:38:14.479  9577  9577 I wrap.sh : : 
09-11 00:38:14.479  9577  9577 I wrap.sh : 0x0073f71fe820 is located 0 bytes after 4194336-byte region [0x0073f6dfe800,0x0073f71fe820)
09-11 00:38:14.480  9577  9577 I wrap.sh : allocated by thread T16 (CrGpuMain) here:
I 00:38:22.519  224.311s Main  Running: /home/hyhy100/chromium/src/third_party/android_platform/development/scripts/stack.py --output-directory /home/hyhy100/chromium/src/out/android-arm64-static --apks-directory /tmp/tmpzho364jg --quiet /tmp/tmpavma11a1
09-11 00:38:14.481  9577  9577 I wrap.sh : 
09-11 00:38:14.481  9577  9577 I wrap.sh : Stack Trace:
09-11 00:38:14.481  9577  9577 I wrap.sh :   RELADDR   FUNCTION                                                                          FILE:LINE
09-11 00:38:14.481  9577  9577 I wrap.sh :   v------>  GrCpuBuffer::Make(unsigned long)                                                  ../../third_party/skia/src/gpu/ganesh/GrCpuBuffer.h:29:20
09-11 00:38:14.481  9577  9577 I wrap.sh :   24963018  GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned long, bool)                ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:56:30
09-11 00:38:14.481  9577  9577 I wrap.sh :   24964b24  GrBufferAllocPool::resetCpuData(unsigned long)                                    ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:389:60
09-11 00:38:14.481  9577  9577 I wrap.sh :   24966558  GrBufferAllocPool::createBlock(unsigned long)                                     ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:362:15
09-11 00:38:14.482  9577  9577 I wrap.sh :   24965a38  GrBufferAllocPool::makeSpace(unsigned long, unsigned long, sk_sp<GrBuffer const>*, unsigned long*)  ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:229:16
09-11 00:38:14.482  9577  9577 I wrap.sh :   24967b90  GrVertexBufferAllocPool::makeSpace(unsigned long, int, sk_sp<GrBuffer const>*, int*)  ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:445:28
09-11 00:38:14.482  9577  9577 I wrap.sh :   24b97020  GrMeshDrawOp::PatternHelper::init(GrMeshDrawTarget*, GrPrimitiveType, unsigned long, sk_sp<GrBuffer const>, int, int, int, int)  ../../third_party/skia/src/gpu/ganesh/ops/GrMeshDrawOp.cpp:87:25
09-11 00:38:14.482  9577  9577 I wrap.sh :   24b973b4  GrMeshDrawOp::QuadHelper::QuadHelper(GrMeshDrawTarget*, unsigned long, int)       ../../third_party/skia/src/gpu/ganesh/ops/GrMeshDrawOp.cpp:125:11
09-11 00:38:14.482  9577  9577 I wrap.sh :   24bea08c  skgpu::ganesh::RegionOp::(anonymous namespace)::RegionOpImpl::onPrepareDraws(GrMeshDrawTarget*)  ../../third_party/skia/src/gpu/ganesh/ops/RegionOp.cpp:127:20
09-11 00:38:14.482  9577  9577 I wrap.sh :   24bcba98  GrOp::prepare(GrOpFlushState*)                                                    ../../third_party/skia/src/gpu/ganesh/ops/GrOp.h:187:15
09-11 00:38:14.482  9577  9577 I wrap.sh :   24bcafe0  skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*)                                ../../third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:531:27
09-11 00:38:14.482  9577  9577 I wrap.sh :   249f40c8  GrRenderTask::prepare(GrOpFlushState*)                                            ../../third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
09-11 00:38:14.482  9577  9577 I wrap.sh :   2499ac58  GrDrawingManager::executeRenderTasks(GrOpFlushState*)                             ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:260:21
09-11 00:38:14.482  9577  9577 I wrap.sh :   24998d98  GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:203:34
09-11 00:38:14.482  9577  9577 I wrap.sh :   2499c8e4  GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:530:27
09-11 00:38:14.482  9577  9577 I wrap.sh :   2498afb0  GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:92:47
09-11 00:38:14.482  9577  9577 I wrap.sh :   v------>  GrDirectContextPriv::flushSurface(GrSurfaceProxy*, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
09-11 00:38:14.483  9577  9577 I wrap.sh :   24983fc0  GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:516:25
09-11 00:38:14.483  9577  9577 I wrap.sh :   24c22444  skgpu::ganesh::Flush(SkSurface*)                                                  ../../third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:782:45
09-11 00:38:14.483  9577  9577 I wrap.sh :   2a1cfaac  gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*)  ../../gpu/command_buffer/service/shared_context_state.cc:798:9
09-11 00:38:14.483  9577  9577 I wrap.sh :   2a184c54  gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM()                             ../../gpu/command_buffer/service/raster_decoder.cc:3128:30
09-11 00:38:14.483  9577  9577 I wrap.sh :   2a17f3c8  gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*)  ../../gpu/command_buffer/service/raster_decoder_autogen.h:162:3
09-11 00:38:14.483  9577  9577 I wrap.sh :   2a18e488  gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)  ../../gpu/command_buffer/service/raster_decoder.cc:1510:18
09-11 00:38:14.483  9577  9577 I wrap.sh :   2829ff1c  gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)                    ../../gpu/command_buffer/service/command_buffer_service.cc:231:35
09-11 00:38:14.483  9577  9577 I wrap.sh :   2a4673e0  gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)  ../../gpu/ipc/service/command_buffer_stub.cc:503:22
09-11 00:38:14.483  9577  9577 I wrap.sh :   2a4662a4  gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&)  ../../gpu/ipc/service/command_buffer_stub.cc:154:7
09-11 00:38:14.483  9577  9577 I wrap.sh :   2a47ecac  gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long)  ../../gpu/ipc/service/gpu_channel.cc:932:13
09-11 00:38:14.483  9577  9577 I wrap.sh :   v------>  void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&)  ../../base/functional/bind_internal.h:738:12
09-11 00:38:14.483  9577  9577 I wrap.sh :   2a48bf84  void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, void, 0ul, 1ul, 2ul>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>&&)  ../../base/functional/bind_internal.h:954:5
09-11 00:38:14.483  9577  9577 I wrap.sh :   v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0ul, 1ul, 2ul>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>)  ../../base/functional/bind_internal.h:1067:14
09-11 00:38:14.483  9577  9577 I wrap.sh :   2a48bd68  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:980:12
09-11 00:38:14.483  9577  9577 I wrap.sh :   138d1804  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:156:12
09-11 00:38:14.483  9577  9577 I wrap.sh :   282cf2b8  gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)  ../../gpu/command_buffer/service/scheduler_dfs.cc:600:24
09-11 00:38:14.483  9577  9577 I wrap.sh : : 
09-11 00:38:14.483  9577  9577 I wrap.sh : Thread T16 (CrGpuMain) created by T0 (ileged_process4) here:
I 00:38:25.413  227.206s Main  Running: /home/hyhy100/chromium/src/third_party/android_platform/development/scripts/stack.py --output-directory /home/hyhy100/chromium/src/out/android-arm64-static --apks-directory /tmp/tmpzho364jg --quiet /tmp/tmpkwiglwt8
09-11 00:38:14.512  9577  9577 I wrap.sh : : 
09-11 00:38:14.512  9577  9577 I wrap.sh : SUMMARY: AddressSanitizer: heap-buffer-overflow (/data/app/~~KPyAmZWcrOc5MMNAXCzsqg==/org.chromium.chrome-S467huOY7bZcvacNu-lOrA==/lib/arm64/libchrome.so+0x24b692e0) (BuildId: 6ea1b6ebac3bf624) 
09-11 00:38:14.512  9577  9577 I wrap.sh : Shadow bytes around the buggy address:
09-11 00:38:14.512  9577  9577 I wrap.sh :   0x0073f71fe580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-11 00:38:14.512  9577  9577 I wrap.sh :   0x0073f71fe600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-11 00:38:14.512  9577  9577 I wrap.sh :   0x0073f71fe680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-11 00:38:14.513  9577  9577 I wrap.sh :   0x0073f71fe700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-11 00:38:14.513  9577  9577 I wrap.sh :   0x0073f71fe780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-11 00:38:14.513  9577  9577 I wrap.sh : =>0x0073f71fe800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
09-11 00:38:14.513  9577  9577 I wrap.sh :   0x0073f71fe880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-11 00:38:14.513  9577  9577 I wrap.sh :   0x0073f71fe900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-11 00:38:14.513  9577  9577 I wrap.sh :   0x0073f71fe980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-11 00:38:14.513  9577  9577 I wrap.sh :   0x0073f71fea00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-11 00:38:14.514  9577  9577 I wrap.sh :   0x0073f71fea80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-11 00:38:14.514  9577  9577 I wrap.sh : Shadow byte legend (one shadow byte represents 8 application bytes):
09-11 00:38:14.514  9577  9577 I wrap.sh :   Addressable:           00
09-11 00:38:14.514  9577  9577 I wrap.sh :   Partially addressable: 01 02 03 04 05 06 07 
09-11 00:38:14.514  9577  9577 I wrap.sh :   Heap left redzone:       fa
09-11 00:38:14.514  9577  9577 I wrap.sh :   Freed heap region:       fd
09-11 00:38:14.514  9577  9577 I wrap.sh :   Stack left redzone:      f1
09-11 00:38:14.514  9577  9577 I wrap.sh :   Stack mid redzone:       f2
09-11 00:38:14.514  9577  9577 I wrap.sh :   Stack right redzone:     f3
09-11 00:38:14.515  9577  9577 I wrap.sh :   Stack after return:      f5
09-11 00:38:14.515  9577  9577 I wrap.sh :   Stack use after scope:   f8
09-11 00:38:14.515  9577  9577 I wrap.sh :   Global redzone:          f9
09-11 00:38:14.515  9577  9577 I wrap.sh :   Global init order:       f6
09-11 00:38:14.515  9577  9577 I wrap.sh :   Poisoned by user:        f7
09-11 00:38:14.515  9577  9577 I wrap.sh :   Container overflow:      fc
09-11 00:38:14.515  9577  9577 I wrap.sh :   Array cookie:            ac
09-11 00:38:14.515  9577  9577 I wrap.sh :   Intra object redzone:    bb
09-11 00:38:14.515  9577  9577 I wrap.sh :   ASan internal:           fe
09-11 00:38:14.516  9577  9577 I wrap.sh :   Left alloca redzone:     ca
09-11 00:38:14.516  9577  9577 I wrap.sh :   Right alloca redzone:    cb
09-11 00:38:14.516  9577  9577 I wrap.sh : : 
09-11 00:38:14.516  9577  9577 I wrap.sh : ==9578==ADDITIONAL INFO
09-11 00:38:14.516  9577  9577 I wrap.sh : : 
09-11 00:38:14.516  9577  9577 I wrap.sh : ==9578==Note: Please include this section with the ASan report.
09-11 00:38:14.516  9577  9577 I wrap.sh : Task trace:
I 00:38:25.465  227.257s Main  Running: /home/hyhy100/chromium/src/third_party/android_platform/development/scripts/stack.py --output-directory /home/hyhy100/chromium/src/out/android-arm64-static --apks-directory /tmp/tmpzho364jg --quiet /tmp/tmp95exoi3u
09-11 00:38:14.516  9577  9577 I wrap.sh : 
09-11 00:38:14.516  9577  9577 I wrap.sh : Stack Trace:
09-11 00:38:14.517  9577  9577 I wrap.sh :   RELADDR   FUNCTION                                                              FILE:LINE
09-11 00:38:14.517  9577  9577 I wrap.sh :   282cd620  gpu::SchedulerDfs::RunNextTask()                                      ../../gpu/command_buffer/service/scheduler_dfs.cc:540:27
09-11 00:38:14.517  9577  9577 I wrap.sh :   282cd620  gpu::SchedulerDfs::RunNextTask()                                      ../../gpu/command_buffer/service/scheduler_dfs.cc:540:27
09-11 00:38:14.517  9577  9577 I wrap.sh :   282cd620  gpu::SchedulerDfs::RunNextTask()                                      ../../gpu/command_buffer/service/scheduler_dfs.cc:540:27
09-11 00:38:14.517  9577  9577 I wrap.sh :   282c8268  gpu::SchedulerDfs::TryScheduleSequence(gpu::SchedulerDfs::Sequence*)  ../../gpu/command_buffer/service/scheduler_dfs.cc:342:11
09-11 00:38:14.517  9577  9577 I wrap.sh : : 
09-11 00:38:14.517  9577  9577 I wrap.sh : : 
09-11 00:38:14.517  9577  9577 I wrap.sh : Command line: ` --type=gpu-process --enable-crash-reporter=,unknown --no-subproc-heap-profiling --gpu-preferences=UAAAAAAAAAAgAIAsAAAAAAAAAAAAAAAAAABgAAIAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=5,i,5094911813524918415,10363945074875014685,262144 --field-trial-handle=3,i,17483529603100381663,843663544159005069,262144 --variations-seed-version --host-package-name=org.chromium.chrome --package-name=org.chromium.chrome --host-package-label=Chromium --host-version-code=661700004 --package-version-name=129.0.6617.0 --mojo-platform-channel-handle=binder:0 --enable-dom-distiller`
09-11 00:38:14.517  9577  9577 I wrap.sh : : 
09-11 00:38:14.517  9577  9577 I wrap.sh : : 
09-11 00:38:14.517  9577  9577 I wrap.sh : ==9578==END OF ADDITIONAL INFO
09-11 00:38:14.518  9577  9577 I wrap.sh : ==9578==ABORTING

```

### ap...@google.com (2024-09-11)

Project: skia
Branch: chrome/m126

commit 6473303eae04fe03fd2b75544118c258f667354e
Author: James Godfrey-Kittle <jamesgk@google.com>
Date:   Tue Aug 20 14:35:00 2024

    [M126-LTS][ganesh] Avoid int overflow when combining RegionOps
    
    M126 merge issues:
      Conflicting includes
    
    Bug: b/360758697
    Change-Id: I46eb92ac6ed71646fb05a910f8d577ec851e3b3f
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/891636
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/894463
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Reviewed-by: James Godfrey-Kittle <jamesgk@google.com>

M       src/gpu/ganesh/ops/RegionOp.cpp

https://skia-review.googlesource.com/894463


### sp...@google.com (2024-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
Additional $10,000 reward for baseline demonstration of memory corruption in Android GPU process, following up from initial $15,000 reward for high-quality report of GPU process memory corruption


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-11)

Thank you for the follow up here and the demonstration of this on Android provided from the new stack trace.

re:

> `According to [1], vulnerabilities as "High-quality report of demonstrated memory corruption" in non-sandboxed process (e.g: GPU process in Android, according to " Also includes the GPU process on Android. RCE in the Android GPU process is considered a sandbox escape since the GPU process is not sandboxed on the Android platform.")`

The expectation here is that you would need to demonstrate memory corruption or a greater degree of exploitability on Android for the consideration of non-sandbox process level rewards. Simply pointing to code or relying on the transitive properties of a feature on Android with a demonstration only on desktop would not allow for high-level rewards on its own.

### ap...@google.com (2024-09-12)

Project: skia
Branch: chrome/m120

commit 74fd62677838629e369e4bd347d514b6e3f0f5b0
Author: James Godfrey-Kittle <jamesgk@google.com>
Date:   Tue Aug 20 14:35:00 2024

    [M120-LTS][ganesh] Avoid int overflow when combining RegionOps
    
    M120 merge issues:
      Conflicting includes
    
    Bug: b/360758697
    No-Try: true
    No-Presubmit: true
    No-Tree-Checks: true
    Change-Id: I46eb92ac6ed71646fb05a910f8d577ec851e3b3f
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/891636
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/894936
    Reviewed-by: James Godfrey-Kittle <jamesgk@google.com>

M       src/gpu/ganesh/ops/RegionOp.cpp

https://skia-review.googlesource.com/894936


### pe...@google.com (2024-11-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/360758697)*
