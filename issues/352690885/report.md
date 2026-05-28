# Fatal error in Bytecode mismatch at offset 8 in interpreter.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [352690885](https://issues.chromium.org/issues/352690885) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>GarbageCollection, Blink>JavaScript>Parser, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ta...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2024-07-12 |
| **Bounty** | $8,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

All tests were performed on d8 12.6.228.21 Latest Release (Debug and Release) with the following args.gn:

Release:

```
is_component_build = false
is_debug = false
target_cpu = "x64"
v8_enable_sandbox = true
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
v8_enable_verify_heap = true
dcheck_always_on = false

```

Debug:

```
is_component_build = true
is_debug = true
symbol_level = 2
target_cpu = "x64"
v8_enable_sandbox = true
v8_enable_backtrace = true
v8_enable_fast_mksnapshot = true
v8_enable_slow_dchecks = true
v8_optimized_debug = false

```

Multiple DChecks can be hit on v8 leading to different Bytecode Mismatches and invalid JavaScript results (see testcase\_5.js, testcase\_6.js).

```
testcase_1.js (d8 debug)

#
# Fatal error in ../../src/ast/scopes.cc, line 1550
# Debug check failed: scope->outer_scope()->is_class_scope().
#
#
#
#FailureMessage Object: 0x7ffdfc76f9b8
==== C stack trace ===============================

    v8_12.6.228.21/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7f9d789e0b0e]
    v8_12.6.228.21/v8/out/x64.debug/libv8_libplatform.so(+0x52b2d) [0x7f9d6e1ddb2d]
    v8_12.6.228.21/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x1ea) [0x7f9d789b112a]
    v8_12.6.228.21/v8/out/x64.debug/libv8_libbase.so(+0x57afc) [0x7f9d789b0afc]
    v8_12.6.228.21/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x55) [0x7f9d789b1215]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Scope::GetHomeObjectScope()+0x109) [0x7f9d74569e79]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Scope::ResolveVariable(v8::internal::VariableProxy*)+0x9a) [0x7f9d7456ceca]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Scope::ResolveVariablesRecursively(v8::internal::Scope*)+0x21a) [0x7f9d7456b68a]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::DeclarationScope::AllocateVariables(v8::internal::ParseInfo*)+0xfb) [0x7f9d74567f4b]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::DeclarationScope::Analyze(v8::internal::ParseInfo*)+0x33d) [0x7f9d74567dad]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(void v8::internal::Parser::PostProcessParseResult<v8::internal::Isolate>(v8::internal::Isolate*, v8::internal::ParseInfo*, v8::internal::FunctionLiteral*)+0xcf) [0x7f9d755b25cf]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Parser::ParseProgram(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Script>, v8::internal::ParseInfo*, v8::internal::MaybeHandle<v8::internal::ScopeInfo>)+0x4c2) [0x7f9d755a2af2]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::parsing::ParseProgram(v8::internal::ParseInfo*, v8::internal::Handle<v8::internal::Script>, v8::internal::MaybeHandle<v8::internal::ScopeInfo>, v8::internal::Isolate*, v8::internal::parsing::ReportStatisticsMode)+0x246) [0x7f9d755fe746]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x64b826c) [0x7f9d746b826c]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Compiler::GetFunctionFromEval(v8::internal::Handle<v8::internal::String>, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Handle<v8::internal::Context>, v8::internal::LanguageMode, v8::internal::ParseRestriction, int, int, int, v8::internal::ParsingWhileDebugging)+0x9d5) [0x7f9d746b9875]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x75c19d3) [0x7f9d757c19d3]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x75bf64b) [0x7f9d757bf64b]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Runtime_ResolvePossiblyDirectEval(int, unsigned long*, v8::internal::Isolate*)+0x106) [0x7f9d757bf326]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x5a83378) [0x7f9d73c83378]
Trace/breakpoint trap

```
```
testcase_2.js (d8 debug)

#
# Fatal error in gen/torque-generated/src/objects/js-objects-tq-inl.inc, line 33
# Check failed: !v8::internal::v8_flags.enable_slow_asserts.value() || (IsJSReceiver_NonInline(*this)).
#
#
#
#FailureMessage Object: 0x7ffcff6d27d8
==== C stack trace ===============================

    v8_12.6.228.21/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7f2ab75ecb0e]
    v8_12.6.228.21/v8/out/x64.debug/libv8_libplatform.so(+0x52b2d) [0x7f2ab7542b2d]
    v8_12.6.228.21/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x1ea) [0x7f2ab75bd12a]
    ./d8(v8::internal::TorqueGeneratedJSReceiver<v8::internal::JSReceiver, v8::internal::HeapObject>::TorqueGeneratedJSReceiver(unsigned long)+0xa4) [0x5564804f0fc4]
    ./d8(v8::internal::JSReceiver::JSReceiver(unsigned long)+0x1d) [0x5564804f0ecd]
    ./d8(v8::internal::TorqueGeneratedJSObject<v8::internal::JSObject, v8::internal::JSReceiver>::TorqueGeneratedJSObject(unsigned long)+0x21) [0x5564804f0e21]
    ./d8(v8::internal::JSObject::JSObject(unsigned long)+0x1d) [0x5564804f0dad]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::TorqueGeneratedJSObject<v8::internal::JSObject, v8::internal::JSReceiver>::cast(v8::internal::Tagged<v8::internal::Object>)+0x21) [0x7f2abd840791]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Handle<v8::internal::JSObject> const v8::internal::Handle<v8::internal::JSObject>::cast<v8::internal::Object>(v8::internal::Handle<v8::internal::Object>)+0x37) [0x7f2abd83e0c7]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Handle<v8::internal::JSObject> v8::internal::Arguments<(v8::internal::ArgumentsType)0>::at<v8::internal::JSObject>(int) const+0x43) [0x7f2abe2ecba3]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x75b1f85) [0x7f2abebb1f85]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Runtime_LoadKeyedFromSuper(int, unsigned long*, v8::internal::Isolate*)+0x106) [0x7f2abebb1e46]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x5a83378) [0x7f2abd083378]
Trace/breakpoint trap

```
```
testcase_3.js (d8 debug)

#
# Fatal error in ../../src/ast/scopes.cc, line 984
# Debug check failed: cache != this implies cache->outer_scope()->deserialized_scope_uses_external_cache() || cache->GetHomeObjectScope() == this.
#
#
#
#FailureMessage Object: 0x7fff9e6bbef8
==== C stack trace ===============================

    v8_12.6.228.21/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7fe3833ecb0e]
    v8_12.6.228.21/v8/out/x64.debug/libv8_libplatform.so(+0x52b2d) [0x7fe383342b2d]
    v8_12.6.228.21/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x1ea) [0x7fe3833bd12a]
    v8_12.6.228.21/v8/out/x64.debug/libv8_libbase.so(+0x57afc) [0x7fe3833bcafc]
    v8_12.6.228.21/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x55) [0x7fe3833bd215]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Scope::LookupInScopeInfo(v8::internal::AstRawString const*, v8::internal::Scope*)+0x184) [0x7fe389763c94]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Variable* v8::internal::Scope::Lookup<(v8::internal::Scope::ScopeLookupMode)1>(v8::internal::VariableProxy*, v8::internal::Scope*, v8::internal::Scope*, v8::internal::Scope*, bool)+0x281) [0x7fe389773801]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Scope::ResolveVariable(v8::internal::VariableProxy*)+0x16e) [0x7fe38976cf9e]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Scope::ResolveVariablesRecursively(v8::internal::Scope*)+0x21a) [0x7fe38976b68a]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::DeclarationScope::AllocateVariables(v8::internal::ParseInfo*)+0xfb) [0x7fe389767f4b]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::DeclarationScope::Analyze(v8::internal::ParseInfo*)+0x33d) [0x7fe389767dad]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(void v8::internal::Parser::PostProcessParseResult<v8::internal::Isolate>(v8::internal::Isolate*, v8::internal::ParseInfo*, v8::internal::FunctionLiteral*)+0xcf) [0x7fe38a7b25cf]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Parser::ParseProgram(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Script>, v8::internal::ParseInfo*, v8::internal::MaybeHandle<v8::internal::ScopeInfo>)+0x4c2) [0x7fe38a7a2af2]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::parsing::ParseProgram(v8::internal::ParseInfo*, v8::internal::Handle<v8::internal::Script>, v8::internal::MaybeHandle<v8::internal::ScopeInfo>, v8::internal::Isolate*, v8::internal::parsing::ReportStatisticsMode)+0x246) [0x7fe38a7fe746]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x64b826c) [0x7fe3898b826c]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Compiler::GetFunctionFromEval(v8::internal::Handle<v8::internal::String>, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Handle<v8::internal::Context>, v8::internal::LanguageMode, v8::internal::ParseRestriction, int, int, int, v8::internal::ParsingWhileDebugging)+0x9d5) [0x7fe3898b9875]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x75c19d3) [0x7fe38a9c19d3]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x75bf64b) [0x7fe38a9bf64b]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Runtime_ResolvePossiblyDirectEval(int, unsigned long*, v8::internal::Isolate*)+0x106) [0x7fe38a9bf326]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x5a83378) [0x7fe388e83378]
Trace/breakpoint trap

```
```
testcase_4.js (d8 debug)

Bytecode mismatch found for function: anonymous testcase_4.js:171
Original bytecode:
Parameter count 1
Register count 5
Frame size 40
         0x45d000401e4 @    0 : 19 ff f9          Mov <context>, r0
  217 S> 0x45d000401e7 @    3 : 15 ff 02 01       LdaImmutableContextSlot <context>, [2], [1]
         0x45d000401eb @    7 : c9                Star1
         0x45d000401ec @    8 : 17 03             LdaImmutableCurrentContextSlot [3]
         0x45d000401ee @   10 : c8                Star2
         0x45d000401ef @   11 : 13 00             LdaConstant [0]
         0x45d000401f1 @   13 : c7                Star3
         0x45d000401f2 @   14 : 0c                LdaZero
         0x45d000401f3 @   15 : c6                Star4
         0x45d000401f4 @   16 : 68 36 00 f8 04    CallRuntime [StoreToSuper], r1-r4
         0x45d000401f9 @   21 : 8f 06             Jump [6] (0x45d000401ff @ 27)
         0x45d000401fb @   23 : 10                LdaTheHole
         0x45d000401fc @   24 : ac                SetPendingMessage
         0x45d000401fd @   25 : 0b f9             Ldar r0
         0x45d000401ff @   27 : 21 01 00          LdaGlobal [1], [0]
         0x45d00040202 @   30 : af                Return
Constant pool (size = 2)
0x45d000401ad: [TrustedFixedArray]
 - map: 0x25d200000595 <Map(TRUSTED_FIXED_ARRAY_TYPE)>
 - length: 2
           0: 0x25d20024da45 <String[4]: #test>
           1: 0x25d20000424d <String[5]: #Array>
Handler Table (size = 16)
   from   to       hdlr (prediction,   data)
  (   3,  21)  ->    23 (prediction=1, data=0)
Source Position Table (size = 13)
0x045d00040221 <Other heap object (TRUSTED_BYTE_ARRAY_TYPE)>

New bytecode:
Parameter count 1
Register count 5
Frame size 40
         0x45d00040288 @    0 : 19 ff f9          Mov <context>, r0
         0x45d0004028b @    3 : 15 ff 02 01       LdaImmutableContextSlot <context>, [2], [1]
         0x45d0004028f @    7 : c9                Star1
         0x45d00040290 @    8 : 15 ff 02 02       LdaImmutableContextSlot <context>, [2], [2]
         0x45d00040294 @   12 : c8                Star2
         0x45d00040295 @   13 : 13 00             LdaConstant [0]
         0x45d00040297 @   15 : c7                Star3
         0x45d00040298 @   16 : 0c                LdaZero
         0x45d00040299 @   17 : c6                Star4
         0x45d0004029a @   18 : 68 36 00 f8 04    CallRuntime [StoreToSuper], r1-r4
         0x45d0004029f @   23 : 8f 06             Jump [6] (0x45d000402a5 @ 29)
         0x45d000402a1 @   25 : 10                LdaTheHole
         0x45d000402a2 @   26 : ac                SetPendingMessage
         0x45d000402a3 @   27 : 0b f9             Ldar r0
         0x45d000402a5 @   29 : 21 01 00          LdaGlobal [1], [0]
         0x45d000402a8 @   32 : af                Return
Constant pool (size = 2)
0x45d00040251: [TrustedFixedArray]
 - map: 0x25d200000595 <Map(TRUSTED_FIXED_ARRAY_TYPE)>
 - length: 2
           0: 0x25d20024da45 <String[4]: #test>
           1: 0x25d20000424d <String[5]: #Array>
Handler Table (size = 16)
   from   to       hdlr (prediction,   data)
  (   3,  23)  ->    25 (prediction=1, data=0)
Source Position Table (size = 0)


#
# Fatal error in ../../src/interpreter/interpreter.cc, line 241
# Bytecode mismatch at offset 8

#
#
#
#FailureMessage Object: 0x7fff7b78f4c8
==== C stack trace ===============================

    v8_12.6.228.21/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7fdcdd628b0e]
    v8_12.6.228.21/v8/out/x64.debug/libv8_libplatform.so(+0x52b2d) [0x7fdcdd57eb2d]
    v8_12.6.228.21/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x1ea) [0x7fdcdd5f912a]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(void v8::internal::interpreter::InterpreterCompilationJob::CheckAndPrintBytecodeMismatch<v8::internal::Isolate>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Script>, v8::internal::Handle<v8::internal::BytecodeArray>)+0x38b) [0x7fdcd9bd7bfb]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::CompilationJob::Status v8::internal::interpreter::InterpreterCompilationJob::DoFinalizeJobImpl<v8::internal::Isolate>(v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Isolate*)+0x466) [0x7fdcd9bd5fd6]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::interpreter::InterpreterCompilationJob::FinalizeJobImpl(v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Isolate*)+0x127) [0x7fdcd9bd4687]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::UnoptimizedCompilationJob::FinalizeJob(v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Isolate*)+0x1fc) [0x7fdcd92ac4ac]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Compiler::CollectSourcePositions(v8::internal::Isolate*, v8::internal::Handle<v8::internal::SharedFunctionInfo>)+0x96b) [0x7fdcd92b494b]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::SharedFunctionInfo::EnsureSourcePositionsAvailable(v8::internal::Isolate*, v8::internal::Handle<v8::internal::SharedFunctionInfo>)+0xae) [0x7fdcda123dae]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x64b3646) [0x7fdcd92b3646]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*, v8::internal::CreateSourcePositions)+0x9cc) [0x7fdcd92b571c]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*)+0x40f) [0x7fdcd92b669f]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::JSFunction::CalculateExpectedNofProperties(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>)+0x1f3) [0x7fdcd9eef163]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::JSFunction::EnsureHasInitialMap(v8::internal::Handle<v8::internal::JSFunction>)+0x1cc) [0x7fdcd9eeea1c]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::JSFunction::GetDerivedMap(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::JSReceiver>)+0x28) [0x7fdcd9eef588]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::JSObject::New(v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::JSReceiver>, v8::internal::Handle<v8::internal::AllocationSite>, v8::internal::NewJSObjectType)+0x232) [0x7fdcd9f347d2]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x75f7d95) [0x7fdcda3f7d95]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(v8::internal::Runtime_NewObject(int, unsigned long*, v8::internal::Isolate*)+0x106) [0x7fdcda3f7bf6]
    v8_12.6.228.21/v8/out/x64.debug/libv8.so(+0x5a8357d) [0x7fdcd888357d]
Trace/breakpoint trap



```
```
testcase_5.js (d8 release)

TypeError: Cannot read properties of null (reading '__proto__')
TypeError: Cannot read properties of null (reading '__proto__')
TypeError: Cannot read properties of null (reading '__proto__')
TypeError: Cannot read properties of null (reading '__proto__')
TypeError: Cannot read properties of null (reading '__proto__')
TypeError: Cannot read properties of null (reading '__proto__')
TypeError: Cannot read properties of null (reading '__proto__')
TypeError: Cannot read properties of null (reading '__proto__')
TypeError: Cannot read properties of null (reading '__proto__')
------------------------------Garbage Collector-----------------------------
[object Object]

```
```
testcase_6.js (d8 release)

------------------------------Garbage Collector-----------------------------
super.x - value inside class definition:  800
super.x - value outside class definition: 900


```

