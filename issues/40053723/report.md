# uaf in VideoFrame::CreateImageBitmap

| Field | Value |
|-------|-------|
| **Issue ID** | [40053723](https://issues.chromium.org/issues/40053723) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>WebCodecs |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2020-10-27 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36

Steps to reproduce the problem:
Chromium 88.0.4305.0(asan build)
1.python3.6m -m http.server 8000
2./chrome --enable-experimental-web-platform-features http://localhost:8000/crash.html

3.

What is the expected behavior?

What went wrong?
[3310358:3310358:1027/102901.122636:ERROR:sandbox_linux.cc(374)] InitializeSandbox() called with multiple threads in process gpu-process.
[3310358:3310358:1027/102901.456350:ERROR:shared_image_backing_gl_texture.cc(438)] CreateSharedImage: invalid size
[3310358:3310358:1027/102901.456516:ERROR:shared_image_factory.cc(553)] CreateSharedImage: could not create backing.
[3310358:3310358:1027/102901.456621:ERROR:shared_image_stub.cc(201)] SharedImageStub: Unable to create shared image
=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6070000503c0 at pc 0x56064c689d41 bp 0x7ffe45d10110 sp 0x7ffe45d10108
READ of size 8 at 0x6070000503c0 thread T0 (chrome)
    #0 0x56064c689d40 in base::internal::Invoker<base::internal::BindState<blink::VideoFrame::CreateImageBitmap(blink::ScriptState*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&)::$_0, base::internal::UnretainedWrapper<gpu::SharedImageInterface>, gpu::Mailbox>, void (gpu::SyncToken const&, bool)>::RunOnce(base::internal::BindStateBase*, gpu::SyncToken const&, bool) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:418
    #1 0x56064c689d40 in Invoke<(lambda at ../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:416:11), gpu::SharedImageInterface *, gpu::Mailbox, const gpu::SyncToken &, bool> ./../../base/bind_internal.h:379
    #2 0x56064c689d40 in MakeItSo<(lambda at ../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:416:11), gpu::SharedImageInterface *, gpu::Mailbox, const gpu::SyncToken &, bool> ./../../base/bind_internal.h:637
    #3 0x56064c689d40 in RunImpl<(lambda at ../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:416:11), std::__1::tuple<base::internal::UnretainedWrapper<gpu::SharedImageInterface>, gpu::Mailbox>, 0, 1> ./../../base/bind_internal.h:710
    #4 0x56064c689d40 in RunOnce ./../../base/bind_internal.h:679
    #5 0x56064c689d40 in ?? ??:0
    #6 0x56063e7b7852 in viz::SingleReleaseCallback::Run(gpu::SyncToken const&, bool) ./../../base/callback.h:101
    #7 0x56063e7b7852 in Run ./../../components/viz/common/resources/single_release_callback.cc:24
    #8 0x56063e7b7852 in ?? ??:0
    #9 0x560648c106d4 in blink::MailboxRef::~MailboxRef() ./../../third_party/blink/renderer/platform/graphics/mailbox_ref.cc:21
    #10 0x560648c106d4 in ~MailboxRef ./../../third_party/blink/renderer/platform/graphics/mailbox_ref.cc:40
    #11 0x560648c106d4 in ?? ??:0
    #12 0x560648b174a8 in blink::AcceleratedStaticBitmapImage::~AcceleratedStaticBitmapImage() ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:64
    #13 0x560648b174a8 in Destruct ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:44
    #14 0x560648b174a8 in Release ./../../base/memory/ref_counted.h:400
    #15 0x560648b174a8 in Release ./../../base/memory/scoped_refptr.h:322
    #16 0x560648b174a8 in ~scoped_refptr ./../../base/memory/scoped_refptr.h:224
    #17 0x560648b174a8 in ~AcceleratedStaticBitmapImage ./../../third_party/blink/renderer/platform/graphics/accelerated_static_bitmap_image.cc:98
    #18 0x560648b174a8 in ?? ??:0
    #19 0x560648b1757d in blink::AcceleratedStaticBitmapImage::~AcceleratedStaticBitmapImage() ./../../third_party/blink/renderer/platform/graphics/accelerated_static_bitmap_image.cc:96
    #20 0x560648b1757d in ?? ??:0
    #21 0x56064c686ed1 in blink::VideoFrame::CreateImageBitmap(blink::ScriptState*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:64
    #22 0x56064c686ed1 in Destruct ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:44
    #23 0x56064c686ed1 in Release ./../../base/memory/ref_counted.h:400
    #24 0x56064c686ed1 in Release ./../../base/memory/scoped_refptr.h:322
    #25 0x56064c686ed1 in ~scoped_refptr ./../../base/memory/scoped_refptr.h:224
    #26 0x56064c686ed1 in CreateImageBitmap ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:444
    #27 0x56064c686ed1 in ?? ??:0
    #28 0x56064c687819 in non-virtual thunk to blink::VideoFrame::CreateImageBitmap(blink::ScriptState*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:?
    #29 0x56064c687819 in ?? ??:0
    #30 0x56064c68bb30 in blink::ImageBitmapFactories::CreateImageBitmap(blink::ScriptState*, blink::ImageBitmapSource*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/core/imagebitmap/image_bitmap_factories.cc:204
    #31 0x56064c68bb30 in ?? ??:0
    #32 0x56064c6847ed in blink::VideoFrame::createImageBitmap(blink::ScriptState*, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:318
    #33 0x56064c6847ed in ?? ??:0
    #34 0x56064c67f97a in blink::(anonymous namespace)::CreateImageBitmapOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_video_frame.cc:334
    #35 0x56064c67f97a in ?? ??:0
    #36 0x560636d0619a in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #37 0x560636d0619a in ?? ??:0
    #38 0x560636d03cf5 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111
    #39 0x560636d03cf5 in ?? ??:0
    #40 0x560636d0186e in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:141
    #41 0x560636d0186e in ?? ??:0
    #42 0x560638e50457 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #43 0x560638e50457 in ?? ??:0
    #44 0x560638de0f97 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #45 0x560638de0f97 in ?? ??:0
    #46 0x560638ea09fa in Builtins_PromiseFulfillReactionJob setup-isolate-deserialize.cc:?
    #47 0x560638ea09fa in ?? ??:0
    #48 0x560638e020d6 in Builtins_RunMicrotasks setup-isolate-deserialize.cc:?
    #49 0x560638e020d6 in ?? ??:0
    #50 0x560638ddea17 in Builtins_JSRunMicrotasksEntry setup-isolate-deserialize.cc:?
    #51 0x560638ddea17 in ?? ??:0
    #52 0x560636fa8c38 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/simulator.h:142
    #53 0x560636fa8c38 in Invoke ./../../v8/src/execution/execution.cc:383
    #54 0x560636fa8c38 in ?? ??:0
    #55 0x560636fac708 in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:428
    #56 0x560636fac708 in ?? ??:0
    #57 0x560636facb58 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*, v8::internal::MaybeHandle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:505
    #58 0x560636facb58 in ?? ??:0
    #59 0x5606370348d2 in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) ./../../v8/src/execution/microtask-queue.cc:165
    #60 0x5606370348d2 in ?? ??:0
    #61 0x5606370342c5 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate*) ./../../v8/src/execution/microtask-queue.cc:117
    #62 0x5606370342c5 in ?? ??:0
    #63 0x56064860cbaa in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:363
    #64 0x56064860cbaa in ?? ??:0
    #65 0x56064860dc59 in blink::V8ScriptRunner::CompileAndRunScript(v8::Isolate*, blink::ScriptState*, blink::ExecutionContext*, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::mojom::V8CacheOptions, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:440
    #66 0x56064860dc59 in ?? ??:0
    #67 0x56064854efc9 in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local<v8::Context>, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:100
    #68 0x56064854efc9 in ?? ??:0
    #69 0x560648551d30 in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:298
    #70 0x560648551d30 in ?? ??:0
    #71 0x560647f0a475 in blink::ClassicScript::RunScript(blink::LocalDOMWindow*) ./../../third_party/blink/renderer/core/script/classic_script.cc:42
    #72 0x560647f0a475 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:36
    #73 0x560647f0a475 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:29
    #74 0x560647f0a475 in ?? ??:0
    #75 0x560647f5a8fd in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) ./../../third_party/blink/renderer/core/script/pending_script.cc:264
    #76 0x560647f5a8fd in ?? ??:0
    #77 0x560647f5a211 in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third_party/blink/renderer/core/script/pending_script.cc:170
    #78 0x560647f5a211 in ?? ??:0
    #79 0x560647f51803 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third_party/blink/renderer/core/script/script_loader.cc:915
    #80 0x560647f51803 in ?? ??:0
    #81 0x5606492b81eb in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:609
    #82 0x5606492b81eb in ?? ??:0
    #83 0x5606492b7d9b in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:332
    #84 0x5606492b7d9b in ?? ??:0
    #85 0x56064926e833 in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:539
    #86 0x56064926e833 in ?? ??:0
    #87 0x56064927241a in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::__1::unique_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::__1::default_delete<blink::HTMLDocumentParser::TokenizedChunk> >, bool*) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:780
    #88 0x56064927241a in ?? ??:0
    #89 0x56064926e0dd in blink::HTMLDocumentParser::PumpPendingSpeculations() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:840
    #90 0x56064926e0dd in ?? ??:0
    #91 0x56064926da7e in blink::HTMLDocumentParser::ResumeParsingAfterYield() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:526
    #92 0x56064926da7e in ?? ??:0
    #93 0x560638fa5f91 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) ./../../base/callback.h:101
    #94 0x560638fa5f91 in Run ./../../third_party/blink/renderer/platform/scheduler/common/post_cancellable_task.cc:47
    #95 0x560638fa5f91 in ?? ??:0
    #96 0x560638fa6f66 in base::internal::Invoker<base::internal::BindState<void (blink::TaskHandle::Runner::*)(blink::TaskHandle const&), base::WeakPtr<blink::TaskHandle::Runner>, blink::TaskHandle>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:498
    #97 0x560638fa6f66 in MakeItSo<void (blink::TaskHandle::Runner::*)(const blink::TaskHandle &), base::WeakPtr<blink::TaskHandle::Runner>, blink::TaskHandle> ./../../base/bind_internal.h:657
    #98 0x560638fa6f66 in RunImpl<void (blink::TaskHandle::Runner::*)(const blink::TaskHandle &), std::__1::tuple<base::WeakPtr<blink::TaskHandle::Runner>, blink::TaskHandle>, 0, 1> ./../../base/bind_internal.h:710
    #99 0x560638fa6f66 in RunOnce ./../../base/bind_internal.h:679
    #100 0x560638fa6f66 in ?? ??:0
    #101 0x56063a1ec7d5 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:101
    #102 0x56063a1ec7d5 in RunTask ./../../base/task/common/task_annotator.cc:163
    #103 0x56063a1ec7d5 in ?? ??:0
    #104 0x56063a225660 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332
    #105 0x56063a225660 in ?? ??:0
    #106 0x56063a224dbf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:252
    #107 0x56063a224dbf in ?? ??:0
    #108 0x56063a118170 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #109 0x56063a118170 in ?? ??:0
    #110 0x56063a227476 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:446
    #111 0x56063a227476 in ?? ??:0
    #112 0x56063a199d3a in base::RunLoop::Run() ./../../base/run_loop.cc:124
    #113 0x56063a199d3a in ?? ??:0
    #114 0x56064d595fa8 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:256
    #115 0x56064d595fa8 in ?? ??:0
    #116 0x560639ef916f in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:498
    #117 0x560639ef916f in ?? ??:0
    #118 0x560639efc59d in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:882
    #119 0x560639efc59d in ?? ??:0
    #120 0x560639ef608c in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #121 0x560639ef608c in ?? ??:0
    #122 0x560639ef668c in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #123 0x560639ef668c in ?? ??:0
    #124 0x56062f336615 in ChromeMain ./../../chrome/app/chrome_main.cc:130
    #125 0x56062f336615 in ?? ??:0
    #126 0x7ff78b7260b2 in __libc_start_main ??:?
    #127 0x7ff78b7260b2 in ?? ??:0

0x6070000503c0 is located 0 bytes inside of 80-byte region [0x6070000503c0,0x607000050410)
freed by thread T0 (chrome) here:
    #0 0x56062f33436d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160
    #1 0x56062f33436d in ?? ??:0
    #2 0x56063505bc1e in viz::ContextProviderCommandBuffer::~ContextProviderCommandBuffer() ./../../buildtools/third_party/libc++/trunk/include/memory:2378
    #3 0x56063505bc1e in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633
    #4 0x56063505bc1e in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/memory:2587
    #5 0x56063505bc1e in ~ContextProviderCommandBuffer ./../../services/viz/public/cpp/gpu/context_provider_command_buffer.cc:99
    #6 0x56063505bc1e in ?? ??:0
    #7 0x56063505bf3d in viz::ContextProviderCommandBuffer::~ContextProviderCommandBuffer() ./../../services/viz/public/cpp/gpu/context_provider_command_buffer.cc:86
    #8 0x56063505bf3d in ?? ??:0
    #9 0x56064c68684b in blink::VideoFrame::CreateImageBitmap(blink::ScriptState*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../base/memory/scoped_refptr.h:322
    #10 0x56064c68684b in ~scoped_refptr ./../../base/memory/scoped_refptr.h:224
    #11 0x56064c68684b in CreateImageBitmap ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:438
    #12 0x56064c68684b in ?? ??:0
    #13 0x56064c687819 in non-virtual thunk to blink::VideoFrame::CreateImageBitmap(blink::ScriptState*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:?
    #14 0x56064c687819 in ?? ??:0
    #15 0x56064c68bb30 in blink::ImageBitmapFactories::CreateImageBitmap(blink::ScriptState*, blink::ImageBitmapSource*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/core/imagebitmap/image_bitmap_factories.cc:204
    #16 0x56064c68bb30 in ?? ??:0
    #17 0x56064c6847ed in blink::VideoFrame::createImageBitmap(blink::ScriptState*, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:318
    #18 0x56064c6847ed in ?? ??:0
    #19 0x56064c67f97a in blink::(anonymous namespace)::CreateImageBitmapOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_video_frame.cc:334
    #20 0x56064c67f97a in ?? ??:0
    #21 0x560636d0619a in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #22 0x560636d0619a in ?? ??:0
    #23 0x560636d03cf5 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111
    #24 0x560636d03cf5 in ?? ??:0
    #25 0x560636d0186e in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:141
    #26 0x560636d0186e in ?? ??:0
    #27 0x560638e50457 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #28 0x560638e50457 in ?? ??:0
    #29 0x560638de0f97 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #30 0x560638de0f97 in ?? ??:0
    #31 0x560638ea09fa in Builtins_PromiseFulfillReactionJob setup-isolate-deserialize.cc:?
    #32 0x560638ea09fa in ?? ??:0
    #33 0x560638e020d6 in Builtins_RunMicrotasks setup-isolate-deserialize.cc:?
    #34 0x560638e020d6 in ?? ??:0
    #35 0x560638ddea17 in Builtins_JSRunMicrotasksEntry setup-isolate-deserialize.cc:?
    #36 0x560638ddea17 in ?? ??:0
    #37 0x560636fa8c38 in Call ./../../v8/src/execution/simulator.h:142
    #38 0x560636fa8c38 in Invoke ./../../v8/src/execution/execution.cc:383
    #39 0x560636fa8c38 in ?? ??:0
    #40 0x560636fac708 in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:428
    #41 0x560636fac708 in ?? ??:0
    #42 0x560636facb58 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*, v8::internal::MaybeHandle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:505
    #43 0x560636facb58 in ?? ??:0
    #44 0x5606370348d2 in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) ./../../v8/src/execution/microtask-queue.cc:165
    #45 0x5606370348d2 in ?? ??:0
    #46 0x5606370342c5 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate*) ./../../v8/src/execution/microtask-queue.cc:117
    #47 0x5606370342c5 in ?? ??:0
    #48 0x56064860cbaa in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:363
    #49 0x56064860cbaa in ?? ??:0
    #50 0x56064860dc59 in blink::V8ScriptRunner::CompileAndRunScript(v8::Isolate*, blink::ScriptState*, blink::ExecutionContext*, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::mojom::V8CacheOptions, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:440
    #51 0x56064860dc59 in ?? ??:0
    #52 0x56064854efc9 in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local<v8::Context>, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:100
    #53 0x56064854efc9 in ?? ??:0
    #54 0x560648551d30 in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:298
    #55 0x560648551d30 in ?? ??:0
    #56 0x560647f0a475 in RunScriptAndReturnValue ./../../third_party/blink/renderer/core/script/classic_script.cc:42
    #57 0x560647f0a475 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:36
    #58 0x560647f0a475 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:29
    #59 0x560647f0a475 in ?? ??:0
    #60 0x560647f5a8fd in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) ./../../third_party/blink/renderer/core/script/pending_script.cc:264
    #61 0x560647f5a8fd in ?? ??:0
    #62 0x560647f5a211 in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third_party/blink/renderer/core/script/pending_script.cc:170
    #63 0x560647f5a211 in ?? ??:0
    #64 0x560647f51803 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third_party/blink/renderer/core/script/script_loader.cc:915
    #65 0x560647f51803 in ?? ??:0
    #66 0x5606492b81eb in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:609
    #67 0x5606492b81eb in ?? ??:0

previously allocated by thread T0 (chrome) here:
    #0 0x56062f333b0d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99
    #1 0x56062f333b0d in ?? ??:0
    #2 0x56063153ce60 in gpu::GpuChannelHost::CreateClientSharedImageInterface() ./../../buildtools/third_party/libc++/trunk/include/memory:3043
    #3 0x56063153ce60 in CreateClientSharedImageInterface ./../../gpu/ipc/client/gpu_channel_host.cc:255
    #4 0x56063153ce60 in ?? ??:0
    #5 0x56063505d978 in viz::ContextProviderCommandBuffer::BindToCurrentThread() ./../../services/viz/public/cpp/gpu/context_provider_command_buffer.cc:332
    #6 0x56063505d978 in ?? ??:0
    #7 0x56064d54b363 in content::RenderThreadImpl::SharedMainThreadContextProvider() ./../../content/renderer/render_thread_impl.cc:1224
    #8 0x56064d54b363 in ?? ??:0
    #9 0x56064d58a172 in content::RendererBlinkPlatformImpl::SharedMainThreadContextProvider() ./../../content/renderer/renderer_blink_platform_impl.cc:522
    #10 0x56064d58a172 in ?? ??:0
    #11 0x56064c6858bd in blink::VideoFrame::CreateImageBitmap(blink::ScriptState*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:381
    #12 0x56064c6858bd in ?? ??:0
    #13 0x56064c687819 in non-virtual thunk to blink::VideoFrame::CreateImageBitmap(blink::ScriptState*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:?
    #14 0x56064c687819 in ?? ??:0
    #15 0x56064c68bb30 in blink::ImageBitmapFactories::CreateImageBitmap(blink::ScriptState*, blink::ImageBitmapSource*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/core/imagebitmap/image_bitmap_factories.cc:204
    #16 0x56064c68bb30 in ?? ??:0
    #17 0x56064c6847ed in blink::VideoFrame::createImageBitmap(blink::ScriptState*, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:318
    #18 0x56064c6847ed in ?? ??:0
    #19 0x56064c67f97a in blink::(anonymous namespace)::CreateImageBitmapOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_video_frame.cc:334
    #20 0x56064c67f97a in ?? ??:0
    #21 0x560636d0619a in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #22 0x560636d0619a in ?? ??:0
    #23 0x560636d03cf5 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111
    #24 0x560636d03cf5 in ?? ??:0
    #25 0x560636d0186e in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:141
    #26 0x560636d0186e in ?? ??:0
    #27 0x560638e50457 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #28 0x560638e50457 in ?? ??:0
    #29 0x560638de0f97 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #30 0x560638de0f97 in ?? ??:0
    #31 0x560638ea09fa in Builtins_PromiseFulfillReactionJob setup-isolate-deserialize.cc:?
    #32 0x560638ea09fa in ?? ??:0
    #33 0x560638e020d6 in Builtins_RunMicrotasks setup-isolate-deserialize.cc:?
    #34 0x560638e020d6 in ?? ??:0
    #35 0x560638ddea17 in Builtins_JSRunMicrotasksEntry setup-isolate-deserialize.cc:?
    #36 0x560638ddea17 in ?? ??:0
    #37 0x560636fa8c38 in Call ./../../v8/src/execution/simulator.h:142
    #38 0x560636fa8c38 in Invoke ./../../v8/src/execution/execution.cc:383
    #39 0x560636fa8c38 in ?? ??:0
    #40 0x560636fac708 in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:428
    #41 0x560636fac708 in ?? ??:0
    #42 0x560636facb58 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*, v8::internal::MaybeHandle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:505
    #43 0x560636facb58 in ?? ??:0
    #44 0x5606370348d2 in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) ./../../v8/src/execution/microtask-queue.cc:165
    #45 0x5606370348d2 in ?? ??:0
    #46 0x5606370342c5 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate*) ./../../v8/src/execution/microtask-queue.cc:117
    #47 0x5606370342c5 in ?? ??:0
    #48 0x56064860cbaa in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:363
    #49 0x56064860cbaa in ?? ??:0
    #50 0x56064860dc59 in blink::V8ScriptRunner::CompileAndRunScript(v8::Isolate*, blink::ScriptState*, blink::ExecutionContext*, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::mojom::V8CacheOptions, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:440
    #51 0x56064860dc59 in ?? ??:0
    #52 0x56064854efc9 in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local<v8::Context>, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:100
    #53 0x56064854efc9 in ?? ??:0
    #54 0x560648551d30 in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:298
    #55 0x560648551d30 in ?? ??:0
    #56 0x560647f0a475 in RunScriptAndReturnValue ./../../third_party/blink/renderer/core/script/classic_script.cc:42
    #57 0x560647f0a475 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:36
    #58 0x560647f0a475 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:29
    #59 0x560647f0a475 in ?? ??:0
    #60 0x560647f5a8fd in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) ./../../third_party/blink/renderer/core/script/pending_script.cc:264
    #61 0x560647f5a8fd in ?? ??:0
    #62 0x560647f5a211 in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third_party/blink/renderer/core/script/pending_script.cc:170
    #63 0x560647f5a211 in ?? ??:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/test/asan-linux-release/chrome+0x2759cd40)
Shadow bytes around the buggy address:
  0x0c0e80002020: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa
  0x0c0e80002030: fa fa fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c0e80002040: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fd fd
  0x0c0e80002050: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd
  0x0c0e80002060: fd fd fd fd fd fa fa fa fa fa fd fd fd fd fd fd
=>0x0c0e80002070: fd fd fd fa fa fa fa fa[fd]fd fd fd fd fd fd fd
  0x0c0e80002080: fd fd fa fa fa fa fd fd fd fd fd fd fd fd fd fa
  0x0c0e80002090: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa
  0x0c0e800020a0: fa fa fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c0e800020b0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fd fd
  0x0c0e800020c0: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd
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
    #0 0x56062f2c6b3b in __interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4176
    #1 0x56062f2c6b3b in ?? ??:0
    #2 0x56063a2d0c89 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:833
    #3 0x56063a2d0c89 in ?? ??:0
    #4 0x56063a0c6773 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:198
    #5 0x56063a0c6773 in StackTrace ./../../base/debug/stack_trace.cc:195
    #6 0x56063a0c6773 in ?? ??:0
    #7 0x56063a2cf87e in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:345
    #8 0x56063a2cf87e in ?? ??:0
    #9 0x7ff78d3a53c0 in __funlockfile :?
    #10 0x7ff78d3a53c0 in ?? ??:0
    #11 0x7ff78b74518b in gsignal ??:?
    #12 0x7ff78b74518b in ?? ??:0
    #13 0x7ff78b724859 in abort ??:?
    #14 0x7ff78b724859 in ?? ??:0
    #15 0x56062f323007 in __sanitizer::Abort() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cpp:152
    #16 0x56062f323007 in ?? ??:0
    #17 0x56062f321b81 in __sanitizer::Die() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cpp:58
    #18 0x56062f321b81 in ?? ??:0
    #19 0x56062f30e1c4 in __asan::ScopedInErrorReport::~ScopedInErrorReport() /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:189
    #20 0x56062f30e1c4 in ?? ??:0
    #21 0x56062f30fbae in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:477
    #22 0x56062f30fbae in ?? ??:0
    #23 0x56062f310438 in __asan_report_load8 /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_rtl.cpp:120
    #24 0x56062f310438 in ?? ??:0
    #25 0x56064c689d41 in operator() ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:418
    #26 0x56064c689d41 in Invoke<(lambda at ../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:416:11), gpu::SharedImageInterface *, gpu::Mailbox, const gpu::SyncToken &, bool> ./../../base/bind_internal.h:379
    #27 0x56064c689d41 in MakeItSo<(lambda at ../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:416:11), gpu::SharedImageInterface *, gpu::Mailbox, const gpu::SyncToken &, bool> ./../../base/bind_internal.h:637
    #28 0x56064c689d41 in RunImpl<(lambda at ../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:416:11), std::__1::tuple<base::internal::UnretainedWrapper<gpu::SharedImageInterface>, gpu::Mailbox>, 0, 1> ./../../base/bind_internal.h:710
    #29 0x56064c689d41 in RunOnce ./../../base/bind_internal.h:679
    #30 0x56064c689d41 in ?? ??:0
    #31 0x56063e7b7853 in Run ./../../base/callback.h:101
    #32 0x56063e7b7853 in Run ./../../components/viz/common/resources/single_release_callback.cc:24
    #33 0x56063e7b7853 in ?? ??:0
    #34 0x560648c106d5 in ReleaseCallbackOnContextThread ./../../third_party/blink/renderer/platform/graphics/mailbox_ref.cc:21
    #35 0x560648c106d5 in ~MailboxRef ./../../third_party/blink/renderer/platform/graphics/mailbox_ref.cc:40
    #36 0x560648c106d5 in ?? ??:0
    #37 0x560648b174a9 in DeleteInternal<blink::MailboxRef> ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:64
    #38 0x560648b174a9 in Destruct ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:44
    #39 0x560648b174a9 in Release ./../../base/memory/ref_counted.h:400
    #40 0x560648b174a9 in Release ./../../base/memory/scoped_refptr.h:322
    #41 0x560648b174a9 in ~scoped_refptr ./../../base/memory/scoped_refptr.h:224
    #42 0x560648b174a9 in ~AcceleratedStaticBitmapImage ./../../third_party/blink/renderer/platform/graphics/accelerated_static_bitmap_image.cc:98
    #43 0x560648b174a9 in ?? ??:0
    #44 0x560648b1757e in blink::AcceleratedStaticBitmapImage::~AcceleratedStaticBitmapImage() ./../../third_party/blink/renderer/platform/graphics/accelerated_static_bitmap_image.cc:96
    #45 0x560648b1757e in ?? ??:0
    #46 0x56064c686ed2 in DeleteInternal<blink::Image> ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:64
    #47 0x56064c686ed2 in Destruct ./../../third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:44
    #48 0x56064c686ed2 in Release ./../../base/memory/ref_counted.h:400
    #49 0x56064c686ed2 in Release ./../../base/memory/scoped_refptr.h:322
    #50 0x56064c686ed2 in ~scoped_refptr ./../../base/memory/scoped_refptr.h:224
    #51 0x56064c686ed2 in blink::VideoFrame::CreateImageBitmap(blink::ScriptState*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:444
    #52 0x56064c686ed2 in ?? ??:0
    #53 0x56064c68781a in non-virtual thunk to blink::VideoFrame::CreateImageBitmap(blink::ScriptState*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:?
    #54 0x56064c68781a in ?? ??:0
    #55 0x56064c68bb31 in blink::ImageBitmapFactories::CreateImageBitmap(blink::ScriptState*, blink::ImageBitmapSource*, base::Optional<blink::IntRect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/core/imagebitmap/image_bitmap_factories.cc:204
    #56 0x56064c68bb31 in ?? ??:0
    #57 0x56064c6847ee in blink::VideoFrame::createImageBitmap(blink::ScriptState*, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:318
    #58 0x56064c6847ee in ?? ??:0
    #59 0x56064c67f97b in blink::(anonymous namespace)::CreateImageBitmapOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_video_frame.cc:334
    #60 0x56064c67f97b in ?? ??:0
    #61 0x560636d0619b in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #62 0x560636d0619b in ?? ??:0
    #63 0x560636d03cf6 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111
    #64 0x560636d03cf6 in ?? ??:0
    #65 0x560636d0186f in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:141
    #66 0x560636d0186f in ?? ??:0
    #67 0x560638e50458 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #68 0x560638e50458 in ?? ??:0
  r8: 0000000000000000  r9: 00007ffe45d0f150 r10: 0000000000000008 r11: 0000000000000246
 r12: 00007ffe45d10108 r13: 00007ffe45d10110 r14: 00007ffe45d100b0 r15: 00005606508765c8
  di: 0000000000000002  si: 00007ffe45d0f150  bp: 00007ffe45d100e0  bx: 00007ff78a630e00
  dx: 0000000000000000  ax: 0000000000000000  cx: 00007ff78b74518b  sp: 00007ffe45d0f150
  ip: 00007ff78b74518b efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Chromium 88.0.4305.0  Channel: n/a
OS Version: 20.04
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 369 B)

