# Security: UAF in void perfetto::DataSource<perfetto::perfetto_track_event::TrackEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40062949](https://issues.chromium.org/issues/40062949) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Speed>Tracing |
| **Platforms** | Linux |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | kh...@google.com |
| **Created** | 2023-02-07 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in void perfetto::DataSource<perfetto::perfetto\_track\_event::TrackEvent

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**

1. unzip the webserver and run `python3 -m http.server 8000` in the webserver dir.
2. download the latest asan-linux build and run `./chrome --user-data-dir=/tmp/aaa --no-sandbox --trace-config-file http://localhost:8000/poc.html`

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]

=================================================================  

==29460==ERROR: AddressSanitizer: heap-use-after-free on address 0x62b0000d1418 at pc 0x557eecebd325 bp 0x7f429ea0db10 sp 0x7f429ea0db08  

READ of size 8 at 0x62b0000d1418 thread T13 (ServiceWorker t)  

==29460==WARNING: invalid path to external symbolizer!  

==29460==WARNING: Failed to use and restart external symbolizer!  

#0 0x557eecebd324 in void perfetto::DataSource<perfetto::perfetto\_track\_event::TrackEvent, perfetto::internal::TrackEventDataSourceTraits>::TraceWithInstances<perfetto::internal::TrackEventDataSource<perfetto::perfetto\_track\_event::TrackEvent, &perfetto::perfetto\_track\_event::internal::kCategoryRegistry>::CategoryTracePointTraits, void perfetto::internal::TrackEventDataSource<perfetto::perfetto\_track\_event::TrackEvent, &perfetto::perfetto\_track\_event::internal::kCategoryRegistry>::TraceForCategoryImpl<unsigned long, char [22], perfetto::Track, perfetto::TraceTimestamp, void, void, std::Cr::function<void (perfetto::EventContext&)>>(unsigned int, unsigned long const&, char const (&) [22], perfetto::protos::pbzero::perfetto\_pbzero\_enum\_TrackEvent::Type, perfetto::Track const&, perfetto::TraceTimestamp const&, std::Cr::function<void (perfetto::EventContext&)>&&)::'lambda'(perfetto::DataSource<perfetto::perfetto\_track\_event::TrackEvent, perfetto::internal::TrackEventDataSourceTraits>::TraceContext)>(unsigned int, char [22], unsigned long::TracePointData) ./../../third\_party/perfetto/include/perfetto/tracing/data\_source.h:397:9  

#1 0x557eecebc520 in TraceWithInstances<unsigned long, (lambda at ../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:531:30)> ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:613:7  

#2 0x557eecebc520 in TraceForCategoryImpl<unsigned long, char[22], perfetto::Track, perfetto::TraceTimestamp, void, void, std::Cr::function<void (perfetto::EventContext &)> > ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:530:5  

#3 0x557eecebc520 in void perfetto::internal::TrackEventDataSource<perfetto::perfetto\_track\_event::TrackEvent, &perfetto::perfetto\_track\_event::internal::kCategoryRegistry>::TraceForCategory<unsigned long, char [22], std::Cr::function<void (perfetto::EventContext&)>>(unsigned int, unsigned long const&, char const (&) [22], perfetto::protos::pbzero::perfetto\_pbzero\_enum\_TrackEvent::Type, std::Cr::function<void (perfetto::EventContext&)>&&) ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:312:5  

#4 0x557eecebc158 in operator() ./../../base/synchronization/waitable\_event.cc:17:5  

#5 0x557eecebc158 in void perfetto::internal::TrackEventDataSource<perfetto::perfetto\_track\_event::TrackEvent, &perfetto::perfetto\_track\_event::internal::kCategoryRegistry>::CallIfCategoryEnabled[base::WaitableEvent::Signal()::$\_0](javascript:void(0);)(unsigned long, base::WaitableEvent::Signal()::$\_0)::'lambda'(unsigned int)::operator()(unsigned int) const ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:289:43  

#6 0x557eecebba14 in CallIfEnabled<perfetto::internal::TrackEventDataSource<perfetto::perfetto\_track\_event::TrackEvent, &perfetto::perfetto\_track\_event::internal::kCategoryRegistry>::CategoryTracePointTraits, (lambda at ../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:289:9)> ./../../third\_party/perfetto/include/perfetto/tracing/data\_source.h:351:5  