While analyzing the testcase, we also hit this dchecks inside Maglev:

```
#
# Fatal error in ../../src/maglev/maglev-graph-builder.h, line 700
# Debug check failed: source_position_iterator_.code_offset() > offset (1005 vs. 1007).
#
#
#
#FailureMessage Object: 0x7f849f7fc2a8
==== C stack trace ===============================

TypeError: Cannot read properties of null (reading '__proto__')
    v8_12.3.219.16/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7f84db35b41e]
    v8_12.3.219.16/v8/out/x64.debug/libv8_libplatform.so(+0x5004d) [0x7f84d17dd04d]
    v8_12.3.219.16/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x1ea) [0x7f84db32b97a]
    v8_12.3.219.16/v8/out/x64.debug/libv8_libbase.so(+0x5634c) [0x7f84db32b34c]
    v8_12.3.219.16/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x55) [0x7f84db32ba65]
    v8_12.3.219.16/v8/out/x64.debug/libv8.so(v8::internal::maglev::MaglevGraphBuilder::UpdateSourceAndBytecodePosition(int)+0x100) [0x7f84d87fb270]
    v8_12.3.219.16/v8/out/x64.debug/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode()+0xf1) [0x7f84d87fb3a1]
    v8_12.3.219.16/v8/out/x64.debug/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildBody()+0x12b) [0x7f84d87f36bb]
    v8_12.3.219.16/v8/out/x64.debug/libv8.so(v8::internal::maglev::MaglevGraphBuilder::Build()+0x36c) [0x7f84d87efacc]
    v8_12.3.219.16/v8/out/x64.debug/libv8.so(v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*)+0x59b) [0x7f84d87ee22b]
    v8_12.3.219.16/v8/out/x64.debug/libv8.so(v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x69) [0x7f84d88e8f49]
    v8_12.3.219.16/v8/out/x64.debug/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x159) [0x7f84d74d1a59]
    v8_12.3.219.16/v8/out/x64.debug/libv8.so(v8::internal::maglev::MaglevConcurrentDispatcher::JobTask::Run(v8::JobDelegate*)+0x469) [0x7f84d88ec219]
    v8_12.3.219.16/v8/out/x64.debug/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xcc) [0x7f84d17daf9c]
    v8_12.3.219.16/v8/out/x64.debug/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xaf) [0x7f84d17e3ccf]
    v8_12.3.219.16/v8/out/x64.debug/libv8_libbase.so(v8::base::Thread::NotifyStartedAndRun()+0x36) [0x7f84db35a9f6]
    v8_12.3.219.16/v8/out/x64.debug/libv8_libbase.so(+0x847e6) [0x7f84db3597e6]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7f84d0e94ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126850) [0x7f84d0f26850]
Trace/breakpoint trap

```
### Commit that introduced the bug:

