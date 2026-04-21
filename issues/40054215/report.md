# crash in gpu::gles2::GLES2Implementation::ReadPixels

| Field | Value |
|-------|-------|
| **Issue ID** | [40054215](https://issues.chromium.org/issues/40054215) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | va...@chromium.org |
| **Created** | 2020-12-18 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36

Steps to reproduce the problem:

version:
Ubuntu 20.04
chrome version:Google Chrome 89.0.4350.4 dev (office build without asan)
chrome version:Chromium 89.0.4355.0 with ASAN build

./chrome http://locahost:8000/crash.html
or
./chrome http://locahost:8000/wraper.html

When open  crash.html directly, the repro rate is about 30%.
I used site isolation abusing(127.0.0.1:8000/crash.html and localhost:8000/crash.html run in deffent process) in wraper.html,and the repro rate is 100% in my local tests.

What is the expected behavior?

What went wrong?
Received signal 11 SEGV_MAPERR 7f2485cfa000
[2120646:2120646:1218/215915.335506:ERROR:command_buffer_stub.cc(440)] Got WaitForGetOffset command while currently waiting for offset.
[2120646:2120646:1218/215915.335861:ERROR:gles2_cmd_decoder.cc(5997)] Error: 4 for Command kReadPixels
error: unknown argument '--demangle=True'
    #0 0x5564d3329b1b in __interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4186
    #1 0x5564d3329b1b in ?? ??:0
    #2 0x5564de66a559 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:833
    #3 0x5564de66a559 in ?? ??:0
    #4 0x5564de4545d3 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:198
    #5 0x5564de4545d3 in StackTrace ./../../base/debug/stack_trace.cc:195
    #6 0x5564de4545d3 in ?? ??:0
    #7 0x5564de66912f in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:345
    #8 0x5564de66912f in ?? ??:0
error: unknown argument '--demangle=True'
    #9 0x7f24a2ee23c0 in __funlockfile :?
    #10 0x7f24a2ee23c0 in ?? ??:0
    #11 0x5564e2cb5734 in gpu::gles2::GLES2Implementation::ReadPixels(int, int, int, int, unsigned int, unsigned int, void*) ./../../gpu/command_buffer/client/gles2_implementation.cc:?
    #12 0x5564e2cb5734 in ?? ??:0
    #13 0x5564d56bac67 in GrGLFunction<void (int, int, int, int, unsigned int, unsigned int, void*)>::GrGLFunction<(anonymous namespace)::gles_bind<void, int, int, int, int, unsigned int, unsigned int, void*>(void (gpu::gles2::GLES2Interface::*)(int, int, int, int, unsigned int, unsigned int, void*), gpu::gles2::GLES2Interface*, gpu::ContextSupport*)::{lambda(int, int, int, int, unsigned int, unsigned int, void*)#1}>((anonymous namespace)::gles_bind<void, int, int, int, int, unsigned int, unsigned int, void*>(void (gpu::gles2::GLES2Interface::*)(int, int, int, int, unsigned int, unsigned int, void*), gpu::gles2::GLES2Interface*, gpu::ContextSupport*)::{lambda(int, int, int, int, unsigned int, unsigned int, void*)#1})::{lambda(void const*, int, int, int, int, unsigned int, unsigned int, void*)#1}::__invoke(void const, int, int, int, int, unsigned int, unsigned int, void*) ./../../gpu/skia_bindings/gl_bindings_skia_cmd_buffer.cc:37
    #14 0x5564d56bac67 in operator() ./../../third_party/skia/include/gpu/gl/GrGLFunctions.h:316
    #15 0x5564d56bac67 in __invoke ./../../third_party/skia/include/gpu/gl/GrGLFunctions.h:314
    #16 0x5564d56bac67 in ?? ??:0
    #17 0x5564e0eecfd7 in GrGLGpu::readOrTransferPixelsFrom(GrSurface*, int, int, int, int, GrColorType, GrColorType, void*, int) ./../../third_party/skia/include/gpu/gl/GrGLFunctions.h:322
    #18 0x5564e0eecfd7 in readOrTransferPixelsFrom ./../../third_party/skia/src/gpu/gl/GrGLGpu.cpp:2119
    #19 0x5564e0eecfd7 in ?? ??:0
    #20 0x5564e0f00a81 in GrGLGpu::onReadPixels(GrSurface*, int, int, int, int, GrColorType, GrColorType, void*, unsigned long) ./../../third_party/skia/src/gpu/gl/GrGLGpu.cpp:2156
    #21 0x5564e0f00a81 in ?? ??:0
    #22 0x5564e0a43924 in GrGpu::readPixels(GrSurface*, int, int, int, int, GrColorType, GrColorType, void*, unsigned long) ./../../third_party/skia/src/gpu/GrGpu.cpp:407
    #23 0x5564e0a43924 in ?? ??:0
    #24 0x5564e0ac8bbe in GrSurfaceContext::readPixels(GrDirectContext*, GrImageInfo const&, void*, unsigned long, SkIPoint) ./../../third_party/skia/src/gpu/GrSurfaceContext.cpp:329
    #25 0x5564e0ac8bbe in ?? ??:0
    #26 0x5564e0d92230 in SkImage_GpuBase::onReadPixels(GrDirectContext*, SkImageInfo const&, void*, unsigned long, int, int, SkImage::CachingHint) const ./../../third_party/skia/src/image/SkImage_GpuBase.cpp:184
    #27 0x5564e0d92230 in ?? ??:0
    #28 0x5564d40736e7 in SkImage::makeRasterImage(SkImage::CachingHint) const ./../../third_party/skia/src/image/SkImage.cpp:57
    #29 0x5564d40736e7 in readPixels ./../../third_party/skia/src/image/SkImage.cpp:325
    #30 0x5564d40736e7 in makeRasterImage ./../../third_party/skia/src/image/SkImage.cpp:521
    #31 0x5564d40736e7 in ?? ??:0
    #32 0x5564d40731c2 in SkImage::makeNonTextureImage() const ./../../third_party/skia/src/image/SkImage.cpp:502
    #33 0x5564d40731c2 in ?? ??:0
    #34 0x5564ed408993 in blink::MailboxTextureBacking::GetSkImageViaReadback() ./../../third_party/blink/renderer/platform/graphics/mailbox_texture_backing.cc:78
    #35 0x5564ed408993 in ?? ??:0
    #36 0x5564e16da6d4 in cc::PaintImage::GetSwSkImage() const ./../../cc/paint/paint_image.cc:124
    #37 0x5564e16da6d4 in ?? ??:0
    #38 0x5564e2e3e577 in cc::PlaybackImageProvider::GetRasterContent(cc::DrawImage const&) ./../../cc/raster/playback_image_provider.cc:72
    #39 0x5564e2e3e577 in ?? ??:0
    #40 0x5564e2e0f639 in cc::(anonymous namespace)::DispatchingImageProvider::GetRasterContent(cc::DrawImage const&) ./../../cc/tiles/tile_manager.cc:66
    #41 0x5564e2e0f639 in ?? ??:0
    #42 0x5564e16ed339 in cc::DrawImageOp::RasterWithFlags(cc::DrawImageOp const*, cc::PaintFlags const*, SkCanvas*, cc::PlaybackParams const&) ./../../cc/paint/paint_op_buffer.cc:1493
    #43 0x5564e16ed339 in ?? ??:0
    #44 0x5564e16f8d6d in cc::PaintOpBuffer::Playback(SkCanvas*, cc::PlaybackParams const&, std::__1::vector<unsigned long, std::__1::allocator<unsigned long> > const*) const ./../../cc/paint/paint_op_buffer.cc:2486
    #45 0x5564e16f8d6d in Playback ./../../cc/paint/paint_op_buffer.cc:2887
    #46 0x5564e16f8d6d in ?? ??:0
    #47 0x5564e16fd54d in cc::$_14::__invoke(cc::PaintOp const*, SkCanvas*, cc::PlaybackParams const&) ./../../cc/paint/paint_op_buffer.cc:2747
    #48 0x5564e16fd54d in Raster ./../../cc/paint/paint_op_buffer.cc:1646
    #49 0x5564e16fd54d in Raster ./../../cc/paint/paint_op_buffer.cc:123
    #50 0x5564e16fd54d in operator() ./../../cc/paint/paint_op_buffer.cc:157
    #51 0x5564e16fd54d in __invoke ./../../cc/paint/paint_op_buffer.cc:157
    #52 0x5564e16fd54d in ?? ??:0
    #53 0x5564e16f8bb6 in cc::PaintOpBuffer::Playback(SkCanvas*, cc::PlaybackParams const&, std::__1::vector<unsigned long, std::__1::allocator<unsigned long> > const*) const ./../../cc/paint/paint_op_buffer.cc:2255
    #54 0x5564e16f8bb6 in Playback ./../../cc/paint/paint_op_buffer.cc:2890
    #55 0x5564e16f8bb6 in ?? ??:0
    #56 0x5564e16fd54d in Playback ./../../cc/paint/paint_op_buffer.cc:2747
    #57 0x5564e16fd54d in Raster ./../../cc/paint/paint_op_buffer.cc:1646
    #58 0x5564e16fd54d in Raster ./../../cc/paint/paint_op_buffer.cc:123
    #59 0x5564e16fd54d in operator() ./../../cc/paint/paint_op_buffer.cc:157
    #60 0x5564e16fd54d in __invoke ./../../cc/paint/paint_op_buffer.cc:157
    #61 0x5564e16fd54d in ?? ??:0
    #62 0x5564e16f8bb6 in Raster ./../../cc/paint/paint_op_buffer.cc:2255
    #63 0x5564e16f8bb6 in Playback ./../../cc/paint/paint_op_buffer.cc:2890
    #64 0x5564e16f8bb6 in ?? ??:0
    #65 0x5564e168a64e in cc::DisplayItemList::Raster(SkCanvas*, cc::ImageProvider*) const ./../../cc/paint/display_item_list.cc:100
    #66 0x5564e168a64e in ?? ??:0
    #67 0x5564e2dbf83f in cc::RasterSource::PlaybackDisplayListToCanvas(SkCanvas*, cc::ImageProvider*) const ./../../cc/raster/raster_source.cc:127
    #68 0x5564e2dbf83f in ?? ??:0
    #69 0x5564e2dbf3f9 in cc::RasterSource::PlaybackToCanvas(SkCanvas*, gfx::Size const&, gfx::Rect const&, gfx::Rect const&, gfx::AxisTransform2d const&, cc::RasterSource::PlaybackSettings const&) const ./../../cc/raster/raster_source.cc:116
    #70 0x5564e2dbf3f9 in ?? ??:0
    #71 0x5564e2f6eaf9 in cc::RasterBufferProvider::PlaybackToMemory(void*, viz::ResourceFormat, gfx::Size const&, unsigned long, cc::RasterSource const*, gfx::Rect const&, gfx::Rect const&, gfx::AxisTransform2d const&, gfx::ColorSpace const&, bool, cc::RasterSource::PlaybackSettings const&) ./../../cc/raster/raster_buffer_provider.cc:107
    #72 0x5564e2f6eaf9 in ?? ??:0
    #73 0x5564e2fa5d95 in cc::OneCopyRasterBufferProvider::PlaybackToStagingBuffer(cc::StagingBuffer*, cc::RasterSource const*, gfx::Rect const&, gfx::Rect const&, gfx::AxisTransform2d const&, viz::ResourceFormat, gfx::ColorSpace const&, cc::RasterSource::PlaybackSettings const&, unsigned long, unsigned long) ./../../cc/raster/one_copy_raster_buffer_provider.cc:355
    #74 0x5564e2fa5d95 in ?? ??:0
    #75 0x5564e2fa461c in cc::OneCopyRasterBufferProvider::PlaybackAndCopyOnWorkerThread(gpu::Mailbox*, unsigned int, bool, gpu::SyncToken const&, cc::RasterSource const*, gfx::Rect const&, gfx::Rect const&, gfx::AxisTransform2d const&, gfx::Size const&, viz::ResourceFormat, gfx::ColorSpace const&, cc::RasterSource::PlaybackSettings const&, unsigned long, unsigned long) ./../../cc/raster/one_copy_raster_buffer_provider.cc:291
    #76 0x5564e2fa461c in ?? ??:0
    #77 0x5564e2fa4325 in cc::OneCopyRasterBufferProvider::RasterBufferImpl::Playback(cc::RasterSource const*, gfx::Rect const&, gfx::Rect const&, unsigned long, gfx::AxisTransform2d const&, cc::RasterSource::PlaybackSettings const&, GURL const&) ./../../cc/raster/one_copy_raster_buffer_provider.cc:129
    #78 0x5564e2fa4325 in ?? ??:0
    #79 0x5564e2e151ff in cc::(anonymous namespace)::RasterTaskImpl::RunOnWorkerThread() ./../../cc/tiles/tile_manager.cc:132
    #80 0x5564e2e151ff in ?? ??:0
    #81 0x5564f1ca864b in content::CategorizedWorkerPool::RunTaskInCategoryWithLockAcquired(cc::TaskCategory) ./../../content/renderer/categorized_worker_pool.cc:430
    #82 0x5564f1ca864b in ?? ??:0
    #83 0x5564f1ca58eb in content::CategorizedWorkerPool::Run(std::__1::vector<cc::TaskCategory, std::__1::allocator<cc::TaskCategory> > const&, base::ConditionVariable*) ./../../content/renderer/categorized_worker_pool.cc:408
    #84 0x5564f1ca58eb in Run ./../../content/renderer/categorized_worker_pool.cc:292
    #85 0x5564f1ca58eb in ?? ??:0
    #86 0x5564de69f1a6 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:87
    #87 0x5564de69f1a6 in ?? ??:0
    #88 0x7f24a2ed6609 in start_thread /build/glibc-ZN95T4/glibc-2.31/nptl/pthread_create.c:477
    #89 0x7f24a2ed6609 in ?? ??:0
error: unknown argument '--demangle=True'
    #90 0x7f24a1161293 in clone ??:?
    #91 0x7f24a1161293 in ?? ??:0
  r8: 0000000000040000  r9: 0000000000040000 r10: 00000c1600018df1 r11: 00000000000005a7
 r12: 00000c1600018df1 r13: 00007f248f9320d0 r14: 000060b0000c6f8c r15: 000060b0000c6f94
  di: 000060b0000c6f8c  si: 0000000000020000  bp: 00007f2490900180  bx: 00007f24908fffc0
  dx: 0000000000000000  ax: 00007f2485cfa000  cx: 00000fe491ee9c50  sp: 00007f24908fffc0
  ip: 00005564e2cb5734 efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 00007f2485cfa000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: 87.0.4280.88  Channel: dev
OS Version: 20.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2020-12-18)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-12-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-12-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5763344819879936.

