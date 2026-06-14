# Security: Debug check failed: start_instr <= end_instr . in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [41493674](https://issues.chromium.org/issues/41493674) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2024-01-23 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91736
    - link: https://crrev.com/4a31b449133e3c1315e46fa7b15529e7fa4ae879 
- Commit Message

```
commit 4a31b449133e3c1315e46fa7b15529e7fa4ae879
Author: Darius Mercadier <dmercadier@chromium.org>
Date:   Tue Jan 9 12:28:32 2024 +0100

    [turboshaft] Use a single operation for Smi->Word32 bitcast
    
    Bug: v8:12783
    Change-Id: I2e0a989fee59442a1edc0f4e881b43d69dbc7438
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5083021
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91736}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux32-debug-v8-component-91943/d8 --allow-natives-syntax --jit-fuzzing --turboshaft-loop-peeling poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/backend/register-allocator.cc, line 2778
# Debug check failed: start_instr <= end_instr (994 vs. 0).
#
#
#
#FailureMessage Object: 0xe11fc190
==== C stack trace ===============================

    /tmp/d8-linux32-debug-v8-component-91943/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1f) [0xf7f5a3ef]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libplatform.so(+0x16724) [0xf7f05724]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xf7) [0xf7f39517]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libbase.so(+0x26f16) [0xf7f38f16]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x31) [0xf7f39561]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::RegisterAllocator::FindOptimalSplitPos(v8::internal::compiler::LifetimePosition, v8::internal::compiler::LifetimePosition)+0x1f9) [0xf6dca2e9]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::RegisterAllocator::SplitBetween(v8::internal::compiler::LiveRange*, v8::internal::compiler::LifetimePosition, v8::internal::compiler::LifetimePosition)+0x78) [0xf6dca5a8]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::LinearScanAllocator::AllocateBlockedReg(v8::internal::compiler::LiveRange*, v8::internal::compiler::RegisterAllocationData::SpillMode)+0x1426) [0xf6dd3d06]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::LinearScanAllocator::ProcessCurrentRange(v8::internal::compiler::LiveRange*, v8::internal::compiler::RegisterAllocationData::SpillMode)+0x10b) [0xf6dd0f6b]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::LinearScanAllocator::AllocateRegisters()+0xea8) [0xf6dcf0e8]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::AllocateGeneralRegistersPhase<v8::internal::compiler::LinearScanAllocator>::Run(v8::internal::compiler::PipelineData*, v8::internal::Zone*)+0x59) [0xf715dfd9]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::AllocateGeneralRegistersPhase<v8::internal::compiler::LinearScanAllocator>>()+0x8a) [0xf715153a]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::PipelineImpl::AllocateRegisters(v8::internal::RegisterConfiguration const*, v8::internal::compiler::CallDescriptor*, bool)+0x2df) [0xf714f07f]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::PipelineImpl::AllocateRegisters(v8::internal::compiler::CallDescriptor*, bool)+0x98) [0xf714de58]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::PipelineImpl::SelectInstructions(v8::internal::compiler::Linkage*)+0xc35) [0xf7143515]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::PipelineImpl::OptimizeGraph(v8::internal::compiler::Linkage*)+0xf20) [0xf713aa80]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0xcb) [0xf71396db]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x86) [0xf56da856]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::OptimizingCompileDispatcher::CompileNext(v8::internal::TurbofanCompilationJob*, v8::internal::LocalIsolate*)+0x36) [0xf5792836]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::OptimizingCompileDispatcher::CompileTask::Run(v8::JobDelegate*)+0x285) [0xf5794a55]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xcb) [0xf7f0436b]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x9f) [0xf7f06aff]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libbase.so(+0x4700e) [0xf7f5900e]
    /lib/i386-linux-gnu/libc.so.6(+0x86c01) [0xf2c86c01]
    /lib/i386-linux-gnu/libc.so.6(+0x12353c) [0xf2d2353c]

```

