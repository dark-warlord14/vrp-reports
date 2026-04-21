# uaf in load4 SkRasterPipeline_opts.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40053541](https://issues.chromium.org/issues/40053541) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | ne...@gmail.com |
| **Assignee** | aa...@chromium.org |
| **Created** | 2020-10-10 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36

Steps to reproduce the problem:
Chromium 88.0.4288.0
1.build latest chrome with asan
2.python3.6m -m http.server 8000
3../crhome --user-data-dir=/tmp/no --enable-experimental-web-platform-features http://127.0.0.1:8000/crash.html

What is the expected behavior?

What went wrong?
==99054==ERROR: AddressSanitizer: heap-use-after-free on address 0x61e00008b8a8 at pc 0x563da24dc897 bp 0x7ffe292315b0 sp 0x7ffe292315a8
READ of size 8 at 0x61e00008b8a8 thread T0 (chrome)
    #0 0x563da24dc896 in load4 ./../../third_party/skia/src/opts/SkRasterPipeline_opts.h:498:35
    #1 0x563da24dc896 in load_f16_k ./../../third_party/skia/src/opts/SkRasterPipeline_opts.h:2133:5
    #2 0x563da24dc896 in hsw::load_f16(unsigned long, void**, unsigned long, unsigned long, float vector[8], float vector[8], float vector[8], float vector[8], float vector[8], float vector[8], float vector[8], float vector[8]) ./../../third_party/skia/src/opts/SkRasterPipeline_opts.h:2129:1
    #3 0x563da24fac3f in hsw::start_pipeline(unsigned long, unsigned long, unsigned long, unsigned long, void**) ./../../third_party/skia/src/opts/SkRasterPipeline_opts.h:1091:13
    #4 0x563da20fb05d in SkRasterPipeline::run(unsigned long, unsigned long, unsigned long, unsigned long) const ./../../third_party/skia/src/core/SkRasterPipeline.cpp:377:5
    #5 0x563da1f54321 in convert_with_pipeline ./../../third_party/skia/src/core/SkConvertPixels.cpp:219:14
    #6 0x563da1f54321 in SkConvertPixels(SkImageInfo const&, void*, unsigned long, SkImageInfo const&, void const*, unsigned long) ./../../third_party/skia/src/core/SkConvertPixels.cpp:235:5
    #7 0x563da20d334e in SkPixmap::readPixels(SkImageInfo const&, void*, unsigned long, int, int) const ./../../third_party/skia/src/core/SkPixmap.cpp:170:5
    #8 0x563da1ea0a38 in SkBitmap::readPixels(SkImageInfo const&, void*, unsigned long, int, int) const ./../../third_party/skia/src/core/SkBitmap.cpp:468:16
    #9 0x563da22baded in SkImage_Raster::onReadPixels(GrDirectContext*, SkImageInfo const&, void*, unsigned long, int, int, SkImage::CachingHint) const ./../../third_party/skia/src/image/SkImage_Raster.cpp:179:24
    #10 0x563da22a82b9 in readPixels ./../../third_party/skia/src/image/SkImage.cpp:56:25
    #11 0x563da22a82b9 in SkImage::readPixels(SkImageInfo const&, void*, unsigned long, int, int, SkImage::CachingHint) const ./../../third_party/skia/src/image/SkImage.cpp:63:18
    #12 0x563daed97475 in cc::PaintImage::readPixels(SkImageInfo const&, void*, unsigned long, int, int) const ./../../cc/paint/paint_image.cc:145:30
    #13 0x563db8ed65c4 in blink::ImageDataBuffer::ImageDataBuffer(scoped_refptr<blink::StaticBitmapImage>) ./../../third_party/blink/renderer/platform/graphics/image_data_buffer.cc:91:22
    #14 0x563db8ed6ff1 in blink::ImageDataBuffer::Create(scoped_refptr<blink::StaticBitmapImage>) ./../../third_party/blink/renderer/platform/graphics/image_data_buffer.cc:116:28
    #15 0x563db8f43d7a in operator() ./../../third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc:503:21
    #16 0x563db8f43d7a in Invoke<(lambda at ../../third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc:500:15), scoped_refptr<blink::StaticBitmapImage>, blink::UkmParameters> ./../../base/bind_internal.h:379:12
    #17 0x563db8f43d7a in MakeItSo<(lambda at ../../third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc:500:15), scoped_refptr<blink::StaticBitmapImage>, blink::UkmParameters> ./../../base/bind_internal.h:637:12
    #18 0x563db8f43d7a in RunImpl<(lambda at ../../third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc:500:15), std::__1::tuple<scoped_refptr<blink::StaticBitmapImage>, blink::UkmParameters>, 0, 1> ./../../base/bind_internal.h:710:12
    #19 0x563db8f43d7a in base::internal::Invoker<base::internal::BindState<blink::CanvasAsyncBlobCreator::RecordIdentifiabilityMetric()::$_0, scoped_refptr<blink::StaticBitmapImage>, blink::UkmParameters>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:679:12
    #20 0x563dabc31a61 in Run ./../../base/callback.h:100:12
    #21 0x563dabc31a61 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:163:33
    #22 0x563dabc6b241 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332:23
    #23 0x563dabc6aaab in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:252:36
    #24 0x563dabb5d710 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #25 0x563dabc6c5bd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:446:12
    #26 0x563dabbdcf46 in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #27 0x563dbeae3164 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:256:16
    #28 0x563dab962574 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:860:10
    #29 0x563dab95bf9c in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:373:36
    #30 0x563dab95c5c8 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:399:10
    #31 0x563da1649886 in ChromeMain ./../../chrome/app/chrome_main.cc:119:12
    #32 0x7f8a0bdbfb96 in __libc_start_main /build/glibc-2ORdQG/glibc-2.27/csu/../csu/libc-start.c:310:0