`8f477f936c9b9e6b4c9f35a8ccc5e65bd4cb7f4e`

```
[parser] Fix home object proxy to work off-thread

Because the home object has special scope lookup rules due to class
heritage position, VariableProxies of the home object are currently
directly created on the correct scope during parsing. However, during
off-thread parsing the main thread is parked, and the correct scope
may try to dereference a main-thread Handle.

This CL moves the logic into ResolveVariable instead, which happens
during postprocessing, with the main thread unparked.

```
### Root cause:

Example:

```

/**

Compilation 1)

Frame size 8
  136 S> 0x17f6000401d4 @    0 : 15 ff 02 01       LdaImmutableContextSlot <context>, [2], [1]
         0x17f6000401d8 @    4 : ca                Star0
         0x17f6000401d9 @    5 : 17 03             LdaImmutableCurrentContextSlot [3]
         0x17f6000401db @    7 : 30 f9 00 00       GetNamedPropertyFromSuper r0, [0], [0]
         0x17f6000401df @   11 : 21 01 02          LdaGlobal [1], [2]
         0x17f6000401e2 @   14 : af                Return
Constant pool (size = 2)
0x17f60004019d: [TrustedFixedArray]
 - map: 0x2cbf00000595 <Map(TRUSTED_FIXED_ARRAY_TYPE)>
 - length: 2
           0: 0x2cbf0024da45 <String[4]: #test>
           1: 0x2cbf0000424d <String[5]: #Array>
Handler Table (size = 0)
Source Position Table (size = 12)
0x17f600040201 <Other heap object (TRUSTED_BYTE_ARRAY_TYPE)>

Compilation 2)

New bytecode:
Parameter count 1
Register count 1
Frame size 8
         0x17f60004024c @    0 : 15 ff 02 01       LdaImmutableContextSlot <context>, [2], [1]
         0x17f600040250 @    4 : ca                Star0
         0x17f600040251 @    5 : 15 ff 02 02       LdaImmutableContextSlot <context>, [2], [2]
         0x17f600040255 @    9 : 30 f9 00 00       GetNamedPropertyFromSuper r0, [0], [0]
         0x17f600040259 @   13 : 21 01 02          LdaGlobal [1], [2]
         0x17f60004025c @   16 : af                Return

**/

class var_1 {

    constructor() {

        new class var_2 {

            [new class extends (() => {
                
                super.test;

                return Array;

            })() {

            }()] = super.__proto__;

        };

    }
}

new var_1;

```

