# Security: Signal SIGSEGV in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [329130358](https://issues.chromium.org/issues/329130358) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>Runtime, Infra>Client>V8 |
| **Platforms** | Linux, Mac |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ah...@chromium.org |
| **Created** | 2024-03-12 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 92403
    - link: https://crrev.com/6d26d2b5f88fbb3e3ea7020c2ec16e47ed1aceb6 
- Commit Message

```
commit 6d26d2b5f88fbb3e3ea7020c2ec16e47ed1aceb6
Author: Andreas Haas <ahaas@chromium.org>
Date:   Mon Feb 19 13:52:47 2024 +0100

    [wasm][fuzzing] Add jit_fuzzing implication for wasm
    
    R=saelo@chromium.org
    
    Change-Id: Icf7507797e62cd9956098394a070bdee2328b914
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5300094
    Commit-Queue: Andreas Haas <ahaas@chromium.org>
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Reviewed-by: Samuel Groß <saelo@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92403}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-92762/d8 --expose-gc --jit-fuzzing --wasm-staging poc.js
# OUTPUT ==============================================================
Received signal 11 <unknown> 000000000000

==== C stack trace ===============================

 [0x7f048d36b963]
 [0x7f048d36b8b2]
 [0x7f0487642520]
 [0x1d295d3e5915]
[end of stack trace]

```