0x61e00008b8a8 is located 40 bytes inside of 2440-byte region [0x61e00008b880,0x61e00008c208)
freed by thread T0 (chrome) here:
    #0 0x563da1646ead in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x563db8f39346 in unref ./../../third_party/skia/include/core/SkRefCnt.h:180:13
    #2 0x563db8f39346 in SkSafeUnref<SkData> ./../../third_party/skia/include/core/SkRefCnt.h:150:14
    #3 0x563db8f39346 in ~sk_sp ./../../third_party/skia/include/core/SkRefCnt.h:251:9
    #4 0x563db8f39346 in blink::CanvasAsyncBlobCreator::~CanvasAsyncBlobCreator() ./../../third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc:283:49
    #5 0x563daa9b24ab in Finalize ./../../third_party/blink/renderer/platform/heap/heap_page.cc:95:5
    #6 0x563daa9b24ab in blink::NormalPage::ToBeFinalizedObject::Finalize() ./../../third_party/blink/renderer/platform/heap/heap_page.cc:1403:11
    #7 0x563daa9b26c7 in blink::NormalPage::FinalizeSweep(blink::SweepResult) ./../../third_party/blink/renderer/platform/heap/heap_page.cc:1412:12
    #8 0x563daa9aa88f in blink::BaseArena::InvokeFinalizersOnSweptPages() ./../../third_party/blink/renderer/platform/heap/heap_page.cc:379:11
    #9 0x563daa9aafaf in blink::BaseArena::CompleteSweep() ./../../third_party/blink/renderer/platform/heap/heap_page.cc:403:3
    #10 0x563daa9981d0 in blink::ThreadHeap::CompleteSweep() ./../../third_party/blink/renderer/platform/heap/heap.cc:710:17
    #11 0x563daa9c7f84 in blink::ThreadState::CompleteSweep() ./../../third_party/blink/renderer/platform/heap/thread_state.cc:760:12
    #12 0x563daa9ca15d in blink::ThreadState::StartIncrementalMarking(blink::BlinkGC::GCReason) ./../../third_party/blink/renderer/platform/heap/thread_state.cc:508:3
    #13 0x563daa9da13e in blink::UnifiedHeapController::TracePrologue(v8::EmbedderHeapTracer::TraceFlags) ./../../third_party/blink/renderer/platform/heap/unified_heap_controller.cc:63:18
    #14 0x563da8c2b3f2 in v8::internal::MarkCompactCollector::Prepare() ./../../v8/src/heap/mark-compact.cc:856:44
    #15 0x563da8b927e6 in v8::internal::Heap::MarkCompact() ./../../v8/src/heap/heap.cc:2182:29
    #16 0x563da8b8c6fd in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:2005:7
    #17 0x563da8b85228 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1609:13
    #18 0x563da8b9b985 in v8::internal::Heap::AllocateExternalBackingStore(std::__1::function<void* (unsigned long)> const&, unsigned long) ./../../v8/src/heap/heap.cc:2818:7
    #19 0x563da8f9c4cc in v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag) ./../../v8/src/objects/backing-store.cc:252:37
    #20 0x563da8791fb3 in v8::internal::(anonymous namespace)::ConstructBuffer(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::JSReceiver>, v8::internal::Handle<v8::internal::Object>, v8::internal::InitializedFlag) ./../../v8/src/builtins/builtins-arraybuffer.cc:56:7
    #21 0x563da878fd09 in v8::internal::Builtin_Impl_ArrayBufferConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-arraybuffer.cc:92:12
    #22 0x563daa8972f7 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit ??:0:0
    #23 0x563daa826924 in Builtins_JSBuiltinsConstructStub ??:0:0
    #24 0x563daa92755e in Builtins_ConstructHandler ??:0:0
    #25 0x563daa8298f7 in Builtins_InterpreterEntryTrampoline ??:0:0
    #26 0x563daa82741a in Builtins_JSEntryTrampoline ??:0:0
    #27 0x563daa8271f7 in Builtins_JSEntry ??:0:0
    #28 0x563da8a167be in Call ./../../v8/src/execution/simulator.h:142:12
    #29 0x563da8a167be in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:368:33
    #30 0x563da8a1575e in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:462:10
    #31 0x563da8650d70 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) ./../../v8/src/api/api.cc:5007:7
    #32 0x563db72537de in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:629:17
    #33 0x563db89b8aa2 in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:107:8
    #34 0x563db89b9509 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:251:7

