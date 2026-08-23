# AddressSanitizer heap-buffer-overflow in skcms CLUT from a PNG iCCP chunk on the default Rust ICC path

| Field | Value |
|-------|-------|
| **Issue ID** | [504103236](https://issues.chromium.org/issues/504103236) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | oj...@gmail.com |
| **Assignee** | se...@microsoft.com |
| **Created** | 2026-04-18 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

AddressSanitizer heap-buffer-overflow in skcms CLUT from a PNG iCCP chunk on the default Rust ICC path

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

A crafted PNG `iCCP` chunk reaches `skcms` with `A2B.input_channels=2`, `A2B.output_channels=4`, and `grid_points=[2,0,0,0]` on Chromium's default Rust ICC parser path. In `clut()`, `grid_points[1] - 1` becomes `-1`, which reaches `sample_clut_16(grid_16, -1, &R,&G,&B,&A)`. The 4-channel `sample_clut_16` uses `gather_16`, whose `load<uint16_t>` goes through the instrumented `memcpy` in `Transform_inl.h`, so AddressSanitizer reports a clean `heap-buffer-overflow` at `Transform_inl.h:100` with a 2-byte read before a Rust-owned `Vec<u8>`.

The read fires during PNG decode itself - specifically inside `SkColorSpace::Make` -> `skcms_ApproximatelyEqualProfiles` called from `SkEncodedInfo::makeImageInfo` on `blink::SkiaImageDecoderBase::OnSetData`. A plain `<img src=evil.png>` is enough. No canvas, no JavaScript, no feature flag, no user interaction.

## Steps to Reproduce

1. Put `poc.html` and `evil.png` in the same directory and serve them locally:
   ```
   python3 -m http.server 7200 --bind 127.0.0.1
   
   ```
2. Launch Chrome against a fresh profile and open the PoC:
   ```
   ASAN_OPTIONS=symbolize=1:external_symbolizer_path=/path/to/asan-dev/llvm-symbolizer \
   /path/to/asan-dev/chrome \
     --user-data-dir=/tmp/icc-asan \
     --no-sandbox \
     http://127.0.0.1:7200/poc.html
   
   ```
3. Chrome's renderer aborts with `AddressSanitizer: heap-buffer-overflow`:

```
[5656:5656:0419/015841.538209:WARNING:sandbox/policy/linux/sandbox_linux.cc:404] InitializeSandbox() called with multiple threads in process gpu-process.
[5616:5616:0419/015841.604702:WARNING:chrome/browser/signin/account_consistency_mode_manager.cc:74] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
[5616:5616:0419/015841.987596:ERROR:dbus/object_proxy.cc:572] Failed to call method: org.freedesktop.DBus.Properties.GetAll: object_path= /org/freedesktop/UPower/devices/DisplayDevice: org.freedesktop.DBus.Error.ServiceUnknown: The name org.freedesktop.UPower was not provided by any .service files
[5616:5616:0419/015841.987644:WARNING:dbus/property.cc:174] GetAll request failed for: org.freedesktop.UPower.Device
[5616:5616:0419/015842.021037:WARNING:ui/base/idle/idle_linux.cc:111] None of the known D-Bus ScreenSaver services could be used.
=================================================================
==5728==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x781b5f7721f8 at pc 0x5943cf707a49 bp 0x7fffc7b69490 sp 0x7fffc7b69488
READ of size 2 at 0x781b5f7721f8 thread T0 (chrome)
    #0 0x5943cf707a48 in skcms_private::hsw::clut(unsigned int, unsigned int, unsigned char const*, unsigned char const*, unsigned char const*, float vector[8]*, float vector[8]*, float vector[8]*, float vector[8]*) third_party/skia/modules/skcms/src/Transform_inl.h:100:5
    #1 0x5943cf6fcad9 in skcms_private::hsw::exec_stages(skcms_private::Op const*, void const**, char const*, char*, int) third_party/skia/modules/skcms/src/Transform_inl.h:760:5
    #2 0x5943cf6f42ba in skcms_private::hsw::run_program(skcms_private::Op const*, void const**, long, char const*, char*, int, unsigned long, unsigned long) third_party/skia/modules/skcms/src/Transform_inl.h:1586:9
    #3 0x5943cf6ea90d in skcms_Transform third_party/skia/modules/skcms/skcms.cc:3089:5
    #4 0x5943cf6e8f4d in skcms_ApproximatelyEqualProfiles third_party/skia/modules/skcms/skcms.cc:1782:10
    #5 0x5943cf2b9b19 in SkColorSpace::Make(skcms_ICCProfile const&) third_party/skia/src/core/SkColorSpace.cpp:345:16
    #6 0x5943e8c38779 in SkEncodedInfo::makeImageInfo() const third_party/skia/src/codec/SkEncodedInfo.cpp:19:46
    #7 0x5943f7ac753f in blink::SkiaImageDecoderBase::OnSetData(scoped_refptr<blink::SegmentReader>) third_party/skia/include/codec/SkCodec.h:233:55
    #8 0x5943f762bf09 in blink::ImageDecoder::SetData(scoped_refptr<blink::SegmentReader>, bool) third_party/blink/renderer/platform/image-decoders/image_decoder.h:286:5
    #9 0x5943f7a85a54 in blink::ImageDecoder::CreateByMimeType(blink::String, scoped_refptr<blink::SegmentReader>, bool, blink::ImageDecoder::AlphaOption, blink::ImageDecoder::HighBitDepthDecodingOption, blink::ColorBehavior, cc::AuxImage, unsigned long, SkISize const&, blink::ImageDecoder::AnimationOption) third_party/blink/renderer/platform/image-decoders/image_decoder.cc:353:14
    #10 0x5943f7a84787 in blink::ImageDecoder::Create(scoped_refptr<blink::SegmentReader>, bool, blink::ImageDecoder::AlphaOption, blink::ImageDecoder::HighBitDepthDecodingOption, blink::ColorBehavior, cc::AuxImage, unsigned long, SkISize const&, blink::ImageDecoder::AnimationOption) third_party/blink/renderer/platform/image-decoders/image_decoder.cc:290:10
    #11 0x5943f7624ee0 in blink::DeferredImageDecoder::Create(scoped_refptr<blink::SharedBuffer>, bool, blink::ImageDecoder::AlphaOption, blink::ColorBehavior) third_party/blink/renderer/platform/image-decoders/image_decoder.h:230:12
    #12 0x5943f7539cd0 in blink::BitmapImage::SetData(scoped_refptr<blink::SharedBuffer>, bool) third_party/blink/renderer/platform/graphics/bitmap_image.cc:240:14
    #13 0x5943f60f6930 in blink::ImageResourceContent::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ResourceStatus, blink::ImageResourceContent::UpdateImageOption, bool, bool) third_party/blink/renderer/core/loader/resource/image_resource_content.cc:514:35
    #14 0x5943f60e7047 in blink::ImageResource::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ImageResourceContent::UpdateImageOption, bool) third_party/blink/renderer/core/loader/resource/image_resource.cc:677:31
    #15 0x5943f60e7d8a in blink::ImageResource::AppendData(std::__Cr::variant<blink::SegmentedBuffer, base::span<char const, 18446744073709551615ul, char const*>>) third_party/blink/renderer/core/loader/resource/image_resource.cc:460:7
    #16 0x5943df2cd4ee in blink::ResourceLoader::DidReceiveDataImpl(std::__Cr::variant<blink::SegmentedBuffer, base::span<char const, 18446744073709551615ul, char const*>>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1067:14
    #17 0x5943df2cfd15 in non-virtual thunk to blink::ResourceLoader::DidReceiveData(base::span<char const, 18446744073709551615ul, char const*>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1041:3
    #18 0x5943df30a28b in blink::ResponseBodyLoader::OnStateChange() third_party/blink/renderer/platform/loader/fetch/response_body_loader.cc:433:12
    #19 0x5943df2bbbda in blink::ResourceLoader::DidStartLoadingResponseBodyInternal(blink::BytesConsumer&) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:346:28
    #20 0x5943df2c813b in blink::ResourceLoader::DidReceiveResponse(blink::WebURLResponse const&, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:787:3
    #21 0x5943df3369ae in blink::BackgroundURLLoader::Context::OnReceivedResponse(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int) third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:492:14
    #22 0x5943df336efe in void base::internal::DecayedFunctorTraits<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>::Invoke<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>, int>(void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&, int&&) base/functional/bind_internal.h:740:12
    #23 0x5943df336c4a in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>>, void (int)>::RunOnce(base::internal::BindStateBase*, int) base/functional/bind_internal.h:932:12
    #24 0x5943daa5bfd3 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (int)>&&, int&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (int)>, int>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/callback.h:155:12
    #25 0x5943df333fc7 in blink::BackgroundURLLoader::Context::RunTasksOnMainThread() base/functional/callback.h:155:12
    #26 0x5943df32c670 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Context::*&&)(), scoped_refptr<blink::BackgroundURLLoader::Context>&&>, base::internal::BindState<true, true, false, void (blink::BackgroundURLLoader::Context::*)(), scoped_refptr<blink::BackgroundURLLoader::Context>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #27 0x5943e6a347e3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #28 0x5943e6aa58ec in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #29 0x5943e6aa478a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #30 0x5943e68f247f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #31 0x5943e6aa6fd4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12
    #32 0x5943e69aeb20 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #33 0x5943f305318a in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:337:16
    #34 0x5943e2a1a2ff in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #35 0x5943e2a1b637 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #36 0x5943e2a1e348 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #37 0x5943e2a17d01 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:356:36
    #38 0x5943e2a182fc in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:369:10
    #39 0x5943ce68b2a9 in ChromeMain chrome/app/chrome_main.cc:194:12
    #40 0x7beb6122a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #41 0x7beb6122a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #42 0x5943ce5b0029 in _start (/home/ubuntu/workspaces/chromium/asan-chrome/chrome+0x10fdf029) (BuildId: 250795ae951b3a3b)

0x781b5f7721f8 is located 8 bytes before 32-byte region [0x781b5f772200,0x781b5f772220)
allocated by thread T0 (chrome) here:
    #0 0x5943ce650934 in malloc (/home/ubuntu/workspaces/chromium/asan-chrome/chrome+0x1107f934) (BuildId: 250795ae951b3a3b)
    #1 0x5944017a54bd in <std::alloc::System as core::alloc::global::GlobalAlloc>::alloc third_party/rust-toolchain/lib/rustlib/src/rust/library/std/src/sys/alloc/unix.rs:14:22
    #2 0x5944017a54bd in __rustc::__rust_alloc build/rust/allocator/lib.rs:67:20
    #3 0x594401a4c24f in alloc::alloc::alloc third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:101:9
    #4 0x594401a4c24f in <alloc::alloc::Global>::alloc_impl_runtime third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:210:73
    #5 0x594401a4c24f in <alloc::alloc::Global>::alloc_impl third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:332:9
    #6 0x594401a4c24f in <alloc::alloc::Global as core::alloc::Allocator>::allocate third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs:449:14
    #7 0x594401a4c24f in <alloc::raw_vec::RawVecInner>::try_allocate_in third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/raw_vec/mod.rs:465:47

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/modules/skcms/src/Transform_inl.h:100:5 in skcms_private::hsw::clut(unsigned int, unsigned int, unsigned char const*, unsigned char const*, unsigned char const*, float vector[8]*, float vector[8]*, float vector[8]*, float vector[8]*)
Shadow bytes around the buggy address:
  0x781b5f771f00: fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd fd fa
  0x781b5f771f80: f7 fa fd fd fd fa f7 fa fd fd fd fd f7 fa fd fd
  0x781b5f772000: fd fa f7 fa fd fd fd fa f7 fa fd fd fd fa f7 fa
  0x781b5f772080: fd fd fd fa f7 fa 00 00 00 00 f7 fa 00 00 00 fa
  0x781b5f772100: f7 fa fd fd fd fd f7 fa 00 00 00 fa f7 fa 00 00
=>0x781b5f772180: 05 fa f7 fa 00 00 00 00 f7 fa fd fd fd fd f7[fa]
  0x781b5f772200: 00 00 00 00 f7 fa 00 00 00 00 fa fa fa fa fa fa
  0x781b5f772280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x781b5f772300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x781b5f772380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x781b5f772400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==5728==ADDITIONAL INFO

==5728==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5943df3330f8 in blink::BackgroundURLLoader::Context::PostTaskToMainThread(blink::CrossThreadOnceFunction<void ()>) third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:422:52
    #1 0x5943e773f1d3 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:103:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=5618 --enable-crash-reporter=, --noerrdialogs --user-data-dir=/tmp/vrp-asan-final --change-stack-guard-on-fork=enable --no-sandbox --file-url-path-alias=/gen=/home/ubuntu/workspaces/chromium/asan-chrome/gen --ozone-platform=headless --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1776538144286546 --launch-time-ticks=577576962 --shared-files=v8_context_snapshot_data:100 --field-trial-handle=3,i,17917323113847744871,1648601036738241172,262144 --disable-features=PaintHolding --variations-seed-version --pseudonymization-salt-handle=7,i,4452130130514639713,14902716215317280498,4 --trace-process-track-uuid=3190708990997080739 --enable-logging=stderr`


==5728==END OF ADDITIONAL INFO

==5728==ABORTING

```

4. Re-run with skcms forced and the crash disappears:
   ```
   ASAN_OPTIONS=symbolize=1:external_symbolizer_path=/path/to/asan-dev/llvm-symbolizer \
   /path/to/asan-dev/chrome \
     --user-data-dir=/tmp/icc-skcms \
     --no-sandbox \
     --enable-features=ForceSkcmsICCParsing \
     http://127.0.0.1:7200/poc.html
   
   ```

## Result

- Default run: AddressSanitizer reports a `heap-buffer-overflow` READ of size 2 in `skcms_private::hsw::clut`, called from the PNG image decoder. Allocation origin is a Rust `Vec<u8>` from `<alloc::raw_vec::RawVecInner>::try_allocate_in`.
- Kill-switch run (`--enable-features=ForceSkcmsICCParsing`): no crash, PNG decodes normally.

The differential is the proof that the Rust ICC parser path is the source of the OOB.

## Root Cause

1. `moxcms` accepts an `mft2` tag with `input_channels=2, output_channels=4`. The check in `read_lut_a_to_b_type` uses `(in_chan==3 || out_chan==4) || (in_chan==4 || out_chan==3)`, so `(2,4)` passes because `out_chan==4` is true.
2. `third_party/skia/rust/icc/FFI.rs` (`LutWarehouse::Lut` arm) maps any `num_input_channels` other than 3 or 4 to `grid_points=[grid_size, 0, 0, 0]`, leaving a zero in an active dimension.
3. `rust_icc::ToSkcmsA2B` in `FFI.cpp` accepts `input_channels=2` because the check is only `< 1 || > 4`, and writes the half-populated `skcms_A2B` (including the zero dimension) to the output.
4. `SkCodecs::MakeICCProfileWithRust` in `SkCodecColorProfileRust.cpp` discards the return value of `rust_icc::ToSkcmsIccProfile`, so any future validator failure in the FFI would also flow through.
5. `skcms_ApproximatelyEqualProfiles`, called from `SkColorSpace::Make` during image decode, runs `skcms_Transform` over 84 probe pixels. `clut()` in `Transform_inl.h` computes `grid_points[1] - 1 = -1`, producing `ix = -1`. For `output_channels=4` the dispatch is `sample_clut_16(grid_16, -1, &R, &G, &B, &A)`, which issues `gather_16(grid_16, 4*ix + k)` for each of R,G,B,A. The first load reads 2 bytes at `grid_16 + 2*(4*(-1)+0) = grid_16 - 8`, which is before the Rust-owned `Vec<u8>`.

The 3-channel variant of the same bug exists (`output_channels=3`) but uses the AVX2 `gather_48` path (`vpgatherdq`), which is not instrumented by AddressSanitizer. The 4-channel variant in this report routes through `gather_16` -> `load<uint16_t>` -> `memcpy(&val, ptr, 2)` at `Transform_inl.h:100`, which is instrumented, so ASAN catches the read cleanly.

## Attachments

- `poc.html` - one-line HTML with `<img src=evil.png>`. No JavaScript.
- `evil.png` - minimized 193-byte PNG with the crafted `iCCP` chunk.
- `make_icc_poc.py` - deterministic generator for `evil.png`.

#### Impact analysis

## Security Impact

Any origin that serves `<img src=evil.png>` (or any other Blink image-decode consumer such as `<picture>`, CSS `background-image`, `createImageBitmap`, or canvas `drawImage`) triggers a 2-byte OOB read that ASAN confirms as a `heap-buffer-overflow` in the renderer. On non-sanitizer builds the same read returns whatever bytes precede the Rust-owned CLUT allocation; if the read lands on a page boundary it crashes the renderer process (remote DoS via image load).

The allocation that is being read underflowed is a Rust `Vec<u8>` that holds the attacker-controlled CLUT, so the bug is a memory-safety violation at the Rust/C++ FFI boundary: the Rust side installs an `skcms_A2B` struct whose `grid_points[1]` is `0`, and the C++ side consumes it as a valid LUT dimension.

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

- [make_icc_poc.py](attachments/make_icc_poc.py) (text/x-python, 4.0 KB)
- [poc.html](attachments/poc.html) (text/html, 60 B)
- [evil.png](attachments/evil.png) (image/png, 193 B)

## Timeline

### ar...@google.com (2026-04-21)

Thanks!

2 byte OOB in the renderer process, via the image decoding path: Medium severity.

From the source code, I see @kj...@google.com

<https://skia.googlesource.com/skcms/+/15db2430b6288ac0a6b23e3f6a163fa016a3fab1>

just fixed something potentially similar to what is reported here.

- [Bug 498869813](https://issues.chromium.org/issues/498869813)
- [Bug 498927031](https://issues.chromium.org/issues/498927031)

---

Could you please check if this is a duplicate? If not, could you please help route this bug to the right owner?

### ar...@google.com (2026-04-21)

I reproduced on chromium-149.0.7795.2-linux-asan.zip:

```
[3587319:3587319:0421/160058.128577:ERROR:dbus/object_proxy.cc:572] Failed to call method: org.freedesktop.DBus.NameHas                                                                                                         │
│ Owner: object_path= /org/freedesktop/DBus: unknown error type:                                                                                                                                                                  │
│     #0 0x5599127a3a48 in skcms_private::hsw::clut(unsigned int, unsigned int, unsigned char const*, unsigned char const                                                                                                         │
│ *, unsigned char const*, float vector[8]*, float vector[8]*, float vector[8]*, float vector[8]*) third_party/skia/modul                                                                                                         │
│ es/skcms/src/Transform_inl.h:100:5                                                                                                                                                                                              │
│     #1 0x559912798ad9 in skcms_private::hsw::exec_stages(skcms_private::Op const*, void const**, char const*, char*, in                                                                                                         │
│ t) third_party/skia/modules/skcms/src/Transform_inl.h:760:5                                                                                                                                                                     │
│     #2 0x5599127902ba in skcms_private::hsw::run_program(skcms_private::Op const*, void const**, long, char const*, cha                                                                                                         │
│ r*, int, unsigned long, unsigned long) third_party/skia/modules/skcms/src/Transform_inl.h:1586:9                                                                                                                                │
│     #3 0x55991278690d in skcms_Transform third_party/skia/modules/skcms/skcms.cc:3089:5                                                                                                                                         │
│     #4 0x559912784f4d in skcms_ApproximatelyEqualProfiles third_party/skia/modules/skcms/skcms.cc:1782:10                                                                                                                       │
│     #5 0x559912355b19 in SkColorSpace::Make(skcms_ICCProfile const&) third_party/skia/src/core/SkColorSpace.cpp:345:16                                                                                                          │
│     #6 0x55992bcd4779 in SkEncodedInfo::makeImageInfo() const third_party/skia/src/codec/SkEncodedInfo.cpp:19:46                                                                                                                │
│     #7 0x55993ab6353f in blink::SkiaImageDecoderBase::OnSetData(scoped_refptr<blink::SegmentReader>) third_party/skia/i                                                                                                         │
│ nclude/codec/SkCodec.h:233:55                                                                                                                                                                                                   │
│     #8 0x55993a6c7f09 in blink::ImageDecoder::SetData(scoped_refptr<blink::SegmentReader>, bool) third_party/blink/rend                                                                                                         │
│ erer/platform/image-decoders/image_decoder.h:286:5                                                                                                                                                                              │
│     #9 0x55993ab21a54 in blink::ImageDecoder::CreateByMimeType(blink::String, scoped_refptr<blink::SegmentReader>, bool                                                                                                         │
│ , blink::ImageDecoder::AlphaOption, blink::ImageDecoder::HighBitDepthDecodingOption, blink::ColorBehavior, cc::AuxImage                                                                                                         │
│ , unsigned long, SkISize const&, blink::ImageDecoder::AnimationOption) third_party/blink/renderer/platform/image-decode                                                                                                         │
│ rs/image_decoder.cc:353:14                                                                                                                                                                                                      │
│     #10 0x55993ab20787 in blink::ImageDecoder::Create(scoped_refptr<blink::SegmentReader>, bool, blink::ImageDecoder::A                                                                                                         │
│ lphaOption, blink::ImageDecoder::HighBitDepthDecodingOption, blink::ColorBehavior, cc::AuxImage, unsigned long, SkISize                                                                                                         │
│  const&, blink::ImageDecoder::AnimationOption) third_party/blink/renderer/platform/image-decoders/image_decoder.cc:290:                                                                                                         │
│ 10                                                                                                                                                                                                                              │
│     #11 0x55993a6c0ee0 in blink::DeferredImageDecoder::Create(scoped_refptr<blink::SharedBuffer>, bool, blink::ImageDec                                                                                                         │
│ oder::AlphaOption, blink::ColorBehavior) third_party/blink/renderer/platform/image-decoders/image_decoder.h:230:12                                                                                                              │
│     #12 0x55993a5d5cd0 in blink::BitmapImage::SetData(scoped_refptr<blink::SharedBuffer>, bool) third_party/blink/rende                                                                                                         │
│ rer/platform/graphics/bitmap_image.cc:240:14                                                                                                                                                                                    │
│     #13 0x559939192930 in blink::ImageResourceContent::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ResourceS                                                                                                         │
│ tatus, blink::ImageResourceContent::UpdateImageOption, bool, bool) third_party/blink/renderer/core/loader/resource/imag                                                                                                         │
│ e_resource_content.cc:514:35                                                                                                                                                                                                    │
│     #14 0x559939183047 in blink::ImageResource::UpdateImage(scoped_refptr<blink::SharedBuffer>, blink::ImageResourceCon                                                                                                         │
│ tent::UpdateImageOption, bool) third_party/blink/renderer/core/loader/resource/image_resource.cc:677:31                                                                                                                         │
│     #15 0x559939183d8a in blink::ImageResource::AppendData(std::__Cr::variant<blink::SegmentedBuffer, base::span<char c                                                                                                         │
│ onst, 18446744073709551615ul, char const*>>) third_party/blink/renderer/core/loader/resource/image_resource.cc:460:7                                                                                                            │
│     #16 0x5599223694ee in blink::ResourceLoader::DidReceiveDataImpl(std::__Cr::variant<blink::SegmentedBuffer, base::sp                                                                                                         │
│ an<char const, 18446744073709551615ul, char const*>>) third_party/blink/renderer/platform/loader/fetch/resource_loader.                                                                                                         │
│ cc:1067:14                                                                                                                                                                                                                      │
│     #17 0x55992236bd15 in non-virtual thunk to blink::ResourceLoader::DidReceiveData(base::span<char const, 18446744073                                                                                                         │
│ 709551615ul, char const*>) third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:1041:3                                                                                                                           │
│     #18 0x5599223a628b in blink::ResponseBodyLoader::OnStateChange() third_party/blink/renderer/platform/loader/fetch/r                                                                                                         │
│ esponse_body_loader.cc:433:12                                                                                                                                                                                                   │
│     #19 0x559922357bda in blink::ResourceLoader::DidStartLoadingResponseBodyInternal(blink::BytesConsumer&) third_party                                                                                                         │
│ /blink/renderer/platform/loader/fetch/resource_loader.cc:346:28                                                                                                                                                                 │
│     #20 0x55992236413b in blink::ResourceLoader::DidReceiveResponse(blink::WebURLResponse const&, std::__Cr::variant<mo                                                                                                         │
│ jo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>)                                                                                                         │
│  third_party/blink/renderer/platform/loader/fetch/resource_loader.cc:787:3                                                                                                                                                      │
│     #21 0x5599223d29ae in blink::BackgroundURLLoader::Context::OnReceivedResponse(mojo::StructPtr<network::mojom::URLRe                                                                                                         │
│ sponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__C                                                                                                         │
│ r::optional<mojo_base::BigBuffer>, int) third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_load                                                                                                         │
│ er.cc:492:14                                                                                                                                                                                                                    │
│     #22 0x5599223d2efe in void base::internal::DecayedFunctorTraits<void (blink::BackgroundURLLoader::Context::*)(mojo:                                                                                                         │
│ :StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, b                                                                                                         │
│ link::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Cont                                                                                                         │
│ ext>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std                                                                                                         │
│ ::__Cr::optional<mojo_base::BigBuffer>&&>::Invoke<void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network                                                                                                         │
│ ::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuf                                                                                                         │
│ fer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>, mojo::Struct                                                                                                         │
│ Ptr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_ba                                                                                                         │
│ se::BigBuffer>, int>(void (blink::BackgroundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, st                                                                                                         │
│ d::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<moj                                                                                                         │
│ o_base::BigBuffer>, int), scoped_refptr<blink::BackgroundURLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResp                                                                                                         │
│ onseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&, int&&                                                                                                         │
│ ) base/functional/bind_internal.h:740:12                                                                                                                                                                                        │
│     #23 0x5599223d2c4a in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Conte                                                                                                         │
│ xt::*&&)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBase<mojo::DataPipeCons                                                                                                         │
│ umerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refptr<blink::BackgroundU                                                                                                         │
│ RLLoader::Context>&&, mojo::StructPtr<network::mojom::URLResponseHead>&&, mojo::ScopedHandleBase<mojo::DataPipeConsumer                                                                                                         │
│ Handle>&&, std::__Cr::optional<mojo_base::BigBuffer>&&>, base::internal::BindState<true, true, false, void (blink::Back                                                                                                         │
│ groundURLLoader::Context::*)(mojo::StructPtr<network::mojom::URLResponseHead>, std::__Cr::variant<mojo::ScopedHandleBas                                                                                                         │
│ e<mojo::DataPipeConsumerHandle>, blink::SegmentedBuffer>, std::__Cr::optional<mojo_base::BigBuffer>, int), scoped_refpt                                                                                                         │
│ r<blink::BackgroundURLLoader::Context>, mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::                                                                                                         │
│ DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>>, void (int)>::RunOnce(base::internal::BindStateBase                                                                                                         │
│ *, int) base/functional/bind_internal.h:932:12                                                                                                                                                                                  │
│     #24 0x55991daf7fd3 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (int)>&&, int&&                                                                                                         │
│ >, base::internal::BindState<false, true, true, base::OnceCallback<void (int)>, int>, void ()>::RunOnce(base::internal:                                                                                                         │
│ :BindStateBase*) base/functional/callback.h:155:12                                                                                                                                                                              │
│     #25 0x5599223cffc7 in blink::BackgroundURLLoader::Context::RunTasksOnMainThread() base/functional/callback.h:155:12                                                                                                         │
│     #26 0x5599223c8670 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::BackgroundURLLoader::Conte                                                                                                         │
│ xt::*&&)(), scoped_refptr<blink::BackgroundURLLoader::Context>&&>, base::internal::BindState<true, true, false, void (b                                                                                                         │
│ link::BackgroundURLLoader::Context::*)(), scoped_refptr<blink::BackgroundURLLoader::Context>>, void ()>::RunOnce(base::                                                                                                         │
│ internal::BindStateBase*) base/functional/bind_internal.h:740:12                                                                                                                                                                │
│     #27 0x559929ad07e3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12                                                                                                                │
│     #28 0x559929b418ec in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyN                                                                                                         │
│ ow*) base/task/common/task_annotator.h:112:5                                                                                                                                                                                    │
│     #29 0x559929b4078a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/seq                                                                                                         │
│ uence_manager/thread_controller_with_message_pump_impl.cc:336:40                                                                                                                                                                │
│     #30 0x55992998e47f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_de                                                                                                         │
│ fault.cc:42:55                                                                                                                                                                                                                  │
│     #31 0x559929b42fd4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDe                                                                                                         │
│ lta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12                                                                                                                                              │
│     #32 0x559929a4ab20 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14                                                                                                                                     │
│     #33 0x5599360ef18a in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:337:16                                                                                                           │
│     #34 0x559925ab62ff in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664                                                                                                         │
│ :14                                                                                                                                                                                                                             │
│     #35 0x559925ab7637 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<ch                                                                                                         │
│ ar>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/conten                                                                                                         │
│ t_main_runner_impl.cc:771:12                                                                                                                                                                                                    │
│     #36 0x559925aba348 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10                                                                                                                 │
│     #37 0x559925ab3d01 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/a                                                                                                         │
│ pp/content_main.cc:356:36                                                                                                                                                                                                       │
│     #38 0x559925ab42fc in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:369:10                                                                                                                   │
│     #39 0x5599117272a9 in ChromeMain chrome/app/chrome_main.cc:194:12                                                                                                                                                           │
│     #40 0x7fc4cd829f74 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16                                                                                                                               │
│     #41 0x7ffc2d205df8  (<unknown module>)                                                                                                                                                                                      │
│                                                                                                                                                                                                                                 │
│ 0x7bf4cbe6fee8 is located 8 bytes before 32-byte region [0x7bf4cbe6fef0,0x7bf4cbe6ff10)                                                                                                                                         │
│ allocated by thread T0 (chrome) here:                                                                                                                                                                                           │
│     #0 0x5599116ec934 in malloc (/usr/local/google/btrfs_mount/asan/src/asan_chrome/chrome+0x1107f934) (BuildId: 250795                                                                                                         │
│ ae951b3a3b)                                                                                                                                                                                                                     │
│     #1 0x5599448414bd in <std::alloc::System as core::alloc::global::GlobalAlloc>::alloc third_party/rust-toolchain/lib                                                                                                         │
│ /rustlib/src/rust/library/std/src/sys/alloc/unix.rs:14:22                                                                                                                                                                       │
│     #2 0x5599448414bd in __rustc::__rust_alloc build/rust/allocator/lib.rs:67:20                                                                                                                                                │
│     #3 0x559944ae824f in alloc::alloc::alloc third_party/rust-toolchain/lib/rustlib/src/rust/library/alloc/src/alloc.rs                                                                                                         │
│ :101:9                                                                                                                                                                                                                          │
│     #4 0x559944ae824f in <alloc::alloc::Global>::alloc_impl_runtime third_party/rust-toolchain/lib/rustlib/src/rust/lib                                                                                                         │
│ rary/alloc/src/alloc.rs:210:73                                                                                                                                                                                                  │
│     #5 0x559944ae824f in <alloc::alloc::Global>::alloc_impl third_party/rust-toolchain/lib/rustlib/src/rust/library/all                                                                                                         │
│ oc/src/alloc.rs:332:9                                                                                                                                                                                                           │
│     #6 0x559944ae824f in <alloc::alloc::Global as core::alloc::Allocator>::allocate third_party/rust-toolchain/lib/rust                                                                                                         │
│ lib/src/rust/library/alloc/src/alloc.rs:449:14                                                                                                                                                                                  │
│     #7 0x559944ae824f in <alloc::raw_vec::RawVecInner>::try_allocate_in third_party/rust-toolchain/lib/rustlib/src/rust                                                                                                         │
│ /library/alloc/src/raw_vec/mod.rs:465:47                                                                                                                                                                                        │
│                                                                                                                                                                                                                                 │
│ SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/modules/skcms/src/Transform_inl.h:100:5 in skcms_priva                                                                                                         │
│ te::hsw::clut(unsigned int, unsigned int, unsigned char const*, unsigned char const*, unsigned char const*, float vecto                                                                                                         │
│ r[8]*, float vector[8]*, float vector[8]*, float vector[8]*)                                                                                                                                                                    │
│ Shadow bytes around the buggy address:                                                                                                                                                                                          │
│   0x7bf4cbe6fc00: 05 fa f7 fa fd fd fd fa f7 fa fd fd fd fd f7 fa                                                                                                                                                               │
│   0x7bf4cbe6fc80: fd fd fd fa f7 fa fd fd fd fd f7 fa fd fd fd fa                                                                                                                                                               │
│   0x7bf4cbe6fd00: f7 fa fd fd fd fa f7 fa fd fd fd fd f7 fa fd fd                                                                                                                                                               │
│   0x7bf4cbe6fd80: fd fd f7 fa 00 00 00 00 f7 fa 00 00 00 fa f7 fa                                                                                                                                                               │
│   0x7bf4cbe6fe00: fd fd fd fd f7 fa 00 00 00 fa f7 fa 00 00 05 fa                                                                                                                                                               │
│ =>0x7bf4cbe6fe80: f7 fa 00 00 00 00 f7 fa fd fd fd fd f7[fa]00 00                                                                                                                                                               │
│   0x7bf4cbe6ff00: 00 00 f7 fa 00 00 00 00 fa fa fa fa fa fa fa fa                                                                                                                                                               │
│   0x7bf4cbe6ff80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa                                                                                                                                                               │
│   0x7bf4cbe70000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa                                                                                                                                                               │
│   0x7bf4cbe70080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa                                                                                                                                                               │
│   0x7bf4cbe70100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa                                                                                                                                                               │
│ Shadow byte legend (one shadow byte represents 8 application bytes):                                                                                                                                                            │
│   Addressable:           00                                                                                                                                                                                                     │
│   Partially addressable: 01 02 03 04 05 06 07                                                                                                                                                                                   │
│   Heap left redzone:       fa                                                                                                                                                                                                   │
│   Freed heap region:       fd                                                                                                                                                                                                   │
│   Stack left redzone:      f1                                                                                                                                                                                                   │
│   Stack mid redzone:       f2                                                                                                                                                                                                   │
│   Stack right redzone:     f3                                                                                                                                                                                                   │
│   Stack after return:      f5                                                                                                                                                                                                   │
│   Stack use after scope:   f8                                                                                                                                                                                                   │
│   Global redzone:          f9                                                                                                                                                                                                   │
│   Global init order:       f6                                                                                                                                                                                                   │
│   Poisoned by user:        f7                                                                                                                                                                                                   │
│   Container overflow:      fc                                                                                                                                                                                                   │
│   Array cookie:            ac                                                                                                                                                                                                   │
│   Intra object redzone:    bb                                                                                                                                                                                                   │
│   ASan internal:           fe                                                                                                                                                                                                   │
│   Left alloca redzone:     ca                                                                                                                                                                                                   │
│   Right alloca redzone:    cb                                                                                                                                                                                                   │
│                                                                                                                                                                                                                                 │
│ ==3587647==ADDITIONAL INFO                                                                                                                                                                                                      │
│                                                                                                                                                                                                                                 │
│ ==3587647==Note: Please include this section with the ASan report.                                                                                                                                                              │
│ Task trace:                                                                                                                                                                                                                     │
│     #0 0x5599223cf0f8 in blink::BackgroundURLLoader::Context::PostTaskToMainThread(blink::CrossThreadOnceFunction<void                                                                                                          │
│ ()>) third_party/blink/renderer/platform/loader/fetch/url_loader/background_url_loader.cc:422:52                                                                                                                                │
│     #1 0x55992a7db1d3 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/                                                                                                         │
│ public/cpp/system/simple_watcher.cc:103:13                                                                                                                                                                                      │
│                                                                                                                                                                                                                                 │
│                                                                                                                                                                                                                                 │
│ Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=3587532 --enable-crash-reporter=, --noerrdialogs -                                                                                                         │
│ -user-data-dir=/tmp/icc-asan-test --change-stack-guard-on-fork=enable --no-sandbox --file-url-path-alias=/gen=/usr/loca                                                                                                         │
│ l/google/btrfs_mount/asan/src/asan_chrome/gen --ozone-platform=headless --disable-gpu-compositing --lang=en-US --num-ra                                                                                                         │
│ ster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-177531716193782                                                                                                         │
│ 4 --launch-time-ticks=1470095781912 --shared-files=v8_context_snapshot_data:100 --field-trial-handle=3,i,85339079835430                                                                                                         │
│ 10942,9154770658356434946,262144 --disable-features=PaintHolding --variations-seed-version --pseudonymization-salt-hand                                                                                                         │
│ le=7,i,13345646082069521405,5879668300211190914,4 --trace-process-track-uuid=3190708990997080739`                                                                                                                               │
│                                                                                                                                                                                                                                 │
│                                                                                                                                                                                                                                 │
│ ==3587647==END OF ADDITIONAL INFO                                                                                                                                                                                               │
│                                                                                                                                                                                                                                 │
│ ==3587647==ABORTING                                                                                                                

```

