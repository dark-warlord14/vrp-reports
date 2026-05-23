# Heap-buffer-overflow in v8::internal::Invoke

| Field | Value |
|-------|-------|
| **Issue ID** | [40086898](https://issues.chromium.org/issues/40086898) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | bm...@chromium.org |
| **Created** | 2017-02-26 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6614862227832832

Fuzzer: decoder_langfuzz
Job Type: linux_asan_chrome_v8_d8
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x622000002c89
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: V8: 43421:43428

Reproducer Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97huhK6ZFLR1AybbA-b8Wa0asAYTadoTHlOmLVmCMU4Upla9fwvQOJtm_T469aOtxwVttXGjmxF1ukjQLfQ7XmxXFGQ0qGTzm-P35iBhtbNcsIlA-QPt6OnuC-XBtHdjG1abUGldk-SyHTQgvY7gUk8YHaBSl6HNGUAMfNr_Dlx6PK2momwtAdSghXnIWCenxbKCFBhBT1O7lfSKAu1a8C96FiSXGHEblmxmPul6Ll2KxPULps50iWu4aky_eHWPGjBQRYbb8AGQpHGrw2RYsrZylbSWZK6xgYh-ZQw18N4ZFZsgts9uFXcp4csBN2sqZnbbFCIBsbfubgxb-7xfd0tzm6ZzZVFVhSCNlTRHIqLCp-4G1k?testcase_id=6614862227832832


Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### sh...@chromium.org (2017-02-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-26)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-02-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-02-26)

This looks like it's triggered by a sort, so I'm suspecting https://codereview.chromium.org/2693043009 from the blame range. Assigning to bmeurer who reviewed the CL and cwhan.tunz@gmail.com who wrote it. Can you please look at this ASAP.

### cw...@gmail.com (2017-02-27)

I don't have a permission to see the testcase.

### cw...@gmail.com (2017-02-27)

seems there are some cases that do not follow strict weak ordering relation in the comparison function of std::sort.

### bm...@chromium.org (2017-02-27)

Being worked on here: https://chromium-review.googlesource.com/c/447036/

### bu...@chromium.org (2017-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/cd3a76d56f544c5c90cd262d2576b7bb1ef04c13

commit cd3a76d56f544c5c90cd262d2576b7bb1ef04c13
Author: Choongwoo Han <cwhan.tunz@gmail.com>
Date: Mon Feb 27 11:41:25 2017

[typedarrays] Fix Out of Bound Access in TypedArraySortFast

Compare function for std::sort should satisfy strict weak ordering
relation.

BUG=chromium:696251

Change-Id: I1c07e3bb1b012fd203bc059a21a75ae0fc61f5ac
Reviewed-on: https://chromium-review.googlesource.com/447036
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Commit-Queue: Peter Marshall <petermarshall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#43446}
[modify] https://crrev.com/cd3a76d56f544c5c90cd262d2576b7bb1ef04c13/src/runtime/runtime-typedarray.cc
[add] https://crrev.com/cd3a76d56f544c5c90cd262d2576b7bb1ef04c13/test/mjsunit/regress/regress-696251.js


### cl...@chromium.org (2017-02-28)

ClusterFuzz has detected this issue as fixed in range 43445:43458.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6614862227832832

Fuzzer: decoder_langfuzz
Job Type: linux_asan_chrome_v8_d8
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x622000002c89
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: V8: 43421:43428
Fixed: V8: 43445:43458

Reproducer Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97huhK6ZFLR1AybbA-b8Wa0asAYTadoTHlOmLVmCMU4Upla9fwvQOJtm_T469aOtxwVttXGjmxF1ukjQLfQ7XmxXFGQ0qGTzm-P35iBhtbNcsIlA-QPt6OnuC-XBtHdjG1abUGldk-SyHTQgvY7gUk8YHaBSl6HNGUAMfNr_Dlx6PK2momwtAdSghXnIWCenxbKCFBhBT1O7lfSKAu1a8C96FiSXGHEblmxmPul6Ll2KxPULps50iWu4aky_eHWPGjBQRYbb8AGQpHGrw2RYsrZylbSWZK6xgYh-ZQw18N4ZFZsgts9uFXcp4csBN2sqZnbbFCIBsbfubgxb-7xfd0tzm6ZzZVFVhSCNlTRHIqLCp-4G1k?testcase_id=6614862227832832


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-02-28)

ClusterFuzz testcase 6614862227832832 is verified as fixed, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-03-01)

[Empty comment from Monorail migration]

### is...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### is...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-08)

Your change meets the bar and is auto-approved for M58. Please go ahead and merge the CL to branch 3029 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), bhthompson@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cw...@gmail.com (2017-03-08)

Could you also merge this two following commits?

https://chromium.googlesource.com/v8/v8.git/+/a3709d47e65885ba1dbae086dd8452cbf3cbe899
https://chromium.googlesource.com/v8/v8.git/+/5fc1bd5b32be6812c8e09d2486a81eb7d0918a1c

which fix a correctness bug.

### mb...@google.com (2017-03-08)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-03-12)

Please merge your change to M58 branch 3029 before 5:00 PM PT, Monday (03/13/17) so we can take it in for next week dev release. Thank you!


### is...@chromium.org (2017-03-13)

All three fixes mentioned in c#8 and c#15 are merged: https://codereview.chromium.org/2740943002/

### aw...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

Congratulations! The panel decided to award $1,500 for this bug - cheers!

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-06-07)

This issue was migrated from crbug.com/chromium/696251?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/696462, crbug.com/chromium/698113]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086898)*
