# Security: IDN URL Spoofing with using "U+0437" (cyrillic small letter Ze)

| Field | Value |
|-------|-------|
| **Issue ID** | [40090728](https://issues.chromium.org/issues/40090728) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Internationalization |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2018-03-08 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 67.0.3364.0 (Official Build) canary (64-bit)  

Operating System: All

**REPRODUCTION CASE**

<http://xn--g1amdam3je98g4t.com> is shown [https://ԝзѕснооӏѕ.com](https://%D4%9D%D0%B7%D1%95%D1%81%D0%BD%D0%BE%D0%BE%D3%8F%D1%95.com)

Note: "w3schools.com" is a top-10K site.

## Attachments

- [Screen Shot 2018-03-08 at 14.45.02.png](attachments/Screen Shot 2018-03-08 at 14.45.02.png) (image/png, 28.4 KB)
- [Screen Shot 2018-03-16 at 21.23.28.png](attachments/Screen Shot 2018-03-16 at 21.23.28.png) (image/png, 36.9 KB)

## Timeline

### el...@chromium.org (2018-03-09)

[Empty comment from Monorail migration]

[Monorail components: UI>Internationalization UI>Security>UrlFormatting]

### mb...@chromium.org (2018-03-09)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-03-09)

It should be labeled as a ‘sev-medium’ like https://crbug.com/chromium/813814 and others.

### mb...@chromium.org (2018-03-09)

We've been pretty inconsistent with the severity for this type of spoof. Medium and Low are both used fairly frequently. Since that bug is fairly recent I'll up this to medium for consistency, but I'll defer to anyone who deals with this type of issue more often if they want to change it again.

### sh...@chromium.org (2018-03-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-11)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-03-13)

Another example - http://xn--12-6kc4a0ah.com (hoa123.com is also a top-10K site).

### js...@chromium.org (2018-03-13)

Thank you for the report. 

Curiously, U+0417 (З) is in the Unicode confusables list, but its lowercase counterpart U+0437 (з) is not.
The same is true of U+04E0 (Ӡ) and U+04E1 (ӡ). 

https://unicode.org/cldr/utility/confusables.jsp?a=%D0%B7%D3%A1&r=None found more:

U+025C (ɜ), U+1D08 (ᴈ)
U+021D(ȝ)	U+0292(ʒ)	U+04E1(ӡ)	U+10F3(ჳ)	
U+2CCD(ⳍ)	U+A76B(ꝫ). 

U+2CCD is Coptic that is not allowed. Others have to added to confusable map. 
 

### js...@chromium.org (2018-03-13)

Well,  [[\u025c\u1d08\u021d\u0292\u04e1\u10f3\u2ccd\ua76b] & [:IdentifierStatus=Allowed:]]  has only one element, U+04E1.  
( https://goo.gl/p1uKHj )

So, for this bug, U+0437 and U+04E1 have to be mapped to 3. 

'1' (digit 1) will be a can of worms.  (https://crbug.com/chromium/817247 )

### js...@chromium.org (2018-03-13)

$ egrep '^[0-9]{2,}\.' alexa_domains.list | wc -l
50

$ egrep '[0-9]' alexa_domains.list  | wc -l
663

$ egrep '[0-9]{2,}' alexa_domains.list | wc -l
345 




### bu...@chromium.org (2018-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/de9acc5cb3527da9173f01973d849bd47f91a9fd

commit de9acc5cb3527da9173f01973d849bd47f91a9fd
Author: Jungshik Shin <jshin@chromium.org>
Date: Fri Mar 16 02:25:57 2018

Add more to confusables list

U+04FB (ӻ) to f
U+050F (ԏ) to t
U+050B (ԋ) and U+0527 (ԧ) to h
U+0437(з) and U+04E1(ӡ) to 3

Add tests for the above entries and tests for ASCII-digit spoofing.

Bug: 816769,820068
Test: components_unittests --gtest_filter=*IDN*
Change-Id: I6cd0a7e97cd0ec2df522ce30f632acfd7b78eee2
Reviewed-on: https://chromium-review.googlesource.com/962875
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/master@{#543600}
[modify] https://crrev.com/de9acc5cb3527da9173f01973d849bd47f91a9fd/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/de9acc5cb3527da9173f01973d849bd47f91a9fd/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/de9acc5cb3527da9173f01973d849bd47f91a9fd/components/url_formatter/top_domains/test_skeletons.gperf
[modify] https://crrev.com/de9acc5cb3527da9173f01973d849bd47f91a9fd/components/url_formatter/url_formatter_unittest.cc


### ch...@gmail.com (2018-03-16)

Verified today on 67.0.3373.0, ԝзѕснооӏѕ.com is shown as expected. Thanks Jungshik as ever!

### ch...@gmail.com (2018-03-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-03-16)

Thank you for verifying the fix and reporting the bug. 


### sh...@chromium.org (2018-03-17)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-20)

This bug requires manual review: Less than 24 days to go before AppStore submit on M66
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-03-20)

Merge approved - branch:3359

### bu...@chromium.org (2018-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a0909838fdd22cf3de12f2e6f896ac14d82257d0

commit a0909838fdd22cf3de12f2e6f896ac14d82257d0
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue Mar 20 20:50:45 2018

[M66 branch] Add more to confusables list

U+04FB (ӻ) to f
U+050F (ԏ) to t
U+050B (ԋ) and U+0527 (ԧ) to h
U+0437(з) and U+04E1(ӡ) to 3

Add tests for the above entries and tests for ASCII-digit spoofing.

Bug: 816769,820068
Test: components_unittests --gtest_filter=*IDN*
Change-Id: I6cd0a7e97cd0ec2df522ce30f632acfd7b78eee2
Reviewed-on: https://chromium-review.googlesource.com/962875
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#543600}(cherry picked from commit de9acc5cb3527da9173f01973d849bd47f91a9fd)
Reviewed-on: https://chromium-review.googlesource.com/971769
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3359@{#355}
Cr-Branched-From: 66afc5e5d10127546cc4b98b9117aff588b5e66b-refs/heads/master@{#540276}
[modify] https://crrev.com/a0909838fdd22cf3de12f2e6f896ac14d82257d0/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/a0909838fdd22cf3de12f2e6f896ac14d82257d0/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/a0909838fdd22cf3de12f2e6f896ac14d82257d0/components/url_formatter/top_domains/test_skeletons.gperf
[modify] https://crrev.com/a0909838fdd22cf3de12f2e6f896ac14d82257d0/components/url_formatter/url_formatter_unittest.cc


### aw...@chromium.org (2018-03-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-26)

$500 for this report, thanks!

### aw...@chromium.org (2018-03-26)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/820068?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090728)*