previously allocated by thread T0 (chrome) here:
    #0 0x563da164664d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x563da1f56f08 in PrivateNewWithCopy ./../../third_party/skia/src/core/SkData.cpp:76:21
    #2 0x563da1f56f08 in SkData::MakeUninitialized(unsigned long) ./../../third_party/skia/src/core/SkData.cpp:111:12
    #3 0x563db8f36d7c in blink::CanvasAsyncBlobCreator::CanvasAsyncBlobCreator(scoped_refptr<blink::StaticBitmapImage>, blink::ImageEncodeOptions const*, blink::CanvasAsyncBlobCreator::ToBlobFunctionType, blink::V8BlobCallback*, base::TimeTicks, blink::ExecutionContext*, blink::UkmParameters, blink::ScriptPromiseResolver*) ./../../third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc:248:26
    #4 0x563db8f35807 in blink::CanvasAsyncBlobCreator::CanvasAsyncBlobCreator(scoped_refptr<blink::StaticBitmapImage>, blink::ImageEncodeOptions const*, blink::CanvasAsyncBlobCreator::ToBlobFunctionType, base::TimeTicks, blink::ExecutionContext*, blink::UkmParameters, blink::ScriptPromiseResolver*) ./../../third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc:155:7
    #5 0x563db8f4ec73 in blink::CanvasAsyncBlobCreator* blink::MakeGarbageCollectedTrait<blink::CanvasAsyncBlobCreator>::Call<scoped_refptr<blink::StaticBitmapImage>&, blink::ImageEncodeOptions const*&, blink::CanvasAsyncBlobCreator::ToBlobFunctionType&, base::TimeTicks&, blink::ExecutionContext*, blink::UkmParameters&, blink::ScriptPromiseResolver*&>(scoped_refptr<blink::StaticBitmapImage>&, blink::ImageEncodeOptions const*&, blink::CanvasAsyncBlobCreator::ToBlobFunctionType&, base::TimeTicks&, blink::ExecutionContext*&&, blink::UkmParameters&, blink::ScriptPromiseResolver*&) ./../../third_party/blink/renderer/platform/heap/heap.h:545:32
    #6 0x563db8f4dd5d in MakeGarbageCollected<blink::CanvasAsyncBlobCreator, scoped_refptr<blink::StaticBitmapImage> &, const blink::ImageEncodeOptions *&, blink::CanvasAsyncBlobCreator::ToBlobFunctionType &, base::TimeTicks &, blink::ExecutionContext *, blink::UkmParameters &, blink::ScriptPromiseResolver *&> ./../../third_party/blink/renderer/platform/heap/heap.h:585:15
    #7 0x563db8f4dd5d in blink::CanvasRenderingContextHost::convertToBlob(blink::ScriptState*, blink::ImageEncodeOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/core/html/canvas/canvas_rendering_context_host.cc:339:27
    #8 0x563db8ebd373 in blink::HTMLCanvasElement::convertToBlob(blink::ScriptState*, blink::ImageEncodeOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/core/html/canvas/html_canvas_element.cc:434:38
    #9 0x563dbe92aa76 in blink::(anonymous namespace)::ConvertToBlobOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_html_canvas_element.cc:278:41
    #10 0x563da877a8b9 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158:3
    #11 0x563da8778371 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111:36
    #12 0x563da8775ed2 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:141:5
    #13 0x563daa8972f7 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit ??:0:0
    #14 0x563daa8298f7 in Builtins_InterpreterEntryTrampoline ??:0:0
    #15 0x563daa8298f7 in Builtins_InterpreterEntryTrampoline ??:0:0
    #16 0x563daa8298f7 in Builtins_InterpreterEntryTrampoline ??:0:0
    #17 0x563daa82741a in Builtins_JSEntryTrampoline ??:0:0
    #18 0x563daa8271f7 in Builtins_JSEntry ??:0:0
    #19 0x563da8a167be in Call ./../../v8/src/execution/simulator.h:142:12
    #20 0x563da8a167be in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:368:33
    #21 0x563da8a1575e in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:462:10
    #22 0x563da860caf6 in v8::Script::Run(v8::Local<v8::Context>) ./../../v8/src/api/api.cc:2159:7
    #23 0x563db724fc96 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:362:22
    #24 0x563db7250d85 in blink::V8ScriptRunner::CompileAndRunScript(v8::Isolate*, blink::ScriptState*, blink::ExecutionContext*, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::mojom::V8CacheOptions, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:440:11
    #25 0x563db815c119 in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local<v8::Context>, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:100:37
    #26 0x563db815f258 in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:298:33
    #27 0x563dbaba2661 in RunScriptAndReturnValue ./../../third_party/blink/renderer/core/script/classic_script.cc:42:40
    #28 0x563dbaba2661 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:36:3
    #29 0x563dbaba2661 in blink::ClassicScript::RunScript(blink::LocalDOMWindow*) ./../../third_party/blink/renderer/core/script/classic_script.cc:29:10
    #30 0x563dbabf4489 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) ./../../third_party/blink/renderer/core/script/pending_script.cc:264:13
    #31 0x563dbabf3d8d in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third_party/blink/renderer/core/script/pending_script.cc:170:3
    #32 0x563dbabfa08f in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third_party/blink/renderer/core/script/script_loader.cc:914:9
    #33 0x563dbaba91fa in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:609:20
    #34 0x563dbaba8d98 in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:332:3

