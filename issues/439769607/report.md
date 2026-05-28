# Debug check failed: constpool_.isEmpty in assembler-arm64.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [439769607](https://issues.chromium.org/issues/439769607) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | e5...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2025-08-19 |
| **Bounty** | Confirmed (amount unknown) |

## Description

## RCA

For arm64 device, if deopt nums exceed the limit,this fails when EmitDeopts.

```
bool MaglevCodeGenerator::EmitDeopts() {
  const size_t num_deopts = code_gen_state_.eager_deopts().size() +
                            code_gen_state_.lazy_deopts().size();
  if (num_deopts > Deoptimizer::kMaxNumberOfEntries) {
    return false;
  }
  // ...
}


```

EmitCode will fail too, but do not clear ConstPool for Arm64 Platform.

```
bool MaglevCodeGenerator::EmitCode() {
   // ...
   if (!EmitDeopts()) return false;
  // ...
}

bool MaglevCodeGenerator::Assemble() {
  if (!EmitCode()) {
#ifdef V8_TARGET_ARCH_ARM
    // Even if we fail, we force emit the constant pool, so that it is empty.
    __ CheckConstPool(true, false);
#endif
    return false;
  }
  // ...
}


```

This will cause the following check fail in ~Assembler.

```
Assembler::~Assembler() {
  DCHECK(constpool_.IsEmpty());
  DCHECK_EQ(veneer_pool_blocked_nesting_, 0);
}


```
## POC

```
argsList = ""
var body = "";
var ITER = 3300;
for (var i = 0; i < ITER; i++) {
  body += "let i" + i + " = () => {};\\nfor(let j = 0; j < 1; j++) {\\n  i" + i + "();\\n}"
}
var Func = new Function(argsList, body);

% PrepareFunctionForOptimization(Func);
Func();
% OptimizeMaglevOnNextCall(Func);
Func();

Func();


```
## Trace

```
#
# Fatal error in ../../src/codegen/arm64/assembler-arm64.cc, line 417
# Debug check failed: constpool_.IsEmpty().
#
#
#
#FailureMessage Object: 0x16b359298
==== C stack trace ===============================

    0   libv8_libbase.dylib                 0x0000000104c3a11c v8::base::debug::StackTrace::StackTrace() + 24
    1   libv8_libplatform.dylib             0x0000000104c76718 v8::platform::(anonymous namespace)::PrintStackTrace() + 116
    2   libv8_libbase.dylib                 0x0000000104c1d4e4 V8_Fatal(char const*, int, char const*, ...) + 352
    3   libv8_libbase.dylib                 0x0000000104c1ce28 v8::base::SetFatalFunction(void (*)(char const*, int, char const*)) + 0
    4   libv8.dylib                         0x000000010d4475d8 v8::internal::Assembler::~Assembler() + 384
    5   libv8.dylib                         0x000000010cbd80fc v8::internal::maglev::MaglevCodeGenerator::~MaglevCodeGenerator() + 252
    6   libv8.dylib                         0x000000010cbdadcc v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*) + 4180
    7   libv8.dylib                         0x000000010cdad6a4 v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*) + 96
    8   libv8.dylib                         0x000000010bb13d88 v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*) + 160
    9   libv8.dylib                         0x000000010bb36120 v8::internal::(anonymous namespace)::CompileMaglev(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::BytecodeOffset, v8::internal::(anonymous namespace)::CompileResultBehavior) + 832
    10  libv8.dylib                         0x000000010bb24e84 v8::internal::(anonymous namespace)::GetOrCompileOptimized(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind, v8::internal::BytecodeOffset, v8::internal::(anonymous namespace)::CompileResultBehavior) + 1512
    11  libv8.dylib                         0x000000010bb240f0 v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind) + 700
    12  libv8.dylib                         0x000000010c89dd34 v8::internal::(anonymous namespace)::CompileOptimized(v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind, v8::internal::Isolate*) + 316
    13  libv8.dylib                         0x000000010c897078 v8::internal::__RT_impl_Runtime_OptimizeMaglevEager(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) + 156
    14  libv8.dylib                         0x000000010c896c5c v8::internal::Runtime_OptimizeMaglevEager(int, unsigned long*, v8::internal::Isolate*) + 148
    15  ???                                 0x00000003079ef5f0 0x0 + 13012760048
    16  ???                                 0x0000000307739270 0x0 + 13009916528
    17  ???                                 0x0000000300001330 0x0 + 12884906800
    18  ???                                 0x000000030772e740 0x0 + 13009872704
    19  ???                                 0x000000030772e374 0x0 + 13009871732
    20  libv8.dylib                         0x000000010bd35bcc v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) + 5132
    21  libv8.dylib                         0x000000010bd36954 v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>) + 444
    22  libv8.dylib                         0x000000010b92ea98 v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) + 1156
    23  d8                                  0x0000000104ac20f8 v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) + 1756
    24  d8                                  0x0000000104ade22c v8::SourceGroup::Execute(v8::Isolate*) + 472
    25  d8                                  0x0000000104ae29f0 v8::Shell::RunMainIsolate(v8::Isolate*, bool) + 476
    26  d8                                  0x0000000104ae23ac v8::Shell::RunMain(v8::Isolate*, bool) + 344
    27  d8                                  0x0000000104ae3edc v8::Shell::Main(int, char**) + 3308
    28  dyld                                0x0000000182902b98 start + 6076
[1]    50281 trace trap  ./d8 --allow-natives-syntax poc.js


```

