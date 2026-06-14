# Security DCHECK failure: IsA<Derived>(from) in casting.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40052030](https://issues.chromium.org/issues/40052030) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>CSS, Blink>Internals>WTF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | an...@chromium.org |
| **Created** | 2020-04-16 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6087798403170304

Fuzzer: jesse_avalanche
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::To<blink::CSSValuePair,blink::CSSValue>
  blink::StylePropertySerializer::BorderRadiusValue
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=759560:759564

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6087798403170304

Issue filed automatically.



## Timeline

### cl...@chromium.org (2020-04-16)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>CSS Blink>Internals>WTF]

### [Deleted User] (2020-04-16)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2020-04-17)

I'm guessing this was caused by https://chromium-review.googlesource.com/c/chromium/src/+/2146908 - enabling 'revert' for stable. That's the only style-related CL in the blamelist.

This is a high security issue, can you please take a look, and revert the 'revert' feature if you can't address this appropriately?

### yo...@yoav.ws (2020-04-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-04-17)

ClusterFuzz testcase 6087798403170304 is verified as fixed in https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=759987:759988

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7075110be08ba3547fa6c2ad7c38a5c109fe3f4e

commit 7075110be08ba3547fa6c2ad7c38a5c109fe3f4e
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date: Sat Apr 18 07:05:32 2020

Handle 'revert' in StylePropertySerializer::CommonShorthandChecks

The 'initial', 'inherit' and 'unset' keywords were handled, but
'revert' was not. This caused crashes when trying to represent certain
declaration block serializations using shorthands.

Change to use IsCSSWideKeyword instead, which includes 'revert'.
(It should also avoid the same problem the next time a new CSS-wide
keyword is added).

Bug: 1071454
Change-Id: I968a32a5ad5b2a1a1958f60ec19679c6a642df14
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2152817
Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/heads/master@{#760310}

[modify] https://crrev.com/7075110be08ba3547fa6c2ad7c38a5c109fe3f4e/third_party/blink/renderer/core/css/style_property_serializer.cc
[modify] https://crrev.com/7075110be08ba3547fa6c2ad7c38a5c109fe3f4e/third_party/blink/web_tests/external/wpt/css/cssom/css-style-attr-decl-block.html


### [Deleted User] (2020-04-18)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/56516ffbd9555c153e3a933e21fa586ebf7aa7b8

commit 56516ffbd9555c153e3a933e21fa586ebf7aa7b8
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date: Sat Apr 18 20:50:49 2020

Revert the revert of 'revert'

This enables support for the 'revert' keyword once again,
now that https://crbug.com/chromium/1071454 is fixed.

This reverts commit e5912ac3d2a3dd77ee101f214ffea31b93a60c34.

Bug: 579788, 1071454
Change-Id: I5ca25177567e80f85e05584dcfee12c5398e1084
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2153121
Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/heads/master@{#760336}

[modify] https://crrev.com/56516ffbd9555c153e3a933e21fa586ebf7aa7b8/third_party/blink/renderer/platform/runtime_enabled_features.json5


### do...@chromium.org (2020-04-19)

Thanks for promptly addressing this issue!

### na...@google.com (2020-04-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-23)

Congrats the Panel decided to award $5,000 for this report and you got a $1,000 fuzzing bonus!

### na...@google.com (2020-04-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1071454?no_tracker_redirect=1

[Multiple monorail components: Blink>CSS, Blink>Internals>WTF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052030)*
