# Security: UAF in webrtc::PeerConnection::ReportTransportStats()

| Field | Value |
|-------|-------|
| **Issue ID** | [40064615](https://issues.chromium.org/issues/40064615) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ht...@chromium.org |
| **Created** | 2023-05-17 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in webrtc::PeerConnection::ReportTransportStats()

**VERSION**  

Chromium 115.0.5775.0 (Developer Build) (64-bit)  

Revision f4538fa9bfb5e86f0e82a0c5b42638b2e82fd527-refs/heads/main@{#1144563}  

OS Linux

**REPRODUCTION CASE**

1. put the attachments into the webserver and run `python3 -m http.server 8000`
2. run the command:  
   
   ./chrome --user-data-dir=/tmp/any --no-sandbox <http://localhost:8000/poc.html>  
   
   If the rendered page doesn't crash, wait for a little long time.

I can reproduce this issue in both Linux and Windows.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]

=================================================================  

==2296==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x1217aac57358 at pc 0x7ffa5139f088 bp 0x0034423fcfd0 sp 0x0034423fd018  

WRITE of size 8 at 0x1217aac57358 thread T18  

==2296==WARNING: Failed to use and restart external symbolizer!  

==2296==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==2296==\*\*\* Most likely this means that the app is already \*\*\*  

==2296==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==2296==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==2296==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffa5139f087 in std::\_\_Cr::construct\_at<rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);),rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);) &,rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);) \*> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_memory\construct\_at.h:37  

#1 0x7ffa5139ef5f in std::\_\_Cr::vector<rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);),std::\_\_Cr::allocator<rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);) > >::\_\_construct\_at\_end<rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);) \*,0> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1031  

#2 0x7ffa5139a376 in std::\_\_Cr::vector<rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);),std::\_\_Cr::allocator<rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);) > >::vector C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1196  

#3 0x7ffa51441de8 in webrtc::PeerConnection::ReportTransportStats C:\b\s\w\ir\cache\builder\src\third\_party\webrtc\pc\peer\_connection.cc:2752  

#4 0x7ffa514571cb in webrtc::webrtc\_function\_impl::CallHelpers<void (cricket::IceConnectionState)>::CallInlineStorage<`lambda at ../../third_party/webrtc/pc/peer_connection.cc:734:7'> C:\b\s\w\ir\cache\builder\src\third_party\webrtc\rtc_base\untyped_function.h:66 #5 0x7ffa50df4c5e in webrtc::callback_list_impl::CallbackListReceivers::Foreach C:\b\s\w\ir\cache\builder\src\third_party\webrtc\rtc_base\callback_list.cc:77 #6 0x7ffa513b41d4 in webrtc::JsepTransportController::UpdateAggregateStates_n C:\b\s\w\ir\cache\builder\src\third_party\webrtc\pc\jsep_transport_controller.cc:1282 #7 0x7ffa513ab194 in webrtc::JsepTransportController::OnTransportWritableState_n C:\b\s\w\ir\cache\builder\src\third_party\webrtc\pc\jsep_transport_controller.cc:1167 #8 0x7ffa5e0adb62 in cricket::DtlsTransport::set_writable C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\dtls_transport.cc:829 #9 0x7ffa5e0afa41 in cricket::DtlsTransport::OnDtlsEvent C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\dtls_transport.cc:693 #10 0x7ffa6121dbbc in rtc::OpenSSLStreamAdapter::ContinueSSL C:\b\s\w\ir\cache\builder\src\third_party\webrtc\rtc_base\openssl_stream_adapter.cc:915 #11 0x7ffa61218fb0 in rtc::OpenSSLStreamAdapter::OnEvent C:\b\s\w\ir\cache\builder\src\third_party\webrtc\rtc_base\openssl_stream_adapter.cc:773 #12 0x7ffa5e0a976e in cricket::StreamInterfaceChannel::OnPacketReceived C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\dtls_transport.cc:120 #13 0x7ffa5e0b31fa in cricket::DtlsTransport::OnReadPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\dtls_transport.cc:635 #14 0x7ffa5e08a602 in cricket::P2PTransportChannel::OnReadPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\p2p_transport_channel.cc:2217 #15 0x7ffa5e0bd136 in cricket::Connection::OnReadPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\connection.cc:459 #16 0x7ffa61242008 in cricket::UDPPort::OnReadPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\stun_port.cc:411 #17 0x7ffa61243b1e in cricket::UDPPort::HandleIncomingPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\stun_port.cc:352 #18 0x7ffa5e05b2d5 in cricket::AllocationSequence::OnReadPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\client\basic_port_allocator.cc:1736 #19 0x7ffa70c2923d in blink::`anonymous namespace'::IpcPacketSocket::OnDataReceived C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\p2p\ipc\_socket\_factory.cc:664  