The `.home_object (super) Variable` for the access to `super` property is assigned to a wrong scope. On the first compilation, the associated scope is that of its own class. (class `var_1` on the example). Then, `LdaImmutableCurrentContextSlot [3]` is generated which access to the wrong Context.

At the property access moment, the class is under construction and the variable slots are initialized with default values. The slot that should contain the `.home_object` is by default "undefined", so it triggers a JavaScript grammar error when accessing to any property of `super`, as it is "undefined". (see testcase\_1.js disabling DChecks)

We can trigger another compilation by calling the Garbage Collector and flushing the code (See testcase\_4.js), which will use `Lazy Compiation (Builtins_CompileLazy)` this time, ending on a correct bytecode. This time, the scope of the `.home_object` variable is correct, but this would produce a `Bytecode Mismatch` between the two compilations.

As can be observed on testcase\_5.js and testcase\_6.js, we can get the two compilations in the same testcase, obtaining different values for the same object.

VERSION
Chrome Version: 126.0.6478.126 Release
Operating System: Tested on v8 Linux

REPRODUCTION CASE

- testcase\_1.js
- testcase\_2.js
- testcase\_3.js
- testcase\_4.js
- testcase\_5.js
- testcase\_6.js

PATCH ANALYSIS

For a fast patch, `8f477f936c9b9e6b4c9f35a8ccc5e65bd4cb7f4e` must be reversed.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: DCheck on V8

