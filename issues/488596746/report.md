# Skia JPEG MPF integer overflow in SkJpegMultiPictureParameters::Make leading to OOB Read/Write

| Field | Value |
|-------|-------|
| **Issue ID** | [488596746](https://issues.chromium.org/issues/488596746) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Images>Codecs |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | cc...@chromium.org |
| **Created** | 2026-03-01 |
| **Bounty** | $2,000.00 |

## Description

## VULNERABILITY DETAILS

A crafted JPEG with malformed MPF metadata triggers memory-unsafe behavior in Skia JPEG multi-picture parsing.

Root cause:

- In `SkJpegMultiPictureParameters::Make` (`third_party/skia/src/codec/SkJpegMultiPicture.cpp`), the parser validates MP-entry size with 32-bit arithmetic:
  - `mpEntriesData->size() != kMPEntrySize * numberOfImages`
- `kMPEntrySize` is 16 and `numberOfImages` is attacker-controlled from MPF tags.
- With `numberOfImages = 0x10000001`, `16 * numberOfImages` wraps in 32-bit to `0x10`, so a tiny 16-byte MP-entry buffer passes validation even though true required size is `0x100000010`.

This causes out-of-bounds reads when parsing MP entries (`SkCodecPriv::GetEndianInt`), and attacker-influenced writes into `SkJpegMultiPictureParameters::images[i]` fields (`size`, `dataOffset`) during the parse loop.

Crash Log:

```
=================================================================
==3856572==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7e6faf7a8857 at pc 0x7f6110c7bd39 bp 0x7ffd89b4a1e0 sp 0x7ffd89b4a1d8
READ of size 1 at 0x7e6faf7a8857 thread T0 (chrome)
    #0 0x7f6110c7bd38 in SkCodecPriv::GetEndianInt(unsigned char const*, bool) third_party/skia/src/codec/SkCodecPriv.h:292:35
    #1 0x7f6110d7a38d in SkJpegMultiPictureParameters::Make(sk_sp<SkData const> const&) third_party/skia/src/codec/SkJpegMultiPicture.cpp:183:36
    #2 0x7f6110d701be in find_mp_params(std::__Cr::vector<SkJpegMetadataDecoder::Segment, std::__Cr::allocator<SkJpegMetadataDecoder::Segment>> const&, SkJpegSourceMgr*, SkJpegSegment*) third_party/skia/src/codec/SkJpegMetadataDecoderImpl.cpp:61:20
    #3 0x7f6110d7205d in SkJpegMetadataDecoderImpl::mightHaveGainmapImage() const third_party/skia/src/codec/SkJpegMetadataDecoderImpl.cpp:474:12
    #4 0x7f5ff9e74847 in blink::JPEGImageDecoder::GetGainmapInfoAndData(SkGainmapInfo&, scoped_refptr<blink::SegmentReader>&) const third_party/blink/renderer/platform/image-decoders/jpeg/jpeg_image_decoder.cc:1003:26
    #5 0x7f600f2628fd in blink::DeferredImageDecoder::ActivateLazyGainmapDecoding() third_party/blink/renderer/platform/graphics/deferred_image_decoder.cc:372:27
    #6 0x7f600f261c4a in blink::DeferredImageDecoder::ActivateLazyDecoding() third_party/blink/renderer/platform/graphics/deferred_image_decoder.cc:334:3
    #7 0x7f600f260b27 in blink::DeferredImageDecoder::PrepareLazyDecodedFrames() third_party/blink/renderer/platform/graphics/deferred_image_decoder.cc:428:3
    #8 0x7f600f25d43e in blink::DeferredImageDecoder::SetDataInternal(scoped_refptr<blink::SharedBuffer>, bool, bool) third_party/blink/renderer/platform/graphics/deferred_image_decoder.cc:221:5
    #9 0x7f600f2605b9 in blink::DeferredImageDecoder::SetData(scoped_refptr<blink::SharedBuffer>, bool) third_party/blink/renderer/platform/graphics/deferred_image_decoder.cc:209:3
    #10 0x7f600ef5ae74 in blink::BitmapImage::SetData(scoped_refptr<blink::SharedBuffer>, bool) third_party/blink/renderer/platform/graphics/bitmap_image.cc:242:15
    #11 0x7f602e1816ff in blink::ImageResourceContent::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ResourceStatus, blink::ImageResourceContent::UpdateImageOption, bool, bool) third_party/blink/renderer/core/loader/resource/image_resource_content.cc:505:35
    #12 0x7f602e15501f in blink::ImageResource::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ImageResourceContent::UpdateImageOption, bool) third_party/blink/renderer/core/loader/resource/image_resource.cc:674:31
    #13 0x7f602e158899 in blink::ImageResource::Finish(base::TimeTicks, base::SingleThreadTaskRunner*) third_party/blink/renderer/core/loader/resource/image_resource.cc:545:5
    #14 0x7f6010447600 in blink::ResourceFetcher::HandleLoaderFinish(blink::Resource*, base::TimeTicks, blink::ResourceFetcher::LoaderFinishType, unsigned int) third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc:2534:15
    #15 0x7f6010560a96 in blink::ResourceLoader::DidFinishLoading(base::TimeTicks, long, unsigned long, long) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1133:13
    #16 0x7f601055cf10 in blink::ResourceLoader::DidFinishLoadingBody() third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:366:5
    #17 0x7f601060a1dd in blink::ResponseBodyLoader::DidFinishLoadingBody() third_party/blink/renderer/platform/loader/fetch/response_body_loader.cc:458:12
    #18 0x7f601060f82f in blink::ResponseBodyLoader::OnStateChange() third_party/blink/renderer/platform/loader/fetch/response_body_loader.cc:660:7
    #19 0x7f60102f6793 in blink::DataPipeBytesConsumer::SignalComplete() third_party/blink/renderer/platform/loader/fetch/data_pipe_bytes_consumer.cc:202:15
    #20 0x7f60102f5eca in blink::DataPipeBytesConsumer::CompletionNotifier::SignalComplete() third_party/blink/renderer/platform/loader/fetch/data_pipe_bytes_consumer.cc:21:22
    #21 0x7f601055fd6f in blink::ResourceLoader::DidFinishLoading(base::TimeTicks, long, unsigned long, long) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1114:39
    #22 0x7f6010675498 in blink::BackgroundURLLoader::Context::OnCompletedRequest(network::URLLoaderCompletionStatus const&) third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:526:16
    #23 0x7f6010675ee9 in void base::internal::DecayedFunctorTraits<void (blink::BackgroundURLLoader::Context::*)(network::URLLoaderCompletionStatus const&), scoped_refptr<blink::BackgroundURLLoader::Context>&&, network::URLLoaderCompletionStatus&&>::Invoke<void (blink::BackgroundURLLoader::Context::*)(network::URLLoaderCompletionStatus const&), scoped_refptr<blink::BackgroundURLLoader::Context>, network::URLLoaderCompletionStatus>(void (blink::BackgroundURLLoader::Context::*)(network::URLLoaderCompletionStatus const&), scoped_refptr<blink::BackgroundURLLoader::Context>&&, network::URLLoaderCompletionStatus&&) base/functional/bind_internal.h:740:12
    #24 0x7f6010675e30 in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(network::URLLoaderCompletionStatus const&), scoped_refptr<blink::BackgroundURLLoader::Context>&&, network::URLLoaderCompletionStatus&&>, void, 0ul, 1ul>::MakeItSo<void (blink::BackgroundURLLoader::Context::*)(network::URLLoaderCompletionStatus const&), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>, network::URLLoaderCompletionStatus>>(void (blink::BackgroundURLLoader::Context::*&&)(network::URLLoaderCompletionStatus const&), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>, network::URLLoaderCompletionStatus>&&) base/functional/bind_internal.h:932:12
    #25 0x7f6010675c51 in void base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(network::URLLoaderCompletionStatus const&), scoped_refptr<blink::BackgroundURLLoader::Context>&&, network::URLLoaderCompletionStatus&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(network::URLLoaderCompletionStatus const&), scoped_refptr<blink::BackgroundURLLoader::Context>, network::URLLoaderCompletionStatus>, void ()>::RunImpl<void (blink::BackgroundURLLoader::Context::*)(network::URLLoaderCompletionStatus const&), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>, network::URLLoaderCompletionStatus>, 0ul, 1ul>(void (blink::BackgroundURLLoader::Context::*&&)(network::URLLoaderCompletionStatus const&), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>, network::URLLoaderCompletionStatus>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/functional/bind_internal.h:1069:14
    #26 0x7f6010675ac8 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(network::URLLoaderCompletionStatus const&), scoped_refptr<blink::BackgroundURLLoader::Context>&&, network::URLLoaderCompletionStatus&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(network::URLLoaderCompletionStatus const&), scoped_refptr<blink::BackgroundURLLoader::Context>, network::URLLoaderCompletionStatus>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:982:12
    #27 0x7f600e7cba92 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
    #28 0x7f600ef1e004 in blink::CrossThreadOnceFunction<void ()>::Run() && third_party/blink/renderer/platform/wtf/functional.h:311:33
    #29 0x7f6010669a9c in blink::BackgroundURLLoader::Context::RunTasksOnMainThread() third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:454:23
    #30 0x7f601065d941 in void base::internal::DecayedFunctorTraits<void (blink::BackgroundURLLoader::Context::*)(), scoped_refptr<blink::BackgroundURLLoader::Context>&&>::Invoke<void (blink::BackgroundURLLoader::Context::*)(), scoped_refptr<blink::BackgroundURLLoader::Context>>(void (blink::BackgroundURLLoader::Context::*)(), scoped_refptr<blink::BackgroundURLLoader::Context>&&) base/functional/bind_internal.h:740:12
    #31 0x7f601065d887 in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(), scoped_refptr<blink::BackgroundURLLoader::Context>&&>, void, 0ul>::MakeItSo<void (blink::BackgroundURLLoader::Context::*)(), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>>>(void (blink::BackgroundURLLoader::Context::*&&)(), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>>&&) base/functional/bind_internal.h:932:12
    #32 0x7f601065d6f1 in void base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(), scoped_refptr<blink::BackgroundURLLoader::Context>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(), scoped_refptr<blink::BackgroundURLLoader::Context>>, void ()>::RunImpl<void (blink::BackgroundURLLoader::Context::*)(), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>>, 0ul>(void (blink::BackgroundURLLoader::Context::*&&)(), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1069:14
    #33 0x7f601065d588 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(), scoped_refptr<blink::BackgroundURLLoader::Context>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(), scoped_refptr<blink::BackgroundURLLoader::Context>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:982:12
    #34 0x7f6119e35d12 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
    #35 0x7f611a3628de in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:229:34
    #36 0x7f611a492f07 in void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_4>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_4&&) base/task/common/task_annotator.h:112:5
    #37 0x7f611a491efe in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:23
    #38 0x7f611a490c7a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #39 0x7f611a4923d2 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #40 0x7f6119fb18a4 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #41 0x7f611a494072 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #42 0x7f611a1ea787 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #43 0x7f61022244b5 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #44 0x7f6102d0e6ca in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #45 0x7f6102d0ff03 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #46 0x7f6102d136f6 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #47 0x7f6102d0954f in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #48 0x7f6102d0a3c5 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #49 0x556268331dc0 in ChromeMain chrome/app/chrome_main.cc:191:12
    #50 0x556268331621 in main chrome/app/chrome_exe_main_aura.cc:17:10
    #51 0x7f5fd8e4ed8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x7e6faf7a8857 is located 0 bytes after 65623-byte region [0x7e6faf798800,0x7e6faf7a8857)
allocated by thread T0 (chrome) here:
    #0 0x5562682ed694 in malloc (/mnt/lvm_data/chromium/src/out/asan_dbg_symbols/chrome+0xf386694) (BuildId: f1c93601b224f8ea)
    #1 0x7f5ffc01cd08 in chromium_jpeg_get_large third_party/libjpeg_turbo/src/jmemnobs.c:51:18
    #2 0x7f5ffc016a73 in alloc_large third_party/libjpeg_turbo/src/jmemmgr.c:392:29
    #3 0x7f5ffbff60fd in save_marker third_party/libjpeg_turbo/src/jdmarker.c:782:9
    #4 0x7f5ffbff3c38 in read_markers third_party/libjpeg_turbo/src/jdmarker.c:1082:12
    #5 0x7f5ffbfebb68 in consume_markers third_party/libjpeg_turbo/src/jdinput.c:339:9
    #6 0x7f5ffbfda4eb in chromium_jpeg_consume_input third_party/libjpeg_turbo/src/jdapimin.c:327:15
    #7 0x7f5ffbfda1e9 in chromium_jpeg_read_header third_party/libjpeg_turbo/src/jdapimin.c:275:13
    #8 0x7f5ff9e7c85a in blink::JPEGImageReader::Decode(blink::JPEGImageDecoder::DecodingMode) third_party/blink/renderer/platform/image-decoders/jpeg/jpeg_image_decoder.cc:386:13
    #9 0x7f5ff9e7418a in blink::JPEGImageDecoder::Decode(blink::JPEGImageDecoder::DecodingMode) third_party/blink/renderer/platform/image-decoders/jpeg/jpeg_image_decoder.cc:1346:17
    #10 0x7f5ff9e75566 in blink::JPEGImageDecoder::DecodeSize() third_party/blink/renderer/platform/image-decoders/jpeg/jpeg_image_decoder.cc:1088:3
    #11 0x7f5ff9e1ddd3 in blink::ImageDecoder::IsSizeAvailable() third_party/blink/renderer/platform/image-decoders/image_decoder.cc:488:5
    #12 0x7f600f260929 in blink::DeferredImageDecoder::PrepareLazyDecodedFrames() third_party/blink/renderer/platform/graphics/deferred_image_decoder.cc:411:49
    #13 0x7f600f25d43e in blink::DeferredImageDecoder::SetDataInternal(scoped_refptr<blink::SharedBuffer>, bool, bool) third_party/blink/renderer/platform/graphics/deferred_image_decoder.cc:221:5
    #14 0x7f600f25d09f in blink::DeferredImageDecoder::Create(scoped_refptr<blink::SharedBuffer>, bool, blink::ImageDecoder::AlphaOption, blink::ColorBehavior) third_party/blink/renderer/platform/graphics/deferred_image_decoder.cc:84:12
    #15 0x7f600ef5aeec in blink::BitmapImage::SetData(scoped_refptr<blink::SharedBuffer>, bool) third_party/blink/renderer/platform/graphics/bitmap_image.cc:247:14
    #16 0x7f602e1816ff in blink::ImageResourceContent::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ResourceStatus, blink::ImageResourceContent::UpdateImageOption, bool, bool) third_party/blink/renderer/core/loader/resource/image_resource_content.cc:505:35
    #17 0x7f602e15501f in blink::ImageResource::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ImageResourceContent::UpdateImageOption, bool) third_party/blink/renderer/core/loader/resource/image_resource.cc:674:31
    #18 0x7f602e15666b in blink::ImageResource::AppendData(std::__Cr::variant<blink::SegmentedBuffer, base::span<char const, 18446744073709551615ul, char const*>>) third_party/blink/renderer/core/loader/resource/image_resource.cc:457:7
    #19 0x7f6010597e55 in blink::ResourceLoader::DidReceiveDataImpl(std::__Cr::variant<blink::SegmentedBuffer, base::span<char const, 18446744073709551615ul, char const*>>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1053:14
    #20 0x7f601059cf9c in blink::ResourceLoader::DidReceiveData(base::span<char const, 18446744073709551615ul, char const*>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1027:3
    #21 0x7f601060817a in blink::ResponseBodyLoader::DidReceiveData(base::span<char const, 18446744073709551615ul, char const*>) third_party/blink/renderer/platform/loader/fetch/response_body_loader.cc:433:12
    #22 0x7f601060eca4 in blink::ResponseBodyLoader::OnStateChange() third_party/blink/renderer/platform/loader/fetch/response_body_loader.cc:642:9
    #23 0x7f601060c025 in blink::ResponseBodyLoader::Start() third_party/blink/renderer/platform/loader/fetch/response_body_loader.cc:515:3
    #24 0x7f601055a5ec in blink::ResourceLoader::DidStartLoadingResponseBodyInternal(blink::BytesConsumer&) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:345:28
    #25 0x7f6010588171 in blink::ResourceLoader::DidReceiveResponse(blink::WebURLResponse const&, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:786:3
    #26 0x7f60106716c0 in blink::BackgroundURLLoader::Context::OnReceivedResponse(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int) third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:492:14
    #27 0x7f60106722d8 in void base::internal::DecayedFunctorTraits<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>::Invoke<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int>(void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&, int&&) base/functional/bind_internal.h:740:12
    #28 0x7f6010671fde in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>, void, 0ul, 1ul, 2ul, 3ul>::MakeItSo<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>>, int>(void (blink::BackgroundURLLoader::Context::*&&)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>>&&, int&&) base/functional/bind_internal.h:932:12
    #29 0x7f6010671d43 in void base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>>, void (int)>::RunImpl<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>>, 0ul, 1ul, 2ul, 3ul>(void (blink::BackgroundURLLoader::Context::*&&)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), std::__Cr::tuple<scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>, int&&) base/functional/bind_internal.h:1069:14

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/src/codec/SkCodecPriv.h:292:35 in SkCodecPriv::GetEndianInt(unsigned char const*, bool)
Shadow bytes around the buggy address:
  0x7e6faf7a8580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e6faf7a8600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e6faf7a8680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e6faf7a8700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e6faf7a8780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7e6faf7a8800: 00 00 00 00 00 00 00 00 00 00[07]fa fa fa fa fa
  0x7e6faf7a8880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e6faf7a8900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e6faf7a8980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e6faf7a8a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7e6faf7a8a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==3856572==ADDITIONAL INFO

==3856572==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7f601066939a in blink::BackgroundURLLoader::Context::PostTaskToMainThread(blink::CrossThreadOnceFunction<void ()>) third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:422:52
    #1 0x7f61175c47b8 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:103:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=3840477 --enable-crash-reporter=, --noerrdialogs --user-data-dir=/tmp/chromium-cdp-profile-8_f83a6t --change-stack-guard-on-fork=enable --no-sandbox --disable-dev-shm-usage --remote-debugging-port=58341 --ozone-platform=headless --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=6 --time-ticks-at-unix-epoch=-1755397479121000 --launch-time-ticks=16919866895654 --shared-files=v8_context_snapshot_data:100 --field-trial-handle=3,i,18360823009163257586,8577354655934701638,262144 --disable-features=PaintHolding --variations-seed-version --pseudonymization-salt-handle=7,i,10546060741813747647,2610201529368585060,4 --trace-process-track-uuid=3362606884126403353 --enable-logging=stderr`


==3856572==END OF ADDITIONAL INFO

```
## VERSION

Chrome Version: 146.0.7639.0 (local Chromium Release build, dev/mainline-style) + dev
Operating System: Ubuntu 22.04.3 LTS (Jammy), Linux 5.15.0-151-generic x86\_64

## REPRODUCTION CASE

PoC files:

- `skia-mpf-get-endian-int-20260228_032208.html`

Directly opening it would crash with ASAN logs.

Type of crash: renderer/tab crash (target crash after file load)

## CREDIT INFORMATION

Reporter credit: heapracer (@heapracer)

## Attachments

- [skia-mpf-get-endian-int-20260228_032208.html](attachments/skia-mpf-get-endian-int-20260228_032208.html) (text/html, 87.8 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4913387221745664.

### 24...@project.gserviceaccount.com (2026-03-04)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-03-04)

Automatically assigning owner based on suspected regression changelist https://skia.googlesource.com/skia/+/ba721d5c6a1347a81c61fb30aee1b36d9e2fd263 (SkCodec: Consolidate Tiff parsing functions

Parsing of Apple HDR images will require extracting HDR parameters
from the MakerNote section of Exif metadata. This MakerNote data is
stored in a Tiff Image File Directory.

That will make the third place that Tiff IFD parsing will need to be
done (the other two being Exif and MPF). Chromium also has its own
bespoke Tiff IFD parser (which would make four).

Add the class SkTiffImageFileDirectory, which parses these structures,
and change SkJpegMultiPictureParameters and SkParseEncodedOrigin to
use them.

Add the class SkExifMetadata, with the intention that it will replace
the direct calls to SkParseEncodedOrigin, and will eventually be
used by Chromium (much like SkXmp can be today).

Bug: chromium:1488376
Change-Id: Ice1923dd98701ccaf2d790cff749bc4eac008796
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/762016
Reviewed-by: Leon Scroggins <scroggo@google.com>
Commit-Queue: ccameron chromium <ccameron@chromium.org>
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2026-03-04)

Detailed Report: https://clusterfuzz.com/testcase?key=4913387221745664

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x7aa416b6c859
Crash State:
  SkJpegMultiPictureParameters::Make
  SkJpegMetadataDecoderImpl::mightHaveGainmapImage
  blink::JPEGImageDecoder::GetGainmapInfoAndData
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1213630:1213644

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4913387221745664

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ch...@google.com (2026-03-04)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-04)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must exceed severity.

### cc...@chromium.org (2026-03-06)

<https://skia-review.googlesource.com/c/skia/+/1181498>

There is a more robust patch (one where we never do any pointer math) that I want to follow-up with.

### dx...@google.com (2026-03-16)

Project: skia  

Branch:  main  

Author:  Christopher Cameron [ccameron@chromium.org](mailto:ccameron@chromium.org)  

Link:    <https://skia-review.googlesource.com/1181498>

SkJpegMultiPictureParameters: Fix out of bounds read

---


Expand for full commit details
```
     
    Fix a bug where the MPEntries array can be read out of bounds. 
     
    This can happen because the bounds check did not check for overflow. Fix 
    that. Also, change the inner loop to extract a separate SkData for each 
    MPEntry and fail if that extraction fails. 
     
    A more robust solution would be to have create a SkMemoryStream for 
    mpEntriesData, but that will require a version of 
    SkStreamPriv::ReadU16BE with a parametric endian-ness, which will be 
    added in a follow-on patch (this patch is smaller to enable merging if 
    needed). 
     
    Change-Id: Id3f9ce45209de28990670f6a2d82c7bc639eeea5 
    Bug: 488596746 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1181498 
    Reviewed-by: Kaylee Lubick <kjlubick@google.com> 
    Reviewed-by: Christopher Cameron <ccameron@google.com> 
    Commit-Queue: Christopher Cameron <ccameron@google.com>

```

---

Files:

- M `src/codec/SkJpegMultiPicture.cpp`

---

Hash: df5f12318313254224cb284b56c979bf55ba2dd7  

Date: Mon Mar 9 21:30:58 2026


---

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7671180>

Roll Skia from 93167171d595 to df5f12318313 (2 revisions)

---


Expand for full commit details
```
     
    https://skia.googlesource.com/skia.git/+log/93167171d595..df5f12318313 
     
    2026-03-16 ccameron@chromium.org SkJpegMultiPictureParameters: Fix out of bounds read 
    2026-03-16 skia-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 3d9301dec00f to 26ad58d0b7b7 (2 revisions) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/skia-autoroll 
    Please CC brettos@google.com,skiabot@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Skia: https://bugs.chromium.org/p/skia/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:mac14.arm64-blink-rel;luci.chromium.try:win_optional_gpu_tests_rel 
    Cq-Do-Not-Cancel-Tryjobs: true 
    Bug: chromium:488596746 
    Tbr: brettos@google.com 
    Change-Id: I7c129dab67506a05c7b03f41327a599f46c4a18a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7671180 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1600074}

