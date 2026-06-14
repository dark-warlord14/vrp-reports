# Security: Debug check failed: is_loadable(). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [41494611](https://issues.chromium.org/issues/41494611) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2024-01-25 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91912
    - link: https://crrev.com/16f9aac2b8b4fd89768519b130afff47728b9136 
- Commit Message

```
commit 16f9aac2b8b4fd89768519b130afff47728b9136
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Thu Jan 18 17:18:26 2024 +0100

    [maglev] CSE
    
    A GVN style (but greedy) common subexpression elimination.
    
    Every value node has a hash called `value_number` constructed from a
    "seed" value for immediate arguments, the opcode and every input
    value node. Expressions with the same value number are candidates for
    de-duplication. Candidates are verified by checking the opcode and
    every input for equality. If this check succeeds the instruction must
    be identical as long as we ensure there are no collisions in the
    "seed" value.
    
    Instructions marked allocating or reading also participate in CSE.
    Most allocating instructions do not create something uniquely
    identifiable, those that did were marked `not_idempotent`.
    Instructions marked reading are only available for elimination within
    an `effect_epoch`. Epochs increment with writes.
    
    Bug: v8:7700
    Change-Id: Ic6bfd65bb8141185866ff2a7b099415fa41c9e80
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4765634
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91912}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91994/d8 --allow-natives-syntax --optimize-on-next-call-optimizes-to-maglev --maglev-cse poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/maglev/maglev-ir.h, line 2266
# Debug check failed: is_loadable().
#
#
#
#FailureMessage Object: 0x7ffc5e6e4300
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-91994/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f1c479e0a83]
    /tmp/d8-linux-debug-v8-component-91994/libv8_libplatform.so(+0x18e5d) [0x7f1c42bf3e5d]
    /tmp/d8-linux-debug-v8-component-91994/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x17e) [0x7f1c479c1c4e]
    /tmp/d8-linux-debug-v8-component-91994/libv8_libbase.so(+0x2b695) [0x7f1c479c1695]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(v8::internal::maglev::ValueNode::allocation() const+0x113) [0x7f1c46127033]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::AssignFixedInput(v8::internal::maglev::Input&)+0x34) [0x7f1c464ade84]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::AssignInputs(v8::internal::maglev::NodeBase*)+0x5b) [0x7f1c464a84db]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::AllocateNode(v8::internal::maglev::Node*)+0xa9) [0x7f1c464a51b9]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::AllocateRegisters()+0x153b) [0x7f1c464a117b]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::StraightForwardRegisterAllocator(v8::internal::maglev::MaglevCompilationInfo*, v8::internal::maglev::Graph*)+0x83) [0x7f1c4649f2c3]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*)+0x117d) [0x7f1c461d22cd]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x6a) [0x7f1c4628ec3a]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x8d) [0x7f1c4521277d]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(+0x2638518) [0x7f1c45238518]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(+0x26242d8) [0x7f1c452242d8]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0xbd) [0x7f1c45225fdd]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(+0x3369ffe) [0x7f1c45f69ffe]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(v8::internal::Runtime_CompileOptimized(int, unsigned long*, v8::internal::Isolate*)+0x92) [0x7f1c45f699f2]
    /tmp/d8-linux-debug-v8-component-91994/libv8.so(+0x1b986bd) [0x7f1c447986bd]

```

