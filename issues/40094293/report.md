# DCHECK failure in 0 <= index && index < node->op()->ValueInputCount() in node-properties.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40094293](https://issues.chromium.org/issues/40094293) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | si...@chromium.org |
| **Created** | 2019-03-14 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5661775296069632

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  0 <= index && index < node->op()->ValueInputCount() in node-properties.cc
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=60090:60091

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5661775296069632

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

## Timeline

### cl...@chromium.org (2019-03-14)

Automatically adding ccs based on suspected regression changelists:

[turbofan] add fast path for String.p.startsWith by usharma1998@gmail.com - https://chromium.googlesource.com/v8/v8/+/acadb202710a7fef8bf738297e0f6f435aa53090

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label.

### sh...@chromium.org (2019-03-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-03-15)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-03-15)

can https://chromium-review.googlesource.com/c/v8/v8/+/1491872 be reverted?

### wf...@chromium.org (2019-03-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-17)

[Empty comment from Monorail migration]

### si...@chromium.org (2019-03-18)

I'm going to revert.

### si...@chromium.org (2019-03-18)

Chromiumdash reports that the first release containing the offending patch is M75:

https://chromiumdash.appspot.com/commit/acadb202710a7fef8bf738297e0f6f435aa53090

Are the 74 labels misplaced?

### si...@chromium.org (2019-03-18)

[Empty comment from Monorail migration]

### si...@chromium.org (2019-03-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-03-18)

ClusterFuzz testcase 6252032307625984 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### cl...@chromium.org (2019-03-18)

ClusterFuzz has detected this issue as fixed in range 60278:60279.

Detailed report: https://clusterfuzz.com/testcase?key=5661775296069632

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  0 <= index && index < node->op()->ValueInputCount() in node-properties.cc
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=60090:60091
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=60278:60279

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5661775296069632

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2019-03-19)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-20)

Congrats the Panel decided to reward $1,000 + $500 bonus. 

### aw...@google.com (2019-03-21)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/941952?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/942394, crbug.com/chromium/942845]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094293)*