## Other
Please note to include the flags `--expose-gc --jit-fuzzing --wasm-staging` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.4.0 - 12.4.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-92762.zip
2. Run: `d8 --expose-gc --jit-fuzzing --wasm-staging poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)    


## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 699 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-03-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5974772218789888.

### ki...@gmail.com (2024-03-14)

Please impot test/mjsunit/wasm/wasm-module-builder.js and re-run clusterfuzz

### ja...@chromium.org (2024-03-14)

Thanks for pointing that out. I'll try again and include that file.

In the mean time, I'm setting a provisional severity of High (S1), and a Found In of the current Extended Stable: 122.

Adding the current v8 shepherd for further triage.

### cl...@appspot.gserviceaccount.com (2024-03-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4683893570994176.

### ki...@gmail.com (2024-03-14)

It seems there may still be issues with the sample you uploaded to ClusterFuzz. Could you try reproducing it locally to investigate further?



### ja...@chromium.org (2024-03-14)

Hi, yes, I was able to reproduce locally on Linux using the steps you provided. cffsmith@ should be able to add more information when they take a look.

I'll try one more time with clusterfuzz

### cl...@appspot.gserviceaccount.com (2024-03-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5133404613312512.

### 24...@project.gserviceaccount.com (2024-03-15)

Detailed Report: https://clusterfuzz.com/testcase?key=5133404613312512

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: Segv on unknown address
Crash Address: 
Crash State:
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  Builtins_JSEntry
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=92402:92403

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5133404613312512

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2024-03-15)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### pe...@google.com (2024-03-15)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-03-15)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cf...@google.com (2024-03-18)

ahaas@, could you PTAL?

### ah...@chromium.org (2024-03-18)

The repro is quite simple, actually. It calls a WebAssembly.Function from WebAssembly with `ref.call`. The WebAssembly.Function wraps a JavaScript function that triggers a GC.  The repro runs with --jit-fuzzing, which in this case means that the wasm-to-js wrapper triggers tier-up already with the first call. Note that the tier-up gets triggered synchronously at the beginning of the first call to the wasm-to-js wrapper, but the optimized wrapper only gets used at the second call of the wasm-to-js wrapper. 

There seems to be missing something in the GC support of `WasmInternalFunction`. Before the GC the `code` field is set correctly, but after the GC it is invalid. The tier up of the wasm-to-js wrapper seems to matter, because without the tier up the `code` field seems to be preserved. But with the tier up, the `code` field references the generic wasm-to-js builtin before tier up, the optimized wasm-to-js wrapper after tier-up, and an invalid value after the GC.

### ap...@google.com (2024-03-18)

Project: v8/v8
Branch: main

commit b93975a48c722c2e5fe9b39437738eb2e23dac74
Author: Andreas Haas <ahaas@chromium.org>
Date:   Mon Mar 18 15:25:15 2024

    [wasm][gc] Scan the code field of the WasmInternalFunction
    
    The code field in the WasmInternalFunction is a code pointer since
    https://crrev.com/c/5110559, so it has to be scanned explicitly.
    
    Bug: 329130358
    Change-Id: Ifc7a7cddb245e46fb9c006e560073a8d7ac65389
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5374907
    Commit-Queue: Andreas Haas <ahaas@chromium.org>
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92878}

M       src/objects/objects-body-descriptors-inl.h
A       test/mjsunit/regress/wasm/regress-329130358.js

https://chromium-review.googlesource.com/5374907


### pe...@google.com (2024-03-19)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=329130358&entry.958145677=Linux, Mac&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>API, Blink>JavaScript>Runtime, Infra>Client>V8&entry.975983575=ahaas@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

### pe...@google.com (2024-03-19)

This is sufficiently serious that it should be merged to extended stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M122. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M123. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: M122 is already shipping to stable.


Merge review required: M123 is already shipping to stable.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [122, 123].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### ah...@chromium.org (2024-03-20)

1. https://chromium-review.googlesource.com/c/v8/v8/+/5374907
2. Yes, in 125.0.6368.0
3. No
4. No
5. No

### pe...@google.com (2024-03-20)

This is sufficiently serious that it should be merged to extended stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M122. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M123. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to dev. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M124. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: M122 is already shipping to stable.


Merge review required: M123 is already shipping to stable.


Merge approved: your change passed merge requirements and is auto-approved for M124. Please go ahead and merge the CL to branch 6367 (refs/branch-heads/6367) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [122, 123, 124].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### ah...@chromium.org (2024-03-21)

1. https://chromium-review.googlesource.com/c/v8/v8/+/5374907
2. Yes, in 125.0.6368.0
3. No
4. No
5. No

### ap...@google.com (2024-03-21)

Project: v8/v8
Branch: refs/branch-heads/12.4

commit 2a2e7a8b0a02a8211902a61eb588d2e05aa1c3a6
Author: Andreas Haas <ahaas@chromium.org>
Date:   Mon Mar 18 15:25:15 2024

    Merged: [wasm][gc] Scan the code field of the WasmInternalFunction
    
    The code field in the WasmInternalFunction is a code pointer since
    https://crrev.com/c/5110559, so it has to be scanned explicitly.
    
    Bug: 329130358
    
    (cherry picked from commit b93975a48c722c2e5fe9b39437738eb2e23dac74)
    
    Change-Id: If179456d54b3790593c33ed5a6ac4dc2c24b631a
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5378293
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Commit-Queue: Andreas Haas <ahaas@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.4@{#6}
    Cr-Branched-From: 309640da62fae0485c7e4f64829627c92d53b35d-refs/heads/12.4.254@{#1}
    Cr-Branched-From: 5dc24701432278556a9829d27c532f974643e6df-refs/heads/main@{#92862}

M       src/objects/objects-body-descriptors-inl.h
A       test/mjsunit/regress/wasm/regress-329130358.js

https://chromium-review.googlesource.com/5378293


### am...@google.com (2024-03-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-27)

Congratulations! The Chrome VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us!

### am...@chromium.org (2024-03-27)

M123 Stable and M122 Extended Stable merges approved for <https://crrev.com/c/5378293>
please merge to 12.3-lkgr and 12.2-lkgr by EOD tomorrow, Thursday 28 March so this fix can be included in the next Stable and Extended Stable security updates -- thank you!

### pe...@google.com (2024-04-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pb...@google.com (2024-04-01)

Please find the merges to M123 and M122 below

12.3: <https://chromium-review.googlesource.com/c/v8/v8/+/5408910>
12.2: <https://chromium-review.googlesource.com/c/v8/v8/+/5410311>

### pe...@google.com (2024-04-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/329130358)*