#20 0x7ffa71cc2628 in blink::P2PSocketClientImpl::DataReceived C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\p2p\socket\_client\_impl.cc:125  

#21 0x7ffa5ad06dcc in network::mojom::blink::P2PSocketClientStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\services\network\public\mojom\p2p.mojom-blink.cc:1828  

#22 0x7ffa5de77cbb in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:1016  

#23 0x7ffa611bb7d6 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#24 0x7ffa5de7d795 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:701  

#25 0x7ffa5de69b54 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1096  

#26 0x7ffa5de6893e in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:710  

#27 0x7ffa611bb7d6 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#28 0x7ffa5de8e14f in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:550  

#29 0x7ffa5de8fa43 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:607  

#30 0x7ffa5de91a28 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int),base::internal::UnretainedWrapper[mojo::Connector,base::unretained\_traits::MayNotDangle,0](javascript:void(0);) >,void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#31 0x7ffa5348b1c3 in base::RepeatingCallback<void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#32 0x7ffa5348afca in base::internal::Invoker<base::internal::BindState<void (\*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:989  

#33 0x7ffa5dd59e52 in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#34 0x7ffa5dd5946b in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#35 0x7ffa5dd5a828 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);),int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#36 0x7ffa5d2b5cd6 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:186  

#37 0x7ffa6084e212 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:486  

#38 0x7ffa6084cf8f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#39 0x7ffa60881ac3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:40  

#40 0x7ffa608508fe in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:651  

#41 0x7ffa5d320197 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#42 0x7ffa5d27a1bd in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:342  

#43 0x7ffa5d27a5ee in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:414  

#44 0x7ffa5d1d2e21 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:133  

#45 0x7ff7c97f58b3 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:278  

#46 0x7ffac84d26ac in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x1800126ac)  

#47 0x7ffac9e4a9f7 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005a9f7)

0x1217aac57358 is located 0 bytes after 8-byte region [0x1217aac57350,0x1217aac57358)  

allocated by thread T18 here:  

#0 0x7ff7c97fec2d in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffa72ca3a9e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffa4fb38a4d in std::\_\_Cr::vector<perfetto::trace\_processor::GlobalNodeGraph::Edge \*,std::\_\_Cr::allocator<perfetto::trace\_processor::GlobalNodeGraph::Edge \*> >::\_\_vallocate C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:690  

#3 0x7ffa5139a355 in std::\_\_Cr::vector<rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);),std::\_\_Cr::allocator<rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);) > >::vector C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1195  

#4 0x7ffa51441de8 in webrtc::PeerConnection::ReportTransportStats C:\b\s\w\ir\cache\builder\src\third\_party\webrtc\pc\peer\_connection.cc:2752  

