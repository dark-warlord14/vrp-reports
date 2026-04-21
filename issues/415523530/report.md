# Debug check failed: CanElideWriteBarrier(object, value). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [415523530](https://issues.chromium.org/issues/415523530) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Linux |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2025-05-04 |
| **Bounty** | $3,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 99836
    - link: https://crrev.com/6953465cfa8d77c67f6cab42cfe3bf5204028a22
- Commit Message

```
commit 6953465cfa8d77c67f6cab42cfe3bf5204028a22
Author: Marja Hölttä <marja@chromium.org>
Date:   Tue Apr 22 08:44:55 2025 +0200

    [maglev] Type system refactoring: Fix write barriers in dead code
    
    Fixed: 412125812
    Change-Id: I7d5886dd3c00762ee650a60a3d6607e90929fd18
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6478150
    Commit-Queue: Marja Hölttä <marja@chromium.org>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#99836}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-100039/d8 --allow-natives-syntax --future --turbolev poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/maglev/maglev-graph-builder.cc, line 5513
# Debug check failed: CanElideWriteBarrier(object, value).
#
#
#
#FailureMessage Object: 0x7ffc5f68faf0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-100039/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f29c1c163d3]
    /tmp/d8-linux-debug-v8-component-100039/libv8_libplatform.so(+0x1ba1d) [0x7f29c1bbfa1d]
    /tmp/d8-linux-debug-v8-component-100039/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7f29c1bf9504]
    /tmp/d8-linux-debug-v8-component-100039/libv8_libbase.so(+0x2bec5) [0x7f29c1bf8ec5]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildStoreTaggedFieldNoWriteBarrier(v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, int, v8::internal::maglev::StoreTaggedMode)+0x175) [0x7f29bfccb675]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::maglev::MaglevGraphBuilder::TrySpecializeStoreContextSlot(v8::internal::maglev::ValueNode*, int, v8::internal::maglev::ValueNode*, v8::internal::maglev::Node**)+0x3a6) [0x7f29bfccb046]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::maglev::MaglevGraphBuilder::StoreAndCacheContextSlot(v8::internal::maglev::ValueNode*, int, v8::internal::maglev::ValueNode*, v8::internal::ContextMode)+0x12e) [0x7f29bfccba5e]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode()+0x7fc) [0x7f29bfbbab7c]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildLoopForPeeling()+0x18e) [0x7f29bfd2234e]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::maglev::MaglevGraphBuilder::PeelLoop()+0x12c) [0x7f29bfd2203c]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildBody()+0x270) [0x7f29bfbb6490]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::maglev::MaglevGraphBuilder::Build()+0x37d) [0x7f29bfbb258d]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::compiler::turboshaft::MaglevGraphBuildingPhase::Run(v8::internal::compiler::turboshaft::PipelineData*, v8::internal::Zone*, v8::internal::compiler::Linkage*)+0x1cb) [0x7f29c139f36b]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(auto v8::internal::compiler::turboshaft::Pipeline::Run<v8::internal::compiler::turboshaft::MaglevGraphBuildingPhase, v8::internal::compiler::Linkage*&>(v8::internal::compiler::Linkage*&)+0xf7) [0x7f29c0b96057]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::compiler::turboshaft::Pipeline::CreateGraphWithMaglev(v8::internal::compiler::Linkage*)+0xbb) [0x7f29c0b82c0b]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x1d7) [0x7f29c0b829d7]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x92) [0x7f29be7e3ed2]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(+0x31fb07d) [0x7f29be7fb07d]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0x3d7) [0x7f29be7feac7]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(+0x42d46a5) [0x7f29bf8d46a5]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(+0x42cbe33) [0x7f29bf8cbe33]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(v8::internal::Runtime_OptimizeTurbofanEager(int, unsigned long*, v8::internal::Isolate*)+0xa0) [0x7f29bf8cb9a0]
    /tmp/d8-linux-debug-v8-component-100039/libv8.so(+0x23f243d) [0x7f29bd9f243d]

```

## Other
Please note to include the flags `--allow-natives-syntax --future --turbolev` for clusterfuzz classification.

VERSION
Tested on v8 version: 13.7.0 - 13.8.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-100039.zip
2. Run: `d8 --allow-natives-syntax --future --turbolev poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy) and Nan Wang (@eternalsakura13)


## Attachments

- poc.js (text/javascript, 493 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-05-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6333482384949248.

### 24...@project.gserviceaccount.com (2025-05-04)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-05-04)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/6953465cfa8d77c67f6cab42cfe3bf5204028a22 ([maglev] Type system refactoring: Fix write barriers in dead code

Fixed: 412125812
Change-Id: I7d5886dd3c00762ee650a60a3d6607e90929fd18
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6478150
Commit-Queue: Marja Hölttä <marja@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#99836}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2025-05-04)

Detailed Report: https://clusterfuzz.com/testcase?key=6333482384949248

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  CanElideWriteBarrier(object, value) in maglev-graph-builder.cc
  v8::internal::maglev::MaglevGraphBuilder::BuildStoreTaggedFieldNoWriteBarrier
  v8::internal::maglev::MaglevGraphBuilder::TrySpecializeStoreContextSlot
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=99835:99836

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6333482384949248

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ma...@chromium.org (2025-05-12)

Not a duplicate

### dx...@google.com (2025-05-12)

Project: v8/v8  

Branch: main  

Author: Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6532350>

[maglev types] Write barriers in dead code - fix three

---


Expand for full commit details
```
     
    This CL inserts an early bailout if the value type is empty, so that we 
    don't end up with contradictions about whether or not a write barrier is 
    needed. 
     
    Fixed: 415523530 
    Change-Id: I5db2f43c72f270411f587cba44c3406752411796 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6532350 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#100222}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`
- A `test/mjsunit/maglev/regress-415523530.js`

---

Hash: d948770f56e6f0e8632934085b08e252080d4196  

Date:  Mon May 12 10:09:51 2025


---

### ch...@google.com (2025-05-13)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### 24...@project.gserviceaccount.com (2025-05-13)

ClusterFuzz testcase 6333482384949248 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=100221:100222

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2025-05-13)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### me...@google.com (2025-05-14)

marja: Can you confirm this is a regression in M137? Also, could you please evaluate the severity?

### me...@google.com (2025-05-15)

(Tentatively setting high severity)

### ma...@chromium.org (2025-05-15)

Yes, it's in M137. This is low severity, this is a DCHECK failing because we get confused about whether dead code should or should not use write barriers. It's likely that nothing else will go wrong (and the code is dead anyway, so it doesn't really matter what's in it).

### ch...@google.com (2025-05-15)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ki...@gmail.com (2025-05-19)

Hi, please mark this issue as fixed, thanks!

### ma...@chromium.org (2025-05-19)

Trying to mark as fixed again, let's see if the bot reopens it. Hmm, not sure if this should be categorized as "Vulnerability", maybe it should be downgraded to "Bug".

### sp...@google.com (2025-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
report of mitigated memory corruption in a sandboxed process / the renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-22)

Thank you both for your efforts on this issue. Based on the comments above and an off-bug discussion with the V8 security team, we have assessed this issue to be mitigated based on the investigation into this issue and that it seems a second bug would be necessary to for this issue to have security implications.

### ch...@google.com (2025-08-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of mitigated memory corruption in a sandboxed process / the renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/415523530)*
