# uaf in  use-after-poison in blink::CanvasResourceHost::InitializeForRecording(canvas_resource_host.cc)

| Field | Value |
|-------|-------|
| **Issue ID** | [40054164](https://issues.chromium.org/issues/40054164) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas, Blink>Paint |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | yi...@chromium.org |
| **Created** | 2020-12-14 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36

Steps to reproduce the problem:
I found that by simply modifying the original POC, 
the https://crbug.com/chromium/1143662(https://bugs.chromium.org/p/chromium/issues/detail?id=1143662) can continue to be repro. 

Since the status of the issue(1143662) has been fixed, I am afraid that no one will track the comments, so I opened a new issue.
If these are the same root cause,please merge to one.
thanks.

What is the expected behavior?

What went wrong?
READ of size 8 at 0x7efad1c84970 thread T0 (chrome)
error: unknown argument '--demangle=True'
    #0 0x556b197c1326 in blink::CanvasResourceHost::InitializeForRecording(cc::PaintCanvas*) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_host.cc:44
    #1 0x556b197c1326 in ?? ??:0
    #2 0x556b197c732c in blink::CanvasResourceProvider::FlushCanvas() ./../../base/callback.h:168
    #3 0x556b197c732c in FlushCanvas ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1235
    #4 0x556b197c732c in ?? ??:0
    #5 0x556b197d1ce0 in blink::FlushForImageListener::NotifyFlushForImage(int) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1167
    #6 0x556b197d1ce0 in NotifyFlushForImage ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:57
    #7 0x556b197d1ce0 in ?? ??:0
    #8 0x556b197d1618 in blink::CanvasResourceProviderSharedImage::ShouldReplaceTargetBuffer(int) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:553
    #9 0x556b197d1618 in ?? ??:0
    #10 0x556b197d2b35 in blink::CanvasResourceProviderSharedImage::WillDrawInternal(bool) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:429
    #11 0x556b197d2b35 in ?? ??:0
    #12 0x556b197c5c02 in blink::CanvasResourceProvider::EnsureSkiaCanvas() ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1102
    #13 0x556b197c5c02 in ?? ??:0
    #14 0x556b197c83a3 in blink::CanvasResourceProvider::RasterRecord(sk_sp<cc::PaintOpBuffer>) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1247
    #15 0x556b197c83a3 in ?? ??:0
    #16 0x556b197ceea4 in blink::CanvasResourceProviderSharedImage::RasterRecord(sk_sp<cc::PaintOpBuffer>) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:491
    #17 0x556b197ceea4 in ?? ??:0
    #18 0x556b197c71a1 in blink::CanvasResourceProvider::FlushCanvas() ./../../third_party/blink/renderer/platform/graphics/canvas_resource_provider.cc:1230
    #19 0x556b197c71a1 in ?? ??:0
    #20 0x556b1979be77 in blink::Canvas2DLayerBridge::FlushRecording() ./../../third_party/blink/renderer/platform/graphics/canvas_2d_layer_bridge.cc:499
    #21 0x556b1979be77 in ?? ??:0
    #22 0x556b197a1925 in blink::Canvas2DLayerBridge::NewImageSnapshot() ./../../third_party/blink/renderer/platform/graphics/canvas_2d_layer_bridge.cc:682
    #23 0x556b197a1925 in ?? ??:0
    #24 0x556b1cd08085 in blink::CanvasRenderingContext2D::GetImage() ./../../third_party/blink/renderer/modules/canvas/canvas2d/canvas_rendering_context_2d.cc:690
    #25 0x556b1cd08085 in ?? ??:0
    #26 0x556b175f3f70 in blink::HTMLCanvasElement::GetSourceImageForCanvasInternal(blink::SourceImageStatus*) ./../../third_party/blink/renderer/core/html/canvas/html_canvas_element.cc:1353
    #27 0x556b175f3f70 in ?? ??:0
    #28 0x556b175fd1ac in non-virtual thunk to blink::HTMLCanvasElement::GetSourceImageForCanvas(blink::SourceImageStatus*, blink::FloatSize const&) ./../../third_party/blink/renderer/core/html/canvas/html_canvas_element.cc:1305
    #29 0x556b175fd1ac in ?? ??:0
    #30 0x556b1ccd6c99 in ?? ??:0
    #31 0x556b1ccd6c99 in blink::BaseRenderingContext2D::drawImage(blink::ScriptState*, blink::CanvasImageSource*, double, double, double, double, double, double, double, double, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc:1256
    #32 0x556b1ccd6c99 in ?? ??:0
    #33 0x556b1ccd642a in blink::BaseRenderingContext2D::drawImage(blink::ScriptState*, blink::CSSImageValueOrHTMLImageElementOrSVGImageElementOrHTMLVideoElementOrHTMLCanvasElementOrImageBitmapOrOffscreenCanvas const&, double, double, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc:1078
    #34 0x556b1ccd642a in ?? ??:0
    #35 0x556b1cd3e1d8 in blink::(anonymous namespace)::DrawImageOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_canvas_rendering_context_2d.cc:2060
    #36 0x556b1cd3e1d8 in DrawImageOperationCallback ./gen/third_party/blink/renderer/bindings/modules/v8/v8_canvas_rendering_context_2d.cc:2212
    #37 0x556b1cd3e1d8 in ?? ??:0
    #38 0x556b0736e7d1 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158
    #39 0x556b0736e7d1 in ?? ??:0
    #40 0x556b0736c38e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111
    #41 0x556b0736c38e in ?? ??:0
    #42 0x556b0736a088 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:141
    #43 0x556b0736a088 in ?? ??:0
    #44 0x556b0954f9b7 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit setup-isolate-deserialize.cc:?
    #45 0x556b0954f9b7 in ?? ??:0
    #46 0x556b094e982e in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #47 0x556b094e982e in ?? ??:0
    #48 0x556b094e982e in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #49 0x556b094e982e in ?? ??:0
    #50 0x556b094e982e in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #51 0x556b094e982e in ?? ??:0
    #52 0x556b094e749a in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:?
    #53 0x556b094e749a in ?? ??:0
    #54 0x556b094e7277 in Builtins_JSEntry setup-isolate-deserialize.cc:?
    #55 0x556b094e7277 in ?? ??:0
    #56 0x556b07612d25 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/simulator.h:142
    #57 0x556b07612d25 in Invoke ./../../v8/src/execution/execution.cc:368
    #58 0x556b07612d25 in ?? ??:0
    #59 0x556b07611ce0 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:462
    #60 0x556b07611ce0 in ?? ??:0
    #61 0x556b07200388 in v8::Script::Run(v8::Local<v8::Context>) ./../../v8/src/api/api.cc:2141
    #62 0x556b07200388 in ?? ??:0
    #63 0x556b19288d3c in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:363
    #64 0x556b19288d3c in ?? ??:0
    #65 0x556b19289ec0 in blink::V8ScriptRunner::CompileAndRunScript(v8::Isolate*, blink::ScriptState*, blink::ExecutionContext*, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:443
    #66 0x556b19289ec0 in ?? ??:0
    #67 0x556b191cf8c0 in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local<v8::Context>, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&) ./../../third_party/blink/renderer/bindings/core/v8/script_controller.cc:91
    #68 0x556b191cf8c0 in ?? ??:0
    #69 0x556b18b80065 in blink::ClassicScript::RunScript(blink::LocalDOMWindow*) ./../../third_party/blink/renderer/core/script/classic_script.cc:42
    #70 0x556b18b80065 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:36
    #71 0x556b18b80065 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:29
    #72 0x556b18b80065 in ?? ??:0
    #73 0x556b18bd0fc7 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) ./../../third_party/blink/renderer/core/script/pending_script.cc:264
    #74 0x556b18bd0fc7 in ?? ??:0
    #75 0x556b18bd08e1 in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third_party/blink/renderer/core/script/pending_script.cc:170
    #76 0x556b18bd08e1 in ?? ??:0
    #77 0x556b18bc7dbf in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third_party/blink/renderer/core/script/script_loader.cc:922
    #78 0x556b18bc7dbf in ?? ??:0
    #79 0x556b19e639db in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:609
    #80 0x556b19e639db in ?? ??:0
    #81 0x556b19e6358b in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:332
    #82 0x556b19e6358b in ?? ??:0
    #83 0x556b19e18216 in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:610
    #84 0x556b19e18216 in ?? ??:0
    #85 0x556b19e1bd5d in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::__1::unique_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::__1::default_delete<blink::HTMLDocumentParser::TokenizedChunk> >, bool*) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:851
    #86 0x556b19e1bd5d in ?? ??:0
    #87 0x556b19e17aa6 in blink::HTMLDocumentParser::PumpPendingSpeculations() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:911
    #88 0x556b19e17aa6 in ?? ??:0
    #89 0x556b19e1743e in blink::HTMLDocumentParser::ResumeParsingAfterYield() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:597
    #90 0x556b19e1743e in ?? ??:0
    #91 0x556b0969abc5 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) ./../../base/callback.h:101
    #92 0x556b0969abc5 in Run ./../../third_party/blink/renderer/platform/scheduler/common/post_cancellable_task.cc:47
    #93 0x556b0969abc5 in ?? ??:0
    #94 0x556b0969bb56 in base::internal::Invoker<base::internal::BindState<void (blink::TaskHandle::Runner::*)(blink::TaskHandle const&), base::WeakPtr<blink::TaskHandle::Runner>, blink::TaskHandle>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:498
    #95 0x556b0969bb56 in MakeItSo<void (blink::TaskHandle::Runner::*)(const blink::TaskHandle &), base::WeakPtr<blink::TaskHandle::Runner>, blink::TaskHandle> ./../../base/bind_internal.h:657
    #96 0x556b0969bb56 in RunImpl<void (blink::TaskHandle::Runner::*)(const blink::TaskHandle &), std::tuple<base::WeakPtr<blink::TaskHandle::Runner>, blink::TaskHandle>, 0, 1> ./../../base/bind_internal.h:710
    #97 0x556b0969bb56 in RunOnce ./../../base/bind_internal.h:679
    #98 0x556b0969bb56 in ?? ??:0
    #99 0x556b0a912e47 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:101
    #100 0x556b0a912e47 in RunTask ./../../base/task/common/task_annotator.cc:163
    #101 0x556b0a912e47 in ?? ??:0
    #102 0x556b0a950431 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351
    #103 0x556b0a950431 in ?? ??:0
    #104 0x556b0a94fb74 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #105 0x556b0a94fb74 in ?? ??:0
    #106 0x556b0a83c1c0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #107 0x556b0a83c1c0 in ?? ??:0
    #108 0x556b0a95240c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #109 0x556b0a95240c in ?? ??:0
    #110 0x556b0a8c06b0 in base::RunLoop::Run() ./../../base/run_loop.cc:131
    #111 0x556b0a8c06b0 in ?? ??:0
    #112 0x556b1e1ac82e in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:260
    #113 0x556b1e1ac82e in ?? ??:0
    #114 0x556b0a61d849 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:512
    #115 0x556b0a61d849 in ?? ??:0
    #116 0x556b0a620b79 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:902
    #117 0x556b0a620b79 in ?? ??:0
    #118 0x556b0a61acde in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #119 0x556b0a61acde in ?? ??:0
    #120 0x556b0a61b2cc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #121 0x556b0a61b2cc in ?? ??:0
    #122 0x556aff583667 in ChromeMain ./../../chrome/app/chrome_main.cc:130
    #123 0x556aff583667 in ?? ??:0
error: unknown argument '--demangle=True'
    #124 0x7f125f5230b2 in __libc_start_main ??:?
    #125 0x7f125f5230b2 in ?? ??:0

Address 0x7efad1c84970 is a wild pointer.
SUMMARY: AddressSanitizer: use-after-poison (/home/pwnexp/asan-linux-release/chrome+0x245e1326)
Shadow bytes around the buggy address:
  0x0fdfda3888d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fdfda3888e0: 00 00 00 00 00 00 00 00 00 00 00 f7 00 00 00 00
  0x0fdfda3888f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fdfda388900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fdfda388910: 00 00 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7
=>0x0fdfda388920: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7
  0x0fdfda388930: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdfda388940: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdfda388950: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdfda388960: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdfda388970: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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

Did this work before? N/A 

Chrome version: Chromium 88.0.4324.11  Channel: n/a
OS Version: 20.04
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 652 B)