## Other
Please note to include the flags `--allow-natives-syntax --jit-fuzzing --turboshaft-loop-peeling` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.2.0 - 12.3.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux32-debug/d8-linux32-debug-v8-component-91943.zip
2. Run: `d8 --allow-natives-syntax --jit-fuzzing --turboshaft-loop-peeling poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 920 B)
- [poc.js](attachments/poc_53087948.js) (text/plain, 920 B)

## Timeline

### ki...@gmail.com (2024-01-23)

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91736
    - link: https://crrev.com/4a31b449133e3c1315e46fa7b15529e7fa4ae879 
- Commit Message

```
commit 4a31b449133e3c1315e46fa7b15529e7fa4ae879
Author: Darius Mercadier <dmercadier@chromium.org>
Date:   Tue Jan 9 12:28:32 2024 +0100

    [turboshaft] Use a single operation for Smi->Word32 bitcast
    
    Bug: v8:12783
    Change-Id: I2e0a989fee59442a1edc0f4e881b43d69dbc7438
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5083021
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91736}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux32-debug-v8-component-91943/d8 --allow-natives-syntax --jit-fuzzing --turboshaft-loop-peeling poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/compiler/backend/register-allocator.cc, line 2778
# Debug check failed: start_instr <= end_instr (994 vs. 0).
#
#
#
#FailureMessage Object: 0xe11fc190
==== C stack trace ===============================

    /tmp/d8-linux32-debug-v8-component-91943/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1f) [0xf7f5a3ef]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libplatform.so(+0x16724) [0xf7f05724]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xf7) [0xf7f39517]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libbase.so(+0x26f16) [0xf7f38f16]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x31) [0xf7f39561]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::RegisterAllocator::FindOptimalSplitPos(v8::internal::compiler::LifetimePosition, v8::internal::compiler::LifetimePosition)+0x1f9) [0xf6dca2e9]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::RegisterAllocator::SplitBetween(v8::internal::compiler::LiveRange*, v8::internal::compiler::LifetimePosition, v8::internal::compiler::LifetimePosition)+0x78) [0xf6dca5a8]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::LinearScanAllocator::AllocateBlockedReg(v8::internal::compiler::LiveRange*, v8::internal::compiler::RegisterAllocationData::SpillMode)+0x1426) [0xf6dd3d06]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::LinearScanAllocator::ProcessCurrentRange(v8::internal::compiler::LiveRange*, v8::internal::compiler::RegisterAllocationData::SpillMode)+0x10b) [0xf6dd0f6b]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::LinearScanAllocator::AllocateRegisters()+0xea8) [0xf6dcf0e8]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::AllocateGeneralRegistersPhase<v8::internal::compiler::LinearScanAllocator>::Run(v8::internal::compiler::PipelineData*, v8::internal::Zone*)+0x59) [0xf715dfd9]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::AllocateGeneralRegistersPhase<v8::internal::compiler::LinearScanAllocator>>()+0x8a) [0xf715153a]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::PipelineImpl::AllocateRegisters(v8::internal::RegisterConfiguration const*, v8::internal::compiler::CallDescriptor*, bool)+0x2df) [0xf714f07f]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::PipelineImpl::AllocateRegisters(v8::internal::compiler::CallDescriptor*, bool)+0x98) [0xf714de58]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::PipelineImpl::SelectInstructions(v8::internal::compiler::Linkage*)+0xc35) [0xf7143515]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::PipelineImpl::OptimizeGraph(v8::internal::compiler::Linkage*)+0xf20) [0xf713aa80]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0xcb) [0xf71396db]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x86) [0xf56da856]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::OptimizingCompileDispatcher::CompileNext(v8::internal::TurbofanCompilationJob*, v8::internal::LocalIsolate*)+0x36) [0xf5792836]
    /tmp/d8-linux32-debug-v8-component-91943/libv8.so(v8::internal::OptimizingCompileDispatcher::CompileTask::Run(v8::JobDelegate*)+0x285) [0xf5794a55]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xcb) [0xf7f0436b]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x9f) [0xf7f06aff]
    /tmp/d8-linux32-debug-v8-component-91943/libv8_libbase.so(+0x4700e) [0xf7f5900e]
    /lib/i386-linux-gnu/libc.so.6(+0x86c01) [0xf2c86c01]
    /lib/i386-linux-gnu/libc.so.6(+0x12353c) [0xf2d2353c]

