# Heap UAF write in libyuv Convert8To16Row_Any_AVX2 via crafted raw VideoFrame input

| Field | Value |
|-------|-------|
| **Issue ID** | [491515787](https://issues.chromium.org/issues/491515787) |
| **Status** | Verified |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | Unknown |
| **Reporter** | sh...@gmail.com |
| **Created** | 2026-03-11 |
| **Bounty** | $7,000.00 |

## Description

# Note

This is the same issues as <https://issues.chromium.org/issues/488516881>, which got incorrectly closed. Its reproduced in <https://clusterfuzz.com/testcase?key=5670022819020800>, which you can see `==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x773c022c6440 at pc 0x5789c2ff30ae bp 0x746bf8394430 sp 0x746bf8393bf0` in the log but somehow Clusterfuzz didn't manage to recognize it.

## VULNERABILITY DETAILS

A WebCodecs VideoEncoder can be driven into a heap-use-after-free with a write primitive in the renderer process. The bug appears to be a lifetime/ownership error in the raw-frame conversion pipeline used by VideoEncoder. Attacker-controlled raw VideoFrame inputs are converted through libyuv (8-bit -> 10-bit path), and stale/freed memory is subsequently written during conversion. The failing write occurs in Convert8To16Row\_Any\_AVX2 while processing frame buffers derived from JS-supplied frame metadata and payloads (format/layout/stride/coded size/transfer behavior).

Crash log:

```
==217383==ERROR: AddressSanitizer: heap-use-after-free on address 0x7ea546140980 at pc 0x56334a039cfe bp 0x7b613739cf70 sp 0x7b613739c730
WRITE of size 44 at 0x7ea546140980 thread T4 (ThreadPoolForeg)
[217383:217383:0301/014040.337243:WARNING:media/base/video_frame_converter.cc:81] EncoderStatus::10 Data: {"dst":"format:PIXEL_FORMAT_I420 storage_type:OWNED_MEMORY coded_size:214x176 visible_rect:0,0 214x175 natural_size:214x175 timestamp:2600274 color_space: {primaries:INVALID, transfer:INVALID, matrix:INVALID, range:INVALID} hdr_metadata: {}","src":"format:PIXEL_FORMAT_YUV444P10 storage_type:OWNED_MEMORY coded_size:216x175 visible_rect:0,0 216x175 natural_size:216x175 timestamp:2600274 color_space: {primaries:BT709, transfer:BT709, matrix:BT709, range:LIMITED} hdr_metadata: {}"}
    #0 0x56334a039cfd in __asan_memcpy (/mnt/lvm_data/chromium/src/out/asan_dbg_symbols/chrome+0xf35acfd) (BuildId: 3afd3fb7d064a1b6)
    #1 0x7f667bb54faa in Convert8To16Row_Any_AVX2 third_party/libyuv/source/row_any.cc:1636:1
    #2 0x7f667bb23860 in Convert8To16Plane third_party/libyuv/source/planar_functions.cc:244:5
    #3 0x7f667bb0d7b3 in I420ToI010 third_party/libyuv/source/convert_from.cc:106:3
    #4 0x7f667aec2181 in media::VpxVideoEncoder::Encode(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>) media/video/vpx_video_encoder.cc:662:7
    #5 0x7f667ae2003b in void base::internal::DecayedFunctorTraits<void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&>::Invoke<void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>(void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*&&, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&) base/functional/bind_internal.h:740:12
    #6 0x7f667ae1fd74 in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&>, void, 0ul, 1ul, 2ul, 3ul>::MakeItSo<void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>>(void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>&&) base/functional/bind_internal.h:932:12
    #7 0x7f667ae1fa47 in void base::internal::Invoker<base::internal::FunctorTraits<void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&>, base::internal::BindState<true, true, false, void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>, void ()>::RunImpl<void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>, 0ul, 1ul, 2ul, 3ul>(void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/functional/bind_internal.h:1069:14
    #8 0x7f667ae1f878 in base::internal::Invoker<base::internal::FunctorTraits<void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&>, base::internal::BindState<true, true, false, void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:982:12
    #9 0x7f66af5d3112 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
    #10 0x7f66afaff12e in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:229:34
    #11 0x7f66afcec7d7 in void base::TaskAnnotator::RunTask<base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)::$_0>(perfetto::StaticString, base::PendingTask&, base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)::$_0&&) base/task/common/task_annotator.h:112:5
    #12 0x7f66afcec274 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:691:19
    #13 0x7f66afcec428 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:676:3
    #14 0x7f66afcea93d in base::internal::TaskTracker::RunTaskWithShutdownBehavior(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:706:7
    #15 0x7f66afce9a49 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType) base/task/thread_pool/task_tracker.cc:506:5
    #16 0x7f66afce8593 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:394:5
    #17 0x7f66afd3b243 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:473:36
    #18 0x7f66afd3a5ab in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #19 0x7f66afd39e25 in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #20 0x7f66afeac06c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #21 0x56334a039896 in asan_thread_start(void*) asan_interceptors.cpp

0x7ea546140980 is located 384 bytes inside of 123967-byte region [0x7ea546140800,0x7ea54615ec3f)
freed by thread T-1 here:
AddressSanitizer: CHECK failed: asan_descriptions.cpp:184 "((res.trace)) != (0)" (0x0, 0x0) (tid=217660)
    #0 0x56334a046d61 in __asan::CheckUnwind() asan_rtl.cpp
    #1 0x56334a061af2 in __sanitizer::CheckFailed(char const*, int, char const*, unsigned long long, unsigned long long) sanitizer_termination.cpp
    #2 0x563349fa50a3 in __asan::HeapAddressDescription::Print() const asan_descriptions.cpp
    #3 0x563349fa8167 in __asan::ErrorGeneric::Print() asan_errors.cpp
    #4 0x56334a04211f in __asan::ScopedInErrorReport::~ScopedInErrorReport() asan_report.cpp
    #5 0x56334a0444ac in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) asan_report.cpp
    #6 0x56334a039d30 in __asan_memcpy (/mnt/lvm_data/chromium/src/out/asan_dbg_symbols/chrome+0xf35ad30) (BuildId: 3afd3fb7d064a1b6)
    #7 0x7f667bb54faa in Convert8To16Row_Any_AVX2 third_party/libyuv/source/row_any.cc:1636:1
    #8 0x7f667bb23860 in Convert8To16Plane third_party/libyuv/source/planar_functions.cc:244:5
    #9 0x7f667bb0d7b3 in I420ToI010 third_party/libyuv/source/convert_from.cc:106:3
    #10 0x7f667aec2181 in media::VpxVideoEncoder::Encode(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>) media/video/vpx_video_encoder.cc:662:7
    #11 0x7f667ae2003b in void base::internal::DecayedFunctorTraits<void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&>::Invoke<void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>(void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*&&, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&) base/functional/bind_internal.h:740:12
    #12 0x7f667ae1fd74 in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&>, void, 0ul, 1ul, 2ul, 3ul>::MakeItSo<void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>>(void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>&&) base/functional/bind_internal.h:932:12
    #13 0x7f667ae1fa47 in void base::internal::Invoker<base::internal::FunctorTraits<void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&>, base::internal::BindState<true, true, false, void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>, void ()>::RunImpl<void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>, 0ul, 1ul, 2ul, 3ul>(void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/functional/bind_internal.h:1069:14
    #14 0x7f667ae1f878 in base::internal::Invoker<base::internal::FunctorTraits<void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&>, base::internal::BindState<true, true, false, void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:982:12
    #15 0x7f66af5d3112 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
    #16 0x7f66afaff12e in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:229:34
    #17 0x7f66afcec7d7 in void base::TaskAnnotator::RunTask<base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)::$_0>(perfetto::StaticString, base::PendingTask&, base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)::$_0&&) base/task/common/task_annotator.h:112:5
    #18 0x7f66afcec274 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:691:19
    #19 0x7f66afcec428 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:676:3
    #20 0x7f66afcea93d in base::internal::TaskTracker::RunTaskWithShutdownBehavior(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:706:7
    #21 0x7f66afce9a49 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType) base/task/thread_pool/task_tracker.cc:506:5
    #22 0x7f66afce8593 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:394:5
    #23 0x7f66afd3b243 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:473:36
    #24 0x7f66afd3a5ab in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #25 0x7f66afd39e25 in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #26 0x7f66afeac06c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #27 0x56334a039896 in asan_thread_start(void*) asan_interceptors.cpp
    #28 0x7f656e9d4ac2 in start_thread nptl/pthread_create.c:442:8
    #29 0x7f656ea668cf  misc/../sysdeps/unix/sysv/linux/x86_64/clone3.S:81


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==100280==END OF ADDITIONAL INFO

```
## VERSION

Chrome Version: 147.0.7703.0 (dev, ASan-instrumented Chromium build)

Operating System: Ubuntu 22.04.3 LTS (Jammy), x86\_64, kernel 5.15.0-151-generic

## REPRODUCTION CASE

PoC file:

- `highbd-fuzzer-1.html`

Opening it with --autoplay-policy=no-user-gesture-required flag directly can trigger the bug. Note that this flag is not required for this vulnerability, just for making PoC leading to crash more reliably.

```
ASAN_OPTIONS=detect_odr_violation=0 chrome --headless file:///highbd-fuzzer-1.html --autoplay-policy=no-user-gesture-required

```

Also attached `heap-spray-poc.html`, which is a poc for controlled write, but it is less reliable.

Type of crash: Renderer (tab) process memory corruption

## CREDIT INFORMATION

Reporter credit: heapracer (@heapracer)

## Attachments

- [highbd-fuzzer-1.html](attachments/highbd-fuzzer-1.html) (text/html, 13.2 KB)
- [heap-spray-poc.html](attachments/heap-spray-poc.html) (text/html, 7.7 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5880598220537856.

### th...@chromium.org (2026-03-11)

[security shepherd] Kicked off run for heap-spray-poc since it does not require a flag.

Reporter: If you're able to provide a stable POC that does not require a flag that would be helpful.

### 24...@project.gserviceaccount.com (2026-03-11)

Testcase 5880598220537856 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5880598220537856.

### sh...@gmail.com (2026-03-11)

Hi, that heap spray poc also needs --autoplay-policy=no-user-gesture-required, so that the video can auto play without any user interactions.

### cl...@appspot.gserviceaccount.com (2026-03-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6017607677280256.

### th...@chromium.org (2026-03-11)

Ah okay, I thought the first POC required it and the second less reliable one one didn't. I've uploaded to CF again but for the first POC (highbd-fuzzer-1.html) and with the flag. Thanks.

### 24...@project.gserviceaccount.com (2026-03-11)

Detailed Report: https://clusterfuzz.com/testcase?key=6017607677280256

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Ill
Crash Address: 0x5726aa7775be
Crash State:
  partition_alloc::internal::FreelistCorruptionDetected
  partition_alloc::internal::PartitionBucket::SlowPathAlloc
  void* partition_alloc::PartitionRoot::Alloc<
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1598026

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6017607677280256

Additional requirements: Requires HTTP

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### sh...@gmail.com (2026-03-11)

Not sure whats going on but this instance works: <https://clusterfuzz.com/testcase-detail/5670022819020800>

### th...@chromium.org (2026-03-12)

I can see that my first CF attempt <https://clusterfuzz.com/testcase?key=5880598220537856> also reproduced this but not consistently. However, that's not going to be very helpful for determining when this issue was introduced. I've just tried kicking off the same initial CF but with an M146 revision, though I'm not sure if I'm configuring the field appropriately (I used 76b7d80e5cda23fe6537eed26d68c92e995c7f39). If that can repro then I'll set the Found In to M146. If not, then I'm not sure.

I forgot to link this bug on the new CF run, but it's <https://clusterfuzz.com/testcase-detail/6132855339941888>

(Note: I also tried reproing manually on M146+7+8 on glinux with the flag + highbd-fuzzer-1.html and did not succeed.)

### th...@chromium.org (2026-03-12)

Reporter: Are you able to reproduce this on M146? M145?

### cl...@appspot.gserviceaccount.com (2026-03-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5758459953741824.

### th...@chromium.org (2026-03-13)

Okay I'm retrying CF but this time with revision 1582197 (corresponds to branch position for M146). Hopefully this one will be configured correctly. The one I kicked off in [#comment10](https://issues.chromium.org/issues/491515787#comment10) did repro but I'm pretty sure that was still trying M148.

### th...@chromium.org (2026-03-13)

Great, CF was able to repro on that revision (though not reliably), so I'll set the found in to extended stable M146.

mbonadei@: could you PTAL?

### ch...@google.com (2026-03-14)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-14)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### da...@chromium.org (2026-03-17)

Looked at this a bit tonight before running out of time:

- Output should be sized correctly by `RecreateVpxImageIfNeeded`, which is called here:
  
  - <https://source.chromium.org/chromium/chromium/src/+/main:media/video/vpx_video_encoder.cc;l=671;drc=8872cfcbeb584472c8f53db28966ee84da0b09b2>
- We DCHECK the frame size is as expected here:
  
  - <https://source.chromium.org/chromium/chromium/src/+/main:media/video/vpx_video_encoder.cc;l=636;drc=8872cfcbeb584472c8f53db28966ee84da0b09b2>
- Which should match what the `g_w` and `g_h` values are due to:
  
  - <https://source.chromium.org/chromium/chromium/src/+/main:media/video/vpx_video_encoder.cc;l=150;drc=8872cfcbeb584472c8f53db28966ee84da0b09b2>

I'll try to reproduce tomorrow and see what I can come up with. Two guesses:

- Maybe something is going wrong during `vpx_image_alloc`?
- Could really be a bug in libyuv wanting more padding on the planes than libvpx is using.

### eu...@chromium.org (2026-03-17)

1. First Frame (I420P10):
   
   - The PoC submits a video frame with the format PIXEL\_FORMAT\_YUV420P10 (10-bit YUV) and a specific size (e.g., 63x186).
   - In VpxVideoEncoder::Encode, this reaches the VP9PROFILE\_PROFILE2 case.
   - RecreateVpxImageIfNeeded(VPX\_IMG\_FMT\_I42016, /*needs\_memory=*/false) is called. Since vpx\_image\_ is uninitialized or has a different format/size, it allocates a
     wrapper (vpx\_img\_wrap) without allocating its own memory buffer.
   - SetupStandardYuvPlanes(\*frame, &vpx\_image\_) is called. This function takes the pointers to the actual plane data from the submitted VideoFrame (which is backed by
     external JavaScript ArrayBuffer memory) and stores them directly into vpx\_image\_.planes.
2. Detaching Memory (The Free):
   
   - The JavaScript PoC then explicitly detaches the ArrayBuffer that was backing the first video frame (by doing structuredClone with transferring).
   - This frees the backing memory. However, VpxVideoEncoder still holds a cached vpx\_image\_ object where vpx\_image\_.planes contains raw pointers to this now-freed memory.
3. Second Frame (I420):
   
   - The PoC then submits a second video frame with the format PIXEL\_FORMAT\_I420 (8-bit YUV) but the same dimensions.
   - In VpxVideoEncoder::Encode, it again hits the VP9PROFILE\_PROFILE2 case.
   - Because the input is 8-bit but the profile requires 10-bit, the encoder decides it needs to upsample the frame and allocate its own internal 16-bit memory buffer for
     libvpx to use.
   - It calls RecreateVpxImageIfNeeded(VPX\_IMG\_FMT\_I42016, /*needs\_memory=*/true).
   - The Bug: RecreateVpxImageIfNeeded checks if it needs to do anything:

```
        const bool has_changed = vpx_image_.fmt != fmt ||
                                 vpx_image_.d_w != codec_config_.g_w ||
                                 vpx_image_.d_h != codec_config_.g_h;

```

Because the format (VPX\_IMG\_FMT\_I42016) and dimensions haven't changed since the first frame, has\_changed evaluates to false, and the function returns early without
doing anything.
Crucially, it ignores the fact that needs\_memory transitioned from false to true.
\* The code then proceeds to copy and convert the 8-bit I420 frame into the 10-bit vpx\_image\_ buffers:

```
        libyuv::I420ToI010(...,
                           reinterpret_cast<uint16_t*>(planes[VPX_PLANE_Y]), ...);

```

- Since vpx\_image\_ was not recreated to allocate its own memory, planes still contains the dangling pointers from the first frame. libyuv::I420ToI010 writes the
  converted frame data directly into the freed JavaScript ArrayBuffer memory, triggering the AddressSanitizer use-after-free trap.
  
  Summary: The core issue is that RecreateVpxImageIfNeeded only checks if the dimensions or format changed, but it fails to check if the memory ownership model (needs\_memory)
  changed. When transitioning from needs\_memory=false (using pointers into external VideoFrame memory) to needs\_memory=true (requiring vpx\_image\_ to allocate its own internal
  buffer), it incorrectly bails out and writes data into dangling pointers.

### eu...@chromium.org (2026-03-17)

fix in progress: <https://chromium-review.googlesource.com/c/chromium/src/+/7670921>

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7670921>

media: Fix VpxVideoEncoder memory ownership bug

---


Expand for full commit details
```
     
    When encoding VP9 Profile 2 or 3, the encoder reuses its internal 
    image wrapper (`vpx_image_t`) between frames to save allocations. 
    However, it only checked if the format and dimensions changed. 
     
    If one frame provided external memory and the next frame required 
    the encoder to allocate its own buffer, the encoder would incorrectly 
    try to reuse the old external memory pointers. 
     
    This CL adds a check to ensure the image wrapper is recreated when 
    the memory ownership requirement changes between frames. 
     
    Bug: 491515787 
    Change-Id: If08d974edb10348a7fae18754788c0102e03c292 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7670921 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600950}

```

---

Files:

- M `media/video/software_video_encoder_test.cc`
- M `media/video/vpx_video_encoder.cc`
- M `media/video/vpx_video_encoder.h`

---

Hash: [46bc46aeb6740ddee2c122ad1f5045b12b37a83a](https://chromiumdash.appspot.com/commit/46bc46aeb6740ddee2c122ad1f5045b12b37a83a)  

Date: Wed Mar 18 01:48:13 2026


---

### ch...@google.com (2026-03-18)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1600950) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1600950) appears to be after beta branch point (1596535).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-19)

Merge review required: M147 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-19)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### eu...@chromium.org (2026-03-19)

> Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/7670921>

> Has this fix been verified on Canary to not pose any stability regressions?

yes

> Does this fix pose any potential non-verifiable stability risks?

no

> Does this fix pose any known compatibility risks?

no

> Does it require manual verification by the test team? If so, please describe required testing.

yes, use open `heap-spray-poc.html` from the report and see if it crashes

### dr...@chromium.org (2026-03-20)

No crashes in Canary. Approved to merge to M146 and M147.

### dx...@google.com (2026-03-23)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7694114>

[M147] media: Fix VpxVideoEncoder memory ownership bug

---


Expand for full commit details
```
     
    When encoding VP9 Profile 2 or 3, the encoder reuses its internal 
    image wrapper (`vpx_image_t`) between frames to save allocations. 
    However, it only checked if the format and dimensions changed. 
     
    If one frame provided external memory and the next frame required 
    the encoder to allocate its own buffer, the encoder would incorrectly 
    try to reuse the old external memory pointers. 
     
    This CL adds a check to ensure the image wrapper is recreated when 
    the memory ownership requirement changes between frames. 
     
    (cherry picked from commit 46bc46aeb6740ddee2c122ad1f5045b12b37a83a) 
     
    Bug: 491515787 
    Change-Id: If08d974edb10348a7fae18754788c0102e03c292 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7670921 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1600950} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7694114 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1294} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `media/video/software_video_encoder_test.cc`
- M `media/video/vpx_video_encoder.cc`
- M `media/video/vpx_video_encoder.h`

---

Hash: [c27a8c35deabfe4d40ac94427deb87ca5912b0ac](https://chromiumdash.appspot.com/commit/c27a8c35deabfe4d40ac94427deb87ca5912b0ac)  

Date: Mon Mar 23 22:26:02 2026


---

### pe...@google.com (2026-03-23)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7693915>

[M146] media: Fix VpxVideoEncoder memory ownership bug

---


Expand for full commit details
```
     
    When encoding VP9 Profile 2 or 3, the encoder reuses its internal 
    image wrapper (`vpx_image_t`) between frames to save allocations. 
    However, it only checked if the format and dimensions changed. 
     
    If one frame provided external memory and the next frame required 
    the encoder to allocate its own buffer, the encoder would incorrectly 
    try to reuse the old external memory pointers. 
     
    This CL adds a check to ensure the image wrapper is recreated when 
    the memory ownership requirement changes between frames. 
     
    (cherry picked from commit 46bc46aeb6740ddee2c122ad1f5045b12b37a83a) 
     
    Bug: 491515787 
    Change-Id: If08d974edb10348a7fae18754788c0102e03c292 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7670921 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1600950} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7693915 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3095} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `media/video/software_video_encoder_test.cc`
