# DCHECK failure in GetReadOnlyRoots().fixed_cow_array_map() != map() in fixed-array-inl.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40094554](https://issues.chromium.org/issues/40094554) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | du...@microsoft.com |
| **Created** | 2019-04-10 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=4867906201583616

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  GetReadOnlyRoots().fixed_cow_array_map() != map() in fixed-array-inl.h
  v8::internal::FixedArray::set
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=60722:60723

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4867906201583616

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

## Timeline

### cl...@chromium.org (2019-04-10)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/0b1e9ef244c0e9e92bb477938e6de4df5c3ac841 (Add new frozen, sealed packed elements kind).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### sh...@chromium.org (2019-04-11)

[Empty comment from Monorail migration]

### ct...@chromium.org (2019-04-11)

Setting impact and milestone based on the regression range.

### ct...@chromium.org (2019-04-11)

[Empty comment from Monorail migration]

### du...@microsoft.com (2019-04-11)

PoC: 
var a = ['a'];
Object.seal(a);
a[0] = 'b';

PoC: 
var a = [null, 'a'];
Object.seal(a);
a.shift();

### sh...@chromium.org (2019-04-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/56873d9616812f02ced5d26d09c3d5f5a3b207b8

commit 56873d9616812f02ced5d26d09c3d5f5a3b207b8
Author: Z Duong Nguyen-Huu <duongn@microsoft.com>
Date: Fri Apr 12 19:43:39 2019

Handle COW map for sealed, frozen object

Basically, SetPropertyInternal is called without handling COW map.

Improve test coverage as well.

Bug: chromium:951438
Change-Id: Iea8c818ab6a8ddea204f86a9d676a1ea42fd07f0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1562731
Commit-Queue: Z Nguyen-Huu <duongn@microsoft.com>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/master@{#60834}
[modify] https://crrev.com/56873d9616812f02ced5d26d09c3d5f5a3b207b8/src/elements-kind.h
[modify] https://crrev.com/56873d9616812f02ced5d26d09c3d5f5a3b207b8/src/lookup.cc
[modify] https://crrev.com/56873d9616812f02ced5d26d09c3d5f5a3b207b8/src/objects/js-objects.cc
[modify] https://crrev.com/56873d9616812f02ced5d26d09c3d5f5a3b207b8/test/mjsunit/object-freeze.js
[modify] https://crrev.com/56873d9616812f02ced5d26d09c3d5f5a3b207b8/test/mjsunit/object-prevent-extensions.js
[modify] https://crrev.com/56873d9616812f02ced5d26d09c3d5f5a3b207b8/test/mjsunit/object-seal.js


### cl...@chromium.org (2019-04-13)

ClusterFuzz has detected this issue as fixed in range 60833:60834.

Detailed report: https://clusterfuzz.com/testcase?key=4867906201583616

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  GetReadOnlyRoots().fixed_cow_array_map() != map() in fixed-array-inl.h
  v8::internal::FixedArray::set
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=60722:60723
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=60833:60834

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4867906201583616

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-04-13)

ClusterFuzz testcase 4867906201583616 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-04-14)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-04-18)

Congrats! The Panel decided to reward $3,500 for this report!

### aw...@google.com (2019-04-19)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/951438?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094554)*
