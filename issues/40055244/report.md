# crash in VideoFrame

| Field | Value |
|-------|-------|
| **Issue ID** | [40055244](https://issues.chromium.org/issues/40055244) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Internals>Modularization, Blink>JavaScript, Blink>Media>WebCodecs |
| **Platforms** | Linux, Mac |
| **Reporter** | ne...@gmail.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2021-03-18 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36

Steps to reproduce the problem:
ubuntu 20.04
Google Chrome 90.0.4427.5 dev (official build)
Chromium 91.0.4451.0

./chrome --enable-experimental-web-platform-features poc.html

What is the expected behavior?

What went wrong?
Received signal 11 SEGV_ACCERR 6230df828d00
error: unknown argument '--demangle=True'
    #0 0x556e8bc3c7fb in __interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4186
    #1 0x556e8bc3c7fb in ?? ??:0
    #2 0x556e985132e9 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:833
    #3 0x556e985132e9 in ?? ??:0
    #4 0x556e982d2403 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:198
    #5 0x556e982d2403 in StackTrace ./../../base/debug/stack_trace.cc:195
    #6 0x556e982d2403 in ?? ??:0
    #7 0x556e98511e27 in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:345
    #8 0x556e98511e27 in ?? ??:0
error: unknown argument '--demangle=True'
    #9 0x7fab53d663c0 in __funlockfile :?
    #10 0x7fab53d663c0 in ?? ??:0
error: unknown argument '--demangle=True'
    #11 0x7fab51e7bec8 in memcpy ??:?
    #12 0x7fab51e7bec8 in ?? ??:0
    #13 0x556e8bc7f952 in __asan_memcpy /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:22
    #14 0x556e8bc7f952 in ?? ??:0
    #15 0x556eab2acd2f in blink::VideoFrame::Create(blink::ScriptState*, WTF::String const&, blink::HeapVector<blink::Member<blink::PlaneInit>, 0u> const&, blink::VideoFramePlaneInit const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:509
    #16 0x556eab2acd2f in ?? ??:0
    #17 0x556eab2a0da1 in blink::(anonymous namespace)::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_video_frame.cc:319
    #18 0x556eab2a0da1 in ConstructorCallback ./gen/third_party/blink/renderer/bindings/modules/v8/v8_video_frame.cc:355
    #19 0x556eab2a0da1 in ?? ??:0
    #20 0x556e9489d253 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #21 0x556e9489d253 in ?? ??:0
    #22 0x556e94899fb7 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:113
    #23 0x556e94899fb7 in ?? ??:0
    #24 0x556e9489890f in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:139
    #25 0x556e9489890f in ?? ??:0
    #26 0x556e96b1eb78 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #27 0x556e96b1eb78 in ?? ??:0
  r8: 00000c4e7fff9c50  r9: 0000000000000018 r10: ffffffffffffffff r11: 0000000000000017
 r12: 00000ff5e9b86400 r13: 000062700000e1c0 r14: 00006230df828d00 r15: 000062700000e1c0
  di: 000062700000e1c0  si: 00006230df828d00  bp: 00007fffeb1f1d10  bx: 00000000000000c0
  dx: 00000000000000c0  ax: 000062700000e1c0  cx: 0000000000000000  sp: 00007fffeb1f14c8
  ip: 00007fab51e7bec8 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 00006230df828d00
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: 90.0.4427.5   Channel: dev
OS Version: 20.04
Flash Version:

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 331 B)
- [poc2.html](attachments/poc2.html) (text/plain, 307 B)

## Timeline

### [Deleted User] (2021-03-18)

[Empty comment from Monorail migration]

### ne...@gmail.com (2021-03-18)

According to the stack trace, this is a heap overflow. 
After simple modification,  can trigger asan recognizable heap overflow crash log.

