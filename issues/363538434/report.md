# DCHECK on V8 Parser while parsing Class Static Functions

| Field | Value |
|-------|-------|
| **Issue ID** | [363538434](https://issues.chromium.org/issues/363538434) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Parser |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ta...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2024-09-01 |
| **Bounty** | $8,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

## VULNERABILITY DETAILS

DCHECK on V8 Parser while parsing Class Static Functions.

### Stack Trace

```
#
# Fatal error in ../../src/parsing/parser.cc, line 1120
# Debug check failed: class_info.static_elements_function_id == initializer_id (3 vs. 2).
#
#
#
#FailureMessage Object: 0x7fff9480e098
==== C stack trace ===============================

    ./v8_12.8.374.24/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7f657912917e]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8_libplatform.so(+0x5757d) [0x7f657908457d]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x205) [0x7f65790fc675]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8_libbase.so(+0x5601c) [0x7f65790fc01c]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x4d) [0x7f65790fc74d]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8.so(v8::internal::Parser::ParseClassForMemberInitialization(v8::internal::FunctionKind, int, int, int, v8::internal::AstRawString const*)+0x41a) [0x7f6575b8dffa]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8.so(v8::internal::Parser::ParseFunction(v8::internal::Isolate*, v8::internal::ParseInfo*, v8::internal::Handle<v8::internal::SharedFunctionInfo>)+0x6a2) [0x7f6575b8d802]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8.so(v8::internal::parsing::ParseFunction(v8::internal::ParseInfo*, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Isolate*, v8::internal::parsing::ReportStatisticsMode)+0x362) [0x7f6575be22f2]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8.so(v8::internal::parsing::ParseAny(v8::internal::ParseInfo*, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Isolate*, v8::internal::parsing::ReportStatisticsMode)+0x1dc) [0x7f6575be254c]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8.so(+0x6e71a0e) [0x7f6575071a0e]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8.so(v8::internal::ErrorUtils::NewCalledNonCallableError(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>)+0x7b) [0x7f657507291b]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8.so(+0x7bbadd2) [0x7f6575dbadd2]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8.so(v8::internal::Runtime_ThrowCalledNonCallable(int, unsigned long*, v8::internal::Isolate*)+0xf8) [0x7f6575dbaca8]
    ./v8_12.8.374.24/v8/out/x64.debug/libv8.so(+0x608133d) [0x7f657428133d]

```
### Reproduction Steps

1. Build 12.8.374.24 with Debug mode by adding `is_debug = true` into args.gn.
2. Execute the testcase attached: `./d8 reduced_dcheck_class_static_function.js`
3. It should print the DCheck mentioned on the Stack Trace.

### Root Cause

#### Initial considerations:

- The misaligment between `class_info.static_elements_function_id` and `initializer_id` triggers the DCheck which happens inside `ParseClassForMemberInitialization` function: `DCHECK_EQ(class_info.static_elements_function_id, initializer_id);`
- `ParseClassForMemberInitialization` receives the `initializer_id` by parameter.
- `class_info.static_elements_function_id` gets the value of `function_literal_id_` which is a member of `parser-base.h`
- `function_literal_id_` can be manipulated by the functions: `GetNextFunctionLiteralId`, `SkipFunctionLiterals` and `ResetFunctionLiteralId`.

#### The problem:

```
FunctionLiteral* Parser::ParseClassForMemberInitialization(
    FunctionKind initalizer_kind, int initializer_pos, int initializer_id,
    int initializer_end_pos, const AstRawString* class_name) {
  
  ...
  ResetFunctionLiteralId(); //[1]
  SkipFunctionLiterals(initializer_id - 1); //[2]
  ...

    ParseClassLiteralBody(class_info, class_name, class_token_pos, Token::kEos); //[3]

    if (initalizer_kind == FunctionKind::kClassMembersInitializerFunction) {
     ...
    } else {
      DCHECK_EQ(class_info.static_elements_function_id, initializer_id); //[4]
      initializer = CreateStaticElementsInitializer(class_name, &class_info);
    }
    ...
  }

  ...
  DCHECK_EQ(initializer->function_literal_id(), initializer_id); //[5]
  ...
}

```

[1] and [2] are used to set an initial value to `function_literal_id_`. As can be observed, it sets the value of `initializer_id - 1`, assuming that `function_literal_id_` will be increased only once. The problem is that `ParseClassLiteralBody` ([3]) increases multiple times the `function_literal_id_` variable causing the misaligment.

#### Multiple Increases of `function_literal_id_`:

```
template <typename Impl>
typename ParserBase<Impl>::ClassLiteralPropertyT
ParserBase<Impl>::ParseClassPropertyDefinition(ClassInfo* class_info,
                                               ParsePropertyInfo* prop_info,
                                               bool has_extends) {
  ...
  if (name_token == Token::kStatic) {
    ...
    if (peek() == Token::kLeftParen) {
      ...
    } else if (peek() == Token::kAssign || peek() == Token::kSemicolon ||
               peek() == Token::kRightBrace) {
      ...
    } else {
      prop_info->is_static = true;
      name_expression = ParseProperty(prop_info); //[6]
    }
  } else {
    ...
  }

  switch (prop_info->kind) {
    case ParsePropertyKind::kAssign:
    case ParsePropertyKind::kClassField:
    case ParsePropertyKind::kShorthandOrClassField:
    case ParsePropertyKind::kNotSet: { 

      ...

      ExpressionT initializer = ParseMemberInitializer(
          class_info, property_beg_pos, prop_info->is_static); //[7]
      ...

      //[8]

```

[6] `ParseProperty` increases the `function_literal_id_` via `ParseFunctionLiteral` function. Full backtrace:

```
#0  0x00004f0e3d4d174b in v8::internal::ParserBase<v8::internal::Parser>::GetNextFunctionLiteralId (this=0x7fff7da5ec50) at ../../src/parsing/parser-base.h:296
#1  0x00004f0e3d4c39b0 in v8::internal::Parser::ParseFunctionLiteral (this=0x7fff7da5ec50, function_name=0x559dcbee9108, function_name_location=..., function_name_validity=v8::internal::kFunctionNameValidityUnknown, kind=v8::internal::FunctionKind::kNormalFunction, 
    function_token_pos=0x18, function_syntax_kind=v8::internal::FunctionSyntaxKind::kAnonymousExpression, language_mode=v8::internal::LanguageMode::kStrict, arguments_for_wrapped_function=0x0) at ../../src/parsing/parser.cc:2733
#2  0x00004f0e3d4f6a83 in v8::internal::ParserBase<v8::internal::Parser>::ParseFunctionExpression (this=0x7fff7da5ec50) at ../../src/parsing/parser-base.h:3960
#3  0x00004f0e3d4f54cd in v8::internal::ParserBase<v8::internal::Parser>::ParsePrimaryExpression (this=0x7fff7da5ec50) at ../../src/parsing/parser-base.h:2121
#4  0x00004f0e3d4f45a7 in v8::internal::ParserBase<v8::internal::Parser>::ParseMemberExpression (this=0x7fff7da5ec50) at ../../src/parsing/parser-base.h:3987
#5  0x00004f0e3d4f4447 in v8::internal::ParserBase<v8::internal::Parser>::ParseLeftHandSideExpression (this=0x7fff7da5ec50) at ../../src/parsing/parser-base.h:3709
#6  0x00004f0e3d4f32ba in v8::internal::ParserBase<v8::internal::Parser>::ParsePostfixExpression (this=0x7fff7da5ec50) at ../../src/parsing/parser-base.h:3676
#7  0x00004f0e3d4f2bde in v8::internal::ParserBase<v8::internal::Parser>::ParseUnaryExpression (this=0x7fff7da5ec50) at ../../src/parsing/parser-base.h:3666
#8  0x00004f0e3d4f24ac in v8::internal::ParserBase<v8::internal::Parser>::ParseBinaryExpression (this=0x7fff7da5ec50, prec=0x6) at ../../src/parsing/parser-base.h:3548
#9  0x00004f0e3d4f1dac in v8::internal::ParserBase<v8::internal::Parser>::ParseLogicalExpression (this=0x7fff7da5ec50) at ../../src/parsing/parser-base.h:3318
#10 0x00004f0e3d4f07fa in v8::internal::ParserBase<v8::internal::Parser>::ParseConditionalExpression (this=0x7fff7da5ec50) at ../../src/parsing/parser-base.h:3303
#11 0x00004f0e3d4f0316 in v8::internal::ParserBase<v8::internal::Parser>::ParseAssignmentExpressionCoverGrammar (this=0x7fff7da5ec50) at ../../src/parsing/parser-base.h:3090
#12 0x00004f0e3d4d77e5 in v8::internal::ParserBase<v8::internal::Parser>::ParseAssignmentExpression (this=0x7fff7da5ec50) at ../../src/parsing/parser-base.h:2229
#13 0x00004f0e3d5002e4 in v8::internal::ParserBase<v8::internal::Parser>::ParseProperty (this=0x7fff7da5ec50, prop_info=0x7fff7da5e700) at ../../src/parsing/parser-base.h:2486

```

[7] `ParseMemberInitializer` increases the `function_literal_id_` via `EnsureStaticElementsScope`. Full backtrace:

```
#0  0x00004f0e3d4d174b in v8::internal::ParserBase<v8::internal::Parser>::GetNextFunctionLiteralId (this=0x7fff7da5ec50) at ../../src/parsing/parser-base.h:296
#1  0x00004f0e3d5036f8 in v8::internal::ParserBase<v8::internal::Parser>::ClassInfo::EnsureStaticElementsScope (this=0x7fff7da5e7e0, parser=0x7fff7da5ec50, beg_pos=0x10) at ../../src/parsing/parser-base.h:623
#2  0x00004f0e3d504576 in v8::internal::ParserBase<v8::internal::Parser>::ParseMemberInitializer (this=0x7fff7da5ec50, class_info=0x7fff7da5e7e0, beg_pos=0x10, is_static=0x1) at ../../src/parsing/parser-base.h:2696

```

[8] At this moment, the mismatch is already set. The function returns until the DCheck is hit.

### Bisect: Introduced Commit

Commit: cca606336c6753a2ddcd425019c1be11f9ba6216

Title: [parser] Only reparse the relevant segments for class initializers

Review: <https://chromium-review.googlesource.com/c/v8/v8/+/5676330>

### Bisect: Introduced Major Chrome

Chrome Stable: 128.0.6613.84

## VERSION

Chrome Version: [128.0.6613.113] + [stable]
Operating System: [All]

## REPRODUCTION CASE

Attached: `reduced_dcheck_class_static_function.js`

## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: [Browser]

## CREDIT INFORMATION

Reporter credit: Tashita Software Security

## Attachments

- [reduced_dcheck_class_static_function.js](attachments/reduced_dcheck_class_static_function.js) (text/javascript, 61 B)
- [static_unreachable.js](attachments/static_unreachable.js) (text/javascript, 39 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-09-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5109830918275072.

### 24...@project.gserviceaccount.com (2024-09-02)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-09-02)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/cca606336c6753a2ddcd425019c1be11f9ba6216 ([parser] Only reparse the relevant segments for class initializers

This changes the source positions for static elements and instance
members initializer functions to only cover exactly the region of a
class they need. ParseClassLiteralBody is changed to only parse body
statements, not everything starting from { to }. And class literal
rewriting is moved outside to where the class literal is parsed, so
that initializer functions can only do the bits that they need.

The entire outer scope chain is always deserialized, and is used as
the scope for parsing. Private variables and variables for computed
field names are allowed to be created on the scope despite already
being resolved. FinalizeReparsedClassScope is repurposed to properly
initialize those variables after we finished parsing the class body.

Change-Id: I87d10bc633dee40b99437af87d600fe06d711afc
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5676330
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Auto-Submit: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#94853}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2024-09-02)

Detailed Report: https://clusterfuzz.com/testcase?key=5109830918275072

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  class_info.static_elements_function_id == initializer_id in parser.cc
  v8::internal::Parser::ParseClassForMemberInitialization
  v8::internal::Parser::ParseFunction
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=94852:94853

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5109830918275072

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ad...@google.com (2024-09-02)

cffsmith@ as current V8 sheriff, please could you update the severity/bug class to whatever are the consequences of going past this DCHECK in production. Thanks!

### pe...@google.com (2024-09-02)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-09-02)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ja...@chromium.org (2024-09-10)

[secondary security shepherd]

Hi ishell@, following up on [comment#6](https://issues.chromium.org/issues/363538434#comment6), could you review the severity/bug class consequences of passing the DCHECK in production?

Thank you

### ap...@google.com (2024-09-11)

Project: v8/v8
Branch: main

commit 8068f489ec2c7e9de15e179c8c25b45224f7f96f
Author: Toon Verwaest <verwaest@chromium.org>
Date:   Wed Sep 11 15:29:39 2024

    [parser] Fix initializer ids w/ computed property names
    
    Move the initializer id before the computed property name ids.
    
    Bug: 363538434
    Change-Id: Ife1abf50a9348242f5e5f6c69c2911106f5a67dd
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5850479
    Commit-Queue: Toon Verwaest <verwaest@chromium.org>
    Auto-Submit: Toon Verwaest <verwaest@chromium.org>
    Reviewed-by: Igor Sheludko <ishell@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#96059}

M       src/parsing/parser-base.h
M       src/parsing/parser.cc
M       src/parsing/parser.h
M       src/parsing/preparser.h
A       test/mjsunit/regress/regress-363538434.js

https://chromium-review.googlesource.com/5850479


### ta...@gmail.com (2024-09-12)

Hi There,

We have detected a "unreachable code" on the commit 8068f489ec2c7e9de15e179c8c25b45224f7f96f, which addresses the bug fixed yesterday, at [comment #10](https://issues.chromium.org/issues/363538434#comment10).

We’re confident that you’ll identify the problem quickly, or perhaps you’ve already encountered it, but as trigger for this issue is quite unusual, we have attached the sample.

Notice that this new issue needs to contain an JavaScript object method which misses the closing curly brace `}`.

Thanks!

```
#
# Fatal error in ../../src/ast/ast-traversal-visitor.h, line 58
# unreachable code
#
#
#
#FailureMessage Object: 0x7ffe4ccc33f0
==== C stack trace ===============================

    v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f6163f4ff73]
    v8/out/x64.debug/libv8_libplatform.so(+0x1994d) [0x7f6163ef894d]
    v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7f6163f31554]
    v8/out/x64.debug/libv8.so(+0x28ac5b3) [0x7f6160cac5b3]
    v8/out/x64.debug/libv8.so(v8::internal::AstFunctionLiteralIdReindexer::Reindex(v8::internal::Expression*)+0x58) [0x7f6160cab248]
    v8/out/x64.debug/libv8.so(v8::internal::ParserBase<v8::internal::Parser>::ParseClassPropertyDefinition(v8::internal::ParserBase<v8::internal::Parser>::ClassInfo*, v8::internal::ParserBase<v8::internal::Parser>::ParsePropertyInfo*, bool)+0x3b6) [0x7f6161c58096]
    v8/out/x64.debug/libv8.so(v8::internal::ParserBase<v8::internal::Parser>::ParseClassLiteralBody(v8::internal::ParserBase<v8::internal::Parser>::ClassInfo&, v8::internal::AstRawString const*, int, v8::internal::Token::Value)+0x1f8) [0x7f6161c2fca8]
    v8/out/x64.debug/libv8.so(v8::internal::ParserBase<v8::internal::Parser>::ParseClassLiteral(v8::internal::Scope*, v8::internal::AstRawString const*, v8::internal::Scanner::Location, bool, int)+0x3ca) [0x7f6161c5212a]
    v8/out/x64.debug/libv8.so(v8::internal::ParserBase<v8::internal::Parser>::ParseMemberWithPresentNewPrefixesExpression()+0x133) [0x7f6161c4e533]
    v8/out/x64.debug/libv8.so(v8::internal::ParserBase<v8::internal::Parser>::ParseBinaryExpression(int)+0x112) [0x7f6161c4aa82]
    v8/out/x64.debug/libv8.so(v8::internal::ParserBase<v8::internal::Parser>::ParseAssignmentExpressionCoverGrammar()+0x97) [0x7f6161c48bf7]
    v8/out/x64.debug/libv8.so(v8::internal::ParserBase<v8::internal::Parser>::ParseExpressionCoverGrammar()+0xe4) [0x7f6161c4f6a4]
    v8/out/x64.debug/libv8.so(v8::internal::ParserBase<v8::internal::Parser>::ParseExpressionOrLabelledStatement(v8::internal::ZoneList<v8::internal::AstRawString const*>*, v8::internal::ZoneList<v8::internal::AstRawString const*>*, v8::internal::AllowLabelledFunctionStatement)+0x1a6) [0x7f6161c5e266]
    v8/out/x64.debug/libv8.so(v8::internal::ParserBase<v8::internal::Parser>::ParseStatementList(v8::internal::ScopedList<v8::internal::Statement*, void*>*, v8::internal::Token::Value)+0x239) [0x7f6161c2af69]
    v8/out/x64.debug/libv8.so(v8::internal::Parser::DoParseProgram(v8::internal::Isolate*, v8::internal::ParseInfo*)+0x44c) [0x7f6161c2a14c]
    v8/out/x64.debug/libv8.so(v8::internal::Parser::ParseProgram(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Script>, v8::internal::ParseInfo*, v8::internal::MaybeHandle<v8::internal::ScopeInfo>)+0x3ad) [0x7f6161c2993d]
    v8/out/x64.debug/libv8.so(v8::internal::parsing::ParseProgram(v8::internal::ParseInfo*, v8::internal::Handle<v8::internal::Script>, v8::internal::MaybeHandle<v8::internal::ScopeInfo>, v8::internal::Isolate*, v8::internal::parsing::ReportStatisticsMode)+0x1cf) [0x7f6161c67eff]
    v8/out/x64.debug/libv8.so(+0x2ad0e28) [0x7f6160ed0e28]
    v8/out/x64.debug/libv8.so(+0x2aea30e) [0x7f6160eea30e]
    v8/out/x64.debug/libv8.so(+0x2ad49dc) [0x7f6160ed49dc]
    v8/out/x64.debug/libv8.so(v8::internal::Compiler::GetSharedFunctionInfoForScript(v8::internal::Isolate*, v8::internal::Handle<v8::internal::String>, v8::internal::ScriptDetails const&, v8::ScriptCompiler::CompileOptions, v8::ScriptCompiler::NoCacheReason, v8::internal::NativesFlag, v8::ScriptCompiler::CompilationDetails*)+0x33) [0x7f6160ed45c3]
    v8/out/x64.debug/libv8.so(v8::ScriptCompiler::CompileUnboundInternal(v8::Isolate*, v8::ScriptCompiler::Source*, v8::ScriptCompiler::CompileOptions, v8::ScriptCompiler::NoCacheReason)+0x3d6) [0x7f6160c01c26]
    v8/out/x64.debug/libv8.so(v8::ScriptCompiler::Compile(v8::Local<v8::Context>, v8::ScriptCompiler::Source*, v8::ScriptCompiler::CompileOptions, v8::ScriptCompiler::NoCacheReason)+0x36) [0x7f6160c02246]
    ./d8(v8::MaybeLocal<v8::Script> v8::Shell::CompileString<v8::Script>(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::String>, v8::ScriptOrigin const&)+0x209) [0x5654fe8aa229]
    ./d8(v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*)+0x59e) [0x5654fe8a970e]
    ./d8(v8::SourceGroup::Execute(v8::Isolate*)+0x2be) [0x5654fe8c3cde]
    ./d8(v8::Shell::RunMainIsolate(v8::Isolate*, bool)+0x13e) [0x5654fe8c88ce]
    ./d8(v8::Shell::RunMain(v8::Isolate*, bool)+0x118) [0x5654fe8c8438]
    ./d8(v8::Shell::Main(int, char**)+0xdfd) [0x5654fe8c9f3d]
    /lib/x86_64-linux-gnu/libc.so.6(+0x29d90) [0x7f615dc29d90]
    /lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0x80) [0x7f615dc29e40]
    ./d8(_start+0x2a) [0x5654fe891d9a]
Trace/breakpoint trap

```

### 24...@project.gserviceaccount.com (2024-09-13)

ClusterFuzz testcase 5109830918275072 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=96058:96059

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### cl...@appspot.gserviceaccount.com (2024-09-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5401078656860160.

### is...@chromium.org (2024-09-13)

Indeed ClusterFuzz has already detected this issue (will be tracked here: [issue 366323452](https://issues.chromium.org/issues/366323452)). Thank you for the smaller repro and explanation.

### pe...@google.com (2024-09-13)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: M128 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M129 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128, 129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2024-09-13)

Looking at canary, a parser related crash (not enough to autofile a bug) just started occurring on Canary today. Given the scope of this change, this fix should not yet be merged nor or on Monday since the M129 Stable RC is being re-cut on Monday. I'll revisit this next week after 129 Stable RC has been recut and there's more Canary data to verify if there's an issue or not.

### pe...@google.com (2024-09-17)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: M128 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M129 is already shipping to stable.

**Merge approved:** your change passed merge requirements and is auto-approved for M130. Please go ahead and merge the CL to branch 6723 (refs/branch-heads/6723) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: eakpobaro (Android), eakpobaro (iOS), gmpritchard (ChromeOS), danielyip (Desktop)
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128, 129, 130].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sp...@google.com (2024-09-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process / the renderer + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-19)

Congratulations Tashita Software team! Thank you for your efforts and reporting this issue to us!

### ta...@gmail.com (2024-09-19)

Glad to contribute and appreciate your quick response.

### am...@chromium.org (2024-09-19)

It looks like the issue with scopes was resolved through the respective crash report related to that culprit, looking at newer Canary data, there appear to be no other parser related issues.
This fix landed on 130, so no merge to 130 needed.

Merges approved for <https://crrev.com/c/5850479>, please go ahead and merge this fix to branch to 12.9 and 12.8 at soonest, before 10am tomorrow, 20 September, so this fix can be included in the next Stable and Extended Stable updates.

### is...@chromium.org (2024-09-19)

We'll need to merge back <https://crrev.com/c/5850479> with a follow-up fix <https://crrev.com/c/5872647> (see [#comment14](https://issues.chromium.org/issues/363538434#comment14), <https://crbug.com/366323452#comment3>). The second CL wasn't released to Canary yet.

### am...@chromium.org (2024-09-19)

Sorry I missed that, it wasn't clear from that comment that the other CL needed backporting in relation to this fix.
Can <https://crrev.com/c/5850479> be backmerged in the meantime, or does it need to have <https://crrev.com/c/5872647> merged with it at the together in order?

### am...@chromium.org (2024-09-19)

Adding a follow up note since I'm about to board a plane in a bit: if <https://crrev.com/c/5872647> has to be backmerged with <https://crrev.com/c/5850479> then the merged should be held back until appropriate bake time and merge review revisited Monday, meaning that this may need to wait until the stable update the following wee.

### is...@chromium.org (2024-09-20)

Preparing merge CLs combining both CLs (<https://crrev.com/c/5850479> and <https://crrev.com/c/5872647>) for Monday:

M129: <https://crrev.com/c/5877006>

M128: <https://crrev.com/c/5874049>

### ap...@google.com (2024-09-23)

Project: v8/v8
Branch: refs/branch-heads/12.9

commit bd22ebd5e81debd7eac52f3d019fda679b878024
Author: Igor Sheludko <ishell@chromium.org>
Date:   Fri Sep 20 13:37:33 2024

    Merged: [parser] Fix initializer ids w/ computed property names
    
    Move the initializer id before the computed property name ids.
    
    Bug: 363538434
    (cherry picked from commit 8068f489ec2c7e9de15e179c8c25b45224f7f96f)
    
    
    Merged: [parser] Fix parse errors in static computed class properties
    
    Otherwise we'll try to rewrite a FailureExpression
    
    (cherry picked from commit 3b1adc17c16bdf748b947b372e7685b36b6dc02c)
    
    Bug: 366323452
    Change-Id: I1c172effc29ab593545700d79a10cd2aecaa6112
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5877006
    Commit-Queue: Igor Sheludko <ishell@chromium.org>
    Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.9@{#39}
    Cr-Branched-From: 64a21d7ad7fca1ddc73a9264132f703f35000b69-refs/heads/12.9.202@{#1}
    Cr-Branched-From: da4200b2cfe6eb1ad73c457ed27cf5b7ff32614f-refs/heads/main@{#95679}

M       src/parsing/parser-base.h
M       src/parsing/parser.cc
M       src/parsing/parser.h
M       src/parsing/preparser.h
A       test/mjsunit/regress/regress-363538434.js
A       test/mjsunit/regress/regress-366323452.js

https://chromium-review.googlesource.com/5877006


### pe...@google.com (2024-09-23)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ap...@google.com (2024-09-23)

Project: v8/v8
Branch: refs/branch-heads/12.8

commit e2b6cf4e6e8b036fe75142a9ab18ed8fe4169cee
Author: Igor Sheludko <ishell@chromium.org>
Date:   Fri Sep 20 13:41:33 2024

    Merged: [parser] Fix initializer ids w/ computed property names
    
    Move the initializer id before the computed property name ids.
    
    Bug: 363538434
    (cherry picked from commit 8068f489ec2c7e9de15e179c8c25b45224f7f96f)
    
    
    Merged: [parser] Fix parse errors in static computed class properties
    
    Otherwise we'll try to rewrite a FailureExpression
    
    (cherry picked from commit 3b1adc17c16bdf748b947b372e7685b36b6dc02c)
    
    Bug: 366323452
    Change-Id: If1311f0cd280b0cdd9dcb8967c45bffd123c466e
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5874049
    Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    Commit-Queue: Igor Sheludko <ishell@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.8@{#69}
    Cr-Branched-From: 70cbb397b153166027e34c75adf8e7993858222e-refs/heads/12.8.374@{#1}
    Cr-Branched-From: 451b63ed4251c2b21c56144d8428f8be3331539b-refs/heads/main@{#95151}

M       src/parsing/parser-base.h
M       src/parsing/parser.cc
M       src/parsing/parser.h
M       src/parsing/preparser.h
A       test/mjsunit/regress/regress-363538434.js
A       test/mjsunit/regress/regress-366323452.js

https://chromium-review.googlesource.com/5874049


### qk...@google.com (2024-09-26)

Labeling LTS-NotApplicable-126 because the patch[1] is a fix for a previous CL (https://chromium-review.googlesource.com/c/v8/v8/+/5850479) which was fixing issue https://crbug.com/363538434 which was introduced in M128.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/5872647

### pe...@google.com (2024-12-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/363538434)*
