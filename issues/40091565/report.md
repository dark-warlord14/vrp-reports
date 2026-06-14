# Security: IDN URL Spoofing with Georgian Letter Vin

| Field | Value |
|-------|-------|
| **Issue ID** | [40091565](https://issues.chromium.org/issues/40091565) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2018-06-04 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: Version 69.0.3449.0 (Official Build) canary (64-bit)  

Operating System: Mac

**REPRODUCTION CASE**  

-(U+10D5) "ვ" looks like an "3" and it's not easy to catch the spoofing.

Real domain: <http://www.163.com/>

Spoof domain: <http://xn--16-pik.com/>

## Attachments

- [Screen Shot 2018-06-11 at 20.32.58.png](attachments/Screen Shot 2018-06-11 at 20.32.58.png) (image/png, 26.8 KB)

## Timeline

### me...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox UI>Security>UrlFormatting]

### sh...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### pa...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### pa...@chromium.org (2018-06-07)

Since jshin is gone, can somebody else pick this one up?

### jd...@chromium.org (2018-06-07)

I forget but don't we have some system for dealing with this problem generally? Like a blacklist of character points that we don't render? If not, what's the right action here?

### me...@chromium.org (2018-06-07)

There is an additional look-alike character mapping that we use to determine to fall back to punycode: https://cs.chromium.org/chromium/src/components/url_formatter/idn_spoof_checker.cc?rcl=ab8ee841dc483441eac21b5fff2e7d092b05e2a7&l=157

I'll add this character to the list.

### me...@chromium.org (2018-06-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d616695bd68610e75b90d734d72d42534bf01b82

commit d616695bd68610e75b90d734d72d42534bf01b82
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Fri Jun 08 19:19:41 2018

Add confusability mapping entries for Myanmar and Georgian

U+10D5 (ვ), U+1012 (ဒ) => 3

Bug: 847242, 849398
Test: components_unittests --gtest_filter=*IDN*
Change-Id: I9abb8560cf1c9e8e5e8d89980780b89461f7be52
Reviewed-on: https://chromium-review.googlesource.com/1091430
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#565709}
[modify] https://crrev.com/d616695bd68610e75b90d734d72d42534bf01b82/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/d616695bd68610e75b90d734d72d42534bf01b82/components/url_formatter/url_formatter_unittest.cc


### jd...@chromium.org (2018-06-11)

Fixed?

### ch...@gmail.com (2018-06-11)

Verified today in M69.0.3456.0, http://16ვ.com is shown in punycode, so, it's fixed.

### jd...@chromium.org (2018-06-12)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-06-12)

The same thing in issue https://crbug.com/chromium/847242. Fixed.

### sh...@chromium.org (2018-06-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-19)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-06-19)

Approving this merge for M68. Branch:3440

### bu...@chromium.org (2018-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/93c0d219306d70faf545afd6baf3e6f389c76f55

commit 93c0d219306d70faf545afd6baf3e6f389c76f55
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Wed Jun 20 17:45:43 2018

Add confusability mapping entries for Myanmar and Georgian

U+10D5 (ვ), U+1012 (ဒ) => 3

TBR=meacer@chromium.org

(cherry picked from commit d616695bd68610e75b90d734d72d42534bf01b82)

Bug: 847242, 849398
Test: components_unittests --gtest_filter=*IDN*
Change-Id: I9abb8560cf1c9e8e5e8d89980780b89461f7be52
Reviewed-on: https://chromium-review.googlesource.com/1091430
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#565709}
Reviewed-on: https://chromium-review.googlesource.com/1108380
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/branch-heads/3440@{#464}
Cr-Branched-From: 010ddcfda246975d194964ccf20038ebbdec6084-refs/heads/master@{#561733}
[modify] https://crrev.com/93c0d219306d70faf545afd6baf3e6f389c76f55/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/93c0d219306d70faf545afd6baf3e6f389c76f55/components/url_formatter/url_formatter_unittest.cc


### aw...@chromium.org (2018-06-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-21)

But $500 for this one :-)

### aw...@google.com (2018-06-21)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/849398?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091565)*
