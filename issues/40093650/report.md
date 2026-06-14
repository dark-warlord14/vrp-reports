# Use-of-uninitialized-value in avx::store_bgra

| Field | Value |
|-------|-------|
| **Issue ID** | [40093650](https://issues.chromium.org/issues/40093650) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2019-01-05 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6616039945928704

Fuzzer: cdiehl_dharma
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  avx::store_bgra
  avx::start_pipeline
  RunBasedAdditiveBlitter::flush_if_y_changed
  
Sanitizer: memory (MSAN)

Recommended Security Severity: Low

Regressed: https://clusterfuzz.com/revisions?job=linux_msan_chrome&range=582653:582655

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6616039945928704

Additional requirements: Requires Gestures

Issue filed automatically.

See https://www.chromium.org/developers/testing/memorysanitizer#TOC-Reproducing-ClusterFuzz-Bugs for instructions to reproduce this bug locally.

## Timeline

### cl...@chromium.org (2019-01-05)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Skia]

### sh...@chromium.org (2019-01-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-04-16)

ClusterFuzz has detected this issue as fixed in range 650882:650884.

Detailed report: https://clusterfuzz.com/testcase?key=6616039945928704

Fuzzer: cdiehl_dharma
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  avx::store_bgra
  avx::start_pipeline
  RunBasedAdditiveBlitter::flush_if_y_changed
  
Sanitizer: memory (MSAN)

Recommended Security Severity: Low

Regressed: https://clusterfuzz.com/revisions?job=linux_msan_chrome&range=582653:582655
Fixed: https://clusterfuzz.com/revisions?job=linux_msan_chrome&range=650882:650884

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6616039945928704

Additional requirements: Requires Gestures

See https://www.chromium.org/developers/testing/memorysanitizer#TOC-Reproducing-ClusterFuzz-Bugs for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-04-16)

ClusterFuzz testcase 6616039945928704 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-04-17)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-05-01)

Congrats! The Panel awarded $1,500 for this report :) 

### aw...@google.com (2019-05-01)

[Empty comment from Monorail migration]

### [Deleted User] (2019-05-07)

Thanks!

### sh...@chromium.org (2019-07-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-07-24)

This issue was migrated from crbug.com/chromium/919300?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093650)*