CREDIT INFORMATION
Reporter credit: Tashita Software Security

## Attachments

- [testcase_1.js](attachments/testcase_1.js) (text/javascript, 207 B)
- [testcase_2.js](attachments/testcase_2.js) (text/javascript, 131 B)
- [testcase_3.js](attachments/testcase_3.js) (text/javascript, 120 B)
- [testcase_4.js](attachments/testcase_4.js) (text/javascript, 346 B)
- [testcase_5.js](attachments/testcase_5.js) (text/javascript, 900 B)
- [testcase_6.js](attachments/testcase_6.js) (text/javascript, 1.1 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-07-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6301262158954496.

### cl...@appspot.gserviceaccount.com (2024-07-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4915002542587904.

### cl...@appspot.gserviceaccount.com (2024-07-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6212966489718784.

### cl...@appspot.gserviceaccount.com (2024-07-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6260376721096704.

### cl...@appspot.gserviceaccount.com (2024-07-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5078158451605504.

### cl...@appspot.gserviceaccount.com (2024-07-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6224228665720832.

### am...@chromium.org (2024-07-15)

Thank you for the report. In the future, please report each potential security issue as a in a separate report. One of the testcases look similar to that of a recently resolved issue. Since only reproducing this will confirm, I've gone ahead and am keeping this in one report for now. I've uploaded each testcase to clusterfuzz (d8\_dbg) in the meantime.
I did notice that no specific command line arguments were included for any testcase, so I've had to go ahead let clusterfuzz attempt to reproduce based on default d8 args.

If there are specific command line arguments needed here, please include them. I do not want to manually attempt a reproduction until that is confirmed.

### am...@chromium.org (2024-07-15)

Going to tentatively assign and set some of the security flags in advance. Will update this issue as more information as it becomes available.

### am...@chromium.org (2024-07-15)

so far testcase 4 and testcase 5 result in duplicate results to each other.

### ta...@gmail.com (2024-07-15)

Hello, thank you for the response!

All testcases point to the same root cause, they are all variants of the same bug. The testcase\_4.js needs the flags `--stress-lazy-source-positions` and `--no-enable_slow_asserts` to reproduce the bytecode mismatch.

### pe...@google.com (2024-07-15)

Thank you for providing more feedback. Adding the requester to the CC list.

### am...@chromium.org (2024-07-15)

Thanks for the quick response! Apologies for missing this was the same root cause. In that case, thank you for keeping this together in one report with different POCs -- very thorough.
Those flags are part of the clusterfuzz default for d8 dbg, so it looks like they are all reproducing.

### 24...@project.gserviceaccount.com (2024-07-15)

Detailed Report: https://clusterfuzz.com/testcase?key=6301262158954496

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  scope->outer_scope()->is_class_scope() in scopes.cc
  v8::internal::Scope::GetHomeObjectScope
  v8::internal::Scope::ResolveVariable
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=92721:92722

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6301262158954496

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### am...@chromium.org (2024-07-15)

Since clusterfuzz can reproduce this, I'm not going to attempt to manually repro. It's going to take some time before CF comes up with regression info. In the meantime, I'm updating owner and cc for visibility to the correct folks.

Setting FoundIn-126 as since 126 is current Stable and this looks to go back at least this far, if not a bit longer. (updated to add: haha, looks like Clusterfuzz won the race here, and this does in fact go back to 126)

### 24...@project.gserviceaccount.com (2024-07-15)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-07-15)

Detailed Report: https://clusterfuzz.com/testcase?key=4915002542587904

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  Handle<To> v8::internal::Cast(Handle<From>, const v8::SourceLocation &) [To = v8
  v8::internal::Handle<v8::internal::JSObject> v8::internal::Cast<v8::internal::JS
  v8::internal::__RT_impl_Runtime_LoadKeyedFromSuper
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=92721:92722

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4915002542587904

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2024-07-15)

Detailed Report: https://clusterfuzz.com/testcase?key=6212966489718784

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  cache != this implies cache->outer_scope()->deserialized_scope_uses_external_cac
  v8::internal::Scope::LookupInScopeInfo
  v8::internal::Variable* v8::internal::Scope::Lookup<
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=92721:92722

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6212966489718784

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2024-07-15)

