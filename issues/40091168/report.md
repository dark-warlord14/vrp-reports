# U+0153 (œ), U+00e6 (æ) may lead to url spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40091168](https://issues.chromium.org/issues/40091168) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox, UI>Internationalization |
| **Platforms** | Mac |
| **Reporter** | zx...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2018-04-21 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36

Steps to reproduce the problem:
https://xn--fabook-jhb.com/
this domain looks like facebook.com in address bar, and it's already alive

What is the expected behavior?

What went wrong?
from https://bugs.chromium.org/p/chromium/issues/detail?id=833138
As it's a different case  from the original issue, I create a new issue about it.
U+0152 (œ) looks like `ce` in address bar, and it's original character are `oe` so it will not be blocked and can spoof lots of domains in top domain list, for example, facebook.com

Did this work before? N/A 

Chrome version: 66.0.3359.117  Channel: stable
OS Version: OS X 10.13.4
Flash Version: Shockwave Flash 29.0 r0

## Attachments

- [facebbook_spoof.png](attachments/facebbook_spoof.png) (image/png, 13.0 KB)

## Timeline

### va...@chromium.org (2018-04-22)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-04-22)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox UI>Internationalization]

### sh...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-04-24)

Well, we can be aggressive, but this seems to be a bit too stretchy. We do have a lot of not-so-likely entries in our supplementary table to be on the safe side. So, I'm not saying this should not be in. 



### zx...@gmail.com (2018-04-25)

[Comment Deleted]

### sh...@chromium.org (2018-05-09)

jshin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2018-05-10)

Definitely not for M66. Maybe, M-67. 



### js...@chromium.org (2018-05-11)

Need to look for similar cases in the set at https://goo.gl/2j6r18 . 

### js...@chromium.org (2018-05-11)

U+00E6 æ => a e
U+04D5 ӕ => a e

Borderline list: 

U+044E ю => i o  ? 
U+044B ы =>  b i or b l 


The above characters + diacritics will be handled automatically because diacritic removal is done earlier. 

### js...@chromium.org (2018-05-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-05-14)

https://chromium-review.googlesource.com/c/chromium/src/+/1055894

### bu...@chromium.org (2018-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f8bc31acf099873ebc623e92908477f2e99c17f6

commit f8bc31acf099873ebc623e92908477f2e99c17f6
Author: Jungshik Shin <jshin@chromium.org>
Date: Wed May 16 02:11:14 2018

Add a few more confusability mapping entries

U+0153(œ) => ce
U+00E6(æ), U+04D5 (ӕ) => ae
U+0499(ҙ) => 3
U+0525(ԥ) => n

Bug: 835554, 826019, 836885
Test: components_unittests --gtest_filter=*IDN*
Change-Id: Ic89211f70359d3d67cc25c1805b426b72cdb16ae
Reviewed-on: https://chromium-review.googlesource.com/1055894
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/master@{#558928}
[modify] https://crrev.com/f8bc31acf099873ebc623e92908477f2e99c17f6/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/f8bc31acf099873ebc623e92908477f2e99c17f6/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/f8bc31acf099873ebc623e92908477f2e99c17f6/components/url_formatter/top_domains/test_skeletons.gperf
[modify] https://crrev.com/f8bc31acf099873ebc623e92908477f2e99c17f6/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2018-05-17)

follow-up bug: crbug.om/843352 


### js...@chromium.org (2018-05-17)

[Empty comment from Monorail migration]

[Monorail components: UI>Security>UrlFormatting]

### sh...@chromium.org (2018-05-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-04)

Thanks zxyrzg02@, $500 for this report.

### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-06-08)

No merge needed

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/835554?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091168)*
