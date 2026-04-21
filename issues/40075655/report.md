# UAF in GrDrawOpAtlas (with --headless mode)

| Field | Value |
|-------|-------|
| **Issue ID** | [40075655](https://issues.chromium.org/issues/40075655) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | em...@gmail.com |
| **Assignee** | ja...@google.com |
| **Created** | 2023-10-26 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

UAF in GrDrawOpAtlas (with --headless mode)  

tested os:  

ubuntu 22.04

tested chrome:  

Chromium 119.0.6041.0  

Chromium 120.0.6091.0 gs://chromium-browser-asan/linux-release/asan-linux-release-1215342.zip

./chrome --use-gl=angle --use-angle=swiftshader --user-data-dir=/tmp/xxs --no-sandbox --incognito --headless --remote-debugging-port=0 ./crash.html  

If it doesn't repro immediately, you can try a few more times. In my local machine, it can usually be reproduced in 2 or 3 times.

**Problem Description:**  

==1382130==ERROR: AddressSanitizer: heap-use-after-free on address 0x502000006b50 at pc 0x5592e204c040 bp 0x7fff38b57250 sp 0x7fff38b57248  

READ of size 8 at 0x502000006b50 thread T0 (chrome)  

#0 0x5592e204c03f in GrDrawOpAtlas::uploadPlotToTexture(std::\_\_Cr::function<bool (GrTextureProxy\*, SkIRect, GrColorType, void const\*, unsigned long)>&, GrTextureProxy\*, skgpu::Plot\*) ./../../third\_party/skia/src/gpu/ganesh/GrDrawOpAtlas.cpp:140:5  

#1 0x5592e1df40a9 in operator() ./../../third\_party/libc++/src/include/\_\_functional/function.h:856:16  

#2 0x5592e1df40a9 in operator() ./../../third\_party/libc++/src/include/\_\_functional/function.h:1170:12  

#3 0x5592e1df40a9 in doUpload ./../../third\_party/skia/src/gpu/ganesh/GrOpFlushState.cpp:142:5  

#4 0x5592e1df40a9 in GrOpFlushState::preExecuteDraws() ./../../third\_party/skia/src/gpu/ganesh/GrOpFlushState.cpp:82:15  

#5 0x5592e1dba45b in GrDrawingManager::executeRenderTasks(GrOpFlushState\*) ./../../third\_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:255:17  

#6 0x5592e1db8a4f in GrDrawingManager::flush(SkSpan<GrSurfaceProxy\*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const\*) ./../../third\_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:194:34  

#7 0x5592e1dbb46a in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy\*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const\*) ./../../third\_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:521:27  

#8 0x5592e1db406d in GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy\*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const\*) ./../../third\_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:67:47  

#9 0x5592e1d46f9b in flushSurface ./../../third\_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:79:22  

#10 0x5592e1d46f9b in GrDirectContext::flush(SkSurface\*, GrFlushInfo const&, skgpu::MutableTextureState const\*) ./../../third\_party/skia/src/gpu/ganesh/GrDirectContext.cpp:521:25  

#11 0x5592e20bf79a in skgpu::ganesh::Flush(SkSurface\*) ./../../third\_party/skia/src/gpu/ganesh/surface/SkSurface\_Ganesh.cpp:783:45  

#12 0x5592e8b66297 in gpu::raster::RasterDecoderImpl::FlushSurface(gpu::SkiaImageRepresentation::ScopedWriteAccess\*) ./../../gpu/command\_buffer/service/raster\_decoder.cc:798:7  

#13 0x5592e8b52090 in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM() ./../../gpu/command\_buffer/service/raster\_decoder.cc:3208:7  

#14 0x5592e8b4c32c in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile\*) ./../../gpu/command\_buffer/service/raster\_decoder\_autogen.h:162:3  

#15 0x5592e8b57be1 in gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile\*, int, int\*) ./../../gpu/command\_buffer/service/raster\_decoder.cc:1564:18  

#16 0x5592e8aa38bf in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface\*) ./../../gpu/command\_buffer/service/command\_buffer\_service.cc:232:35  

#17 0x5592e8a917e1 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::\_\_Cr::vector<gpu::SyncToken, std::\_\_Cr::allocator[gpu::SyncToken](javascript:void(0);)> const&) ./../../gpu/ipc/service/command\_buffer\_stub.cc:507:22  

#18 0x5592e8a909b8 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command\_buffer\_stub.cc:153:7  

#19 0x5592e8ab00ba in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)) ./../../gpu/ipc/service/gpu\_channel.cc:873:13  

#20 0x5592e8ac3386 in void base::internal::FunctorTraits<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), void>::Invoke<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);) const&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)>(void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);) const&, mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)&&) ./../../base/functional/bind\_internal.h:713:12  

#21 0x5592e8ac3172 in MakeItSo<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), std::\_\_Cr::tuple<base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) > > ./../../base/functional/bind\_internal.h:896:5  

#22 0x5592e8ac3172 in RunImpl<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), std::\_\_Cr::tuple<base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);) >, 0UL, 1UL> ./../../base/functional/bind\_internal.h:968:12  

#23 0x5592e8ac3172 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), base::WeakPtr[gpu::GpuChannel](javascript:void(0);), mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:919:1

**Additional Comments:**

\*\*Chrome version: \*\* 119.0.6041.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.4 KB)
- [asan.log](attachments/asan.log) (text/plain, 18.4 KB)

