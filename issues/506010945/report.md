# AddressSanitizer heap-buffer-overflow in skcms CLUT from a PNG iCCP chunk on the default Rust ICC path

| Field | Value |
|-------|-------|
| **Issue ID** | [506010945](https://issues.chromium.org/issues/506010945) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | oj...@gmail.com |
| **Assignee** | se...@microsoft.com |
| **Created** | 2026-04-24 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

Heap-buffer-overflow in skcms clut() via a PNG iCCP mAB tag with output\_channels=1 on the default Rust ICC path

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

A crafted PNG `iCCP` chunk carrying an `mAB` A-to-B tag with `input_channels=1`, `output_channels=1`, `grid_size=2`, and a 16-bit CLUT is accepted by the Rust ICC parser path in Skia. Native skcms requires `mAB` tags to have exactly three output channels, but the Rust parser and Rust→skcms bridge accept `output_channels=1` and forward an `skcms_A2B` state that skcms never produces on its own parse path. `clut()` in skcms has runtime sampling logic only for 3 or 4 output channels; the `output_channels=1` PoC falls into the 4-channel `gather_16` path, which performs a 2-byte out-of-bounds read past the Rust-owned CLUT `Vec<u8>` during ordinary PNG image decode.

The validator mismatch survives the Apr 22 fix wave for `504103236` / `504160794` (Skia commit [`f4834c75d3`](https://skia.googlesource.com/skia/+/f4834c75d3ec17a87ab16a1340dc8e910f244072), rolled into Chromium by [`e990e7d6c8c9`](https://chromium.googlesource.com/chromium/src/+/e990e7d6c8c9)) because that fix only constrains channel counts to `1..=4`, not to `== 3` for `mAB`. Unlike those two reports, this path does not depend on `ToSkcmsIccProfile()` returning false; it returns true and the invalid state flows through.

## Steps to reproduce

1. Place the four attached files into one directory and start the server from that directory: `python3 server.py`. It listens on `http://127.0.0.1:7211`.
2. Download a currently-shipping Linux Canary ASAN build with the in-tree helper: `python3 src/tools/get_asan_chrome/get_asan_chrome.py --os linux --channel canary --download_directory <asan-dir>`. This fetches `149.0.7809.0` (branch position 1619429).
3. Launch the ASAN Canary against a fresh profile:
   ```
   ASAN_OPTIONS=symbolize=1:external_symbolizer_path=<asan-dir>/llvm-symbolizer:abort_on_error=1:halt_on_error=1 \
   <asan-dir>/chrome --user-data-dir=$(mktemp -d) --no-sandbox --headless=new \
     --disable-gpu http://127.0.0.1:7211/poc.html
   
   ```

## Observed

The renderer aborts with AddressSanitizer reporting a heap-buffer-overflow 2-byte read at `third_party/skia/modules/skcms/src/Transform_inl.h:100`, called from `skcms_ApproximatelyEqualProfiles` during PNG decode. The allocation origin is a Rust `Vec<u8>` grown via `alloc::raw_vec::RawVecInner::finish_grow`.

## Symbolized ASAN trace

```
[55683:55683:0424/144625.126015:ERROR:dbus/object_proxy.cc:572] Failed to call method: org.freedesktop.DBus.Properties.GetAll: object_path= /org/freedesktop/UPower/devices/DisplayDevice: org.freedesktop.DBus.Error.ServiceUnknown: The name org.freedesktop.UPower was not provided by any .service files
=================================================================
==55792==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7720e092d7b8 at pc 0x62b14e54f8f0 bp 0x7ffebdd21ab0 sp 0x7ffebdd21aa8
READ of size 2 at 0x7720e092d7b8 thread T0 (chrome)
    #0 0x62b14e54f8ef in skcms_private::hsw::clut(unsigned int, unsigned int, unsigned char const*, unsigned char const*, unsigned char const*, float vector[8]*, float vector[8]*, float vector[8]*, float vector[8]*) third_party/skia/modules/skcms/src/Transform_inl.h:100:5
    #1 0x62b14e544ba9 in skcms_private::hsw::exec_stages(skcms_private::Op const*, void const**, char const*, char*, int) third_party/skia/modules/skcms/src/Transform_inl.h:760:5
    #2 0x62b14e53c38a in skcms_private::hsw::run_program(skcms_private::Op const*, void const**, long, char const*, char*, int, unsigned long, unsigned long) third_party/skia/modules/skcms/src/Transform_inl.h:1586:9
    #3 0x62b14e5329dd in skcms_Transform third_party/skia/modules/skcms/skcms.cc:3089:5
    #4 0x62b14e53101d in skcms_ApproximatelyEqualProfiles third_party/skia/modules/skcms/skcms.cc:1782:10
    #5 0x62b14e101c79 in SkColorSpace::Make(skcms_ICCProfile const&) third_party/skia/src/core/SkColorSpace.cpp:345:16
    #6 0x62b167c4fb29 in SkEncodedInfo::makeImageInfo() const third_party/skia/src/codec/SkEncodedInfo.cpp:19:46
    #7 0x62b176b519ef in blink::SkiaImageDecoderBase::OnSetData(scoped_refptr<blink::SegmentReader>) third_party/skia/include/codec/SkCodec.h:233:55
    #8 0x62b1766b39a9 in blink::ImageDecoder::SetData(scoped_refptr<blink::SegmentReader>, bool) third_party/blink/renderer/platform/image-decoders/image_decoder.h:286:5
    #9 0x62b176b0ff04 in blink::ImageDecoder::CreateByMimeType(blink::String, scoped_refptr<blink::SegmentReader>, bool, blink::ImageDecoder::AlphaOption, blink::ImageDecoder::HighBitDepthDecodingOption, blink::ColorBehavior, cc::AuxImage, unsigned long, SkISize const&, blink::ImageDecoder::AnimationOption) third_party/blink/renderer/platform/image-decoders/image_decoder.cc:353:14
    #10 0x62b176b0ec37 in blink::ImageDecoder::Create(scoped_refptr<blink::SegmentReader>, bool, blink::ImageDecoder::AlphaOption, blink::ImageDecoder::HighBitDepthDecodingOption, blink::ColorBehavior, cc::AuxImage, unsigned long, SkISize const&, blink::ImageDecoder::AnimationOption) third_party/blink/renderer/platform/image-decoders/image_decoder.cc:290:10
    #11 0x62b1766ac980 in blink::DeferredImageDecoder::Create(scoped_refptr<blink::SharedBuffer>, bool, blink::ImageDecoder::AlphaOption, blink::ColorBehavior) third_party/blink/renderer/platform/image-decoders/image_decoder.h:230:12
    #12 0x62b1765bea80 in blink::BitmapImage::SetData(scoped_refptr<blink::SharedBuffer>, bool) third_party/blink/renderer/platform/graphics/bitmap_image.cc:240:14
    #13 0x62b1751680b0 in blink::ImageResourceContent::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ResourceStatus, blink::ImageResourceContent::UpdateImageOption, bool, bool) third_party/blink/renderer/core/loader/resource/image_resource_content.cc:515:35
    #14 0x62b175158377 in blink::ImageResource::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ImageResourceContent::UpdateImageOption, bool) third_party/blink/renderer/core/loader/resource/image_resource.cc:704:31
    #15 0x62b1751590ba in blink::ImageResource::AppendData(std::__Cr::variant<blink::SegmentedBuffer, base::span<char const, 18446744073709551615ul, char const*>>) third_party/blink/renderer/core/loader/resource/image_resource.cc:461:7
    #16 0x62b15e1730ce in blink::ResourceLoader::DidReceiveDataImpl(std::__Cr::variant<blink::SegmentedBuffer, base::span<char const, 18446744073709551615ul, char const*>>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1067:14
    #17 0x62b15e1758e5 in non-virtual thunk to blink::ResourceLoader::DidReceiveData(base::span<char const, 18446744073709551615ul, char const*>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1041:3
    #18 0x62b15e1afc8b in blink::ResponseBodyLoader::OnStateChange() third_party/blink/renderer/platform/loader/fetch/response_body_loader.cc:433:12
    #19 0x62b15e16187a in blink::ResourceLoader::DidStartLoadingResponseBodyInternal(blink::BytesConsumer&) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:346:28
    #20 0x62b15e16dd1b in blink::ResourceLoader::DidReceiveResponse(blink::WebURLResponse const&, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:787:3
    #21 0x62b15e1dc3be in blink::BackgroundURLLoader::Context::OnReceivedResponse(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int) third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:492:14
    #22 0x62b15e1dc90e in void base::internal::DecayedFunctorTraits<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>::Invoke<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int>(void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&, int&&) base/functional/bind_internal.h:740:12
    #23 0x62b15e1dc65a in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>>, void (int)>::RunOnce(base::internal::BindStateBase*, int) base/functional/bind_internal.h:932:12
    #24 0x62b1598bd983 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (int)>&&, int&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (int)>, int>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/callback.h:155:12
    #25 0x62b15e1d99d7 in blink::BackgroundURLLoader::Context::RunTasksOnMainThread() base/functional/callback.h:155:12
    #26 0x62b15e1d2080 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(), scoped_refptr<blink::BackgroundURLLoader::Context>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(), scoped_refptr<blink::BackgroundURLLoader::Context>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #27 0x62b1658bbaf3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #28 0x62b16592d34c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #29 0x62b16592c1ea in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #30 0x62b16577929f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:47:55
    #31 0x62b16592ea34 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12
    #32 0x62b1658359d0 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #33 0x62b17209ffea in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:337:16
    #34 0x62b161c11caf in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:665:14
    #35 0x62b161c12fe7 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:772:12
    #36 0x62b161c15f58 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1164:10
    #37 0x62b161c0f6b1 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:356:36
    #38 0x62b161c0fcac in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:369:10
    #39 0x62b14d4d02a9 in ChromeMain chrome/app/chrome_main.cc:194:12
    #40 0x7b00e222a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #41 0x7b00e222a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #42 0x62b14d3f5029 in _start (/home/ubuntu/workspaces/chromium/asan-chrome/canary/chrome+0x110dc029) (BuildId: f8f259e958de3990)

0x7720e092d7b8 is located 0 bytes after 8-byte region [0x7720e092d7b0,0x7720e092d7b8)
allocated by thread T0 (chrome) here:
    #0 0x62b14d495d3c in realloc (/home/ubuntu/workspaces/chromium/asan-chrome/canary/chrome+0x1117cd3c) (BuildId: f8f259e958de3990)
    #1 0x62b180ade47e in alloc::alloc::realloc_nonnull third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:155:14
    #2 0x62b180ade47e in <alloc::alloc::Global>::grow_impl_runtime third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:259:31
    #3 0x62b180ade47e in <alloc::alloc::Global>::grow_impl third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:362:9
    #4 0x62b180ade47e in <alloc::alloc::Global as core::alloc::Allocator>::grow third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:474:23
    #5 0x62b180ade47e in <alloc::raw_vec::RawVecInner>::finish_grow third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/raw_vec/mod.rs:556:28

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/modules/skcms/src/Transform_inl.h:100:5 in skcms_private::hsw::clut(unsigned int, unsigned int, unsigned char const*, unsigned char const*, unsigned char const*, float vector[8]*, float vector[8]*, float vector[8]*, float vector[8]*)
Shadow bytes around the buggy address:
  0x7720e092d500: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fd
  0x7720e092d580: f7 fa fd fd f7 fa fd fd f7 fa 00 fa f7 fa fd fd
  0x7720e092d600: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fd
  0x7720e092d680: f7 fa 00 07 f7 fa 00 fa f7 fa 00 00 f7 fa 00 fa
  0x7720e092d700: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa 02 fa
=>0x7720e092d780: f7 fa fd fa f7 fa 00[fa]f7 fa 02 fa fa fa fa fa
  0x7720e092d800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7720e092d880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7720e092d900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7720e092d980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7720e092da00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==55792==ADDITIONAL INFO

==55792==Note: Please include this section with the ASan report.
Task trace:
    #0 0x62b15e1d8b08 in blink::BackgroundURLLoader::Context::PostTaskToMainThread(blink::CrossThreadOnceFunction<void ()>) third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:422:52
    #1 0x62b16671d913 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:103:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=55685 --enable-crash-reporter=, --noerrdialogs --user-data-dir=/tmp/tmp.65MvzuaZlY --change-stack-guard-on-fork=enable --no-sandbox --file-url-path-alias=/gen=/home/ubuntu/workspaces/chromium/asan-chrome/canary/gen --ozone-platform=headless --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1777012108416806 --launch-time-ticks=4676572383 --shared-files=v8_context_snapshot_data:100 --field-trial-handle=3,i,3379391451853565885,10846409164686895126,262144 --disable-features=PaintHolding --variations-seed-version --pseudonymization-salt-handle=7,i,13697734770634168978,14117384571277345036,4 --trace-process-track-uuid=3190708990997080739`


==55792==END OF ADDITIONAL INFO

==55792==ABORTING

```
## Expected

The Rust ICC parser path should reject `mAB` A2B profiles whose `output_channels != 3`, matching the native skcms validator. No out-of-bounds read should be reachable from image decode.

## Root cause

All permalinks below are pinned to Chromium commit `4850635c95ef1c5d863ea9db3bf9c78d1878e0e3`.

1. `moxcms` accepts unsupported `mAB` channel combinations. [`third_party/rust/chromium_crates_io/vendor/moxcms-v0_8/src/reader.rs` L369-373](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:third_party/rust/chromium_crates_io/vendor/moxcms-v0_8/src/reader.rs;l=369-373). `if in_channels > 4 && out_channels > 4` only rejects profiles where both sides exceed 4, so `(in=1, out=1)` passes this channel-count gate and the parser returns an `mAB` lut with `out_channels = 1`. Upstream moxcms fixed this in commit [`2c24c00c2c`](https://github.com/awxkee/moxcms/commit/2c24c00c2c) on 2026-04-22 but the Chromium-vendored v0.8.1 copy has not been rerolled.
2. The Skia Rust FFI preserves any `output_channels ∈ 1..=4`. [`third_party/skia/rust/icc/FFI.rs` L543-548](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:third_party/skia/rust/icc/FFI.rs;l=543-548). The Apr 22 fix added `num_output_channels == 0 || > 4` as rejection criteria, but `1`, `2`, and `4` are still accepted for `mAB`.
3. The C++ bridge forwards the unsupported value into `skcms_A2B` and returns success. [`third_party/skia/rust/icc/FFI.cpp` L138-152](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:third_party/skia/rust/icc/FFI.cpp;l=138-152). `ToSkcmsA2B` only rejects `output_channels > 4` and writes `output_channels = 1` into the `skcms_A2B`. `SkCodecColorProfileRust.cpp` now correctly propagates the `ToSkcmsIccProfile` return, but the return is `true` because the struct passed the bridge's looser check.
4. Native skcms requires `mAB.output_channels == 3`, but only on its own parse path. [`third_party/skia/modules/skcms/skcms.cc` L952-955](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:third_party/skia/modules/skcms/skcms.cc;l=952-955). The Rust path bypasses this validator entirely because it produces the struct directly without going through `read_mAB_or_mBA`.
5. `clut()` has runtime sampling logic only for `output_channels == 3` or `4`. [`third_party/skia/modules/skcms/src/Transform_inl.h` L681-755](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:third_party/skia/modules/skcms/src/Transform_inl.h;l=681-755). The `assert(output_channels == 3 || output_channels == 4)` is compiled out in release/ASAN builds. For `output_channels == 1`, the code falls into the 4-channel `sample_clut_16` branch, which calls `gather_16(grid_16, 4*ix + k)` for each of R/G/B/A. The ICC CLUT payload is 4 bytes (`2^1 * 1 * 2`), and the Rust bridge pads it to an 8-byte `Vec<u8>` for normal gather safety. When interpolation samples `ix=1`, the 4-channel sampler's first `gather_16(grid_16, 4*ix + 0)` reaches byte offset 8, so the `load<uint16_t>` at [`Transform_inl.h` L97-101](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:third_party/skia/modules/skcms/src/Transform_inl.h;l=97-101) reads 2 bytes past the end of the allocation.
6. The read is reachable from image decode. [`skcms_ApproximatelyEqualProfiles` at `skcms.cc` L1780-1826](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:third_party/skia/modules/skcms/skcms.cc;l=1780-1826) is called from [`SkColorSpace::Make` at `SkColorSpace.cpp` L345](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:third_party/skia/src/core/SkColorSpace.cpp;l=345), which `SkEncodedInfo::makeImageInfo` invokes inside `blink::SkiaImageDecoderBase::OnSetData`. The probe runs `clut()` against 84 fixed-input pixels and triggers the OOB immediately; on a non-sanitizer build that happens to survive the probe, [`SkCodec::applyColorXform` at `SkCodec.cpp` L884-890](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:third_party/skia/src/codec/SkCodec.cpp;l=884-890) re-enters `clut()` per decoded row with the same `skcms_A2B` state.

## Kill-switch state

`kForceSkcmsICCParsing` in [`third_party/blink/common/features.cc` L984](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:third_party/blink/common/features.cc;l=984), propagated via [`content/common/skia_utils.cc` L42-43](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:content/common/skia_utils.cc;l=42-43), has flipped three times on Linux:

| Commit | Branch position | Date | Default |
| --- | --- | --- | --- |
| [`f84de7096c6ac`](https://chromium.googlesource.com/chromium/src/+/f84de7096c6ac) | 1609054 | 2026-04-02 | enabled (Rust off) |
| [`10cdd32446ab4`](https://chromium.googlesource.com/chromium/src/+/10cdd32446ab4) | 1614337 | 2026-04-14 | disabled (Rust on) |
| [`a80c946a0d916`](https://chromium.googlesource.com/chromium/src/+/a80c946a0d916) | 1619495 | 2026-04-23 07:16 -0700 | re-enabled (Rust off) |

Canary `149.0.7809.0` is cut at position `1619429` — 66 commits before the latest re-enable — so it ships with the Rust parser active by default. Dev `149.0.7795.0` (position ~1615530) is in the same window. Current main (post `1619495`) has the kill-switch on; the PoC needs `--disable-features=ForceSkcmsICCParsing` on a ToT build, but the validator mismatch remains in the tree.

## Distinction from prior reports

- `504103236` shares the same sink (`clut()` at `Transform_inl.h:100`) but uses the legacy `read_lut_a_to_b_type` (mft1/mft2) validator with `grid_points[i] = 0`. The Apr 22 fix enforces `grid_points[i] >= 2`, closing that trigger. This report reaches the same sink via `read_lut_abm_type` (mAB) with `output_channels = 1`, which remains accepted on the Rust path.
- `504160794` shares the same validator family (`read_lut_abm_type`) but a different sink (`select_curve_ops`). The Apr 22 fix rejects `input_channels > 4`, closing that trigger. This report stays in `1..=4` on both sides and therefore passes every check added by that fix.

The underlying defect is an invariant disagreement between the Rust parser (allows `output_channels ∈ {1, 2, 4}` for `mAB`) and the skcms sink (requires `== 3`). The Apr 22 return-value propagation fix does not apply because `ToSkcmsIccProfile()` succeeds.

## Suggested fix direction

Enforce `output_channels == 3` for `mAB` A2B in `third_party/skia/rust/icc/FFI.rs` and `third_party/skia/rust/icc/FFI.cpp`, matching native skcms. Separately, reroll the vendored moxcms to pick up upstream [`2c24c00c2c`](https://github.com/awxkee/moxcms/commit/2c24c00c2c). A regression test covering `(IN=1, OUT=1, GRID=2, WIDTH=2)` would catch the attached crash; broader channel-count tests should also cover the rejected-by-native `output_channels ∈ {1, 2, 4}` states.

#### Impact analysis

## Attack scenario

Any origin that serves a crafted `<img src=evil.png>` (or any other Blink image-decode consumer: `<picture>`, CSS `background-image`, SVG `url()`, `createImageBitmap`, canvas `drawImage`, worker `ImageDecoder`) triggers the OOB read during decode. No JavaScript, user interaction, feature flag, or CORS prompt is required.

---

### The cause

#### What version of Chrome have you found the security issue in?

149.0.7809.0 Canary Linux ASAN (branch position 1619429)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

M. Fauzan Wijaya (Gh05t666nero)

## Attachments

- [poc.html](attachments/poc.html) (text/html, 60 B)
- [make_icc_poc.py](attachments/make_icc_poc.py) (text/x-python, 3.7 KB)
- [evil.png](attachments/evil.png) (image/png, 196 B)
- [server.py](attachments/server.py) (text/x-python, 767 B)
- [asan.log](attachments/asan.log) (text/plain, 17.3 KB)
- [evil-g2.png](attachments/evil-g2.png) (image/png, 270 B)
- [evil-g3.png](attachments/evil-g3.png) (image/png, 273 B)
- [evil-g5.png](attachments/evil-g5.png) (image/png, 278 B)
- [evil-g10.png](attachments/evil-g10.png) (image/png, 287 B)
- [evil-g17.png](attachments/evil-g17.png) (image/png, 305 B)
- [evil-g50.png](attachments/evil-g50.png) (image/png, 373 B)
- [evil-g100.png](attachments/evil-g100.png) (image/png, 478 B)
- [evil-g255.png](attachments/evil-g255.png) (image/png, 806 B)
- [make_poc.py](attachments/make_poc.py) (text/x-python, 6.9 KB)
- [result.json](attachments/result.json) (application/json, 1.2 KB)
- [server.py](attachments/server_75905398.py) (text/x-python, 1.5 KB)
- [test.html](attachments/test.html) (text/html, 1.1 KB)
- [gen.py](attachments/gen.py) (text/x-python, 2.8 KB)
- [mab.png](attachments/mab.png) (image/png, 741 B)
- [read-b2a.py](attachments/read-b2a.py) (text/x-python, 1.9 KB)
- [repro.html](attachments/repro.html) (text/html, 64 B)
- [serve.py](attachments/serve.py) (text/x-python, 386 B)

## Timeline

### oj...@gmail.com (2026-04-24)

Missed this in the initial filing. Two things to add.

**1. Decode-time OOB reaches canvas `getImageData`, not only the probe.** A 256-entry `curv` input table that maps every byte of [`skcms_252_random_bytes`](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:third_party/skia/modules/skcms/skcms.cc;l=1751-1768) to `0x0000` and one of the four values missing from that array (`{10, 43, 192, 241}`) to `0xFFFF` makes the probe run with `lo = hi = 0` (safe) and decode run with `lo = hi = grid_size - 1` (OOB). The same `skcms_A2B` is re-used in [`SkCodec::applyColorXform` at `SkCodec.cpp:884-890`](https://source.chromium.org/chromium/chromium/src/+/4850635c95ef1c5d863ea9db3bf9c78d1878e0e3:third_party/skia/src/codec/SkCodec.cpp;l=884-890).

**2. The OOB read offset is attacker-controlled via `grid_size`.** `sample_clut_16` reads four u16 values starting at byte offsets `2*(4*(grid_size-1) + 0..3)` from the CLUT Vec. The Rust bridge pads the Vec for normal 3-channel gather safety, but the malformed `output_channels=1` state uses the 4-channel gather stride. For `grid=255`, the four loads start at CLUT byte offsets `2032`, `2034`, `2036`, and `2038`, while the padded Vec is 512 bytes long, so the read window starts about 1520 bytes past the allocation.

Repro on Linux Chrome Dev 149.0.7795.2 (non-ASAN, Rust ICC default-on, same branch-position window as Canary 7809):

1. Unpack the attached files into one directory.
2. `python3 server.py` (binds `127.0.0.1:7600`).
3. ```
   google-chrome-unstable --user-data-dir=$(mktemp -d) \
     --headless=new --dump-dom \
     http://127.0.0.1:7600/test.html
   
   ```

One non-ASAN run printed the following grid sweep output. The exact hex values can vary across fresh browser processes because they depend on adjacent heap state; the stable property is that the returned canvas pixel can change when the attacker changes `grid_size`.

```
[REPORT] {'grids': ['{
  "g2":   "fff800ff",
  "g3":   "00ff4aff",
  "g5":   "00010aff",
  "g10":  "88d45bff",
  "g17":  "000000ff",
  "g50":  "6b0014ff",
  "g100": "000000ff",
  "g255": "000000ff"
}']}

```

Each grid samples a different 4-u16 window via `canvas.getImageData` (some grids can return `000000ff` when the adjacent heap window is zero-initialized). The differing outputs across grid sizes show this is a JS-observable heap-content oracle, not just a sanitizer-only crash.

On the Canary ASAN build the same sequence aborts inside the JS-triggered canvas raster path (frames trimmed from the attached `asan.log`):

```
#0  skcms_private::hsw::clut                        Transform_inl.h:100
#4  SkCodec::applyColorXform                        SkCodec.cpp:887
#27 BaseRenderingContext2D::getImageDataInternal    base_rendering_context_2d.cc:444
#30 v8_canvas_rendering_context_2d::GetImageDataOperationCallback

```

Attachments: `make_poc.py`, `server.py`, `test.html`, `evil-g{2,3,5,10,17,50,100,255}.png`, `result.json`, `asan.log`.

### ns...@chromium.org (2026-04-24)

I verified this on Linux in 149.0.7795.0. I can't verify on other platforms, but I don't immediately see why this wouldn't repro.

### ns...@chromium.org (2026-04-24)

P1/S1 as this demonstrates memory corruption in the renderer process.

kjlubick@, please take a look. I can't quite verify this is not a dupe of [issue 504103236](https://issues.chromium.org/issues/504103236), since my canary asan build does not yet have <https://chromiumdash.appspot.com/commit/e990e7d6c8c99b2445fd3dc8fed8e5f5888771d7>.

### ch...@google.com (2026-04-25)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### se...@microsoft.com (2026-04-25)

Tentative fix in https://skia-review.googlesource.com/c/skia/+/1218736

### oj...@gmail.com (2026-04-25)

Additional write sink for the same Rust mAB validator gap (#1/#2 read sink stays as-is).

With `output_channels=4` and four parsed b\_curves, the loop at FFI.cpp:148-150 (`i < 4`) writes a 4th `skcms_Curve` (32 bytes) past `skcms_A2B::output_curves[3]`. That lands in `skcms_B2A::input_curves[0]`, putting attacker `table_entries` and a `table_16` heap pointer into a field the up-front memset in `ToSkcmsIccProfile` left zero. Default ASan does not catch intra-object overflows (<https://github.com/google/sanitizers/wiki/AddressSanitizerIntraObjectOverflow>), so verification is via gdb.

Repro on Chrome 149.0.7808.0 Dev (Linux ASAN, Rust ICC default-on):

1. `python3 serve.py` (binds 127.0.0.1:7203)
2. Run:

```
ASAN_OPTIONS=symbolize=1:external_symbolizer_path=$ASAN/llvm-symbolizer:abort_on_error=0 \
  gdb -q -batch -ex "source read-b2a.py" -ex run --args $ASAN/chrome \
    --user-data-dir=$(mktemp -d) --headless=new --single-process \
    http://127.0.0.1:7203/repro.html

```

`read-b2a.py` reads 32 bytes at offset 560 (`skcms_B2A::input_curves[0]`):

```
profile heap base    = 0x00007d8ff5539280
B2A.input_curves[0]  table_entries = 0x00000100
                     table_8       = 0x0000000000000000
                     table_16      = 0x00007d4ff5290b00
OOB write confirmed: 4th b_curve overwrote B2A.input_curves[0]

```

`0x100 = 256` matches the `count` of the 4th `curv` tag in mab.png; `table_16` points into the Rust-owned curve table.

---

Per #7, CL 1218736 already closes this. The new `output_channels != 3` gate in `ToSkcmsA2B` rejects the input before the buggy loop, and the regression test row covers `output_channels=4`. Posting only so the issue thread documents both the read sink (#1/#2) and this write sink reachable through the same gap. The write target `B2A.input_curves[0]` is unread by current consumers (gated on `has_B2A`), so this is OOB write per CWE-787 with demonstrable corruption, not a controlled-write primitive (i think).

### dx...@google.com (2026-04-27)

Project: skia  

Branch:  main  

Author:  Sergio Gonzalez Martin [sergiog@microsoft.com](mailto:sergiog@microsoft.com)  

Link:    <https://skia-review.googlesource.com/1218736>

[rust icc] Require output\_channels == 3 for A2B, matching skcms

---


Expand for full commit details
```
     
    A crafted mAB tag with output_channels=1 passes the Rust parser and 
    bridge but causes a heap-buffer-overflow in skcms clut() during PNG 
    decode. The previous check (> 4) was too permissive. 
     
    Add regression tests for output_channels ∈ {1, 2, 4} in 
    RustIcc_reject_malformed_a2b, and fix RustIcc_a2b_b2a_flags to supply 
    valid A2B data (3 output channels with curves). 
     
    Bug: 506010945 
    Change-Id: Ic2618a2dad60955eab010bf4efcc9b70d0fb5b39 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1218736 
    Reviewed-by: Florin Malita <fmalita@google.com> 
    Commit-Queue: Kaylee Lubick <kjlubick@google.com> 
    Reviewed-by: Kaylee Lubick <kjlubick@google.com>

```

---

Files:

- M `rust/icc/FFI.cpp`
- M `rust/icc/FFI.rs`
- M `tests/RustIccTest.cpp`

---

Hash: acb0421565d3ea8cf334985912301890fa7c8433  

Date: Fri Apr 24 20:33:08 2026


---

### dx...@google.com (2026-04-28)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7797913>

Roll Skia from e59ca98647fe to d3934f5b07cc (9 revisions)

---


Expand for full commit details
```
     
    https://skia.googlesource.com/skia.git/+log/e59ca98647fe..d3934f5b07cc 
     
    2026-04-27 kjlubick@google.com Make local optimized copy of program when creating SkRP version 
    2026-04-27 recipe-mega-autoroller@chops-service-accounts.iam.gserviceaccount.com Roll recipe dependencies (trivial). 
    2026-04-27 sergiog@microsoft.com [rust icc] Make B2A conversion failure non-fatal in ToSkcmsIccProfile 
    2026-04-27 recipe-mega-autoroller@chops-service-accounts.iam.gserviceaccount.com Roll recipe dependencies (trivial). 
    2026-04-27 fmalita@google.com [skottie] Randomize order support 
    2026-04-27 sergiog@microsoft.com [rust icc] Require output_channels == 3 for A2B, matching skcms 
    2026-04-27 skia-autoroll@skia-public.iam.gserviceaccount.com Manual roll ANGLE from 887d15753e30 to 1a95cc9cfeb4 (1 revision) 
    2026-04-27 kjlubick@google.com Avoid removing too many stack entries in SkRP during discard_stack 
    2026-04-27 recipe-mega-autoroller@chops-service-accounts.iam.gserviceaccount.com Roll recipe dependencies (trivial). 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/skia-autoroll 
    Please CC bwils@google.com,skiabot@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Skia: https://bugs.chromium.org/p/skia/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:mac14.arm64-blink-rel;luci.chromium.try:win_optional_gpu_tests_rel 
    Cq-Do-Not-Cancel-Tryjobs: true 
    Bug: chromium:452666425,chromium:506010945 
    Tbr: bwils@google.com 
    Change-Id: I37126b904e1db674dc9953a7bcf67002bbc507af 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7797913 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1621463}

```

---

Files:

- M `DEPS`
- M `third_party/skia`

---

Hash: [fca4d626eacac62a269a20155bc563021139c509](https://chromiumdash.appspot.com/commit/fca4d626eacac62a269a20155bc563021139c509)  

Date: Tue Apr 28 01:24:59 2026


---

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

Polite request for reward reassessment under the pre-April-30 framework that applies to this report (snapshot: <https://web.archive.org/web/20260403162256/https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules>). Please add the Security-VRP-Reassessment-Request hotlist (id: 8186354) if I'm not able to do so myself.

The rationale "Baseline. User information disclosure" ($2,000) maps to the Other vulnerability classes table. I'd like to ask whether the report could be considered against the Memory corruption table instead.

Footnote [3] of the Memory corruption table explicitly covers renderer OOB reads: "Reports of renderer OOB reads or DCHECK / SEGV / etc. bugs in V8, without demonstration of write or RCE, are only eligible for baseline reward amounts." That sets the eligible floor at renderer baseline ($7,000), not at User information disclosure baseline ($2,000).

The "Access to a value versus the potential for RCE" section allows discretion to use a lower info-disclosure-consistent amount only when the report does not demonstrate a write or attacker control. [Comment #8](https://issues.chromium.org/issues/506010945#comment8) (Apr 25, three days before the fix landed Apr 28) documents an additional OOB write reachable through the same Rust mAB validator gap, with gdb-confirmed evidence: profile heap base 0x00007d8ff5539280, B2A.input\_curves[0].table\_entries 0x00000100 (matching the 4th curv tag count in mab.png), table\_16 0x00007d4ff5290b00 (Rust-owned curve table pointer). I disclaimed this as a controlled-write primitive, but it is a demonstrated write per CWE-787, which would seem to remove the basis for the info-disclosure-tier discretion. [Comment #2](https://issues.chromium.org/issues/506010945#comment2) additionally documents attacker-controlled OOB read offset via grid\_size (about 1520 bytes past allocation at grid=255) and a JS-observable heap content oracle via canvas.getImageData.

Given the demonstrated write plus attacker-controlled offset, the report appears to fit "High-quality report of demonstrated memory corruption" (renderer: Up to $10,000) rather than baseline alone.

The report also identifies three specific commits introducing the kForceSkcmsICCParsing flag flips (f84de7096c6ac on 2026-04-02, 10cdd32446ab4 on 2026-04-14, a80c946a0d916 on 2026-04-23), which appears to meet the $1,000 specific-commit bisect bonus criteria.

To be explicit about what I'm not asking: not the controlled-write tier ([comment #8](https://issues.chromium.org/issues/506010945#comment8) already disclaimed this), and not the patch bonus (the suggestion was in the report text rather than uploaded to Gerrit). Just the demonstrated-memory-corruption tier plus the bisect bonus.

Thanks for considering.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/506010945)*
