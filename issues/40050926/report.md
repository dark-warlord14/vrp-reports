# Security: heap-buffer-overflow in blink::FFTFrame::DoFFT

| Field | Value |
|-------|-------|
| **Issue ID** | [40050926](https://issues.chromium.org/issues/40050926) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2019-12-09 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of content\_shell.

**VERSION**  

Chrome Version: asan-linux-release-722857  

Operating System: Linux 64bit

**REPRODUCTION CASE**

<script>
o79=new AudioContext({latencyHint:'interactive',sampleRate:4510});
o129=o79.createPanner();
o129.panningModel='HRTF';
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

# Crash State:

==10724==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60d0000402f0 at pc 0x562d09c02e3d bp 0x7fcb40887ab0 sp 0x7fcb40887aa8  

READ of size 16 at 0x60d0000402f0 thread T13 (HRTF database l)  

#0 0x562d09c02e3c in radf4\_ps third\_party/pffft/src/pffft.c:624:35  

#1 0x562d09bfd60d in rfftf1\_ps third\_party/pffft/src/pffft.c:977:9  

#2 0x562d09bfcd6c in pffft\_transform\_internal third\_party/pffft/src/pffft.c:1622:13  

#3 0x562d10f615d7 in blink::FFTFrame::DoFFT(float const\*) third\_party/blink/renderer/platform/audio/pffft/fft\_frame\_pffft.cc:164:3  

#4 0x562d10f5e2f6 in ExtractAverageGroupDelay third\_party/blink/renderer/platform/audio/hrtf\_kernel.cc:58:20  

#5 0x562d10f5e2f6 in blink::HRTFKernel::HRTFKernel(blink::AudioChannel\*, unsigned long, float) third\_party/blink/renderer/platform/audio/hrtf\_kernel.cc:74:18  

#6 0x562d10f5998c in make\_unique<blink::HRTFKernel, blink::AudioChannel \*&, const unsigned long &, float &> buildtools/third\_party/libc++/trunk/include/memory:3043:32  

#7 0x562d10f5998c in blink::HRTFElevation::CalculateKernelsForAzimuthElevation(int, int, float, int, std::\_\_1::unique\_ptr<blink::HRTFKernel, std::\_\_1::default\_delete[blink::HRTFKernel](javascript:void(0);) >&, std::\_\_1::unique\_ptr<blink::HRTFKernel, std::\_\_1::default\_delete[blink::HRTFKernel](javascript:void(0);) >&) third\_party/blink/renderer/platform/audio/hrtf\_elevation.cc:165:14  

#8 0x562d10f5a928 in blink::HRTFElevation::CreateForSubject(int, int, float) third\_party/blink/renderer/platform/audio/hrtf\_elevation.cc:226:20  

#9 0x562d10f5829c in blink::HRTFDatabase::HRTFDatabase(float) third\_party/blink/renderer/platform/audio/hrtf\_database.cc:55:9  

#10 0x562d10f5644f in make\_unique<blink::HRTFDatabase, float &> buildtools/third\_party/libc++/trunk/include/memory:3043:32  

#11 0x562d10f5644f in blink::HRTFDatabaseLoader::LoadTask() third\_party/blink/renderer/platform/audio/hrtf\_database\_loader.cc:83:20  

#12 0x562d04dc21a2 in Run base/callback.h:98:12  

#13 0x562d04dc21a2 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:142:33  

#14 0x562d04dfa5f8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:365:23  

#15 0x562d04df9f79 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219:7  

#16 0x562d04d21c00 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:55  

#17 0x562d04dfc39e in Run base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:12  

#18 0x562d04dfc39e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#19 0x562d04d7fde1 in base::RunLoop::Run() base/run\_loop.cc:156:14  

#20 0x562d02356db5 in blink::scheduler::WorkerThread::SimpleThreadImpl::Run() third\_party/blink/renderer/platform/scheduler/worker/worker\_thread.cc:169:14  

#21 0x562d04f10111 in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:81:13  

#22 0x7fcb610396da in start\_thread (/lib/x86\_64-linux-gnu/libpthread.so.0+0x76da)

0x60d0000402f8 is located 0 bytes to the right of 136-byte region [0x60d000040270,0x60d0000402f8)  

allocated by thread T13 (HRTF database l) here:  

#0 0x562cfd1ad602 in \_\_interceptor\_calloc /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:154:3  

#1 0x562d09cadbf2 in PartitionAllocGenericFlags base/allocator/partition\_allocator/partition\_alloc.h:402:30  

#2 0x562d09cadbf2 in AllocFlags base/allocator/partition\_allocator/partition\_alloc.h:443:10  

#3 0x562d09cadbf2 in WTF::Partitions::FastZeroedMalloc(unsigned long, char const\*) third\_party/blink/renderer/platform/wtf/allocator/partitions.cc:236:33  

#4 0x562d0239f9e0 in blink::AudioArray<float>::Allocate(unsigned long) third\_party/blink/renderer/platform/audio/audio\_array.h:83:39  

#5 0x562d0ae31538 in AudioArray third\_party/blink/renderer/platform/audio/audio\_array.h:50:5  

#6 0x562d0ae31538 in make\_unique<blink::AudioArray<float>, unsigned long &> buildtools/third\_party/libc++/trunk/include/memory:3043:32  

#7 0x562d0ae31538 in AudioChannel third\_party/blink/renderer/platform/audio/audio\_channel.h:58:19  

#8 0x562d0ae31538 in make\_unique<blink::AudioChannel, unsigned int &> buildtools/third\_party/libc++/trunk/include/memory:3043:32  

#9 0x562d0ae31538 in blink::AudioBus::AudioBus(unsigned int, unsigned int, bool) third\_party/blink/renderer/platform/audio/audio\_bus.cc:69:20  

#10 0x562d0ae3ba22 in Create third\_party/blink/renderer/platform/audio/audio\_bus.cc:60:29  

#11 0x562d0ae3ba22 in blink::AudioBus::CreateBySampleRateConverting(blink::AudioBus const\*, bool, double) third\_party/blink/renderer/platform/audio/audio\_bus.cc:624:7  

#12 0x562d10f59665 in blink::HRTFElevation::CalculateKernelsForAzimuthElevation(int, int, float, int, std::\_\_1::unique\_ptr<blink::HRTFKernel, std::\_\_1::default\_delete[blink::HRTFKernel](javascript:void(0);) >&, std::\_\_1::unique\_ptr<blink::HRTFKernel, std::\_\_1::default\_delete[blink::HRTFKernel](javascript:void(0);) >&) third\_party/blink/renderer/platform/audio/hrtf\_elevation.cc:155:36  

#13 0x562d10f5a928 in blink::HRTFElevation::CreateForSubject(int, int, float) third\_party/blink/renderer/platform/audio/hrtf\_elevation.cc:226:20  

#14 0x562d10f5829c in blink::HRTFDatabase::HRTFDatabase(float) third\_party/blink/renderer/platform/audio/hrtf\_database.cc:55:9  

#15 0x562d10f5644f in make\_unique<blink::HRTFDatabase, float &> buildtools/third\_party/libc++/trunk/include/memory:3043:32  

#16 0x562d10f5644f in blink::HRTFDatabaseLoader::LoadTask() third\_party/blink/renderer/platform/audio/hrtf\_database\_loader.cc:83:20  

#17 0x562d04dc21a2 in Run base/callback.h:98:12  

#18 0x562d04dc21a2 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:142:33  

#19 0x562d04dfa5f8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:365:23  

#20 0x562d04df9f79 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219:7  

#21 0x562d04d21c00 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:55  

#22 0x562d04dfc39e in Run base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:12  

#23 0x562d04dfc39e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#24 0x562d04d7fde1 in base::RunLoop::Run() base/run\_loop.cc:156:14  

#25 0x562d02356db5 in blink::scheduler::WorkerThread::SimpleThreadImpl::Run() third\_party/blink/renderer/platform/scheduler/worker/worker\_thread.cc:169:14  

#26 0x562d04f10111 in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:81:13  

#27 0x7fcb610396da in start\_thread (/lib/x86\_64-linux-gnu/libpthread.so.0+0x76da)

Thread T13 (HRTF database l) created by T0 (content\_shell) here:  

#0 0x562cfd197d1a in \_\_interceptor\_pthread\_create /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors.cpp:214:3  

#1 0x562d04f0f35e in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadPriority) base/threading/platform\_thread\_posix.cc:120:13  

#2 0x562d04e442a3 in base::SimpleThread::StartAsync() base/threading/simple\_thread.cc:51:13  

#3 0x562d02355315 in blink::scheduler::WorkerThread::Init() third\_party/blink/renderer/platform/scheduler/worker/worker\_thread.cc:61:12  

#4 0x562d022bd16a in blink::Thread::CreateThread(blink::ThreadCreationParams const&) third\_party/blink/renderer/platform/scheduler/common/thread.cc:82:11  

#5 0x562d0ab611b0 in blink::Platform::CreateThread(blink::ThreadCreationParams const&) third\_party/blink/renderer/platform/exported/platform.cc:302:10  

#6 0x562d10f55b47 in blink::HRTFDatabaseLoader::LoadAsynchronously() third\_party/blink/renderer/platform/audio/hrtf\_database\_loader.cc:97:34  

#7 0x562d10f557d9 in blink::HRTFDatabaseLoader::CreateAndLoadAsynchronouslyIfNecessary(float) third\_party/blink/renderer/platform/audio/hrtf\_database\_loader.cc:60:11  

#8 0x562d10f4fc9c in blink::AudioListener::CreateAndLoadHRTFDatabaseLoader(float) third\_party/blink/renderer/modules/webaudio/audio\_listener.cc:283:9  

#9 0x562d10eb750a in blink::PannerHandler::SetPanningModel(unsigned int) third\_party/blink/renderer/modules/webaudio/panner\_node.cc:389:17  

#10 0x562d10eb1738 in blink::PannerHandler::SetPanningModel(WTF::String const&) third\_party/blink/renderer/modules/webaudio/panner\_node.cc  

#11 0x562d10f2e2cd in PanningModelAttributeSetter gen/third\_party/blink/renderer/bindings/modules/v8/v8\_panner\_node.cc:120:9  

#12 0x562d10f2e2cd in blink::V8PannerNode::PanningModelAttributeSetterCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/modules/v8/v8\_panner\_node.cc:583:3  

#13 0x562d00077e09 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3  

#14 0x562d0007597b in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36  

#15 0x562d000742d7 in v8::internal::Builtins::InvokeApiFunction(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);)) v8/src/builtins/builtins-api.cc:227:16  

#16 0x562d00af23c3 in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::Maybe[v8::internal::ShouldThrow](javascript:void(0);)) v8/src/objects/objects.cc:1565:5  

#17 0x562d00afeedf in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::Maybe[v8::internal::ShouldThrow](javascript:void(0);), v8::internal::StoreOrigin, bool\*) v8/src/objects/objects.cc:2474:16  

#18 0x562d00afe5a8 in v8::internal::Object::SetProperty(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::StoreOrigin, v8::Maybe[v8::internal::ShouldThrow](javascript:void(0);)) v8/src/objects/objects.cc:2529:9  

#19 0x562d00f2e6d7 in v8::internal::Runtime::SetObjectProperty(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::StoreOrigin, v8::Maybe[v8::internal::ShouldThrow](javascript:void(0);)) v8/src/runtime/runtime-object.cc:430:3  

#20 0x562d00f3c50e in \_\_RT\_impl\_Runtime\_SetNamedProperty v8/src/runtime/runtime-object.cc:697:3  

#21 0x562d00f3c50e in v8::internal::Runtime\_SetNamedProperty(int, unsigned long\*, v8::internal::Isolate\*) v8/src/runtime/runtime-object.cc:689:1  

#22 0x562d020219b7 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit (/fuzzer3/dl/asan-linux-release-722857/content\_shell+0xb81a9b7)  

#23 0x562d02095f9f in Builtins\_StaNamedPropertyNoFeedbackHandler (/fuzzer3/dl/asan-linux-release-722857/content\_shell+0xb88ef9f)  

#24 0x562d01fab96a in Builtins\_InterpreterEntryTrampoline (/fuzzer3/dl/asan-linux-release-722857/content\_shell+0xb7a496a)  

#25 0x562d01fa9139 in Builtins\_JSEntryTrampoline (/fuzzer3/dl/asan-linux-release-722857/content\_shell+0xb7a2139)  

#26 0x562d01fa8f17 in Builtins\_JSEntry (/fuzzer3/dl/asan-linux-release-722857/content\_shell+0xb7a1f17)  

#27 0x562d002fea72 in Call v8/src/execution/simulator.h:142:12  

#28 0x562d002fea72 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:266:33  

#29 0x562d002fdc8e in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:360:10  

#30 0x562cfff21269 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api/api.cc:2155:7  

#31 0x562d0a24ec77 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:341:22  

#32 0x562d0bb5a8ee in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:132:20  

#33 0x562d0bb5d44e in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:359:33  

#34 0x562d0bb5de52 in blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:324:3  

#35 0x562d0dd973d4 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script\*, blink::ScriptElementBase\*, bool, bool, bool, base::TimeTicks, bool) third\_party/blink/renderer/core/script/pending\_script.cc:267:13  

#36 0x562d0dd96e79 in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) third\_party/blink/renderer/core/script/pending\_script.cc:175:3  

#37 0x562d0dd9c4bd in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third\_party/blink/renderer/core/script/script\_loader.cc:895:9  

#38 0x562d0dd36acb in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element\*, WTF::TextPosition const&) third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:610:20  

#39 0x562d0dd3664b in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element\*, WTF::TextPosition const&) third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:333:3  

#40 0x562d0ca2dac9 in RunScriptsForPausedTreeBuilder third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:303:21  

#41 0x562d0ca2dac9 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >) third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:543:9  

#42 0x562d0ca297e9 in blink::HTMLDocumentParser::PumpPendingSpeculations() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:601:9  

#43 0x562d022b8317 in Run base/callback.h:98:12  

#44 0x562d022b8317 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) third\_party/blink/renderer/platform/scheduler/common/post\_cancellable\_task.cc:47:21  

#45 0x562d04dc21a2 in Run base/callback.h:98:12  

#46 0x562d04dc21a2 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:142:33  

#47 0x562d04dfa5f8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:365:23  

#48 0x562d04df9f79 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219:7  

#49 0x562d04d21c00 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:55  

#50 0x562d04dfc39e in Run base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:12  

#51 0x562d04dfc39e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#52 0x562d04d7fde1 in base::RunLoop::Run() base/run\_loop.cc:156:14  

#53 0x562d11851b2f in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:213:16  

#54 0x562d0268341f in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:492:14  

#55 0x562d0268687a in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:871:10  

#56 0x562d0a15fa5a in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:423:29  

#57 0x562cff8a6e1f in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#58 0x562cfd1d9aeb in main content/shell/app/shell\_main.cc:43:10  

#59 0x7fcb5ad9ab96 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)

SUMMARY: AddressSanitizer: heap-buffer-overflow third\_party/pffft/src/pffft.c:624:35 in radf4\_ps  

Shadow bytes around the buggy address:  

0x0c1a80000000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1a80000010: fd fa fa fa fa fa fa fa fa fa 00 00 00 00 00 00  

0x0c1a80000020: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

0x0c1a80000030: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1a80000040: fd fd fd fd fd fd fa fa fa fa fa fa fa fa 00 00  

=>0x0c1a80000050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00[00]fa  

0x0c1a80000060: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c1a80000070: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa  

0x0c1a80000080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c1a80000090: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c1a800000a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==10724==ABORTING

## Attachments

- [pffft_crash.html](attachments/pffft_crash.html) (text/plain, 391 B)

## Timeline

### cl...@chromium.org (2019-12-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5976112890970112.

### cl...@chromium.org (2019-12-09)

Testcase 5976112890970112 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5976112890970112.

### cl...@chromium.org (2019-12-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5885567262851072.

### me...@chromium.org (2019-12-09)

I reproed this on trunk.
olka@ or maxmorin@ could you please take a look?

[Monorail components: Blink>WebRTC>Audio]

### cl...@chromium.org (2019-12-09)

Testcase 5885567262851072 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5885567262851072.

### me...@chromium.org (2019-12-09)

[Empty comment from Monorail migration]

### ol...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### al...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### al...@chromium.org (2019-12-10)

I compiled top of tree chrome (commit 4f673421b42b2a83283036d41f54ae4b250bbf91, is_debug=false) and tried the JS code via pffft_crash.html (see the attached file). It didn't crash. Let me know if the way I tried to reproduce is incorrect.

### al...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-10)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2019-12-10)

I am able to repro on trunk (868fd439462640cb3f621a131cefff95bdfecea7) on linux. Did you try is_asan=true?
You can download this trunk build and verify this https://ci.chromium.org/p/chromium/builders/ci/ASAN%20Release/117277

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### li...@chromium.org (2020-01-14)

Friendly ping from the security marshal--alessiob@, any progress? This is a high severity issue, so ideally let's try to close this out soon.

### al...@chromium.org (2020-01-14)

Sorry for the belated answer.

TL;DR: it's not a pffft issue, but an incorrect usage of its (fragile) API

When the dchecks are active, https://cs.chromium.org/chromium/src/third_party/blink/renderer/platform/audio/hrtf_kernel.cc?rcl=1aa2f57c1ae45e03204ae3519c06201e75e32f8e&l=51 crashes. That shows the issue: fft size is 32 but the input vector has size 26 (incorrect).
Note however that 4510 is an uncommon sample rate that has no practical application: it's lower than 8k (AFAIK the minimum supported by a sound card) and it's a weird value for common frame sizes such as 10 and 20 ms (non integer number of samples).

To isolate the problem, you can try the test below in https://cs.chromium.org/chromium/src/third_party/pffft/pffft_unittest.cc?type=cs&q=pffft_u&sq=package:chromium&g=0&l=1

TEST(PffftTest, ReproBug1032000) {
  constexpr int kFftSize = 32;
  constexpr int kInputSize = ***** [INPUT SIZE HERE] *****;

  PFFFT_Setup* setup = pffft_new_setup(kFftSize, PFFFT_REAL);

  float* out = static_cast<float*>(pffft_aligned_malloc(kFftSize * sizeof(float)));
  float* tmp = static_cast<float*>(pffft_aligned_malloc(kFftSize * sizeof(float)));

  float* in = static_cast<float*>(pffft_aligned_malloc(kInputSize * sizeof(float)));
  for (int i = 0; i < kInputSize; ++i) {
    in[i] = 10.f;
  }
  
  pffft_transform_ordered(setup, in, out, tmp, PFFFT_FORWARD);
}

ASAN finds heap-buffer-overflow when kInputSize <= 24 or when kInputSize in [29, 31].
Not sure why ASAN misses heap-buffer-overflow when kInputSize in [25, 28] (maybe because of SIMD?)
Anyways, when the input size is shorter than the fft size, the buffer overflow is expected.

I will reassign this bug to the blink owners since unfortunately there's not much I can do in pffft, the API of which only gets pointers to data (without size).
My recommendation is to improve the Blink C++ PFFFT wrapper by requiring the size information and always checking that it's correct - i.e., input size == fft size.
For instance: FFTFrame::DoFFT(const float* data) -> FFTFrame::DoFFT(absl::Span<const float> data) and similarly for FFTFrame::DoInverseFFT().
That's also recommended in //third_party/pffft/README.md and an example is given (namely, https://cs.chromium.org/chromium/src/third_party/webrtc/modules/audio_processing/utility/pffft_wrapper.h).

Finally, I hope that at some point I will have time to rewrite the entire library in C++ to expose a safer interface, but that's not gonna happen any time soon.

### al...@chromium.org (2020-01-14)

[Empty comment from Monorail migration]

### ho...@chromium.org (2020-01-14)

rtoy@ has worked on PFFFT integration.

[Monorail components: -Blink>WebRTC>Audio Blink>WebAudio]

### sh...@chromium.org (2020-01-15)

rtoy: Uh oh! This issue still open and hasn't been updated in the last 37 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rt...@chromium.org (2020-01-15)

Thanks for the analysis in c#15.  I think this is probably caused by HRTFPanner::FftSizeForSampleRate.  For a sample rate of 4510, the analysis_fft_size should be 16, but PFFFT has a lower FFT size of 32.  I think we might need to add a 16-point FFT or adjust the allocation of the response to have a size that is at least 32.  The 16-point FFT probably doesn't have to have the same performance as the rest of PFFFT.  Zero-padding the response is easier.

### rt...@chromium.org (2020-01-15)

See also https://crbug.com/chromium/1041411.  This apparently has a more reliable test case where clusterfuzz can reproduce the problem.  The main difference is that this bug uses an AudioContext, but the other uses an OfflineAudioContext (at 4 kHz).

### rt...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6e00639d878b4e71689798aba8e0e216bd59e42c

commit 6e00639d878b4e71689798aba8e0e216bd59e42c
Author: Raymond Toy <rtoy@chromium.org>
Date: Fri Jan 17 13:50:58 2020

Zero-pad HRTF response if needed

The HRTF response size can some times be smaller than the FFT size.
This can happen if the FFT size has a lower limit, such as for PFFFT
which clamps the size to the lower bound.  To account for this, create
a new HRTF response that is zero-padded to the FFT size.

Manually tested against repro cases from the bugs; ASAN issue no
longer reproduces.

Bug: 1032000, 1041411
Change-Id: Ic2136a92a6e1bf4f2f78f434b065c21dc1b72b5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2003571
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#732837}

[modify] https://crrev.com/6e00639d878b4e71689798aba8e0e216bd59e42c/third_party/blink/renderer/platform/audio/hrtf_elevation.cc


### rt...@chromium.org (2020-01-18)

I'm going to duplicate this to 1041411 since it has a reliable repro case.  Copying the labels to that issue as well.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b6dcb22b638605068d8c74e9821827e7948d5fe1

commit b6dcb22b638605068d8c74e9821827e7948d5fe1
Author: Raymond Toy <rtoy@chromium.org>
Date: Tue Jan 21 19:14:13 2020

Zero-pad HRTF response if needed

The HRTF response size can some times be smaller than the FFT size.
This can happen if the FFT size has a lower limit, such as for PFFFT
which clamps the size to the lower bound.  To account for this, create
a new HRTF response that is zero-padded to the FFT size.

Manually tested against repro cases from the bugs; ASAN issue no
longer reproduces.

(cherry picked from commit 6e00639d878b4e71689798aba8e0e216bd59e42c)

Bug: 1032000, 1041411
Change-Id: Ic2136a92a6e1bf4f2f78f434b065c21dc1b72b5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2003571
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#732837}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2010172
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#642}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/b6dcb22b638605068d8c74e9821827e7948d5fe1/third_party/blink/renderer/platform/audio/hrtf_elevation.cc


### [Deleted User] (2020-04-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-05-15)

Adding reward-topanel here as it was duplicated to a newer bug.

### [Deleted User] (2020-05-16)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-21)

Congrats! The Panel decided to award $500 for this report

### na...@google.com (2020-05-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1032000?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1041411]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050926)*
