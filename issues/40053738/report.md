#  use-after-poison in blink::CanvasResourceHost::InitializeForRecording(canvas_resource_host.cc)

| Field | Value |
|-------|-------|
| **Issue ID** | [40053738](https://issues.chromium.org/issues/40053738) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Canvas, Blink>Paint |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | yi...@chromium.org |
| **Created** | 2020-10-29 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36

Steps to reproduce the problem:
1.build latest chrome with asan(Chromium 88.0.4288.0)
2../chrome crash.html

What is the expected behavior?

What went wrong?
[1102546:1102546:1029/204740.830460:ERROR:sandbox_linux.cc(374)] InitializeSandbox() called with multiple threads in process gpu-process.
=================================================================
==1==ERROR: AddressSanitizer: use-after-poison on address 0x7e9ebf834238 at pc 0x55f303d87067 bp 0x7ffca3c09030 sp 0x7ffca3c09028
READ of size 8 at 0x7e9ebf834238 thread T0 (chrome)
    #0 0x55f303d87066 in blink::CanvasResourceHost::InitializeForRecording(cc::PaintCanvas*) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_host.cc:44
    #1 0x55f303d87066 in ?? ??:0
    #2 0x55f303d8d26c in blink::CanvasResourceProvider::FlushCanvas() ./../../base/callback.h:161
    #3 0x55f303d8d26c in FlushCanvas ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1241
    #4 0x55f303d8d26c in ?? ??:0
    #5 0x55f303d97c6c in blink::FlushForImageListener::NotifyFlushForImage(int) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1173
    #6 0x55f303d97c6c in NotifyFlushForImage ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:57
    #7 0x55f303d97c6c in ?? ??:0
    #8 0x55f303d975d8 in blink::CanvasResourceProviderSharedImage::ShouldReplaceTargetBuffer(int) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:553
    #9 0x55f303d975d8 in ?? ??:0
    #10 0x55f303d98b5b in blink::CanvasResourceProviderSharedImage::WillDrawInternal(bool) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:429
    #11 0x55f303d98b5b in ?? ??:0
    #12 0x55f303d8b9bf in blink::CanvasResourceProvider::EnsureSkiaCanvas() ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1104
    #13 0x55f303d8b9bf in ?? ??:0
    #14 0x55f303d8e3a2 in blink::CanvasResourceProvider::RasterRecord(sk_sp<cc::PaintOpBuffer>) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1253
    #15 0x55f303d8e3a2 in ?? ??:0
    #16 0x55f303d94f81 in blink::CanvasResourceProviderSharedImage::RasterRecord(sk_sp<cc::PaintOpBuffer>) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:491
    #17 0x55f303d94f81 in ?? ??:0
    #18 0x55f303d8d0e1 in blink::CanvasResourceProvider::FlushCanvas() ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1236
    #19 0x55f303d8d0e1 in ?? ??:0
    #20 0x55f303d62407 in blink::Canvas2DLayerBridge::FlushRecording() ./../../third_party/blink/renderer/platform/graphics/canvas_2d_layer_bridge.cc:499
    #21 0x55f303d62407 in ?? ??:0
    #22 0x55f303d67dc5 in blink::Canvas2DLayerBridge::NewImageSnapshot() ./../../third_party/blink/renderer/platform/graphics/canvas_2d_layer_bridge.cc:682
    #23 0x55f303d67dc5 in ?? ??:0
    #24 0x55f3073ba0f5 in blink::CanvasRenderingContext2D::GetImage() ./../../third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc:689
    #25 0x55f3073ba0f5 in ?? ??:0
    #26 0x55f301beb2a3 in blink::HTMLCanvasElement::GetSourceImageForCanvasInternal(blink::SourceImageStatus*) ./../../third_party/blink/renderer/core/html/canvas/html_canvas_element.cc:1344
    #27 0x55f301beb2a3 in ?? ??:0
    #28 0x55f301bf456c in non-virtual thunk to blink::HTMLCanvasElement::GetSourceImageForCanvas(blink::SourceImageStatus*, blink::FloatSize const&) ./../../third_party/blink/renderer/core/html/canvas/html_canvas_element.cc:1296
    #29 0x55f301bf456c in ?? ??:0
    #30 0x55f307389de7 in ?? ??:0
    #31 0x55f307389de7 in blink::BaseRenderingContext2D::drawImage(blink::ScriptState*, blink::CanvasImageSource*, double, double, double, double, double, double, double, double, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc:1239
    #32 0x55f307389de7 in ?? ??:0
    #33 0x55f3073895b9 in blink::BaseRenderingContext2D::drawImage(blink::ScriptState*, blink::CSSImageValueOrHTMLImageElementOrSVGImageElementOrHTMLVideoElementOrHTMLCanvasElementOrImageBitmapOrOffscreenCanvas const&, double, double, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc:1061
    #34 0x55f3073895b9 in ?? ??:0
    #35 0x55f30734bbb8 in blink::(anonymous namespace)::DrawImageOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_offscreen_canvas_rendering_context_2d.cc:1926
    #36 0x55f30734bbb8 in DrawImageOperationCallback ./gen/third_party/blink/renderer/bindings/modules/v8/v8_offscreen_canvas_rendering_context_2d.cc:2078
    #37 0x55f30734bbb8 in ?? ??:0
    #38 0x55f2f1f35cfa in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #39 0x55f2f1f35cfa in ?? ??:0
    #40 0x55f2f1f33855 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111
    #41 0x55f2f1f33855 in ?? ??:0
    #42 0x55f2f1f313ce in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:141
    #43 0x55f2f1f313ce in ?? ??:0
    #44 0x55f2f407e1d7 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #45 0x55f2f407e1d7 in ?? ??:0
    #46 0x55f2f400eaf7 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #47 0x55f2f400eaf7 in ?? ??:0
    #48 0x55f2f400eaf7 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #49 0x55f2f400eaf7 in ?? ??:0
    #50 0x55f2f400c61a in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:?
    #51 0x55f2f400c61a in ?? ??:0
    #52 0x55f2f400c3f7 in Builtins_JSEntry setup-isolate-deserialize.cc:?
    #53 0x55f2f400c3f7 in ?? ??:0
    #54 0x55f2f21d86af in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/simulator.h:142
    #55 0x55f2f21d86af in Invoke ./../../v8/src/execution/execution.cc:368
    #56 0x55f2f21d86af in ?? ??:0
    #57 0x55f2f21d7660 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:462
    #58 0x55f2f21d7660 in ?? ??:0
    #59 0x55f2f1dcf1ad in v8::Script::Run(v8::Local<v8::Context>) ./../../v8/src/api/api.cc:2125
    #60 0x55f2f1dcf1ad in ?? ??:0
    #61 0x55f30386f9da in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:362
    #62 0x55f30386f9da in ?? ??:0
    #63 0x55f303870ab9 in blink::V8ScriptRunner::CompileAndRunScript(v8::Isolate*, blink::ScriptState*, blink::ExecutionContext*, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::mojom::V8CacheOptions, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:440
    #64 0x55f303870ab9 in ?? ??:0
    #65 0x55f3037b1f39 in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local<v8::Context>, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:99
    #66 0x55f3037b1f39 in ?? ??:0
    #67 0x55f3037b4ca0 in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:297
    #68 0x55f3037b4ca0 in ?? ??:0
    #69 0x55f30316d495 in blink::ClassicScript::RunScript(blink::LocalDOMWindow*) ./../../third_party/blink/renderer/core/script/classic_script.cc:42
    #70 0x55f30316d495 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:36
    #71 0x55f30316d495 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:29
    #72 0x55f30316d495 in ?? ??:0
    #73 0x55f3031bd8cd in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) ./../../third_party/blink/renderer/core/script/pending_script.cc:264
    #74 0x55f3031bd8cd in ?? ??:0
    #75 0x55f3031bd1e1 in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third_party/blink/renderer/core/script/pending_script.cc:170
    #76 0x55f3031bd1e1 in ?? ??:0
    #77 0x55f3031b47d3 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third_party/blink/renderer/core/script/script_loader.cc:915
    #78 0x55f3031b47d3 in ?? ??:0
    #79 0x55f3044263bb in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:609
    #80 0x55f3044263bb in ?? ??:0
    #81 0x55f304425f6b in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:332
    #82 0x55f304425f6b in ?? ??:0
    #83 0x55f3043dca03 in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:539
    #84 0x55f3043dca03 in ?? ??:0
    #85 0x55f3043e05ea in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::__1::unique_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::__1::default_delete<blink::HTMLDocumentParser::TokenizedChunk> >, bool*) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:780
    #86 0x55f3043e05ea in ?? ??:0
    #87 0x55f3043dc2ad in blink::HTMLDocumentParser::PumpPendingSpeculations() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:840
    #88 0x55f3043dc2ad in ?? ??:0
    #89 0x55f3043dbc4e in blink::HTMLDocumentParser::ResumeParsingAfterYield() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:526
    #90 0x55f3043dbc4e in ?? ??:0
    #91 0x55f2f41d4231 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) ./../../base/callback.h:101
    #92 0x55f2f41d4231 in Run ./../../third_party/blink/renderer/platform/scheduler/common/post_cancellable_task.cc:47
    #93 0x55f2f41d4231 in ?? ??:0
    #94 0x55f2f41d5206 in base::internal::Invoker<base::internal::BindState<void (blink::TaskHandle::Runner::*)(blink::TaskHandle const&), base::WeakPtr<blink::TaskHandle::Runner>, blink::TaskHandle>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:498
    #95 0x55f2f41d5206 in MakeItSo<void (blink::TaskHandle::Runner::*)(const blink::TaskHandle &), base::WeakPtr<blink::TaskHandle::Runner>, blink::TaskHandle> ./../../base/bind_internal.h:657
    #96 0x55f2f41d5206 in RunImpl<void (blink::TaskHandle::Runner::*)(const blink::TaskHandle &), std::__1::tuple<base::WeakPtr<blink::TaskHandle::Runner>, blink::TaskHandle>, 0, 1> ./../../base/bind_internal.h:710
    #97 0x55f2f41d5206 in RunOnce ./../../base/bind_internal.h:679
    #98 0x55f2f41d5206 in ?? ??:0
    #99 0x55f2f5418325 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:101
    #100 0x55f2f5418325 in RunTask ./../../base/task/common/task_annotator.cc:163
    #101 0x55f2f5418325 in ?? ??:0
    #102 0x55f2f5451660 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332
    #103 0x55f2f5451660 in ?? ??:0
    #104 0x55f2f5450dbf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:252
    #105 0x55f2f5450dbf in ?? ??:0
    #106 0x55f2f5343cc0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #107 0x55f2f5343cc0 in ?? ??:0
    #108 0x55f2f5453476 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:446
    #109 0x55f2f5453476 in ?? ??:0
    #110 0x55f2f53c588a in base::RunLoop::Run() ./../../base/run_loop.cc:124
    #111 0x55f2f53c588a in ?? ??:0
    #112 0x55f3087f0ac8 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:256
    #113 0x55f3087f0ac8 in ?? ??:0
    #114 0x55f2f5124cbf in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:498
    #115 0x55f2f5124cbf in ?? ??:0
    #116 0x55f2f51280ed in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:882
    #117 0x55f2f51280ed in ?? ??:0
    #118 0x55f2f5121bdc in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #119 0x55f2f5121bdc in ?? ??:0
    #120 0x55f2f51221dc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #121 0x55f2f51221dc in ?? ??:0
    #122 0x55f2ea55d315 in ChromeMain ./../../chrome/app/chrome_main.cc:130
    #123 0x55f2ea55d315 in ?? ??:0
    #124 0x7f4db05c60b2 in __libc_start_main ??:?
    #125 0x7f4db05c60b2 in ?? ??:0

Address 0x7e9ebf834238 is a wild pointer.
SUMMARY: AddressSanitizer: use-after-poison (/home/test/asan-linux-release/chrome+0x23a7b066)
Shadow bytes around the buggy address:
  0x0fd457efe7f0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd457efe800: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd457efe810: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd457efe820: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd457efe830: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x0fd457efe840: f7 f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd457efe850: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 00 00 00
  0x0fd457efe860: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd457efe870: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd457efe880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd457efe890: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==1==ABORTING
Received signal 6
    #0 0x55f2ea4ed83b in __interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4176
    #1 0x55f2ea4ed83b in ?? ??:0
    #2 0x55f2f54fcc79 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:833
    #3 0x55f2f54fcc79 in ?? ??:0
    #4 0x55f2f52f22c3 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:198
    #5 0x55f2f52f22c3 in StackTrace ./../../base/debug/stack_trace.cc:195
    #6 0x55f2f52f22c3 in ?? ??:0
    #7 0x55f2f54fb86e in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:345
    #8 0x55f2f54fb86e in ?? ??:0
    #9 0x7f4db22453c0 in __funlockfile :?
    #10 0x7f4db22453c0 in ?? ??:0
    #11 0x7f4db05e518b in gsignal ??:?
    #12 0x7f4db05e518b in ?? ??:0
    #13 0x7f4db05c4859 in abort ??:?
    #14 0x7f4db05c4859 in ?? ??:0
    #15 0x55f2ea549d07 in __sanitizer::Abort() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cpp:152
    #16 0x55f2ea549d07 in ?? ??:0
    #17 0x55f2ea548881 in __sanitizer::Die() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cpp:58
    #18 0x55f2ea548881 in ?? ??:0
    #19 0x55f2ea534ec4 in __asan::ScopedInErrorReport::~ScopedInErrorReport() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:189
    #20 0x55f2ea534ec4 in ?? ??:0
    #21 0x55f2ea5368ae in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:477
    #22 0x55f2ea5368ae in ?? ??:0
    #23 0x55f2ea537138 in __asan_report_load8 /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_rtl.cpp:120
    #24 0x55f2ea537138 in ?? ??:0
    #25 0x55f303d87067 in blink::CanvasResourceHost::InitializeForRecording(cc::PaintCanvas*) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_host.cc:44
    #26 0x55f303d87067 in ?? ??:0
    #27 0x55f303d8d26d in Run ./../../base/callback.h:161
    #28 0x55f303d8d26d in blink::CanvasResourceProvider::FlushCanvas() ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1241
    #29 0x55f303d8d26d in ?? ??:0
    #30 0x55f303d97c6d in OnFlushForImage ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1173
    #31 0x55f303d97c6d in NotifyFlushForImage ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:57
    #32 0x55f303d97c6d in ?? ??:0
    #33 0x55f303d975d9 in blink::CanvasResourceProviderSharedImage::ShouldReplaceTargetBuffer(int) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:553
    #34 0x55f303d975d9 in ?? ??:0
    #35 0x55f303d98b5c in blink::CanvasResourceProviderSharedImage::WillDrawInternal(bool) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:429
    #36 0x55f303d98b5c in ?? ??:0
    #37 0x55f303d8b9c0 in blink::CanvasResourceProvider::EnsureSkiaCanvas() ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1104
    #38 0x55f303d8b9c0 in ?? ??:0
    #39 0x55f303d8e3a3 in blink::CanvasResourceProvider::RasterRecord(sk_sp<cc::PaintOpBuffer>) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1253
    #40 0x55f303d8e3a3 in ?? ??:0
    #41 0x55f303d94f82 in blink::CanvasResourceProviderSharedImage::RasterRecord(sk_sp<cc::PaintOpBuffer>) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:491
    #42 0x55f303d94f82 in ?? ??:0
    #43 0x55f303d8d0e2 in blink::CanvasResourceProvider::FlushCanvas() ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1236
    #44 0x55f303d8d0e2 in ?? ??:0
    #45 0x55f303d62408 in blink::Canvas2DLayerBridge::FlushRecording() ./../../third_party/blink/renderer/platform/graphics/canvas_2d_layer_bridge.cc:499
    #46 0x55f303d62408 in ?? ??:0
    #47 0x55f303d67dc6 in blink::Canvas2DLayerBridge::NewImageSnapshot() ./../../third_party/blink/renderer/platform/graphics/canvas_2d_layer_bridge.cc:682
    #48 0x55f303d67dc6 in ?? ??:0
    #49 0x55f3073ba0f6 in blink::CanvasRenderingContext2D::GetImage() ./../../third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc:689
    #50 0x55f3073ba0f6 in ?? ??:0
    #51 0x55f301beb2a4 in blink::HTMLCanvasElement::GetSourceImageForCanvasInternal(blink::SourceImageStatus*) ./../../third_party/blink/renderer/core/html/canvas/html_canvas_element.cc:1344
    #52 0x55f301beb2a4 in ?? ??:0
    #53 0x55f301bf456d in GetSourceImageForCanvas ./../../third_party/blink/renderer/core/html/canvas/html_canvas_element.cc:1296
    #54 0x55f301bf456d in ?? ??:0
    #55 0x55f307389de8 in ?? ??:0
    #56 0x55f307389de8 in blink::BaseRenderingContext2D::drawImage(blink::ScriptState*, blink::CanvasImageSource*, double, double, double, double, double, double, double, double, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc:1239
    #57 0x55f307389de8 in ?? ??:0
    #58 0x55f3073895ba in blink::BaseRenderingContext2D::drawImage(blink::ScriptState*, blink::CSSImageValueOrHTMLImageElementOrSVGImageElementOrHTMLVideoElementOrHTMLCanvasElementOrImageBitmapOrOffscreenCanvas const&, double, double, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc:1061
    #59 0x55f3073895ba in ?? ??:0
    #60 0x55f30734bbb9 in DrawImageOperationOverload1 ./gen/third_party/blink/renderer/bindings/modules/v8/v8_offscreen_canvas_rendering_context_2d.cc:1926
    #61 0x55f30734bbb9 in DrawImageOperationCallback ./gen/third_party/blink/renderer/bindings/modules/v8/v8_offscreen_canvas_rendering_context_2d.cc:2078
    #62 0x55f30734bbb9 in ?? ??:0
    #63 0x55f2f1f35cfb in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #64 0x55f2f1f35cfb in ?? ??:0
    #65 0x55f2f1f33856 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111
    #66 0x55f2f1f33856 in ?? ??:0
    #67 0x55f2f1f313cf in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:141
    #68 0x55f2f1f313cf in ?? ??:0
    #69 0x55f2f407e1d8 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #70 0x55f2f407e1d8 in ?? ??:0
  r8: 0000000000000000  r9: 00007ffca3c08070 r10: 0000000000000008 r11: 0000000000000246
 r12: 00007ffca3c09028 r13: 00007ffca3c09030 r14: 00007ffca3c08fd0 r15: 000055f30bad2e48
  di: 0000000000000002  si: 00007ffca3c08070  bp: 00007ffca3c09000  bx: 00007f4daf4d0e00
  dx: 0000000000000000  ax: 0000000000000000  cx: 00007f4db05e518b  sp: 00007ffca3c08070
  ip: 00007f4db05e518b efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Chromium 88.0.4288.0   Channel: n/a
OS Version: 20.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### cl...@chromium.org (2020-10-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5676297261219840.

### wf...@chromium.org (2020-10-29)

Thanks for your report.

[Monorail components: Blink>Canvas Blink>Paint]

### cl...@chromium.org (2020-10-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-10-29)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-10-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-10-30)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/785e9823a06e717fb4e31a345dc58daa24712752 (Create FlushForImageListener in CanvasResourceProvider).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2020-10-30)

Detailed Report: https://clusterfuzz.com/testcase?key=5676297261219840

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7e8ef803d788
Crash State:
  blink::CanvasResourceHost::InitializeForRecording
  blink::CanvasResourceProvider::FlushCanvas
  blink::FlushForImageListener::NotifyFlushForImage
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=793660:793665

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5676297261219840

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5676297261219840 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2020-10-30)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-30)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@chromium.org (2020-10-30)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Paint]