```

---

Files:

- M `DEPS`
- M `third_party/skia`

---

Hash: [52f40ff8d2c781bc9545af064836fb41bfb84751](https://chromiumdash.appspot.com/commit/52f40ff8d2c781bc9545af064836fb41bfb84751)  

Date: Mon Mar 16 20:13:48 2026


---

### 24...@project.gserviceaccount.com (2026-03-17)

ClusterFuzz testcase 4913387221745664 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1600070:1600083

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-03-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-21)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1600074) appears to be after stable branch point (1582197).

Merge review required: a commit with DEPS changes was detected.

Requesting merge to beta (M147) because latest trunk commit (1600074) appears to be after beta branch point (1596535).

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-23)

No crashes in Canary, approved to merge to M146 and M147.

### dx...@google.com (2026-03-25)

Project: skia  

Branch:  chrome/m147  

Author:  Christopher Cameron [ccameron@chromium.org](mailto:ccameron@chromium.org)  

Link:    <https://skia-review.googlesource.com/1195096>

SkJpegMultiPictureParameters: Fix out of bounds read

---


Expand for full commit details
```
     
    Fix a bug where the MPEntries array can be read out of bounds. 
     
    This can happen because the bounds check did not check for overflow. Fix 
    that. Also, change the inner loop to extract a separate SkData for each 
    MPEntry and fail if that extraction fails. 
     
    A more robust solution would be to have create a SkMemoryStream for 
    mpEntriesData, but that will require a version of 
    SkStreamPriv::ReadU16BE with a parametric endian-ness, which will be 
    added in a follow-on patch (this patch is smaller to enable merging if 
    needed). 
     
    Change-Id: Id3f9ce45209de28990670f6a2d82c7bc639eeea5 
    Bug: 488596746 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1181498 
    Reviewed-by: Kaylee Lubick <kjlubick@google.com> 
    Reviewed-by: Christopher Cameron <ccameron@google.com> 
    Commit-Queue: Christopher Cameron <ccameron@google.com> 
    (cherry picked from commit df5f12318313254224cb284b56c979bf55ba2dd7) 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1195096

