# Security: Heap-use-after-free in BluetoothChooserController::AddOrUpdateDevice

| Field | Value |
|-------|-------|
| **Issue ID** | [40053894](https://issues.chromium.org/issues/40053894) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bluetooth |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2020-11-16 |
| **Bounty** | $15,000.00 |

## Description

**VERSION**  

Chrome Version: 89.0.4327.0 (Official Build) canary (x86\_64)  

Operating System: MacOS

**REPRODUCTION CASE**

1. Go to <https://maxlgu.github.io/pr/max-nonbasiccard/>
2. Click on "Busy" button.
3. In payment dialog try to change <http://www.google.com> to <https://lbstyle.github.io/index.html> then click on "Go!" button.
4. Click anywhere.

=================================================================  

==9728==ERROR: AddressSanitizer: heap-use-after-free on address 0x60f00012e248 at pc 0x0001344e8b4c bp 0x7fff518a8e30 sp 0x7fff518a8e28  

READ of size 8 at 0x60f00012e248 thread T0  

#0 0x1344e8b4b in std::\_\_1::\_\_hash\_iterator<std::\_\_1::\_\_hash\_node<std::\_\_1::\_\_hash\_value\_type<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::basic\_string<unsigned short, base::string16\_internals::string16\_char\_traits, std::\_\_1::allocator<unsigned short> > >, void\*>\*> std::\_\_1::\_\_hash\_table<std::\_\_1::\_\_hash\_value\_type<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::basic\_string<unsigned short, base::string16\_internals::string16\_char\_traits, std::\_\_1::allocator<unsigned short> > >, std::\_\_1::\_\_unordered\_map\_hasher<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::\_\_hash\_value\_type<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::basic\_string<unsigned short, base::string16\_internals::string16\_char\_traits, std::\_\_1::allocator<unsigned short> > >, std::\_\_1::hash<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > >, true>, std::\_\_1::\_\_unordered\_map\_equal<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::\_\_hash\_value\_type<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::basic\_string<unsigned short, base::string16\_internals::string16\_char\_traits, std::\_\_1::allocator<unsigned short> > >, std::\_\_1::equal\_to<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > >, true>, std::\_\_1::allocator<std::\_\_1::\_\_hash\_value\_type<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::basic\_string<unsigned short, base::string16\_internals::string16\_char\_traits, std::\_\_1::allocator<unsigned short> > > > >::find<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > >(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) \_\_hash\_table:799  

#1 0x1344e62d3 in BluetoothChooserController::AddOrUpdateDevice(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, bool, std::\_\_1::basic\_string<unsigned short, base::string16\_internals::string16\_char\_traits, std::\_\_1::allocator<unsigned short> > const&, bool, bool, int) bluetooth\_chooser\_controller.cc:217  

#2 0x11ef0a665 in content::BluetoothDeviceChooserController::AddFilteredDevice(device::BluetoothDevice const&) bluetooth\_device\_chooser\_controller.cc:338  

#3 0x12e1d989f in device::BluetoothAdapterMac::ClassicDeviceAdded(IOBluetoothDevice\*) bluetooth\_adapter\_mac.mm:604  

#4 0x12e1de27a in device::BluetoothAdapterMac::AddPairedDevices() bluetooth\_adapter\_mac.mm:757  

#5 0x12e1dafac in device::BluetoothAdapterMac::PollAdapter() bluetooth\_adapter\_mac.mm:577  

#6 0x12e1d4fdb in device::BluetoothAdapterMac::LazyInitialize() bluetooth\_adapter\_mac.mm:363  

#7 0x12e1d6098 in device::BluetoothAdapterMac::IsPowered() const bluetooth\_adapter\_mac.mm:223  

#8 0x11ef08326 in content::BluetoothDeviceChooserController::GetDevice(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&)>, base::OnceCallback<void (blink::mojom::WebBluetoothResult)>) bluetooth\_device\_chooser\_controller.cc:319  

#9 0x11ef2448c in content::WebBluetoothServiceImpl::RequestDeviceImpl(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)) web\_bluetooth\_service\_impl.cc:1579  

#10 0x11ef4c011 in void base::internal::FunctorTraits<void (content::WebBluetoothServiceImpl::\*)(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), void>::Invoke<void (content::WebBluetoothServiceImpl::\*)(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), base::WeakPtr[content::WebBluetoothServiceImpl](javascript:void(0);), mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);) >(void (content::WebBluetoothServiceImpl::\*)(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), base::WeakPtr[content::WebBluetoothServiceImpl](javascript:void(0);)&&, mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);)&&, base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>&&, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)&&) bind\_internal.h:498  

#11 0x11eeec36c in BluetoothAdapterFactoryWrapper::OnGetAdapter(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)) callback.h:101  

#12 0x11eeedc75 in void base::internal::FunctorTraits<void (BluetoothAdapterFactoryWrapper::\*)(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), void>::Invoke<void (BluetoothAdapterFactoryWrapper::\*)(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), base::WeakPtr<BluetoothAdapterFactoryWrapper>, base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);) >(void (BluetoothAdapterFactoryWrapper::\*)(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), base::WeakPtr<BluetoothAdapterFactoryWrapper>&&, base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>&&, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)&&) bind\_internal.h:498  

#13 0x12e1a69ca in device::BluetoothAdapterFactory::AdapterInitialized() callback.h:101  

#14 0x12e1ddea9 in device::BluetoothAdapterMac::Initialize(base::OnceCallback<void ()>) callback.h:101  

#15 0x12e1a6228 in device::BluetoothAdapterFactory::GetAdapter(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>) bluetooth\_adapter\_factory.cc:87  

#16 0x11eeebe3f in BluetoothAdapterFactoryWrapper::AcquireAdapter(device::BluetoothAdapter::Observer\*, base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>) bluetooth\_adapter\_factory\_wrapper.cc:60  

#17 0x11ef239ed in content::WebBluetoothServiceImpl::RequestDevice(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>) web\_bluetooth\_service\_impl.cc:784  

#18 0x11d313742 in blink::mojom::WebBluetoothServiceStubDispatch::AcceptWithResponder(blink::mojom::WebBluetoothService\*, mojo::Message\*, std::\_\_1::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_1::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) web\_bluetooth.mojom.cc:3834  

#19 0x11ef3bce7 in blink::mojom::WebBluetoothServiceStub<mojo::RawPtrImplRefTraits[blink::mojom::WebBluetoothService](javascript:void(0);) >::AcceptWithResponder(mojo::Message\*, std::\_\_1::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_1::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) web\_bluetooth.mojom.h:409  

#20 0x128eedab3 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) interface\_endpoint\_client.cc:528  

#21 0x128ef74b8 in mojo::MessageDispatcher::Accept(mojo::Message\*) message\_dispatcher.cc:41  

#22 0x128f04daf in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) multiplex\_router.cc:955  

#23 0x128f033a7 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) multiplex\_router.cc:622  

#24 0x128ef74b8 in mojo::MessageDispatcher::Accept(mojo::Message\*) message\_dispatcher.cc:41  

#25 0x128ee0dc0 in mojo::Connector::DispatchMessage(mojo::Message) connector.cc:508  

#26 0x128ee3581 in mojo::Connector::ReadAllAvailableMessages() connector.cc:566  

#27 0x128f5c4b4 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) callback.h:168  

#28 0x128f5e08a in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) bind\_internal.h:498  

#29 0x12754bb85 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) callback.h:101  

#30 0x12759439a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:357  

#31 0x127593af7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:268  

#32 0x1276b5b98 in \_\_\_ZN4base24MessagePumpCFRunLoopBase13RunWorkSourceEPv\_block\_invoke message\_pump\_mac.mm:358  

#33 0x12769deb9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xe05feb9)  

#34 0x1276b3ff5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*) message\_pump\_mac.mm:334  

#35 0x7fffc05ace50 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (CoreFoundation:x86\_64+0xa4e50)  

#36 0x7fffc058e0cb in \_\_CFRunLoopDoSources0+0x22b (CoreFoundation:x86\_64+0x860cb)  

#37 0x7fffc058d5b5 in \_\_CFRunLoopRun+0x3a5 (CoreFoundation:x86\_64+0x855b5)  

#38 0x7fffc058cfb3 in CFRunLoopRunSpecific+0x1a3 (CoreFoundation:x86\_64+0x84fb3)  

#39 0x7fffbfaebebb in RunCurrentEventLoopInMode+0xef (HIToolbox:x86\_64+0x30ebb)  

#40 0x7fffbfaebcf0 in ReceiveNextEventCommon+0x1af (HIToolbox:x86\_64+0x30cf0)  

#41 0x7fffbfaebb25 in \_BlockUntilNextEventMatchingListInModeWithFilter+0x46 (HIToolbox:x86\_64+0x30b25)  

#42 0x7fffbe080a03 in \_DPSNextEvent+0x45f (AppKit:x86\_64+0x46a03)  

#43 0x7fffbe7fc7ed in -[NSApplication(NSEvent) \_nextEventMatchingEventMask:untilDate:inMode:dequeue:]+0xaeb (AppKit:x86\_64+0x7c27ed)  

#44 0x128a110e2 in \_\_71-[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]\_block\_invoke chrome\_browser\_application\_mac.mm:227  

#45 0x12769deb9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xe05feb9)  

#46 0x128a10c8a in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:] chrome\_browser\_application\_mac.mm:226  

#47 0x7fffbe07538a in -[NSApplication run]+0x39d (AppKit:x86\_64+0x3b38a)  

#48 0x1276b83aa in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:691  

#49 0x1276b2c89 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*) message\_pump\_mac.mm:149  

#50 0x12759655b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:477  

#51 0x1274e9e9b in base::RunLoop::Run() run\_loop.cc:124  

#52 0x127d03ca1 in ChromeBrowserMainParts::MainMessageLoopRun(int\*) chrome\_browser\_main.cc:1711  

#53 0x11f009a59 in content::BrowserMainLoop::RunMainMessageLoopParts() browser\_main\_loop.cc:1019  

#54 0x11f00f8f1 in content::BrowserMainRunnerImpl::Run() browser\_main\_runner\_impl.cc:150  

#55 0x11f000c5c in content::BrowserMain(content::MainFunctionParams const&) browser\_main.cc:47  

#56 0x126d540b6 in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) content\_main\_runner\_impl.cc:521  

#57 0x126d53323 in content::ContentMainRunnerImpl::Run(bool) content\_main\_runner\_impl.cc:883  

#58 0x126d4f41b in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content\_main.cc:372  

#59 0x126d4fadc in content::ContentMain(content::ContentMainParams const&) content\_main.cc:398  

#60 0x1196449b5 in ChromeMain chrome\_main.cc:130  

#61 0x10e35229e in main chrome\_exe\_main\_mac.cc:117  

#62 0x7fffd61d5234 in start+0x0 (libdyld.dylib:x86\_64+0x5234)

0x60f00012e248 is located 72 bytes inside of 176-byte region [0x60f00012e200,0x60f00012e2b0)  

freed by thread T0 here:  

#0 0x10e63d479 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x43479)  

#1 0x127c639a9 in ChromeBluetoothDelegate::RunBluetoothChooser(content::RenderFrameHost\*, base::RepeatingCallback<void (content::BluetoothChooserEvent, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&)> const&) memory:2378  

#2 0x11ef07e43 in content::BluetoothDeviceChooserController::GetDevice(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&)>, base::OnceCallback<void (blink::mojom::WebBluetoothResult)>) bluetooth\_device\_chooser\_controller.cc:296  

#3 0x11ef2448c in content::WebBluetoothServiceImpl::RequestDeviceImpl(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)) web\_bluetooth\_service\_impl.cc:1579  

#4 0x11ef4c011 in void base::internal::FunctorTraits<void (content::WebBluetoothServiceImpl::\*)(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), void>::Invoke<void (content::WebBluetoothServiceImpl::\*)(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), base::WeakPtr[content::WebBluetoothServiceImpl](javascript:void(0);), mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);) >(void (content::WebBluetoothServiceImpl::\*)(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), base::WeakPtr[content::WebBluetoothServiceImpl](javascript:void(0);)&&, mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);)&&, base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>&&, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)&&) bind\_internal.h:498  

#5 0x11eeec36c in BluetoothAdapterFactoryWrapper::OnGetAdapter(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)) callback.h:101  

#6 0x11eeedc75 in void base::internal::FunctorTraits<void (BluetoothAdapterFactoryWrapper::\*)(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), void>::Invoke<void (BluetoothAdapterFactoryWrapper::\*)(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), base::WeakPtr<BluetoothAdapterFactoryWrapper>, base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);) >(void (BluetoothAdapterFactoryWrapper::\*)(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), base::WeakPtr<BluetoothAdapterFactoryWrapper>&&, base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>&&, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)&&) bind\_internal.h:498  

#7 0x12e1a69ca in device::BluetoothAdapterFactory::AdapterInitialized() callback.h:101  

#8 0x12e1ddea9 in device::BluetoothAdapterMac::Initialize(base::OnceCallback<void ()>) callback.h:101  

#9 0x12e1a6228 in device::BluetoothAdapterFactory::GetAdapter(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>) bluetooth\_adapter\_factory.cc:87  

#10 0x11eeebe3f in BluetoothAdapterFactoryWrapper::AcquireAdapter(device::BluetoothAdapter::Observer\*, base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>) bluetooth\_adapter\_factory\_wrapper.cc:60  

#11 0x11ef239ed in content::WebBluetoothServiceImpl::RequestDevice(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>) web\_bluetooth\_service\_impl.cc:784  

#12 0x11d313742 in blink::mojom::WebBluetoothServiceStubDispatch::AcceptWithResponder(blink::mojom::WebBluetoothService\*, mojo::Message\*, std::\_\_1::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_1::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) web\_bluetooth.mojom.cc:3834  

#13 0x11ef3bce7 in blink::mojom::WebBluetoothServiceStub<mojo::RawPtrImplRefTraits[blink::mojom::WebBluetoothService](javascript:void(0);) >::AcceptWithResponder(mojo::Message\*, std::\_\_1::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_1::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) web\_bluetooth.mojom.h:409  

#14 0x128eedab3 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) interface\_endpoint\_client.cc:528  

#15 0x128ef74b8 in mojo::MessageDispatcher::Accept(mojo::Message\*) message\_dispatcher.cc:41  

#16 0x128f04daf in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) multiplex\_router.cc:955  

#17 0x128f033a7 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) multiplex\_router.cc:622  

#18 0x128ef74b8 in mojo::MessageDispatcher::Accept(mojo::Message\*) message\_dispatcher.cc:41  

#19 0x128ee0dc0 in mojo::Connector::DispatchMessage(mojo::Message) connector.cc:508  

#20 0x128ee3581 in mojo::Connector::ReadAllAvailableMessages() connector.cc:566  

#21 0x128f5c4b4 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) callback.h:168  

#22 0x128f5e08a in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) bind\_internal.h:498  

#23 0x12754bb85 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) callback.h:101  

#24 0x12759439a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:357  

#25 0x127593af7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:268  

#26 0x1276b5b98 in \_\_\_ZN4base24MessagePumpCFRunLoopBase13RunWorkSourceEPv\_block\_invoke message\_pump\_mac.mm:358  

#27 0x12769deb9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xe05feb9)  

#28 0x1276b3ff5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*) message\_pump\_mac.mm:334  

#29 0x7fffc05ace50 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (CoreFoundation:x86\_64+0xa4e50)

previously allocated by thread T0 here:  

#0 0x10e63d330 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x43330)  

#1 0x127392f57 in operator new(unsigned long) new.cpp:67  

#2 0x127c638b1 in ChromeBluetoothDelegate::RunBluetoothChooser(content::RenderFrameHost\*, base::RepeatingCallback<void (content::BluetoothChooserEvent, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&)> const&) chrome\_bluetooth\_delegate.cc:73  

#3 0x11ef07e43 in content::BluetoothDeviceChooserController::GetDevice(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&)>, base::OnceCallback<void (blink::mojom::WebBluetoothResult)>) bluetooth\_device\_chooser\_controller.cc:296  

#4 0x11ef2448c in content::WebBluetoothServiceImpl::RequestDeviceImpl(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)) web\_bluetooth\_service\_impl.cc:1579  

#5 0x11ef4c011 in void base::internal::FunctorTraits<void (content::WebBluetoothServiceImpl::\*)(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), void>::Invoke<void (content::WebBluetoothServiceImpl::\*)(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), base::WeakPtr[content::WebBluetoothServiceImpl](javascript:void(0);), mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);) >(void (content::WebBluetoothServiceImpl::\*)(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), base::WeakPtr[content::WebBluetoothServiceImpl](javascript:void(0);)&&, mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);)&&, base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>&&, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)&&) bind\_internal.h:498  

#6 0x11eeec36c in BluetoothAdapterFactoryWrapper::OnGetAdapter(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)) callback.h:101  

#7 0x11eeedc75 in void base::internal::FunctorTraits<void (BluetoothAdapterFactoryWrapper::\*)(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), void>::Invoke<void (BluetoothAdapterFactoryWrapper::\*)(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), base::WeakPtr<BluetoothAdapterFactoryWrapper>, base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);) >(void (BluetoothAdapterFactoryWrapper::\*)(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)), base::WeakPtr<BluetoothAdapterFactoryWrapper>&&, base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>&&, scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)&&) bind\_internal.h:498  

#8 0x12e1a69ca in device::BluetoothAdapterFactory::AdapterInitialized() callback.h:101  

#9 0x12e1ddea9 in device::BluetoothAdapterMac::Initialize(base::OnceCallback<void ()>) callback.h:101  

#10 0x12e1a6228 in device::BluetoothAdapterFactory::GetAdapter(base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>) bluetooth\_adapter\_factory.cc:87  

#11 0x11eeebe3f in BluetoothAdapterFactoryWrapper::AcquireAdapter(device::BluetoothAdapter::Observer\*, base::OnceCallback<void (scoped\_refptr[device::BluetoothAdapter](javascript:void(0);))>) bluetooth\_adapter\_factory\_wrapper.cc:60  

#12 0x11ef239ed in content::WebBluetoothServiceImpl::RequestDevice(mojo::StructPtr[blink::mojom::WebBluetoothRequestDeviceOptions](javascript:void(0);), base::OnceCallback<void (blink::mojom::WebBluetoothResult, mojo::StructPtr[blink::mojom::WebBluetoothDevice](javascript:void(0);))>) web\_bluetooth\_service\_impl.cc:784  

#13 0x11d313742 in blink::mojom::WebBluetoothServiceStubDispatch::AcceptWithResponder(blink::mojom::WebBluetoothService\*, mojo::Message\*, std::\_\_1::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_1::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) web\_bluetooth.mojom.cc:3834  

#14 0x11ef3bce7 in blink::mojom::WebBluetoothServiceStub<mojo::RawPtrImplRefTraits[blink::mojom::WebBluetoothService](javascript:void(0);) >::AcceptWithResponder(mojo::Message\*, std::\_\_1::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_1::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) web\_bluetooth.mojom.h:409  

#15 0x128eedab3 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) interface\_endpoint\_client.cc:528  

#16 0x128ef74b8 in mojo::MessageDispatcher::Accept(mojo::Message\*) message\_dispatcher.cc:41  

#17 0x128f04daf in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) multiplex\_router.cc:955  

#18 0x128f033a7 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) multiplex\_router.cc:622  

#19 0x128ef74b8 in mojo::MessageDispatcher::Accept(mojo::Message\*) message\_dispatcher.cc:41  

#20 0x128ee0dc0 in mojo::Connector::DispatchMessage(mojo::Message) connector.cc:508  

#21 0x128ee3581 in mojo::Connector::ReadAllAvailableMessages() connector.cc:566  

#22 0x128f5c4b4 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) callback.h:168  

#23 0x128f5e08a in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) bind\_internal.h:498  

#24 0x12754bb85 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) callback.h:101  

#25 0x12759439a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:357  

#26 0x127593af7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:268  

#27 0x1276b5b98 in \_\_\_ZN4base24MessagePumpCFRunLoopBase13RunWorkSourceEPv\_block\_invoke message\_pump\_mac.mm:358  

#28 0x12769deb9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xe05feb9)  

#29 0x1276b3ff5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*) message\_pump\_mac.mm:334

SUMMARY: AddressSanitizer: heap-use-after-free \_\_hash\_table:799 in std::\_\_1::\_\_hash\_iterator<std::\_\_1::\_\_hash\_node<std::\_\_1::\_\_hash\_value\_type<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::basic\_string<unsigned short, base::string16\_internals::string16\_char\_traits, std::\_\_1::allocator<unsigned short> > >, void\*>\*> std::\_\_1::\_\_hash\_table<std::\_\_1::\_\_hash\_value\_type<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::basic\_string<unsigned short, base::string16\_internals::string16\_char\_traits, std::\_\_1::allocator<unsigned short> > >, std::\_\_1::\_\_unordered\_map\_hasher<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::\_\_hash\_value\_type<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::basic\_string<unsigned short, base::string16\_internals::string16\_char\_traits, std::\_\_1::allocator<unsigned short> > >, std::\_\_1::hash<std::\_\_1::ba  

Shadow bytes around the buggy address:  

0x1c1e00025bf0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

0x1c1e00025c00: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c1e00025c10: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x1c1e00025c20: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c1e00025c30: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

=>0x1c1e00025c40: fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd  

0x1c1e00025c50: fd fd fd fd fd fd fa fa fa fa fa fa fa fa 00 00  

0x1c1e00025c60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1c1e00025c70: 00 00 00 fa fa fa fa fa fa fa fa fa 00 00 00 00  

0x1c1e00025c80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1c1e00025c90: 00 00 fa fa fa fa fa fa fa fa 00 00 00 00 00 00  

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

## Attachments

- [screen.mov](attachments/screen.mov) (video/quicktime, 8.1 MB)

## Timeline

### [Deleted User] (2020-11-16)

[Empty comment from Monorail migration]

### ch...@gmail.com (2020-11-18)

This is a regression from https://crrev.com/ea7e22dd8eadee210ca26e84ead1d5a6bc4e07bb.

### mb...@chromium.org (2020-11-19)

Sorry for the delay here, and thanks for the report!

On a side note, could you please attach any proof of concept files to issues in the future? We don't like to rely on external sites for pocs when we can help it.

[Monorail components: Blink>Bluetooth]

### ch...@gmail.com (2020-11-19)

Oh sorry! I will do that in the future. 

### ms...@google.com (2020-11-19)

+1 for a reduced repro case, I get these errors, presumably because I don't have a payment method registered in my dev browser...
  NotSupportedError: The payment method "https://skilful-reserve-239412.appspot.com/method-manifest" is not supported.
  Cannot make payment
  No enrolled instrument

### ms...@chromium.org (2020-11-19)

Okay, I installed the Max-Pay thing, and that gets me through the process. I'm updating my local build now to continue trying to repro (was on an older revision)

### ch...@gmail.com (2020-11-19)

This bug repro only on MacOS. 

### ms...@chromium.org (2020-11-19)

Okay, updated the bug accordingly, and I'll update my build there.

### re...@chromium.org (2020-11-19)

What appears to be happening here is that BluetoothChooserDesktop acts as glue between content::BluetoothDeviceChooserController and BluetoothChooserController, and only holds a raw pointer to the later. It makes the assumption that it will be destroyed if BluetoothChooserController is, but that assumption is violated in the cases where chrome::ShowDeviceChooserDialog() returns early rather than constructing a view which will own the BluetoothChooserController until it is dismissed.

Other choosers, such as for navigator.usb.requestDevice(), navigator.serial.requestPort() and navigator.hid.requestDevice() avoid this issue by not having a similar intermediate object and guaranteeing that a prompt dismissal event is fired when the ChooserController is destroyed, even if that happens early such as in chrome::ShowDeviceChooserDialog().

### re...@chromium.org (2020-11-19)

This condition became much easier to hit after the fix for https://crbug.com/chromium/1143057 because previously the case where chrome::ShowDeviceChooserDialog() returned early could only be triggered by extensions with a WebContents that could not be mapped back to a Browser instance, such as in an extension popup window.

### ms...@chromium.org (2020-11-20)

Hmm, I guess BluetoothChooserDesktop could hold a WeakPtr, but that might just be a bandaid; this pattern of chooser and controller ownership is strange.

### re...@chromium.org (2020-11-20)

I'm working on a couple of changes. The first will be holding a WeakPtr in BluetoothChooserDesktop. This will be similar to how UsbChooserController passes WeakPtrs to itself when making external calls. The second will be revising my earlier fix to make sure that the appropriate events are passed back to the //content layer to make sure that the automatic dismissal of the chooser is recognized.

I'm open to other suggestions to improve the ownership model. This permissions code is challenging because there are a lot of agents which control the lifecycle of a prompt.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9e1196f5e0b789af65df444d97ffe50adae27b00

commit 9e1196f5e0b789af65df444d97ffe50adae27b00
Author: Mike Wasserman <msw@chromium.org>
Date: Fri Nov 20 04:15:50 2020

Bluetooth: Use WeakPtr for prompt controllers

The desktop chooser and scanning prompt hold controller raw pointers.
The controllers might be destroyed immediately, leaving bad pointers.
Use WeakPtrs instead of raw pointers and refactor init patterns.

Bug: 1149692
Change-Id: Ic1efee18ec2e98921206bea14c3c1500ea085877
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2551936
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Michael Wasserman <msw@chromium.org>
Cr-Commit-Position: refs/heads/master@{#829523}

[modify] https://crrev.com/9e1196f5e0b789af65df444d97ffe50adae27b00/chrome/browser/bluetooth/chrome_bluetooth_delegate.cc
[modify] https://crrev.com/9e1196f5e0b789af65df444d97ffe50adae27b00/chrome/browser/ui/bluetooth/bluetooth_chooser_controller.cc
[modify] https://crrev.com/9e1196f5e0b789af65df444d97ffe50adae27b00/chrome/browser/ui/bluetooth/bluetooth_chooser_controller.h
[modify] https://crrev.com/9e1196f5e0b789af65df444d97ffe50adae27b00/chrome/browser/ui/bluetooth/bluetooth_chooser_desktop.cc
[modify] https://crrev.com/9e1196f5e0b789af65df444d97ffe50adae27b00/chrome/browser/ui/bluetooth/bluetooth_chooser_desktop.h
[modify] https://crrev.com/9e1196f5e0b789af65df444d97ffe50adae27b00/chrome/browser/ui/bluetooth/bluetooth_scanning_prompt_controller.cc
[modify] https://crrev.com/9e1196f5e0b789af65df444d97ffe50adae27b00/chrome/browser/ui/bluetooth/bluetooth_scanning_prompt_controller.h
[modify] https://crrev.com/9e1196f5e0b789af65df444d97ffe50adae27b00/chrome/browser/ui/bluetooth/bluetooth_scanning_prompt_desktop.cc
[modify] https://crrev.com/9e1196f5e0b789af65df444d97ffe50adae27b00/chrome/browser/ui/bluetooth/bluetooth_scanning_prompt_desktop.h


### ms...@chromium.org (2020-11-20)

Should be fixed by the change above; I'll verify on the next Canary with that change and then request merge for M-88.

### ms...@chromium.org (2020-11-20)

Not available on canary, but fixed on ToT, requesting merge of this targeted crash fix for M-88.

### ch...@gmail.com (2020-11-21)

Double-check. Fixed on canary 89.0.4332.0.

### [Deleted User] (2020-11-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-21)

Your change meets the bar and is auto-approved for M88. Please go ahead and merge the CL to branch 4324 (refs/branch-heads/4324) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/83c20d21547fd6f8cf5f16a3a7e687e48390f142

commit 83c20d21547fd6f8cf5f16a3a7e687e48390f142
Author: Mike Wasserman <msw@chromium.org>
Date: Mon Nov 23 20:25:06 2020

Bluetooth: Use WeakPtr for prompt controllers

The desktop chooser and scanning prompt hold controller raw pointers.
The controllers might be destroyed immediately, leaving bad pointers.
Use WeakPtrs instead of raw pointers and refactor init patterns.

(cherry picked from commit 9e1196f5e0b789af65df444d97ffe50adae27b00)

Bug: 1149692
Change-Id: Ic1efee18ec2e98921206bea14c3c1500ea085877
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2551936
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Michael Wasserman <msw@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#829523}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2554097
Reviewed-by: Michael Wasserman <msw@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#263}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/83c20d21547fd6f8cf5f16a3a7e687e48390f142/chrome/browser/bluetooth/chrome_bluetooth_delegate.cc
[modify] https://crrev.com/83c20d21547fd6f8cf5f16a3a7e687e48390f142/chrome/browser/ui/bluetooth/bluetooth_chooser_controller.cc
[modify] https://crrev.com/83c20d21547fd6f8cf5f16a3a7e687e48390f142/chrome/browser/ui/bluetooth/bluetooth_chooser_controller.h
[modify] https://crrev.com/83c20d21547fd6f8cf5f16a3a7e687e48390f142/chrome/browser/ui/bluetooth/bluetooth_chooser_desktop.cc
[modify] https://crrev.com/83c20d21547fd6f8cf5f16a3a7e687e48390f142/chrome/browser/ui/bluetooth/bluetooth_chooser_desktop.h
[modify] https://crrev.com/83c20d21547fd6f8cf5f16a3a7e687e48390f142/chrome/browser/ui/bluetooth/bluetooth_scanning_prompt_controller.cc
[modify] https://crrev.com/83c20d21547fd6f8cf5f16a3a7e687e48390f142/chrome/browser/ui/bluetooth/bluetooth_scanning_prompt_controller.h
[modify] https://crrev.com/83c20d21547fd6f8cf5f16a3a7e687e48390f142/chrome/browser/ui/bluetooth/bluetooth_scanning_prompt_desktop.cc
[modify] https://crrev.com/83c20d21547fd6f8cf5f16a3a7e687e48390f142/chrome/browser/ui/bluetooth/bluetooth_scanning_prompt_desktop.h


### ms...@chromium.org (2020-11-23)

The fix was merged to M-88; please help verify on the next dev channel release there, thanks!

### ad...@google.com (2020-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-03)

The VRP panel has decided to award $15,000 for this bug :)

### ad...@google.com (2020-12-04)

[Empty comment from Monorail migration]

### re...@chromium.org (2020-12-16)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b5c737a3dea757d03a35dc221807002be40b9dc5

commit b5c737a3dea757d03a35dc221807002be40b9dc5
Author: Stefan Zager <szager@chromium.org>
Date: Fri Jan 08 21:29:44 2021

Add UpdateViewportIntersection breakdowns for UMA

The UMA category was added by:

https://chromium-review.googlesource.com/c/chromium/src/+/2593246

Bug: 1149692
Change-Id: I6016fb72cc62ead7d8f91210a690793cccd693a6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2613346
Commit-Queue: Stefan Zager <szager@chromium.org>
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Mark Pearson <mpearson@chromium.org>
Cr-Commit-Position: refs/heads/master@{#841652}

[modify] https://crrev.com/b5c737a3dea757d03a35dc221807002be40b9dc5/tools/metrics/histograms/histograms_xml/blink/histograms.xml
[modify] https://crrev.com/b5c737a3dea757d03a35dc221807002be40b9dc5/tools/metrics/histograms/histograms_xml/histogram_suffixes_list.xml


### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b936f9ef2fbdfa14e97f3899dbd3653ee4be24f7

commit b936f9ef2fbdfa14e97f3899dbd3653ee4be24f7
Author: Reilly Grant <reillyg@chromium.org>
Date: Thu Apr 29 21:04:43 2021

bluetooth: Add test for background permission requests

This change adds a test for sites which attempt to show the Web
Bluetooth permission prompt while they are in the background. This
scenario exposed a use-after-free which was fixed without a
corresponding test in r829523.

This exposed a more general issue that in this scenario the Promise
returned by requestDevice() would never resolve. Fixing this requires
making sure that the chooser event callback is executed when the
controller is destroyed and fixing the resulting reentrancy issues. To
make this simpler the success and failure callbacks passed to
BluetoothDeviceChooserController have been merged.

Bug: 730593,1149692
Change-Id: I9042e2c636322ad3ab2dff04050b45a5c3ec2fbb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2858256
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Mike Wasserman <msw@chromium.org>
Cr-Commit-Position: refs/heads/master@{#877638}

[modify] https://crrev.com/b936f9ef2fbdfa14e97f3899dbd3653ee4be24f7/chrome/browser/bluetooth/web_bluetooth_browsertest.cc
[modify] https://crrev.com/b936f9ef2fbdfa14e97f3899dbd3653ee4be24f7/chrome/browser/ui/bluetooth/bluetooth_chooser_controller.cc
[modify] https://crrev.com/b936f9ef2fbdfa14e97f3899dbd3653ee4be24f7/content/browser/bluetooth/bluetooth_device_chooser_controller.cc
[modify] https://crrev.com/b936f9ef2fbdfa14e97f3899dbd3653ee4be24f7/content/browser/bluetooth/bluetooth_device_chooser_controller.h
[modify] https://crrev.com/b936f9ef2fbdfa14e97f3899dbd3653ee4be24f7/content/browser/bluetooth/web_bluetooth_service_impl.cc
[modify] https://crrev.com/b936f9ef2fbdfa14e97f3899dbd3653ee4be24f7/content/browser/bluetooth/web_bluetooth_service_impl.h


### is...@google.com (2021-04-29)

This issue was migrated from crbug.com/chromium/1149692?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053894)*