#7 0x557eecebba14 in CallIfCategoryEnabled<(lambda at ../../base/synchronization/waitable\_event.cc:17:5)> ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:288:5  

#8 0x557eecebba14 in base::WaitableEvent::Signal() ./../../base/synchronization/waitable\_event.cc:17:5  

#9 0x557eecf439da in DecrementBy ./../../base/task/common/operations\_controller.cc:103:24  

#10 0x557eecf439da in base::internal::OperationsController::TryBeginOperation() ./../../base/task/common/operations\_controller.cc:56:7  

#11 0x557eecf22ca8 in base::sequence\_manager::internal::TaskQueueImpl::GuardedTaskPoster::PostTask(base::sequence\_manager::internal::PostedTask) ./../../base/task/sequence\_manager/task\_queue\_impl.cc:104:39  

#12 0x557eecf23f4f in base::sequence\_manager::internal::TaskQueueImpl::TaskRunner::PostDelayedTask(base::Location const&, base::OnceCallback<void ()>, base::TimeDelta) ./../../base/task/sequence\_manager/task\_queue\_impl.cc:144:24  

#13 0x557ee9703717 in blink::scheduler::BlinkSchedulerSingleThreadTaskRunner::PostDelayedTask(base::Location const&, base::OnceCallback<void ()>, base::TimeDelta) ./../../third\_party/blink/renderer/platform/scheduler/common/blink\_scheduler\_single\_thread\_task\_runner.h:50:20  

#14 0x557eecf8b008 in base::TaskRunner::PostTask(base::Location const&, base::OnceCallback<void ()>) ./../../base/task/task\_runner.cc:47:10  

#15 0x557eedaff382 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple\_watcher.cc:101:23  

#16 0x557eedafba1f in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const\*) ./../../mojo/public/cpp/system/simple\_watcher.cc:61:14  

#17 0x557edae95d67 in DispatchEvent ./../../mojo/core/ipcz\_driver/mojo\_trap.cc:577:3  

#18 0x557edae95d67 in mojo::core::ipcz\_driver::MojoTrap::DispatchOrQueueEvent(mojo::core::ipcz\_driver::MojoTrap::Trigger&, MojoTrapEvent const&) ./../../mojo/core/ipcz\_driver/mojo\_trap.cc:552:3  

#19 0x557edae9681e in DispatchOrQueueTriggerRemoval ./../../mojo/core/ipcz\_driver/mojo\_trap.cc:524:3  

#20 0x557edae9681e in mojo::core::ipcz\_driver::MojoTrap::RemoveTrigger(unsigned long) ./../../mojo/core/ipcz\_driver/mojo\_trap.cc:285:3  

#21 0x557eedafbf2b in mojo::SimpleWatcher::Cancel() ./../../mojo/public/cpp/system/simple\_watcher.cc:184:7  

#22 0x557eedafbbd3 in mojo::SimpleWatcher::~SimpleWatcher() ./../../mojo/public/cpp/system/simple\_watcher.cc:131:5  

#23 0x557eeda5cd38 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#24 0x557eeda5cd38 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#25 0x557eeda5cd38 in CancelWait ./../../mojo/public/cpp/bindings/lib/connector.cc:643:19  

#26 0x557eeda5cd38 in mojo::Connector::PassMessagePipe() ./../../mojo/public/cpp/bindings/lib/connector.cc:233:3  

#27 0x557eeda5cb77 in mojo::Connector::CloseMessagePipe() ./../../mojo/public/cpp/bindings/lib/connector.cc:227:3  

#28 0x557eeda8f845 in mojo::internal::MultiplexRouter::CloseMessagePipe() ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:567:14  

#29 0x557eeda83588 in mojo::internal::InterfacePtrStateBase::~InterfacePtrStateBase() ./../../mojo/public/cpp/bindings/lib/interface\_ptr\_state.cc:23:14  

#30 0x557ee96c7d1f in ~InterfacePtrState ./../../mojo/public/cpp/bindings/lib/interface\_ptr\_state.h:141:32  

#31 0x557ee96c7d1f in ~Remote ./../../mojo/public/cpp/bindings/remote.h:87:21  

#32 0x557ee96c7d1f in WTF::ThreadSpecific<mojo::Remote[blink::mojom::blink::BlobRegistry](javascript:void(0);)>::Destroy(void\*) ./../../third\_party/blink/renderer/platform/wtf/thread\_specific.h:95:14  