```

---

Files:

- M `src/codec/SkJpegMultiPicture.cpp`

---

Hash: abbe599fb3c0ef2fa82bfadbb0ddcd321f22faf0  

Date: Mon Mar 9 21:30:58 2026


---

### pe...@google.com (2026-03-25)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-03-26)

Project: skia  

Branch:  chrome/m146  

Author:  Christopher Cameron [ccameron@chromium.org](mailto:ccameron@chromium.org)  

Link:    <https://skia-review.googlesource.com/1195376>

SkJpegMultiPictureParameters: Fix out of bounds read

---


Expand for full commit details
```
     
    Fix a bug where the MPEntries array can be read out of bounds. 
     
    This can happen because the bounds check did not check for overflow. Fix 
    that. Also, change the inner loop to extract a separate SkData for each 
    MPEntry and fail if that extraction fails. 
     
    A more robust solution would be to have create a SkMemoryStream for 
    mpEntriesData, but that will require a version of 
    SkStreamPriv::ReadU16BE with a parametric endian-ness, which will be 
    added in a follow-on patch (this patch is smaller to enable merging if 
    needed). 
     
    Change-Id: Id3f9ce45209de28990670f6a2d82c7bc639eeea5 
    Bug: 488596746 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1181498 
    Reviewed-by: Kaylee Lubick <kjlubick@google.com> 
    Reviewed-by: Christopher Cameron <ccameron@google.com> 
    Commit-Queue: Christopher Cameron <ccameron@google.com> 
    (cherry picked from commit df5f12318313254224cb284b56c979bf55ba2dd7) 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1195376