SUMMARY: AddressSanitizer: heap-use-after-free (/home/test/chromium/src/out/chrome/chrome+0xa82f896)
Shadow bytes around the buggy address:
  0x0c3c800096c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3c800096d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3c800096e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3c800096f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3c80009700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c3c80009710: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x0c3c80009720: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80009730: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80009740: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80009750: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80009760: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==99054==ABORTING
Received signal 6
    #0 0x563da15d9a3b in backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4176:13
    #1 0x563dabd18d54 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:840:39
    #2 0x563dabb0ede2 in StackTrace ./../../base/debug/stack_trace.cc:198:12
    #3 0x563dabb0ede2 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:195:28
    #4 0x563dabd1791e in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:345:3
    #5 0x7f8a134f38a0 in __funlockfile ??:?
    #6 0x7f8a134f38a0 in ?? ??:0
    #7 0x7f8a0bddcf47 in __libc_signal_restore_set /build/glibc-2ORdQG/glibc-2.27/signal/../sysdeps/unix/sysv/linux/nptl-signals.h:80:0
    #8 0x7f8a0bddcf47 in raise /build/glibc-2ORdQG/glibc-2.27/signal/../sysdeps/unix/sysv/linux/raise.c:48:0
    #9 0x7f8a0bdde8b1 in abort /build/glibc-2ORdQG/glibc-2.27/stdlib/abort.c:79:0
    #10 0x563da1635f07 in __sanitizer::Abort() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cpp:152:3
    #11 0x563da1634a81 in __sanitizer::Die() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cpp:58:5
    #12 0x563da16210c4 in __asan::ScopedInErrorReport::~ScopedInErrorReport() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:189:7
    #13 0x563da1622aae in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:477:1
    #14 0x563da1623815 in __asan_report_load_n /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_rtl.cpp:145:1
    #15 0x563da24dc897 in load4 ./../../third_party/skia/src/opts/SkRasterPipeline_opts.h:498:35
    #16 0x563da24dc897 in load_f16_k ./../../third_party/skia/src/opts/SkRasterPipeline_opts.h:2133:5
    #17 0x563da24dc897 in hsw::load_f16(unsigned long, void**, unsigned long, unsigned long, float vector[8], float vector[8], float vector[8], float vector[8], float vector[8], float vector[8], float vector[8], float vector[8]) ./../../third_party/skia/src/opts/SkRasterPipeline_opts.h:2129:1
    #18 0x563da24fac40 in hsw::start_pipeline(unsigned long, unsigned long, unsigned long, unsigned long, void**) ./../../third_party/skia/src/opts/SkRasterPipeline_opts.h:1091:13
    #19 0x563da20fb05e in SkRasterPipeline::run(unsigned long, unsigned long, unsigned long, unsigned long) const ./../../third_party/skia/src/core/SkRasterPipeline.cpp:377:5
    #20 0x563da1f54322 in convert_with_pipeline ./../../third_party/skia/src/core/SkConvertPixels.cpp:219:14
    #21 0x563da1f54322 in SkConvertPixels(SkImageInfo const&, void*, unsigned long, SkImageInfo const&, void const*, unsigned long) ./../../third_party/skia/src/core/SkConvertPixels.cpp:235:5
    #22 0x563da20d334f in SkPixmap::readPixels(SkImageInfo const&, void*, unsigned long, int, int) const ./../../third_party/skia/src/core/SkPixmap.cpp:170:5
    #23 0x563da1ea0a39 in SkBitmap::readPixels(SkImageInfo const&, void*, unsigned long, int, int) const ./../../third_party/skia/src/core/SkBitmap.cpp:468:16
    #24 0x563da22badee in SkImage_Raster::onReadPixels(GrDirectContext*, SkImageInfo const&, void*, unsigned long, int, int, SkImage::CachingHint) const ./../../third_party/skia/src/image/SkImage_Raster.cpp:179:24
    #25 0x563da22a82ba in readPixels ./../../third_party/skia/src/image/SkImage.cpp:56:25
    #26 0x563da22a82ba in SkImage::readPixels(SkImageInfo const&, void*, unsigned long, int, int, SkImage::CachingHint) const ./../../third_party/skia/src/image/SkImage.cpp:63:18
    #27 0x563daed97476 in cc::PaintImage::readPixels(SkImageInfo const&, void*, unsigned long, int, int) const ./../../cc/paint/paint_image.cc:145:30
    #28 0x563db8ed65c5 in blink::ImageDataBuffer::ImageDataBuffer(scoped_refptr<blink::StaticBitmapImage>) ./../../third_party/blink/renderer/platform/graphics/image_data_buffer.cc:91:22
    #29 0x563db8ed6ff2 in blink::ImageDataBuffer::Create(scoped_refptr<blink::StaticBitmapImage>) ./../../third_party/blink/renderer/platform/graphics/image_data_buffer.cc:116:28
    #30 0x563db8f43d7b in operator() ./../../third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc:503:21
    #31 0x563db8f43d7b in Invoke<(lambda at ../../third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc:500:15), scoped_refptr<blink::StaticBitmapImage>, blink::UkmParameters> ./../../base/bind_internal.h:379:12
    #32 0x563db8f43d7b in MakeItSo<(lambda at ../../third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc:500:15), scoped_refptr<blink::StaticBitmapImage>, blink::UkmParameters> ./../../base/bind_internal.h:637:12
    #33 0x563db8f43d7b in RunImpl<(lambda at ../../third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc:500:15), std::__1::tuple<scoped_refptr<blink::StaticBitmapImage>, blink::UkmParameters>, 0, 1> ./../../base/bind_internal.h:710:12
    #34 0x563db8f43d7b in base::internal::Invoker<base::internal::BindState<blink::CanvasAsyncBlobCreator::RecordIdentifiabilityMetric()::$_0, scoped_refptr<blink::StaticBitmapImage>, blink::UkmParameters>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:679:12
    #35 0x563dabc31a62 in Run ./../../base/callback.h:100:12
    #36 0x563dabc31a62 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:163:33
    #37 0x563dabc6b242 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332:23
    #38 0x563dabc6aaac in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:252:36
    #39 0x563dabb5d711 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #40 0x563dabc6c5be in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:446:12
    #41 0x563dabbdcf47 in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #42 0x563dbeae3165 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:256:16
    #43 0x563dab962575 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:860:10
    #44 0x563dab95bf9d in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:373:36
    #45 0x563dab95c5c9 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:399:10
    #46 0x563da1649887 in ChromeMain ./../../chrome/app/chrome_main.cc:119:12
    #47 0x7f8a0bdbfb97 in __libc_start_main /build/glibc-2ORdQG/glibc-2.27/csu/../csu/libc-start.c:310:0
    #48 0x563da15a156a in _start ??:0:0
  r8: 0000000000000000  r9: 00007ffe292305f0 r10: 0000000000000008 r11: 0000000000000246
 r12: 00007ffe292315a8 r13: 00007ffe292315b0 r14: 00007ffe29231550 r15: 0000563dc1d26348
  di: 0000000000000002  si: 00007ffe292305f0  bp: 00007ffe29231580  bx: 0000563dc1c93ed8
  dx: 0000000000000000  ax: 0000000000000000  cx: 00007f8a0bddcf47  sp: 00007ffe292305f0
  ip: 00007f8a0bddcf47 efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Chromium 88.0.4288.0  Channel: n/a
