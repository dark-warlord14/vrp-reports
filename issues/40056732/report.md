# Security:  ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fde15ff9890 at pc 0x7fde364c5034

| Field | Value |
|-------|-------|
| **Issue ID** | [40056732](https://issues.chromium.org/issues/40056732) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Media |
| **Reporter** | he...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-04-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Opening the .ogv file and playing by pressing the play button crashes the browser tab.

**VERSION**  

Chrome Version: Version 20.0.1100.0 (131961) asan-symbolized-linux-release-131961

Operating System: xubuntu 11.00

**REPRODUCTION CASE**  

Open the attached file in browser and press play button.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace, registers, exception record]**  

**Client ID (if relevant): [see link above]**

# stderr: [15760:22236:133717149415:ERROR:ffmpeg\_video\_decoder.cc(355)] Error decoding a video frame with timestamp: 266667 us, duration: 66667 us, packet size: 131 bytes [15760:7072:133860758269:ERROR:ffmpeg\_video\_decoder.cc(355)] Error decoding a video frame with timestamp: 533000 us, duration: 66000 us, packet size: 19 bytes

==15760== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fde15ff9890 at pc 0x7fde364c5034 bp 0x7fde1958fe50 sp 0x7fde1958fe48  

READ of size 8 at 0x7fde15ff9890 thread T4403  

#0 0x7fde364c5034 in av\_freep /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/ffmpeg/libavutil/mem.c:181  

#1 0x7fde364a5060 in avformat\_close\_input /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/ffmpeg/libavformat/utils.c:2750  

0x7fde15ff9890 is located 4 bytes to the right of 12-byte region [0x7fde15ff9880,0x7fde15ff988c)  

allocated by thread T4403 here:  

#0 0x7fde4a9f66fc in posix\_memalign ??:0  

#1 0x7fde364c4d22 in av\_malloc /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/ffmpeg/libavutil/mem.c:94  

#2 0x7fde364c504c in av\_mallocz /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/ffmpeg/libavutil/mem.c:186  

#3 0x7fde36483ee7 in ogg\_packet /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/ffmpeg/libavformat/oggdec.c:400  

#4 0x7fde36486451 in ogg\_get\_headers /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/ffmpeg/libavformat/oggdec.c:467  

#5 0x7fde4a15315f in media::FFmpegDemuxer::InitializeTask(media::DemuxerHost\*, base::Callback<void (media::PipelineStatus)> const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/media/filters/ffmpeg\_demuxer.cc:483  

#6 0x7fde4a157979 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (media::FFmpegDemuxer::\*)(media::DemuxerHost\*, base::Callback<void (media::PipelineStatus)> const&)>, void (media::FFmpegDemuxer\* const&, media::DemuxerHost\* const&, base::Callback<void (media::PipelineStatus)> const&)>::MakeItSo(base::internal::RunnableAdapter<void (media::FFmpegDemuxer::\*)(media::DemuxerHost\*, base::Callback<void (media::PipelineStatus)> const&)>, media::FFmpegDemuxer\* const&, media::DemuxerHost\* const&, base::Callback<void (media::PipelineStatus)> const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:927  

#7 0x7fde45bce263 in MessageLoop::RunTask(base::PendingTask const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:459  

#8 0x7fde45bcea54 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:470  

#9 0x7fde45bcee0e in MessageLoop::DoWork() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:647  

#10 0x7fde45bdb1ee in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_pump\_default.cc:28  

#11 0x7fde45bcda7c in MessageLoop::RunInternal() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:418  

#12 0x7fde45bcc758 in MessageLoop::Run() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:301  

#13 0x7fde45c43bc8 in base::Thread::ThreadMain() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/threading/thread.cc:164  

#14 0x7fde45c38aec in ThreadFunc /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/threading/platform\_thread\_posix.cc:65  

#15 0x7fde4a9f94eb in **asan::AsanThread::ThreadStart() ??:0  

Thread T4403 created by T0 here:  

#0 0x7fde4a9f2833 in pthread\_create ??:0  

#1 0x7fde45c386b4 in CreateThread /b/build/slave/ASAN\_Release\_\_symbolized*/build/base/threading/platform\_thread\_posix.cc:127  

#2 0x7fde45c3859d in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate\*, unsigned long\*) /b/build/slave/ASAN\_Release\_\_symbolized*/build/base/threading/platform\_thread\_posix.cc:249  

#3 0x7fde45c43515 in base::Thread::StartWithOptions(base::Thread::Options const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/threading/thread.cc:72  

#4 0x7fde45c4337f in base::Thread::Start() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/threading/thread.cc:61  

#5 0x7fde4a11a426 in media::MessageLoopFactory::GetThread(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/media/base/message\_loop\_factory.cc:42  

#6 0x7fde4a11a1d9 in media::MessageLoopFactory::GetMessageLoop(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/media/base/message\_loop\_factory.cc:24  

