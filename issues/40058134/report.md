# Security: Debug Check failed in HAS_WEAK_HEAP_OBJECT_TAG

| Field | Value |
|-------|-------|
| **Issue ID** | [40058134](https://issues.chromium.org/issues/40058134) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Linux, Mac |
| **Reporter** | vu...@gmail.com |
| **Assignee** | pt...@chromium.org |
| **Created** | 2021-12-06 |
| **Bounty** | $5,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

##################poc###################  

function main() {  

for (let i = 655; i !== 1; i = i / 3) {  

i %= 2;  

const c = { "b": 1, "a":1, "c": 1, "d": 1 };  

eval();  

}  

}  

main();

# 

# Fatal error in ../../src/objects/tagged-impl-inl.h, line 212

# Debug check failed: !HAS\_WEAK\_HEAP\_OBJECT\_TAG(ptr\_).

# 

# 

# 

#FailureMessage Object: 0x7ffeaf835890  

==== C stack trace ===============================

```
./d8(+0x4c2f23) [0x56517bc42f23]  
./d8(+0x4c276b) [0x56517bc4276b]  
./d8(+0x4baf78) [0x56517bc3af78]  
./d8(+0x4bab75) [0x56517bc3ab75]  
./d8(+0x8bae6c) [0x56517c03ae6c]  
./d8(+0x8ba982) [0x56517c03a982]  
./d8(+0x8ac8da) [0x56517c02c8da]  
./d8(+0x8ac6f7) [0x56517c02c6f7]  
./d8(+0x8ac41a) [0x56517c02c41a]  
./d8(+0x4c3bfd) [0x56517bc43bfd]  
./d8(+0x4c42b3) [0x56517bc442b3]  
./d8(+0x8af2e8) [0x56517c02f2e8]  
./d8(+0x7e4e54) [0x56517bf64e54]  
./d8(+0x7e1c80) [0x56517bf61c80]  
./d8(+0x7dee23) [0x56517bf5ee23]  
./d8(+0x7f02f4) [0x56517bf702f4]  
./d8(+0x7f0415) [0x56517bf70415]  
./d8(+0x79d45a) [0x56517bf1d45a]  
./d8(+0xddbe51) [0x56517c55be51]  
[0x17ad07ede338]  

```

Trace/breakpoint trap (core dumped)

**VERSION**  

v8 f738a4a5e67095a5294c3a5e060caa8f56c67f1e

**REPRODUCTION CASE**  

./d8 poc.js

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Timeline

### [Deleted User] (2021-12-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-12-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5695763554041856.

### cl...@chromium.org (2021-12-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-12-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-12-07)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### cl...@chromium.org (2021-12-07)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/863bc2b88a88caef91ec1afad528ef76d3749f54 ([turbofan] Improve StoreStoreElimination).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2021-12-07)

Detailed Report: https://clusterfuzz.com/testcase?key=5695763554041856

Fuzzer: None
Job Type: linux32_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_)) in tagged-impl.h
  V8_Dcheck
  v8::internal::Object::VerifyPointer
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux32_asan_d8_dbg&range=78229:78230

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5695763554041856

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### pt...@chromium.org (2021-12-07)

Thanks for the report!
Reverting the culprit CL right now until I know how to fix the issue.

[Monorail components: -Blink>JavaScript>Runtime Blink>JavaScript>Compiler>Turbofan]

### gi...@appspot.gserviceaccount.com (2021-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/41b9cd7fd4d00eea1ad140114ba56ccfcf344255

commit 41b9cd7fd4d00eea1ad140114ba56ccfcf344255
Author: Patrick Thier <pthier@chromium.org>
Date: Tue Dec 07 09:58:09 2021

Revert "[turbofan] Improve StoreStoreElimination"

This reverts commit 863bc2b88a88caef91ec1afad528ef76d3749f54.

Reason for revert: https://crbug.com/1276923

Original change's description:
> [turbofan] Improve StoreStoreElimination
>
> Previously, StoreStoreElimination handled allocations as
> "can observe anything". This is pretty conservative and prohibits
> elimination of repeated double stores to the same field.
> With this CL allocations are changed to "observes initializing or
> transitioning stores".
> This way it is guaranteed that initializing stores to a freshly created
> object or stores that are part of a map transition are not eliminated
> before allocations (that can trigger GC), but allows elimination of
> non-initializing, non-transitioning, unobservable stores in the
> presence of allocations.
>
> Bug: v8:12200
> Change-Id: Ie1419696b9c8cb7c39aecf38d9f08102177b2c0f
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3295449
> Commit-Queue: Patrick Thier <pthier@chromium.org>
> Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
> Reviewed-by: Maya Lekova <mslekova@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#78230}

