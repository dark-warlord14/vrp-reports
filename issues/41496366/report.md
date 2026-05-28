# Security: Debug check failed: op.input_count >= 2  in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [41496366](https://issues.chromium.org/issues/41496366) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Reporter** | je...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2024-01-31 |
| **Bounty** | $7,000.00 |

## Description

see comment https://crbug.com/chromium/1523415#c2


VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91976
    - link: https://crrev.com/e08a30ef808cc7fce03279d4f327ad6505050c4d 
- Commit Message

```
commit e08a30ef808cc7fce03279d4f327ad6505050c4d
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Wed Jan 24 08:55:16 2024 +0100

    [turboshaft] Enable x64 instruction selection on Turboshaft by default
   
    Bug: v8:12783, chromium:1454443
    Change-Id: I53aeb54ec7b8963cbfbeaae5d1493a547532986d
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5233500
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91976}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux32-debug-v8-component-92093/d8 --expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging --turboshaft-csa poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/backend/ia32/instruction-selector-ia32.cc, line 550
# Debug check failed: op.input_count >= 2 (1 vs. 2).
#
#
#
#FailureMessage Object: 0xffffb170
==== C stack trace ===============================

    /tmp/d8-linux32-debug-v8-component-92093/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1f) [0xf7fb333f]
    /tmp/d8-linux32-debug-v8-component-92093/libv8_libplatform.so(+0x163b4) [0xf7f5f3b4]
    /tmp/d8-linux32-debug-v8-component-92093/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xf7) [0xf7f926d7]
    /tmp/d8-linux32-debug-v8-component-92093/libv8_libbase.so(+0x270d6) [0xf7f920d6]
    /tmp/d8-linux32-debug-v8-component-92093/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x31) [0xf7f92721]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::IA32OperandGeneratorT<v8::internal::compiler::TurboshaftAdapter>::GetEffectiveAddressMemoryOperand(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::InstructionOperand*, unsigned int*, v8::internal::compiler::OperandGeneratorT<v8::internal::compiler::TurboshaftAdapter>::RegisterMode)+0x7e0) [0xf7231840]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitLoad(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::OpIndex, unsigned int)+0xb7) [0xf721f857]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitLoad(v8::internal::compiler::turboshaft::OpIndex)+0xcc) [0xf721f64c]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitNode(v8::internal::compiler::turboshaft::OpIndex)+0x3cf3) [0xf6cfd993]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitBlock(v8::internal::compiler::turboshaft::Block*)+0x624) [0xf6cf1ae4]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::SelectInstructions()+0x8c4) [0xf6cf0a04]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::InstructionSelector::SelectInstructions()+0x49) [0xf6d09e79]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::turboshaft::InstructionSelectionPhase::Run(v8::internal::Zone*, v8::internal::compiler::CallDescriptor const*, v8::internal::compiler::Linkage*, v8::internal::CodeTracer*)+0x68a) [0xf77091da]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::InstructionSelectionPhase, v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&>(v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&)+0xe5) [0xf70d9f35]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::PipelineImpl::SelectInstructionsTurboshaft(v8::internal::compiler::Linkage*)+0xe0) [0xf70cc210]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::PipelineImpl::OptimizeGraph(v8::internal::compiler::Linkage*)+0xe16) [0xf70c4c36]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0xcb) [0xf70c399b]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x86) [0xf565bf76]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x20839b2) [0xf56839b2]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x20708c1) [0xf56708c1]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0xd5) [0xf5672bb5]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x2e34f8f) [0xf6434f8f]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::Runtime_CompileOptimized(int, unsigned int*, v8::internal::Isolate*)+0x86) [0xf6434926]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x16dd799) [0xf4cdd799]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x13b2f89) [0xf49b2f89]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x13b2eb7) [0xf49b2eb7]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x13abdf9) [0xf49abdf9]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x13abc6d) [0xf49abc6d]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x224086b) [0xf584086b]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>)+0x2cb) [0xf5841feb]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>)+0x68a) [0xf53aa41a]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::Script::Run(v8::Local<v8::Context>)+0x2c) [0xf53a9d7c]
    /tmp/d8-linux32-debug-v8-component-92093/d8(v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::PrintResult, v8::Shell::ReportExceptions, v8::Shell::ProcessMessageQueue)+0xaf0) [0x5659f060]
    /tmp/d8-linux32-debug-v8-component-92093/d8(v8::SourceGroup::Execute(v8::Isolate*)+0x2cb) [0x565b9e9b]
    /tmp/d8-linux32-debug-v8-component-92093/d8(v8::Shell::RunMainIsolate(v8::Isolate*, bool)+0x111) [0x565bdcb1]
    /tmp/d8-linux32-debug-v8-component-92093/d8(v8::Shell::RunMain(v8::Isolate*, bool)+0x114) [0x565bd874]
    /tmp/d8-linux32-debug-v8-component-92093/d8(v8::Shell::Main(int, char**)+0x14dd) [0x565c046d]
    /tmp/d8-linux32-debug-v8-component-92093/d8(main+0x1f) [0x565c06df]
    /lib/i386-linux-gnu/libc.so.6(+0x21519) [0xf2c21519]
Received signal 6

```

