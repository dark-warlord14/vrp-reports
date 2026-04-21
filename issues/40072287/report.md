# Security: Fatal error in ../../src/ast/ast.h, line 1477

| Field | Value |
|-------|-------|
| **Issue ID** | [40072287](https://issues.chromium.org/issues/40072287) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Compiler, Blink>JavaScript>Interpreter, Blink>JavaScript>Parser |
| **Platforms** | Linux |
| **Reporter** | be...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2023-09-14 |
| **Bounty** | $7,000.00 |

## Description

Security: Fatal error in ../../src/ast/ast.h, line 1477

Steps to reproduce the problem:
build flag:
gn gen out/fuzzbuild_new --args='is_debug=false dcheck_always_on=true v8_static_library=true v8_enable_slow_dchecks=true v8_enable_v8_checks=true v8_enable_verify_heap=true v8_enable_verify_csa=true v8_fuzzilli=true sanitizer_coverage_flags="trace-pc-guard" target_cpu="x64"'

environment:
Ubuntu 22.04.2 LTS 5.19.0-42-generic
v8 Version: commit c6a550a59e163a012aac9848071f8d6c96c1103d

or download d8 binary with 
https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-asan-linux-debug-v8-component-89834.zip?generation=1694049655561191&alt=media

run with:
d8 --allow-natives-syntax --fuzzing poc.js

result will be:


#
# Fatal error in ../../src/ast/ast.h, line 1477
# Debug check failed: is_resolved().
#
#
#
#FailureMessage Object: 0x7ffa8448c460
==== C stack trace ===============================

    ../d8-asan-linux-debug-v8-component-89834/d8(__interceptor_backtrace+0x75) [0x56522e9924c5]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7ffa91ccbaa3]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8_libplatform.so(+0x36c5a) [0x7ffa87fdbc5a]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x26f) [0x7ffa91c853ff]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8_libbase.so(+0x523af) [0x7ffa91c843af]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::BytecodeGenerator::VisitNamedSuperPropertyLoad(v8::internal::Property*, v8::internal::interpreter::Register)+0x8a7) [0x7ffa8c9ea777]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::BytecodeGenerator::VisitNoStackOverflowCheck(v8::internal::AstNode*)+0x446) [0x7ffa8ca0c256]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::BytecodeGenerator::VisitExpressionStatement(v8::internal::ExpressionStatement*)+0x29b) [0x7ffa8c9af6eb]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::BytecodeGenerator::VisitNoStackOverflowCheck(v8::internal::AstNode*)+0x413) [0x7ffa8ca0c223]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::BytecodeGenerator::VisitStatements(v8::internal::ZoneList<v8::internal::Statement*> const*)+0x12c) [0x7ffa8c9a9e9c]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::BytecodeGenerator::VisitBlockDeclarationsAndStatements(v8::internal::Block*)+0x382) [0x7ffa8c9ab7a2]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::BytecodeGenerator::VisitBlock(v8::internal::Block*)+0x676) [0x7ffa8c9aab26]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::BytecodeGenerator::VisitInitializeClassStaticElementsStatement(v8::internal::InitializeClassStaticElementsStatement*)+0xf3) [0x7ffa8c9cc223]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::BytecodeGenerator::VisitNoStackOverflowCheck(v8::internal::AstNode*)+0x476) [0x7ffa8ca0c286]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::BytecodeGenerator::VisitStatements(v8::internal::ZoneList<v8::internal::Statement*> const*)+0x12c) [0x7ffa8c9a9e9c]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::BytecodeGenerator::GenerateBytecodeBody()+0x5eb) [0x7ffa8c9a63db]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::BytecodeGenerator::GenerateBytecode(unsigned long)+0x901) [0x7ffa8c9a38f1]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::interpreter::InterpreterCompilationJob::ExecuteJobImpl()+0xb5c) [0x7ffa8ca4df8c]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::UnoptimizedCompilationJob::ExecuteJob()+0x204) [0x7ffa8ba3d934]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(+0x3ab148e) [0x7ffa8bab148e]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(+0x3a69f8e) [0x7ffa8ba69f8e]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*, v8::internal::CreateSourcePositions)+0x1612) [0x7ffa8ba678d2]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*)+0xc00) [0x7ffa8ba6be50]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(+0x5d51921) [0x7ffa8dd51921]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(v8::internal::Runtime_CompileLazy(int, unsigned long*, v8::internal::Isolate*)+0x146) [0x7ffa8dd507c6]
    /home/goushi/v8/v8/out/d8-asan-linux-debug-v8-component-89834/libv8.so(+0x2ad4b7d) [0x7ffa8aad4b7d]
