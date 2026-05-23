# Maglev type confusion via corrupted Phi node metadata

| Field | Value |
|-------|-------|
| **Issue ID** | [441668149](https://issues.chromium.org/issues/441668149) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2025-08-28 |
| **Bounty** | $7,000.00 |

## Description

```

#
# Fatal error in ../../src/base/bit-field.h, line 56
# Debug check failed: is_valid(value).
#
#
#
#FailureMessage Object: 0x7bbc00ca1460
==== C stack trace ===============================

    ../v8/v8/out/x64.build/d8(__interceptor_backtrace+0x46) [0x56156e9e8286]
    /home/user/v8/v8/out/x64.build/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fbc2899b0b3]
    /home/user/v8/v8/out/x64.build/libv8_libplatform.so(+0x392ea) [0x7fbc288e62ea]
    /home/user/v8/v8/out/x64.build/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x2a0) [0x7fbc289617f0]
    /home/user/v8/v8/out/x64.build/libv8_libbase.so(+0x5a7ef) [0x7fbc289607ef]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MergePointInterpreterFrameState::MergeValue(v8::internal::maglev::MaglevGraphBuilder const*, v8::internal::interpreter::Register, v8::internal::maglev::KnownNodeAspects const&, v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::base::ThreadedListBase<v8::internal::maglev::MergePointInterpreterFrameState::Alternatives, v8::base::EmptyBase, v8::base::ThreadedListTraits<v8::internal::maglev::MergePointInterpreterFrameState::Alternatives>, false>*, bool)+0x1bde) [0x7fbc3140678e]
    /home/user/v8/v8/out/x64.build/libv8.so(+0x8a5e1ba) [0x7fbc314161ba]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MergePointInterpreterFrameState::MergePhis(v8::internal::maglev::MaglevGraphBuilder*, v8::internal::maglev::MaglevCompilationUnit&, v8::internal::maglev::InterpreterFrameState&, v8::internal::maglev::BasicBlock*, bool)+0x20a) [0x7fbc313fc6fa]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MergePointInterpreterFrameState::Merge(v8::internal::maglev::MaglevGraphBuilder*, v8::internal::maglev::MaglevCompilationUnit&, v8::internal::maglev::InterpreterFrameState&, v8::internal::maglev::BasicBlock*)+0x204) [0x7fbc313fc054]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitJump()+0x12c) [0x7fbc310a6d9c]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode()+0xbfa) [0x7fbc30ffc9fa]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MaglevGraphBuilder::BuildBody()+0x537) [0x7fbc31025697]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MaglevGraphBuilder::Build()+0xac2) [0x7fbc310bf2c2]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*)+0x798) [0x7fbc30e12728]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x113) [0x7fbc30f98f43]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x1ad) [0x7fbc2e110cbd]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MaglevConcurrentDispatcher::JobTask::Run(v8::JobDelegate*)+0x8a9) [0x7fbc30f9e1c9]
    /home/user/v8/v8/out/x64.build/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0x2e6) [0x7fbc288e3746]
    /home/user/v8/v8/out/x64.build/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x1f1) [0x7fbc288ea941]
    /home/user/v8/v8/out/x64.build/libv8_libbase.so(+0x91b2e) [0x7fbc28997b2e]
    ../v8/v8/out/x64.build/d8(+0x1999b7) [0x56156ea3f9b7]
    /lib/x86_64-linux-gnu/libc.so.6(+0x9caa4) [0x7fbc26f9faa4]
    /lib/x86_64-linux-gnu/libc.so.6(+0x129c3c) [0x7fbc2702cc3c]
Received signal 6
Aborted

```
#### VERSION

V8 version 14.1.0 (candidate)

#### REPRODUCTION CASE

Build: `python3 tools/dev/gm.py x64.debug`

Run: `./d8 poc.js`

---

Reporter credit: Shaheen Fazim

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 719 B)

## Timeline

### fa...@gmail.com (2025-08-28)

