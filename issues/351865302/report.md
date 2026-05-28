# Fatal error in ../../src/compiler/simplified-lowering.cc, line 568

| Field | Value |
|-------|-------|
| **Issue ID** | [351865302](https://issues.chromium.org/issues/351865302) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler, Blink>JavaScript>Compiler>Maglev, Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | be...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2024-07-09 |
| **Bounty** | $7,000.00 |

## Description

Security: Fatal error in ../../src/compiler/simplified-lowering.cc, line 568

Steps to reproduce the problem:
build flag:
gn gen out/fuzzbuild_new --args='is_debug=false dcheck_always_on=true v8_static_library=true v8_enable_slow_dchecks=true v8_enable_v8_checks=true v8_enable_verify_heap=true v8_enable_verify_csa=true v8_fuzzilli=true sanitizer_coverage_flags="trace-pc-guard" target_cpu="x64"'

environment:
Ubuntu 22.04.2 LTS 5.19.0-42-generic
v8 Version: commit 106f228ca86505edb70aa575c99fd2d636819d17

or download d8 binary with 
https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-arm-asan-linux-debug-v8-component-94899.zip?generation=1720486183963990&alt=media

run with:
./d8 --allow-natives-syntax --jit-fuzzing poc.js

result will be:

#
# Fatal error in ../../src/compiler/simplified-lowering.cc, line 568
# Debug check failed: current_type.Maybe(integer).
#
#
#
#FailureMessage Object: 0x78fd1452b860
==== C stack trace ===============================

    ./d8(__interceptor_backtrace+0x46) [0x5b66cb1ee616]
    /home/goushi/prebuild_v8/94899/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x78fd4b165963]
    /home/goushi/prebuild_v8/94899/libv8_libplatform.so(+0x3172a) [0x78fd4b0b772a]
    /home/goushi/prebuild_v8/94899/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x2a0) [0x78fd4b126d00]
    /home/goushi/prebuild_v8/94899/libv8_libbase.so(+0x50e0f) [0x78fd4b125e0f]
    /home/goushi/prebuild_v8/94899/libv8.so(v8::internal::compiler::RepresentationSelector::Weaken(v8::internal::compiler::Node*, v8::internal::compiler::Type, v8::internal::compiler::Type)+0x3e2) [0x78fd4890e6b2]
    /home/goushi/prebuild_v8/94899/libv8.so(v8::internal::compiler::RepresentationSelector::UpdateFeedbackType(v8::internal::compiler::Node*)+0x11e6) [0x78fd489041e6]
    /home/goushi/prebuild_v8/94899/libv8.so(v8::internal::compiler::RepresentationSelector::RetypeNode(v8::internal::compiler::Node*)+0x3d) [0x78fd48902abd]
    /home/goushi/prebuild_v8/94899/libv8.so(v8::internal::compiler::RepresentationSelector::RunRetypePhase()+0x459) [0x78fd488e1b89]
    /home/goushi/prebuild_v8/94899/libv8.so(v8::internal::compiler::SimplifiedLowering::LowerAllNodes()+0x477) [0x78fd488cf447]
    /home/goushi/prebuild_v8/94899/libv8.so(v8::internal::compiler::SimplifiedLoweringPhase::Run(v8::internal::compiler::TFPipelineData*, v8::internal::Zone*, v8::internal::compiler::Linkage*)+0x234) [0x78fd48843fe4]
    /home/goushi/prebuild_v8/94899/libv8.so(auto v8::internal::compiler::PipelineImpl::Run<v8::internal::compiler::SimplifiedLoweringPhase, v8::internal::compiler::Linkage*&>(v8::internal::compiler::Linkage*&)+0x17e) [0x78fd48791c3e]
    /home/goushi/prebuild_v8/94899/libv8.so(v8::internal::compiler::PipelineImpl::OptimizeTurbofanGraph(v8::internal::compiler::Linkage*)+0xaef) [0x78fd4878460f]
    /home/goushi/prebuild_v8/94899/libv8.so(v8::internal::compiler::PipelineCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x319) [0x78fd487827a9]
    /home/goushi/prebuild_v8/94899/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x1a5) [0x78fd43de2e45]
    /home/goushi/prebuild_v8/94899/libv8.so(v8::internal::OptimizingCompileDispatcher::CompileNext(v8::internal::TurbofanCompilationJob*, v8::internal::LocalIsolate*)+0x4a) [0x78fd43fe33aa]
    /home/goushi/prebuild_v8/94899/libv8.so(v8::internal::OptimizingCompileDispatcher::CompileTask::Run(v8::JobDelegate*)+0x5f1) [0x78fd43fe9911]
    /home/goushi/prebuild_v8/94899/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0x2b9) [0x78fd4b0b4969]
    /home/goushi/prebuild_v8/94899/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x1f1) [0x78fd4b0bb901]
    /home/goushi/prebuild_v8/94899/libv8_libbase.so(+0x8e413) [0x78fd4b163413]
    ./d8(+0x15ef27) [0x5b66cb242f27]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x78fd3da94ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126850) [0x78fd3db26850]