### cl...@chromium.org (2020-12-21)

ClusterFuzz testcase 5763344819879936 appears to be flaky, updating reproducibility label.

### ca...@chromium.org (2020-12-22)

I was able to reproduce this one.  zmo@ could you help find an owner for this? Thanks

[Monorail components: Internals>GPU>Internals]

### zm...@chromium.org (2020-12-22)

This looks like OOP-R related Skia code. GPU command buffer client side APIs isn't "safe", so using the APIs in the wrong way definitely could trigger crashes.

vtelezhnikov@: can you take a look?

### [Deleted User] (2020-12-22)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-01)

vtelezhnikov: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vt...@google.com (2021-01-11)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-01-11)

I reproduced on the ToT, cc::PaintImage::GetSwSkImage() happens on a wrong thread. This might be related to refactoring for OOP-R Canvas, not sure yet if this is regression or we just surfaced threading issue. 

+cc jochin@ and sushraja@ who work on OOP-R for canvas.

[2592637:12:0111/133154.040391:FATAL:GrSingleOwner.h(42)] assert(fOwner == self || fOwner == kIllegalThreadID)
#0 0x7f42a5771069 base::debug::CollectStackTrace()
#1 0x7f42a567a643 base::debug::StackTrace::StackTrace()
#2 0x7f42a569a783 logging::LogMessage::~LogMessage()
#3 0x7f42a44c72f5 SkAbort_FileLine()
#4 0x7f42a45dc7bf GrSingleOwner::enter()
#5 0x7f42a4620ead GrSurfaceContext::readPixels()
#6 0x7f42a470f2ab SkImage_GpuBase::onReadPixels()
#7 0x7f42a49bc434 SkImage::makeRasterImage()
#8 0x7f42a49bc20d SkImage::makeNonTextureImage()
#9 0x7f4299b02ffc blink::MailboxTextureBacking::GetSkImageViaReadback()
#10 0x7f42a40d3c6e cc::PaintImage::GetSwSkImage()
#11 0x7f429ff5ef5a cc::PlaybackImageProvider::GetRasterContent()
#12 0x7f429ffbaf05 cc::(anonymous namespace)::DispatchingImageProvider::GetRasterContent()
#13 0x7f42a40dc72a cc::DrawImageOp::RasterWithFlags()
#14 0x7f42a40e4799 cc::$_40::__invoke()
#15 0x7f42a40e2328 cc::PaintOpBuffer::Playback()
#16 0x7f42a40dd9e1 cc::$_15::__invoke()
#17 0x7f42a40e2254 cc::PaintOpBuffer::Playback()
#18 0x7f42a40dd9e1 cc::$_15::__invoke()
#19 0x7f42a40e2254 cc::PaintOpBuffer::Playback()
#20 0x7f42a40b92c9 cc::DisplayItemList::Raster()
#21 0x7f429ff6160b cc::RasterSource::PlaybackDisplayListToCanvas()
#22 0x7f429ff61579 cc::RasterSource::PlaybackToCanvas()
#23 0x7f429ff5f875 cc::RasterBufferProvider::PlaybackToMemory()
#24 0x7f429ff5ddc0 cc::OneCopyRasterBufferProvider::PlaybackToStagingBuffer()
#25 0x7f429ff5d2b3 cc::OneCopyRasterBufferProvider::PlaybackAndCopyOnWorkerThread()
#26 0x7f429ff5d18b cc::OneCopyRasterBufferProvider::RasterBufferImpl::Playback()
#27 0x7f429ffbbf5c cc::(anonymous namespace)::RasterTaskImpl::RunOnWorkerThread()
#28 0x7f42a2e71974 content::CategorizedWorkerPool::RunTaskInCategoryWithLockAcquired()
#29 0x7f42a2e7087b content::CategorizedWorkerPool::Run()
#30 0x7f42a578b4fe base::(anonymous namespace)::ThreadFunc()