### ar...@google.com (2026-04-21)

I can't reproduce on stable. Tested: 147.0.7727.101

### ar...@google.com (2026-04-21)

I can't reproduce on beta. Tested: 148.0.7778.40

So, this is affecting M149

### oj...@gmail.com (2026-04-21)

Quick question [kj...@google.com](mailto:kj...@google.com) before this closes out, can you share the timeline on 504317459?

I filed 504103236 on Apr 19 at 02:16 UTC and 504160794 at 07:53 UTC. Both have working PoCs, symbolized stack traces, and root-cause breakdowns, and [ar...@google.com](mailto:ar...@google.com) #5 reproduced 504103236 earlier. If 504317459 was filed after those two, "earliest actionable report" should cover mine.

Also, the two reports target different moxcms validators. 504103236 is read\_lut\_a\_to\_b\_type (mft1/mft2 tags). 504160794 is read\_lut\_abm\_type (mAB/mBA tags). Each needs a separate patch, even with the shared downstream FFI issue.

Let me know what you need from me.

### kj...@google.com (2026-04-21)

I was a bit hasty on marking 504160794 as a duplicate. That appears to have a distinct problem than this (at least on second look).

This bug was filed first so I've swapped the order of duplicates.

### oj...@gmail.com (2026-04-21)

