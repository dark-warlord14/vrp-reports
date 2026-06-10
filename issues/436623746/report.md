# Signal SIGABRT in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [436623746](https://issues.chromium.org/issues/436623746) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2025-08-06 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 101399
    - link: https://crrev.com/aff5adff76188541e7eb092e8ab3e6c97c50541d
- Commit Message

```
commit aff5adff76188541e7eb092e8ab3e6c97c50541d
Author: Darius Mercadier <dmercadier@chromium.org>
Date:   Mon Jul 14 16:39:55 2025 +0200

    [turboshaft] re-enable Late Load Elimination verification
    
    Fixed: 425754604
    Bug: 404257893
    Change-Id: I8ae87d2a89e5745bcf4aa41d209e436b40c62b50
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6734503
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#101399}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-101767/d8 --fuzzing --turboshaft-verify-load-elimination poc.js
# OUTPUT ==============================================================
abort: Turboshaft's load elimination wrongly eliminated a Load

==== JS stack trace =========================================

    0: ExitFrame [pc: 0x7f28ca1c6e3d]
    1: f1 [0x156600065179] [./output_poc.js:~1] [pc=0x7f28e000123d](this=0x15660004c3b5 <JSGlobalProxy>#0#)
    2: /* anonymous */ [0x156600065119] [./output_poc.js:18] [bytecode=0x2c600100049 offset=22](this=0x15660004c3b5 <JSGlobalProxy>#0#)
    3: InternalFrame [pc: 0x7f28c9c45927]
    4: EntryFrame [pc: 0x7f28c9c4566b]

==== Details ================================================

[0]: ExitFrame [pc: 0x7f28ca1c6e3d]
[1]: f1 [0x156600065179] [./output_poc.js:~1] [pc=0x7f28e000123d](this=0x15660004c3b5 <JSGlobalProxy>#0#) {
// optimized frame
--------- s o u r c e   c o d e ---------
function f1() {\x0a  for (var v8 = 0; v8 < 4000; v8++) {\x0a    v16 = f2(6);\x0a    v8 % -13 ? v18 = v16 + "@mac.com" : v18 = v16 + "(at)mac.com";\x0a    var v9 = /^[a-zA-Z0-9\\-\\._]+@[a-zA-Z0-9\\-_]+(\\.?[a-zA-Z0-9\\-_]*)\\.[a-zA-Z]{2,3}$/;\x0a    if (v9.test(v18)) {\x0a      var v10 = v18 + " appears to be a valid email addr...

-----------------------------------------
}
[2]: /* anonymous */ [0x156600065119] [./output_poc.js:18] [bytecode=0x2c600100049 offset=22](this=0x15660004c3b5 <JSGlobalProxy>#0#) {
  // expression stack (top to bottom)
  [03] : 0x15660004c3b5 <JSGlobalProxy>#0#
  [02] : 0x156600065119 <JSFunction (sfi = 0x156600064f39)>#1#
  [01] : 0x156600065179 <JSFunction f1 (sfi = 0x156600065015)>#2#
  [00] : 0x156600000011 <undefined>
--------- s o u r c e   c o d e ---------
function f1() {\x0a  for (var v8 = 0; v8 < 4000; v8++) {\x0a    v16 = f2(6);\x0a    v8 % -13 ? v18 = v16 + "@mac.com" : v18 = v16 + "(at)mac.com";\x0a    var v9 = /^[a-zA-Z0-9\\-\\._]+@[a-zA-Z0-9\\-_]+(\\.?[a-zA-Z0-9\\-_]*)\\.[a-zA-Z]{2,3}$/;\x0a    if (v9.test(v18)) {\x0a      var v10 = v18 + " appears to be a valid...

-----------------------------------------
}

[3]: InternalFrame [pc: 0x7f28c9c45927]
[4]: EntryFrame [pc: 0x7f28c9c4566b]
-- ObjectCacheKey --

 #0# 0x15660004c3b5: 0x15660004c3b5 <JSGlobalProxy>
 #1# 0x156600065119: 0x156600065119 <JSFunction (sfi = 0x156600064f39)>
 #2# 0x156600065179: 0x156600065179 <JSFunction f1 (sfi = 0x156600065015)>
=====================

Received signal 6

==== C stack trace ===============================

/tmp/d8-linux-debug-v8-component-101767/libv8_libbase.so(_ZN2v84base5debug10StackTraceC1Ev+0x13)[0x7f28c79f5823]
/tmp/d8-linux-debug-v8-component-101767/libv8_libbase.so(+0x4c77f)[0x7f28c79f577f]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x7f28c7242520]
/lib/x86_64-linux-gnu/libc.so.6(pthread_kill+0x12c)[0x7f28c72969fc]
/lib/x86_64-linux-gnu/libc.so.6(raise+0x16)[0x7f28c7242476]
/lib/x86_64-linux-gnu/libc.so.6(abort+0xd3)[0x7f28c72287f3]
/tmp/d8-linux-debug-v8-component-101767/libv8_libbase.so(_ZN2v84base2OS5AbortEv+0x31)[0x7f28c79f2e01]
/tmp/d8-linux-debug-v8-component-101767/libv8.so(+0x46ad94b)[0x7f28cc0ad94b]
/tmp/d8-linux-debug-v8-component-101767/libv8.so(_ZN2v88internal13Runtime_AbortEiPmPNS0_7IsolateE+0xa0)[0x7f28cc0ad490]
/tmp/d8-linux-debug-v8-component-101767/libv8.so(+0x27c6e3d)[0x7f28ca1c6e3d]
[end of stack trace]

```

