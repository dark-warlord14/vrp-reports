# Security:  UAF in  dav1d_get_bits  function

| Field | Value |
|-------|-------|
| **Issue ID** | [40056868](https://issues.chromium.org/issues/40056868) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Media>Codecs |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | wt...@google.com |
| **Created** | 2021-08-13 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

This issue is found by my fuzzer.This vulnerability is only triggered on the release version with asan enabled. I don’t know why the normal version can’t crash. If you know, please tell me. I’m not very familiar with chrome.

**VERSION**  

Chrome Version: 94.0.4604.0 dev x64  

Operating System: windows10 21h1

# **REPRODUCTION CASE** C:\src\chromium\src\out\Release>chrome.exe --no-sandbox C:\Users\yaozhihua\Desktop\FuzzToolsPrivate\MutatorFuzzv1.0\crash\crash\_2021\_05\_24\_13\_47\_34.avif

==5952==ERROR: AddressSanitizer: heap-use-after-free on address 0x11d33640260a at pc 0x7ffeb2496138 bp 0x0047ebffccc0 sp 0x0047ebffcd08  

READ of size 1 at 0x11d33640260a thread T13  

==5952==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==5952==\*\*\* Most likely this means that the app is already \*\*\*  

==5952==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==5952==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==5952==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffeb2496137 in dav1d\_get\_bits C:\src\chromium\src\third\_party\dav1d\libdav1d\src\getbits.c:69  

#1 0x7ffeb23e2706 in dav1d\_parse\_obus C:\src\chromium\src\third\_party\dav1d\libdav1d\src\obu.c:1189  

#2 0x7ffeb22a18e4 in gen\_picture C:\src\chromium\src\third\_party\dav1d\libdav1d\src\lib.c:432  

#3 0x7ffeb22a19ec in dav1d\_get\_picture C:\src\chromium\src\third\_party\dav1d\libdav1d\src\lib.c:477  

#4 0x7ffeb084c1e4 in dav1dCodecGetNextImage C:\src\chromium\src\third\_party\libavif\src\src\codec\_dav1d.c:94  

#5 0x7ffeb0831a31 in avifDecoderNextImage C:\src\chromium\src\third\_party\libavif\src\src\read.c:3625  

#6 0x7ffeb08348d8 in avifDecoderNthImage C:\src\chromium\src\third\_party\libavif\src\src\read.c:3792  

#7 0x7ffeb0463316 in blink::AVIFImageDecoder::Decode C:\src\chromium\src\third\_party\blink\renderer\platform\image-decoders\avif\avif\_image\_decoder.cc:577  

#8 0x7ffeb0138b14 in blink::ImageDecoder::DecodeFrameBufferAtIndex C:\src\chromium\src\third\_party\blink\renderer\platform\image-decoders\image\_decoder.cc:422  

#9 0x7ffeb002d9ea in blink::ImageDecoderWrapper::Decode C:\src\chromium\src\third\_party\blink\renderer\platform\graphics\image\_decoder\_wrapper.cc:133  

#10 0x7ffeb003de06 in blink::ImageFrameGenerator::DecodeAndScale C:\src\chromium\src\third\_party\blink\renderer\platform\graphics\image\_frame\_generator.cc:146  

#11 0x7ffeafec71fd in blink::DecodingImageGenerator::GetPixels C:\src\chromium\src\third\_party\blink\renderer\platform\graphics\decoding\_image\_generator.cc:199  

#12 0x7fff07901cbd in cc::PaintImage::DecodeFromGenerator C:\src\chromium\src\cc\paint\paint\_image.cc:235  

#13 0x7fff07901971 in cc::PaintImage::Decode C:\src\chromium\src\cc\paint\paint\_image.cc:208  

#14 0x7ffef57d738c in cc::`anonymous namespace'::DrawAndScaleImage C:\src\chromium\src\cc\tiles\gpu_image_decode_cache.cc:275 #15 0x7ffef57d3dbf in cc::GpuImageDecodeCache::DecodeImageIfNecessary C:\src\chromium\src\cc\tiles\gpu_image_decode_cache.cc:2012 #16 0x7ffef57ccf80 in cc::GpuImageDecodeCache::DecodeImageInTask C:\src\chromium\src\cc\tiles\gpu_image_decode_cache.cc:1498 #17 0x7ffef57e5471 in cc::GpuImageDecodeTaskImpl::RunOnWorkerThread C:\src\chromium\src\cc\tiles\gpu_image_decode_cache.cc:531 #18 0x7ffecb0f2978 in content::CategorizedWorkerPool::RunTaskInCategoryWithLockAcquired C:\src\chromium\src\content\renderer\categorized_worker_pool.cc:453 #19 0x7ffecb0f13ad in content::CategorizedWorkerPool::RunTaskWithLockAcquired C:\src\chromium\src\content\renderer\categorized_worker_pool.cc:423 #20 0x7ffecb0f128f in content::CategorizedWorkerPool::Run C:\src\chromium\src\content\renderer\categorized_worker_pool.cc:306 #21 0x7fff09e8fc6f in base::`anonymous namespace'::ThreadFunc C:\src\chromium\src\base\threading\platform\_thread\_win.cc:121  

#22 0x7fff091cd5e3 in \_asan\_print\_accumulated\_stats+0x15e3 (C:\src\chromium\src\out\Release\clang\_rt.asan\_dynamic-x86\_64.dll+0x18003d5e3)  

#23 0x7fff44067033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#24 0x7fff44962650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x11d33640260a is located 13322 bytes inside of 17747-byte region [0x11d3363ff200,0x11d336403753)  

freed by thread T13 here:  

#0 0x7fff091c1c7b in \_asan\_memmove+0x2db (C:\src\chromium\src\out\Release\clang\_rt.asan\_dynamic-x86\_64.dll+0x180031c7b)  

#1 0x7ffeb082e2bd in avifDecoderItemRead C:\src\chromium\src\third\_party\libavif\src\src\read.c:1048  

#2 0x7ffeb0830e3e in avifDecoderPrepareSample C:\src\chromium\src\third\_party\libavif\src\src\read.c:3004  

#3 0x7ffeb0831871 in avifDecoderNextImage C:\src\chromium\src\third\_party\libavif\src\src\read.c:3613  

#4 0x7ffeb08348d8 in avifDecoderNthImage C:\src\chromium\src\third\_party\libavif\src\src\read.c:3792  

#5 0x7ffeb0463316 in blink::AVIFImageDecoder::Decode C:\src\chromium\src\third\_party\blink\renderer\platform\image-decoders\avif\avif\_image\_decoder.cc:577  

#6 0x7ffeb0138b14 in blink::ImageDecoder::DecodeFrameBufferAtIndex C:\src\chromium\src\third\_party\blink\renderer\platform\image-decoders\image\_decoder.cc:422  

#7 0x7ffeb002d9ea in blink::ImageDecoderWrapper::Decode C:\src\chromium\src\third\_party\blink\renderer\platform\graphics\image\_decoder\_wrapper.cc:133  

#8 0x7ffeb003de06 in blink::ImageFrameGenerator::DecodeAndScale C:\src\chromium\src\third\_party\blink\renderer\platform\graphics\image\_frame\_generator.cc:146  

#9 0x7ffeafec71fd in blink::DecodingImageGenerator::GetPixels C:\src\chromium\src\third\_party\blink\renderer\platform\graphics\decoding\_image\_generator.cc:199  

#10 0x7fff07901cbd in cc::PaintImage::DecodeFromGenerator C:\src\chromium\src\cc\paint\paint\_image.cc:235  

#11 0x7fff07901971 in cc::PaintImage::Decode C:\src\chromium\src\cc\paint\paint\_image.cc:208  

#12 0x7ffef57d738c in cc::`anonymous namespace'::DrawAndScaleImage C:\src\chromium\src\cc\tiles\gpu_image_decode_cache.cc:275 #13 0x7ffef57d3dbf in cc::GpuImageDecodeCache::DecodeImageIfNecessary C:\src\chromium\src\cc\tiles\gpu_image_decode_cache.cc:2012 #14 0x7ffef57ccf80 in cc::GpuImageDecodeCache::DecodeImageInTask C:\src\chromium\src\cc\tiles\gpu_image_decode_cache.cc:1498 #15 0x7ffef57e5471 in cc::GpuImageDecodeTaskImpl::RunOnWorkerThread C:\src\chromium\src\cc\tiles\gpu_image_decode_cache.cc:531 #16 0x7ffecb0f2978 in content::CategorizedWorkerPool::RunTaskInCategoryWithLockAcquired C:\src\chromium\src\content\renderer\categorized_worker_pool.cc:453 #17 0x7ffecb0f13ad in content::CategorizedWorkerPool::RunTaskWithLockAcquired C:\src\chromium\src\content\renderer\categorized_worker_pool.cc:423 #18 0x7ffecb0f128f in content::CategorizedWorkerPool::Run C:\src\chromium\src\content\renderer\categorized_worker_pool.cc:306 #19 0x7fff09e8fc6f in base::`anonymous namespace'::ThreadFunc C:\src\chromium\src\base\threading\platform\_thread\_win.cc:121  

#20 0x7fff091cd5e3 in \_asan\_print\_accumulated\_stats+0x15e3 (C:\src\chromium\src\out\Release\clang\_rt.asan\_dynamic-x86\_64.dll+0x18003d5e3)  

#21 0x7fff44067033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#22 0x7fff44962650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

previously allocated by thread T13 here:  

#0 0x7fff091c1d7b in \_asan\_memmove+0x3db (C:\src\chromium\src\out\Release\clang\_rt.asan\_dynamic-x86\_64.dll+0x180031d7b)  

#1 0x7ffeb0821c7d in avifAlloc C:\src\chromium\src\third\_party\libavif\src\src\mem.c:10  

#2 0x7ffeb0823458 in avifRWDataRealloc C:\src\chromium\src\third\_party\libavif\src\src\rawdata.c:13  

#3 0x7ffeb082e2bd in avifDecoderItemRead C:\src\chromium\src\third\_party\libavif\src\src\read.c:1048  

#4 0x7ffeb0830e3e in avifDecoderPrepareSample C:\src\chromium\src\third\_party\libavif\src\src\read.c:3004  

#5 0x7ffeb0831871 in avifDecoderNextImage C:\src\chromium\src\third\_party\libavif\src\src\read.c:3613  

#6 0x7ffeb08348d8 in avifDecoderNthImage C:\src\chromium\src\third\_party\libavif\src\src\read.c:3792  

#7 0x7ffeb0463316 in blink::AVIFImageDecoder::Decode C:\src\chromium\src\third\_party\blink\renderer\platform\image-decoders\avif\avif\_image\_decoder.cc:577  

#8 0x7ffeb0138b14 in blink::ImageDecoder::DecodeFrameBufferAtIndex C:\src\chromium\src\third\_party\blink\renderer\platform\image-decoders\image\_decoder.cc:422  

#9 0x7ffeb002d9ea in blink::ImageDecoderWrapper::Decode C:\src\chromium\src\third\_party\blink\renderer\platform\graphics\image\_decoder\_wrapper.cc:133  

#10 0x7ffeb003de06 in blink::ImageFrameGenerator::DecodeAndScale C:\src\chromium\src\third\_party\blink\renderer\platform\graphics\image\_frame\_generator.cc:146  

#11 0x7ffeafec71fd in blink::DecodingImageGenerator::GetPixels C:\src\chromium\src\third\_party\blink\renderer\platform\graphics\decoding\_image\_generator.cc:199  

#12 0x7fff07901cbd in cc::PaintImage::DecodeFromGenerator C:\src\chromium\src\cc\paint\paint\_image.cc:235  

#13 0x7fff07901971 in cc::PaintImage::Decode C:\src\chromium\src\cc\paint\paint\_image.cc:208  

#14 0x7ffef57d738c in cc::`anonymous namespace'::DrawAndScaleImage C:\src\chromium\src\cc\tiles\gpu_image_decode_cache.cc:275 #15 0x7ffef57d3dbf in cc::GpuImageDecodeCache::DecodeImageIfNecessary C:\src\chromium\src\cc\tiles\gpu_image_decode_cache.cc:2012 #16 0x7ffef57ccf80 in cc::GpuImageDecodeCache::DecodeImageInTask C:\src\chromium\src\cc\tiles\gpu_image_decode_cache.cc:1498 #17 0x7ffef57e5471 in cc::GpuImageDecodeTaskImpl::RunOnWorkerThread C:\src\chromium\src\cc\tiles\gpu_image_decode_cache.cc:531 #18 0x7ffecb0f2978 in content::CategorizedWorkerPool::RunTaskInCategoryWithLockAcquired C:\src\chromium\src\content\renderer\categorized_worker_pool.cc:453 #19 0x7ffecb0f13ad in content::CategorizedWorkerPool::RunTaskWithLockAcquired C:\src\chromium\src\content\renderer\categorized_worker_pool.cc:423 #20 0x7ffecb0f128f in content::CategorizedWorkerPool::Run C:\src\chromium\src\content\renderer\categorized_worker_pool.cc:306 #21 0x7fff09e8fc6f in base::`anonymous namespace'::ThreadFunc C:\src\chromium\src\base\threading\platform\_thread\_win.cc:121  

#22 0x7fff091cd5e3 in \_asan\_print\_accumulated\_stats+0x15e3 (C:\src\chromium\src\out\Release\clang\_rt.asan\_dynamic-x86\_64.dll+0x18003d5e3)  

#23 0x7fff44067033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#24 0x7fff44962650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

Thread T13 created by T0 here:  

#0 0x7fff091cdff2 in \_asan\_wrap\_CreateThread+0x62 (C:\src\chromium\src\out\Release\clang\_rt.asan\_dynamic-x86\_64.dll+0x18003dff2)  

#1 0x7fff09e8f07f in base::`anonymous namespace'::CreateThreadInternal C:\src\chromium\src\base\threading\platform\_thread\_win.cc:185  

#2 0x7fff09dcaaa0 in base::SimpleThread::StartAsync C:\src\chromium\src\base\threading\simple\_thread.cc:51  

#3 0x7ffecb0eed44 in content::CategorizedWorkerPool::Start C:\src\chromium\src\content\renderer\categorized\_worker\_pool.cc:211  

#4 0x7ffecb1d7a06 in content::RenderThreadImpl::Init C:\src\chromium\src\content\renderer\render\_thread\_impl.cc:712  

#5 0x7ffecb1d91fe in content::RenderThreadImpl::RenderThreadImpl C:\src\chromium\src\content\renderer\render\_thread\_impl.cc:561  

#6 0x7ffecb200757 in content::RendererMain C:\src\chromium\src\content\renderer\renderer\_main.cc:213  

#7 0x7ffecb5a81b8 in content::ContentMainRunnerImpl::Run C:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:973  

#8 0x7ffecb5a4827 in content::RunContentProcess C:\src\chromium\src\content\app\content\_main.cc:390  

#9 0x7ffecb5a5843 in content::ContentMain C:\src\chromium\src\content\app\content\_main.cc:418  

#10 0x7ffece091499 in ChromeMain C:\src\chromium\src\chrome\app\chrome\_main.cc:172  

#11 0x7ff7f98c5573 in MainDllLoader::Launch C:\src\chromium\src\chrome\app\main\_dll\_loader\_win.cc:169  

#12 0x7ff7f98c29af in main C:\src\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#13 0x7ff7f9a9627b in \_\_scrt\_common\_main\_seh D:\agent\_work\13\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#14 0x7fff44067033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#15 0x7fff44962650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

SUMMARY: AddressSanitizer: heap-use-after-free C:\src\chromium\src\third\_party\dav1d\libdav1d\src\getbits.c:69 in dav1d\_get\_bits  

Shadow bytes around the buggy address:  

0x03bb9d000470: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03bb9d000480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03bb9d000490: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03bb9d0004a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03bb9d0004b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x03bb9d0004c0: fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03bb9d0004d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03bb9d0004e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03bb9d0004f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03bb9d000500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03bb9d000510: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==5952==ABORTING

Reporter credit:  

Zhihua Yao of KunLun Lab  

ryelv of tencent security

## Attachments

- [crash_2021_05_24_13_47_34.avif](attachments/crash_2021_05_24_13_47_34.avif) (application/octet-stream, 63.5 KB)

## Timeline

### [Deleted User] (2021-08-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-08-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5669511444103168.

### wf...@chromium.org (2021-08-13)

Hi thanks for your report. I can't get this to trigger on release asan build I am using 94.0.4595.0 (Developer Build) (64-bit) though so maybe this is a very recent regression, but then clusterfuzz can't repro on head either. Do you know what flags you are using to compile chrome here?

### ha...@gmail.com (2021-08-13)

I am going to rebuild the chromium and test the recent version.I will give you feedback.

### [Deleted User] (2021-08-13)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2021-08-13)

Thanks, adding some owners in the meantime.

[Monorail components: Internals>Media>Codecs]

### ha...@gmail.com (2021-08-13)

When I was built the chromium,I dsiabled the dcheck and enable the Experimental Web Platform features

### cl...@chromium.org (2021-08-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5725106788433920.

### wf...@chromium.org (2021-08-13)

I am able to repro with Experimental Web Platform features, hopefully clusterfuzz can too. Sec Severity High.

wtc -> Can you take a look at this? Do we have a avif fuzzer running ourselves?

### [Deleted User] (2021-08-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-08-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5015458590556160.

### ha...@gmail.com (2021-08-14)

Yeah,I am aslo could repro in 95.0.4607.0 dev x64

0:015> g
ModLoad: 00007fff`3ff30000 00007fff`3ff42000   C:\Windows\SYSTEM32\kernel.appcore.dll
(445c.1f44): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** WARNING: Unable to verify checksum for C:\src\chromium\src\out\Default\blink_platform.dll
blink_platform!refill+0x26 [inlined in blink_platform!dav1d_get_bits+0x35]:
00007ffe`ca2a5f4a 0fb609          movzx   ecx,byte ptr [rcx] ds:00000203`29a44eaa=??
0:020> !heap -p -a rcx
**********************************************

the `!heap -p' commands in exts.dll have been replaced
with equivalent commands in ext.dll.
If your are in a KD session, use `!ext.heap -p`
**********************************************
0:020> !ext.heap -p -a rcx
    address 0000020329a44eaa found in
    _DPH_HEAP_ROOT @ 2037b3a1000
    in free-ed allocation (  DPH_HEAP_BLOCK:         VirtAddr         VirtSize)
                                20328a8eb60:      20329a41000             6000
    00007fff44a09144 ntdll!RtlDebugFreeHeap+0x0000000000000038
    00007fff44935cc1 ntdll!RtlpFreeHeap+0x00000000000000c1
    00007fff44935b74 ntdll!RtlpFreeHeapInternal+0x0000000000000464
    00007fff449347b1 ntdll!RtlFreeHeap+0x0000000000000051
    00007fff4250f05b ucrtbase!_free_base+0x000000000000001b
    00007ffec9af250f blink_platform!avifDecoderItemRead+0x0000000000000194 [o:\third_party\libavif\src\src\read.c @ 1049]
    00007ffec9af2fe5 blink_platform!avifDecoderPrepareSample+0x0000000000000092 [o:\third_party\libavif\src\src\read.c @ 3005]
    00007ffec9af322e blink_platform!avifDecoderNextImage+0x000000000000008d [o:\third_party\libavif\src\src\read.c @ 3614]
    00007ffec9af3c5e blink_platform!avifDecoderNthImage+0x0000000000000077 [o:\third_party\libavif\src\src\read.c @ 3793]
    00007ffec99ef95e blink_platform!blink::AVIFImageDecoder::DecodeToYUV+0x000000000000006e [o:\third_party\blink\renderer\platform\image-decoders\avif\avif_image_decoder.cc @ 366]
    00007ffec85e8c31 blink_modules!blink::ImageDecoderCore::MaybeDecodeToYuv+0x0000000000000101 [o:\third_party\blink\renderer\modules\webcodecs\image_decoder_core.cc @ 356]
    00007ffec85e885e blink_modules!blink::ImageDecoderCore::Decode+0x000000000000017e [o:\third_party\blink\renderer\modules\webcodecs\image_decoder_core.cc @ 171]
    00007ffec85ec5f6 +0x0000000000000026 [o:\base\bind_internal.h @ 694]
    00007ffec85edc85 blink_modules!base::internal::ReturnAsParamAdapter<std::__1::unique_ptr<blink::ImageDecoderCore::ImageDecodeResult,std::__1::default_delete<blink::ImageDecoderCore::ImageDecodeResult> > >+0x0000000000000045 [o:\base\post_task_and_reply_with_result_internal.h @ 22]
    00007ffec85eddf5 +0x0000000000000035 [o:\base\bind_internal.h @ 690]
    00007fff0b16258f base!base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply+0x000000000000002f [o:\base\threading\post_task_and_reply_impl.cc @ 97]
    00007fff0b1627e4 base!base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce+0x0000000000000054 [o:\base\bind_internal.h @ 690]
    00007fff0b12b640 base!base::TaskAnnotator::RunTask+0x0000000000000190 [o:\base\task\common\task_annotator.cc @ 178]
    00007fff0b151947 base!base::internal::TaskTracker::RunSkipOnShutdown+0x0000000000000017 [o:\base\task\thread_pool\task_tracker.cc @ 664]
    00007fff0b151334 base!base::internal::TaskTracker::RunTask+0x0000000000000304 [o:\base\task\thread_pool\task_tracker.cc @ 528]
    00007fff0b150e5e base!base::internal::TaskTracker::RunAndPopNextTask+0x000000000000023e [o:\base\task\thread_pool\task_tracker.cc @ 433]
    00007fff0b15a513 base!base::internal::WorkerThread::RunWorker+0x0000000000000323 [o:\base\task\thread_pool\worker_thread.cc @ 371]
    00007fff0b15a0c8 base!base::internal::WorkerThread::RunPooledWorker+0x0000000000000018 [o:\base\task\thread_pool\worker_thread.cc @ 263]
    00007fff0b19e9b0 base!base::`anonymous namespace'::ThreadFunc+0x00000000000000f0 [o:\base\threading\platform_thread_win.cc @ 113]
    00007fff44067034 KERNEL32!BaseThreadInitThunk+0x0000000000000014
    00007fff44962651 ntdll!RtlUserThreadStart+0x0000000000000021

### cl...@chromium.org (2021-08-14)

Detailed Report: https://clusterfuzz.com/testcase?key=5015458590556160

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x62900007160a
Crash State:
  dav1d_get_bits
  dav1d_parse_obus
  gen_picture
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=906866:906870

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5015458590556160

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5015458590556160 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2021-08-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2021-08-18)

