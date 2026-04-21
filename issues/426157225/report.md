# Debug check failed: predecessors_so_far_ < predecessor_count_ (2 vs. 2). in v8 [426157225] - Chromium

| Field | Value |
|-------|-------|
| **Issue ID** | [426157225](https://issues.chromium.org/issues/426157225) |
| **Status** | Unknown |
| **Severity** | Unknown |
| **Priority** | Unknown |
| **Component** | Unknown |
| **Reporter** | Unknown |
| **Bounty** | Confirmed (amount unknown) |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 100753
    - link: https://crrev.com/1af713dbe9344e057c55ee3a45d2f3045cf36f67
- Commit Message

```
commit 1af713dbe9344e057c55ee3a45d2f3045cf36f67
Author: Marja Hölttä <marja@chromium.org>
Date:   Tue Jun 10 14:21:22 2025 +0200

    [maglev] Support (inlining) polymorphic calls
    
    Bug:411351177
    
    Change-Id: I086f47cb03214afec404c6d56cc9e2e364526e53
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6607688
    Commit-Queue: Marja Hölttä <marja@chromium.org>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Reviewed-by: Victor Gomes <victorgomes@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#100753}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-100914/d8 --allow-natives-syntax --maglev-poly-calls --turbolev poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/maglev/maglev-interpreter-frame-state.cc, line 738
# Debug check failed: predecessors_so_far_ < predecessor_count_ (2 vs. 2).
#
#
#
#FailureMessage Object: 0x7ffd026d4bd0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-100914/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f58f024d943]
    /tmp/d8-linux-debug-v8-component-100914/libv8_libplatform.so(+0x1bb1d) [0x7f58f01f4b1d]
    /tmp/d8-linux-debug-v8-component-100914/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7f58f022f244]
    /tmp/d8-linux-debug-v8-component-100914/libv8_libbase.so(+0x2cc05) [0x7f58f022ec05]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(v8::internal::maglev::MergePointInterpreterFrameState::Merge(v8::internal::maglev::MaglevGraphBuilder*, v8::internal::maglev::MaglevCompilationUnit&, v8::internal::maglev::InterpreterFrameState&, v8::internal::maglev::BasicBlock*)+0x240) [0x7f58edec4fe0]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode()+0x11c4) [0x7f58edc14df4]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildBody()+0x1c4) [0x7f58edc0f804]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(v8::internal::maglev::MaglevGraphBuilder::Build()+0x3b3) [0x7f58edc0b493]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(v8::internal::compiler::turboshaft::TurbolevGraphBuildingPhase::Run(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::Zone*, v8::internal::compiler::Linkage*)+0x4ad) [0x7f58ef505e7d]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(auto v8::internal::compiler::turboshaft::Pipeline::Run<v8::internal::compiler::turboshaft::TurbolevGraphBuildingPhase, v8::internal::compiler::Linkage*&>(v8::internal::compiler::Linkage*&)+0xf5) [0x7f58eec49045]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(v8::internal::compiler::turboshaft::Pipeline::CreateGraphWithMaglev(v8::internal::compiler::Linkage*)+0xbb) [0x7f58eec35bcb]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x1d7) [0x7f58eec35997]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x92) [0x7f58ec83bac2]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(+0x346bbe6) [0x7f58ec86bbe6]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(+0x3451fd4) [0x7f58ec851fd4]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0x3fa) [0x7f58ec8544ba]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(+0x4470385) [0x7f58ed870385]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(+0x4467bbd) [0x7f58ed867bbd]
    /tmp/d8-linux-debug-v8-component-100914/libv8.so(v8::internal::Runtime_OptimizeTurbofanEager(int, unsigned long*, v8::internal::Isolate*)+0xa0) [0x7f58ed867700]
    [0x7f586f4e84fd]

```

## Other
Please note to include the flags `--allow-natives-syntax --maglev-poly-calls --turbolev` for clusterfuzz classification.

VERSION
Tested on v8 version: 13.9.0 - 13.9.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-100914.zip
2. Run: `d8 --allow-natives-syntax --maglev-poly-calls --turbolev poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy) and Nan Wang (@eternalsakura13)

## Attachments

- unknown (, 0 B)
- unknown (, 0 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-06-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4886114443657216.

### cl...@appspot.gserviceaccount.com (2025-06-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6602206476173312.

### am...@chromium.org (2025-06-20)

Hi Sakura and Kipreyyy, thanks for this report.

Was able to reproduce this easily. Adding SI-None hotlist as
--turbolev is not yet shipping

### am...@chromium.org (2025-06-20)

I'm not sure if turbolev issues should be assigned to turbo\* components or maglev, so just putting it in the upper level Compiler component.

### 24...@project.gserviceaccount.com (2025-06-20)

Detailed Report: https://clusterfuzz.com/testcase?key=6602206476173312

Fuzzer: None
Job Type: linux_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  predecessors_so_far_ < predecessor_count_ in maglev-interpreter-frame-state.cc
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=100752:100753

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6602206476173312

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2025-06-20)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-06-20)

Detailed Report: https://clusterfuzz.com/testcase?key=4886114443657216

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  predecessors_so_far_ < predecessor_count_ in maglev-interpreter-frame-state.cc
  v8::internal::maglev::MergePointInterpreterFrameState::Merge
  v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=100752:100753

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4886114443657216

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ma...@chromium.org (2025-06-23)

Thanks for the report! --maglev-poly-calls is not enabled by default so this doesn't have any security implications currently.

### ma...@chromium.org (2025-06-23)

This issue is not specific to Turbolev, it also reproes without --turbolev, when optimizing to Maglev instead of Turbofan.

### ki...@gmail.com (2025-06-23)

Re #c9: Hi, this vulnerability should still be considered high-risk because this flag is not marked as experimental,and it should be security\_impact\_none, so please change it back to S1.

### ma...@chromium.org (2025-06-23)

Hmm, let me check with security folks about that again. S3 definition says "Low severity (S3) vulnerabilities are usually bugs that would normally be a higher severity, but which have extreme mitigating factors or highly limited scope." and the flag not being on could be considered an extreme mitigating factor.

### ki...@gmail.com (2025-06-23)

Hi, please ask the security team or the Chrome VRP personnel to determine this matter, because in v8 flag is not considered a mitigating factor (unless it is marked as experimental).

### ma...@chromium.org (2025-06-23)

Re-checked the V8 specific guidelines, looks like S1 is appropriate. However, the offending CL landed 10 days before this report, so, that might lower the changes for VRP.

### ki...@gmail.com (2025-06-26)

hello, any update?

### dx...@google.com (2025-06-26)

Project: v8/v8  
Branch: main  
Author: Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  
Link:      <https://chromium-review.googlesource.com/6658623>

[maglev] Fix merge states in polymorphic calls

---


Expand for full commit details

```
    We were fixing the predecessor count (if a continuation was dead) but we 
    might already have created a MergePointInterpreterFrameState with the 
    wrong predecessor count. 
     
    This CL simplifies dead bytecode detection so that it's not done inside 
    VisitSingleBytecode but outside. This way callers can choose to not 
    detect and handle dead bytecodes, which is the right thing to do when 
    only one polymorphic branch is dead. 
     
    Fixed: 426157225 
    Bug: 411351177 
    Change-Id: I45a785d4441c6216b176e964a5c1eaea305e5968 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6658623 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101061}
