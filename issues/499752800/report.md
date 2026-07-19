# Debug check failed: i < this ->context_local_count() (0 vs. 0). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [499752800](https://issues.chromium.org/issues/499752800) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 148 |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2026-04-06 |
| **Bounty** | $8,000.00 |

## Description

# Steps to reproduce the problem

Tested on v8 version: 14.8.104
Affected on v8 beta version: 14.8.178.1

1. Build: `python3 tools/dev/gm.py x64.debug`
2. Run: `./d8 --allow-natives-syntax --fuzzing --jit-fuzzing poc.js`

# Problem Description

## VULNERABILITY DETAILS

### Crash Log

```
#
# Fatal error in gen/torque-generated/src/objects/scope-info-tq-inl.inc, line 1562
# Debug check failed: i < this ->context_local_count() (0 vs. 0).
#
#
#
#FailureMessage Object: 0x7ffe90c7afc8
==== C stack trace ===============================

    ./14.8.104/out.gn/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x29) [0x7ae9765b4fb9]
    ./14.8.104/out.gn/x64.debug/libv8_libplatform.so(+0x4e2cd) [0x7ae9765162cd]
    ./14.8.104/out.gn/x64.debug/libv8_libbase.so(v8::base::PrintStackTraceIfAvailable()+0x14) [0x7ae976588094]
    ./14.8.104/out.gn/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x1f9) [0x7ae976588849]
    ./14.8.104/out.gn/x64.debug/libv8_libbase.so(+0x5310c) [0x7ae97658810c]
    ./14.8.104/out.gn/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x4d) [0x7ae97658894d]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::TorqueGeneratedScopeInfo<v8::internal::ScopeInfo, v8::internal::HeapObject>::context_local_infos(int) const+0xc3) [0x7ae9715c1473]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::ScopeInfo::ContextLocalMode(int) const+0x1b) [0x7ae9715b721b]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::compiler::ScopeInfoRef::ContextLocalMode(int) const+0x4a) [0x7ae97315b59a]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::maglev::MaglevGraphBuilder::GetContextMaybeAssigned(v8::internal::compiler::ScopeInfoRef, int, v8::internal::VariableMode*)+0xe8) [0x7ae972040308]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::maglev::MaglevGraphBuilder::StoreAndCacheContextSlot(v8::internal::maglev::ValueNode*, int, v8::internal::maglev::ValueNode*, v8::internal::ContextMode, v8::internal::compiler::ScopeInfoRef)+0x7d) [0x7ae972051a6d]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitStaCurrentContextSlotNoCell()+0x75) [0x7ae972052d75]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode()+0xef9) [0x7ae972065bf9]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildBody()+0x1b3) [0x7ae972071f33]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::maglev::MaglevGraphBuilder::Build()+0x383) [0x7ae9720a9d03]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*)+0x441) [0x7ae971df2b71]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x69) [0x7ae97203ce89]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x12d) [0x7ae9704d7d9d]
    ./14.8.104/out.gn/x64.debug/libv8.so(+0xa2f3667) [0x7ae9704f3667]
    ./14.8.104/out.gn/x64.debug/libv8.so(+0xa2e6088) [0x7ae9704e6088]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0x3a4) [0x7ae9704e4f84]
    ./14.8.104/out.gn/x64.debug/libv8.so(+0xb769069) [0x7ae971969069]
    ./14.8.104/out.gn/x64.debug/libv8.so(+0xb762204) [0x7ae971962204]
    ./14.8.104/out.gn/x64.debug/libv8.so(v8::internal::Runtime_OptimizeMaglevEager(int, unsigned long*, v8::internal::Isolate*)+0x151) [0x7ae971961e51]
    ./14.8.104/out.gn/x64.debug/libv8.so(+0x90148fd) [0x7ae96f2148fd]
Received signal 6
Aborted (core dumped)

```
### Bisect

The bug was instroduced by this commit: 2413eb9b1c59c0afe439d1f1eb92378e1c79e7f6

```
[maglev] Accurately track scope infos

This is necessary to correctly understand the context we're in.

Bug: 495041650
Change-Id: Ia73dc8d0eda5bcba06f928ad206fef70de8a2952
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7693574
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#105998}

```
### Root Cause

```
MaybeAssignedFlag MaglevGraphBuilder::GetContextMaybeAssigned(
    compiler::ScopeInfoRef scope_info, int index, VariableMode* mode) {
  if (index < Context::MIN_CONTEXT_SLOTS) {
    *mode = VariableMode::kConst;
    return kNotAssigned;
  }
...
  if (index == scope_info.ReceiverContextSlotIndex() &&
      IsDerivedConstructor(scope_info.function_kind())) {
    *mode = VariableMode::kConst;
    return kMaybeAssigned;
  }
  int var_index = index - header_length;
  *mode = scope_info.ContextLocalMode(var_index);   // current scope_info has no local
  return scope_info.ContextLocalMaybeAssignedFlag(var_index);
}

```
### Version