[1]    19319 trace trap  ./d8 --allow-natives-syntax --jit-fuzzing poc.js

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 711 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-07-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5176765641064448.

### 24...@project.gserviceaccount.com (2024-07-09)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-07-09)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/6588ba2f6bfbe641303f7f97dfa7aaf13837ce87 ([tiering] More tiering tweaks

- make maglev tiering essentially tickless by always doing the next step
  on the next tick
- change OSR from N ticks to M interrupt budget (1 tick) where M is a
  multiplier of the bytecode size

Change-Id: I7faaf3faf474f9b4ea04beacc10bc925e8dff5d7
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4360037
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#86640}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2024-07-09)

Detailed Report: https://clusterfuzz.com/testcase?key=5176765641064448

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  current_type.Maybe(integer) in simplified-lowering.cc
  v8::internal::compiler::RepresentationSelector::Weaken
  v8::internal::compiler::RepresentationSelector::UpdateFeedbackType
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=86639:86640

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5176765641064448

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### fl...@google.com (2024-07-11)

Assigning provisional severity of High.

### ap...@google.com (2024-07-12)

Project: v8/v8
Branch: main

commit 03dded9955d9665822d8e1c5906fabbc03282eb4
Author: Toon Verwaest <verwaest@chromium.org>
Date:   Fri Jul 12 15:19:31 2024

    [parsing] Allow NewUnresolved to be used for reparsing class initializers
    
    This makes NewUnresolved as permissive as AddUnresolved. Class initializers
    will manually handle resolution of unresolved references that end up in the
    already resolved class scope. (They end up there because that's where computed
    property names in class literals are resolved.)
    
    Bug: 351865302
    Change-Id: I4a9eb8f6af9b792f0f344e2571c60824afe3c649
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5701134
    Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    Auto-Submit: Toon Verwaest <verwaest@chromium.org>
    Commit-Queue: Toon Verwaest <verwaest@chromium.org>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95003}

M       src/ast/scopes.h

https://chromium-review.googlesource.com/5701134


### pe...@google.com (2024-07-13)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-13)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ar...@chromium.org (2024-08-07)

Hey Nico,

Checking in on this security bug assigned to you: "Security: Fatal error in ../../src/compiler/simplified-lowering.cc, line 568"

It's been triaged as High severity and has been open for a few weeks now. Is there anything I can do to help unblock progress on this?
Please let me know if you have any updates or if there's anything I can do to assist!

Best,
Secondary Security Shepherd

### pe...@google.com (2024-08-09)

nicohartmann: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### am...@chromium.org (2024-08-19)

[secondary shepherd check-in] hey folks -- this Stable impacting issue has been open for some time. Can you please address this issue at soonest. Please let us know if there is some sort of blocker preventing resolution here. Thank you!

### ni...@chromium.org (2024-08-20)

I'm looking into this again. Will give an update as soon as I have one.

### ap...@google.com (2024-08-20)

Project: v8/v8
Branch: main

commit f784b0b05be96cda5b769a3df92fc3c012657166
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Tue Aug 20 16:26:39 2024

    [turbofan] Handle Type::None() in SameValue
    
    Bug: chromium:351865302
    Change-Id: Ibab11d8a68fe7c55113abf31c090fd66b3ff0542
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5797195
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95728}

M       src/compiler/operation-typer.cc

https://chromium-review.googlesource.com/5797195


### ni...@chromium.org (2024-08-20)

While the fix is simple, there is quite some complexity involved in producing this issue. It is possible that this an actual vulnerability, since the fix is trivial, we should consider backmerging.

### 24...@project.gserviceaccount.com (2024-08-21)

ClusterFuzz testcase 5176765641064448 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=95727:95728

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-08-21)