#5 0x7ffa514571cb in webrtc::webrtc\_function\_impl::CallHelpers<void (cricket::IceConnectionState)>::CallInlineStorage<`lambda at ../../third_party/webrtc/pc/peer_connection.cc:734:7'> C:\b\s\w\ir\cache\builder\src\third_party\webrtc\rtc_base\untyped_function.h:66 #6 0x7ffa50df4c5e in webrtc::callback_list_impl::CallbackListReceivers::Foreach C:\b\s\w\ir\cache\builder\src\third_party\webrtc\rtc_base\callback_list.cc:77 #7 0x7ffa513b41d4 in webrtc::JsepTransportController::UpdateAggregateStates_n C:\b\s\w\ir\cache\builder\src\third_party\webrtc\pc\jsep_transport_controller.cc:1282 #8 0x7ffa513ab194 in webrtc::JsepTransportController::OnTransportWritableState_n C:\b\s\w\ir\cache\builder\src\third_party\webrtc\pc\jsep_transport_controller.cc:1167 #9 0x7ffa5e0adb62 in cricket::DtlsTransport::set_writable C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\dtls_transport.cc:829 #10 0x7ffa5e0afa41 in cricket::DtlsTransport::OnDtlsEvent C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\dtls_transport.cc:693 #11 0x7ffa6121dbbc in rtc::OpenSSLStreamAdapter::ContinueSSL C:\b\s\w\ir\cache\builder\src\third_party\webrtc\rtc_base\openssl_stream_adapter.cc:915 #12 0x7ffa61218fb0 in rtc::OpenSSLStreamAdapter::OnEvent C:\b\s\w\ir\cache\builder\src\third_party\webrtc\rtc_base\openssl_stream_adapter.cc:773 #13 0x7ffa5e0a976e in cricket::StreamInterfaceChannel::OnPacketReceived C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\dtls_transport.cc:120 #14 0x7ffa5e0b31fa in cricket::DtlsTransport::OnReadPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\dtls_transport.cc:635 #15 0x7ffa5e08a602 in cricket::P2PTransportChannel::OnReadPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\p2p_transport_channel.cc:2217 #16 0x7ffa5e0bd136 in cricket::Connection::OnReadPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\connection.cc:459 #17 0x7ffa61242008 in cricket::UDPPort::OnReadPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\stun_port.cc:411 #18 0x7ffa61243b1e in cricket::UDPPort::HandleIncomingPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\base\stun_port.cc:352 #19 0x7ffa5e05b2d5 in cricket::AllocationSequence::OnReadPacket C:\b\s\w\ir\cache\builder\src\third_party\webrtc\p2p\client\basic_port_allocator.cc:1736 #20 0x7ffa70c2923d in blink::`anonymous namespace'::IpcPacketSocket::OnDataReceived C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\p2p\ipc\_socket\_factory.cc:664  

#21 0x7ffa71cc2628 in blink::P2PSocketClientImpl::DataReceived C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\p2p\socket\_client\_impl.cc:125  

#22 0x7ffa5ad06dcc in network::mojom::blink::P2PSocketClientStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\services\network\public\mojom\p2p.mojom-blink.cc:1828  

#23 0x7ffa5de77cbb in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:1016  

#24 0x7ffa611bb7d6 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#25 0x7ffa5de7d795 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:701  

#26 0x7ffa5de69b54 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1096  

#27 0x7ffa5de6893e in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:710

Thread T18 created by T0 here:  

#0 0x7ff7c97f4392 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffa5d1d1c4f in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:198 #2 0x7ffa5d279371 in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:215 #3 0x7ffa6eb1bc2b in blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\peer_connection_dependency_factory.cc:471 #4 0x7ffa6eb1b66c in blink::PeerConnectionDependencyFactory::GetPcFactory C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\peer_connection_dependency_factory.cc:458 #5 0x7ffa6eb21ef1 in blink::PeerConnectionDependencyFactory::CreatePeerConnection C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\peer_connection_dependency_factory.cc:683 #6 0x7ffa6ab94e97 in blink::RTCPeerConnectionHandler::Initialize C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\rtc_peer_connection_handler.cc:1098 #7 0x7ffa71951ac8 in blink::RTCPeerConnection::RTCPeerConnection C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\rtc_peer_connection.cc:641 #8 0x7ffa7197a465 in cppgc::MakeGarbageCollectedTrait<blink::RTCPeerConnection>::Call<blink::ExecutionContext \*&,webrtc::PeerConnectionInterface::RTCConfiguration,bool,blink::GoogMediaConstraints \*&,blink::ExceptionState &> C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\allocation.h:242 #9 0x7ffa7195104a in blink::MakeGarbageCollected<blink::RTCPeerConnection,blink::ExecutionContext \*&,webrtc::PeerConnectionInterface::RTCConfiguration,bool,blink::GoogMediaConstraints \*&,blink::ExceptionState &> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\garbage_collected.h:37 #10 0x7ffa7194d994 in blink::RTCPeerConnection::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\rtc_peer_connection.cc:568 #11 0x7ffa706e0268 in blink::`anonymous namespace'::v8\_rtc\_peer\_connection::ConstructorCallback C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\renderer\bindings\modules\v8\v8\_rtc\_peer\_connection.cc:612  

