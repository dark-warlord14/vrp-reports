# UAF in content::MediaSessionImpl::BuildMetadata

| Field | Value |
|-------|-------|
| **Issue ID** | [338929744](https://issues.chromium.org/issues/338929744) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Session |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2024-05-06 |
| **Bounty** | $1,000.00 |

## Description

UAF in content::MediaSessionImpl::BuildMetadata
tested os: Ubuntu 22.04
tested chrome version:
Chromium 126.0.6461.0
Chromium 121.0.6163.0

repro steps:
./chrome --user-data-dir=/tmp/xxs --incognito --disable-gpu <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html> <http://localhost:8605/crash2/crash.html>

# It was reproduced on my local machine after waiting for a few minutes. If you can't reproduce it, you can use the script in the attachment to open multiple browsers simultaneously for testing; it should reproduce the issue quickly. ./launcher.sh ./chrome <http://localhost:8880/crash.html> 5 2>&1

==1056414==ERROR: AddressSanitizer: heap-use-after-free on address 0x50e0000d24a0 at pc 0x600bbfe530c2 bp 0x7ffdb30bf4b0 sp 0x7ffdb30bf4a8
READ of size 1 at 0x50e0000d24a0 thread T0 (chrome)
#0 0x600bbfe530c1 in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long) *asan\_rtl*:17
#1 0x600bbfe52c45 in base::internal::(anonymous namespace)::SafelyUnwrapForDereference(unsigned long) *asan\_rtl*:5
#2 0x600bb803ca95 in SafelyUnwrapPtrForDereference[content::MediaSessionServiceImpl](javascript:void(0);) ./../../base/allocator/partition\_allocator/src/partition\_alloc/pointers/raw\_ptr\_hookable\_impl.h:84:9
#3 0x600bb803ca95 in GetForDereference ./../../base/allocator/partition\_allocator/src/partition\_alloc/pointers/raw\_ptr.h:979:12
#4 0x600bb803ca95 in operator-> ./../../base/allocator/partition\_allocator/src/partition\_alloc/pointers/raw\_ptr.h:672:12
#5 0x600bb803ca95 in content::MediaSessionImpl::BuildMetadata(media\_session::MediaMetadata&, std::\_\_Cr::vector<media\_session::MediaImage, std::\_\_Cr::allocator<media\_session::MediaImage>>&) ./../../content/browser/media/session/media\_session\_impl.cc:1890:26
#6 0x600bb8025fff in content::MediaSessionImpl::RebuildAndNotifyMetadataChanged() ./../../content/browser/media/session/media\_session\_impl.cc:1825:3
#7 0x600bb8025d48 in content::MediaSessionImpl::DidFinishNavigation(content::NavigationHandle\*) ./../../content/browser/media/session/media\_session\_impl.cc:309:3
#8 0x600bb8ed811f in void content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle\*&>(void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle\*&) ./../../content/browser/web\_contents/web\_contents\_impl.h:1645:9
#9 0x600bb8ed99f0 in content::WebContentsImpl::DidFinishNavigation(content::NavigationHandle\*) ./../../content/browser/web\_contents/web\_contents\_impl.cc:6509:16
#10 0x600bb85b4394 in content::NavigationRequest::~NavigationRequest() ./../../content/browser/renderer\_host/navigation\_request.cc:2196:20
#11 0x600bb85b9af3 in content::NavigationRequest::~NavigationRequest() ./../../content/browser/renderer\_host/navigation\_request.cc:2101:41
#12 0x600bb8652d42 in operator() ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:67:5
#13 0x600bb8652d42 in reset ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:278:7
#14 0x600bb8652d42 in ~unique\_ptr ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:248:71
#15 0x600bb8652d42 in content::Navigator::DidNavigate(content::RenderFrameHostImpl\*, content::mojom::DidCommitProvisionalLoadParams const&, std::\_\_Cr::unique\_ptr<content::NavigationRequest, std::\_\_Cr::default\_delete[content::NavigationRequest](javascript:void(0);)>, bool) ./../../content/browser/renderer\_host/navigator.cc:772:1
#16 0x600bb86c6074 in content::RenderFrameHostImpl::DidCommitNavigationInternal(std::\_\_Cr::unique\_ptr<content::NavigationRequest, std::\_\_Cr::default\_delete[content::NavigationRequest](javascript:void(0);)>, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitSameDocumentNavigationParams](javascript:void(0);)) ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:13936:58
#17 0x600bb86c2528 in content::RenderFrameHostImpl::DidCommitNavigation(content::NavigationRequest\*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)) ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:14682:8
#18 0x600bb8766cfc in Invoke<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), content::RenderFrameHostImpl *, content::NavigationRequest *, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);) > ./../../base/functional/bind\_internal.h:738:12
#19 0x600bb8766cfc in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (content::RenderFrameHostImpl::*&&)(content::NavigationRequest*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), content::RenderFrameHostImpl*, content::NavigationRequest*&&>, void, 0ul, 1ul>::MakeItSo<void (content::RenderFrameHostImpl::*)(content::NavigationRequest*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<content::RenderFrameHostImpl, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<content::NavigationRequest, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)>(void (content::RenderFrameHostImpl::*&&)(content::NavigationRequest*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<content::RenderFrameHostImpl, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<content::NavigationRequest, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>&&, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);)&&, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)&&) ./../../base/functional/bind\_internal.h:930:12
#20 0x600bb8766a39 in RunImpl<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<content::RenderFrameHostImpl, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<content::NavigationRequest, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> >, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1067:14
#21 0x600bb8766a39 in base::internal::Invoker<base::internal::FunctorTraits<void (content::RenderFrameHostImpl::*&&)(content::NavigationRequest*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), content::RenderFrameHostImpl\*, content::NavigationRequest\*&&>, base::internal::BindState<true, true, false, void (content::RenderFrameHostImpl::*)(content::NavigationRequest*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), base::internal::UnretainedWrapper<content::RenderFrameHostImpl, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<content::NavigationRequest, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void (mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);))>::RunOnce(base::internal::BindStateBase\*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);)&&, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)&&) ./../../base/functional/bind\_internal.h:980:12
#22 0x600bb2f59033 in Run ./../../base/functional/callback.h:156:12
#23 0x600bb2f59033 in content::mojom::NavigationClient\_CommitNavigation\_ForwardToCallback::Accept(mojo::Message\*) ./gen/content/common/navigation\_client.mojom.cc:1183:26
#24 0x600bc165795d in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1031:41
#25 0x600bc167315a in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19
#26 0x600bc165c3a5 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:721:20
#27 0x600bc2452dae in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc\_mojo\_bootstrap.cc:1198:24
#28 0x600bc2454413 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);), mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind\_internal.h:738:12
#29 0x600bc2454413 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::\_\_Cr::tuple<scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);), mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind\_internal.h:930:12
#30 0x600bc2454413 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::\_\_Cr::tuple<scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);), mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind\_internal.h:1067:14
#31 0x600bc2454413 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController\*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);), mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind\_internal.h:980:12
#32 0x600bbff63ec4 in Run ./../../base/functional/callback.h:156:12
#33 0x600bbff63ec4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:203:34
#34 0x600bbffc5676 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:475:11)> ./../../base/task/common/task\_annotator.h:90:5
#35 0x600bbffc5676 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:473:23
#36 0x600bbffc458d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:338:40
#37 0x600bbffc63ba in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0
#38 0x600bc012c459 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:694:48
#39 0x600bbffc7026 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:645:12
#40 0x600bbfef677f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14
#41 0x600bb75469e2 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1102:18
#42 0x600bb754e0bc in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:159:15
#43 0x600bb753d528 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:34:28
#44 0x600bbd626130 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:717:10
#45 0x600bbd629ccf in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1309:10
#46 0x600bbd629385 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1154:12
#47 0x600bbd623580 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:332:36
#48 0x600bbd623c0b in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:345:10
#49 0x600badc40408 in ChromeMain ./../../chrome/app/chrome\_main.cc:192:12
#50 0x7a659ea29d8f in \_\_libc\_start\_call\_main ./csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

0x50e0000d24a0 is located 0 bytes inside of 160-byte region [0x50e0000d24a0,0x50e0000d2540)
freed by thread T0 (chrome) here:
#0 0x600badc3e48d in operator delete(void\*) *asan\_rtl*:3
#1 0x600bb8051495 in operator() ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:67:5
#2 0x600bb8051495 in reset ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:278:7
#3 0x600bb8051495 in ~unique\_ptr ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:248:71
#4 0x600bb8051495 in ~SelfOwnedReceiver ./../../mojo/public/cpp/bindings/self\_owned\_receiver.h:104:32
#5 0x600bb8051495 in mojo::internal::SelfOwnedReceiver[blink::mojom::MediaSessionService](javascript:void(0);)::Close() ./../../mojo/public/cpp/bindings/self\_owned\_receiver.h:84:18
#6 0x600bb8050af6 in mojo::internal::SelfOwnedReceiver[blink::mojom::MediaSessionService](javascript:void(0);)::OnDisconnect(unsigned int, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&) ./../../mojo/public/cpp/bindings/self\_owned\_receiver.h:113:5
#7 0x600bb80512c6 in Invoke<void (mojo::internal::SelfOwnedReceiver[blink::mojom::MediaSessionService](javascript:void(0);)::*)(unsigned int, const std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > &), mojo::internal::SelfOwnedReceiver[blink::mojom::MediaSessionService](javascript:void(0);) *, unsigned int, const std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > &> ./../../base/functional/bind\_internal.h:738:12
#8 0x600bb80512c6 in MakeItSo<void (mojo::internal::SelfOwnedReceiver[blink::mojom::MediaSessionService](javascript:void(0);)::*)(unsigned int, const std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > &), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::internal::SelfOwnedReceiver[blink::mojom::MediaSessionService](javascript:void(0);), base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> >, unsigned int, const std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > &> ./../../base/functional/bind\_internal.h:930:12
#9 0x600bb80512c6 in RunImpl<void (mojo::internal::SelfOwnedReceiver[blink::mojom::MediaSessionService](javascript:void(0);)::*)(unsigned int, const std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > &), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::internal::SelfOwnedReceiver[blink::mojom::MediaSessionService](javascript:void(0);), base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind\_internal.h:1067:14
#10 0x600bb80512c6 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::internal::SelfOwnedReceiver[blink::mojom::MediaSessionService](javascript:void(0);)::*&&)(unsigned int, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&), mojo::internal::SelfOwnedReceiver[blink::mojom::MediaSessionService](javascript:void(0);)*>, base::internal::BindState<true, true, false, void (mojo::internal::SelfOwnedReceiver[blink::mojom::MediaSessionService](javascript:void(0);)::*)(unsigned int, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&), base::internal::UnretainedWrapper<mojo::internal::SelfOwnedReceiver[blink::mojom::MediaSessionService](javascript:void(0);), base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void (unsigned int, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&)>::RunOnce(base::internal::BindStateBase*, unsigned int, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&) ./../../base/functional/bind\_internal.h:980:12
#11 0x600bc165ce74 in Run ./../../base/functional/callback.h:156:12
#12 0x600bc165ce74 in mojo::InterfaceEndpointClient::NotifyError(std::\_\_Cr::optional[mojo::DisconnectReason](javascript:void(0);) const&) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:765:45
#13 0x600bc16833ab in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(mojo::internal::MultiplexRouter::Task\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1034:13
#14 0x600bc1679f5a in mojo::internal::MultiplexRouter::ProcessTasks(mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:947:15
#15 0x600bc167580e in mojo::internal::MultiplexRouter::OnPipeConnectionError(bool) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:856:3
#16 0x600bc16857f1 in Invoke<void (mojo::internal::MultiplexRouter::*)(bool), mojo::internal::MultiplexRouter *, bool> ./../../base/functional/bind\_internal.h:738:12
#17 0x600bc16857f1 in MakeItSo<void (mojo::internal::MultiplexRouter::*)(bool), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::internal::MultiplexRouter, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, bool> > ./../../base/functional/bind\_internal.h:930:12
#18 0x600bc16857f1 in RunImpl<void (mojo::internal::MultiplexRouter::*)(bool), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::internal::MultiplexRouter, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, bool>, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1067:14
#19 0x600bc16857f1 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::internal::MultiplexRouter::*&&)(bool), mojo::internal::MultiplexRouter*, bool&&>, base::internal::BindState<true, true, false, void (mojo::internal::MultiplexRouter::*)(bool), base::internal::UnretainedWrapper<mojo::internal::MultiplexRouter, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, bool>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind\_internal.h:980:12
#20 0x600bc164da91 in Run ./../../base/functional/callback.h:156:12
#21 0x600bc164da91 in mojo::Connector::HandleError(bool, bool) ./../../mojo/public/cpp/bindings/lib/connector.cc:681:44
#22 0x600bc164fcd1 in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:0:0
#23 0x600bc164fcd1 in mojo::Connector::OnWatcherHandleReady(char const\*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:410:3
#24 0x600bc16515ba in Invoke<void (mojo::Connector::*)(const char *, unsigned int), mojo::Connector *, const char *, unsigned int> ./../../base/functional/bind\_internal.h:738:12
#25 0x600bc16515ba in MakeItSo<void (mojo::Connector::*const &)(const char *, unsigned int), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind\_internal.h:930:12
#26 0x600bc16515ba in RunImpl<void (mojo::Connector::*const &)(const char *, unsigned int), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> > &, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1067:14
#27 0x600bc16515ba in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) ./../../base/functional/bind\_internal.h:987:12
#28 0x600bb29600b3 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/functional/callback.h:344:12
#29 0x600bb295fe3f in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:671:12
#30 0x600bb295fe3f in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::\_\_Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:930:12
#31 0x600bb295fe3f in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::\_\_Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind\_internal.h:1067:14
#32 0x600bb295fe3f in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind\_internal.h:987:12
#33 0x600bc16d9c8b in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/functional/callback.h:344:12
#34 0x600bc16d95b3 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14
#35 0x600bc16da7f4 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);) &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind\_internal.h:738:12
#36 0x600bc16da7f4 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind\_internal.h:954:5
#37 0x600bc16da7f4 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);)&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/functional/bind\_internal.h:1067:14
#38 0x600bbff63ec4 in Run ./../../base/functional/callback.h:156:12
#39 0x600bbff63ec4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:203:34
#40 0x600bbffc5676 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:475:11)> ./../../base/task/common/task\_annotator.h:90:5
#41 0x600bbffc5676 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:473:23
#42 0x600bbffc458d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:338:40
#43 0x600bbffc63ba in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0
#44 0x600bc012bb22 in base::MessagePumpGlib::HandleDispatch() ./../../base/message\_loop/message\_pump\_glib.cc:649:46
#45 0x600bc012e9e8 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (*)(void*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:274:43
#46 0x7a659fd15d3a in g\_main\_context\_dispatch ??:0:0

previously allocated by thread T0 (chrome) here:
#0 0x600badc3dc2d in operator new(unsigned long) *asan\_rtl*:3
#1 0x600bb804e05a in content::MediaSessionServiceImpl::Create(content::RenderFrameHost\*, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);)) ./../../content/browser/media/session/media\_session\_service\_impl.cc:41:11
#2 0x600bb74df491 in Invoke<void (*const &)(content::RenderFrameHost *, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);)), content::RenderFrameHost *, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);) > ./../../base/functional/bind\_internal.h:671:12
#3 0x600bb74df491 in MakeItSo<void (*const &)(content::RenderFrameHost *, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);)), const std::\_\_Cr::tuple<> &, content::RenderFrameHost *, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);) > ./../../base/functional/bind\_internal.h:930:12
#4 0x600bb74df491 in RunImpl<void (*const &)(content::RenderFrameHost *, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);)), const std::\_\_Cr::tuple<> &> ./../../base/functional/bind\_internal.h:1067:14
#5 0x600bb74df491 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(content::RenderFrameHost*, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))>, base::internal::BindState<false, true, false, void (*)(content::RenderFrameHost*, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))>, void (content::RenderFrameHost*, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))>::Run(base::internal::BindStateBase*, content::RenderFrameHost*, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);)&&) ./../../base/functional/bind\_internal.h:987:12
#6 0x600bb751a3dd in base::RepeatingCallback<void (content::RenderFrameHost*, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))>::Run(content::RenderFrameHost\*, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);)) const & ./../../base/functional/callback.h:344:12
#7 0x600bb7519f38 in void mojo::internal::BinderContextTraits[content::RenderFrameHost\*](javascript:void(0);)::BindGenericReceiver[blink::mojom::MediaSessionService](javascript:void(0);)(base::RepeatingCallback<void (content::RenderFrameHost\*, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))> const&, content::RenderFrameHost\*, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/binder\_map\_internal.h:40:12
#8 0x600bb751a112 in Invoke<void (*const &)(const base::RepeatingCallback<void (content::RenderFrameHost *, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))> &, content::RenderFrameHost *, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)), const base::RepeatingCallback<void (content::RenderFrameHost *, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))> &, content::RenderFrameHost *, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);) > ./../../base/functional/bind\_internal.h:671:12
#9 0x600bb751a112 in MakeItSo<void (*const &)(const base::RepeatingCallback<void (content::RenderFrameHost *, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))> &, content::RenderFrameHost *, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)), const std::\_\_Cr::tuple<base::RepeatingCallback<void (content::RenderFrameHost *, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))> > &, content::RenderFrameHost *, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);) > ./../../base/functional/bind\_internal.h:930:12
#10 0x600bb751a112 in RunImpl<void (*const &)(const base::RepeatingCallback<void (content::RenderFrameHost *, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))> &, content::RenderFrameHost *, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)), const std::\_\_Cr::tuple<base::RepeatingCallback<void (content::RenderFrameHost *, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))> > &, 0UL> ./../../base/functional/bind\_internal.h:1067:14
#11 0x600bb751a112 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (content::RenderFrameHost*, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))> const&, content::RenderFrameHost*, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)), base::RepeatingCallback<void (content::RenderFrameHost*, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (content::RenderFrameHost*, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))> const&, content::RenderFrameHost*, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)), base::RepeatingCallback<void (content::RenderFrameHost*, mojo::PendingReceiver[blink::mojom::MediaSessionService](javascript:void(0);))>>, void (content::RenderFrameHost*, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);))>::Run(base::internal::BindStateBase*, content::RenderFrameHost*, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)&&) ./../../base/functional/bind\_internal.h:987:12
#12 0x600bb87475bd in base::RepeatingCallback<void (content::RenderFrameHost*, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);))>::Run(content::RenderFrameHost*, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)) const & ./../../base/functional/callback.h:344:12
#13 0x600bb8746e17 in RunCallbackWithContext ./../../mojo/public/cpp/bindings/lib/binder\_map\_internal.h:121:14
#14 0x600bb8746e17 in mojo::internal::GenericCallbackBinderWithContext[content::RenderFrameHost\*](javascript:void(0);)::BindInterface(content::RenderFrameHost*, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/binder\_map\_internal.h:102:5
#15 0x600bb87466b4 in mojo::BinderMapWithContext[content::RenderFrameHost\*](javascript:void(0);)::TryBind(content::RenderFrameHost\*, mojo::GenericPendingReceiver\*) ./../../mojo/public/cpp/bindings/binder\_map.h:112:17
#16 0x600bb874636e in content::BrowserInterfaceBrokerImpl<content::RenderFrameHostImpl, content::RenderFrameHost\*>::BindInterface(mojo::GenericPendingReceiver) ./../../content/browser/browser\_interface\_broker\_impl.h:88:37
#17 0x600bb8745f34 in content::BrowserInterfaceBrokerImpl<content::RenderFrameHostImpl, content::RenderFrameHost\*>::GetInterface(mojo::GenericPendingReceiver) ./../../content/browser/browser\_interface\_broker\_impl.h:60:7
#18 0x600bb24113e3 in blink::mojom::BrowserInterfaceBrokerStubDispatch::Accept(blink::mojom::BrowserInterfaceBroker\*, mojo::Message\*) ./gen/third\_party/blink/public/mojom/browser\_interface\_broker.mojom.cc:188:13
#19 0x600bc16571d7 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1036:54
#20 0x600bc167305d in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:48:24
#21 0x600bc165c3a5 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:721:20
#22 0x600bc1680d3c in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1120:42
#23 0x600bc167eab4 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:733:7
#24 0x600bc167315a in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19
#25 0x600bc164e853 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:554:49
#26 0x600bc1650290 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:611:14
#27 0x600bc1650cad in Invoke<void (mojo::Connector::*)(), const base::WeakPtr[mojo::Connector](javascript:void(0);) &> ./../../base/functional/bind\_internal.h:738:12
#28 0x600bc1650cad in MakeItSo<void (mojo::Connector::*)(), std::\_\_Cr::tuple<base::WeakPtr[mojo::Connector](javascript:void(0);) > > ./../../base/functional/bind\_internal.h:954:5
#29 0x600bc1650cad in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr[mojo::Connector](javascript:void(0);)&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr[mojo::Connector](javascript:void(0);)>, void ()>::RunImpl<void (mojo::Connector::*)(), std::\_\_Cr::tuple<base::WeakPtr[mojo::Connector](javascript:void(0);)>, 0ul>(void (mojo::Connector::*&&)(), std::\_\_Cr::tuple<base::WeakPtr[mojo::Connector](javascript:void(0);)>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul>) ./../../base/functional/bind\_internal.h:1067:14
#30 0x600bbff63ec4 in Run ./../../base/functional/callback.h:156:12
#31 0x600bbff63ec4 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:203:34
#32 0x600bbffc5676 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:475:11)> ./../../base/task/common/task\_annotator.h:90:5
#33 0x600bbffc5676 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:473:23
#34 0x600bbffc458d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:338:40
#35 0x600bbffc63ba in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0
#36 0x600bc012bb22 in base::MessagePumpGlib::HandleDispatch() ./../../base/message\_loop/message\_pump\_glib.cc:649:46
#37 0x600bc012e9e8 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (*)(void*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:274:43
#38 0x7a659fd15d3a in g\_main\_context\_dispatch ??:0:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwn11/asan-linux-release/chrome+0x20d020c1) (BuildId: 8fbb97da385e0340)
Shadow bytes around the buggy address:
0x50e0000d2200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x50e0000d2280: fd fd fd fd fa fa fa fa fa fa f7 fa fd fd fd fd
0x50e0000d2300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x50e0000d2380: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
0x50e0000d2400: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
=>0x50e0000d2480: fa fa f7 fa[fd]fd fd fd fd fd fd fd fd fd fd fd
0x50e0000d2500: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
0x50e0000d2580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x50e0000d2600: fd fd fd fd fa fa fa fa fa fa f7 fa fd fd fd fd
0x50e0000d2680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x50e0000d2700: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
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

==1056414==ADDITIONAL INFO

==1056414==Note: Please include this section with the ASan report.
Task trace:
#0 0x600bc2446f52 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message\*) ./../../ipc/ipc\_mojo\_bootstrap.cc:1137:13
#1 0x600bc16da197 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple\_watcher.cc:102:13

MiraclePtr Status: PROTECTED
This crash occurred while a raw\_ptr<T> object containing a dangling pointer was being dereferenced.
MiraclePtr is expected to make this crash non-exploitable once fully enabled.
Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==1056414==END OF ADDITIONAL INFO
==1056414==ABORTING
[0506/225431.207197:ERROR:elf\_dynamic\_array\_reader.h(64)] tag not found
Received signal 6
#0 0x600badbb08a6 in \_\_\_interceptor\_backtrace /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_common\_interceptors.inc:4364:13
#1 0x600bc00e59d8 in base::debug::CollectStackTrace(void const\*\*, unsigned long) ./../../base/debug/stack\_trace\_posix.cc:1043:7
#2 0x600bc00ad717 in StackTrace ./../../base/debug/stack\_trace.cc:241:20
#3 0x600bc00ad717 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack\_trace.cc:236:28
#4 0x600bc00e4cc6 in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo\_t\*, void\*) ./../../base/debug/stack\_trace\_posix.cc:462:3
#5 0x7a659ea42520 in \_\_GI\_\_\_sigaction :?
#6 0x7a659ea969fc in \_\_pthread\_kill\_implementation ./nptl/pthread\_kill.c:43:17
#7 0x7a659ea969fc in \_\_pthread\_kill\_internal ./nptl/pthread\_kill.c:78:10
#8 0x7a659ea969fc in pthread\_kill ./nptl/pthread\_kill.c:89:10
#9 0x7a659ea42476 in gsignal ./signal/../sysdeps/posix/raise.c:26:13
#10 0x7a659ea287f3 in abort ./stdlib/abort.c:79:7
#11 0x600badc2731c in \_\_sanitizer::Abort() /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/sanitizer\_common/sanitizer\_posix\_libcdep.cpp:163:3
#12 0x600badc25d1e in \_\_sanitizer::Die() /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/sanitizer\_common/sanitizer\_termination.cpp:58:5
#13 0x600badc0c559 in \_\_asan::ScopedInErrorReport::~ScopedInErrorReport() *asan\_rtl*:7
#14 0x600badc0f697 in \_\_asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) *asan\_rtl*:1
#15 0x600badc10336 in \_\_asan\_report\_load1 *asan\_rtl*:1
#16 0x600bbfe530c2 in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long) *asan\_rtl*:17
#17 0x600bbfe52c46 in base::internal::(anonymous namespace)::SafelyUnwrapForDereference(unsigned long) *asan\_rtl*:5
#18 0x600bb803ca96 in SafelyUnwrapPtrForDereference[content::MediaSessionServiceImpl](javascript:void(0);) ./../../base/allocator/partition\_allocator/src/partition\_alloc/pointers/raw\_ptr\_hookable\_impl.h:84:9
#19 0x600bb803ca96 in GetForDereference ./../../base/allocator/partition\_allocator/src/partition\_alloc/pointers/raw\_ptr.h:979:12
#20 0x600bb803ca96 in operator-> ./../../base/allocator/partition\_allocator/src/partition\_alloc/pointers/raw\_ptr.h:672:12
#21 0x600bb803ca96 in content::MediaSessionImpl::BuildMetadata(media\_session::MediaMetadata&, std::\_\_Cr::vector<media\_session::MediaImage, std::\_\_Cr::allocator<media\_session::MediaImage>>&) ./../../content/browser/media/session/media\_session\_impl.cc:1890:26
#22 0x600bb8026000 in content::MediaSessionImpl::RebuildAndNotifyMetadataChanged() ./../../content/browser/media/session/media\_session\_impl.cc:1825:3
#23 0x600bb8025d49 in content::MediaSessionImpl::DidFinishNavigation(content::NavigationHandle\*) ./../../content/browser/media/session/media\_session\_impl.cc:309:3
#24 0x600bb8ed8120 in void content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle\*&>(void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle\*&) ./../../content/browser/web\_contents/web\_contents\_impl.h:1645:9
#25 0x600bb8ed99f1 in content::WebContentsImpl::DidFinishNavigation(content::NavigationHandle\*) ./../../content/browser/web\_contents/web\_contents\_impl.cc:6509:16
#26 0x600bb85b4395 in content::NavigationRequest::~NavigationRequest() ./../../content/browser/renderer\_host/navigation\_request.cc:2196:20
#27 0x600bb85b9af4 in content::NavigationRequest::~NavigationRequest() ./../../content/browser/renderer\_host/navigation\_request.cc:2101:41
#28 0x600bb8652d43 in operator() ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:67:5
#29 0x600bb8652d43 in reset ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:278:7
#30 0x600bb8652d43 in ~unique\_ptr ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:248:71
#31 0x600bb8652d43 in content::Navigator::DidNavigate(content::RenderFrameHostImpl\*, content::mojom::DidCommitProvisionalLoadParams const&, std::\_\_Cr::unique\_ptr<content::NavigationRequest, std::\_\_Cr::default\_delete[content::NavigationRequest](javascript:void(0);)>, bool) ./../../content/browser/renderer\_host/navigator.cc:772:1
#32 0x600bb86c6075 in content::RenderFrameHostImpl::DidCommitNavigationInternal(std::\_\_Cr::unique\_ptr<content::NavigationRequest, std::\_\_Cr::default\_delete[content::NavigationRequest](javascript:void(0);)>, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitSameDocumentNavigationParams](javascript:void(0);)) ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:13936:58
#33 0x600bb86c2529 in content::RenderFrameHostImpl::DidCommitNavigation(content::NavigationRequest\*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)) ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:14682:8
#34 0x600bb8766cfd in Invoke<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), content::RenderFrameHostImpl *, content::NavigationRequest *, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);) > ./../../base/functional/bind\_internal.h:738:12
#35 0x600bb8766cfd in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (content::RenderFrameHostImpl::*&&)(content::NavigationRequest*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), content::RenderFrameHostImpl*, content::NavigationRequest*&&>, void, 0ul, 1ul>::MakeItSo<void (content::RenderFrameHostImpl::*)(content::NavigationRequest*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<content::RenderFrameHostImpl, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<content::NavigationRequest, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)>(void (content::RenderFrameHostImpl::*&&)(content::NavigationRequest*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<content::RenderFrameHostImpl, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<content::NavigationRequest, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>&&, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);)&&, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)&&) ./../../base/functional/bind\_internal.h:930:12
#36 0x600bb8766a3a in RunImpl<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<content::RenderFrameHostImpl, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<content::NavigationRequest, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> >, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1067:14
#37 0x600bb8766a3a in base::internal::Invoker<base::internal::FunctorTraits<void (content::RenderFrameHostImpl::*&&)(content::NavigationRequest*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), content::RenderFrameHostImpl\*, content::NavigationRequest\*&&>, base::internal::BindState<true, true, false, void (content::RenderFrameHostImpl::*)(content::NavigationRequest*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)), base::internal::UnretainedWrapper<content::RenderFrameHostImpl, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<content::NavigationRequest, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void (mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);), mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);))>::RunOnce(base::internal::BindStateBase\*, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadParams](javascript:void(0);)&&, mojo::StructPtr[content::mojom::DidCommitProvisionalLoadInterfaceParams](javascript:void(0);)&&) ./../../base/functional/bind\_internal.h:980:12
#38 0x600bb2f59034 in Run ./../../base/functional/callback.h:156:12
#39 0x600bb2f59034 in content::mojom::NavigationClient\_CommitNavigation\_ForwardToCallback::Accept(mojo::Message\*) ./gen/content/common/navigation\_client.mojom.cc:1183:26
#40 0x600bc165795e in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1031:41
#41 0x600bc167315b in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19
#42 0x600bc165c3a6 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:721:20
#43 0x600bc2452daf in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc\_mojo\_bootstrap.cc:1198:24
#44 0x600bc2454414 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);), mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind\_internal.h:738:12
#45 0x600bc2454414 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::\_\_Cr::tuple<scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);), mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind\_internal.h:930:12
#46 0x600bc2454414 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::\_\_Cr::tuple<scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);), mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind\_internal.h:1067:14
#47 0x600bc2454414 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController\*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);), mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind\_internal.h:980:12
#48 0x600bbff63ec5 in Run ./../../base/functional/callback.h:156:12
#49 0x600bbff63ec5 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:203:34
#50 0x600bbffc5677 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:475:11)> ./../../base/task/common/task\_annotator.h:90:5
#51 0x600bbffc5677 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:473:23
#52 0x600bbffc458e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:338:40
#53 0x600bbffc63bb in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0
#54 0x600bc012c45a in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:694:48
#55 0x600bbffc7027 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:645:12
#56 0x600bbfef6780 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14
#57 0x600bb75469e3 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1102:18
#58 0x600bb754e0bd in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:159:15
#59 0x600bb753d529 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:34:28
#60 0x600bbd626131 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:717:10
#61 0x600bbd629cd0 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1309:10
#62 0x600bbd629386 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1154:12
#63 0x600bbd623581 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:332:36
#64 0x600bbd623c0c in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:345:10
#65 0x600badc40409 in ChromeMain ./../../chrome/app/chrome\_main.cc:192:12
#66 0x7a659ea29d90 in \_\_libc\_start\_call\_main ./csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16
#67 0x7a659ea29e40 in \_\_libc\_start\_main ./csu/../csu/libc-start.c:392:3
#68 0x600badb6c02a in \_start ??:0:0
r8: 00007ffdb30be5c0 r9: 0000000000000000 r10: 0000000000000008 r11: 0000000000000246
r12: 0000000000000006 r13: 0000000000000016 r14: 0000600bdd25b2d8 r15: 0fffff0000000000
di: 0000000000101e9e si: 0000000000101e9e bp: 0000000000101e9e bx: 00007a659db35580
dx: 0000000000000006 ax: 0000000000000000 cx: 00007a659ea969fc sp: 00007ffdb30be4f0
ip: 00007a659ea969fc efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Aborted

## Attachments

- [crash.html](attachments/crash.html) (text/html, 630 B)
- [launcher.sh](attachments/launcher.sh) (text/x-sh, 727 B)
- [asan.log](attachments/asan.log) (text/plain, 52.6 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-05-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4919998683217920.

### ca...@chromium.org (2024-05-08)

Looks like CF wasn't able to reproduce this, I'll try to reproduce this locally

### ca...@chromium.org (2024-05-08)

I wasn't able to reproduce this locally either, but the ASAN report looks valid, so I'll tentatively triage this as valid. 

### ca...@chromium.org (2024-05-08)

steimel: Can you help further triage this? As mentioned in #2 and #3, I wasn't able to reproduce this either locally or in clusterfuzz, but the report looks valid. Thanks  Setting FoundIn to the current extended stable since reporter mentioned they were able to reproduce in 121

### ca...@chromium.org (2024-05-08)

Triageing as high severity due to MiraclePtr protection

### el...@chromium.org (2024-05-08)

Security shepherd: Impact = extended stable as well.

### pe...@google.com (2024-05-09)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-09)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-05-23)

steimel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### da...@chromium.org (2024-05-23)

Tommy, can you take a look or reassign if you don't have bandwidth?

### st...@chromium.org (2024-05-24)

speculative fix: crrev.com/c/5564794

### em...@gmail.com (2024-05-24)

I confirm that after applying the patch (https://chromium-review.googlesource.com/c/chromium/src/+/5564794), the issue did not repro.

### ap...@google.com (2024-05-24)

Project: chromium/src
Branch: main

commit 1f0de3303671c6c041930c7f4f8a9ad017a7f211
Author: Tommy Steimel <steimel@chromium.org>
Date:   Fri May 24 13:57:53 2024

    MediaSession: Use a MediaSessionImpl WeakPtr in MediaSessionServiceImpl
    
    Currently, every time MediaSessionServiceImpl wants to talk to its
    associated MediaSessionImpl, it recalculates it from its
    RenderFrameHostId. This can lead to issues where a
    MediaSessionServiceImpl of a disconnected RenderFrameHost can no longer
    access the MediaSessionImpl to tell it that it is being deleted,
    leaving MediaSessionImpl with a dangling raw_ptr.
    
    Bug: 338929744
    Change-Id: I8f404c1a39510a24643c1f973a32bf6c0bbde123
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5564794
    Reviewed-by: Frank Liberato <liberato@chromium.org>
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1305678}

M       content/browser/media/session/media_session_impl.cc
M       content/browser/media/session/media_session_impl.h
M       content/browser/media/session/media_session_service_impl.cc
M       content/browser/media/session/media_session_service_impl.h

https://chromium-review.googlesource.com/5564794


### st...@chromium.org (2024-05-24)

Thanks for confirming that!

### pe...@google.com (2024-05-24)

Requesting merge to extended stable (M124) because latest trunk commit (1305678) appears to be after extended stable branch point (1274542).
Requesting merge to stable (M125) because latest trunk commit (1305678) appears to be after stable branch point (1287751).
Requesting merge to beta (M126) because latest trunk commit (1305678) appears to be after beta branch point (1300313).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-05-25)

Merge review required: M126 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-05-25)