#33 0x557eed00d603 in OnThreadExitInternal ./../../base/threading/thread\_local\_storage.cc:354:7  

#34 0x557eed00d603 in base::internal::PlatformThreadLocalStorage::OnThreadExit(void\*) ./../../base/threading/thread\_local\_storage.cc:408:3  

#35 0x7f43b0607710 in \_\_GI\_\_\_nptl\_deallocate\_tsd ./nptl/nptl\_deallocate\_tsd.c:73:29  

#36 0x7f43b0607710 in \_\_GI\_\_\_nptl\_deallocate\_tsd ./nptl/nptl\_deallocate\_tsd.c:22:1

0x62b0000d1418 is located 25112 bytes inside of 25888-byte region [0x62b0000cb200,0x62b0000d1720)  

freed by thread T13 (ServiceWorker t) here:  

#0 0x557eda6a2a9d in operator delete(void\*) *asan\_rtl*:3  

#1 0x557eed00d603 in OnThreadExitInternal ./../../base/threading/thread\_local\_storage.cc:354:7  

#2 0x557eed00d603 in base::internal::PlatformThreadLocalStorage::OnThreadExit(void\*) ./../../base/threading/thread\_local\_storage.cc:408:3  

#3 0x7f43b0607710 in \_\_GI\_\_\_nptl\_deallocate\_tsd ./nptl/nptl\_deallocate\_tsd.c:73:29  

#4 0x7f43b0607710 in \_\_GI\_\_\_nptl\_deallocate\_tsd ./nptl/nptl\_deallocate\_tsd.c:22:1

previously allocated by thread T13 (ServiceWorker t) here:  

#0 0x557eda6a223d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x557eda7ff16f in perfetto::PlatformThreadLocalObject::CreateInstance() ./../../third\_party/perfetto/src/tracing/platform.cc:31:53  

#2 0x557eed176ec2 in base::tracing::PerfettoPlatform::GetOrCreateThreadLocalObject() ./../../base/tracing/perfetto\_platform.cc:57:14  

#3 0x557eeced5ca0 in GetOrCreateTracingTLS ./../../third\_party/perfetto/include/perfetto/tracing/internal/tracing\_muxer.h:62:48  

#4 0x557eeced5ca0 in GetOrCreateDataSourceTLS ./../../third\_party/perfetto/include/perfetto/tracing/data\_source.h:602:52  

#5 0x557eeced5ca0 in void perfetto::DataSource<perfetto::perfetto\_track\_event::TrackEvent, perfetto::internal::TrackEventDataSourceTraits>::TraceWithInstances<perfetto::internal::TrackEventDataSource<perfetto::perfetto\_track\_event::TrackEvent, &perfetto::perfetto\_track\_event::internal::kCategoryRegistry>::CategoryTracePointTraits, void perfetto::internal::TrackEventDataSource<perfetto::perfetto\_track\_event::TrackEvent, &perfetto::perfetto\_track\_event::internal::kCategoryRegistry>::TraceForCategoryImpl<unsigned long, perfetto::StaticString, perfetto::Track, perfetto::TraceTimestamp, void, void, std::Cr::function<void (perfetto::EventContext&)>>(unsigned int, unsigned long const&, perfetto::StaticString const&, perfetto::protos::pbzero::perfetto\_pbzero\_enum\_TrackEvent::Type, perfetto::Track const&, perfetto::TraceTimestamp const&, std::Cr::function<void (perfetto::EventContext&)>&&)::'lambda'(perfetto::DataSource<perfetto::perfetto\_track\_event::TrackEvent, perfetto::internal::TrackEventDataSourceTraits>::TraceContext)>(unsigned int, perfetto::StaticString, unsigned long::TracePointData) ./../../third\_party/perfetto/include/perfetto/tracing/data\_source.h:388:20  

#6 0x557eeced50c0 in TraceWithInstances<unsigned long, (lambda at ../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:531:30)> ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:613:7  

#7 0x557eeced50c0 in TraceForCategoryImpl<unsigned long, perfetto::StaticString, perfetto::Track, perfetto::TraceTimestamp, void, void, std::Cr::function<void (perfetto::EventContext &)> > ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:530:5  