## Timeline

### cl...@appspot.gserviceaccount.com (2025-08-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5525323298832384.

### e5...@gmail.com (2025-08-20)

Sorry for the confusion. The "\n" characters in the POC were likely escaped incorrectly when it was copied and pasted.

The POC should be

```
argsList = ""
var body = "";
var ITER = 3300;
for (var i = 0; i < ITER; i++) {
  body += "let i" + i + " = () => {};\nfor(let j = 0; j < 1; j++) {\n  i" + i + "();\n}"
}
var Func = new Function(argsList, body);

% PrepareFunctionForOptimization(Func);
Func();
% OptimizeMaglevOnNextCall(Func);
Func();

Func();

```

### cl...@appspot.gserviceaccount.com (2025-08-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5051984147054592.

### cl...@appspot.gserviceaccount.com (2025-08-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5867619932372992.

### fl...@google.com (2025-08-20)

Assigning tentative severity & foundin due to being in V8 + a plausible-looking stacktrace and explanation.

However, reporter, I'm still not able to reproduce given the newest testcase you've given.  I've run it on Linux arm64, and tried both with default settings and with the `--maglev` flag.  Is there some other platform we should be running this on, or some other set of flags we should be using?  It will be hard for us to triage/fix without some way to reproduce.

### e5...@gmail.com (2025-08-21)

I can repro both on mac apple silicon and the linux\_asan\_d8\_v8\_arm64\_dbg build clusterfuzz used with only "--allow-natives-syntax" flag. Maybe a longer timeout limit is needed? It takes longer time for me on the linux\_asan\_d8\_v8\_arm64\_dbg build than on my mac.

### cl...@appspot.gserviceaccount.com (2025-08-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5759125480734720.

### ch...@google.com (2025-08-21)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-08-21)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cl...@appspot.gserviceaccount.com (2025-08-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6373182390861824.

### ta...@google.com (2025-08-22)

I am unable to reproduce it myself, but mdanylo@ was able to reproduce it on our fuzzing machine. Based on the description, I believe it's related to [crrev/c/4579308](https://crrev.com/c/4579308). I am conservatively keeping the vulnerability type, but I am unsure if it has any security implications. victorgomes@ could you please take a look at it?

### vi...@chromium.org (2025-08-25)

Not a vulnerability, since we drop the assembly code.

### dx...@google.com (2025-08-25)

Project: v8/v8  

Branch:  main  

Author:  Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6875820>

[maglev] Properly clear state on failures

---


Expand for full commit details
```
     
    Fixed: 439769607 
    Change-Id: Ia540ce656311aba7f7e4e28f2adec8dd0773fe7a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6875820 
    Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102012}

```

---

Files:

- M `src/codegen/arm/assembler-arm.h`
- M `src/codegen/arm64/assembler-arm64.h`
- M `src/codegen/ia32/assembler-ia32.h`
- M `src/codegen/loong64/assembler-loong64.h`
- M `src/codegen/mips64/assembler-mips64.h`
- M `src/codegen/ppc/assembler-ppc.h`
- M `src/codegen/riscv/assembler-riscv.h`
- M `src/codegen/s390/assembler-s390.h`
- M `src/codegen/x64/assembler-x64.h`
- M `src/maglev/maglev-code-generator.cc`

---

Hash: [6b50f3ee796639fe3e0b666aa670a15e2e169cbe](https://chromiumdash.appspot.com/commit/6b50f3ee796639fe3e0b666aa670a15e2e169cbe)  

Date: Mon Aug 25 12:02:40 2025


---

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Thank you for the report. As this is a report of an issue that does not have any security implications, this report is unfortunately not eligible for a Chrome VRP reward.

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### ch...@google.com (2025-12-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you for the report. As this is a report of an issue that does not have any security implications, this report is unfortunately not eligible for a Chrome VRP reward.
> 
> Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.
> 
> Regards,
> Google Security Bot
> 
> 
> --
> How did we do? Please

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/439769607)*
