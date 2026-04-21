# Security: Check failed: !v8::internal::v8_flags.enable_slow_asserts.value() || (IsSharedFunctionInfo_NonInline(*this)).

| Field | Value |
|-------|-------|
| **Issue ID** | [40075744](https://issues.chromium.org/issues/40075744) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Linux, Mac |
| **Reporter** | ki...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2023-10-27 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 90091
    - link: https://crrev.com/b076402592741b4608a16690781231ca96f452ac 
- Commit Message

```
commit b076402592741b4608a16690781231ca96f452ac
Author: Choongwoo Han <choongwoo.han@microsoft.com>
Date:   Thu Sep 21 07:24:09 2023 -0700

    Register weak objects in maglev code
    
    Maglev is holding strong references of objects in InstructionStream
    while TurboFan is managing them as weak objects with
    `RegisterWeakObjectsInOptimizedCode` function. Thus, the objects
    referenced by Maglev code is not freed until the code is freed.
    
    This CL updates Maglev to run the same function as TurboFan in the
    finalize step.
    
    Bug: chromium:1485367
    
    Change-Id: I47bd1de05e9014f277fd43bf58e184553f4966c5
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4880639
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Choongwoo Han <choongwoo.han@microsoft.com>
    Reviewed-by: Jakob Linke <jgruber@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#90091}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-90623/d8 --allow-natives-syntax --expose-gc --maglev-inline-api-calls poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/objects/object-type.cc, line 82
# Type cast failed in Parameter 0 at ../../src/builtins/builtins-constructor-gen.cc:179
  Expected SharedFunctionInfo but found 0x8ab00000061: [Oddball] in ReadOnlySpace: #undefined

#
#
#
#FailureMessage Object: 0x7ffd71e62be0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-90623/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f083c0a1cf3]
    /tmp/d8-linux-debug-v8-component-90623/libv8_libplatform.so(+0x19b9d) [0x7f083c048b9d]
    /tmp/d8-linux-debug-v8-component-90623/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f083c081cc4]
    /tmp/d8-linux-debug-v8-component-90623/libv8.so(v8::internal::CheckObjectType(unsigned long, unsigned long, unsigned long)+0x37b9) [0x7f083a2bcd99]
    /tmp/d8-linux-debug-v8-component-90623/libv8.so(+0x14f6a9f) [0x7f08388f6a9f]

```

## Other
Please note to include the flags `--allow-natives-syntax --expose-gc --maglev-inline-api-calls` for clusterfuzz classification.

VERSION
Tested on v8 version: 11.9.0 - 12.0.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-90623.zip
2. Run: `d8 --allow-natives-syntax --expose-gc --maglev-inline-api-calls poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 877 B)
- [poc.js](attachments/poc.js) (text/plain, 877 B)

## Timeline

### ki...@gmail.com (2023-10-27)

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 90091
    - link: https://crrev.com/b076402592741b4608a16690781231ca96f452ac 
- Commit Message

```
commit b076402592741b4608a16690781231ca96f452ac
Author: Choongwoo Han <choongwoo.han@microsoft.com>
Date:   Thu Sep 21 07:24:09 2023 -0700

    Register weak objects in maglev code
    
    Maglev is holding strong references of objects in InstructionStream
    while TurboFan is managing them as weak objects with
    `RegisterWeakObjectsInOptimizedCode` function. Thus, the objects
    referenced by Maglev code is not freed until the code is freed.
    
    This CL updates Maglev to run the same function as TurboFan in the
    finalize step.
    
    Bug: chromium:1485367
    
    Change-Id: I47bd1de05e9014f277fd43bf58e184553f4966c5
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4880639
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Choongwoo Han <choongwoo.han@microsoft.com>
    Reviewed-by: Jakob Linke <jgruber@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#90091}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-90623/d8 --allow-natives-syntax --expose-gc --maglev-inline-api-calls poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/objects/object-type.cc, line 82
# Type cast failed in Parameter 0 at ../../src/builtins/builtins-constructor-gen.cc:179
  Expected SharedFunctionInfo but found 0x8ab00000061: [Oddball] in ReadOnlySpace: #undefined

#
#
#
#FailureMessage Object: 0x7ffd71e62be0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-90623/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f083c0a1cf3]
    /tmp/d8-linux-debug-v8-component-90623/libv8_libplatform.so(+0x19b9d) [0x7f083c048b9d]
    /tmp/d8-linux-debug-v8-component-90623/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f083c081cc4]
    /tmp/d8-linux-debug-v8-component-90623/libv8.so(v8::internal::CheckObjectType(unsigned long, unsigned long, unsigned long)+0x37b9) [0x7f083a2bcd99]
    /tmp/d8-linux-debug-v8-component-90623/libv8.so(+0x14f6a9f) [0x7f08388f6a9f]

```

## Other
Please note to include the flags `--allow-natives-syntax --expose-gc --maglev-inline-api-calls` for clusterfuzz classification.

VERSION
Tested on v8 version: 11.9.0 - 12.0.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-90623.zip
2. Run: `d8 --allow-natives-syntax --expose-gc --maglev-inline-api-calls poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)  

