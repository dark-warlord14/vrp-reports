# Security: Debug check failed: is_loadable(). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [325678240](https://issues.chromium.org/issues/325678240) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2024-02-17 |
| **Bounty** | $8,000.00 |

## Description

## VULNERABILITY DETAILS

### INTRODUCE

After bisect, it was determined that following commit caused this problem.

- Commit Info
  - Version: 90861
  - link: <https://crrev.com/7b59899e869fd1520ca45c6eb9f418402ec9ce59>
- Commit Message

```
commit 7b59899e869fd1520ca45c6eb9f418402ec9ce59
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Fri Nov 10 11:15:12 2023 +0100

    [maglev] Hoist some phi input untagging out of loops

    Implement the ability to hoist untagging operations for untagged loop
    phis out of the loop.

    If we can hoist the untagging we ignore the input edge in
    representation inference, since it should always be cheaper to untag
    before the loop.

    For now the optimization is only enabled for OSR values. The reason is
    that in normal code we could have a deopt loop if we can't learn when
    the speculative untagging failed.

    To be able to insert checked untaggings we create a use a new
    checkpointed jump instruction that has a deopt frame attached.

    Bug: v8:7700
    Change-Id: Ic3f3b0809374ffad412ef9028bb047dd6cd57ad0
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5008116
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    Commit-Queue: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#90861}


```
### CRASH LOG

- Debug output

```
# CMD: /tmp/d8-linux-debug-v8-component-92381/d8 --allow-natives-syntax --maglev-hoist-osr-value-phi-untagging poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/maglev/maglev-ir.h, line 2292
# Debug check failed: is_loadable().
#
#
#
#FailureMessage Object: 0x7ffc187750b0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-92381/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7ff1a5a6c873]
    /tmp/d8-linux-debug-v8-component-92381/libv8_libplatform.so(+0x18cdd) [0x7ff1a5a15cdd]
    /tmp/d8-linux-debug-v8-component-92381/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x17e) [0x7ff1a5a4db9e]
    /tmp/d8-linux-debug-v8-component-92381/libv8_libbase.so(+0x2b5e5) [0x7ff1a5a4d5e5]
    /tmp/d8-linux-debug-v8-component-92381/libv8.so(v8::internal::maglev::ValueNode::allocation() const+0x113) [0x7ff1a3fa2e13]
    /tmp/d8-linux-debug-v8-component-92381/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::InitializeBranchTargetPhis(int, v8::internal::maglev::BasicBlock*)+0x123) [0x7ff1a4340fe3]
    /tmp/d8-linux-debug-v8-component-92381/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::AllocateControlNode(v8::internal::maglev::ControlNode*, v8::internal::maglev::BasicBlock*)+0x1a8) [0x7ff1a433bc08]
    /tmp/d8-linux-debug-v8-component-92381/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::AllocateRegisters()+0x4ef) [0x7ff1a4335f0f]
    /tmp/d8-linux-debug-v8-component-92381/libv8.so(v8::internal::maglev::StraightForwardRegisterAllocator::StraightForwardRegisterAllocator(v8::internal::maglev::MaglevCompilationInfo*, v8::internal::maglev::Graph*)+0x83) [0x7ff1a43350a3]
    /tmp/d8-linux-debug-v8-component-92381/libv8.so(v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*)+0x117d) [0x7ff1a4050f7d]
    /tmp/d8-linux-debug-v8-component-92381/libv8.so(v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x6a) [0x7ff1a4111e0a]
    /tmp/d8-linux-debug-v8-component-92381/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x8d) [0x7ff1a3055c4d]
    /tmp/d8-linux-debug-v8-component-92381/libv8.so(v8::internal::maglev::MaglevConcurrentDispatcher::JobTask::Run(v8::JobDelegate*)+0x39b) [0x7ff1a4113b7b]
    /tmp/d8-linux-debug-v8-component-92381/libv8_libplatform.so(v8::platform::DefaultJobState::Join()+0x1ad) [0x7ff1a5a132bd]
    /tmp/d8-linux-debug-v8-component-92381/libv8_libplatform.so(v8::platform::DefaultJobHandle::Join()+0x13) [0x7ff1a5a138b3]
    /tmp/d8-linux-debug-v8-component-92381/libv8.so(+0x37141bc) [0x7ff1a41141bc]
    /tmp/d8-linux-debug-v8-component-92381/libv8.so(+0x3e8da3b) [0x7ff1a488da3b]


```
### Other