OS Version: 20.04
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 846 B)
- [crash.html](attachments/crash.html) (text/plain, 846 B)
- [crash.html](attachments/crash.html) (text/plain, 345 B)

## Timeline

### cl...@chromium.org (2020-10-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5122714946043904.

### me...@chromium.org (2020-10-12)

[Empty comment from Monorail migration]

### me...@chromium.org (2020-10-12)

Thanks for the report. Stack is similar to https://crbug.com/chromium/1062152. Adding tentative labels and assigning to hcm@.

[Monorail components: Internals>Skia]

### [Deleted User] (2020-10-14)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-14)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-15)

[Empty comment from Monorail migration]

### hc...@google.com (2020-10-15)

Seems like same deal again, unreproducible. We need help with a repro/bisect/something here.

### ro...@google.com (2020-10-16)

[Empty comment from Monorail migration]

### bs...@google.com (2020-10-16)

Aaron, I'm not sure who should be looking at this but I'm hoping you do. A CanvasAsyncBlobCreator is getting destroyed before it gets used with SkImage::readPixels.

### bs...@google.com (2020-10-16)

[Empty comment from Monorail migration]

### aa...@chromium.org (2020-10-16)

yiyix@ is currently on bug rotation, assigning to her. 

Here's a recent UAF in canvas that might have some hints. crbug.com/1126424

