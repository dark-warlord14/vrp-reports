# register assign error with jit

| Field | Value |
|-------|-------|
| **Issue ID** | [40062384](https://issues.chromium.org/issues/40062384) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>Runtime |
| **Platforms** | Windows |
| **Reporter** | 5n...@gmail.com |
| **Assignee** | pa...@google.com |
| **Created** | 2022-12-25 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

build flag:  

gn gen out/x64\_release --args="target\_cpu="x64" symbol\_level=2 is\_debug=false is\_component\_build=false v8\_enable\_backtrace = true v8\_enable\_disassembler=true v8\_enable\_object\_print=true"

environment:  

ubuntu 20.04 5.15.0-56-generic

run with:  

d8 --allow-natives-syntax poc.js

run result:  

d8 crash in jit assembly

**Problem Description:**  

This is a register assign error issue with v8,attachment turbo-opt-0.json is the turbo json result of "--trace-turbo" flag.  

d8 crash here:

B1,34:  

1b3 movl rcx,0x50  

1b8 push rcx  

1b9 movl rax,0x1  

1be REX.W movq rbx,0x55fb48c03300  

1c8 REX.W movq rsi,0x2f9c00183bc1 ;; object: 0x2f9c00183bc1 <NativeContext[273]>  

1d2 call 0x55fadfed9f00 (CEntry\_Return1\_ArgvOnStack\_NoBuiltinExit) ;; near builtin entry

**Additional Comments:**

\*\*Chrome version: \*\* 108.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [jit_crash3.js](attachments/jit_crash3.js) (text/plain, 484 B)
- [turbo-opt-0.json](attachments/turbo-opt-0.json) (text/plain, 1.9 MB)

## Timeline

### [Deleted User] (2022-12-25)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-12-26)

Reassigned to thibaudm@ (current V8 security sheriff) for triage. Thanks!

### [Deleted User] (2022-12-26)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-01-03)

I am not able to reproduce with V8 10.8-lkgr. Could you confirm the exact V8 version that you are using, and check whether this still reproduces?

### 5n...@gmail.com (2023-01-03)

This may reproduce with 70bdadce8f79e9ab12b9e8972803aea708fd36e7,with ubuntu 20.04,but I didn't verify this.
I also can't reproduce with v8 lattest head.

### th...@chromium.org (2023-01-04)

Thanks! I can reproduce at this commit. I'll run a bisect.

### cl...@chromium.org (2023-01-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4848542882660352.

### th...@chromium.org (2023-01-04)

It does not reproduce with ClusterFuzz for some reason.
I ran the bisect locally and found this commit:
4055670: [turbofan] Inline BigInt Constructor for Integral32 input | https://chromium-review.googlesource.com/c/v8/v8/+/4055670

Qifan, can you take a look? I can reproduce on ToT.


### pa...@google.com (2023-01-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-04)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>API Blink>JavaScript>Runtime]

### gi...@appspot.gserviceaccount.com (2023-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/63134966fda12fb4dfb51413d545aa0ea7c67db5

commit 63134966fda12fb4dfb51413d545aa0ea7c67db5
Author: Qifan Pan <panq@google.com>
Date: Wed Jan 04 13:16:52 2023

[turbofan] Fix a bug of SignedBigInt64 in representation changer

The expected behavior of the optimized code is deoptimizing when using a BigInt
as an index and throwing an error (from CheckedTaggedToInt64).
The representation changer tries to insert conversions for this case where

- The output node is represented in Word64 (SignedBigInt64)
- The use info is CheckedSigned64AsWord64

The representation changer first rematerializes the output node to
TaggedPointer because the type check is not BigInt. Then it falls wrongly to
the branch where the output representation is TaggedPointer, the output type is
SignedBigInt64 in GetWord64RepresentationFor.

Bug: v8:9407, chromium:1403574, chromium:1404607
Change-Id: I9d7ef4c94c1dc0aa3b4f49871ec35ef0877efc24
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4135876
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Qifan Pan <panq@google.com>
Cr-Commit-Position: refs/heads/main@{#85094}

[modify] https://crrev.com/63134966fda12fb4dfb51413d545aa0ea7c67db5/test/cctest/compiler/test-representation-change.cc
[modify] https://crrev.com/63134966fda12fb4dfb51413d545aa0ea7c67db5/src/compiler/representation-change.cc
[add] https://crrev.com/63134966fda12fb4dfb51413d545aa0ea7c67db5/test/mjsunit/regress/regress-1404607.js


### cl...@chromium.org (2023-01-04)

ClusterFuzz testcase 6226474523885568 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=85093:85094

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### pa...@google.com (2023-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-05)

Merge approved: your change passed merge requirements and is auto-approved for M110. Please go ahead and merge the CL to branch 5481 (refs/branch-heads/5481) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b84a257571d3c1ca77bfa6898fb96003d2138253

commit b84a257571d3c1ca77bfa6898fb96003d2138253
Author: Qifan Pan <panq@google.com>
Date: Wed Jan 04 13:16:52 2023

[turbofan] Fix a bug of SignedBigInt64 in representation changer

The expected behavior of the optimized code is deoptimizing when using a BigInt
as an index and throwing an error (from CheckedTaggedToInt64).
The representation changer tries to insert conversions for this case where

- The output node is represented in Word64 (SignedBigInt64)
- The use info is CheckedSigned64AsWord64

The representation changer first rematerializes the output node to
TaggedPointer because the type check is not BigInt. Then it falls wrongly to
the branch where the output representation is TaggedPointer, the output type is
SignedBigInt64 in GetWord64RepresentationFor.

(cherry picked from commit 63134966fda12fb4dfb51413d545aa0ea7c67db5)

Bug: v8:9407, chromium:1403574, chromium:1404607
Change-Id: I9d7ef4c94c1dc0aa3b4f49871ec35ef0877efc24
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4135876
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Qifan Pan <panq@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#85094}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4138619
Cr-Commit-Position: refs/branch-heads/11.0@{#12}
Cr-Branched-From: 06097c6f0c5af54fd5d6965d37027efb72decd4f-refs/heads/11.0.226@{#1}
Cr-Branched-From: 6bf3344f5d9940de1ab253f1817dcb99c641c9d3-refs/heads/main@{#84857}

[modify] https://crrev.com/b84a257571d3c1ca77bfa6898fb96003d2138253/src/compiler/representation-change.cc
[modify] https://crrev.com/b84a257571d3c1ca77bfa6898fb96003d2138253/test/cctest/compiler/test-representation-change.cc
[add] https://crrev.com/b84a257571d3c1ca77bfa6898fb96003d2138253/test/mjsunit/regress/regress-1404607.js


### [Deleted User] (2023-01-09)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@google.com (2023-01-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6bade738eaae97dbb30df405c98e25c0cef1cbed

commit 6bade738eaae97dbb30df405c98e25c0cef1cbed
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jan 09 19:13:29 2023

Roll v8 11.0 from 06097c6f0c5a to 172c32fa27f5 (17 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/06097c6f0c5a..172c32fa27f5

2023-01-09 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.9
2023-01-09 alexschulze@chromium.org [builtins] Warn only for invalid PGO profiles
2023-01-09 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.8
2023-01-09 leszeks@chromium.org [builtins] Update builtins PGO profiles for M110 (re-try)
2023-01-09 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.7
2023-01-09 panq@google.com [turbofan] Fix a bug of SignedBigInt64 in representation changer
2023-01-09 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.6
2023-01-09 clemensb@chromium.org Merged: [wasm][streaming] Avoid UAF after context disposal
2023-01-05 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.5
2023-01-05 sky@chromium.org moves use_libm_trig_functions flag to right spot
2023-01-03 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.4
2023-01-03 panq@google.com [turbofan] Fix bugs of BigInt constructor inlining
2022-12-21 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.3
2022-12-21 marja@chromium.org Merged: [rab/gsab] Fix ValueSerializer error handling
2022-12-15 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.2
2022-12-15 alexschulze@chromium.org [builtins] Update builtins PGO profiles for M110
2022-12-15 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.1

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-0
Please CC v8-waterfall-sheriff@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.0: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m110: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1400897,chromium:1402139,chromium:1403531,chromium:1403574,chromium:1404607
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I1161b3c3b29b0283f4928d0f95ef7af86dd08922
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4147748
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5481@{#182}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/6bade738eaae97dbb30df405c98e25c0cef1cbed/DEPS


### am...@google.com (2023-01-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-18)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1403574?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>API, Blink>JavaScript>Runtime]
[Monorail mergedwith: crbug.com/chromium/1404607]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062384)*