Merge review required: M128 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-08-21)

Merge review required: M127 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-08-21)

Merge review required: M126 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), srinivassista (Desktop)

### ni...@chromium.org (2024-08-22)

1. Potential security vulnerability due to type confusion
2. <https://chromium-review.googlesource.com/c/v8/v8/+/5797195>
3. Yes
4. No
6. No

### am...@chromium.org (2024-08-22)

<https://crrev.com/c/5797195> approved for merge to M129 Beta and M128 Stable, please merge this fix to 12.9 and 12.8 at soonest so this fix can be included in the next M128 Stable channel update -- ty!

### am...@chromium.org (2024-08-22)

removing security release label, since issue was not yet resolved at the time of M128 Stable milestone release

### ap...@google.com (2024-08-23)

Project: v8/v8
Branch: refs/branch-heads/12.8

commit 10b4403117735b40c77c6941644b512b48a71570
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Tue Aug 20 16:26:39 2024

    Merged: [turbofan] Handle Type::None() in SameValue
    
    Bug: chromium:351865302
    (cherry picked from commit f784b0b05be96cda5b769a3df92fc3c012657166)
    
    Change-Id: Idf6bf9276d5510376594f31ee563e4a0bee617f5
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5806588
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.8@{#42}
    Cr-Branched-From: 70cbb397b153166027e34c75adf8e7993858222e-refs/heads/12.8.374@{#1}
    Cr-Branched-From: 451b63ed4251c2b21c56144d8428f8be3331539b-refs/heads/main@{#95151}

M       src/compiler/operation-typer.cc

https://chromium-review.googlesource.com/5806588


### ap...@google.com (2024-08-23)

Project: v8/v8
Branch: refs/branch-heads/12.9

commit 08be14133a666015289e9768e576e76ce1964aa1
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Tue Aug 20 16:26:39 2024

    Merged: [turbofan] Handle Type::None() in SameValue
    
    Bug: chromium:351865302
    (cherry picked from commit f784b0b05be96cda5b769a3df92fc3c012657166)
    
    Change-Id: I8d3319b0bd131d9321033a2f413c84ec1bfb42ab
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5803048
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.9@{#6}
    Cr-Branched-From: 64a21d7ad7fca1ddc73a9264132f703f35000b69-refs/heads/12.9.202@{#1}
    Cr-Branched-From: da4200b2cfe6eb1ad73c457ed27cf5b7ff32614f-refs/heads/main@{#95679}

M       src/compiler/operation-typer.cc

https://chromium-review.googlesource.com/5803048


### pe...@google.com (2024-08-23)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ni...@chromium.org (2024-08-23)

This code that was broken here has been around for many years (seems at least 6+ years) and is not related to any features merged lately. My guess is that we have never discovered this so far because it requires an extremely specific input program to reproduce.

### sp...@google.com (2024-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
baseline report of memory corruption in a sandboxed process / renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-29)

Congratulations CFF! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-09-18)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### pe...@google.com (2024-09-18)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### pe...@google.com (2024-09-18)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### pe...@google.com (2024-11-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### pe...@google.com (2025-03-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2025-03-12)

1. <https://crrev.com/c/5827958> (<https://crrev.com/c/5701134> isn't applicable to 127)
2. Low, no conflicts
3. 128, 129
4. Yes

### dx...@google.com (2025-03-17)

Project: v8/v8  

Branch: refs/branch-heads/12.6  

Author: Nico Hartmann [nicohartmann@chromium.org](mailto:nicohartmann@chromium.org)  

Link:      <https://chromium-review.googlesource.com/5827958>

[M126-LTS][turbofan] Handle Type::None() in SameValue

---


Expand for full commit details
```
     
    (cherry picked from commit f784b0b05be96cda5b769a3df92fc3c012657166) 
     
    Bug: chromium:351865302 
    Change-Id: Ibab11d8a68fe7c55113abf31c090fd66b3ff0542 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5797195 
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org> 
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
    Auto-Submit: Nico Hartmann <nicohartmann@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#95728} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5827958 
    Reviewed-by: Thibaud Michaud <thibaudm@chromium.org> 
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/12.6@{#94} 
    Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2} 
    Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

```

---

Files:

- M `src/compiler/operation-typer.cc`

---

Hash: c34adcefd17673a7fd67975436e6c708937cd0fe  

Date:  Tue Aug 20 14:26:39 2024


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/351865302)*