### yi...@chromium.org (2020-10-16)

@aaron, could you add me to the cc list? i can't access crbug.com/1126424

### [Deleted User] (2020-10-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yi...@chromium.org (2020-10-27)

i am so sorry forget that i am the owner of this bug. Aaron is current on our bug rotation. Pass to @aaronhk. if it's not finished until the end of this week, i will work on it next week. 

### aa...@chromium.org (2020-10-27)

First of all, this only repros with `--enable-experimental-web-platform-features`, so I don't believe it should be RBS.

### aa...@chromium.org (2020-10-27)

Weird that this doesn't repro for clusterfuzz, this repros for me locally.


### aa...@chromium.org (2020-10-27)

I've managed to minify the testcase somewhat. It seems like the issue is only for "image/webp" with "uint16" pixelformat. If you create a huge array buffer I guess it frees the async blob creator, causing the UAF.

Minified testcase is attached. Can anyone else repro or is it just me?

### la...@google.com (2020-10-27)

+adetaylor@ for visibility

### aa...@chromium.org (2020-10-27)

I think this is related to device memory. If I run the page from https://crbug.com/chromium/1137104#c18 with line 6 changed to:
  let a = new ArrayBuffer(2 ** 31);

it fails every time, but with:
  let a = new ArrayBuffer(2 ** 30);