### cl...@chromium.org (2020-10-30)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Paint]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### aa...@chromium.org (2020-11-02)

Assigning to Yi, who's currently on bug rotation.

### cl...@chromium.org (2020-11-02)

Detailed Report: https://clusterfuzz.com/testcase?key=5676297261219840

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7e8ef803d788
Crash State:
  blink::CanvasResourceHost::InitializeForRecording
  blink::CanvasResourceProvider::FlushCanvas
  blink::FlushForImageListener::NotifyFlushForImage
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=793660:793665

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5676297261219840

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5676297261219840 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### yi...@chromium.org (2020-11-03)

[Empty comment from Monorail migration]

### yi...@chromium.org (2020-11-03)

[Empty comment from Monorail migration]

### yi...@chromium.org (2020-11-04)

[Comment Deleted]

### yi...@chromium.org (2020-11-04)

[Comment Deleted]

### yi...@chromium.org (2020-11-05)

[Comment Deleted]

### yi...@chromium.org (2020-11-05)

[Empty comment from Monorail migration]

### yi...@chromium.org (2020-11-09)

adding webassembly folks. 

If we remove the line new WebAssembly.Memory({initial: 64}).grow(1); from the html file, there is no crashes. If I reduce 64 to 32, there is no crashes. After ruling out every possible bugs in canvas, I suspect there is some problem with web assembly and canvas working together. Could you please investigate this bug on your side as well? Thank you very much