## Other
Please note to include the flags `--expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging --turboshaft-csa` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.3.0 - 12.3.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux32-debug/d8-linux32-debug-v8-component-92093.zip
2. Run: `d8 --expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging --turboshaft-csa poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry



## Attachments

- [poc.js](attachments/poc.js) (text/plain, 4.3 KB)
- [poc.js](attachments/poc.js) (text/javascript, 4.3 KB)

## Timeline

### je...@gmail.com (2024-01-31)

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91976
    - link: https://crrev.com/e08a30ef808cc7fce03279d4f327ad6505050c4d 
- Commit Message

```
commit e08a30ef808cc7fce03279d4f327ad6505050c4d
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Wed Jan 24 08:55:16 2024 +0100

    [turboshaft] Enable x64 instruction selection on Turboshaft by default
    
    Bug: v8:12783, chromium:1454443
    Change-Id: I53aeb54ec7b8963cbfbeaae5d1493a547532986d
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5233500
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91976}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux32-debug-v8-component-92093/d8 --expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging --turboshaft-csa poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/backend/ia32/instruction-selector-ia32.cc, line 550
# Debug check failed: op.input_count >= 2 (1 vs. 2).
#
#
#
#FailureMessage Object: 0xffffb170
==== C stack trace ===============================

    /tmp/d8-linux32-debug-v8-component-92093/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1f) [0xf7fb333f]
    /tmp/d8-linux32-debug-v8-component-92093/libv8_libplatform.so(+0x163b4) [0xf7f5f3b4]
    /tmp/d8-linux32-debug-v8-component-92093/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xf7) [0xf7f926d7]
    /tmp/d8-linux32-debug-v8-component-92093/libv8_libbase.so(+0x270d6) [0xf7f920d6]
    /tmp/d8-linux32-debug-v8-component-92093/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x31) [0xf7f92721]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::IA32OperandGeneratorT<v8::internal::compiler::TurboshaftAdapter>::GetEffectiveAddressMemoryOperand(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::InstructionOperand*, unsigned int*, v8::internal::compiler::OperandGeneratorT<v8::internal::compiler::TurboshaftAdapter>::RegisterMode)+0x7e0) [0xf7231840]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitLoad(v8::internal::compiler::turboshaft::OpIndex, v8::internal::compiler::turboshaft::OpIndex, unsigned int)+0xb7) [0xf721f857]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitLoad(v8::internal::compiler::turboshaft::OpIndex)+0xcc) [0xf721f64c]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitNode(v8::internal::compiler::turboshaft::OpIndex)+0x3cf3) [0xf6cfd993]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::VisitBlock(v8::internal::compiler::turboshaft::Block*)+0x624) [0xf6cf1ae4]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::InstructionSelectorT<v8::internal::compiler::TurboshaftAdapter>::SelectInstructions()+0x8c4) [0xf6cf0a04]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::InstructionSelector::SelectInstructions()+0x49) [0xf6d09e79]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::turboshaft::InstructionSelectionPhase::Run(v8::internal::Zone*, v8::internal::compiler::CallDescriptor const*, v8::internal::compiler::Linkage*, v8::internal::CodeTracer*)+0x68a) [0xf77091da]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::turboshaft::InstructionSelectionPhase, v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&>(v8::internal::compiler::CallDescriptor*&, v8::internal::compiler::Linkage*&, v8::internal::CodeTracer*&)+0xe5) [0xf70d9f35]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::PipelineImpl::SelectInstructionsTurboshaft(v8::internal::compiler::Linkage*)+0xe0) [0xf70cc210]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::PipelineImpl::OptimizeGraph(v8::internal::compiler::Linkage*)+0xe16) [0xf70c4c36]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0xcb) [0xf70c399b]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x86) [0xf565bf76]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x20839b2) [0xf56839b2]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x20708c1) [0xf56708c1]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0xd5) [0xf5672bb5]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x2e34f8f) [0xf6434f8f]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::Runtime_CompileOptimized(int, unsigned int*, v8::internal::Isolate*)+0x86) [0xf6434926]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x16dd799) [0xf4cdd799]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x13b2f89) [0xf49b2f89]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x13b2eb7) [0xf49b2eb7]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x13abdf9) [0xf49abdf9]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x13abc6d) [0xf49abc6d]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(+0x224086b) [0xf584086b]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>)+0x2cb) [0xf5841feb]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>)+0x68a) [0xf53aa41a]
    /tmp/d8-linux32-debug-v8-component-92093/libv8.so(v8::Script::Run(v8::Local<v8::Context>)+0x2c) [0xf53a9d7c]
    /tmp/d8-linux32-debug-v8-component-92093/d8(v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::PrintResult, v8::Shell::ReportExceptions, v8::Shell::ProcessMessageQueue)+0xaf0) [0x5659f060]
    /tmp/d8-linux32-debug-v8-component-92093/d8(v8::SourceGroup::Execute(v8::Isolate*)+0x2cb) [0x565b9e9b]
    /tmp/d8-linux32-debug-v8-component-92093/d8(v8::Shell::RunMainIsolate(v8::Isolate*, bool)+0x111) [0x565bdcb1]
    /tmp/d8-linux32-debug-v8-component-92093/d8(v8::Shell::RunMain(v8::Isolate*, bool)+0x114) [0x565bd874]
    /tmp/d8-linux32-debug-v8-component-92093/d8(v8::Shell::Main(int, char**)+0x14dd) [0x565c046d]
    /tmp/d8-linux32-debug-v8-component-92093/d8(main+0x1f) [0x565c06df]
    /lib/i386-linux-gnu/libc.so.6(+0x21519) [0xf2c21519]