it fails every OTHER time. Perhaps this is why clusterfuzz cannot reproduce.


### la...@google.com (2020-10-27)

This bug is marked as Release Block Stable for M87 which is scheduled for Stable Release cut on November 10th. Please address this bug at the earliest. If this is no longer targeting M87 then please update the milestone target.



### ad...@google.com (2020-10-27)

We have discussed this within security and realized we've been rather inconsistent about "enable-experimental-web-platform-features".

I'm going to remove the RBS label but _please_ fix this urgently nonetheless. We often advise web developers to enable such experimental features, and so we shouldn't expose them to more risk than regular users. I'd like to merge this into M87 if you get the fix done in time.

### aa...@chromium.org (2020-10-28)

[Empty comment from Monorail migration]

### aa...@chromium.org (2020-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c8826f38273bb95b1019ec0a97dec96deb3f89c5

commit c8826f38273bb95b1019ec0a97dec96deb3f89c5
Author: Aaron Krajeski <aaronhk@chromium.org>
Date: Wed Nov 04 02:09:35 2020

Make CanvasAsyncBlobCreator persist through RecordIdentifiabilityMetric

RecordIdentifiabilityMetric used a lambda callback this function and it
was not immediately clear that CanvasAsyncBlobCreator could get garbage
collected before the callback was run. The garbage collection would free
image_ and result in a UAF.