## Timeline

### cl...@chromium.org (2020-10-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6246005899329536.

### cl...@chromium.org (2020-10-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5676389015814144.

### wf...@chromium.org (2020-10-27)

[Empty comment from Monorail migration]

[Monorail components: Blink>Media>Video]

### da...@chromium.org (2020-10-27)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Media>Video Blink>Media>WebCodecs]

### wf...@chromium.org (2020-10-27)

CF can't repro but videocodec team can you take a look at this, please? Is this code in stable or beta?

### da...@chromium.org (2020-10-27)

The feature is behind an origin trial in M86. I'm not sure if the particular issue here is present 86 or only 87+ though. Once we figure out the cause we'll know for sure.

### ch...@chromium.org (2020-10-27)

The API is in Stable, but behind a flag. Some recent changes in this code path only available in Canary - not sure yet if they're critical to the repro

### eu...@chromium.org (2020-10-27)

I think I see what's going on. The culprit is  base::Unretained(shared_image_interface) at https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/webcodecs/video_frame.cc;l=419

After raster_context_provider became refcounted it can be freed when we exit the block and shared_image_interface is being freed with it.



### eu...@chromium.org (2020-10-27)

I don't think it's a problem for M87 or before. Because https://chromium-review.googlesource.com/c/chromium/src/+/2429224 has never been cherry-picked there. And my understanding is that before that raster_context_provider has much wider lifetime. 

