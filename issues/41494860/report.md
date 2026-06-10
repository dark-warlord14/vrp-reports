# Security: heap-buffer-overflow in Blink

| Field | Value |
|-------|-------|
| **Issue ID** | [41494860](https://issues.chromium.org/issues/41494860) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Image, Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | jo...@ret2.one |
| **Assignee** | am...@chromium.org |
| **Created** | 2024-01-25 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

BMP image parsing crash with ASAN because of a wrong address calculation and crash inside a DCHECK because of this same wrong address:

Address calculate: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc;l=1113;drc=e6ee4500f7d6549a9ac1354f8d056da49ef406be>  

Debug check (inside skia): <https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/include/core/SkPixmap.h;l=436;drc=e6ee4500f7d6549a9ac1354f8d056da49ef406be>

The ASAN log says "heap-overflow read", but after this read, the code will do a write (overflow) (I need debug more to give more details).

I want to try to write the exploit to be rated as "High-quality report with functional exploit", Do I have some time or "deadline" to submit the functional exploit after this report?

CRASH LOG

gdb backtrace after crash:

```
#0  ReportGenericError() () at /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:477  
#1  0x000055556486b1d5 in __asan_report_load_n () at /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_rtl.cpp:147  
#2  0x000055556571fb8a in load<unsigned int __attribute__((ext_vector_type(8))), char> () at ../../third_party/skia/modules/skcms/src/Transform_inl.h:109  
#3  Exec_load_8888_k () at ../../third_party/skia/modules/skcms/src/Transform_inl.h:849  
#4  Exec_load_8888 () at ../../third_party/skia/modules/skcms/src/Transform_inl.h:848  
#5  exec_ops() () at ../../third_party/skia/modules/skcms/src/Transform_inl.h:1445  
#6  0x00005555656f6b4b in hsw::run_program(Op const\*, void const\*\*, char const\*, char\*, int, unsigned long, unsigned long) () at ../../third_party/skia/modules/skcms/src/Transform_inl.h:1461  
#7  0x00005555656ed207 in skcms_Transform() () at ../../third_party/skia/modules/skcms/skcms.cc:3009  
#8  0x000055558a3fa178 in ColorCorrectCurrentRow() () at ../../third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc:1120  
#9  0x000055558a3f99ed in ProcessRLEData() () at ../../third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc:888  
#10 0x000055558a3f2f9d in DecodePixelData() () at ../../third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc:818  
#11 0x000055558a3eed98 in DecodeBMP() () at ../../third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc:135  
#12 0x000055558a3fb657 in DecodeHelper() () at ../../third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder.cc:91  
#13 0x000055558a3fb146 in Decode() () at ../../third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder.cc:61  
#14 0x000055558a3d9021 in DecodeFrameBufferAtIndex() () at ../../third_party/blink/renderer/platform/image-decoders/image_decoder.cc:572  
#15 0x000055558dbb33c3 in Decode() () at ../../third_party/blink/renderer/modules/webcodecs/image_decoder_core.cc:187  
...  

```

ASAN log:

```
==101892==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x519000025280 at pc 0x55556571fb8a bp 0x7fffeeaf16b0 sp 0x7fffeeaf16a8  
READ of size 32 at 0x519000025280 thread T3 (ThreadPoolForeg)  
==101892==WARNING: invalid path to external symbolizer!  
==101892==WARNING: Failed to use and restart external symbolizer!  
...  
0x519000025280 is located 0 bytes after 1024-byte region [0x519000024e80,0x519000025280)  
allocated by thread T3 (ThreadPoolForeg) here:  
...  
SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/research/chrome+0x101cbb89) (BuildId: 53d30629de87fa40)   
Shadow bytes around the buggy address:  
  0x519000025000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x519000025080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x519000025100: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x519000025180: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x519000025200: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
=>0x519000025280:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x519000025300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa  
  0x519000025380: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x519000025400: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x519000025480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x519000025500: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
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
...  

```

Full crash logs in attachments

**VERSION**  

Chrome Version: 120.0.6099.0 (Developer Build) custom (64-bit) (commit: e6ee4500f7d6549a9ac1354f8d056da49ef406be)  

Operating System: Tested on: Linux 5.15.0-91-generic and Linux 6.5.0-14-generic

**REPRODUCTION CASE**

```
./chrome --no-sandbox --user-data-dir=/tmp/not-exist http://localhost:8000/  

```

**CREDIT INFORMATION**  

Reporter credit: [jorge.buzeti@ret2.one](mailto:jorge.buzeti@ret2.one) (@r3tr074)

## Attachments

- [index.html](attachments/index.html) (text/plain, 418 B)
- [asan.log](attachments/asan.log) (text/plain, 8.5 KB)
- [bad.bmp](attachments/bad.bmp) (application/octet-stream, 235 B)
- [xcalc-popped.png](attachments/xcalc-popped.png) (image/png, 2.4 MB)
- [deadbeef.png](attachments/deadbeef.png) (image/png, 2.6 MB)
- [cross-libc.html](attachments/cross-libc.html) (text/html, 12.3 KB)

## Timeline

### [Deleted User] (2024-01-25)

[Empty comment from Monorail migration]

### li...@chromium.org (2024-01-25)

Hello,

Similar to crbug.com/1521873 and crbug.com/1521878, this might not be a bug if it hinges on a badly formed image being decoded and hitting a CHECK or DCHECK. However, since you have an ASAN trace I'll leave this open for now, but the ASAN trace is unsymbolized so unfortunately it's not actionable at the moment.

Please update this bug once you have a working PoC we can reproduce, and a symbolized ASAN trace. 

### jo...@ret2.one (2024-01-25)

Sure, here a full symbolized ASAN trace:
```
==870742==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x519000021180 at pc 0x7faa1b3b27aa bp 0x7fa9f8567e70 sp 0x7fa9f8567e68
READ of size 32 at 0x519000021180 thread T2 (ThreadPoolForeg)
    #0 0x7faa1b3b27a9 in unsigned int vector[8] skcms_private::hsw::load<unsigned int vector[8], char>(char const*) third_party/skia/modules/skcms/src/Transform_inl.h:104:5
    #1 0x7faa1b3b27a9 in skcms_private::hsw::Exec_load_8888_k(skcms_private::hsw::NoCtx, char const*, char*, float vector[8]&, float vector[8]&, float vector[8]&, float vector[8]&, int) third_party/skia/modules/skcms/src/Transform_inl.h:902:16
    #2 0x7faa1b3b27a9 in skcms_private::hsw::Exec_load_8888(void const*, char const*, char*, float vector[8]&, float vector[8]&, float vector[8]&, float vector[8]&, int) third_party/skia/modules/skcms/src/Transform_inl.h:901:1
    #3 0x7faa1b3b27a9 in skcms_private::hsw::exec_stages(skcms_private::Op const*, void const**, char const*, char*, int) third_party/skia/modules/skcms/src/Transform_inl.h:1507:17
    #4 0x7faa1b39b615 in skcms_private::hsw::run_program(skcms_private::Op const*, void const**, long, char const*, char*, int, unsigned long, unsigned long) third_party/skia/modules/skcms/src/Transform_inl.h:1544:9
    #5 0x7faa1b395b3f in skcms_Transform third_party/skia/modules/skcms/skcms.cc:2801:5
    #6 0x7faa1b3001c3 in blink::BMPImageReader::ColorCorrectCurrentRow() third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc:1120:7
    #7 0x7faa1b2ffadc in blink::BMPImageReader::ProcessRLEData() third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc:888:11
    #8 0x7faa1b2f9614 in blink::BMPImageReader::DecodePixelData(bool) third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc:818:47
    #9 0x7faa1b2f5813 in blink::BMPImageReader::DecodeBMP(bool) third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc:135:8
    #10 0x7faa1b2f33f3 in blink::BMPImageDecoder::DecodeHelper(bool) third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder.cc:91:19
    #11 0x7faa1b2f2f49 in blink::BMPImageDecoder::Decode(bool) third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder.cc:61:8
    #12 0x7faa1b31db7e in blink::ImageDecoder::DecodeFrameBufferAtIndex(unsigned int) third_party/blink/renderer/platform/image-decoders/image_decoder.cc:572:5
    #13 0x7faa1818dd47 in blink::ImageDecoderCore::Decode(unsigned int, bool, base::AtomicFlag const*) third_party/blink/renderer/modules/webcodecs/image_decoder_core.cc:187:27
    #14 0x7faa181a5fd8 in std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> base::internal::FunctorTraits<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*)>::Invoke<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*), blink::ImageDecoderCore*, unsigned int, bool, base::AtomicFlag*>(std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*), blink::ImageDecoderCore*&&, unsigned int&&, bool&&, base::AtomicFlag*&&) base/functional/bind_internal.h:710:12
    #15 0x7faa181a5fd8 in std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> base::internal::InvokeHelper<false, std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, 0ul, 1ul, 2ul, 3ul>::MakeItSo<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*), std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::ImageDecoderCore>, unsigned int, bool, WTF::CrossThreadUnretainedWrapper<base::AtomicFlag>>>(std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*&&)(unsigned int, bool, base::AtomicFlag const*), std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::ImageDecoderCore>, unsigned int, bool, WTF::CrossThreadUnretainedWrapper<base::AtomicFlag>>&&) base/functional/bind_internal.h:860:12
    #16 0x7faa181a5fd8 in std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> base::internal::Invoker<base::internal::BindState<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*), WTF::CrossThreadUnretainedWrapper<blink::ImageDecoderCore>, unsigned int, bool, WTF::CrossThreadUnretainedWrapper<base::AtomicFlag>>, std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>::RunImpl<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*), std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::ImageDecoderCore>, unsigned int, bool, WTF::CrossThreadUnretainedWrapper<base::AtomicFlag>>, 0ul, 1ul, 2ul, 3ul>(std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*&&)(unsigned int, bool, base::AtomicFlag const*), std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::ImageDecoderCore>, unsigned int, bool, WTF::CrossThreadUnretainedWrapper<base::AtomicFlag>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/functional/bind_internal.h:991:14
    #17 0x7faa181a5fd8 in base::internal::Invoker<base::internal::BindState<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*), WTF::CrossThreadUnretainedWrapper<blink::ImageDecoderCore>, unsigned int, bool, WTF::CrossThreadUnretainedWrapper<base::AtomicFlag>>, std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:904:12
    #18 0x7faa181adaa5 in base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>::Run() && base/functional/callback.h:156:12
    #19 0x7faa181adaa5 in void base::internal::ReturnAsParamAdapter<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*) base/task/post_task_and_reply_with_result_internal.h:23:48
    #20 0x7faa181ae1b5 in void base::internal::FunctorTraits<void (*)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*)>::Invoke<void (*)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*>(void (*&&)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>&&, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*&&) base/functional/bind_internal.h:641:12
    #21 0x7faa181ae1b5 in void base::internal::InvokeHelper<false, void, 0ul, 1ul>::MakeItSo<void (*)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), std::__Cr::tuple<base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>>(void (*&&)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), std::__Cr::tuple<base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&) base/functional/bind_internal.h:860:12
    #22 0x7faa181ae1b5 in void base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (*)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), std::__Cr::tuple<base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul, 1ul>(void (*&&)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), std::__Cr::tuple<base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/functional/bind_internal.h:991:14
    #23 0x7faa181ae1b5 in base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:904:12
    #24 0x7faa6c185a7c in base::OnceCallback<void ()>::Run() && base/functional/callback.h:156:12
    #25 0x7faa6c185a7c in base::internal::PostTaskAndReplyRelay::RunTaskAndPostReply(base::internal::PostTaskAndReplyRelay) base/threading/post_task_and_reply_impl.h:45:28
    #26 0x7faa6c185ed4 in void base::internal::FunctorTraits<void (*)(base::internal::PostTaskAndReplyRelay)>::Invoke<void (*)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay>(void (*&&)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay&&) base/functional/bind_internal.h:641:12
    #27 0x7faa6c185ed4 in void base::internal::InvokeHelper<false, void, 0ul>::MakeItSo<void (*)(base::internal::PostTaskAndReplyRelay), std::__Cr::tuple<base::internal::PostTaskAndReplyRelay>>(void (*&&)(base::internal::PostTaskAndReplyRelay), std::__Cr::tuple<base::internal::PostTaskAndReplyRelay>&&) base/functional/bind_internal.h:860:12
    #28 0x7faa6c185ed4 in void base::internal::Invoker<base::internal::BindState<void (*)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay>, void ()>::RunImpl<void (*)(base::internal::PostTaskAndReplyRelay), std::__Cr::tuple<base::internal::PostTaskAndReplyRelay>, 0ul>(void (*&&)(base::internal::PostTaskAndReplyRelay), std::__Cr::tuple<base::internal::PostTaskAndReplyRelay>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:991:14
    #29 0x7faa6c185ed4 in base::internal::Invoker<base::internal::BindState<void (*)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:904:12
    #30 0x7faa6c0f5193 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:156:12
    #31 0x7faa6c0f5193 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:201:34
    #32 0x7faa6c1b6480 in void base::TaskAnnotator::RunTask<base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)::$_0>(perfetto::StaticString, base::PendingTask&, base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)::$_0&&) base/task/common/task_annotator.h:89:5
    #33 0x7faa6c1b6480 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:679:19
    #34 0x7faa6c1b6748 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:664:3
    #35 0x7faa6c1b5580 in base::internal::TaskTracker::RunTaskWithShutdownBehavior(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:694:7
    #36 0x7faa6c1b5580 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:521:5
    #37 0x7faa6c1b4432 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:416:5
    #38 0x7faa6c1d5470 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:430:36
    #39 0x7faa6c1d4491 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:315:3
    #40 0x7faa6c1d3e85 in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:295:7
    #41 0x7faa6c25bf43 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:103:13
    #42 0x55f59e4f7448 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28

0x519000021180 is located 0 bytes after 1024-byte region [0x519000020d80,0x519000021180)
allocated by thread T2 (ThreadPoolForeg) here:
    #0 0x55f59e4f98bf in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:68:3
    #1 0x7faa6bb0919a in void* partition_alloc::PartitionRoot::AllocInternal<(partition_alloc::internal::AllocFlags)0>(unsigned long, unsigned long, char const*) base/allocator/partition_allocator/src/partition_alloc/partition_root.h:2077:51
    #2 0x7faa6bb0919a in void* partition_alloc::PartitionRoot::AllocInline<(partition_alloc::internal::AllocFlags)0>(unsigned long, char const*) base/allocator/partition_allocator/src/partition_alloc/partition_root.h:514:12
    #3 0x7faa6bb0919a in void* partition_alloc::PartitionRoot::Alloc<(partition_alloc::internal::AllocFlags)0>(unsigned long, char const*) base/allocator/partition_allocator/src/partition_alloc/partition_root.h:508:12
    #4 0x7faa1b321286 in blink::ColorProfileTransform::operator new(unsigned long) third_party/blink/renderer/platform/image-decoders/image_decoder.h:124:3
    #5 0x7faa1b321286 in std::__Cr::__unique_if<blink::ColorProfileTransform>::__unique_single std::__Cr::make_unique<blink::ColorProfileTransform, skcms_ICCProfile const*&, skcms_ICCProfile*>(skcms_ICCProfile const*&, skcms_ICCProfile*&&) third_party/libc++/src/include/__memory/unique_ptr.h:597:26
    #6 0x7faa1b321286 in blink::ImageDecoder::UpdateSkImageColorSpaceAndTransform() third_party/blink/renderer/platform/image-decoders/image_decoder.cc:1136:7
    #7 0x7faa1b31f74d in blink::ImageDecoder::ColorSpaceForSkImages() third_party/blink/renderer/platform/image-decoders/image_decoder.cc:1051:3
    #8 0x7faa1b2f903d in blink::BMPImageReader::InitFrame() third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc:795:44
    #9 0x7faa1b2f57a3 in blink::BMPImageReader::DecodeBMP(bool) third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc:129:61
    #10 0x7faa1b2f33f3 in blink::BMPImageDecoder::DecodeHelper(bool) third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder.cc:91:19
    #11 0x7faa1b2f2f49 in blink::BMPImageDecoder::Decode(bool) third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder.cc:61:8
    #12 0x7faa1b31db7e in blink::ImageDecoder::DecodeFrameBufferAtIndex(unsigned int) third_party/blink/renderer/platform/image-decoders/image_decoder.cc:572:5
    #13 0x7faa1818dd47 in blink::ImageDecoderCore::Decode(unsigned int, bool, base::AtomicFlag const*) third_party/blink/renderer/modules/webcodecs/image_decoder_core.cc:187:27
    #14 0x7faa181a5fd8 in std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> base::internal::FunctorTraits<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*)>::Invoke<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*), blink::ImageDecoderCore*, unsigned int, bool, base::AtomicFlag*>(std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*), blink::ImageDecoderCore*&&, unsigned int&&, bool&&, base::AtomicFlag*&&) base/functional/bind_internal.h:710:12
    #15 0x7faa181a5fd8 in std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> base::internal::InvokeHelper<false, std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, 0ul, 1ul, 2ul, 3ul>::MakeItSo<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*), std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::ImageDecoderCore>, unsigned int, bool, WTF::CrossThreadUnretainedWrapper<base::AtomicFlag>>>(std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*&&)(unsigned int, bool, base::AtomicFlag const*), std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::ImageDecoderCore>, unsigned int, bool, WTF::CrossThreadUnretainedWrapper<base::AtomicFlag>>&&) base/functional/bind_internal.h:860:12
    #16 0x7faa181a5fd8 in std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> base::internal::Invoker<base::internal::BindState<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*), WTF::CrossThreadUnretainedWrapper<blink::ImageDecoderCore>, unsigned int, bool, WTF::CrossThreadUnretainedWrapper<base::AtomicFlag>>, std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>::RunImpl<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*), std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::ImageDecoderCore>, unsigned int, bool, WTF::CrossThreadUnretainedWrapper<base::AtomicFlag>>, 0ul, 1ul, 2ul, 3ul>(std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*&&)(unsigned int, bool, base::AtomicFlag const*), std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::ImageDecoderCore>, unsigned int, bool, WTF::CrossThreadUnretainedWrapper<base::AtomicFlag>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/functional/bind_internal.h:991:14
    #17 0x7faa181a5fd8 in base::internal::Invoker<base::internal::BindState<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> (blink::ImageDecoderCore::*)(unsigned int, bool, base::AtomicFlag const*), WTF::CrossThreadUnretainedWrapper<blink::ImageDecoderCore>, unsigned int, bool, WTF::CrossThreadUnretainedWrapper<base::AtomicFlag>>, std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:904:12
    #18 0x7faa181adaa5 in base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>::Run() && base/functional/callback.h:156:12
    #19 0x7faa181adaa5 in void base::internal::ReturnAsParamAdapter<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*) base/task/post_task_and_reply_with_result_internal.h:23:48
    #20 0x7faa181ae1b5 in void base::internal::FunctorTraits<void (*)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*)>::Invoke<void (*)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*>(void (*&&)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>&&, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*&&) base/functional/bind_internal.h:641:12
    #21 0x7faa181ae1b5 in void base::internal::InvokeHelper<false, void, 0ul, 1ul>::MakeItSo<void (*)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), std::__Cr::tuple<base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>>(void (*&&)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), std::__Cr::tuple<base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&) base/functional/bind_internal.h:860:12
    #22 0x7faa181ae1b5 in void base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (*)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), std::__Cr::tuple<base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul, 1ul>(void (*&&)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), std::__Cr::tuple<base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/functional/bind_internal.h:991:14
    #23 0x7faa181ae1b5 in base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>*), base::OnceCallback<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>, std::__Cr::default_delete<std::__Cr::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult, std::__Cr::default_delete<blink::ImageDecoderCore::ImageDecodeResult>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:904:12
    #24 0x7faa6c185a7c in base::OnceCallback<void ()>::Run() && base/functional/callback.h:156:12
    #25 0x7faa6c185a7c in base::internal::PostTaskAndReplyRelay::RunTaskAndPostReply(base::internal::PostTaskAndReplyRelay) base/threading/post_task_and_reply_impl.h:45:28
    #26 0x7faa6c185ed4 in void base::internal::FunctorTraits<void (*)(base::internal::PostTaskAndReplyRelay)>::Invoke<void (*)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay>(void (*&&)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay&&) base/functional/bind_internal.h:641:12
    #27 0x7faa6c185ed4 in void base::internal::InvokeHelper<false, void, 0ul>::MakeItSo<void (*)(base::internal::PostTaskAndReplyRelay), std::__Cr::tuple<base::internal::PostTaskAndReplyRelay>>(void (*&&)(base::internal::PostTaskAndReplyRelay), std::__Cr::tuple<base::internal::PostTaskAndReplyRelay>&&) base/functional/bind_internal.h:860:12
    #28 0x7faa6c185ed4 in void base::internal::Invoker<base::internal::BindState<void (*)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay>, void ()>::RunImpl<void (*)(base::internal::PostTaskAndReplyRelay), std::__Cr::tuple<base::internal::PostTaskAndReplyRelay>, 0ul>(void (*&&)(base::internal::PostTaskAndReplyRelay), std::__Cr::tuple<base::internal::PostTaskAndReplyRelay>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:991:14
    #29 0x7faa6c185ed4 in base::internal::Invoker<base::internal::BindState<void (*)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:904:12
    #30 0x7faa6c0f5193 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:156:12
    #31 0x7faa6c0f5193 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:201:34
    #32 0x7faa6c1b6480 in void base::TaskAnnotator::RunTask<base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)::$_0>(perfetto::StaticString, base::PendingTask&, base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)::$_0&&) base/task/common/task_annotator.h:89:5
    #33 0x7faa6c1b6480 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:679:19
    #34 0x7faa6c1b6748 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:664:3
    #35 0x7faa6c1b5580 in base::internal::TaskTracker::RunTaskWithShutdownBehavior(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:694:7
    #36 0x7faa6c1b5580 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:521:5
    #37 0x7faa6c1b4432 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:416:5
    #38 0x7faa6c1d5470 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:430:36
    #39 0x7faa6c1d4491 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:315:3
    #40 0x7faa6c1d3e85 in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:295:7
    #41 0x7faa6c25bf43 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:103:13
    #42 0x55f59e4f7448 in asan_thread_start(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:239:28

Thread T2 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x55f59e4df521 in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:250:3
    #1 0x7faa6c25b30f in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:148:13
    #2 0x7faa6c1d32a5 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:191:3
    #3 0x7faa6c1b9594 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() base/task/thread_pool/thread_group.cc:108:13
    #4 0x7faa6c1b8d4d in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() base/task/thread_pool/thread_group.cc:83:3
    #5 0x7faa6c1c0496 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() base/task/thread_pool/thread_group_impl.cc:48:3
    #6 0x7faa6c1c0142 in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>) base/task/thread_pool/thread_group_impl.cc:163:1
    #7 0x7faa6c1cc738 in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*) base/task/thread_pool/thread_pool_impl.cc:189:9
    #8 0x7faa644ee97c in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) content/child/child_process.cc:118:20
    #9 0x7faa682dd755 in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) content/renderer/render_process.cc:18:7
    #10 0x7faa682dd8ab in content::RenderProcessImpl::RenderProcessImpl() content/renderer/render_process_impl.cc:120:7
    #11 0x7faa682ddeea in content::RenderProcessImpl::Create() content/renderer/render_process_impl.cc:289:31
    #12 0x7faa6830aa5d in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:295:53
    #13 0x7faa68d964e6 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:676:14
    #14 0x7faa68d979df in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:780:12
    #15 0x7faa68d9a57a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1146:10
    #16 0x7faa68d9418c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:335:36
    #17 0x7faa68d949ba in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:348:10
    #18 0x55f5a283028e in headless::(anonymous namespace)::HeadlessChildMain(content::ContentMainParams) headless/app/headless_shell.cc:195:12
    #19 0x55f5a283028e in headless::HeadlessShellMain(content::ContentMainParams) headless/app/headless_shell.cc:256:5
    #20 0x55f59e52f954 in ChromeMain chrome/app/chrome_main.cc:179:14
    #21 0x7faa0b064d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f) (BuildId: c289da5071a3399de893d2af81d6a30c62646e1e)

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/modules/skcms/src/Transform_inl.h:104:5 in unsigned int vector[8] skcms_private::hsw::load<unsigned int vector[8], char>(char const*)
Shadow bytes around the buggy address:
  0x519000020f00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x519000020f80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x519000021000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x519000021080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x519000021100: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x519000021180:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x519000021200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x519000021280: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x519000021300: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x519000021380: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x519000021400: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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

==870742==ADDITIONAL INFO

==870742==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7faa1819aab8 in blink::ImageDecoderExternal::MaybeSatisfyPendingDecodes() third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc:520:15
    #1 0x7faa1819aab8 in blink::ImageDecoderExternal::MaybeSatisfyPendingDecodes() third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc:520:15
    #2 0x7faa1819aab8 in blink::ImageDecoderExternal::MaybeSatisfyPendingDecodes() third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc:520:15


==870742==END OF ADDITIONAL INFO
==870742==ABORTING
```
I use the exact same PoC provided in this issue attachment

### [Deleted User] (2024-01-25)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2024-01-26)

Adding some graphics folks to help find an owner, please assign whoever makes the most sense to own this since I"m not sure if it should be routed to Skia folks or Chrome graphics folks!

It looks like the overflow happens when Skia tries to transform a row to be decoded, and a memcpy in load() tries to read invalid data. 
I see that when the load is called it takes the src address and adds 4*i to it (https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/modules/skcms/src/Transform_inl.h;l=902;drc=adb3b9bc3ff928029b19d5ac5379841dae0ad6ed;bpv=1;bpt=1) and i is incremented here (https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/modules/skcms/src/Transform_inl.h;l=1545;drc=adb3b9bc3ff928029b19d5ac5379841dae0ad6ed;bpv=1;bpt=1) by N, which I think the BMPImageReader passes in as the width given by the decoder (https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc;l=1121). 

 I don't see any checks in BMPImageReader or in Skia's transformer to confirm that the coordinates that get passed in are within the bounds of the decoder's width, so either Chrome or Skia should add checks to make sure that those values are within bounds, assuming my analysis is correct. Since I'm not super familiar with this part of the codebase I can't say for sure where this check should happen, my guess would be within Skia's skcms_Transform since it looks like there's some bounds checking there already, and it'll ensure other callers of this API don't have similar overflows.

[Monorail components: Blink>Image Internals>Skia]

### [Deleted User] (2024-01-26)

[Empty comment from Monorail migration]

### jo...@google.com (2024-01-26)

`skcms_Transform` functions as basically a memcpy from one place to another, so I would focus on the call site rather than on skcms itself. The call stack appears to just be skcms loading pixel data from a wild address. Did the BMP decoder get tricked by some out-of-bounds image size or something?

### jo...@google.com (2024-01-26)

FYI: the BMP image reader is not Skia's. It is from Blink:
`blink::BMPImageReader::ColorCorrectCurrentRow() third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc:1120:7`


### jo...@google.com (2024-01-26)

Looks like pkasting@ added ICC support to BMPImageReader?

### jo...@google.com (2024-01-26)

As long as I'm in the neighborhood I will take a look at this and see if I can repro it with the reporter's BMP.

### jo...@google.com (2024-01-26)

When I try it in a debug Content Shell, I hit an SkASSERT inside SkPixmap:

[84911:14083:0126/153010.691512:FATAL:SkPixmap.h(436)] check((unsigned)y < (unsigned)fInfo.height())
0   libbase.dylib                       0x000000010742dab0 base::debug::CollectStackTrace(void const**, unsigned long) + 48
1   libbase.dylib                       0x00000001073d766c base::debug::StackTrace::StackTrace(unsigned long) + 92
2   libbase.dylib                       0x00000001073d7700 base::debug::StackTrace::StackTrace(unsigned long) + 36
3   libbase.dylib                       0x00000001073d76cc base::debug::StackTrace::StackTrace() + 40
4   libbase.dylib                       0x000000010708fe5c logging::LogMessage::Flush() + 192
5   libbase.dylib                       0x000000010708fd74 logging::LogMessage::~LogMessage() + 44
6   libbase.dylib                       0x0000000107090420 logging::LogMessage::~LogMessage() + 28
7   libskia.dylib                       0x0000000110d48650 SkAbort_FileLine(char const*, int, char const*, ...) + 180
8   libimage_decoders.dylib             0x00000002a10e8608 SkPixmap::addr32() const + 0
9   libimage_decoders.dylib             0x00000002a10e84e8 SkPixmap::addr32(int, int) const + 144
10  libimage_decoders.dylib             0x00000002a10e844c SkPixmap::writable_addr32(int, int) const + 40
11  libimage_decoders.dylib             0x00000002a10e83a0 SkBitmap::getAddr32(int, int) const + 100
12  libimage_decoders.dylib             0x00000002a10e72b8 blink::ImageFrame::GetAddr(int, int) + 172


Does SkASSERT count as "hitting a CHECK or DCHECK"?

### li...@chromium.org (2024-01-26)

Hm, normally I would say yes since this assert looks like it's checking if SkColorType is the right color type.  I'm just hesitant because there does seem to be an overflow without the asserts, whereas in the two bugs referenced in https://crbug.com/chromium/1521893#c2 the reporter showed crashes that hit when you cause hit a CHECK or DCHECK. 

I also can't tell if this means that the SkASSERT is preventing the overflow or not, my guess is that it would be? Out of curiosity, why doesn't the addr32 method validate input outside of these asserts in debug builds? 
If the assert is preventing the overflow we should treat this as a valid bug imo. 
danakj@, wdyt?

Reporter: did your poc BMP only crash on debug builds when it hit this assert?


### jo...@ret2.one (2024-01-26)

Yes, I linked this "debug check" in my issue description (inside skia lib: https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/include/core/SkPixmap.h;l=436;drc=e6ee4500f7d6549a9ac1354f8d056da49ef406be), because in blink exist a wrong address calc (https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc;l=1113;drc=e6ee4500f7d6549a9ac1354f8d056da49ef406be)

So, assembling this, exist a memory corruption (heap-overflow read/write) in release builds

### jo...@google.com (2024-01-26)

I'm working on a tentative fix which would allow the BMPImageReader to properly detect this issue.

The problem is that the image header says it is 24-bit true color, but also says that it has a very large palette (holding 185273099 colors). This is not a valid BMP configuration. I am working on a tentative patch which would reject such a malformed BMP.

What is the best way to add a test case for this? I haven't worked on BMPImageReader before so I don't know the protocol for tests/fuzzing.

### jo...@ret2.one (2024-01-26)

The poc crash in release builds too, you can try open in normal Chrome release, after reload sometimes you will see a SIGSEGV (I tested right now in `121.0.6167.85 (Official Build) (64-bit)`)


### jo...@google.com (2024-01-26)

Here's a CL which properly detects the image as malformed: https://crrev.com/c/5241305

There's no tests added yet, though.

### da...@chromium.org (2024-01-26)

> What is the best way to add a test case for this?

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder_test.cc for a test with (fixed) bad values

Fuzzing is something else, not sure if there's libfuzzer tests already, but libfuzzer tests are easy to write: https://source.chromium.org/chromium/chromium/src/+/main:testing/libfuzzer/getting_started.md?ss=chromium%2Fchromium%2Fsrc&q=libfuzzer%20f:md

### da...@chromium.org (2024-01-26)

SkASSERT is not enabled in release builds, it's a dcheck.

https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/include/private/base/SkAssert.h;l=109-119?ss=chromium%2Fchromium%2Fsrc&q=SkASSERT

### jo...@google.com (2024-01-26)

I strongly suspect that the fuzzer is not hooked up to BMPImageReader, as this seems exactly like the kind of case that a fuzzer would discover almost immediately. (Jorge, did you find this via fuzzing or manual inspection?) We should prioritize setting one up. I have set up oss-fuzz on various Skia modules, but haven't done so with Blink yet.

### jo...@google.com (2024-01-26)

Since I've got a CL on deck I'll assign myself to the bug

### li...@chromium.org (2024-01-26)

Blink has a PNG decoder fuzzer set up already (https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/png_fuzzer.cc), could it be possible to reuse this for a BMP decoder fuzzer? They both inherit from ImageDecoder so it looks like it should be straightforward to add a BMP decoder fuzzer.

### jo...@google.com (2024-01-26)

I'll take a look; thanks for the pointer.

### jo...@ret2.one (2024-01-26)

I found this with my custom fuzzer

### jo...@google.com (2024-01-26)

https://crrev.com/c/5241305

### am...@chromium.org (2024-01-27)

Hello! Thanks for your report and your desire to submit an exploit for this bug. 

>>>I want to try to write the exploit to be rated as "High-quality report with functional exploit", Do I have some time or "deadline" to submit the functional exploit after this report?

As long as you can submit the exploit in a reasonable time frame (within 60 days or so) after the bug is reported, we can easily accept it. If you need an extension, please reach out to security-vrp@chromium.org to let us know.
The VRP Panel will likely assess and issue a reward, based on the report state at that time, no long after the bug is closed as fixed. However, you can still submit the exploit after that and we can reassess it for a higher reward amount (based on the high-quality + functional exploit criteria) at that time. 

If you want to provide an exploit after the bug has already gone through VRP Panel review and reward decision, please upload the exploit to this report then email us at security-vrp@chromium.org to let us know and we can put this issue back in our queue for reassessment. 



### [Deleted User] (2024-01-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-28)

[Empty comment from Monorail migration]

### jo...@google.com (2024-01-29)

Re https://crbug.com/chromium/1521893#c14: the large palette was a red herring; I've amended my CL. The root cause was a BMP that had (1) color correction and (2) RLE encoding with an extraneous EOF marker at the very end of the image. Neither of these things are illegal, but it's not a combination that would come up naturally.

(However, the palette handling code looks like it could use some additional tests and/or hardening, separate from this issue.)

### jo...@google.com (2024-01-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4bdd8d61bebbba9fab77fa86a8f66b305995199b

commit 4bdd8d61bebbba9fab77fa86a8f66b305995199b
Author: John Stiles <johnstiles@google.com>
Date: Mon Jan 29 23:50:14 2024

Fix a crash when a BMP image contains an unnecessary EOF code.

Previously, this would try to perform color correction on a row
one past the end of the image data.

Bug: 1521893
Change-Id: I425437005b9ef400138556705616095857d2cf0d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5241305
Auto-Submit: John Stiles <johnstiles@google.com>
Commit-Queue: John Stiles <johnstiles@google.com>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1253633}