```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-graph-builder.h`
- A `test/mjsunit/maglev/regress-426157225.js`

---

Hash: ba86071fd69b93006c92df00d39752157ae1b503  
Date:  Thu Jun 26 12:20:08 2025



---

### ma...@chromium.org (2025-06-26)

I'm assuming the security team will tune in now that this is fixed (pls see comment 14).

### am...@chromium.org (2025-06-26)

I'm unsure of what update is needed from the security team at this time. 
If this is related to VRP,  this bug was just resolved earlier today, so it has not been tagged with the daily automation to put this into the VRP panel queue.

If the question is more general -- if the bug was introduced only 10 days prior to when it was discovered is eligible for a VRP reward would ordinarily be an issue for discussion at VRP panel. I do, however, see that clusterfuzz did discover and report this issue (issue 426648846) within 24 hours of this one, which would result in this report not being eligible for a VRP reward.

### 24...@project.gserviceaccount.com (2025-06-27)

ClusterFuzz testcase 4794265762725888 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=101060:101061

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### am...@chromium.org (2025-06-30)

Thank you for the report, Kipreyyy and Sakura. Since this report collided with a duplicate from Clusterfuzz in less thank a day, this report is unfortunately not eligible for a Chrome VRP reward.

### ch...@google.com (2025-10-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/426157225)*