The image was created itself from here:

#2 0x7f42a40d2faa cc::PaintImage::PaintImage()
#3 0x7f42a40d71ae cc::PaintImageBuilder::WithDefault()
#4 0x7f4299af3547 blink::Image::CreatePaintImageBuilder()
#5 0x7f4299a439ab blink::AcceleratedStaticBitmapImage::PaintImageForCurrentFrame()
#6 0x7f429ba1b42e blink::HTMLCanvasElement::ReplaceExisting2dLayerBridge()
#7 0x7f429ba1b1f2 blink::HTMLCanvasElement::DisableAcceleration()
#8 0x7f4296980da6 blink::CanvasRenderingContext2D::DisableAcceleration()
#9 0x7f429696a111 blink::BaseRenderingContext2D::fillRect()
#10 0x7f429665d6e0 blink::(anonymous namespace)::FillRectOperationCallback()


### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-26)

vasilyt: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-02-02)

+cc fserb for input.

So what happens in this case: 
We fallback to software canvas during fillRect operation, because pattern is not accelerated. [1]
This will create snapshot of current image [2] and paint it to new canvas [3]. This is recording canvas, so it will store the image and it will be accessed on a wrong thread later.

We need to readback this image, but I'm not sure what the best place is to do this. Should it be during ReplaceExisting2dLayerBridge if the new bridge is unaccelerated or should it be somewhere down the path?