==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6030001a18d0 at pc 0x55df2c10e967 bp 0x7ffe53947490 sp 0x7ffe53946c58
READ of size 64 at 0x6030001a18d0 thread T0 (chrome)
    #0 0x55df2c10e966 in __asan_memcpy /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:22
    #1 0x55df2c10e966 in ?? ??:0
    #2 0x55df4b5b158e in blink::VideoFrame::Create(blink::ScriptState*, WTF::String const&, blink::HeapVector<blink::Member<blink::PlaneInit>, 0u> const&, blink::VideoFramePlaneInit const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:520
    #3 0x55df4b5b158e in ?? ??:0
    #4 0x55df4b5c3860 in blink::(anonymous namespace)::v8_video_frame::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_video_frame.cc:330
    #5 0x55df4b5c3860 in ConstructorCallback ./gen/third_party/blink/renderer/bindings/modules/v8/v8_video_frame.cc:366
    #6 0x55df4b5c3860 in ?? ??:0
    #7 0x55df34dfdec2 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #8 0x55df34dfdec2 in ?? ??:0
    #9 0x55df34dfac26 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:113
    #10 0x55df34dfac26 in ?? ??:0
    #11 0x55df34df957e in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:139
    #12 0x55df34df957e in ?? ??:0
    #13 0x55df370c7497 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #14 0x55df370c7497 in ?? ??:0
    #15 0x55df3705c4e0 in Builtins_JSBuiltinsConstructStub setup-isolate-deserialize.cc:?
    #16 0x55df3705c4e0 in ?? ??:0
    #17 0x55df3715529e in Builtins_ConstructHandler setup-isolate-deserialize.cc:?
    #18 0x55df3715529e in ?? ??:0
    #19 0x55df3705eec0 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #20 0x55df3705eec0 in ?? ??:0
    #21 0x55df3705eec0 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #22 0x55df3705eec0 in ?? ??:0
    #23 0x55df3705cf7a in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:?
    #24 0x55df3705cf7a in ?? ??:0
    #25 0x55df3705cd05 in Builtins_JSEntry setup-isolate-deserialize.cc:?
    #26 0x55df3705cd05 in ?? ??:0
    #27 0x55df350f0058 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/simulator.h:144
    #28 0x55df350f0058 in Invoke ./../../v8/src/execution/execution.cc:372
    #29 0x55df350f0058 in ?? ??:0
    #30 0x55df350ef013 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:466
    #31 0x55df350ef013 in ?? ??:0
    #32 0x55df34cc8468 in v8::Script::Run(v8::Local<v8::Context>) ./../../v8/src/api/api.cc:1929
    #33 0x55df34cc8468 in ?? ??:0
    #34 0x55df48157801 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:383
    #35 0x55df48157801 in ?? ??:0
    #36 0x55df48158974 in blink::V8ScriptRunner::CompileAndRunScript(blink::ScriptState*, blink::ClassicScript*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:493
    #37 0x55df48158974 in ?? ??:0
    #38 0x55df479fb92e in blink::ClassicScript::RunScriptAndReturnValue(blink::LocalDOMWindow*, blink::ExecuteScriptPolicy) ./../../third_party/blink/renderer/core/script/classic_script.cc:32
    #39 0x55df479fb92e in RunScriptAndReturnValue ./../../third_party/blink/renderer/core/script/classic_script.cc:50
    #40 0x55df479fb92e in ?? ??:0
    #41 0x55df479fb608 in blink::ClassicScript::RunScript(blink::LocalDOMWindow*) ./../../third_party/blink/renderer/core/script/classic_script.cc:44
    #42 0x55df479fb608 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:37
    #43 0x55df479fb608 in ?? ??:0
    #44 0x55df47a57387 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) ./../../third_party/blink/renderer/core/script/pending_script.cc:264
    #45 0x55df47a57387 in ?? ??:0
    #46 0x55df47a56cdc in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third_party/blink/renderer/core/script/pending_script.cc:170
    #47 0x55df47a56cdc in ?? ??:0
    #48 0x55df47a46479 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third_party/blink/renderer/core/script/script_loader.cc:973
    #49 0x55df47a46479 in ?? ??:0
    #50 0x55df48c9ff3b in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:565
    #51 0x55df48c9ff3b in ?? ??:0
    #52 0x55df48c9fafb in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:327
    #53 0x55df48c9fafb in ?? ??:0
    #54 0x55df48c8730f in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:654
    #55 0x55df48c8730f in ?? ??:0
    #56 0x55df48c84571 in blink::HTMLDocumentParser::PumpTokenizer() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:666
    #57 0x55df48c84571 in PumpTokenizer ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:1024
    #58 0x55df48c84571 in ?? ??:0
    #59 0x55df48c82dce in blink::HTMLDocumentParser::PumpTokenizerIfPossible() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:604
    #60 0x55df48c82dce in ?? ??:0
    #61 0x55df48c832d8 in blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:589
    #62 0x55df48c832d8 in ?? ??:0
    #63 0x55df389d2096 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:101
    #64 0x55df389d2096 in RunTask ./../../base/task/common/task_annotator.cc:168
    #65 0x55df389d2096 in ?? ??:0
    #66 0x55df38a0d937 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351
    #67 0x55df38a0d937 in ?? ??:0
    #68 0x55df38a0d164 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #69 0x55df38a0d164 in ?? ??:0
    #70 0x55df388c88c0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #71 0x55df388c88c0 in ?? ??:0
    #72 0x55df38a0ea5c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #73 0x55df38a0ea5c in ?? ??:0
    #74 0x55df3894fdf1 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:133
    #75 0x55df3894fdf1 in ?? ??:0
    #76 0x55df4d34b2f4 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:264
    #77 0x55df4d34b2f4 in ?? ??:0
    #78 0x55df386a2daa in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:556
    #79 0x55df386a2daa in ?? ??:0
    #80 0x55df386a5f2e in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:947
    #81 0x55df386a5f2e in ?? ??:0
    #82 0x55df386a0426 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #83 0x55df386a0426 in ?? ??:0
    #84 0x55df386a097c in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #85 0x55df386a097c in ?? ??:0
    #86 0x55df2c13c947 in ChromeMain ./../../chrome/app/chrome_main.cc:141
    #87 0x55df2c13c947 in ?? ??:0
    #88 0x7f4b0d63d0b2 in __libc_start_main ??:?
    #89 0x7f4b0d63d0b2 in ?? ??:0