Detailed Report: https://clusterfuzz.com/testcase?key=6224228665720832

Fuzzer: None
Job Type: linux_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  (location_) != nullptr in handles.cc
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=95025:95026

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6224228665720832

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2024-07-15)

Detailed Report: https://clusterfuzz.com/testcase?key=6260376721096704

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  (location_) != nullptr in handles.cc
  v8::internal::HandleBase::IsDereferenceAllowed
  void v8::internal::DeclarationScope::AllocateScopeInfos<v8::internal::Isolate>
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=95025:95026

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6260376721096704

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ma...@chromium.org (2024-07-16)

Having a quick look since syg@ is in meetings all week.

I think it's OK to have all these repros under the same bug report. Based on the description, there's one root cause bug, and then different stuff happens based on what else the repro case does (e.g., if it forces a recompilation).

### ma...@chromium.org (2024-07-16)

I didn't get far, unfortunately. I am very confused.

Looking at this repro:

class C {
  constructor(){
    new class extends ((var_1) => {
      eval("super.__proto__;");
    })() {
    }
  }
}

print("Now running");
new C();

During the outer scope compilation, we have these scopes:

Inner function scope:
function constructor () { // (0x563316175c90) (23, 115)
  // strict mode scope
  // inner scope calls 'eval'
  // BaseConstructor
  // 2 heap slots

  class { // (0x563316177ac0) (35, 111)
    // strict mode scope
    // inner scope calls 'eval'
    // 2 heap slots

    function () { // (0x563316177e40) (35, 35)
      // strict mode scope
      // DefaultBaseConstructor
      // 2 heap slots
    }

    arrow () { // (0x563316177c38) (50, 100)
      // strict mode scope
      // scope skips outer class for #-names
      // inner scope calls 'eval'
      // ArrowFunction
      // 2 heap slots
      // local vars:
      VAR var_1;  // (0x563316177df8) never assigned
    }
  }
}
Global scope:
global { // (0x563316175870) (0, 149)
  // inner scope calls 'eval'
  // will be compiled
  // NormalFunction
  // 1 stack slots
  // 4 heap slots
  // temporary vars:
  TEMPORARY .result;  // (0x563316176148) local[0]
  // local vars:
  LET C;  // (0x563316175fb0) context[3]
  // dynamic vars:
  DYNAMIC_GLOBAL print;  // (0x563316176228) never assigned

  class C { // (0x563316175a60) (0, 117)
    // strict mode scope
    // inner scope calls 'eval'
    // 5 heap slots
    // local vars:
    CONST .home_object;  // (0x563316175e80) context[2], forced context allocation, never assigned
    CONST .static_home_object;  // (0x563316175eb0) context[3], forced context allocation, never assigned
    CONST C;  // (0x563316175ee0) context[4]
    // class var, used, index not saved:
    CONST C;  // (0x563316175ee0) context[4]

    function constructor () { // (0x563316175c90) (23, 115)
      // strict mode scope
      // inner scope calls 'eval'
      // lazily parsed
      // BaseConstructor
      // 2 heap slots
    }
  }
}

