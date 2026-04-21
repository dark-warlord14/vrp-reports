# Security: Heap-use-after-free in location::nearby::chrome::ScheduledExecutor::PendingTaskWithTimer

| Field | Value |
|-------|-------|
| **Issue ID** | [40059392](https://issues.chromium.org/issues/40059392) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pu...@google.com |
| **Created** | 2022-04-16 |
| **Bounty** | $3,000.00 |

## Description

Chromium 102.0.5001.0 Ozone X11 (chromeOS)

**REPRODUCTION CASE**  

This crash occurred during shutdown, I don't have specific steps to repro it again, but still trying to figure it out.

=================================================================  

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b000003418 at pc 0x55d320bb6400 bp 0x7f20648d4480 sp 0x7f20648d4478  

READ of size 8 at 0x60b000003418 thread T3 (ThreadPoolForeg)  

==1==WARNING: invalid path to external symbolizer!  

==1==WARNING: Failed to use and restart external symbolizer!  

#0 0x55d320bb63ff in \_\_root ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1079:59  

#1 0x55d320bb63ff in std::\_\_1::\_\_tree\_iterator<std::\_\_1::\_\_value\_type<base::UnguessableToken, std::\_\_1::unique\_ptr<location::nearby::chrome::ScheduledExecutor::PendingTaskWithTimer, std::\_\_1::default\_delete[location::nearby::chrome::ScheduledExecutor::PendingTaskWithTimer](javascript:void(0);) > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<base::UnguessableToken, std::\_\_1::unique\_ptr<location::nearby::chrome::ScheduledExecutor::PendingTaskWithTimer, std::\_\_1::default\_delete[location::nearby::chrome::ScheduledExecutor::PendingTaskWithTimer](javascript:void(0);) > >, void\*>\*, long> std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::UnguessableToken, std::\_\_1::unique\_ptr<location::nearby::chrome::ScheduledExecutor::PendingTaskWithTimer, std::\_\_1::default\_delete[location::nearby::chrome::ScheduledExecutor::PendingTaskWithTimer](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<base::UnguessableToken, std::\_\_1::\_\_value\_type<base::UnguessableToken, std::\_\_1::unique\_ptr<location::nearby::chrome::ScheduledExecutor::PendingTaskWithTimer, std::\_\_1::default\_delete[location::nearby::chrome::ScheduledExecutor::PendingTaskWithTimer](javascript:void(0);) > >, std::\_\_1::less[base::UnguessableToken](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::UnguessableToken, std::\_\_1::unique\_ptr<location::nearby::chrome::ScheduledExecutor::PendingTaskWithTimer, std::\_\_1::default\_delete[location::nearby::chrome::ScheduledExecutor::PendingTaskWithTimer](javascript:void(0);) > > > >::find[base::UnguessableToken](javascript:void(0);)(base::UnguessableToken const&) ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:2466:39  

#2 0x55d320bb4eb1 in find ./../../buildtools/third\_party/libc++/trunk/include/map:1391:68  

#3 0x55d320bb4eb1 in location::nearby::chrome::ScheduledExecutor::StartTimerWithId(base::UnguessableToken const&, base::TimeDelta) ./../../chrome/services/sharing/nearby/platform/scheduled\_executor.cc:123:29  

#4 0x55d32108e466 in Run ./../../base/callback.h:142:12  

#5 0x55d32108e466 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#6 0x55d3210f7f5a in RunTask<(lambda at ../../base/task/thread\_pool/task\_tracker.cc:710:35)> ./../../base/task/common/task\_annotator.h:74:5  

#7 0x55d3210f7f5a in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource\*, base::SequenceToken const&) ./../../base/task/thread\_pool/task\_tracker.cc:709:19  

#8 0x55d3210f8e1a in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource\*, base::SequenceToken const&) ./../../base/task/thread\_pool/task\_tracker.cc:694:3  

#9 0x55d3210f76e0 in RunTaskWithShutdownBehavior ./../../base/task/thread\_pool/task\_tracker.cc:724:7  

#10 0x55d3210f76e0 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource\*, base::TaskTraits const&) ./../../base/task/thread\_pool/task\_tracker.cc:551:5  

#11 0x55d3211addee in base::internal::TaskTrackerPosix::RunTask(base::internal::Task, base::internal::TaskSource\*, base::TaskTraits const&) ./../../base/task/thread\_pool/task\_tracker\_posix.cc:22:16  

#12 0x55d3210f6aec in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread\_pool/task\_tracker.cc:469:5  

#13 0x55d32110ed8a in base::internal::WorkerThread::RunWorker() ./../../base/task/thread\_pool/worker\_thread.cc:381:34  

#14 0x55d32110e364 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread\_pool/worker\_thread.cc:268:3  

#15 0x55d3211af0df in base::(anonymous namespace)::ThreadFunc(void\*) ./../../base/threading/platform\_thread\_posix.cc:100:13  

#16 0x7f206e8e6608 in start\_thread /build/glibc-sMfBJT/glibc-2.31/nptl/pthread\_create.c:477:8

0x60b000003418 is located 72 bytes inside of 104-byte region [0x60b0000033d0,0x60b000003438)  

freed by thread T0 (chrome) here:  

#0 0x55d3129118ed in operator delete(void\*) *asan\_rtl*:3  

#1 0x55d320bf8e89 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#2 0x55d320bf8e89 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#3 0x55d320bf8e89 in DoShutdown ./../../third\_party/nearby/src/internal/platform/scheduled\_executor.h:98:13  

#4 0x55d320bf8e89 in location::nearby::ScheduledExecutor::~ScheduledExecutor() ./../../third\_party/nearby/src/internal/platform/scheduled\_executor.h:51:5  

#5 0x55d320c653b1 in location::nearby::connections::ClientProxy::~ClientProxy() ./../../third\_party/nearby/src/connections/implementation/client\_proxy.cc:58:40  

#6 0x55d320bf07f9 in location::nearby::connections::Core::~Core() ./../../third\_party/nearby/src/connections/core.cc:45:1  

#7 0x55d320b89f5a in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#8 0x55d320b89f5a in std::\_\_1::unique\_ptr<location::nearby::connections::Core, std::\_\_1::default\_delete[location::nearby::connections::Core](javascript:void(0);) >::reset(location::nearby::connections::Core\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#9 0x55d320b7011f in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:269:19  

#10 0x55d320b7011f in ~pair ./../../buildtools/third\_party/libc++/trunk/include/utility:394:29  

#11 0x55d320b7011f in std::\_\_1::allocator<std::\_\_1::pair<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::unique\_ptr<location::nearby::connections::Core, std::\_\_1::default\_delete[location::nearby::connections::Core](javascript:void(0);) > > >::destroy(std::\_\_1::pair<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::unique\_ptr<location::nearby::connections::Core, std::\_\_1::default\_delete[location::nearby::connections::Core](javascript:void(0);) > >\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator.h:133:15  

#12 0x55d320b8256d in destroy<std::\_\_1::pair<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::unique\_ptr<location::nearby::connections::Core, std::\_\_1::default\_delete[location::nearby::connections::Core](javascript:void(0);) > >, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:308:13  

#13 0x55d320b8256d in \_\_destruct\_at\_end ./../../buildtools/third\_party/libc++/trunk/include/vector:429:9  

#14 0x55d320b8256d in clear ./../../buildtools/third\_party/libc++/trunk/include/vector:372:29  

#15 0x55d320b8256d in std::\_\_1::vector<std::\_\_1::pair<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::unique\_ptr<location::nearby::connections::Core, std::\_\_1::default\_delete[location::nearby::connections::Core](javascript:void(0);) > >, std::\_\_1::allocator<std::\_\_1::pair<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::unique\_ptr<location::nearby::connections::Core, std::\_\_1::default\_delete[location::nearby::connections::Core](javascript:void(0);) > > > >::clear() ./../../buildtools/third\_party/libc++/trunk/include/vector:775:17  

#16 0x55d320b69806 in clear ./../../base/containers/flat\_tree.h:681:9  

#17 0x55d320b69806 in location::nearby::connections::NearbyConnections::~NearbyConnections() ./../../chrome/services/sharing/nearby/nearby\_connections.cc:196:27  

#18 0x55d320b69cfd in location::nearby::connections::NearbyConnections::~NearbyConnections() ./../../chrome/services/sharing/nearby/nearby\_connections.cc:191:41  

#19 0x55d320b647a0 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#20 0x55d320b647a0 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#21 0x55d320b647a0 in sharing::SharingImpl::DoShutDown(bool) ./../../chrome/services/sharing/sharing\_impl.cc:53:23  

#22 0x55d320b6466c in sharing::SharingImpl::ShutDown(base::OnceCallback<void ()>) ./../../chrome/services/sharing/sharing\_impl.cc:45:3  

#23 0x55d31694d2e8 in sharing::mojom::SharingStubDispatch::AcceptWithResponder(sharing::mojom::Sharing\*, mojo::Message\*, std::\_\_1::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_1::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) ./gen/ash/services/nearby/public/mojom/sharing.mojom.cc:401:13  

#24 0x55d3228363ea in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:884:56  

#25 0x55d322849a57 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#26 0x55d3228396dc in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:664:20  

#27 0x55d32285327e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#28 0x55d3228521ec in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:716:7  

#29 0x55d322849a57 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#30 0x55d32282e2ed in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:561:49  

#31 0x55d32282faa0 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:618:14  

#32 0x55d3228191ba in Run ./../../base/callback.h:241:12  

#33 0x55d3228191ba in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#34 0x55d32108e466 in Run ./../../base/callback.h:142:12  

#35 0x55d32108e466 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#36 0x55d3210cfbad in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:388:29)> ./../../base/task/common/task\_annotator.h:74:5  

#37 0x55d3210cfbad in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:386:21  

#38 0x55d3210cf2c7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:291:41  

#39 0x55d3210d0881 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#40 0x55d320f89386 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39:55  

#41 0x55d3210d0f39 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:498:12  

#42 0x55d32100802c in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#43 0x55d320a8b81d in content::UtilityMain(content::MainFunctionParams) ./../../content/utility/utility\_main.cc:275:12  

#44 0x55d320de3902 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:609:14

previously allocated by thread T0 (chrome) here:  

#0 0x55d31291108d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55d320b8da25 in make\_unique<location::nearby::chrome::ScheduledExecutor, scoped\_refptr[base::SequencedTaskRunner](javascript:void(0);) > ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:725:28  

#2 0x55d320b8da25 in location::nearby::api::ImplementationPlatform::CreateScheduledExecutor() ./../../chrome/services/sharing/nearby/platform.cc:94:10  

#3 0x55d320c64566 in ScheduledExecutor ./../../third\_party/nearby/src/internal/platform/scheduled\_executor.h:47:31  

#4 0x55d320c64566 in location::nearby::connections::ClientProxy::ClientProxy(location::nearby::analytics::EventLogger\*) ./../../third\_party/nearby/src/connections/implementation/client\_proxy.cc:47:14  

#5 0x55d320bf044b in location::nearby::connections::Core::Core(location::nearby::connections::ServiceControllerRouter\*) ./../../third\_party/nearby/src/connections/core.cc:34:7  

#6 0x55d320b6a94e in make\_unique<location::nearby::connections::Core, location::nearby::connections::ServiceControllerRouter \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:725:32  

#7 0x55d320b6a94e in location::nearby::connections::NearbyConnections::GetCore(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) ./../../chrome/services/sharing/nearby/nearby\_connections.cc:637:12  

#8 0x55d320b6a13a in location::nearby::connections::NearbyConnections::StartAdvertising(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, std::\_\_1::vector<unsigned char, std::\_\_1::allocator<unsigned char> > const&, mojo::StructPtr[location::nearby::connections::mojom::AdvertisingOptions](javascript:void(0);), mojo::PendingRemote[location::nearby::connections::mojom::ConnectionLifecycleListener](javascript:void(0);), base::OnceCallback<void (location::nearby::connections::mojom::Status)>) ./../../chrome/services/sharing/nearby/nearby\_connections.cc:266:3  

#9 0x55d3169251d2 in location::nearby::connections::mojom::NearbyConnectionsStubDispatch::AcceptWithResponder(location::nearby::connections::mojom::NearbyConnections\*, mojo::Message\*, std::\_\_1::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_1::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) ./gen/ash/services/nearby/public/mojom/nearby\_connections.mojom.cc:4527:13  

#10 0x55d3228363ea in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:884:56  

#11 0x55d322849a57 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#12 0x55d3228396dc in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:664:20  

#13 0x55d32285327e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#14 0x55d3228521ec in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:716:7  

#15 0x55d322849a57 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#16 0x55d32282e2ed in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:561:49  

#17 0x55d32282faa0 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:618:14  

#18 0x55d3228191ba in Run ./../../base/callback.h:241:12  

#19 0x55d3228191ba in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#20 0x55d32108e466 in Run ./../../base/callback.h:142:12  

#21 0x55d32108e466 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#22 0x55d3210cfbad in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:388:29)> ./../../base/task/common/task\_annotator.h:74:5  

#23 0x55d3210cfbad in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:386:21  

#24 0x55d3210cf2c7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:291:41  

#25 0x55d3210d0881 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#26 0x55d320f89386 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39:55  

#27 0x55d3210d0f39 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:498:12  

#28 0x55d32100802c in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#29 0x55d320a8b81d in content::UtilityMain(content::MainFunctionParams) ./../../content/utility/utility\_main.cc:275:12  

#30 0x55d320de3902 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:609:14  

#31 0x55d320de4f51 in content::RunOtherNamedProcessTypeMain(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:691:12  

#32 0x55d320de6894 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1021:10  

#33 0x55d320de1081 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:407:36  

#34 0x55d320de1708 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:435:10  

#35 0x55d31291386a in ChromeMain ./../../chrome/app/chrome\_main.cc:176:12

Thread T3 (ThreadPoolForeg) created by T2 (ThreadPoolForeg) here:  

#0 0x55d3128c92fc in pthread\_create *asan\_rtl*:3  

#1 0x55d3211ae4a1 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadPriority) ./../../base/threading/platform\_thread\_posix.cc:143:13  

#2 0x55d32110d6dd in base::internal::WorkerThread::Start(base::WorkerThreadObserver\*) ./../../base/task/thread\_pool/worker\_thread.cc:111:3  

#3 0x55d321108bc5 in operator() ./../../base/task/thread\_pool/thread\_group\_impl.cc:186:15  

#4 0x55d321108bc5 in void base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker[base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread\\*)](javascript:void(0);)(base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread\*)) ./../../base/task/thread\_pool/thread\_group\_impl.cc:153:9  

#5 0x55d32110874c in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl() ./../../base/task/thread\_pool/thread\_group\_impl.cc:185:23  

#6 0x55d321102706 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushWorkerCreation(base::internal::CheckedLock\*) ./../../base/task/thread\_pool/thread\_group\_impl.cc:118:5  

#7 0x55d321101e89 in base::internal::ThreadGroupImpl::WorkerThreadDelegateImpl::GetWork(base::internal::WorkerThread\*) ./../../base/task/thread\_pool/thread\_group\_impl.cc:618:14  

#8 0x55d32110ece8 in base::internal::WorkerThread::RunWorker() ./../../base/task/thread\_pool/worker\_thread.cc:362:51  

#9 0x55d32110e364 in base::internal::WorkerThread::RunPooledWorker() ./../../base/task/thread\_pool/worker\_thread.cc:268:3  

#10 0x55d3211af0df in base::(anonymous namespace)::ThreadFunc(void\*) ./../../base/threading/platform\_thread\_posix.cc:100:13  

#11 0x7f206e8e6608 in start\_thread /build/glibc-sMfBJT/glibc-2.31/nptl/pthread\_create.c:477:8

Thread T2 (ThreadPoolForeg) created by T0 (chrome) here:  

#0 0x55d3128c92fc in pthread\_create *asan\_rtl*:3  

#1 0x55d3211ae4a1 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadPriority) ./../../base/threading/platform\_thread\_posix.cc:143:13  

#2 0x55d32110d6dd in base::internal::WorkerThread::Start(base::WorkerThreadObserver\*) ./../../base/task/thread\_pool/worker\_thread.cc:111:3  

#3 0x55d321108bc5 in operator() ./../../base/task/thread\_pool/thread\_group\_impl.cc:186:15  

#4 0x55d321108bc5 in void base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker[base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread\\*)](javascript:void(0);)(base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread\*)) ./../../base/task/thread\_pool/thread\_group\_impl.cc:153:9  

#5 0x55d32110874c in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl() ./../../base/task/thread\_pool/thread\_group\_impl.cc:185:23  

#6 0x55d3210ffe98 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() ./../../base/task/thread\_pool/thread\_group\_impl.cc:104:31  

#7 0x55d3210ff43d in base::internal::ThreadGroupImpl::Start(int, int, base::TimeDelta, scoped\_refptr[base::SequencedTaskRunner](javascript:void(0);), base::WorkerThreadObserver\*, base::internal::ThreadGroup::WorkerEnvironment, bool, absl::optional[base::TimeDelta](javascript:void(0);)) ./../../base/task/thread\_pool/thread\_group\_impl.cc:441:1  

#8 0x55d3210e2ce8 in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver\*) ./../../base/task/thread\_pool/thread\_pool\_impl.cc:227:11  

#9 0x55d32110ce30 in StartWithDefaultParams ./../../base/task/thread\_pool/thread\_pool\_instance.cc:69:3  

#10 0x55d32110ce30 in base::ThreadPoolInstance::CreateAndStartWithDefaultParams(base::BasicStringPiece<char, std::\_\_1::char\_traits<char> >) ./../../base/task/thread\_pool/thread\_pool\_instance.cc:57:18  

#11 0x55d32f566121 in content::ChildProcess::ChildProcess(base::ThreadPriority, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, std::\_\_1::unique\_ptr<base::ThreadPoolInstance::InitParams, std::\_\_1::default\_delete[base::ThreadPoolInstance::InitParams](javascript:void(0);) >) ./../../content/child/child\_process.cc:98:7  

#12 0x55d320a8b5a9 in content::UtilityMain(content::MainFunctionParams) ./../../content/utility/utility\_main.cc:211:16  

#13 0x55d320de3902 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:609:14  

#14 0x55d320de4f51 in content::RunOtherNamedProcessTypeMain(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:691:12  

#15 0x55d320de6894 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1021:10  

#16 0x55d320de1081 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:407:36  

#17 0x55d320de1708 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:435:10  

#18 0x55d31291386a in ChromeMain ./../../chrome/app/chrome\_main.cc:176:12  

#19 0x7f206d9d90b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/asan-linux-release-991831/chrome+0x1c5863ff) (BuildId: cb3cce5833f729b9)  

Shadow bytes around the buggy address:  

0x0c167fff8630: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c167fff8640: 00 00 00 00 00 fa fa fa fa fa fa fa fa fa 00 00  

0x0c167fff8650: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  

0x0c167fff8660: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c167fff8670: fd fa fa fa fa fa fa fa fa fa fd fd fd fd fd fd  

=>0x0c167fff8680: fd fd fd[fd]fd fd fd fa fa fa fa fa fa fa fa fa  

0x0c167fff8690: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

0x0c167fff86a0: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd  

0x0c167fff86b0: fd fd fd fd fa fa fa fa fa fa fa fa fd fd fd fd  

0x0c167fff86c0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x0c167fff86d0: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

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

## Attachments

- [screen.webm](attachments/screen.webm) (video/webm, 8.9 MB)

## Timeline

### [Deleted User] (2022-04-16)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-04-19)

1. Click on "Nearby visibility"
2. Run Chromium
3. Double-click  on Nearby icon + press ESC key quickly

### mp...@chromium.org (2022-04-19)

The root cause is the base::Unretained(this) used here [0]. It's used for a callback that runs after a timer, making the race window quite large. There are many uses of this, possibly triggerable from another device on a local network.

It looks like the freed object is deleted by NearbyConnections::OnDisconnect() [1] . This is typically during shutdown but can also be called if the network service crashes [2]. I wouldn't be surprised if you could crash the network service remotely with an OOM. So, you could maybe free the used object at will.

So to exploit this remotely you could potentially set off the callback and crash the network service remotely. I don't know how you would fill the freed object's spot with an attacker-controlled object but it's probably possible with some creativity.

Reporter, if you could demonstrate a remote exploit of this (I'm not sure it's possible) the VRP would likely be more generous with the reward.

For now I'll assign this High severity as the remote triggerability is all speculation by me, and exploitation is likely pretty difficult. But this might need an upgrade to critical severity.

nohle@ can you handle this one?

[0] https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/sharing/nearby/platform/scheduled_executor.cc;drc=c4b56465e4821b2a357367c76e72bc96b8acb65a;l=109
[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/sharing/nearby/nearby_connections.cc;drc=c4b56465e4821b2a357367c76e72bc96b8acb65a;bpv=1;bpt=1;l=231
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/sharing/nearby/nearby_connections.cc;drc=c4b56465e4821b2a357367c76e72bc96b8acb65a;l=123

### [Deleted User] (2022-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### no...@chromium.org (2022-04-19)

Thank you for the report, and thank you Matt for diagnosing! Does this happen on an actual Chromebook or just Chrome OS on Linux?

Pu and Michael, do you want to tackle this one?

### no...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

### pu...@google.com (2022-04-19)

I tried to reproduce this on my DUT (volteer, 102.0.5005.5) but failed.

### ch...@gmail.com (2022-04-20)

Sometimes looks like it can take several tries to repro the crash.

### jo...@chromium.org (2022-04-20)

pushi@ did you deploy an ASAN build of chrome?

This can be done by setting is_asan = true and is_debug = false in 
gn args out_{BOARD}/Release

### pu...@google.com (2022-04-20)

jonmann@ No I did not. I'll deploy an ASAN build to the DUT. Thanks for the suggestion! 

### no...@chromium.org (2022-04-22)

[Comment Deleted]

### no...@chromium.org (2022-04-22)

Here's my read of it. TL;DR: I think Matt is right in https://crbug.com/chromium/1316846#c3 that using weak ptrs will solve this issue. But, here's why I think this happens:

1. |id_to_task_map_| is destroyed before the |timer_task_runner_|. It's swapped with a temp variable in the dtor [1]; regardless, it's also declared _after_ the |timer_task_runner_| [2]. So the map is definitely not there when |timer_task_runner_| is destroyed. (Note that the weak pointers will be invalidated before everything is destroyed, as intended [3]. So that's good.)

2. StartTimerWithId is added to the |timer_task_runner_| [4], and this function references |id_to_task_map_| [5] where we see the crash. I'm a little surprised that using |lock_| doesn't trigger a crash.

3. Here's what I don't understand: Is the |timer_task_runner_| flushed--i.e., all tasks run--before destruction? If so, then it makes sense why StartTimerWIthId would be run after |id_to_task_map_| is destroyed.

[1]https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/sharing/nearby/platform/scheduled_executor.cc;l=64;drc=58a09444b081d0fb2f533b4352815cb63395f026
[2]https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/sharing/nearby/platform/scheduled_executor.h;l=78;drc=bdd68018e8248518e988b1ee5515cd34b96ef8b3
[3]https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/sharing/nearby/platform/scheduled_executor.h;l=80;drc=bdd68018e8248518e988b1ee5515cd34b96ef8b3
[4]https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/sharing/nearby/platform/scheduled_executor.cc;l=109;drc=58a09444b081d0fb2f533b4352815cb63395f026
[5]https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/sharing/nearby/platform/scheduled_executor.cc;l=123;drc=58a09444b081d0fb2f533b4352815cb63395f026

### gi...@appspot.gserviceaccount.com (2022-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6b9fb62ad4bbf7a516e5cf99ccd367a6d4c19b82

commit 6b9fb62ad4bbf7a516e5cf99ccd367a6d4c19b82
Author: Pu Shi <pushi@google.com>
Date: Fri Apr 22 19:00:20 2022

[Nearby] Fix crash caused by base::Unretained during shutdown

In the ScheduledExecutor class the use of base::Unretained(this) in
a callback caused a crash during the shutdown process when the object
has been destroyed. Replacing them with weak pointers will make sure
the callback will not run if the object has been destroyed.

Bug:1316846
TEST = manually tested and passed unit tests

Change-Id: Ia1df0fe5f4d190ce247eb3a38b3983d54a245855
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3600852
Reviewed-by: Josh Nohle <nohle@chromium.org>
Commit-Queue: Pu Shi <pushi@google.com>
Cr-Commit-Position: refs/heads/main@{#995295}

[modify] https://crrev.com/6b9fb62ad4bbf7a516e5cf99ccd367a6d4c19b82/chrome/services/sharing/nearby/platform/scheduled_executor.cc


### ts...@chromium.org (2022-04-22)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Sharing]

### ch...@gmail.com (2022-04-22)

Thanks for the quick fix! 

### no...@chromium.org (2022-04-28)

I'll need to revert this fix. Unfortunately, hansenmichael@ noticed that this causes a DCHECK crash of the utility process because the weak ptr isn't used on the correct sequence. See [1]. Here's the stack trace:

2022-04-28T19:25:21.984461Z FATAL chrome[7942:22]: [sequence_checker.cc(21)] Check failed: checker.CalledOnValidSequence(&bound_at). 
#0 0x7f515d18ea19 base::debug::CollectStackTrace()
#1 0x7f515d034413 base::debug::StackTrace::StackTrace()
#2 0x7f515d05e3e3 logging::LogMessage::~LogMessage()
#3 0x7f515d05ee5e logging::LogMessage::~LogMessage()
#4 0x7f515d0bc329 base::ScopedValidateSequenceChecker::ScopedValidateSequenceChecker()
#5 0x7f515d06cd84 base::internal::WeakReference::IsValid()
#6 0x568025f78258 location::nearby::chrome::ScheduledExecutor::TryCancelTask()
#7 0x568025f78e58 base::internal::Invoker<>::RunOnce()
#8 0x56802451b81b _ZNO4base12OnceCallbackIFbvEE3RunEv
#9 0x568025f99c9c location::nearby::CancelableAlarm::Cancel()
#10 0x568025fb9f41 std::__1::__function::__func<>::operator()()
#11 0x568025f86c9f location::nearby::MonitoredRunnable::operator()()
#12 0x568025f7933b location::nearby::chrome::SubmittableExecutor::RunTask()
#13 0x7f515d0ea317 base::TaskAnnotator::RunTaskImpl()
#14 0x7f515d1484ea base::internal::TaskTracker::RunSkipOnShutdown()
#15 0x7f515d1477c1 base::internal::TaskTracker::RunTask()
#16 0x7f515d1a85e0 base::internal::TaskTrackerPosix::RunTask()
#17 0x7f515d14710e base::internal::TaskTracker::RunAndPopNextTask()
#18 0x7f515d157186 base::internal::WorkerThread::RunWorker()
#19 0x7f515d156e8a base::internal::WorkerThread::RunDedicatedWorker()
#20 0x7f515d1a917c base::(anonymous namespace)::ThreadFunc()
#21 0x7f5148d0ddb1 start_thread
#22 0x7f51487af1ff __GI___clone
Task trace:
#0 0x568025f79470 location::nearby::chrome::SubmittableExecutor::Execute()
#1 0x568025f79470 location::nearby::chrome::SubmittableExecutor::Execute()
#2 0x568025f79470 location::nearby::chrome::SubmittableExecutor::Execute()
#3 0x7f515c09d2cb mojo::SimpleWatcher::Context::CallNotify()
Crash keys:
  "service-name" = "sharing.mojom.Sharing"

[1]https://source.chromium.org/chromium/chromium/src/+/main:base/memory/weak_ptr.h;l=50;drc=b57ac1d5be7dd46af32318abaef882a5cfb11b69

### gi...@appspot.gserviceaccount.com (2022-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/350c96ec8a5bf1494577c47cabf7325934ed12a8

commit 350c96ec8a5bf1494577c47cabf7325934ed12a8
Author: Josh Nohle <nohle@chromium.org>
Date: Thu Apr 28 20:53:20 2022

Revert "[Nearby] Fix crash caused by base::Unretained during shutdown"

This reverts commit 6b9fb62ad4bbf7a516e5cf99ccd367a6d4c19b82.

Reason for revert: Causes DCHECK crash due to weak ptr used on wrong sequence.

Original change's description:
> [Nearby] Fix crash caused by base::Unretained during shutdown
>
> In the ScheduledExecutor class the use of base::Unretained(this) in
> a callback caused a crash during the shutdown process when the object
> has been destroyed. Replacing them with weak pointers will make sure
> the callback will not run if the object has been destroyed.
>
> Bug:1316846
> TEST = manually tested and passed unit tests
>
> Change-Id: Ia1df0fe5f4d190ce247eb3a38b3983d54a245855
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3600852
> Reviewed-by: Josh Nohle <nohle@chromium.org>
> Commit-Queue: Pu Shi <pushi@google.com>
> Cr-Commit-Position: refs/heads/main@{#995295}

Bug: 1316846
Change-Id: Idab77df118c2da3cd41e79bc0b95f6989850a0a7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3614415
Commit-Queue: Josh Nohle <nohle@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Josh Nohle <nohle@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Michael Hansen <hansenmichael@google.com>
Cr-Commit-Position: refs/heads/main@{#997399}

[modify] https://crrev.com/350c96ec8a5bf1494577c47cabf7325934ed12a8/chrome/services/sharing/nearby/platform/scheduled_executor.cc


### [Deleted User] (2022-05-05)

pushi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pu...@google.com (2022-05-05)

Dived deeper into this issue, here are some updates:

1: The root cause of the original UAF crash is the use of base::Unretained(this)[1] when binding an object to a callback function. This does not guarantee the callback function would be cancelled when the bound object gets destroyed. In this crash, the destruction happened when a task had started to run and UAF happened at this line[2].
2: The root cause of the sequence checker failure that Michael encountered after I replaced base::Unretained(this) to weak pointer[3] is that weak pointer issued by WeakFactory cannot be dereferenced or invalidated on any other task runner since the first time it's dereferenced and invalidated on the calling sequence[4]. And my change is conflict to this line[5]

The next step is to use the correct way to pass weak pointers between different sequences.

[1]https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/sharing/nearby/platform/scheduled_executor.cc;l=110;drc=287fa204b78ccaa8da5c1a155c5fbfacafef31c8;bpv=1;bpt=1
[2]https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/sharing/nearby/platform/scheduled_executor.cc;l=123;drc=287fa204b78ccaa8da5c1a155c5fbfacafef31c8;bpv=1;bpt=1
[3]https://chromium-review.googlesource.com/c/chromium/src/+/3600852
[4]https://source.chromium.org/chromium/chromium/src/+/main:base/memory/weak_ptr.h;l=56;drc=287fa204b78ccaa8da5c1a155c5fbfacafef31c8
[5]https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/sharing/nearby/platform/scheduled_executor.cc;l=114;drc=287fa204b78ccaa8da5c1a155c5fbfacafef31c8;bpv=1;bpt=1

### pu...@google.com (2022-05-16)

The new fix has been merged last Thursday 05/12. https://chromium-review.googlesource.com/c/chromium/src/+/3642637

### [Deleted User] (2022-05-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-16)

Requesting merge to extended stable M100 because latest trunk commit (995295) appears to be after extended stable branch point (972766).

Requesting merge to stable M101 because latest trunk commit (995295) appears to be after stable branch point (982481).

Requesting merge to beta M102 because latest trunk commit (995295) appears to be after beta branch point (992738).

Not requesting merge to dev (M103) because latest trunk commit (995295) appears to be prior to dev branch point (1002911). If this is incorrect, please replace the Merge-NA-103 label with Merge-Request-103. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-16)

Merge review required: M102 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-16)

Merge review required: M101 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-16)

Merge review required: M100 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pu...@google.com (2022-05-16)

Merge review required: M102 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
This is a UAF crash fix and M102 is in Phase 1.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3642637

3. Have the changes been released and tested on canary?
No. Tested on DUT with different boards.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
No. Eng Prod testing is not required.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No it does not require manual verification by the test team.


### pu...@google.com (2022-05-16)

Merge review required: M101 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
This is a UAF crash fix and M101 is in Phase 2.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3642637

3. Have the changes been released and tested on canary?
No. Tested on DUT with different boards.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
No. Eng Prod testing is not required.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No it does not require manual verification by the test team.

### pu...@google.com (2022-05-16)

Merge review required: M100 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
This is a UAF crash fix.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3642637

3. Have the changes been released and tested on canary?
No. Tested on DUT with different boards.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
No. Eng Prod testing is not required.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No it does not require manual verification by the test team.

### ma...@google.com (2022-05-16)

Approved, M101

### ce...@google.com (2022-05-17)

Merge approved for M102.

M100 is no longer being updated. I'm going to remove the merge review label for this milestone. Please reach out if additional discussion is needed.

### gi...@appspot.gserviceaccount.com (2022-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/50d38261850ce63ade572cac5898f3e26ee9e2d5

commit 50d38261850ce63ade572cac5898f3e26ee9e2d5
Author: Pu Shi <pushi@google.com>
Date: Tue May 17 15:51:17 2022

[Nearby] Fix use-after-free bug caused by use of base::Unretained(this)

The base::Unretained(this) is being used in the ScheduledExecutor to
bind callbacks to a SequencedTaskRunner, which causes use-after-free
bug. By adding a separate WeakPtrFactory, it ensures the pointer to
the object gets invalidated before invoking callback function in the
task runner.

(cherry picked from commit 85d5e104eaa7f75f4bd905629381a5898f2f1f7f)

Fixed: 1316846
TEST: manully tested with DCHECKs enabled and passed unit tests.
Change-Id: Id11f404779336a22a718f4c5b6a3cb88f80bdfb1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3642637
Commit-Queue: Pu Shi <pushi@google.com>
Reviewed-by: Josh Nohle <nohle@chromium.org>
Commit-Queue: Michael Hansen <hansenmichael@google.com>
Reviewed-by: Michael Hansen <hansenmichael@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1002936}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3651280
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#809}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/50d38261850ce63ade572cac5898f3e26ee9e2d5/chrome/services/sharing/nearby/platform/scheduled_executor.cc
[modify] https://crrev.com/50d38261850ce63ade572cac5898f3e26ee9e2d5/chrome/services/sharing/nearby/platform/scheduled_executor.h


### [Deleted User] (2022-05-17)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2254445512d7389d5c4377b67b5005e3f01ce8a8

commit 2254445512d7389d5c4377b67b5005e3f01ce8a8
Author: Pu Shi <pushi@google.com>
Date: Tue May 17 16:03:44 2022

[Nearby] Fix use-after-free bug caused by use of base::Unretained(this)

The base::Unretained(this) is being used in the ScheduledExecutor to
bind callbacks to a SequencedTaskRunner, which causes use-after-free
bug. By adding a separate WeakPtrFactory, it ensures the pointer to
the object gets invalidated before invoking callback function in the
task runner.

(cherry picked from commit 85d5e104eaa7f75f4bd905629381a5898f2f1f7f)

Fixed: 1316846
TEST: manully tested with DCHECKs enabled and passed unit tests.
Change-Id: Id11f404779336a22a718f4c5b6a3cb88f80bdfb1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3642637
Commit-Queue: Pu Shi <pushi@google.com>
Reviewed-by: Josh Nohle <nohle@chromium.org>
Commit-Queue: Michael Hansen <hansenmichael@google.com>
Reviewed-by: Michael Hansen <hansenmichael@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1002936}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3651398
Reviewed-by: Ryan Hansberry <hansberry@chromium.org>
Cr-Commit-Position: refs/branch-heads/4951@{#1259}
Cr-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}

[modify] https://crrev.com/2254445512d7389d5c4377b67b5005e3f01ce8a8/chrome/services/sharing/nearby/platform/scheduled_executor.cc
[modify] https://crrev.com/2254445512d7389d5c4377b67b5005e3f01ce8a8/chrome/services/sharing/nearby/platform/scheduled_executor.h


### pu...@google.com (2022-05-17)

1. Was this issue a regression for the milestone it was found in?
No.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?
No.

### [Deleted User] (2022-05-17)

[Empty comment from Monorail migration]

### vo...@google.com (2022-05-19)

[Empty comment from Monorail migration]

### vo...@google.com (2022-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-05-20)

[Empty comment from Monorail migration]

### pu...@google.com (2022-05-20)

I'm not sure if I'm supposed to answer these questions but I'll try my best.

1. Number of CLs needed for this fix and links to them.
One CL, https://chromium-review.googlesource.com/c/chromium/src/+/3642637

2. Level of complexity (High, Medium, Low - Explain)
Low. The fix only contains minor change that adds weak pointers. Passed all tests.

3. Has this been merged to a stable release? beta release?
Yes. It has been merged to M101 and M102

4. Overall Recommendation (Yes, No)
Yes

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### gm...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6cb7135bb27987a05aaba2ebb326589ed1745c87

commit 6cb7135bb27987a05aaba2ebb326589ed1745c87
Author: Pu Shi <pushi@google.com>
Date: Thu May 26 12:30:34 2022

[M96-LTS][Nearby] Fix use-after-free bug caused by use of base::Unretained(this)

The base::Unretained(this) is being used in the ScheduledExecutor to
bind callbacks to a SequencedTaskRunner, which causes use-after-free
bug. By adding a separate WeakPtrFactory, it ensures the pointer to
the object gets invalidated before invoking callback function in the
task runner.

(cherry picked from commit 85d5e104eaa7f75f4bd905629381a5898f2f1f7f)

(cherry picked from commit 2254445512d7389d5c4377b67b5005e3f01ce8a8)

Fixed: 1316846
TEST: manully tested with DCHECKs enabled and passed unit tests.
Change-Id: Id11f404779336a22a718f4c5b6a3cb88f80bdfb1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3642637
Commit-Queue: Pu Shi <pushi@google.com>
Commit-Queue: Michael Hansen <hansenmichael@google.com>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1002936}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3651398
Cr-Original-Commit-Position: refs/branch-heads/4951@{#1259}
Cr-Original-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3653768
Reviewed-by: Simon Hangl <simonha@google.com>
Owners-Override: Simon Hangl <simonha@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1637}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/6cb7135bb27987a05aaba2ebb326589ed1745c87/chrome/services/sharing/nearby/platform/scheduled_executor.cc
[modify] https://crrev.com/6cb7135bb27987a05aaba2ebb326589ed1745c87/chrome/services/sharing/nearby/platform/scheduled_executor.h


### am...@google.com (2022-05-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-27)

Congratulations, Khalil! The VRP Panel has decided to award you $3,000 for this report, due this issue not being web accessible and the user interaction required. Thank you for your efforts and reporting this issue to us! 

### vo...@google.com (2022-05-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1316846?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059392)*
