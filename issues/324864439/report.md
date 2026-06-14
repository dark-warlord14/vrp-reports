# OOB in WebRTC-MultiplexCodec

| Field | Value |
|-------|-------|
| **Issue ID** | [324864439](https://issues.chromium.org/issues/324864439) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ho...@google.com |
| **Created** | 2024-02-12 |
| **Bounty** | $7,000.00 |

## Description

tested os: 
- ubuntu & mac

tested chrome version:
- stable & dev & beta

repro steps:
./chrome  --disable-gpu  --use-fake-ui-for-media-stream --use-fake-device-for-media-stream       --incognito   --user-data-dir=/tmp/xx1  --enable-features=WebRTC-MultiplexCodec  http://localhost:8880/crash.html

The PoC originates from https://issues.chromium.org/issues/40060863; I only modified one line of code and added a reload operation to reproduce it.
- transceiver.setCodecPreferences(codecs.filter(codec => codec.mimeType == 'video/vp9'));
+ transceiver.setCodecPreferences(codecs.filter(codec => codec.mimeType == 'video/multiplex'));
And according to the crash log, it should be a similar issue.

==2166822==ERROR: AddressSanitizer: SEGV on unknown address (pc 0x5629084ec442 bp 0x7f101e2de9e0 sp 0x7f101e2de8e0 T4)
==2166822==The signal is caused by a READ memory access.
==2166822==Hint: this fault was caused by a dereference of a high value address (see register values below).  Disassemble the provided pc to learn which register was used.
    #0 0x5629084ec442 in __tree_is_left_child<std::__Cr::__tree_node_base<void *> *> ./../../third_party/libc++/src/include/__tree:112:33
    #1 0x5629084ec442 in __tree_next_iter<std::__Cr::__tree_end_node<std::__Cr::__tree_node_base<void *> *> *, std::__Cr::__tree_node_base<void *> *> ./../../third_party/libc++/src/include/__tree:200:11
    #2 0x5629084ec442 in operator++ ./../../third_party/libc++/src/include/__tree:751:9
    #3 0x5629084ec442 in operator++ ./../../third_party/libc++/src/include/map:874:5
    #4 0x5629084ec442 in __advance<std::__Cr::__map_iterator<std::__Cr::__tree_iterator<std::__Cr::__value_type<unsigned int, webrtc::MultiplexImage>, std::__Cr::__tree_node<std::__Cr::__value_type<unsigned int, webrtc::MultiplexImage>, void *> *, long> > > ./../../third_party/libc++/src/include/__iterator/advance.h:49:7
    #5 0x5629084ec442 in advance<std::__Cr::__map_iterator<std::__Cr::__tree_iterator<std::__Cr::__value_type<unsigned int, webrtc::MultiplexImage>, std::__Cr::__tree_node<std::__Cr::__value_type<unsigned int, webrtc::MultiplexImage>, void *> *, long> >, long, long, void> ./../../third_party/libc++/src/include/__iterator/advance.h:71:3
    #6 0x5629084ec442 in next<std::__Cr::__map_iterator<std::__Cr::__tree_iterator<std::__Cr::__value_type<unsigned int, webrtc::MultiplexImage>, std::__Cr::__tree_node<std::__Cr::__value_type<unsigned int, webrtc::MultiplexImage>, void *> *, long> >, 0> ./../../third_party/libc++/src/include/__iterator/next.h:35:3
    #7 0x5629084ec442 in webrtc::MultiplexEncoderAdapter::OnEncodedImage(webrtc::AlphaCodecStream, webrtc::EncodedImage const&, webrtc::CodecSpecificInfo const*) ./../../third_party/webrtc/modules/video_coding/codecs/multiplex/multiplex_encoder_adapter.cc:325:40
    #8 0x5629084ed4b2 in webrtc::MultiplexEncoderAdapter::AdapterEncodedImageCallback::OnEncodedImage(webrtc::EncodedImage const&, webrtc::CodecSpecificInfo const*) ./../../third_party/webrtc/modules/video_coding/codecs/multiplex/multiplex_encoder_adapter.cc:39:22
    #9 0x5629084e020f in blink::StatsCollectingEncoder::OnEncodedImage(webrtc::EncodedImage const&, webrtc::CodecSpecificInfo const*) ./../../third_party/blink/renderer/platform/peerconnection/stats_collecting_encoder.cc:159:26
    #10 0x5629084cd9f8 in OnEncodedImage ./../../third_party/webrtc/media/engine/simulcast_encoder_adapter.cc:686:38
    #11 0x5629084cd9f8 in webrtc::SimulcastEncoderAdapter::StreamContext::OnEncodedImage(webrtc::EncodedImage const&, webrtc::CodecSpecificInfo const*) ./../../third_party/webrtc/media/engine/simulcast_encoder_adapter.cc:236:19
    #12 0x56290843922d in webrtc::LibvpxVp9Encoder::DeliverBufferedFrame(bool) ./../../third_party/webrtc/modules/video_coding/codecs/vp9/libvpx_vp9_encoder.cc:1770:33
    #13 0x562908420775 in webrtc::LibvpxVp9Encoder::GetEncodedLayerFrame(vpx_codec_cx_pkt const*) ./../../third_party/webrtc/modules/video_coding/codecs/vp9/libvpx_vp9_encoder.cc:1755:3
    #14 0x5628f88cb880 in encoder_encode ./../../third_party/libvpx/source/libvpx/vp9/vp9_cx_iface.c:1556:13
    #15 0x5628f8919afc in vpx_codec_encode ./../../third_party/libvpx/source/libvpx/vpx/src/vpx_encoder.c:212:13
    #16 0x562908431c32 in webrtc::LibvpxVp9Encoder::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/modules/video_coding/codecs/vp9/libvpx_vp9_encoder.cc:1263:39
    #17 0x5629084d46ae in webrtc::SimulcastEncoderAdapter::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/media/engine/simulcast_encoder_adapter.cc:568:33
    #18 0x5629084ea669 in webrtc::MultiplexEncoderAdapter::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/modules/video_coding/codecs/multiplex/multiplex_encoder_adapter.cc:217:30
    #19 0x5628f8428aa2 in webrtc::VideoStreamEncoder::EncodeVideoFrame(webrtc::VideoFrame const&, long) ./../../third_party/webrtc/video/video_stream_encoder.cc:2017:43
    #20 0x5628f842620e in webrtc::VideoStreamEncoder::MaybeEncodeVideoFrame(webrtc::VideoFrame const&, long) ./../../third_party/webrtc/video/video_stream_encoder.cc:1869:3
    #21 0x5628f8422a3b in webrtc::VideoStreamEncoder::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&) ./../../third_party/webrtc/video/video_stream_encoder.cc:1553:5
    #22 0x5628f83f2bd1 in webrtc::(anonymous namespace)::ZeroHertzAdapterMode::SendFrameNow(std::__Cr::optional<webrtc::Timestamp>, webrtc::VideoFrame const&) ./../../third_party/webrtc/video/frame_cadence_adapter.cc:706:14
    #23 0x5628f83f1f1d in ProcessOnDelayedCadence ./../../third_party/webrtc/video/frame_cadence_adapter.cc:632:3
    #24 0x5628f83f1f1d in operator() ./../../third_party/webrtc/video/frame_cadence_adapter.cc:514:18
    #25 0x5628f83f1f1d in __invoke<(lambda at ../../third_party/webrtc/video/frame_cadence_adapter.cc:512:16)> ./../../third_party/libc++/src/include/__type_traits/invoke.h:344:25
    #26 0x5628f83f1f1d in invoke<(lambda at ../../third_party/webrtc/video/frame_cadence_adapter.cc:512:16)> ./../../third_party/libc++/src/include/__functional/invoke.h:28:10
    #27 0x5628f83f1f1d in InvokeR<void, (lambda at ../../third_party/webrtc/video/frame_cadence_adapter.cc:512:16), void> ./../../third_party/abseil-cpp/absl/functional/internal/any_invocable.h:132:3
    #28 0x5628f83f1f1d in void absl::internal_any_invocable::LocalInvoker<false, void, webrtc::(anonymous namespace)::ZeroHertzAdapterMode::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&)::$_0&&>(absl::internal_any_invocable::TypeErasedState*) ./../../third_party/abseil-cpp/absl/functional/internal/any_invocable.h:310:10
    #29 0x5628e588f538 in operator() ./../../third_party/abseil-cpp/absl/functional/internal/any_invocable.h:876:1
    #30 0x5628e588f538 in blink::WebRtcTaskQueue::RunTask(absl::AnyInvocable<void () &&>) ./../../third_party/webrtc_overrides/task_queue_factory.cc:100:5
    #31 0x5628e5890eb7 in Invoke<void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue *, absl::AnyInvocable<void () &&> > ./../../base/functional/bind_internal.h:710:12
    #32 0x5628e5890eb7 in MakeItSo<void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), std::__Cr::tuple<base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&> > > ./../../base/functional/bind_internal.h:860:12
    #33 0x5628e5890eb7 in RunImpl<void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), std::__Cr::tuple<base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:991:14
    #34 0x5628e5890eb7 in base::internal::Invoker<base::internal::BindState<void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:904:12
    #35 0x5628f591e2f4 in Run ./../../base/functional/callback.h:156:12
    #36 0x5628f591e2f4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #37 0x5628f59a02bb in RunTask<(lambda at ../../base/task/thread_pool/task_tracker.cc:680:35)> ./../../base/task/common/task_annotator.h:89:5
    #38 0x5628f59a02bb in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:679:19
    #39 0x5628f59a050c in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) ./../../base/task/thread_pool/task_tracker.cc:664:3
    #40 0x5628f599f7fa in RunTaskWithShutdownBehavior ./../../base/task/thread_pool/task_tracker.cc:694:7
    #41 0x5628f599f7fa in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) ./../../base/task/thread_pool/task_tracker.cc:521:5
    #42 0x5628f599e6ed in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread_pool/task_tracker.cc:416:5
    #43 0x5628f59dffd0 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread_pool/worker_thread.cc:434:36
    #44 0x5628f59df077 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread_pool/worker_thread.cc:318:3
    #45 0x5628f59deb40 in base::internal::WorkerThread::ThreadMain() ./../../base/task/thread_pool/worker_thread.cc:298:7
    #46 0x5628f5a4b717 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103:13
    #47 0x5628e401f918 in asan_thread_start(void*) _asan_rtl_:28

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (/home/pwn11/asan-linux-release/chrome+0x32941442) (BuildId: 59eb2d6bc9ad1b02)
Thread T4 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x5628e40079f1 in ___interceptor_pthread_create _asan_rtl_:3
    #1 0x5628f5a4ac70 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform_thread_posix.cc:148:13
    #2 0x5628f59ddf69 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) ./../../base/task/thread_pool/worker_thread.cc:195:3
    #3 0x5628f59a2c4f in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() ./../../base/task/thread_pool/thread_group.cc:109:13
    #4 0x5628f59a26af in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() ./../../base/task/thread_pool/thread_group.cc:84:3
    #5 0x5628f59d57e9 in ~SemaphoreScopedCommandsExecutor ./../../base/task/thread_pool/thread_group_semaphore.cc:48:3
    #6 0x5628f59d57e9 in base::internal::ThreadGroupSemaphore::PushTaskSourceAndWakeUpWorkers(base::internal::RegisteredTaskSourceAndTransaction) ./../../base/task/thread_pool/thread_group_semaphore.cc:173:1
    #7 0x5628f59b5e88 in base::internal::ThreadPoolImpl::PostTaskWithSequenceNow(base::internal::Task, scoped_refptr<base::internal::Sequence>) ./../../base/task/thread_pool/thread_pool_impl.cc:460:38
    #8 0x5628f59b644a in base::internal::ThreadPoolImpl::PostTaskWithSequence(base::internal::Task, scoped_refptr<base::internal::Sequence>) ./../../base/task/thread_pool/thread_pool_impl.cc:483:12
    #9 0x5628f59dc560 in base::internal::PooledSequencedTaskRunner::PostDelayedTask(base::Location const&, base::OnceCallback<void ()>, base::TimeDelta) ./../../base/task/thread_pool/pooled_sequenced_task_runner.cc:37:40
    #10 0x5628f5926789 in base::DeferredSequencedTaskRunner::StartImpl() ./../../base/task/deferred_sequenced_task_runner.cc:0:0
    #11 0x5628f5926c5d in base::DeferredSequencedTaskRunner::StartWithTaskRunner(scoped_refptr<base::SequencedTaskRunner>) ./../../base/task/deferred_sequenced_task_runner.cc:102:3
    #12 0x5628f7d8c8bc in base::tracing::PerfettoPlatform::StartTaskRunner(scoped_refptr<base::SequencedTaskRunner>) ./../../base/tracing/perfetto_platform.cc:45:26
    #13 0x5628f7d873d1 in tracing::PerfettoTracedProcess::OnThreadPoolAvailable(bool) ./../../services/tracing/public/cpp/perfetto/perfetto_traced_process.cc:413:16
    #14 0x562901012765 in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) ./../../content/child/child_process.cc:124:3
    #15 0x56290c8ce5eb in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) ./../../content/renderer/render_process.cc:18:7
    #16 0x56290c8cdc5f in content::RenderProcessImpl::RenderProcessImpl() ./../../content/renderer/render_process_impl.cc:120:7
    #17 0x56290c8ce2b0 in content::RenderProcessImpl::Create() ./../../content/renderer/render_process_impl.cc:276:31
    #18 0x56290c958149 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:295:53
    #19 0x5628f30730f8 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #20 0x5628f307463c in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #21 0x5628f307706f in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1146:10
    #22 0x5628f3071450 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:335:36
    #23 0x5628f3071acb in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:348:10
    #24 0x5628e4057f28 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #25 0x7f1028229d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16


==2166822==ADDITIONAL INFO

==2166822==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5628f83eec2f in webrtc::(anonymous namespace)::ZeroHertzAdapterMode::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&) ./../../third_party/webrtc/video/frame_cadence_adapter.cc:510:11
    #1 0x5628f83eba4f in webrtc::(anonymous namespace)::FrameCadenceAdapterImpl::OnFrame(webrtc::VideoFrame const&) ./../../third_party/webrtc/video/frame_cadence_adapter.cc:935:11
    #2 0x56290883da65 in blink::MediaStreamVideoWebRtcSink::WebRtcVideoSourceAdapter::OnVideoFrameOnIO(scoped_refptr<media::VideoFrame>, base::TimeTicks) ./../../third_party/blink/renderer/modules/peerconnection/media_stream_video_webrtc_sink.cc:172:46


