# V8 Sandbox Bypass: UB in MessageHandler::GetMessage because of invalid MessageTemplate variant

| Field | Value |
|-------|-------|
| **Issue ID** | [390568183](https://issues.chromium.org/issues/390568183) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | v8...@gmail.com |
| **Assignee** | sr...@google.com |
| **Created** | 2025-01-17 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

During the construction of an error message, the `MessageTemplate` variant used for formatting is read from on-heap data and used in a switch instruction. This probably can be mitigated by using a sbx check in `MessageTemplateFromInt()` (`src/common/message-template.h:762`)

#### VERSION

V8 commit: `ab875b6ed878b0b1934ab935366224ee4c761985` (2025-01-15T14:21:08+00:00)

#### REPRODUCTION CASE

This report does not include a reproducer since an attacker can change the on-heap data only within a narrow time frame, making the bug hard to trigger using the memory corruption API.

The exploitable behavior can be triggered by the JS code below, which constructs the following error message: `Invalid asm.js: Unexpected token`.

```
const t0 = eval((((((((((((("function Module(stdlib, foreign, heap) {\n" + " \"use asm\";\n") + " function ") + "nQU") + "(dividend) {\n") + "") + "  return ((dividend | 0) % ") + 7) + ") | 0;\n") + " }\n") + " return { f: ") + "nQU") + "}\n") + "}; Module");
t0().f();

```

During the construction of the error message, an attacker can change the type (`MessageTemplate`) of the error message before it is loaded here:

```
    #2 0x55555decd3f2 in v8::internal::TaggedField<v8::internal::Smi, 12, v8::internal::V8HeapCompressionSchemeImpl<v8::internal::MainCage>>::load(v8::internal::Tagged<v8::internal::HeapObject>, int) src/objects/tagged-field-inl.h:214:20
    #3 0x55555decd14b in v8::internal::JSMessageObject::raw_type() const src/objects/js-objects-inl.h:728:1
    #4 0x55555de86e34 in v8::internal::JSMessageObject::type() const src/objects/js-objects-inl.h:716:33
    #5 0x55555de84ef9 in v8::internal::MessageHandler::GetMessage(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>) src/execution/messages.cc:190:53
    #6 0x55555c56ee43 in v8::Message::Get() const src/api/api.cc:3087:22
    #7 0x55555c0236e8 in v8::PrintMessageCallback(v8::Local<v8::Message>, v8::Local<v8::Value>) src/d8/d8.cc:4093:47
    #8 0x55555de836c0 in v8::internal::MessageHandler::ReportMessageNoExceptions(v8::internal::Isolate*, v8::internal::MessageLocation const*, v8::internal::DirectHandle<v8::internal::Object>, v8::Local<v8::Value>) src/execution/messages.cc:178:9
    #9 0x55555de7e32b in v8::internal::MessageHandler::ReportMessage(v8::internal::Isolate*, v8::internal::MessageLocation const*, v8::internal::DirectHandle<v8::internal::JSMessageObject>) src/execution/messages.cc:103:5
    #10 0x555561d69eae in v8::internal::PendingCompilationErrorHandler::ReportWarnings(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Script>) const src/parsing/pending-compilation-error-handler.cc:155:5
    #11 0x55555d3b1ae3 in v8::internal::(anonymous namespace)::FinalizeUnoptimizedCompilation(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Script>, v8::internal::UnoptimizedCompileFlags const&, v8::internal::UnoptimizedCompileState const*, std::__Cr::vector<v8::internal::FinalizeUnoptimizedCompilationData, std::__Cr::allocator<v8::internal::FinalizeUnoptimizedCompilationData>> const&) src/codegen/compiler.cc:1481:45
    #12 0x55555d3bde43 in v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*, v8::internal::CreateSourcePositions) src/codegen/compiler.cc:2947:3
    #13 0x55555d3c336c in v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*) src/codegen/compiler.cc:2996:8
    #14 0x5555628a2812 in v8::internal::Runtime_CompileLazy(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-compiler.cc:74:8
    #15 0x55556aee9c35 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #16 0x55556ae44312 in Builtins_CompileLazy setup-isolate-deserialize.cc
    #17 0x55556ae42e40 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #18 0x55556ae4091b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #19 0x55556ae4066a in Builtins_JSEntry setup-isolate-deserialize.cc
    #20 0x55555daf5283 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) src/execution/simulator.h:191:12
    #21 0x55555dae71e0 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:437:22
    #22 0x55555dae8acd in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:537:10
    #23 0x55555c52c654 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2156:7
    #24 0x55555c52b06c in v8::Script::Run(v8::Local<v8::Context>) src/api/api.cc:2119:10
    #25 0x55555bf7679a in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1018:44
    #26 0x55555c031e53 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4869:10
    #27 0x55555c0505fa in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5907:37
    #28 0x55555c04e514 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5816:18
    #29 0x55555c05788b in v8::Shell::Main(int, char**) src/d8/d8.cc:6714:18
    #30 0x55555c059781 in main src/d8/d8.cc:6806:43
    #31 0x7ffff7a211c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #32 0x7ffff7a2128a in __libc_start_main csu/../csu/libc-start.c:360:3
    #33 0x55555bd43029 in _start (/work/v8-build/v8/out/FuzzingSuppressReadsO1/d8+0x67ef029) (BuildId: cbaa25b471887c0f)

```

The value read above is then used here and causes UB:

```
AddressSanitizer:DEADLYSIGNAL
=================================================================
==1034178==ERROR: AddressSanitizer: ILL on unknown address 0x55555dea597b (pc 0x55555dea597b bp 0x7fffffff3e90 sp 0x7fffffff3e70 T0)
    #0 0x55555dea597b in v8::internal::MessageFormatter::TemplateString(v8::internal::MessageTemplate) src/execution/messages.cc:433:3
    #1 0x55555de9bb36 in v8::internal::MessageFormatter::TryFormat(v8::internal::Isolate*, v8::internal::MessageTemplate, v8::base::Vector<v8::internal::DirectHandle<v8::internal::String> const>) src/execution/messages.cc:439:33
    #2 0x55555de85836 in v8::internal::MessageFormatter::Format(v8::internal::Isolate*, v8::internal::MessageTemplate, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) src/execution/messages.cc:408:45
    #3 0x55555de84f96 in v8::internal::MessageHandler::GetMessage(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>) src/execution/messages.cc:190:10
    #4 0x55555c56ee43 in v8::Message::Get() const src/api/api.cc:3087:22
    #5 0x55555c0236e8 in v8::PrintMessageCallback(v8::Local<v8::Message>, v8::Local<v8::Value>) src/d8/d8.cc:4093:47
    #6 0x55555de836c0 in v8::internal::MessageHandler::ReportMessageNoExceptions(v8::internal::Isolate*, v8::internal::MessageLocation const*, v8::internal::DirectHandle<v8::internal::Object>, v8::Local<v8::Value>) src/execution/messages.cc:178:9
    #7 0x55555de7e32b in v8::internal::MessageHandler::ReportMessage(v8::internal::Isolate*, v8::internal::MessageLocation const*, v8::internal::DirectHandle<v8::internal::JSMessageObject>) src/execution/messages.cc:103:5
    #8 0x555561d69eae in v8::internal::PendingCompilationErrorHandler::ReportWarnings(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Script>) const src/parsing/pending-compilation-error-handler.cc:155:5
    #9 0x55555d3b1ae3 in v8::internal::(anonymous namespace)::FinalizeUnoptimizedCompilation(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Script>, v8::internal::UnoptimizedCompileFlags const&, v8::internal::UnoptimizedCompileState const*, std::__Cr::vector<v8::internal::FinalizeUnoptimizedCompilationData, std::__Cr::allocator<v8::internal::FinalizeUnoptimizedCompilationData>> const&) src/codegen/compiler.cc:1481:45
    #10 0x55555d3bde43 in v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*, v8::internal::CreateSourcePositions) src/codegen/compiler.cc:2947:3
    #11 0x55555d3c336c in v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*) src/codegen/compiler.cc:2996:8
    #12 0x5555628a2812 in v8::internal::Runtime_CompileLazy(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-compiler.cc:74:8
    #13 0x55556aee9c35 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #14 0x55556ae44312 in Builtins_CompileLazy setup-isolate-deserialize.cc
    #15 0x55556ae42e40 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #16 0x55556ae4091b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #17 0x55556ae4066a in Builtins_JSEntry setup-isolate-deserialize.cc
    #18 0x55555daf5283 in v8::internal::GeneratedCode<unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**>::Call(unsigned long, unsigned long, unsigned long, unsigned long, long, unsigned long**) src/execution/simulator.h:191:12
    #19 0x55555dae71e0 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:437:22
    #20 0x55555dae8acd in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:537:10
    #21 0x55555c52c654 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2156:7
    #22 0x55555c52b06c in v8::Script::Run(v8::Local<v8::Context>) src/api/api.cc:2119:10
    #23 0x55555bf7679a in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1018:44
    #24 0x55555c031e53 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4869:10
    #25 0x55555c0505fa in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5907:37
    #26 0x55555c04e514 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5816:18
    #27 0x55555c05788b in v8::Shell::Main(int, char**) src/d8/d8.cc:6714:18
    #28 0x55555c059781 in main src/d8/d8.cc:6806:43
    #29 0x7ffff7a211c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #30 0x7ffff7a2128a in __libc_start_main csu/../csu/libc-start.c:360:3
    #31 0x55555bd43029 in _start (/work/v8-build/v8/out/FuzzingSuppressReadsO1/d8+0x67ef029) (BuildId: cbaa25b471887c0f)


## V8 sandbox violation detected!

```
#### CREDIT INFORMATION

Reporter credit: v8sbxfuzz

## Timeline

### ad...@google.com (2025-01-17)

Security shepherd: adding provisional triage labels as is normal for V8 sandbox bypasses.

### 24...@project.gserviceaccount.com (2025-01-20)

ClusterFuzz testcase 5451093869789184 appears to be flaky, updating reproducibility hotlist.

### ap...@google.com (2025-01-20)

Project: v8/v8  

Branch: main  

Author: Stephen Roettger <[sroettger@google.com](mailto:sroettger@google.com)>  

Link:      <https://chromium-review.googlesource.com/6185429>

[sandbox] fix UB after switch on MessageTemplate enum

---


Expand for full commit details
```
[sandbox] fix UB after switch on MessageTemplate enum 
 
MessageFormatter::TemplateString doesn't have a return after the 
exhaustive switch on the MessageTemplate enum. This is UB if the enum 
value can be outside of the range of the declared enum values. 
 
Fixed: 390568183 
Bug: 390617721 
Change-Id: Ifb94d176e0c422807408cebad467066154c36b26 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6185429 
Commit-Queue: Stephen Röttger <sroettger@google.com> 
Reviewed-by: Igor Sheludko <ishell@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98205}

```

---

Files:

- M `src/execution/messages.cc`

---

Hash: 96bafadad1d70c89bef472895ec0e1a837c31e6f  

Date:  Mon Jan 20 17:21:28 2025


---

### sp...@google.com (2025-01-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
v8 sandbox bypass demonstrating memory corruption outside the v8 sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-29)

Congratulations v8sbxfuzz! Thank you for your efforts fuzzing the V8 heap sandbox -- nice work!

### ch...@google.com (2025-04-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/390568183)*