1. Please note to include the flags `--allow-natives-syntax --maglev-hoist-osr-value-phi-untagging` for clusterfuzz classification.
2. Please consider this report as HIGH-Severity since our another report, [issue 41494611](https://issues.chromium.org/issues/41494611), triggered the same DCHECK and also considered as HIGH-Severity.

## VERSION

Tested on v8 version: 12.1.0 - 12.3.0

## REPRODUCTION CASE

1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-92381.zip
2. Run: `d8 --allow-natives-syntax --maglev-hoist-osr-value-phi-untagging poc.js`

## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: tab

## CREDIT INFORMATION

Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 458 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-02-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5151444478394368.

### dr...@chromium.org (2024-02-19)

Uploaded to <https://clusterfuzz.com/testcase-detail/5151444478394368> (in case ClusterFuzz struggles to update when its done)

### ki...@gmail.com (2024-02-19)

Please use Linux debug version d8 to run clusterfuzzer

### dr...@chromium.org (2024-02-20)

That's a good point, thanks, let me pass it to a debug build.

### cl...@appspot.gserviceaccount.com (2024-02-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6210246157991936.

### 24...@project.gserviceaccount.com (2024-02-20)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-02-20)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/7b59899e869fd1520ca45c6eb9f418402ec9ce59 ([maglev] Hoist some phi input untagging out of loops).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2024-02-20)

Detailed Report: https://clusterfuzz.com/testcase?key=6210246157991936

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  is_loadable() in maglev-ir.h
  v8::internal::maglev::ValueNode::allocation
  v8::internal::maglev::StraightForwardRegisterAllocator::InitializeBranchTargetPh
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=90860:90861

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6210246157991936

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ol...@chromium.org (2024-02-20)

Thanks a lot for the nicely bisected and clean poc. Much appreciated.

Removing found in, because this flag is currently disabled in all stable releases and in 123.

Removing security flags, because this bug clobbers an i32 or f64 register and not a tagged one. Thus it is only a correctness issue as we won't treat the value as a pointer.

### ki...@gmail.com (2024-02-20)

Hi, i want to know whether this will cause typer issue? If true, this maybe a security issue :) thanks

### ol...@chromium.org (2024-02-20)

Hi, the typer is in turbofan (4th tier). This bug is in maglev (3rd). It's not a type confusion. We just don't manage to re-load a value after an exception handler ran. But the value itself is treated either as int or double value. So worst case we just have a wrong value there.

### ki...@gmail.com (2024-02-20)

Thanks for your reply :)

### ap...@google.com (2024-02-20)

Project: v8/v8
Branch: main

commit d771d0d479be93a6a9e815c36dd1c27dd1b9c1e4
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Tue Feb 20 16:18:28 2024

    [maglev] Prevent hoisting phi untaggings over exception handlers
    
    Hoisting across exception handler merges would require us to add more
    exception phis.
    
    Drive-By: Add hole check when the new representation is non holey.
    
    Fixed: chromium:325678240
    Change-Id: I76dba06c442336ce28bc469cfab1cdd03c42e96a
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5197678
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    Commit-Queue: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92431}

M       src/maglev/maglev-phi-representation-selector.cc
M       src/maglev/maglev-phi-representation-selector.h
A       test/mjsunit/regress/regress-crbug-325678240.js

https://chromium-review.googlesource.com/5197678


### ap...@google.com (2024-02-21)

Project: v8/v8
Branch: main

commit c692fab817aaa0c572e9e26c9c7b67ccb705d5d6
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Wed Feb 21 16:21:18 2024

    [maglev] Fix to prevent phi untagging for resumable (non-)loops
    
    This reverts the misguided attempt at fixing the issue in
    `regress-crbug-325678240.js` attempted in
    https://crrev.com/c/5197678. The actual problem were not
    exception handlers at all.
    
    The issue is that when osr is attempted inside of a resumable loop,
    then this loop might not be a loop at all (if the back-edge
    unconditionally deopts). Therefore we have a block where
    `block->is_loop()` is false, however
    `block->state()->is_resumable_loop()` is true. The solution is to block
    hoisting on the latter predicate alone.
    
    Fixed: chromium:325678240
    Change-Id: I52aaa2c19f5daaa3af273cd6651474db45660042
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5310170
    Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92455}

M       src/maglev/maglev-phi-representation-selector.cc

https://chromium-review.googlesource.com/5310170


### 24...@project.gserviceaccount.com (2024-02-22)

Detailed Report: https://clusterfuzz.com/testcase?key=6210246157991936

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  is_loadable() in maglev-ir.h
  v8::internal::maglev::ValueNode::allocation
  v8::internal::maglev::StraightForwardRegisterAllocator::InitializeBranchTargetPh
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=90860:90861
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=92430:92431

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6210246157991936

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### am...@chromium.org (2024-02-23)

Thank you for the report, Kipreyy. As conveyed in c#12, this does not appear to be an exploitable security issue, therefore, this report is unfortunately not eligible for a Chrome VRP reward.

### pe...@google.com (2024-05-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/325678240)*