- M `media/video/vpx_video_encoder.cc`
- M `media/video/vpx_video_encoder.h`

---

Hash: [d1b3967efbbc1ecc29aae2e28689f107e267c8f4](https://chromiumdash.appspot.com/commit/d1b3967efbbc1ecc29aae2e28689f107e267c8f4)  

Date: Tue Mar 24 00:09:52 2026


---

### pe...@google.com (2026-03-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-03-31)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7710435>
2. Low - there were no conflicts
3. 146 and 147
4. Yes

### an...@google.com (2026-03-31)

Merge approved for LTS-138

### dx...@google.com (2026-04-06)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7710435>

[M138-LTS] media: Fix VpxVideoEncoder memory ownership bug

---


Expand for full commit details
```
     
    When encoding VP9 Profile 2 or 3, the encoder reuses its internal 
    image wrapper (`vpx_image_t`) between frames to save allocations. 
    However, it only checked if the format and dimensions changed. 
     
    If one frame provided external memory and the next frame required 
    the encoder to allocate its own buffer, the encoder would incorrectly 
    try to reuse the old external memory pointers. 
     
    This CL adds a check to ensure the image wrapper is recreated when 
    the memory ownership requirement changes between frames. 
     
    Bug: 491515787 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7670921 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600950} 
    (cherry picked from commit 46bc46aeb6740ddee2c122ad1f5045b12b37a83a) 
     
    Change-Id: I56177cbec8d7ccd188576aeea4723ffa26ae1af6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7710435 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3521} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `media/video/software_video_encoder_test.cc`
- M `media/video/vpx_video_encoder.cc`
- M `media/video/vpx_video_encoder.h`

---

Hash: [49de955485441fe9caa9fd2e9bef2c16fe65f2af](https://chromiumdash.appspot.com/commit/49de955485441fe9caa9fd2e9bef2c16fe65f2af)  

Date: Mon Apr 6 12:39:25 2026


---

### pe...@google.com (2026-04-15)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-04-16)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7764148>
2. Low - no conflicts
3. 138, 146 and 147
4. Yes

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Baseline. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-05-04)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7764148>

[M144-LTS] media: Fix VpxVideoEncoder memory ownership bug

---


Expand for full commit details
```
     
    When encoding VP9 Profile 2 or 3, the encoder reuses its internal 
    image wrapper (`vpx_image_t`) between frames to save allocations. 
    However, it only checked if the format and dimensions changed. 
     
    If one frame provided external memory and the next frame required 
    the encoder to allocate its own buffer, the encoder would incorrectly 
    try to reuse the old external memory pointers. 
     
    This CL adds a check to ensure the image wrapper is recreated when 
    the memory ownership requirement changes between frames. 
     
    Bug: 491515787 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7670921 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600950} 
    (cherry picked from commit 46bc46aeb6740ddee2c122ad1f5045b12b37a83a) 
     
    Change-Id: Id6248b634f6248d5e3f58c6cf84bb938262f9ea5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7764148 
    Reviewed-by: Achuith Bhandarkar <achuith@chromium.org> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Owners-Override: Achuith Bhandarkar <achuith@chromium.org> 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4846} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `media/video/software_video_encoder_test.cc`
- M `media/video/vpx_video_encoder.cc`
- M `media/video/vpx_video_encoder.h`

---

Hash: [e27fb6aeca7050fb04e993ebe6e2b7ce15a57230](https://chromiumdash.appspot.com/commit/e27fb6aeca7050fb04e993ebe6e2b7ce15a57230)  

Date: Mon May 4 16:39:39 2026


---

### ch...@google.com (2026-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline. Renderer RCE / memory corruption in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491515787)*