## Timeline

### [Deleted User] (2023-10-26)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-10-26)

[security shepherd] I can reproduce this issue. Setting severity high for this.

@hcm@chromium.org can you take a look a this?

[Monorail components: Internals>Skia]

### [Deleted User] (2023-10-31)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2023-10-31)

Behind a nonstandard flag, so impact=none.

### em...@gmail.com (2023-11-14)

Is there any new progress? I see no update in two weeks.
also repro with latest version. 
Chromium 121.0.6128.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1224132.zip)

Thanks.

### an...@chromium.org (2023-11-30)

[security shepherd] Since this feature is behind  a nonstandard flag, the priority is low. hcm@, do you plan to work on this issue soon? Is there someone else who you can hand off to? Also, is there a feature bug we can block with this bug?
Thanks!

### ja...@chromium.org (2023-12-13)

[security shepherd]

hcm@, can you update this bug by marking it as blocking a feature ticket? That'd help with ensuring we make progress on it. Thanks!

### hc...@google.com (2023-12-14)

My Chromium account was a long time ago supposed to be disabled so I didn't get notice on this one..passing to our GPU gardener for triage

### ah...@google.com (2023-12-22)

[secondary security shepherd]

Hello jamesgk@google.com,

Were you able to take a look at this?

Thanks!

### ja...@google.com (2024-01-02)

Sorry I wasn't able to look at this before taking off for the holidays.

I'm able to repro this with the copy of chrome at gs://chromium-browser-asan/linux-release/asan-linux-release-1215342.zip, but not with a local asan release build of chrome. Do we happen to know if this is reproducible on versions past 120?

### ph...@chromium.org (2024-01-19)

[security shepherd] I can't repro on my local asan release build nor can I repro with asan-linux-release-1249373.zip.  I wonder whether we can find out what fixes this via bisecting.

### ph...@chromium.org (2024-01-21)

I tried bisecting but the result is not consistent.  On Friday, I could repro on 6fa42d9f7ad03 on my first try but today I can't repro on the same revision after many tries.

### is...@google.com (2024-01-21)

This issue was migrated from crbug.com/chromium/1496202?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### xi...@chromium.org (2024-04-03)

[secondary security shepherd] Hi jamesgk@, is there any progress on this bug?

Reporter, since it has been several months since this report has filed, could you try to reproduce the issue with the current latest version?

### em...@gmail.com (2024-04-04)

I just tested the latest version and it cannot be reproduced. It should have been fixed a few months ago.

### am...@chromium.org (2024-04-26)

Hi jamesgk@ I've updated this as fixed since this issue has not been able to be reproduced. However, we need to understand what CL this issue was fixed by.
Adding jvanverth@ and egdaniel@ based on their recent Skia / ganesh work.

### jv...@google.com (2024-04-26)

Maybe fixed by this? <https://skia-review.googlesource.com/c/skia/+/769957> There was a somewhat similar crash that I added these checks for.

### am...@chromium.org (2024-04-26)

Thanks for taking a look, but I'm not sure that would be it based on the timing of repro here. This fix was landed in Skia and and rolled in Chromium M120 on 23 October and a month later this issue was still able to reproduced on 121 as per <https://issues.chromium.org/issues/40075655#comment6>

### am...@chromium.org (2024-05-02)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $10,000 for this report of GPU process memory corruption. Thank you for your efforts in discovering and reporting this issue to us!

### jv...@google.com (2024-05-03)

The only other possibility I see is this CL, which should pretty much be a no-op in the context of GrDrawOpAtlas: <https://skia-review.googlesource.com/c/skia/+/790076>. But it does affect GrDrawOpAtlas::uploadPlotToTexture so possibly? I'm not sure why it would make a difference though.

### pe...@google.com (2024-08-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075655)*