## Other
Please note to include the flags `--allow-natives-syntax --optimize-on-next-call-optimizes-to-maglev --maglev-cse` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.2.0 - 12.3.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91994.zip
2. Run: `d8 --allow-natives-syntax --optimize-on-next-call-optimizes-to-maglev --maglev-cse poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 383 B)

## Timeline

### ki...@gmail.com (2024-01-25)

[Comment Deleted]

### [Deleted User] (2024-01-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5084152094720000.

### li...@chromium.org (2024-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-25)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2024-01-25)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### am...@chromium.org (2024-01-25)

[Description Changed]

### ad...@google.com (2024-01-25)

(I am a bot: this is an auto-cc on a security bug)

### am...@chromium.org (2024-01-25)

[Empty comment from Monorail migration]

### ki...@gmail.com (2024-01-26)

Please use Linux d8 debug version to reproduce.

### ki...@gmail.com (2024-01-26)

[Comment Deleted]

### ki...@gmail.com (2024-01-26)

I noticed that Cluster Fuzz is unable to reproduce the POC. However, I can still reproduce it with same flags in latest linux debug build:

$ /tmp/d8-linux-debug-v8-component-92019/d8  --fuzzing --fuzzing --expose-gc --allow-natives-syntax --debug-code --harmony --disable-abortjs --omit-quit --disable-in-process-stack-traces --invoke-weak-callbacks --enable-slow-asserts --verify-heap --allow-natives-syntax --optimize-on-next-call-optimizes-to-maglev --maglev-cse output_poc.js


#
# Fatal error in ../../src/maglev/maglev-ir.h, line 2274
# Debug check failed: is_loadable().
#
#
#
#FailureMessage Object: 0x7ffda6706f30
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-92019/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fca61caea93]
    /tmp/d8-linux-debug-v8-component-92019/libv8_libplatform.so(+0x18e5d) [0x7fca61c57e5d]
    /tmp/d8-linux-debug-v8-component-92019/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x17e) [0x7fca61c8fc5e]
    /tmp/d8-linux-debug-v8-component-92019/libv8_libbase.so(+0x2b6a5) [0x7fca61c8f6a5]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(v8::internal::maglev::ValueNode::allocation() const+0x113) [0x7fca60333423]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::AssignFixedInput(v8::internal::maglev::Input&)+0x34) [0x7fca606cc614]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::AssignInputs(v8::internal::maglev::NodeBase*)+0x5b) [0x7fca606c6abb]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::AllocateNode(v8::internal::maglev::Node*)+0xaa) [0x7fca606c377a]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::AllocateRegisters()+0x156b) [0x7fca606bf74b]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::StraightForwardRegisterAllocator(v8::internal::maglev::MaglevCompilationInfo*, v8::internal::maglev::Graph*)+0x83) [0x7fca606bd863]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*)+0x117d) [0x7fca603de84d]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x6a) [0x7fca6049cf9a]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x8d) [0x7fca5f41d57d]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(+0x26432e2) [0x7fca5f4432e2]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(+0x262f0f8) [0x7fca5f42f0f8]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0xbd) [0x7fca5f430dfd]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(+0x3376a1e) [0x7fca60176a1e]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(v8::internal::Runtime_CompileOptimized(int, unsigned long*, v8::internal::Isolate*)+0x90) [0x7fca60176410]
    /tmp/d8-linux-debug-v8-component-92019/libv8.so(+0x1b9e6bd) [0x7fca5e99e6bd]
[2]    1374439 IOT instruction  /tmp/d8-linux-debug-v8-component-92019/d8 --fuzzing --fuzzing --expose-gc

### ha...@google.com (2024-01-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-26)

Detailed Report: https://clusterfuzz.com/testcase?key=5451357986684928

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  is_loadable() in maglev-ir.h
  v8::internal::maglev::ValueNode::allocation
  v8::internal::maglev::StraightForwardRegisterAllocator::AssignFixedInput
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=91912

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5451357986684928

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2024-01-26)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Compiler>Maglev]

### dm...@chromium.org (2024-01-26)

@Olivf: you'll have to update the security impact; I think that it should be None since Maglev CSE isn't shipping yet. And FoundIn should be 122 or 123, I don't recall.

### ki...@gmail.com (2024-01-26)

As far as I know, this vulnerability was introduced a few commits before the 12.3.0 release, so it should probably be foundin-122?

### ol...@chromium.org (2024-01-29)

[Empty comment from Monorail migration]

### ol...@chromium.org (2024-01-29)

Thanks for the report. Maglev cse is not yet enabled.

### ol...@chromium.org (2024-01-29)

[Empty comment from Monorail migration]

### ol...@chromium.org (2024-01-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/2414b1c31a87d40de79acfcd2a3b0c068f27442e

commit 2414b1c31a87d40de79acfcd2a3b0c068f27442e
Author: Olivier Flückiger <olivf@chromium.org>
Date: Tue Jan 30 09:51:02 2024

[maglev] CSE: clear available expressions for exception handlers

Available expressions are not preserved across exceptions.

Fixed: chromium:1521770, chromium:1521643
Change-Id: Ieae7ef9ed685ef2f682083ff3cc279e9e11395cb
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5245405
Commit-Queue: Olivier Flückiger <olivf@chromium.org>
Auto-Submit: Olivier Flückiger <olivf@chromium.org>
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#92081}

[modify] https://crrev.com/2414b1c31a87d40de79acfcd2a3b0c068f27442e/src/maglev/maglev-interpreter-frame-state.h
[modify] https://crrev.com/2414b1c31a87d40de79acfcd2a3b0c068f27442e/src/maglev/maglev-graph-builder.h
[add] https://crrev.com/2414b1c31a87d40de79acfcd2a3b0c068f27442e/test/mjsunit/maglev/regress-cse.js


### [Deleted User] (2024-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-30)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-30)

This issue was migrated from crbug.com/chromium/1521643?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Compiler>Maglev]
[Monorail components added to Component Tags custom field.]

### am...@google.com (2024-02-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-08)

Congratulations Kipreyyy! The Chrome VRP Panel has decided to award you $7,000 for this report of a renderer process memory corruption bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### pe...@google.com (2024-05-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41494611)*