```

## Other
Please note to include the flags `--allow-natives-syntax --jit-fuzzing --turboshaft-loop-peeling` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.2.0 - 12.3.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux32-debug/d8-linux32-debug-v8-component-91943.zip
2. Run: `d8 --allow-natives-syntax --jit-fuzzing --turboshaft-loop-peeling poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)    


### [Deleted User] (2024-01-23)

[Empty comment from Monorail migration]

### ki...@gmail.com (2024-01-23)

[Empty comment from Monorail migration]

### sa...@google.com (2024-01-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### cl...@chromium.org (2024-01-23)

Detailed Report: https://clusterfuzz.com/testcase?key=5479764283817984

Fuzzer: None
Job Type: linux32_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  start_instr <= end_instr in register-allocator.cc
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux32_asan_d8_dbg&revision=91943

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5479764283817984

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ke...@chromium.org (2024-01-23)

Setting to Severity-High based on the nature of the DCHECK. It can be lowered if there is a reason it wouldn't result in memory corruption.

### [Deleted User] (2024-01-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-23)

[Description Changed]

### [Deleted User] (2024-01-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### ad...@google.com (2024-01-25)

(I am a bot: this is an auto-cc on a security bug)

### am...@chromium.org (2024-01-25)

[Empty comment from Monorail migration]

### ki...@gmail.com (2024-01-26)

Hello, any update?

### gi...@appspot.gserviceaccount.com (2024-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/a5e22070afecdb18db45872ef0eb93947085576d

commit a5e22070afecdb18db45872ef0eb93947085576d
Author: Darius Mercadier <dmercadier@chromium.org>
Date: Thu Jan 25 09:59:03 2024

[turboshaft] Avoid putting FrameState constant bitcast input in register

When constants should be used as Smi as FrameState input, we used to
convert Int32Constant to tagged by using a BitcastWordToTagged, but a
recent CL (https://crrev.com/c/5083021) made that more precise,
generating a BitcastWordToTaggedSigned instead.

When the Instruction Selector visits a BitcastWordToTagged, it emits a
Nop with a DefineSameAsFirst (which seems to be some kind of
GapMove). However, when it visits BitcastWordToTaggedSmi, it doesn't
emit anything and just does a renaming.

For a reason that's not clear to me, the register allocator does not
want to spill registers holding constants that come from renamings,
but is happy to spill registers holding constants coming from
GapMoves.

This lead to the register allocator running out of registers when
allocating registers for FrameState inputs, because it was using one
register per integer constant input and didn't want to spill any of
them.

This CL fixes the issue by adding a special case when generating frame
states in the Instruction Selector: BitcastWordToTaggedSigned with
Word32 constant inputs now lead to using a Constant rather than using
the BitcastWordToTaggedSigned itself.

Bug: v8:12783
Change-Id: Ic3be55ba2c386bd0254c241ac166e97269f39cd8
Fixed: chromium:1520697
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5233669
Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#92020}

[modify] https://crrev.com/a5e22070afecdb18db45872ef0eb93947085576d/src/compiler/turboshaft/operations.h
[modify] https://crrev.com/a5e22070afecdb18db45872ef0eb93947085576d/src/compiler/turboshaft/opmasks.h
[modify] https://crrev.com/a5e22070afecdb18db45872ef0eb93947085576d/src/compiler/backend/instruction-selector.cc
[add] https://crrev.com/a5e22070afecdb18db45872ef0eb93947085576d/test/mjsunit/compiler/regress-crbug-1520697.js


### [Deleted User] (2024-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-27)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M122, which branched on 2024-01-22 (Chromium branch: 6261, Chromium branch position: 1250580)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2024-01-29)

I'm requesting that the CL from https://crbug.com/chromium/1520697#c16 be merged to 122 (since it fixes a security issue that was introduced in 122).

### [Deleted User] (2024-01-29)

Merge review required: M122 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2024-01-29)