#7 0x7fde48cb66fb in WebMediaPlayerImpl /b/build/slave/ASAN\_Release\_\_symbolized\_/build/webkit/media/webmediaplayer\_impl.cc:130  

#8 0x7fde4992dae5 in RenderViewImpl::createMediaPlayer(WebKit::WebFrame\*, WebKit::WebMediaPlayerClient\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/renderer/render\_view\_impl.cc:2220  

#9 0x7fde46f6e6e8 in createWebMediaPlayer /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebKit/chromium/src/WebMediaPlayerClientImpl.cpp:58  

#10 0x7fde46f6e472 in WebKit::WebMediaPlayerClientImpl::loadInternal() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebKit/chromium/src/WebMediaPlayerClientImpl.cpp:250  

#11 0x7fde46f6e22b in WebKit::WebMediaPlayerClientImpl::load(WTF::String const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebKit/chromium/src/WebMediaPlayerClientImpl.cpp:240  

#12 0x7fde4762217d in WebCore::MediaPlayer::loadWithNextMediaEngine(WebCore::MediaPlayerFactory\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.cpp:408  

#13 0x7fde476218b6 in WebCore::MediaPlayer::load(WebCore::KURL const&, WebCore::ContentType const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.cpp:366  

#14 0x7fde47420805 in WebCore::HTMLMediaElement::loadResource(WebCore::KURL const&, WebCore::ContentType&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:964  

#15 0x7fde4741cd52 in WebCore::HTMLMediaElement::loadNextSourceChild() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:865  

#16 0x7fde4741fe4d in WebCore::HTMLMediaElement::selectMediaResource() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:846  

#17 0x7fde4741d06c in WebCore::HTMLMediaElement::loadInternal() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:775  

#18 0x7fde47417b39 in WebCore::HTMLMediaElement::loadTimerFired(WebCore::Timer[WebCore::HTMLMediaElement](javascript:void(0);)\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:587  

#19 0x7fde475a5aa8 in WebCore::ThreadTimers::sharedTimerFiredInternal() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#20 0x7fde48beb0ed in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, void (webkit\_glue::WebKitPlatformSupportImpl\*)>::MakeItSo(base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, webkit\_glue::WebKitPlatformSupportImpl\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:869  

#21 0x7fde48beaf1d in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, void (webkit\_glue::WebKitPlatformSupportImpl\*), void (base::internal::UnretainedWrapper<webkit\_glue::WebKitPlatformSupportImpl>)>, void (webkit\_glue::WebKitPlatformSupportImpl\*)>::Run(base::internal::BindStateBase\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:1170  

#22 0x7fde45c476ea in base::Timer::RunScheduledTask() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/timer.cc:182  

#23 0x7fde45c47cfd in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, void (base::BaseTimerTaskInternal\*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, base::BaseTimerTaskInternal\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:869  

#24 0x7fde45c47bb8 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, void (base::BaseTimerTaskInternal\*), void (base::internal::OwnedWrapper[base::BaseTimerTaskInternal](javascript:void(0);))>, void (base::BaseTimerTaskInternal\*)>::Run(base::internal::BindStateBase\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:1170  

#25 0x7fde45bce263 in MessageLoop::RunTask(base::PendingTask const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:459  

#26 0x7fde45bcea54 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:470  

#27 0x7fde45bcee0e in MessageLoop::DoWork() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:647  

#28 0x7fde45bdb1ee in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_pump\_default.cc:28  

#29 0x7fde45bcda7c in MessageLoop::RunInternal() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:418  

#30 0x7fde45bcc758 in MessageLoop::Run() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:301  

#31 0x7fde49973a3e in RendererMain(content::MainFunctionParams const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/renderer/renderer\_main.cc:281  

#32 0x7fde45afd9c4 in RunZygote /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main\_runner.cc:246  

#33 0x7fde45afd50d in RunNamedProcessTypeMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main\_runner.cc:291  

#34 0x7fde45afceac in (anonymous namespace)::ContentMainRunnerImpl::Run() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main\_runner.cc:520  

#35 0x7fde45afc1cf in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main.cc:35  

#36 0x7fde448970e7 in ChromeMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/chrome/app/chrome\_main.cc:32  

#37 0x7fde4489704b in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#38 0x7fde3d8e330d in \_\_libc\_start\_main /build/buildd/eglibc-2.13/csu/libc-start.c:258  

==15760== ABORTING  

Stats: 4934M malloced (4640M for red zones) by 4140976 calls  

Stats: 1233M realloced by 412434 calls  

Stats: 4920M freed by 4012794 calls  

Stats: 4786M really freed by 3912600 calls  

Stats: 472M (120922 full pages) mmaped in 118 calls  

mmaps by size class: 8:229362; 9:32764; 10:20475; 11:10235; 12:7168; 13:3072; 14:2560; 15:2432; 16:640; 17:192; 18:176; 19:144; 20:4; 21:2; 22:1;  