#8 0x557eeced50c0 in void perfetto::internal::TrackEventDataSource<perfetto::perfetto\_track\_event::TrackEvent, &perfetto::perfetto\_track\_event::internal::kCategoryRegistry>::TraceForCategory<unsigned long, perfetto::StaticString, std::Cr::function<void (perfetto::EventContext&)>>(unsigned int, unsigned long const&, perfetto::StaticString const&, perfetto::protos::pbzero::perfetto\_pbzero\_enum\_TrackEvent::Type, std::Cr::function<void (perfetto::EventContext&)>&&) ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:312:5  

#9 0x557eeced4cc9 in operator() ./../../base/task/common/task\_annotator.cc:93:3  

#10 0x557eeced4cc9 in void perfetto::internal::TrackEventDataSource<perfetto::perfetto\_track\_event::TrackEvent, &perfetto::perfetto\_track\_event::internal::kCategoryRegistry>::CallIfCategoryEnabled<base::TaskAnnotator::WillQueueTask(perfetto::StaticString, base::PendingTask\*)::$\_0>(unsigned long, base::TaskAnnotator::WillQueueTask(perfetto::StaticString, base::PendingTask\*)::$\_0)::'lambda'(unsigned int)::operator()(unsigned int) const ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:289:43  

#11 0x557eeced15b9 in CallIfEnabled<perfetto::internal::TrackEventDataSource<perfetto::perfetto\_track\_event::TrackEvent, &perfetto::perfetto\_track\_event::internal::kCategoryRegistry>::CategoryTracePointTraits, (lambda at ../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:289:9)> ./../../third\_party/perfetto/include/perfetto/tracing/data\_source.h:351:5  

#12 0x557eeced15b9 in CallIfCategoryEnabled<(lambda at ../../base/task/common/task\_annotator.cc:93:3)> ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:288:5  

#13 0x557eeced15b9 in base::TaskAnnotator::WillQueueTask(perfetto::StaticString, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:93:3  

#14 0x557eecf28285 in base::sequence\_manager::internal::TaskQueueImpl::PostImmediateTaskImpl(base::sequence\_manager::internal::PostedTask, base::sequence\_manager::internal::TaskQueueImpl::CurrentThread) ./../../base/task/sequence\_manager/task\_queue\_impl.cc:443:24  

#15 0x557eecf22fa3 in base::sequence\_manager::internal::TaskQueueImpl::PostTask(base::sequence\_manager::internal::PostedTask) ./../../base/task/sequence\_manager/task\_queue\_impl.cc:374:5  

#16 0x557eecf22d2f in base::sequence\_manager::internal::TaskQueueImpl::GuardedTaskPoster::PostTask(base::sequence\_manager::internal::PostedTask) ./../../base/task/sequence\_manager/task\_queue\_impl.cc:108:11  

#17 0x557eecf23f4f in base::sequence\_manager::internal::TaskQueueImpl::TaskRunner::PostDelayedTask(base::Location const&, base::OnceCallback<void ()>, base::TimeDelta) ./../../base/task/sequence\_manager/task\_queue\_impl.cc:144:24  

#18 0x557ee9703717 in blink::scheduler::BlinkSchedulerSingleThreadTaskRunner::PostDelayedTask(base::Location const&, base::OnceCallback<void ()>, base::TimeDelta) ./../../third\_party/blink/renderer/platform/scheduler/common/blink\_scheduler\_single\_thread\_task\_runner.h:50:20  

#19 0x557eecf8b008 in base::TaskRunner::PostTask(base::Location const&, base::OnceCallback<void ()>) ./../../base/task/task\_runner.cc:47:10  

#20 0x557f054e36f4 in content::RendererThreadTypeHandler::HandleThreadTypeChange(int, base::ThreadType) ./../../content/renderer/renderer\_thread\_type\_handler.cc:45:22  

#21 0x557eed0b0275 in base::internal::SetCurrentThreadTypeForPlatform(base::ThreadType, base::MessagePumpType) ./../../base/threading/platform\_thread\_linux.cc:359:31  

#22 0x557eed09ff2c in base::internal::SetCurrentThreadTypeImpl(base::ThreadType, base::MessagePumpType) ./../../base/threading/platform\_thread\_posix.cc:382:7  

#23 0x557eecff66ea in SetCurrentThreadType ./../../base/threading/platform\_thread.cc:82:3  