### yi...@chromium.org (2020-11-10)

The address that is poisoned is the CanvasResourceHost. In our code, we have successfully initialized the class, the dtor for CanvasResourceHost is not called. When we try to call CanvasResourceHost::InitializeForRecording, the sanitizer throws out the error that address is poison for the class CanvasResourceHost. 

I suspect that the memory address is also used by web assembly or some other program. So that it's poisoned. I tried to verify this callback before its usage, but callback.MaybeValid always returns true. Please provide some insights on this issue! I am out of ideas for fixing it. Thank you so much for the help


### ec...@chromium.org (2020-11-11)

The issue can be reproduced with plain JS objects, not using Wasm:
```
let canvas = document.createElement('canvas');
function main(canvas) {
var off_canvas=new OffscreenCanvas(80, 80);
var ctx=off_canvas.getContext('2d');
new ArrayBuffer(1024*1024*1024);
ctx.drawImage(canvas, 5, 5);
let ctx2=canvas.getContext('2d');
ctx2.drawImage(canvas, 5, 5);
};
for (let i=0; i<100; ++i)
main(canvas);
```
It seems that the poisoning of memory can be done by any object exposing the faulty memory access.

### yi...@chromium.org (2020-11-11)

 ecmziegler@ is correct. removing web assembly team from the cc list. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d0cbe5dfa883b6dd7a0827f5881ae5cee4f06cbd

