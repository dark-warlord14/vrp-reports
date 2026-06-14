# heap-buffer-overflow write in libaom

| Field | Value |
|-------|-------|
| **Issue ID** | [339877165](https://issues.chromium.org/issues/339877165) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | jz...@google.com |
| **Created** | 2024-05-11 |
| **Bounty** | $7,000.00 |

## Description

heap-buffer-overflow write in libaom
tested os:ubuntu 22.04
tested chrome:
Chromium 126.0.6461.0
Chromium 119.0.6041.0

repro steps:
./chrome --disable-gpu --use-fake-ui-for-media-stream --use-fake-device-for-media-stream --incognito --user-data-dir=/tmp/xxs http://localhost:8880/crash.html

The buffer overflow will repro immediately.

==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x52e0000befe0 at pc 0x653bb5d6c90d bp 0x789085bb7c10 sp 0x789085bb7c08
WRITE of size 4 at 0x52e0000befe0 thread T75 (CodecWorker)
    #0 0x653bb5d6c90c in fill_variance ./../../third_party/libaom/source/libaom/av1/encoder/var_based_part.c:103:23
    #1 0x653bb5d6c90c in fill_variance_4x4avg ./../../third_party/libaom/source/libaom/av1/encoder/var_based_part.c:420:5
    #2 0x653bb5d6c90c in fill_variance_tree_leaves ./../../third_party/libaom/source/libaom/av1/encoder/var_based_part.c:1166:13
    #3 0x653bb5d6c90c in av1_choose_var_based_partitioning ./../../third_party/libaom/source/libaom/av1/encoder/var_based_part.c:1744:3
    #4 0x653bb5b05112 in encode_nonrd_sb ./../../third_party/libaom/source/libaom/av1/encoder/encodeframe.c:555:5
    #5 0x653bb5b05112 in encode_sb_row ./../../third_party/libaom/source/libaom/av1/encoder/encodeframe.c:1246:7
    #6 0x653bb5b05112 in av1_encode_sb_row ./../../third_party/libaom/source/libaom/av1/encoder/encodeframe.c:1435:3
    #7 0x653bb5bc3223 in enc_row_mt_worker_hook ./../../third_party/libaom/source/libaom/av1/encoder/ethread.c:721:5
    #8 0x653ba3058319 in Execute ./../../media/base/codec_worker_impl.h:58:29
    #9 0x653ba3058319 in media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::ExecuteOnTaskRunner(AVxWorker*) ./../../media/base/codec_worker_impl.h:102:5
    #10 0x653ba3058a44 in Invoke<void (media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::*)(AVxWorker *), media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2> *, AVxWorker *> ./../../base/functional/bind_internal.h:738:12
    #11 0x653ba3058a44 in MakeItSo<void (media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::*)(AVxWorker *), std::__Cr::tuple<base::internal::UnretainedWrapper<media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<AVxWorker, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:930:12
    #12 0x653ba3058a44 in void base::internal::Invoker<base::internal::FunctorTraits<void (media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::*&&)(AVxWorker*), media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>*, AVxWorker*>, base::internal::BindState<true, true, false, void (media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::*)(AVxWorker*), base::internal::UnretainedWrapper<media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<AVxWorker, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::*)(AVxWorker*), std::__Cr::tuple<base::internal::UnretainedWrapper<media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<AVxWorker, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul, 1ul>(void (media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::*&&)(AVxWorker*), std::__Cr::tuple<base::internal::UnretainedWrapper<media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<AVxWorker, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) ./../../base/functional/bind_internal.h:1067:14
    #13 0x653bb27b2ec4 in Run ./../../base/functional/callback.h:156:12
    #14 0x653bb27b2ec4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #15 0x653bb2814676 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:90:5
    #16 0x653bb2814676 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #17 0x653bb281358d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:40
    #18 0x653bb28153ba in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #19 0x653bb26abd2d in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #20 0x653bb2816026 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:645:12
    #21 0x653bb274577f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #22 0x653bb28973ec in base::Thread::Run(base::RunLoop*) ./../../base/threading/thread.cc:338:13
    #23 0x653bb289794e in base::Thread::ThreadMain() ./../../base/threading/thread.cc:410:3
    #24 0x653bb28e0797 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:101:13
    #25 0x653ba04541b6 in asan_thread_start(void*) _asan_rtl_:28

0x52e0000befe0 is located 313 bytes after 43687-byte region [0x52e0000b4400,0x52e0000beea7)
allocated by thread T2 (ThreadPoolForeg) here:
    #0 0x653ba045678f in __interceptor_malloc _asan_rtl_:3
    #1 0x653bb5a0cbe9 in aom_memalign ./../../third_party/libaom/source/libaom/aom_mem/aom_mem.c:59:22
    #2 0x653bb5a0cbe9 in aom_malloc ./../../third_party/libaom/source/libaom/aom_mem/aom_mem.c:67:40
    #3 0x653bb5bb3afa in av1_init_tile_thread_data ./../../third_party/libaom/source/libaom/av1/encoder/ethread.c:1052:11
    #4 0x653bb5a5b47b in encoder_encode ./../../third_party/libaom/source/libaom/av1/av1_cx_iface.c:3233:7
    #5 0x653bb5a4b712 in aom_codec_encode ./../../third_party/libaom/source/libaom/aom/src/aom_encoder.c:191:11
    #6 0x653bc54d33b2 in webrtc::(anonymous namespace)::LibaomAv1Encoder::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/modules/video_coding/codecs/av1/libaom_av1_encoder.cc:700:9
    #7 0x653bc551c16c in webrtc::SimulcastEncoderAdapter::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/media/engine/simulcast_encoder_adapter.cc:546:33
    #8 0x653bb5382be4 in webrtc::VideoStreamEncoder::EncodeVideoFrame(webrtc::VideoFrame const&, long) ./../../third_party/webrtc/video/video_stream_encoder.cc:2030:43
    #9 0x653bb5380246 in webrtc::VideoStreamEncoder::MaybeEncodeVideoFrame(webrtc::VideoFrame const&, long) ./../../third_party/webrtc/video/video_stream_encoder.cc:1875:3
    #10 0x653bb537cb24 in webrtc::VideoStreamEncoder::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&) ./../../third_party/webrtc/video/video_stream_encoder.cc:1565:5
    #11 0x653bb534a513 in OnFrameOnMainQueue ./../../third_party/webrtc/video/frame_cadence_adapter.cc:997:26
    #12 0x653bb534a513 in operator() ./../../third_party/webrtc/video/frame_cadence_adapter.cc:965:5
    #13 0x653bb534a513 in __invoke<(lambda at ../../third_party/webrtc/video/frame_cadence_adapter.cc:951:45)> ./../../third_party/libc++/src/include/__type_traits/invoke.h:150:25
    #14 0x653bb534a513 in invoke<(lambda at ../../third_party/webrtc/video/frame_cadence_adapter.cc:951:45)> ./../../third_party/libc++/src/include/__functional/invoke.h:28:10
    #15 0x653bb534a513 in InvokeR<void, (lambda at ../../third_party/webrtc/video/frame_cadence_adapter.cc:951:45), void> ./../../third_party/abseil-cpp/absl/functional/internal/any_invocable.h:132:3
    #16 0x653bb534a513 in void absl::internal_any_invocable::RemoteInvoker<false, void, webrtc::(anonymous namespace)::FrameCadenceAdapterImpl::OnFrame(webrtc::VideoFrame const&)::$_1&&>(absl::internal_any_invocable::TypeErasedState*) ./../../third_party/abseil-cpp/absl/functional/internal/any_invocable.h:368:10
    #17 0x653ba1c7cbc8 in operator() ./../../third_party/abseil-cpp/absl/functional/internal/any_invocable.h:876:1
    #18 0x653ba1c7cbc8 in blink::WebRtcTaskQueue::RunTask(absl::AnyInvocable<void () &&>) ./../../third_party/webrtc_overrides/task_queue_factory.cc:100:5
    #19 0x653ba1c7e517 in Invoke<void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue *, absl::AnyInvocable<void () &&> > ./../../base/functional/bind_internal.h:738:12
    #20 0x653ba1c7e517 in MakeItSo<void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), std::__Cr::tuple<base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&> > > ./../../base/functional/bind_internal.h:930:12
    #21 0x653ba1c7e517 in RunImpl<void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), std::__Cr::tuple<base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:1067:14
    #22 0x653ba1c7e517 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WebRtcTaskQueue::*&&)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue*, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #23 0x653bb27b2ec4 in Run ./../../base/functional/callback.h:156:12
    #24 0x653bb27b2ec4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #25 0x653bb283519b in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:680:35)> ./../../base/task/common/task_annotator.h:90:5
    #26 0x653bb283519b in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:679:19
    #27 0x653bb28353ec in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:664:3
    #28 0x653bb28346f5 in RunTaskWithShutdownBehavior ./../../base/task/thread_pool/task_tracker.cc:694:7
    #29 0x653bb28346f5 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) ./../../base/task/thread_pool/task_tracker.cc:521:5
    #30 0x653bb2833784 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread_pool/task_tracker.cc:416:5
    #31 0x653bb28732b0 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread_pool/worker_thread.cc:438:36
    #32 0x653bb2872357 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread_pool/worker_thread.cc:322:3
    #33 0x653bb2871e20 in base::internal::WorkerThread::ThreadMain() ./../../base/task/thread_pool/worker_thread.cc:302:7
    #34 0x653bb28e0797 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:101:13
    #35 0x653ba04541b6 in asan_thread_start(void*) _asan_rtl_:28

Thread T75 (CodecWorker) created by T2 (ThreadPoolForeg) here:
    #0 0x653ba043c051 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x653bb28dfcf0 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:146:13
    #2 0x653bb2896703 in base::Thread::StartWithOptions(base::Thread::Options) ./../../base/threading/thread.cc:211:26
    #3 0x653bb2896018 in base::Thread::Start() ./../../base/threading/thread.cc:169:10
    #4 0x653ba305788b in media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::CodecWorkerImpl() ./../../media/base/codec_worker_impl.h:43:13
    #5 0x653ba30572da in media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::Reset(AVxWorker*) ./../../media/base/codec_worker_impl.h:124:57
    #6 0x653bb5bb4491 in av1_create_workers ./../../third_party/libaom/source/libaom/av1/encoder/ethread.c:1104:12
    #7 0x653bb5a5b441 in encoder_encode ./../../third_party/libaom/source/libaom/av1/av1_cx_iface.c:3232:7
    #8 0x653bb5a4b712 in aom_codec_encode ./../../third_party/libaom/source/libaom/aom/src/aom_encoder.c:191:11
    #9 0x653bc54d33b2 in webrtc::(anonymous namespace)::LibaomAv1Encoder::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/modules/video_coding/codecs/av1/libaom_av1_encoder.cc:700:9
    #10 0x653bc551c16c in webrtc::SimulcastEncoderAdapter::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/media/engine/simulcast_encoder_adapter.cc:546:33
    #11 0x653bb5382be4 in webrtc::VideoStreamEncoder::EncodeVideoFrame(webrtc::VideoFrame const&, long) ./../../third_party/webrtc/video/video_stream_encoder.cc:2030:43
    #12 0x653bb5380246 in webrtc::VideoStreamEncoder::MaybeEncodeVideoFrame(webrtc::VideoFrame const&, long) ./../../third_party/webrtc/video/video_stream_encoder.cc:1875:3
    #13 0x653bb537cb24 in webrtc::VideoStreamEncoder::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&) ./../../third_party/webrtc/video/video_stream_encoder.cc:1565:5
    #14 0x653bb534a513 in OnFrameOnMainQueue ./../../third_party/webrtc/video/frame_cadence_adapter.cc:997:26
    #15 0x653bb534a513 in operator() ./../../third_party/webrtc/video/frame_cadence_adapter.cc:965:5
    #16 0x653bb534a513 in __invoke<(lambda at ../../third_party/webrtc/video/frame_cadence_adapter.cc:951:45)> ./../../third_party/libc++/src/include/__type_traits/invoke.h:150:25
    #17 0x653bb534a513 in invoke<(lambda at ../../third_party/webrtc/video/frame_cadence_adapter.cc:951:45)> ./../../third_party/libc++/src/include/__functional/invoke.h:28:10
    #18 0x653bb534a513 in InvokeR<void, (lambda at ../../third_party/webrtc/video/frame_cadence_adapter.cc:951:45), void> ./../../third_party/abseil-cpp/absl/functional/internal/any_invocable.h:132:3
    #19 0x653bb534a513 in void absl::internal_any_invocable::RemoteInvoker<false, void, webrtc::(anonymous namespace)::FrameCadenceAdapterImpl::OnFrame(webrtc::VideoFrame const&)::$_1&&>(absl::internal_any_invocable::TypeErasedState*) ./../../third_party/abseil-cpp/absl/functional/internal/any_invocable.h:368:10
    #20 0x653ba1c7cbc8 in operator() ./../../third_party/abseil-cpp/absl/functional/internal/any_invocable.h:876:1
    #21 0x653ba1c7cbc8 in blink::WebRtcTaskQueue::RunTask(absl::AnyInvocable<void () &&>) ./../../third_party/webrtc_overrides/task_queue_factory.cc:100:5
    #22 0x653ba1c7e517 in Invoke<void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue *, absl::AnyInvocable<void () &&> > ./../../base/functional/bind_internal.h:738:12
    #23 0x653ba1c7e517 in MakeItSo<void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), std::__Cr::tuple<base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&> > > ./../../base/functional/bind_internal.h:930:12
    #24 0x653ba1c7e517 in RunImpl<void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), std::__Cr::tuple<base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:1067:14
    #25 0x653ba1c7e517 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WebRtcTaskQueue::*&&)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue*, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #26 0x653bb27b2ec4 in Run ./../../base/functional/callback.h:156:12
    #27 0x653bb27b2ec4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #28 0x653bb283519b in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:680:35)> ./../../base/task/common/task_annotator.h:90:5
    #29 0x653bb283519b in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:679:19
    #30 0x653bb28353ec in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:664:3
    #31 0x653bb28346f5 in RunTaskWithShutdownBehavior ./../../base/task/thread_pool/task_tracker.cc:694:7
    #32 0x653bb28346f5 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) ./../../base/task/thread_pool/task_tracker.cc:521:5
    #33 0x653bb2833784 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread_pool/task_tracker.cc:416:5
    #34 0x653bb28732b0 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread_pool/worker_thread.cc:438:36
    #35 0x653bb2872357 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread_pool/worker_thread.cc:322:3
    #36 0x653bb2871e20 in base::internal::WorkerThread::ThreadMain() ./../../base/task/thread_pool/worker_thread.cc:302:7
    #37 0x653bb28e0797 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:101:13
    #38 0x653ba04541b6 in asan_thread_start(void*) _asan_rtl_:28

Thread T2 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x653ba043c051 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x653bb28dfcf0 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:146:13
    #2 0x653bb287124a in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) ./../../base/task/thread_pool/worker_thread.cc:199:3
    #3 0x653bb2837a1f in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() ./../../base/task/thread_pool/thread_group.cc:110:13
    #4 0x653bb283751f in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() ./../../base/task/thread_pool/thread_group.cc:85:3
    #5 0x653bb2868422 in ~SemaphoreScopedCommandsExecutor ./../../base/task/thread_pool/thread_group_semaphore.cc:48:3
    #6 0x653bb2868422 in base::internal::ThreadGroupSemaphore::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>) ./../../base/task/thread_pool/thread_group_semaphore.cc:153:1
    #7 0x653bb2847fe4 in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*) ./../../base/task/thread_pool/thread_pool_impl.cc:243:35
    #8 0x653bbe10ad07 in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) ./../../content/child/child_process.cc:118:20
    #9 0x653bc9b9161b in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) ./../../content/renderer/render_process.cc:18:7
    #10 0x653bc9b90caf in content::RenderProcessImpl::RenderProcessImpl() ./../../content/renderer/render_process_impl.cc:112:7
    #11 0x653bc9b912e0 in content::RenderProcessImpl::Create() ./../../content/renderer/render_process_impl.cc:223:31
    #12 0x653bc9c1c5cc in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:296:53
    #13 0x653bafe74269 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:685:14
    #14 0x653bafe757be in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:789:12
    #15 0x653bafe78351 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1156:10
    #16 0x653bafe72580 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:332:36
    #17 0x653bafe72c0b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:345:10
    #18 0x653ba048f408 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #19 0x79a13e829d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/pwn11/asan-linux-release/chrome+0x243cc90c) (BuildId: 8fbb97da385e0340)
Shadow bytes around the buggy address:
  0x52e0000bed00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x52e0000bed80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x52e0000bee00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x52e0000bee80: 00 00 00 00 07 fa fa fa fa fa fa fa fa fa fa fa
  0x52e0000bef00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x52e0000bef80: fa fa fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa
  0x52e0000bf000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x52e0000bf080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x52e0000bf100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x52e0000bf180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x52e0000bf200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==1==ADDITIONAL INFO

==1==Note: Please include this section with the ASan report.
Task trace:
    #0 0x653ba3057e1a in media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::ChangeStateImpl(AVxWorker*, AVxWorkerStatus) ./../../media/base/codec_worker_impl.h:91:11
    #1 0x653bb5341bf3 in webrtc::(anonymous namespace)::FrameCadenceAdapterImpl::OnFrame(webrtc::VideoFrame const&) ./../../third_party/webrtc/video/frame_cadence_adapter.cc:951:11
    #2 0x653bc587e0a5 in blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter::OnVideoFrameOnIO(scoped_refptr<media::VideoFrame>, base::TimeTicks) ./../../third_party/blink/renderer/modules/peerconnection/media_stream_video_webrtc_sink.cc:172:46


==1==END OF ADDITIONAL INFO
==1==ABORTING


## Attachments

- [crash.html](attachments/crash.html) (text/html, 1.9 KB)
- [asan.log](attachments/asan.log) (text/plain, 25.0 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-05-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5296310866345984.

### 24...@project.gserviceaccount.com (2024-05-11)

Testcase 5296310866345984 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5296310866345984.

### ad...@google.com (2024-05-12)

Reporter, ClusterFuzz was unable to reproduce this. On Monday I'll try locally but if you can spot anything which might mean I'll also struggle to reproduce this, please let me know.

### em...@gmail.com (2024-05-12)

I'm not sure why CF can't reproduce the issue. The reproduction method provided above should be sufficient. On my local pc, it reproduces within seconds (reproduces reliably on Ubuntu and occasionally on my Mac.).
If you encounter any issues while testing locally, please let me know.

Thanks.

### ad...@google.com (2024-05-13)

I also can't reproduce locally. With the M124 downloaded ASAN build I'm using (1274542), I see:

```
[7644:11:0513/125024.675679:ERROR:rtp_transceiver.cc(81)] Invalid codec preferences: invalid codec with name "AV1". (INVALID_MODIFICATION)

```

I don't see any such messages from the Canary build I'm using (1299854), but I see no crashes.

This is in a VM based on Ubuntu 22.04 as well. Could you let me know where you downloaded the Chromium Linux build where you could reproduce this?

### em...@gmail.com (2024-05-13)

Both my self-compiled version and the version downloaded from gs://chromium-browser-asan can stably reproduce the issue on my local machine.

I noticed that the original PoC does not reproduce consistently on some machines, so I will look into improving the PoC.

Recently tested new version:
Chromium 126.0.6478.0:
Download command: gsutil cp gs://chromium-browser-asan/linux-release/asan-linux-release-1300036.zip .

### ad...@google.com (2024-05-13)

Thanks - I'll have a crack at reproducing with that specific build tomorrow.

### em...@gmail.com (2024-05-13)

I modified the PoC by changing this line. I'm not sure if it will reproduce on the VM in CF, but it should stably reproduce on physical Linux and Mac machines.
let stream = await navigator.mediaDevices.getDisplayMedia({
                video: { width: { max: 1920 } },
            });

I encountered an upload error. You can directly modify this line in the original PoC.

### cl...@appspot.gserviceaccount.com (2024-05-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6001311433555968.

### ad...@google.com (2024-05-14)

Unable to reproduce on a Mac with the modified POC and canary build 1300313. Trying again on Linux with the specific build in [#comment9](https://issues.chromium.org/issues/339877165#comment9).

### ad...@google.com (2024-05-14)

I still can't reproduce on Ubuntu 22.04 with asan-linux-release-1300036.zip, though this is a VM.

I have been able to reproduce this (or something similar) on a physical Mac, with build 1300313.

```
=================================================================
==43072==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x62e0000a6fe0 at pc 0x0001652fe3a6 bp 0x700013697bd0 sp 0x700013697bc8
WRITE of size 4 at 0x62e0000a6fe0 thread T20
==43072==WARNING: invalid path to external symbolizer!
==43072==WARNING: Failed to use and restart external symbolizer!
::1 - - [14/May/2024 08:59:49] "GET /poc-339877165-modified.html HTTP/1.1" 304 -
    #0 0x1652fe3a5 in av1_choose_var_based_partitioning+0xb4b5 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x135543a5)
    #1 0x1650b9cf4 in av1_encode_sb_row+0x35f4 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1330fcf4)
    #2 0x16516b654 in enc_row_mt_worker_hook+0x1184 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x133c1654)
    #3 0x154299ced in media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::ExecuteOnTaskRunner(AVxWorker*)+0x17d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x24efced)
    #4 0x15429a40c in void base::internal::Invoker<base::internal::FunctorTraits<void (media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::*&&)(AVxWorker*), media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>*, AVxWorker*>, base::internal::BindState<true, true, false, void (media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::*)(AVxWorker*), base::internal::UnretainedWrapper<media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<AVxWorker, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::*)(AVxWorker*), std::__Cr::tuple<base::internal::UnretainedWrapper<media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<AVxWorker, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul, 1ul>(void (media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::*&&)(AVxWorker*), std::__Cr::tuple<base::internal::UnretainedWrapper<media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<AVxWorker, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>)+0x28c (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x24f040c)
    #5 0x16216f33e in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x39e (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x103c533e)
    #6 0x1621cef4d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0xb7d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10424f4d)
    #7 0x1621cdfa0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x190 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10423fa0)
    #8 0x1621cfcf4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x14 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10425cf4)
    #9 0x16207cdc8 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1e8 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x102d2dc8)
    #10 0x1621d0926 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x496 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10426926)
    #11 0x16210ed9e in base::RunLoop::Run(base::Location const&)+0x53e (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10364d9e)
    #12 0x16224a1a9 in base::Thread::Run(base::RunLoop*)+0xd9 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104a01a9)
    #13 0x16224a6eb in base::Thread::ThreadMain()+0x4db (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104a06eb)
    #14 0x16228e09b in base::(anonymous namespace)::ThreadFunc(void*)+0x13b (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104e409b)
    #15 0x106314586 in __sanitizer_weak_hook_memcmp+0x342f6 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x50586)
    #16 0x7ff807af318a in _pthread_start+0x62 (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x618a)
    #17 0x7ff807aeeae2 in thread_start+0xe (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x1ae2)

0x62e0000a6fe0 is located 313 bytes after 43687-byte region [0x62e00009c400,0x62e0000a6ea7)
allocated by thread T17 here:
    #0 0x1063177d2 in __asan_memmove+0x2be2 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x537d2)
    #1 0x164fc793b in aom_malloc+0x1b (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1321d93b)
    #2 0x16515c98a in av1_init_tile_thread_data+0xb9a (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x133b298a)
    #3 0x165017595 in encoder_encode+0x1de5 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1326d595)
    #4 0x165003846 in aom_codec_encode+0x1e6 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x13259846)
    #5 0x173245b7e in webrtc::(anonymous namespace)::LibaomAv1Encoder::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*)+0x21ae (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x2149bb7e)
    #6 0x1731d572d in webrtc::SimulcastEncoderAdapter::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*)+0xc5d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x2142b72d)
    #7 0x1649c4586 in webrtc::VideoStreamEncoder::EncodeVideoFrame(webrtc::VideoFrame const&, long long)+0x1876 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x12c1a586)
    #8 0x1649c1afa in webrtc::VideoStreamEncoder::MaybeEncodeVideoFrame(webrtc::VideoFrame const&, long long)+0x18ea (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x12c17afa)
    #9 0x1649be6ca in webrtc::VideoStreamEncoder::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&)+0x80a (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x12c146ca)
    #10 0x16495cf6a in void absl::internal_any_invocable::RemoteInvoker<false, void, webrtc::(anonymous namespace)::FrameCadenceAdapterImpl::OnFrame(webrtc::VideoFrame const&)::$_1&&>(absl::internal_any_invocable::TypeErasedState*)+0x36a (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x12bb2f6a)
    #11 0x1533450bc in blink::WebRtcTaskQueue::RunTask(absl::AnyInvocable<void () &&>)+0x12c (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x159b0bc)
    #12 0x1533469a8 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WebRtcTaskQueue::*&&)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue*, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1f8 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x159c9a8)
    #13 0x16216f33e in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x39e (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x103c533e)
    #14 0x1621ed5e4 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x254 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104435e4)
    #15 0x1621ed83d in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xdd (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1044383d)
    #16 0x1621ecbb3 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&)+0x463 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10442bb3)
    #17 0x1621ebe41 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x641 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10441e41)
    #18 0x1622292c8 in base::internal::WorkerThread::RunWorker()+0xc08 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1047f2c8)
    #19 0x16222840b in base::internal::WorkerThread::RunPooledWorker()+0xab (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1047e40b)
    #20 0x162227e55 in base::internal::WorkerThread::ThreadMain()+0x1e5 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1047de55)
    #21 0x16228e09b in base::(anonymous namespace)::ThreadFunc(void*)+0x13b (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104e409b)
    #22 0x106314586 in __sanitizer_weak_hook_memcmp+0x342f6 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x50586)
    #23 0x7ff807af318a in _pthread_start+0x62 (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x618a)
    #24 0x7ff807aeeae2 in thread_start+0xe (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x1ae2)

Thread T20 created by T17 here:
    #0 0x10630f31d in __sanitizer_weak_hook_memcmp+0x2f08d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x4b31d)
    #1 0x16228d6e7 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x2e7 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104e36e7)
    #2 0x162249507 in base::Thread::StartWithOptions(base::Thread::Options)+0x527 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1049f507)
    #3 0x162248e73 in base::Thread::Start()+0x1a3 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1049ee73)
    #4 0x15429929f in media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::CodecWorkerImpl()+0x12f (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x24ef29f)
    #5 0x154298e0a in media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::Reset(AVxWorker*)+0x1fa (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x24eee0a)
    #6 0x16515d2fd in av1_create_workers+0x33d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x133b32fd)
    #7 0x16501756a in encoder_encode+0x1dba (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1326d56a)
    #8 0x165003846 in aom_codec_encode+0x1e6 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x13259846)
    #9 0x173245b7e in webrtc::(anonymous namespace)::LibaomAv1Encoder::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*)+0x21ae (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x2149bb7e)
    #10 0x1731d572d in webrtc::SimulcastEncoderAdapter::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*)+0xc5d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x2142b72d)
    #11 0x1649c4586 in webrtc::VideoStreamEncoder::EncodeVideoFrame(webrtc::VideoFrame const&, long long)+0x1876 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x12c1a586)
    #12 0x1649c1afa in webrtc::VideoStreamEncoder::MaybeEncodeVideoFrame(webrtc::VideoFrame const&, long long)+0x18ea (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x12c17afa)
    #13 0x1649be6ca in webrtc::VideoStreamEncoder::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&)+0x80a (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x12c146ca)
    #14 0x16495cf6a in void absl::internal_any_invocable::RemoteInvoker<false, void, webrtc::(anonymous namespace)::FrameCadenceAdapterImpl::OnFrame(webrtc::VideoFrame const&)::$_1&&>(absl::internal_any_invocable::TypeErasedState*)+0x36a (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x12bb2f6a)
    #15 0x1533450bc in blink::WebRtcTaskQueue::RunTask(absl::AnyInvocable<void () &&>)+0x12c (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x159b0bc)
    #16 0x1533469a8 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WebRtcTaskQueue::*&&)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue*, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1f8 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x159c9a8)
    #17 0x16216f33e in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x39e (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x103c533e)
    #18 0x1621ed5e4 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x254 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104435e4)
    #19 0x1621ed83d in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xdd (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1044383d)
    #20 0x1621ecbb3 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&)+0x463 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10442bb3)
    #21 0x1621ebe41 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x641 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10441e41)
    #22 0x1622292c8 in base::internal::WorkerThread::RunWorker()+0xc08 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1047f2c8)
    #23 0x16222840b in base::internal::WorkerThread::RunPooledWorker()+0xab (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1047e40b)
    #24 0x162227e55 in base::internal::WorkerThread::ThreadMain()+0x1e5 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1047de55)
    #25 0x16228e09b in base::(anonymous namespace)::ThreadFunc(void*)+0x13b (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104e409b)
    #26 0x106314586 in __sanitizer_weak_hook_memcmp+0x342f6 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x50586)
    #27 0x7ff807af318a in _pthread_start+0x62 (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x618a)
    #28 0x7ff807aeeae2 in thread_start+0xe (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x1ae2)

Thread T17 created by T15 here:
    #0 0x10630f31d in __sanitizer_weak_hook_memcmp+0x2f08d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x4b31d)
    #1 0x16228d6e7 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x2e7 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104e36e7)
    #2 0x162227477 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x577 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1047d477)
    #3 0x1621f37e7 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x5c7 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104497e7)
    #4 0x1621f30a2 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x42 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104490a2)
    #5 0x162209730 in base::internal::ThreadGroupSemaphore::PushTaskSourceAndWakeUpWorkers(base::internal::RegisteredTaskSourceAndTransaction)+0x2e0 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1045f730)
    #6 0x162222fe0 in base::internal::ThreadPoolImpl::PostTaskWithSequenceNow(base::internal::Task, scoped_refptr<base::internal::Sequence>)+0x430 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10478fe0)
    #7 0x162223825 in base::internal::ThreadPoolImpl::PostTaskWithSequence(base::internal::Task, scoped_refptr<base::internal::Sequence>)+0x5c5 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10479825)
    #8 0x162214e77 in base::internal::PooledSequencedTaskRunner::PostDelayedTask(base::Location const&, base::OnceCallback<void ()>, base::TimeDelta)+0x2f7 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1046ae77)
    #9 0x1621e2aaa in base::TaskRunner::PostTask(base::Location const&, base::OnceCallback<void ()>)+0x13a (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10438aaa)
    #10 0x1533454ac in blink::WebRtcTaskQueue::PostTaskImpl(absl::AnyInvocable<void () &&>, webrtc::TaskQueueBase::PostTaskTraits const&, base::Location const&)+0x2cc (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x159b4ac)
    #11 0x164955045 in webrtc::(anonymous namespace)::FrameCadenceAdapterImpl::OnFrame(webrtc::VideoFrame const&)+0x3e5 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x12bab045)
    #12 0x165775c74 in rtc::VideoBroadcaster::OnFrame(webrtc::VideoFrame const&)+0x6d4 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x139cbc74)
    #13 0x17352d6a8 in rtc::AdaptedVideoTrackSource::OnFrame(webrtc::VideoFrame const&)+0x378 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x217836a8)
    #14 0x17353194d in blink::WebRtcVideoTrackSource::DeliverFrame(scoped_refptr<media::VideoFrame>, gfx::Rect*, long long, std::__Cr::optional<webrtc::Timestamp>, std::__Cr::optional<webrtc::Timestamp>)+0xa4d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x2178794d)
    #15 0x17352fdcb in blink::WebRtcVideoTrackSource::OnFrameCaptured(scoped_refptr<media::VideoFrame>)+0x139b (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x21785dcb)
    #16 0x1735331dc in blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter::OnVideoFrameOnNetworkThread(scoped_refptr<media::VideoFrame>)+0x15c (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x217891dc)
    #17 0x173537ac1 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter::*&&)(scoped_refptr<media::VideoFrame>), scoped_refptr<blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter>&&, scoped_refptr<media::VideoFrame>&&>, base::internal::BindState<true, true, false, void (blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter::*)(scoped_refptr<media::VideoFrame>), scoped_refptr<blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter>, scoped_refptr<media::VideoFrame>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1a1 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x2178dac1)
    #18 0x16216f33e in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x39e (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x103c533e)
    #19 0x1621cef4d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0xb7d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10424f4d)
    #20 0x1621cdfa0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x190 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10423fa0)
    #21 0x1621cfcf4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x14 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10425cf4)
    #22 0x16207cdc8 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1e8 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x102d2dc8)
    #23 0x1621d0926 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x496 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10426926)
    #24 0x16210ed9e in base::RunLoop::Run(base::Location const&)+0x53e (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10364d9e)
    #25 0x16224a1a9 in base::Thread::Run(base::RunLoop*)+0xd9 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104a01a9)
    #26 0x16224a6eb in base::Thread::ThreadMain()+0x4db (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104a06eb)
    #27 0x16228e09b in base::(anonymous namespace)::ThreadFunc(void*)+0x13b (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104e409b)
    #28 0x106314586 in __sanitizer_weak_hook_memcmp+0x342f6 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x50586)
    #29 0x7ff807af318a in _pthread_start+0x62 (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x618a)
    #30 0x7ff807aeeae2 in thread_start+0xe (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x1ae2)

Thread T15 created by T0 here:
    #0 0x10630f31d in __sanitizer_weak_hook_memcmp+0x2f08d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x4b31d)
    #1 0x16228d6e7 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x2e7 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104e36e7)
    #2 0x162249507 in base::Thread::StartWithOptions(base::Thread::Options)+0x527 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1049f507)
    #3 0x173321910 in blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory()+0x530 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x21577910)
    #4 0x173321304 in blink::PeerConnectionDependencyFactory::GetPcFactory()+0xd4 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x21577304)
    #5 0x173329cdb in blink::PeerConnectionDependencyFactory::CreatePeerConnection(webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, webrtc::PeerConnectionObserver*, blink::ExceptionState&)+0x13b (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x2157fcdb)
    #6 0x1733fe0c9 in blink::RTCPeerConnectionHandler::Initialize(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration const&, blink::WebLocalFrame*, blink::ExceptionState&)+0x669 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x216540c9)
    #7 0x1733b7ca8 in blink::RTCPeerConnection::RTCPeerConnection(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::ExceptionState&)+0x918 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x2160dca8)
    #8 0x1733b7218 in blink::RTCPeerConnection* blink::MakeGarbageCollected<blink::RTCPeerConnection, blink::ExecutionContext*&, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::ExceptionState&>(blink::ExecutionContext*&, webrtc::PeerConnectionInterface::RTCConfiguration&&, bool&&, blink::ExceptionState&)+0x1a8 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x2160d218)
    #9 0x1733b3554 in blink::RTCPeerConnection::Create(blink::ExecutionContext*, blink::RTCConfiguration const*, blink::ExceptionState&)+0x684 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x21609554)
    #10 0x171a55ddd in blink::(anonymous namespace)::v8_rtc_peer_connection::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&)+0x86d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x1fcabddd)
    #11 0x1565e6982 in v8::internal::FunctionCallbackArguments::Call(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>)+0x5e2 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x483c982)
    #12 0x1565e4c4e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, unsigned long*, int)+0x4de (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x483ac4e)
    #13 0x1565e2e82 in v8::internal::Builtin_Impl_HandleApiConstruct(v8::internal::BuiltinArguments, v8::internal::Isolate*)+0x1c2 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x4838e82)
    #14 0x159e512f5 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit+0x35 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x80a72f5)
    #15 0x159db2f0e in construct_stub_invoke_deopt_addr+0xf5 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x8008f0e)
    #16 0x159f46713 in Builtins_ConstructHandler+0x353 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x819c713)
    #17 0x159db2226 in Builtins_InterpreterEntryTrampoline+0x126 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x8008226)
    #18 0x159df29f5 in Builtins_AsyncFunctionAwaitResolveClosure+0x35 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x80489f5)
    #19 0x159ecf2ad in Builtins_PromiseFulfillReactionJob+0x2d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x81252ad)
    #20 0x159de1c3a in Builtins_RunMicrotasks+0x2ba (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x8037c3a)
    #21 0x159dafbde in Builtins_JSRunMicrotasksEntry+0x9e (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x8005bde)
    #22 0x15693c1a7 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)+0xfa7 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x4b921a7)
    #23 0x15693f6ab in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)+0x13b (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x4b956ab)
    #24 0x15693fac0 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*)+0x50 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x4b95ac0)
    #25 0x1569ca534 in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*)+0x494 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x4c20534)
    #26 0x1569cb875 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate*)+0x175 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x4c21875)
    #27 0x15ea6300e in blink::scheduler::EventLoop::PerformMicrotaskCheckpoint()+0x21e (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0xccb900e)
    #28 0x15ea94c4f in blink::scheduler::AgentGroupSchedulerImpl::PerformMicrotaskCheckpoint()+0x59f (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0xcceac4f)
    #29 0x15ead7e5f in blink::scheduler::MainThreadSchedulerImpl::PerformMicrotaskCheckpoint()+0x69f (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0xcd2de5f)
    #30 0x15eaebb23 in blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr<blink::scheduler::MainThreadTaskQueue>, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)+0x1b3 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0xcd41b23)
    #31 0x15eb0d03f in blink::scheduler::MainThreadTaskQueue::OnTaskCompleted(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)+0x1bf (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0xcd6303f)
    #32 0x15eb100f1 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::* const&)(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*), blink::scheduler::MainThreadTaskQueue*>, base::internal::BindState<true, true, false, void (blink::scheduler::MainThreadTaskQueue::*)(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*), base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::internal::BindStateBase*, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)+0x161 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0xcd660f1)
    #33 0x1621ace0e in base::RepeatingCallback<void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) const &+0x19e (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10402e0e)
    #34 0x162188009 in base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask*, base::LazyNow*)+0x2a9 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x103de009)
    #35 0x162187c35 in base::sequence_manager::internal::SequenceManagerImpl::DidRunTask(base::LazyNow&)+0x145 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x103ddc35)
    #36 0x1621cf0e9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0xd19 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x104250e9)
    #37 0x1621cdfa0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x190 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10423fa0)
    #38 0x1621cfcf4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x14 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10425cf4)
    #39 0x16207cdc8 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1e8 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x102d2dc8)
    #40 0x1621d0926 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x496 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10426926)
    #41 0x16210ed9e in base::RunLoop::Run(base::Location const&)+0x53e (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x10364d9e)
    #42 0x177429928 in content::RendererMain(content::MainFunctionParams)+0x998 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x2567f928)
    #43 0x15fa4072a in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x28a (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0xdc9672a)
    #44 0x15fa4283d in content::ContentMainRunnerImpl::Run()+0x66d (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0xdc9883d)
    #45 0x15fa3e6c9 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x739 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0xdc946c9)
    #46 0x15fa3f11c in content::ContentMain(content::ContentMainParams)+0x1cc (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0xdc9511c)
    #47 0x151daf44c in ChromeMain+0x3cc (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x544c)
    #48 0x105a60d40 in main+0x260 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):x86_64+0x100000d40)
    #49 0x7ff807767365 in start+0x795 (/usr/lib/dyld:x86_64+0xfffffffffff5c365)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x135543a5) in av1_choose_var_based_partitioning+0xb4b5
Shadow bytes around the buggy address:
  0x62e0000a6d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x62e0000a6d80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x62e0000a6e00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x62e0000a6e80: 00 00 00 00 07 fa fa fa fa fa fa fa fa fa fa fa
  0x62e0000a6f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x62e0000a6f80: fa fa fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa
  0x62e0000a7000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x62e0000a7080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x62e0000a7100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x62e0000a7180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x62e0000a7200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==43072==ADDITIONAL INFO

==43072==Note: Please include this section with the ASan report.
Task trace:
    #0 0x1542997d7 in media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::ChangeStateImpl(AVxWorker*, AVxWorkerStatus)+0x4d7 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x24ef7d7)
    #1 0x164954fce in webrtc::(anonymous namespace)::FrameCadenceAdapterImpl::OnFrame(webrtc::VideoFrame const&)+0x36e (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x12baafce)
    #2 0x1735323e2 in blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter::OnVideoFrameOnIO(scoped_refptr<media::VideoFrame>, base::TimeTicks)+0x132 (/Users/adetaylor/dev/fetchchromium/Canary-126/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6478.0/Chromium Framework:x86_64+0x217883e2)


==43072==END OF ADDITIONAL INFO
==43072==ABORTING
Received signal 6

```

### ad...@google.com (2024-05-14)

Setting S1 for renderer memory corruption. Although this would require the user to interact with the media selection dialog, that's something a user does all the time, so I don't think it counts as the ["unusual" user interaction required to lower severity by one level](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md).

I'll figure out impacted FoundIn versions shortly.

### ad...@google.com (2024-05-14)

The command line which worked for me on Mac was `./Chromium.app/Contents/MacOS/Chromium --use-fake-ui-for-media-stream --use-fake-device-for-media-stream http://localhost:8003/poc-339877165-modified.html`. I didn't end up using `--incognito` or `--user-data-dir`.

On M124 on OS X, I see `Invalid codec preferences: invalid codec with name "AV1"` and the POC doesn't trigger.

With beta M125 1287749, I hit the same buffer overflow as in [#comment12](https://issues.chromium.org/issues/339877165#comment12). So I'm labeling this FoundIn-125.

### pe...@google.com (2024-05-14)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-14)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### wt...@google.com (2024-05-14)

James is looking at this bug.

### jz...@google.com (2024-05-15)

There looks to be some confusion in the code around the superblock size in use. Wan-Teh helped identify a fix related to <https://aomedia-review.googlesource.com/c/aom/+/171941>. I'm getting a change together now.

### jz...@google.com (2024-05-15)

There's some subtlety to the code, but a change should land soon.

### ap...@google.com (2024-05-16)

Project: aom
Branch: main

commit e42f4b1980bbbc772aa886d8b43a885461d7b89e
Author: James Zern <jzern@google.com>
Date:   Tue May 14 17:54:10 2024

    update codec config after svc/scale controls
    
    This ensures the encoder state/allocations stay in sync with scaling and
    svc layer changes. In the SVC case, depending on the resolution,
    differences in the chosen superblock size among layers may have caused a
    crash. This was reproducible in WebRTC in screen content mode.
    
    The fix is based on a change by Yuan Tong (tongyuan200097) [1]. It
    refreshes the encoder config after AOME_SET_SCALEMODE,
    AOME_SET_NUMBER_SPATIAL_LAYERS and AV1E_SET_SVC_PARAMS if no frames have
    been encoded. AV1E_SET_SVC_PARAMS was missed in the original change.
    
    [1]: https://aomedia-review.googlesource.com/c/aom/+/171941/2
    
    Bug: chromium:339877165
    Change-Id: Ib3d2a123b159898d7c7e19c81e89ff148920e1f1

M       av1/av1_cx_iface.c

https://aomedia-review.googlesource.com/190181


### ap...@google.com (2024-05-17)

Project: aom
Branch: main

commit 01467cdbd524900eed283660836179fd1b2cd536
Author: James Zern <jzern@google.com>
Date:   Thu May 16 13:44:52 2024

    encode_api_test: add repro for chromium 339877165
    
    BUG=chromium:339877165
    
    Change-Id: I69dcc2cda098ec96a34e1e5f7ef557ee8caf5521

M       test/encode_api_test.cc

https://aomedia-review.googlesource.com/190261


### ap...@google.com (2024-05-17)

Project: chromium/src
Branch: main

commit cb5651248b18ef54aa60d6cfbb17dcf1feae7538
Author: James Zern <jzern@chromium.org>
Date:   Fri May 17 01:05:24 2024

    Roll src/third_party/libaom/source/libaom/ 8f107273c..0f766c110 (3 commits)
    
    https://aomedia.googlesource.com/aom.git/+log/8f107273cc64..0f766c1101fa
    
    $ git log 8f107273c..0f766c110 --date=short --no-merges --format='%ad %ae %s'
    2024-05-16 jzern disable av1_resize_horz_dir_sse2
    2024-05-14 jzern update codec config after svc/scale controls
    2024-05-15 marpan rtc: Refactor speed features for prune palette
    
    Created with:
      roll-dep src/third_party/libaom/source/libaom
    
    Bug: b:307414544, 339877165
    Change-Id: I3ab7fe7e467f78d154edd27cbdb63e491aa1bb9d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5545036
    Commit-Queue: James Zern <jzern@google.com>
    Reviewed-by: Wan-Teh Chang <wtc@google.com>
    Cr-Commit-Position: refs/heads/main@{#1302353}

M       DEPS
M       third_party/libaom/README.chromium
M       third_party/libaom/source/config/config/aom_version.h
M       third_party/libaom/source/config/linux/ia32/config/av1_rtcd.h
M       third_party/libaom/source/config/linux/x64/config/av1_rtcd.h
M       third_party/libaom/source/config/win/ia32/config/av1_rtcd.h
M       third_party/libaom/source/config/win/x64/config/av1_rtcd.h
M       third_party/libaom/source/libaom

https://chromium-review.googlesource.com/5545036


### jz...@google.com (2024-05-17)

Note one of the contributing factors to this case was from [January 2023](https://aomedia-review.googlesource.com/c/aom/+/169388). There may still have been cases like this prior to that change, however. This means we should extend the merge request back a few versions and consider LTS.

### pe...@google.com (2024-05-17)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-05-17)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### jz...@google.com (2024-05-17)

> Please answer the following questions so that we can safely process your merge request:
> 
> 1. Why does your merge fit within the merge criteria for these milestones?
> 
> - Chrome Browser: <https://chromiumdash.appspot.com/branches>
> - Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

Heap overflow in libaom accessible via WebRTC (and likely WebCodecs).

> 2. What changes specifically would you like to merge? Please link to Gerrit.

- <https://aomedia-review.git.corp.google.com/c/aom/+/190181>
- <https://aomedia-review.git.corp.google.com/c/aom/+/190261>

This roll brought it to main:
<https://chromium-review.googlesource.com/c/chromium/src/+/5545036>

We'll create separate upstream branches for each milestone and cherry-pick the
fix and test to verify.

> 3. Have the changes been released and tested on canary?

Yes. 127.0.6484.0.

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

> 5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>

No.

### am...@chromium.org (2024-05-17)

Thanks for fixing this so quickly! Since this change just landed let's let this bake over the weekend. I'll merge review early next week (Monday afternoon the M125 Stable update for release tuesday is cut in the morning).

### ap...@google.com (2024-05-17)

Project: aom
Branch: karat

commit 6655fea3d5de1a90fe948c58bb6461980b52465b
Author: James Zern <jzern@google.com>
Date:   Tue May 14 17:54:10 2024

    update codec config after svc/scale controls
    
    This ensures the encoder state/allocations stay in sync with scaling and
    svc layer changes. In the SVC case, depending on the resolution,
    differences in the chosen superblock size among layers may have caused a
    crash. This was reproducible in WebRTC in screen content mode.
    
    The fix is based on a change by Yuan Tong (tongyuan200097) [1]. It
    refreshes the encoder config after AOME_SET_SCALEMODE,
    AOME_SET_NUMBER_SPATIAL_LAYERS and AV1E_SET_SVC_PARAMS if no frames have
    been encoded. AV1E_SET_SVC_PARAMS was missed in the original change.
    
    [1]: https://aomedia-review.googlesource.com/c/aom/+/171941/2
    
    Bug: chromium:339877165
    Change-Id: Ib3d2a123b159898d7c7e19c81e89ff148920e1f1
    (cherry picked from commit e42f4b1980bbbc772aa886d8b43a885461d7b89e)

M       av1/av1_cx_iface.c

https://aomedia-review.googlesource.com/190265


### ap...@google.com (2024-05-17)

Project: aom
Branch: karat

commit 830be631d1a80d7eba2ddcb0b4905460f56365bd
Author: James Zern <jzern@google.com>
Date:   Thu May 16 13:44:52 2024

    encode_api_test: add repro for chromium 339877165
    
    BUG=chromium:339877165
    
    Change-Id: I69dcc2cda098ec96a34e1e5f7ef557ee8caf5521
    (cherry picked from commit 01467cdbd524900eed283660836179fd1b2cd536)

M       test/encode_api_test.cc

https://aomedia-review.googlesource.com/190268


### am...@chromium.org (2024-05-21)

In reviewing the roll with these fixes on Canary (<https://crrev.com/c/5545036>) as well as the individual fixes, approving backmerge of these fixes to M126 Beta and M125 Stable.
Please merge to M126 Beta (branch 6478) by EOD today so this fix can be included in tomorrow's Beta update.
Please merge to M125 Stable (branch 4422) by EOD Thursday (23 May) so this fix can be included in next week's Stable update -- thanks!

### jz...@google.com (2024-05-21)

> ... M125 Stable (branch 4422)

I think that's 6422.

### ap...@google.com (2024-05-22)

Project: aom
Branch: m126-6478

commit 1342d2326fbb86111d59934828546ee3a026e4c9
Author: James Zern <jzern@google.com>
Date:   Tue May 14 17:54:10 2024

    update codec config after svc/scale controls
    
    This ensures the encoder state/allocations stay in sync with scaling and
    svc layer changes. In the SVC case, depending on the resolution,
    differences in the chosen superblock size among layers may have caused a
    crash. This was reproducible in WebRTC in screen content mode.
    
    The fix is based on a change by Yuan Tong (tongyuan200097) [1]. It
    refreshes the encoder config after AOME_SET_SCALEMODE,
    AOME_SET_NUMBER_SPATIAL_LAYERS and AV1E_SET_SVC_PARAMS if no frames have
    been encoded. AV1E_SET_SVC_PARAMS was missed in the original change.
    
    [1]: https://aomedia-review.googlesource.com/c/aom/+/171941/2
    
    Bug: chromium:339877165
    Change-Id: Ib3d2a123b159898d7c7e19c81e89ff148920e1f1
    (cherry picked from commit e42f4b1980bbbc772aa886d8b43a885461d7b89e)

M       av1/av1_cx_iface.c

https://aomedia-review.googlesource.com/190401


### ap...@google.com (2024-05-22)

Project: aom
Branch: m126-6478

commit 77665fee933b409dd94e35b0c216645f845b9fd9
Author: James Zern <jzern@google.com>
Date:   Thu May 16 13:44:52 2024

    encode_api_test: add repro for chromium 339877165
    
    BUG=chromium:339877165
    
    Change-Id: I69dcc2cda098ec96a34e1e5f7ef557ee8caf5521
    (cherry picked from commit 01467cdbd524900eed283660836179fd1b2cd536)
    (cherry picked from commit 830be631d1a80d7eba2ddcb0b4905460f56365bd)

M       test/encode_api_test.cc

https://aomedia-review.googlesource.com/190402


### ap...@google.com (2024-05-22)

Project: aom
Branch: m125-6422

commit d3cc351e0294be739dffe277ab9e84f4fe4fc03e
Author: James Zern <jzern@google.com>
Date:   Tue May 14 17:54:10 2024

    update codec config after svc/scale controls
    
    This ensures the encoder state/allocations stay in sync with scaling and
    svc layer changes. In the SVC case, depending on the resolution,
    differences in the chosen superblock size among layers may have caused a
    crash. This was reproducible in WebRTC in screen content mode.
    
    The fix is based on a change by Yuan Tong (tongyuan200097) [1]. It
    refreshes the encoder config after AOME_SET_SCALEMODE,
    AOME_SET_NUMBER_SPATIAL_LAYERS and AV1E_SET_SVC_PARAMS if no frames have
    been encoded. AV1E_SET_SVC_PARAMS was missed in the original change.
    
    [1]: https://aomedia-review.googlesource.com/c/aom/+/171941/2
    
    Bug: chromium:339877165
    Change-Id: Ib3d2a123b159898d7c7e19c81e89ff148920e1f1
    (cherry picked from commit e42f4b1980bbbc772aa886d8b43a885461d7b89e)

M       av1/av1_cx_iface.c

https://aomedia-review.googlesource.com/190421


### ap...@google.com (2024-05-22)

Project: aom
Branch: m125-6422

commit ad697557950c7a75603fde6a6c42caf037b7b5c3
Author: James Zern <jzern@google.com>
Date:   Thu May 16 13:44:52 2024

    encode_api_test: add repro for chromium 339877165
    
    BUG=chromium:339877165
    
    Change-Id: I69dcc2cda098ec96a34e1e5f7ef557ee8caf5521
    (cherry picked from commit 01467cdbd524900eed283660836179fd1b2cd536)

M       test/encode_api_test.cc

https://aomedia-review.googlesource.com/190403


### ap...@google.com (2024-05-22)

Project: chromium/src
Branch: refs/branch-heads/6478

commit ecd4b3a4ce6067b4ca0bb314903a4743fd5e4e42
Author: James Zern <jzern@chromium.org>
Date:   Wed May 22 03:47:28 2024

    Roll src/third_party/libaom/source/libaom/ d9ab67e87..77665fee9 (2 commits)
    
    https://aomedia.googlesource.com/aom.git/+log/d9ab67e87cdd..77665fee933b
    
    $ git log d9ab67e87..77665fee9 --date=short --no-merges --format='%ad %ae %s'
    2024-05-16 jzern encode_api_test: add repro for chromium 339877165
    2024-05-14 jzern update codec config after svc/scale controls
    
    Created with:
      roll-dep src/third_party/libaom/source/libaom
    
    Bug: 339877165
    Change-Id: I80dcd17ed85574bd2a003209434b93de59432e9f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5556562
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org>
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org>
    Auto-Submit: James Zern <jzern@google.com>
    Cr-Commit-Position: refs/branch-heads/6478@{#400}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       DEPS
M       third_party/libaom/README.chromium
M       third_party/libaom/source/config/config/aom_version.h
M       third_party/libaom/source/libaom

https://chromium-review.googlesource.com/5556562


### pe...@google.com (2024-05-22)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### jz...@google.com (2024-05-22)

> LTS Milestone M120
> 
> This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
> 
> 1. Was this issue a regression for the milestone it was found in?

No.

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No. See [comment #23](https://issues.chromium.org/issues/339877165#comment23).

### sp...@google.com (2024-05-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are not already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### ap...@google.com (2024-05-22)

Project: chromium/src
Branch: refs/branch-heads/6422

commit 4bcaaec6f5fefe91e23ee23ccf8a9a5f5f069f11
Author: James Zern <jzern@chromium.org>
Date:   Wed May 22 20:58:12 2024

    Roll src/third_party/libaom/source/libaom/ a4420e55a..ad6975579 (2 commits)
    
    https://aomedia.googlesource.com/aom.git/+log/a4420e55a8d5..ad697557950c
    
    $ git log a4420e55a..ad6975579 --date=short --no-merges --format='%ad %ae %s'
    2024-05-16 jzern encode_api_test: add repro for chromium 339877165
    2024-05-14 jzern update codec config after svc/scale controls
    
    Created with:
      roll-dep src/third_party/libaom/source/libaom
    
    Bug: 339877165
    Change-Id: I85ae8b807738b9cf981080245126f8122dcb198c
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5556566
    Commit-Queue: Wan-Teh Chang <wtc@google.com>
    Auto-Submit: James Zern <jzern@google.com>
    Reviewed-by: Wan-Teh Chang <wtc@google.com>
    Cr-Commit-Position: refs/branch-heads/6422@{#1121}
    Cr-Branched-From: 9012208d0ce02e0cf0adb9b62558627c356f3278-refs/heads/main@{#1287751}

M       DEPS
M       third_party/libaom/README.chromium
M       third_party/libaom/source/config/config/aom_version.h
M       third_party/libaom/source/libaom

https://chromium-review.googlesource.com/5556566


### am...@chromium.org (2024-05-22)

Congratulations Cassidy Kim! Thank you for your efforts and reporting this codec memory corruption bug to us -- nice work!

### ap...@google.com (2024-06-07)

Project: aom
Branch: jellybee

commit 759713613a9205ffc200ddf2aca3b50e33f4a0c6
Author: James Zern <jzern@google.com>
Date:   Tue May 14 17:54:10 2024

    update codec config after svc/scale controls
    
    This ensures the encoder state/allocations stay in sync with scaling and
    svc layer changes. In the SVC case, depending on the resolution,
    differences in the chosen superblock size among layers may have caused a
    crash. This was reproducible in WebRTC in screen content mode.
    
    The fix is based on a change by Yuan Tong (tongyuan200097) [1]. It
    refreshes the encoder config after AOME_SET_SCALEMODE,
    AOME_SET_NUMBER_SPATIAL_LAYERS and AV1E_SET_SVC_PARAMS if no frames have
    been encoded. AV1E_SET_SVC_PARAMS was missed in the original change.
    
    [1]: https://aomedia-review.googlesource.com/c/aom/+/171941/2
    
    Bug: chromium:339877165
    Change-Id: Ib3d2a123b159898d7c7e19c81e89ff148920e1f1
    (cherry picked from commit e42f4b1980bbbc772aa886d8b43a885461d7b89e)

M       av1/av1_cx_iface.c

https://aomedia-review.googlesource.com/190945


### ap...@google.com (2024-06-07)

Project: aom
Branch: jellybee

commit 3a15245e13e347e2016d1077f9d3cd9a62e76c4e
Author: James Zern <jzern@google.com>
Date:   Thu May 16 13:44:52 2024

    encode_api_test: add repro for chromium 339877165
    
    BUG=chromium:339877165
    
    Change-Id: I69dcc2cda098ec96a34e1e5f7ef557ee8caf5521
    (cherry picked from commit 01467cdbd524900eed283660836179fd1b2cd536)

M       test/encode_api_test.cc

https://aomedia-review.googlesource.com/190946


### wt...@google.com (2024-06-11)

The fix for this bug is in the libaom v3.8.3 and v3.9.1 patch releases.

### na...@google.com (2024-06-17)

Based on comment#38 and #23, approving merge for LTS-120

### jz...@google.com (2024-06-17)

An upstream branch was created for M120 some time ago. voit@ pinged me about it and it sounded like he'd do the work, but I see he's left now. I'll pull the patches over.

### ap...@google.com (2024-06-17)

Project: aom
Branch: m120-6099

commit c3c771d1cfd7efd25b6d5bc565bdf5cd971f47b2
Author: James Zern <jzern@google.com>
Date:   Thu May 16 13:44:52 2024

    encode_api_test: add repro for chromium 339877165
    
    BUG=chromium:339877165
    
    Change-Id: I69dcc2cda098ec96a34e1e5f7ef557ee8caf5521
    (cherry picked from commit 01467cdbd524900eed283660836179fd1b2cd536)
    (cherry picked from commit 3a15245e13e347e2016d1077f9d3cd9a62e76c4e)

M       test/encode_api_test.cc

https://aomedia-review.googlesource.com/191182


### ap...@google.com (2024-06-17)

Project: aom
Branch: m120-6099

commit 59b4286870d839e571a8785f9e698fb5263e0182
Author: James Zern <jzern@google.com>
Date:   Tue May 14 17:54:10 2024

    update codec config after svc/scale controls
    
    This ensures the encoder state/allocations stay in sync with scaling and
    svc layer changes. In the SVC case, depending on the resolution,
    differences in the chosen superblock size among layers may have caused a
    crash. This was reproducible in WebRTC in screen content mode.
    
    The fix is based on a change by Yuan Tong (tongyuan200097) [1]. It
    refreshes the encoder config after AOME_SET_SCALEMODE,
    AOME_SET_NUMBER_SPATIAL_LAYERS and AV1E_SET_SVC_PARAMS if no frames have
    been encoded. AV1E_SET_SVC_PARAMS was missed in the original change.
    
    [1]: https://aomedia-review.googlesource.com/c/aom/+/171941/2
    
    Bug: chromium:339877165
    Change-Id: Ib3d2a123b159898d7c7e19c81e89ff148920e1f1
    (cherry picked from commit e42f4b1980bbbc772aa886d8b43a885461d7b89e)
    (cherry picked from commit 759713613a9205ffc200ddf2aca3b50e33f4a0c6)

M       av1/av1_cx_iface.c

https://aomedia-review.googlesource.com/191181


### ap...@google.com (2024-06-18)

Project: chromium/src
Branch: refs/branch-heads/6099

commit ab985c9ffebfaa3e732742f0b899b7e37d78d0f9
Author: James Zern <jzern@chromium.org>
Date:   Tue Jun 18 18:12:03 2024

    Roll src/third_party/libaom/source/libaom/ 1dbe1c7fa..c3c771d1c (2 commits)
    
    https://aomedia.googlesource.com/aom.git/+log/1dbe1c7fae24..c3c771d1cfd7
    
    $ git log 1dbe1c7fa..c3c771d1c --date=short --no-merges --format='%ad %ae %s'
    2024-05-16 jzern encode_api_test: add repro for chromium 339877165
    2024-05-14 jzern update codec config after svc/scale controls
    
    Created with:
      roll-dep src/third_party/libaom/source/libaom
    
    Bug: 339877165
    Change-Id: I6562aa83dd48fce231d46d3becc403743d7cb7df
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5633509
    Auto-Submit: James Zern <jzern@google.com>
    Commit-Queue: Wan-Teh Chang <wtc@google.com>
    Reviewed-by: Wan-Teh Chang <wtc@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#2037}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       DEPS
M       third_party/libaom/README.chromium
M       third_party/libaom/source/config/config/aom_version.h
M       third_party/libaom/source/config/linux/arm-neon-cpu-detect/config/aom_config.asm
M       third_party/libaom/source/config/linux/arm-neon-cpu-detect/config/aom_config.c
M       third_party/libaom/source/config/linux/arm-neon-cpu-detect/config/aom_config.h
M       third_party/libaom/source/config/linux/arm-neon/config/aom_config.asm
M       third_party/libaom/source/config/linux/arm-neon/config/aom_config.c
M       third_party/libaom/source/config/linux/arm-neon/config/aom_config.h
M       third_party/libaom/source/config/linux/arm/config/aom_config.asm
M       third_party/libaom/source/config/linux/arm/config/aom_config.c
M       third_party/libaom/source/config/linux/arm/config/aom_config.h
M       third_party/libaom/source/config/linux/arm64-cpu-detect/config/aom_config.asm
M       third_party/libaom/source/config/linux/arm64-cpu-detect/config/aom_config.c
M       third_party/libaom/source/config/linux/arm64-cpu-detect/config/aom_config.h
M       third_party/libaom/source/config/linux/generic/config/aom_config.asm
M       third_party/libaom/source/config/linux/generic/config/aom_config.c
M       third_party/libaom/source/config/linux/generic/config/aom_config.h
M       third_party/libaom/source/config/linux/ia32/config/aom_config.c
M       third_party/libaom/source/config/linux/ia32/config/aom_config.h
M       third_party/libaom/source/config/linux/x64/config/aom_config.c
M       third_party/libaom/source/config/linux/x64/config/aom_config.h
M       third_party/libaom/source/config/win/arm64-cpu-detect/config/aom_config.asm
M       third_party/libaom/source/config/win/arm64-cpu-detect/config/aom_config.c
M       third_party/libaom/source/config/win/arm64-cpu-detect/config/aom_config.h
M       third_party/libaom/source/config/win/ia32/config/aom_config.c
M       third_party/libaom/source/config/win/ia32/config/aom_config.h
M       third_party/libaom/source/config/win/x64/config/aom_config.c
M       third_party/libaom/source/config/win/x64/config/aom_config.h
M       third_party/libaom/source/libaom

https://chromium-review.googlesource.com/5633509


### ga...@amazon.com (2024-07-11)

Changed status by mistake. Reverted back to fixed but it then it assigned the issue to me. Please ignore this update.

### pe...@google.com (2024-10-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339877165)*
