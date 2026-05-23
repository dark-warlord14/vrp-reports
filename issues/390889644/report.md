# AddressSanitizer: heap-use-after-free sk_careful_memcpy 

| Field | Value |
|-------|-------|
| **Issue ID** | [390889644](https://issues.chromium.org/issues/390889644) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Fonts |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2025-01-19 |
| **Bounty** | $7,000.00 |

## Description

Security Bug
-------------------------

VULNERABILITY DETAILS


VERSION
Chrome Version: Version 134.0.6967.0 (Developer Build) (64-bit)
Operating System: Ubuntu 24.04.1 LTS

REPRODUCTION CASE
1. start a server: python3 -m http.server
2. ./chrome --no-sandbox --disable-gpu http://127.0.0.1:8000/poc.html

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

=================================================================
==11992==ERROR: AddressSanitizer: heap-use-after-free on address 0x7371850dae80 at pc 0x60b70194e4cb bp 0x71a1133fc190 sp 0x71a1133fb950
READ of size 1248 at 0x7371850dae80 thread T9 (ThreadPoolForeg)
==11992==WARNING: invalid path to external symbolizer!
==11992==WARNING: Failed to use and restart external symbolizer!
    #0 0x60b70194e4ca in __asan_memcpy _asan_rtl_:3
    #1 0x60b702682d64 in sk_careful_memcpy ./../../third_party/skia/include/private/base/SkMalloc.h:129:9
    #2 0x60b702682d64 in copy ./../../third_party/skia/include/private/base/SkTArray.h:656:17
    #3 0x60b702682d64 in TArray<4> ./../../third_party/skia/include/private/base/SkTArray.h:552:15
    #4 0x60b702682d64 in STArray ./../../third_party/skia/include/private/base/SkTArray.h:780:11
    #5 0x60b702682d64 in SkPathRef::SkPathRef(SkSpan<SkPoint const>, SkSpan<unsigned char const>, SkSpan<float const>, unsigned int) ./../../third_party/skia/include/private/SkPathRef.h:63:11
    #6 0x60b702681f3e in MakeInternal ./../../third_party/skia/src/core/SkPath.cpp:3576:38
    #7 0x60b702681f3e in SkPath::Make(SkPoint const*, int, unsigned char const*, int, float const*, int, SkPathFillType, bool) ./../../third_party/skia/src/core/SkPath.cpp:3530:12
    #8 0x60b71815e3a2 in SkFontationsScalerContext::generateYScalePathForGlyphId(unsigned short, SkPath*, float, fontations_ffi::BridgeHintingInstance const&) ./../../third_party/skia/src/ports/SkTypeface_fontations.cpp:415:17
    #9 0x60b71815eb74 in sk_fontations::ColorPainter::fill_glyph_solid(unsigned short, unsigned short, float) ./../../third_party/skia/src/ports/SkTypeface_fontations.cpp:1229:20
    #10 0x60b72e631340 in _$LT$skia_cbridge_urust_uside..ColorPainterImpl$u20$as$u20$skrifa..color..ColorPainter$GT$::fill_glyph::he43a3df9e065a2ec ./../../third_party/skia/src/ports/fontations/src/ffi.rs:422:17
    #11 0x60b72e673a5d in skrifa::color::traversal::traverse_v0_range::h81722d6410ab4c6e ./../../third_party/rust/chromium_crates_io/vendor/skrifa-0.26.4/src/color/traversal.rs:603:9
    #12 0x60b72e6707d0 in skrifa::color::ColorGlyph::paint::hab4db2b06726d0cd ./../../third_party/rust/chromium_crates_io/vendor/skrifa-0.26.4/src/color/mod.rs:375:17
    #13 0x60b72e6380a8 in skia_cbridge_urust_uside::draw_colr_glyph::_$u7b$$u7b$closure$u7d$$u7d$::h7a926702ba028d19 ./../../third_party/skia/src/ports/fontations/src/ffi.rs:1084:13
    #14 0x60b72e6380a8 in skia_cbridge_urust_uside::BridgeFontRef::with_font::h7694be5e9eeb7b74 ./../../third_party/skia/src/ports/fontations/src/ffi.rs:1262:9
    #15 0x60b72e6380a8 in skia_cbridge_urust_uside::draw_colr_glyph::ha7107a06ac4ef2f6 ./../../third_party/skia/src/ports/fontations/src/ffi.rs:1081:5
    #16 0x60b71816878d in SkFontationsScalerContext::drawCOLRGlyph(SkGlyph const&, unsigned int, SkCanvas*) ./../../third_party/skia/src/ports/SkTypeface_fontations.cpp:735:23
    #17 0x60b702546b22 in SkDrawable::draw(SkCanvas*, SkMatrix const*) ./../../third_party/skia/src/core/SkDrawable.cpp:48:11
    #18 0x60b702576ff1 in SkGlyphRunListPainterCPU::drawForBitmapDevice(SkCanvas*, SkGlyphRunListPainterCPU::BitmapDevicePainter const*, sktext::GlyphRunList const&, SkPaint const&, SkMatrix const&) ./../../third_party/skia/src/core/SkGlyphRunPainter.cpp:316:31
    #19 0x60b70249822c in SkBitmapDevice::onDrawGlyphRunList(SkCanvas*, sktext::GlyphRunList const&, SkPaint const&) ./../../third_party/skia/src/core/SkBitmapDevice.cpp:534:5
    #20 0x60b702500c94 in SkCanvas::onDrawGlyphRunList(sktext::GlyphRunList const&, SkPaint const&) ./../../third_party/skia/src/core/SkCanvas.cpp:2387:28
    #21 0x60b7025009f2 in SkCanvas::onDrawTextBlob(SkTextBlob const*, float, float, SkPaint const&) ./../../third_party/skia/src/core/SkCanvas.cpp:2372:11
    #22 0x60b702502840 in SkCanvas::drawTextBlob(SkTextBlob const*, float, float, SkPaint const&) ./../../third_party/skia/src/core/SkCanvas.cpp:2522:11
    #23 0x60b71a749d1a in cc::DrawTextBlobOp::RasterWithFlags(cc::DrawTextBlobOp const*, cc::PaintFlags const*, SkCanvas*, cc::PlaybackParams const&)::$_0::operator()(SkCanvas*, SkPaint const&) const ./../../cc/paint/paint_op.cc:1732:8
    #24 0x60b71a7267d7 in DrawToSk<(lambda at ../../cc/paint/paint_op.cc:1730:27)> ./../../cc/paint/paint_flags.h:283:7
    #25 0x60b71a7267d7 in cc::DrawTextBlobOp::RasterWithFlags(cc::DrawTextBlobOp const*, cc::PaintFlags const*, SkCanvas*, cc::PlaybackParams const&) ./../../cc/paint/paint_op.cc:1730:10
    #26 0x60b71a779b8b in cc::PaintOpBuffer::Playback(SkCanvas*, cc::PlaybackParams const&, bool, std::__Cr::vector<unsigned long, std::__Cr::allocator<unsigned long>> const*) const ./../../cc/paint/paint_op_buffer.cc:407:18
    #27 0x60b71a779a44 in cc::PaintOpBuffer::Playback(SkCanvas*, cc::PlaybackParams const&, bool, std::__Cr::vector<unsigned long, std::__Cr::allocator<unsigned long>> const*) const ./../../cc/paint/paint_op_buffer.cc:410:11
    #28 0x60b71a750fff in cc::DisplayItemList::Raster(SkCanvas*, cc::PlaybackParams const&) const ./../../cc/paint/display_item_list.cc:105:20
    #29 0x60b71ba6dc7f in cc::RasterSource::PlaybackDisplayListToCanvas(SkCanvas*, cc::RasterSource::PlaybackSettings const&) const ./../../cc/raster/raster_source.cc:132:20
    #30 0x60b71ba6d728 in cc::RasterSource::PlaybackToCanvas(SkCanvas*, gfx::Size const&, gfx::Rect const&, gfx::Rect const&, gfx::AxisTransform2d const&, cc::RasterSource::PlaybackSettings const&) const ./../../cc/raster/raster_source.cc:119:3
    #31 0x60b71bd46a7f in cc::RasterBufferProvider::PlaybackToMemory(void*, viz::SharedImageFormat, gfx::Size const&, unsigned long, cc::RasterSource const*, gfx::Rect const&, gfx::Rect const&, gfx::AxisTransform2d const&, gfx::ColorSpace const&, bool, cc::RasterSource::PlaybackSettings const&) ./../../cc/raster/raster_buffer_provider.cc:92:20
    #32 0x60b71bd463cf in cc::(anonymous namespace)::BitmapRasterBufferImpl::Playback(cc::RasterSource const*, gfx::Rect const&, gfx::Rect const&, unsigned long, gfx::AxisTransform2d const&, cc::RasterSource::PlaybackSettings const&, GURL const&) ./../../cc/raster/bitmap_raster_buffer_provider.cc:90:5
    #33 0x60b71bad359f in cc::(anonymous namespace)::RasterTaskImpl::RunOnWorkerThread() ./../../cc/tiles/tile_manager.cc:151:21
    #34 0x60b72823b883 in cc::CategorizedWorkerPoolJob::Run(base::span<cc::TaskCategory const, 18446744073709551615ul, cc::TaskCategory const*>, base::JobDelegate*) ./../../cc/raster/categorized_worker_pool.cc:275:29
    #35 0x60b72824364c in Invoke<void (cc::CategorizedWorkerPoolJob::*)(base::span<const cc::TaskCategory, 18446744073709551615UL, const cc::TaskCategory *>, base::JobDelegate *), cc::CategorizedWorkerPoolJob *, const base::span<const cc::TaskCategory, 18446744073709551615UL, const cc::TaskCategory *> &, base::JobDelegate *> ./../../base/functional/bind_internal.h:729:12
    #36 0x60b72824364c in MakeItSo<void (cc::CategorizedWorkerPoolJob::*const &)(base::span<const cc::TaskCategory, 18446744073709551615UL, const cc::TaskCategory *>, base::JobDelegate *), const std::__Cr::tuple<base::internal::UnretainedWrapper<cc::CategorizedWorkerPoolJob, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::span<const cc::TaskCategory, 18446744073709551615UL, const cc::TaskCategory *> > &, base::JobDelegate *> ./../../base/functional/bind_internal.h:921:12
    #37 0x60b72824364c in RunImpl<void (cc::CategorizedWorkerPoolJob::*const &)(base::span<const cc::TaskCategory, 18446744073709551615UL, const cc::TaskCategory *>, base::JobDelegate *), const std::__Cr::tuple<base::internal::UnretainedWrapper<cc::CategorizedWorkerPoolJob, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::span<const cc::TaskCategory, 18446744073709551615UL, const cc::TaskCategory *> > &, 0UL, 1UL> ./../../base/functional/bind_internal.h:1058:14
    #38 0x60b72824364c in base::internal::Invoker<base::internal::FunctorTraits<void (cc::CategorizedWorkerPoolJob::* const&)(base::span<cc::TaskCategory const, 18446744073709551615ul, cc::TaskCategory const*>, base::JobDelegate*), cc::CategorizedWorkerPoolJob*, base::span<cc::TaskCategory const, 18446744073709551615ul, cc::TaskCategory const*> const&>, base::internal::BindState<true, true, false, void (cc::CategorizedWorkerPoolJob::*)(base::span<cc::TaskCategory const, 18446744073709551615ul, cc::TaskCategory const*>, base::JobDelegate*), base::internal::UnretainedWrapper<cc::CategorizedWorkerPoolJob, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::span<cc::TaskCategory const, 18446744073709551615ul, cc::TaskCategory const*>>, void (base::JobDelegate*)>::Run(base::internal::BindStateBase*, base::JobDelegate*) ./../../base/functional/bind_internal.h:978:12
    #39 0x60b71643cb13 in base::RepeatingCallback<void (base::JobDelegate*)>::Run(base::JobDelegate*) const & ./../../base/functional/callback.h:344:12
    #40 0x60b71643e021 in operator() ./../../base/task/thread_pool/job_task_source.cc:101:32
    #41 0x60b71643e021 in Invoke<const (lambda at ../../base/task/thread_pool/job_task_source.cc:97:11) &, base::internal::JobTaskSource *> ./../../base/functional/bind_internal.h:647:12
    #42 0x60b71643e021 in MakeItSo<const (lambda at ../../base/task/thread_pool/job_task_source.cc:97:11) &, const std::__Cr::tuple<base::internal::UnretainedWrapper<base::internal::JobTaskSource, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &> ./../../base/functional/bind_internal.h:921:12
    #43 0x60b71643e021 in RunImpl<const (lambda at ../../base/task/thread_pool/job_task_source.cc:97:11) &, const std::__Cr::tuple<base::internal::UnretainedWrapper<base::internal::JobTaskSource, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind_internal.h:1058:14
    #44 0x60b71643e021 in base::internal::Invoker<base::internal::FunctorTraits<base::internal::JobTaskSource::JobTaskSource(base::Location const&, base::TaskTraits const&, base::RepeatingCallback<void (base::JobDelegate*)>, base::RepeatingCallback<unsigned long (unsigned long)>, base::internal::PooledTaskRunnerDelegate*)::$_0 const&, base::internal::JobTaskSource*>, base::internal::BindState<false, false, false, base::internal::JobTaskSource::JobTaskSource(base::Location const&, base::TaskTraits const&, base::RepeatingCallback<void (base::JobDelegate*)>, base::RepeatingCallback<unsigned long (unsigned long)>, base::internal::PooledTaskRunnerDelegate*)::$_0, base::internal::UnretainedWrapper<base::internal::JobTaskSource, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::Run(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:978:12
    #45 0x60b7163b78c2 in Run ./../../base/functional/callback.h:156:12
    #46 0x60b7163b78c2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:210:34
    #47 0x60b71644589a in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:692:35)> ./../../base/task/common/task_annotator.h:106:5
    #48 0x60b71644589a in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:691:19
    #49 0x60b716445aec in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:676:3
    #50 0x60b7164440c4 in RunTaskWithShutdownBehavior ./../../base/task/thread_pool/task_tracker.cc:706:7
    #51 0x60b7164440c4 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) ./../../base/task/thread_pool/task_tracker.cc:504:5
    #52 0x60b716442ff4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread_pool/task_tracker.cc:394:5
    #53 0x60b716489623 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread_pool/worker_thread.cc:473:36
    #54 0x60b716488757 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread_pool/worker_thread.cc:359:3
    #55 0x60b71648823e in base::internal::WorkerThread::ThreadMain() ./../../base/task/thread_pool/worker_thread.cc:339:7
    #56 0x60b7164f4499 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #57 0x60b70194e106 in asan_thread_start(void*) _asan_rtl_:28

0x7371850dae80 is located 0 bytes inside of 2400-byte region [0x7371850dae80,0x7371850db7e0)
freed by thread T4 (ThreadPoolForeg) here:
    #0 0x60b701950b0c in ___interceptor_realloc _asan_rtl_:3
    #1 0x60b72e558c59 in std::sys::alloc::unix::_$LT$impl$u20$core..alloc..global..GlobalAlloc$u20$for$u20$std..alloc..System$GT$::realloc::h11a5d5329483a32c ./../../third_party/rust-toolchain/lib/rustlib/src/rust/library/std/src/sys/alloc/unix.rs:54:22
    #2 0x60b72e558c59 in __rdl_realloc ./../../third_party/rust-toolchain/lib/rustlib/src/rust/library/std/src/alloc.rs:423:13
    #3 0x60b72e6521d6 in alloc::alloc::realloc::h8c51c1edd9c20eee ./../../third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:136:14
    #4 0x60b72e6521d6 in _$LT$alloc..alloc..Global$u20$as$u20$core..alloc..Allocator$GT$::shrink::h3f698d6a856191d8 ./../../third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:322:31
    #5 0x60b72e6521d6 in alloc::raw_vec::RawVecInner$LT$A$GT$::shrink_unchecked::hb40c2a131e341503 ./../../third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/raw_vec.rs:729:17

previously allocated by thread T9 (ThreadPoolForeg) here:
    #0 0x60b701950b0c in ___interceptor_realloc _asan_rtl_:3
    #1 0x60b72e558c59 in std::sys::alloc::unix::_$LT$impl$u20$core..alloc..global..GlobalAlloc$u20$for$u20$std..alloc..System$GT$::realloc::h11a5d5329483a32c ./../../third_party/rust-toolchain/lib/rustlib/src/rust/library/std/src/sys/alloc/unix.rs:54:22
    #2 0x60b72e558c59 in __rdl_realloc ./../../third_party/rust-toolchain/lib/rustlib/src/rust/library/std/src/alloc.rs:423:13
    #3 0x60b72e65186e in alloc::alloc::realloc::h8c51c1edd9c20eee ./../../third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:136:14
    #4 0x60b72e65186e in alloc::alloc::Global::grow_impl::hd19f76f233ffb281 ./../../third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:225:31
    #5 0x60b72e65186e in _$LT$alloc..alloc..Global$u20$as$u20$core..alloc..Allocator$GT$::grow::hbd0cb9ec9a691fe8 ./../../third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:282:18
    #6 0x60b72e65186e in alloc::raw_vec::finish_grow::hcce11a4b3c274f51 ./../../third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/raw_vec.rs:775:13

Thread T9 (ThreadPoolForeg) created by T3 (ThreadPoolForeg) here:
    #0 0x60b701934b41 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x60b7164f3a18 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:151:13
    #2 0x60b7164872ce in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) ./../../base/task/thread_pool/worker_thread.cc:185:3
    #3 0x60b7164477cc in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() ./../../base/task/thread_pool/thread_group.cc:88:13
    #4 0x60b71644730f in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() ./../../base/task/thread_pool/thread_group.cc:79:3
    #5 0x60b71646e8da in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() ./../../base/task/thread_pool/thread_group_impl.cc:43:3
    #6 0x60b71646f0cc in base::internal::ThreadGroupImpl::PushTaskSourceAndWakeUpWorkers(base::internal::RegisteredTaskSourceAndTransaction) ./../../base/task/thread_pool/thread_group_impl.cc:269:1
    #7 0x60b7164553c2 in base::internal::ThreadPoolImpl::PostTaskWithSequenceNow(base::internal::Task, scoped_refptr<base::internal::Sequence>) ./../../base/task/thread_pool/thread_pool_impl.cc:439:38
    #8 0x60b71645598a in base::internal::ThreadPoolImpl::PostTaskWithSequence(base::internal::Task, scoped_refptr<base::internal::Sequence>) ./../../base/task/thread_pool/thread_pool_impl.cc:462:12
    #9 0x60b716453e89 in base::internal::ThreadPoolImpl::PostDelayedTask(base::Location const&, base::TaskTraits const&, base::OnceCallback<void ()>, base::TimeDelta) ./../../base/task/thread_pool/thread_pool_impl.cc:251:10
    #10 0x60b71643b3ee in PostDelayedTask ./../../base/task/thread_pool.cc:66:31
    #11 0x60b71643b3ee in base::ThreadPool::PostTask(base::Location const&, base::TaskTraits const&, base::OnceCallback<void ()>) ./../../base/task/thread_pool.cc:57:10
    #12 0x60b71258b8ad in blink::worker_pool::PostTask(base::Location const&, base::TaskTraits const&, WTF::CrossThreadOnceFunction<void ()>) ./../../third_party/blink/renderer/platform/scheduler/common/worker_pool.cc:23:3
    #13 0x60b725c3bb0e in blink::BackgroundResourceScriptStreamer::BackgroundProcessor::MaybeStartProcessingResponse(mojo::StructPtr<network::mojom::URLResponseHead>&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&, std::__Cr::optional<mojo_base::BigBuffer>&, scoped_refptr<base::SequencedTaskRunner>, blink::BackgroundResponseProcessor::Client*) ./../../third_party/blink/renderer/bindings/core/v8/script_streamer.cc:1456:5
    #14 0x60b7127a2480 in blink::BackgroundURLLoader::Context::RequestClient::OnReceivedResponse(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>) ./../../third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:335:45
    #15 0x60b7127eced2 in blink::ResourceRequestSender::OnReceivedResponse(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, base::TimeTicks) ./../../third_party/blink/renderer/platform/loader/fetch/url_loader/resource_request_sender.cc:515:26
    #16 0x60b7127c70a4 in blink::MojoURLLoaderClient::OnReceiveResponse(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>) ./../../third_party/blink/renderer/platform/loader/fetch/url_loader/mojo_url_loader_client.cc:312:31
    #17 0x60b706be784d in blink::ThrottlingURLLoader::OnReceiveResponse(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>) ./../../third_party/blink/common/loader/throttling_url_loader.cc:699:23
    #18 0x60b7034ea014 in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient*, mojo::Message*) ./gen/services/network/public/mojom/url_loader.mojom.cc:1263:13
    #19 0x60b7161b4f8a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1051:54
    #20 0x60b7161d092a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #21 0x60b7161ba90e in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:724:20
    #22 0x60b7161df4da in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1121:42
    #23 0x60b7161dd76f in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:734:7
    #24 0x60b7161d092a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #25 0x60b7161ac4da in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:562:49
    #26 0x60b7161adeb0 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:620:14
    #27 0x60b7161ad8d9 in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:452:3
    #28 0x60b7161ad8d9 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:418:3
    #29 0x60b7161af1aa in Invoke<void (mojo::Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> ./../../base/functional/bind_internal.h:729:12
    #30 0x60b7161af1aa in MakeItSo<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind_internal.h:921:12
    #31 0x60b7161af1aa in RunImpl<void (mojo::Connector::*const &)(const char *, unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> ./../../base/functional/bind_internal.h:1058:14
    #32 0x60b7161af1aa in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) ./../../base/functional/bind_internal.h:978:12
    #33 0x60b706bda3e2 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/functional/callback.h:344:12
    #34 0x60b706bda16f in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:662:12
    #35 0x60b706bda16f in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind_internal.h:921:12
    #36 0x60b706bda16f in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind_internal.h:1058:14
    #37 0x60b706bda16f in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind_internal.h:978:12
    #38 0x60b716ecf145 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/functional/callback.h:344:12
    #39 0x60b716ecea73 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:278:14
    #40 0x60b716ecfc1b in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind_internal.h:729:12
    #41 0x60b716ecfc1b in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind_internal.h:945:5
    #42 0x60b716ecfc1b in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/functional/bind_internal.h:1058:14
    #43 0x60b7163b78c2 in Run ./../../base/functional/callback.h:156:12
    #44 0x60b7163b78c2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:210:34
    #45 0x60b71644589a in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:692:35)> ./../../base/task/common/task_annotator.h:106:5
    #46 0x60b71644589a in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:691:19
    #47 0x60b716445aec in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:676:3
    #48 0x60b7164440c4 in RunTaskWithShutdownBehavior ./../../base/task/thread_pool/task_tracker.cc:706:7
    #49 0x60b7164440c4 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) ./../../base/task/thread_pool/task_tracker.cc:504:5
    #50 0x60b716442ff4 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread_pool/task_tracker.cc:394:5
    #51 0x60b716489623 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread_pool/worker_thread.cc:473:36
    #52 0x60b716488757 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread_pool/worker_thread.cc:359:3
    #53 0x60b71648823e in base::internal::WorkerThread::ThreadMain() ./../../base/task/thread_pool/worker_thread.cc:339:7
    #54 0x60b7164f4499 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #55 0x60b70194e106 in asan_thread_start(void*) _asan_rtl_:28

Thread T3 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x60b701934b41 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x60b7164f3a18 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:151:13
    #2 0x60b7164872ce in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) ./../../base/task/thread_pool/worker_thread.cc:185:3
    #3 0x60b7164477cc in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() ./../../base/task/thread_pool/thread_group.cc:88:13
    #4 0x60b71644730f in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() ./../../base/task/thread_pool/thread_group.cc:79:3
    #5 0x60b71646e8da in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() ./../../base/task/thread_pool/thread_group_impl.cc:43:3
    #6 0x60b71646e3ae in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>) ./../../base/task/thread_pool/thread_group_impl.cc:249:1
    #7 0x60b716453119 in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*) ./../../base/task/thread_pool/thread_pool_impl.cc:189:35
    #8 0x60b72423e9c5 in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) ./../../content/child/child_process.cc:101:20
    #9 0x60b72d985f2b in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) ./../../content/renderer/render_process.cc:18:7
    #10 0x60b72d9857b5 in content::RenderProcessImpl::RenderProcessImpl() ./../../content/renderer/render_process_impl.cc:107:7
    #11 0x60b72d985d10 in content::RenderProcessImpl::Create() ./../../content/renderer/render_process_impl.cc:226:31
    #12 0x60b72da051c9 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:279:53
    #13 0x60b71349b194 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:678:14
    #14 0x60b71349c05d in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:782:12
    #15 0x60b71349e8f5 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1142:10
    #16 0x60b71349952d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:348:36
    #17 0x60b713499b1b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:361:10
    #18 0x60b70198bb1a in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #19 0x75a186e2a1c9 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #20 0x75a186e2a28a in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #21 0x60b7018b1029 in _start ??:0:0

Thread T4 (ThreadPoolForeg) created by T3 (ThreadPoolForeg) here:
    #0 0x60b701934b41 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x60b7164f3a18 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:151:13
    #2 0x60b7164872ce in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) ./../../base/task/thread_pool/worker_thread.cc:185:3
    #3 0x60b7164477cc in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() ./../../base/task/thread_pool/thread_group.cc:88:13
    #4 0x60b71644730f in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() ./../../base/task/thread_pool/thread_group.cc:79:3
    #5 0x60b71646e8da in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() ./../../base/task/thread_pool/thread_group_impl.cc:43:3
    #6 0x60b716470788 in base::internal::ThreadGroupImpl::WorkerDelegate::GetWork(base::internal::WorkerThread*) ./../../base/task/thread_pool/thread_group_impl.cc:449:1
    #7 0x60b716489441 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread_pool/worker_thread.cc:460:52
    #8 0x60b716488757 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread_pool/worker_thread.cc:359:3
    #9 0x60b71648823e in base::internal::WorkerThread::ThreadMain() ./../../base/task/thread_pool/worker_thread.cc:339:7
    #10 0x60b7164f4499 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #11 0x60b70194e106 in asan_thread_start(void*) _asan_rtl_:28

SUMMARY: AddressSanitizer: heap-use-after-free (/home/cr/dev/chrome/chrome+0xef484ca) (BuildId: 108374085a71c364)
Shadow bytes around the buggy address:
  0x7371850dac00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7371850dac80: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa
  0x7371850dad00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7371850dad80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7371850dae00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x7371850dae80:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7371850daf00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7371850daf80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7371850db000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7371850db080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7371850db100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==11992==ADDITIONAL INFO

==11992==Note: Please include this section with the ASan report.
Task trace:
    #0 0x60b72823b0ed in cc::CategorizedWorkerPoolJob::Start(int) ./../../cc/raster/categorized_worker_pool.cc:162:7
    #1 0x60b71be537a1 in cc::ProxyMain::BeginMainFrame(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>) ./../../cc/trees/proxy_main.cc:472:9
    #2 0x60b71be71391 in cc::ProxyImpl::ScheduledActionSendBeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/proxy_impl.cc:758:7


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=11941 --enable-crash-reporter=, --change-stack-guard-on-fork=enable --no-sandbox --file-url-path-alias=/gen=/home/cr/dev/chrome/gen --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1737287303110314 --launch-time-ticks=8733558559 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,7919204909938279777,16899972713523075039,2097152 --field-trial-handle=3,i,15683146650311825763,14835717324490625682,262144 --variations-seed-version`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==11992==END OF ADDITIONAL INFO
==11992==ABORTING


CREDIT INFORMATION
Reporter credit: TBA

## Attachments

- [poc.html](attachments/poc.html) (text/html, 465 B)
- [font.woff2](attachments/font.woff2) (application/octet-stream, 1.9 KB)
- [UaF_debug.log](attachments/UaF_debug.log) (text/plain, 35.4 KB)
- [repro.tar.gz](attachments/repro.tar.gz) (application/x-gzip, 2.4 KB)
- [UaF_new.log](attachments/UaF_new.log) (text/plain, 27.7 KB)
- [UaF_132.log](attachments/UaF_132.log) (text/plain, 28.5 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-01-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6411963617705984.

### se...@gmail.com (2025-01-20)

Despite the fact that ClusterFuzz reports it as unreproducible, I can replicate the issue on four different machines with distinct configurations.

1. Proxmox VM 13th Gen Intel(R) Core(TM) i5-13500, VGA compatible controller: Intel Corporation AlderLake-S GT1 (rev 0c), Ubuntu 24.04.1 LTS (Lubuntu distro). It does not require the --disable-gpu flag to reproduce the issue.

2. Desktop 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz, NVIDIA Corporation TU106M [GeForce RTX 2060 Mobile]. Ubuntu 24.04.1 LTS. It does require the --disable-gpu flag to reproduce the issue

3. KVM VM 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz VGA compatible controller: Red Hat, Inc. QXL paravirtual graphic card (rev 05). It does not require the --disable-gpu flag to reproduce the issue. To ensure this, I performed a clean base installation Ubuntu 24.04.1 LTS, and tested with linux-release_asan-linux-release-1408531.zip. 

4. KVM VM 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz, VGA compatible controller: Red Hat, Inc. Virtio 1.0 GPU (rev 01). It does not require --disable-gpu flag to reproduce the issue. Clean base installation of Fedora release 41. Tested with linux-release_asan-linux-release-1408538.zip and Canary chromium-134.0.6968.0-linux-asan.zip. 


### ad...@google.com (2025-01-20)

Well, I also can't reproduce this manually. I am using Linux ASAN release 1408531. I tried enabling the Fontations backend manually in chrome://flags but for some reason still can't trigger it.

Nevertheless from the ASAN trace provided, it seems pretty likely that this is a real UaF. I'm going to assume so. Because I can't reproduce it, I can't be sure what version it was introduced, so I'm assuming 134.

### ad...@google.com (2025-01-20)

Labeling as S1 for renderer RCE.

### se...@gmail.com (2025-01-20)

To rule out any issues that may have arisen from uploading the files. 
sha256sum a1604880a6945539f0c3f6499c7fbfedafadac01206f02ad5c4e1608bf141d06

### se...@gmail.com (2025-01-20)

1. UaF_new.log tested on chromium-134.0.6958.2-linux-asan.zip a different machine Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz Intel Corporation UHD Graphics 620, Fedora release 41. It requires the flag --disable-gpu to reproduce the issue:  ./chrome --no-sandbox --disable-gpu poc.html

2. UaF_132.log tested on chromium-132.0.6834.83-linux-asan.zip, same machine and distro. 




### dr...@chromium.org (2025-01-20)

The interesting bit of code is here: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/ports/SkTypeface_fontations.cpp;l=405>
I'll try to take a closer look. From `UaF_new.log` in [comment #7](https://issues.chromium.org/issues/390889644#comment7) it does looks like different threads are manipulating the path buffer, which I think does not match the assumption we had when designing this - can you comment on that Ben? Do we need a mutex around the path buffer? There seems to be an allocation by chrome, then a write access by a thread from a thread pool.

### pe...@google.com (2025-01-20)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2025-01-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2025-01-20)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### se...@gmail.com (2025-01-20)

Instead of completely disabling the GPU `--disable-gpu`, you can simply use `--disable-gpu-compositing`, which also causes this bug to be reproduced instantly. 

> I can't be sure what version it was introduced, so I'm assuming 134.

I do not reproduce the issue in version 130, so it should be vulnerable from versions 131 through 134.
The oldest version I have tested that reproduces this bug is chromium-131.0.6778.69-linux-asan.zip. 

### dr...@chromium.org (2025-01-21)

I can reproduce locally, will look into a fix.

### dr...@chromium.org (2025-01-21)

I think this was introduced by <https://chromiumdash.appspot.com/commit/2e873e1aa0a5005ea62c311189a0380924956931> and thus is reproducible from 131.0.6778.39 in Stable. Fix under review in <https://skia-review.googlesource.com/c/skia/+/938517>

### ap...@google.com (2025-01-21)

Project: skia  

Branch: main  

Author: Dominik Röttsches <[drott@chromium.org](mailto:drott@chromium.org)>  

Link:      <https://skia-review.googlesource.com/938517>

[Fontations] Protect path retrieval arrays with lock

---


Expand for full commit details
```
[Fontations] Protect path retrieval arrays with lock 
 
Addresses issue with concurrent access to SkFontationsScalerContext, in 
particular with regards to writing and resizing of path extraction 
buffers. 
 
Test: Manually verified with poc.html/font.woff2 from issue. 
Bug: chromium:390889644 
Cq-Include-Trybots: luci.skia.skia.primary:Build-Debian10-Clang-x86_64-Debug-Fontations,Build-Mac-Clang-x86_64-Debug-Fontations,Test-Debian10-Clang-GCE-CPU-AVX2-x86_64-Debug-All-NativeFonts_Fontations,Test-Mac12-Clang-MacBookPro16.2-CPU-AppleIntel-x86_64-Debug-All-NativeFonts_Fontations 
Change-Id: Ibf21569e80469a9991646586d15df50d18a669a1 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/938517 
Reviewed-by: Ben Wagner <bungeman@google.com> 
Reviewed-by: Dominik Röttsches <drott@google.com> 
Commit-Queue: Dominik Röttsches <drott@google.com>

```

---

Files:

- M `src/ports/SkTypeface_fontations.cpp`

---

Hash: 5a6323775b6cf0fe9602070836bcf2ea1c04348a  

Date:  Tue Jan 21 19:22:35 2025


---

### ap...@google.com (2025-01-21)

Project: chromium/src  

Branch: main  

Author: chromium-autoroll <[chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)>  

Link:      <https://chromium-review.googlesource.com/6186737>

Roll Skia from 40c262ff885d to 5a6323775b6c (2 revisions)

---


Expand for full commit details
```
Roll Skia from 40c262ff885d to 5a6323775b6c (2 revisions) 
 
https://skia.googlesource.com/skia.git/+log/40c262ff885d..5a6323775b6c 
 
2025-01-21 drott@chromium.org [Fontations] Protect path retrieval arrays with lock 
2025-01-21 skia-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from a9e496961117 to 8d5a282ee9ba (6 revisions) 
 
If this roll has caused a breakage, revert this CL and stop the roller 
using the controls here: 
https://autoroll.skia.org/r/skia-autoroll 
Please CC robertphillips@google.com,skiabot@google.com on the revert to ensure that a human 
is aware of the problem. 
 
To file a bug in Skia: https://bugs.chromium.org/p/skia/issues/entry 
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
 
To report a problem with the AutoRoller itself, please file a bug: 
https://issues.skia.org/issues/new?component=1389291&template=1850622 
 
Documentation for the AutoRoller is here: 
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
 
Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel 
Cq-Do-Not-Cancel-Tryjobs: true 
Bug: chromium:390889644 
Tbr: robertphillips@google.com 
Test: Test: Manually verified with poc.html/font.woff2 from issue. 
Change-Id: I874222bc38fc17005c2508501358bcd094cdfadb 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6186737 
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
Cr-Commit-Position: refs/heads/main@{#1409242}

```

---

Files:

- M `DEPS`
- M `third_party/skia`

---

Hash: 96fe4a9678b690fc67ebc615a318c2559234e520  

Date:  Tue Jan 21 12:57:34 2025


---

### dr...@chromium.org (2025-01-22)

Adrian, or folks from Chrome security, could you comment with your assessment on severity and your expectations on where to backport this? The report mentions `--disable-gpu` as a reproduction condition when run on native GPUs, whereas the switch is not needed when Chrome runs in a VM (likely because of lack of access to hardware acceleration).

I assume there may be situations where this issue would appear in a native, non-VM execution environment if the machine's GPU is on a hardware acceleration blocklist.

### ad...@google.com (2025-01-22)

As discussed via chat - automation will add merge requests based on the severity and FoundIn fields.

### dr...@chromium.org (2025-01-22)

Updated **FoundIn** to 131, compare [comment #14](https://issues.chromium.org/issues/390889644#comment14). A change that first appeared in 131.0.6778.39 most likely introduced this.

### se...@gmail.com (2025-01-22)

Note --disable-gpu-compositing also triggers this issue.  GPU-blocklist and machines without GPU accelerated compositing are affected. 

### se...@gmail.com (2025-01-23)

out of curiosity, shouldn't you remove the Uncomfirmed hotlist?. Thanks for the quick fix.

### am...@chromium.org (2025-01-27)

because security-impact and milestone was not updated to reflect the change in foundin-, automation did not update this issue with the appropriate merge review tags; I'm going to go ahead and add them now since we're already lagging behind on this

unfortunately, we'll need to wait to review/approve this fix tomorrow since M132 Stable RC for tomorrow's update has already been cut

### pe...@google.com (2025-01-27)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pe...@google.com (2025-01-27)

This issue appears to be blocking an upcoming release and is therefore an **Urgent Release Blocking Issue** as per <http://go/chrome-slo#release-blocking-issues>. Bumping the priority to P0 to better reflect the urgency.

If this is not a release blocking issue, please adjust the release block field. Adjusting the priority will have no affect, P0 will be re-applied whilever this is marked as a release blocking issue.

### pe...@google.com (2025-01-27)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pg...@google.com (2025-01-28)

Updating release block and priority given the new foundin

### se...@gmail.com (2025-01-29)

Just a quick question, with the recent priority changes and the manual updates to the merge review tags, is the fix for M132/M133 still expected to be included in next Tuesday’s advisory once it’s approved and reviewed? Thanks!

### pg...@google.com (2025-01-29)

This report will credited in our release notes once it is released - the timing for which is not yet certain.  

On that note, I see that your credit info is marked as "TBA" - let us know how you'd like to be credited! (unless that TBA doesn't mean "to be announced" and you'd like the credit to say verbatim "TBA")

### se...@gmail.com (2025-01-29)

Reporter credit: Francisco Alonso (@revskills)

### am...@chromium.org (2025-01-29)

<https://skia-review.googlesource.com/938517> approved for merges to M132 and M133, please merge this fix to M133 beta (branch 6943) and M132 Stable (branch 6834) at your earliest convenience, by EOD tomorrow, 30 January

### sp...@google.com (2025-01-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
baseline report of memory corruption in a sandboxed process / renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-29)

Congratulations Francisco! Thank you for your efforts and reporting this issue to us!

### dr...@chromium.org (2025-01-30)

> <https://skia-review.googlesource.com/938517> approved for merges to M132 and M133, please merge this fix to M133 beta (branch 6943) and M132 Stable (branch 6834) at your earliest convenience, by EOD tomorrow, 30 January

Just to clarify, I will merge to `chrome/m133` and `chrome/m132` Skia branches - and I believe this is sufficient for the changes to be picked up into a Chrome release build. armyressler@, could you please confirm that's the right process?

### dr...@chromium.org (2025-01-30)

Merges in CLs

- <https://skia-review.googlesource.com/c/skia/+/944396> M133
- <https://skia-review.googlesource.com/c/skia/+/944376> M132

### ap...@google.com (2025-01-30)

Project: skia  

Branch: chrome/m133  

Author: Dominik Röttsches <[drott@chromium.org](mailto:drott@chromium.org)>  

Link:      <https://skia-review.googlesource.com/944396>

[Cherry-pick][Fontations] Protect path retrieval arrays with lock

---


Expand for full commit details
```
[Cherry-pick][Fontations] Protect path retrieval arrays with lock 
 
Addresses issue with concurrent access to SkFontationsScalerContext, in 
particular with regards to writing and resizing of path extraction 
buffers. 
 
Test: Manually verified with poc.html/font.woff2 from issue. 
Bug: chromium:390889644 
Cq-Include-Trybots: luci.skia.skia.primary:Build-Debian10-Clang-x86_64-Debug-Fontations,Build-Mac-Clang-x86_64-Debug-Fontations,Test-Debian10-Clang-GCE-CPU-AVX2-x86_64-Debug-All-NativeFonts_Fontations,Test-Mac12-Clang-MacBookPro16.2-CPU-AppleIntel-x86_64-Debug-All-NativeFonts_Fontations 
Change-Id: Ibf21569e80469a9991646586d15df50d18a669a1 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/938517 
Reviewed-by: Ben Wagner <bungeman@google.com> 
Reviewed-by: Dominik Röttsches <drott@google.com> 
Commit-Queue: Dominik Röttsches <drott@google.com> 
(cherry picked from commit 5a6323775b6cf0fe9602070836bcf2ea1c04348a) 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/944396 
Commit-Queue: Ben Wagner <bungeman@google.com>

```

---

Files:

- M `src/ports/SkTypeface_fontations.cpp`

---

Hash: ecebe831881cdf52c65df518777210071f7970dd  

Date:  Tue Jan 21 19:22:35 2025


---

### ap...@google.com (2025-01-30)

Project: skia  

Branch: chrome/m132  

Author: Dominik Röttsches <[drott@chromium.org](mailto:drott@chromium.org)>  

Link:      <https://skia-review.googlesource.com/944376>

[Cherry-pick][Fontations] Protect path retrieval arrays with lock

---


Expand for full commit details
```
[Cherry-pick][Fontations] Protect path retrieval arrays with lock 
 
Addresses issue with concurrent access to SkFontationsScalerContext, in 
particular with regards to writing and resizing of path extraction 
buffers. 
 
Test: Manually verified with poc.html/font.woff2 from issue. 
Bug: chromium:390889644 
Cq-Include-Trybots: luci.skia.skia.primary:Build-Debian10-Clang-x86_64-Debug-Fontations,Build-Mac-Clang-x86_64-Debug-Fontations,Test-Debian10-Clang-GCE-CPU-AVX2-x86_64-Debug-All-NativeFonts_Fontations,Test-Mac12-Clang-MacBookPro16.2-CPU-AppleIntel-x86_64-Debug-All-NativeFonts_Fontations 
Change-Id: Ibf21569e80469a9991646586d15df50d18a669a1 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/938517 
Reviewed-by: Ben Wagner <bungeman@google.com> 
Reviewed-by: Dominik Röttsches <drott@google.com> 
Commit-Queue: Dominik Röttsches <drott@google.com> 
(cherry picked from commit 5a6323775b6cf0fe9602070836bcf2ea1c04348a) 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/944376 
Commit-Queue: Ben Wagner <bungeman@google.com>

```

---

Files:

- M `src/ports/SkTypeface_fontations.cpp`

---

Hash: ee9db7d1348f76780fd0184b9b0243d653e36411  

Date:  Tue Jan 21 19:22:35 2025


---

### dr...@chromium.org (2025-01-30)

Amy, both merges have been landed.

### ap...@google.com (2025-01-30)

Project: skia  

Branch: chrome/m133  

Author: Dominik Röttsches <[drott@chromium.org](mailto:drott@chromium.org)>  

Link:      <https://skia-review.googlesource.com/944396>

[Cherry-pick][Fontations] Protect path retrieval arrays with lock

---


Expand for full commit details
```
[Cherry-pick][Fontations] Protect path retrieval arrays with lock 
 
Addresses issue with concurrent access to SkFontationsScalerContext, in 
particular with regards to writing and resizing of path extraction 
buffers. 
 
Test: Manually verified with poc.html/font.woff2 from issue. 
Bug: chromium:390889644 
Cq-Include-Trybots: luci.skia.skia.primary:Build-Debian10-Clang-x86_64-Debug-Fontations,Build-Mac-Clang-x86_64-Debug-Fontations,Test-Debian10-Clang-GCE-CPU-AVX2-x86_64-Debug-All-NativeFonts_Fontations,Test-Mac12-Clang-MacBookPro16.2-CPU-AppleIntel-x86_64-Debug-All-NativeFonts_Fontations 
Change-Id: Ibf21569e80469a9991646586d15df50d18a669a1 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/938517 
Reviewed-by: Ben Wagner <bungeman@google.com> 
Reviewed-by: Dominik Röttsches <drott@google.com> 
Commit-Queue: Dominik Röttsches <drott@google.com> 
(cherry picked from commit 5a6323775b6cf0fe9602070836bcf2ea1c04348a) 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/944396 
Commit-Queue: Ben Wagner <bungeman@google.com>

```

---

Files:

- M `src/ports/SkTypeface_fontations.cpp`

---

Hash: ecebe831881cdf52c65df518777210071f7970dd  

Date:  Tue Jan 21 19:22:35 2025


---

### pb...@google.com (2025-01-30)

Based on comment#37 given the changes are already hence updating the bug with Merge labels.

### ch...@google.com (2025-05-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> baseline report of memory corruption in a sandboxed process / renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/390889644)*