### sa...@chromium.org (2020-10-27)

Should be straightforward to switch to passing the context provider instead, do you want to take that Eugene? Assign back to me if not.

### ch...@chromium.org (2020-10-27)

[Empty comment from Monorail migration]

### eu...@chromium.org (2020-10-27)

Since you offered, I'll pass 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/12561d34b7b32fa359a346bf82e33e5d764c78dd

commit 12561d34b7b32fa359a346bf82e33e5d764c78dd
Author: Dan Sanders <sandersd@chromium.org>
Date: Wed Oct 28 01:26:05 2020

[webcodecs] Fix UaF in VideoFrame::CreateImageBitmap

The lifetime was reduced in commit 8d00b89513b277589d2c56b87f926369942e1177,
making the use of base::Unretained() unsafe in this case.

Bug: 1142675
Change-Id: I57e16ee028c02313601b9a611e7e335dfdcb4aff
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2504592
Reviewed-by: Eugene Zemtsov <eugene@chromium.org>
Commit-Queue: Dan Sanders <sandersd@chromium.org>
Cr-Commit-Position: refs/heads/master@{#821536}

[modify] https://crrev.com/12561d34b7b32fa359a346bf82e33e5d764c78dd/third_party/blink/renderer/modules/webcodecs/video_frame.cc


### [Deleted User] (2020-10-28)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2020-10-28)

As c#9 notes, I think this only affects m88+ and is now fixed.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-05)

Congratulations, the VRP panel has decided to award $5,000 for this report.

### ad...@google.com (2020-11-05)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1142675?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053723)*