commit d0cbe5dfa883b6dd7a0827f5881ae5cee4f06cbd
Author: yiyix <yiyix@chromium.org>
Date: Wed Nov 11 19:32:30 2020

Fix poison address in blink::CanvasResourceHost::InitializeForRecording

After allocate a large buffer in memory and creating canvas, it will
trigger the garbage collection from v8, which will trigger
offscreenCanvas::Dispose to be called. This call will cause the
offscreencanvas detached from the |host|. However the |host| is saved
as a valid callback in the observer list of the canvas resource
provider. Calling this |host| without offscreencanvas causes this access
to poison address.

In my fix, after garbage collection is triggered and dispose is called,
DiscardResourceProvider() is called as well, so it removes itself from
the observer list.

Bug: 1143662
Change-Id: I82c9a1f70c117b03de9fb64f4849c1f3c4311d1a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2531136
Reviewed-by: Juanmi Huertas <juanmihd@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Yi Xu <yiyix@chromium.org>
Cr-Commit-Position: refs/heads/master@{#826391}

[modify] https://crrev.com/d0cbe5dfa883b6dd7a0827f5881ae5cee4f06cbd/third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc


### yi...@chromium.org (2020-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-11)

This bug requires manual review: We don't branch M88 until 2020-11-12.
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
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yi...@chromium.org (2020-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-11)

This bug requires manual review: We are only 5 days from stable.
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

### la...@google.com (2020-11-11)

yiyix@ - please fill the questionnaire in c#30 to consider the merge request.

### rs...@chromium.org (2020-11-12)

Looks like Clusterfuzz didn’t correctly assign the impact label. The regressing CL is in 85.0.4183.54, so this should affect stable.

### ad...@google.com (2020-11-12)

yiyix@ please also mark this as Fixed if it is. For security bugs, we mark as Fixed before doing all the merge processes.

### ad...@google.com (2020-11-12)

[Empty comment from Monorail migration]

### yi...@chromium.org (2020-11-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-11-12)

Detailed Report: https://clusterfuzz.com/testcase?key=5676297261219840

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7e8ef803d788
Crash State:
  blink::CanvasResourceHost::InitializeForRecording
  blink::CanvasResourceProvider::FlushCanvas
  blink::FlushForImageListener::NotifyFlushForImage
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=793660:793665

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5676297261219840

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5676297261219840 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2020-11-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-12)

