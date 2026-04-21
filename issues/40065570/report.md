# Security: UAF in gpu::ClientSharedImageInterface::DestroySharedImage(browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40065570](https://issues.chromium.org/issues/40065570) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Services>Viz |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2023-06-09 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in gpu::ClientSharedImageInterface::DestroySharedImage in browser process.

**VERSION**  

Chromium 116.0.5822.0 (Developer Build) (64-bit)  

Revision 158f730d8773af87ef2013367616bd68ea9d258c-refs/heads/main@{#1155365}  

OS Linux

**REPRODUCTION CASE**

1. put the attachments into the extension\_path.
2. run the command:  
   
   ./chrome --user-data-dir=/tmp --enable-features=SharedBitmapToSharedImage --load-extension="extension\_path"

I reproduced this issue with the asan build:asan-linux-release-1155365.zip

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: [ browser] [2097487:2097487:0609/151936.023240:ERROR:chrome\_browser\_cloud\_management\_controller.cc(162)] Cloud management controller initialization aborted as CBCM is not enabled. [2097487:2097487:0609/151936.447153:ERROR:object\_proxy.cc(590)] Failed to call method: org.freedesktop.portal.Settings.Read: object\_path= /org/freedesktop/portal/desktop: org.freedesktop.portal.Error.NotFound: Requested setting not found [2097549:7:0609/151936.814512:ERROR:command\_buffer\_proxy\_impl.cc(128)] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer. [2097487:2097487:0609/151936.997652:ERROR:gpu\_process\_host.cc(956)] GPU process exited unexpectedly: exit\_code=15

==2097487==ERROR: AddressSanitizer: heap-use-after-free on address 0x51b000181b60 at pc 0x55839393beef bp 0x7fff1703d4d0 sp 0x7fff1703d4c8  

READ of size 1 at 0x51b000181b60 thread T0 (chrome)  

==2097487==WARNING: invalid path to external symbolizer!  

==2097487==WARNING: Failed to use and restart external symbolizer!  

#0 0x55839393beee in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long) *asan\_rtl*:17  

#1 0x55839393ba49 in base::internal::(anonymous namespace)::SafelyUnwrapForDereference(unsigned long) *asan\_rtl*:5  

#2 0x558385ff6a8d in SafelyUnwrapPtrForDereference[gpu::SharedImageInterfaceProxy](javascript:void(0);) ./../../base/allocator/partition\_allocator/pointers/raw\_ptr\_hookable\_impl.h:75:7  

#3 0x558385ff6a8d in GetForDereference ./../../base/allocator/partition\_allocator/pointers/raw\_ptr.h:1038:12  

#4 0x558385ff6a8d in operator-> ./../../base/allocator/partition\_allocator/pointers/raw\_ptr.h:806:12  

#5 0x558385ff6a8d in gpu::ClientSharedImageInterface::DestroySharedImage(gpu::SyncToken const&, gpu::Mailbox const&) ./../../gpu/ipc/client/client\_shared\_image\_interface.cc:178:3  

#6 0x558398a53a22 in cc::(anonymous namespace)::BitmapSoftwareBacking::~BitmapSoftwareBacking() ./../../cc/raster/bitmap\_raster\_buffer\_provider.cc:58:45  

#7 0x558398a53bbd in cc::(anonymous namespace)::BitmapSoftwareBacking::~BitmapSoftwareBacking() ./../../cc/raster/bitmap\_raster\_buffer\_provider.cc:56:37  

#8 0x5583988376fe in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#9 0x5583988376fe in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#10 0x5583988376fe in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#11 0x5583988376fe in ~PoolResource ./../../cc/resources/resource\_pool.cc:639:43  

#12 0x5583988376fe in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#13 0x5583988376fe in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#14 0x5583988376fe in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#15 0x5583988376fe in cc::ResourcePool::DeleteResource(std::\_\_Cr::unique\_ptr<cc::ResourcePool::PoolResource, std::\_\_Cr::default\_delete[cc::ResourcePool::PoolResource](javascript:void(0);)>) ./../../cc/resources/resource\_pool.cc:496:1  

#16 0x55839883877c in cc::ResourcePool::InvalidateResources() ./../../cc/resources/resource\_pool.cc:368:5  

#17 0x5583989213d0 in cc::LayerTreeHostImpl::CleanUpTileManagerResources() ./../../cc/trees/layer\_tree\_host\_impl.cc:3805:19  

#18 0x55839893599c in cc::LayerTreeHostImpl::ReleaseLayerTreeFrameSink() ./../../cc/trees/layer\_tree\_host\_impl.cc:3836:3  

#19 0x558398936fda in cc::LayerTreeHostImpl::InitializeFrameSink(cc::LayerTreeFrameSink\*) ./../../cc/trees/layer\_tree\_host\_impl.cc:3910:3  

#20 0x558398bc332e in cc::SingleThreadProxy::SetLayerTreeFrameSink(cc::LayerTreeFrameSink\*) ./../../cc/trees/single\_thread\_proxy.cc:164:27  

#21 0x55839889db42 in cc::LayerTreeHost::SetLayerTreeFrameSink(std::\_\_Cr::unique\_ptr<cc::LayerTreeFrameSink, std::\_\_Cr::default\_delete[cc::LayerTreeFrameSink](javascript:void(0);)>) ./../../cc/trees/layer\_tree\_host.cc:523:11  

#22 0x55839a8c1326 in ui::Compositor::SetLayerTreeFrameSink(std::\_\_Cr::unique\_ptr<cc::LayerTreeFrameSink, std::\_\_Cr::default\_delete[cc::LayerTreeFrameSink](javascript:void(0);)>, mojo::AssociatedRemote[viz::mojom::DisplayPrivate](javascript:void(0);)) ./../../ui/compositor/compositor.cc:339:10  

#23 0x55838cca4af9 in content::VizProcessTransportFactory::OnEstablishedGpuChannel(base::WeakPtr[ui::Compositor](javascript:void(0);), scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);)) ./../../content/browser/compositor/viz\_process\_transport\_factory.cc:478:15  

#24 0x55838cca95e8 in void base::internal::FunctorTraits<void (content::VizProcessTransportFactory::\*)(base::WeakPtr[ui::Compositor](javascript:void(0);), scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);)), void>::Invoke<void (content::VizProcessTransportFactory::\*)(base::WeakPtr[ui::Compositor](javascript:void(0);), scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);)), base::WeakPtr[content::VizProcessTransportFactory](javascript:void(0);) const&, base::WeakPtr[ui::Compositor](javascript:void(0);), scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);)>(void (content::VizProcessTransportFactory::\*)(base::WeakPtr[ui::Compositor](javascript:void(0);), scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);)), base::WeakPtr[content::VizProcessTransportFactory](javascript:void(0);) const&, base::WeakPtr[ui::Compositor](javascript:void(0);)&&, scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);)&&) ./../../base/functional/bind\_internal.h:746:12  

#25 0x55838cca930f in MakeItSo<void (content::VizProcessTransportFactory::\*)(base::WeakPtr[ui::Compositor](javascript:void(0);), scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);)), std::\_\_Cr::tuple<base::WeakPtr[content::VizProcessTransportFactory](javascript:void(0);), base::WeakPtr[ui::Compositor](javascript:void(0);) >, scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);) > ./../../base/functional/bind\_internal.h:953:5  

#26 0x55838cca930f in RunImpl<void (content::VizProcessTransportFactory::\*)(base::WeakPtr[ui::Compositor](javascript:void(0);), scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);)), std::\_\_Cr::tuple<base::WeakPtr[content::VizProcessTransportFactory](javascript:void(0);), base::WeakPtr[ui::Compositor](javascript:void(0);) >, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1025:12  

#27 0x55838cca930f in base::internal::Invoker<base::internal::BindState<void (content::VizProcessTransportFactory::\*)(base::WeakPtr[ui::Compositor](javascript:void(0);), scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);)), base::WeakPtr[content::VizProcessTransportFactory](javascript:void(0);), base::WeakPtr[ui::Compositor](javascript:void(0);)>, void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>::RunOnce(base::internal::BindStateBase\*, scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);)&&) ./../../base/functional/bind\_internal.h:976:12  

#28 0x55838b42b7f4 in Run ./../../base/functional/callback.h:152:12  

#29 0x55838b42b7f4 in content::BrowserGpuChannelHostFactory::EstablishRequest::RunCallbacksOnMain() ./../../content/browser/gpu/browser\_gpu\_channel\_host\_factory.cc:238:25  

#30 0x55838b42b2e5 in FinishAndRunCallbacksOnMain ./../../content/browser/gpu/browser\_gpu\_channel\_host\_factory.cc:222:3  

#31 0x55838b42b2e5 in Finish ./../../content/browser/gpu/browser\_gpu\_channel\_host\_factory.cc:216:3  

#32 0x55838b42b2e5 in content::BrowserGpuChannelHostFactory::EstablishRequest::OnEstablished(mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&, viz::GpuHostImpl::EstablishChannelStatus) ./../../content/browser/gpu/browser\_gpu\_channel\_host\_factory.cc:211:3  

#33 0x55838b42f18e in Invoke<void (content::BrowserGpuChannelHostFactory::EstablishRequest::\*)(mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus), scoped\_refptr[content::BrowserGpuChannelHostFactory::EstablishRequest](javascript:void(0);), mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus> ./../../base/functional/bind\_internal.h:746:12  

#34 0x55838b42f18e in MakeItSo<void (content::BrowserGpuChannelHostFactory::EstablishRequest::\*)(mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus), std::\_\_Cr::tuple<scoped\_refptr[content::BrowserGpuChannelHostFactory::EstablishRequest](javascript:void(0);) >, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus> ./../../base/functional/bind\_internal.h:925:12  

#35 0x55838b42f18e in RunImpl<void (content::BrowserGpuChannelHostFactory::EstablishRequest::\*)(mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus), std::\_\_Cr::tuple<scoped\_refptr[content::BrowserGpuChannelHostFactory::EstablishRequest](javascript:void(0);) >, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#36 0x55838b42f18e in base::internal::Invoker<base::internal::BindState<void (content::BrowserGpuChannelHostFactory::EstablishRequest::\*)(mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&, viz::GpuHostImpl::EstablishChannelStatus), scoped\_refptr[content::BrowserGpuChannelHostFactory::EstablishRequest](javascript:void(0);)>, void (mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&, viz::GpuHostImpl::EstablishChannelStatus)>::RunOnce(base::internal::BindStateBase\*, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)&&, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&, viz::GpuHostImpl::EstablishChannelStatus) ./../../base/functional/bind\_internal.h:976:12  

#37 0x55839a9e1310 in Run ./../../base/functional/callback.h:152:12  

#38 0x55839a9e1310 in viz::GpuHostImpl::OnChannelEstablished(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&) ./../../components/viz/host/gpu\_host\_impl.cc:511:25  

#39 0x55839a9ed90d in void base::internal::FunctorTraits<void (viz::GpuHostImpl::\*)(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&), void>::Invoke<void (viz::GpuHostImpl::\*)(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&), base::WeakPtr[viz::GpuHostImpl](javascript:void(0);) const&, int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&>(void (viz::GpuHostImpl::\*)(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&), base::WeakPtr[viz::GpuHostImpl](javascript:void(0);) const&, int&&, bool&&, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)&&, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&) ./../../base/functional/bind\_internal.h:746:12  

#40 0x55839a9ed678 in MakeItSo<void (viz::GpuHostImpl::\*)(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &), std::\_\_Cr::tuple<base::WeakPtr[viz::GpuHostImpl](javascript:void(0);), int, bool>, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &> ./../../base/functional/bind\_internal.h:953:5  

#41 0x55839a9ed678 in RunImpl<void (viz::GpuHostImpl::\*)(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &), std::\_\_Cr::tuple<base::WeakPtr[viz::GpuHostImpl](javascript:void(0);), int, bool>, 0UL, 1UL, 2UL> ./../../base/functional/bind\_internal.h:1025:12  

#42 0x55839a9ed678 in base::internal::Invoker<base::internal::BindState<void (viz::GpuHostImpl::\*)(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&), base::WeakPtr[viz::GpuHostImpl](javascript:void(0);), int, bool>, void (mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&)>::RunOnce(base::internal::BindStateBase\*, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)&&, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&) ./../../base/functional/bind\_internal.h:976:12  

#43 0x5583873bee8b in Run ./../../base/functional/callback.h:152:12  

#44 0x5583873bee8b in viz::mojom::GpuService\_EstablishGpuChannel\_ForwardToCallback::Accept(mojo::Message\*) ./gen/services/viz/privileged/mojom/gl/gpu\_service.mojom.cc:2186:26  

#45 0x558395e16410 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1011:41  

#46 0x558395e32c52 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#47 0x558395e1b579 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:701:20  

#48 0x558395e418ce in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#49 0x558395e3f891 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:710:7  

#50 0x558395e32c52 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#51 0x558395e0c0d5 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:561:49  

#52 0x558395e0df83 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:618:14  

#53 0x558395e0d96c in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:451:3  

#54 0x558395e0d96c in mojo::Connector::OnWatcherHandleReady(char const\*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:417:3  

#55 0x558395e10b1f in Invoke<void (mojo::Connector::\*)(const char \*, unsigned int), mojo::Connector \*, const char \*, unsigned int> ./../../base/functional/bind\_internal.h:746:12  

#56 0x558395e10b1f in MakeItSo<void (mojo::Connector::\*const &)(const char \*, unsigned int), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind\_internal.h:925:12  

#57 0x558395e10b1f in void base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(char const\*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::RunImpl<void (mojo::Connector::\* const&)(char const\*, unsigned int), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>> const&, 0ul, 1ul>(void (mojo::Connector::\* const&)(char const\*, unsigned int), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>> const&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul>, unsigned int&&) ./../../base/functional/bind\_internal.h:1025:12  

#58 0x558395e107f6 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(char const\*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) ./../../base/functional/bind\_internal.h:989:12  

#59 0x558386bc4a4e in Run ./../../base/functional/callback.h:333:12  

#60 0x558386bc4a4e in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.h:192:14  

#61 0x558386bc4c65 in Invoke<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:636:12  

#62 0x558386bc4c65 in MakeItSo<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::\_\_Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:925:12  

#63 0x558386bc4c65 in RunImpl<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::\_\_Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#64 0x558386bc4c65 in base::internal::Invoker<base::internal::BindState<void (\*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase\*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind\_internal.h:989:12  

#65 0x558395e9d3d7 in Run ./../../base/functional/callback.h:333:12  

#66 0x558395e9d3d7 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#67 0x558395e9e2ec in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);) &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind\_internal.h:746:12  

#68 0x558395e9e2ec in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind\_internal.h:953:5  

#69 0x558395e9e2ec in void base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::\*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/functional/bind\_internal.h:1025:12  

#70 0x558393a5f767 in Run ./../../base/functional/callback.h:152:12  

#71 0x558393a5f767 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#72 0x558393abe6d5 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#73 0x558393abe6d5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#74 0x558393abd5f5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#75 0x558393abf714 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#76 0x558393c2b3d9 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:691:48  

#77 0x558393ac0499 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:651:12  

#78 0x5583939e360f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#79 0x55838acbb943 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1067:18  

#80 0x55838acc3276 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:158:15  

#81 0x55838acb226a in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:34:28  

#82 0x558390c77a14 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:686:10  

#83 0x558390c7c034 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1263:10  

#84 0x558390c7b8b7 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1117:12  

#85 0x558390c74622 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36  

#86 0x558390c74c99 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:343:10  

#87 0x558381e30978 in ChromeMain ./../../chrome/app/chrome\_main.cc:187:12  

#88 0x7f39c48df082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x51b000181b60 is located 992 bytes inside of 1416-byte region [0x51b000181780,0x51b000181d08)  

freed by thread T0 (chrome) here:  

#0 0x558381e2ea2d in operator delete(void\*) *asan\_rtl*:3  

#1 0x55838b42cf61 in DeleteInternal[gpu::GpuChannelHost](javascript:void(0);) ./../../base/memory/ref\_counted.h:428:5  

#2 0x55838b42cf61 in Destruct ./../../base/memory/ref\_counted.h:381:5  

#3 0x55838b42cf61 in Release ./../../base/memory/ref\_counted.h:417:7  

#4 0x55838b42cf61 in Release ./../../base/memory/scoped\_refptr.h:382:8  

#5 0x55838b42cf61 in ~scoped\_refptr ./../../base/memory/scoped\_refptr.h:280:7  

#6 0x55838b42cf61 in reset ./../../base/memory/scoped\_refptr.h:310:18  

#7 0x55838b42cf61 in operator= ./../../base/memory/scoped\_refptr.h:296:5  

#8 0x55838b42cf61 in content::BrowserGpuChannelHostFactory::EstablishGpuChannel(base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>, bool) ./../../content/browser/gpu/browser\_gpu\_channel\_host\_factory.cc:347:18  

#9 0x55838b42cc08 in content::BrowserGpuChannelHostFactory::EstablishGpuChannel(base::OnceCallback<void (scoped\_refptr[gpu::GpuChannelHost](javascript:void(0);))>) ./../../content/browser/gpu/browser\_gpu\_channel\_host\_factory.cc:317:3  

#10 0x55838cca357a in content::VizProcessTransportFactory::CreateLayerTreeFrameSink(base::WeakPtr[ui::Compositor](javascript:void(0);)) ./../../content/browser/compositor/viz\_process\_transport\_factory.cc:208:35  

#11 0x55839a8c8f67 in RequestNewLayerTreeFrameSink ./../../ui/compositor/compositor.cc:764:23  

#12 0x55839a8c8f67 in non-virtual thunk to ui::Compositor::RequestNewLayerTreeFrameSink() ./../../ui/compositor/compositor.cc:0:0  

#13 0x558398bd3875 in Invoke<void (cc::SingleThreadProxy::\*)(), const base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);) &> ./../../base/functional/bind\_internal.h:746:12  

#14 0x558398bd3875 in MakeItSo<void (cc::SingleThreadProxy::\*)(), std::\_\_Cr::tuple<base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);) > > ./../../base/functional/bind\_internal.h:953:5  

#15 0x558398bd3875 in void base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::\*)(), base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);)>, void ()>::RunImpl<void (cc::SingleThreadProxy::\*)(), std::\_\_Cr::tuple<base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);)>, 0ul>(void (cc::SingleThreadProxy::\*&&)(), std::\_\_Cr::tuple<base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);)>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul>) ./../../base/functional/bind\_internal.h:1025:12  

#16 0x55838259f409 in Run ./../../base/functional/callback.h:152:12  

#17 0x55838259f409 in void base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::ForwardOnce<>() ./../../base/cancelable\_callback.h:127:26  

#18 0x55838259f695 in Invoke<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()> >::\*)(), const base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()> > > &> ./../../base/functional/bind\_internal.h:746:12  

#19 0x55838259f695 in MakeItSo<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()> >::\*)(), std::\_\_Cr::tuple<base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()> > > > > ./../../base/functional/bind\_internal.h:953:5  

#20 0x55838259f695 in void base::internal::Invoker<base::internal::BindState<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::\*)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>>, void ()>::RunImpl<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::\*)(), std::\_\_Cr::tuple<base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>>, 0ul>(void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::\*&&)(), std::\_\_Cr::tuple<base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul>) ./../../base/functional/bind\_internal.h:1025:12  

#21 0x558393a5f767 in Run ./../../base/functional/callback.h:152:12  

#22 0x558393a5f767 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#23 0x558393abe6d5 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#24 0x558393abe6d5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#25 0x558393abd5f5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#26 0x558393abf714 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#27 0x558393c2aa4a in base::MessagePumpGlib::HandleDispatch() ./../../base/message\_loop/message\_pump\_glib.cc:646:46  

#28 0x558393c2da62 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:274:43  

#29 0x7f39c5ffa17c in g\_main\_context\_dispatch ??:0:0

previously allocated by thread T0 (chrome) here:  

#0 0x558381e2e1cd in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55838b42aff6 in MakeRefCounted<gpu::GpuChannelHost, const int &, const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);) > ./../../base/memory/scoped\_refptr.h:155:12  

#2 0x55838b42aff6 in content::BrowserGpuChannelHostFactory::EstablishRequest::OnEstablished(mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&, viz::GpuHostImpl::EstablishChannelStatus) ./../../content/browser/gpu/browser\_gpu\_channel\_host\_factory.cc:207:20  

#3 0x55838b42f18e in Invoke<void (content::BrowserGpuChannelHostFactory::EstablishRequest::\*)(mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus), scoped\_refptr[content::BrowserGpuChannelHostFactory::EstablishRequest](javascript:void(0);), mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus> ./../../base/functional/bind\_internal.h:746:12  

#4 0x55838b42f18e in MakeItSo<void (content::BrowserGpuChannelHostFactory::EstablishRequest::\*)(mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus), std::\_\_Cr::tuple<scoped\_refptr[content::BrowserGpuChannelHostFactory::EstablishRequest](javascript:void(0);) >, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus> ./../../base/functional/bind\_internal.h:925:12  

#5 0x55838b42f18e in RunImpl<void (content::BrowserGpuChannelHostFactory::EstablishRequest::\*)(mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus), std::\_\_Cr::tuple<scoped\_refptr[content::BrowserGpuChannelHostFactory::EstablishRequest](javascript:void(0);) >, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#6 0x55838b42f18e in base::internal::Invoker<base::internal::BindState<void (content::BrowserGpuChannelHostFactory::EstablishRequest::\*)(mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&, viz::GpuHostImpl::EstablishChannelStatus), scoped\_refptr[content::BrowserGpuChannelHostFactory::EstablishRequest](javascript:void(0);)>, void (mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&, viz::GpuHostImpl::EstablishChannelStatus)>::RunOnce(base::internal::BindStateBase\*, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)&&, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&, viz::GpuHostImpl::EstablishChannelStatus) ./../../base/functional/bind\_internal.h:976:12  

#7 0x55839a9e1310 in Run ./../../base/functional/callback.h:152:12  

#8 0x55839a9e1310 in viz::GpuHostImpl::OnChannelEstablished(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&) ./../../components/viz/host/gpu\_host\_impl.cc:511:25  

#9 0x55839a9ed90d in void base::internal::FunctorTraits<void (viz::GpuHostImpl::\*)(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&), void>::Invoke<void (viz::GpuHostImpl::\*)(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&), base::WeakPtr[viz::GpuHostImpl](javascript:void(0);) const&, int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&>(void (viz::GpuHostImpl::\*)(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&), base::WeakPtr[viz::GpuHostImpl](javascript:void(0);) const&, int&&, bool&&, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)&&, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&) ./../../base/functional/bind\_internal.h:746:12  

#10 0x55839a9ed678 in MakeItSo<void (viz::GpuHostImpl::\*)(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &), std::\_\_Cr::tuple<base::WeakPtr[viz::GpuHostImpl](javascript:void(0);), int, bool>, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &> ./../../base/functional/bind\_internal.h:953:5  

#11 0x55839a9ed678 in RunImpl<void (viz::GpuHostImpl::\*)(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), const gpu::GPUInfo &, const gpu::GpuFeatureInfo &), std::\_\_Cr::tuple<base::WeakPtr[viz::GpuHostImpl](javascript:void(0);), int, bool>, 0UL, 1UL, 2UL> ./../../base/functional/bind\_internal.h:1025:12  

#12 0x55839a9ed678 in base::internal::Invoker<base::internal::BindState<void (viz::GpuHostImpl::\*)(int, bool, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&), base::WeakPtr[viz::GpuHostImpl](javascript:void(0);), int, bool>, void (mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);), gpu::GPUInfo const&, gpu::GpuFeatureInfo const&)>::RunOnce(base::internal::BindStateBase\*, mojo::ScopedHandleBase[mojo::MessagePipeHandle](javascript:void(0);)&&, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&) ./../../base/functional/bind\_internal.h:976:12  

#13 0x5583873bee8b in Run ./../../base/functional/callback.h:152:12  

#14 0x5583873bee8b in viz::mojom::GpuService\_EstablishGpuChannel\_ForwardToCallback::Accept(mojo::Message\*) ./gen/services/viz/privileged/mojom/gl/gpu\_service.mojom.cc:2186:26  

#15 0x558395e16410 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1011:41  

#16 0x558395e32c52 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#17 0x558395e1b579 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:701:20  

#18 0x558395e418ce in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#19 0x558395e3f891 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:710:7  

#20 0x558395e32c52 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#21 0x558395e0c0d5 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:561:49  

#22 0x558395e0df83 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:618:14  

#23 0x558395e0d96c in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:451:3  

#24 0x558395e0d96c in mojo::Connector::OnWatcherHandleReady(char const\*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:417:3  

#25 0x558395e10b1f in Invoke<void (mojo::Connector::\*)(const char \*, unsigned int), mojo::Connector \*, const char \*, unsigned int> ./../../base/functional/bind\_internal.h:746:12  

#26 0x558395e10b1f in MakeItSo<void (mojo::Connector::\*const &)(const char \*, unsigned int), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind\_internal.h:925:12  

#27 0x558395e10b1f in void base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(char const\*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::RunImpl<void (mojo::Connector::\* const&)(char const\*, unsigned int), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>> const&, 0ul, 1ul>(void (mojo::Connector::\* const&)(char const\*, unsigned int), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>> const&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul>, unsigned int&&) ./../../base/functional/bind\_internal.h:1025:12  

#28 0x558395e107f6 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(char const\*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) ./../../base/functional/bind\_internal.h:989:12  

#29 0x558386bc4a4e in Run ./../../base/functional/callback.h:333:12  

#30 0x558386bc4a4e in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.h:192:14  

#31 0x558386bc4c65 in Invoke<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:636:12  

#32 0x558386bc4c65 in MakeItSo<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::\_\_Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:925:12  

#33 0x558386bc4c65 in RunImpl<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::\_\_Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#34 0x558386bc4c65 in base::internal::Invoker<base::internal::BindState<void (\*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase\*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind\_internal.h:989:12  

#35 0x558395e9d3d7 in Run ./../../base/functional/callback.h:333:12  

#36 0x558395e9d3d7 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#37 0x558395e9e2ec in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);) &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind\_internal.h:746:12  

#38 0x558395e9e2ec in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind\_internal.h:953:5  

#39 0x558395e9e2ec in void base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::\*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/functional/bind\_internal.h:1025:12  

#40 0x558393a5f767 in Run ./../../base/functional/callback.h:152:12  

#41 0x558393a5f767 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#42 0x558393abe6d5 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#43 0x558393abe6d5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#44 0x558393abd5f5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#45 0x558393abf714 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#46 0x558393c2b3d9 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:691:48  

#47 0x558393ac0499 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:651:12  

#48 0x5583939e360f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#49 0x55838acbb943 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1067:18

SUMMARY: AddressSanitizer: heap-use-after-free (/home/kuer/chromium\_version/latest\_asan/chrome+0x1fa8aeee) (BuildId: e8c423599b8f6d28)  

Shadow bytes around the buggy address:  

0x51b000181880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x51b000181900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x51b000181980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x51b000181a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x51b000181a80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x51b000181b00: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd  

0x51b000181b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x51b000181c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x51b000181c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x51b000181d00: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x51b000181d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==2097487==ADDITIONAL INFO

==2097487==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x558395e9dcf6 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple\_watcher.cc:102:13

MiraclePtr Status: PROTECTED  

This crash occurred while a raw\_ptr<T> object containing a dangling pointer was being dereferenced.  

MiraclePtr is expected to make this crash non-exploitable once fully enabled.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==2097487==END OF ADDITIONAL INFO  

==2097487==ABORTING

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 204 B)
- [background.js](attachments/background.js) (text/plain, 61 B)

