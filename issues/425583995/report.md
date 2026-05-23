# Debug check failed: pc_offset() < unresolved_branches_first_limit()

| Field | Value |
|-------|-------|
| **Issue ID** | [425583995](https://issues.chromium.org/issues/425583995) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2025-06-17 |
| **Bounty** | $7,000.00 |

## Description

```

#
# Fatal error in ../../src/codegen/arm64/assembler-arm64.cc, line 4917
# Debug check failed: pc_offset() < unresolved_branches_first_limit().
#
#
#
#FailureMessage Object: 0x16d305468
==== C stack trace ===============================

    0   libv8_libbase.dylib                 0x0000000104389ee8 v8::base::debug::StackTrace::StackTrace() + 24
    1   libv8_libplatform.dylib             0x00000001043c67c8 v8::platform::(anonymous namespace)::PrintStackTrace() + 116
    2   libv8_libbase.dylib                 0x000000010436d5cc V8_Fatal(char const*, int, char const*, ...) + 352
    3   libv8_libbase.dylib                 0x000000010436ced0 v8::base::SetFatalFunction(void (*)(char const*, int, char const*)) + 0
    4   libv8.dylib                         0x000000010c96b6dc v8::internal::Assembler::CheckVeneerPool(bool, bool, unsigned long) + 232
    5   libv8.dylib                         0x000000010aeb3208 v8::internal::Assembler::Emit(unsigned int) + 132
    6   libv8.dylib                         0x000000010c96bc8c v8::internal::Assembler::EmitVeneers(bool, bool, unsigned long) + 908
    7   libv8.dylib                         0x000000010c977f14 v8::internal::MacroAssembler::PushHelper(int, int, v8::internal::CPURegister const&, v8::internal::CPURegister const&, v8::internal::CPURegister const&, v8::internal::CPURegister const&) + 136
    8   libv8.dylib                         0x000000010c3a8d48 void v8::internal::maglev::detail::PushIteratorReverse<v8::internal::maglev::RepeatIterator<v8::internal::Register>>(v8::internal::maglev::MaglevAssembler*, v8::base::iterator_range<v8::internal::maglev::RepeatIterator<v8::internal::Register>>) + 324
    9   libv8.dylib                         0x000000010c3a8aec void v8::internal::maglev::detail::PushIteratorReverse<std::__Cr::reverse_iterator<v8::internal::maglev::Input*>, v8::base::iterator_range<v8::internal::maglev::RepeatIterator<v8::internal::Register>>>(v8::internal::maglev::MaglevAssembler*, v8::base::iterator_range<std::__Cr::reverse_iterator<v8::internal::maglev::Input*>>, v8::base::iterator_range<v8::internal::maglev::RepeatIterator<v8::internal::Register>>) + 108
    10  libv8.dylib                         0x000000010c35ff7c v8::internal::maglev::CallKnownJSFunction::GenerateCode(v8::internal::maglev::MaglevAssembler*, v8::internal::maglev::ProcessingState const&) + 356
    11  libv8.dylib                         0x000000010bf32110 v8::internal::maglev::ProcessResult v8::internal::maglev::NodeMultiProcessor<v8::internal::maglev::(anonymous namespace)::SafepointingNodeProcessor, v8::internal::maglev::(anonymous namespace)::MaglevCodeGeneratingNodeProcessor>::Process<v8::internal::maglev::CallKnownJSFunction>(v8::internal::maglev::CallKnownJSFunction*, v8::internal::maglev::ProcessingState const&) + 1160
    12  libv8.dylib                         0x000000010beef718 v8::internal::maglev::MaglevCodeGenerator::EmitCode() + 7092
    13  libv8.dylib                         0x000000010beed8d4 v8::internal::maglev::MaglevCodeGenerator::Assemble() + 48
    14  libv8.dylib                         0x000000010bfc82f0 v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*) + 5532
    15  libv8.dylib                         0x000000010c0e514c v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*) + 96
    16  libv8.dylib                         0x000000010af9587c v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*) + 160
    17  libv8.dylib                         0x000000010c0e718c v8::internal::maglev::MaglevConcurrentDispatcher::JobTask::Run(v8::JobDelegate*) + 856
    18  libv8_libplatform.dylib             0x00000001043c52cc v8::platform::DefaultJobWorker::Run() + 292
    19  libv8_libplatform.dylib             0x00000001043c7d0c v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run() + 276
    20  libv8_libbase.dylib                 0x00000001043882ec v8::base::ThreadEntry(void*) + 180
    21  libsystem_pthread.dylib             0x00000001911fac0c _pthread_start + 136
    22  libsystem_pthread.dylib             0x00000001911f5b80 thread_start + 8
zsh: trace trap  ./v8/v8/out/debug/d8 poc.js

```
#### VERSION

V8 version 13.9.0 (candidate)

#### REPRODUCTION CASE

Build: `v8 Debug build, MacOS arm64`

Run: `./d8 poc.js`

---

Reporter credit: Shaheen Fazim

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 745 B)