#24 0x557eecff66ea in base::PlatformThread::SetCurrentThreadType(base::ThreadType) ./../../base/threading/platform\_thread.cc:57:3  

#25 0x557eed0a011b in base::(anonymous namespace)::ThreadFunc(void\*) ./../../base/threading/platform\_thread\_posix.cc:94:5  

#26 0x7f43b060ab42 in start\_thread ./nptl/pthread\_create.c:442:8

Thread T13 (ServiceWorker t) created by T7 (ThreadPoolSingl) here:  

#0 0x557eda659d2a in pthread\_create *asan\_rtl*:3  

#1 0x557eed09f3b0 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform\_thread\_posix.cc:147:13  

#2 0x557eed001e21 in base::SimpleThread::StartAsync() ./../../base/threading/simple\_thread.cc:54:13  

#3 0x557ee983b7c4 in blink::NonMainThread::CreateThread(blink::ThreadCreationParams const&) ./../../third\_party/blink/renderer/platform/scheduler/worker/non\_main\_thread\_impl.cc:35:11  

#4 0x557efd04eec3 in blink::WorkerBackingThread::WorkerBackingThread(blink::ThreadCreationParams const&) ./../../third\_party/blink/renderer/core/workers/worker\_backing\_thread.cc:59:23  

#5 0x557f03b0fdf2 in make\_unique<blink::WorkerBackingThread, blink::ThreadCreationParams> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:30  

#6 0x557f03b0fdf2 in blink::ServiceWorkerThread::ServiceWorkerThread(std::Cr::unique\_ptr<blink::ServiceWorkerGlobalScopeProxy, std::Cr::default\_delete[blink::ServiceWorkerGlobalScopeProxy](javascript:void(0);)>, std::Cr::unique\_ptr<blink::ServiceWorkerInstalledScriptsManager, std::Cr::default\_delete[blink::ServiceWorkerInstalledScriptsManager](javascript:void(0);)>, mojo::PendingRemote[blink::mojom::blink::CacheStorage](javascript:void(0);), scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);), base::TokenType[blink::ServiceWorkerTokenTypeMarker](javascript:void(0);) const&) ./../../third\_party/blink/renderer/modules/service\_worker/service\_worker\_thread.cc:56:30  

#7 0x557f03b0c76c in make\_unique<blink::ServiceWorkerThread, std::Cr::unique\_ptr<blink::ServiceWorkerGlobalScopeProxy, std::Cr::default\_delete[blink::ServiceWorkerGlobalScopeProxy](javascript:void(0);) >, std::Cr::unique\_ptr<blink::ServiceWorkerInstalledScriptsManager, std::Cr::default\_delete[blink::ServiceWorkerInstalledScriptsManager](javascript:void(0);) >, mojo::PendingRemote[blink::mojom::blink::CacheStorage](javascript:void(0);), scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);) &, base::TokenType[blink::ServiceWorkerTokenTypeMarker](javascript:void(0);) &> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:30  

#8 0x557f03b0c76c in blink::WebEmbeddedWorkerImpl::StartWorkerThread(std::Cr::unique\_ptr<blink::WebEmbeddedWorkerStartData, std::Cr::default\_delete[blink::WebEmbeddedWorkerStartData](javascript:void(0);)>, std::Cr::unique\_ptr<blink::ServiceWorkerInstalledScriptsManager, std::Cr::default\_delete[blink::ServiceWorkerInstalledScriptsManager](javascript:void(0);)>, std::Cr::unique\_ptr<blink::ServiceWorkerContentSettingsProxy, std::Cr::default\_delete[blink::ServiceWorkerContentSettingsProxy](javascript:void(0);)>, mojo::PendingRemote[blink::mojom::blink::CacheStorage](javascript:void(0);), mojo::PendingRemote[blink::mojom::blink::BrowserInterfaceBroker](javascript:void(0);), blink::InterfaceRegistry\*, scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);)) ./../../third\_party/blink/renderer/modules/exported/web\_embedded\_worker\_impl.cc:224:20  