Received signal 6

```

## Other
Please note to include the flags `--expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging --turboshaft-csa` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.3.0 - 12.3.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux32-debug/d8-linux32-debug-v8-component-92093.zip
2. Run: `d8 --expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging --turboshaft-csa poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

### je...@gmail.com (2024-01-31)

I don't believe this is the actual introduction point, but I'm unable to identify a better one by adjusting flags.
However, it has been in existence for over 7 days.

### [Deleted User] (2024-01-31)

[Empty comment from Monorail migration]

### me...@chromium.org (2024-01-31)

Thanks for the report and the bisect.

nicohartmann: Can you PTAL?


[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### je...@gmail.com (2024-01-31)

[Comment Deleted]

### dm...@chromium.org (2024-01-31)

CC jkummerow@ who implemented the IA32 instruction selector for Turboshaft.

### ni...@chromium.org (2024-01-31)

I am taking a look. This is not a security issue because it requires --turboshaft-csa, which is an experimental feature.

### ni...@chromium.org (2024-01-31)

To be a bit more specific: What's required is the `--turboshaft-instruction-selection` flag, which is disabled by default on ia32. It is implied by the experimental `--turboshaft-csa` flag. There is no security impact currently, but this could be a security issue once we ship it, so setting severity to high.

### je...@gmail.com (2024-01-31)

This message is just for the Chrome VRP team:
Although the Turboshaft CSA feature has not yet been released in the stable version, it is still eligible for the full VRP reward.

https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules
```
Bugs in unlaunched features - those that are behind a flag not enabled by default - are generally eligible for the full potential VRP reward. This is with the exception of bugs in V8 features marked as Experimental, as these features are part of early and experimental V8 development efforts and introduce a known stability and security risk. Security bugs specific to V8 Experimental features are not eligible for Chrome VRP rewards. The experimental status of a V8 feature is indicated in the flag definition in the source code, in the flag description in the help menu, and through a printed message at runtime.
```


From the flag in the --help output and the runtime message, we can see that, even though it is not yet enabled, it is not one of those experimental features that are ineligible for the V8 VRP.
```
  --turboshaft-csa (run the CSA pipeline with turboshaft)
        type: bool  default: --no-turboshaft-csa
```

In the issue tracker, Security_Impact represents the scope of impact of a vulnerability. Security_Impact-None is the correct categorization. Security_Severity indicates the level of harm of the vulnerability. Security_Severity-High is appropriate.


### gi...@appspot.gserviceaccount.com (2024-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/95f8155029402a21768f3bdb8e88902e508472e4

commit 95f8155029402a21768f3bdb8e88902e508472e4
Author: Nico Hartmann <nicohartmann@chromium.org>
Date: Wed Jan 31 16:44:47 2024

[turboshaft] Prevent Loads/Stores with offsets that are out of range

Bug: v8:12783, chromium:1523415
Change-Id: I087611da51d4a6c1fe0d60512a17ae5046b3abd2
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5249899
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#92124}

[modify] https://crrev.com/95f8155029402a21768f3bdb8e88902e508472e4/src/compiler/turboshaft/operations.h
[modify] https://crrev.com/95f8155029402a21768f3bdb8e88902e508472e4/src/compiler/backend/x64/instruction-selector-x64.cc
[add] https://crrev.com/95f8155029402a21768f3bdb8e88902e508472e4/test/mjsunit/regress/regress-1523415.js
[modify] https://crrev.com/95f8155029402a21768f3bdb8e88902e508472e4/src/compiler/turboshaft/load-store-simplification-reducer.h
[modify] https://crrev.com/95f8155029402a21768f3bdb8e88902e508472e4/src/compiler/backend/ia32/instruction-selector-ia32.cc


### ad...@google.com (2024-01-31)

(I am a bot: this is an auto-cc on a security bug)

### ni...@chromium.org (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1523415?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### am...@google.com (2024-02-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-14)

Congratulations Jerry! The Chrome VRP Panel has decided to award you $7,000 for this report of a memory corruption bug in the renderer / sandboxed process. Thank you for your efforts and reporting this issue to us!

### je...@gmail.com (2024-02-15)

Hi, Amy :)
It's great to see you again in the new issue tracker. More bug reports are waiting for us.

### pe...@google.com (2024-05-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41496366)*