[modify] https://crrev.com/4bdd8d61bebbba9fab77fa86a8f66b305995199b/third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder_test.cc
[modify] https://crrev.com/4bdd8d61bebbba9fab77fa86a8f66b305995199b/third_party/blink/renderer/platform/blink_platform_unittests_bundle_data.filelist
[add] https://crrev.com/4bdd8d61bebbba9fab77fa86a8f66b305995199b/third_party/blink/web_tests/images/resources/unnecessary-eof.bmp
[modify] https://crrev.com/4bdd8d61bebbba9fab77fa86a8f66b305995199b/third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc


### gi...@appspot.gserviceaccount.com (2024-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/99e1c863159244eabfc5d0e6aa9407ddeeab49e6

commit 99e1c863159244eabfc5d0e6aa9407ddeeab49e6
Author: John Stiles <johnstiles@google.com>
Date: Tue Jan 30 00:04:36 2024

Add BMPImageDecoder fuzz test.

Change-Id: Idf292ea41a61d794962f020e330699d9fa615e93
Bug: 1521893
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5239056
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Auto-Submit: John Stiles <johnstiles@google.com>
Commit-Queue: John Stiles <johnstiles@google.com>
Cr-Commit-Position: refs/heads/main@{#1253635}

[modify] https://crrev.com/99e1c863159244eabfc5d0e6aa9407ddeeab49e6/third_party/blink/renderer/platform/image-decoders/BUILD.gn
[modify] https://crrev.com/99e1c863159244eabfc5d0e6aa9407ddeeab49e6/third_party/blink/renderer/platform/image-decoders/DEPS
[add] https://crrev.com/99e1c863159244eabfc5d0e6aa9407ddeeab49e6/third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder_fuzzer.cc


### gi...@appspot.gserviceaccount.com (2024-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3f8586dc78bc65b8516df62b0ebac064afd388fe

commit 3f8586dc78bc65b8516df62b0ebac064afd388fe
Author: Adrian Taylor <adetaylor@chromium.org>
Date: Tue Jan 30 00:15:04 2024

Revert "Add BMPImageDecoder fuzz test."

This reverts commit 99e1c863159244eabfc5d0e6aa9407ddeeab49e6.

Reason for revert: This is going to make lots of bots go red, because unfortunately the syntax for declaring fuzz tests changed about 20 commits earlier.

Original change's description:
> Add BMPImageDecoder fuzz test.
>
> Change-Id: Idf292ea41a61d794962f020e330699d9fa615e93
> Bug: 1521893
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5239056
> Reviewed-by: Peter Kasting <pkasting@chromium.org>
> Auto-Submit: John Stiles <johnstiles@google.com>
> Commit-Queue: John Stiles <johnstiles@google.com>
> Cr-Commit-Position: refs/heads/main@{#1253635}

Bug: 1521893
Change-Id: I7844825fb95ad7bf6641a0bb902876e908c5ebf9
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5247344
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Owners-Override: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1253640}

[modify] https://crrev.com/3f8586dc78bc65b8516df62b0ebac064afd388fe/third_party/blink/renderer/platform/image-decoders/BUILD.gn
[modify] https://crrev.com/3f8586dc78bc65b8516df62b0ebac064afd388fe/third_party/blink/renderer/platform/image-decoders/DEPS
[delete] https://crrev.com/9f35de2abccccf3d4f085122ca1f69d728fbad2a/third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder_fuzzer.cc


### [Deleted User] (2024-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-30)

Requesting merge to extended stable M120 because latest trunk commit (1253635) appears to be after extended stable branch point (1217362).

Requesting merge to stable M121 because latest trunk commit (1253635) appears to be after stable branch point (1233107).

Requesting merge to beta M122 because latest trunk commit (1253635) appears to be after beta branch point (1250580).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121, 122].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2024-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4f957bb9874c0cff439ba1a3f525a3d609c8803c