#9 0x557f03b0b7a3 in blink::WebEmbeddedWorkerImpl::StartWorkerContext(std::Cr::unique\_ptr<blink::WebEmbeddedWorkerStartData, std::Cr::default\_delete[blink::WebEmbeddedWorkerStartData](javascript:void(0);)>, std::Cr::unique\_ptr<blink::WebServiceWorkerInstalledScriptsManagerParams, std::Cr::default\_delete[blink::WebServiceWorkerInstalledScriptsManagerParams](javascript:void(0);)>, blink::CrossVariantMojoRemote[blink::mojom::WorkerContentSettingsProxyInterfaceBase](javascript:void(0);), blink::CrossVariantMojoRemote[blink::mojom::CacheStorageInterfaceBase](javascript:void(0);), blink::CrossVariantMojoRemote[blink::mojom::BrowserInterfaceBrokerInterfaceBase](javascript:void(0);), blink::InterfaceRegistry\*, scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);)) ./../../third\_party/blink/renderer/modules/exported/web\_embedded\_worker\_impl.cc:131:3  

#10 0x557f05420382 in content::ServiceWorkerContextClient::StartWorkerContextOnInitiatorThread(std::Cr::unique\_ptr<blink::WebEmbeddedWorker, std::Cr::default\_delete[blink::WebEmbeddedWorker](javascript:void(0);)>, std::Cr::unique\_ptr<blink::WebEmbeddedWorkerStartData, std::Cr::default\_delete[blink::WebEmbeddedWorkerStartData](javascript:void(0);)>, std::Cr::unique\_ptr<blink::WebServiceWorkerInstalledScriptsManagerParams, std::Cr::default\_delete[blink::WebServiceWorkerInstalledScriptsManagerParams](javascript:void(0);)>, mojo::PendingRemote[blink::mojom::WorkerContentSettingsProxy](javascript:void(0);), mojo::PendingRemote[blink::mojom::CacheStorage](javascript:void(0);), mojo::PendingRemote[blink::mojom::BrowserInterfaceBroker](javascript:void(0);)) ./../../content/renderer/service\_worker/service\_worker\_context\_client.cc:195:12  

#11 0x557f05415a84 in content::EmbeddedWorkerInstanceClientImpl::StartWorker(mojo::StructPtr[blink::mojom::EmbeddedWorkerStartParams](javascript:void(0);)) ./../../content/renderer/service\_worker/embedded\_worker\_instance\_client\_impl.cc:135:35  

#12 0x557edeca7c7a in blink::mojom::EmbeddedWorkerInstanceClientStubDispatch::Accept(blink::mojom::EmbeddedWorkerInstanceClient\*, mojo::Message\*) ./gen/third\_party/blink/public/mojom/service\_worker/embedded\_worker.mojom.cc:636:13  

#13 0x557eeda681b9 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1007:54  

#14 0x557eeda85ae0 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#15 0x557eeda6dae8 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:694:20  

#16 0x557eeda93e77 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#17 0x557eeda92207 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:710:7  

#18 0x557eeda85ae0 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#19 0x557eeda5e17f in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:550:49  

#20 0x557eeda5fd4a in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:607:14  

#21 0x557eeda62e50 in Invoke<void (mojo::Connector::\*)(unsigned int), mojo::Connector \*, unsigned int> ./../../base/functional/bind\_internal.h:745:12  

#22 0x557eeda62e50 in MakeItSo<void (mojo::Connector::\*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle> > &, unsigned int> ./../../base/functional/bind\_internal.h:924:12  

#23 0x557eeda62e50 in RunImpl<void (mojo::Connector::\*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle> > &, 0UL> ./../../base/functional/bind\_internal.h:1019:12  

#24 0x557eeda62e50 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) ./../../base/functional/bind\_internal.h:983:12  

#25 0x557edf304bde in Run ./../../base/functional/callback.h:333:12  

#26 0x557edf304bde in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.h:192:14  

#27 0x557edf304df5 in Invoke<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:635:12  

#28 0x557edf304df5 in MakeItSo<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:924:12  

#29 0x557edf304df5 in RunImpl<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind\_internal.h:1019:12  

#30 0x557edf304df5 in base::internal::Invoker<base::internal::BindState<void (\*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase\*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind\_internal.h:983:12  

#31 0x557eedafe929 in Run ./../../base/functional/callback.h:333:12  

#32 0x557eedafe929 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#33 0x557eedaff76c in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind\_internal.h:745:12  

#34 0x557eedaff76c in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind\_internal.h:947:5  