## Other
Please note to include the flags `--fuzzing --turboshaft-verify-load-elimination` for clusterfuzz classification.

VERSION
Tested on v8 version: 14.0.0 - 14.1.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-101767.zip
2. Run: `d8 --fuzzing --turboshaft-verify-load-elimination poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy) and Nan Wang (@eternalsakura13)

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 565 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-08-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6331529651224576.

### za...@google.com (2025-08-06)

[security shepherd]
Hi ishell@ can you help take a look at this v8 bug? I couldn't reproduce it using fuzzer. Thanks.

### cl...@appspot.gserviceaccount.com (2025-08-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5249649950523392.

### is...@chromium.org (2025-08-07)

Thank you for the report!

The issue reproduces on ToT on x64.debug build approximately every 10th run.

### cl...@appspot.gserviceaccount.com (2025-08-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4564027598372864.

### ch...@google.com (2025-08-07)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2025-08-08)

Project: v8/v8  

Branch:  main  

Author:  Nico Hartmann [nicohartmann@chromium.org](mailto:nicohartmann@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6829829>

[turboshaft] Fix LateLoadElimination bug around String maps

---


Expand for full commit details
```
     
    Bug: 436623746 
    Change-Id: Ic64eb77a4575374e96bb25652fe01cf09cd29a98 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6829829 
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101815}

