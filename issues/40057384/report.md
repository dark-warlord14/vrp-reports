# use after poison in blink::Element::DidMoveToNewDocument

| Field | Value |
|-------|-------|
| **Issue ID** | [40057384](https://issues.chromium.org/issues/40057384) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | om...@chromium.org |
| **Created** | 2021-09-24 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36

Steps to reproduce the problem:
chrome version:
Version 95.0.4638.17 (Official Build) dev (64-bit)
Chromium 96.0.4652.0  gs://chromium-browser-asan/linux-release/asan-linux-release-924556.zip.

Ubuntu :20.04
1 ./chrome -user-data-dir=/tmp/2x http://localhost:8000/main.html
2 Crash will repro in a few seconds.
In the Official Build version, I only confirmed the SIGSEGV crash without in-depth analysis, so I can't  100% sure that it is the same issue.

What is the expected behavior?

What went wrong?
=================================================================
==1==ERROR: AddressSanitizer: use-after-poison on address 0x7ed50029efcc at pc 0x560a4bdabdb7 bp 0x7ffe93a19fd0 sp 0x7ffe93a19fc8
READ of size 4 at 0x7ed50029efcc thread T0 (chrome)
error: unknown argument '--demangle=True'
    #0 0x560a4bdabdb6 in blink::Node::DidMoveToNewDocument(blink::Document&) ./../../third_party/blink/renderer/platform/wtf/vector.h:1184
    #1 0x560a4bdabdb6 in IsEmpty ./../../third_party/blink/renderer/platform/wtf/vector.h:1187
    #2 0x560a4bdabdb6 in IsEmpty ./../../third_party/blink/renderer/core/dom/events/event_listener_map.h:56
    #3 0x560a4bdabdb6 in DidMoveToNewDocument ./../../third_party/blink/renderer/core/dom/node.cc:2612
    #4 0x560a4bdabdb6 in ?? ??:0
    #5 0x560a4be2d2d9 in blink::Element::DidMoveToNewDocument(blink::Document&) ./../../third_party/blink/renderer/core/dom/element.cc:6034
    #6 0x560a4be2d2d9 in ?? ??:0
    #7 0x560a4d0bc893 in blink::HTMLMediaElement::DidMoveToNewDocument(blink::Document&) ./../../third_party/blink/renderer/core/html/media/html_media_element.cc:686
    #8 0x560a4d0bc893 in ?? ??:0
    #9 0x560a4ca76fd0 in blink::TreeScopeAdopter::MoveNodeToNewDocument(blink::Node&, blink::Document&, blink::Document&) const ./../../third_party/blink/renderer/core/dom/tree_scope_adopter.cc:179
    #10 0x560a4ca76fd0 in ?? ??:0
    #11 0x560a4ca7647a in blink::TreeScopeAdopter::MoveTreeToNewScope(blink::Node&) const ./../../third_party/blink/renderer/core/dom/tree_scope_adopter.cc:65
    #12 0x560a4ca7647a in ?? ??:0
    #13 0x560a4ca760f9 in blink::TreeScopeAdopter::Execute() const ./../../third_party/blink/renderer/core/dom/tree_scope_adopter.cc:41
    #14 0x560a4ca760f9 in ?? ??:0
    #15 0x560a4c03318d in blink::TreeScope::AdoptIfNeeded(blink::Node&) ./../../third_party/blink/renderer/core/dom/tree_scope.cc:446
    #16 0x560a4c03318d in ?? ??:0
    #17 0x560a4bc34fa4 in blink::Document::adoptNode(blink::Node*, blink::ExceptionState&) ./../../third_party/blink/renderer/core/dom/document.cc:1333
    #18 0x560a4bc34fa4 in ?? ??:0
    #19 0x560a52d99fab in blink::(anonymous namespace)::v8_document::AdoptNodeOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_document.cc:4951
    #20 0x560a52d99fab in ?? ??:0
    #21 0x560a3a1a2302 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:152
    #22 0x560a3a1a2302 in ?? ??:0
    #23 0x560a3a19ff2c in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:112
    #24 0x560a3a19ff2c in ?? ??:0
    #25 0x560a3a19d96b in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:142
    #26 0x560a3a19d96b in ?? ??:0
    #12 0x7f6200080df7  (<unknown module>)
    #13 0x7f620000c760  (<unknown module>)
    #14 0x7f620000a75b  (<unknown module>)
    #15 0x7f620000a486  (<unknown module>)
    #27 0x560a3a48053b in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/simulator.h:152
    #28 0x560a3a48053b in Invoke ./../../v8/src/execution/execution.cc:383
    #29 0x560a3a48053b in ?? ??:0
    #30 0x560a3a47dd4b in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:478
    #31 0x560a3a47dd4b in ?? ??:0
    #32 0x560a3addd71a in v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator*) ./../../v8/src/objects/objects.cc:1600
    #33 0x560a3addd71a in GetPropertyWithAccessor ./../../v8/src/objects/objects.cc:1461
    #34 0x560a3addd71a in ?? ??:0
    #35 0x560a3addb255 in v8::internal::Object::GetProperty(v8::internal::LookupIterator*, bool) ./../../v8/src/objects/objects.cc:1169
    #36 0x560a3addb255 in ?? ??:0
    #37 0x560a3a803775 in v8::internal::LoadIC::Load(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Name>, bool, v8::internal::Handle<v8::internal::Object>) ./../../v8/src/ic/ic.cc:497
    #38 0x560a3a803775 in ?? ??:0
    #39 0x560a3a812a3a in v8::internal::KeyedLoadIC::Load(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) ./../../v8/src/ic/ic.cc:1551
    #40 0x560a3a812a3a in ?? ??:0
    #41 0x560a3a82b77f in v8::internal::Runtime_KeyedLoadIC_Miss(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/ic/ic.cc:2652
    #42 0x560a3a82b77f in Runtime_KeyedLoadIC_Miss ./../../v8/src/ic/ic.cc:2635
    #43 0x560a3a82b77f in ?? ??:0
    #23 0x7f6200080cf7  (<unknown module>)
    #24 0x7f62001c4c0d  (<unknown module>)
    #25 0x7f620000c760  (<unknown module>)
    #26 0x7f620000c760  (<unknown module>)
    #27 0x7f620000c760  (<unknown module>)
    #28 0x7f62001c48a1  (<unknown module>)
    #29 0x7f620000c760  (<unknown module>)
    #30 0x7f620000c760  (<unknown module>)
    #31 0x7f620000c760  (<unknown module>)
    #32 0x7f6200009a67  (<unknown module>)
    #33 0x7f6200118dfa  (<unknown module>)
    #34 0x7f620000c760  (<unknown module>)
    #35 0x7f620000c760  (<unknown module>)
    #36 0x7f620000a75b  (<unknown module>)
    #37 0x7f620000a486  (<unknown module>)
    #44 0x560a3a48053b in Call ./../../v8/src/execution/simulator.h:152
    #45 0x560a3a48053b in Invoke ./../../v8/src/execution/execution.cc:383
    #46 0x560a3a48053b in ?? ??:0
    #47 0x560a3a47dd4b in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:478
    #48 0x560a3a47dd4b in ?? ??:0
    #49 0x560a3a07b2f8 in v8::Script::Run(v8::Local<v8::Context>) ./../../v8/src/api/api.cc:2084
    #50 0x560a3a07b2f8 in ?? ??:0
    #51 0x560a4c24d63b in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:424
    #52 0x560a4c24d63b in ?? ??:0
    #53 0x560a4c24e6e3 in blink::V8ScriptRunner::CompileAndRunScript(blink::ScriptState*, blink::ClassicScript*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:516
    #54 0x560a4c24e6e3 in ?? ??:0
    #55 0x560a4e652586 in blink::ClassicScript::RunScriptAndReturnValue(blink::LocalDOMWindow*, blink::ExecuteScriptPolicy) ./../../third_party/blink/renderer/core/script/classic_script.cc:32
    #56 0x560a4e652586 in RunScriptAndReturnValue ./../../third_party/blink/renderer/core/script/classic_script.cc:50
    #57 0x560a4e652586 in ?? ??:0
    #58 0x560a4e652285 in blink::ClassicScript::RunScript(blink::LocalDOMWindow*) ./../../third_party/blink/renderer/core/script/classic_script.cc:44
    #59 0x560a4e652285 in RunScript ./../../third_party/blink/renderer/core/script/classic_script.cc:37
    #60 0x560a4e652285 in ?? ??:0
    #61 0x560a4e6ab7d3 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script*, blink::ScriptElementBase*, bool, bool, bool, base::TimeTicks, bool) ./../../third_party/blink/renderer/core/script/pending_script.cc:264
    #62 0x560a4e6ab7d3 in ?? ??:0
    #63 0x560a4e6ab14d in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) ./../../third_party/blink/renderer/core/script/pending_script.cc:170
    #64 0x560a4e6ab14d in ?? ??:0
    #65 0x560a4e69c798 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third_party/blink/renderer/core/script/script_loader.cc:987
    #66 0x560a4e69c798 in ?? ??:0
    #67 0x560a4f54d152 in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:561
    #68 0x560a4f54d152 in ?? ??:0
    #69 0x560a4f54cb24 in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, WTF::TextPosition const&) ./../../third_party/blink/renderer/core/script/html_parser_script_runner.cc:323
    #70 0x560a4f54cb24 in ?? ??:0
    #71 0x560a4f535d3f in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:662
    #72 0x560a4f535d3f in ?? ??:0
    #73 0x560a4f538dff in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::__1::unique_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::__1::default_delete<blink::HTMLDocumentParser::TokenizedChunk> >, bool*) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:897
    #74 0x560a4f538dff in ?? ??:0
    #75 0x560a4f535655 in blink::HTMLDocumentParser::PumpPendingSpeculations() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:957
    #76 0x560a4f535655 in ?? ??:0
    #77 0x560a4f53502e in blink::HTMLDocumentParser::ResumeParsingAfterYield() ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:649
    #78 0x560a4f53502e in ?? ??:0
    #79 0x560a3ce6fa3d in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) ./../../base/callback.h:99
    #80 0x560a3ce6fa3d in Run ./../../third_party/blink/renderer/platform/scheduler/common/post_cancellable_task.cc:49
    #81 0x560a3ce6fa3d in ?? ??:0
    #82 0x560a3ce7024e in base::internal::Invoker<base::internal::BindState<void (blink::TaskHandle::Runner::*)(blink::TaskHandle const&), base::WeakPtr<blink::TaskHandle::Runner>, blink::TaskHandle>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:509
    #83 0x560a3ce7024e in MakeItSo<void (blink::TaskHandle::Runner::*)(const blink::TaskHandle &), base::WeakPtr<blink::TaskHandle::Runner>, blink::TaskHandle> ./../../base/bind_internal.h:668
    #84 0x560a3ce7024e in RunImpl<void (blink::TaskHandle::Runner::*)(const blink::TaskHandle &), std::__1::tuple<base::WeakPtr<blink::TaskHandle::Runner>, blink::TaskHandle>, 0UL, 1UL> ./../../base/bind_internal.h:721
    #85 0x560a3ce7024e in RunOnce ./../../base/bind_internal.h:690
    #86 0x560a3ce7024e in ?? ??:0
    #87 0x560a3fabe5f3 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:99
    #88 0x560a3fabe5f3 in RunTask ./../../base/task/common/task_annotator.cc:178
    #89 0x560a3fabe5f3 in ?? ??:0
    #90 0x560a3faf5b51 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:357
    #91 0x560a3faf5b51 in ?? ??:0
    #92 0x560a3faf53a3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260
    #93 0x560a3faf53a3 in ?? ??:0
    #94 0x560a3faf64c1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread_controller_with_message_pump_impl.cc:?
    #95 0x560a3faf64c1 in ?? ??:0
    #96 0x560a3f9b75ad in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:38
    #97 0x560a3f9b75ad in ?? ??:0
    #98 0x560a3faf6b8c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:462
    #99 0x560a3faf6b8c in ?? ??:0
    #100 0x560a3fa3a201 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134
    #101 0x560a3fa3a201 in ?? ??:0
    #102 0x560a53b1ebc3 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:265
    #103 0x560a53b1ebc3 in ?? ??:0
    #104 0x560a3e894823 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:583
    #105 0x560a3e894823 in ?? ??:0
    #106 0x560a3e8988df in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:974
    #107 0x560a3e8988df in ?? ??:0
    #108 0x560a3e891e7a in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:390
    #109 0x560a3e891e7a in ?? ??:0
    #110 0x560a3e893a54 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:418
    #111 0x560a3e893a54 in ?? ??:0
    #112 0x560a31a91fd1 in ChromeMain ./../../chrome/app/chrome_main.cc:172
    #113 0x560a31a91fd1 in ?? ??:0
error: unknown argument '--demangle=True'
    #114 0x7f632f76c0b2 in __libc_start_main ??:?
    #115 0x7f632f76c0b2 in ?? ??:0

Address 0x7ed50029efcc is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison (/home/test/asan-linux-release/chrome+0x24a39db6)
Shadow bytes around the buggy address:
  0x0fdb2004bda0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fdb2004bdb0: 00 00 00 00 00 00 00 00 00 00 00 f7 f7 00 00 00
  0x0fdb2004bdc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fdb2004bdd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fdb2004bde0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0fdb2004bdf0: 00 00 f7 f7 f7 f7 00 f7 f7[f7]f7 00 f7 f7 f7 f7
  0x0fdb2004be00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fdb2004be10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fdb2004be20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fdb2004be30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fdb2004be40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==1==ABORTING

Did this work before? N/A 

Chrome version: 96.0.4652.0  Channel: n/a
OS Version: 20.04

## Attachments

- deleted (application/octet-stream, 0 B)
- [crash.html](attachments/crash.html) (text/plain, 492 B)
- [main.html](attachments/main.html) (text/plain, 152 B)
- [testharness.js](attachments/testharness.js) (text/plain, 151.3 KB)
- [testharnessreport.js](attachments/testharnessreport.js) (text/plain, 14.2 KB)
- [min_poc.html](attachments/min_poc.html) (text/plain, 358 B)
- [min.asan](attachments/min.asan) (text/plain, 20.4 KB)
- [min_poc3.html](attachments/min_poc3.html) (text/plain, 358 B)

## Timeline

### [Deleted User] (2021-09-24)

[Empty comment from Monorail migration]

### aj...@google.com (2021-09-24)

[Empty comment from Monorail migration]

### aj...@google.com (2021-09-24)

[Empty comment from Monorail migration]

### aj...@google.com (2021-09-24)

Thanks - I'm attempting to repro - in future it is helpful for us if you can upload the elements of the poc directly (rather than in a zip) and if you can only upload the minimum necessary for the poc - we have to eyeball all the code we're going to run and the test harness scripts are very large!

### aj...@google.com (2021-09-24)

In a v8 build with `v8_enable_verify_heap = true` I hit a DCHECK:

C:\src\chromium\src [(f0f5561...) +1 ~0 -0 !]> c:\src\chromium\src\out\Asan\Chrome.exe --ignore-certificate-errors --allow-insecure-localhost --no-sandbox https://192.168.11.1:8443/
#
# Fatal error in ../../v8/src/heap/cppgc/marker.cc, line 194
# Debug check failed: !HeapObjectHeader::FromObject(item.key).IsMarked().
#
#
#
#FailureMessage Object: 0000132611046040Backtrace:
        base::debug::CollectStackTrace [0x00007FF9420D9F29+25] (C:\src\chromium\src\base\debug\stack_trace_win.cc:303)
        base::debug::StackTrace::StackTrace [0x00007FF941DC66F1+33] (C:\src\chromium\src\base\debug\stack_trace.cc:197)
        gin::`anonymous namespace'::PrintStackTrace [0x00007FF94502A9FB+259] (C:\src\chromium\src\gin\v8_platform.cc:46)
        V8_Fatal [0x00007FF943D317C4+580] (C:\src\chromium\src\v8\src\base\logging.cc:164)
        v8::base::`anonymous namespace'::DefaultDcheckHandler [0x00007FF943D30618+40] (C:\src\chromium\src\v8\src\base\logging.cc:57)
        cppgc::internal::MarkerBase::~MarkerBase [0x00007FF93E713CDB+1259] (C:\src\chromium\src\v8\src\heap\cppgc\marker.cc:194)
        v8::internal::`anonymous namespace'::UnifiedHeapMarker::~UnifiedHeapMarker [0x00007FF93C0BBA97+23] (C:\src\chromium\src\v8\src\heap\cppgc-js\cpp-heap.cc:181)
        v8::internal::CppHeap::TraceEpilogue [0x00007FF93C0B4ACC+588] (C:\src\chromium\src\v8\src\heap\cppgc-js\cpp-heap.cc:489)
        v8::internal::LocalEmbedderHeapTracer::TraceEpilogue [0x00007FF93C0D7DE5+325] (C:\src\chromium\src\v8\src\heap\embedder-tracing.cc:37)
        v8::internal::Heap::PerformGarbageCollection [0x00007FF93C21B487+6487] (C:\src\chromium\src\v8\src\heap\heap.cc:2253)
        v8::internal::Heap::CollectGarbage [0x00007FF93C210CE5+6901] (C:\src\chromium\src\v8\src\heap\heap.cc:1789)
        v8::internal::Heap::FinalizeIncrementalMarkingAtomically [0x00007FF93C216D65+245] (C:\src\chromium\src\v8\src\heap\heap.cc:3722)
        v8::EmbedderHeapTracer::IncreaseAllocatedSize [0x00007FF93B676680+224] (C:\src\chromium\src\v8\src\api\api.cc:10092)
        cppgc::internal::StatsCollector::NotifySafePointForConservativeCollection [0x00007FF93E7439D8+488] (C:\src\chromium\src\v8\src\heap\cppgc\stats-collector.cc:63)
        cppgc::internal::ObjectAllocator::OutOfLineAllocate [0x00007FF93E728168+264] (C:\src\chromium\src\v8\src\heap\cppgc\object-allocator.cc:120)
        cppgc::MakeGarbageCollectedTrait<blink::HeapVectorBacking<std::__1::pair<cppgc::internal::BasicMember<const blink::ActiveScriptWrappableBase,cppgc::internal::UntracedMemberTag,cppgc::internal::NoWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>, [0x00007FF9493E9869+537] (C:\src\chromium\src\third_party\blink\renderer\platform\heap\v8_wrapper\collection_support\heap_vector_backing.h:211)
        WTF::VectorBufferBase<std::__1::pair<cppgc::internal::BasicMember<const blink::ActiveScriptWrappableBase,cppgc::internal::UntracedMemberTag,cppgc::internal::NoWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>,cppgc::internal::BasicMember<const b [0x00007FF9493E9582+642] (C:\src\chromium\src\third_party\blink\renderer\platform\wtf\vector.h:500)
        WTF::Vector<std::__1::pair<cppgc::internal::BasicMember<const blink::ActiveScriptWrappableBase,cppgc::internal::UntracedMemberTag,cppgc::internal::NoWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>,cppgc::internal::BasicMember<const blink::Acti [0x00007FF9493E87CE+302] (C:\src\chromium\src\third_party\blink\renderer\platform\wtf\vector.h:2256)
        WTF::Vector<std::__1::pair<cppgc::internal::BasicMember<const blink::ActiveScriptWrappableBase,cppgc::internal::UntracedMemberTag,cppgc::internal::NoWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>,cppgc::internal::BasicMember<const blink::Acti [0x00007FF9493EA7E3+931] (C:\src\chromium\src\third_party\blink\renderer\platform\wtf\vector.h:1846)
        WTF::Vector<std::__1::pair<cppgc::internal::BasicMember<const blink::ActiveScriptWrappableBase,cppgc::internal::UntracedMemberTag,cppgc::internal::NoWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>,cppgc::internal::BasicMember<const blink::Acti [0x00007FF9493EA1F7+679] (C:\src\chromium\src\third_party\blink\renderer\platform\wtf\vector.h:1955)
        blink::ActiveScriptWrappableManager::Add [0x00007FF9493E7B9D+941] (C:\src\chromium\src\third_party\blink\renderer\platform\bindings\active_script_wrappable_manager.h:39)
        blink::ActiveScriptWrappableBase::ActiveScriptWrappableBaseConstructed [0x00007FF9493E777F+367] (C:\src\chromium\src\third_party\blink\renderer\platform\bindings\active_script_wrappable_base.cc:16)
        blink::IntersectionObserver::Create [0x00007FF952433922+930] (C:\src\chromium\src\third_party\blink\renderer\core\intersection_observer\intersection_observer.cc:258)
        blink::VideoWakeLock::StartIntersectionObserver [0x00007FF952C44F7D+1197] (C:\src\chromium\src\third_party\blink\renderer\core\html\media\video_wake_lock.cc:183)
        blink::VideoWakeLock::VideoWakeLock [0x00007FF952C448AE+926] (C:\src\chromium\src\third_party\blink\renderer\core\html\media\video_wake_lock.cc:39)
        blink::HTMLVideoElement::HTMLVideoElement [0x00007FF94D43C918+2008] (C:\src\chromium\src\third_party\blink\renderer\core\html\media\html_video_element.cc:104)
        blink::HTMLVideoConstructor [0x00007FF94D84DC22+162] (C:\src\chromium\src\out\Asan\gen\third_party\blink\renderer\core\html_element_factory.cc:678)
        blink::HTMLElementFactory::Create [0x00007FF94D843C85+2085] (C:\src\chromium\src\out\Asan\gen\third_party\blink\renderer\core\html_element_factory.cc:857)
        blink::Document::CreateElementForBinding [0x00007FF9489234AD+1597] (C:\src\chromium\src\third_party\blink\renderer\core\dom\document.cc:1034)
        blink::`anonymous namespace'::v8_document::CreateElementOperationCallbackForMainWorld [0x00007FF958F105A0+3261] (C:\src\chromium\src\out\Asan\gen\third_party\blink\renderer\bindings\modules\v8\v8_document.cc:5369)
        v8::internal::FunctionCallbackArguments::Call [0x00007FF93B845FB0+2496] (C:\src\chromium\src\v8\src\api\api-arguments-inl.h:152)
        v8::internal::`anonymous namespace'::HandleApiCallHelper<0> [0x00007FF93B83FEE0+5520] (C:\src\chromium\src\v8\src\builtins\builtins-api.cc:112)
        v8::internal::Builtin_Impl_HandleApiCall [0x00007FF93B838D50+1936] (C:\src\chromium\src\v8\src\builtins\builtins-api.cc:142)
        v8::internal::Builtin_HandleApiCall [0x00007FF93B83782B+555] (C:\src\chromium\src\v8\src\builtins\builtins-api.cc:130)
        (No symbol) [0x00007EF2000D363C]

Adding owners from https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/dom/OWNERS



[Monorail components: Blink>DOM]

### [Deleted User] (2021-09-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-09-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5737122756362240.

### cl...@chromium.org (2021-09-24)

ClusterFuzz testcase 5737122756362240 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2021-09-24)

Detailed Report: https://clusterfuzz.com/testcase?key=5737122756362240

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7eae0027e5f0
Crash State:
  blink::EventListenerMap::Add
  blink::EventTarget::AddEventListenerInternal
  blink::VideoWakeLock::VideoWakeLock
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=924851

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5737122756362240

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5737122756362240 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### aj...@google.com (2021-09-24)

CF hits VideoWakeLock so adding dalecurtis

=================================================================
==1==ERROR: AddressSanitizer: use-after-poison on address 0x7eae0027e5f0 at pc 0x55fba2350727 bp 0x7ffcaf484af0 sp 0x7ffcaf484ae8
READ of size 8 at 0x7eae0027e5f0 thread T0 (chrome)
SCARINESS: 33 (8-byte-read-use-after-poison)
    #0 0x55fba2350726 in Buffer third_party/blink/renderer/platform/wtf/vector.h:514:24
    #1 0x55fba2350726 in data third_party/blink/renderer/platform/wtf/vector.h:1210:28
    #2 0x55fba2350726 in begin third_party/blink/renderer/platform/wtf/vector.h:1214:29
    #3 0x55fba2350726 in blink::EventListenerMap::Add(WTF::AtomicString const&, blink::EventListener*, blink::AddEventListenerOptionsResolved const*, blink::RegisteredEventListener*) third_party/blink/renderer/core/dom/events/event_listener_map.cc:134:26
    #4 0x55fba2344541 in blink::EventTarget::AddEventListenerInternal(WTF::AtomicString const&, blink::EventListener*, blink::AddEventListenerOptionsResolved const*) third_party/blink/renderer/core/dom/events/event_target.cc:481:59
    #5 0x55fba372c9b0 in blink::VideoWakeLock::VideoWakeLock(blink::HTMLVideoElement&) third_party/blink/renderer/core/html/media/video_wake_lock.cc:31:18
    #6 0x55fba370e89b in Call<blink::HTMLVideoElement &> v8/include/cppgc/allocation.h:174:32
    #7 0x55fba370e89b in MakeGarbageCollected<blink::VideoWakeLock, blink::HTMLVideoElement &> v8/include/cppgc/allocation.h:212:7
    #8 0x55fba370e89b in MakeGarbageCollected<blink::VideoWakeLock, blink::HTMLVideoElement &> third_party/blink/renderer/platform/heap/v8_wrapper/heap.h:26:10
    #9 0x55fba370e89b in blink::HTMLVideoElement::HTMLVideoElement(blink::Document&) third_party/blink/renderer/core/html/media/html_video_element.cc:104:16
    #10 0x55fba52cbdb9 in Call<blink::Document &> v8/include/cppgc/allocation.h:174:32
    #11 0x55fba52cbdb9 in MakeGarbageCollected<blink::HTMLVideoElement, blink::Document &> v8/include/cppgc/allocation.h:212:7
    #12 0x55fba52cbdb9 in MakeGarbageCollected<blink::HTMLVideoElement, blink::Document &> third_party/blink/renderer/platform/heap/v8_wrapper/heap.h:26:10
    #13 0x55fba52cbdb9 in blink::HTMLVideoConstructor(blink::Document&, blink::CreateElementFlags) gen/third_party/blink/renderer/core/html_element_factory.cc:678:10
    #14 0x55fba52b7634 in blink::HTMLElementFactory::Create(WTF::AtomicString const&, blink::Document&, blink::CreateElementFlags) gen/third_party/blink/renderer/core/html_element_factory.cc:857:10

From CF crashes in VideoWakeLock

### aj...@google.com (2021-09-25)

Also get this stack on a dcheck-disabled asan build:

==52676==ERROR: AddressSanitizer: use-after-poison on address 0x7ee500149f84 at pc 0x7ff94fcab645 bp 0x0047135fc2e0 sp 0x0047135fc328
READ of size 4 at 0x7ee500149f84 thread T0
    #0 0x7ff94fcab644 in WTF::Vector<std::__1::pair<WTF::AtomicString,cppgc::internal::BasicMember<blink::HeapVector<blink::RegisteredEventListener,1>,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy> >,2,blink::HeapAllocator>::size C:\src\chromium\src\third_party\blink\renderer\platform\wtf\vector.h:1184
    #1 0x7ff94fcab644 in WTF::Vector<std::__1::pair<WTF::AtomicString,cppgc::internal::BasicMember<blink::HeapVector<blink::RegisteredEventListener,1>,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy> >,2,blink::HeapAllocator>::IsEmpty C:\src\chromium\src\third_party\blink\renderer\platform\wtf\vector.h:1187
    #2 0x7ff94fcab644 in blink::EventListenerMap::IsEmpty C:\src\chromium\src\third_party\blink\renderer\core\dom\events\event_listener_map.h:56
    #3 0x7ff94fcab644 in blink::Node::DidMoveToNewDocument(class blink::Document &) C:\src\chromium\src\third_party\blink\renderer\core\dom\node.cc:2612:23
    #4 0x7ff94fbe4ca7 in blink::Element::DidMoveToNewDocument(class blink::Document &) C:\src\chromium\src\third_party\blink\renderer\core\dom\element.cc:6030:9
    #5 0x7ff9532cd752 in blink::HTMLMediaElement::DidMoveToNewDocument(class blink::Document &) C:\src\chromium\src\third_party\blink\renderer\core\html\media\html_media_element.cc:686:16
    #6 0x7ff954c21a83 in blink::TreeScopeAdopter::MoveNodeToNewDocument(class blink::Node &, class blink::Document &, class blink::Document &) const C:\src\chromium\src\third_party\blink\renderer\core\dom\tree_scope_adopter.cc:179:8
    #7 0x7ff954c20ce6 in blink::TreeScopeAdopter::MoveTreeToNewScope(class blink::Node &) const C:\src\chromium\src\third_party\blink\renderer\core\dom\tree_scope_adopter.cc:65:7
    #8 0x7ff954c20983 in blink::TreeScopeAdopter::Execute(void) const C:\src\chromium\src\third_party\blink\renderer\core\dom\tree_scope_adopter.cc:41:3
    #9 0x7ff94fe6d888 in blink::TreeScope::AdoptIfNeeded(class blink::Node &) C:\src\chromium\src\third_party\blink\renderer\core\dom\tree_scope.cc:446:13
    #10 0x7ff94f79a332 in blink::Document::adoptNode(class blink::Node *, class blink::ExceptionState &) C:\src\chromium\src\third_party\blink\renderer\core\dom\document.cc:1333:3
    #11 0x7ff95dbbee7f in blink::`anonymous namespace'::v8_document::AdoptNodeOperationCallback C:\src\chromium\src\out\Asan\gen\third_party\blink\renderer\bindings\modules\v8\v8_document.cc:4951:41
    #12 0x7ff944d5f447 in v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo) C:\src\chromium\src\v8\src\api\api-arguments-inl.h:152:3
    #13 0x7ff944d5c133 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\src\chromium\src\v8\src\builtins\builtins-api.cc:112:36
    #14 0x7ff944d5902f in v8::internal::Builtin_Impl_HandleApiCall C:\src\chromium\src\v8\src\builtins\builtins-api.cc:142:5
    #15 0x7ff944d581e1 in v8::internal::Builtin_HandleApiCall(int, unsigned __int64 *, class v8::internal::Isolate *) C:\src\chromium\src\v8\src\builtins\builtins-api.cc:130:1
    #16 0x7efb000c16bb  (<unknown module>)

Address 0x7ee500149f84 is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison C:\src\chromium\src\third_party\blink\renderer\platform\wtf\vector.h:1184 in WTF::Vector<std::__1::pair<WTF::AtomicString,cppgc::internal::BasicMember<blink::HeapVector<blink::RegisteredEventListener,1>,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy> >,2,blink::HeapAllocator>::size
Shadow bytes around the buggy address:
  0x12196eea93a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x12196eea93b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x12196eea93c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x12196eea93d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x12196eea93e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x12196eea93f0:[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x12196eea9400: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x12196eea9410: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x12196eea9420: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x12196eea9430: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x12196eea9440: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
==52676==ABORTING

### em...@gmail.com (2021-09-26)

I uploaded minimized poc. And get a little different stack trace.

==2160810==ERROR: AddressSanitizer: use-after-poison on address 0x7ea70023a96c at pc 0x555bdae06057 bp 0x7ffe506bc990 sp 0x7ffe506bc988
READ of size 2 at 0x7ea70023a96c thread T0 (swain)
    #0 0x555bdae06056 in __cxx_atomic_load<unsigned short> ./../../buildtools/third_party/libc++/trunk/include/atomic:1006:12
    #1 0x555bdae06056 in load ./../../buildtools/third_party/libc++/trunk/include/atomic:1615:17
    #2 0x555bdae06056 in LoadEncoded<cppgc::internal::AccessMode::kAtomic, cppgc::internal::HeapObjectHeader::EncodedHalf::kHigh, std::__1::memory_order_acquire> ./../../v8/src/heap/cppgc/heap-object-header.h:304:40
    #3 0x555bdae06056 in IsInConstruction<cppgc::internal::AccessMode::kAtomic> ./../../v8/src/heap/cppgc/heap-object-header.h:237:7
    #4 0x555bdae06056 in MarkAndPush ./../../v8/src/heap/cppgc/marking-state.h:193:14
    #5 0x555bdae06056 in MarkAndPush ./../../v8/src/heap/cppgc/marking-state.h:184:3
    #6 0x555bdae06056 in cppgc::internal::MarkingStateBase::ProcessEphemeron(void const*, void const*, cppgc::TraceDescriptor, cppgc::Visitor&) ./../../v8/src/heap/cppgc/marking-state.h:296:7
    #7 0x555bdae1e56d in operator() ./../../v8/src/heap/cppgc/marker.cc:519:40
    #8 0x555bdae1e56d in DrainWorklistWithPredicate<150UL, heap::base::Worklist<cppgc::internal::MarkingWorklists::EphemeronPairItem, 64>::Local, (lambda at ../../v8/src/heap/cppgc/marker.cc:518:15), (lambda at ../../v8/src/heap/cppgc/marker.cc:102:7)> ./../../v8/src/heap/cppgc/marking-state.h:454:5
    #9 0x555bdae1e56d in DrainWorklistWithBytesAndTimeDeadline<150UL, heap::base::Worklist<cppgc::internal::MarkingWorklists::EphemeronPairItem, 64>::Local, (lambda at ../../v8/src/heap/cppgc/marker.cc:518:15)> ./../../v8/src/heap/cppgc/marker.cc:101:10
    #10 0x555bdae1e56d in cppgc::internal::MarkerBase::ProcessWorklistsWithDeadline(unsigned long, v8::base::TimeTicks) ./../../v8/src/heap/cppgc/marker.cc:515:12
    #11 0x555bdae1bbe7 in cppgc::internal::MarkerBase::AdvanceMarkingWithLimits(v8::base::TimeDelta, unsigned long) ./../../v8/src/heap/cppgc/marker.cc:402:15
    #12 0x555bd9a4e686 in v8::internal::CppHeap::AdvanceTracing(double) ./../../v8/src/heap/cppgc-js/cpp-heap.cc:457:16
    #13 0x555bd9bab4bb in v8::internal::MarkCompactCollector::PerformWrapperTracing() ./../../v8/src/heap/mark-compact.cc:1900:42
    #14 0x555bd9b7cb67 in v8::internal::MarkCompactCollector::MarkLiveObjects() ./../../v8/src/heap/mark-compact.cc:2092:9
    #15 0x555bd9b7add7 in v8::internal::MarkCompactCollector::CollectGarbage() ./../../v8/src/heap/mark-compact.cc:586:3
    #16 0x555bd9af0529 in v8::internal::Heap::MarkCompact() ./../../v8/src/heap/heap.cc:2475:29
    #17 0x555bd9aeacbb in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:2205:7
   

Address 0x7ea70023a96c is a wild pointer inside of access range of size 0x000000000002.
SUMMARY: AddressSanitizer: use-after-poison (/home/test/chromium/src/out/chrome_asan_shared/swain+0x1441a056)
Shadow bytes around the buggy address:
  0x0fd56003f4d0: 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd56003f4e0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 00 00 00
  0x0fd56003f4f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd56003f500: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd56003f510: 00 00 00 f7 f7 f7 00 00 00 00 00 00 00 00 00 00
=>0x0fd56003f520: 00 00 00 00 00 00 00 00 00 00 f7 f7 f7[f7]f7 f7
  0x0fd56003f530: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd56003f540: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd56003f550: f7 f7 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd56003f560: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd56003f570: 00 00 00 00 00 00 00 00 00 00 f7 f7 f7 00 00 00
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
==2160810==ABORTING

### [Deleted User] (2021-09-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-26)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2021-09-28)

Thanks - I consistently get:

    #0 0x7ffe20250055 in WTF::Vector<std::__1::pair<WTF::AtomicString,cppgc::internal::BasicMember<blink::HeapVector<blink::RegisteredEventListener,1>,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy> >,2,blink::HeapAllocator>::size C:\src\chromium\src\third_party\blink\renderer\platform\wtf\vector.h:1184
    #1 0x7ffe20250055 in blink::EventListenerMap::Remove(class WTF::AtomicString const &, class blink::EventListener const *, class blink::EventListenerOptions const *, unsigned int *, class blink::RegisteredEventListener *) C:\src\chromium\src\third_party\blink\renderer\core\dom\events\event_listener_map.cc:192:1
    #2 0x7ffe1c0168a9 in blink::EventTarget::RemoveEventListenerInternal(class WTF::AtomicString const &, class blink::EventListener const *, class blink::EventListenerOptions const *) C:\src\chromium\src\third_party\blink\renderer\core\dom\events\event_target.cc:604:30
    #3 0x7ffe248d7b58 in blink::MediaCustomControlsFullscreenDetector::Detach(void) C:\src\chromium\src\third_party\blink\renderer\core\html\media\media_custom_controls_fullscreen_detector.cc:125:18
    #4 0x7ffe1fd1f035 in blink::HTMLVideoElement::ContextDestroyed(void) C:\src\chromium\src\third_party\blink\renderer\core\html\media\html_video_element.cc:141:41
    #5 0x7ffe18ce2bc8 in blink::ContextLifecycleObserver::NotifyContextDestroyed(void) C:\src\chromium\src\third_party\blink\renderer\platform\context_lifecycle_observer.cc:46:3
    #6 0x7ffe204f020d in blink::ContextLifecycleNotifier::NotifyContextDestroyed::<lambda_0>::operator() C:\src\chromium\src\third_party\blink\renderer\platform\context_lifecycle_notifier.cc:33

void MediaCustomControlsFullscreenDetector::Detach() {
  if (viewport_intersection_observer_) {
    viewport_intersection_observer_->disconnect();
    viewport_intersection_observer_ = nullptr;
  }
  VideoElement().removeEventListener(event_type_names::kLoadedmetadata, this,
                                     true);
  VideoElement().GetDocument().removeEventListener(
      event_type_names::kWebkitfullscreenchange, this, true);
  VideoElement().GetDocument().removeEventListener(
      event_type_names::kFullscreenchange, this, true);
  VideoElement().SetIsEffectivelyFullscreen(
      WebFullscreenVideoStatus::kNotEffectivelyFullscreen);
}


### ma...@chromium.org (2021-09-30)

Sorry for the delay looking at this. Based on the variety of stack traces here, it sounds like this might be an issue more in the allocator or garbage collection, rather than any DOM or Media code? See, e.g. https://crbug.com/chromium/1252878#c12, and the DCHECK in https://crbug.com/chromium/1252878#c5.

I'm going to change components and unassign myself. Feel free to put all of that back if you disagree.

[Monorail components: -Blink>DOM Blink>JavaScript>GarbageCollection Blink>MemoryAllocator>Partition]

### ml...@chromium.org (2021-10-01)

Looks like it could be related to https://crbug.com/chromium/1248435 which was not fully fixed as it is also somehow related to EventListenerMap.

Will try to reproduce this one now.

[Monorail components: -Blink>JavaScript>GarbageCollection -Blink>MemoryAllocator>Partition Blink>GarbageCollection]

### ml...@chromium.org (2021-10-01)

Omer found an issue that explains what we see here and is taking over fixing it. The problem is present in M94-M96.

From our understanding, it's related to https://crbug.com/chromium/1251673.

+adetaylor: Can you help us out with how to merge (and possible reward this)? The other issue was not reproducible for us. In this issue https://crbug.com/chromium/1252878#c5 (when running with our heap verifier) immediately showed us where we have a problem.

Technical tl;dr: In ephemeron processing for C++ there's a corner case where it's possible to find new ephemerons (and thus possibly new objects) that we wouldn't otherwise see during marking.

Follow up for us is checking whether we run with the right flags on the fuzzers as we switched to Oilpan library in M94 which actually has better verifiers. #5 shows that we could've caught this in a more actionable fashion.

### gi...@appspot.gserviceaccount.com (2021-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e677a6f6b257e992094b9183a958b67ecc68aa85

commit e677a6f6b257e992094b9183a958b67ecc68aa85
Author: Omer Katz <omerkatz@chromium.org>
Date: Fri Oct 01 13:20:19 2021

cppgc: Fix ephemeron iterations

If processing the marking worklists found new ephemeron pairs, but
processing the existing ephemeron pairs didn't mark new objects, marking
would stop and the newly discovered ephemeron pairs would not be
processed. This can lead to a marked key with an unmarked value.

Bug: chromium:1252878
Change-Id: I0f158f6f64490f1f06961520b4ba57fa204bd867
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3199872
Commit-Queue: Omer Katz <omerkatz@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77197}

[modify] https://crrev.com/e677a6f6b257e992094b9183a958b67ecc68aa85/src/heap/cppgc/marking-state.h
[modify] https://crrev.com/e677a6f6b257e992094b9183a958b67ecc68aa85/src/heap/cppgc/marker.cc
[modify] https://crrev.com/e677a6f6b257e992094b9183a958b67ecc68aa85/test/unittests/heap/cppgc/marker-unittest.cc


### ja...@chromium.org (2021-10-01)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-10-01)

Re https://crbug.com/chromium/1252878#c18:

- on merging, please just mark this as Fixed and then sheriffbot will apply our normal merge request guidelines.
- on rewarding, thanks. I'll arrange (via amyressler@) for the VRP panel to understand the contribution of both bugs to this solution.

### om...@chromium.org (2021-10-01)

adetaylor@ I think Michael was asking about merging this issue and https://crbug.com/chromium/1251673, as in marking one of them as duplicate.

### ad...@chromium.org (2021-10-01)

Ah. Right!

Please mark https://crbug.com/chromium/1251673 as a duplicate of this one, if you're convinced it's the same root cause.

### [Deleted User] (2021-10-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-02)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M94. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M95. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-02)

Merge review required: M95 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-02)

