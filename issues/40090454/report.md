# Myanmar character in domain names can lead to spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40090454](https://issues.chromium.org/issues/40090454) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Internationalization |
| **Platforms** | Mac |
| **Reporter** | zx...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2018-02-11 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36

Steps to reproduce the problem:
http://google.xn--rid4c.com/ not shown in punycode
and you can regist domain ငဝ.com

What is the expected behavior?

What went wrong?
Myanmar (1000— 109F)
U+1004 (င) => c
U+101d (ဝ) => o
U+100c (ဌ) => g
U+1042 (၂) => j
U+1054 (ၔ) => e

Did this work before? N/A 

Chrome version: 64.0.3282.140  Channel: stable
OS Version: OS X 10.13.3
Flash Version: Shockwave Flash 28.0 r0

## Attachments

- [屏幕快照 2018-02-11 下午11.51.47.png](attachments/屏幕快照 2018-02-11 下午11.51.47.png) (image/png, 8.3 KB)

## Timeline

### el...@chromium.org (2018-02-11)

This could well be working as expected, insofar as "google.co.com" isn't a real domain and doesn't look like one either. Inter-label character set mixing is different than Intra-label mixing. As noted in https://www.chromium.org/developers/design-documents/idn-in-google-chrome,

"Google Chrome decides if it should show Unicode or punycode for each domain label (component) of a hostname separately."


[Monorail components: UI>Internationalization UI>Security>UrlFormatting]

### in...@chromium.org (2018-02-12)

Jshin@, can you please triage and close if this is working as intended.

### js...@chromium.org (2018-02-13)

This is rather interesting. According to registry.co.com, co.com tries to attract those without .com domain to get an alternative ( <foo>.co.com).  

Anyway, this is working as intended.  



### js...@chromium.org (2018-02-14)

I'm adding the following 4 entries to the confusability list for Chrome:

U+1004 (င) => c
U+100c (ဌ) => g
U+1042 (၂) => j
U+1054 (ၔ) => e

Thank you for reporting. 


U+101d (ဝ) => o  // this is already covered by Unicode data. 


### js...@chromium.org (2018-02-14)

[Empty comment from Monorail migration]

### oc...@chromium.org (2018-02-14)

[Empty comment from Monorail migration]

### zx...@gmail.com (2018-02-15)

Thank for the fast fix :-)

### bu...@chromium.org (2018-02-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/37747f4a4972e6d44d3f956f8d3a63255ef0941a

commit 37747f4a4972e6d44d3f956f8d3a63255ef0941a
Author: Jungshik Shin <jshin@chromium.org>
Date: Thu Feb 15 06:56:39 2018

Add more entries to the confusability mapping

U+014B (ŋ) => n
U+1004 (င) => c
U+100c (ဌ) => g
U+1042 (၂) => j
U+1054 (ၔ) => e

Bug: 811117,808316
Test: components_unittests -gtest_filter=*IDN*
Change-Id: I29f73c48d665bd9070050bd7f0080563635b9c63
Reviewed-on: https://chromium-review.googlesource.com/919423
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#536955}
[modify] https://crrev.com/37747f4a4972e6d44d3f956f8d3a63255ef0941a/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/37747f4a4972e6d44d3f956f8d3a63255ef0941a/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/37747f4a4972e6d44d3f956f8d3a63255ef0941a/components/url_formatter/top_domains/test_skeletons.gperf
[modify] https://crrev.com/37747f4a4972e6d44d3f956f8d3a63255ef0941a/components/url_formatter/url_formatter_unittest.cc


### sh...@chromium.org (2018-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-15)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-02-19)

http://google.xn--rid4c.com/ will not be blocked (https://crbug.com/chromium/811117#c1, https://crbug.com/chromium/811117#c3), but if there's a domain in the top 10k list which can be spoofed by 5 Burmese characters in https://crbug.com/chromium/811117#c4, it'll be blocked.



### sh...@chromium.org (2018-02-19)

[Empty comment from Monorail migration]

### aw...@google.com (2018-02-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-26)

Congrats zxyrzg02@ - the VRP panel decided to award $500 for this report. A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in our release notes?

### aw...@chromium.org (2018-02-27)

[Empty comment from Monorail migration]

### zx...@gmail.com (2018-02-27)

[Comment Deleted]

### zx...@gmail.com (2018-03-02)

[Comment Deleted]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-03-19)

Approved for M66 - branch:3359

### js...@chromium.org (2018-03-20)

The CL for this bug was landed on Feb 15 (2 weeks before M66 branch) :-)

See https://crbug.com/chromium/811117#c8. 

### ab...@google.com (2018-03-20)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/811117?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090454)*