## Timeline

### fa...@gmail.com (2025-06-17)

This PoC trying to trigger an integer overflow in V8 Maglev by dynamically creating a JavaScript function with 40,000 arguments, causing internal register count calculations (such as pc\_offset or veneer management) to exceed 32-bit limits during JIT compilation; repeated invocations force On-Stack Replacement (OSR), leading to a crash in the assembler during Maglev code generation.

### fa...@gmail.com (2025-06-17)

deleted

### cl...@appspot.gserviceaccount.com (2025-06-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5453980591128576.

### es...@chromium.org (2025-06-19)

Note: FoundIn and Severity are provisional

### cl...@appspot.gserviceaccount.com (2025-06-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6226831434776576.

### 24...@project.gserviceaccount.com (2025-06-19)

Detailed Report: https://clusterfuzz.com/testcase?key=6226831434776576

Fuzzer: None
Job Type: linux_asan_d8_v8_arm64_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  pc_offset() < unresolved_branches_first_limit() in assembler-arm64.cc
  v8::internal::Assembler::CheckVeneerPool
  v8::internal::Assembler::Emit
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_v8_arm64_dbg&revision=100909

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6226831434776576

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### ch...@google.com (2025-06-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-06-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-06-27)

Project: v8/v8  

Branch: main  

Author: Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6683635>

[arm64] Ensure InstructionAccurateScope is called with correct count

---


Expand for full commit details
```
     
    The scope prevents veneer pool generation. We need to pass the 
    correct count of instructions to CheckVeneerPool inside the scope 
    constructor, otherwise we might overflow the veneer distance 
    margin in the next check (after the scope has ended). 
     
    Fixed: 425583995 
    Change-Id: Iebb81898c4f7999137fc784ce6704773614c2bb5 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6683635 
    Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101089}

```

---

Files:

- M `src/codegen/arm64/macro-assembler-arm64.cc`
- M `src/codegen/arm64/macro-assembler-arm64.h`
- A `test/mjsunit/regress/regress-425583995.js`

---

Hash: c58fda1f0ec46429dd66c2cacf6a98fac001e4fd  

Date:  Fri Jun 27 10:40:10 2025


---

### ch...@google.com (2025-06-27)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-06-27)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M138. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [138, 139].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### vi...@chromium.org (2025-06-27)

1. https://chromium-review.googlesource.com/c/v8/v8/+/6683635
2. Not yet (landed today).
3. No.
4. No.
5. No.

### am...@chromium.org (2025-06-27)

We are entering a release freeze. We have been asked to pause on merges to Stable / 138 for now to ensure if there is an emergency respin for a security or functional issue during the freeze, the changes from the emergency build as as minimal as possible.
I'll revisit merge review mid next week before the US holiday.

### am...@chromium.org (2025-07-02)

Merges approved for https://crrev.com/c/6683635, please merge this fix to 13.9 and 13.8 before EOD, Thursday, 10 July 

### sp...@google.com (2025-07-02)

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

### am...@chromium.org (2025-07-02)

Thank you for your efforts and reporting this issue to us.

### dx...@google.com (2025-07-03)

Project: v8/v8  

Branch: refs/branch-heads/13.9  

Author: Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6703637>

Merged: [arm64] Ensure InstructionAccurateScope is called with correct count

---


Expand for full commit details
```
     
    The scope prevents veneer pool generation. We need to pass the 
    correct count of instructions to CheckVeneerPool inside the scope 
    constructor, otherwise we might overflow the veneer distance 
    margin in the next check (after the scope has ended). 
     
    Bug: 425583995 
     
    (cherry picked from commit c58fda1f0ec46429dd66c2cacf6a98fac001e4fd) 
     
    Change-Id: Ibb71b840d30d7c442e51a81fd12909401eeaf6e6 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6703637 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/13.9@{#10} 
    Cr-Branched-From: 76ea4091129171336d347c2624f6062bd9708042-refs/heads/13.9.205@{#1} 
    Cr-Branched-From: 28242121f590fe04758efec176658cd57310b297-refs/heads/main@{#100941}

```

