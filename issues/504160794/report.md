# AddressSanitizer heap-buffer-overflow in skcms CLUT from a PNG iCCP chunk on the default Rust ICC path

| Field | Value |
|-------|-------|
| **Issue ID** | [504160794](https://issues.chromium.org/issues/504160794) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | oj...@gmail.com |
| **Assignee** | se...@microsoft.com |
| **Created** | 2026-04-19 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

Heap-buffer-overflow in skcms::select\_curve\_ops via a PNG iCCP mAB tag on the default Rust ICC path

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/>

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

A PNG `iCCP` chunk carrying an `mAB`  (A-to-B multidimensional LUT) tag with `input_channels=64` and `output_channels=3` is accepted by the default Rust ICC parser because the channel check in `moxcms::Reader::read_lut_abm_type` ([reader.rs](https://source.chromium.org/chromium/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6:third_party/rust/chromium_crates_io/vendor/moxcms-v0_8/src/reader.rs)) reads `if in_channels > 4 && out_channels > 4 { return Ok(None); }`, where the intent is `||`.

The Rust FFI in [FFI.rs](https://source.chromium.org/chromium/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6:third_party/skia/rust/icc/FFI.rs) forwards `A2B.input_channels = 64` to C++. `rust_icc::ToSkcmsA2B` in [FFI.cpp](https://source.chromium.org/chromium/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6:third_party/skia/rust/icc/FFI.cpp) returns `false` because the value is out of range, but `SkCodecs::MakeICCProfileWithRust` in [SkCodecColorProfileRust.cpp](https://source.chromium.org/chromium/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6:third_party/skia/src/codec/SkCodecColorProfileRust.cpp) throws that return value away, so the incomplete `skcms_A2B` is installed anyway. When `SkColorSpace::Make` runs `skcms_ApproximatelyEqualProfiles` during PNG decode, it reaches `add_curve_ops(A2B.input_curves, 64)` in [skcms.cc](https://source.chromium.org/chromium/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6:third_party/skia/modules/skcms/skcms.cc), and `select_curve_ops` iterates its loop 64 times. At the first iteration it reads `curves[63].table_entries`, which sits 2016 bytes from the start of the four-element `input_curves` array and 1176 bytes past the end of the 1000-byte `ColorProfile` heap allocation.

A plain `<img src=evil.png>` triggers this on dev/beta Chromium with no JavaScript, no user gesture, and no feature flag.

Choosing other values for `input_channels` shifts the read offset: each `+1` moves it by 32 bytes (`sizeof(skcms_Curve)`). Setting `input_channels=5` reaches `curves[4].table_entries` inside the `skcms_A2B` struct and also reaches `kOps[4]` inside `select_curve_op`, which AddressSanitizer reports as a `global-buffer-overflow` 4 bytes past a 96-byte static array.

## Tested build

- `chromium/src` revision [`736c900b2d459d998a4ea2da291d98fbfce75ca6`](https://chromium.googlesource.com/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6)

## Steps to reproduce

1. Place `poc.html` and `evil.png` in a directory and serve it locally on port 7200, e.g. `python3 -m http.server 7200`.
2. Launch the ASAN Chromium build against a fresh user-data directory:
   ```
   ASAN_OPTIONS=symbolize=1:external_symbolizer_path=<asan-dir>/llvm-symbolizer <asan-dir>/chrome --user-data-dir=/tmp/p1 --no-sandbox --headless=new --disable-gpu --virtual-time-budget=10000 http://127.0.0.1:7200/poc.html
   
   ```
   The renderer aborts and AddressSanitizer prints a symbolized `heap-buffer-overflow` report identifying `select_curve_ops` in `skcms.cc` as the site of the OOB read and `SkCodecs::MakeICCProfileWithRust` as the origin of the 1000-byte allocation.

## ASAN stack trace

```
[37715:37715:0419/074644.093283:ERROR:dbus/object_proxy.cc:572] Failed to call method: org.freedesktop.DBus.Properties.GetAll: object_path= /org/freedesktop/UPower/devices/DisplayDevice: org.freedesktop.DBus.Error.ServiceUnknown: The name org.freedesktop.UPower was not provided by any .service files
=================================================================
==37825==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6e4cb3062e00 at pc 0x590cacc40e57 bp 0x7fff6648bb20 sp 0x7fff6648bb18
READ of size 4 at 0x6e4cb3062e00 thread T0 (chrome)
    #0 0x590cacc40e56 in select_curve_ops(skcms_Curve const*, int, OpAndArg*) third_party/skia/modules/skcms/skcms.cc:2545:27
    #1 0x590cacc3fbef in skcms_Transform::$_2::operator()(skcms_Curve const*, int) const third_party/skia/modules/skcms/skcms.cc:2758:22
    #2 0x590cacc393d3 in skcms_Transform third_party/skia/modules/skcms/skcms.cc:2877:22
    #3 0x590cacc37f4d in skcms_ApproximatelyEqualProfiles third_party/skia/modules/skcms/skcms.cc:1782:10
    #4 0x590cac808b19 in SkColorSpace::Make(skcms_ICCProfile const&) third_party/skia/src/core/SkColorSpace.cpp:345:16
    #5 0x590cc6187779 in SkEncodedInfo::makeImageInfo() const third_party/skia/src/codec/SkEncodedInfo.cpp:19:46
    #6 0x590cd501653f in blink::SkiaImageDecoderBase::OnSetData(scoped_refptr<blink::SegmentReader>) third_party/skia/include/codec/SkCodec.h:233:55
    #7 0x590cd4b7af09 in blink::ImageDecoder::SetData(scoped_refptr<blink::SegmentReader>, bool) third_party/blink/renderer/platform/image-decoders/image_decoder.h:286:5
    #8 0x590cd4fd4a54 in blink::ImageDecoder::CreateByMimeType(blink::String, scoped_refptr<blink::SegmentReader>, bool, blink::ImageDecoder::AlphaOption, blink::ImageDecoder::HighBitDepthDecodingOption, blink::ColorBehavior, cc::AuxImage, unsigned long, SkISize const&, blink::ImageDecoder::AnimationOption) third_party/blink/renderer/platform/image-decoders/image_decoder.cc:353:14
    #9 0x590cd4fd3787 in blink::ImageDecoder::Create(scoped_refptr<blink::SegmentReader>, bool, blink::ImageDecoder::AlphaOption, blink::ImageDecoder::HighBitDepthDecodingOption, blink::ColorBehavior, cc::AuxImage, unsigned long, SkISize const&, blink::ImageDecoder::AnimationOption) third_party/blink/renderer/platform/image-decoders/image_decoder.cc:290:10
    #10 0x590cd4b73ee0 in blink::DeferredImageDecoder::Create(scoped_refptr<blink::SharedBuffer>, bool, blink::ImageDecoder::AlphaOption, blink::ColorBehavior) third_party/blink/renderer/platform/image-decoders/image_decoder.h:230:12
    #11 0x590cd4a88cd0 in blink::BitmapImage::SetData(scoped_refptr<blink::SharedBuffer>, bool) third_party/blink/renderer/platform/graphics/bitmap_image.cc:240:14
    #12 0x590cd3645930 in blink::ImageResourceContent::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ResourceStatus, blink::ImageResourceContent::UpdateImageOption, bool, bool) third_party/blink/renderer/core/loader/resource/image_resource_content.cc:514:35
    #13 0x590cd3636047 in blink::ImageResource::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ImageResourceContent::UpdateImageOption, bool) third_party/blink/renderer/core/loader/resource/image_resource.cc:677:31
    #14 0x590cd3636d8a in blink::ImageResource::AppendData(std::__Cr::variant<blink::SegmentedBuffer, base::span<char const, 18446744073709551615ul, char const*>>) third_party/blink/renderer/core/loader/resource/image_resource.cc:460:7
    #15 0x590cbc81c4ee in blink::ResourceLoader::DidReceiveDataImpl(std::__Cr::variant<blink::SegmentedBuffer, base::span<char const, 18446744073709551615ul, char const*>>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1067:14
    #16 0x590cbc81ed15 in non-virtual thunk to blink::ResourceLoader::DidReceiveData(base::span<char const, 18446744073709551615ul, char const*>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1041:3
    #17 0x590cbc85928b in blink::ResponseBodyLoader::OnStateChange() third_party/blink/renderer/platform/loader/fetch/response_body_loader.cc:433:12
    #18 0x590cbc80abda in blink::ResourceLoader::DidStartLoadingResponseBodyInternal(blink::BytesConsumer&) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:346:28
    #19 0x590cbc81713b in blink::ResourceLoader::DidReceiveResponse(blink::WebURLResponse const&, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:787:3
    #20 0x590cbc8859ae in blink::BackgroundURLLoader::Context::OnReceivedResponse(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int) third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:492:14
    #21 0x590cbc885efe in void base::internal::DecayedFunctorTraits<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>::Invoke<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int>(void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&, int&&) base/functional/bind_internal.h:740:12
    #22 0x590cbc885c4a in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>>, void (int)>::RunOnce(base::internal::BindStateBase*, int) base/functional/bind_internal.h:932:12
    #23 0x590cb7faafd3 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (int)>&&, int&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (int)>, int>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/callback.h:155:12
    #24 0x590cbc882fc7 in blink::BackgroundURLLoader::Context::RunTasksOnMainThread() base/functional/callback.h:155:12
    #25 0x590cbc87b670 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(), scoped_refptr<blink::BackgroundURLLoader::Context>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(), scoped_refptr<blink::BackgroundURLLoader::Context>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #26 0x590cc3f837e3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #27 0x590cc3ff48ec in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #28 0x590cc3ff378a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #29 0x590cc3e4147f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #30 0x590cc3ff5fd4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12
    #31 0x590cc3efdb20 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #32 0x590cd05a218a in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:337:16
    #33 0x590cbff692ff in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #34 0x590cbff6a637 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #35 0x590cbff6d348 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #36 0x590cbff66d01 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:356:36
    #37 0x590cbff672fc in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:369:10
    #38 0x590cabbda2a9 in ChromeMain chrome/app/chrome_main.cc:194:12
    #39 0x70bcb4a2a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #40 0x70bcb4a2a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #41 0x590cabaff029 in _start (/home/ubuntu/workspaces/chromium/asan-chrome/chrome+0x10fdf029) (BuildId: 250795ae951b3a3b)

0x6e4cb3062e00 is located 1176 bytes after 1000-byte region [0x6e4cb3062580,0x6e4cb3062968)
allocated by thread T0 (chrome) here:
    #0 0x590cabbd859d in operator new(unsigned long) (/home/ubuntu/workspaces/chromium/asan-chrome/chrome+0x110b859d) (BuildId: 250795ae951b3a3b)
    #1 0x590cacc1bfa0 in SkCodecs::MakeICCProfileWithRust(sk_sp<SkData const>) third_party/skia/src/codec/SkCodecColorProfileRust.cpp:31:25
    #2 0x590cc6186afc in SkCodecs::ColorProfile::MakeICCProfile(sk_sp<SkData const>) third_party/skia/src/codec/SkCodecColorProfile.cpp:83:12
    #3 0x590cc61a5a9c in SkPngRustCodec::MakeFromStream(std::__Cr::unique_ptr<SkStream, std::__Cr::default_delete<SkStream>>, SkCodec::Result*) third_party/skia/src/codec/SkPngRustCodec.cpp:168:17
    #4 0x590cc61a5299 in SkPngRustDecoder::Decode(std::__Cr::unique_ptr<SkStream, std::__Cr::default_delete<SkStream>>, SkCodec::Result*, void*) third_party/skia/src/codec/SkPngRustDecoder.cpp:34:12
    #5 0x590cd501646f in blink::SkiaImageDecoderBase::OnSetData(scoped_refptr<blink::SegmentReader>) third_party/blink/renderer/platform/image-decoders/skia/skia_image_decoder_base.cc:86:14
    #6 0x590cd4b7af09 in blink::ImageDecoder::SetData(scoped_refptr<blink::SegmentReader>, bool) third_party/blink/renderer/platform/image-decoders/image_decoder.h:286:5
    #7 0x590cd4fd4a54 in blink::ImageDecoder::CreateByMimeType(blink::String, scoped_refptr<blink::SegmentReader>, bool, blink::ImageDecoder::AlphaOption, blink::ImageDecoder::HighBitDepthDecodingOption, blink::ColorBehavior, cc::AuxImage, unsigned long, SkISize const&, blink::ImageDecoder::AnimationOption) third_party/blink/renderer/platform/image-decoders/image_decoder.cc:353:14
    #8 0x590cd4fd3787 in blink::ImageDecoder::Create(scoped_refptr<blink::SegmentReader>, bool, blink::ImageDecoder::AlphaOption, blink::ImageDecoder::HighBitDepthDecodingOption, blink::ColorBehavior, cc::AuxImage, unsigned long, SkISize const&, blink::ImageDecoder::AnimationOption) third_party/blink/renderer/platform/image-decoders/image_decoder.cc:290:10
    #9 0x590cd4b73ee0 in blink::DeferredImageDecoder::Create(scoped_refptr<blink::SharedBuffer>, bool, blink::ImageDecoder::AlphaOption, blink::ColorBehavior) third_party/blink/renderer/platform/image-decoders/image_decoder.h:230:12
    #10 0x590cd4a88cd0 in blink::BitmapImage::SetData(scoped_refptr<blink::SharedBuffer>, bool) third_party/blink/renderer/platform/graphics/bitmap_image.cc:240:14
    #11 0x590cd3645930 in blink::ImageResourceContent::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ResourceStatus, blink::ImageResourceContent::UpdateImageOption, bool, bool) third_party/blink/renderer/core/loader/resource/image_resource_content.cc:514:35
    #12 0x590cd3636047 in blink::ImageResource::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ImageResourceContent::UpdateImageOption, bool) third_party/blink/renderer/core/loader/resource/image_resource.cc:677:31
    #13 0x590cd3636d8a in blink::ImageResource::AppendData(std::__Cr::variant<blink::SegmentedBuffer, base::span<char const, 18446744073709551615ul, char const*>>) third_party/blink/renderer/core/loader/resource/image_resource.cc:460:7
    #14 0x590cbc81c4ee in blink::ResourceLoader::DidReceiveDataImpl(std::__Cr::variant<blink::SegmentedBuffer, base::span<char const, 18446744073709551615ul, char const*>>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1067:14
    #15 0x590cbc81ed15 in non-virtual thunk to blink::ResourceLoader::DidReceiveData(base::span<char const, 18446744073709551615ul, char const*>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1041:3
    #16 0x590cbc85928b in blink::ResponseBodyLoader::OnStateChange() third_party/blink/renderer/platform/loader/fetch/response_body_loader.cc:433:12
    #17 0x590cbc80abda in blink::ResourceLoader::DidStartLoadingResponseBodyInternal(blink::BytesConsumer&) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:346:28
    #18 0x590cbc81713b in blink::ResourceLoader::DidReceiveResponse(blink::WebURLResponse const&, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:787:3
    #19 0x590cbc8859ae in blink::BackgroundURLLoader::Context::OnReceivedResponse(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int) third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:492:14
    #20 0x590cbc885efe in void base::internal::DecayedFunctorTraits<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>::Invoke<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int>(void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&, int&&) base/functional/bind_internal.h:740:12
    #21 0x590cbc885c4a in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>>, void (int)>::RunOnce(base::internal::BindStateBase*, int) base/functional/bind_internal.h:932:12
    #22 0x590cb7faafd3 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (int)>&&, int&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (int)>, int>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/callback.h:155:12
    #23 0x590cbc882fc7 in blink::BackgroundURLLoader::Context::RunTasksOnMainThread() base/functional/callback.h:155:12
    #24 0x590cbc87b670 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(), scoped_refptr<blink::BackgroundURLLoader::Context>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(), scoped_refptr<blink::BackgroundURLLoader::Context>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #25 0x590cc3f837e3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #26 0x590cc3ff48ec in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #27 0x590cc3ff378a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #28 0x590cc3e4147f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #29 0x590cc3ff5fd4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/modules/skcms/skcms.cc:2545:27 in select_curve_ops(skcms_Curve const*, int, OpAndArg*)
Shadow bytes around the buggy address:
  0x6e4cb3062b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e4cb3062c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e4cb3062c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e4cb3062d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e4cb3062d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x6e4cb3062e00:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e4cb3062e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e4cb3062f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e4cb3062f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e4cb3063000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6e4cb3063080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==37825==ADDITIONAL INFO

==37825==Note: Please include this section with the ASan report.
Task trace:
    #0 0x590cbc8820f8 in blink::BackgroundURLLoader::Context::PostTaskToMainThread(blink::CrossThreadOnceFunction<void ()>) third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:422:52
    #1 0x590cc4c8e1d3 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:103:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=37718 --enable-crash-reporter=, --noerrdialogs --user-data-dir=/tmp/p1 --change-stack-guard-on-fork=enable --no-sandbox --file-url-path-alias=/gen=/home/ubuntu/workspaces/chromium/asan-chrome/gen --ozone-platform=headless --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1776554627983056 --launch-time-ticks=4975995880 --shared-files=v8_context_snapshot_data:100 --field-trial-handle=3,i,18058394970892133764,3878336514317533622,262144 --disable-features=PaintHolding --variations-seed-version --pseudonymization-salt-handle=7,i,7079416843415264851,3999492147164696732,4 --trace-process-track-uuid=3190708990997080739`


==37825==END OF ADDITIONAL INFO

==37825==ABORTING

```
## Root cause

Four defects on one reachable path; fixing any one closes the bug.

1. The channel check in `moxcms::Reader::read_lut_abm_type` ([reader.rs](https://source.chromium.org/chromium/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6:third_party/rust/chromium_crates_io/vendor/moxcms-v0_8/src/reader.rs)) uses `if in_channels > 4 && out_channels > 4 { return Ok(None); }`. The operator should be `||`. For `(in=64, out=3)` the expression is `true && false`, so the check passes.
2. The `LutWarehouse::Multidimensional` arm in [FFI.rs](https://source.chromium.org/chromium/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6:third_party/skia/rust/icc/FFI.rs) copies `mdt.num_input_channels` into `A2B.input_channels` and truncates `mdt.grid_points[..4]` into a fixed four-element array without rejecting out-of-range channel counts.
3. `rust_icc::ToSkcmsA2B` in [FFI.cpp](https://source.chromium.org/chromium/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6:third_party/skia/rust/icc/FFI.cpp) does reject `input_channels > 4` and returns `false`, but it writes the partially-filled `skcms_A2B` struct first. Only four of the 64 declared `input_curves` slots end up populated.
4. `SkCodecs::MakeICCProfileWithRust` in [SkCodecColorProfileRust.cpp](https://source.chromium.org/chromium/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6:third_party/skia/src/codec/SkCodecColorProfileRust.cpp) ignores the `bool` returned by `rust_icc::ToSkcmsIccProfile`, so the half-populated profile flows through and gets installed on the `SkColorSpace`.

With the profile installed, `SkColorSpace::Make` runs `skcms_ApproximatelyEqualProfiles`, which runs `skcms_Transform` over 84 probe pixels. That path calls `add_curve_ops(A2B.input_curves, A2B.input_channels)` with the attacker-controlled channel count. `add_curve_ops` in [skcms.cc](https://source.chromium.org/chromium/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6:third_party/skia/modules/skcms/skcms.cc) declares a four-element stack buffer `OpAndArg oa[4]`, asserts `numChannels <= 4` (the assertion is removed in release builds), and calls `select_curve_ops(curves, 64, oa)`. The loop reads `curves[index].table_entries` for `index` from 63 down to 0. The first read is 63 slots past `&A2B::input_curves[0]`, which is past the end of the 1000-byte `ColorProfile` allocation that the renderer made in `SkCodecs::MakeICCProfileWithRust`.

## Related report

A separate report of mine (*<https://issues.chromium.org/issues/504103236>*) targets a different validator (`read_lut_a_to_b_type`, handling the legacy mft1/mft2 tags) and a different sink (`clut()` via `sample_clut_16`). A patch to that validator does not close this report because mAB/mBA tags take a different parser path (`read_lut_abm_type`). Defects 3 and 4 above are common to both reports, so a patch on either of those two defects would close both as a side effect.

## Suggested fix

In `moxcms::Reader::read_lut_a_to_b_type` and `read_lut_abm_type`, replace the current channel checks with a plain range test, for example:

```
if !(1..=4).contains(&in_channels) || !(1..=4).contains(&out_channels) {
    return Err(CmsError::InvalidProfile);
}

```

Separately, have `SkCodecs::MakeICCProfileWithRust` check the return of `rust_icc::ToSkcmsIccProfile` and fail the decode when it returns `false`. The upstream moxcms repository is <https://github.com/awxkee/moxcms>.

## Attachments

- `poc.html` one-line HTML that loads `evil.png`.
- `evil.png` 620-byte PNG with the crafted `iCCP` mAB tag (`input_channels=64`, `output_channels=3`).
- `make_icc_poc.py` deterministic generator. `python3 make_icc_poc.py N` emits the variant for `input_channels=N` (default 64; `N=5` reproduces the `kOps[4]` global OOB).

#### Impact analysis

## Security impact

Any origin serving `<img src=evil.png>` reaches this path during Blink's image decode. The same decode flow is used by `<img>`, `<picture>`, CSS `background-image`, SVG `url()`, `createImageBitmap`, canvas `drawImage`, and worker `ImageDecoder`. There is no CORS prompt, no user gesture, and no feature flag to enable.

The Rust ICC parser is the dev/beta default: `SK_CODEC_COLOR_PROFILE_PARSE_WITH_RUST` is listed in the `defines` array of `config("skia_config")` in [skia/BUILD.gn](https://source.chromium.org/chromium/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6:skia/BUILD.gn), and `blink::features::kForceSkcmsICCParsing` is declared `FEATURE_DISABLED_BY_DEFAULT` in [features.cc](https://source.chromium.org/chromium/chromium/src/+/736c900b2d459d998a4ea2da291d98fbfce75ca6:third_party/blink/common/features.cc).

The `input_channels` byte of the mAB tag controls the OOB distance, so the attacker can aim the 4-byte read at different offsets past the `ColorProfile` allocation by varying that single byte.

---

### The cause

#### What version of Chrome have you found the security issue in?

Chromium 149.0.7795.0 Dev ASAN

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

M. Fauzan Wijaya (Gh05t666nero)

## Attachments

- [poc.mp4](attachments/poc.mp4) (video/mp4, 6.3 MB)
- [make_icc_poc.py](attachments/make_icc_poc.py) (text/x-python, 3.1 KB)
- [evil.png](attachments/evil.png) (image/png, 620 B)
- [poc.html](attachments/poc.html) (text/html, 60 B)

## Timeline

### oj...@gmail.com (2026-04-21)

Hi, any update on this?

### ar...@google.com (2026-04-21)

Thanks!

I triaged: <https://g-issues.chromium.org/issues/504103236> and assigned to @kj...@google.com
This is likely similar, but I won't have time today. I am delegating to the GPU security triage.

### se...@microsoft.com (2026-04-22)

Tentative fix in https://skia-review.googlesource.com/c/skia/+/1215636

### dx...@google.com (2026-04-22)

Project: skia  

Branch:  main  

Author:  Sergio Gonzalez Martin [sergiog@microsoft.com](mailto:sergiog@microsoft.com)  

Link:    <https://skia-review.googlesource.com/1215636>

[rust icc] Reject unsupported A2B/B2A channel counts and grid dimensions

---


Expand for full commit details
```
     
    Fixes: 
    - Check ToSkcmsIccProfile return; return nullptr on failure. 
    - Validate channel counts (1-4) in both FFI.rs and FFI.cpp. 
    - Validate grid_points[i] >= 2 for every active CLUT dimension. 
    - Fix Lut arm to populate grid_points for all active input channels. 
    - Move FFI.cpp writes to output struct after validation (don't write 
      input_channels=64 before returning false). 
     
    Bug: 503958940 
    Bug: 504160794 
    Bug: 504103236 
    Change-Id: Ic034ec283807e665d50d6377a1757dee4451574b 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1215636 
    Reviewed-by: Florin Malita <fmalita@google.com> 
    Commit-Queue: Florin Malita <fmalita@google.com> 
    Reviewed-by: Kaylee Lubick <kjlubick@google.com>

```

---

Files:

- M `rust/icc/FFI.cpp`
- M `rust/icc/FFI.rs`
- M `src/codec/SkCodecColorProfileRust.cpp`
- M `tests/RustIccTest.cpp`

---

Hash: f4834c75d3ec17a87ab16a1340dc8e910f244072  

Date: Wed Apr 22 13:12:25 2026


---

### ds...@google.com (2026-04-22)

If i'm reading the above correctly, this is an out of bounds write in the GPU process, so setting P1/S1.

I *think* it's saying this feature is off by default, if that's the case we should add the Security Impact None label as it doesn't impact Chrome at this point and this bug be set blocking the feature release.

Tentatively setting the OS to all, as I don't see anything OS specific and the FoundIn to 146 since the code appears to be from last year.

### ch...@google.com (2026-04-23)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-04-23)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7791121>

Roll Skia from 684457bb5dba to 8106701adb3e (15 revisions)

---


Expand for full commit details
```
     
    https://skia.googlesource.com/skia.git/+log/684457bb5dba..8106701adb3e 
     
    2026-04-23 michaelludwig@google.com Revert "Reland "[graphite] Replicate Dawn format capability table"" 
    2026-04-23 skia-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from 664858ab7de2 to 887d15753e30 (13 revisions) 
    2026-04-23 skia-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 97c656c3aa9d to b68105cc00f0 (6 revisions) 
    2026-04-23 skia-autoroll@skia-public.iam.gserviceaccount.com Roll Skia Infra from 298872497a26 to 5300bf8291db (9 revisions) 
    2026-04-23 skia-autoroll@skia-public.iam.gserviceaccount.com Roll Dawn from e10184f6962d to 219c6e1eb500 (11 revisions) 
    2026-04-22 recipe-mega-autoroller@chops-service-accounts.iam.gserviceaccount.com Roll recipe dependencies (trivial). 
    2026-04-22 michaelludwig@google.com Revert "[sksl] Limit field count for structs" 
    2026-04-22 thomsmit@google.com [graphite] Add sparse strips flattenner bench 
    2026-04-22 alexisdavidc@google.com Add test for capped hairlines 
    2026-04-22 michaelludwig@google.com Reland "[graphite] Replicate Dawn format capability table" 
    2026-04-22 sergiog@microsoft.com [rust icc] Reject unsupported A2B/B2A channel counts and grid dimensions 
    2026-04-22 michaelludwig@google.com Implement onIsAlphaUnchanged() for SkColorSpaceXformColorFilter 
    2026-04-22 thomsmit@google.com [graphite] Make tiger svg dataset shareable 
    2026-04-22 skia-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from f4814e7bd340 to 97c656c3aa9d (9 revisions) 
    2026-04-22 skia-autoroll@skia-public.iam.gserviceaccount.com Roll skcms from 15db2430b628 to a7a3b15f0635 (1 revision) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/skia-autoroll 
    Please CC jlavrova@google.com,skiabot@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Skia: https://bugs.chromium.org/p/skia/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:mac14.arm64-blink-rel;luci.chromium.try:win_optional_gpu_tests_rel 
    Cq-Do-Not-Cancel-Tryjobs: true 
    Bug: chromium:501177192,chromium:502108891,chromium:502280548,chromium:503958940,chromium:504103236,chromium:504160794 
    Tbr: jlavrova@google.com 
    Test: Test: Test: BufferZeroInitTest.ResolveQuerySet 
    Test: Test: Test: angle_trace_tests --gtest_filter=*quick_hit_casino_slots 
    Change-Id: Iab1ca678bdf7c76a2d6d36faff37d05b568da1a3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7791121 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1619589}

```

---

Files:

- M `DEPS`
- M `third_party/skia`

---

Hash: [e990e7d6c8c99b2445fd3dc8fed8e5f5888771d7](https://chromiumdash.appspot.com/commit/e990e7d6c8c99b2445fd3dc8fed8e5f5888771d7)  

Date: Thu Apr 23 16:49:50 2026


---

### ch...@google.com (2026-04-28)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### aj...@google.com (2026-05-05)

Medium as this is a read in the renderer.

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### oj...@gmail.com (2026-05-08)

Appeal reward reason: Hi Chrome VRP Panel,

Polite request for reward reassessment under the pre-April-30 framework (snapshot: <https://web.archive.org/web/20260403162256/https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules>). Please add the Security-VRP-Reassessment-Request hotlist (id: 8186354) if I'm not able to do so myself.

I accept the S2 downgrade in [comment #10](https://issues.chromium.org/issues/504160794#comment10). This is a renderer OOB read without demonstrated write or RCE. My question is only about which baseline tier applies.

The rationale "Baseline. User information disclosure" ($2,000) maps to the Other vulnerability classes table. I'd like to ask whether footnote [3] of the Memory corruption table is the more directly applicable rule: "Reports of renderer OOB reads or DCHECK / SEGV / etc. bugs in V8, without demonstration of write or RCE, are only eligible for baseline reward amounts."

Footnote [3] explicitly covers renderer OOB reads and sets the cap at baseline memory corruption ($7,000 renderer) rather than redirecting to a different table. The "Access to a value versus the potential for RCE" section gives discretion to use an info-disclosure-consistent amount, but footnote [3] would seem to set the eligible baseline at the renderer memory corruption row.

Report characteristics: heap-buffer-overflow read in renderer sandboxed process, reachable from any web origin via image decode (img/picture/CSS/SVG/canvas/createImageBitmap/worker ImageDecoder), no JavaScript or user gesture or feature flag or CORS prompt required, attacker-controlled OOB read offset via input\_channels (each +1 = 32 bytes), four distinct defects on the reachable path identified with permalinks, and the suggested fix direction was applied in CL 1215636.

I'm asking whether this fits Memory corruption baseline tier ($7,000 renderer per footnote [3]) rather than User information disclosure baseline tier ($2,000).

Thanks for considering.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/504160794)*