0x6030001a18d0 is located 0 bytes to the right of 32-byte region [0x6030001a18b0,0x6030001a18d0)
allocated by thread T0 (chrome) here:
    #0 0x55df2c10f54d in __interceptor_malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:145
    #1 0x55df2c10f54d in ?? ??:0
    #2 0x55df49895432 in blink::ArrayBufferContents::AllocateMemoryWithFlags(unsigned long, blink::ArrayBufferContents::InitializationPolicy, int) ./../../base/allocator/partition_allocator/partition_root.h:1151
    #3 0x55df49895432 in AllocateMemoryWithFlags ./../../third_party/blink/renderer/core/typed_arrays/array_buffer/array_buffer_contents.cc:135
    #4 0x55df49895432 in ?? ??:0
    #5 0x55df48141b6c in blink::(anonymous namespace)::ArrayBufferAllocator::AllocateUninitialized(unsigned long) ./../../third_party/blink/renderer/bindings/core/v8/v8_initializer.cc:695
    #6 0x55df48141b6c in ?? ??:0
    #7 0x55df352739bd in v8::internal::Heap::AllocateExternalBackingStore(std::__1::function<void* (unsigned long)> const&, unsigned long) ./../../buildtools/third_party/libc++/trunk/include/functional:2224
    #8 0x55df352739bd in operator() ./../../buildtools/third_party/libc++/trunk/include/functional:2563
    #9 0x55df352739bd in AllocateExternalBackingStore ./../../v8/src/heap/heap.cc:2869
    #10 0x55df352739bd in ?? ??:0
    #11 0x55df35693034 in v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag) ./../../v8/src/objects/backing-store.cc:245
    #12 0x55df35693034 in ?? ??:0
    #13 0x55df3584070d in v8::internal::JSTypedArray::GetBuffer() ./../../v8/src/objects/js-array-buffer.cc:169
    #14 0x55df3584070d in ?? ??:0
    #15 0x55df34eedef8 in v8::internal::Builtin_Impl_TypedArrayPrototypeBuffer(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-typed-array.cc:24
    #16 0x55df34eedef8 in ?? ??:0
    #17 0x55df370c7497 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #18 0x55df370c7497 in ?? ??:0
    #19 0x55df3705cf7a in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:?
    #20 0x55df3705cf7a in ?? ??:0
    #21 0x55df3705cd05 in Builtins_JSEntry setup-isolate-deserialize.cc:?
    #22 0x55df3705cd05 in ?? ??:0
    #23 0x55df350f0058 in Call ./../../v8/src/execution/simulator.h:144
    #24 0x55df350f0058 in Invoke ./../../v8/src/execution/execution.cc:372
    #25 0x55df350f0058 in ?? ??:0
    #26 0x55df350ef013 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:466
    #27 0x55df350ef013 in ?? ??:0
    #28 0x55df359b3c77 in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator*) ./../../v8/src/objects/objects.cc:1642
    #29 0x55df359b3c77 in GetPropertyWithAccessor ./../../v8/src/objects/objects.cc:1503
    #30 0x55df359b3c77 in ?? ??:0
    #31 0x55df359b1a96 in v8::internal::Object::GetProperty(v8::internal::LookupIterator*, bool) ./../../v8/src/objects/objects.cc:1137
    #32 0x55df359b1a96 in ?? ??:0
    #33 0x55df3547caff in v8::internal::LoadIC::Load(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Name>, bool, v8::internal::Handle<v8::internal::Object>) ./../../v8/src/ic/ic.cc:479
    #34 0x55df3547caff in ?? ??:0
    #35 0x55df3549d5fd in v8::internal::Runtime_LoadNoFeedbackIC_Miss(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/ic/ic.cc:2395
    #36 0x55df3549d5fd in Runtime_LoadNoFeedbackIC_Miss ./../../v8/src/ic/ic.cc:2380
    #37 0x55df3549d5fd in ?? ??:0
    #38 0x55df370c7397 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc:?
    #39 0x55df370c7397 in ?? ??:0
    #40 0x55df3714c936 in Builtins_LdaNamedPropertyHandler setup-isolate-deserialize.cc:?
    #41 0x55df3714c936 in ?? ??:0
    #42 0x55df3705eec0 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #43 0x55df3705eec0 in ?? ??:0
    #44 0x55df3705eec0 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #45 0x55df3705eec0 in ?? ??:0
    #46 0x55df3705cf7a in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:?
    #47 0x55df3705cf7a in ?? ??:0
    #48 0x55df3705cd05 in Builtins_JSEntry setup-isolate-deserialize.cc:?
    #49 0x55df3705cd05 in ?? ??:0
    #50 0x55df350f0058 in Call ./../../v8/src/execution/simulator.h:144
    #51 0x55df350f0058 in Invoke ./../../v8/src/execution/execution.cc:372
    #52 0x55df350f0058 in ?? ??:0
    #53 0x55df350ef013 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:466
    #54 0x55df350ef013 in ?? ??:0
    #55 0x55df34cc8468 in v8::Script::Run(v8::Local<v8::Context>) ./../../v8/src/api/api.cc:1929
    #56 0x55df34cc8468 in ?? ??:0
    #57 0x55df48157801 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:383
    #58 0x55df48157801 in ?? ??:0
    #59 0x55df48158974 in blink::V8ScriptRunner::CompileAndRunScript(blink::ScriptState*, blink::ClassicScript*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:493
    #60 0x55df48158974 in ?? ??:0
    #61 0x55df479fb92e in RunScriptOnScriptStateAndReturnValue ./../../third_party/blink/renderer/core/script/classic_script.cc:32
    #62 0x55df479fb92e in RunScriptAndReturnValue ./../../third_party/blink/renderer/core/script/classic_script.cc:50
    #63 0x55df479fb92e in ?? ??:0
    #64 0x55df479fb608 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:44
    #65 0x55df479fb608 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:37
    #66 0x55df479fb608 in ?? ??:0
    #67 0x55df47a57387 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) ./../../third_party/blink/renderer/core/script/pending_script.cc:264
    #68 0x55df47a57387 in ?? ??:0

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/test/asan-linux-release/chrome+0xaa84966)
Shadow bytes around the buggy address:
  0x0c068002c2c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c068002c2d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c068002c2e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c068002c2f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fd fd
  0x0c068002c300: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa
=>0x0c068002c310: fd fd fd fd fa fa 00 00 00 00[fa]fa 00 00 00 00
  0x0c068002c320: fa fa fd fd fd fa fa fa 00 00 00 fa fa fa 00 00
  0x0c068002c330: 00 00 fa fa fd fd fd fa fa fa 00 00 00 fa fa fa
  0x0c068002c340: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c068002c350: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c068002c360: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

### cl...@chromium.org (2021-03-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5713366077997056.

### cl...@chromium.org (2021-03-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5674580946255872.

### cl...@chromium.org (2021-03-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6468109540851712.

### ke...@chromium.org (2021-03-24)

This overflow looks plausible but it is hard to assess by code inspection. I'll try cluster-fuzz one more time and then pass to an area owner for triage.

### cl...@chromium.org (2021-03-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5087392579780608.

### cl...@chromium.org (2021-03-24)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-03-24)

CF reproduced. Severity-Medium because it is an OOB read. Securty_Impact-None because of the requirement for the experimental web platform features switch to be set.

sandersd@ can you PTAL?

[Monorail components: Blink>Media>WebCodecs]

### sa...@chromium.org (2021-03-24)

This path has an explicit bounds check (using gfx::Size::GetCheckedArea()), it should be rejected long before memory is accessed. I'll investigate.

### cl...@chromium.org (2021-03-24)