Bug: chromium:1276923
Change-Id: I43dc3572ce1ef1fda42b7551ce8210d9f03e36ca
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3318666
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Maya Lekova <mslekova@chromium.org>
Commit-Queue: Patrick Thier <pthier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#78277}

[modify] https://crrev.com/41b9cd7fd4d00eea1ad140114ba56ccfcf344255/src/compiler/simplified-operator.cc
[modify] https://crrev.com/41b9cd7fd4d00eea1ad140114ba56ccfcf344255/src/compiler/simplified-operator.h
[modify] https://crrev.com/41b9cd7fd4d00eea1ad140114ba56ccfcf344255/src/compiler/store-store-elimination.cc
[delete] https://crrev.com/3902ffbba425d23696b8d4f9ea96f924e9e84ff2/test/mjsunit/compiler/regress-store-store-elim.js
[modify] https://crrev.com/41b9cd7fd4d00eea1ad140114ba56ccfcf344255/src/compiler/effect-control-linearizer.cc


### cl...@chromium.org (2021-12-07)

ClusterFuzz testcase 5695763554041856 is verified as fixed in https://clusterfuzz.com/revisions?job=linux32_asan_d8_dbg&range=78276:78277

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### vu...@gmail.com (2021-12-08)

OK, It can't be re-triaged.

### [Deleted User] (2021-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e926da459296ad095e98c69b180b2347b93078fc

commit e926da459296ad095e98c69b180b2347b93078fc
Author: Patrick Thier <pthier@chromium.org>
Date: Mon Dec 13 08:49:33 2021

Reland "[turbofan] Improve StoreStoreElimination"

This is a reland of 863bc2b88a88caef91ec1afad528ef76d3749f54

Diff to original:
- Don't eliminate GC observable stores that were temporarily
  unobservable during traversal.
- Skip the previously added test for single-generation
- Add new test

Original change's description:
> [turbofan] Improve StoreStoreElimination
>
> Previously, StoreStoreElimination handled allocations as
> "can observe anything". This is pretty conservative and prohibits
> elimination of repeated double stores to the same field.
> With this CL allocations are changed to "observes initializing or
> transitioning stores".
> This way it is guaranteed that initializing stores to a freshly created
> object or stores that are part of a map transition are not eliminated
> before allocations (that can trigger GC), but allows elimination of
> non-initializing, non-transitioning, unobservable stores in the
> presence of allocations.
>
> Bug: v8:12200
> Change-Id: Ie1419696b9c8cb7c39aecf38d9f08102177b2c0f
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3295449
> Commit-Queue: Patrick Thier <pthier@chromium.org>
> Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
> Reviewed-by: Maya Lekova <mslekova@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#78230}

Bug: v8:12200, chromium:1276923, v8:12477
Change-Id: Ied45ee28ac12b370f7b232d2d338f93e10fea6b4
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3320460
Reviewed-by: Maya Lekova <mslekova@chromium.org>
Commit-Queue: Patrick Thier <pthier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#78349}

[add] https://crrev.com/e926da459296ad095e98c69b180b2347b93078fc/test/mjsunit/regress/regress-crbug-1276923.js
[modify] https://crrev.com/e926da459296ad095e98c69b180b2347b93078fc/src/compiler/simplified-operator.h
[modify] https://crrev.com/e926da459296ad095e98c69b180b2347b93078fc/src/compiler/simplified-operator.cc
[modify] https://crrev.com/e926da459296ad095e98c69b180b2347b93078fc/src/compiler/store-store-elimination.cc
[add] https://crrev.com/e926da459296ad095e98c69b180b2347b93078fc/test/mjsunit/compiler/regress-store-store-elim.js
[modify] https://crrev.com/e926da459296ad095e98c69b180b2347b93078fc/src/compiler/effect-control-linearizer.cc
[modify] https://crrev.com/e926da459296ad095e98c69b180b2347b93078fc/test/mjsunit/mjsunit.status


### [Deleted User] (2022-03-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-03-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-23)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Also please accept our sincere apologies in the delay in getting a reward decision to you, as this issue appears to have slipped through security triage and was without a security severity so in our VRP backlog. Thank you for your efforts and reporting this issue to us. 

### [Deleted User] (2022-03-24)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### is...@google.com (2022-03-25)

This issue was migrated from crbug.com/chromium/1276923?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058134)*