## Timeline

### [Deleted User] (2020-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-12-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5675719442366464.

### cl...@chromium.org (2020-12-15)

ClusterFuzz testcase 5675719442366464 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2020-12-15)

Detailed Report: https://clusterfuzz.com/testcase?key=5675719442366464

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  r. Sending zygote magic failed in zygote_linux.cc
  content::Zygote::ProcessRequests
  content::ZygoteMain
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=836724

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5675719442366464

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5675719442366464 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### cl...@chromium.org (2020-12-15)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Core]

### ca...@chromium.org (2020-12-16)

yiyix: Can you please take a look at this bug since you fixed the similar crbug.com/1143662

[Monorail components: -Internals>Core Blink>Canvas Blink>Paint]

### yi...@chromium.org (2020-12-16)

thank you emilykim8708@ for continuing to invest in this problem! 

yes, I am aware that the issue you found in offscreencanvas exists for canvas as well. I am currently working on this https://crbug.com/chromium/1152288 which is a better way to solve this use after poison issue.

### yi...@chromium.org (2020-12-16)

i will merge that bug to this one.

### yi...@chromium.org (2020-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-16)

Setting milestone and target because of Security_Impact=Beta and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yi...@chromium.org (2020-12-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-12-17)

Detailed Report: https://clusterfuzz.com/testcase?key=5675719442366464

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  r. Sending zygote magic failed in zygote_linux.cc
  content::Zygote::ProcessRequests
  content::ZygoteMain
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=836724

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5675719442366464

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5675719442366464 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aedd4d97491936c57c45552dfeb8ea6ea985d26d