---

Files:

- M `src/codegen/arm64/macro-assembler-arm64.cc`
- M `src/codegen/arm64/macro-assembler-arm64.h`
- A `test/mjsunit/regress/regress-425583995.js`

---

Hash: f0a977abb8016d905b2f04dca2b7158ba86b3360  

Date:  Fri Jun 27 10:40:10 2025


---

### pe...@google.com (2025-07-03)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### vi...@chromium.org (2025-07-04)

1. No
2. No

### fa...@gmail.com (2025-07-04)

*Thanks* for *the* `reward`!

### dx...@google.com (2025-07-07)

Project: v8/v8  

Branch: refs/branch-heads/13.8  

Author: Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6701570>

Merged: [arm64] Ensure InstructionAccurateScope is called with correct count

---


Expand for full commit details
```
     
    The scope prevents veneer pool generation. We need to pass the 
    correct count of instructions to CheckVeneerPool inside the scope 
    constructor, otherwise we might overflow the veneer distance 
    margin in the next check (after the scope has ended). 
     
    Bug: 425583995 
     
    (cherry picked from commit c58fda1f0ec46429dd66c2cacf6a98fac001e4fd) 
     
    Change-Id: I95cf184422d3b62c222aa378148337884047f9e7 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6701570 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/13.8@{#47} 
    Cr-Branched-From: 61ddd471ece346840bbebbb308dceb4b4ce31b28-refs/heads/13.8.258@{#1} 
    Cr-Branched-From: fdb5de2c741658e94944f2ec1218530e98601c23-refs/heads/main@{#100480}

```

---

Files:

- M `src/codegen/arm64/macro-assembler-arm64.cc`
- M `src/codegen/arm64/macro-assembler-arm64.h`
- A `test/mjsunit/regress/regress-425583995.js`

---

Hash: c3445c839ca1bb62a0c74f45d81ea10ad50ce1e1  

Date:  Fri Jun 27 10:40:10 2025


---

### ch...@google.com (2025-07-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2025-07-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### ch...@google.com (2025-07-09)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-09)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### vi...@chromium.org (2025-07-09)

Regarding #27:

1. 1
2. Low: just affect arm64 when using InstructionScopes with zero as argument.
3. No
4. Yes

### rz...@google.com (2025-07-10)

R #30,#27, the CL being backmerged is <https://chromium-review.googlesource.com/c/v8/v8/+/6712494>

### cl...@appspot.gserviceaccount.com (2025-07-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6537898278977536.

### dx...@google.com (2025-08-07)

Project: v8/v8  

Branch:  refs/branch-heads/13.2  

Author:  Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6712494>

[M132-LTS][arm64] Ensure InstructionAccurateScope is called with correct count

---


Expand for full commit details
```
     
    The scope prevents veneer pool generation. We need to pass the 
    correct count of instructions to CheckVeneerPool inside the scope 
    constructor, otherwise we might overflow the veneer distance 
    margin in the next check (after the scope has ended). 
     
    (cherry picked from commit c58fda1f0ec46429dd66c2cacf6a98fac001e4fd) 
     
    Fixed: 425583995 
    Change-Id: Iebb81898c4f7999137fc784ce6704773614c2bb5 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6683635 
    Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#101089} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6712494 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/13.2@{#104} 
    Cr-Branched-From: 24068c59cedad9ee976ddc05431f5f497b1ebd71-refs/heads/13.2.152@{#1} 
    Cr-Branched-From: 6054ba94db0969220be4f94dc1677fc4696bdc4f-refs/heads/main@{#97085}

```

---

Files:

- M `src/codegen/arm64/macro-assembler-arm64.cc`
- M `src/codegen/arm64/macro-assembler-arm64.h`
- A `test/mjsunit/regress/regress-425583995.js`

---

Hash: [385d92ca6813453b32b657b21c4a2d2b13d4ab1c](http://crrev.com/385d92ca6813453b32b657b21c4a2d2b13d4ab1c)  

Date: Fri Jun 27 10:40:10 2025


---

### ch...@google.com (2025-10-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a sandboxed process / renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/425583995)*
