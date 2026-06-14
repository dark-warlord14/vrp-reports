# Security: IDN URL Spoofing with Georgian Letter Jil "ძ"

| Field | Value |
|-------|-------|
| **Issue ID** | [40092752](https://issues.chromium.org/issues/40092752) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Internationalization |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | li...@google.com |
| **Created** | 2018-10-18 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 72.0.3582.0 (Official Build) canary (64-bit)  

Operating System: Mac

**REPRODUCTION CASE**  

Cyrillic letter U+10EB (ძ) looks very similar to the Latin letter d.

Visit: <http://xn--4000-pfr.com/>

Real domain 4000.com (listed in top-100k domain)

## Attachments

- [Screen Shot 2018-10-18 at 02.16.16.png](attachments/Screen Shot 2018-10-18 at 02.16.16.png) (image/png, 17.0 KB)

## Timeline

### ch...@gmail.com (2018-10-18)

Oops sorry! I meant d4000.com not 4000.com :-)

### aa...@google.com (2018-10-18)

[Empty comment from Monorail migration]

[Monorail components: UI>Internationalization UI>Security>UrlFormatting]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-03)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-11-08)

While this is a good spoof, it only affects one domain from the list of top domains. Since the impact is small, I'm lowering the severity further.

### ch...@gmail.com (2018-11-08)

Right. 

### sh...@chromium.org (2018-11-08)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-06-25)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-06-25)

We should be able to map to d in https://cs.chromium.org/chromium/src/components/url_formatter/idn_spoof_checker.cc?l=181 so that it'll fall back to punycode in the omnibox.

### me...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8fe27d03e5e8827f7b4cbc0fedcbd1d4d1c851ee

commit 8fe27d03e5e8827f7b4cbc0fedcbd1d4d1c851ee
Author: Cynthia Liang <liangcyn@google.com>
Date: Tue Jul 16 01:16:16 2019

Added Georgian d to confusables mapping

Added Georgian d to mapping of frequently confused symbol
based on idn spoofing possibility of d4000.com

Bug: 896533
Change-Id: I2c308379ffa9d4b67923dee3d40700c0c733a696
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1677554
Reviewed-by: Tommy Li <tommycli@chromium.org>
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Commit-Queue: Cynthia Liang <liangcyn@google.com>
Cr-Commit-Position: refs/heads/master@{#677585}

[modify] https://crrev.com/8fe27d03e5e8827f7b4cbc0fedcbd1d4d1c851ee/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/8fe27d03e5e8827f7b4cbc0fedcbd1d4d1c851ee/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/8fe27d03e5e8827f7b4cbc0fedcbd1d4d1c851ee/components/url_formatter/top_domains/test_domains.skeletons
[modify] https://crrev.com/8fe27d03e5e8827f7b4cbc0fedcbd1d4d1c851ee/components/url_formatter/url_formatter_unittest.cc


### me...@chromium.org (2019-07-17)

Cynthia: Thanks again for fixing this, I think we can close it now.

### li...@google.com (2019-07-17)

Sounds good.

### sh...@chromium.org (2019-07-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-22)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-01)

Congrats! The Panel decided to reward you $500 for this report! 

### na...@google.com (2019-08-01)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/896533?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092752)*