Appreciate the clarification and the swap. Standing by if the new owner needs anything...

### ch...@google.com (2026-04-22)

The Found In field may only contain numeric values.
Some values were corrected.
You can see the changes by toggling full history on the issue.

### ch...@google.com (2026-04-22)

Setting milestone because of s2 severity.

### ch...@google.com (2026-04-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2026-04-22)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

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

### pe...@google.com (2026-04-23)

@oj...@gmail.com is this now fixed?
(Once fixed rewards may be possible tbd)

### oj...@gmail.com (2026-04-23)

I rechecked current chromium main and the exact 504103236 state is no longer reachable.

The vulnerable sink in skcms still depends on active grid\_points[i] being >= 2, but the Rust ICC bridge now blocks the bad state in multiple places: FFI.rs rejects active CLUT dimensions < 2 and now populates all active legacy mft grid dimensions, FFI.cpp revalidates active grid\_points before exposing skcms structs, and SkCodecColorProfileRust.cpp now aborts if ToSkcmsIccProfile() fails. There is also a regression test that explicitly rejects the malformed A2B shape with input\_channels=2 and grid\_points={2,0,0,0}.

The fix is present in the current tree via Skia commit f4834c75d3, rolled into Chromium by e990e7d6c8c9.

Separately, current main now enables kForceSkcmsICCParsing by default, so decode-time ICC parsing is currently routed to skcms rather than the Rust ICC parser.

I have not rerun the original ASan PoC.

### oj...@gmail.com (2026-04-23)

Update: I reran the original PoC under ASan.

My local `src/out/asan-chrome` binary was stale and still reproduces the bug, so I retested on the nearest archived Linux ASan build for current main commit position `refs/heads/main@{#1619708}` (`#1619706`, `Chromium 149.0.7810.0`).

The PoC no longer reproduces there, either by default or with `--disable-features=ForceSkcmsICCParsing`, and I do not get the prior ASan heap-buffer-overflow in `third_party/skia/modules/skcms/src/Transform_inl.h`.

This appears fixed. :)

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/504103236)*
