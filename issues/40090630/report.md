# Security: IDN URL Spoofing with using U+04CF 

| Field | Value |
|-------|-------|
| **Issue ID** | [40090630](https://issues.chromium.org/issues/40090630) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Internationalization |
| **Platforms** | Linux, Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2018-02-28 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 66.0.3356.0 (Official Build) canary (64-bit)
Operating System: Mac

- U+04CF (ӏ) looks like an "I" 

http://xn--80aai1bls6k55bcq.com/ (ӏпѕтаԍгам.com)
http://xn--80ajo90d.com/ (ӏкеа.com)

It's not easy to catch the spoofing 

Note on Windows: the URLs are blocked.

## Attachments

- [spoof.png](attachments/spoof.png) (image/png, 21.9 KB)
- [Screen Shot on Windows 7.png](attachments/Screen Shot on Windows 7.png) (image/png, 15.2 KB)

## Timeline

### el...@chromium.org (2018-02-28)

Can you explain what you mean by "the URLs are blocked"?

[Monorail components: UI>Internationalization UI>Security>UrlFormatting]

### ch...@gmail.com (2018-02-28)

E.g http://xn--istagram-irb.com is shown in punycode instead of ӏпѕтаԍгам.com (only on Windows).

### ke...@chromium.org (2018-02-28)

jshin@: Can you have a look at these? These are imperfect homographs, but they still resemble the characters they are spoofing. What is the current expectation on strings like this?

### js...@chromium.org (2018-03-01)

U+04CF on Mac OS/Linux is mapped to lowercase L while on Windows it's mapped to lowercase I.  

Depending on fonts, U+04CF looks different. There's no easy way to handle both cases. 


### sh...@chromium.org (2018-03-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-03-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-03-02)

One possibility is that we generate multiple skeletons to cover font/pltform differences and compare them to the skeletons of top domains we have. 




### js...@chromium.org (2018-03-14)

[\u0131\u0269\u026A\u03B9\u0456\u04CF\u13A5\uA647\U000118C3] & [:IdentifierStatus=Allowed:]
=>


 ı 	U+0131	LATIN SMALL LETTER DOTLESS I
 ι 	U+03B9	GREEK SMALL LETTER IOTA
 і 	U+0456	CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I
 ӏ 	U+04CF	CYRILLIC SMALL LETTER PALOCHKA

Three more characters that may need a similar treatment. 

They're currently folded to 'i'.  In addition to that, we can map them to 'l' (lowercase L) for the 2nd check and calculate the skeleton.  Then, it'd match 'digit 1' as well because digit 1's skeleton is lowercase L. (see https://crbug.com/chromium/820068)



### js...@chromium.org (2018-03-14)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-03-22)

https://chromium-review.googlesource.com/c/chromium/src/+/974165 is a CL. 


### sh...@chromium.org (2018-04-06)

jshin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2018-04-13)

I revised  the CL (https://crbug.com/chromium/817247#c22) to handle only U+04CF.  We need to come up with another way to handle them (mapping 'i' to 'l' is one possibility, but it can affect too many domains). 

I'll file a new bug on them. 


### js...@chromium.org (2018-04-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f9b56bc54fdff5981dba39a707489c3ca9980fac

commit f9b56bc54fdff5981dba39a707489c3ca9980fac
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue Apr 17 06:15:05 2018

Map U+04CF to lowercase L as well.

U+04CF (ӏ) has the confusability skeleton of 'i' (lowercase
I), but it can be confused for 'l' (lowercase L) or '1' (digit) if rendered
in some fonts.

If a host name contains it, calculate the confusability skeleton
twice, once with the default mapping to 'i' (lowercase I) and the 2nd
time with an alternative mapping to 'l'. Mapping them to 'l' (lowercase L)
also gets it treated as similar to digit 1 because the confusability
skeleton of digit 1 is 'l'.

Bug: 817247
Test: components_unittests --gtest_filter=*IDN*
Change-Id: I7442b950c9457eea285e17f01d1f43c9acc5d79c
Reviewed-on: https://chromium-review.googlesource.com/974165
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Eric Lawrence <elawrence@chromium.org>
Cr-Commit-Position: refs/heads/master@{#551263}
[modify] https://crrev.com/f9b56bc54fdff5981dba39a707489c3ca9980fac/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/f9b56bc54fdff5981dba39a707489c3ca9980fac/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/f9b56bc54fdff5981dba39a707489c3ca9980fac/components/url_formatter/top_domains/test_skeletons.gperf
[modify] https://crrev.com/f9b56bc54fdff5981dba39a707489c3ca9980fac/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2018-04-17)

Will ask for merge to M67 after a canary is out. 


### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-23)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-25)

Your change meets the bar and is auto-approved for M67. Please go ahead and merge the CL to branch 3396 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/507d6f67c07f8e0e0bf9d80fe21f38f9903c63e2

commit 507d6f67c07f8e0e0bf9d80fe21f38f9903c63e2
Author: Jungshik Shin <jshin@chromium.org>
Date: Wed Apr 25 21:25:43 2018

[Merge M67] Map U+04CF to lowercase L as well.

U+04CF (ӏ) has the confusability skeleton of 'i' (lowercase
I), but it can be confused for 'l' (lowercase L) or '1' (digit) if rendered
in some fonts.

If a host name contains it, calculate the confusability skeleton
twice, once with the default mapping to 'i' (lowercase I) and the 2nd
time with an alternative mapping to 'l'. Mapping them to 'l' (lowercase L)
also gets it treated as similar to digit 1 because the confusability
skeleton of digit 1 is 'l'.

TBR=govind@chromium.org

Bug: 817247
Test: components_unittests --gtest_filter=*IDN*
Change-Id: I7442b950c9457eea285e17f01d1f43c9acc5d79c
Reviewed-on: https://chromium-review.googlesource.com/974165
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Eric Lawrence <elawrence@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#551263}(cherry picked from commit f9b56bc54fdff5981dba39a707489c3ca9980fac)
Reviewed-on: https://chromium-review.googlesource.com/1028339
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3396@{#309}
Cr-Branched-From: 9ef2aa869bc7bc0c089e255d698cca6e47d6b038-refs/heads/master@{#550428}
[modify] https://crrev.com/507d6f67c07f8e0e0bf9d80fe21f38f9903c63e2/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/507d6f67c07f8e0e0bf9d80fe21f38f9903c63e2/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/507d6f67c07f8e0e0bf9d80fe21f38f9903c63e2/components/url_formatter/top_domains/test_skeletons.gperf
[modify] https://crrev.com/507d6f67c07f8e0e0bf9d80fe21f38f9903c63e2/components/url_formatter/url_formatter_unittest.cc


### aw...@chromium.org (2018-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-27)

$500 for this one :-)

### aw...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-05-15)

Filed https://crbug.com/chromium/843352 about https://crbug.com/chromium/817247#c12

### js...@chromium.org (2018-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/817247?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090630)*
