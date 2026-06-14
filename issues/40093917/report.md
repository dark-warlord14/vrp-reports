# Security DCHECK failure: RotateTransformOperation::IsMatchingOperationType(transform.GetType()) in rotate

| Field | Value |
|-------|-------|
| **Issue ID** | [40093917](https://issues.chromium.org/issues/40093917) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Platform |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ke...@chromium.org |
| **Created** | 2019-02-01 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5115262500208640

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  RotateTransformOperation::IsMatchingOperationType(transform.GetType()) in rotate
  blink::RotateTransformOperation::Blend
  blink::TransformOperations::BlendPrefixByMatchingOperations
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628046:628047

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5115262500208640

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

## Timeline

### cl...@chromium.org (2019-02-01)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Platform]

### cl...@chromium.org (2019-02-01)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/9f9fed4945dd427a903cc71f21c3b884bd9cd6d3 (Fix edge cases for interpolation of rotation transforms.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### sh...@chromium.org (2019-02-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-01)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-02-01)

[Empty comment from Monorail migration]

### ke...@chromium.org (2019-02-01)

[Empty comment from Monorail migration]

### ke...@chromium.org (2019-02-01)

https://chromium-review.googlesource.com/c/chromium/src/+/1450394

### sh...@chromium.org (2019-02-02)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/321af0cd3771eea8cb7d622a23175b9374c7244e

commit 321af0cd3771eea8cb7d622a23175b9374c7244e
Author: Kevin Ellis <kevers@chromium.org>
Date: Mon Feb 04 16:14:26 2019

Fix DCHECK failure in RotateTransformOperation

Bug: 927555
Change-Id: Id92f4b7a6180b01cf8b9621976549f0181cad4e7
Reviewed-on: https://chromium-review.googlesource.com/c/1450394
Reviewed-by: Ian Vollick <vollick@chromium.org>
Commit-Queue: Kevin Ellis <kevers@chromium.org>
Cr-Commit-Position: refs/heads/master@{#628757}
[modify] https://crrev.com/321af0cd3771eea8cb7d622a23175b9374c7244e/third_party/blink/renderer/platform/transforms/rotate_transform_operation.cc


### ke...@chromium.org (2019-02-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-02-05)

ClusterFuzz has detected this issue as fixed in range 628749:628758.

Detailed report: https://clusterfuzz.com/testcase?key=5115262500208640

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  RotateTransformOperation::IsMatchingOperationType(transform.GetType()) in rotate
  blink::RotateTransformOperation::Blend
  blink::TransformOperations::BlendPrefixByMatchingOperations
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628046:628047
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=628749:628758

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5115262500208640

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-02-05)

ClusterFuzz testcase 5115262500208640 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-02-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

This bug requires manual review: M73 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-02-11)

abdulsyed@ looks like this is automatically verified so wondering do we need to have security TPM review for this ?

### na...@google.com (2019-02-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-13)

Congrats! The Panel decided to reward $1500 for this report :) 

### aw...@chromium.org (2019-02-14)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-20)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/927555?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093917)*