## Timeline

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### ar...@google.com (2023-06-09)

Thanks for the bug report!

I tried to reproduce. I got an error, but a different one:
```
./out/Debug/chrome --user-data-dir=/tmp --enable-features=SharedBitmapToSharedImage --load-extension="extension_path" 
[1]+  ����� 1                 nohup Xvfb :4 > /dev/null 2>&1
[393651:393651:0609/115439.726753:ERROR:chrome_browser_cloud_management_controller.cc(162)] Cloud management controller initialization aborted as CBCM is not enabled.
[393688:393688:0609/115439.837520:ERROR:viz_main_impl.cc(186)] Exiting GPU process due to errors during initialization
[393802:393802:0609/115439.964933:ERROR:viz_main_impl.cc(186)] Exiting GPU process due to errors during initialization
[393651:393674:0609/115440.013024:FATAL:browser_child_process_host_impl.cc(139)] Check failed: ::content::BrowserThread::CurrentlyOn(BrowserThread::UI). Must be called on Chrome_UIThread; actually called on Chrome_IOThread.
#0 0x55ff1fe14622 base::debug::CollectStackTrace()
#1 0x55ff1fdfbb33 base::debug::StackTrace::StackTrace()
#2 0x55ff1fcf4a1d logging::LogMessage::~LogMessage()
#3 0x55ff1fcdb920 logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage()
#4 0x55ff1fcdb777 logging::CheckError::~CheckError()
#5 0x55ff1d140458 content::BrowserChildProcessHost::FromID()
#6 0x55ff2344f9a4 extensions::ProcessesTerminateFunction::GetProcessHandleOnIO()
#7 0x55ff1a0f2e91 base::internal::Invoker<>::RunOnce()
#8 0x55ff19cd08df base::internal::ReturnAsParamAdapter<>()
#9 0x55ff19cd0a70 base::internal::Invoker<>::RunOnce()
#10 0x55ff1fdbcdb1 base::(anonymous namespace)::PostTaskAndReplyRelay::RunTaskAndPostReply()
#11 0x55ff1fdbd3aa base::internal::Invoker<>::RunOnce()
#12 0x55ff1fd570ee base::TaskAnnotator::RunTaskImpl()
#13 0x55ff1fd8c603 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#14 0x55ff1fd8b914 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#15 0x55ff1fd8d155 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#16 0x55ff1fe24e23 base::MessagePumpEpoll::Run()
#17 0x55ff1fd8d7cb base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#18 0x55ff1fd31f22 base::RunLoop::Run()
#19 0x55ff1fdc24cd base::Thread::Run()
#20 0x55ff1d176a90 content::BrowserProcessIOThread::IOThreadRun()
#21 0x55ff1d176a12 content::BrowserProcessIOThread::Run()
#22 0x55ff1fdc289a base::Thread::ThreadMain()
#23 0x55ff1fdde558 base::(anonymous namespace)::ThreadFunc()
#24 0x7f4fb3e96fd4 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x88fd3)
#25 0x7f4fb3f1766c (/usr/lib/x86_64-linux-gnu/libc.so.6+0x10966b)
Task trace:
#0 0x55ff2344f30a extensions::ProcessesTerminateFunction::Run()
#1 0x55ff20d0ae6b IPC::(anonymous namespace)::ChannelAssociatedGroupController::Accept()
#2 0x55ff209f82e7 mojo::SimpleWatcher::Context::Notify()
Crash keys:
  "extension-1" = "pmnllbnhomlkaplikekhaejolihhfmhh"
  "num-extensions" = "1"
  "breadcrumbs" = "0:00:00 Startup
"
  "reentry_guard_tls_slot" = "unused"
  "variations" = "db59f83a-3f4a17df,8bccc03b-3f4a17df,5f2c0f7c-3f4a17df,da493d3c-3f4a17df,90080029-3f4a17df,ecaca27c-a123a0cf,391562d6-3f4a17df,c07e430b-2fa7646d,9f476f76-3f4a17df,f3ed486d-3f4a17df,e28cd73c-3f4a17df,36d5ee52-3f4a17df,b13ca3d9-84f6cff8,65570806-377be55a,4ad2637c-3f4a17df,8659ca17-3f4a17df,ade3efeb-e1cc0f14,3fd33f16-27b09c4c,1166396-1166396,3095b8fe-3f4a17df,5f36436a-3f4a17df,83a5bd87-3f4a17df,fc9ceed7-3f4a17df,87a22c16-5123f057,5de2eeca-3f4a17df,78aca32-3f4a17df,250dda8b-3f4a17df,28329b37-17727981,37d8197a-7aa38cf1,dcceede7-908383eb,fd4b313c-3f4a17df,afa71e8b-aea4882e,e5ade537-e5ade537,47be28a0-3f4a17df,ef4764d7-c9f4d4ef,a779bb20-3f4a17df,f0682056-324bfab2,788db06c-edf91aba,2da2abac-b7f59038,d3566fbd-c6f74b94,75ffb03a-3f4a17df,c4e32a07-3a3251a9,741e95d4-3f4a17df,a83da733-3f4a17df,1b245f0d-eaf735a3,520b2a89-88bf9f37,42f1f10d-98837767,ad4acdda-3f4a17df,7fb629a1-60fdb59,90860314-3f4a17df,d6284ba0-e23dfbb,de2c80ca-da5d16c4,6ad21bf6-727a1257,ca12356a-23abfa84,cb87f652-63e2f275,28410024-3f4a17df,b1ceb06f-3f4a17df,d2e8e6e4-3f4a17df,8c82550d-3f4a17df,f829ac10-139f755,eddd0d82-3f4a17df,c65234ba-3f4a17df,f9bc57e6-3f4a17df,e5249c82-3f4a17df,99c32967-f0a9a61e,8d494515-3f4a17df,e0e63e5f-decb98bf,6fea66b3-6beda842,201e98ca-53757ab,5c7c8339-3f4a17df,6e4a21fe-efc28565,4749874c-455e925b,824b2e8d-78665c96,caa76e48-caa76e48,857feb0-3f4a17df,737aa661-737aa661,e521d2ef-3f4a17df,e79d4056-80f9a33e,7ec047c2-3f4a17df,ec21b181-3f4a17df,cf80e172-3f4a17df,632df39e-3f4a17df,38bbf096-3f4a17df,a18444ea-a18444ea,13427e22-3f4a17df,4ff8f5b5-9c1f9d3b,8d7344de-3f4a17df,5851a53a-8897814c,910af27f-3f4a17df,60929057-3a760994,fd051c38-3f4a17df,f2855e3d-de2b6078,42f0e0ea-75d6947c,160d8d8d-9d12ca0c,4ea303a6-3f4a17df,3042ad4b-ad2fa222,b3c54bb3-a058b5d3,f654ad46-c94f66c2,9e5c75f1-30e1b12b,17cd3426-3f4a17df,77b7ea96-9a159164,1bb6a450-3f4a17df,3e99ae8f-21e7ece7,df41299a-3f4a17df,b349dbf8-3f4a17df,5be633d-3f4a17df,870c1db8-3f4a17df,f14c322f-f9a43703,7d41a07a-3f4a17df,78ccea4c-3f4a17df,55c00994-2f393ff0,263848e4-3f4a17df,9982045c-3f4a17df,cf64b238-3f4a17df,a79ba57a-f23d1dea,ea23a088-7e86b809,371f259c-3f4a17df,b46f46d-3f4a17df,3b96a1d-3f4a17df,ebf54a8-3f4a17df,6becb1e-a6ea97a2,76415c5-eea70808,595f5eb0-f23d1dea,f73d1d52-3f4a17df,87f33ad6-3f4a17df,1584cf60-3f4a17df,b32beb42-872d480b,db96cb03-3f4a17df,81b1a2c3-3f4a17df,d92d97b4-e913bec6,c23b87b6-539521b5,94f1fa38-ced24900,d7d493f4-a9412e3f,565dffc5-565dffc5,9a564e2a-3f4a17df,d664a1aa-3f4a17df,8ddeb5cd-3f4a17df,2f7e7ede-3f4a17df,ee9c60c1-6bb5a4c5,9481ce98-3d47f4f4,4b935545-3d47f4f4,be338734-dee66fa8,a41a7188-dee66fa8,70678518-dee66fa8,5f9907a9-dee66fa8,8eeccb9a-dee66fa8,2b465683-dee66fa8,9a38bae3-3d47f4f4,6948f188-f23d1dea,c9af35af-ec47f63d,2d1e43a3-3f4a17df,b0455224-417b7a1e,d4e31d2-417b7a1e,386dc267-3d47f4f4,1db9f55a-139f755,"
  "num-experiments" = "155"
  "switch-2" = "--load-extension=extension_path"
  "switch-1" = "--user-data-dir=/tmp"
  "num-switches" = "5"
  "commandline-enabled-feature-1" = "SharedBitmapToSharedImage"
  "osarch" = "x86_64"
  "pid" = "393651"
  "ptype" = "browser"
```

