# Security: Heap-use-after-free in WebRTC

| Field | Value |
|-------|-------|
| **Issue ID** | [40053633](https://issues.chromium.org/issues/40053633) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | kk...@gmail.com |
| **Assignee** | hb...@chromium.org |
| **Created** | 2020-10-16 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.cc;drc=ca70ba3c2187f4cf18f4ce57d53723f99fd089da;l=706>

```
void PeerConnectionTracker::OnSuspend() {  
  DCHECK_CALLED_ON_VALID_THREAD(main_thread_);  
  for (auto it = peer_connection_local_id_map_.begin();           
       it != peer_connection_local_id_map_.end(); ++it) {  
    it->key->CloseClientPeerConnection();                          // \*\*\* 1 \*\*\*  
  }  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc;l=2043;drc=ca70ba3c2187f4cf18f4ce57d53723f99fd089da>

```
void RTCPeerConnectionHandler::CloseClientPeerConnection() {  
  DCHECK(task_runner_->RunsTasksInCurrentSequence());  
  if (!is_closed_)  
    client_->ClosePeerConnection();                                  // \*\*\* 2 \*\*\*  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc;drc=ca70ba3c2187f4cf18f4ce57d53723f99fd089da;bpv=1;bpt=1;l=3328>

```
void RTCPeerConnection::ClosePeerConnection() {  
  DCHECK(signaling_state_ !=  
         webrtc::PeerConnectionInterface::SignalingState::kClosed);  
  CloseInternal();                                                    // \*\*\* 3 \*\*\*  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc;drc=ca70ba3c2187f4cf18f4ce57d53723f99fd089da;l=3504>

```
void RTCPeerConnection::CloseInternal() {  
  DCHECK(signaling_state_ !=  
         webrtc::PeerConnectionInterface::SignalingState::kClosed);  
  peer_handler_->Stop();  
  closed_ = true;  
  
  ChangeIceConnectionState(  
      webrtc::PeerConnectionInterface::kIceConnectionClosed);  
  SetPeerConnectionState(  
      webrtc::PeerConnectionInterface::PeerConnectionState::kClosed);  
  ChangeSignalingState(webrtc::PeerConnectionInterface::SignalingState::kClosed,  
                       false);  
  for (auto& transceiver : transceivers_) {  
    transceiver->OnPeerConnectionClosed();                          // \*\*\* 4 \*\*\*  
  }  
  if (sctp_transport_) {  
    sctp_transport_->Close();                                       // \*\*\* 5 \*\*\*  
  }  
  for (auto& dtls_transport_iter : dtls_transports_by_native_transport_) {  
    dtls_transport_iter.value->Close();  
  }  
  
  feature_handle_for_scheduler_.reset();  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc;l=1105;drc=ca70ba3c2187f4cf18f4ce57d53723f99fd089da;bpv=1;bpt=1>

```
bool RTCPeerConnectionHandler::Initialize(  
    const webrtc::PeerConnectionInterface::RTCConfiguration&  
        server_configuration,  
    const MediaConstraints& options,  
    WebLocalFrame\* frame) {  
  ...   
  
  if (peer_connection_tracker_) {  
    peer_connection_tracker_->RegisterPeerConnection(this, configuration_,   // \*\*\* 6 \*\*\*  
                                                     options, frame_);  
  }  
  
  return true;  
}  
  

```

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.cc;drc=ca70ba3c2187f4cf18f4ce57d53723f99fd089da;bpv=1;bpt=1;l=774>

```
void PeerConnectionTracker::RegisterPeerConnection(  
    RTCPeerConnectionHandler\* pc_handler,  
    const webrtc::PeerConnectionInterface::RTCConfiguration& config,  
    const MediaConstraints& constraints,  
    const blink::WebLocalFrame\* frame) {  
  
  ...  
  
  peer_connection_local_id_map_.insert(pc_handler, lid);                 // \*\*\* 7 \*\*\*  
  
  if (current_thermal_state_ !=  
      base::PowerObserver::DeviceThermalState::kUnknown) {  
    pc_handler->OnThermalStateChange(current_thermal_state_);  
  }  
}  

```

`PeerConnectionTracker::OnSuspend` is a method which is called when user's PC goes to sleep.  

`PeerConnectionTracker::OnSuspend` iterates through the elements of the `peer_connection_local_id_map_`  

container and calls `RTCPeerConnectionHandler::CloseClientPeerConnection` [1].  

`RTCPeerConnectionHandler::CloseClientPeerConnection` directly calls `RTCPeerConnection::ClosePeerConnection` [2].  

`RTCPeerConnection::ClosePeerConnection` finally calls `RTCPeerConnection::CloseInternal` which can call user defined JavaScript callback [4, 5].

If the attacker modifies (especially inserts elements into) `peer_connection_local_id_map_` from inside of user defined JavaScript callback [4, 5],  

the iterator will become invalid. In JavaScript `new PeerConnection()` will instantiate `RTCPeerConnection` and `RTCPeerConnectionHandler`.  

While instantiating `RTCPeerConnectionHandler`, `RTCPeerConnectionHandler::Initialize` is called and it will call `PeerConnectionTracker::RegisterPeerConnection` [6].  

In `PeerConnectionTracker::RegisterPeerConnection`, the attacker can insert new elements into `peer_connection_local_id_map_` container [7].

Because of the user defined JavaScript callback, the attack can stably allocate some objects into freed area.  

So I guess this vulnerability is exploitable.

I suggest the patch of this vulnerability. Please check the attachment.

**VERSION**  

Chrome Version: stable / master  

Operating System: Windows, MacOS and Linux

**REPRODUCTION CASE**

\*\*\* You have to sleep your PC or laptop after visiting page. And wake up! \*\*\*  

Please see the attachment.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==5072==ERROR: AddressSanitizer: heap-use-after-free on address 0x010d41b2b290 at pc 0x07feabe786c6 bp 0x0000009fe2a0 sp 0x0000009fe2e8  

READ of size 8 at 0x010d41b2b290 thread T0  

==5072==WARNING: Failed to use and restart external symbolizer!  

==5072==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==5072==\*\*\* Most likely this means that the app is already \*\*\*  

==5072==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==5072==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==5072==\*\*\* or produce wrong results. \*\*\*  

#0 0x7feabe786c5 in blink::PeerConnectionTracker::OnSuspend C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\peer\_connection\_tracker.cc:709  

#1 0x7fe9d55855f in blink::mojom::blink::PeerConnectionManagerStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\public\mojom\peerconnection\peer\_connection\_tracker.mojom-blink.cc:338  

#2 0x7fe9ead3f25 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:554  

#3 0x7fea103860e in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:41  

#4 0x7fe9eae5a8a in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:955  

#5 0x7fe9eae4a36 in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:622  

#6 0x7fea103860e in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:41  

#7 0x7fe9eaced04 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:510  

#8 0x7fe9ead0988 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:568  

#9 0x7fe9eb1d7c5 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:274  

#10 0x7fe9e6b69d9 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:163  

#11 0x7fea0bd1a5e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:332  

#12 0x7fea0bd116a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:252  

#13 0x7fea0b99493 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#14 0x7fea0bd3173 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:446  

#15 0x7fe9e669aa1 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:124  

#16 0x7fea09cebd9 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:256  

#17 0x7fe9e454ed7 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:860  

#18 0x7fe9e451d6c in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:373  

#19 0x7fe9e452363 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:399  

#20 0x7fe9531143d in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:130  

#21 0x13ff55b76 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#22 0x13ff52a46 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:339  

#23 0x14032d7bf in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#24 0x7772556c in BaseThreadInitThunk+0xc (C:\Windows\system32\kernel32.dll+0x78d3556c)  

#25 0x7788372c in RtlUserThreadStart+0x1c (C:\Windows\SYSTEM32\ntdll.dll+0x78ea372c)

0x010d41b2b290 is located 16 bytes inside of 64-byte region [0x010d41b2b280,0x010d41b2b2c0)  

freed by thread T0 here:  

#0 0x13fff5074 in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7fe9d70730d in WTF::HashTable<blink::FrameOrWorkerScheduler::Observer \*,WTF::KeyValuePair<blink::FrameOrWorkerScheduler::Observer \*,blink::FrameOrWorkerScheduler::ObserverType>,WTF::KeyValuePairKeyExtractor,WTF::PtrHash[blink::FrameOrWorkerScheduler::Observer](javascript:void(0);),WTF::HashMapValueTraits<WTF::HashTraits<blink::FrameOrWorkerScheduler::Observer \*>,WTF::HashTraits[blink::FrameOrWorkerScheduler::ObserverType](javascript:void(0);) >,WTF::HashTraits<blink::FrameOrWorkerScheduler::Observer \*>,WTF::PartitionAllocator>::RehashTo C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\wtf\hash\_table.h:1855  

#2 0x7feabe99710 in WTF::HashTable<blink::RTCPeerConnectionHandler \*,WTF::KeyValuePair<blink::RTCPeerConnectionHandler \*,int>,WTF::KeyValuePairKeyExtractor,WTF::PtrHash[blink::RTCPeerConnectionHandler](javascript:void(0);),WTF::HashMapValueTraits<WTF::HashTraits<blink::RTCPeerConnectionHandler \*>,WTF::HashTraits<int> >,WTF::HashTraits<blink::RTCPeerConnectionHandler \*>,WTF::PartitionAllocator>::Expand C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\wtf\hash\_table.h:1744  

#3 0x7feabe993aa in WTF::HashTable<blink::RTCPeerConnectionHandler \*,WTF::KeyValuePair<blink::RTCPeerConnectionHandler \*,int>,WTF::KeyValuePairKeyExtractor,WTF::PtrHash[blink::RTCPeerConnectionHandler](javascript:void(0);),WTF::HashMapValueTraits<WTF::HashTraits<blink::RTCPeerConnectionHandler \*>,WTF::HashTraits<int> >,WTF::HashTraits<blink::RTCPeerConnectionHandler \*>,WTF::PartitionAllocator>::insert<WTF::HashMapTranslator<WTF::HashMapValueTraits<WTF::HashTraits<blink::RTCPeerConnectionHandler \*>,WTF::HashTraits<int> >,WTF::PtrHash[blink::RTCPeerConnectionHandler](javascript:void(0);),WTF::PartitionAllocator>,blink::RTCPeerConnectionHandler \*&,int &> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\wtf\hash\_table.h:1393  

#4 0x7feabe7ae16 in blink::PeerConnectionTracker::RegisterPeerConnection C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\peer\_connection\_tracker.cc:797  

#5 0x7feaccd76a3 in blink::RTCPeerConnectionHandler::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\rtc\_peer\_connection\_handler.cc:1151  

#6 0x7feaed99ec2 in blink::RTCPeerConnection::RTCPeerConnection C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\rtc\_peer\_connection.cc:809  

#7 0x7feaedc62ad in blink::MakeGarbageCollectedTrait[blink::RTCPeerConnection](javascript:void(0);)::Call<blink::ExecutionContext \*&,webrtc::PeerConnectionInterface::RTCConfiguration,bool,bool,bool,blink::MediaConstraints &,blink::ExceptionState &> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\heap\heap.h:545  

#8 0x7feaed943a3 in blink::RTCPeerConnection::Create C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\rtc\_peer\_connection.cc:701  

#9 0x7feaed99249 in blink::RTCPeerConnection::Create C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\rtc\_peer\_connection.cc:739  

#10 0x7feae3bea99 in blink::`anonymous namespace'::ConstructorCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_rtc_peer_connection.cc:658 #11 0x7fe9ae91a69 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:158 #12 0x7fe9ae8dba6 in v8::internal::`anonymous namespace'::HandleApiCallHelper<1> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:111  

#13 0x7fe9ae8c1ae in v8::internal::Builtin\_Impl\_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:137  

#14 0x7fe9ae8b57e in v8::internal::Builtin\_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:129  

#15 0x7fe9d26441b in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit+0x3b (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187f5441b)  

#16 0x7fe9d1f280d in Builtins\_JSBuiltinsConstructStub+0xed (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187ee280d)  

#17 0x7fe9d2f5f9e in Builtins\_ConstructHandler+0x2be (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187fe5f9e)  

#18 0x7fe9d1f5a17 in Builtins\_InterpreterEntryTrampoline+0xd7 (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187ee5a17)  

#19 0x7fe9d1f351a in Builtins\_JSEntryTrampoline+0x5a (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187ee351a)  

#20 0x7fe9d1f310b in Builtins\_JSEntry+0xcb (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187ee310b)  

#21 0x7fe9b19ccfb in v8::internal::`anonymous namespace'::Invoke C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:368  

#22 0x7fe9b19ba4d in v8::internal::Execution::Call C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:462  

#23 0x7fe9ad5a87c in v8::Function::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:5009  

#24 0x7fea2fbeab3 in blink::V8ScriptRunner::CallFunction C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\v8\_script\_runner.cc:629  

#25 0x7fea8f1c3b3 in blink::bindings::CallbackInvokeHelper[blink::CallbackFunctionBase,blink::bindings::CallbackInvokeHelperMode::kLegacyTreatNonObjectAsNull](javascript:void(0);)::Call C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\callback\_invoke\_helper.cc:129  

#26 0x7feaa315471 in blink::V8EventHandlerNonNull::InvokeWithoutRunnabilityCheck C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\renderer\bindings\core\v8\v8\_event\_handler\_non\_null.cc:178  

#27 0x7fea6f84775 in blink::JSEventHandler::InvokeInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\js\_event\_handler.cc:124  

#28 0x7fea6ad23b9 in blink::JSBasedEventListener::Invoke C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\js\_based\_event\_listener.cc:150

previously allocated by thread T0 here:  

#0 0x13fff5174 in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7fe9f9cebdd in WTF::Partitions::BufferMalloc C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\wtf\allocator\partitions.cc:226  

#2 0x7feabe996e6 in WTF::HashTable<blink::RTCPeerConnectionHandler \*,WTF::KeyValuePair<blink::RTCPeerConnectionHandler \*,int>,WTF::KeyValuePairKeyExtractor,WTF::PtrHash[blink::RTCPeerConnectionHandler](javascript:void(0);),WTF::HashMapValueTraits<WTF::HashTraits<blink::RTCPeerConnectionHandler \*>,WTF::HashTraits<int> >,WTF::HashTraits<blink::RTCPeerConnectionHandler \*>,WTF::PartitionAllocator>::Expand C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\wtf\hash\_table.h:1744  

#3 0x7feabe993aa in WTF::HashTable<blink::RTCPeerConnectionHandler \*,WTF::KeyValuePair<blink::RTCPeerConnectionHandler \*,int>,WTF::KeyValuePairKeyExtractor,WTF::PtrHash[blink::RTCPeerConnectionHandler](javascript:void(0);),WTF::HashMapValueTraits<WTF::HashTraits<blink::RTCPeerConnectionHandler \*>,WTF::HashTraits<int> >,WTF::HashTraits<blink::RTCPeerConnectionHandler \*>,WTF::PartitionAllocator>::insert<WTF::HashMapTranslator<WTF::HashMapValueTraits<WTF::HashTraits<blink::RTCPeerConnectionHandler \*>,WTF::HashTraits<int> >,WTF::PtrHash[blink::RTCPeerConnectionHandler](javascript:void(0);),WTF::PartitionAllocator>,blink::RTCPeerConnectionHandler \*&,int &> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\wtf\hash\_table.h:1393  

#4 0x7feabe7ae16 in blink::PeerConnectionTracker::RegisterPeerConnection C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\peer\_connection\_tracker.cc:797  

#5 0x7feaccd76a3 in blink::RTCPeerConnectionHandler::Initialize C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\rtc\_peer\_connection\_handler.cc:1151  

#6 0x7feaed99ec2 in blink::RTCPeerConnection::RTCPeerConnection C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\rtc\_peer\_connection.cc:809  

#7 0x7feaedc62ad in blink::MakeGarbageCollectedTrait[blink::RTCPeerConnection](javascript:void(0);)::Call<blink::ExecutionContext \*&,webrtc::PeerConnectionInterface::RTCConfiguration,bool,bool,bool,blink::MediaConstraints &,blink::ExceptionState &> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\heap\heap.h:545  

#8 0x7feaed943a3 in blink::RTCPeerConnection::Create C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\rtc\_peer\_connection.cc:701  

#9 0x7feaed99249 in blink::RTCPeerConnection::Create C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\rtc\_peer\_connection.cc:739  

#10 0x7feae3bea99 in blink::`anonymous namespace'::ConstructorCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_rtc_peer_connection.cc:658 #11 0x7fe9ae91a69 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:158 #12 0x7fe9ae8dba6 in v8::internal::`anonymous namespace'::HandleApiCallHelper<1> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:111  

#13 0x7fe9ae8c1ae in v8::internal::Builtin\_Impl\_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:137  

#14 0x7fe9ae8b57e in v8::internal::Builtin\_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:129  

#15 0x7fe9d26441b in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit+0x3b (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187f5441b)  

#16 0x7fe9d1f280d in Builtins\_JSBuiltinsConstructStub+0xed (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187ee280d)  

#17 0x7fe9d2f5f9e in Builtins\_ConstructHandler+0x2be (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187fe5f9e)  

#18 0x7fe9d1f5a17 in Builtins\_InterpreterEntryTrampoline+0xd7 (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187ee5a17)  

#19 0x7fe9d1f5a17 in Builtins\_InterpreterEntryTrampoline+0xd7 (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187ee5a17)  

#20 0x7fe9d1f351a in Builtins\_JSEntryTrampoline+0x5a (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187ee351a)  

#21 0x7fe9d1f310b in Builtins\_JSEntry+0xcb (C:\Users\usr\Desktop\win32-release\_x64\_asan-win32-release\_x64-817308\asan-win32-release\_x64-817308\chrome.dll+0x187ee310b)  

#22 0x7fe9b19ccfb in v8::internal::`anonymous namespace'::Invoke C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:368  

#23 0x7fe9b19ba4d in v8::internal::Execution::Call C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:462  

#24 0x7fe9ad5a87c in v8::Function::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:5009  

#25 0x7fea2fbeab3 in blink::V8ScriptRunner::CallFunction C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\v8\_script\_runner.cc:629  

#26 0x7fea8f1c3b3 in blink::bindings::CallbackInvokeHelper[blink::CallbackFunctionBase,blink::bindings::CallbackInvokeHelperMode::kLegacyTreatNonObjectAsNull](javascript:void(0);)::Call C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\callback\_invoke\_helper.cc:129  

#27 0x7feaa315471 in blink::V8EventHandlerNonNull::InvokeWithoutRunnabilityCheck C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\renderer\bindings\core\v8\v8\_event\_handler\_non\_null.cc:178  

#28 0x7fea6f84775 in blink::JSEventHandler::InvokeInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\js\_event\_handler.cc:124

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\peerconnection\peer\_connection\_tracker.cc:709 in blink::PeerConnectionTracker::OnSuspend  

Shadow bytes around the buggy address:  

0x0022e9de5600: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 00  

0x0022e9de5610: fa fa fa fa 00 00 00 00 00 00 00 00 fa fa fa fa  

0x0022e9de5620: 00 00 00 00 00 00 00 00 fa fa fa fa 00 00 00 00  

0x0022e9de5630: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 00  

0x0022e9de5640: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

=>0x0022e9de5650: fd fd[fd]fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x0022e9de5660: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x0022e9de5670: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa  

0x0022e9de5680: fd fd fd fd fd fd fd fd fa fa fa fa 00 00 00 00  

0x0022e9de5690: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 00  

0x0022e9de56a0: fa fa fa fa 00 00 00 00 00 00 00 00 fa fa fa fa  

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

==5072==ABORTING

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### bd...@chromium.org (2020-10-16)

Assigning to guidou@, feel free to suggest someone else who can work on fixing this security bug.
Marking as Security_Impact-Stable as this might have been this way for awhile.



[Monorail components: Blink>WebRTC]

### [Deleted User] (2020-10-16)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kk...@gmail.com (2020-10-19)

I attached an example to control register. (Windows)


======= WINDBG LOG ==========

          000007fe`dd756f2a 4839fb          cmp     rbx,rdi
          000007fe`dd756f2d 7448            je      chrome!blink::PeerConnectionTracker::OnSuspend+0x97 (000007fe`dd756f77)
          000007fe`dd756f2f 488b0b          mov     rcx,qword ptr [rbx]
          000007fe`dd756f32 488b01          mov     rax,qword ptr [rcx] ds:41414141`41414141=????????????????
          000007fe`dd756f35 ff9008010000    call    qword ptr [rax+108h]
          000007fe`dd756f3b 4889d8          mov     rax,rbx
          000007fe`dd756f3e 4883c010        add     rax,10h
          000007fe`dd756f42 4889fb          mov     rbx,rdi
          000007fe`dd756f45 4839f8          cmp     rax,rdi

==================

### gu...@chromium.org (2020-10-19)

[Empty comment from Monorail migration]

### hb...@chromium.org (2020-10-19)

Thank you for an excellent bug description, this looks like a real problem. One way to mitigate this might be to copy the map before iterating so that we do not have an iterator that gets invalidated.

This means that it would be possible to create a peer connection inside of a callback from a suspended event and it would not get closed... trying to think if this could be an issue or not? Considering this level of "suspension" does not correspond to JavaScript actually suspending, this would be the same as if a peer connection was created after the suspension for other reasons (such as having code running every second that ensures there exists a non-closed peer connection). Because JavaScript is still alive after this suspension event and already allows creating non-closed PCs in such a scenario, I do not think it is important that a peer connection created in a callback gets closed, and it is OK to only close the PCs that existed at the time of the suspension event.

I think having PCs alive after suspension, or getUserMedia() track for that matter, are issues worth discussing on their own, but tangental to this security issue. Here we should just avoid the heap-use-after-free.

### kk...@gmail.com (2020-10-21)

On Windows 10 32bit, I successfully controlled EIP, EAX, ECX registers. I attached a PoC code, please check it out.

======== WINDBG LOG ==========

0:000> r
eax=51515151 ebx=04a0c8b0 ecx=41414141 edx=00000000 esi=00ea21e8 edi=04a0c8c0
eip=51515151 esp=0077f4d4 ebp=0077f4ec iopl=0         nv up ei ng nz na po cy
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00210283
51515151 51              push    ecx

0:000> kb
 # ChildEBP RetAddr  Args to Child              
WARNING: Frame IP not in any known module. Following frames may be wrong.
00 0077f4d0 153573b6 04a0c880 00000008 00ea21e8 0x51515151
01 0077f4ec 11b31153 00000000 00000000 00000000 chrome!blink::PeerConnectionTracker::OnSuspend+0x66 [c:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\peer_connection_tracker.cc @ 707] 
02 0077f530 1535e453 00ea21e8 0077f594 0077f580 chrome!blink::mojom::blink::PeerConnectionManagerStubDispatch::Accept+0x63 [c:\b\s\w\ir\cache\builder\src\out\Release\gen\third_party\blink\public\mojom\peerconnection\peer_connection_tracker.mojom-blink.cc @ 338] 
03 0077f540 0f935c31 0077f594 00000006 00000000 chrome!blink::mojom::blink::PeerConnectionManagerStub<mojo::RawPtrImplRefTraits<blink::mojom::blink::PeerConnectionManager> >::Accept+0x13 [c:\b\s\w\ir\cache\builder\src\out\Release\gen\third_party\blink\public\mojom\peerconnection\peer_connection_tracker.mojom-blink.h @ 291] 
04 0077f580 0f935258 0077f594 00e5e1a0 00000000 chrome!mojo::InterfaceEndpointClient::HandleValidatedMessage+0x201 [c:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 554] 
05 0077f5e0 0f934b93 0077f60c 00000002 00e08e38 chrome!mojo::internal::MultiplexRouter::ProcessIncomingMessage+0x248 [c:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc @ 952] 
06 0077f65c 0f9344f1 0077f6cc 0077f680 000064df chrome!mojo::internal::MultiplexRouter::Accept+0xb3 [c:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc @ 624] 
07 0077f6c4 0f932c52 00000000 00000000 00000000 chrome!mojo::Connector::DispatchMessageW+0xf1 [c:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc @ 508] 
08 0077f778 0f932abf 0077f78c 0fe9ba0f 00000000 chrome!mojo::Connector::ReadAllAvailableMessages+0x82 [c:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc @ 567] 
09 (Inline) -------- -------- -------- -------- chrome!mojo::Connector::OnHandleReadyInternal+0x9 [c:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc @ 408] 
0a 0077f780 0fe9ba0f 00000000 0077f79c 0f932a9f chrome!mojo::Connector::OnWatcherHandleReady+0xf [c:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc @ 380] 
0b (Inline) -------- -------- -------- -------- chrome!base::internal::FunctorTraits<void (chrome::mojom::ChromeRenderFrame_GetMediaFeedURL_ProxyToResponder::*)(const base::Optional<GURL> &) __attribute__((thiscall)),void>::Invoke+0x9 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 498] 
0c (Inline) -------- -------- -------- -------- chrome!base::internal::InvokeHelper<0,void>::MakeItSo+0x9 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 637] 
0d (Inline) -------- -------- -------- -------- chrome!base::internal::Invoker<base::internal::BindState<void (chrome::mojom::ChromeRenderFrame_GetMediaFeedURL_ProxyToResponder::*)(const base::Optional<GURL> &) __attribute__((thiscall)),std::__1::unique_ptr<chrome::mojom::ChromeRenderFrame_GetMediaFeedURL_ProxyToResponder,std::__1::default_delete<chrome::mojom::ChromeRenderFrame_GetMediaFeedURL_ProxyToResponder> > >,void (const base::Optional<GURL> &)>::RunImpl+0x9 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 710] 
0e 0077f78c 0f932a9f 00ec83c0 00000000 0077f7b0 chrome!base::internal::Invoker<base::internal::BindState<void (chrome::mojom::ChromeRenderFrame_GetMediaFeedURL_ProxyToResponder::*)(const base::Optional<GURL> &) __attribute__((thiscall)),std::__1::unique_ptr<chrome::mojom::ChromeRenderFrame_GetMediaFeedURL_ProxyToResponder,std::__1::default_delete<chrome::mojom::ChromeRenderFrame_GetMediaFeedURL_ProxyToResponder> > >,void (const base::Optional<GURL> &)>::RunOnce+0xf [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 683] 
0f (Inline) -------- -------- -------- -------- chrome!base::RepeatingCallback<void (unsigned int)>::Run+0x9 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 133] 
10 0077f79c 105cf863 00ec8374 00000000 07221fec chrome!mojo::SimpleWatcher::DiscardReadyState+0xf [c:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.h @ 194] 
11 (Inline) -------- -------- -------- -------- chrome!base::internal::FunctorTraits<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),void>::Invoke+0xa [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 393] 
12 (Inline) -------- -------- -------- -------- chrome!base::internal::InvokeHelper<0,void>::MakeItSo+0xa [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 637] 
13 (Inline) -------- -------- -------- -------- chrome!base::internal::Invoker<base::internal::BindState<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::RunImpl+0xa [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 710] 
14 0077f7b0 0f9328b2 00ec8360 00000000 07221fec chrome!base::internal::Invoker<base::internal::BindState<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run+0x13 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 692] 
15 (Inline) -------- -------- -------- -------- chrome!base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run+0x18 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 133] 
16 0077f828 10ab5821 00000001 00000000 07221fec chrome!mojo::SimpleWatcher::OnHandleReady+0x142 [c:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc @ 293] 
17 (Inline) -------- -------- -------- -------- chrome!base::internal::FunctorTraits<void (content::MediaWebContentsObserver::*)(content::RenderFrameHost *, int, const std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > &) __attribute__((thiscall)),void>::Invoke+0x1a [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 498] 
18 (Inline) -------- -------- -------- -------- chrome!base::internal::InvokeHelper<1,void>::MakeItSo+0x34 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 657] 
19 (Inline) -------- -------- -------- -------- chrome!base::internal::Invoker<base::internal::BindState<void (content::MediaWebContentsObserver::*)(content::RenderFrameHost *, int, const std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > &) __attribute__((thiscall)),base::WeakPtr<content::MediaWebContentsObserver>,content::RenderFrameHost *,int,std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > >,void ()>::RunImpl+0x34 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 710] 
1a 0077f84c 0f90ef84 07221fc8 29479b1d 00000000 chrome!base::internal::Invoker<base::internal::BindState<void (content::MediaWebContentsObserver::*)(content::RenderFrameHost *, int, const std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > &) __attribute__((thiscall)),base::WeakPtr<content::MediaWebContentsObserver>,content::RenderFrameHost *,int,std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > >,void ()>::RunOnce+0x41 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 683] 
1b (Inline) -------- -------- -------- -------- chrome!base::OnceCallback<void ()>::Run+0x10 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 99] 
1c 0077f8c0 1290f745 168be566 00ebbc58 2965fed4 chrome!base::TaskAnnotator::RunTask+0xe4 [c:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 142] 
1d 0077f978 1290f323 0077f9a0 0077f9a8 00ecc748 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x1b5 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 332] 
1e 0077f9dc 0f90ccd2 0077f9f8 01000000 00e086a8 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x63 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 254] 
1f 0077fa1c 0f90cb3e 00e22dc4 ffffffff 00000000 chrome!base::MessagePumpDefault::Run+0x52 [c:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc @ 41] 
20 0077fa58 0f90c581 00000001 ffffffff 7fffffff chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x6e [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 454] 
21 0077fab0 127f4b6e 0077fab8 00df2d00 032501d4 chrome!base::RunLoop::Run+0x81 [c:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 126] 
22 0077fb70 11f42925 0077fba8 0877fbbc 00df5238 chrome!content::RendererMain+0x2ae [c:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc @ 231] 
23 0077fb8c 0f8c67cd 0077fbbc 0077fba8 0077fd3c chrome!content::RunOtherNamedProcessTypeMain+0x185 [c:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 561] 
24 0077fbd8 0f8c66d3 00000000 00000003 0077fcd0 chrome!content::ContentMainRunnerImpl::Run+0xed [c:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 883] 
25 0077fbe8 0f8b7c50 00dda6b8 ffffffff 00000000 chrome!content::ContentServiceManagerMainDelegate::RunEmbedderProcess+0x13 [c:\b\s\w\ir\cache\builder\src\content\app\content_service_manager_main_delegate.cc @ 60] 
26 0077fcd0 0f8b7733 0077fcdc 0077fce0 16699a70 chrome!service_manager::Main+0x460 [c:\b\s\w\ir\cache\builder\src\services\service_manager\embedder\main.cc @ 453] 
27 0077fd10 0f8b4615 0077fd28 0077fd1c 00000000 chrome!content::ContentMain+0x33 [c:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 19] 
28 0077fd7c 00f420b4 00f40000 0077fda8 2711498e chrome!ChromeMain+0xf5 [c:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 122] 
29 0077fdcc 00f41642 00f40000 2711498e 00000000 chrome_exe!Ordinal0+0x20b4
2a 0077ff08 0105943a 00f40000 00000000 00dd1ca8 chrome_exe!Ordinal0+0x1642
2b 0077ff54 76c8cec9 004bb000 76c8ceb0 0077ffc0 chrome_exe!GetHandleVerifier+0xc936a
2c 0077ff64 77915fcd 004bb000 2ef13d62 00000000 KERNEL32!BaseThreadInitThunk+0x19
2d 0077ffc0 77915fa1 ffffffff 779548bd 00000000 ntdll!EtwProcessPrivateLoggerRequest+0xd8d
2e 0077ffd0 00000000 010594c0 004bb000 00000000 ntdll!EtwProcessPrivateLoggerRequest+0xd61

=================================================================================


### hb...@chromium.org (2020-10-21)

Scary stuff, let's fix this!

### hb...@chromium.org (2020-10-21)

Fix under review here: https://chromium-review.googlesource.com/c/chromium/src/+/2489302

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f3322ca65051888a966733e2fc56fc44021bcea3

commit f3322ca65051888a966733e2fc56fc44021bcea3
Author: Henrik Boström <hbos@chromium.org>
Date: Wed Oct 21 21:59:23 2020

[PeerConnection] Fix possible crash in tracker's OnSuspend.

This can happen if peer connections are created or garbage collected
inside of JavaScript event listeners triggered by OnSuspend which
closes peer connections.

Bug: chromium:1139153
Change-Id: I3d36c418f2f1a1e41886ff22901feeaaaee28029
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2489302
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Henrik Boström <hbos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#819533}

[modify] https://crrev.com/f3322ca65051888a966733e2fc56fc44021bcea3/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.cc


### hb...@chromium.org (2020-10-22)

It's fixed! It would be nice if you could Verify this, kkwondotnet@, but at the time of writing there has not been a new Canary cut with it yet. Release status:
https://chromiumdash.appspot.com/commit/f3322ca65051888a966733e2fc56fc44021bcea3

Let's check back tomorrow.

### [Deleted User] (2020-10-22)

[Empty comment from Monorail migration]

### kk...@gmail.com (2020-10-23)

Thank you for the nice bug fix! I checked that commit. I think that there is no problem.

### hb...@chromium.org (2020-10-23)

Thanks! I think it makes sense to backmerge this to M87 on all chromium platforms.

Requesting to merge https://crbug.com/chromium/1139153#c9. This is a third_party/webrtc CL.

### hb...@chromium.org (2020-10-23)

Sorry, correction, this is a chromium CL.

### [Deleted User] (2020-10-23)

This bug requires manual review: M87's targeted beta branch promotion date has already passed, so this requires manual review
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

### hb...@chromium.org (2020-10-23)

1. I'll let chrome-security@google.com decide but this is a security issue with heap-use-after-free. https://crbug.com/chromium/1139153#c6 illustrates how to exploit this.
2. https://chromium.googlesource.com/chromium/src.git/+/f3322ca65051888a966733e2fc56fc44021bcea3
3. Yes.
4. The security vulnerability has been there for a long time, it should also in current Stable (M86). I'll let chrome-security decide the severity and if we want to merge into M86 as well.
5. It's a security fix.
6. No.
7. N/A

### la...@google.com (2020-10-23)

adetaylor@ - WDYT on taking this for M87

### ad...@chromium.org (2020-10-23)

As this is an externally-reported medium severity bug our normal practice is to merge back to M87. (I believe bdea@ decided this was only Medium severity because of the need to sleep/wake the PC, otherwise this would be High and we'd be merging back to M86 as well). The fix looks self-explanatory and straightforward so I'm approving merge to M87, branch 4280.

### ad...@google.com (2020-10-26)

[Empty comment from Monorail migration]

### hb...@chromium.org (2020-10-26)

Backmerging here: https://chromium-review.googlesource.com/c/chromium/src/+/2498568

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b631b3e3b31f16f0e54b7f5fff3de979e48ae16e

commit b631b3e3b31f16f0e54b7f5fff3de979e48ae16e
Author: Henrik Boström <hbos@chromium.org>
Date: Mon Oct 26 16:28:08 2020

[M87] [PeerConnection] Fix possible crash in tracker's OnSuspend.

This can happen if peer connections are created or garbage collected
inside of JavaScript event listeners triggered by OnSuspend which
closes peer connections.

(cherry picked from commit f3322ca65051888a966733e2fc56fc44021bcea3)

Bug: chromium:1139153
Change-Id: I3d36c418f2f1a1e41886ff22901feeaaaee28029
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2489302
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Henrik Boström <hbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#819533}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2498568
Reviewed-by: Henrik Boström <hbos@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#764}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/b631b3e3b31f16f0e54b7f5fff3de979e48ae16e/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.cc


### ad...@google.com (2020-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-28)

Congratulations, the VRP panel has decided to award $7,500 for this bug. Someone from our finance team will be in touch to arrange payment. Thank you for all the analysis. How would you like to be credited in the Chrome release notes?

### kk...@gmail.com (2020-10-29)

Jong-Gwon Kim (kkwon)
And thank you for reward!

### ad...@chromium.org (2020-10-29)

Thank YOU for the report :)

### ad...@google.com (2020-10-29)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### ke...@google.com (2020-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/145c9ccd2c4ff4cb72d3b8f14a09240e5de254be

commit 145c9ccd2c4ff4cb72d3b8f14a09240e5de254be
Author: Henrik Boström <hbos@chromium.org>
Date: Wed Dec 16 18:40:59 2020

[PeerConnection] Fix possible crash in tracker's OnSuspend.

This can happen if peer connections are created or garbage collected
inside of JavaScript event listeners triggered by OnSuspend which
closes peer connections.

(cherry picked from commit f3322ca65051888a966733e2fc56fc44021bcea3)

Bug: chromium:1139153
Change-Id: I3d36c418f2f1a1e41886ff22901feeaaaee28029
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2489302
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Henrik Boström <hbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#819533}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587055
Reviewed-by: Henrik Boström <hbos@chromium.org>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1487}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/145c9ccd2c4ff4cb72d3b8f14a09240e5de254be/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.cc


### [Deleted User] (2020-12-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1139153?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053633)*
