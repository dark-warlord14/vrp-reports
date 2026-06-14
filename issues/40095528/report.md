# Bad-cast to net::URLRequestFtpJob from invalid vptr in net::URLRequestFtpJob::OnStartCompleted

| Field | Value |
|-------|-------|
| **Issue ID** | [40095528](https://issues.chromium.org/issues/40095528) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Network |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | te...@google.com |
| **Created** | 2019-06-28 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5155387255160832

Fuzzer: domino
Job Type: linux_ubsan_vptr_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x2c4782449c00
Crash State:
  Bad-cast to net::URLRequestFtpJob from invalid vptr
  net::URLRequestFtpJob::OnStartCompleted
  base::TaskAnnotator::RunTask
  
Sanitizer: undefined (UBSAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_ubsan_vptr_chrome&range=672917:672918

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5155387255160832

Additional requirements: Requires HTTP

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

## Timeline

### cl...@chromium.org (2019-06-28)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Network]

### cl...@chromium.org (2019-06-28)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/d89ab35b9c9669781d98b4977660f153e459699f (Add Uma histogram metrics for tracking successful/failed ftp requests.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### sh...@chromium.org (2019-06-28)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@google.com (2019-06-28)

[Empty comment from Monorail migration]

### te...@google.com (2019-06-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-06-29)

ClusterFuzz testcase 5155387255160832 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_ubsan_vptr_chrome&range=673458:673459

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-06-30)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $3,500 for this report!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/979505?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/979605]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095528)*