[1] https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc;drc=b6496a2a60ea1712e46c32eb1be8d2e03d99af8b;l=875
[2] https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/html/canvas/html_canvas_element.cc;drc=b6496a2a60ea1712e46c32eb1be8d2e03d99af8b;l=1614
[3] https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/html/canvas/html_canvas_element.cc;drc=b6496a2a60ea1712e46c32eb1be8d2e03d99af8b;l=1652

### fs...@chromium.org (2021-02-02)

adding juanmi and aaron, who have done similiar things before.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b01bb3a0850e323369dd097ad3499501716820fc

commit b01bb3a0850e323369dd097ad3499501716820fc
Author: Vasiliy Telezhnikov <vasilyt@chromium.org>
Date: Tue Feb 02 16:51:30 2021

Add thread checks to MailboxTextureBacking

MailboxTextureBacking holds reference to either SkImage or context
provider and it's not safe to access it from different threads.

Bug: 1160258
Change-Id: I732d8f9b034f4edf9935f99400df19c849d2ca99
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2626775
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Cr-Commit-Position: refs/heads/master@{#849633}

[modify] https://crrev.com/b01bb3a0850e323369dd097ad3499501716820fc/third_party/blink/renderer/platform/graphics/mailbox_texture_backing.h
[modify] https://crrev.com/b01bb3a0850e323369dd097ad3499501716820fc/third_party/blink/renderer/platform/graphics/mailbox_texture_backing.cc


### rs...@chromium.org (2021-02-12)

Is this fixed with c#16?

### va...@chromium.org (2021-02-12)

No, CL in https://crbug.com/chromium/1160258#c16 just added dchecks.

### [Deleted User] (2021-02-16)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2021-02-17)

Security marshal here: did the DCHECKS help make progress towards a fix?

### va...@chromium.org (2021-02-17)

I was working on fix, but I suddenly can't repro problem anymore on ToT, something else has changed. I'll do a bisect.

### va...@chromium.org (2021-02-18)

Re https://crbug.com/chromium/1160258#c21 it was unrelated, bisected to https://chromium-review.googlesource.com/c/chromium/src/+/2645491 . It just made my environment to use software compositing where this doesn't reproduce. 

The fix for the problem is in CQ.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f01b9f02a9d63eb7ec5bdd000244bb1de2d2a79c

commit f01b9f02a9d63eb7ec5bdd000244bb1de2d2a79c
Author: Vasiliy Telezhnikov <vasilyt@chromium.org>
Date: Thu Feb 18 16:10:09 2021

Canvas: Readback PaintImage for DisableAcceleration

When switching Canvas2DLayerBridges we draw the image from old one to
new one. When old one was accelerated the PaintImage will be texture
backed and needs to be read back to draw on accelerated canvas.

Normally it would happen during the canvas draw, but there are some code
paths (e.g printing) that take recording of canvas and raster it on a
different thread. This might break because accelerated images are bound
to the thread they were created on.

This CL adds read back to ReplaceExistingCanvas2DLayerBridge to make
sure it will happen before any usage.

Bug: 1160258
Change-Id: I856c3d0adeb370d50baa2cd3cb9152bdb3799253
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2702841
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Cr-Commit-Position: refs/heads/master@{#855279}

[modify] https://crrev.com/f01b9f02a9d63eb7ec5bdd000244bb1de2d2a79c/third_party/blink/renderer/core/html/canvas/html_canvas_element.cc
[modify] https://crrev.com/f01b9f02a9d63eb7ec5bdd000244bb1de2d2a79c/cc/paint/paint_image_builder.cc


### va...@chromium.org (2021-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-19)

Requesting merge to beta M89 because latest trunk commit (855279) appears to be after beta branch point (843830).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-19)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-02-22)

