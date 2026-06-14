# Crash in v8::internal::Simulator::DecodeType3

| Field | Value |
|-------|-------|
| **Issue ID** | [40089572](https://issues.chromium.org/issues/40089572) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | da...@chromium.org |
| **Created** | 2017-11-11 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6497963143856128

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_v8_arm_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0xcbe17ed4
Crash State:
  v8::internal::Simulator::DecodeType3
  v8::internal::Simulator::InstructionDecode
  v8::internal::Simulator::CallInternal
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_v8_arm_dbg&range=48861:48862

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6497963143856128

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for more information.

## Timeline

### es...@chromium.org (2017-11-11)

danno could you take a look please? Thanks!

### sh...@chromium.org (2017-11-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-11-12)

[Empty comment from Monorail migration]

### da...@chromium.org (2017-11-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/4d70aa02fdcc2426222d06b333f6b13a4101e28f

commit 4d70aa02fdcc2426222d06b333f6b13a4101e28f
Author: Daniel Clifford <danno@chromium.org>
Date: Wed Nov 22 12:32:37 2017

Fix hole handling in fast arguments slice

Bug: chromium:784080
Change-Id: I38c539435d867f6abb80218457e5b5a982e34817
Reviewed-on: https://chromium-review.googlesource.com/785210
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Daniel Clifford <danno@chromium.org>
Cr-Commit-Position: refs/heads/master@{#49571}
[modify] https://crrev.com/4d70aa02fdcc2426222d06b333f6b13a4101e28f/src/builtins/builtins-array-gen.cc
[add] https://crrev.com/4d70aa02fdcc2426222d06b333f6b13a4101e28f/test/mjsunit/regress/regress-784080.js


### cl...@chromium.org (2017-11-22)

ClusterFuzz has detected this issue as fixed in range 49570:49571.

Detailed report: https://clusterfuzz.com/testcase?key=6497963143856128

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_v8_arm_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0xcbe17ed4
Crash State:
  v8::internal::Simulator::DecodeType3
  v8::internal::Simulator::InstructionDecode
  v8::internal::Simulator::CallInternal
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_v8_arm_dbg&range=48861:48862
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_v8_arm_dbg&range=49570:49571

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6497963143856128

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-11-22)

ClusterFuzz testcase 6497963143856128 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-11-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-08)

Hi decoder.oh@ - the VRP Panel decided to award $1000 for this, plus the $500 clusterfuzz bonus.  Thanks!

### aw...@chromium.org (2017-12-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-31)

[Empty comment from Monorail migration]

### is...@google.com (2018-03-31)

This issue was migrated from crbug.com/chromium/784080?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089572)*