mallocs by size class: 8:2740121; 9:492788; 10:304389; 11:217712; 12:160087; 13:83350; 14:61929; 15:56939; 16:12850; 17:3366; 18:4178; 19:3251; 20:8; 21:7; 22:1;  

frees by size class: 8:2624628; 9:488577; 10:296331; 11:217493; 12:159984; 13:83307; 14:61908; 15:56931; 16:12831; 17:3361; 18:4176; 19:3251; 20:8; 21:7; 22:1;  

rfrees by size class: 8:2561902; 9:477896; 10:288054; 11:210242; 12:154782; 13:81114; 14:60138; 15:55422; 16:12534; 17:3274; 18:4064; 19:3164; 20:7; 21:6; 22:1;  

Stats: malloc large: 10811 small slow: 70058  

Shadow byte and word:  

0x1ffbc2bff312: fb  

0x1ffbc2bff310: 00 04 fb fb fb fb fb fb  

More shadow bytes:  

0x1ffbc2bff2f0: 00 00 00 00 00 00 00 00  

0x1ffbc2bff2f8: fb fb fb fb fb fb fb fb  

0x1ffbc2bff300: fa fa fa fa fa fa fa fa  

0x1ffbc2bff308: fa fa fa fa fa fa fa fa  

=>0x1ffbc2bff310: 00 04 fb fb fb fb fb fb  

0x1ffbc2bff318: fb fb fb fb fb fb fb fb  

0x1ffbc2bff320: fa fa fa fa fa fa fa fa  

0x1ffbc2bff328: fa fa fa fa fa fa fa fa  

0x1ffbc2bff330: 00 00 00 00 00 00 fb fb  

Killed

## Attachments

- [sparky-heap-buffer-overflow-034.ogv](attachments/sparky-heap-buffer-overflow-034.ogv) (application/ogg; charset=binary, 17.2 KB)
- [overflow.zip](attachments/overflow.zip) (application/zip; charset=binary, 14.3 KB)

## Timeline

### js...@chromium.org (2012-04-15)

The report looks bad, but I fed it to clusterfuzz with an autoplay and loop wrapper, and didn't see a repro: https://cluster-fuzz.appspot.com/testcase?key=36251848

I'll leave untriaged and take a closer look tomorrow.

### in...@chromium.org (2012-04-16)

That type="video/ogg" was causing issues. I fixed it, and now uploading to CF.

### sc...@gmail.com (2012-04-16)

Dale, this looks really similar to https://crbug.com/chromium/116927. Would you mind taking a look? Is it possible that we lost an ffmpeg patch in a recent roll?

### da...@chromium.org (2012-04-16)

Looking. Need to get a better stack trace. We definitely didn't lose any patches.

### in...@chromium.org (2012-04-16)

Here is your better stacktrace. It reproduces fine locally, but can you guys help us figure out from repro that why it might not be reproducing in a headless vm (ClusterFuzz) . Does it use any of accelerated stuff ? This is needed so that we get adequate fuzzing coverage on ClusterFuzz.

=================================================================
==7072== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fbd4e8bc37c at pc 0x7fbd4e53d63b bp 0x7fbd48892790 sp 0x7fbd48892788
WRITE of size 4 at 0x7fbd4e8bc37c thread T22
    #0 0x7fbd4e53d63b in ogg_read_seek chrome-asan/src/third_party/ffmpeg/libavformat/oggdec.c:711
    #1 0x7fbd4e559bf7 in av_seek_frame chrome-asan/src/third_party/ffmpeg/libavformat/utils.c:1772
    #2 0x7fbd757033e1 in media::FFmpegDemuxer::SeekTask(base::TimeDelta, base::Callback<void (media::PipelineStatus)> const&) chrome-asan/src/media/filters/ffmpeg_demuxer.cc:605
    #3 0x7fbd757090f9 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (media::FFmpegDemuxer::*)(base::TimeDelta, base::Callback<void (media::PipelineStatus)> const&)>, void (media::FFmpegDemuxer* const&, base::TimeDelta const&, base::Callback<void (media::PipelineStatus)> const&)>::MakeItSo(base::internal::RunnableAdapter<void (media::FFmpegDemuxer::*)(base::TimeDelta, base::Callback<void (media::PipelineStatus)> const&)>, media::FFmpegDemuxer* const&, base::TimeDelta const&, base::Callback<void (media::PipelineStatus)> const&) chrome-asan/src/./base/bind_internal.h:927
    #4 0x7fbd7119ffa3 in MessageLoop::RunTask(base::PendingTask const&) chrome-asan/src/base/message_loop.cc:459
    #5 0x7fbd711a0704 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) chrome-asan/src/base/message_loop.cc:470
    #6 0x7fbd711a0abe in MessageLoop::DoWork() chrome-asan/src/base/message_loop.cc:647
    #7 0x7fbd711acd3e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) chrome-asan/src/base/message_pump_default.cc:28
    #8 0x7fbd7119f7bc in MessageLoop::RunInternal() chrome-asan/src/base/message_loop.cc:418
    #9 0x7fbd7119e4a8 in MessageLoop::Run() chrome-asan/src/base/message_loop.cc:301
    #10 0x7fbd71214868 in base::Thread::ThreadMain() chrome-asan/src/base/threading/thread.cc:164
    #11 0x7fbd712097dc in ThreadFunc chrome-asan/src/base/threading/platform_thread_posix.cc:65
    #12 0x7fbd75fce44f in __asan::AsanThread::ThreadStart() ??:0
