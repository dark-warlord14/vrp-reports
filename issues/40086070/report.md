# Crash in v8::internal::DoubleToRadixCString

| Field | Value |
|-------|-------|
| **Issue ID** | [40086070](https://issues.chromium.org/issues/40086070) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ya...@chromium.org |
| **Created** | 2016-11-24 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5631879828209664

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7f305efe6980
Crash State:
  v8::internal::DoubleToRadixCString
  v8::internal::Builtin_Impl_NumberPrototypeToString
  v8::internal::Builtin_NumberPrototypeToString
  
Recommended Security Severity: Medium

Regressed: V8: r41254:41255

Minimized Testcase (8.61 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96I_mzJFv5CUq1VHG7hWpgpyHVrCotjJ0PizDNJLOAW7N35uU-YKtkS1bZZnNe5y9QMdAVjvwpwBQgZVOpUwxRbQgZjnjMu5YLH_AvEcFiOXHCozELIy88APAk0gqjuJAb1xKDWecz9X0ZnWNlq93WZzIlCEA?testcase_id=5631879828209664

Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### ro...@chromium.org (2016-11-24)

Yang, bisects to your CL.

### do...@chromium.org (2016-11-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-11-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/b6d2bacd66391c0c6e501a810695259ab852a573

commit b6d2bacd66391c0c6e501a810695259ab852a573
Author: yangguo <yangguo@chromium.org>
Date: Fri Nov 25 07:46:10 2016

Fix Number.prototype.toString with non-default radix wrt modulo.

TBR=tebbi@chromium.org
BUG=chromium:668510

Review-Url: https://codereview.chromium.org/2526223003
Cr-Commit-Position: refs/heads/master@{#41280}

[modify] https://crrev.com/b6d2bacd66391c0c6e501a810695259ab852a573/src/conversions.cc
[modify] https://crrev.com/b6d2bacd66391c0c6e501a810695259ab852a573/test/mjsunit/number-tostring.js


### cl...@chromium.org (2016-11-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5663238525288448

Fuzzer: mbarbella_js_mutation
Job Type: linux_asan_d8_v8_arm_dbg
Platform Id: linux

Crash Type: Global-buffer-overflow READ 1
Crash Address: 0xf67c5838
Crash State:
  v8::internal::DoubleToRadixCString
  v8::internal::Builtin_Impl_NumberPrototypeToString
  v8::internal::Builtin_NumberPrototypeToString
  
Regressed: V8: r41254:41255

Minimized Testcase (0.09 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96Zvj-3UE3IEN0UCQLAl8JhESOHYUEbOP0l1d1zwbZmcEte_zGMU0or1U6rhwEpYaQpMpdQDEMkAHC1azN66jpyhRhNq23FI2uoNBoCttji7kab9vsp1REXoAcp2yfckfF2SYL5NQ907h4asB2X1jVteknGcA?testcase_id=5663238525288448
function __f_6(a, b, c) {
 b.toString(c);
}
__f_6("600f9f6dd18bc8000",111111111111111114140, 12);


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### sh...@chromium.org (2016-11-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-25)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-11-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-11-26)

ClusterFuzz has detected this issue as fixed in range 41279:41280.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5631879828209664

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7f305efe6980
Crash State:
  v8::internal::DoubleToRadixCString
  v8::internal::Builtin_Impl_NumberPrototypeToString
  v8::internal::Builtin_NumberPrototypeToString
  
Recommended Security Severity: Medium

Regressed: V8: r41254:41255
Fixed: V8: r41279:41280

Minimized Testcase (8.61 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96I_mzJFv5CUq1VHG7hWpgpyHVrCotjJ0PizDNJLOAW7N35uU-YKtkS1bZZnNe5y9QMdAVjvwpwBQgZVOpUwxRbQgZjnjMu5YLH_AvEcFiOXHCozELIy88APAk0gqjuJAb1xKDWecz9X0ZnWNlq93WZzIlCEA?testcase_id=5631879828209664

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-11-26)

ClusterFuzz has detected this issue as fixed in range 41279:41280.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5663238525288448

Fuzzer: mbarbella_js_mutation
Job Type: linux_asan_d8_v8_arm_dbg
Platform Id: linux

Crash Type: Global-buffer-overflow READ 1
Crash Address: 0xf67c5838
Crash State:
  v8::internal::DoubleToRadixCString
  v8::internal::Builtin_Impl_NumberPrototypeToString
  v8::internal::Builtin_NumberPrototypeToString
  
Regressed: V8: r41254:41255
Fixed: V8: r41279:41280

Minimized Testcase (0.09 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96Zvj-3UE3IEN0UCQLAl8JhESOHYUEbOP0l1d1zwbZmcEte_zGMU0or1U6rhwEpYaQpMpdQDEMkAHC1azN66jpyhRhNq23FI2uoNBoCttji7kab9vsp1REXoAcp2yfckfF2SYL5NQ907h4asB2X1jVteknGcA?testcase_id=5663238525288448
function __f_6(a, b, c) {
 b.toString(c);
}
__f_6("600f9f6dd18bc8000",111111111111111114140, 12);


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-11-26)

ClusterFuzz testcase is verified as fixed, closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2016-11-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-02)

The panel declined to reward in this case, since it was trunk churn.

### de...@googlemail.com (2016-12-02)

Umm, since when are trunk issues not eligible for rewards? It was found as part of the fuzzer contribution program and fixed as a result of this bug report.

### aw...@google.com (2016-12-15)

Retagging with reward-topanel as we might have missed #3!

### aw...@google.com (2016-12-16)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-12-16)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### sh...@chromium.org (2016-12-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ya...@chromium.org (2016-12-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-12)

Hi decoder.oh@ - the panel took another look at this.  While there was a fix landed in this bug, the mbarbella_js_mutation fuzzer found (#9) it independently within 48 hours - even though that was after the fix.  We double checked that our fuzzer hadn't just picked up the case that was check in as part of #3 so we're confident that we would have found this bug without your fuzzer, and thus it falls outside the scope of the VRP. However the panel used their discretion to reward $500 in this case.

### aw...@chromium.org (2017-01-13)

hi yangguo@ - would you be able to merge this to the M56 branch?

### aw...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-03-04)

This issue was migrated from crbug.com/chromium/668510?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086070)*