```

---

Files:

- M `src/codec/SkJpegMultiPicture.cpp`

---

Hash: 30d129c8800b5626c46fb83fa62db10b9b22b319  

Date: Mon Mar 9 21:30:58 2026


---

### pe...@google.com (2026-04-03)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-04-03)

1. <https://skia-review.git.corp.google.com/c/skia/+/1202798>
2. Low - no conflicts
3. 146 and 147
4. Yes

### dx...@google.com (2026-04-03)

Project: skia  

Branch:  chrome/m138  

Author:  Christopher Cameron [ccameron@chromium.org](mailto:ccameron@chromium.org)  

Link:    <https://skia-review.googlesource.com/1202798>

[M138-LTS] SkJpegMultiPictureParameters: Fix out of bounds read

---


Expand for full commit details
```
     
    Fix a bug where the MPEntries array can be read out of bounds. 
     
    This can happen because the bounds check did not check for overflow. Fix 
    that. Also, change the inner loop to extract a separate SkData for each 
    MPEntry and fail if that extraction fails. 
     
    A more robust solution would be to have create a SkMemoryStream for 
    mpEntriesData, but that will require a version of 
    SkStreamPriv::ReadU16BE with a parametric endian-ness, which will be 
    added in a follow-on patch (this patch is smaller to enable merging if 
    needed). 
     
    Bug: 488596746 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1181498 
    Reviewed-by: Kaylee Lubick <kjlubick@google.com> 
    Reviewed-by: Christopher Cameron <ccameron@google.com> 
    Commit-Queue: Christopher Cameron <ccameron@google.com> 
    (cherry picked from commit df5f12318313254224cb284b56c979bf55ba2dd7) 
     
    Change-Id: Ieb40055d9056969a5a9f741ea881688f914c98dc 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1202798 
    Reviewed-by: Florin Malita <fmalita@google.com>