+Adetaylor(Security TPM) for Merge Review

vasilyt@ Please reply to questions posted in https://crbug.com/chromium/1160258#c28

### va...@chromium.org (2021-02-22)

I'm not sure how large is security risk here, so I'll try to describe what's going on and answer the questions to https://crbug.com/chromium/1160258#c28 as much as I can.

To trigger the crash the page needs to fill canvas with pattern and immediately try to print the page. It will crash the renderer process sometimes (depends on timing of the threads). This quite specific setup, so I don't think we'll encounter this in normal pages, although because the issue is racy, I guess it's possible.

The underlying issue is that we access GrContext from two different threads which will use GLES2 Command Buffer. Neither of classes is thread safe.

1. I'm not sure, this change fixes the issue that can happen in very specific circumstances
2. https://chromium-review.googlesource.com/c/chromium/src/+/2702841
3. Yes
4. No?
5. Fixes crash, fix landed after branch.
6. No
7. N/A

### ad...@google.com (2021-02-22)

Thanks. Supposedly (from the Security_Impact) label this is an M89 regression. Even if it's hard to reliably reproduce, that doesn't necessarily mean it's hard to exploit (the attacker can keep trying!) so the high severity is probably valid. Approving merge to M89, branch 4389 even at this late stage.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bb28efa7bccc16747c6a042b8bd956c99199ec6a