0x7fbd4e8bc37c is located 260 bytes to the left of 480-byte region [0x7fbd4e8bc480,0x7fbd4e8bc660)
freed by thread T16 here:
    #0 0x7fbd75fd1b42 in operator delete(void*) ??:0
    #1 0x7fbd711a6462 in std::deque<base::PendingTask, std::allocator<base::PendingTask> >::_M_pop_front_aux() /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/deque.tcc:446
    #2 0x7fbd711a0aa3 in MessageLoop::DoWork() chrome-asan/src/base/message_loop.cc:641
    #3 0x7fbd711acd3e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) chrome-asan/src/base/message_pump_default.cc:28
    #4 0x7fbd7119f7bc in MessageLoop::RunInternal() chrome-asan/src/base/message_loop.cc:418
    #5 0x7fbd7119e4a8 in MessageLoop::Run() chrome-asan/src/base/message_loop.cc:301
    #6 0x7fbd71214868 in base::Thread::ThreadMain() chrome-asan/src/base/threading/thread.cc:164
    #7 0x7fbd712097dc in ThreadFunc chrome-asan/src/base/threading/platform_thread_posix.cc:65
    #8 0x7fbd75fce44f in __asan::AsanThread::ThreadStart() ??:0
previously allocated by thread T22 here:
    #0 0x7fbd75fd19c2 in operator new(unsigned long) ??:0
    #1 0x7fbd711a42b2 in std::deque<base::PendingTask, std::allocator<base::PendingTask> >::_M_push_back_aux(base::PendingTask const&) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/deque.tcc:369
    #2 0x7fbd7119dcce in MessageLoop::AddToIncomingQueue(base::PendingTask*) chrome-asan/src/base/message_loop.cc:590
    #3 0x7fbd7119df09 in MessageLoop::PostDelayedTask(tracked_objects::Location const&, base::Callback<void ()> const&, long) chrome-asan/src/base/message_loop.cc:266
    #4 0x7fbd7119dfee in MessageLoop::PostDelayedTask(tracked_objects::Location const&, base::Callback<void ()> const&, base::TimeDelta) chrome-asan/src/base/message_loop.cc:273
    #5 0x7fbd711ac433 in base::MessageLoopProxyImpl::PostTaskHelper(tracked_objects::Location const&, base::Callback<void ()> const&, base::TimeDelta, bool) chrome-asan/src/base/message_loop_proxy_impl.cc:93
    #6 0x7fbd711ac36f in base::MessageLoopProxyImpl::PostDelayedTask(tracked_objects::Location const&, base::Callback<void ()> const&, base::TimeDelta) chrome-asan/src/base/message_loop_proxy_impl.cc:37
    #7 0x7fbd711ac2dd in base::MessageLoopProxyImpl::PostDelayedTask(tracked_objects::Location const&, base::Callback<void ()> const&, long) chrome-asan/src/base/message_loop_proxy_impl.cc:21
    #8 0x7fbd71208a34 in base::TaskRunner::PostTask(tracked_objects::Location const&, base::Callback<void ()> const&) chrome-asan/src/base/task_runner.cc:45
    #9 0x7fbd7427c9a2 in webkit_media::WebMediaPlayerProxy::NetworkEventCallback(media::NetworkEvent) chrome-asan/src/webkit/media/webmediaplayer_proxy.cc:110
    #10 0x7fbd742776a8 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (webkit_media::WebMediaPlayerProxy::*)(media::NetworkEvent)>, void (webkit_media::WebMediaPlayerProxy* const&, media::NetworkEvent const&)>::MakeItSo(base::internal::RunnableAdapter<void (webkit_media::WebMediaPlayerProxy::*)(media::NetworkEvent)>, webkit_media::WebMediaPlayerProxy* const&, media::NetworkEvent const&) chrome-asan/src/./base/bind_internal.h:897
    #11 0x7fbd756d4a54 in media::Pipeline::NotifyNetworkEventTask(media::NetworkEvent) chrome-asan/src/media/base/pipeline.cc:908
    #12 0x7fbd756db4c5 in media::Pipeline::NotifyCanPlayThrough() chrome-asan/src/media/base/pipeline.cc:1369
    #13 0x7fbd756de6cc in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (media::Pipeline::*)()>, void (media::Pipeline* const&)>::MakeItSo(base::internal::RunnableAdapter<void (media::Pipeline::*)()>, media::Pipeline* const&) chrome-asan/src/./base/bind_internal.h:869
    #14 0x7fbd7119ffa3 in MessageLoop::RunTask(base::PendingTask const&) chrome-asan/src/base/message_loop.cc:459
    #15 0x7fbd711a0704 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) chrome-asan/src/base/message_loop.cc:470
    #16 0x7fbd711a0abe in MessageLoop::DoWork() chrome-asan/src/base/message_loop.cc:647
    #17 0x7fbd711acd3e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) chrome-asan/src/base/message_pump_default.cc:28
    #18 0x7fbd7119f7bc in MessageLoop::RunInternal() chrome-asan/src/base/message_loop.cc:418
    #19 0x7fbd7119e4a8 in MessageLoop::Run() chrome-asan/src/base/message_loop.cc:301
    #20 0x7fbd71214868 in base::Thread::ThreadMain() chrome-asan/src/base/threading/thread.cc:164
    #21 0x7fbd712097dc in ThreadFunc chrome-asan/src/base/threading/platform_thread_posix.cc:65
    #22 0x7fbd75fce44f in __asan::AsanThread::ThreadStart() ??:0