It looks like M87 may be delayed, so adding a merge request for M86 for consideration.

yiyix@ please act upon https://crbug.com/chromium/1143662#c30, https://crbug.com/chromium/1143662#c31. The main thing we need to know about is whether there's any stability risk from merging back to stable without the normal weeks of end-user testing on beta, dev, etc.

### cl...@chromium.org (2020-11-12)

ClusterFuzz testcase 5676297261219840 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=826382:826405

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### yi...@chromium.org (2020-11-12)

1. Does your merge fit within the Merge Decision Guidelines?
Yes, I have asked  rsesek
2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2531136
3. Has the change landed and been verified on ToT?
yes
4. Does this change need to be merged into other active release branches (M-1, M+1)?
yes, the regression cl happened in m85, so any release after needs to be merged
5. Why are these changes required in this milestone after branch?
it is a security bug, the severity is marked high
6. Is this a new feature?
no
7. If it is a new feature, is it behind a flag using finch?
n/a

### yi...@chromium.org (2020-11-12)

sorry, i am waiting for the clusterfuzz verified label to appear before stating it's verified. 

### ad...@google.com (2020-11-13)

There's likely to be another M86 release after all, so approving merge to M86. Please merge to branch 4240 if there is no sign of trouble from Canary. Also approving merge to M87, branch 4280.