During run time, after we've deconstructed the scope chain and call GetHomeObjectScope, we have these:

global { // (0x563316173860) (-1, -1)
  // NormalFunction
  // 3 heap slots

  class { // (0x563316173d90) (0, 117)
    // strict mode scope
    // 2 heap slots

    function () { // (0x563316173bf0) (-1, -1)
      // strict mode scope
      // BaseConstructor
      // 2 heap slots

      arrow () { // (0x563316173a50) (-1, -1)
        // strict mode scope
        // scope skips outer class for #-names
        // ArrowFunction
        // 2 heap slots

        eval { // (0x563316173f20) (0, 16)
          // strict mode scope
          // will be compiled
          // NormalFunction
          // 2 heap slots
          // temporary vars:
          TEMPORARY .result;  // (0x5633161741a0) 
        }
      }
    }
  }
}

Now we're trying to GetHomeObjectScope with the eval scope, then we walk up to the arrow scope. At that point, it has skip_outer_class_for_private_names, but its outer scope is not a class scope, so the DCHECK fails.

But why is the arrow function scope no longer inside a class scope?

### ma...@chromium.org (2024-07-16)

Aha, clusterfuzz is blaming https://chromium-review.googlesource.com/c/v8/v8/+/5703778 which sounds legit.

I will stay away from this! :)


### pe...@google.com (2024-07-16)

Setting milestone because of s0/s1 severity.

### ap...@google.com (2024-07-16)

Project: v8/v8
Branch: main

commit f0a3073d941249ba790a8a4bc891e82ec83e8986
Author: Toon Verwaest <verwaest@chromium.org>
Date:   Tue Jul 16 17:32:07 2024

    [parser] Make sure we have an SFI on the literal
    
    (Doesn't actually fix the bug I'm pointing at, just a benign verification issue)
    
    Bug: 352690885
    Change-Id: I2ccc3d4497338d940407999bb116f7e379e11084
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5713176
    Commit-Queue: Toon Verwaest <verwaest@chromium.org>
    Commit-Queue: Marja Hölttä <marja@chromium.org>
    Auto-Submit: Toon Verwaest <verwaest@chromium.org>
    Reviewed-by: Marja Hölttä <marja@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95063}

M       src/interpreter/interpreter.cc

https://chromium-review.googlesource.com/5713176


### ap...@google.com (2024-07-29)

Project: v8/v8
Branch: main

commit af7f8f06b604f007b7bac75365266246d122e28a
Author: Shu-yu Guo <syg@chromium.org>
Date:   Mon Jul 29 09:00:54 2024

    [parser] Fix HomeObjectScope to start at the receiver scope
    
    Bug: 352690885
    Change-Id: I6c9bb1d48468853908a48edccc00a70ba0987164
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5715410
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Shu-yu Guo <syg@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95362}

