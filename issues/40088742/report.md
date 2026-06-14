# ProxyHasProperty stub crashes when trap is a Smi

| Field | Value |
|-------|-------|
| **Issue ID** | [40088742](https://issues.chromium.org/issues/40088742) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2017-08-17 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5958699981209600

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0xffffffffffffffff
Crash State:
  v8::internal::Invoke
  v8::internal::CallInternal
  v8::Script::Run
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=47371:47372

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5958699981209600

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for more information.

## Timeline

### rs...@chromium.org (2017-08-17)

jkummerow: Can you take a look? Clusterfuzz blames https://chromium.googlesource.com/v8/v8/+log/b0d09b4967c709dfd26ee0364b375e622d49841f..221e54ddbc903b42c370f285c168d9eef6dda3cb?pretty=fuller&n=10000 but I can't assign to the author of that CL.

### jk...@chromium.org (2017-08-17)

Maya, this one's for you.

Repro:
out/x64.debug/d8 -e "'foo' in new Proxy({}, {has: 0})"

The fix seems simple: I think you need the "GotoIf(TaggedIsSmi(trap), &trap_not_callable);" line that the "get" stub has but the "has" stub doesn't.

### ne...@chromium.org (2017-08-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@google.com (2017-08-18)

The fix is already pending a code review: https://chromium-review.googlesource.com/c/620647

### bu...@chromium.org (2017-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/03285ec968a78683be5342c4a035da81bf394816

commit 03285ec968a78683be5342c4a035da81bf394816
Author: Maya Lekova <mslekova@google.com>
Date: Fri Aug 18 13:56:18 2017

[builtins] Fix crash in ProxyHasProperty stub

The crash used to happen when trap is a Smi.

Bug: chromium:756608
Change-Id: I0a6f0328afc64d8e521b5b370a291f9aef6b08d0
Reviewed-on: https://chromium-review.googlesource.com/620647
Reviewed-by: Georg Neis <neis@chromium.org>
Commit-Queue: Maya Lekova <mslekova@google.com>
Cr-Commit-Position: refs/heads/master@{#47429}
[modify] https://crrev.com/03285ec968a78683be5342c4a035da81bf394816/src/builtins/builtins-proxy-gen.cc
[add] https://crrev.com/03285ec968a78683be5342c4a035da81bf394816/test/mjsunit/regress/regress-756608.js


### jk...@chromium.org (2017-08-18)

Should be fixed by #7. Thanks for the quick turnaround!

### cl...@chromium.org (2017-08-19)

ClusterFuzz has detected this issue as fixed in range 47428:47429.

Detailed report: https://clusterfuzz.com/testcase?key=5958699981209600

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0xffffffffffffffff
Crash State:
  v8::internal::Invoke
  v8::internal::CallInternal
  v8::Script::Run
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=47371:47372
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=47428:47429

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5958699981209600

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-08-19)

ClusterFuzz testcase 5958699981209600 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-08-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-01)

Groovy - your fuzzer got you another $3,500 :-)

### aw...@chromium.org (2017-09-01)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-11-25)

This issue was migrated from crbug.com/chromium/756608?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088742)*