### go...@chromium.org (2020-11-13)

Please merge your change to M86 branch 4240 before 12:30 PM PDT, Friday, Nov 13th so we can take it in for M86 respin.Thank you. 

### [Deleted User] (2020-11-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b816df595a886ce56694f133ee06cc9f9500375a

commit b816df595a886ce56694f133ee06cc9f9500375a
Author: yiyix <yiyix@chromium.org>
Date: Fri Nov 13 22:15:50 2020

Fix poison address in blink::CanvasResourceHost::InitializeForRecording

After allocate a large buffer in memory and creating canvas, it will
trigger the garbage collection from v8, which will trigger
offscreenCanvas::Dispose to be called. This call will cause the
offscreencanvas detached from the |host|. However the |host| is saved
as a valid callback in the observer list of the canvas resource
provider. Calling this |host| without offscreencanvas causes this access
to poison address.

In my fix, after garbage collection is triggered and dispose is called,
DiscardResourceProvider() is called as well, so it removes itself from
the observer list.

(cherry picked from commit d0cbe5dfa883b6dd7a0827f5881ae5cee4f06cbd)

Bug: 1143662
Change-Id: I82c9a1f70c117b03de9fb64f4849c1f3c4311d1a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2531136
Reviewed-by: Juanmi Huertas <juanmihd@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Yi Xu <yiyix@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#826391}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2538172
Reviewed-by: Yi Xu <yiyix@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1400}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/b816df595a886ce56694f133ee06cc9f9500375a/third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/37dea8ff8afa702fdd02374cd6eb35f230d730b0

