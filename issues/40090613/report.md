# Security DCHECK failure: i < length_ in StringImpl.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40090613](https://issues.chromium.org/issues/40090613) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Layout |
| **Platforms** | Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ea...@chromium.org |
| **Created** | 2018-02-27 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6031107917873152

Fuzzer: miaubiz_css_fuzzer
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  i < length_ in StringImpl.h
  blink::InlineTextBox::IsLineBreak
  blink::InlineFlowBox::ComputeOverflow
  
Sanitizer: address (ASAN)

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6031107917873152

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for more information.

## Timeline

### sh...@chromium.org (2018-02-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-27)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-02-27)

Repros easily on a Windows build with DCHECKs (haven't tried other platforms). This is trying to read index 0 from a zero-length string in the LineLayoutItem. Emil, can you please help triage this?

[Monorail components: Blink>Layout]

### ea...@chromium.org (2018-03-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2304f6f1ff0d506c9dcb3ed610e67250daf866ed

commit 2304f6f1ff0d506c9dcb3ed610e67250daf866ed
Author: Emil A Eklund <eae@chromium.org>
Date: Fri Mar 02 00:46:36 2018

Check actual text length in InlineTextBox::IsLineBreak

Check the length of the underlying string, rather than the length of the
text box as the two may differ due to text normalization.

Bug: 816768
Change-Id: Ibb91256200d51f6ec19dcff6e84bc12e5230f776
Reviewed-on: https://chromium-review.googlesource.com/942367
Commit-Queue: Koji Ishii <kojii@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/master@{#540382}
[modify] https://crrev.com/2304f6f1ff0d506c9dcb3ed610e67250daf866ed/third_party/WebKit/Source/core/layout/line/InlineTextBox.cpp


### cl...@chromium.org (2018-03-02)

ClusterFuzz has detected this issue as fixed in range 540368:540424.

Detailed report: https://clusterfuzz.com/testcase?key=6031107917873152

Fuzzer: miaubiz_css_fuzzer
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  i < length_ in StringImpl.h
  blink::InlineTextBox::IsLineBreak
  blink::InlineFlowBox::ComputeOverflow
  
Sanitizer: address (ASAN)

Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=540368:540424

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6031107917873152

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-03-02)

ClusterFuzz testcase 6031107917873152 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-03-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-03-19)

Approved for M66 - branch:3359

### aw...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-06-08)

This issue was migrated from crbug.com/chromium/816768?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090613)*
