# Stack-buffer-overflow in v8::internal::DoubleToRadixCString

| Field | Value |
|-------|-------|
| **Issue ID** | [40086464](https://issues.chromium.org/issues/40086464) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ya...@chromium.org |
| **Created** | 2017-01-10 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5430118219776000

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_v8_mipsel_dbg
Platform Id: linux

Crash Type: Stack-buffer-overflow WRITE 1
Crash Address: 0xdd9bd044
Crash State:
  v8::internal::DoubleToRadixCString
  v8::internal::Builtin_Impl_NumberPrototypeToString
  v8::internal::Builtin_NumberPrototypeToString
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: V8: r41254:41255

Minimized Testcase (6.93 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97Rjac1GOhxDLJWb27tYeadq24hCM3Lgfiuf86W9mAxz-E_qnk1EwrEG_vLjqAC7R_4cn9gtmY9She6liPIIN5WTekkLOrir_Lg1a_s_Xsycj-S-92FxvP1vs_0zNDJS6foO6DEPmCckvnnxlAK12IHxRs2L2RVQBzMInipDxN7jUy9azBRZH9RtlJkvUdQtByUbDxuWobzqCcrmdPFr7Dbg9PIrNoPEMtVWh42eGt32UZiOjAOrnWO5n5gluLUNkOG2CJDIu5KdST9nZ0cPsNzHmqsIHkpTENtaHUMnVFrK1Zv7zmmcFH1xA4DPrOVQClKtTy5Z-uRiDU2sVis4zwZDq88BC320gpQE1THg8Ur8qtIQ-w6tBgZxTlo65vN3MX0oRruigCvktWYV5BzfOXCHXRorg?testcase_id=5430118219776000

Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### sh...@chromium.org (2017-01-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-11)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2017-01-14)

Regression range points to https://chromium.googlesource.com/v8/v8/+/21b0dbedfd470b67c47f84428e1af95a506e49e5, which looks related.

### bu...@chromium.org (2017-01-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/73de4f8f1e89da2bb54bb3b79c58e10cf50cfd53

commit 73de4f8f1e89da2bb54bb3b79c58e10cf50cfd53
Author: yangguo <yangguo@chromium.org>
Date: Mon Jan 16 11:44:29 2017

Fix overflow in Number.prototype.toString with custom radix.

R=tebbi@chromium.org
BUG=chromium:679841

Review-Url: https://codereview.chromium.org/2638733002
Cr-Commit-Position: refs/heads/master@{#42364}

[modify] https://crrev.com/73de4f8f1e89da2bb54bb3b79c58e10cf50cfd53/src/conversions.cc


### bu...@chromium.org (2017-01-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d33dc16f435c529d818ba5a27c2d206e2ff91144

commit d33dc16f435c529d818ba5a27c2d206e2ff91144
Author: yangguo <yangguo@chromium.org>
Date: Mon Jan 16 13:49:00 2017

Add test case for Number.prototype.toString (r42364).

TBR=tebbi@chromium.org
BUG=chromium:679841

Review-Url: https://codereview.chromium.org/2631163002
Cr-Commit-Position: refs/heads/master@{#42375}

[add] https://crrev.com/d33dc16f435c529d818ba5a27c2d206e2ff91144/test/mjsunit/regress/regress-crbug-679841.js


### cl...@chromium.org (2017-01-17)

ClusterFuzz has detected this issue as fixed in range 42363:42364.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5430118219776000

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_v8_mipsel_dbg
Platform Id: linux

Crash Type: Stack-buffer-overflow WRITE 1
Crash Address: 0xdd9bd044
Crash State:
  v8::internal::DoubleToRadixCString
  v8::internal::Builtin_Impl_NumberPrototypeToString
  v8::internal::Builtin_NumberPrototypeToString
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: V8: r41254:41255
Fixed: V8: r42363:42364

Minimized Testcase (6.93 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97Rjac1GOhxDLJWb27tYeadq24hCM3Lgfiuf86W9mAxz-E_qnk1EwrEG_vLjqAC7R_4cn9gtmY9She6liPIIN5WTekkLOrir_Lg1a_s_Xsycj-S-92FxvP1vs_0zNDJS6foO6DEPmCckvnnxlAK12IHxRs2L2RVQBzMInipDxN7jUy9azBRZH9RtlJkvUdQtByUbDxuWobzqCcrmdPFr7Dbg9PIrNoPEMtVWh42eGt32UZiOjAOrnWO5n5gluLUNkOG2CJDIu5KdST9nZ0cPsNzHmqsIHkpTENtaHUMnVFrK1Zv7zmmcFH1xA4DPrOVQClKtTy5Z-uRiDU2sVis4zwZDq88BC320gpQE1THg8Ur8qtIQ-w6tBgZxTlo65vN3MX0oRruigCvktWYV5BzfOXCHXRorg?testcase_id=5430118219776000

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ya...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-04-25)

This issue was migrated from crbug.com/chromium/679841?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086464)*