M       src/ast/scopes.cc

https://chromium-review.googlesource.com/5715410


### 24...@project.gserviceaccount.com (2024-07-30)

ClusterFuzz testcase 5078158451605504 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=95062:95063

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-07-30)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2024-08-01)

<https://crrev.com/c/5715410> approved for merges
please merge to 12.8, 12.7, and 12.7 at soonest (by 10am Pacific Time, Friday 2 August) so this fix can be included in the next respective updates

### go...@google.com (2024-08-02)

Please merge to branch 12.8, 12.7, and 12.6 ASAP.

### pe...@google.com (2024-08-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-08-05)

Project: v8/v8
Branch: refs/branch-heads/12.7

commit 275eeabbe7759bc8bd79ce9613b78bb3f283b7df
Author: Shu-yu Guo <syg@chromium.org>
Date:   Mon Jul 29 09:00:54 2024

    Merged: [parser] Fix HomeObjectScope to start at the receiver scope
    
    Bug: 352690885
    (cherry picked from commit af7f8f06b604f007b7bac75365266246d122e28a)
    
    Change-Id: I8f7d2fb62a39117025be218fcc17dc74614f4e4a
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5762852
    Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
    Reviewed-by: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.7@{#34}
    Cr-Branched-From: 35cc908918d3f8083955ed8328506f964e17ae40-refs/heads/12.7.224@{#1}
    Cr-Branched-From: 6d60e6734b32211215c8410db6fe2b84b13abe0e-refs/heads/main@{#94324}

M       src/ast/scopes.cc

https://chromium-review.googlesource.com/5762852


### ap...@google.com (2024-08-05)

Project: v8/v8
Branch: refs/branch-heads/12.6

commit 7acd351777d9135f4e631c04b6f28a10e57952b9
Author: Shu-yu Guo <syg@chromium.org>
Date:   Mon Jul 29 09:00:54 2024

    Merged: [parser] Fix HomeObjectScope to start at the receiver scope
    
    Bug: 352690885
    (cherry picked from commit af7f8f06b604f007b7bac75365266246d122e28a)
    
    Change-Id: Icabc232c03142d6f4137f6ae5fb8359c7cf1b9ee
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5762851
    Reviewed-by: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
    Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.6@{#56}
    Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2}
    Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

M       src/ast/scopes.cc

https://chromium-review.googlesource.com/5762851


### ap...@google.com (2024-08-05)

Project: v8/v8
Branch: refs/branch-heads/12.8

commit de5e0165c23f3c0d96240854e9457952641ee957
Author: Shu-yu Guo <syg@chromium.org>
Date:   Mon Jul 29 09:00:54 2024

    Merged: [parser] Fix HomeObjectScope to start at the receiver scope
    
    Bug: 352690885
    (cherry picked from commit af7f8f06b604f007b7bac75365266246d122e28a)
    
    Change-Id: Ic95ed304891aa5158d072038a0198d6bbb718441
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5762853
    Reviewed-by: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
    Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.8@{#12}
    Cr-Branched-From: 70cbb397b153166027e34c75adf8e7993858222e-refs/heads/12.8.374@{#1}
    Cr-Branched-From: 451b63ed4251c2b21c56144d8428f8be3331539b-refs/heads/main@{#95151}

M       src/ast/scopes.cc

https://chromium-review.googlesource.com/5762853


### go...@google.com (2024-08-05)

Looks like this is merged to M126, M127 & M128.

Please remove Merge-Approved fields if nothing else is pending. 

### sp...@google.com (2024-08-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for baseline report of potential memory corruption in a sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-14)

Congratulations Tashita Software Security team! Thank you for your efforts and reporting this issue to us!

### ta...@gmail.com (2024-08-16)

Thanks to all of you for the effort!

### ap...@google.com (2024-08-16)

Project: v8/v8
Branch: main

commit 087bd753c6324319ca57e28c652058a8f456d579
Author: Shu-yu Guo <syg@chromium.org>
Date:   Wed Aug 14 15:21:21 2024

    [parser] Add regression tests
    
    Bug: 352690885
    Change-Id: I890c2cc2931245404c33a08effaa42d8977ad20c
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5787339
    Auto-Submit: Shu-yu Guo <syg@chromium.org>
    Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95670}

A       test/mjsunit/regress/regress-352690885-1.js
A       test/mjsunit/regress/regress-352690885-2.js
A       test/mjsunit/regress/regress-352690885-3.js
A       test/mjsunit/regress/regress-352690885-4.js
A       test/mjsunit/regress/regress-352690885-5.js
A       test/mjsunit/regress/regress-352690885-6.js

https://chromium-review.googlesource.com/5787339


### pe...@google.com (2024-11-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/352690885)*