Tested on v8 version: 14.8.104
Affected on v8 beta version: 14.8.178.1

### Credit

Reporter credit: sw33t - supported by LLM

# Summary

Debug check failed: i < this ->context\_local\_count() (0 vs. 0). in v8

# Custom Questions

#### Type of crash:

tab

#### Reporter credit:

sw33t

# Additional Data

Category: Security   

Chrome Channel: Beta   

Regression: N/A \

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 301 B)

## Timeline

### dc...@chromium.org (2026-04-07)

triaging provisionally and routing to the v8 team

### ch...@google.com (2026-04-07)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-07)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### cl...@appspot.gserviceaccount.com (2026-04-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5404099952541696.

### is...@chromium.org (2026-04-07)

Thank you for the report!

### is...@chromium.org (2026-04-07)

Looks similar to [issue 498199197](https://issues.chromium.org/issues/498199197), seems to be caused by the [same culprit](https://crrev.com/c/7693574) but still reproduces.

### dx...@google.com (2026-04-10)

Project: v8/v8  

Branch:  main  

Author:  Toon Verwaest [verwaest@chromium.org](mailto:verwaest@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7748466>

[maglev] Fix context scope tracking across register moves

---


Expand for full commit details
```
     
    Bug: 499752800 
    Change-Id: I3d41e8106c91eb839cc7f1c8f210c572ded90438 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7748466 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Auto-Submit: Toon Verwaest <verwaest@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106387}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-graph-builder.h`
- A `test/mjsunit/maglev/regress-499752800.js`

---

Hash: [5c719bd690fb4c4bb014f061bad5b0b44aae8aae](https://chromiumdash.appspot.com/commit/5c719bd690fb4c4bb014f061bad5b0b44aae8aae)  

Date: Fri Apr 10 10:46:13 2026


---

### ch...@google.com (2026-04-11)

This is sufficiently serious that it should be merged to M146. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to M147. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to M148. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M148. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

### ch...@google.com (2026-04-11)

**M146** merge request created. **Please update [crbug/501626564](https://crbug.com/501626564) to have this merge reviewed.**

### ch...@google.com (2026-04-11)

**M147** merge request created. **Please update [crbug/501627526](https://crbug.com/501627526) to have this merge reviewed.**

### ch...@google.com (2026-04-11)

**M148** merge request created. **Please update [crbug/501628709](https://crbug.com/501628709) to have this merge reviewed.**

### 24...@project.gserviceaccount.com (2026-04-11)

ClusterFuzz testcase 5404099952541696 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=106386:106387

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ml...@google.com (2026-04-13)

Culprit: <https://chromium.googlesource.com/v8/v8/+log/bdf51b8fe17de7f5240273d61ff829519cc67589..2413eb9b1c59c0afe439d1f1eb92378e1c79e7f6?pretty=fuller&n=10000>

Also identified by CF.

### ch...@google.com (2026-04-14)

Setting milestone because of s0/s1 severity.

### sw...@gmail.com (2026-04-16)

Hello, Is this one eligible for CVE and reward, please?

### sw...@gmail.com (2026-04-17)

I can trigger this one in 14.8.178.6, it might need to backmerge to M148. Thanks.

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
Baseline with bisect. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-06-16)

Project: v8/v8  

Branch:  refs/branch-heads/14.8  

Author:  Toon Verwaest [verwaest@chromium.org](mailto:verwaest@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7929506>

[M148] [maglev] Fix context scope tracking across register moves

---


Expand for full commit details
```
[M148] [maglev] Fix context scope tracking across register moves

Original change's description:
> [maglev] Fix context scope tracking across register moves
>
> Bug: 499752800
> Change-Id: I3d41e8106c91eb839cc7f1c8f210c572ded90438
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7748466
> Reviewed-by: Igor Sheludko <ishell@chromium.org>
> Auto-Submit: Toon Verwaest <verwaest@chromium.org>
> Commit-Queue: Igor Sheludko <ishell@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#106387}

(cherry picked from commit 5c719bd690fb4c4bb014f061bad5b0b44aae8aae)

Bug: 501628709,499752800
Change-Id: I3d41e8106c91eb839cc7f1c8f210c572ded90438
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7929506
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/14.8@{#68}
Cr-Branched-From: f9659283a5f8d42b3c09228cf5df606fcaf47a3d-refs/heads/14.8.178@{#1}
Cr-Branched-From: 141232520dc4910401240c531db3af36910a0fd1-refs/heads/main@{#106240}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-graph-builder.h`
- A `test/mjsunit/maglev/regress-499752800.js`

---

Hash: [dee74a59afceb8ce1372a116a4f674a8513ec312](https://chromiumdash.appspot.com/commit/dee74a59afceb8ce1372a116a4f674a8513ec312)  

Date: Fri Apr 10 10:46:13 2026


---

### pe...@google.com (2026-06-16)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ch...@google.com (2026-07-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/499752800)*