commit aedd4d97491936c57c45552dfeb8ea6ea985d26d
Author: yiyix <yiyix@chromium.org>
Date: Thu Dec 17 21:10:46 2020

Fix poison address in blink::CanvasResourceHost::InitializeForRecording

After allocate a large buffer in memory and creating canvas, it will
trigger the garbage collection from v8, which will trigger
HtmlCanvasElement::Dispose to be called. This call will cause the
canvas element detached from the |host|. However the |host| is saved
as a valid callback in the observer list of the canvas resource
provider. Calling this |host| without canvas element causes this access
to poison address.

In my fix, after garbage collection is triggered and dispose is called,
DiscardResourceProvider() is called as well, so it removes itself from
the observer list.

Bug: 1158266

Change-Id: I40bfc24ff5dcdb7a248114220100b6dd54ac06f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2595734
Commit-Queue: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Yi Xu <yiyix@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#838228}

[modify] https://crrev.com/aedd4d97491936c57c45552dfeb8ea6ea985d26d/third_party/blink/renderer/core/html/canvas/html_canvas_element.cc


### ad...@google.com (2020-12-21)

yiyix@ the previous commit appears to be a fix, so marking as such, so Sheriffbot adds appropriate merge requests.

### [Deleted User] (2020-12-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-21)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M88. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-21)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2020-12-21)