commit 37dea8ff8afa702fdd02374cd6eb35f230d730b0
Author: yiyix <yiyix@chromium.org>
Date: Fri Nov 13 22:45:01 2020

Fix poison address in blink::CanvasResourceHost::InitializeForRecording

After allocate a large buffer in memory and creating canvas, it will
trigger the garbage collection from v8, which will trigger
offscreenCanvas::Dispose to be called. This call will cause the
offscreencanvas detached from the |host|. However the |host| is saved
as a valid callback in the observer list of the canvas resource
provider. Calling this |host| without offscreencanvas causes this access
to poison address.

In my fix, after garbage collection is triggered and dispose is called,
DiscardResourceProvider() is called as well, so it removes itself from
the observer list.

(cherry picked from commit d0cbe5dfa883b6dd7a0827f5881ae5cee4f06cbd)

Bug: 1143662
Change-Id: I82c9a1f70c117b03de9fb64f4849c1f3c4311d1a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2531136
Reviewed-by: Juanmi Huertas <juanmihd@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Yi Xu <yiyix@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#826391}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2536994
Auto-Submit: Yi Xu <yiyix@chromium.org>
Reviewed-by: Yi Xu <yiyix@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1456}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/37dea8ff8afa702fdd02374cd6eb35f230d730b0/third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc


### yi...@chromium.org (2020-11-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7cd1ce59d2b2ab3de986e780200e2c5c1f8df78e

commit 7cd1ce59d2b2ab3de986e780200e2c5c1f8df78e
Author: yiyix <yiyix@chromium.org>
Date: Wed Nov 18 08:33:24 2020

Fix poison address in blink::CanvasResourceHost::InitializeForRecording

After allocate a large buffer in memory and creating canvas, it will
trigger the garbage collection from v8, which will trigger
offscreenCanvas::Dispose to be called. This call will cause the
offscreencanvas detached from the |host|. However the |host| is saved
as a valid callback in the observer list of the canvas resource
provider. Calling this |host| without offscreencanvas causes this access
to poison address.

In my fix, after garbage collection is triggered and dispose is called,
DiscardResourceProvider() is called as well, so it removes itself from
the observer list.

(cherry picked from commit d0cbe5dfa883b6dd7a0827f5881ae5cee4f06cbd)

(cherry picked from commit 37dea8ff8afa702fdd02374cd6eb35f230d730b0)

Bug: 1143662
Change-Id: I82c9a1f70c117b03de9fb64f4849c1f3c4311d1a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2531136
Reviewed-by: Juanmi Huertas <juanmihd@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Yi Xu <yiyix@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#826391}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2536994
Auto-Submit: Yi Xu <yiyix@chromium.org>
Reviewed-by: Yi Xu <yiyix@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4240@{#1456}
Cr-Original-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2544704
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240_112@{#28}
Cr-Branched-From: 427c00d3874b6abcf4c4c2719768835fc3ef26d6-refs/branch-heads/4240@{#1291}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/7cd1ce59d2b2ab3de986e780200e2c5c1f8df78e/third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc


### ad...@google.com (2020-11-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-18)

Congratulations, the VRP panel has awarded $5,000 for this bug.

### ad...@google.com (2020-11-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7cd1ce59d2b2ab3de986e780200e2c5c1f8df78e

commit 7cd1ce59d2b2ab3de986e780200e2c5c1f8df78e
Author: yiyix <yiyix@chromium.org>
Date: Wed Nov 18 08:33:24 2020

Fix poison address in blink::CanvasResourceHost::InitializeForRecording

After allocate a large buffer in memory and creating canvas, it will
trigger the garbage collection from v8, which will trigger
offscreenCanvas::Dispose to be called. This call will cause the
offscreencanvas detached from the |host|. However the |host| is saved
as a valid callback in the observer list of the canvas resource
provider. Calling this |host| without offscreencanvas causes this access
to poison address.

In my fix, after garbage collection is triggered and dispose is called,
DiscardResourceProvider() is called as well, so it removes itself from
the observer list.

(cherry picked from commit d0cbe5dfa883b6dd7a0827f5881ae5cee4f06cbd)

(cherry picked from commit 37dea8ff8afa702fdd02374cd6eb35f230d730b0)

Bug: 1143662
Change-Id: I82c9a1f70c117b03de9fb64f4849c1f3c4311d1a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2531136
Reviewed-by: Juanmi Huertas <juanmihd@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Yi Xu <yiyix@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#826391}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2536994
Auto-Submit: Yi Xu <yiyix@chromium.org>
Reviewed-by: Yi Xu <yiyix@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4240@{#1456}
Cr-Original-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2544704
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240_112@{#28}
Cr-Branched-From: 427c00d3874b6abcf4c4c2719768835fc3ef26d6-refs/branch-heads/4240@{#1291}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/7cd1ce59d2b2ab3de986e780200e2c5c1f8df78e/third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc


### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-02-19)

This issue was migrated from crbug.com/chromium/1143662?no_tracker_redirect=1

[Multiple monorail components: Blink>Canvas, Blink>Paint]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053738)*