### [Deleted User] (2023-10-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-10-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6301443888185344.

### cl...@chromium.org (2023-10-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-10-27)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### cl...@chromium.org (2023-10-27)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/bc5ebd949c2dea946f4493942db460ecb56e0652 ([fuzzing] Allow OptimizeMaglevOnNextCall for fuzzing).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2023-10-27)

Detailed Report: https://clusterfuzz.com/testcase?key=6301443888185344

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: Fatal error
Crash Address: 
Crash State:
  Type cast failed in Parameter 0 at ../../src/builtins/builtins-constructor-gen.c
  v8::internal::CheckObjectType
  Builtins_FastNewClosure
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=90546:90547

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6301443888185344

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ma...@chromium.org (2023-10-27)

Not sure why P3, setting to P1 until evaluated. + security sheriff and v8 fuzzing owner to evaluate priority.

It was expected that any use of OptimizeMaglevOnNextCall bisect back to my CL enabling it. To find the older culprit, I'll try to reupload using OptimizeFunctionOnNextCall.

### ma...@chromium.org (2023-10-27)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-10-27)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript>Runtime Blink>JavaScript>Compiler>Maglev]

### cl...@chromium.org (2023-10-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6486881986871296.

### cl...@chromium.org (2023-10-27)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-10-27)

The reupload in https://crbug.com/chromium/1496606#c11 confirms the initial bisection from https://crbug.com/chromium/1496606#c1. Assigning to reviewer of that CL for now.

### le...@chromium.org (2023-10-27)

Seems to require --maglev-inline-api-calls (which is off by default, so setting severity to low) -- Igor, can you take a look?

### ki...@gmail.com (2023-10-27)

re https://crbug.com/chromium/1496606#c14:
Hello! It seems there might be some misunderstanding.

The VRP (Vulnerability Reward Program) employs different tags to classify issues, where "Security_Impact" represents the scope of impact, while "Security_Severity" denotes the specific level of severity.

Please change "Security_Impact-Head" to "Security_Impact-None."

Please reevaluate its Security_Severity label based on the severity of the vulnerability, rather than whether it requires a flag "--maglev-inline-api-calls".









### ki...@gmail.com (2023-10-27)

In addition, I'm not entirely sure whether this flag is necessary and whether it can be triggered without this flag. At least from the point of introduction of the vulnerability, I don't think this is necessary.


### le...@chromium.org (2023-10-27)

You're right, I always get confused between severity and impact. Changing impact to None and clearing severity until we take a closer look.

For now I'm operating under the assumption that this flag is required for the crash, pending further investigation. If you manage to get this crash without the flag, please let us know.

### ki...@gmail.com (2023-10-31)

Hello，any update?thanks

### is...@chromium.org (2023-10-31)

[Empty comment from Monorail migration]

### is...@chromium.org (2023-10-31)


The issue seems to be related to inlining Api calls to Maglev vs lazy deopting from the Api call.

Smaller repro: out/x64.debug/d8 test.js --allow-natives-syntax --expose-gc --maglev-inline-api-calls

=== test.js ===
function main() {
  var v0 = [function f4() {}];
  var err = new Error();
  err.stack;
  try {
    v0();
  } catch (e) {
    print(e);
    e.stack;
  }
}

Error.prepareStackTrace = function (v1, v2) {
  gc();
};

%PrepareFunctionForOptimization(main);
main();
%OptimizeMaglevOnNextCall(main);
main();


### is...@chromium.org (2023-10-31)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-10-31)

Setting provisional severity of High, assuming this causes renderer memory corruption.

### gi...@appspot.gserviceaccount.com (2023-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/3281d2b6b068ef50350bfc68f476d410df5edfa4

commit 3281d2b6b068ef50350bfc68f476d410df5edfa4
Author: Igor Sheludko <ishell@chromium.org>
Date: Thu Nov 02 14:04:07 2023

[maglev] Fix inlining Api call builtin

... which didn't work when the Maglev code had to be lazy
deoptimized.