Merge review required: M125 is already shipping to stable.

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

### pe...@google.com (2024-05-25)

Merge review required: M124 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

### am...@chromium.org (2024-05-28)

<https://crrev.com/c/c5564794> approved for merge
Please merge this fix to M124 (branch 6367) and M125 (branch 6422) by 10am Pacific tomorrow (Wednesday) so this fix can be included in the next updates for each
Please merge this fix to M126 (branch 6478) by EOD tomorrow so this fix can be included in the next M126 Beta update

### ap...@google.com (2024-05-28)

Project: chromium/src
Branch: refs/branch-heads/6422

commit 3469a2af1f769284f59ba8dc68d7e813b9c82b6a
Author: Tommy Steimel <steimel@chromium.org>
Date:   Tue May 28 23:37:42 2024

    [M125]MediaSession: Use a MediaSessionImpl WeakPtr in MediaSessionServiceImpl
    
    Currently, every time MediaSessionServiceImpl wants to talk to its
    associated MediaSessionImpl, it recalculates it from its
    RenderFrameHostId. This can lead to issues where a
    MediaSessionServiceImpl of a disconnected RenderFrameHost can no longer
    access the MediaSessionImpl to tell it that it is being deleted,
    leaving MediaSessionImpl with a dangling raw_ptr.
    
    (cherry picked from commit 1f0de3303671c6c041930c7f4f8a9ad017a7f211)
    
    Bug: 338929744
    Change-Id: I8f404c1a39510a24643c1f973a32bf6c0bbde123
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5564794
    Reviewed-by: Frank Liberato <liberato@chromium.org>
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1305678}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5577053
    Cr-Commit-Position: refs/branch-heads/6422@{#1176}
    Cr-Branched-From: 9012208d0ce02e0cf0adb9b62558627c356f3278-refs/heads/main@{#1287751}

M       content/browser/media/session/media_session_impl.cc
M       content/browser/media/session/media_session_impl.h
M       content/browser/media/session/media_session_service_impl.cc
M       content/browser/media/session/media_session_service_impl.h

https://chromium-review.googlesource.com/5577053


### ap...@google.com (2024-05-28)

Project: chromium/src
Branch: refs/branch-heads/6367

commit 11c5f7911caab6930812a515eac27e35776ba35c
Author: Tommy Steimel <steimel@chromium.org>
Date:   Tue May 28 23:37:26 2024

    [M124]MediaSession: Use a MediaSessionImpl WeakPtr in MediaSessionServiceImpl
    
    Currently, every time MediaSessionServiceImpl wants to talk to its
    associated MediaSessionImpl, it recalculates it from its
    RenderFrameHostId. This can lead to issues where a
    MediaSessionServiceImpl of a disconnected RenderFrameHost can no longer
    access the MediaSessionImpl to tell it that it is being deleted,
    leaving MediaSessionImpl with a dangling raw_ptr.
    
    (cherry picked from commit 1f0de3303671c6c041930c7f4f8a9ad017a7f211)
    
    Bug: 338929744
    Change-Id: I092d217d4a975b67a84280687ed5461a14ead98a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5577944
    Reviewed-by: Frank Liberato <liberato@chromium.org>
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6367@{#1245}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       content/browser/media/session/media_session_impl.cc
M       content/browser/media/session/media_session_impl.h
M       content/browser/media/session/media_session_service_impl.cc
M       content/browser/media/session/media_session_service_impl.h

https://chromium-review.googlesource.com/5577944


### ap...@google.com (2024-05-28)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 61a366f93b728d3fa29ec71af3e12c29c0e2f6d6
Author: Tommy Steimel <steimel@chromium.org>
Date:   Tue May 28 23:40:36 2024

    [M126]MediaSession: Use a MediaSessionImpl WeakPtr in MediaSessionServiceImpl
    
    Currently, every time MediaSessionServiceImpl wants to talk to its
    associated MediaSessionImpl, it recalculates it from its
    RenderFrameHostId. This can lead to issues where a
    MediaSessionServiceImpl of a disconnected RenderFrameHost can no longer
    access the MediaSessionImpl to tell it that it is being deleted,
    leaving MediaSessionImpl with a dangling raw_ptr.
    
    (cherry picked from commit 1f0de3303671c6c041930c7f4f8a9ad017a7f211)
    
    Bug: 338929744
    Change-Id: I8f404c1a39510a24643c1f973a32bf6c0bbde123
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5564794
    Reviewed-by: Frank Liberato <liberato@chromium.org>
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1305678}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5578717
    Cr-Commit-Position: refs/branch-heads/6478@{#773}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       content/browser/media/session/media_session_impl.cc
M       content/browser/media/session/media_session_impl.h
M       content/browser/media/session/media_session_service_impl.cc
M       content/browser/media/session/media_session_service_impl.h

https://chromium-review.googlesource.com/5578717


### pe...@google.com (2024-05-28)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### da...@google.com (2024-05-29)

merged to m124 as per #c22

### sp...@google.com (2024-05-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
highly mitigated memory corruption in a non-sandboxed process, mitigated by BRP protection, race condition --  to the extent we were unable to reproduce this issue 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are not already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-30)

Thanks for your efforts in discovering and reporting this issue to us, Cassidy Kim.

### pe...@google.com (2024-05-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### vo...@google.com (2024-05-30)

1. <https://crrev.com/c/5583452>
2. Low - trivial conflicts
3. M124, M125, M126
4. Yes

### ap...@google.com (2024-06-07)

Project: chromium/src
Branch: refs/branch-heads/6099

commit c5d65d649a9faf7d12fd4b24b9c7371b9701ffb4
Author: Zakhar Voit <voit@google.com>
Date:   Fri Jun 07 11:26:03 2024

    [M120-LTS] MediaSession: Use a MediaSessionImpl WeakPtr in MediaSessionServiceImpl
    
    Currently, every time MediaSessionServiceImpl wants to talk to its
    associated MediaSessionImpl, it recalculates it from its
    RenderFrameHostId. This can lead to issues where a
    MediaSessionServiceImpl of a disconnected RenderFrameHost can no longer
    access the MediaSessionImpl to tell it that it is being deleted,
    leaving MediaSessionImpl with a dangling raw_ptr.
    
    (cherry picked from commit 1f0de3303671c6c041930c7f4f8a9ad017a7f211)
    
    (cherry picked from commit 11c5f7911caab6930812a515eac27e35776ba35c)
    
    Bug: 338929744
    Change-Id: I092d217d4a975b67a84280687ed5461a14ead98a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5577944
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Cr-Original-Commit-Position: refs/branch-heads/6367@{#1245}
    Cr-Original-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5583452
    Owners-Override: Michael Ershov <miersh@google.com>
    Commit-Queue: Michael Ershov <miersh@google.com>
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
    Reviewed-by: Michael Ershov <miersh@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#2035}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       content/browser/media/session/media_session_impl.cc
M       content/browser/media/session/media_session_impl.h
M       content/browser/media/session/media_session_service_impl.cc
M       content/browser/media/session/media_session_service_impl.h

https://chromium-review.googlesource.com/5583452


### pe...@google.com (2024-08-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/338929744)*