Replies to https://crbug.com/chromium/1520697#c21:

1. The CL fixes a security issue.
2. https://crrev.com/c/5233669
3. yes, it landed 3 days ago on canary
4. no
5. 
6. no

### pb...@google.com (2024-01-30)

Approving the merge to M122 Branch, please goahead and get the CL merged asap. For branch info please refer go/chromebranches

### gi...@appspot.gserviceaccount.com (2024-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/86c99d863f9402e896362237669a40b1f07d2a82

commit 86c99d863f9402e896362237669a40b1f07d2a82
Author: Darius Mercadier <dmercadier@chromium.org>
Date: Thu Jan 25 09:59:03 2024

Merged: [turboshaft] Avoid putting FrameState constant bitcast input in register

When constants should be used as Smi as FrameState input, we used to
convert Int32Constant to tagged by using a BitcastWordToTagged, but a
recent CL (https://crrev.com/c/5083021) made that more precise,
generating a BitcastWordToTaggedSigned instead.

When the Instruction Selector visits a BitcastWordToTagged, it emits a
Nop with a DefineSameAsFirst (which seems to be some kind of
GapMove). However, when it visits BitcastWordToTaggedSmi, it doesn't
emit anything and just does a renaming.

For a reason that's not clear to me, the register allocator does not
want to spill registers holding constants that come from renamings,
but is happy to spill registers holding constants coming from
GapMoves.

This lead to the register allocator running out of registers when
allocating registers for FrameState inputs, because it was using one
register per integer constant input and didn't want to spill any of
them.

This CL fixes the issue by adding a special case when generating frame
states in the Instruction Selector: BitcastWordToTaggedSigned with
Word32 constant inputs now lead to using a Constant rather than using
the BitcastWordToTaggedSigned itself.

Bug: v8:12783, chromium:1520697
(cherry picked from commit a5e22070afecdb18db45872ef0eb93947085576d)

Change-Id: I5da8a10bc9ffd95511f2237488178fe8066ba65a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5250114
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/branch-heads/12.2@{#22}
Cr-Branched-From: 6eb5a9616aa6f8c705217aeb7c7ab8c037a2f676-refs/heads/12.2.281@{#1}
Cr-Branched-From: 44cf56d850167c6988522f8981730462abc04bcc-refs/heads/main@{#91934}

[modify] https://crrev.com/86c99d863f9402e896362237669a40b1f07d2a82/src/compiler/turboshaft/opmasks.h
[modify] https://crrev.com/86c99d863f9402e896362237669a40b1f07d2a82/src/compiler/turboshaft/operations.h
[modify] https://crrev.com/86c99d863f9402e896362237669a40b1f07d2a82/src/compiler/backend/instruction-selector.cc
[add] https://crrev.com/86c99d863f9402e896362237669a40b1f07d2a82/test/mjsunit/compiler/regress-crbug-1520697.js


### [Deleted User] (2024-02-01)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2024-02-01)

Re https://crbug.com/chromium/1520697#c25: the issue was introduced in M122, so there is no need to backmerge to M120.

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations on another one, Kipreyyy! The Chrome VRP Panel has decided to award you $7,000 for this report of memory corruption in the renderer / sandboxed process + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### [Deleted User] (2024-02-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### dm...@chromium.org (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1520697?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### vo...@google.com (2024-02-07)

Introduced in M122, so marking the bug as not applicable to M114 and M120 LTS.

### pe...@google.com (2024-05-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493674)*
