# V8 Undefined Behavior to Sandbox Bypass: Perfetto

| Field | Value |
|-------|-------|
| **Issue ID** | [480442279](https://issues.chromium.org/issues/480442279) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | V8 version 14.5.0 (candidate) |
| **Reporter** | am...@gmail.com |
| **Assignee** | om...@chromium.org |
| **Created** | 2026-02-01 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# Steps to reproduce the problem

1. Found with code analysis

# Problem Description

Hi Team during code analysis found below snippet is vulnerable for undefined behavior which will lead to sandbox bypass

Below code snippet in **code-data-source.cc**

```
InternedV8JsScript::Type GetJsScriptType(Tagged<Script> script) {
  if (script->compilation_type() == Script::CompilationType::kEval) {
    return InternedV8JsScript::TYPE_EVAL;
  }

  // TODO(carlscab): Camillo to extend the Script::Type enum. compilation_type
  // will no longer be needed.

  switch (script->type()) {
    case Script::Type::kNative:
      return InternedV8JsScript::TYPE_NATIVE;
    case Script::Type::kExtension:
      return InternedV8JsScript::TYPE_EXTENSION;
    case Script::Type::kNormal:
      return InternedV8JsScript::TYPE_NORMAL;
#if V8_ENABLE_WEBASSEMBLY
    case Script::Type::kWasm:
      UNREACHABLE();
#endif  // V8_ENABLE_WEBASSEMBLY
    case Script::Type::kInspector:
      return InternedV8JsScript::TYPE_INSPECTOR;
  }
}

```

The above code uses switch case to decide the return statement but there is no default or unreachable checks involved since the type obtained from v8 heap it can be modified using background helper and results in Unintended Behaviour to sandbox bypass

It is called via **InternJsScript** method in same code

```
uint64_t CodeDataSourceIncrementalState::InternJsScript(Isolate& isolate,
                                                        Tagged<Script> script) {
  auto [it, was_inserted] = scripts_.emplace(
      CodeDataSourceIncrementalState::ScriptUniqueId{isolate.id(),
                                                     script->id()},
      next_script_iid());
  uint64_t iid = it->second;
  if (!was_inserted) {
    return iid;
  }

  auto* proto = serialized_interned_data_->add_v8_js_script();
  proto->set_iid(iid);
  proto->set_script_id(script->id());
  proto->set_type(GetJsScriptType(script));   <------------------ here
  if (IsString(script->name())) {
    PerfettoV8String(Cast<String>(script->name()))
        .WriteToProto(*proto->set_name());
  }
  if (log_script_sources() && IsString(script->source())) {
    PerfettoV8String(Cast<String>(script->source()))
        .WriteToProto(*proto->set_source());
  }

  return iid;
}

```

further **InternJsScript** method is called in **perfetto-logger.cc**

```
void PerfettoLogger::CodeCreateEvent(CodeTag tag,
                                     DirectHandle<AbstractCode> abstract_code,
                                     DirectHandle<SharedFunctionInfo> info,
                                     DirectHandle<Name> script_name, int line,
                                     int column) {
  DisallowGarbageCollection no_gc;
  DCHECK(IsScript(info->script()));

  CodeDataSource::Trace(
      [&](v8::internal::CodeDataSource::TraceContext trace_context) {
        CodeTraceContext ctx = NewCodeTraceContext(trace_context);

        auto* code_proto = ctx.set_v8_js_code();
        code_proto->set_v8_isolate_iid(ctx.InternIsolate(isolate_));
        code_proto->set_v8_js_function_iid(ctx.InternJsFunction(
            isolate_, info,
            ctx.InternJsScript(isolate_, Cast<Script>(info->script())), line,    <----------------------------------here
            column));
        WriteJsCode(&isolate_, ctx, *abstract_code, *code_proto);
      });
}

```

Note: in this issue i wasnt able to reach this area since it requires many flag and still im surfing on this, but as per code this is vulnerable, so raised it

In Build gn args: v8\_use\_perfetto = true is mandatory in d8 running arg: --perfetto-code-logger --enable-tracing is mandatory

This will invoke the perfetto initialize in d8 main code but below code in perfetto-logger.cc didnt add the listener, in all the case the num\_active\_data\_sources\_ is 0

```
void Register(Isolate* isolate) {
    auto logger = std::make_unique<PerfettoLogger>(isolate);
    base::MutexGuard lock(&mutex_);
    if (num_active_data_sources_ != 0) {
      isolate->logger()->AddListener(logger.get());
    }
    CHECK(isolates_.emplace(isolate, std::move(logger)).second);
  }

```

num\_active\_data\_sources\_ is incremented on same file

```
  void OnCodeDataSourceStart() {
    base::MutexGuard lock(&mutex_);
    ++num_active_data_sources_;
    if (num_active_data_sources_ == 1) {
      StartLogging(lock);
    }
    LogExistingCodeForAllIsolates(lock);
  }

```

This will be invoked from in code-data-source.cc

```
void CodeDataSource::OnStart(const StartArgs&) {
  PerfettoLogger::OnCodeDataSourceStart();
}

```

These are my current traces and im trying to enable the perfetto properly to trigger this path.

My d8 args: --allow-natives-syntax --enable-tracing --perfetto-code-logger --log-code --fuzzing --sandbox-fuzzing --single-threaded --expose-gc poc.js
Kindly share details on where it was missed to initialize the onstart method in perfetto, where it is missed in the flow (experts need your inputs)

Note: once i successfully enabled perfetto in v8 i will try to share working POC

# Summary

V8 Undefined Behavior to Sandbox Bypass: Perfetto

# Custom Questions

#### Reporter credit:

Ameen Basha M K

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [code-data-source-UB-Fix.patch](attachments/code-data-source-UB-Fix.patch) (text/x-diff, 443 B)
- [poc_arbitrary_rip.js](attachments/poc_arbitrary_rip.js) (text/javascript, 1.3 KB)
- [reproduction.patch](attachments/reproduction.patch) (text/x-diff, 1.2 KB)
- [perfetto_controlled_write.webm](attachments/perfetto_controlled_write.webm) (video/webm, 3.2 MB)

## Timeline

### am...@gmail.com (2026-02-01)

Impact will be similar to this issue
Ref:https://issues.chromium.org/issues/390568183

### am...@gmail.com (2026-02-01)

Bisection Details:
Commit Link: https://chromium.googlesource.com/v8/v8/+/0016438c83ed01061d40f1cc59bb96cf89430cd5%5E%21/src/tracing/code-data-source.cc
Commit ID : 0016438c83ed01061d40f1cc59bb96cf89430cd5 

Introduced on Jan 24 2024

### an...@chromium.org (2026-02-01)

Thanks for the report. Please do try to provide a PoC as it really helps with our debugging process.
I'll provisionally triage it for the V8 shepherd to take a quick look at the information already present.

### am...@gmail.com (2026-02-02)

Hi yes, trying to enable perfetto in v8 for poc, but facing above issue, Any leads to reach the PerfettoV8String method? seems the issue was in listener addition, not working in my v8 seems it is common issue, Did i miss any flags to achieve this?

### ta...@google.com (2026-02-02)

Hi Toon, CYPTAL as you reviewed the commit?

### ch...@google.com (2026-02-02)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### am...@gmail.com (2026-02-03)

Patch:

To fix this issue default case should be attached with UNREACHABLE() to avoid any Undefined Behaviour in this area

Added a patch file here, let me know whether it is fine for patch bonus or should i have to raise it via gerrit?



### om...@google.com (2026-02-05)

Thanks for the report!
A fix is in flight.

### dx...@google.com (2026-02-05)

Project: v8/v8  

Branch:  main  

Author:  Omer Katz [omerkatz@chromium.org](mailto:omerkatz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7544573>

Add UNREACHABLE after exhaustive switch in code-data-source.cc

---


Expand for full commit details
```
     
    Bug: 480442279 
    Change-Id: Ic16b9291a8931a0a0b5115cc9450249ce26b6903 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7544573 
    Commit-Queue: Omer Katz <omerkatz@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Auto-Submit: Omer Katz <omerkatz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105095}

```

---

Files:

- M `src/tracing/code-data-source.cc`

---

Hash: [a53e590365adf4c3e3126d9e9472f1892571ed18](https://chromiumdash.appspot.com/commit/a53e590365adf4c3e3126d9e9472f1892571ed18)  

Date: Thu Feb 5 13:01:40 2026


---

### am...@gmail.com (2026-02-17)

Team, Kindly share the bounty details

### am...@gmail.com (2026-02-24)

Gentle Reminder Kindly update the bounty details

### am...@gmail.com (2026-03-09)

Friendly Ping For Bounty Update

### sp...@google.com (2026-03-11)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

No POC, does not demonstrate as per the v8 sandbox bypass requirements

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### am...@gmail.com (2026-03-14)

Hi Team i have attached a **poc with sandbox bypass to controlled PC `0x414141414141`**

Kindly reinitiate the VRP Process with updated poc details for bounty allocation

**For VRP:** `initially i have attached the Bisection and Fix Patch too` 

Steps to Reproduce:

1. apply the patch (This is to Enable code data source so perfetto can be called, also since the fix is deployed in latest branch i just removed the fix for poc)
2. Build v8 with below attached Build args
3. run ./d8 --enable-tracing --perfetto-code-logger --sandbox-fuzzing --allow-natives-syntax --disable-in-process-stack-traces poc\_arbitrary\_rip.js
4. You can see the crash at 0x414141414141

Attached a poc to show the crash address details (Tested on latest with attached patch)

Asan Crash:

```
## V8 sandbox violation detected!

AddressSanitizer:DEADLYSIGNAL
=================================================================
==144471==ERROR: AddressSanitizer: SEGV on unknown address 0x414141414141 (pc 0x414141414141 bp 0x7fff4f668cf0 sp 0x7fff4f668c00 T0)
==144471==The signal is caused by a READ memory access.
    #0 0x414141414141  (<unknown module>)
    #1 0x63bacd46693d in InternJsScript src/tracing/code-trace-context.h:50:31
    #2 0x63bacd46693d in operator() src/tracing/perfetto-logger.cc:357:17
    #3 0x63bacd46693d in TraceWithInstances<perfetto::DataSource<v8::internal::CodeDataSource, v8::internal::CodeDataSourceTraits>::DefaultTracePointTraits, (lambda at ../../src/tracing/perfetto-logger.cc:350:7)> third_party/perfetto/include/perfetto/tracing/data_source.h:465:7
    #4 0x63bacd46693d in void perfetto::DataSource<v8::internal::CodeDataSource, v8::internal::CodeDataSourceTraits>::Trace<v8::internal::PerfettoLogger::CodeCreateEvent(v8::internal::LogEventListener::CodeTag, v8::internal::DirectHandle<v8::internal::AbstractCode>, v8::internal::DirectHandle<v8::internal::SharedFunctionInfo>, v8::internal::DirectHandle<v8::internal::Name>, int, int)::$_0>(v8::internal::PerfettoLogger::CodeCreateEvent(v8::internal::LogEventListener::CodeTag, v8::internal::DirectHandle<v8::internal::AbstractCode>, v8::internal::DirectHandle<v8::internal::SharedFunctionInfo>, v8::internal::DirectHandle<v8::internal::Name>, int, int)::$_0)::'lambda'(unsigned int)::operator()(unsigned int) const third_party/perfetto/include/perfetto/tracing/data_source.h:405:7
    #5 0x63bacd45fb0d in CallIfEnabled<perfetto::DataSource<v8::internal::CodeDataSource, v8::internal::CodeDataSourceTraits>::DefaultTracePointTraits, (lambda at ../../third_party/perfetto/include/perfetto/tracing/data_source.h:404:44)> third_party/perfetto/include/perfetto/tracing/data_source.h:435:5
    #6 0x63bacd45fb0d in Trace<(lambda at ../../src/tracing/perfetto-logger.cc:350:7)> third_party/perfetto/include/perfetto/tracing/data_source.h:404:5
    #7 0x63bacd45fb0d in v8::internal::PerfettoLogger::CodeCreateEvent(v8::internal::LogEventListener::CodeTag, v8::internal::DirectHandle<v8::internal::AbstractCode>, v8::internal::DirectHandle<v8::internal::SharedFunctionInfo>, v8::internal::DirectHandle<v8::internal::Name>, int, int) src/tracing/perfetto-logger.cc:349:3
    #8 0x63bacb550831 in CodeCreateEvent src/logging/code-events.h:193:17
    #9 0x63bacb550831 in v8::internal::Compiler::LogFunctionCompilation(v8::internal::Isolate*, v8::internal::LogEventListener::CodeTag, v8::internal::DirectHandle<v8::internal::Script>, v8::internal::DirectHandle<v8::internal::SharedFunctionInfo>, v8::internal::DirectHandle<v8::internal::FeedbackVector>, v8::internal::DirectHandle<v8::internal::AbstractCode>, v8::internal::CodeKind, double) src/codegen/compiler.cc:306:20
    #10 0x63bacb56574d in LogUnoptimizedCompilation src/codegen/compiler.cc:426:3
    #11 0x63bacb56574d in v8::internal::(anonymous namespace)::FinalizeUnoptimizedCompilation(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Script>, v8::internal::UnoptimizedCompileFlags const&, v8::internal::UnoptimizedCompileState const*, std::__Cr::vector<v8::internal::FinalizeUnoptimizedCompilationData, std::__Cr::allocator<v8::internal::FinalizeUnoptimizedCompilationData>> const&) src/codegen/compiler.cc:1481:5
    #12 0x63bacb567f7a in v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*, v8::internal::CreateSourcePositions) src/codegen/compiler.cc:3064:3
    #13 0x63bacb56a8b1 in v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*) src/codegen/compiler.cc:3113:8
    #14 0x63bacc944ccd in __RT_impl_Runtime_CompileLazy src/runtime/runtime-compiler.cc:88:8
    #15 0x63bacc944ccd in v8::internal::Runtime_CompileLazy(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-compiler.cc:69:1
    #16 0x63bad029dcb5 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #17 0x63bad01edddc in Builtins_CompileLazy setup-isolate-deserialize.cc
    #18 0x63bad01ec8bb in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #19 0x63bad01e965b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #20 0x63bad01e93aa in Builtins_JSEntry setup-isolate-deserialize.cc
    #21 0x63bacb731666 in Call src/execution/simulator.h:216:12
    #22 0x63bacb731666 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:474:22
    #23 0x63bacb732bd8 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) src/execution/execution.cc:574:10
    #24 0x63bacb3ad7c2 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2034:7
    #25 0x63bacac88137 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:1041:44
    #26 0x63bacacc0809 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:5665:10
    #27 0x63bacacccd0d in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:6684:37
    #28 0x63bacaccc145 in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:6592:18
    #29 0x63bacaccf96b in v8::Shell::Main(int, char**) src/d8/d8.cc:7506:18
    #30 0x7fc4c542a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #31 0x7fc4c542a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #32 0x63bacab7f029 in _start (/home/basha/Desktop/v8fuzz/v8/out/asan/d8+0x14bc029) (BuildId: 28e9176861523183)

==144471==Register values:
rax = 0x000063bacd739823  rbx = 0x00007fff4f668c00  rcx = 0x000063baca4045e8  rdx = 0x0000000000000003  
rdi = 0x00007a830101efc4  rsi = 0x0000000000000183  rbp = 0x00007fff4f668cf0  rsp = 0x00007fff4f668c00  
 r8 = 0x00000fba989026a1   r9 = 0x00007dd4c481350a  r10 = 0x00000fba989026a1  r11 = 0x00000fbb188fa6a0  
r12 = 0x00007a830101efad  r13 = 0x00007bc4c356d800  r14 = 0x0000000000000003  r15 = 0x00007dd4c4813502  
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (<unknown module>) 
==144471==ABORTING


```

Build Args:

```
is_debug = false
is_asan = true
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true
dcheck_always_on = false
v8_static_library = true
v8_fuzzilli = false
target_cpu = "x64"
v8_use_perfetto = true

```

### jk...@chromium.org (2026-03-16)

#15: Reads are not sandbox violations. Can you demonstrate a write? Also, I think (but I'm not sure) that ASan instrumentation can confuse the automatic detection of what counts as valid sandbox escape, so to get more reliable reports I recommend using non-ASan builds for sandbox testing.

EDIT: Just noticed that this appears to control the PC, which does sound more scary. Then again this needs to apply a custom patch. Can you control the PC with an official shipping build? What really matters is whether Chrome users are affected. If you need to play custom tricks with `d8`, then it's not a vulnerability in the wild.

### am...@gmail.com (2026-03-16)

Hi yes it is a controlled PC `0x414141414141`, As stated in description i tried to enable via flags but it didnt work as per my analysis, i asked for quick help on this from chrome team

---

So i just patched to enable the perfetto code source

The tracing-controller.cc change is NOT removing a security fix — it's d8 test infrastructure configuration. It makes d8 activate the "dev.v8.code" Perfetto data source, which Chrome can already do natively through its tracing UI (DevTools → Performance recording, chrome://tracing).

In Chrome, the code path is reachable when:

--js-flags=--perfetto-code-logger is set (enables CodeDataSource::Register())
A performance trace is started that includes dev.v8.code

Note: perfetto is available on chrome already, The patch didnt introduce this bug, patch just enabled the feature (which i struggle to enable)

---

So in general it is controlled PC attack on release build(if the feature is enabled in v8) (or) chrome

hope `mini patch to reproduce the bugs are acceptable until the patch intentionally introduce the bug, so in this way it is acceptable` i think

Additional note: in patch i have removed the fix (which deployed for this issue) too just to show the impact in latest (Removal of unreachable() is not needed in previous vulnerable builds)

### am...@gmail.com (2026-03-17)

Team Kindly add the reward-topanel hotlists again for VRP Bounty Discussion (Poc for controlled PC `0x414141414141` is attached on [comment #15](https://issues.chromium.org/issues/480442279#comment15))

Issue is already fixed, Bounty alone pending

### ml...@google.com (2026-03-17)

The VRP hotlist is already on the bug. This is still in progress. The bug should be considered as demonstrated write access for the sandbox.

Mitigating factors: This actually needs perfetto tracing which is not enabled by default.

### am...@gmail.com (2026-03-17)

Thanks for the update, Yes chrome can enable this with flag, but since the feature is available in stable anyone consuming v8 can be vulnerable for using this feature (eg: nodejs, if they consume this feature since the feature is in stable, so i hope this will be falls as stable one in v8 )

so the issue will be automatically discussed on next VRP meet? no need of any tracking from my end right?

When i track the reward-topanel my other eligible bugs are showing other than this one so the confusion

Since this scenario is new, these questions arise, will be rectified in future issues

### ml...@chromium.org (2026-03-17)

> Thanks for the update, Yes chrome can enable this with flag, but since the feature is available in stable anyone consuming v8 can be vulnerable for using this feature (eg: nodejs, if they consume this feature since the feature is in stable, so i hope this will be falls as stable one in v8 )

We do not track vulnerabilities in Node.

I will ping the VRP folks here.

### ml...@google.com (2026-03-18)

You can ask for re-assessment at [security@chromium.org](mailto:security@chromium.org). That should come from you as a reporter.

### aj...@google.com (2026-03-18)

Reporter asks for reassessment.

### am...@gmail.com (2026-04-09)

Friendly ping, kindly update the bounty details

### am...@gmail.com (2026-04-26)

VRP Team, Any update on bounty for controlled PC POC updated above in comment15

### am...@gmail.com (2026-05-05)

VRP Team, Its been around 2 months for bounty reassessment request, Kindly update the bounty details

### aj...@google.com (2026-05-12)

The panel has reassessed and we do not believe this manifests in a shipped version of Chrome. Sorry.

### am...@gmail.com (2026-05-12)

Chrome ships perfetto in stable with a flag support, Why the conclusion was different

My previous perfetto issues of same category are awarded, why the same is not applicable here

The patch are use to only enable the perferto in standalone v8, it was available on chrome with a flag

Kindly reassess this case, as this was a controlled PC issue with higher bounty range in sandbox bypass

### ch...@google.com (2026-05-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### aj...@google.com (2026-05-19)

The panel only considers information provided at or close the time of the initial bug report and will not be providing any further updates or assessments of this issue.

### am...@gmail.com (2026-05-19)

I have updated the poc within 2 days of initial VRP assessment, it wasnt a big delay

Also i have intially attached the struggles to enable to perfetto in v8 and clearly explains the bug will lead to UB

The only delay is submission of poc post assessment but that doesnt lower the severity of the issue anyway

Request for bounty reassessment since the issue was fixed and feature shipped in chrome, also a poc was submitted for exploit

## Bounty Award

> No POC, does not demonstrate as per the v8 sandbox bypass requirements
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/480442279)*