#12 0x7ffa53befb9b in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:99  

#13 0x7ffa53bec30c in v8::internal::`anonymous namespace'::HandleApiCallHelper<1> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:113 #14 0x7ffa53beade2 in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:148 #15 0x7ffa53bea1d0 in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:135 #16 0x7ffa72ba58f9 in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit+0x39 (C:\chromium_version\latest_asan\chrome.dll+0x1a31158f9) #17 0x7ffa72b0cbb1 in Builtins_JSBuiltinsConstructStub+0xf1 (C:\chromium_version\latest_asan\chrome.dll+0x1a307cbb1) #18 0x7ffa72c6c1db in Builtins_ConstructHandler+0x2db (C:\chromium_version\latest_asan\chrome.dll+0x1a31dc1db) #19 0x7ffa72b0fa25 in Builtins_InterpreterEntryTrampoline+0xe5 (C:\chromium_version\latest_asan\chrome.dll+0x1a307fa25) #20 0x7ffa72b0fa25 in Builtins_InterpreterEntryTrampoline+0xe5 (C:\chromium_version\latest_asan\chrome.dll+0x1a307fa25) #21 0x7ffa72b0d91b in Builtins_JSEntryTrampoline+0x5b (C:\chromium_version\latest_asan\chrome.dll+0x1a307d91b) #22 0x7ffa72b0d51a in Builtins_JSEntry+0xda (C:\chromium_version\latest_asan\chrome.dll+0x1a307d51a) #23 0x7ffa54093962 in v8::internal::`anonymous namespace'::Invoke C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:427  

#24 0x7ffa54096d9d in v8::internal::Execution::CallScript C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:540  

#25 0x7ffa53a89a88 in v8::Script::Run C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:2316  

#26 0x7ffa62dca193 in blink::V8ScriptRunner::RunCompiledScript C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\v8\_script\_runner.cc:404  

#27 0x7ffa62dcbe4b in blink::V8ScriptRunner::CompileAndRunScript C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\v8\_script\_runner.cc:517  

#28 0x7ffa62d6c8eb in blink::ClassicScript::RunScriptOnScriptStateAndReturnValue C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\script\classic\_script.cc:219  

#29 0x7ffa62d6e0b3 in blink::Script::RunScriptOnScriptState C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\script\script.cc:36  

#30 0x7ffa62d6e60c in blink::Script::RunScript C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\script\script.cc:43  

#31 0x7ffa6b602cf5 in blink::PendingScript::ExecuteScriptBlockInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\script\pending\_script.cc:291  

#32 0x7ffa6b601ddf in blink::PendingScript::ExecuteScriptBlock C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\script\pending\_script.cc:188  

#33 0x7ffa6c54dad3 in blink::ScriptLoader::PrepareScript C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\script\script\_loader.cc:1266  

#34 0x7ffa6b903d75 in blink::HTMLParserScriptRunner::ProcessScriptElementInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\script\html\_parser\_script\_runner.cc:535  

#35 0x7ffa6b903509 in blink::HTMLParserScriptRunner::ProcessScriptElement C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\script\html\_parser\_script\_runner.cc:298  

#36 0x7ffa66a822a5 in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:597  

#37 0x7ffa66a7e0f0 in blink::HTMLDocumentParser::PumpTokenizer C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:661  

#38 0x7ffa66a7c13f in blink::HTMLDocumentParser::PumpTokenizerIfPossible C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:562  

#39 0x7ffa66a7ca6d in blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:547  