Detailed Report: https://clusterfuzz.com/testcase?key=5087392579780608

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ {*}
Crash Address: 0x6090002219f4
Crash State:
  blink::VideoFrame::Create
  blink::v8_video_frame::ConstructorCallback
  v8::internal::FunctionCallbackArguments::Call
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=848369:848371

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5087392579780608

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5087392579780608 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@chromium.org (2021-03-24)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-03-24)

As noted offline this feature is in Origin Trial so Security-Impact_Beta is correct, as set by Clusterfuzz.

### cl...@chromium.org (2021-03-25)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Internals>Modularization Blink>JavaScript]

### [Deleted User] (2021-03-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@chromium.org (2021-03-25)

A fix was committed in https://chromium.googlesource.com/chromium/src/+/7b71636960573861d2fe63c9141d8597bc52dd77, I am not sure why this bug didn't get updated.

### [Deleted User] (2021-03-25)

This bug requires manual review: M90's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@chromium.org (2021-03-25)

1. We're right around the two week cutoff so it is unclear. It's a security fix, has small scope, and affects only a feature that is in Origin Trial (WebCodecs), so I expect it meets the bar.
2. https://chromium.googlesource.com/chromium/src/+/7b71636960573861d2fe63c9141d8597bc52dd77
3. Yes
4. No, the security issue was introduced in M90, and M91 has not branched yet.
5. Security fix.
6. No.
7. WebCodecs as a whole is in Origin Trial.

### ad...@google.com (2021-03-25)

sandersd@ thanks. Do you consider this fixed? If so please mark it so - https://chromium.googlesource.com/chromium/src/+/master/docs/security/security-labels.md#TOC-Merge-labels.

### ad...@google.com (2021-03-25)

Approving merge to M90, branch 4430.

### sa...@chromium.org (2021-03-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/21ef6e2450221f97803237a80440f53887479fad

commit 21ef6e2450221f97803237a80440f53887479fad
Author: Dan Sanders <sandersd@chromium.org>
Date: Fri Mar 26 02:23:00 2021

[webcodecs] Validate that PlaneInit parameters fit in int

These parameters are passed to gfx::Size() which expects int.

(cherry picked from commit 7b71636960573861d2fe63c9141d8597bc52dd77)

Bug: 1189576
Change-Id: Icdf32d88e828759938700e27ea5d19c18cf1eed3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2785545
Auto-Submit: Dan Sanders <sandersd@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Dan Sanders <sandersd@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#866315}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2787328
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4430@{#769}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/21ef6e2450221f97803237a80440f53887479fad/third_party/blink/renderer/modules/webcodecs/video_frame.cc


### cl...@chromium.org (2021-03-26)

ClusterFuzz testcase 5087392579780608 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=866310:866322

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/50b5988dda392a10cdfaf6c22f6ebfdb22ba3b5c

commit 50b5988dda392a10cdfaf6c22f6ebfdb22ba3b5c
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Wed Mar 31 01:24:52 2021

Mark WebCodecs width/height properties with [EnforceRange]

We expect these values to be within valid range.

Bug: 1189576
Change-Id: I3f592983a3d665b16f632fdf2cb6dbdedf3734ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2792742
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Chrome Cunningham <chcunningham@chromium.org>
Commit-Queue: Chrome Cunningham <chcunningham@chromium.org>
Cr-Commit-Position: refs/heads/master@{#867919}

[modify] https://crrev.com/50b5988dda392a10cdfaf6c22f6ebfdb22ba3b5c/third_party/blink/renderer/modules/webcodecs/image_decoder_init.idl
[modify] https://crrev.com/50b5988dda392a10cdfaf6c22f6ebfdb22ba3b5c/third_party/blink/renderer/modules/webcodecs/video_decoder_config.idl
[modify] https://crrev.com/50b5988dda392a10cdfaf6c22f6ebfdb22ba3b5c/third_party/blink/renderer/modules/webcodecs/video_encoder_config.idl
[modify] https://crrev.com/50b5988dda392a10cdfaf6c22f6ebfdb22ba3b5c/third_party/blink/renderer/modules/webcodecs/video_frame_plane_init.idl
[modify] https://crrev.com/50b5988dda392a10cdfaf6c22f6ebfdb22ba3b5c/third_party/blink/web_tests/external/wpt/webcodecs/video-frame.any.js


### am...@google.com (2021-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-31)

Congratulations, neklab2015@! The VRP Panel has decided to award you $2000 for this report. 

### am...@google.com (2021-04-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-07-03)

This issue was migrated from crbug.com/chromium/1189576?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Internals>Modularization, Blink>JavaScript, Blink>Media>WebCodecs]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055244)*