```
Fuzzer % time ./v8/v8/out/arm64.debug/d8 poc.js


#
# Fatal error in ../../src/base/bit-field.h, line 56
# Debug check failed: is_valid(value).
#
#
#
#FailureMessage Object: 0x16de20768
==== C stack trace ===============================

    0   libv8_libbase.dylib                 0x00000001033fce80 v8::base::debug::StackTrace::StackTrace() + 32
    1   libv8_libbase.dylib                 0x00000001033fcebc v8::base::debug::StackTrace::StackTrace() + 28
    2   libv8_libplatform.dylib             0x000000010355bfa0 v8::platform::(anonymous namespace)::PrintStackTrace() + 60
    3   libv8_libbase.dylib                 0x00000001033cf460 V8_Fatal(char const*, int, char const*, ...) + 352
    4   libv8_libbase.dylib                 0x00000001033cee84 v8::base::SetFatalFunction(void (*)(char const*, int, char const*)) + 0
    5   libv8_libbase.dylib                 0x00000001033cf56c V8_Dcheck(char const*, int, char const*) + 108
    6   libv8.dylib                         0x0000000119df7c00 v8::base::BitField<unsigned long, 16, 16, unsigned long long>::encode(unsigned long) + 60
    7   libv8.dylib                         0x000000011a0428b0 v8::internal::maglev::Phi* v8::internal::maglev::NodeBase::Allocate<v8::internal::maglev::Phi, v8::internal::maglev::MergePointInterpreterFrameState*, v8::internal::interpreter::Register&>(v8::internal::Zone*, unsigned long, v8::internal::maglev::MergePointInterpreterFrameState*&&, v8::internal::interpreter::Register&) + 248
    8   libv8.dylib                         0x000000011a03dac0 v8::internal::maglev::Phi* v8::internal::maglev::NodeBase::New<v8::internal::maglev::Phi, v8::internal::maglev::MergePointInterpreterFrameState*, v8::internal::interpreter::Register&>(v8::internal::Zone*, unsigned long, v8::internal::maglev::MergePointInterpreterFrameState*&&, v8::internal::interpreter::Register&) + 48
    9   libv8.dylib                         0x000000011a03cf20 v8::internal::maglev::MergePointInterpreterFrameState::MergeValue(v8::internal::maglev::MaglevGraphBuilder const*, v8::internal::interpreter::Register, v8::internal::maglev::KnownNodeAspects const&, v8::internal::maglev::ValueNode*, v8::internal::maglev::ValueNode*, v8::base::ThreadedListBase<v8::internal::maglev::MergePointInterpreterFrameState::Alternatives, v8::base::EmptyBase, v8::base::ThreadedListTraits<v8::internal::maglev::MergePointInterpreterFrameState::Alternatives>, false>*, bool) + 1764
    10  libv8.dylib                         0x000000011a048178 _ZZN2v88internal6maglev31MergePointInterpreterFrameState9MergePhisEPNS1_18MaglevGraphBuilderERNS1_21MaglevCompilationUnitERNS1_21InterpreterFrameStateEPNS1_10BasicBlockEbENK3$_0clERPNS1_9ValueNodeENS0_11interpreter8RegisterE + 288
    11  libv8.dylib                         0x000000011a048278 _ZN2v88internal6maglev28CompactInterpreterFrameState16ForEachParameterIRZNS1_31MergePointInterpreterFrameState9MergePhisEPNS1_18MaglevGraphBuilderERNS1_21MaglevCompilationUnitERNS1_21InterpreterFrameStateEPNS1_10BasicBlockEbE3$_0EEvRKS7_OT_ + 152
    12  libv8.dylib                         0x000000011a048004 _ZN2v88internal6maglev28CompactInterpreterFrameState15ForEachRegisterIRZNS1_31MergePointInterpreterFrameState9MergePhisEPNS1_18MaglevGraphBuilderERNS1_21MaglevCompilationUnitERNS1_21InterpreterFrameStateEPNS1_10BasicBlockEbE3$_0EEvRKS7_OT_ + 44
    13  libv8.dylib                         0x000000011a039b18 _ZN2v88internal6maglev28CompactInterpreterFrameState12ForEachValueIZNS1_31MergePointInterpreterFrameState9MergePhisEPNS1_18MaglevGraphBuilderERNS1_21MaglevCompilationUnitERNS1_21InterpreterFrameStateEPNS1_10BasicBlockEbE3$_0EEvRKS7_OT_ + 44
    14  libv8.dylib                         0x000000011a039ac0 v8::internal::maglev::MergePointInterpreterFrameState::MergePhis(v8::internal::maglev::MaglevGraphBuilder*, v8::internal::maglev::MaglevCompilationUnit&, v8::internal::maglev::InterpreterFrameState&, v8::internal::maglev::BasicBlock*, bool) + 112
    15  libv8.dylib                         0x000000011a0399c0 v8::internal::maglev::MergePointInterpreterFrameState::Merge(v8::internal::maglev::MaglevGraphBuilder*, v8::internal::maglev::MaglevCompilationUnit&, v8::internal::maglev::InterpreterFrameState&, v8::internal::maglev::BasicBlock*) + 564
    16  libv8.dylib                         0x000000011a039780 v8::internal::maglev::MergePointInterpreterFrameState::Merge(v8::internal::maglev::MaglevGraphBuilder*, v8::internal::maglev::InterpreterFrameState&, v8::internal::maglev::BasicBlock*) + 76
    17  libv8.dylib                         0x0000000119d76888 v8::internal::maglev::MaglevGraphBuilder::MergeIntoFrameState(v8::internal::maglev::BasicBlock*, int) + 368
    18  libv8.dylib                         0x0000000119de962c v8::internal::maglev::MaglevGraphBuilder::VisitJump() + 144
    19  libv8.dylib                         0x0000000119de9840 v8::internal::maglev::MaglevGraphBuilder::VisitJumpConstant() + 24
    20  libv8.dylib                         0x0000000119da6f4c v8::internal::maglev::MaglevGraphBuilder::VisitSingleBytecode() + 4760
    21  libv8.dylib                         0x0000000119db50f0 v8::internal::maglev::MaglevGraphBuilder::BuildBody() + 424
    22  libv8.dylib                         0x0000000119df282c v8::internal::maglev::MaglevGraphBuilder::Build() + 1144
    23  libv8.dylib                         0x0000000119b00d3c v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*) + 844
    24  libv8.dylib                         0x0000000119d723c0 v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*) + 132
    25  libv8.dylib                         0x00000001180ae2dc v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*) + 344
    26  libv8.dylib                         0x0000000119d752bc v8::internal::maglev::MaglevConcurrentDispatcher::JobTask::Run(v8::JobDelegate*) + 1048
    27  libv8_libplatform.dylib             0x000000010355899c v8::platform::DefaultJobWorker::Run() + 232
    28  libv8_libplatform.dylib             0x0000000103563134 v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run() + 224
    29  libv8_libbase.dylib                 0x00000001033fc134 v8::base::Thread::NotifyStartedAndRun() + 68
    30  libv8_libbase.dylib                 0x00000001033faff8 v8::base::ThreadEntry(void*) + 364
    31  libsystem_pthread.dylib             0x000000018a303c0c _pthread_start + 136
    32  libsystem_pthread.dylib             0x000000018a2feb80 thread_start + 8
zsh: trace trap  ./v8/v8/out/arm64.debug/d8 poc.js
./v8/v8/out/arm64.debug/d8 poc.js  9.87s user 0.19s system 128% cpu 7.857 total

```