#40 0x7ffa66a9c905 in base::internal::Invoker<base::internal::BindState<void (blink::HTMLDocumentParser::\*)(bool, base::TimeTicks),cppgc::internal::BasicPersistent[blink::HTMLDocumentParser,cppgc::internal::StrongPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);),bool,base::TimeTicks>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#41 0x7ffa5d2b5cd6 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:186  

#42 0x7ffa6084e212 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:486  

#43 0x7ffa6084cf8f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#44 0x7ffa60881ac3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:40  

#45 0x7ffa608508fe in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:651  

#46 0x7ffa5d320197 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#47 0x7ffa6004389a in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:331  

#48 0x7ffa5ba5543e in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:767  

#49 0x7ffa5ba581ef in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1140  

#50 0x7ffa5ba52ffd in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:326  

#51 0x7ffa5ba53b33 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:343  

#52 0x7ffa4fa91699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:187  

#53 0x7ff7c97463e4 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#54 0x7ff7c9742bd8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#55 0x7ff7c9b72fab in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#56 0x7ffac84d26ac in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x1800126ac)  

#57 0x7ffac9e4a9f7 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005a9f7)

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_memory\construct\_at.h:37 in std::\_\_Cr::construct\_at<rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);),rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);) &,rtc::scoped\_refptr[webrtc::SctpDataChannel](javascript:void(0);) \*>  

Shadow bytes around the buggy address:  

0x1217aac57080: fa fa fd fa fa fa 00 fa fa fa fd fd fa fa 00 00  

0x1217aac57100: fa fa fd fa fa fa 00 fa fa fa fd fd fa fa fd fa  

0x1217aac57180: fa fa fd fa fa fa 00 00 fa fa fd fa fa fa 00 fa  

0x1217aac57200: fa fa fd fa fa fa 00 fa fa fa fd fd fa fa fa fa  

0x1217aac57280: fa fa fd fa fa fa 00 fa fa fa fd fd fa fa fd fd  

=>0x1217aac57300: fa fa 00 fa fa fa fd fa fa fa 00[fa]fa fa fd fd  

0x1217aac57380: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fa  

0x1217aac57400: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fa  

0x1217aac57480: fa fa fd fd fa fa fd fd fa fa fd fa fa fa 00 fa  

0x1217aac57500: fa fa fd fa fa fa fd fa fa fa fd fd fa fa 00 fa  

0x1217aac57580: fa fa fa fa fa fa fd fd fa fa fd fa fa fa 00 fa  

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

==2296==ADDITIONAL INFO

==2296==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x7ffa5dd5a2e1 in mojo::SimpleWatcher::Context::Notify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:102

==2296==END OF ADDITIONAL INFO  

==2296==ABORTING  

[9440:4264:0516/233437.432:ERROR:ssl\_client\_socket\_impl.cc(980)] handshake failed; returned -1, SSL error code 1, net\_error -101

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 585 B)
- [RTCPeerConnection-perfect-negotiation-helper.js](attachments/RTCPeerConnection-perfect-negotiation-helper.js) (text/plain, 6.0 KB)
- [testharness.js](attachments/testharness.js) (text/plain, 180.4 KB)
- [asan_linux.log](attachments/asan_linux.log) (text/plain, 65.4 KB)

## Timeline

### [Deleted User] (2023-05-17)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-05-18)

Thanks for the report. Unfortunately I haven't been able to reproduce this on an trunk or Stable ASAN build. Are there any other special configuration instructions you might be missing?

herre@: Can you PTAL or someone else on WebRTC? Can you repro, or if not is there enough information in the crash stack to investigate the cause?

[Monorail components: Blink>WebRTC]

### 0x...@gmail.com (2023-05-19)

I just download the latest official asan build to reproduce this issue.
Sometimes it needs long time to be reproduced. 
And you can open the poc tab and wait for hours until it crashes.

### 0x...@gmail.com (2023-05-19)

In fact it can be reproduced in minutes.

### he...@google.com (2023-05-22)

Harald, would you have a chance to look into this? Looks like you wrote the ReportTransportStats code and did some refactoring around the list it iterates. Can you repro? Does this make any sense? 

### 0x...@gmail.com (2023-05-30)