Thread T22 created by T16 here:
    #0 0x7fbd75fc6eb5 in pthread_create ??:0
    #1 0x7fbd712093ac in CreateThread chrome-asan/src/base/threading/platform_thread_posix.cc:127
    #2 0x7fbd7120929d in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) chrome-asan/src/base/threading/platform_thread_posix.cc:249
    #3 0x7fbd712141c5 in base::Thread::StartWithOptions(base::Thread::Options const&) chrome-asan/src/base/threading/thread.cc:72
    #4 0x7fbd7121402f in base::Thread::Start() chrome-asan/src/base/threading/thread.cc:61
    #5 0x7fbd756cb8a6 in media::MessageLoopFactory::GetThread(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) chrome-asan/src/media/base/message_loop_factory.cc:42
    #6 0x7fbd756cb659 in media::MessageLoopFactory::GetMessageLoop(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) chrome-asan/src/media/base/message_loop_factory.cc:24
    #7 0x7fbd7426e15b in WebMediaPlayerImpl chrome-asan/src/webkit/media/webmediaplayer_impl.cc:130
    #8 0x7fbd74ed4cf5 in RenderViewImpl::createMediaPlayer(WebKit::WebFrame*, WebKit::WebMediaPlayerClient*) chrome-asan/src/content/renderer/render_view_impl.cc:2237
    #9 0x7fbd72537548 in createWebMediaPlayer chrome-asan/src/third_party/WebKit/Source/WebKit/chromium/src/WebMediaPlayerClientImpl.cpp:56
    #10 0x7fbd725372d2 in WebKit::WebMediaPlayerClientImpl::loadInternal() chrome-asan/src/third_party/WebKit/Source/WebKit/chromium/src/WebMediaPlayerClientImpl.cpp:298
    #11 0x7fbd7253708b in WebKit::WebMediaPlayerClientImpl::load(WTF::String const&) chrome-asan/src/third_party/WebKit/Source/WebKit/chromium/src/WebMediaPlayerClientImpl.cpp:288
    #12 0x7fbd72bdd916 in WebCore::MediaPlayer::loadWithNextMediaEngine(WebCore::MediaPlayerFactory*) chrome-asan/src/third_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.cpp:415
    #13 0x7fbd72bdd032 in WebCore::MediaPlayer::load(WebCore::KURL const&, WebCore::ContentType const&, WTF::String const&) chrome-asan/src/third_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.cpp:373
    #14 0x7fbd729d8c0a in WebCore::HTMLMediaElement::loadResource(WebCore::KURL const&, WebCore::ContentType&, WTF::String const&) chrome-asan/src/third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:971
    #15 0x7fbd729d4e1c in WebCore::HTMLMediaElement::loadNextSourceChild() chrome-asan/src/third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:872
    #16 0x7fbd729d8209 in WebCore::HTMLMediaElement::selectMediaResource() chrome-asan/src/third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:852
    #17 0x7fbd729d5180 in WebCore::HTMLMediaElement::loadInternal() chrome-asan/src/third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:780
    #18 0x7fbd729cfc43 in WebCore::HTMLMediaElement::loadTimerFired(WebCore::Timer<WebCore::HTMLMediaElement>*) chrome-asan/src/third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:591
    #19 0x7fbd72b61db8 in WebCore::ThreadTimers::sharedTimerFiredInternal() chrome-asan/src/third_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118
    #20 0x7fbd741a3a7d in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, void (webkit_glue::WebKitPlatformSupportImpl*)>::MakeItSo(base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, webkit_glue::WebKitPlatformSupportImpl*) chrome-asan/src/./base/bind_internal.h:869
    #21 0x7fbd741a38ad in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (webkit_glue::WebKitPlatformSupportImpl::*)()>, void (webkit_glue::WebKitPlatformSupportImpl*), void (base::internal::UnretainedWrapper<webkit_glue::WebKitPlatformSupportImpl>)>, void (webkit_glue::WebKitPlatformSupportImpl*)>::Run(base::internal::BindStateBase*) chrome-asan/src/./base/bind_internal.h:1170
    #22 0x7fbd7121832a in base::Timer::RunScheduledTask() chrome-asan/src/base/timer.cc:182
    #23 0x7fbd7121893d in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, void (base::BaseTimerTaskInternal*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, base::BaseTimerTaskInternal*) chrome-asan/src/./base/bind_internal.h:869
    #24 0x7fbd712187f8 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::*)()>, void (base::BaseTimerTaskInternal*), void (base::internal::OwnedWrapper<base::BaseTimerTaskInternal>)>, void (base::BaseTimerTaskInternal*)>::Run(base::internal::BindStateBase*) chrome-asan/src/./base/bind_internal.h:1170
    #25 0x7fbd7119ffa3 in MessageLoop::RunTask(base::PendingTask const&) chrome-asan/src/base/message_loop.cc:459
    #26 0x7fbd711a0704 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) chrome-asan/src/base/message_loop.cc:470
    #27 0x7fbd711a0abe in MessageLoop::DoWork() chrome-asan/src/base/message_loop.cc:647
    #28 0x7fbd711acd3e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) chrome-asan/src/base/message_pump_default.cc:28
    #29 0x7fbd7119f7bc in MessageLoop::RunInternal() chrome-asan/src/base/message_loop.cc:418
    #30 0x7fbd7119e4a8 in MessageLoop::Run() chrome-asan/src/base/message_loop.cc:301
    #31 0x7fbd71214868 in base::Thread::ThreadMain() chrome-asan/src/base/threading/thread.cc:164
    #32 0x7fbd712097dc in ThreadFunc chrome-asan/src/base/threading/platform_thread_posix.cc:65
    #33 0x7fbd75fce44f in __asan::AsanThread::ThreadStart() ??:0