commit bb28efa7bccc16747c6a042b8bd956c99199ec6a
Author: Vasiliy Telezhnikov <vasilyt@chromium.org>
Date: Tue Feb 23 00:03:30 2021

Canvas: Readback PaintImage for DisableAcceleration

When switching Canvas2DLayerBridges we draw the image from old one to
new one. When old one was accelerated the PaintImage will be texture
backed and needs to be read back to draw on accelerated canvas.

Normally it would happen during the canvas draw, but there are some code
paths (e.g printing) that take recording of canvas and raster it on a
different thread. This might break because accelerated images are bound
to the thread they were created on.

This CL adds read back to ReplaceExistingCanvas2DLayerBridge to make
sure it will happen before any usage.

(cherry picked from commit f01b9f02a9d63eb7ec5bdd000244bb1de2d2a79c)

Bug: 1160258
Change-Id: I856c3d0adeb370d50baa2cd3cb9152bdb3799253
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2702841
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#855279}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2713520
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4389@{#1294}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/bb28efa7bccc16747c6a042b8bd956c99199ec6a/third_party/blink/renderer/core/html/canvas/html_canvas_element.cc
[modify] https://crrev.com/bb28efa7bccc16747c6a042b8bd956c99199ec6a/cc/paint/paint_image_builder.cc


### am...@google.com (2021-02-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-25)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and nice work! 

### am...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1160258?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1160260]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054215)*