Bug: v8:13825, chromium:1445925, chromium:1496606
Change-Id: I640791a0ce1f8180cdc280382c0f7b0e5668d5dd
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4994337
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/main@{#90715}

[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/codegen/x64/macro-assembler-x64.h
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/maglev/maglev-assembler.h
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/codegen/arm64/macro-assembler-arm64.h
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/codegen/arm/macro-assembler-arm.h
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/maglev/arm64/maglev-assembler-arm64-inl.h
[add] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/test/mjsunit/regress/regress-crbug-1496606.js
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/maglev/x64/maglev-assembler-x64-inl.h
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/builtins/x64/builtins-x64.cc
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/maglev/maglev-ir.cc
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/builtins/arm64/builtins-arm64.cc
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/builtins/arm/builtins-arm.cc
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/codegen/arm64/macro-assembler-arm64.cc
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/maglev/arm/maglev-assembler-arm-inl.h
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/codegen/arm/macro-assembler-arm.cc
[modify] https://crrev.com/3281d2b6b068ef50350bfc68f476d410df5edfa4/src/codegen/x64/macro-assembler-x64.cc


### is...@chromium.org (2023-11-02)

Thank you for the report!

### [Deleted User] (2023-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/d5481000308f561dd8dc1b0c7ac42d983e162574

commit d5481000308f561dd8dc1b0c7ac42d983e162574
Author: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
Date: Thu Nov 02 21:38:38 2023

Revert "[maglev] Fix inlining Api call builtin"

This reverts commit 3281d2b6b068ef50350bfc68f476d410df5edfa4.

Reason for revert: Failed on Linux arm64 gc stress 
https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Linux%20-%20arm64%20-%20sim%20-%20gc%20stress/29537/overview

Original change's description:
> [maglev] Fix inlining Api call builtin
>
> ... which didn't work when the Maglev code had to be lazy
> deoptimized.
>
> Bug: v8:13825, chromium:1445925, chromium:1496606
> Change-Id: I640791a0ce1f8180cdc280382c0f7b0e5668d5dd
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4994337
> Reviewed-by: Toon Verwaest <verwaest@chromium.org>
> Commit-Queue: Igor Sheludko <ishell@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#90715}

Bug: v8:13825, chromium:1445925, chromium:1496606
Change-Id: I9b555efaf3ca9354a6cd585c782a2b0307ddbf64
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5002570
Owners-Override: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#90717}

[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/codegen/x64/macro-assembler-x64.h
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/maglev/maglev-assembler.h
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/codegen/arm64/macro-assembler-arm64.h
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/codegen/arm/macro-assembler-arm.h
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/maglev/arm64/maglev-assembler-arm64-inl.h
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/maglev/x64/maglev-assembler-x64-inl.h
[delete] https://crrev.com/af403d77484ad67f8f065a6071e05020edd90b1d/test/mjsunit/regress/regress-crbug-1496606.js
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/builtins/x64/builtins-x64.cc
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/maglev/maglev-ir.cc
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/builtins/arm64/builtins-arm64.cc
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/builtins/arm/builtins-arm.cc
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/codegen/arm64/macro-assembler-arm64.cc
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/maglev/arm/maglev-assembler-arm-inl.h
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/codegen/x64/macro-assembler-x64.cc
[modify] https://crrev.com/d5481000308f561dd8dc1b0c7ac42d983e162574/src/codegen/arm/macro-assembler-arm.cc


### is...@chromium.org (2023-11-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/961dd29ccfd1716a88bc8bc236768f7dc828aacc

commit 961dd29ccfd1716a88bc8bc236768f7dc828aacc
Author: Igor Sheludko <ishell@chromium.org>
Date: Mon Nov 06 14:50:50 2023

Reland "[maglev] Fix inlining Api call builtin"

This is a reland of commit 3281d2b6b068ef50350bfc68f476d410df5edfa4
The temporary fix is to disable code space compaction when
--maglev-inline-api-calls is enabled.

Original change's description:
> [maglev] Fix inlining Api call builtin
>
> ... which didn't work when the Maglev code had to be lazy
> deoptimized.
>
> Bug: v8:13825, chromium:1445925, chromium:1496606
> Change-Id: I640791a0ce1f8180cdc280382c0f7b0e5668d5dd
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4994337
> Reviewed-by: Toon Verwaest <verwaest@chromium.org>
> Commit-Queue: Igor Sheludko <ishell@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#90715}

Bug: v8:13825, chromium:1445925, chromium:1496606
Change-Id: Ic2c08540e6095d21d58c2e6058fe14006cd6ac5e
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5003146
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/main@{#90763}

[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/codegen/x64/macro-assembler-x64.h
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/flags/flag-definitions.h
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/maglev/maglev-assembler.h
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/codegen/arm64/macro-assembler-arm64.h
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/codegen/arm/macro-assembler-arm.h
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/maglev/arm64/maglev-assembler-arm64-inl.h
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/maglev/x64/maglev-assembler-x64-inl.h
[add] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/test/mjsunit/regress/regress-crbug-1496606.js
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/builtins/x64/builtins-x64.cc
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/maglev/maglev-ir.cc
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/builtins/arm64/builtins-arm64.cc
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/builtins/arm/builtins-arm.cc
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/codegen/arm64/macro-assembler-arm64.cc
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/maglev/arm/maglev-assembler-arm-inl.h
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/codegen/x64/macro-assembler-x64.cc
[modify] https://crrev.com/961dd29ccfd1716a88bc8bc236768f7dc828aacc/src/codegen/arm/macro-assembler-arm.cc


### ki...@gmail.com (2023-11-07)

Please mark it as fixed :)

### cl...@chromium.org (2023-11-07)

ClusterFuzz testcase 6301443888185344 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=90762:90763

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### is...@chromium.org (2023-11-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-07)

[Description Changed]

### am...@google.com (2023-11-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-09)

Congratulations Zhenghang Xiao! The Chrome VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2023-11-11)

[Empty comment from Monorail migration]

### is...@google.com (2023-11-11)

This issue was migrated from crbug.com/chromium/1496606?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1496161, crbug.com/chromium/1499743]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075744)*
