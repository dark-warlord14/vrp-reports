# Security:  IDN URL Spoofing with “ก” 

| Field | Value |
|-------|-------|
| **Issue ID** | [40092396](https://issues.chromium.org/issues/40092396) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2018-09-08 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 71.0.3545.3 (Official Build) canary (64-bit)  

Operating System: Mac

**REPRODUCTION CASE**

Visit <http://xn--11-lqi.com/>

- U+0E01 (ก) is more similar to 'n'

Note: n11.com is a top-10K site.

## Attachments

- [Screen Shot 2018-09-08 at 02.35.18.png](attachments/Screen Shot 2018-09-08 at 02.35.18.png) (image/png, 31.1 KB)

## Timeline

### ch...@gmail.com (2018-09-08)

Looks like U+0E01 (ก) was missed in https://crbug.com/chromium/833143.


### mp...@google.com (2018-09-09)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox UI>Security>UrlFormatting]

### sh...@chromium.org (2018-09-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-10)

[Empty comment from Monorail migration]

### ct...@chromium.org (2018-09-12)

I have a quick CL up to add this to the confusables list while meacer is OOO:

https://chromium-review.googlesource.com/c/chromium/src/+/1220773

### bu...@chromium.org (2018-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3983030c2ee3e54afa60fe24f23e4c98067a3634

commit 3983030c2ee3e54afa60fe24f23e4c98067a3634
Author: Christopher Thompson <cthomp@chromium.org>
Date: Fri Sep 14 00:30:39 2018

Add additional Lao character to IDN confusables

  U+0E01 (ก) => n

Prior Lao/Thai entries were added in crrev.com/c/1058710.

Test: components_unittests --gtest_filter=*IDN*
Bug: 882078
Change-Id: I1e90b144a1d791341b515d026a6bc4be7cbed57d
Reviewed-on: https://chromium-review.googlesource.com/1220773
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Christopher Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/heads/master@{#591227}
[modify] https://crrev.com/3983030c2ee3e54afa60fe24f23e4c98067a3634/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/3983030c2ee3e54afa60fe24f23e4c98067a3634/components/url_formatter/top_domains/alexa_domains.skeletons
[modify] https://crrev.com/3983030c2ee3e54afa60fe24f23e4c98067a3634/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/3983030c2ee3e54afa60fe24f23e4c98067a3634/components/url_formatter/top_domains/test_domains.skeletons
[modify] https://crrev.com/3983030c2ee3e54afa60fe24f23e4c98067a3634/components/url_formatter/url_formatter_unittest.cc


### ct...@chromium.org (2018-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-18)

This bug requires manual review: Less than 24 days to go before AppStore submit on M70
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-09-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-09-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/db0a0dfdc697039796e2b955dbaa01ffce2fb16b

commit db0a0dfdc697039796e2b955dbaa01ffce2fb16b
Author: Christopher Thompson <cthomp@chromium.org>
Date: Tue Sep 18 23:59:03 2018

[M70] Add additional Lao character to IDN confusables

  U+0E01 (ก) => n

Prior Lao/Thai entries were added in crrev.com/c/1058710.

Test: components_unittests --gtest_filter=*IDN*
Bug: 882078
Change-Id: I1e90b144a1d791341b515d026a6bc4be7cbed57d
Reviewed-on: https://chromium-review.googlesource.com/1220773
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Christopher Thompson <cthomp@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#591227}(cherry picked from commit 3983030c2ee3e54afa60fe24f23e4c98067a3634)
Reviewed-on: https://chromium-review.googlesource.com/1232679
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/branch-heads/3538@{#514}
Cr-Branched-From: 79f7c91a2b2a2932cd447fa6f865cb6662fa8fa6-refs/heads/master@{#587811}
[modify] https://crrev.com/db0a0dfdc697039796e2b955dbaa01ffce2fb16b/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/db0a0dfdc697039796e2b955dbaa01ffce2fb16b/components/url_formatter/top_domains/alexa_domains.skeletons
[modify] https://crrev.com/db0a0dfdc697039796e2b955dbaa01ffce2fb16b/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/db0a0dfdc697039796e2b955dbaa01ffce2fb16b/components/url_formatter/top_domains/test_domains.skeletons
[modify] https://crrev.com/db0a0dfdc697039796e2b955dbaa01ffce2fb16b/components/url_formatter/url_formatter_unittest.cc


### aw...@chromium.org (2018-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-04)

$500 for this one!

### aw...@chromium.org (2018-10-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/882078?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092396)*