Merge review required: M94 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2021-10-04)

[Empty comment from Monorail migration]

### om...@chromium.org (2021-10-04)

1. This is a fix to a bug introduced in M94 that can potentially lead to a UAF.
2. crrev.com/c/3199872
3. Fix landed on canary in 96.0.4660.0
4. No
5. No Chrome OS
6. No

### am...@chromium.org (2021-10-04)

merge approved to M94 and M95, please merge to respective branches as soon as possible for both (by EOD 4 October or early tomorrow, 5 October at latest) so this fix can be included in beta RC and stable refresh this week - thanks! 

### gi...@appspot.gserviceaccount.com (2021-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/ad55ae0b84beeb29f9ca5c7b5096632dce0ecd17

commit ad55ae0b84beeb29f9ca5c7b5096632dce0ecd17
Author: Omer Katz <omerkatz@chromium.org>
Date: Fri Oct 01 13:20:19 2021

cppgc: Fix ephemeron iterations

If processing the marking worklists found new ephemeron pairs, but
processing the existing ephemeron pairs didn't mark new objects, marking
would stop and the newly discovered ephemeron pairs would not be
processed. This can lead to a marked key with an unmarked value.

(cherry picked from commit e677a6f6b257e992094b9183a958b67ecc68aa85)

Bug: chromium:1252878
Change-Id: I0f158f6f64490f1f06961520b4ba57fa204bd867
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3199872
Commit-Queue: Omer Katz <omerkatz@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#77197}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3203051
Cr-Commit-Position: refs/branch-heads/9.4@{#41}
Cr-Branched-From: 3b51863bc25492549a8bf96ff67ce481b1a3337b-refs/heads/9.4.146@{#1}
Cr-Branched-From: 2890419fc8fb9bdb507fdd801d76fa7dd9f022b5-refs/heads/master@{#76233}

[modify] https://crrev.com/ad55ae0b84beeb29f9ca5c7b5096632dce0ecd17/src/heap/cppgc/marking-state.h
[modify] https://crrev.com/ad55ae0b84beeb29f9ca5c7b5096632dce0ecd17/src/heap/cppgc/marker.cc
[modify] https://crrev.com/ad55ae0b84beeb29f9ca5c7b5096632dce0ecd17/test/unittests/heap/cppgc/marker-unittest.cc


### gi...@appspot.gserviceaccount.com (2021-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/53d43b00a7bad10750226eebc29f846beca5e157

commit 53d43b00a7bad10750226eebc29f846beca5e157
Author: Omer Katz <omerkatz@chromium.org>
Date: Fri Oct 01 13:20:19 2021

cppgc: Fix ephemeron iterations

If processing the marking worklists found new ephemeron pairs, but
processing the existing ephemeron pairs didn't mark new objects, marking
would stop and the newly discovered ephemeron pairs would not be
processed. This can lead to a marked key with an unmarked value.

(cherry picked from commit e677a6f6b257e992094b9183a958b67ecc68aa85)

Bug: chromium:1252878
Change-Id: I0f158f6f64490f1f06961520b4ba57fa204bd867
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3199872
Commit-Queue: Omer Katz <omerkatz@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#77197}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3203052
Cr-Commit-Position: refs/branch-heads/9.5@{#32}
Cr-Branched-From: 4a03d61accede9dd0e3e6dc0456ff5a0e3f792b4-refs/heads/9.5.172@{#1}
Cr-Branched-From: 9a607043cb3161f8ceae1583807bece595388108-refs/heads/main@{#76741}

[modify] https://crrev.com/53d43b00a7bad10750226eebc29f846beca5e157/src/heap/cppgc/marking-state.h
[modify] https://crrev.com/53d43b00a7bad10750226eebc29f846beca5e157/test/unittests/heap/cppgc/marker-unittest.cc
[modify] https://crrev.com/53d43b00a7bad10750226eebc29f846beca5e157/src/heap/cppgc/marker.cc


### om...@google.com (2021-10-05)

Back merges are done

### ml...@chromium.org (2021-10-05)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-06)

Congratulations - the VRP Panel has decided to award you $10,000 for this report! 
As mentioned in https://crbug.com/chromium/1252878#c18, your report help the team identify the cause of another issue that was not able to be reproduced from the other report, so we all wanted to reward you for that in addition to rewarding you for this report. Very nice work and thank you for this report! 

### am...@chromium.org (2021-10-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-07)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### om...@google.com (2021-10-08)

No reason to back merge to M90. This code was only enabled in M94.

### em...@gmail.com (2021-10-08)

After simple modification of the poc file, I can still repro this issue. Can someone check it?
version: Chromium 97.0.4665.0 gs://chromium-browser-asan/linux-release/asan-linux-release-929567.zip

READ of size 8 at 0x7ee000299b70 thread T0 (chrome)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x559a553490e2 in cppgc::internal::(anonymous namespace)::TraceConservatively(cppgc::internal::ConservativeTracingVisitor*, cppgc::internal::HeapObjectHeader const&) ./../../v8/src/heap/cppgc/visitor.cc:38
    #1 0x559a553490e2 in ?? ??:0
    #2 0x559a5531e5a4 in cppgc::internal::MarkerBase::MarkNotFullyConstructedObjects() ./../../v8/src/heap/cppgc/marker.cc:556
    #3 0x559a5531e5a4 in ?? ??:0
    #4 0x559a5531dfe0 in cppgc::internal::MarkerBase::EnterAtomicPause(cppgc::EmbedderStackState) ./../../v8/src/heap/cppgc/marker.cc:254
    #5 0x559a5531dfe0 in ?? ??:0
    #6 0x559a53f07493 in non-virtual thunk to v8::internal::CppHeap::EnterFinalPause(cppgc::EmbedderStackState) ./../../v8/src/heap/cppgc-js/cpp-heap.cc:475
    #7 0x559a53f07493 in ?? ??:0
    #8 0x559a53f1a67a in ?? ??:0
    #9 0x559a53f1a67a in v8::internal::LocalEmbedderHeapTracer::EnterFinalPause() ./../../v8/src/heap/embedder-tracing.cc:57
    #10 0x559a53f1a67a in ?? ??:0
    #11 0x559a5406a0de in v8::internal::MarkCompactCollector::MarkLiveObjects() ./../../v8/src/heap/mark-compact.cc:2080
    #12 0x559a5406a0de in ?? ??:0
    #13 0x559a54069587 in v8::internal::MarkCompactCollector::CollectGarbage() ./../../v8/src/heap/mark-compact.cc:580
    #14 0x559a54069587 in ?? ??:0
    #15 0x559a53fa76d9 in v8::internal::Heap::MarkCompact() ./../../v8/src/heap/heap.cc:2480
    #16 0x559a53fa76d9 in ?? ??:0
    #17 0x559a53fa0fbf in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:2210
    #18 0x559a53fa0fbf in ?? ??:0
    #19 0x559a53f9942d in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1793
    #20 0x559a53f9942d in ?? ??:0
    #21 0x559a53f9e6e6 in v8::internal::Heap::FinalizeIncrementalMarkingAtomically(v8::internal::GarbageCollectionReason) ./../../v8/src/heap/heap.cc:1464
    #22 0x559a53f9e6e6 in FinalizeIncrementalMarkingAtomically ./../../v8/src/heap/heap.cc:3730
    #23 0x559a53f9e6e6 in ?? ??:0
    #24 0x559a53a98710 in v8::EmbedderHeapTracer::IncreaseAllocatedSize(unsigned long) ./../../v8/src/heap/embedder-tracing.h:108
    #25 0x559a53a98710 in IncreaseAllocatedSize ./../../v8/src/api/api.cc:10071
    #26 0x559a53a98710 in ?? ??:0
    #27 0x559a55337e5f in cppgc::internal::StatsCollector::NotifySafePointForConservativeCollection() stats-collector.cc:?
    #28 0x559a55337e5f in ForAllAllocationObservers<(lambda at ../../v8/src/heap/cppgc/stats-collector.cc:82:29)> ./../../v8/src/heap/cppgc/stats-collector.h:367
    #29 0x559a55337e5f in AllocatedObjectSizeSafepointImpl ./../../v8/src/heap/cppgc/stats-collector.cc:82
    #30 0x559a55337e5f in NotifySafePointForConservativeCollection ./../../v8/src/heap/cppgc/stats-collector.cc:63
    #31 0x559a55337e5f in ?? ??:0
    #32 0x559a553284a4 in cppgc::internal::ObjectAllocator::OutOfLineAllocate(cppgc::internal::NormalPageSpace&, unsigned long, unsigned short) ./../../v8/src/heap/cppgc/object-allocator.cc:120
    #33 0x559a553284a4 in ?? ??:0
    #34 0x559a66a726b7 in blink::AutoplayPolicy::AutoplayPolicy(blink::HTMLMediaElement*) ./../../v8/include/cppgc/allocation.h:64
    #35 0x559a66a726b7 in Allocate ./../../v8/include/cppgc/allocation.h:112
    #36 0x559a66a726b7 in Call<blink::HTMLMediaElement *&> ./../../v8/include/cppgc/allocation.h:173
    #37 0x559a66a726b7 in MakeGarbageCollected<blink::AutoplayUmaHelper, blink::HTMLMediaElement *&> ./../../v8/include/cppgc/allocation.h:212
    #38 0x559a66a726b7 in MakeGarbageCollected<blink::AutoplayUmaHelper, blink::HTMLMediaElement *&> ./../../third_party/blink/renderer/platform/heap/heap.h:26
    #39 0x559a66a726b7 in AutoplayPolicy ./../../third_party/blink/renderer/core/html/media/autoplay_policy.cc:158
    #40 0x559a66a726b7 in ?? ??:0
    #41 0x559a66a20162 in blink::HTMLMediaElement::HTMLMediaElement(blink::QualifiedName const&, blink::Document&) ./../../v8/include/cppgc/allocation.h:174
    #42 0x559a66a20162 in MakeGarbageCollected<blink::AutoplayPolicy, blink::HTMLMediaElement *> ./../../v8/include/cppgc/allocation.h:212
    #43 0x559a66a20162 in MakeGarbageCollected<blink::AutoplayPolicy, blink::HTMLMediaElement *> ./../../third_party/blink/renderer/platform/heap/heap.h:26
    #44 0x559a66a20162 in HTMLMediaElement ./../../third_party/blink/renderer/core/html/media/html_media_element.cc:571
    #45 0x559a66a20162 in ?? ??:0
    #46 0x559a66a81a49 in blink::HTMLVideoElement::HTMLVideoElement(blink::Document&) ./../../third_party/blink/renderer/core/html/media/html_video_element.cc:83
    #47 0x559a66a81a49 in ?? ??:0
    #48 0x559a6864bc09 in blink::HTMLVideoConstructor(blink::Document&, blink::CreateElementFlags) ./../../v8/include/cppgc/allocation.h:174
    #49 0x559a6864bc09 in MakeGarbageCollected<blink::HTMLVideoElement, blink::Document &> ./../../v8/include/cppgc/allocation.h:212
    #50 0x559a6864bc09 in MakeGarbageCollected<blink::HTMLVideoElement, blink::Document &> ./../../third_party/blink/renderer/platform/heap/heap.h:26
    #51 0x559a6864bc09 in HTMLVideoConstructor ./gen/third_party/blink/renderer/core/html_element_factory.cc:678
    #52 0x559a6864bc09 in ?? ??:0
    #53 0x559a68637444 in blink::HTMLElementFactory::Create(WTF::AtomicString const&, blink::Document&, blink::CreateElementFlags) ./gen/third_party/blink/renderer/core/html_element_factory.cc:857
    #54 0x559a68637444 in ?? ??:0
    #55 0x559a6558bdea in blink::Document::CreateElementForBinding(WTF::AtomicString const&, blink::ExceptionState&) ./../../third_party/blink/renderer/core/dom/document.cc:1033
    #56 0x559a6558bdea in ?? ??:0
    #57 0x559a6c6ee809 in blink::(anonymous namespace)::v8_document::CreateElementOperationCallbackForMainWorld(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_document.cc:5294
    #58 0x559a6c6ee809 in CreateElementOperationCallbackForMainWorld ./gen/third_party/blink/renderer/bindings/modules/v8/v8_document.cc:5352
    #59 0x559a6c6ee809 in ?? ??:0
    #60 0x559a53b348e7 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:152
    #61 0x559a53b348e7 in ?? ??:0
    #62 0x559a53b3253e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:112
    #63 0x559a53b3253e in ?? ??:0
    #64 0x559a53b2ff9a in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:142
    #65 0x559a53b2ff9a in ?? ??:0

### rz...@google.com (2021-10-08)

Not needed on M90

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### ml...@chromium.org (2021-10-13)

Only saw #42 now. Will take a look immediately. Sorry, for not getting back to this earlier. It's likely that this is a different issue though.

### ml...@chromium.org (2021-10-13)

I branched the report in #42 into https://crbug.com/chromium/1259587 to track this specifically.

### kb...@chromium.org (2021-10-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### pa...@chromium.org (2021-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-13)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1252878?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1249381, crbug.com/chromium/1252879, crbug.com/chromium/1253291]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057384)*
