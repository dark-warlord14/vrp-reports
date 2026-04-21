# Security: UAF in DevToolsDataSource::OnLoadComplete

| Field | Value |
|-------|-------|
| **Issue ID** | [40064142](https://issues.chromium.org/issues/40064142) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools, UI>Browser>WebUI |
| **Platforms** | Linux |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2023-04-21 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in DevToolsDataSource::OnLoadComplete

**VERSION**  

Chromium 114.0.5725.0 (Developer Build) (64-bit)  

Revision 2e1e3a8b5f1e13220d98ecfe4800a1b8c117a438-refs/heads/main@{#1133421}  

OS Linux

**REPRODUCTION CASE**

1. unzip the file into the webserver dir and run `python3 -m http.server 8000`:
2. ./chrome --user-data-dir=/tmp/any --disable-popup-blocking --no-sandbox --auto-open-devtools-for-tabs <http://localhost:8000/icr.html> <http://localhost:8000/> <http://localhost:8000/br.html>

PS: Try a little more times to reproduce this issue.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==42612==ERROR: AddressSanitizer: heap-use-after-free on address 0x6030001f5be8 at pc 0x558985f84d07 bp 0x7ffd821b4a70 sp 0x7ffd821b4a68  

READ of size 8 at 0x6030001f5be8 thread T0 (chrome)  

==42612==WARNING: invalid path to external symbolizer!  

==42612==WARNING: Failed to use and restart external symbolizer!  

#0 0x558985f84d06 in erase ./../../buildtools/third\_party/libc++/trunk/include/list:1722:31  

#1 0x558985f84d06 in DevToolsDataSource::OnLoadComplete(std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void\*>, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>>>) ./../../chrome/browser/ui/webui/devtools\_ui\_data\_source.cc:372:21  

#2 0x558985f85f75 in Invoke<void (DevToolsDataSource::\*)(std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void \*>, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > > >), DevToolsDataSource \*, std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void \*>, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > > > > ./../../base/functional/bind\_internal.h:746:12  

#3 0x558985f85f75 in MakeItSo<void (DevToolsDataSource::\*)(std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void \*>, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > > >), std::Cr::tuple<base::internal::UnretainedWrapper<DevToolsDataSource, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void \*> >, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > > > > ./../../base/functional/bind\_internal.h:925:12  

#4 0x558985f85f75 in RunImpl<void (DevToolsDataSource::\*)(std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void \*>, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > > >), std::Cr::tuple<base::internal::UnretainedWrapper<DevToolsDataSource, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void \*> >, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1025:12  

#5 0x558985f85f75 in base::internal::Invoker<base::internal::BindState<void (DevToolsDataSource::\*)(std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void\*>, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>>>), base::internal::UnretainedWrapper<DevToolsDataSource, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void\*>>, void (std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>>>)>::RunOnce(base::internal::BindStateBase\*, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>>>&&) ./../../base/functional/bind\_internal.h:976:12  

#6 0x5589736c2b01 in Run ./../../base/functional/callback.h:152:12  

#7 0x5589736c2b01 in network::(anonymous namespace)::SaveToStringBodyHandler::NotifyConsumerOfCompletion(bool) ./../../services/network/public/cpp/simple\_url\_loader.cc:719:41  

#8 0x5589736c81af in network::(anonymous namespace)::SimpleURLLoaderImpl::FinishWithResult(int) ./../../services/network/public/cpp/simple\_url\_loader.cc:1629:18  

#9 0x5589736c068a in network::(anonymous namespace)::SimpleURLLoaderImpl::OnReceiveResponse(mojo::StructPtr[network::mojom::URLResponseHead](javascript:void(0);), mojo::ScopedHandleBase[mojo::DataPipeConsumerHandle](javascript:void(0);), absl::optional<mojo\_base::BigBuffer>) ./../../services/network/public/cpp/simple\_url\_loader.cc:0:0  

#10 0x5589604c3aa1 in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient\*, mojo::Message\*) ./gen/services/network/public/mojom/url\_loader.mojom.cc:1207:13  

#11 0x55897323bc95 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1011:54  

#12 0x558973259882 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#13 0x558973241688 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:696:20  

#14 0x5589732679fe in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#15 0x558973265da2 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:710:7  

#16 0x558973259882 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#17 0x558973231a57 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:550:49  

#18 0x558973233643 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:607:14  

#19 0x558973236860 in Invoke<void (mojo::Connector::\*)(unsigned int), mojo::Connector \*, unsigned int> ./../../base/functional/bind\_internal.h:746:12  

#20 0x558973236860 in MakeItSo<void (mojo::Connector::\*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind\_internal.h:925:12  

#21 0x558973236860 in RunImpl<void (mojo::Connector::\*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#22 0x558973236860 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) ./../../base/functional/bind\_internal.h:989:12  

#23 0x558963a67ade in Run ./../../base/functional/callback.h:333:12  

#24 0x558963a67ade in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.h:192:14  

#25 0x558963a67cf5 in Invoke<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:636:12  

#26 0x558963a67cf5 in MakeItSo<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:925:12  

#27 0x558963a67cf5 in RunImpl<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#28 0x558963a67cf5 in base::internal::Invoker<base::internal::BindState<void (\*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase\*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind\_internal.h:989:12  

#29 0x5589732cc477 in Run ./../../base/functional/callback.h:333:12  

#30 0x5589732cc477 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#31 0x5589732cd2dc in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);) &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind\_internal.h:746:12  

#32 0x5589732cd2dc in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind\_internal.h:953:5  

#33 0x5589732cd2dc in RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind\_internal.h:1025:12  

#34 0x5589732cd2dc in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#35 0x5589708fc937 in Run ./../../base/functional/callback.h:152:12  

#36 0x5589708fc937 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#37 0x558970969485 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#38 0x558970969485 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#39 0x5589709683a5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#40 0x55897096a4c4 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#41 0x558970ae753a in base::MessagePumpGlib::HandleDispatch() ./../../base/message\_loop/message\_pump\_glib.cc:625:46  

#42 0x558970aea3f2 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:274:43  

#43 0x7f3517c4f17c in g\_main\_context\_dispatch ??:0:0

0x6030001f5be8 is located 8 bytes inside of 32-byte region [0x6030001f5be0,0x6030001f5c00)  

freed by thread T0 (chrome) here:  

#0 0x55895ea4218d in operator delete(void\*) *asan\_rtl*:3  

#1 0x558985f7c70c in \_\_libcpp\_operator\_delete<void \*> ./../../buildtools/third\_party/libc++/trunk/include/new:278:3  

#2 0x558985f7c70c in \_\_do\_deallocate\_handle\_size<> ./../../buildtools/third\_party/libc++/trunk/include/new:302:10  

#3 0x558985f7c70c in \_\_libcpp\_deallocate ./../../buildtools/third\_party/libc++/trunk/include/new:318:14  

#4 0x558985f7c70c in deallocate ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator.h:131:13  

#5 0x558985f7c70c in deallocate ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:288:13  

#6 0x558985f7c70c in clear ./../../buildtools/third\_party/libc++/trunk/include/list:750:13  

#7 0x558985f7c70c in ~\_\_list\_imp ./../../buildtools/third\_party/libc++/trunk/include/list:730:3  

#8 0x558985f7c70c in ~DevToolsDataSource ./../../chrome/browser/ui/webui/devtools\_ui\_data\_source.cc:106:44  

#9 0x558985f7c70c in DevToolsDataSource::~DevToolsDataSource() ./../../chrome/browser/ui/webui/devtools\_ui\_data\_source.cc:106:43  

#10 0x558969b6efea in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#11 0x558969b6efea in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#12 0x558969b6efea in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#13 0x558969b6efea in ~URLDataSourceImpl ./../../content/browser/webui/url\_data\_source\_impl.cc:24:1  

#14 0x558969b6efea in content::URLDataSourceImpl::~URLDataSourceImpl() ./../../content/browser/webui/url\_data\_source\_impl.cc:23:41  

#15 0x558969b693f7 in content::URLDataManager::DeleteDataSource(content::URLDataSourceImpl const\*) ./../../content/browser/webui/url\_data\_manager.cc:90:5  

#16 0x558969b8de91 in Destruct ./../../content/browser/webui/url\_data\_source\_impl.h:37:5  

#17 0x558969b8de91 in Release ./../../base/memory/ref\_counted.h:418:7  

#18 0x558969b8de91 in Release ./../../base/memory/scoped\_refptr.h:382:8  

#19 0x558969b8de91 in ~scoped\_refptr ./../../base/memory/scoped\_refptr.h:280:7  

#20 0x558969b8de91 in ~RetainedRefWrapper ./../../base/functional/bind\_internal.h:311:7  

#21 0x558969b8de91 in ~\_\_tuple\_leaf ./../../buildtools/third\_party/libc++/trunk/include/tuple:293:7  

#22 0x558969b8de91 in ~\_\_tuple\_impl ./../../buildtools/third\_party/libc++/trunk/include/tuple:479:37  

#23 0x558969b8de91 in ~tuple ./../../buildtools/third\_party/libc++/trunk/include/tuple:566:28  

#24 0x558969b8de91 in ~BindState ./../../base/functional/bind\_internal.h:1223:24  

#25 0x558969b8de91 in base::internal::BindState<void (\*)(mojo::StructPtr[network::mojom::URLResponseHead](javascript:void(0);), std::Cr::map<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>, std::Cr::less<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const>, std::Cr::allocator<std::Cr::pair<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>>>> const\*, bool, scoped\_refptr[content::URLDataSourceImpl](javascript:void(0);), mojo::PendingRemote[network::mojom::URLLoaderClient](javascript:void(0);), absl::optional[net::HttpByteRange](javascript:void(0);), base::ElapsedTimer, scoped\_refptr[base::RefCountedMemory](javascript:void(0);)), mojo::StructPtr[network::mojom::URLResponseHead](javascript:void(0);), base::internal::UnretainedWrapper<std::Cr::map<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>, std::Cr::less<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const>, std::Cr::allocator<std::Cr::pair<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>>>> const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, bool, base::internal::RetainedRefWrapper[content::URLDataSourceImpl](javascript:void(0);), mojo::PendingRemote[network::mojom::URLLoaderClient](javascript:void(0);), absl::optional[net::HttpByteRange](javascript:void(0);), base::ElapsedTimer>::Destroy(base::internal::BindStateBase const\*) ./../../base/functional/bind\_internal.h:1226:5  

#26 0x558985f849b6 in Run ./../../base/functional/callback.h:153:3  

#27 0x558985f849b6 in DevToolsDataSource::OnLoadComplete(std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void\*>, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>>>) ./../../chrome/browser/ui/webui/devtools\_ui\_data\_source.cc:369:8  

#28 0x558985f85f75 in Invoke<void (DevToolsDataSource::\*)(std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void \*>, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > > >), DevToolsDataSource \*, std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void \*>, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > > > > ./../../base/functional/bind\_internal.h:746:12  

#29 0x558985f85f75 in MakeItSo<void (DevToolsDataSource::\*)(std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void \*>, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > > >), std::Cr::tuple<base::internal::UnretainedWrapper<DevToolsDataSource, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void \*> >, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > > > > ./../../base/functional/bind\_internal.h:925:12  

#30 0x558985f85f75 in RunImpl<void (DevToolsDataSource::\*)(std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void \*>, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > > >), std::Cr::tuple<base::internal::UnretainedWrapper<DevToolsDataSource, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void \*> >, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1025:12  

#31 0x558985f85f75 in base::internal::Invoker<base::internal::BindState<void (DevToolsDataSource::\*)(std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void\*>, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>>>), base::internal::UnretainedWrapper<DevToolsDataSource, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, std::Cr::\_\_list\_iterator<DevToolsDataSource::PendingRequest, void\*>>, void (std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>>>)>::RunOnce(base::internal::BindStateBase\*, std::Cr::unique\_ptr<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>, std::Cr::default\_delete<std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>>>>&&) ./../../base/functional/bind\_internal.h:976:12  

#32 0x5589736c2b01 in Run ./../../base/functional/callback.h:152:12  

#33 0x5589736c2b01 in network::(anonymous namespace)::SaveToStringBodyHandler::NotifyConsumerOfCompletion(bool) ./../../services/network/public/cpp/simple\_url\_loader.cc:719:41  

#34 0x5589736c81af in network::(anonymous namespace)::SimpleURLLoaderImpl::FinishWithResult(int) ./../../services/network/public/cpp/simple\_url\_loader.cc:1629:18  

#35 0x5589736c068a in network::(anonymous namespace)::SimpleURLLoaderImpl::OnReceiveResponse(mojo::StructPtr[network::mojom::URLResponseHead](javascript:void(0);), mojo::ScopedHandleBase[mojo::DataPipeConsumerHandle](javascript:void(0);), absl::optional<mojo\_base::BigBuffer>) ./../../services/network/public/cpp/simple\_url\_loader.cc:0:0  

#36 0x5589604c3aa1 in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient\*, mojo::Message\*) ./gen/services/network/public/mojom/url\_loader.mojom.cc:1207:13  

#37 0x55897323bc95 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1011:54  

#38 0x558973259882 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#39 0x558973241688 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:696:20  

#40 0x5589732679fe in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#41 0x558973265da2 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:710:7  

#42 0x558973259882 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#43 0x558973231a57 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:550:49  

#44 0x558973233643 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:607:14  

#45 0x558973236860 in Invoke<void (mojo::Connector::\*)(unsigned int), mojo::Connector \*, unsigned int> ./../../base/functional/bind\_internal.h:746:12  

#46 0x558973236860 in MakeItSo<void (mojo::Connector::\*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind\_internal.h:925:12  

#47 0x558973236860 in RunImpl<void (mojo::Connector::\*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#48 0x558973236860 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) ./../../base/functional/bind\_internal.h:989:12  

#49 0x558963a67ade in Run ./../../base/functional/callback.h:333:12  

#50 0x558963a67ade in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.h:192:14  

#51 0x558963a67cf5 in Invoke<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:636:12  

#52 0x558963a67cf5 in MakeItSo<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:925:12  

#53 0x558963a67cf5 in RunImpl<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#54 0x558963a67cf5 in base::internal::Invoker<base::internal::BindState<void (\*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase\*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind\_internal.h:989:12  

#55 0x5589732cc477 in Run ./../../base/functional/callback.h:333:12  

#56 0x5589732cc477 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#57 0x5589732cd2dc in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);) &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind\_internal.h:746:12  

#58 0x5589732cd2dc in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind\_internal.h:953:5  

#59 0x5589732cd2dc in RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind\_internal.h:1025:12  

#60 0x5589732cd2dc in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#61 0x5589708fc937 in Run ./../../base/functional/callback.h:152:12  

#62 0x5589708fc937 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#63 0x558970969485 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#64 0x558970969485 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#65 0x5589709683a5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#66 0x55897096a4c4 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#67 0x558970ae753a in base::MessagePumpGlib::HandleDispatch() ./../../base/message\_loop/message\_pump\_glib.cc:625:46  

#68 0x558970aea3f2 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:274:43

previously allocated by thread T0 (chrome) here:  

#0 0x55895ea4192d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x558985f82ea2 in \_\_libcpp\_operator\_new<unsigned long> ./../../buildtools/third\_party/libc++/trunk/include/new:268:10  

#2 0x558985f82ea2 in \_\_libcpp\_allocate ./../../buildtools/third\_party/libc++/trunk/include/new:294:10  

#3 0x558985f82ea2 in allocate ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator.h:115:38  

#4 0x558985f82ea2 in allocate ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:268:20  

#5 0x558985f82ea2 in \_\_allocate\_node ./../../buildtools/third\_party/libc++/trunk/include/list:1108:28  

#6 0x558985f82ea2 in emplace<> ./../../buildtools/third\_party/libc++/trunk/include/list:1627:29  

#7 0x558985f82ea2 in DevToolsDataSource::StartNetworkRequest(GURL const&, net::NetworkTrafficAnnotationTag const&, int, base::OnceCallback<void (scoped\_refptr[base::RefCountedMemory](javascript:void(0);))>) ./../../chrome/browser/ui/webui/devtools\_ui\_data\_source.cc:323:41  

#8 0x558985f81dd7 in DevToolsDataSource::StartRemoteDataRequest(GURL const&, base::OnceCallback<void (scoped\_refptr[base::RefCountedMemory](javascript:void(0);))>) ./../../chrome/browser/ui/webui/devtools\_ui\_data\_source.cc:270:3  

#9 0x558985f802f0 in DevToolsDataSource::StartDataRequest(GURL const&, base::RepeatingCallback<content::WebContents\* ()> const&, base::OnceCallback<void (scoped\_refptr[base::RefCountedMemory](javascript:void(0);))>) ./../../chrome/browser/ui/webui/devtools\_ui\_data\_source.cc:190:7  

#10 0x558969b8b4f1 in StartURLLoader ./../../content/browser/webui/web\_ui\_url\_loader\_factory.cc:273:21  

#11 0x558969b8b4f1 in content::(anonymous namespace)::WebUIURLLoaderFactory::CreateLoaderAndStart(mojo::PendingReceiver[network::mojom::URLLoader](javascript:void(0);), int, unsigned int, network::ResourceRequest const&, mojo::PendingRemote[network::mojom::URLLoaderClient](javascript:void(0);), net::MutableNetworkTrafficAnnotationTag const&) ./../../content/browser/webui/web\_ui\_url\_loader\_factory.cc:384:5  

#12 0x5589611577a3 in network::mojom::URLLoaderFactoryStubDispatch::Accept(network::mojom::URLLoaderFactory\*, mojo::Message\*) ./gen/services/network/public/mojom/url\_loader\_factory.mojom.cc:307:13  

#13 0x55897323bc95 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1011:54  

#14 0x55897325977c in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:48:24  

#15 0x558973241688 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:696:20  

#16 0x5589732679fe in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#17 0x558973265da2 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:710:7  

#18 0x558973259882 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#19 0x558973231a57 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:550:49  

#20 0x558973233643 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:607:14  

#21 0x558973236860 in Invoke<void (mojo::Connector::\*)(unsigned int), mojo::Connector \*, unsigned int> ./../../base/functional/bind\_internal.h:746:12  

#22 0x558973236860 in MakeItSo<void (mojo::Connector::\*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind\_internal.h:925:12  

#23 0x558973236860 in RunImpl<void (mojo::Connector::\*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#24 0x558973236860 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) ./../../base/functional/bind\_internal.h:989:12  

#25 0x558963a67ade in Run ./../../base/functional/callback.h:333:12  

#26 0x558963a67ade in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.h:192:14  

#27 0x558963a67cf5 in Invoke<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:636:12  

#28 0x558963a67cf5 in MakeItSo<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:925:12  

#29 0x558963a67cf5 in RunImpl<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#30 0x558963a67cf5 in base::internal::Invoker<base::internal::BindState<void (\*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase\*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind\_internal.h:989:12  

#31 0x5589732cc477 in Run ./../../base/functional/callback.h:333:12  

#32 0x5589732cc477 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#33 0x5589732cd2dc in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);) &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind\_internal.h:746:12  

#34 0x5589732cd2dc in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind\_internal.h:953:5  

#35 0x5589732cd2dc in RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind\_internal.h:1025:12  

#36 0x5589732cd2dc in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#37 0x5589708fc937 in Run ./../../base/functional/callback.h:152:12  

#38 0x5589708fc937 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#39 0x558970969485 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#40 0x558970969485 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#41 0x5589709683a5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#42 0x55897096a4c4 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#43 0x558970ae753a in base::MessagePumpGlib::HandleDispatch() ./../../base/message\_loop/message\_pump\_glib.cc:625:46  

#44 0x558970aea3f2 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:274:43  

#45 0x7f3517c4f17c in g\_main\_context\_dispatch ??:0:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/zzz/chromium\_version/latest\_asan/chrome+0x34d0bd06) (BuildId: 9cbf71f8efc6a5dd)  

Shadow bytes around the buggy address:  

0x6030001f5900: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd  

0x6030001f5980: fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa  

0x6030001f5a00: fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd  

0x6030001f5a80: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd  

0x6030001f5b00: fd fa f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa  

=>0x6030001f5b80: fd fd fd fd f7 fa fd fd fd fd f7 fa fd[fd]fd fd  

0x6030001f5c00: f7 fa fd fd fd fa f7 fa fd fd fd fa f7 fa fd fd  

0x6030001f5c80: fd fa f7 fa fd fd fd fa f7 fa fd fd fd fd f7 fa  

0x6030001f5d00: fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd  

0x6030001f5d80: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd  

0x6030001f5e00: fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa  

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

==42612==ADDITIONAL INFO

==42612==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x5589732ccd7e in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple\_watcher.cc:102:13

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to this crash.  

This crash is still exploitable with MiraclePtr.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==42612==END OF ADDITIONAL INFO  

==42612==ABORTING  

[0420/172105.113523:ERROR:nacl\_helper\_linux.cc(355)] NaCl helper process running without a sandbox!  

Most likely you need to configure your SUID sandbox correctly

## Attachments

- deleted (application/octet-stream, 0 B)
- [icr.html](attachments/icr.html) (text/plain, 3.2 KB)
- [testharness.js](attachments/testharness.js) (text/plain, 180.4 KB)
- [helpers.js](attachments/helpers.js) (text/plain, 4.4 KB)
- [testharnessreport.js](attachments/testharnessreport.js) (text/plain, 14.2 KB)
- [br.html](attachments/br.html) (text/plain, 427 B)

## Timeline

### [Deleted User] (2023-04-21)

[Empty comment from Monorail migration]

### za...@google.com (2023-04-21)

Hi dgozman@ can you help investigate this UAF bug? Thanks.

[Monorail components: UI>Browser>WebUI]

### za...@google.com (2023-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-22)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-25)

While this issue does appear to require a compromised renderer, there do not appear any other significant mitigations to knock this down to a medium since this is a UAF in the browser process. Updating as high severity for now unless there is new information that follows. 

### am...@chromium.org (2023-04-26)

POC files from webserver.zip.
Thank you for the report, asnine. In the future, please upload the individual POC files to the report and avoid submitting archives. Thank you! 

### am...@chromium.org (2023-04-26)

This bug wasn't repro'ed. I can attempt to repro later but based on quick analysis, this issue doesn't appear to be recently introduced in 114, but looks like it would have existed for some time. Going to update foundin- accordingly. 
asnine / OP, if you happened to have information that is contrary to this please let me know and I can adjust accordingly. 

### ca...@chromium.org (2023-04-26)

I couldn't reproduce this either. However, we can do a speculative fix based on the stacks provided. This doesn't look like any recent regression to me as well/

On a somewhat tangential subject, please note that based on the stack trace we're performing a remote DevTools resource fetch for a DevTools instance being opened locally. This doesn't look like the intended behavior to me, and I could reproduce this part (the only resource being fetched is https://chrome-devtools-frontend.appspot.com/serve_file/@<commit-hash>/third_party/vscode.web-custom-data/browsers.css-data.json). cc: dsv@ on that, Danil, is this expected?



### ds...@chromium.org (2023-04-27)

[Empty comment from Monorail migration]

### sz...@chromium.org (2023-04-28)

Re https://crbug.com/chromium/1435166#c11: Yes, we recently added MDN documentation for CSS properties (see bug#1401107). The data itself is too large to be bundled with the Chromium binary (similarly to locale files for translations), so we fetch it on-demand from the appspot server.

Note though that we didn't modify the backend for this. We fetch from the "devtools://devtools/remote/...." URL similar to what remote debugging does. So any bug in there predates the MDN or l10n file fetching.

### sz...@chromium.org (2023-04-28)

I looked at the code a bit. I didn't manage to repro with the above page, but I managed to write a unittest that has similar stack traces.

**I think** what happens is that web_ui_url_loader_factory creates a callback that retains the DevToolsDataSource [1]. If we assume that the URLDataManagerBackend goes away while the request is in-flight, then the DevToolsDataSource is only kept alive by callback. So once the DevToolsDataSource::OnLoadComplete method calls the callback, the DevToolsDataSource goes away and the rest of "OnLoadComplete" holds on to an invalid `this`. I'll upload a fix where we first remove the PendingRequest from the list, take ownership of the callback, and then run the callback.

[1]: https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/webui/web_ui_url_loader_factory.cc;l=268-271;drc=15d2e059bf8cb5cd56e9571697fb75f00954642f

=================================================================
==636017==ERROR: AddressSanitizer: heap-use-after-free on address 0x6030002dc828 at pc 0x5609644acd7c bp 0x7ffcf17df0a0 sp 0x7ffcf17df098
READ of size 8 at 0x6030002dc828 thread T0
    #0 0x5609644acd7b in std::Cr::list<DevToolsDataSource::PendingRequest, std::Cr::allocator<DevToolsDataSource::PendingRequest>>::erase(std::Cr::__list_const_iterator<DevToolsDataSource::PendingRequest, void*>) buildtools/third_party/libc++/trunk/include/list:1722:31
    #1 0x5609644aca5a in DevToolsDataSource::OnLoadComplete(std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void*>, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>>>) chrome/browser/ui/webui/devtools_ui_data_source.cc:375:21
    #2 0x5609644adbf5 in Invoke<void (DevToolsDataSource::*)(std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void *>, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> >, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > > >), DevToolsDataSource *, std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void *>, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> >, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > > > > base/functional/bind_internal.h:746:12
    #3 0x5609644adbf5 in MakeItSo<void (DevToolsDataSource::*)(std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void *>, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> >, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > > >), std::Cr::tuple<base::internal::UnretainedWrapper<DevToolsDataSource, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void *> >, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> >, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > > > > base/functional/bind_internal.h:925:12
    #4 0x5609644adbf5 in RunImpl<void (DevToolsDataSource::*)(std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void *>, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> >, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > > >), std::Cr::tuple<base::internal::UnretainedWrapper<DevToolsDataSource, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void *> >, 0UL, 1UL> base/functional/bind_internal.h:1025:12
    #5 0x5609644adbf5 in base::internal::Invoker<base::internal::BindState<void (DevToolsDataSource::*)(std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void*>, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>>>), base::internal::UnretainedWrapper<DevToolsDataSource, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void*>>, void (std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>>>)>::RunOnce(base::internal::BindStateBase*, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>>>&&) base/functional/bind_internal.h:976:12
    #6 0x5609314042cd in base::OnceCallback<void (std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>>>)>::Run(std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>>>) && base/functional/callback.h:152:12
    #7 0x56094ad42f1c in network::(anonymous namespace)::SimpleURLLoaderImpl::FinishWithResult(int) services/network/public/cpp/simple_url_loader.cc:1629:18
    #8 0x56094ad434cd in network::(anonymous namespace)::SimpleURLLoaderImpl::MaybeComplete() services/network/public/cpp/simple_url_loader.cc:1921:3
    #9 0x56094ad39189 in network::(anonymous namespace)::SimpleURLLoaderImpl::OnComplete(network::URLLoaderCompletionStatus const&) services/network/public/cpp/simple_url_loader.cc:1845:3
    #10 0x560935f697d7 in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient*, mojo::Message*) gen/services/network/public/mojom/url_loader.mojom.cc:1294:13
    #11 0x56094a15c376 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1011:54
    #12 0x56094a184fad in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #13 0x56094a162e4b in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:696:20
    #14 0x56094a19657e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1096:42
    #15 0x56094a19443d in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:710:7
    #16 0x56094a184fad in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #17 0x56094a14e5b3 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:550:49
    #18 0x56094a1508d4 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:607:14
    #19 0x56094a1500b6 in OnHandleReadyInternal mojo/public/cpp/bindings/lib/connector.cc:440:3
    #20 0x56094a1500b6 in mojo::Connector::OnWatcherHandleReady(unsigned int) mojo/public/cpp/bindings/lib/connector.cc:411:3
    #21 0x56094a153fa0 in Invoke<void (mojo::Connector::*)(unsigned int), mojo::Connector *, unsigned int> base/functional/bind_internal.h:746:12
    #22 0x56094a153fa0 in MakeItSo<void (mojo::Connector::*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> base/functional/bind_internal.h:925:12
    #23 0x56094a153fa0 in RunImpl<void (mojo::Connector::*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0> > &, 0UL> base/functional/bind_internal.h:1025:12
    #24 0x56094a153fa0 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:989:12
    #25 0x560939fa95e0 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:333:12
    #26 0x560939fa9345 in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:636:12
    #27 0x560939fa9345 in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:925:12
    #28 0x560939fa9345 in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> base/functional/bind_internal.h:1025:12
    #29 0x560939fa9345 in base::internal::Invoker<base::internal::BindState<void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:989:12
    #30 0x560945ad3796 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:333:12
    #31 0x560950727252 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #32 0x56095072819c in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> base/functional/bind_internal.h:746:12
    #33 0x56095072819c in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > base/functional/bind_internal.h:953:5
    #34 0x56095072819c in RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> base/functional/bind_internal.h:1025:12
    #35 0x56095072819c in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:976:12
    #36 0x56094ca182a0 in Run base/functional/callback.h:152:12
    #37 0x56094ca182a0 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:186:34
    #38 0x56094cacd331 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:488:11)> base/task/common/task_annotator.h:89:5
    #39 0x56094cacd331 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:23
    #40 0x56094cacb31e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351:41
    #41 0x56094cacecc4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #42 0x56094cc7f2a8 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:290:55
    #43 0x56094cacfedd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:651:12
    #44 0x56094c9892ae in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #45 0x56094c98b21f in base::RunLoop::RunUntilIdle() base/run_loop.cc:143:3
    #46 0x5609489c126e in base::test::TaskEnvironment::RunUntilIdle() base/test/task_environment.cc:736:51
    #47 0x560949a9a28b in content::BrowserTaskEnvironment::~BrowserTaskEnvironment() content/public/test/browser_task_environment.cc:134:3
    #48 0x56092cf01922 in ~DevToolsUIDataSourceRealURLLoaderTest chrome/browser/ui/webui/devtools_ui_data_source_unittest.cc:365:7
    #49 0x56092cf01922 in DevToolsUIDataSourceRealURLLoaderTest_KillDataSourceWithRemoteRequestInFlight_Test::~DevToolsUIDataSourceRealURLLoaderTest_KillDataSourceWithRemoteRequestInFlight_Test() chrome/browser/ui/webui/devtools_ui_data_source_unittest.cc:383:1
    #50 0x560934c24435 in DeleteSelf_ third_party/googletest/src/googletest/include/gtest/gtest.h:318:24
    #51 0x560934c24435 in HandleExceptionsInMethodIfSupported<testing::Test, void> third_party/googletest/src/googletest/src/gtest.cc
    #52 0x560934c24435 in testing::TestInfo::Run() third_party/googletest/src/googletest/src/gtest.cc:2855:5
    #53 0x560934c263f6 in testing::TestSuite::Run() third_party/googletest/src/googletest/src/gtest.cc:3008:30
    #54 0x560934c56e26 in testing::internal::UnitTestImpl::RunAllTests() third_party/googletest/src/googletest/src/gtest.cc:5866:44
    #55 0x560934c55c7d in testing::UnitTest::Run() third_party/googletest/src/googletest/src/gtest.cc:5440:10
    #56 0x5609489d9bfb in RUN_ALL_TESTS third_party/googletest/src/googletest/include/gtest/gtest.h:2284:73
    #57 0x5609489d9bfb in base::TestSuite::Run() base/test/test_suite.cc:464:16
    #58 0x560949c543ae in content::UnitTestTestSuite::Run() content/public/test/unittest_test_suite.cc:181:23
    #59 0x56094898aac1 in Invoke<int (content::UnitTestTestSuite::*)(), content::UnitTestTestSuite *> base/functional/bind_internal.h:746:12
    #60 0x56094898aac1 in MakeItSo<int (content::UnitTestTestSuite::*)(), std::Cr::tuple<base::internal::UnretainedWrapper<content::UnitTestTestSuite, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0> > > base/functional/bind_internal.h:925:12
    #61 0x56094898aac1 in RunImpl<int (content::UnitTestTestSuite::*)(), std::Cr::tuple<base::internal::UnretainedWrapper<content::UnitTestTestSuite, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1025:12
    #62 0x56094898aac1 in base::internal::Invoker<base::internal::BindState<int (content::UnitTestTestSuite::*)(), base::internal::UnretainedWrapper<content::UnitTestTestSuite, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>>, int ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:976:12
    #63 0x5609489e4c5b in Run base/functional/callback.h:152:12
    #64 0x5609489e4c5b in RunTestSuite base/test/launcher/unit_test_launcher.cc:179:38
    #65 0x5609489e4c5b in base::(anonymous namespace)::LaunchUnitTestsInternal(base::OnceCallback<int ()>, unsigned long, int, unsigned long, bool, base::RepeatingCallback<void ()>, base::OnceCallback<void ()>) base/test/launcher/unit_test_launcher.cc:240:10
    #66 0x5609489e452f in base::LaunchUnitTests(int, char**, base::OnceCallback<int ()>, unsigned long) base/test/launcher/unit_test_launcher.cc:288:10
    #67 0x56094898a252 in main chrome/test/base/run_all_unittests.cc:87:10
    #68 0x7f2454646189 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x6030002dc828 is located 8 bytes inside of 32-byte region [0x6030002dc820,0x6030002dc840)
freed by thread T0 here:
    #0 0x5609287fd19d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x5609644acebf in __libcpp_operator_delete<void *> buildtools/third_party/libc++/trunk/include/new:278:3
    #2 0x5609644acebf in __do_deallocate_handle_size<> buildtools/third_party/libc++/trunk/include/new:302:10
    #3 0x5609644acebf in __libcpp_deallocate buildtools/third_party/libc++/trunk/include/new:318:14
    #4 0x5609644acebf in deallocate buildtools/third_party/libc++/trunk/include/__memory/allocator.h:131:13
    #5 0x5609644acebf in deallocate buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:288:13
    #6 0x5609644acebf in std::Cr::__list_imp<DevToolsDataSource::PendingRequest, std::Cr::allocator<DevToolsDataSource::PendingRequest>>::clear() buildtools/third_party/libc++/trunk/include/list:750:13
    #7 0x5609644a53f6 in ~__list_imp buildtools/third_party/libc++/trunk/include/list:730:3
    #8 0x5609644a53f6 in DevToolsDataSource::~DevToolsDataSource() chrome/browser/ui/webui/devtools_ui_data_source.cc:108:1
    #9 0x5609644a550d in DevToolsDataSource::~DevToolsDataSource() chrome/browser/ui/webui/devtools_ui_data_source.cc:106:43
    #10 0x56092cf05689 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:65:5
    #11 0x56092cf05689 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:297:7
    #12 0x56092cf05689 in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:263:75
    #13 0x56092cf05689 in ~OwnedWrapper base/functional/bind_internal.h:330:7
    #14 0x56092cf05689 in ~__tuple_leaf buildtools/third_party/libc++/trunk/include/tuple:293:7
    #15 0x56092cf05689 in ~tuple buildtools/third_party/libc++/trunk/include/tuple:566:28
    #16 0x56092cf05689 in ~BindState base/functional/bind_internal.h:1223:24
    #17 0x56092cf05689 in base::internal::BindState<DevToolsUIDataSourceRealURLLoaderTest_KillDataSourceWithRemoteRequestInFlight_Test::TestBody()::$_0, base::internal::OwnedWrapper<DevToolsDataSource, std::Cr::default_delete<DevToolsDataSource>>>::Destroy(base::internal::BindStateBase const*) base/functional/bind_internal.h:1226:5
    #18 0x56092cf040b6 in base::OnceCallback<void (scoped_refptr<base::RefCountedMemory>)>::Run(scoped_refptr<base::RefCountedMemory>) && base/functional/callback.h:153:3
    #19 0x5609644ac99c in DevToolsDataSource::OnLoadComplete(std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void*>, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>>>) chrome/browser/ui/webui/devtools_ui_data_source.cc:371:8
    #20 0x5609644adbf5 in Invoke<void (DevToolsDataSource::*)(std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void *>, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> >, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > > >), DevToolsDataSource *, std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void *>, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> >, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > > > > base/functional/bind_internal.h:746:12
    #21 0x5609644adbf5 in MakeItSo<void (DevToolsDataSource::*)(std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void *>, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> >, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > > >), std::Cr::tuple<base::internal::UnretainedWrapper<DevToolsDataSource, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void *> >, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> >, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > > > > base/functional/bind_internal.h:925:12
    #22 0x5609644adbf5 in RunImpl<void (DevToolsDataSource::*)(std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void *>, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> >, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > > >), std::Cr::tuple<base::internal::UnretainedWrapper<DevToolsDataSource, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void *> >, 0UL, 1UL> base/functional/bind_internal.h:1025:12
    #23 0x5609644adbf5 in base::internal::Invoker<base::internal::BindState<void (DevToolsDataSource::*)(std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void*>, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>>>), base::internal::UnretainedWrapper<DevToolsDataSource, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>, std::Cr::__list_iterator<DevToolsDataSource::PendingRequest, void*>>, void (std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>>>)>::RunOnce(base::internal::BindStateBase*, std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>>>&&) base/functional/bind_internal.h:976:12
    #24 0x5609314042cd in base::OnceCallback<void (std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>>>)>::Run(std::Cr::unique_ptr<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>, std::Cr::default_delete<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>>>>) && base/functional/callback.h:152:12
    #25 0x56094ad42f1c in network::(anonymous namespace)::SimpleURLLoaderImpl::FinishWithResult(int) services/network/public/cpp/simple_url_loader.cc:1629:18
    #26 0x56094ad434cd in network::(anonymous namespace)::SimpleURLLoaderImpl::MaybeComplete() services/network/public/cpp/simple_url_loader.cc:1921:3
    #27 0x56094ad39189 in network::(anonymous namespace)::SimpleURLLoaderImpl::OnComplete(network::URLLoaderCompletionStatus const&) services/network/public/cpp/simple_url_loader.cc:1845:3
    #28 0x560935f697d7 in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient*, mojo::Message*) gen/services/network/public/mojom/url_loader.mojom.cc:1294:13
    #29 0x56094a15c376 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1011:54
    #30 0x56094a184fad in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #31 0x56094a162e4b in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:696:20
    #32 0x56094a19657e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1096:42
    #33 0x56094a19443d in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:710:7
    #34 0x56094a184fad in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #35 0x56094a14e5b3 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:550:49
    #36 0x56094a1508d4 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:607:14
    #37 0x56094a1500b6 in OnHandleReadyInternal mojo/public/cpp/bindings/lib/connector.cc:440:3
    #38 0x56094a1500b6 in mojo::Connector::OnWatcherHandleReady(unsigned int) mojo/public/cpp/bindings/lib/connector.cc:411:3
    #39 0x56094a153fa0 in Invoke<void (mojo::Connector::*)(unsigned int), mojo::Connector *, unsigned int> base/functional/bind_internal.h:746:12
    #40 0x56094a153fa0 in MakeItSo<void (mojo::Connector::*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> base/functional/bind_internal.h:925:12
    #41 0x56094a153fa0 in RunImpl<void (mojo::Connector::*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0> > &, 0UL> base/functional/bind_internal.h:1025:12
    #42 0x56094a153fa0 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:989:12
    #43 0x560939fa95e0 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:333:12
    #44 0x560939fa9345 in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:636:12
    #45 0x560939fa9345 in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:925:12
    #46 0x560939fa9345 in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> base/functional/bind_internal.h:1025:12
    #47 0x560939fa9345 in base::internal::Invoker<base::internal::BindState<void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:989:12
    #48 0x560945ad3796 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:333:12
    #49 0x560950727252 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #50 0x56095072819c in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> base/functional/bind_internal.h:746:12
    #51 0x56095072819c in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > base/functional/bind_internal.h:953:5
    #52 0x56095072819c in RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> base/functional/bind_internal.h:1025:12
    #53 0x56095072819c in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:976:12
    #54 0x56094ca182a0 in Run base/functional/callback.h:152:12
    #55 0x56094ca182a0 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:186:34
    #56 0x56094cacd331 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:488:11)> base/task/common/task_annotator.h:89:5
    #57 0x56094cacd331 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:23

previously allocated by thread T0 here:
    #0 0x5609287fc93d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x5609644ab49d in __libcpp_operator_new<unsigned long> buildtools/third_party/libc++/trunk/include/new:268:10
    #2 0x5609644ab49d in __libcpp_allocate buildtools/third_party/libc++/trunk/include/new:294:10
    #3 0x5609644ab49d in allocate buildtools/third_party/libc++/trunk/include/__memory/allocator.h:115:38
    #4 0x5609644ab49d in allocate buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:268:20
    #5 0x5609644ab49d in __allocate_node buildtools/third_party/libc++/trunk/include/list:1108:28
    #6 0x5609644ab49d in emplace<> buildtools/third_party/libc++/trunk/include/list:1627:29
    #7 0x5609644ab49d in DevToolsDataSource::StartNetworkRequest(GURL const&, net::NetworkTrafficAnnotationTag const&, int, base::OnceCallback<void (scoped_refptr<base::RefCountedMemory>)>) chrome/browser/ui/webui/devtools_ui_data_source.cc:325:41
    #8 0x5609644aa037 in DevToolsDataSource::StartRemoteDataRequest(GURL const&, base::OnceCallback<void (scoped_refptr<base::RefCountedMemory>)>) chrome/browser/ui/webui/devtools_ui_data_source.cc:272:3
    #9 0x5609644a8a84 in DevToolsDataSource::StartDataRequest(GURL const&, base::RepeatingCallback<content::WebContents* ()> const&, base::OnceCallback<void (scoped_refptr<base::RefCountedMemory>)>) chrome/browser/ui/webui/devtools_ui_data_source.cc:192:7
    #10 0x56092ceffe52 in DevToolsUIDataSourceRealURLLoaderTest_KillDataSourceWithRemoteRequestInFlight_Test::TestBody() chrome/browser/ui/webui/devtools_ui_data_source_unittest.cc:398:16
    #11 0x560934c21563 in testing::Test::Run() third_party/googletest/src/googletest/src/gtest.cc:2670:5
    #12 0x560934c2431b in testing::TestInfo::Run() third_party/googletest/src/googletest/src/gtest.cc:2849:11
    #13 0x560934c263f6 in testing::TestSuite::Run() third_party/googletest/src/googletest/src/gtest.cc:3008:30
    #14 0x560934c56e26 in testing::internal::UnitTestImpl::RunAllTests() third_party/googletest/src/googletest/src/gtest.cc:5866:44
    #15 0x560934c55c7d in testing::UnitTest::Run() third_party/googletest/src/googletest/src/gtest.cc:5440:10
    #16 0x5609489d9bfb in RUN_ALL_TESTS third_party/googletest/src/googletest/include/gtest/gtest.h:2284:73
    #17 0x5609489d9bfb in base::TestSuite::Run() base/test/test_suite.cc:464:16
    #18 0x560949c543ae in content::UnitTestTestSuite::Run() content/public/test/unittest_test_suite.cc:181:23
    #19 0x56094898aac1 in Invoke<int (content::UnitTestTestSuite::*)(), content::UnitTestTestSuite *> base/functional/bind_internal.h:746:12
    #20 0x56094898aac1 in MakeItSo<int (content::UnitTestTestSuite::*)(), std::Cr::tuple<base::internal::UnretainedWrapper<content::UnitTestTestSuite, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0> > > base/functional/bind_internal.h:925:12
    #21 0x56094898aac1 in RunImpl<int (content::UnitTestTestSuite::*)(), std::Cr::tuple<base::internal::UnretainedWrapper<content::UnitTestTestSuite, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0> >, 0UL> base/functional/bind_internal.h:1025:12
    #22 0x56094898aac1 in base::internal::Invoker<base::internal::BindState<int (content::UnitTestTestSuite::*)(), base::internal::UnretainedWrapper<content::UnitTestTestSuite, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>>, int ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:976:12
    #23 0x5609489e4c5b in Run base/functional/callback.h:152:12
    #24 0x5609489e4c5b in RunTestSuite base/test/launcher/unit_test_launcher.cc:179:38
    #25 0x5609489e4c5b in base::(anonymous namespace)::LaunchUnitTestsInternal(base::OnceCallback<int ()>, unsigned long, int, unsigned long, bool, base::RepeatingCallback<void ()>, base::OnceCallback<void ()>) base/test/launcher/unit_test_launcher.cc:240:10
    #26 0x5609489e452f in base::LaunchUnitTests(int, char**, base::OnceCallback<int ()>, unsigned long) base/test/launcher/unit_test_launcher.cc:288:10
    #27 0x56094898a252 in main chrome/test/base/run_all_unittests.cc:87:10
    #28 0x7f2454646189 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/list:1722:31 in std::Cr::list<DevToolsDataSource::PendingRequest, std::Cr::allocator<DevToolsDataSource::PendingRequest>>::erase(std::Cr::__list_const_iterator<DevToolsDataSource::PendingRequest, void*>)
Shadow bytes around the buggy address:
  0x6030002dc580: 00 00 00 fa fa fa fd fd fd fd fa fa 00 00 00 00
  0x6030002dc600: fa fa fd fd fd fd fa fa fd fd fd fa fa fa fd fd
  0x6030002dc680: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa
  0x6030002dc700: fd fd fd fd fa fa fd fd fd fa fa fa fd fd fd fa
  0x6030002dc780: fa fa fd fd fd fa fa fa fd fd fd fd fa fa 00 00
=>0x6030002dc800: 00 00 fa fa fd[fd]fd fd fa fa 00 00 00 fa fa fa
  0x6030002dc880: fd fd fd fd fa fa fd fd fd fd fa fa 00 00 00 00
  0x6030002dc900: fa fa 00 00 00 00 fa fa 00 00 00 fa fa fa fd fd
  0x6030002dc980: fd fa fa fa fd fd fd fa fa fa fd fd fd fd fa fa
  0x6030002dca00: 00 00 00 00 fa fa fd fd fd fd fa fa fd fd fd fa
  0x6030002dca80: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd
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

==636017==ADDITIONAL INFO

==636017==Note: Please include this section with the ASan report.
Task trace:
    #0 0x560950727af3 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:102:13
    #1 0x56094a64d7fd in net::HttpStreamFactory::Job::RunLoop(int) net/http/http_stream_factory_job.cc:634:11
    #2 0x56094a879587 in net::TransportClientSocketPool::InvokeUserCallbackLater(net::ClientSocketHandle*, base::OnceCallback<void (int)>, int, net::SocketTag const&) net/socket/transport_client_socket_pool.cc:1410:7
    #3 0x560946cc63b5 in net::MockHostResolverBase::Resolve(net::MockHostResolverBase::RequestImpl*) net/dns/mock_host_resolver.cc:955:9


==636017==END OF ADDITIONAL INFO
==636017==ABORTING

### sz...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

[Monorail components: Platform>DevTools]

### gi...@appspot.gserviceaccount.com (2023-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d6272b794cbbb146303c3acb48713244a92cce48

commit d6272b794cbbb146303c3acb48713244a92cce48
Author: Simon Zünd <szuend@chromium.org>
Date: Tue May 02 06:05:35 2023

[devtools] Delete PendingRequest first in DevToolsDataSource

The way URLDataSources are used in Chromium, it can happen that the
"content::URLDataSource::GotDataCallback" closure is the last shared
owner of the data source itself. This means that the URLDataSource
is deleted after the callback is done running.

This CL fixes an invalid access to DevToolsDataSource, where we
access `this` in the OnLoadComplete method after we call the
GotDataCallback.

R=dsv@chromium.org

Fixed: 1435166
Change-Id: I32e4a717ca27bc011449c8f8efeaffe70aaa8898
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4487280
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Simon Zünd <szuend@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1138173}

[modify] https://crrev.com/d6272b794cbbb146303c3acb48713244a92cce48/chrome/browser/ui/webui/devtools_ui_data_source_unittest.cc
[modify] https://crrev.com/d6272b794cbbb146303c3acb48713244a92cce48/chrome/browser/ui/webui/devtools_ui_data_source.cc


### sz...@chromium.org (2023-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-02)

hi szuend@ thanks for landing a security fix for this issue. In the future, when resolving a security bug, please just go ahead mark as fixed with out manually requesting a merge (as per security merge triage guidelines: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/merge_request.md#security-merge-triage). 
This allows our sheriffbot to add the appropriate merge request/review labels based on security severity and impact and put the issue in the security merge review queue. 

That all being said, it looks like you've specifically looking to merge this fix to M114. This looks like a fairly trivial fix, is there some compatibility or other potential risk with backmerging this fix beyond 114? 
This is a high severity security issue, this should be considered for backmerged to M113, which was just promoted to Stable today, and M112 which is now Extended Stable. 

M114 is now beta, so I'm going to let this fix get a bit more bake time before approving for M114. 


### sz...@chromium.org (2023-05-03)

I apologize, I wasn't aware that security issues handle back-merges automatically.

No concerns with merging the fix further back, no risks I'm aware of. I also verified with the latest Canary that everything works as expected.

### [Deleted User] (2023-05-03)

Merge review required: M114 is already shipping to beta.

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

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sz...@chromium.org (2023-05-03)

1. High severity security fix.
2. https://crrev.com/c/4487280
3. Yes
4. No

### am...@chromium.org (2023-05-05)

No worries at all, szuend@ -- thanks for confirming there are no concerns with a backmerge here. 

114 merge approved - please merge this fix to branch 5735
113 merge approved - please merge this fix to branch 5672 
112 merge approved - please merge this fix to branch 5615

Please complete all merges at your earliest convenience -- thank you! 

### gi...@appspot.gserviceaccount.com (2023-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aa887211b1dd295422c36d95f862e55a76fc2346

commit aa887211b1dd295422c36d95f862e55a76fc2346
Author: Simon Zünd <szuend@chromium.org>
Date: Fri May 05 06:36:47 2023

[devtools] Delete PendingRequest first in DevToolsDataSource

The way URLDataSources are used in Chromium, it can happen that the
"content::URLDataSource::GotDataCallback" closure is the last shared
owner of the data source itself. This means that the URLDataSource
is deleted after the callback is done running.

This CL fixes an invalid access to DevToolsDataSource, where we
access `this` in the OnLoadComplete method after we call the
GotDataCallback.

R=dsv@chromium.org

(cherry picked from commit d6272b794cbbb146303c3acb48713244a92cce48)

Fixed: 1435166
Change-Id: I32e4a717ca27bc011449c8f8efeaffe70aaa8898
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4487280
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Simon Zünd <szuend@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1138173}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4507693
Cr-Commit-Position: refs/branch-heads/5672@{#1101}
Cr-Branched-From: 5f2a72468eda1eb945b3b5a2298b5d1cd678521e-refs/heads/main@{#1121455}

[modify] https://crrev.com/aa887211b1dd295422c36d95f862e55a76fc2346/chrome/browser/ui/webui/devtools_ui_data_source_unittest.cc
[modify] https://crrev.com/aa887211b1dd295422c36d95f862e55a76fc2346/chrome/browser/ui/webui/devtools_ui_data_source.cc


### gi...@appspot.gserviceaccount.com (2023-05-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0033e41efa25c0a8f78c564f3ec24e80d95612e5

commit 0033e41efa25c0a8f78c564f3ec24e80d95612e5
Author: Simon Zünd <szuend@chromium.org>
Date: Mon May 08 05:16:35 2023

[devtools] Delete PendingRequest first in DevToolsDataSource

The way URLDataSources are used in Chromium, it can happen that the
"content::URLDataSource::GotDataCallback" closure is the last shared
owner of the data source itself. This means that the URLDataSource
is deleted after the callback is done running.

This CL fixes an invalid access to DevToolsDataSource, where we
access `this` in the OnLoadComplete method after we call the
GotDataCallback.

R=dsv@chromium.org

(cherry picked from commit d6272b794cbbb146303c3acb48713244a92cce48)

Fixed: 1435166
Change-Id: I32e4a717ca27bc011449c8f8efeaffe70aaa8898
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4487280
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Simon Zünd <szuend@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1138173}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4507143
Cr-Commit-Position: refs/branch-heads/5615@{#1406}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/0033e41efa25c0a8f78c564f3ec24e80d95612e5/chrome/browser/ui/webui/devtools_ui_data_source_unittest.cc
[modify] https://crrev.com/0033e41efa25c0a8f78c564f3ec24e80d95612e5/chrome/browser/ui/webui/devtools_ui_data_source.cc


### gi...@appspot.gserviceaccount.com (2023-05-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8d9cbf2f96417405f552f0dc2b083d1fd0b099da

commit 8d9cbf2f96417405f552f0dc2b083d1fd0b099da
Author: Simon Zünd <szuend@chromium.org>
Date: Mon May 08 05:34:29 2023

[devtools] Delete PendingRequest first in DevToolsDataSource

The way URLDataSources are used in Chromium, it can happen that the
"content::URLDataSource::GotDataCallback" closure is the last shared
owner of the data source itself. This means that the URLDataSource
is deleted after the callback is done running.

This CL fixes an invalid access to DevToolsDataSource, where we
access `this` in the OnLoadComplete method after we call the
GotDataCallback.

R=dsv@chromium.org

(cherry picked from commit d6272b794cbbb146303c3acb48713244a92cce48)

Fixed: 1435166
Change-Id: I32e4a717ca27bc011449c8f8efeaffe70aaa8898
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4487280
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Simon Zünd <szuend@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1138173}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4506406
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5735@{#365}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/8d9cbf2f96417405f552f0dc2b083d1fd0b099da/chrome/browser/ui/webui/devtools_ui_data_source_unittest.cc
[modify] https://crrev.com/8d9cbf2f96417405f552f0dc2b083d1fd0b099da/chrome/browser/ui/webui/devtools_ui_data_source.cc


### am...@google.com (2023-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-12)

Congratulations, asnine! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-05-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-16)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1435166?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, UI>Browser>WebUI]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064142)*