#35 0x557eedaff76c in RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind\_internal.h:1019:12  

#36 0x557eedaff76c in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:970:12  

#37 0x557eeced1ab3 in Run ./../../base/functional/callback.h:152:12  

#38 0x557eeced1ab3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:165:32  

#39 0x557eecf9652c in RunTask<(lambda at ../../base/task/thread\_pool/task\_tracker.cc:650:35)> ./../../base/task/common/task\_annotator.h:87:5  

#40 0x557eecf9652c in RunTaskImpl ./../../base/task/thread\_pool/task\_tracker.cc:649:19  

#41 0x557eecf9652c in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource\*, base::SequenceToken const&) ./../../base/task/thread\_pool/task\_tracker.cc:634:3  

#42 0x557eecf956d6 in RunTaskWithShutdownBehavior ./../../base/task/thread\_pool/task\_tracker.cc:664:7  

#43 0x557eecf956d6 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource\*, base::TaskTraits const&) ./../../base/task/thread\_pool/task\_tracker.cc:491:5  

#44 0x557eecf9494e in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) ./../../base/task/thread\_pool/task\_tracker.cc:406:5  

#45 0x557eecfd0ccf in base::internal::WorkerThread::RunWorker() ./../../base/task/thread\_pool/worker\_thread.cc:480:34  

#46 0x557eecfd0211 in base::internal::WorkerThread::RunSharedWorker() ./../../base/task/thread\_pool/worker\_thread.cc:366:3  

#47 0x557eecfcfb7d in base::internal::WorkerThread::ThreadMain() ./../../base/task/thread\_pool/worker\_thread.cc:339:7  

#48 0x557eed0a01bc in base::(anonymous namespace)::ThreadFunc(void\*) ./../../base/threading/platform\_thread\_posix.cc:102:13  

#49 0x7f43b060ab42 in start\_thread ./nptl/pthread\_create.c:442:8

Thread T7 (ThreadPoolSingl) created by T0 (chrome) here:  

#0 0x557eda659d2a in pthread\_create *asan\_rtl*:3  

#1 0x557eed09f3b0 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadType, base::MessagePumpType) ./../../base/threading/platform\_thread\_posix.cc:147:13  

#2 0x557eecfce91b in base::internal::WorkerThread::Start(scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);), base::WorkerThreadObserver\*) ./../../base/task/thread\_pool/worker\_thread.cc:193:3  

#3 0x557eecfafc4a in CreateTaskRunnerImpl<base::internal::(anonymous namespace)::WorkerThreadDelegate> ./../../base/task/thread\_pool/pooled\_single\_thread\_task\_runner\_manager.cc:674:13  

#4 0x557eecfafc4a in base::internal::PooledSingleThreadTaskRunnerManager::CreateSingleThreadTaskRunner(base::TaskTraits const&, base::SingleThreadTaskRunnerThreadMode) ./../../base/task/thread\_pool/pooled\_single\_thread\_task\_runner\_manager.cc:613:10  

#5 0x557f02a7b972 in content::ExposeRendererInterfacesToBrowser(base::WeakPtr[content::RenderThreadImpl](javascript:void(0);), mojo::BinderMap\*) ./../../content/renderer/browser\_exposed\_renderer\_interfaces.cc:181:7  

#6 0x557f02a5332d in content::RenderThreadImpl::Init() ./../../content/renderer/render\_thread\_impl.cc:616:3  

#7 0x557f02a56a56 in content::RenderThreadImpl::RenderThreadImpl(base::RepeatingCallback<void ()>, std::Cr::unique\_ptr<blink::scheduler::WebThreadScheduler, std::Cr::default\_delete[blink::scheduler::WebThreadScheduler](javascript:void(0);)>) ./../../content/renderer/render\_thread\_impl.cc:560:3  

#8 0x557f05408d2f in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer\_main.cc:282:9  

#9 0x557eea343a87 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:684:14  

#10 0x557eea345cf0 in content::RunOtherNamedProcessTypeMain(std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:769:12  

#11 0x557eea348260 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1122:10  

#12 0x557eea34034e in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:335:36  

#13 0x557eea3409b0 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:363:10  

#14 0x557eda6a4ce6 in ChromeMain ./../../chrome/app/chrome\_main.cc:190:12  