I will try again in release mode.

### ar...@google.com (2023-06-09)

[Comment Deleted]

### ar...@google.com (2023-06-09)

Hi reporter,
I am not able to reproduce the bug specific to SharedBitmapToSharedImage. I am using:
```
git fetch
git checkout 158f730d8773af87ef2013367616bd68ea9d258c
gclient sync
gn gen ./out/asan --args='use_goma=true is_debug=false is_asan=true dcheck_always_on=false'
ninja -C ./out/asan chrome
mkdir -p extension_path
tee extension_path/manifest.json << EOT
{
  "name": "UAF crash",
  "description": "A UAF crash",
  "version": "2.0",
  "background": {
    "service_worker": "background.js"
  },

  "manifest_version": 3,
  "permissions": [
    "processes"
  ]
}
EOT

tee extension_path/background.js << EOT
setTimeout(() => {
	chrome.processes.terminate(2)
}, 100);
EOT

./out/asan/chrome \
  --user-data-dir=/tmp \
  --enable-features=SharedBitmapToSharedImage \
  --load-extension="extension_path"
```

Am I missing something?

### ar...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2023-06-12)

Hi, you can reproduce this issue with the asan build: 
gs://chromium-browser-asan/linux-release/asan-linux-release-1156017.zip

This issue also affect the chromium(arm) in MacOS.

