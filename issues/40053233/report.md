# Global-buffer-overflow in blink::MathMLOperatorElement::ComputeOperatorProperty

| Field | Value |
|-------|-------|
| **Issue ID** | [40053233](https://issues.chromium.org/issues/40053233) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>MathML |
| **Platforms** | Linux, Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | fw...@igalia.com |
| **Created** | 2020-09-03 |
| **Bounty** | $3,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=4829989417844736

Fuzzer: jesse_avalanche
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Global-buffer-overflow READ 4
Crash Address: 0x7ff9774716bc
Crash State:
  blink::MathMLOperatorElement::ComputeOperatorProperty
  blink::MathMLOperatorElement::HasBooleanProperty
  blink::NGMathUnderOverLayoutAlgorithm::Layout
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=803905:803910

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4829989417844736

Issue filed automatically.



## Timeline

### cl...@chromium.org (2020-09-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-09-03)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Layout]

### cl...@chromium.org (2020-09-03)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/2e4742edd2be43c2b65092e411b70bab2cd2221f ([mathml] Refine constants used for <munderover> layout).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### fw...@igalia.com (2020-09-03)

[Empty comment from Monorail migration]

### fw...@igalia.com (2020-09-03)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Layout Blink>MathML]

### fw...@igalia.com (2020-09-03)

fix for this is easy ; but still need to write WPT tests: https://chromium-review.googlesource.com/c/chromium/src/+/2390633

### [Deleted User] (2020-09-03)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fw...@igalia.com (2020-09-04)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b7f7d543465f8846cd5e58b45d6bfb4207bc3b21

commit b7f7d543465f8846cd5e58b45d6bfb4207bc3b21
Author: Frédéric Wang <fwang@igalia.com>
Date: Fri Sep 04 16:13:59 2020

[mathml] Fix dictionary category for unknown operators with explicit form

MathMLOperatorElement::ComputeDictionaryCategory was wrongly implemented
in [1] and returns an unknown category for an operator that is not in
the dictionary AND has an explicit form attribute. This caused a crash
when the function was finally used in [2] and [3].

This CL fixes that mistake and adds a DCHECK after the unique call to
ComputeDictionaryCategory to ensure the category is not unknown.
Additionally, the documentation of the corresponding low-level
platform/text API is updated to make clear it never returns an unknown
category.

WPT tests are added, one of them contains an munderover whose base is an
operator outside the dictionary with an explicit form, allowing to
ensure no crash happens for the code added in [2] [3]. Another one
verifies default operator spacing and will cover the code added in [4].

[1] https://chromium-review.googlesource.com/c/chromium/src/+/2368362
[2] https://chromium-review.googlesource.com/c/chromium/src/+/2390760
[3] https://chromium-review.googlesource.com/c/chromium/src/+/2383023
[4] https://chromium-review.googlesource.com/c/chromium/src/+/2390652

Bug: 6606, 1124617
Change-Id: Ic6ba0b663d14634ca5c66070a5b3cfc2eaa3d198
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2390633
Reviewed-by: Rob Buis <rbuis@igalia.com>
Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
Commit-Queue: Ian Kilpatrick <ikilpatrick@chromium.org>
Cr-Commit-Position: refs/heads/master@{#804559}

[modify] https://crrev.com/b7f7d543465f8846cd5e58b45d6bfb4207bc3b21/third_party/blink/renderer/core/mathml/mathml_operator_element.cc
[modify] https://crrev.com/b7f7d543465f8846cd5e58b45d6bfb4207bc3b21/third_party/blink/renderer/platform/text/mathml_operator_dictionary.h
[modify] https://crrev.com/b7f7d543465f8846cd5e58b45d6bfb4207bc3b21/third_party/blink/web_tests/TestExpectations
[add] https://crrev.com/b7f7d543465f8846cd5e58b45d6bfb4207bc3b21/third_party/blink/web_tests/external/wpt/mathml/presentation-markup/operators/mo-not-in-dictionary-lspace-rspace-ref.html
[add] https://crrev.com/b7f7d543465f8846cd5e58b45d6bfb4207bc3b21/third_party/blink/web_tests/external/wpt/mathml/presentation-markup/operators/mo-not-in-dictionary-lspace-rspace.html
[add] https://crrev.com/b7f7d543465f8846cd5e58b45d6bfb4207bc3b21/third_party/blink/web_tests/external/wpt/mathml/presentation-markup/operators/mo-not-in-dictionary-movablelimits-ref.html
[add] https://crrev.com/b7f7d543465f8846cd5e58b45d6bfb4207bc3b21/third_party/blink/web_tests/external/wpt/mathml/presentation-markup/operators/mo-not-in-dictionary-movablelimits.html


### [Deleted User] (2020-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fw...@igalia.com (2020-09-04)

This bug should be fixed now.

### [Deleted User] (2020-09-04)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-09-05)

ClusterFuzz testcase 4829989417844736 is verified as fixed in https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=804558:804559

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-09-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-05)

Requesting merge to beta M86 because latest trunk commit (804559) appears to be after beta branch point (800218).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-05)

This bug requires manual review: M86's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2020-09-06)

Please reply to https://crbug.com/chromium/1124617#c17 which helps in merge decision.


+Adetaylor(Security TPM)

### fw...@igalia.com (2020-09-07)

Hi,

I'm not sure I'm supposed to reply to this but:

1. This is a fix for a crash found by clusterfuzz. It is gated under the MathMLCore flag.

2. CL: https://chromium-review.googlesource.com/c/chromium/src/+/2390633

3. Yes. 2 WPT tests triggering the crash have been added in the mentioned CL.

4. This is a fix for a crash introduced by recent CLs (merged during the past week). Not sure what was the timing with respect to branch point, though.

https://chromium-review.googlesource.com/c/chromium/src/+/2368362 (crashing code)
https://chromium-review.googlesource.com/c/chromium/src/+/2390760 (caller 1)
https://chromium-review.googlesource.com/c/chromium/src/+/2383023 (caller 2)

5. This code is part of the MathML implementation. The crashing code can only be triggered if MathMLCore is enabled.

6. It's behind an experimental flag disabled on release but implied by the "experimental web platform features" switch. It it does not use finch.


### ad...@chromium.org (2020-09-08)

It looks to me like this regressed in 87 so adjusting security impact, merge labels etc.

### ad...@google.com (2020-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-09)

Congratulations, the VRP panel has decided to award $2000 for this bug + the $1000 fuzzer bonus.

### ad...@google.com (2020-09-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1124617?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/6606]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053233)*