```

---

Files:

- M `src/codec/SkJpegMultiPicture.cpp`

---

Hash: 8dae1b3c5291f42b592a85f211a4eb8b31b28729  

Date: Mon Mar 9 21:30:58 2026


---

### kj...@google.com (2026-04-03)

Oh, whoops. I thought it had already been approved for merge to 138. Let me know if I need to revert

### vi...@google.com (2026-04-06)

I believe everything is fine, Kaylee. Thank you.

### sp...@google.com (2026-04-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-05-06)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-06)

1. <https://skia-review.git.corp.google.com/c/skia/+/1227856>
2. Low. No conflicts
3. 138, 146 and 147
4. Yes

### dx...@google.com (2026-06-03)

Project: skia  

Branch:  chrome/m144  

Author:  Christopher Cameron [ccameron@chromium.org](mailto:ccameron@chromium.org)  

Link:    <https://skia-review.googlesource.com/1227856>

[M144-LTS] SkJpegMultiPictureParameters: Fix out of bounds read

---


Expand for full commit details
```
     
    Fix a bug where the MPEntries array can be read out of bounds. 
     
    This can happen because the bounds check did not check for overflow. Fix 
    that. Also, change the inner loop to extract a separate SkData for each 
    MPEntry and fail if that extraction fails. 
     
    A more robust solution would be to have create a SkMemoryStream for 
    mpEntriesData, but that will require a version of 
    SkStreamPriv::ReadU16BE with a parametric endian-ness, which will be 
    added in a follow-on patch (this patch is smaller to enable merging if 
    needed). 
     
    Bug: 488596746 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1181498 
    Reviewed-by: Kaylee Lubick <kjlubick@google.com> 
    Reviewed-by: Christopher Cameron <ccameron@google.com> 
    Commit-Queue: Christopher Cameron <ccameron@google.com> 
    (cherry picked from commit df5f12318313254224cb284b56c979bf55ba2dd7) 
     
    Change-Id: Ib56c8723ca001da2555cd82fe82859a6783030de 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1227856 
    Reviewed-by: Christopher Cameron <ccameron@google.com> 
    Commit-Queue: Christopher Cameron <ccameron@google.com>

```

---

Files:

- M `src/codec/SkJpegMultiPicture.cpp`

---

Hash: b0ac10a99e91f624bcc82e98cb0b4fb6a0cdd9a8  

Date: Mon Mar 9 21:30:58 2026


---

### ch...@google.com (2026-07-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488596746)*