Thread T16 created by T0 here:
    #0 0x7fbd75fc6eb5 in pthread_create ??:0
    #1 0x7fbd712093ac in CreateThread chrome-asan/src/base/threading/platform_thread_posix.cc:127
    #2 0x7fbd7120929d in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) chrome-asan/src/base/threading/platform_thread_posix.cc:249
    #3 0x7fbd712141c5 in base::Thread::StartWithOptions(base::Thread::Options const&) chrome-asan/src/base/threading/thread.cc:72
    #4 0x7fbd748115dc in RenderProcessHostImpl::Init() chrome-asan/src/content/browser/renderer_host/render_process_host_impl.cc:416
    #5 0x7fbd74827a22 in content::RenderViewHostImpl::CreateRenderView(std::basic_string<unsigned short, base::string16_char_traits, std::allocator<unsigned short> > const&, int) chrome-asan/src/content/browser/renderer_host/render_view_host_impl.cc:212
    #6 0x7fbd748f0fe9 in WebContentsImpl::CreateRenderViewForRenderManager(content::RenderViewHost*) chrome-asan/src/content/browser/web_contents/web_contents_impl.cc:2562
    #7 0x7fbd748f113d in non-virtual thunk to WebContentsImpl::CreateRenderViewForRenderManager(content::RenderViewHost*) ???:0
    #8 0x7fbd74a878de in RenderViewHostManager::InitRenderView(content::RenderViewHost*, content::NavigationEntryImpl const&) chrome-asan/src/content/browser/web_contents/render_view_host_manager.cc:584
    #9 0x7fbd74a8691c in RenderViewHostManager::Navigate(content::NavigationEntryImpl const&) chrome-asan/src/content/browser/web_contents/render_view_host_manager.cc:121
    #10 0x7fbd748e7022 in WebContentsImpl::NavigateToEntry(content::NavigationEntryImpl const&, content::NavigationController::ReloadType) chrome-asan/src/content/browser/web_contents/web_contents_impl.cc:1066
    #11 0x7fbd748e6f27 in WebContentsImpl::NavigateToPendingEntry(content::NavigationController::ReloadType) chrome-asan/src/content/browser/web_contents/web_contents_impl.cc:1053
    #12 0x7fbd748ce249 in NavigationControllerImpl::NavigateToPendingEntry(content::NavigationController::ReloadType) chrome-asan/src/content/browser/web_contents/navigation_controller_impl.cc:1312
    #13 0x7fbd748cebc0 in NavigationControllerImpl::LoadEntry(content::NavigationEntryImpl*) chrome-asan/src/content/browser/web_contents/navigation_controller_impl.cc:366
    #14 0x7fbd7006441f in LoadURLInContents chrome-asan/src/chrome/browser/ui/browser_navigator.cc:280
    #15 0x7fbd7006241d in browser::Navigate(browser::NavigateParams*) chrome-asan/src/chrome/browser/ui/browser_navigator.cc:562
    #16 0x7fbd7004a945 in BrowserInit::LaunchWithProfile::OpenTabsInBrowser(Browser*, bool, std::vector<BrowserInit::LaunchWithProfile::Tab, std::allocator<BrowserInit::LaunchWithProfile::Tab> > const&) chrome-asan/src/chrome/browser/ui/browser_init.cc:1295
    #17 0x7fbd70048d30 in BrowserInit::LaunchWithProfile::ProcessSpecifiedURLs(std::vector<GURL, std::allocator<GURL> > const&) chrome-asan/src/chrome/browser/ui/browser_init.cc:1203
    #18 0x7fbd700488ef in BrowserInit::LaunchWithProfile::ProcessStartupURLs(std::vector<GURL, std::allocator<GURL> > const&) chrome-asan/src/chrome/browser/ui/browser_init.cc:1159
    #19 0x7fbd70047afd in BrowserInit::LaunchWithProfile::ProcessLaunchURLs(bool, std::vector<GURL, std::allocator<GURL> > const&) chrome-asan/src/chrome/browser/ui/browser_init.cc:1080
    #20 0x7fbd70046433 in BrowserInit::LaunchWithProfile::Launch(Profile*, std::vector<GURL, std::allocator<GURL> > const&, bool) chrome-asan/src/chrome/browser/ui/browser_init.cc:923
    #21 0x7fbd70045524 in BrowserInit::LaunchBrowser(CommandLine const&, Profile*, FilePath const&, BrowserInit::IsProcessStartup, BrowserInit::IsFirstRun, int*) chrome-asan/src/chrome/browser/ui/browser_init.cc:744
    #22 0x7fbd7004d1a1 in BrowserInit::ProcessCmdLineImpl(CommandLine const&, FilePath const&, bool, Profile*, std::vector<Profile*, std::allocator<Profile*> > const&, int*, BrowserInit*) chrome-asan/src/chrome/browser/ui/browser_init.cc:1841
    #23 0x7fbd70c33d0c in BrowserInit::Start(CommandLine const&, FilePath const&, Profile*, std::vector<Profile*, std::allocator<Profile*> > const&, int*) chrome-asan/src/./chrome/browser/ui/browser_init.h:54
    #24 0x7fbd70c32596 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome-asan/src/chrome/browser/chrome_browser_main.cc:1748
    #25 0x7fbd70c3115a in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome-asan/src/chrome/browser/chrome_browser_main.cc:1336
    #26 0x7fbd746ba738 in content::BrowserMainLoop::CreateThreads() chrome-asan/src/content/browser/browser_main_loop.cc:434
    #27 0x7fbd746bce9d in (anonymous namespace)::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) chrome-asan/src/content/browser/browser_main_runner.cc:82
    #28 0x7fbd746b87a2 in BrowserMain(content::MainFunctionParams const&) chrome-asan/src/content/browser/browser_main.cc:17
    #29 0x7fbd710cf60e in RunNamedProcessTypeMain chrome-asan/src/content/app/content_main_runner.cc:283
    #30 0x7fbd710cefdc in (anonymous namespace)::ContentMainRunnerImpl::Run() chrome-asan/src/content/app/content_main_runner.cc:520
    #31 0x7fbd710ce2ff in content::ContentMain(int, char const**, content::ContentMainDelegate*) chrome-asan/src/content/app/content_main.cc:35
    #32 0x7fbd6fe642e7 in ChromeMain chrome-asan/src/chrome/app/chrome_main.cc:32
    #33 0x7fbd6fe6424b in main chrome-asan/src/chrome/app/chrome_exe_main_gtk.cc:18
    #34 0x7fbd68f51c4d in ?? ??:0