+adetaylor@ (Security TPM) for M88 merge review

### ad...@chromium.org (2020-12-21)

Approving merge to M88, branch 4324.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/64cdb99ce66bcb3919eb981d432b9eac06c4eb0a

commit 64cdb99ce66bcb3919eb981d432b9eac06c4eb0a
Author: yiyix <yiyix@chromium.org>
Date: Tue Dec 22 06:45:18 2020

Fix poison address in blink::CanvasResourceHost::InitializeForRecording

After allocate a large buffer in memory and creating canvas, it will
trigger the garbage collection from v8, which will trigger
HtmlCanvasElement::Dispose to be called. This call will cause the
canvas element detached from the |host|. However the |host| is saved
as a valid callback in the observer list of the canvas resource
provider. Calling this |host| without canvas element causes this access
to poison address.

In my fix, after garbage collection is triggered and dispose is called,
DiscardResourceProvider() is called as well, so it removes itself from
the observer list.

TBR=jbroman@chromium.org

Bug: 1158266

(cherry picked from commit aedd4d97491936c57c45552dfeb8ea6ea985d26d)

Change-Id: I40bfc24ff5dcdb7a248114220100b6dd54ac06f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2595734
Commit-Queue: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Yi Xu <yiyix@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#838228}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2599947
Reviewed-by: Yi Xu <yiyix@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1137}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/64cdb99ce66bcb3919eb981d432b9eac06c4eb0a/third_party/blink/renderer/core/html/canvas/html_canvas_element.cc


### am...@google.com (2021-01-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-14)

[Comment Deleted]

### am...@google.com (2021-01-14)

Since this bug was already internally reported with a fix in progress, the VRP panel has decided to award you with $500 as thanks and appreciation for your report! Congratulations and thank you for your contributions!

### ad...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-05)

Hello OP/emilykim@, we consider attachments/pocs included with reports to be an integral part of the report (https://bughunters.google.com/about/rules/5745167867576320), so I've undeleted them. Thank you! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1158266?no_tracker_redirect=1

[Multiple monorail components: Blink>Canvas, Blink>Paint]
[Monorail mergedwith: crbug.com/chromium/1152288]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054164)*