#15 0x7f43b059fd8f in \_\_libc\_start\_call\_main ./csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/kuer/chromium\_version/latest\_asan/chrome+0x1f21f324) (BuildId: 17f067f6abe67b5b)  

Shadow bytes around the buggy address:  

0x62b0000d1180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x62b0000d1200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x62b0000d1280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x62b0000d1300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x62b0000d1380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x62b0000d1400: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd  

0x62b0000d1480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x62b0000d1500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x62b0000d1580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x62b0000d1600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x62b0000d1680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==29460==ADDITIONAL INFO

==29460==Note: Please include this section with the ASan report.  

Task trace:

==29460==END OF ADDITIONAL INFO  

==29460==ABORTING

## Attachments

- [webserver.zip](attachments/webserver.zip) (application/octet-stream, 48.2 KB)

## Timeline

### 0x...@gmail.com (2023-02-07)

Chromium	112.0.5582.0 (Developer Build) (64-bit) 
Revision	96177c3eeb9f5fcfe82739e830b4fa5cce11fccf-refs/heads/main@{#1102098}
OS	Linux

### [Deleted User] (2023-02-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-02-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6389256359706624.

### ma...@google.com (2023-02-10)

Can repro this in M112 on Linux

Sev-High for renderer UAF, but Impact-None because this requires --trace-config-file.

ddiproietto@, could you PTAL?


[Monorail components: Speed>Tracing]

### [Deleted User] (2023-02-12)

[Empty comment from Monorail migration]

### dd...@google.com (2023-02-13)

It looks like we're trying to trace on thread exit, after having freed the perfetto TLS.

Is this related to the SDK migration?

### rs...@google.com (2023-02-13)

[Empty comment from Monorail migration]

### rs...@google.com (2023-02-13)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-02-13)

Yeah this looks due to the SDK migration. We had flipped the build to the SDK for Linux, but have since reverted. Nothing urgent here, but we should address this before the next attempt.

wrt addressing this: Could we observe when the data source TLS is destroyed (e.g. via a destructor) and reset the tls_state_ pointer in the data source [1]? That'd at least prevent the invalid memory access, although it may lead to recreation of the data source TLS (not sure if this is an issue, maybe it's fine?).

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/perfetto/include/perfetto/tracing/data_source.h;drc=8ce391bed5ee336e59ccd87b8869760c30e2aad7;l=624

### kh...@google.com (2023-03-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/45d38165520fa951236fbb79a8bd46f41eb38bdb

commit 45d38165520fa951236fbb79a8bd46f41eb38bdb
Author: Mikhail Khokhlov <khokhlov@google.com>
Date: Mon Mar 20 10:37:14 2023

Destroy TLS slots in reverse order

TLS slots used to be destroyed from last created to first created
when this code was first designed. After the slot reclamation was
introduced in https://crrev.com/423911 the destruction order changed
(albeit the comment in the code still reflected the reverse order).

This CL restores the reverse destruction order by tracking the global
slot sequence number and sorting the destructors by it. This order is
relied upon by the Perfetto tracing system, because it stores the
tracing state in the TLS, and since the destructors of other slots can
emit trace events, so the tracing slot should be destroyed last.

Also fixes the handling of slots that were created during the
destruction phase (now they are destroyed correctly).

Bug: 1413701
Change-Id: I3d5608d78153c6d251001b524e4e6f6eacaa6668
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4299789
Reviewed-by: Gabriel Charette <gab@chromium.org>
Reviewed-by: Alexander Timin <altimin@chromium.org>
Commit-Queue: Mikhail Khokhlov <khokhlov@google.com>
Cr-Commit-Position: refs/heads/main@{#1119244}

[modify] https://crrev.com/45d38165520fa951236fbb79a8bd46f41eb38bdb/base/threading/thread_local_storage.cc
[modify] https://crrev.com/45d38165520fa951236fbb79a8bd46f41eb38bdb/base/threading/thread_local_storage_unittest.cc


### kh...@google.com (2023-03-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-29)

Congratulations, asnine! The VRP Panel had decided to award you $3,000 for this report. The reward amount was decided upon due this issue appears to be specific to and require the --trace-config-file flag, which is a development / testing flag. If you can demonstrate this issue without the reliance on this flag, we would be happy to reassess for a potential change in reward amount. 
Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-06-26)

This issue was migrated from crbug.com/chromium/1413701?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062949)*