==2166822==END OF ADDITIONAL INFO
==2166822==ABORTING

## Attachments

- [crash.html](attachments/crash.html) (text/html, 30.8 KB)
- [asan.log](attachments/asan.log) (text/plain, 14.3 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-02-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5194555139227648.

### wf...@chromium.org (2024-02-12)

Thank you for your report. `WebRTC-MultiplexCodec` seems to be disabled by default so this is security impact none, for now. Triage will continue.

### wf...@chromium.org (2024-02-12)

letting clusterfuzz stew on this for a bit. added some folks from [issue 40060863](https://issues.chromium.org/issues/40060863) which I agree does look similar.

### em...@gmail.com (2024-02-13)

Sorry, I missed one launch flag. you may need to add '--disable-in-process-stack-traces' to get the crash log.

### za...@google.com (2024-02-21)

Can you give an update on this bug? handellm@ Thanks! 

### ha...@google.com (2024-02-22)

Managed to repro. The feature is unused by Google as it seems, and there's no Finch launch active for it.

### ha...@google.com (2024-02-22)

Debugged and the root cause of the problem seems to be the MultiplexEncoderAdapter segfaults when Simulcast is used. Is it worth keeping this feature or should we delete it? -> Stefan for decision.

### ho...@google.com (2024-02-22)

I'd suggest we delete it as I know of no users of it.

### ha...@google.com (2024-02-22)

CL: <https://chromium-review.googlesource.com/c/chromium/src/+/5317574>

CC dcheng & guidou

### ap...@google.com (2024-02-23)

Project: chromium/src
Branch: main

commit e02391a1043606e148ab5f2ec5b768360e4a4487
Author: Markus Handell <handellm@google.com>
Date:   Fri Feb 23 08:43:09 2024

    Fix OOB related to WebRTC-MultiplexCodec.
    
    The implementation segfaults when the multiplex codec is configured
    together with simulcast. Fix by removing the feature.
    
    Fixed: 324864439
    Change-Id: I298fe1b75f1cbc9cdd2b29cb81714c43dbe6cb5e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5317574
    Reviewed-by: Daniel Cheng <dcheng@chromium.org>
    Auto-Submit: Markus Handell <handellm@google.com>
    Commit-Queue: Markus Handell <handellm@google.com>
    Reviewed-by: Guido Urdaneta <guidou@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1264453}

M       third_party/blink/common/features.cc
M       third_party/blink/public/common/features.h
M       third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc

https://chromium-review.googlesource.com/5317574


### ap...@google.com (2024-02-23)

Project: chromium/src
Branch: main

commit 1a2bd5970106d991344ba5fcb644d2a5b9ca23b0
Author: Markus Handell <handellm@google.com>
Date:   Fri Feb 23 12:56:03 2024

    PeerConnectionDependencyFactory: remove unused include.
    
    Bug: 324864439
    Change-Id: I7ffd0c917461c98a76ef5154132562951a22a912
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5318260
    Reviewed-by: Guido Urdaneta <guidou@chromium.org>
    Auto-Submit: Markus Handell <handellm@google.com>
    Commit-Queue: Guido Urdaneta <guidou@chromium.org>
    Commit-Queue: Markus Handell <handellm@google.com>
    Cr-Commit-Position: refs/heads/main@{#1264504}

M       third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc

https://chromium-review.googlesource.com/5318260


### ap...@google.com (2024-02-26)

Project: src
Branch: main

commit 97df932ecc58ac9ee49192992c22995809145cbf
Author: Markus Handell <handellm@webrtc.org>
Date:   Fri Feb 23 12:12:54 2024

    Remove multiplex codec.
    
    The feature isn't in use by Google and has proven to contain security
    issues. It's time to remove it.
    
    Bug: b/324864439
    Change-Id: I80344eb2f2060469d2d69a54dc4519fdd02ab4ea
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/340324
    Reviewed-by: Stefan Holmer <stefan@webrtc.org>
    Commit-Queue: Markus Handell <handellm@webrtc.org>
    Reviewed-by: Björn Terelius <terelius@webrtc.org>
    Cr-Commit-Position: refs/heads/main@{#41808}

M       api/video/video_codec_type.h
M       api/video_codecs/video_codec.cc
M       api/video_codecs/video_decoder_software_fallback_wrapper.cc
M       call/rtp_payload_params.cc
M       examples/BUILD.gn
D       examples/unityplugin/ANDROID_INSTRUCTION
D       examples/unityplugin/DEPS
D       examples/unityplugin/README
D       examples/unityplugin/class_reference_holder.cc
D       examples/unityplugin/class_reference_holder.h
D       examples/unityplugin/java/src/org/webrtc/UnityUtility.java
D       examples/unityplugin/jni_onload.cc
D       examples/unityplugin/simple_peer_connection.cc
D       examples/unityplugin/simple_peer_connection.h
D       examples/unityplugin/unity_plugin_apis.cc
D       examples/unityplugin/unity_plugin_apis.h
D       examples/unityplugin/video_observer.cc
D       examples/unityplugin/video_observer.h
M       logging/rtc_event_log/encoder/rtc_event_log_encoder_new_format.cc
M       logging/rtc_event_log/rtc_event_log_parser.cc
M       media/BUILD.gn
M       media/base/media_constants.cc
D       media/engine/multiplex_codec_factory.cc
D       media/engine/multiplex_codec_factory.h
D       media/engine/multiplex_codec_factory_unittest.cc
M       media/engine/webrtc_video_engine.cc
M       modules/rtp_rtcp/source/create_video_rtp_depacketizer.cc
M       modules/video_coding/BUILD.gn
D       modules/video_coding/codecs/multiplex/augmented_video_frame_buffer.cc
D       modules/video_coding/codecs/multiplex/include/augmented_video_frame_buffer.h
D       modules/video_coding/codecs/multiplex/include/multiplex_decoder_adapter.h
D       modules/video_coding/codecs/multiplex/include/multiplex_encoder_adapter.h
D       modules/video_coding/codecs/multiplex/multiplex_decoder_adapter.cc
D       modules/video_coding/codecs/multiplex/multiplex_encoded_image_packer.cc
D       modules/video_coding/codecs/multiplex/multiplex_encoded_image_packer.h
D       modules/video_coding/codecs/multiplex/multiplex_encoder_adapter.cc
D       modules/video_coding/codecs/multiplex/test/multiplex_adapter_unittest.cc
M       modules/video_coding/video_codec_initializer.cc
M       modules/video_coding/video_codec_initializer_unittest.cc
M       rtc_base/experiments/balanced_degradation_settings_unittest.cc
M       rtc_base/experiments/min_video_bitrate_experiment.cc
M       rtc_base/experiments/min_video_bitrate_experiment_unittest.cc
M       rtc_tools/rtc_event_log_to_text/converter.cc
M       test/scenario/BUILD.gn
M       test/scenario/video_stream.cc
M       test/video_codec_tester.cc
M       video/BUILD.gn
M       video/encoder_overshoot_detector.cc
M       video/encoder_overshoot_detector_unittest.cc
M       video/end_to_end_tests/codec_tests.cc
M       video/full_stack_tests.cc
M       video/pc_full_stack_tests.cc
M       video/video_quality_test.cc
M       video/video_stream_encoder_unittest.cc

https://webrtc-review.googlesource.com/340324


### am...@google.com (2024-02-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-29)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $7,000 for this report of an OOB read / memory corruption in a sandboxed process. Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-06-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/324864439)*
