# Security: TSAN: data race in media::FFmpegDemuxer::~FFmpegDemuxer

| Field | Value |
|-------|-------|
| **Issue ID** | [40084517](https://issues.chromium.org/issues/40084517) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media |
| **Reporter** | cl...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2016-06-09 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The latest tsan build of chrome crashes as follows:

==================  

WARNING: ThreadSanitizer: data race (pid=5586)  

Write of size 1 at 0x7d040001c205 by main thread:  

#0 Invalidate base/memory/weak\_ptr.cc:22:13 (content\_shell+0x000000555d7e)  

#1 Invalidate base/memory/weak\_ptr.cc:64 (content\_shell+0x000000555d7e)  

#2 base::internal::WeakReferenceOwner::~WeakReferenceOwner() base/memory/weak\_ptr.cc:51 (content\_shell+0x000000555d7e)  

#3 ~WeakPtrFactory base/memory/weak\_ptr.h:285:39 (content\_shell+0x000004dc6d14)  

#4 media::FFmpegDemuxer::~FFmpegDemuxer() media/filters/ffmpeg\_demuxer.cc:789 (content\_shell+0x000004dc6d14)  

#5 media::FFmpegDemuxer::~FFmpegDemuxer() media/filters/ffmpeg\_demuxer.cc:789:33 (content\_shell+0x000004dc6f29)  

#6 operator() buildtools/third\_party/libc++/trunk/include/memory:2529:13 (content\_shell+0x00000428a908)  

#7 reset buildtools/third\_party/libc++/trunk/include/memory:2735 (content\_shell+0x00000428a908)  

#8 ~unique\_ptr buildtools/third\_party/libc++/trunk/include/memory:2703 (content\_shell+0x00000428a908)  

#9 media::WebMediaPlayerImpl::~WebMediaPlayerImpl() media/blink/webmediaplayer\_impl.cc:263 (content\_shell+0x00000428a908)  

#10 media::WebMediaPlayerImpl::~WebMediaPlayerImpl() media/blink/webmediaplayer\_impl.cc:232:43 (content\_shell+0x00000428aac9)  

#11 deletePtr third\_party/WebKit/Source/wtf/OwnPtrCommon.h:54:9 (content\_shell+0x0000027cd583)  

#12 reset third\_party/WebKit/Source/wtf/OwnPtr.h:110 (content\_shell+0x0000027cd583)  

#13 clearMediaPlayerAndAudioSourceProviderClientWithoutLocking third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:3134 (content\_shell+0x0000027cd583)  

#14 blink::HTMLMediaElement::clearMediaPlayer() third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:3148 (content\_shell+0x0000027cd583)  

#15 blink::HTMLMediaElement::stop() third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:3176:5 (content\_shell+0x0000027cd751)  

#16 non-virtual thunk to blink::HTMLMediaElement::stop() third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:3167:24 (content\_shell+0x0000027cd9a0)  

#17 blink::ContextLifecycleNotifier::notifyStoppingActiveDOMObjects() third\_party/WebKit/Source/core/dom/ContextLifecycleNotifier.cpp:97:30 (content\_shell+0x00000266ae58)  

#18 blink::ExecutionContext::stopActiveDOMObjects() third\_party/WebKit/Source/core/dom/ExecutionContext.cpp:88:5 (content\_shell+0x0000025602d6)  

#19 blink::Document::detach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Document.cpp:2151:5 (content\_shell+0x00000250d5c0)  

#20 blink::FrameLoader::prepareForCommit() third\_party/WebKit/Source/core/loader/FrameLoader.cpp:1123:30 (content\_shell+0x000002d073ef)  

#21 blink::FrameLoader::commitProvisionalLoad() third\_party/WebKit/Source/core/loader/FrameLoader.cpp:1140:10 (content\_shell+0x000002d07640)  

#22 commitIfReady third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:249:24 (content\_shell+0x000002ce77ce)  

#23 blink::DocumentLoader::processData(char const\*, unsigned long) third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:523 (content\_shell+0x000002ce77ce)  

#24 blink::DocumentLoader::dataReceived(blink::Resource\*, char const\*, unsigned long) third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:501:5 (content\_shell+0x000002ce7645)  

#25 blink::RawResource::appendData(char const\*, unsigned long) third\_party/WebKit/Source/core/fetch/RawResource.cpp:100:12 (content\_shell+0x000002b7135a)  

#26 blink::ResourceLoader::didReceiveData(blink::WebURLLoader\*, char const\*, int, int) third\_party/WebKit/Source/core/fetch/ResourceLoader.cpp:199:17 (content\_shell+0x000002b8fcfa)  

#27 content::WebURLLoaderImpl::Context::OnReceivedData(std::\_\_1::unique\_ptr<content::RequestPeer::ReceivedData, std::\_\_1::default\_delete[content::RequestPeer::ReceivedData](javascript:void(0);) >) content/child/web\_url\_loader\_impl.cc:717:14 (content\_shell+0x00000586c5eb)  

#28 content::WebURLLoaderImpl::RequestPeerImpl::OnReceivedData(std::\_\_1::unique\_ptr<content::RequestPeer::ReceivedData, std::\_\_1::default\_delete[content::RequestPeer::ReceivedData](javascript:void(0);) >) content/child/web\_url\_loader\_impl.cc:894:13 (content\_shell+0x00000586d14f)  

#29 content::ResourceDispatcher::OnReceivedData(int, int, int, int) content/child/resource\_dispatcher.cc:284:25 (content\_shell+0x000003d0400c)  

#30 DispatchToMethodImpl<content::ResourceDispatcher \*, void (content::ResourceDispatcher::\*)(int, int, int, int), int, int, int, int, 0, 1, 2, 3> base/tuple.h:126:3 (content\_shell+0x000003d063dc)  

#31 DispatchToMethod<content::ResourceDispatcher \*, void (content::ResourceDispatcher::\*)(int, int, int, int), int, int, int, int> base/tuple.h:133 (content\_shell+0x000003d063dc)  

#32 DispatchToMethod<content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, int, int, int), void, std::\_\_1::tuple<int, int, int, int> > ipc/ipc\_message\_templates.h:26 (content\_shell+0x000003d063dc)  

#33 bool IPC::MessageT<ResourceMsg\_DataReceived\_Meta, std::\_\_1::tuple<int, int, int, int>, void>::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void, void (content::ResourceDispatcher::\*)(int, int, int, int)>(IPC::Message const\*, content::ResourceDispatcher\*, content::ResourceDispatcher\*, void\*, void (content::ResourceDispatcher::\*)(int, int, int, int)) ipc/ipc\_message\_templates.h:121 (content\_shell+0x000003d063dc)  

#34 content::ResourceDispatcher::DispatchMessage(IPC::Message const&) content/child/resource\_dispatcher.cc:508:5 (content\_shell+0x000003d024ea)  

#35 content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) content/child/resource\_dispatcher.cc:126:3 (content\_shell+0x000003d01cd7)  

#36 DispatchMessage content/child/resource\_scheduling\_filter.cc:99:25 (content\_shell+0x000003d08b00)  

#37 content::(anonymous namespace)::DispatchMessageTask::run() content/child/resource\_scheduling\_filter.cc:31 (content\_shell+0x000003d08b00)  

#38 scheduler::WebTaskRunnerImpl::runTask(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >) components/scheduler/child/web\_task\_runner\_impl.cc:70:9 (content\_shell+0x00000588b43d)  

#39 Run<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:160:12 (content\_shell+0x00000588b891)  

#40 MakeItSo<base::internal::RunnableAdapter<void (\*)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)> &, std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:312 (content\_shell+0x00000588b891)  

#41 base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>, void (std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >, false, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:364 (content\_shell+0x00000588b891)  

#42 Run base/callback.h:397:12 (content\_shell+0x0000005c43fd)  

#43 base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51 (content\_shell+0x0000005c43fd)  

#44 scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:289:19 (content\_shell+0x0000058962f5)  

#45 scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:201:13 (content\_shell+0x00000589496f)  

#46 Run<scheduler::TaskQueueManager \*, const base::TimeTicks &, const bool &> base/bind\_internal.h:187:12 (content\_shell+0x00000589742e)  

#47 MakeItSo<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)> &, base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:325 (content\_shell+0x00000589742e)  

#48 base::internal::Invoker<base::IndexSequence<0ul, 1ul, 2ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)>, void (scheduler::TaskQueueManager\*, base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool>, true, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:364 (content\_shell+0x00000589742e)  

#49 Run base/callback.h:397:12 (content\_shell+0x0000005c43fd)  

#50 base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51 (content\_shell+0x0000005c43fd)  

#51 base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:475:19 (content\_shell+0x000000557efb)  

#52 base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:484:5 (content\_shell+0x0000005584ad)  

#53 base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:601:13 (content\_shell+0x000000558c52)  

#54 base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:33:31 (content\_shell+0x00000055c301)  

#55 base::MessageLoop::RunHandler() base/message\_loop/message\_loop.cc:439:10 (content\_shell+0x00000055789b)  

#56 base::RunLoop::Run() base/run\_loop.cc:35:10 (content\_shell+0x000000574e87)  

#57 base::MessageLoop::Run() base/message\_loop/message\_loop.cc:294:12 (content\_shell+0x0000005570e5)  

#58 content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:199:37 (content\_shell+0x00000406a9d9)  

#59 content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:345:14 (content\_shell+0x00000052490b)  

#60 content::RunNamedProcessTypeMain(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:428:12 (content\_shell+0x00000052546f)  

#61 content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:787:12 (content\_shell+0x00000052616d)  

#62 content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:20:28 (content\_shell+0x00000052431e)  

#63 main content/shell/app/shell\_main.cc:48:10 (content\_shell+0x0000004bb4c2)

Previous read of size 1 at 0x7d040001c205 by thread T10:  

#0 IsValid base/memory/weak\_ptr.cc:28:10 (content\_shell+0x000000555cfa)  

#1 base::internal::WeakReference::is\_valid() const base/memory/weak\_ptr.cc:45 (content\_shell+0x000000555cfa)  

#2 get base/memory/weak\_ptr.h:213:32 (content\_shell+0x000004dccc48)  

#3 MakeItSo<base::internal::RunnableAdapter<void (media::FFmpegDemuxer::\*)(const base::Callback<void (media::PipelineStatus), base::internal::CopyMode::Copyable> &, int)> &, base::WeakPtr[media::FFmpegDemuxer](javascript:void(0);), const base::Callback<void (media::PipelineStatus), base::internal::CopyMode::Copyable> &, int> base/bind\_internal.h:322 (content\_shell+0x000004dccc48)  

#4 base::internal::Invoker<base::IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (media::FFmpegDemuxer::\*)(base::Callback<void (media::PipelineStatus), (base::internal::CopyMode)1> const&, int)>, void (media::FFmpegDemuxer\*, base::Callback<void (media::PipelineStatus), (base::internal::CopyMode)1> const&, int), base::WeakPtr[media::FFmpegDemuxer](javascript:void(0);), base::Callback<void (media::PipelineStatus), (base::internal::CopyMode)1> const&>, true, void (int)>::Run(base::internal::BindStateBase\*, int&&) base/bind\_internal.h:364 (content\_shell+0x000004dccc48)  

#5 Run base/callback.h:397:12 (content\_shell+0x000000c797da)  

#6 void base::internal::ReplyAdapter<int, int>(base::Callback<void (int), (base::internal::CopyMode)1> const&, int\*) base/task\_runner\_util.h:34 (content\_shell+0x000000c797da)  

#7 Run<const base::Callback<void (int), base::internal::CopyMode::Copyable> &, int \*> base/bind\_internal.h:160:12 (content\_shell+0x000000c7990c)  

#8 MakeItSo<base::internal::RunnableAdapter<void (\*)(const base::Callback<void (int), base::internal::CopyMode::Copyable> &, int \*)> &, const base::Callback<void (int), base::internal::CopyMode::Copyable> &, int \*> base/bind\_internal.h:312 (content\_shell+0x000000c7990c)  

#9 base::internal::Invoker<base::IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(base::Callback<void (int), (base::internal::CopyMode)1> const&, int\*)>, void (base::Callback<void (int), (base::internal::CopyMode)1> const&, int\*), base::Callback<void (int), (base::internal::CopyMode)1> const&, base::internal::OwnedWrapper<int> >, false, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:364 (content\_shell+0x000000c7990c)  

#10 Run base/callback.h:397:12 (content\_shell+0x000000595e0e)  

#11 base::(anonymous namespace)::PostTaskAndReplyRelay::RunReplyAndSelfDestruct() base/threading/post\_task\_and\_reply\_impl.cc:58 (content\_shell+0x000000595e0e)  

#12 Run<base::(anonymous namespace)::PostTaskAndReplyRelay \*> base/bind\_internal.h:187:12 (content\_shell+0x000000595ed5)  

#13 MakeItSo<base::internal::RunnableAdapter<void (base::(anonymous namespace)::PostTaskAndReplyRelay::\*)()> &, base::(anonymous namespace)::PostTaskAndReplyRelay \*> base/bind\_internal.h:312 (content\_shell+0x000000595ed5)  

#14 base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (base::(anonymous namespace)::PostTaskAndReplyRelay::\*)()>, void (base::(anonymous namespace)::PostTaskAndReplyRelay\*), base::internal::UnretainedWrapper<base::(anonymous namespace)::PostTaskAndReplyRelay> >, false, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:364 (content\_shell+0x000000595ed5)  

#15 Run base/callback.h:397:12 (content\_shell+0x0000005c43fd)  

#16 base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51 (content\_shell+0x0000005c43fd)  

#17 base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:475:19 (content\_shell+0x000000557efb)  

#18 base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:484:5 (content\_shell+0x0000005584ad)  

#19 base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:601:13 (content\_shell+0x000000558c52)  

#20 base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:33:31 (content\_shell+0x00000055c301)  

#21 base::MessageLoop::RunHandler() base/message\_loop/message\_loop.cc:439:10 (content\_shell+0x00000055789b)  

#22 base::RunLoop::Run() base/run\_loop.cc:35:10 (content\_shell+0x000000574e87)  

#23 base::MessageLoop::Run() base/message\_loop/message\_loop.cc:294:12 (content\_shell+0x0000005570e5)  

#24 base::Thread::Run(base::MessageLoop\*) base/threading/thread.cc:204:17 (content\_shell+0x0000005ecf59)  

#25 base::Thread::ThreadMain() base/threading/thread.cc:256:3 (content\_shell+0x0000005ed129)  

#26 base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:70:13 (content\_shell+0x00000059597d)

Location is heap block of size 8 at 0x7d040001c200 allocated by thread T10:  

#0 operator new(unsigned long) <null> (content\_shell+0x0000004bafde)  

#1 base::internal::WeakReferenceOwner::GetRef() const base/memory/weak\_ptr.cc:57:13 (content\_shell+0x000000555eac)  

#2 GetWeakPtr base/memory/weak\_ptr.h:289:45 (content\_shell+0x000004dc738e)  

#3 media::FFmpegDemuxer::Initialize(media::DemuxerHost\*, base::Callback<void (media::PipelineStatus), (base::internal::CopyMode)1> const&, bool) media/filters/ffmpeg\_demuxer.cc:825 (content\_shell+0x000004dc738e)  

#4 InitializeDemuxer media/base/pipeline\_impl.cc:918:13 (content\_shell+0x000004da32ad)  

#5 media::PipelineImpl::StateTransitionTask(media::PipelineStatus) media/base/pipeline\_impl.cc:460 (content\_shell+0x000004da32ad)  

#6 media::PipelineImpl::StartTask() media/base/pipeline\_impl.cc:611:3 (content\_shell+0x000004d9f3e6)  

#7 Run<media::PipelineImpl \*> base/bind\_internal.h:187:12 (content\_shell+0x000004da4bc3)  

#8 MakeItSo<base::internal::RunnableAdapter<void (media::PipelineImpl::\*)()> &, base::WeakPtr[media::PipelineImpl](javascript:void(0);)> base/bind\_internal.h:325 (content\_shell+0x000004da4bc3)  

#9 base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (media::PipelineImpl::\*)()>, void (media::PipelineImpl\*), base::WeakPtr[media::PipelineImpl](javascript:void(0);)&>, true, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:364 (content\_shell+0x000004da4bc3)  

#10 Run base/callback.h:397:12 (content\_shell+0x0000005c43fd)  

#11 base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51 (content\_shell+0x0000005c43fd)  

#12 base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:475:19 (content\_shell+0x000000557efb)  

#13 base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:484:5 (content\_shell+0x0000005584ad)  

#14 base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:601:13 (content\_shell+0x000000558c52)  

#15 base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:33:31 (content\_shell+0x00000055c301)  

#16 base::MessageLoop::RunHandler() base/message\_loop/message\_loop.cc:439:10 (content\_shell+0x00000055789b)  

#17 base::RunLoop::Run() base/run\_loop.cc:35:10 (content\_shell+0x000000574e87)  

#18 base::MessageLoop::Run() base/message\_loop/message\_loop.cc:294:12 (content\_shell+0x0000005570e5)  

#19 base::Thread::Run(base::MessageLoop\*) base/threading/thread.cc:204:17 (content\_shell+0x0000005ecf59)  

#20 base::Thread::ThreadMain() base/threading/thread.cc:256:3 (content\_shell+0x0000005ed129)  

#21 base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:70:13 (content\_shell+0x00000059597d)

Thread T10 'Media' (tid=5705, running) created by main thread at:  

#0 pthread\_create <null> (content\_shell+0x00000045d225)  

#1 base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadPriority) base/threading/platform\_thread\_posix.cc:109:13 (content\_shell+0x0000005956ca)  

#2 base::PlatformThread::CreateWithPriority(unsigned long, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadPriority) base/threading/platform\_thread\_posix.cc:190:10 (content\_shell+0x0000005955d5)  

#3 base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:118:10 (content\_shell+0x0000005eccd0)  

#4 base::Thread::Start() base/threading/thread.cc:88:10 (content\_shell+0x0000005ecb14)  

#5 content::RenderThreadImpl::GetMediaThreadTaskRunner() content/renderer/render\_thread\_impl.cc:1944:20 (content\_shell+0x00000402b0d3)  

#6 content::RenderFrameImpl::createMediaPlayer(blink::WebMediaPlayerSource const&, blink::WebMediaPlayerClient\*, blink::WebMediaPlayerEncryptedMediaClient\*, blink::WebContentDecryptionModule\*, blink::WebString const&, blink::WebMediaSession\*) content/renderer/render\_frame\_impl.cc:2537:54 (content\_shell+0x000004000a75)  

#7 non-virtual thunk to content::RenderFrameImpl::createMediaPlayer(blink::WebMediaPlayerSource const&, blink::WebMediaPlayerClient\*, blink::WebMediaPlayerEncryptedMediaClient\*, blink::WebContentDecryptionModule\*, blink::WebString const&, blink::WebMediaSession\*) content/renderer/render\_frame\_impl.cc:2488:41 (content\_shell+0x0000040015d0)  

#8 blink::FrameLoaderClientImpl::createWebMediaPlayer(blink::HTMLMediaElement&, blink::WebMediaPlayerSource const&, blink::WebMediaPlayerClient\*) third\_party/WebKit/Source/web/FrameLoaderClientImpl.cpp:823:41 (content\_shell+0x000001c4af3a)  

#9 blink::HTMLMediaElement::startPlayerLoad() third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:1097:50 (content\_shell+0x0000027c4a43)  

#10 blink::HTMLMediaElement::loadResource(blink::WebMediaPlayerSource const&, blink::ContentType&) third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:1044:13 (content\_shell+0x0000027c3523)  

#11 blink::HTMLMediaElement::loadSourceFromAttribute() third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:950:5 (content\_shell+0x0000027c2bb7)  

#12 blink::HTMLMediaElement::selectMediaResource() third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:906:9 (content\_shell+0x0000027c27d2)  

#13 blink::HTMLMediaElement::loadInternal() third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:853:5 (content\_shell+0x0000027c1483)  

#14 blink::HTMLMediaElement::loadTimerFired(blink::Timer[blink::HTMLMediaElement](javascript:void(0);)\*) third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:660:13 (content\_shell+0x0000027be4bc)  

#15 blink::Timer[blink::HTMLMediaElement](javascript:void(0);)::fired() third\_party/WebKit/Source/platform/Timer.h:172:9 (content\_shell+0x0000027d6166)  

#16 blink::TimerBase::runInternal() third\_party/WebKit/Source/platform/Timer.cpp:136:5 (content\_shell+0x000005335cf3)  

#17 blink::TimerBase::CancellableTimerTask::run() third\_party/WebKit/Source/platform/Timer.h:113:26 (content\_shell+0x000005335ebb)  

#18 scheduler::WebTaskRunnerImpl::runTask(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >) components/scheduler/child/web\_task\_runner\_impl.cc:70:9 (content\_shell+0x00000588b43d)  

#19 Run<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:160:12 (content\_shell+0x00000588b891)  

#20 MakeItSo<base::internal::RunnableAdapter<void (\*)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)> &, std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:312 (content\_shell+0x00000588b891)  

#21 base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>, void (std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >, false, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:364 (content\_shell+0x00000588b891)  

#22 Run base/callback.h:397:12 (content\_shell+0x0000005c43fd)  

#23 base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51 (content\_shell+0x0000005c43fd)  

#24 scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:289:19 (content\_shell+0x0000058962f5)  

#25 scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:201:13 (content\_shell+0x00000589496f)  

#26 Run<scheduler::TaskQueueManager \*, const base::TimeTicks &, const bool &> base/bind\_internal.h:187:12 (content\_shell+0x00000589742e)  

#27 MakeItSo<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)> &, base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:325 (content\_shell+0x00000589742e)  

#28 base::internal::Invoker<base::IndexSequence<0ul, 1ul, 2ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)>, void (scheduler::TaskQueueManager\*, base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool>, true, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:364 (content\_shell+0x00000589742e)  

#29 Run base/callback.h:397:12 (content\_shell+0x0000005c43fd)  

#30 base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51 (content\_shell+0x0000005c43fd)  

#31 base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:475:19 (content\_shell+0x000000557efb)  

#32 base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:484:5 (content\_shell+0x0000005584ad)  

#33 base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:601:13 (content\_shell+0x000000558c52)  

#34 base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:33:31 (content\_shell+0x00000055c301)  

#35 base::MessageLoop::RunHandler() base/message\_loop/message\_loop.cc:439:10 (content\_shell+0x00000055789b)  

#36 base::RunLoop::Run() base/run\_loop.cc:35:10 (content\_shell+0x000000574e87)  

#37 base::MessageLoop::Run() base/message\_loop/message\_loop.cc:294:12 (content\_shell+0x0000005570e5)  

#38 content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:199:37 (content\_shell+0x00000406a9d9)  

#39 content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:345:14 (content\_shell+0x00000052490b)  

#40 content::RunNamedProcessTypeMain(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:428:12 (content\_shell+0x00000052546f)  

#41 content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:787:12 (content\_shell+0x00000052616d)  

#42 content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:20:28 (content\_shell+0x00000052431e)  

#43 main content/shell/app/shell\_main.cc:48:10 (content\_shell+0x0000004bb4c2)

# SUMMARY: ThreadSanitizer: data race base/memory/weak\_ptr.cc:22:13 in Invalidate

During fuzzing with ASAN I see quite a few crashes with the following ASAN ouput. Which might have the same root cause. The testcases don't reproduce though.

=================================================================  

==20448==ERROR: AddressSanitizer: heap-use-after-free on address 0x6130003bb390 at pc 0x00000089d958 bp 0x7febc0bf5110 sp 0x7febc0bf5108  

READ of size 8 at 0x6130003bb390 thread T50 (Media)  

#0 0x89d957 in base::Thread::IsRunning() const base/threading/thread.cc:193:7  

#1 0xe0b5e56 in media::FFmpegDemuxer::OnFindStreamInfoDone(base::Callback<void (media::PipelineStatus), (base::internal::CopyMode)1> const&, int) media/filters/ffmpeg\_demuxer.cc:1066:25  

#2 0xe0c1686 in Run<media::FFmpegDemuxer \*, const base::Callback<void (media::PipelineStatus), base::internal::CopyMode::Copyable> &, int> base/bind\_internal.h:186:12  

#3 0xe0c1686 in MakeItSo<base::WeakPtr[media::FFmpegDemuxer](javascript:void(0);), const base::Callback<void (media::PipelineStatus), base::internal::CopyMode::Copyable> &, int> base/bind\_internal.h:324  

#4 0xe0c1686 in base::internal::Invoker<base::IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (media::FFmpegDemuxer::\*)(base::Callback<void (media::PipelineStatus), (base::internal::CopyMode)1> const&, int)>, void (media::FFmpegDemuxer\*, base::Callback<void (media::PipelineStatus), (base::internal::CopyMode)1> const&, int), base::WeakPtr[media::FFmpegDemuxer](javascript:void(0);), base::Callback<void (media::PipelineStatus), (base::internal::CopyMode)1> const&>, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (media::FFmpegDemuxer::\*)(base::Callback<void (media::PipelineStatus), (base::internal::CopyMode)1> const&, int)> >, void (int)>::Run(base::internal::BindStateBase\*, int&&) base/bind\_internal.h:362  

#5 0x1b4daf7 in Run base/callback.h:397:12  

#6 0x1b4daf7 in void base::internal::ReplyAdapter<int, int>(base::Callback<void (int), (base::internal::CopyMode)1> const&, int\*) base/task\_runner\_util.h:34  

#7 0x79275d in Run base/callback.h:397:12  

#8 0x79275d in base::(anonymous namespace)::PostTaskAndReplyRelay::RunReplyAndSelfDestruct() base/threading/post\_task\_and\_reply\_impl.cc:58  

#9 0x820d91 in Run base/callback.h:397:12  

#10 0x820d91 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#11 0x6d64c5 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:475:19  

#12 0x6d72ef in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:484:5  

#13 0x6d874c in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:601:13  

#14 0x6e29ed in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:33:31  

#15 0x72be29 in base::RunLoop::Run() base/run\_loop.cc:35:10  

#16 0x6d3c48 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:294:12  

#17 0x89dc9a in base::Thread::ThreadMain() base/threading/thread.cc:254:3  

#18 0x791aa0 in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:70:13  

#19 0x7fed8bf69181 in start\_thread /build/eglibc-3GlaMS/eglibc-2.19/nptl/pthread\_create.c:312

0x6130003bb390 is located 144 bytes inside of 368-byte region [0x6130003bb300,0x6130003bb470)  

freed by thread T0 (content\_shell) here:  

#0 0x50068b in operator delete(void\*) (/home/nils/fuzzer3/chrome/content\_shell+0x50068b)  

#1 0xbf16cd3 in operator() buildtools/third\_party/libc++/trunk/include/memory:2529:13  

#2 0xbf16cd3 in reset buildtools/third\_party/libc++/trunk/include/memory:2735  

#3 0xbf16cd3 in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/memory:2703  

#4 0xbf16cd3 in media::WebMediaPlayerImpl::~WebMediaPlayerImpl() media/blink/webmediaplayer\_impl.cc:263  

#5 0xbf1757a in media::WebMediaPlayerImpl::~WebMediaPlayerImpl() media/blink/webmediaplayer\_impl.cc:232:43  

#6 0x6bbb1ff in deletePtr third\_party/WebKit/Source/wtf/OwnPtrCommon.h:54:9  

#7 0x6bbb1ff in reset third\_party/WebKit/Source/wtf/OwnPtr.h:110  

#8 0x6bbb1ff in clearMediaPlayerAndAudioSourceProviderClientWithoutLocking third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:3124  

#9 0x6bbb1ff in blink::HTMLMediaElement::clearMediaPlayer() third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:3138  

#10 0x6bbb9d2 in blink::HTMLMediaElement::stop() third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:3166:5  

#11 0x67732bd in blink::ContextLifecycleNotifier::notifyStoppingActiveDOMObjects() third\_party/WebKit/Source/core/dom/ContextLifecycleNotifier.cpp:97:30  

#12 0x636ae4b in blink::Document::detach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Document.cpp:2194:5  

#13 0x7ce1551 in blink::FrameLoader::prepareForCommit() third\_party/WebKit/Source/core/loader/FrameLoader.cpp:1124:30  

#14 0x7ce1cf0 in blink::FrameLoader::commitProvisionalLoad() third\_party/WebKit/Source/core/loader/FrameLoader.cpp:1141:10  

#15 0x7c7da75 in commitIfReady third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:243:24  

#16 0x7c7da75 in blink::DocumentLoader::processData(char const\*, unsigned long) third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:517  

#17 0x7c7d70c in blink::DocumentLoader::dataReceived(blink::Resource\*, char const\*, unsigned long) third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:495:5  

#18 0x77c3d3d in blink::RawResource::appendData(char const\*, unsigned long) third\_party/WebKit/Source/core/fetch/RawResource.cpp:100:12  

#19 0x10104291 in content::WebURLLoaderImpl::Context::OnReceivedData(std::\_\_1::unique\_ptr<content::RequestPeer::ReceivedData, std::\_\_1::default\_delete[content::RequestPeer::ReceivedData](javascript:void(0);) >) content/child/web\_url\_loader\_impl.cc:716:14  

#20 0x10106653 in content::WebURLLoaderImpl::RequestPeerImpl::OnReceivedData(std::\_\_1::unique\_ptr<content::RequestPeer::ReceivedData, std::\_\_1::default\_delete[content::RequestPeer::ReceivedData](javascript:void(0);) >) content/child/web\_url\_loader\_impl.cc:893:13  

#21 0xae311e2 in content::ResourceDispatcher::OnReceivedData(int, int, int, int) content/child/resource\_dispatcher.cc:284:25  

#22 0xae394fc in DispatchToMethodImpl<content::ResourceDispatcher \*, void (content::ResourceDispatcher::\*)(int, int, int, int), int, int, int, int, 0, 1, 2, 3> base/tuple.h:166:3  

#23 0xae394fc in DispatchToMethod<content::ResourceDispatcher \*, void (content::ResourceDispatcher::\*)(int, int, int, int), int, int, int, int> base/tuple.h:173  

#24 0xae394fc in DispatchToMethod<content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, int, int, int), void, std::\_\_1::tuple<int, int, int, int> > ipc/ipc\_message\_templates.h:26  

#25 0xae394fc in bool IPC::MessageT<ResourceMsg\_DataReceived\_Meta, std::\_\_1::tuple<int, int, int, int>, void>::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void, void (content::ResourceDispatcher::\*)(int, int, int, int)>(IPC::Message const\*, content::ResourceDispatcher\*, content::ResourceDispatcher\*, void\*, void (content::ResourceDispatcher::\*)(int, int, int, int)) ipc/ipc\_message\_templates.h:121  

#26 0xae2b38b in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) content/child/resource\_dispatcher.cc:508:5  

#27 0xae29d4d in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) content/child/resource\_dispatcher.cc:126:3  

#28 0x10160a33 in Run<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:159:12  

#29 0x10160a33 in MakeItSo<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:311  

#30 0x10160a33 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>, void (std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)> >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:362  

#31 0x820d91 in Run base/callback.h:397:12  

#32 0x820d91 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#33 0x1017c0ac in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:289:19  

#34 0x10177dbc in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:201:13  

#35 0x1017e5e4 in Run<scheduler::TaskQueueManager \*, const base::TimeTicks &, const bool &> base/bind\_internal.h:186:12  

#36 0x1017e5e4 in MakeItSo<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:324  

#37 0x1017e5e4 in base::internal::Invoker<base::IndexSequence<0ul, 1ul, 2ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)>, void (scheduler::TaskQueueManager\*, base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool>, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)> >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:362  

#38 0x820d91 in Run base/callback.h:397:12  

#39 0x820d91 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#40 0x6d64c5 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:475:19  

#41 0x6d72ef in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:484:5  

#42 0x6d874c in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:601:13  

#43 0x6e29ed in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:33:31  

#44 0x72be29 in base::RunLoop::Run() base/run\_loop.cc:35:10  

#45 0x6d3c48 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:294:12

previously allocated by thread T0 (content\_shell) here:  

#0 0x5000cb in operator new(unsigned long) (/home/nils/fuzzer3/chrome/content\_shell+0x5000cb)  

#1 0xbf19f5e in media::WebMediaPlayerImpl::StartPipeline() media/blink/webmediaplayer\_impl.cc:1308:20  

#2 0xbf278e5 in Run<media::WebMediaPlayerImpl \*, bool> base/bind\_internal.h:186:12  

#3 0xbf278e5 in MakeItSo<base::WeakPtr[media::WebMediaPlayerImpl](javascript:void(0);), bool> base/bind\_internal.h:324  

#4 0xbf278e5 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (media::WebMediaPlayerImpl::\*)(bool)>, void (media::WebMediaPlayerImpl\*, bool), base::WeakPtr[media::WebMediaPlayerImpl](javascript:void(0);) >, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (media::WebMediaPlayerImpl::\*)(bool)> >, void (bool)>::Run(base::internal::BindStateBase\*, bool&&) base/bind\_internal.h:362  

#5 0x9f9da17 in Run base/callback.h:397:12  

#6 0x9f9da17 in MakeItSo<const bool &> base/bind\_internal.h:311  

#7 0x9f9da17 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::Callback<void (bool), (base::internal::CopyMode)1>, void (bool), bool&>, base::internal::InvokeHelper<false, void, base::Callback<void (bool), (base::internal::CopyMode)1> >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:362  

#8 0x820d91 in Run base/callback.h:397:12  

#9 0x820d91 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#10 0x1017c0ac in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:289:19  

#11 0x10177dbc in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:201:13  

#12 0x10180de4 in Run<scheduler::TaskQueueManager \*, const base::TimeTicks &, const bool &> base/bind\_internal.h:186:12  

#13 0x10180de4 in MakeItSo<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:324  

#14 0x10180de4 in base::internal::Invoker<base::IndexSequence<0ul, 1ul, 2ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)>, void (scheduler::TaskQueueManager\*, base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks&, bool>, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)> >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:362  

#15 0x820d91 in Run base/callback.h:397:12  

#16 0x820d91 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#17 0x6d64c5 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:475:19  

#18 0x6d72ef in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:484:5  

#19 0x6d8f32 in base::MessageLoop::DoDelayedWork(base::TimeTicks\*) base/message\_loop/message\_loop.cc:639:10  

#20 0x6e2831 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:37:27  

#21 0x72be29 in base::RunLoop::Run() base/run\_loop.cc:35:10  

#22 0x6d3c48 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:294:12  

#23 0xb8aecc1 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:199:37  

#24 0x63ad47 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:345:14  

#25 0x63f555 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:787:12  

#26 0x639acd in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:20:28  

#27 0x502222 in main content/shell/app/shell\_main.cc:48:10  

#28 0x7fed8b42eec4 in \_\_libc\_start\_main /build/eglibc-3GlaMS/eglibc-2.19/csu/libc-start.c:287

Thread T50 (Media) created by T0 (content\_shell) here:  

#0 0x4bf4b6 in \_\_interceptor\_pthread\_create (/home/nils/fuzzer3/chrome/content\_shell+0x4bf4b6)  

#1 0x791241 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadPriority) base/threading/platform\_thread\_posix.cc:109:13  

#2 0x89d13d in base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:116:10  

#3 0x89cdb0 in base::Thread::Start() base/threading/thread.cc:86:10  

#4 0xb7f2504 in content::RenderThreadImpl::GetMediaThreadTaskRunner() content/renderer/render\_thread\_impl.cc:1933:20  

#5 0xb7766bc in content::RenderFrameImpl::createMediaPlayer(blink::WebMediaPlayerSource const&, blink::WebMediaPlayerClient\*, blink::WebMediaPlayerEncryptedMediaClient\*, blink::WebContentDecryptionModule\*, blink::WebString const&, blink::WebMediaSession\*) content/renderer/render\_frame\_impl.cc:2522:54  

#6 0xb778869 in non-virtual thunk to content::RenderFrameImpl::createMediaPlayer(blink::WebMediaPlayerSource const&, blink::WebMediaPlayerClient\*, blink::WebMediaPlayerEncryptedMediaClient\*, blink::WebContentDecryptionModule\*, blink::WebString const&, blink::WebMediaSession\*) content/renderer/render\_frame\_impl.cc:2473:41  

#7 0x482f443 in blink::FrameLoaderClientImpl::createWebMediaPlayer(blink::HTMLMediaElement&, blink::WebMediaPlayerSource const&, blink::WebMediaPlayerClient\*) third\_party/WebKit/Source/web/FrameLoaderClientImpl.cpp:823:41  

#8 0x6ba1de6 in blink::HTMLMediaElement::startPlayerLoad() third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:1097:50  

#9 0x6b9d109 in blink::HTMLMediaElement::loadResource(blink::WebMediaPlayerSource const&, blink::ContentType&) third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:1044:13  

#10 0x6b9ba96 in blink::HTMLMediaElement::loadSourceFromAttribute() third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:950:5  

#11 0x6b96de9 in blink::HTMLMediaElement::loadInternal() third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:853:5  

#12 0x6b8e245 in blink::HTMLMediaElement::loadTimerFired(blink::Timer[blink::HTMLMediaElement](javascript:void(0);)\*) third\_party/WebKit/Source/core/html/HTMLMediaElement.cpp:660:13  

#13 0xefba7fd in blink::TimerBase::runInternal() third\_party/WebKit/Source/platform/Timer.cpp:136:5  

#14 0xefbadb7 in blink::TimerBase::CancellableTimerTask::run() third\_party/WebKit/Source/platform/Timer.h:113:26  

#15 0x10160a33 in Run<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:159:12  

#16 0x10160a33 in MakeItSo<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:311  

#17 0x10160a33 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>, void (std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)> >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:362  

#18 0x820d91 in Run base/callback.h:397:12  

#19 0x820d91 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#20 0x1017c0ac in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:289:19  

#21 0x10177dbc in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:201:13  

#22 0x1017e5e4 in Run<scheduler::TaskQueueManager \*, const base::TimeTicks &, const bool &> base/bind\_internal.h:186:12  

#23 0x1017e5e4 in MakeItSo<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:324  

#24 0x1017e5e4 in base::internal::Invoker<base::IndexSequence<0ul, 1ul, 2ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)>, void (scheduler::TaskQueueManager\*, base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool>, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)> >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:362  

#25 0x820d91 in Run base/callback.h:397:12  

#26 0x820d91 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#27 0x6d64c5 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:475:19  

#28 0x6d72ef in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:484:5  

#29 0x6d874c in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:601:13  

#30 0x6e29ed in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:33:31  

#31 0x72be29 in base::RunLoop::Run() base/run\_loop.cc:35:10  

#32 0x6d3c48 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:294:12  

#33 0xb8aecc1 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:199:37  

#34 0x63ad47 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:345:14  

#35 0x63f555 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:787:12  

#36 0x639acd in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:20:28  

#37 0x502222 in main content/shell/app/shell\_main.cc:48:10  

#38 0x7fed8b42eec4 in \_\_libc\_start\_main /build/eglibc-3GlaMS/eglibc-2.19/csu/libc-start.c:287

SUMMARY: AddressSanitizer: heap-use-after-free base/threading/thread.cc:193:7 in base::Thread::IsRunning() const  

Shadow bytes around the buggy address:  

0x0c268006f620: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c268006f630: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c268006f640: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c268006f650: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c268006f660: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c268006f670: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c268006f680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

0x0c268006f690: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c268006f6a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c268006f6b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c268006f6c0: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

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

==20448==ABORTING

**VERSION**  

Chrome Version: tsan-linux-release-398598  

Operating System: linux

**REPRODUCTION CASE**  

(movie.webm attached):

<html>
<script>
function start() {
let v = document.createElement("iframe");
v.src = "movie.webm";
for(var x=0; x<5; x++) container.appendChild(v.cloneNode(true));
window.setTimeout("location.reload()", Math.random() \\* 200);
}
</script>
<body onload="start()">
<div id="container"></div>
</body>
</html>

## Attachments

- [movie.webm](attachments/movie.webm) (application/octet-stream, 693 B)

## Timeline

### cl...@chromium.org (2016-06-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5148559406268416

### np...@chromium.org (2016-06-10)

Uploading to ClusterFuzz again with both the html and the webm.

### cl...@chromium.org (2016-06-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5174828231557120

### cl...@chromium.org (2016-06-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5913209076973568

### cl...@chromium.org (2016-06-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5179677702619136

### np...@chromium.org (2016-06-10)

The previous runs were apparently not including both files.  Latest one should be correct.

### np...@chromium.org (2016-06-10)

Can't repro on CF.

### cl...@gmail.com (2016-06-12)

Still repros fine for me with latest tsan build tsan-linux-release-399234 ...

### aa...@google.com (2016-06-16)

reopeing as per c#8

### es...@chromium.org (2016-06-17)

I can't repro this on tsan-linux-release-399234. inferno@, do you have any tips?

### es...@chromium.org (2016-06-20)

dalecurtis, could you please take a look? Thanks!

Tentatively setting security labels based on report, but please adjust if necessary.

[Monorail components: Internals>Media]

### da...@chromium.org (2016-06-20)

Ooh, good find. Might explain some other weird checks and stuff we've seen in the field.

### da...@chromium.org (2016-06-20)

Fix here https://codereview.chromium.org/2084643003

### bu...@chromium.org (2016-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9053fbc0d49919dd9e48b86d7df820562e845d80

commit 9053fbc0d49919dd9e48b86d7df820562e845d80
Author: dalecurtis <dalecurtis@chromium.org>
Date: Mon Jun 20 23:40:21 2016

Invalidate FFmpegDemuxer WeakPtrs on the right thread.

Previously these may not have been invalidated until the class is
destructed on the render thread, when they are bound to the media
thread.

BUG=618625
TEST=none

Review-Url: https://codereview.chromium.org/2084643003
Cr-Commit-Position: refs/heads/master@{#400835}

[modify] https://crrev.com/9053fbc0d49919dd9e48b86d7df820562e845d80/media/filters/ffmpeg_demuxer.cc


### sh...@chromium.org (2016-06-21)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-06-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2016-06-21)

At least OS-Linux, add more labels if appropriate.  Please make sure to add OS labels to release blockers.

### da...@chromium.org (2016-06-21)

[Empty comment from Monorail migration]

### da...@chromium.org (2016-06-21)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-21)

Your change meets the bar and is auto-approved for M52 (branch: 2743)

### bu...@chromium.org (2016-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0827287fdad94c10746403cdc271c06970a1dd15

commit 0827287fdad94c10746403cdc271c06970a1dd15
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Wed Jun 22 01:17:01 2016

Merge M52: "Invalidate FFmpegDemuxer WeakPtrs on the right thread."

Previously these may not have been invalidated until the class is
destructed on the render thread, when they are bound to the media
thread.

BUG=618625
TEST=none

Review-Url: https://codereview.chromium.org/2084643003
Cr-Commit-Position: refs/heads/master@{#400835}
(cherry picked from commit 9053fbc0d49919dd9e48b86d7df820562e845d80)

Review URL: https://codereview.chromium.org/2080603009 .

Cr-Commit-Position: refs/branch-heads/2743@{#443}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/0827287fdad94c10746403cdc271c06970a1dd15/media/filters/ffmpeg_demuxer.cc


### da...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-26)

Removing ReleaseBlock-Beta as this is already in M53

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

Another one to add to your haul, thanks!

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/618625?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084517)*