### 0x...@gmail.com (2023-06-12)

Another heap-buffer-overflow crash also occurs.
=================================================================
==2740446==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x51b000140860 at pc 0x564bd0d5a213 bp 0x7fff9eab32d0 sp 0x7fff9eab32c8
READ of size 8 at 0x51b000140860 thread T0 (chrome)
==2740446==WARNING: invalid path to external symbolizer!
==2740446==WARNING: Failed to use and restart external symbolizer!
    #0 0x564bd0d5a212 in GetForExtraction ./../../base/allocator/partition_allocator/pointers/raw_ptr.h:1044:47
    #1 0x564bd0d5a212 in operator gpu::GpuChannelHost * ./../../base/allocator/partition_allocator/pointers/raw_ptr.h:817:59
    #2 0x564bd0d5a212 in gpu::SharedImageInterfaceProxy::DestroySharedImage(gpu::SyncToken const&, gpu::Mailbox const&) ./../../gpu/ipc/client/shared_image_interface_proxy.cc:296:64
    #3 0x564bd0d32dec in gpu::ClientSharedImageInterface::DestroySharedImage(gpu::SyncToken const&, gpu::Mailbox const&) ./../../gpu/ipc/client/client_shared_image_interface.cc:178:11
    #4 0x564be37a25e2 in cc::(anonymous namespace)::BitmapSoftwareBacking::~BitmapSoftwareBacking() ./../../cc/raster/bitmap_raster_buffer_provider.cc:58:45
    #5 0x564be37a277d in cc::(anonymous namespace)::BitmapSoftwareBacking::~BitmapSoftwareBacking() ./../../cc/raster/bitmap_raster_buffer_provider.cc:56:37
    #6 0x564be3585fbe in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:65:5
    #7 0x564be3585fbe in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:297:7
    #8 0x564be3585fbe in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:263:75
    #9 0x564be3585fbe in ~PoolResource ./../../cc/resources/resource_pool.cc:639:43
    #10 0x564be3585fbe in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:65:5
    #11 0x564be3585fbe in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:297:7
    #12 0x564be3585fbe in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:263:75
    #13 0x564be3585fbe in cc::ResourcePool::DeleteResource(std::__Cr::unique_ptr<cc::ResourcePool::PoolResource, std::__Cr::default_delete<cc::ResourcePool::PoolResource>>) ./../../cc/resources/resource_pool.cc:496:1
    #14 0x564be358703c in cc::ResourcePool::InvalidateResources() ./../../cc/resources/resource_pool.cc:368:5
    #15 0x564be366fc90 in cc::LayerTreeHostImpl::CleanUpTileManagerResources() ./../../cc/trees/layer_tree_host_impl.cc:3805:19
    #16 0x564be368425c in cc::LayerTreeHostImpl::ReleaseLayerTreeFrameSink() ./../../cc/trees/layer_tree_host_impl.cc:3836:3
    #17 0x564be368589a in cc::LayerTreeHostImpl::InitializeFrameSink(cc::LayerTreeFrameSink*) ./../../cc/trees/layer_tree_host_impl.cc:3910:3
    #18 0x564be3911f3e in cc::SingleThreadProxy::SetLayerTreeFrameSink(cc::LayerTreeFrameSink*) ./../../cc/trees/single_thread_proxy.cc:164:27
    #19 0x564be35ec402 in cc::LayerTreeHost::SetLayerTreeFrameSink(std::__Cr::unique_ptr<cc::LayerTreeFrameSink, std::__Cr::default_delete<cc::LayerTreeFrameSink>>) ./../../cc/trees/layer_tree_host.cc:523:11
    #20 0x564be5629a06 in ui::Compositor::SetLayerTreeFrameSink(std::__Cr::unique_ptr<cc::LayerTreeFrameSink, std::__Cr::default_delete<cc::LayerTreeFrameSink>>, mojo::AssociatedRemote<viz::mojom::DisplayPrivate>) ./../../ui/compositor/compositor.cc:339:10
    #21 0x564bd79e9bd9 in content::VizProcessTransportFactory::OnEstablishedGpuChannel(base::WeakPtr<ui::Compositor>, scoped_refptr<gpu::GpuChannelHost>) ./../../content/browser/compositor/viz_process_transport_factory.cc:478:15
    #22 0x564bd79ee6d8 in void base::internal::FunctorTraits<void (content::VizProcessTransportFactory::*)(base::WeakPtr<ui::Compositor>, scoped_refptr<gpu::GpuChannelHost>), void>::Invoke<void (content::VizProcessTransportFactory::*)(base::WeakPtr<ui::Compositor>, scoped_refptr<gpu::GpuChannelHost>), base::WeakPtr<content::VizProcessTransportFactory> const&, base::WeakPtr<ui::Compositor>, scoped_refptr<gpu::GpuChannelHost>>(void (content::VizProcessTransportFactory::*)(base::WeakPtr<ui::Compositor>, scoped_refptr<gpu::GpuChannelHost>), base::WeakPtr<content::VizProcessTransportFactory> const&, base::WeakPtr<ui::Compositor>&&, scoped_refptr<gpu::GpuChannelHost>&&) ./../../base/functional/bind_internal.h:746:12
    #23 0x564bd79ee3ff in MakeItSo<void (content::VizProcessTransportFactory::*)(base::WeakPtr<ui::Compositor>, scoped_refptr<gpu::GpuChannelHost>), std::__Cr::tuple<base::WeakPtr<content::VizProcessTransportFactory>, base::WeakPtr<ui::Compositor> >, scoped_refptr<gpu::GpuChannelHost> > ./../../base/functional/bind_internal.h:953:5
    #24 0x564bd79ee3ff in RunImpl<void (content::VizProcessTransportFactory::*)(base::WeakPtr<ui::Compositor>, scoped_refptr<gpu::GpuChannelHost>), std::__Cr::tuple<base::WeakPtr<content::VizProcessTransportFactory>, base::WeakPtr<ui::Compositor> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:1025:12
    #25 0x564bd79ee3ff in base::internal::Invoker<base::internal::BindState<void (content::VizProcessTransportFactory::*)(base::WeakPtr<ui::Compositor>, scoped_refptr<gpu::GpuChannelHost>), base::WeakPtr<content::VizProcessTransportFactory>, base::WeakPtr<ui::Compositor>>, void (scoped_refptr<gpu::GpuChannelHost>)>::RunOnce(base::internal::BindStateBase*, scoped_refptr<gpu::GpuChannelHost>&&) ./../../base/functional/bind_internal.h:976:12
    #26 0x564bd616dc84 in Run ./../../base/functional/callback.h:152:12
    #27 0x564bd616dc84 in content::BrowserGpuChannelHostFactory::EstablishRequest::RunCallbacksOnMain() ./../../content/browser/gpu/browser_gpu_channel_host_factory.cc:238:25
    #28 0x564bd616d775 in FinishAndRunCallbacksOnMain ./../../content/browser/gpu/browser_gpu_channel_host_factory.cc:222:3
    #29 0x564bd616d775 in Finish ./../../content/browser/gpu/browser_gpu_channel_host_factory.cc:216:3
    #30 0x564bd616d775 in content::BrowserGpuChannelHostFactory::EstablishRequest::OnEstablished(mojo::ScopedHandleBase<mojo::MessagePipeHandle>, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&, viz::GpuHostImpl::EstablishChannelStatus) ./../../content/browser/gpu/browser_gpu_channel_host_factory.cc:211:3
    #31 0x564bd617161e in Invoke<void (content::BrowserGpuChannelHostFactory::EstablishRequest::*)(mojo::ScopedHandleBase<mojo::MessagePipeHandle>, const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus), scoped_refptr<content::BrowserGpuChannelHostFactory::EstablishRequest>, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus> ./../../base/functional/bind_internal.h:746:12
    #32 0x564bd617161e in MakeItSo<void (content::BrowserGpuChannelHostFactory::EstablishRequest::*)(mojo::ScopedHandleBase<mojo::MessagePipeHandle>, const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus), std::__Cr::tuple<scoped_refptr<content::BrowserGpuChannelHostFactory::EstablishRequest> >, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus> ./../../base/functional/bind_internal.h:925:12
    #33 0x564bd617161e in RunImpl<void (content::BrowserGpuChannelHostFactory::EstablishRequest::*)(mojo::ScopedHandleBase<mojo::MessagePipeHandle>, const gpu::GPUInfo &, const gpu::GpuFeatureInfo &, viz::GpuHostImpl::EstablishChannelStatus), std::__Cr::tuple<scoped_refptr<content::BrowserGpuChannelHostFactory::EstablishRequest> >, 0UL> ./../../base/functional/bind_internal.h:1025:12
    #34 0x564bd617161e in base::internal::Invoker<base::internal::BindState<void (content::BrowserGpuChannelHostFactory::EstablishRequest::*)(mojo::ScopedHandleBase<mojo::MessagePipeHandle>, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&, viz::GpuHostImpl::EstablishChannelStatus), scoped_refptr<content::BrowserGpuChannelHostFactory::EstablishRequest>>, void (mojo::ScopedHandleBase<mojo::MessagePipeHandle>, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&, viz::GpuHostImpl::EstablishChannelStatus)>::RunOnce(base::internal::BindStateBase*, mojo::ScopedHandleBase<mojo::MessagePipeHandle>&&, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&, viz::GpuHostImpl::EstablishChannelStatus) ./../../base/functional/bind_internal.h:976:12
    #35 0x564be57498e0 in Run ./../../base/functional/callback.h:152:12
    #36 0x564be57498e0 in viz::GpuHostImpl::OnChannelEstablished(int, bool, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&) ./../../components/viz/host/gpu_host_impl.cc:511:25
    #37 0x564be5755edd in void base::internal::FunctorTraits<void (viz::GpuHostImpl::*)(int, bool, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&), void>::Invoke<void (viz::GpuHostImpl::*)(int, bool, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&), base::WeakPtr<viz::GpuHostImpl> const&, int, bool, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&>(void (viz::GpuHostImpl::*)(int, bool, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&), base::WeakPtr<viz::GpuHostImpl> const&, int&&, bool&&, mojo::ScopedHandleBase<mojo::MessagePipeHandle>&&, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&) ./../../base/functional/bind_internal.h:746:12
    #38 0x564be5755c48 in MakeItSo<void (viz::GpuHostImpl::*)(int, bool, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, const gpu::GPUInfo &, const gpu::GpuFeatureInfo &), std::__Cr::tuple<base::WeakPtr<viz::GpuHostImpl>, int, bool>, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, const gpu::GPUInfo &, const gpu::GpuFeatureInfo &> ./../../base/functional/bind_internal.h:953:5
    #39 0x564be5755c48 in RunImpl<void (viz::GpuHostImpl::*)(int, bool, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, const gpu::GPUInfo &, const gpu::GpuFeatureInfo &), std::__Cr::tuple<base::WeakPtr<viz::GpuHostImpl>, int, bool>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1025:12
    #40 0x564be5755c48 in base::internal::Invoker<base::internal::BindState<void (viz::GpuHostImpl::*)(int, bool, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&), base::WeakPtr<viz::GpuHostImpl>, int, bool>, void (mojo::ScopedHandleBase<mojo::MessagePipeHandle>, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&)>::RunOnce(base::internal::BindStateBase*, mojo::ScopedHandleBase<mojo::MessagePipeHandle>&&, gpu::GPUInfo const&, gpu::GpuFeatureInfo const&) ./../../base/functional/bind_internal.h:976:12
    #41 0x564bd20ffecb in Run ./../../base/functional/callback.h:152:12
    #42 0x564bd20ffecb in viz::mojom::GpuService_EstablishGpuChannel_ForwardToCallback::Accept(mojo::Message*) ./gen/services/viz/privileged/mojom/gl/gpu_service.mojom.cc:2186:26
    #43 0x564be0b66550 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1011:41
    #44 0x564be0b82d92 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #45 0x564be0b6b6b9 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:701:20
    #46 0x564be0b91a0e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1096:42
    #47 0x564be0b8f9d1 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:710:7
    #48 0x564be0b82d92 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #49 0x564be0b5c215 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) ./../../mojo/public/cpp/bindings/lib/connector.cc:561:49
    #50 0x564be0b5e0c3 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:618:14
    #51 0x564be0b60555 in Invoke<void (mojo::Connector::*)(), const base::WeakPtr<mojo::Connector> &> ./../../base/functional/bind_internal.h:746:12
    #52 0x564be0b60555 in MakeItSo<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector> > > ./../../base/functional/bind_internal.h:953:5
    #53 0x564be0b60555 in void base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunImpl<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>, 0ul>(void (mojo::Connector::*&&)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) ./../../base/functional/bind_internal.h:1025:12
    #54 0x564bde7a9c57 in Run ./../../base/functional/callback.h:152:12
    #55 0x564bde7a9c57 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:186:34
    #56 0x564bde80ba95 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:488:11)> ./../../base/task/common/task_annotator.h:89:5
    #57 0x564bde80ba95 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:23
    #58 0x564bde80a9b5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351:41
    #59 0x564bde80cad4 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #60 0x564bde97b66a in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:646:46
    #61 0x564bde97e682 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:274:43
    #62 0x7fb6a0a2717c in g_main_context_dispatch ??:0:0