Hi, this issue can also be reproduced in the stable Version 114.0.5735.91 (Official Build) (64-bit).
The point is to wait a few minutes until it crashes

### ht...@chromium.org (2023-05-31)

This crash trace is showing use of the UnsafeList(), which returns a copy of a std:.vector.
It's called on the network / worker thread, but the TransceiverList lives inside the RtpTransmissionManager, which lives on the signaling thread.

The trace shows that at the time of the crash, the signaling thread is calling the TransceiverList.Add function, which will grow the vector by deallocating and allocating a new one, which will naturally create problems.

Possible solutions:
- Guard the list by a lock (ugly)
- Turn UnsafeList() into CrossThreadList(), which will do a blocking call to the signaling thread (not allowed by network thread logic)
- Move ReportTransportStats to the signaling thread
- Revert https://webrtc-review.googlesource.com/c/src/+/213662 which seems to be the CL that moved ReportTransportStats to the network thread

Adding tommi@ to the CC list as the expert on "what goes where" (and the author of the CL)




### to...@chromium.org (2023-05-31)

Related bug: https://bugs.chromium.org/p/webrtc/issues/detail?id=12692

### to...@chromium.org (2023-05-31)

I think that reverting https://webrtc-review.googlesource.com/c/src/+/213662 would be complicated since there are many changes that have landed since, in the same area of the code.

Besides, doing that wouldn't actually solve the core issue with UnsafeList() which I think we should get rid of.

There's another call to UnsafeList() from the network thread from within PeerConnection::OnTransportChanged() which I think we'll need to take a look at too. I'll start by looking into the issue as it relates to the stats.

### ht...@chromium.org (2023-06-01)

I think I'll hotfix this by making a copy of the pointer list that's accessible on the network thread, and updated via a PostTask.


### gi...@appspot.gserviceaccount.com (2023-06-01)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/dba22d31909298161318e00d43a80cdb0abc940f

commit dba22d31909298161318e00d43a80cdb0abc940f
Author: Tommi <tommi@webrtc.org>
Date: Thu Jun 01 14:08:52 2023

Move transceiver iteration loop over to the signaling thread.

This is required for ReportTransportStats since iterating over the
transceiver list from the network thread is not safe.

Bug: chromium:1446274, webrtc:12692
Change-Id: I7c514df9f029112c4b1da85826af91217850fb26
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/307340
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#40197}

[modify] https://crrev.com/dba22d31909298161318e00d43a80cdb0abc940f/pc/peer_connection_integrationtest.cc
[modify] https://crrev.com/dba22d31909298161318e00d43a80cdb0abc940f/pc/peer_connection.h
[modify] https://crrev.com/dba22d31909298161318e00d43a80cdb0abc940f/pc/peer_connection.cc


### gi...@appspot.gserviceaccount.com (2023-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/54a0d5753f1a5c86dd2a592aa8d520e9b500f390

commit 54a0d5753f1a5c86dd2a592aa8d520e9b500f390
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jun 01 19:06:58 2023

Roll WebRTC from 513ab0cb2c00 to dba22d319092 (1 revision)

https://webrtc.googlesource.com/src.git/+log/513ab0cb2c00..dba22d319092

2023-06-01 tommi@webrtc.org Move transceiver iteration loop over to the signaling thread.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com,webrtc-infra@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1446274
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: I30886612f63be2b4859cf039dae8bcb7542ef402
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4581387
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1152039}

[modify] https://crrev.com/54a0d5753f1a5c86dd2a592aa8d520e9b500f390/DEPS


### ct...@chromium.org (2023-06-02)

Current security shepherd here setting some security labels (Sev-High for renderer UAF, FoundIn-114 as it is reported to repro in M114, and adding all Blink platforms).

### [Deleted User] (2023-06-02)

[Empty comment from Monorail migration]

### to...@webrtc.org (2023-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-02)

Requesting merge to stable M114 because latest trunk commit (1152039) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1152039) appears to be after beta branch point (1148114).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-03)

Requesting merge to stable M114 because latest trunk commit (1152039) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1152039) appears to be after beta branch point (1148114).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-04)