Looks like an issue in libavif rather than dav1d since the memory is freed by libavif. +jdrago in case there's been a fix in this area we should pick up.

### jd...@netflix.com (2021-08-18)

Hello Dale --

Is there a commit range for libavif related to this regression that I could inspect? I see that the attached AVIF has an a1lx box property, so I suspect this could be related to progressive decoding (which is the newest feature, and hasn't shipped in Chrome yet, I don't think). Does the issue go away if avifDecoder.allowProgressive is never set to AVIF_TRUE?

I don't believe WTC is available until next week, but if it is progressive decoding related, never setting allowProgressive  to AVIF_TRUE should avoid it. Of course, rolling back to a libavif commit that doesn't have code entirely is probably even safer.

### jd...@netflix.com (2021-08-18)

I see the Chromium commit range, which includes this commit:

https://chromium.googlesource.com/chromium/src/+/e91e0194604cf3c4917f71b8a64964343bde3d59

If this is something that can consistently be reproduced via ClusterFuzz with local changes (I'm not familiar), I'd be curious if simply removing / commenting out this line:

decoder_->allowProgressive = !IsAllDataReceived();

... eliminates the issue. It is probably easier to simply revert this Chromium commit (e91e0194604cf3c4917f71b8a64964343bde3d59) for now though. To revert libavif itself back to a commit which has zero understanding of progressive images, the most recent libavif version is v0.9.2, which is commit 45d58a5160ba2c33f5b341f3ba4b8ffe82928f87 and has zero progressive support in it.

### da...@chromium.org (2021-08-18)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-08-18)

Disabling progressive image support does fix the issue. The crash doesn't occur on the first partial decode, but only when transitioning from that to the full decode.

### fg...@chromium.org (2021-08-18)

Thanks for checking Dale. I think disabling support is the best option for now. Wan-Teh can look into fixing this when he gets back.


### da...@chromium.org (2021-08-18)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-08-18)

Sent https://chromium-review.googlesource.com/c/chromium/src/+/3105147 to disable progressive support for now.

### jd...@netflix.com (2021-08-19)

Using the testcase payload above and some sneaky VirtualProtect trickery in Windows, I successfully reproduced the use-after-free in a debugger and diagnosed/fixed the bug (I believe). I have an open PR waiting here with WTC's name on it when he returns:

https://github.com/AOMediaCodec/libavif/pull/736

The new progressive image decode paths were (correctly) reusing a buffer inside of an AVIF "item" for the partial item payload reads it must do, but this code was not accounting for the fact that this buffer might still be in use by the underlying AV1 decoder when the next read comes in (which might cause a resize of the buffer, thus creating the use-after-free). My PR creates the item's buffer in its entirety once (no reallocation of this buffer), so the addresses should stay consistent for the duration of the progressive decode now. 

I don't think this potential fix should change any of the current strategy for handling this issue, to be clear. We should continue with the disabling of progressive functionality for now, and when WTC comes back, we can audit this new PR and reenable it in a future milestone. I am confident though (having reproduced this) that Dale's PR is sufficient to avoid this. Without progressive decoding enabled, libavif never does partial item reads on an AV1 payload, which (combined with reallocs due to the partial reads) is the source of this issue.

### gi...@appspot.gserviceaccount.com (2021-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e4442c1820ed4d8e155d2ec2fb9f35560da85636

commit e4442c1820ed4d8e155d2ec2fb9f35560da85636
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Thu Aug 19 12:46:50 2021

Disable progressive AVIF support.

R=pkasting

Bug: 1221717,1239472
Change-Id: I82c6e8dce55b680e71f81ce4d5112979147278fe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3105147
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/main@{#913367}

[modify] https://crrev.com/e4442c1820ed4d8e155d2ec2fb9f35560da85636/third_party/blink/renderer/platform/image-decoders/avif/avif_image_decoder.cc
[modify] https://crrev.com/e4442c1820ed4d8e155d2ec2fb9f35560da85636/third_party/blink/renderer/platform/image-decoders/avif/avif_image_decoder_test.cc


### da...@chromium.org (2021-08-19)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-08-19)

Thanks Joe!

### rs...@chromium.org (2021-08-19)

Marking as Fixed for sheriffbot to handle merge decisions.

### [Deleted User] (2021-08-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-20)

Your change meets the bar and is auto-approved for M94. Please go ahead and merge the CL to branch 4606 (refs/branch-heads/4606) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2021-08-20)

Merge https://chromium-review.googlesource.com/c/chromium/src/+/3111566

### gi...@appspot.gserviceaccount.com (2021-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/57dfffd794cafdeb4c3bdb40ac96ebdb6d22c2f6

commit 57dfffd794cafdeb4c3bdb40ac96ebdb6d22c2f6
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Fri Aug 20 21:22:17 2021

Merge M94: "Disable progressive AVIF support."

R=​pkasting

(cherry picked from commit e4442c1820ed4d8e155d2ec2fb9f35560da85636)

Bug: 1221717,1239472
Change-Id: I82c6e8dce55b680e71f81ce4d5112979147278fe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3105147
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#913367}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3111566
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#183}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/57dfffd794cafdeb4c3bdb40ac96ebdb6d22c2f6/third_party/blink/renderer/platform/image-decoders/avif/avif_image_decoder.cc
[modify] https://crrev.com/57dfffd794cafdeb4c3bdb40ac96ebdb6d22c2f6/third_party/blink/renderer/platform/image-decoders/avif/avif_image_decoder_test.cc


### cl...@chromium.org (2021-08-21)

ClusterFuzz testcase 5015458590556160 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=910752:913964

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### am...@google.com (2021-08-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-25)

Congratulations, Zhihua Yao and ryelv! The VRP Panel has decided to award you $5000 for this report. A member of our finance team will be in touch soon to arrange payment. Nice find and thank you for your report! 

### gi...@appspot.gserviceaccount.com (2021-08-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/644407353b5499109fc5f568dbaf9119016e4d39

commit 644407353b5499109fc5f568dbaf9119016e4d39
Author: Wan-Teh Chang <wtc@google.com>
Date: Thu Aug 26 00:36:20 2021

Roll src/third_party/libavif/src/ bd1492e18..641039caf (3 commits)

https://chromium.googlesource.com/external/github.com/AOMediaCodec/libavif.git/+log/bd1492e1812f..641039cafa3e

$ git log bd1492e18..641039caf --date=short --no-merges --format='%ad %ae %s'
2021-08-22 jdrago Allocate alpha alongside YUV (if necessary) during y4m decode to avoid incorrect alphaRowBytes math
2021-08-19 jdrago When creating the read buffer in avifDecoderItemRead(), always make the buffer the item's full size
2021-08-11 frankgalligan Check for scale values that cause overflow (#735)

Created with:
  roll-dep src/third_party/libavif/src
R=dalecurtis@chromium.org,pkasting@chromium.org

Bug: 1221717,1239472
Change-Id: Ia3b118eff9e34e33b6f5b53236ee956accc4a37d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3119836
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Wan-Teh Chang <wtc@google.com>
Cr-Commit-Position: refs/heads/main@{#915399}

[modify] https://crrev.com/644407353b5499109fc5f568dbaf9119016e4d39/DEPS


### gi...@appspot.gserviceaccount.com (2021-08-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/df38cebb076a09c948129b7f732a19bcf4c21592

commit df38cebb076a09c948129b7f732a19bcf4c21592
Author: Wan-Teh Chang <wtc@google.com>
Date: Thu Aug 26 11:26:41 2021

Revert "Disable progressive AVIF support."

This reverts commit e4442c1820ed4d8e155d2ec2fb9f35560da85636.

Reason for revert: The libavif bug has been fixed in crrev.com/c/3119836

Original change's description:
> Disable progressive AVIF support.
>
> R=​pkasting
>
> Bug: 1221717,1239472
> Change-Id: I82c6e8dce55b680e71f81ce4d5112979147278fe
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3105147
> Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
> Commit-Queue: Peter Kasting <pkasting@chromium.org>
> Reviewed-by: Peter Kasting <pkasting@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#913367}

Bug: 1221717,1239472
Change-Id: I24f59b7c91f5c264dfff136e9fa3a24a677e9e0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3120314
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/main@{#915540}

[modify] https://crrev.com/df38cebb076a09c948129b7f732a19bcf4c21592/third_party/blink/renderer/platform/image-decoders/avif/avif_image_decoder.cc
[modify] https://crrev.com/df38cebb076a09c948129b7f732a19bcf4c21592/third_party/blink/renderer/platform/image-decoders/avif/avif_image_decoder_test.cc


### wt...@google.com (2021-08-26)

Dale: Thank you very much for handling this bug in my absence.

Re: https://crbug.com/chromium/1239472#c9

wfh@chromium.org wrote:
> wtc -> Can you take a look at this? Do we have a avif fuzzer running ourselves?

The libavif project has an avif_decode_fuzzer running under oss-fuzz, but that fuzzer uses different decoder options from Chrome, so it cannot reproduce this UAF error.

I just wrote a libavif pull request to make avif_decode_fuzzer behave more like Chrome:
https://github.com/AOMediaCodec/libavif/pull/743

That will allow avif_decode_fuzzer to reproduce this UAF error. (I am not sure if the pull request will be accepted because it can be considered as Chrome-centric.) A good long-term solution may be to write a fuzzer using Chrome's blink::AVIFImageDecoder class.

### da...@chromium.org (2021-08-26)

AVIF also gets fuzzed in Chrome via https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webcodecs/image_decoder_fuzzer.cc

That path should exercise this issue with a corpus of progressive avif (which we have), so I think the fuzzer just hasn't discovered it yet.

### am...@google.com (2021-08-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8c7de307b53d0b972df5fa9ce699d53e7b0d90f9

commit 8c7de307b53d0b972df5fa9ce699d53e7b0d90f9
Author: Wan-Teh Chang <wtc@google.com>
Date: Mon Aug 30 21:02:14 2021

Roll src/third_party/libavif/src/ bd1492e18..641039caf (3 commits)

Merge to M94 branch:4606.

https://chromium.googlesource.com/external/github.com/AOMediaCodec/libavif.git/+log/bd1492e1812f..641039cafa3e

$ git log bd1492e18..641039caf --date=short --no-merges --format='%ad %ae %s'
2021-08-22 jdrago Allocate alpha alongside YUV (if necessary) during y4m decode to avoid incorrect alphaRowBytes math
2021-08-19 jdrago When creating the read buffer in avifDecoderItemRead(), always make the buffer the item's full size
2021-08-11 frankgalligan Check for scale values that cause overflow (#735)

Created with:
  roll-dep src/third_party/libavif/src
R=​dalecurtis@chromium.org,pkasting@chromium.org

(cherry picked from commit 644407353b5499109fc5f568dbaf9119016e4d39)

Bug: 1221717,1239472
Change-Id: Ia3b118eff9e34e33b6f5b53236ee956accc4a37d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3119836
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Wan-Teh Chang <wtc@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#915399}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3130744
Auto-Submit: Wan-Teh Chang <wtc@google.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4606@{#515}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/8c7de307b53d0b972df5fa9ce699d53e7b0d90f9/DEPS


### gi...@appspot.gserviceaccount.com (2021-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9752a9a086037a66997d16eed90432e48e6c15d5

commit 9752a9a086037a66997d16eed90432e48e6c15d5
Author: Wan-Teh Chang <wtc@google.com>
Date: Tue Aug 31 01:42:49 2021

Revert "Disable progressive AVIF support."

Merge to M94 branch:4606.

This reverts commit e4442c1820ed4d8e155d2ec2fb9f35560da85636.

Reason for revert: The libavif bug has been fixed in crrev.com/c/3119836

Original change's description:
> Disable progressive AVIF support.
>
> R=​pkasting
>
> Bug: 1221717,1239472
> Change-Id: I82c6e8dce55b680e71f81ce4d5112979147278fe
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3105147
> Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
> Commit-Queue: Peter Kasting <pkasting@chromium.org>
> Reviewed-by: Peter Kasting <pkasting@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#913367}

(cherry picked from commit df38cebb076a09c948129b7f732a19bcf4c21592)

Bug: 1221717,1239472
Change-Id: I24f59b7c91f5c264dfff136e9fa3a24a677e9e0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3120314
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#915540}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3130144
Commit-Queue: Wan-Teh Chang <wtc@google.com>
Cr-Commit-Position: refs/branch-heads/4606@{#528}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/9752a9a086037a66997d16eed90432e48e6c15d5/third_party/blink/renderer/platform/image-decoders/avif/avif_image_decoder.cc
[modify] https://crrev.com/9752a9a086037a66997d16eed90432e48e6c15d5/third_party/blink/renderer/platform/image-decoders/avif/avif_image_decoder_test.cc


### vo...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1239472?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056868)*