Address 0x51b000140860 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/kuer/chromium_version/latest_asan/chrome+0x1217e212) (BuildId: 04e1cae293a53688)
Shadow bytes around the buggy address:
  0x51b000140580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51b000140600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51b000140680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51b000140700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51b000140780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x51b000140800: fa fa fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa
  0x51b000140880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51b000140900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51b000140980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51b000140a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x51b000140a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==2740446==ADDITIONAL INFO

==2740446==Note: Please include this section with the ASan report.
Task trace:
    #0 0x564be0b5e909 in PostDispatchNextMessageFromPipe ./../../mojo/public/cpp/bindings/lib/connector.cc:581:7
    #1 0x564be0b5e909 in mojo::Connector::ScheduleDispatchOfPendingMessagesOrWaitForMore(unsigned long) ./../../mojo/public/cpp/bindings/lib/connector.cc:602:5
    #2 0x564be0bede36 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:102:13


==2740446==END OF ADDITIONAL INFO
==2740446==ABORTING
[0612/000603.823824:ERROR:nacl_helper_linux.cc(355)] NaCl helper process running without a sandbox!
Most likely you need to configure your SUID sandbox correctly

### [Deleted User] (2023-06-12)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@google.com (2023-06-12)

Thanks!
I definitely can't reproduce. On two very different Linux desktop. I executed:
```
wget  https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1156017.zip --output-document=out.zip

unzip out.zip

mkdir -p extension_path
tee extension_path/manifest.json << EOT
{
  "name": "UAF crash",
  "description": "A UAF crash",
  "version": "2.0",
  "background": {
    "service_worker": "background.js"
  },

  "manifest_version": 3,
  "permissions": [
    "processes"
  ]
}
EOT

tee extension_path/background.js << EOT
setTimeout(() => {
	chrome.processes.terminate(2)
}, 100);
EOT

./asan-linux-release-1156017/chrome
  --user-data-dir=/tmp \
  --enable-features=SharedBitmapToSharedImage \
  --load-extension="extension_path"
```