Now the callback is in a separate function and the caller is bound to
be persistent, matching the pattern of other callback functions in this
class.

The dispose method also needs to be moved. Prior to this change it was
always called before the RecordIdentifiabilityMetric finished. It worked
because the callback kept a pointer to the image, that had already been
destroyed, a bit of a Mr Burns situation:
https://www.youtube.com/watch?v=aI0euMFAWF8

Bug: 1137104
Change-Id: Iccfaf9cc15352ee3b002dad1e4241c0683fbc8bb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2505460
Reviewed-by: Philip Jägenstedt <foolip@chromium.org>
Reviewed-by: Juanmi Huertas <juanmihd@chromium.org>
Reviewed-by: Yi Xu <yiyix@chromium.org>
Commit-Queue: Aaron Krajeski <aaronhk@chromium.org>
Cr-Commit-Position: refs/heads/master@{#823850}

[modify] https://crrev.com/c8826f38273bb95b1019ec0a97dec96deb3f89c5/third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc


### aa...@chromium.org (2020-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-04)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-09)

Requesting merge to M87 per https://crbug.com/chromium/1137104#c22. Sheriffbot should reply with a merge questionnaire; the main thing is whether there's any stability risk by merging this fix to the stable branch.

At this point I think I'd be inclined to merge this into the first stable _refresh_ of M87, not the initial release.

### [Deleted User] (2020-11-09)

This bug requires manual review: We are only 7 days from stable.
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

### la...@google.com (2020-11-10)

please address the merge questionnaire to pick this merge

### aa...@chromium.org (2020-11-11)

Answers to the questionnaire:

1. Yes
2. https://chromium-review.googlesource.com/c/chromium/src/+/2505460
3. Yes
4. No
5. It fixes a potential security problem.
6. No

### ad...@chromium.org (2020-11-11)

I'm setting myself a NextAction date to approve merge for the first M87 stable refresh.

### ad...@google.com (2020-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-11)

Congratulations, the VRP panel has decided to award $5,000 for this report.

### ad...@google.com (2020-11-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-19)

Approving merge to M87, branch 4280, assuming this has caused no known problems in Canary.

### [Deleted User] (2020-11-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/188751720cdee4aadc1f3b5a04a99ff485596f1e

commit 188751720cdee4aadc1f3b5a04a99ff485596f1e
Author: Aaron Krajeski <aaronhk@chromium.org>
Date: Tue Nov 24 19:13:17 2020

Make CanvasAsyncBlobCreator persist through RecordIdentifiabilityMetric

RecordIdentifiabilityMetric used a lambda callback this function and it
was not immediately clear that CanvasAsyncBlobCreator could get garbage
collected before the callback was run. The garbage collection would free
image_ and result in a UAF.

Now the callback is in a separate function and the caller is bound to
be persistent, matching the pattern of other callback functions in this
class.

The dispose method also needs to be moved. Prior to this change it was
always called before the RecordIdentifiabilityMetric finished. It worked
because the callback kept a pointer to the image, that had already been
destroyed, a bit of a Mr Burns situation:
https://www.youtube.com/watch?v=aI0euMFAWF8

(cherry picked from commit c8826f38273bb95b1019ec0a97dec96deb3f89c5)

Bug: 1137104
Change-Id: Iccfaf9cc15352ee3b002dad1e4241c0683fbc8bb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2505460
Reviewed-by: Philip Jägenstedt <foolip@chromium.org>
Reviewed-by: Juanmi Huertas <juanmihd@chromium.org>
Reviewed-by: Yi Xu <yiyix@chromium.org>
Commit-Queue: Aaron Krajeski <aaronhk@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#823850}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2557270
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1592}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/188751720cdee4aadc1f3b5a04a99ff485596f1e/third_party/blink/renderer/core/html/canvas/canvas_async_blob_creator.cc


### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-03-29)

Hi neklab2015@ - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1137104?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1137103]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053541)*