Requesting merge to stable M114 because latest trunk commit (1152039) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1152039) appears to be after beta branch point (1148114).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-05)

Requesting merge to stable M114 because latest trunk commit (1152039) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1152039) appears to be after beta branch point (1148114).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-06-06)

please merge this fix to M115/branch 5790 by EOD tomorrow (Tuesday, 6 June) so this fix can be included in next M115/beta 
please merge this fix to M114/branch 5735 by 10am Pacific Friday, 9 June so this fix can be included in the next M114/stable update -- thank you! 

### gi...@appspot.gserviceaccount.com (2023-06-06)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/ba943f71e64a93558a51e75d18917f363b8672e9

commit ba943f71e64a93558a51e75d18917f363b8672e9
Author: Tommi <tommi@webrtc.org>
Date: Thu Jun 01 14:08:52 2023

[M115] Move transceiver iteration loop over to the signaling thread.

This is required for ReportTransportStats since iterating over the
transceiver list from the network thread is not safe.

(cherry picked from commit dba22d31909298161318e00d43a80cdb0abc940f)

Bug: chromium:1446274, webrtc:12692
Change-Id: I7c514df9f029112c4b1da85826af91217850fb26
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/307340
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Cr-Original-Commit-Position: refs/heads/main@{#40197}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/308000
Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
Cr-Commit-Position: refs/branch-heads/5790@{#2}
Cr-Branched-From: 2eacbbc03a4a41ea658661225eb1c8fc07884c33-refs/heads/main@{#40122}

[modify] https://crrev.com/ba943f71e64a93558a51e75d18917f363b8672e9/pc/peer_connection_integrationtest.cc
[modify] https://crrev.com/ba943f71e64a93558a51e75d18917f363b8672e9/pc/peer_connection.h
[modify] https://crrev.com/ba943f71e64a93558a51e75d18917f363b8672e9/pc/peer_connection.cc


### [Deleted User] (2023-06-06)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-06-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-06)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/e46e37b6f831763aceaf5f5bd081a47cbd562890

commit e46e37b6f831763aceaf5f5bd081a47cbd562890
Author: Tommi <tommi@webrtc.org>
Date: Thu Jun 01 14:08:52 2023

[M114] Move transceiver iteration loop over to the signaling thread.

This is required for ReportTransportStats since iterating over the
transceiver list from the network thread is not safe.

(cherry picked from commit dba22d31909298161318e00d43a80cdb0abc940f)

No-Try: true
Bug: chromium:1446274, webrtc:12692
Change-Id: I7c514df9f029112c4b1da85826af91217850fb26
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/307340
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Cr-Original-Commit-Position: refs/heads/main@{#40197}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/308001
Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
Cr-Commit-Position: refs/branch-heads/5735@{#3}
Cr-Branched-From: df7df199abd619e75b9f1d9a7e12fc3f3f748775-refs/heads/main@{#39949}

[modify] https://crrev.com/e46e37b6f831763aceaf5f5bd081a47cbd562890/pc/peer_connection_integrationtest.cc
[modify] https://crrev.com/e46e37b6f831763aceaf5f5bd081a47cbd562890/pc/peer_connection.h
[modify] https://crrev.com/e46e37b6f831763aceaf5f5bd081a47cbd562890/pc/peer_connection.cc


### to...@chromium.org (2023-06-06)

Replying to https://crbug.com/chromium/1446274#c8:

1. Yes (regressed and found in M114). M108 is not affected.
2. Assuming that M108 is the latest LTS milestone, then yes. https://crbug.com/chromium/1446274#c7 points out the details.

### to...@chromium.org (2023-06-06)

Sorry, that^^^ was a reply to https://crbug.com/chromium/1446274#c25.

### rz...@google.com (2023-06-06)

[Empty comment from Monorail migration]

### rz...@google.com (2023-06-06)

Not needed in 108, see https://crbug.com/chromium/1446274#c28

### rz...@google.com (2023-06-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations, asnine! The VRP Panel has decided to award you $3,000 for this report of a mildly mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1446274?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064615)*