I trust you this is reproducing on your side.

Tentatively, I will use:
- Security_Severity-High: Memory corruption. I think it happens in the browser process.
- Security_Impact-None: This is behind the "SharedBitmapToSharedImage" feature, which is turned off by default.
- OS: A priori, every OSes except iOS.
- FoundIn-XXX: I don't know. I can't reproduce.
- Owner: magchen@chromium.org, as owner of the feature. Could you please take a look? Feel free to re-evaluate Security_Severity and Security_Impact..

[Monorail components: Internals>Services>Viz]

### ah...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### ah...@google.com (2023-06-27)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-07-12)

Adding some CC's. Zmo, is there someone who might have cycles to take a look at this? I realize there may not be a lot to go on ...

### ma...@chromium.org (2023-07-12)

The feature SharedBitmapToSharedImage is not completed yet. It's not in a state that you can enable it by default. I am still working on it. The progress is expected to be slow.

### za...@google.com (2023-08-10)

Secondary security shepherd here, magchen@chromium.org any update on this bug? Do we have an ETA already? Thanks.

### zm...@chromium.org (2023-08-10)

Since this is behind a feature flag that's not ready to be enabled anytime soon, drop to P2.

magchen@ is on vacation. Add vasilyt@ as well.

### pa...@chromium.org (2023-09-27)