commit 4f957bb9874c0cff439ba1a3f525a3d609c8803c
Author: John Stiles <johnstiles@google.com>
Date: Tue Jan 30 20:29:36 2024

Reland "Add BMPImageDecoder fuzz test."

This is a reland of commit 99e1c863159244eabfc5d0e6aa9407ddeeab49e6

Original change's description:
> Add BMPImageDecoder fuzz test.
>
> Change-Id: Idf292ea41a61d794962f020e330699d9fa615e93
> Bug: 1521893
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5239056
> Reviewed-by: Peter Kasting <pkasting@chromium.org>
> Auto-Submit: John Stiles <johnstiles@google.com>
> Commit-Queue: John Stiles <johnstiles@google.com>
> Cr-Commit-Position: refs/heads/main@{#1253635}

Bug: 1521893
Change-Id: I5ace381c25683aec15326c3aace5e1662b268181
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5249868
Reviewed-by: Adrian Taylor <adetaylor@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: John Stiles <johnstiles@google.com>
Cr-Commit-Position: refs/heads/main@{#1254137}

[modify] https://crrev.com/4f957bb9874c0cff439ba1a3f525a3d609c8803c/third_party/blink/renderer/platform/image-decoders/BUILD.gn
[modify] https://crrev.com/4f957bb9874c0cff439ba1a3f525a3d609c8803c/third_party/blink/renderer/platform/image-decoders/DEPS
[add] https://crrev.com/4f957bb9874c0cff439ba1a3f525a3d609c8803c/third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder_fuzzer.cc


### [Deleted User] (2024-01-31)

Requesting merge to extended stable M120 because latest trunk commit (1253635) appears to be after extended stable branch point (1217362).

Requesting merge to stable M121 because latest trunk commit (1253635) appears to be after stable branch point (1233107).

Requesting merge to beta M122 because latest trunk commit (1253635) appears to be after beta branch point (1250580).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121, 122].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@google.com (2024-01-31)

1. https://crrev.com/c/5241305
2. Not to my knowledge
3. New CHECKs have been added to guard against further security issues. There is a chance that a maliciously-crafted BMP could trigger them.
4. It could affect rendering of maliciously-crafted BMP images. I have verified that the test suite at https://entropymine.com/jason/bmpsuite/bmpsuite/html/bmpsuite.html is unaffected.
5. Please verify that the BMP attached to this bug does not trigger ASAN when Chrome renders it.

### am...@chromium.org (2024-02-01)

merges for https://crrev.com/c/5241305 approved
if possible, please merge this fix to M121 Stable / branch 6167 and M120 Extended Stable by EOD today (1 February) so this fix can be included in next week's Stable and Extended security updates 

please also merge this fix to M122 Beta, branch 6261 at your earliest convenience -- thank you

### jo...@google.com (2024-02-01)

Cherrypick CLs created in 6099, 6167 and 6261.

### jo...@google.com (2024-02-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d6f1887d2df88cdb46392e204b72377301288514

commit d6f1887d2df88cdb46392e204b72377301288514
Author: John Stiles <johnstiles@google.com>
Date: Thu Feb 01 20:01:52 2024

Fix a crash when a BMP image contains an unnecessary EOF code.

Previously, this would try to perform color correction on a row
one past the end of the image data.

(cherry picked from commit 4bdd8d61bebbba9fab77fa86a8f66b305995199b)

Bug: 1521893
Change-Id: I425437005b9ef400138556705616095857d2cf0d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5241305
Auto-Submit: John Stiles <johnstiles@google.com>
Commit-Queue: John Stiles <johnstiles@google.com>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1253633}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5258700
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/branch-heads/6167@{#1734}
Cr-Branched-From: 222e786949e76e342d325ea0d008b4b6273f3a89-refs/heads/main@{#1233107}

[modify] https://crrev.com/d6f1887d2df88cdb46392e204b72377301288514/third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder_test.cc
[modify] https://crrev.com/d6f1887d2df88cdb46392e204b72377301288514/third_party/blink/renderer/platform/blink_platform_unittests_bundle_data.filelist
[add] https://crrev.com/d6f1887d2df88cdb46392e204b72377301288514/third_party/blink/web_tests/images/resources/unnecessary-eof.bmp
[modify] https://crrev.com/d6f1887d2df88cdb46392e204b72377301288514/third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc


### gi...@appspot.gserviceaccount.com (2024-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/260481b16f4ef027342981cc304caf1027eae099

commit 260481b16f4ef027342981cc304caf1027eae099
Author: John Stiles <johnstiles@google.com>
Date: Thu Feb 01 20:40:55 2024

Fix a crash when a BMP image contains an unnecessary EOF code.

Previously, this would try to perform color correction on a row
one past the end of the image data.

(cherry picked from commit 4bdd8d61bebbba9fab77fa86a8f66b305995199b)

Bug: 1521893
Change-Id: I425437005b9ef400138556705616095857d2cf0d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5241305
Auto-Submit: John Stiles <johnstiles@google.com>
Commit-Queue: John Stiles <johnstiles@google.com>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1253633}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5259699
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/branch-heads/6099@{#1915}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/260481b16f4ef027342981cc304caf1027eae099/third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder_test.cc
[modify] https://crrev.com/260481b16f4ef027342981cc304caf1027eae099/third_party/blink/renderer/platform/blink_platform_unittests_bundle_data.filelist
[add] https://crrev.com/260481b16f4ef027342981cc304caf1027eae099/third_party/blink/web_tests/images/resources/unnecessary-eof.bmp
[modify] https://crrev.com/260481b16f4ef027342981cc304caf1027eae099/third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc


### gi...@appspot.gserviceaccount.com (2024-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b9f58ca9ae3bc72a82382e44ff06f19b6a257c1a

commit b9f58ca9ae3bc72a82382e44ff06f19b6a257c1a
Author: John Stiles <johnstiles@google.com>
Date: Thu Feb 01 23:14:28 2024

Fix a crash when a BMP image contains an unnecessary EOF code.

Previously, this would try to perform color correction on a row
one past the end of the image data.

(cherry picked from commit 4bdd8d61bebbba9fab77fa86a8f66b305995199b)

Bug: 1521893
Change-Id: I425437005b9ef400138556705616095857d2cf0d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5241305
Auto-Submit: John Stiles <johnstiles@google.com>
Commit-Queue: John Stiles <johnstiles@google.com>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1253633}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5258886
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/branch-heads/6261@{#392}
Cr-Branched-From: 9755d9d81e4a8cb5b4f76b23b761457479dbb06b-refs/heads/main@{#1250580}

[modify] https://crrev.com/b9f58ca9ae3bc72a82382e44ff06f19b6a257c1a/third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder_test.cc
[modify] https://crrev.com/b9f58ca9ae3bc72a82382e44ff06f19b6a257c1a/third_party/blink/renderer/platform/blink_platform_unittests_bundle_data.filelist
[add] https://crrev.com/b9f58ca9ae3bc72a82382e44ff06f19b6a257c1a/third_party/blink/web_tests/images/resources/unnecessary-eof.bmp
[modify] https://crrev.com/b9f58ca9ae3bc72a82382e44ff06f19b6a257c1a/third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc


### is...@google.com (2024-02-01)

This issue was migrated from crbug.com/chromium/1521893?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Image, Internals>Skia]
[Monorail components added to Component Tags custom field.]

### am...@google.com (2024-02-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-14)

Congratulations Jorge! The Chrome VRP Panel has decided to award you $7,000 for this report of a memory corruption bug in the renderer / sandboxed process. A member of the p2p-vrp finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work!

### jo...@ret2.one (2024-02-15)

I'm very happy with this! But I finished the RCE exploit in rendering process literally today, how do I proceed? I need to send the exploit to vrp email or attach here?
Exploit use this heap oob write and target Chromium version 123.0.6264.0

### am...@chromium.org (2024-02-15)

Posting directly to the relevant bug report for the vulnerability is best. Please never send exploits via email. :)
You can upload your exploit and any further information directly here.

### jo...@ret2.one (2024-02-20)

Right! Below I will try to give an overview of the exploit code and explain what it does

# Exploit

## The bug

The bug happened because a malformed BMP image reach in `BMPImageReader::ColorCorrectCurrentRow` with `coord_.y()=-1` and, on calculate address to this row buffer, this code will be executed:

```
const uint32_t* addr32(int x, int y) const {
    SkASSERT((unsigned)x < (unsigned)fInfo.width());
    SkASSERT((unsigned)y < (unsigned)fInfo.height());
    return (const uint32_t*)((const char*)this->addr32() + (size_t)y * fRowBytes + (x << 2));
}

```

Since `y` is -1 and will be multiplied by `fRowBytes`, this address will sum `this->addr32()` with a negative number, and the final pointer will point to last chunk.

## Primitives

`fRowBytes` is the size of a row and can be calculated as `width * 4`, so fRowBytes will be 1/4 of total buffer size. Take the width 0x400 as an example, we will have this `y * fRowBytes + (x << 2)`, giving the values, y=-1, x=0 and fRowBytes=0x1000 (0x400 \* 4), the result will be `-1 * 0x1000 + (0 << 2)`=-0x1000, and add this with `this->addr32`, the result will be 0x1000 before to pointer start.
Good, we can overwrite 1/4 of the last chunk, but what we write? We just write null bytes, except 0xff bytes and the most significant byte from uint32's values are ignored, as you can see here:

```
pwndbg> x/6gx 0x62400eee000
0x62400eee000:	0x4141414141414141	0x4242424242424242
0x62400eee010:	0x4343434343434343	0x4444444444444444
0x62400eee020:	0x4545454545454545	0xff00ff00ff00ff00
pwndbg> ni
...
pwndbg> x/6gx 0x62400eee000
0x62400eee000:	0x4100000041000000	0x4200000042000000
0x62400eee010:	0x4300000043000000	0x4400000044000000
0x62400eee020:	0x4500000045000000	0xff00ff00ff00ff00

```

Ok, very very strict primitives, so, what type of data is viable to corrupt in exploitable point view? In this case is very complex to overwrite a pointer because we will just generate a null pointer or pointer which will crash on deref, other idea is overwrite a ref\_count\_, but this prop only exist at the beginning of the chunk.

## Cross-cache / Cross-bucket overflow

Digging into PartitionAlloc code, I didn't find any redzone between slot's, span's or buckets. So, its completely possible and stable to alloc slots of different size's in adjacent memory.
With a little bit of spray and free's, you can manipulate the heap layout to allocate vulnerable chunk just before(after in our case) the victim chunk.

## Strategy

Using this new cross-bucket overflow technique, the target is allocate a CSSVariableData right before the vulnerable image chunk and overflow the ref\_count\_. I set the width to 0x800 to allocate a buffer of 0x8000 size, and allocate a CSSVariableData of 0x2000 size (1/4 of 0x8000):

```
for (let i = 0; i < 50; i++) {
  for (let j = 0; j < 4; j++) {
    const CSSValName = `${i}.${j}`.padEnd(0x7fcc, 'A'); // 0x7fcc=0x8000-0x34
    div0.style.setProperty(`--a${i}.${j}`, CSSValName);
    const CSSValName2 = `${i}.${j}`.padEnd(0x1fcc, 'C'); // 0x1fcc=0x2000-0x34
    div0.style.setProperty(`--c${i}.${j}`, CSSValName2);
  }
  ...
}

for (let i = 10; i < 30; i++) {
  div0.style.removeProperty(`--a${i}.2`);
}
for (let i = 46; i > 20; i--) {
  div0.style.removeProperty(`--c${i}.0`);
}
gc(); await sleep(500);

```

After successful corrupt the refcount and force the CSSVariable free, we create a UAF and alloc a AudioArray with full controlled data to forge a new length and create a OOB read memory in heap. With this leak in hands, we free CSSVariable and AudioArray, creating a double-free and allocation a new AudioArray we can corrupt freelist to point to another place where exist a vtable pointer, after that we have control flow and memory leak and just need choose a shellcode, i just use a system call to simplification of the exploit.

### Environment

OS used to develop exploit: Linux 6.5.0-17-generic, Ubuntu 22.04.3 LTS  

Chrome version: Chromium 123.0.6264.0  

Chrome commit: fca38abc0001a07f87d0d9aa050ab2d65576aca5  

Start cmd: `./chrome --no-sandbox --headless --user-data-dir=/tmp/not-exist --disable-gpu --remote-debugging-port=9222 --enable-logging=stderr http://localhost:8000/cross-libc.html`  

args.gn:

```
# Set build arguments here. See `gn help buildargs`.
dcheck_always_on = false # I modify build/config/dcheck_always_on.gni to disable dcheck
is_debug = false
is_component_build = true
enable_nacl = false
symbol_level = 2
v8_symbol_level = 0
is_asan = false

```

The exploit reliability are a little bit low.

> Images and exploit in attachments

### am...@chromium.org (2024-02-21)

Thanks so much for the exploit and the related analysis. We'll give it a look at a forthcoming VRP panel session.

### am...@chromium.org (2024-02-29)

Congratulations! The Chrome VRP Panel has assessed your exploit submission and decided to award you an additional $8000 for a total of $15,000 -- the reward for high quality report + functional exploit. Thank you for the extra effort to craft an exploit and demonstrate the exploitability of this issue in Chrome -- great work!

### ap...@google.com (2024-03-13)

Project: chromium/src
Branch: refs/branch-heads/6099_225

commit 74686d7ac67fcc6aad9d34c7ab0b231e5c70c0be
Author: John Stiles <johnstiles@google.com>
Date:   Wed Mar 13 14:44:42 2024

    Fix a crash when a BMP image contains an unnecessary EOF code.
    
    Previously, this would try to perform color correction on a row
    one past the end of the image data.
    
    Bug: 1521893
    Change-Id: I425437005b9ef400138556705616095857d2cf0d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5241305
    Auto-Submit: John Stiles <johnstiles@google.com>
    Commit-Queue: John Stiles <johnstiles@google.com>
    Reviewed-by: Peter Kasting <pkasting@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1253633}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5284451
    Reviewed-by: John Stiles <johnstiles@google.com>
    Auto-Submit: Richard Yeh <rcy@google.com>
    Reviewed-by: Kyle Williams <kdgwill@chromium.org>
    Owners-Override: Richard Yeh <rcy@google.com>
    Commit-Queue: Kyle Williams <kdgwill@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099_225@{#15}
    Cr-Branched-From: 6d3cc0dac5057925e096b1329680124b19f35842-refs/branch-heads/6099@{#1762}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       third_party/blink/renderer/platform/blink_platform_unittests_bundle_data.filelist
M       third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_decoder_test.cc
M       third_party/blink/renderer/platform/image-decoders/bmp/bmp_image_reader.cc
A       third_party/blink/web_tests/images/resources/unnecessary-eof.bmp

https://chromium-review.googlesource.com/5284451


### pe...@google.com (2024-05-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### cs...@gmail.com (2024-05-27)

This doesn't work for me on any release, including Chromium prebuilts before this was reported. I've tried to use cross-libc.html on ChromeOS r120, ChromeOS r124, and Chromium r120 (Chromium 120.0.6099.71, Debian Linux) using the exact command (`./chrome --no-sandbox --headless --user-data-dir=/tmp/not-exist --disable-gpu --remote-debugging-port=9222 --enable-logging=stderr http://localhost:8000/cross-libc.html`) and yet I keep getting this error in devtools console:

```
[0527/132953.259453:WARNING:sandbox_linux.cc(400)] InitializeSandbox() called with multiple threads in process gpu-process.
[0527/132953.422099:WARNING:bluez_dbus_manager.cc(248)] Floss manager not present, cannot set Floss enable/disable.

DevTools listening on ws://127.0.0.1:9222/devtools/browser/541980dd-aacd-47a3-a2f3-ac3413ebe717
[0527/132954.020131:INFO:CONSOLE(118)] "start", source: http://localhost:8000/cross-libc.html (118)
[0527/132955.927980:INFO:CONSOLE(147)] "overflowing...", source: http://localhost:8000/cross-libc.html (147)
[0527/133002.880389:INFO:CONSOLE(173)] "continuing...", source: http://localhost:8000/cross-libc.html (173)
[0527/133002.894049:INFO:CONSOLE(177)] "0", source: http://localhost:8000/cross-libc.html (177)
[0527/133002.898195:INFO:CONSOLE(181)] "WARN: insufficient CSSVars found, found vs min: 0 vs 10", source: http://localhost:8000/cross-libc.html (181)

```

Any reason why? I always get the CSSVars issue and `0` instead of 4008 at `INFO:CONSOLE(177)`, for all three devices/tests.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41494860)*
