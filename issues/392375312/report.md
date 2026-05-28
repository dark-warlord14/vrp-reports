# Information Leak via Out-of-Bounds Read in media::AudioBuffer

| Field | Value |
|-------|-------|
| **Issue ID** | [392375312](https://issues.chromium.org/issues/392375312) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Chrome Version** | 133.0.6876.6  |
| **Reporter** | bl...@gmail.com |
| **Assignee** | tg...@google.com |
| **Created** | 2025-01-26 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Build the chrome:

```
gn gen out/MediaMojoRelease --args="is_debug=false symbol_level=2 enable_nacl=false is_component_build=true dcheck_always_on=false"

```

2. Launch chrome with mojo enable:

```
Release\chrome.exe  --enable-blink-features=MojoJS,MojoJSTest

```

3. Attach the GPU process with a debugger(I don't know why ASAN can't capture this case).
4. Visit the poc.html to trigger crash.

# Problem Description

There is an insufficient validation of the frame\_count parameter when creating an [AudioBuffer](https://source.chromium.org/chromium/chromium/src/+/main:media/base/audio_buffer.cc;drc=27d34700b83f381c62e3a348de2e6dfdc08364b8;l=123) from mojo data.

And the `frame_count` is used to calculate [`data_size_per_channel`](https://source.chromium.org/chromium/chromium/src/+/main:media/base/audio_buffer.cc;drc=27d34700b83f381c62e3a348de2e6dfdc08364b8;bpv=1;bpt=1;l=184?gsn=data_size_per_channel&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Dc%252B%252B%3Fpath%3Dmedia%2Fbase%2Faudio_buffer.cc%23sB4c8_k1CpqMfD_STMuX97qisAXEK675vg36__jUHkw), which represents the size of the data per audio channel.

The `data_size_per_channel` value is subsequently used as the size parameter in a [memcpy](https://source.chromium.org/chromium/chromium/src/+/main:media/base/audio_buffer.cc;bpv=1;bpt=1;l=207?gsn=memcpy&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Dc%252B%252B%23memcpy%2523n%2523builtin), , resulting in an out-of-bounds memory read.

Additionally, the out-of-bounds data located on the heap can be transmitted back to the renderer process after encoding, leading to potential data leakage or further exploitation opportunities.

# Additional Comments

## BISECT

The vulnerability may exist in the first commit of AudioBuffer:
<https://source.chromium.org/chromium/chromium/src/+/55de3108f586fc00efa0a1352f7b63960fb8d15d:media/base/audio_buffer.cc;dlc=fd45eed1e4973593cc55c45424e1fde808bd6d9d>

# Summary

Information Leak via Out-of-Bounds Read in media::AudioBuffer

# Custom Questions

#### Type of crash:

GPU Process

#### Crash state:

```
00 0000008a`c97fc838 00007fff`09cd0762     VCRUNTIME140!memcpy_avx_ermsb_Intel+0x2e9 [D:\a\_work\1\s\src\vctools\crt\vcruntime\src\string\amd64\Intel\memcpy_avx_ermsb_aligned.asm @ 363] 
01 0000008a`c97fc840 00007fff`09cd1767     media!media::AudioBuffer::AudioBuffer+0x7a2 [F:\Chromium\src\media\base\audio_buffer.cc @ 211] 
*** WARNING: Unable to verify checksum for D:\Chromium\dev_6876\Release\media_mojo_services.dll
02 0000008a`c97fc940 00007ffe`9319e359     media!media::AudioBuffer::CopyFrom+0xd7 [F:\Chromium\src\media\base\audio_buffer.cc @ 305] 
03 0000008a`c97fca30 00007ffe`92fe96e1     media_mojo_services!mojo::TypeConverter<scoped_refptr<media::AudioBuffer>,mojo::StructPtr<media::mojom::AudioBuffer> >::Convert+0x679 [F:\Chromium\src\media\mojo\common\media_type_converters.cc @ 250] 
04 (Inline Function) --------`--------     media_mojo_services!mojo::StructPtr<media::mojom::AudioBuffer>::To+0x8 [F:\Chromium\src\mojo\public\cpp\bindings\struct_ptr.h @ 67] 
05 0000008a`c97fcc40 00007ffe`9306879c     media_mojo_services!media::MojoAudioEncoderService::Encode+0x61 [F:\Chromium\src\media\mojo\services\mojo_audio_encoder_service.cc @ 52] 
06 0000008a`c97fcd00 00007ffe`92fd9d9c     media_mojo_services!media::mojom::AudioEncoderStubDispatch::AcceptWithResponder+0x59c [F:\Chromium\src\out\Release\gen\media\mojo\mojom\audio_encoder.mojom.cc @ 1005] 
*** WARNING: Unable to verify checksum for D:\Chromium\dev_6876\Release\mojo_public_cpp_bindings.dll
07 0000008a`c97fce80 00007fff`c14841e7     media_mojo_services!media::mojom::AudioEncoderStub<mojo::UniquePtrImplRefTraits<media::mojom::AudioEncoder,std::__Cr::default_delete<media::mojom::AudioEncoder> > >::AcceptWithResponder+0x3c [F:\Chromium\src\out\Release\gen\media\mojo\mojom\audio_encoder.mojom.h @ 229] 
08 0000008a`c97fced0 00007fff`c148e13d     mojo_public_cpp_bindings!mojo::InterfaceEndpointClient::HandleValidatedMessage+0x727 [F:\Chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 1032] 
09 0000008a`c97fd100 00007fff`c1486b85     mojo_public_cpp_bindings!mojo::MessageDispatcher::Accept+0xed [F:\Chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc @ 48] 
0a 0000008a`c97fd1b0 00007fff`c1493c9a     mojo_public_cpp_bindings!mojo::InterfaceEndpointClient::HandleIncomingMessage+0x375 [F:\Chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 751] 
0b 0000008a`c97fd370 00007fff`c14931a8     mojo_public_cpp_bindings!mojo::internal::MultiplexRouter::ProcessIncomingMessage+0x5ca [F:\Chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc @ 1120] 
0c 0000008a`c97fd4a0 00007fff`c148e189     mojo_public_cpp_bindings!mojo::internal::MultiplexRouter::Accept+0x1f8 [F:\Chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc @ 737] 
0d 0000008a`c97fd6f0 00007fff`c147861b     mojo_public_cpp_bindings!mojo::MessageDispatcher::Accept+0x139 [F:\Chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc @ 43] 
0e 0000008a`c97fd7a0 00007fff`c147926d     mojo_public_cpp_bindings!mojo::Connector::DispatchMessageW+0x38b [F:\Chromium\src\mojo\public\cpp\bindings\lib\connector.cc @ 561] 
0f 0000008a`c97fd930 00007fff`c1478ef7     mojo_public_cpp_bindings!mojo::Connector::ReadAllAvailableMessages+0x14d [F:\Chromium\src\mojo\public\cpp\bindings\lib\connector.cc @ 620] 
10 (Inline Function) --------`--------     mojo_public_cpp_bindings!mojo::Connector::OnHandleReadyInternal+0x2c [F:\Chromium\src\mojo\public\cpp\bindings\lib\connector.cc @ 452] 
11 0000008a`c97fd9e0 00007fff`c1479d8a     mojo_public_cpp_bindings!mojo::Connector::OnWatcherHandleReady+0x57 [F:\Chromium\src\mojo\public\cpp\bindings\lib\connector.cc @ 418] 
*** WARNING: Unable to verify checksum for D:\Chromium\dev_6876\Release\mojo_public_system_cpp.dll
12 0000008a`c97fda30 00007fff`56c1d002     mojo_public_cpp_bindings!base::RepeatingCallback<void (unsigned int)>::Run+0xaa [F:\Chromium\src\base\functional\callback.h @ 345] 
13 0000008a`c97fdac0 00007fff`56c1ce19     mojo_public_system_cpp!base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run+0xb2 [F:\Chromium\src\base\functional\callback.h @ 345] 
*** WARNING: Unable to verify checksum for D:\Chromium\dev_6876\Release\base.dll
14 0000008a`c97fdb50 00007fff`26601b64     mojo_public_system_cpp!mojo::SimpleWatcher::OnHandleReady+0x139 [F:\Chromium\src\mojo\public\cpp\system\simple_watcher.cc @ 279] 
15 0000008a`c97fdbf0 00007fff`266d5614     base!base::OnceCallback<void ()>::Run+0x94 [F:\Chromium\src\base\functional\callback.h @ 156] 
16 0000008a`c97fdc70 00007fff`2673a373     base!base::TaskAnnotator::RunTaskImpl+0x154 [F:\Chromium\src\base\task\common\task_annotator.cc @ 209] 
17 (Inline Function) --------`--------     base!base::TaskAnnotator::RunTask+0x54 [F:\Chromium\src\base\task\common\task_annotator.h @ 106] 
18 (Inline Function) --------`--------     base!base::internal::TaskTracker::RunTaskImpl+0x78 [F:\Chromium\src\base\task\thread_pool\task_tracker.cc @ 677] 
19 0000008a`c97fdd10 00007fff`267396e5     base!base::internal::TaskTracker::RunSkipOnShutdown+0xc3 [F:\Chromium\src\base\task\thread_pool\task_tracker.cc @ 662] 
1a (Inline Function) --------`--------     base!base::internal::TaskTracker::RunTaskWithShutdownBehavior+0x43 [F:\Chromium\src\base\task\thread_pool\task_tracker.cc @ 692] 
1b 0000008a`c97fddd0 00007fff`26738ea0     base!base::internal::TaskTracker::RunTask+0x495 [F:\Chromium\src\base\task\thread_pool\task_tracker.cc @ 520] 
1c 0000008a`c97ff770 00007fff`267481c1     base!base::internal::TaskTracker::RunAndPopNextTask+0x310 [F:\Chromium\src\base\task\thread_pool\task_tracker.cc @ 417] 
1d 0000008a`c97ffa20 00007fff`26747cd8     base!base::internal::WorkerThread::RunWorker+0x3c1 [F:\Chromium\src\base\task\thread_pool\worker_thread.cc @ 493] 
1e 0000008a`c97ffbd0 00007fff`267cbc47     base!base::internal::WorkerThread::RunSharedWorker+0x18 [F:\Chromium\src\base\task\thread_pool\worker_thread.cc @ 390] 
1f 0000008a`c97ffc10 00007ff8`0053e8d7     base!base::`anonymous namespace'::ThreadFunc+0xe7 [F:\Chromium\src\base\threading\platform_thread_win.cc @ 118] 
20 0000008a`c97ffc90 00007ff8`01d9fbcc     KERNEL32!BaseThreadInitThunk+0x17
21 0000008a`c97ffcc0 00000000`00000000     ntdll!RtlUserThreadStart+0x2c

```
#### Reporter credit:

@Bl1nnnk and @Pisanbao

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A

## Attachments

- poc.html (text/html, 3.2 KB)
- get_mojomjs.py (text/x-python, 826 B)

## Timeline

### bl...@gmail.com (2025-01-26)

Crash state:

```
00 0000008a`c97fc838 00007fff`09cd0762     VCRUNTIME140!memcpy_avx_ermsb_Intel+0x2e9 [D:\a\_work\1\s\src\vctools\crt\vcruntime\src\string\amd64\Intel\memcpy_avx_ermsb_aligned.asm @ 363] 
01 0000008a`c97fc840 00007fff`09cd1767     media!media::AudioBuffer::AudioBuffer+0x7a2 [F:\Chromium\src\media\base\audio_buffer.cc @ 211] 
*** WARNING: Unable to verify checksum for D:\Chromium\dev_6876\Release\media_mojo_services.dll
02 0000008a`c97fc940 00007ffe`9319e359     media!media::AudioBuffer::CopyFrom+0xd7 [F:\Chromium\src\media\base\audio_buffer.cc @ 305] 
03 0000008a`c97fca30 00007ffe`92fe96e1     media_mojo_services!mojo::TypeConverter<scoped_refptr<media::AudioBuffer>,mojo::StructPtr<media::mojom::AudioBuffer> >::Convert+0x679 [F:\Chromium\src\media\mojo\common\media_type_converters.cc @ 250] 
04 (Inline Function) --------`--------     media_mojo_services!mojo::StructPtr<media::mojom::AudioBuffer>::To+0x8 [F:\Chromium\src\mojo\public\cpp\bindings\struct_ptr.h @ 67] 
05 0000008a`c97fcc40 00007ffe`9306879c     media_mojo_services!media::MojoAudioEncoderService::Encode+0x61 [F:\Chromium\src\media\mojo\services\mojo_audio_encoder_service.cc @ 52] 
06 0000008a`c97fcd00 00007ffe`92fd9d9c     media_mojo_services!media::mojom::AudioEncoderStubDispatch::AcceptWithResponder+0x59c [F:\Chromium\src\out\Release\gen\media\mojo\mojom\audio_encoder.mojom.cc @ 1005] 
*** WARNING: Unable to verify checksum for D:\Chromium\dev_6876\Release\mojo_public_cpp_bindings.dll
07 0000008a`c97fce80 00007fff`c14841e7     media_mojo_services!media::mojom::AudioEncoderStub<mojo::UniquePtrImplRefTraits<media::mojom::AudioEncoder,std::__Cr::default_delete<media::mojom::AudioEncoder> > >::AcceptWithResponder+0x3c [F:\Chromium\src\out\Release\gen\media\mojo\mojom\audio_encoder.mojom.h @ 229] 
08 0000008a`c97fced0 00007fff`c148e13d     mojo_public_cpp_bindings!mojo::InterfaceEndpointClient::HandleValidatedMessage+0x727 [F:\Chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 1032] 
09 0000008a`c97fd100 00007fff`c1486b85     mojo_public_cpp_bindings!mojo::MessageDispatcher::Accept+0xed [F:\Chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc @ 48] 
0a 0000008a`c97fd1b0 00007fff`c1493c9a     mojo_public_cpp_bindings!mojo::InterfaceEndpointClient::HandleIncomingMessage+0x375 [F:\Chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 751] 
0b 0000008a`c97fd370 00007fff`c14931a8     mojo_public_cpp_bindings!mojo::internal::MultiplexRouter::ProcessIncomingMessage+0x5ca [F:\Chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc @ 1120] 
0c 0000008a`c97fd4a0 00007fff`c148e189     mojo_public_cpp_bindings!mojo::internal::MultiplexRouter::Accept+0x1f8 [F:\Chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc @ 737] 
0d 0000008a`c97fd6f0 00007fff`c147861b     mojo_public_cpp_bindings!mojo::MessageDispatcher::Accept+0x139 [F:\Chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc @ 43] 
0e 0000008a`c97fd7a0 00007fff`c147926d     mojo_public_cpp_bindings!mojo::Connector::DispatchMessageW+0x38b [F:\Chromium\src\mojo\public\cpp\bindings\lib\connector.cc @ 561] 
0f 0000008a`c97fd930 00007fff`c1478ef7     mojo_public_cpp_bindings!mojo::Connector::ReadAllAvailableMessages+0x14d [F:\Chromium\src\mojo\public\cpp\bindings\lib\connector.cc @ 620] 
10 (Inline Function) --------`--------     mojo_public_cpp_bindings!mojo::Connector::OnHandleReadyInternal+0x2c [F:\Chromium\src\mojo\public\cpp\bindings\lib\connector.cc @ 452] 
11 0000008a`c97fd9e0 00007fff`c1479d8a     mojo_public_cpp_bindings!mojo::Connector::OnWatcherHandleReady+0x57 [F:\Chromium\src\mojo\public\cpp\bindings\lib\connector.cc @ 418] 
*** WARNING: Unable to verify checksum for D:\Chromium\dev_6876\Release\mojo_public_system_cpp.dll
12 0000008a`c97fda30 00007fff`56c1d002     mojo_public_cpp_bindings!base::RepeatingCallback<void (unsigned int)>::Run+0xaa [F:\Chromium\src\base\functional\callback.h @ 345] 
13 0000008a`c97fdac0 00007fff`56c1ce19     mojo_public_system_cpp!base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run+0xb2 [F:\Chromium\src\base\functional\callback.h @ 345] 
*** WARNING: Unable to verify checksum for D:\Chromium\dev_6876\Release\base.dll
14 0000008a`c97fdb50 00007fff`26601b64     mojo_public_system_cpp!mojo::SimpleWatcher::OnHandleReady+0x139 [F:\Chromium\src\mojo\public\cpp\system\simple_watcher.cc @ 279] 
15 0000008a`c97fdbf0 00007fff`266d5614     base!base::OnceCallback<void ()>::Run+0x94 [F:\Chromium\src\base\functional\callback.h @ 156] 
16 0000008a`c97fdc70 00007fff`2673a373     base!base::TaskAnnotator::RunTaskImpl+0x154 [F:\Chromium\src\base\task\common\task_annotator.cc @ 209] 
17 (Inline Function) --------`--------     base!base::TaskAnnotator::RunTask+0x54 [F:\Chromium\src\base\task\common\task_annotator.h @ 106] 
18 (Inline Function) --------`--------     base!base::internal::TaskTracker::RunTaskImpl+0x78 [F:\Chromium\src\base\task\thread_pool\task_tracker.cc @ 677] 
19 0000008a`c97fdd10 00007fff`267396e5     base!base::internal::TaskTracker::RunSkipOnShutdown+0xc3 [F:\Chromium\src\base\task\thread_pool\task_tracker.cc @ 662] 
1a (Inline Function) --------`--------     base!base::internal::TaskTracker::RunTaskWithShutdownBehavior+0x43 [F:\Chromium\src\base\task\thread_pool\task_tracker.cc @ 692] 
1b 0000008a`c97fddd0 00007fff`26738ea0     base!base::internal::TaskTracker::RunTask+0x495 [F:\Chromium\src\base\task\thread_pool\task_tracker.cc @ 520] 
1c 0000008a`c97ff770 00007fff`267481c1     base!base::internal::TaskTracker::RunAndPopNextTask+0x310 [F:\Chromium\src\base\task\thread_pool\task_tracker.cc @ 417] 
1d 0000008a`c97ffa20 00007fff`26747cd8     base!base::internal::WorkerThread::RunWorker+0x3c1 [F:\Chromium\src\base\task\thread_pool\worker_thread.cc @ 493] 
1e 0000008a`c97ffbd0 00007fff`267cbc47     base!base::internal::WorkerThread::RunSharedWorker+0x18 [F:\Chromium\src\base\task\thread_pool\worker_thread.cc @ 390] 
1f 0000008a`c97ffc10 00007ff8`0053e8d7     base!base::`anonymous namespace'::ThreadFunc+0xe7 [F:\Chromium\src\base\threading\platform_thread_win.cc @ 118] 
20 0000008a`c97ffc90 00007ff8`01d9fbcc     KERNEL32!BaseThreadInitThunk+0x17
21 0000008a`c97ffcc0 00000000`00000000     ntdll!RtlUserThreadStart+0x2c


```

### bl...@gmail.com (2025-01-26)

The \*.mojom.js files should be extracted from the corresponding chrome building outputs and placed in a folder named mojomjs, located in the same directory as the PoC file.

### aj...@google.com (2025-01-27)

This works with asan if you do the following (possibly not all switches are necessary, but I cannot get asan output if the sandbox is enabled):-

```
D:\chromium\src>d:\chromium\src\out\Asan\Chrome.exe \
 --enable-logging \
 --user-data-dir=d:\temp\asan-profile \
 --v=1 \
 --no-default-browser-check \
 --no-first-run \
 --ignore-certificate-errors \
 --disable-extensions \
 --no-sandbox \
 --enable-logging \
 --log-file=d:\temp\asan.log \
 --enable-blink-features=MojoJS,MojoJSTest \
 D:\pocs\gwar-392375312\poc.html

```
```
    #0 0x7fffc6cd7b1b  (d:\chromium\src\out\Asan\clang_rt.asan_dynamic-x86_64.dll+0x180047b1b)
    #1 0x7fff40ea7a2e in media::AudioBuffer::AudioBuffer(enum media::SampleFormat, enum media::ChannelLayout, int, int, int, bool, unsigned char const *const *, unsigned __int64, class base::TimeDelta, class scoped_refptr<class media::AudioBufferMemoryPool>) D:\chromium\src\media\base\audio_buffer.cc:204:9
    #2 0x7fff40eaae26 in media::AudioBuffer::CopyFrom(enum media::SampleFormat, enum media::ChannelLayout, int, int, int, unsigned char const *const *, class base::TimeDelta, class scoped_refptr<class media::AudioBufferMemoryPool>) D:\chromium\src\media\base\audio_buffer.cc:299:11
    #3 0x7fff4d18a798 in mojo::TypeConverter<class scoped_refptr<class media::AudioBuffer>, class mojo::StructPtr<class media::mojom::AudioBuffer>>::Convert(class mojo::StructPtr<class media::mojom::AudioBuffer> const &) D:\chromium\src\media\mojo\common\media_type_converters.cc:250:10
    #4 0x7fff68182af8 in media::MojoAudioEncoderService::Encode(class mojo::StructPtr<class media::mojom::AudioBuffer>, class base::OnceCallback<(class media::TypedStatus<struct media::EncoderStatusTraits> const &)>) D:\chromium\src\media\mojo\services\mojo_audio_encoder_service.cc:51:30
    #5 0x7fff40c700dd in media::mojom::AudioEncoderStubDispatch::AcceptWithResponder(class media::mojom::AudioEncoder *, class mojo::Message *, class std::__Cr::unique_ptr<class mojo::MessageReceiverWithStatus, struct std::__Cr::default_delete<class mojo::MessageReceiverWithStatus>>) D:\chromium\src\out\asan\gen\media\mojo\mojom\audio_encoder.mojom.cc:1005:13
    #6 0x7fff627430ea in media::mojom::AudioEncoderStub<struct mojo::UniquePtrImplRefTraits<class media::mojom::AudioEncoder, struct std::__Cr::default_delete<class media::mojom::AudioEncoder>>>::AcceptWithResponder(class mojo::Message *, class std::__Cr::unique_ptr<class mojo::MessageReceiverWithStatus, struct std::__Cr::default_delete<class mojo::MessageReceiverWithStatus>>) D:\chromium\src\out\asan\gen\media\mojo\mojom\audio_encoder.mojom.h:229:12
    #7 0x7fff545d47ff in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message *) D:\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1005:56
    #8 0x7fff5aa691a6 in mojo::MessageDispatcher::Accept(class mojo::Message *) D:\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:48:24
    #9 0x7fff545db1f4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message *) D:\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:724:20
    #10 0x7fff545ba07f in mojo::internal::MultiplexRouter::ProcessIncomingMessage(class mojo::internal::MultiplexRouter::MessageWrapper *, enum mojo::internal::MultiplexRouter::ClientCallBehavior, class base::SequencedTaskRunner *) D:\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1121:42
    #11 0x7fff545b7f68 in mojo::internal::MultiplexRouter::Accept(class mojo::Message *) D:\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:734:7
    #12 0x7fff5aa692b9 in mojo::MessageDispatcher::Accept(class mojo::Message *) D:\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43:19
    #13 0x7fff545f2760 in mojo::Connector::DispatchMessageW(class mojo::ScopedHandleBase<class mojo::MessageHandle>) D:\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:562:49
    #14 0x7fff545f4370 in mojo::Connector::ReadAllAvailableMessages(void) D:\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:620:14
    #15 0x7fff545f3d53 in mojo::Connector::OnWatcherHandleReady(char const *, unsigned int) D:\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:418:3
    #16 0x7fff545f5aa3 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl mojo::Connector::*const &)(char const *, unsigned int), class mojo::Connector *, char const *const &>, struct base::internal::BindState<1, 1, 0, void (__cdecl mojo::Connector::*)(char const *, unsigned int), class base::internal::UnretainedWrapper<class mojo::Connector, struct base::unretained_traits::MayNotDangle, 0>, class base::internal::UnretainedWrapper<char const, struct base::unretained_traits::MayNotDangle, 0>>, (unsigned int)>::Run(class base::internal::BindStateBase *, unsigned int) D:\chromium\src\base\functional\bind_internal.h:978:12
    #17 0x7fff43a06f43 in base::RepeatingCallback<(unsigned int)>::Run(unsigned int) const & D:\chromium\src\base\functional\callback.h:344:12
    #18 0x7fff43a06cd0 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl *const &)(class base::RepeatingCallback<(unsigned int)> const &, unsigned int, struct mojo::HandleSignalsState const &), class base::RepeatingCallback<void __cdecl(unsigned int)> const &>, struct base::internal::BindState<0, 1, 0, void (__cdecl *)(class base::RepeatingCallback<(unsigned int)> const &, unsigned int, struct mojo::HandleSignalsState const &), class base::RepeatingCallback<void __cdecl(unsigned int)>>, (unsigned int, struct mojo::HandleSignalsState const &)>::Run(class base::internal::BindStateBase *, unsigned int, struct mojo::HandleSignalsState const &) D:\chromium\src\base\functional\bind_internal.h:978:12
    #19 0x7fff54b8f93e in base::RepeatingCallback<(unsigned int, struct mojo::HandleSignalsState const &)>::Run(unsigned int, struct mojo::HandleSignalsState const &) const & D:\chromium\src\base\functional\callback.h:344:12
    #20 0x7fff54b8f2a5 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, struct mojo::HandleSignalsState const &) D:\chromium\src\mojo\public\cpp\system\simple_watcher.cc:278:14
    #21 0x7fff54b904a0 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl mojo::SimpleWatcher::*&&)(int, unsigned int, struct mojo::HandleSignalsState const &), class base::WeakPtr<class mojo::SimpleWatcher> &&, int &&, unsigned int &&, struct mojo::HandleSignalsState &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl mojo::SimpleWatcher::*)(int, unsigned int, struct mojo::HandleSignalsState const &), class base::WeakPtr<class mojo::SimpleWatcher>, int, unsigned int, struct mojo::HandleSignalsState>, (void)>::RunOnce(class base::internal::BindStateBase *) D:\chromium\src\base\functional\bind_internal.h:971:12
    #22 0x7fff547f0e31 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) D:\chromium\src\base\task\common\task_annotator.cc:210:34
    #23 0x7fff60ada2a6 in base::internal::TaskTracker::RunSkipOnShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::internal::SequenceToken const &) D:\chromium\src\base\task\thread_pool\task_tracker.cc:676:3
    #24 0x7fff60ad8486 in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraits const &) D:\chromium\src\base\task\thread_pool\task_tracker.cc:504:5
    #25 0x7fff60ad72bc in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) D:\chromium\src\base\task\thread_pool\task_tracker.cc:394:5
    #26 0x7fff66e19f93 in base::internal::WorkerThread::RunWorker(void) D:\chromium\src\base\task\thread_pool\worker_thread.cc:473:36
    #27 0x7fff66e18c45 in base::internal::WorkerThread::RunSharedWorker(void) D:\chromium\src\base\task\thread_pool\worker_thread.cc:369:3
    #28 0x7fff546d0617 in base::`anonymous namespace'::ThreadFunc D:\chromium\src\base\threading\platform_thread_win.cc:114:13
    #29 0x7fffc6ce992d  (d:\chromium\src\out\Asan\clang_rt.asan_dynamic-x86_64.dll+0x18005992d)
    #30 0x7ff821fe259c  (C:\WINDOWS\System32\KERNEL32.DLL+0x18001259c)
    #31 0x7ff8236aaf37  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005af37)

0x11efea564900 is located 0 bytes after 8192-byte region [0x11efea562900,0x11efea564900)
allocated by thread T35 here:
    #0 0x7fffc6cea0dd  (d:\chromium\src\out\Asan\clang_rt.asan_dynamic-x86_64.dll+0x18005a0dd)
    #1 0x7fff3df59cad in std::__Cr::vector<unsigned char, class std::__Cr::allocator<unsigned char>>::vector<unsigned char, class std::__Cr::allocator<unsigned char>>(unsigned __int64) D:\chromium\src\third_party\libc++\src\include\__vector\vector.h:143:7
    #2 0x7fff3e358274 in mojo::ArrayTraits<class std::__Cr::vector<unsigned char, class std::__Cr::allocator<unsigned char>>>::Resize(class std::__Cr::vector<unsigned char, class std::__Cr::allocator<unsigned char>> &, unsigned __int64) D:\chromium\src\mojo\public\cpp\bindings\array_traits.h:149:17
    #3 0x7fff3e357deb in mojo::internal::Serializer<class mojo::ArrayDataView<unsigned char>, class std::__Cr::vector<unsigned char, class std::__Cr::allocator<unsigned char>>>::Deserialize(class mojo::internal::Array_Data<unsigned char> *, class std::__Cr::vector<unsigned char, class std::__Cr::allocator<unsigned char>> *, class mojo::Message *) D:\chromium\src\mojo\public\cpp\bindings\lib\array_serialization.h:543:12
    #4 0x7fff40d0ce03 in mojo::StructTraits<class media::mojom::AudioBufferDataView, class mojo::StructPtr<class media::mojom::AudioBuffer>>::Read(class media::mojom::AudioBufferDataView, class mojo::StructPtr<class media::mojom::AudioBuffer> *) D:\chromium\src\out\asan\gen\media\mojo\mojom\media_types.mojom.cc:2770:29
    #5 0x7fff40c6fd66 in media::mojom::AudioEncoderStubDispatch::AcceptWithResponder(class media::mojom::AudioEncoder *, class mojo::Message *, class std::__Cr::unique_ptr<class mojo::MessageReceiverWithStatus, struct std::__Cr::default_delete<class mojo::MessageReceiverWithStatus>>) D:\chromium\src\out\asan\gen\media\mojo\mojom\audio_encoder.mojom.cc:991:39
    #6 0x7fff627430ea in media::mojom::AudioEncoderStub<struct mojo::UniquePtrImplRefTraits<class media::mojom::AudioEncoder, struct std::__Cr::default_delete<class media::mojom::AudioEncoder>>>::AcceptWithResponder(class mojo::Message *, class std::__Cr::unique_ptr<class mojo::MessageReceiverWithStatus, struct std::__Cr::default_delete<class mojo::MessageReceiverWithStatus>>) D:\chromium\src\out\asan\gen\media\mojo\mojom\audio_encoder.mojom.h:229:12
    #7 0x7fff545d47ff in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message *) D:\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1005:56
    #8 0x7fff5aa691a6 in mojo::MessageDispatcher::Accept(class mojo::Message *) D:\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:48:24
    #9 0x7fff545db1f4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message *) D:\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:724:20
    #10 0x7fff545ba07f in mojo::internal::MultiplexRouter::ProcessIncomingMessage(class mojo::internal::MultiplexRouter::MessageWrapper *, enum mojo::internal::MultiplexRouter::ClientCallBehavior, class base::SequencedTaskRunner *) D:\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1121:42
    #11 0x7fff545b7f68 in mojo::internal::MultiplexRouter::Accept(class mojo::Message *) D:\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:734:7
    #12 0x7fff5aa692b9 in mojo::MessageDispatcher::Accept(class mojo::Message *) D:\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43:19
    #13 0x7fff545f2760 in mojo::Connector::DispatchMessageW(class mojo::ScopedHandleBase<class mojo::MessageHandle>) D:\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:562:49
    #14 0x7fff545f4370 in mojo::Connector::ReadAllAvailableMessages(void) D:\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:620:14
    #15 0x7fff545f3d53 in mojo::Connector::OnWatcherHandleReady(char const *, unsigned int) D:\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:418:3
    #16 0x7fff545f5aa3 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl mojo::Connector::*const &)(char const *, unsigned int), class mojo::Connector *, char const *const &>, struct base::internal::BindState<1, 1, 0, void (__cdecl mojo::Connector::*)(char const *, unsigned int), class base::internal::UnretainedWrapper<class mojo::Connector, struct base::unretained_traits::MayNotDangle, 0>, class base::internal::UnretainedWrapper<char const, struct base::unretained_traits::MayNotDangle, 0>>, (unsigned int)>::Run(class base::internal::BindStateBase *, unsigned int) D:\chromium\src\base\functional\bind_internal.h:978:12
    #17 0x7fff43a06f43 in base::RepeatingCallback<(unsigned int)>::Run(unsigned int) const & D:\chromium\src\base\functional\callback.h:344:12
    #18 0x7fff43a06cd0 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl *const &)(class base::RepeatingCallback<(unsigned int)> const &, unsigned int, struct mojo::HandleSignalsState const &), class base::RepeatingCallback<void __cdecl(unsigned int)> const &>, struct base::internal::BindState<0, 1, 0, void (__cdecl *)(class base::RepeatingCallback<(unsigned int)> const &, unsigned int, struct mojo::HandleSignalsState const &), class base::RepeatingCallback<void __cdecl(unsigned int)>>, (unsigned int, struct mojo::HandleSignalsState const &)>::Run(class base::internal::BindStateBase *, unsigned int, struct mojo::HandleSignalsState const &) D:\chromium\src\base\functional\bind_internal.h:978:12
    #19 0x7fff54b8f93e in base::RepeatingCallback<(unsigned int, struct mojo::HandleSignalsState const &)>::Run(unsigned int, struct mojo::HandleSignalsState const &) const & D:\chromium\src\base\functional\callback.h:344:12
    #20 0x7fff54b8f2a5 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, struct mojo::HandleSignalsState const &) D:\chromium\src\mojo\public\cpp\system\simple_watcher.cc:278:14
    #21 0x7fff54b904a0 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl mojo::SimpleWatcher::*&&)(int, unsigned int, struct mojo::HandleSignalsState const &), class base::WeakPtr<class mojo::SimpleWatcher> &&, int &&, unsigned int &&, struct mojo::HandleSignalsState &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl mojo::SimpleWatcher::*)(int, unsigned int, struct mojo::HandleSignalsState const &), class base::WeakPtr<class mojo::SimpleWatcher>, int, unsigned int, struct mojo::HandleSignalsState>, (void)>::RunOnce(class base::internal::BindStateBase *) D:\chromium\src\base\functional\bind_internal.h:971:12
    #22 0x7fff547f0e31 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) D:\chromium\src\base\task\common\task_annotator.cc:210:34
    #23 0x7fff60ada2a6 in base::internal::TaskTracker::RunSkipOnShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::internal::SequenceToken const &) D:\chromium\src\base\task\thread_pool\task_tracker.cc:676:3
    #24 0x7fff60ad8486 in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraits const &) D:\chromium\src\base\task\thread_pool\task_tracker.cc:504:5
    #25 0x7fff60ad72bc in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) D:\chromium\src\base\task\thread_pool\task_tracker.cc:394:5
    #26 0x7fff66e19f93 in base::internal::WorkerThread::RunWorker(void) D:\chromium\src\base\task\thread_pool\worker_thread.cc:473:36
    #27 0x7fff66e18c45 in base::internal::WorkerThread::RunSharedWorker(void) D:\chromium\src\base\task\thread_pool\worker_thread.cc:369:3

Thread T35 created by T0 here:
    #0 0x7fffc6ce9842  (d:\chromium\src\out\Asan\clang_rt.asan_dynamic-x86_64.dll+0x180059842)
    #1 0x7fff546cf3a1 in base::`anonymous namespace'::CreateThreadInternal D:\chromium\src\base\threading\platform_thread_win.cc:182:7
    #2 0x7fff66e171b0 in base::internal::WorkerThread::Start(class scoped_refptr<class base::SingleThreadTaskRunner>, class base::WorkerThreadObserver *) D:\chromium\src\base\task\thread_pool\worker_thread.cc:185:3
    #3 0x7fff60ae4371 in base::internal::PooledSingleThreadTaskRunnerManager::CreateSingleThreadTaskRunner(class base::TaskTraits const &, enum base::SingleThreadTaskRunnerThreadMode) D:\chromium\src\base\task\thread_pool\pooled_single_thread_task_runner_manager.cc:685:10
    #4 0x7fff5aaf3cb9 in base::internal::ThreadPoolImpl::CreateSingleThreadTaskRunner(class base::TaskTraits const &, enum base::SingleThreadTaskRunnerThreadMode) D:\chromium\src\base\task\thread_pool\thread_pool_impl.cc:272:45
    #5 0x7fff547bbb9b in base::ThreadPool::CreateSingleThreadTaskRunner(class base::TaskTraits const &, enum base::SingleThreadTaskRunnerThreadMode) D:\chromium\src\base\task\thread_pool.cc:104:31
    #6 0x7fff662b71d5 in content::GpuServiceFactory::RunMediaService(class mojo::PendingReceiver<class media::mojom::MediaService>) D:\chromium\src\content\gpu\gpu_service_factory.cc:86:21
    #7 0x7fff662b87f3 in content::GpuChildThread::BindServiceInterface(class mojo::GenericPendingReceiver) D:\chromium\src\content\gpu\gpu_child_thread_receiver_bindings.cc:50:23
    #8 0x7fff593c7b8d in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl content::ChildThreadImpl::*&&)(class mojo::GenericPendingReceiver), class base::WeakPtr<class content::ChildThreadImpl> &&, class mojo::GenericPendingReceiver &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl content::ChildThreadImpl::*)(class mojo::GenericPendingReceiver), class base::WeakPtr<class content::ChildThreadImpl>, class mojo::GenericPendingReceiver>, (void)>::RunImpl<void (__cdecl content::ChildThreadImpl::*)(class mojo::GenericPendingReceiver), class std::__Cr::tuple<class base::WeakPtr<class content::ChildThreadImpl>, class mojo::GenericPendingReceiver>, 0, 1>(void (__cdecl content::ChildThreadImpl::*&&)(class mojo::GenericPendingReceiver), class std::__Cr::tuple<class base::WeakPtr<class content::ChildThreadImpl>, class mojo::GenericPendingReceiver> &&, struct std::__Cr::integer_sequence<unsigned __int64, 0, 1>) D:\chromium\src\base\functional\bind_internal.h:1058:14
    #9 0x7fff547f0e31 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) D:\chromium\src\base\task\common\task_annotator.cc:210:34
    #10 0x7fff5ab2ee4c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:470:23
    #11 0x7fff5ab2d65a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #12 0x7fff5ab848b2 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) D:\chromium\src\base\message_loop\message_pump_default.cc:42:55
    #13 0x7fff5ab30f02 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:643:12
    #14 0x7fff54886529 in base::RunLoop::Run(class base::Location const &) D:\chromium\src\base\run_loop.cc:134:14
    #15 0x7fff595ebaf8 in content::GpuMain(struct content::MainFunctionParams) D:\chromium\src\content\gpu\gpu_main.cc:452:14
    #16 0x7fff51b1ab08 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) D:\chromium\src\content\app\content_main_runner_impl.cc:773:14
    #17 0x7fff51b1dbc9 in content::ContentMainRunnerImpl::Run(void) D:\chromium\src\content\app\content_main_runner_impl.cc:1145:10
    #18 0x7fff51b0e6ba in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) D:\chromium\src\content\app\content_main.cc:348:36
    #19 0x7fff51b0eebe in content::ContentMain(struct content::ContentMainParams) D:\chromium\src\content\app\content_main.cc:361:10
    #20 0x7fff3dbf17bb in ChromeMain D:\chromium\src\chrome\app\chrome_main.cc:222:12
    #21 0x7ff66d294a0e in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) D:\chromium\src\chrome\app\main_dll_loader_win.cc:201:12
    #22 0x7ff66d2923dd in main D:\chromium\src\chrome\app\chrome_exe_main_win.cc:352:20
    #23 0x7ff66d9e31bb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #24 0x7ff821fe259c  (C:\WINDOWS\System32\KERNEL32.DLL+0x18001259c)
    #25 0x7ff8236aaf37  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005af37)

SUMMARY: AddressSanitizer: heap-buffer-overflow D:\chromium\src\media\base\audio_buffer.cc:204:9 in media::AudioBuffer::AudioBuffer(enum media::SampleFormat, enum media::ChannelLayout, int, int, int, bool, unsigned char const *const *, unsigned __int64, class base::TimeDelta, class scoped_refptr<class media::AudioBufferMemoryPool>)
Shadow bytes around the buggy address:
  0x11efea564680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11efea564700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11efea564780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11efea564800: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11efea564880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x11efea564900:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11efea564980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11efea564a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11efea564a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11efea564b00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11efea564b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==31700==ADDITIONAL INFO

==31700==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7fff54b8ffff in mojo::SimpleWatcher::Context::Notify(unsigned int, struct MojoHandleSignalsState, unsigned int) D:\chromium\src\mojo\public\cpp\system\simple_watcher.cc:102:13


Command line: `"d:\chromium\src\out\Asan\chrome.exe" --type=gpu-process --no-sandbox --user-data-dir="d:\temp\asan-profile" --no-pre-read-main-dll --start-stack-profiler --gpu-preferences=UAAAAAAAAADgAAAEAAAAAAAAAAAAAAAAAADAAAMAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --metrics-shmem-handle=1896,i,2324486555974272091,8979524588196226844,262144 --field-trial-handle=1956,i,5947329910558542678,18431343241337672840,262144 --variations-seed-version --enable-logging=handle --log-file=2152 --v=1 --mojo-platform-channel-handle=1948 /prefetch:2`


==31700==END OF ADDITIONAL INFO
==31700==ABORTING

```

### pe...@google.com (2025-01-28)

Setting milestone because of s2 severity.

### pe...@google.com (2025-01-28)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### tg...@google.com (2025-01-29)

I think the fix is relatively straightforward, but I am unable to repro the original issue with ASAN on Linux.

ajgo@, would you mind checking if the following patch fixes the issue?
<https://chromium-review.googlesource.com/c/chromium/src/+/6210759>

Please reassign to me if you can't.

### aj...@google.com (2025-01-29)

Yep - I'll start a build going.

### aj...@google.com (2025-01-29)

With the patch:-

```
[13480:12856:0128/180937.286:FATAL:audio_bus.cc(56)] Check failed: channels > 0 (0 vs. 0)
        base::debug::CollectStackTrace [0x00007FFF028B8A5A+58] (C:\src\chromium\src\base\debug\stack_trace_win.cc:326)
        base::debug::StackTrace::StackTrace [0x00007FFF06C92236+230] (C:\src\chromium\src\base\debug\stack_trace.cc:249)
        logging::LogMessage::Flush [0x00007FFF02A3C41E+1038] (C:\src\chromium\src\base\logging.cc:741)
        logging::LogMessage::~LogMessage [0x00007FFF02A3BEF7+55] (C:\src\chromium\src\base\logging.cc:730)
        logging::`anonymous namespace'::CheckLogMessage::~CheckLogMessage [0x00007FFF02A7DF63+179] (C:\src\chromium\src\base\check.cc:190)
        logging::NotReachedNoreturnError::~NotReachedNoreturnError [0x00007FFF02A7D8DB+11] (C:\src\chromium\src\base\check.cc:345)
        media::IsValidChannelCount [0x00007FFF03F8756D+493] (C:\src\chromium\src\media\base\audio_bus.cc:56)
        media::AudioBus::AudioBus [0x00007FFF03F87022+498] (C:\src\chromium\src\media\base\audio_bus.cc:72)
        media::AudioBus::Create [0x00007FFF03F88FF3+51] (C:\src\chromium\src\media\base\audio_bus.cc:133)
        media::AudioBuffer::WrapOrCopyToAudioBus [0x00007FFEF3F3EF41+929] (C:\src\chromium\src\media\base\audio_buffer.cc:461)
        media::MojoAudioEncoderService::Encode [0x00007FFF11EE2371+913] (C:\src\chromium\src\media\mojo\services\mojo_audio_encoder_service.cc:52)
        media::mojom::AudioEncoderStubDispatch::AcceptWithResponder [0x00007FFEF3D6F424+1636] (C:\src\chromium\src\out\asan\gen\media\mojo\mojom\audio_encoder.mojom.cc:1008)
        media::mojom::AudioEncoderStub<mojo::UniquePtrImplRefTraits<media::mojom::AudioEncoder,std::__Cr::default_delete<media::mojom::AudioEncoder> > >::AcceptWithResponder [0x00007FFF0DB3A1DD+269] (C:\src\chromium\src\out\asan\gen\media\mojo\mojom\audio_encoder.mojom.h:229)
        mojo::InterfaceEndpointClient::HandleValidatedMessage [0x00007FFF027A7C2F+2767] (C:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1005)
        mojo::MessageDispatcher::Accept [0x00007FFF079335DA+682] (C:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:48)
        mojo::InterfaceEndpointClient::HandleIncomingMessage [0x00007FFF027AD9BF+415] (C:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:724)
        mojo::internal::MultiplexRouter::ProcessIncomingMessage [0x00007FFF02794514+1956] (C:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1121)
        mojo::internal::MultiplexRouter::Accept [0x00007FFF02792968+1592] (C:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:734)
        mojo::MessageDispatcher::Accept [0x00007FFF079336BB+907] (C:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43)
        mojo::Connector::DispatchMessageW [0x00007FFF027C13D5+1157] (C:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:562)
        mojo::Connector::ReadAllAvailableMessages [0x00007FFF027C2E71+721] (C:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:620)
        mojo::Connector::OnWatcherHandleReady [0x00007FFF027C2898+232] (C:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:418)
        base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*const &)(const char *, unsigned int),mojo::Connector *,const char *const &>,base::internal::BindState<1,1,0,void (mojo::Connector::*)(const char *, unsigned int),base::internal: [0x00007FFF027C4224+452] (C:\src\chromium\src\base\functional\bind_internal.h:978)
        base::RepeatingCallback<void (unsigned int)>::Run [0x00007FFEF5E8CBFF+399] (C:\src\chromium\src\base\functional\callback.h:344)
        base::internal::Invoker<base::internal::FunctorTraits<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),const base::RepeatingCallback<void (unsigned int)> &>,base::internal::BindState<0,1 [0x00007FFEF5E8C9E0+272] (C:\src\chromium\src\base\functional\bind_internal.h:978)
        base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run [0x00007FFF02C2752E+414] (C:\src\chromium\src\base\functional\callback.h:344)
        mojo::SimpleWatcher::OnHandleReady [0x00007FFF02C26E21+1089] (C:\src\chromium\src\mojo\public\cpp\system\simple_watcher.cc:279)
        base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher> &&,int &&,unsigned int &&,mojo::HandleSignalsState &&>,base::internal::BindState< [0x00007FFF02C27F9B+459] (C:\src\chromium\src\base\functional\bind_internal.h:971)
        base::TaskAnnotator::RunTaskImpl [0x00007FFF02946A7D+973] (C:\src\chromium\src\base\task\common\task_annotator.cc:210)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFF079CA345+3157] (C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:470)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FFF079C909A+522] (C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330)
        base::MessagePumpDefault::Run [0x00007FFF07A0CB23+771] (C:\src\chromium\src\base\message_loop\message_pump_default.cc:42)
        base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FFF079CC033+1187] (C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:643)
        base::RunLoop::Run [0x00007FFF029A643F+1263] (C:\src\chromium\src\base\run_loop.cc:134)
        content::GpuMain [0x00007FFF069391CC+3404] (C:\src\chromium\src\content\gpu\gpu_main.cc:452)
        content::RunOtherNamedProcessTypeMain [0x00007FFF00742462+786] (C:\src\chromium\src\content\app\content_main_runner_impl.cc:773)
        content::ContentMainRunnerImpl::Run [0x00007FFF007446A1+1601] (C:\src\chromium\src\content\app\content_main_runner_impl.cc:1145)
        content::RunContentProcess [0x00007FFF007389A6+1190] (C:\src\chromium\src\content\app\content_main.cc:348)
        content::ContentMain [0x00007FFF0073954E+478] (C:\src\chromium\src\content\app\content_main.cc:361)
        ChromeMain [0x00007FFEF1921682+1554] (C:\src\chromium\src\chrome\app\chrome_main.cc:222)
        MainDllLoader::Launch [0x00007FF6F39A45EE+2382] (C:\src\chromium\src\chrome\app\main_dll_loader_win.cc:201)
        main [0x00007FF6F39A1FE5+3957] (C:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:352)
        __scrt_common_main_seh [0x00007FF6F3F9347C+268] (D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288)
        BaseThreadInitThunk [0x00007FFF9218259D+29]
        RtlUserThreadStart [0x00007FFF93F2AF38+40]
Task trace:
        mojo::SimpleWatcher::Context::Notify [0x00007FFF02C27B36+1110] (C:\src\chromium\src\mojo\public\cpp\system\simple_watcher.cc:102)

```

which is a safe crash - possibly as this is renderer reachable you want to not crash and a deserialization failure so the sending renderer is killed? But certainly the right place for the fix.

### aj...@google.com (2025-01-29)

That is, the fix works!

### tg...@google.com (2025-01-29)

Thank you Alex!

For the "safe crash", I followed what this file was already doing for other types of similar validations. We could return nullptr instead, check for it [here](https://source.chromium.org/chromium/chromium/src/+/main:media/mojo/services/mojo_audio_encoder_service.cc;l=52;drc=69ad3067faf616b1618b4b49a1cf7fccb171dac2), and explicitly close the mojo service.

### ap...@google.com (2025-01-30)

Project: chromium/src  

Branch: main  

Author: Thomas Guilbert <[tguilbert@chromium.org](mailto:tguilbert@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6210759>

Add mojom AudioBuffer data size checks

---


Expand for full commit details
```
Add mojom AudioBuffer data size checks 
 
See attached bug for details. 
 
Fixed: 392375312 
Change-Id: Ie70e603470b8c5cf1b8c12286169e2cb7fedc9d8 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6210759 
Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
Commit-Queue: Thomas Guilbert <tguilbert@chromium.org> 
Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1413238}

```

---

Files:

- M `media/mojo/common/media_type_converters.cc`

---

Hash: fccd12a6c506421818ae24afa19ac73b59c7732f  

Date:  Wed Jan 29 16:22:59 2025


---

### pe...@google.com (2025-01-30)

The NextAction date has arrived: 2025-01-30
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### sp...@google.com (2025-02-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of user information disclosure 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-06)

Congratulations Bl1nnnk and Pisanbao. Thank you for your efforts and reporting this issue to us!

### bl...@gmail.com (2025-02-06)

Thank you,

I would like to confirm whether this case qualifies for the "High Quality && High Impact [1]" category as described [here](https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules). The issue affects Android, where the GPU process is not sandboxed, and the PoC successfully demonstrates the leakage. Additionally, the example submission for this category also needs Mojo enabled: <https://issues.chromium.org/issues/40057994>

### am...@chromium.org (2025-02-06)

Hello, no this does not qualify for the `high quality && high impact` category.
This case is a read from a buffer with no attacker control of that value and falls into the special category described [in our policy here](https://g.co/chrome/vrp#memory-corruption-access-to-a-value-versus-the-potential-for-rce)

### ch...@google.com (2025-05-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/392375312)*