ping @magchen@chromium.com, have you been able to make progress on this?

### ma...@chromium.org (2023-09-27)

I am working on it. Thanks.

### ma...@chromium.org (2023-10-02)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-10-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9971898fcd3ba38585e68e529f5461fa1aff2453

commit 9971898fcd3ba38585e68e529f5461fa1aff2453
Author: Maggie Chen <magchen@chromium.org>
Date: Mon Oct 23 21:30:00 2023

Remove shared_image_interface_ from LayerTreeFrameSink since it's not ready for testing yet

This code path is disabled by default because it's not fully
implemented yet. But people will enable the flag
kSharedBitmapToSharedImage and run the tests on it. Now remove the
code so it cannot be enabled by the flag.

|Shared_image_interface| will be put back after "notification for
gpu channel lost" and "OutputSurface SharedIamge to
SharedBitmap support" are implemented.

Bug: 1434885, 1453577
Change-Id: Iccb0b932ea9cfa32b07c73061359025ac8972b1f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4968653
Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org>
Commit-Queue: Maggie Chen <magchen@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1213757}

[modify] https://crrev.com/9971898fcd3ba38585e68e529f5461fa1aff2453/cc/trees/layer_tree_frame_sink.cc


### ma...@chromium.org (2023-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-02)

Congratulations asnine! The Chrome VRP has decided to award you $2,000 for this highly mitigated bug, mitigated by requiring the installation of an extension and shutdown to trigger. This issue is also BRP protected, which was not enabled across all platforms at the time of this report, so that was not part of the consideration in terms of mitigation at that time. 
Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2024-01-30)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-30)

This issue was migrated from crbug.com/chromium/1453577?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1434885]
[Monorail mergedwith: crbug.com/chromium/1457700, crbug.com/chromium/1457773, crbug.com/chromium/1476288, crbug.com/chromium/1488192, crbug.com/chromium/1519655]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065570)*