Received signal 6
Aborted (core dumped)



## Attachments

- [poc.js](attachments/poc.js) (text/plain, 1.0 KB)

## Timeline

### [Deleted User] (2023-09-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-09-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5972992206766080.

### ja...@chromium.org (2023-09-14)

Sent the sample to clusterfuzz.

### ja...@chromium.org (2023-09-14)

Hi sroettger, passing this your way because you are the current v8 security shepherd.

I've added provisional ratings of severity High and found in of the M116 (the current extended stable release).

[Monorail components: Blink>JavaScript>Compiler]

### ja...@chromium.org (2023-09-14)

I was able to reproduce the stack trace that was reported by running the steps that the reporter documented.

### [Deleted User] (2023-09-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-09-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-09-14)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Interpreter Blink>JavaScript>Parser]

### cl...@chromium.org (2023-09-14)

Detailed Report: https://clusterfuzz.com/testcase?key=5972992206766080

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  is_resolved() in ast.h
  v8::internal::interpreter::BytecodeGenerator::VisitNamedSuperPropertyLoad
  v8::internal::interpreter::BytecodeGenerator::VisitNoStackOverflowCheck
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=87854:87855

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5972992206766080

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sr...@google.com (2023-09-15)

ishell@ can you take a look?
Clusterfuzz bisected this to c4bace41c896eeceed948b365855ec0048880439

### [Deleted User] (2023-09-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-15)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@chromium.org (2023-09-18)

[Empty comment from Monorail migration]

### is...@chromium.org (2023-09-18)

Thank you for the report!

The fix is on the way: https://chromium-review.googlesource.com/c/v8/v8/+/4871981

Setting severity to low because reproduction in real life requires a certain combination of lazy function compilations and stack overflow failures.

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-13)

Dear owner, please check the status of the issue and update it according to our guideline: http://go/v8-issue-guidelines

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### ad...@google.com (2024-01-25)

(I am a bot: this is an auto-cc on a security bug)

### am...@chromium.org (2024-01-25)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-25)

This issue was migrated from crbug.com/chromium/1482685?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>Compiler, Blink>JavaScript>Interpreter, Blink>JavaScript>Parser]
[Monorail components added to Component Tags custom field.]

### 24...@project.gserviceaccount.com (2024-03-09)

ClusterFuzz testcase 5972992206766080 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=92721:92722

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### am...@chromium.org (2024-03-11)

This issue was resolved by the fix landed for [crbug.com/327740539](https://crbug.com/327740539)

### pg...@google.com (2024-03-19)

Hi @reporter - how would you like to be credited for this bug?

### am...@chromium.org (2024-03-19)

This issue was automatically closed as Fixed/Verified by Clusterfuzz due to a fix landed on [crbug.com/327740539](https://crbug.com/327740539); it seems that (based on off-bug chat with ishell@ the `.home_object` variable might be left unresolved if we have to re-parse the function source. So I have re-opened this issue in the interim and it is not considered to be resolved yet at this time.

While this issue may share a root cause with [crbug.com/327740539](https://crbug.com/327740539), these are in fact two separate crashes -- one happens during parsing and another one during bytecode compilation.

Igor has conveyed he'll re-investigate this one in the next couple of days.

### be...@gmail.com (2024-03-19)

credit: CFF of Topsec Alpha Team

### pe...@google.com (2024-03-20)

ishell: Uh oh! This issue still open and hasn't been updated in the last 183 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### is...@chromium.org (2024-03-22)

Yes, the <https://chromium-review.googlesource.com/c/v8/v8/+/5350482> is indeed a better fix for this issue.

### am...@google.com (2024-03-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-27)

Congratulations CFF! The Chrome VRP Panel has decided to award you $7,000 for this report V8 memory corruption. Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-06-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072287)*