==7072== ABORTING
Stats: 121M malloced (138M for red zones) by 334602 calls
Stats: 5M realloced by 13363 calls
Stats: 94M freed by 248069 calls
Stats: 0M really freed by 0 calls
Stats: 304M (77868 full pages) mmaped in 75 calls
  mmaps   by size class: 8:311277; 9:24573; 10:16380; 11:10235; 12:4096; 13:2560; 14:1280; 15:384; 16:448; 17:96; 18:32; 19:48; 20:16; 22:4; 23:1;
  mallocs by size class: 8:292313; 9:14422; 10:13327; 11:7692; 12:2876; 13:2103; 14:1009; 15:294; 16:405; 17:79; 18:20; 19:41; 20:16; 22:4; 23:1;
  frees   by size class: 8:215406; 9:11189; 10:12274; 11:3310; 12:2492; 13:1929; 14:804; 15:192; 16:360; 17:65; 18:12; 19:18; 20:13; 22:4; 23:1;
  rfrees  by size class:
Stats: malloc large: 161 small slow: 1576
Shadow byte and word:
  0x1ff7a9d1786f: fa
  0x1ff7a9d17868: fa fa fa fa fa fa fa fa
More shadow bytes:
  0x1ff7a9d17848: fb fb fb fb fb fb fb fb
  0x1ff7a9d17850: fa fa fa fa fa fa fa fa
  0x1ff7a9d17858: fa fa fa fa fa fa fa fa
  0x1ff7a9d17860: fa fa fa fa fa fa fa fa