```

---

Files:

- M `src/compiler/turboshaft/late-load-elimination-reducer.cc`
- M `src/compiler/turboshaft/late-load-elimination-reducer.h`

---

Hash: [19c0bf473e65931e71035533ffdb040989614362](http://crrev.com/19c0bf473e65931e71035533ffdb040989614362)  

Date: Fri Aug 8 14:56:12 2025


---

### ki...@gmail.com (2025-08-10)

Can you mark this bug as fixed?

### ch...@google.com (2025-08-11)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M138. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [138, 139, 140].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sp...@google.com (2025-08-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-08-15)

<https://crrev.com/c/6829829> approved for merge to M140 beta / please merge this fix to 14.0 at your earliest convenience

### dx...@google.com (2025-08-18)

Project: v8/v8  

Branch:  refs/branch-heads/14.0  

Author:  Nico Hartmann [nicohartmann@chromium.org](mailto:nicohartmann@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6850493>

Merged: [turboshaft] Fix LateLoadElimination bug around String maps

---


Expand for full commit details
```
     
    Bug: 436623746 
    (cherry picked from commit 19c0bf473e65931e71035533ffdb040989614362) 
     
    Change-Id: Ia95442dca758a6bfecdbecbb14bbcad926cdc5f8 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6850493 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.0@{#4} 
    Cr-Branched-From: 4ec2f43a229069d6124c88527ee7bb9cc642edc3-refs/heads/14.0.365@{#1} 
    Cr-Branched-From: a88b57016d5caf9b5ed8f07b7d2f3e729520b8b5-refs/heads/main@{#101731}

```

---

Files:

- M `src/compiler/turboshaft/late-load-elimination-reducer.cc`
- M `src/compiler/turboshaft/late-load-elimination-reducer.h`

---

Hash: [0652ef4bf0ab62b6453d869b5e544c93d6e0b560](https://chromiumdash.appspot.com/commit/0652ef4bf0ab62b6453d869b5e544c93d6e0b560)  

Date: Fri Aug 8 14:56:12 2025


---

### pe...@google.com (2025-08-18)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2025-08-20)

Labelled as not applicable for M132-LTS and M138-LTS, because the suspected CL[1] was not included in M132 and M138.

[1] <https://chromium-review.googlesource.com/c/v8/v8/+/6734503>

### jk...@chromium.org (2025-08-22)

#15: To clarify, the "suspected" CL enabled the *verifier* that detected the bug. The bug itself is much older, it probably dates back to last year:

```
commit 3ecb8552efcc92b7a443b10939d99e04d5ba4cd6
Author: Darius Mercadier <dmercadier@chromium.org>
Date:   Wed May 8 10:10:29 2024 +0200

    [turboshaft] Enable late load elimination by default

```

### qk...@google.com (2025-08-25)

#16: Thank you for correcting me. If so, we need to merge back the fix to M132 and M138.

### dm...@chromium.org (2025-09-02)

I don't think that this is a security issue.

In the repro, we start with a 1-byte ConsString, we load its map (for a CheckString), then the GC runs and turns it into a 1-byte SeqString, and then we reload the map to look at the instance type to figure out if it's a 1-byte or 2-byte string. Load elimination eliminates the reloading of the map, and just uses the original map to figure out if it's a 1-byte or a 2-byte string. This isn't wrong, since a GC cannot turn a 1-byte string into a 2-byte string (and vice versa). So, in the repro, not reloading the map is a correct optimization, and the verifier is just wrongly complaining (crashing).

In general, we are aware that Late Load Elimination maybe have invalid (outdated) maps for strings, but it should never be an issue because of how string maps are used. I think that we have 3 operations that should load string maps:

- CheckString. For CheckString, the shape doesn't matter at all, so the fact that the map might be outdated doesn't matter since it will remain a string map.
- StringAt. This one cares about the exact shape of the string, but it is lowered to a loop that contains a runtime call, which will prevent all kind of load elimination of the LoadMap. So it's safe.
- NewConsString. It only cares about whether a string is 1-byte or 2-byte. A GC cannot change that (only internalization can I think), so working with an outdated map is safe.

So, I'm downgrading this bug to type Bug instead of Vulnerability.

I'll upload a fix to the verifier to ignore string maps. This is only a temporary solution though, because the assumption that we don't care about string shapes is a bit brittle and not really checked anywhere. I'll open another Bug to look into finding a robust solution to this.

### dx...@google.com (2025-09-03)

Project: v8/v8  

Branch:  main  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6905293>

[turboshaft] Fix false-positive around strings in Load Elim verifier

---


Expand for full commit details
```
     
    This CL includes a revert of the previous "fix", 
    https://crrev.com/c/6829829, which tuned down load elimination to get 
    rid of the false positive. Now that we know that it was a false 
    positive, we can revert load elimination to its previous state and 
    just fix the verifier instead. 
     
    Fixed: 436623746 
    Change-Id: I38bae084d995985631291946f4ed60c1b00c99b7 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6905293 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org> 
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102216}

```

---

Files:

- M `src/compiler/turboshaft/assembler.h`
- M `src/compiler/turboshaft/late-load-elimination-reducer.cc`
- M `src/compiler/turboshaft/late-load-elimination-reducer.h`
- M `src/compiler/turboshaft/machine-lowering-reducer-inl.h`

---

Hash: [4a2ca5c123ceb14c2cea63f642cc078c4367d040](https://chromiumdash.appspot.com/commit/4a2ca5c123ceb14c2cea63f642cc078c4367d040)  

Date: Wed Sep 3 11:39:05 2025


---

### qk...@google.com (2025-09-05)

Labeling as not-applicable for LTS-138 because the fix seems to require some dependent CLs[1][2][3] to be merged to the M138 branch. So, I'm not sure if it's safe to merge all of them to the LTS branch.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/6632920
[2] https://chromium-review.googlesource.com/c/v8/v8/+/6734503
[3] https://chromium-review.googlesource.com/c/v8/v8/+/6829829

### rz...@google.com (2025-09-09)

Labelling as not applicable for LTS 132 because the bug was a false positive.

### ch...@google.com (2025-11-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/436623746)*
