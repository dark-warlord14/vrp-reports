# Buffer overflow in vp9_get_token_cost via crafted VideoEncoder frame sequence

| Field | Value |
|-------|-------|
| **Issue ID** | [488585490](https://issues.chromium.org/issues/488585490) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Media>Video |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | ma...@google.com |
| **Created** | 2026-03-01 |
| **Bounty** | $2,000.00 |

## Description

## VULNERABILITY DETAILS

A crafted WebCodecs VideoEncoder VP9 sequence triggers an out-of-bounds read in libvpx at vp9\_get\_token\_cost. The issue is attacker-influenced through coefficient values that drive v, which is converted into `extrabits = abs(v) - CAT6_MIN_VAL`, then indexed as `cat6_high_table[extrabits >> 8]` without a sufficient bounds check for all reachable values. This yields an attacker-influenced 2-byte out-of-bounds read (table element type is uint16\_t) in the renderer process during VP9 encode cost computation.

Crash Log:

```
=================================================================
==3855047==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7fe749294a92 at pc 0x7fe74bd808b0 bp 0x7be206f94d80 sp 0x7be206f94d78
READ of size 2 at 0x7fe749294a92 thread T4 (ThreadPoolForeg)
    #0 0x7fe74bd808af in vp9_get_token_cost third_party/libvpx/source/libvpx/vp9/encoder/vp9_tokenize.h:120:12
    #1 0x7fe74bd7fcb8 in cost_coeffs third_party/libvpx/source/libvpx/vp9/encoder/vp9_rdopt.c:426:14
    #2 0x7fe74bd7edf9 in rate_block third_party/libvpx/source/libvpx/vp9/encoder/vp9_rdopt.c:695:10
    #3 0x7fe74bd7a98a in block_rd_txfm third_party/libvpx/source/libvpx/vp9/encoder/vp9_rdopt.c:826:10
    #4 0x7fe74bb8220c in vp9_foreach_transformed_block_in_plane third_party/libvpx/source/libvpx/vp9/common/vp9_blockd.c:70:7
    #5 0x7fe74bd78850 in txfm_rd_in_plane third_party/libvpx/source/libvpx/vp9/encoder/vp9_rdopt.c:876:3
    #6 0x7fe74bd74e62 in choose_largest_tx_size third_party/libvpx/source/libvpx/vp9/encoder/vp9_rdopt.c:903:3
    #7 0x7fe74bd749ce in super_block_yrd third_party/libvpx/source/libvpx/vp9/encoder/vp9_rdopt.c:1036:5
    #8 0x7fe74bd72505 in rd_pick_intra_sby_mode third_party/libvpx/source/libvpx/vp9/encoder/vp9_rdopt.c:1393:5
    #9 0x7fe74bd71611 in vp9_rd_pick_intra_mode_sb third_party/libvpx/source/libvpx/vp9/encoder/vp9_rdopt.c:3240:9
    #10 0x7fe74bc47be4 in hybrid_intra_mode_search third_party/libvpx/source/libvpx/vp9/encoder/vp9_encodeframe.c:4351:5
    #11 0x7fe74bc46fa3 in nonrd_pick_sb_modes third_party/libvpx/source/libvpx/vp9/encoder/vp9_encodeframe.c:4422:5
    #12 0x7fe74bc35c05 in nonrd_use_partition third_party/libvpx/source/libvpx/vp9/encoder/vp9_encodeframe.c:5020:7
    #13 0x7fe74bc3758c in nonrd_use_partition third_party/libvpx/source/libvpx/vp9/encoder/vp9_encodeframe.c:5083:9
    #14 0x7fe74bc376b5 in nonrd_use_partition third_party/libvpx/source/libvpx/vp9/encoder/vp9_encodeframe.c:5085:9
    #15 0x7fe74bc3758c in nonrd_use_partition third_party/libvpx/source/libvpx/vp9/encoder/vp9_encodeframe.c:5083:9
    #16 0x7fe74bc25ef1 in encode_nonrd_sb_row third_party/libvpx/source/libvpx/vp9/encoder/vp9_encodeframe.c:5310:9
    #17 0x7fe74bc23df0 in vp9_encode_sb_row third_party/libvpx/source/libvpx/vp9/encoder/vp9_encodeframe.c:5472:3
    #18 0x7fe74bcad84c in enc_row_mt_worker_hook third_party/libvpx/source/libvpx/vp9/encoder/vp9_ethread.c:617:7
    #19 0x7fe74a001158 in media::CodecWorkerImpl<VPxWorkerInterface, VPxWorkerImpl, VPxWorker, VPxWorkerStatus, (VPxWorkerStatus)0, (VPxWorkerStatus)1, (VPxWorkerStatus)2>::Execute(VPxWorker*) media/base/codec_worker_impl.h:69:29
    #20 0x7fe74bcab4ad in launch_enc_workers third_party/libvpx/source/libvpx/vp9/encoder/vp9_ethread.c:163:7
    #21 0x7fe74bcad26f in vp9_encode_tiles_row_mt third_party/libvpx/source/libvpx/vp9/encoder/vp9_ethread.c:680:3
    #22 0x7fe74bc2c5ed in encode_frame_internal third_party/libvpx/source/libvpx/vp9/encoder/vp9_encodeframe.c:5741:7
    #23 0x7fe74bc296db in vp9_encode_frame third_party/libvpx/source/libvpx/vp9/encoder/vp9_encodeframe.c:5953:5
    #24 0x7fe74bca2b3e in encode_without_recode_loop third_party/libvpx/source/libvpx/vp9/encoder/vp9_encoder.c:4277:3
    #25 0x7fe74bc9851c in encode_frame_to_data_rate third_party/libvpx/source/libvpx/vp9/encoder/vp9_encoder.c:5390:10
    #26 0x7fe74bc8b465 in Pass0Encode third_party/libvpx/source/libvpx/vp9/encoder/vp9_encoder.c:5669:3
    #27 0x7fe74bc89643 in vp9_get_compressed_data third_party/libvpx/source/libvpx/vp9/encoder/vp9_encoder.c:6434:5
    #28 0x7fe74bdc9fa7 in encoder_encode third_party/libvpx/source/libvpx/vp9/vp9_cx_iface.c:1556:20
    #29 0x7fe74bdf8e7f in vpx_codec_encode third_party/libvpx/source/libvpx/vpx/src/vpx_encoder.c:218:13
    #30 0x7fe74aabdc51 in media::VpxVideoEncoder::Encode(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>) media/video/vpx_video_encoder.cc:742:20
    #31 0x7fe74aa1b03b in void base::internal::DecayedFunctorTraits<void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&>::Invoke<void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>(void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*&&, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&) base/functional/bind_internal.h:740:12
    #32 0x7fe74aa1ad74 in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&>, void, 0ul, 1ul, 2ul, 3ul>::MakeItSo<void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>>(void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>&&) base/functional/bind_internal.h:932:12
    #33 0x7fe74aa1aa47 in void base::internal::Invoker<base::internal::FunctorTraits<void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&>, base::internal::BindState<true, true, false, void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>, void ()>::RunImpl<void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>, 0ul, 1ul, 2ul, 3ul>(void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), std::__Cr::tuple<base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/functional/bind_internal.h:1069:14
    #34 0x7fe74aa1a878 in base::internal::Invoker<base::internal::FunctorTraits<void (media::VideoEncoder::*&&)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), media::VideoEncoder*, scoped_refptr<media::VideoFrame>&&, media::VideoEncoder::EncodeOptions&&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>&&>, base::internal::BindState<true, true, false, void (media::VideoEncoder::*)(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>), base::internal::UnretainedWrapper<media::VideoEncoder, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:982:12
    #35 0x7fe77f1ce112 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
    #36 0x7fe77f6fa12e in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:229:34
    #37 0x7fe77f8e77d7 in void base::TaskAnnotator::RunTask<base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)::$_0>(perfetto::StaticString, base::PendingTask&, base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)::$_0&&) base/task/common/task_annotator.h:112:5
    #38 0x7fe77f8e7274 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:691:19
    #39 0x7fe77f8e7428 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:676:3
    #40 0x7fe77f8e593d in base::internal::TaskTracker::RunTaskWithShutdownBehavior(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:706:7
    #41 0x7fe77f8e4a49 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType) base/task/thread_pool/task_tracker.cc:506:5
    #42 0x7fe77f8e3593 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:394:5
    #43 0x7fe77f936243 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:473:36
    #44 0x7fe77f9355ab in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #45 0x7fe77f934e25 in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #46 0x7fe77faa706c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #47 0x562fe99bd896 in asan_thread_start(void*) asan_interceptors.cpp

0x7fe749294a92 is located 18 bytes after global variable 'vp9_cat6_high10_high_cost' defined in '../../third_party/libvpx/source/libvpx/vp9/encoder/vp9_tokenize.c' (0x7fe749294880) of size 512
SUMMARY: AddressSanitizer: global-buffer-overflow third_party/libvpx/source/libvpx/vp9/encoder/vp9_tokenize.h:120:12 in vp9_get_token_cost
Shadow bytes around the buggy address:
  0x7fe749294800: 00 00 00 00 00 00 00 00 00 00 00 00 f9 f9 f9 f9
  0x7fe749294880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7fe749294900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7fe749294980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7fe749294a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7fe749294a80: f9 f9[f9]f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9 f9
  0x7fe749294b00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7fe749294b80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7fe749294c00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7fe749294c80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7fe749294d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
Thread T4 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x562fe99a36c1 in pthread_create (/mnt/lvm_data/chromium/src/out/asan_dbg_symbols/chrome+0xf3406c1) (BuildId: 3afd3fb7d064a1b6)
    #1 0x7fe77faa5b69 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x7fe77faa56c8 in base::PlatformThreadBase::CreateWithType(unsigned long, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:322:10
    #3 0x7fe77f9327b8 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:185:3
    #4 0x7fe77f8f34b4 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush() base/task/thread_pool/thread_group.cc:65:13
    #5 0x7fe77f8f3289 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor() base/task/thread_pool/thread_group.cc:56:3
    #6 0x7fe77f9126bf in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() base/task/thread_pool/thread_group_impl.cc:71:3
    #7 0x7fe77f90549e in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>) base/task/thread_pool/thread_group_impl.cc:289:3
    #8 0x7fe77f91bb7e in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*) base/task/thread_pool/thread_pool_impl.cc:197:35
    #9 0x7fe75a88459e in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>, bool) content/child/child_process.cc:112:20
    #10 0x7fe7675ff616 in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>) content/renderer/render_process.cc:18:7
    #11 0x7fe7675ff8cf in content::RenderProcessImpl::RenderProcessImpl() content/renderer/render_process_impl.cc:98:7
    #12 0x7fe767600460 in content::RenderProcessImpl::Create() content/renderer/render_process_impl.cc:223:31
    #13 0x7fe76765b8b2 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:285:53
    #14 0x7fe76813c92a in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #15 0x7fe76813e163 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #16 0x7fe768141956 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #17 0x7fe7681377af in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #18 0x7fe768138625 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #19 0x562fe9a04700 in ChromeMain chrome/app/chrome_main.cc:191:12
    #20 0x562fe9a03f61 in main chrome/app/chrome_exe_main_aura.cc:17:10
    #21 0x7fe63e564d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16


==3855047==ADDITIONAL INFO

==3855047==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7fe74aa166bc in media::OffloadingVideoEncoder::Encode(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>) media/video/offloading_video_encoder.cc:64:7
    #1 0x7fe74aa187fd in base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)> media::OffloadingVideoEncoder::WrapCallback<base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>>(base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>) media/video/offloading_video_encoder.cc:97:10
    #2 0x7fe74aa166bc in media::OffloadingVideoEncoder::Encode(scoped_refptr<media::VideoFrame>, media::VideoEncoder::EncodeOptions const&, base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>) media/video/offloading_video_encoder.cc:64:7


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=3837542 --enable-crash-reporter=,custom --noerrdialogs --user-data-dir=/tmp/vp9_yes_crash_check_1772327959/profile --change-stack-guard-on-fork=enable --no-sandbox --disable-dev-shm-usage --autoplay-policy=no-user-gesture-required --ozone-platform=headless --disable-gpu-compositing --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1755397479121000 --launch-time-ticks=16930486893472 --shared-files=v8_context_snapshot_data:100 --field-trial-handle=3,i,14386064033147920290,12349290705452148965,262144 --disable-features=PaintHolding --variations-seed-version --pseudonymization-salt-handle=7,i,11198883022770146187,4803122057752559843,4 --trace-process-track-uuid=1205913054661273622 --enable-logging=stderr`


==3855047==END OF ADDITIONAL INFO

```

VERSION
Chrome Version: 146.0.7680.31 + stable (latest released, Chrome for Testing), 147.0.7703.0 + dev (latest preview, Chrome for Testing)

Operating System: Ubuntu 22.04.3 LTS (x86\_64), Linux kernel 5.15.0-151-generic

## REPRODUCTION CASE

Attached file:

- `repro_vp9_get_token_cost_min193.html`

Repro steps (ASAN build):

1. Launch Chromium ASAN build.
2. Open `repro_vp9_get_token_cost_min193.html`.
3. Observe renderer crash with global OOB in `vp9_get_token_cost`.

Type of crash: tab (renderer process)

Reporter credit: heapracer (@heapracer)

## Attachments

- [repro_vp9_get_token_cost_min193.html](attachments/repro_vp9_get_token_cost_min193.html) (text/html, 20.3 MB)
- [b488585490-repro_vp9_get_token_cost_min193.html](attachments/b488585490-repro_vp9_get_token_cost_min193.html) (text/html, 831.6 KB)

## Timeline

### sh...@gmail.com (2026-03-01)

oops, forgot the file:

### me...@google.com (2026-03-06)

Thanks for the report, I can repro locally with stable. wtc: Could you PTAL?

### ch...@google.com (2026-03-06)

Setting milestone because of s0/s1 severity.

### jz...@google.com (2026-03-06)

Thanks for the report. I can reproduce this. Given past security assessments related to overreads I'm going to drop this to S2. I think this aligns with the [documentation](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md) (*An out-of-bounds read in a renderer process*). If anyone disagrees and wants this at P1/S1 please feel free to update (and if you have supporting reasoning or documentation, please give it); I don't think it will change the timeline for the fix.

### jz...@google.com (2026-03-07)

redacted

### dx...@google.com (2026-03-17)

Project: webm/libvpx  

Branch:  main  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://chromium-review.googlesource.com/7660032>

encode\_api\_test: add repro for [b/488585490](https://issues.chromium.org/issues/488585490)

---


Expand for full commit details
```
     
    This causes a read overflow in vp9_cat6_high10_high_cost[]. 
     
    Note this differs from the settings used by WebCodecs and the sequence 
    in the original POC. Using a single frame (6) from that sequence and 
    lossless encoding produces a more extreme overflow. 
     
    An additional test case may be added, but converting the POC to a unit 
    test wasn't causing a failure as encoding diverged on frame 6 from that 
    observed in Chrome (likely incomplete settings transfer). 
     
    Bug: 488585490 
    Change-Id: Id105d73c54556b17590af44cfa710a8f5cd3f9b2

```

---

Files:

- M `test/encode_api_test.cc`
- M `test/test-data.mk`
- M `test/test-data.sha1`

---

Hash: [42d580255a7b842c66f655f035ff3038c0c71d14](https://chromiumdash.appspot.com/commit/42d580255a7b842c66f655f035ff3038c0c71d14)  

Date: Thu Mar 12 02:15:52 2026


---

### dx...@google.com (2026-03-25)

Project: webm/libvpx  

Branch:  main  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://chromium-review.googlesource.com/7695293>

vp9: Add check to validate source input

---


Expand for full commit details
```
     
    Return invalid_params. 
     
    The check is wrapped around a new control: 
    VP9E_SET_VALIDATE_INPUT_HBD, 
    and is enabled by default. 
     
    Check is done only CONFIG_VP9_HIGHBITDEPTH build 
    and for bitdepth > 8. 
     
    Bug: 488585490 
    Change-Id: Ic79dff1bd314d4b197087d3c46d315ece8fd355c

```

---

Files:

- M `test/encode_api_test.cc`
- M `vp9/vp9_cx_iface.c`
- M `vpx/vp8cx.h`

---

Hash: [090dd8b8cb3a11dec5250bef62aba9b99eb46636](https://chromiumdash.appspot.com/commit/090dd8b8cb3a11dec5250bef62aba9b99eb46636)  

Date: Mon Mar 23 22:09:28 2026


---

### dx...@google.com (2026-03-27)

Project: chromium/src  

Branch:  main  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://chromium-review.googlesource.com/7705144>

Roll src/third\_party/libvpx/source/libvpx/ 3fce57ecc..090dd8b8c (1 commit)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/webm/libvpx.git/+log/3fce57ecc905..090dd8b8cb3a 
     
    $ git log 3fce57ecc..090dd8b8c --date=short --no-merges --format='%ad %ae %s' 
    2026-03-23 marpan vp9: Add check to validate source input 
     
    Created with: 
      roll-dep src/third_party/libvpx/source/libvpx 
    R=jzern@google.com 
     
    Bug: 308446709, 488585490 
    Change-Id: I45e9a2da38aba5c260f01f4c3aff1cd1651709f0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7705144 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Commit-Queue: Marco Paniconi <marpan@google.com> 
    Reviewed-by: James Zern <jzern@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1605940}

```

---

Files:

- M `DEPS`
- M `third_party/libvpx/README.chromium`
- M `third_party/libvpx/source/config/vpx_version.h`
- M `third_party/libvpx/source/libvpx`

---

Hash: [51ae1a1774180e0f565b28a2a6c0df5ae857168c](https://chromiumdash.appspot.com/commit/51ae1a1774180e0f565b28a2a6c0df5ae857168c)  

Date: Fri Mar 27 02:54:09 2026


---

### dx...@google.com (2026-03-30)

Project: webm/libvpx  

Branch:  main  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://chromium-review.googlesource.com/7711998>

vp9; move source input check to validate\_img

---


Expand for full commit details
```
     
    And remove the check: 
    ctx->oxcf.input_bit_depth > 8 
     
    Bug: 488585490 
    Change-Id: Ibf73572d9db20e8a731fffe363675a7f8173d4f7

```

---

Files:

- M `vp9/vp9_cx_iface.c`

---

Hash: [d20e271c144ee80e5c6025b26bc01a8b8c59a187](https://chromiumdash.appspot.com/commit/d20e271c144ee80e5c6025b26bc01a8b8c59a187)  

Date: Mon Mar 30 21:17:30 2026


---

### ch...@google.com (2026-04-06)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488585490)*