=>0x1ff7a9d17868: fa fa fa fa fa fa fa fa
  0x1ff7a9d17870: fa fa fa fa fa fa fa fa
  0x1ff7a9d17878: fa fa fa fa fa fa fa fa
  0x1ff7a9d17880: fa fa fa fa fa fa fa fa
  0x1ff7a9d17888: fa fa fa fa fa fa fa fa


### da...@chromium.org (2012-04-16)

[Comment Deleted]

### da...@chromium.org (2012-04-16)

Trace is off, actual problem is on line 708. The problem is ogg_read_seek is trying to write to a stream which doesn't exist:

 704     // Try seeking to a keyframe first. If this fails (very possible),
 705     // av_seek_frame will fall back to ignoring keyframes
 706     if (s->streams[stream_index]->codec->codec_type == AVMEDIA_TYPE_VIDEO
 707         && !(flags & AVSEEK_FLAG_ANY))
 708         os->keyframe_seek = 1;

ogg->nstreams == 1, and stream_index == 1, so os = ogg->streams + stream_index is OOB. Have temp fix, but will send to upstream FFmpeg to ensure this is the right fix first.

### in...@chromium.org (2012-04-16)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-04-16)

To clarify, this traces back to Chrome 17 at least and, as far as I can tell, at worst we're writing a 1 or 0 OOB.

### sc...@gmail.com (2012-04-16)

Most any OOB write is painful :(

### da...@chromium.org (2012-04-18)

The change is in the try bots right now for M20. M19 will just needs the DEPS updated once that lands.

If you want to land this in M18 though it's going to be a little trickier since we switched over to the new FFmpeg repository w/ M19.  I'll need update the M18 source branch and build M18 era DLLs for Windows. Over chat inferno indicated landing in M19 was sufficient. Is this still the case? Please move to Mstone-19 if so.

### sc...@gmail.com (2012-04-18)

Yeah, M19 is fine if that makes your life easier.

### bu...@chromium.org (2012-04-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=132822

------------------------------------------------------------------------
r132822 | dalecurtis@google.com | Wed Apr 18 11:07:00 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=132822&r2=132821&pathrev=132822
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/ffmpeg/ffmpeg_regression_tests.cc?r1=132822&r2=132821&pathrev=132822

Roll DEPS for new ffmpeg binaries. Add regression test.

Pulls in the following patches:
69a5a2e Update README, roll new FFmpeg binaries for Windows.
317085d oggdec: Safety check against stream counts being inconsistent in seek()
0d3e542 oggdec: Recreate streams only in the 1 stream case.
f1dea64 Update sigs to allow us to prevent ID3v1 tag reads.

ffmpeg_revision:
http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/?view=log

ffmpeg_hash:
http://git.chromium.org/gitweb/?p=chromium/third_party/ffmpeg.git;a=commit;h=HEAD

BUG=123481
TEST=ffmpeg_regression_tests + asan/valgrind.
TBR=scherkus

Review URL: https://chromiumcodereview.appspot.com/10021045
------------------------------------------------------------------------

### in...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-04-20)

Looks like this was stable in M20, M19 deps need to be rolled.  scarybeasts indicated that you guys would take of that, but I don't see it changed.  Need me to roll the deps or are you guys going to do it?

### sc...@gmail.com (2012-04-21)

Oh, sorry for the misunderstanding. We don't handle ffmpeg merges because it's a bit of a black art, what with the need to produce Windows binaries on top of the code merge itself.

Would you be so kind as to get this fix to M19 branch for us?

### da...@chromium.org (2012-04-23)

Sure, this one's just a DEPS roll, no black art required. :)

### da...@chromium.org (2012-04-23)

Landed, https://chromereviews.googleplex.com/4333013

### sc...@gmail.com (2012-04-24)

Thanks Dale, this includes the source change on the branch needed for e.g. Linux builds too, right?

### da...@chromium.org (2012-04-24)

Yup.

### in...@chromium.org (2012-04-24)

Great find @Heikkinenhannu. We hope that you continue this streak of finding awesome bugs. This qualifies for $1000 Chromium Security Reward.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2012-04-24)

@heikkinenhannu: thanks! BTW -- use of ASAN and a Finnish-sounding handle, you're not related to Team Oulu are you? :)

(And related, what exact name / affiliation would you like credited in our release notes?)

### he...@gmail.com (2012-04-24)

I have a friend who works at OUSPG and his success inspired me to try it myself.

I would like to be credited just my name Hannu Heikkinen

### sc...@gmail.com (2012-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

### al...@chromium.org (2012-05-16)

[Comment Deleted]

### sc...@gmail.com (2012-07-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=24176

------------------------------------------------------------------------
r24176 | dalecurtis@google.com | 2012-04-23T17:54:43.756857Z

------------------------------------------------------------------------

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/123481?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056732)*