### ct...@chromium.org (2025-08-28)

Appears to be tickling the same DCHECK as [Issue 437816268](https://issues.chromium.org/issues/437816268) (and [Issue 4219333669](https://issues.chromium.org/issues/4219333669)), but via a different route (stack traces are very different) so keeping this separate. It is unclear whether this DHECK ever has a security impact though.

I'll upload to ClusterFuzz to see if it can repro.

### cl...@appspot.gserviceaccount.com (2025-08-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5099080745156608.

### cl...@appspot.gserviceaccount.com (2025-08-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6612174772305920.

### ct...@chromium.org (2025-08-28)

Standard clusterfuzz job can't repro -- it may be timing out. Attempting again against an arm64 bot (based on [Comment #2](https://issues.chromium.org/issues/441668149#comment2)) and increasing the timeout to see if it can repro.

### 24...@project.gserviceaccount.com (2025-08-29)

Detailed Report: https://clusterfuzz.com/testcase?key=6612174772305920

Fuzzer: None
Job Type: linux_asan_d8_v8_arm64_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  is_valid(value) in bit-field.h
  v8::internal::maglev::MergePointInterpreterFrameState::MergeValue
  v8::internal::maglev::MergePointInterpreterFrameState::MergePhis
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_v8_arm64_dbg&range=101253:101254

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6612174772305920

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2025-08-29)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/a0a94ad0a7b6e8340ad90a504d25549e5daa1f5e ([maglev] Refactor bitfield for better alignment

- Reduce InputCountField size to 16 bits.
- Force OpProperties to have 16 bits.

New bitfield format:
[opcode:16][input_count:16][properties:16][extras:16]

Change-Id: I8784118d38d1f7d0ec3a6ec92fea46c8ea246e4d
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6703544
Auto-Submit: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#101254}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### vi...@chromium.org (2025-08-29)

Thanks for the report. The poc is creating a `Phi` that overflows our maximum limit for node inputs (`UINT16_MAX`).

However, I don't think this is a vulnerability. The overflow occurs when setting the `input_count`, but the node is allocated with the correct number of inputs. This should prevent any OOB memory access.

### vi...@chromium.org (2025-08-29)

Actually, after a better look at it. It seems like the register allocator will allocate side tables with `input_count` and might access with predecessor id (> UINT16\_MAX).

This should create an OOB access.

### ch...@google.com (2025-08-30)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-08-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### dx...@google.com (2025-09-01)

Project: v8/v8  

Branch:  main  

Author:  Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6904548>

[maglev] Allow maglev graph building to abort

---


Expand for full commit details
```
     
    Fixed: 441668149 
    Change-Id: I2e10f0c06783a9e513c615efc0b29740b74f42c2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6904548 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102162}

```

---

Files:

- M `src/codegen/bailout-reason.h`
- M `src/compiler/turboshaft/turbolev-graph-builder.cc`
- M `src/maglev/maglev-compiler.cc`
- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-graph-builder.h`
- M `src/maglev/maglev-inlining.cc`
- M `src/maglev/maglev-inlining.h`
- M `src/maglev/maglev-ir.h`

---

Hash: [24ae3662bf8cbe12e6331f369595eafe763a89c9](https://chromiumdash.appspot.com/commit/24ae3662bf8cbe12e6331f369595eafe763a89c9)  

Date: Mon Sep 1 13:37:54 2025


---

### ch...@google.com (2025-09-02)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### vi...@chromium.org (2025-09-02)

1. <https://chromium-review.googlesource.com/c/v8/v8/+/6904548>
2. It hasn't landed on Canary yet.
3. No.
4. No.
5. No.

### ch...@google.com (2025-09-03)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-09-03)

In reviewing this for potential backmerge, I've come across a crash that appears related to this change (v8::internal::maglev::MaglevGraphBuilder::Build())
<https://crash.corp.google.com/browse?q=stable_signature%3D%27crash_reporter%3A%3ADumpWithoutCrashing-320aa8f7%27>

I want to defer backmerge approval for the time being until there is a bit more Canary data to verify there is confirm no backmerge risk.

### sp...@google.com (2025-09-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process / renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ts...@google.com (2025-09-11)

Victor, curious if the crash in C#17 was determined to be related or unrelated? Thanks!

### vi...@chromium.org (2025-09-12)

I think the crash (starting in July and peaking in August) is unrelated, since it is much older than the fix (1st of September).

### vi...@chromium.org (2025-09-12)

The crash seems to match <https://chromium-review.googlesource.com/c/v8/v8/+/6732622> instead.

### ts...@google.com (2025-09-12)

Please merge to M140 (7339) and M141 (7390) as soon as you are able. Thanks!

### dx...@google.com (2025-09-15)

Project: v8/v8  

Branch:  refs/branch-heads/14.1  

Author:  Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6945497>

Merged: [maglev] Allow maglev graph building to abort

---


Expand for full commit details
```
     
    Fixed: 441668149 
     
    (cherry picked from commit 24ae3662bf8cbe12e6331f369595eafe763a89c9) 
     
    Change-Id: Id4fe1d636c2fd68d69dca70623a39b92977a1e8a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6945497 
    Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.1@{#4} 
    Cr-Branched-From: 1f4839b6a7095c09cb5cc10603ad7b22037405f3-refs/heads/14.1.146@{#1} 
    Cr-Branched-From: cd6944c05d268ef7d734cf33af86bc94c6172c2f-refs/heads/main@{#102149}

```

---

Files:

- M `src/codegen/bailout-reason.h`
- M `src/compiler/turboshaft/turbolev-graph-builder.cc`
- M `src/maglev/maglev-compiler.cc`
- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-graph-builder.h`
- M `src/maglev/maglev-inlining.cc`
- M `src/maglev/maglev-inlining.h`
- M `src/maglev/maglev-ir.h`

---

Hash: [3275b87237ba02d4a343b1b17a2e47fbee8f572a](https://chromiumdash.appspot.com/commit/3275b87237ba02d4a343b1b17a2e47fbee8f572a)  

Date: Mon Sep 1 13:37:54 2025


---

### pe...@google.com (2025-09-15)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### vi...@chromium.org (2025-09-15)

1. No.
2. No.

### qk...@google.com (2025-09-16)

Labeled as not applicable for M132/138 LTS because the branches don't contain the culprit[1].

[1]  https://chromium-review.googlesource.com/c/v8/v8/+/6703544

### dx...@google.com (2025-09-16)

Project: v8/v8  

Branch:  refs/branch-heads/14.0  

Author:  Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6943535>

Merged: [maglev] Allow maglev graph building to abort

---


Expand for full commit details
```
     
    Fixed: 441668149 
     
    (cherry picked from commit 24ae3662bf8cbe12e6331f369595eafe763a89c9) 
     
    Change-Id: I64d39ad287a6db82a5b586cc0567971432622010 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6943535 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.0@{#10} 
    Cr-Branched-From: 4ec2f43a229069d6124c88527ee7bb9cc642edc3-refs/heads/14.0.365@{#1} 
    Cr-Branched-From: a88b57016d5caf9b5ed8f07b7d2f3e729520b8b5-refs/heads/main@{#101731}

```

---

Files:

- M `src/codegen/bailout-reason.h`
- M `src/compiler/turboshaft/turbolev-graph-builder.cc`
- M `src/maglev/maglev-compiler.cc`
- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-graph-builder.h`
- M `src/maglev/maglev-inlining.cc`
- M `src/maglev/maglev-inlining.h`
- M `src/maglev/maglev-ir.h`

---

Hash: [07ad1d3ae25acdf80fe9206b73f29d604cbfc47d](https://chromiumdash.appspot.com/commit/07ad1d3ae25acdf80fe9206b73f29d604cbfc47d)  

Date: Mon Sep 1 13:37:54 2025


---

### ch...@google.com (2025-09-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sr...@google.com (2025-09-16)

Please complete your merges to M141 branch before 2pm PST today so they can be part of the beta release tomorrow ( we are cutting stable RC next week) so it would be good to get beta coverage for these CL's this week

### vi...@chromium.org (2025-09-17)

Re: [comment #30](https://issues.chromium.org/issues/441668149#comment30) already merged, see [comment #23](https://issues.chromium.org/issues/441668149#comment23) and #27.

### fa...@gmail.com (2025-09-26)

Hi, can I get a CVE and credit (chome release) for this issue? Thank you.

### wf...@chromium.org (2025-10-13)

Hi, I think this bug regressed in 140 and was fixed before 140 went to stable, so would not qualify for a CVE [1], but it did qualify for a reward as it prevented the regression from shipping to our users, so thank you for your report!

[1] - <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/vrp-faq.md#will-i-receive-a-cve-for-my-bug>

### ch...@google.com (2025-12-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a sandboxed process / renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/441668149)*
