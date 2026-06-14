# Security: IDN URL Spoofing with using "U+00FE"

| Field | Value |
|-------|-------|
| **Issue ID** | [40090044](https://issues.chromium.org/issues/40090044) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2018-01-03 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 65.0.3310.0  

Operating System: All

**REPRODUCTION CASE**  

PoC: <http://xn--wikiedia-s6a.com/>

wikiþedia.com >> wikiþedia.com

Chrome does not block it.

## Attachments

- [Screen Shot 2018-01-03 at 23.48.09.png](attachments/Screen Shot 2018-01-03 at 23.48.09.png) (image/png, 86.1 KB)

## Timeline

### me...@chromium.org (2018-01-04)

[Empty comment from Monorail migration]

[Monorail components: UI>Security>UrlFormatting]

### sh...@chromium.org (2018-01-04)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-01-09)

Also U+00DE þaypal.com appears to be registered.

### js...@chromium.org (2018-01-10)

U+00DE cannot be used (it's an uppercase Thorn) while U+00FE can be. 

I'll deal with this along with https://crbug.com/chromium/793628. 



### js...@chromium.org (2018-01-11)

https://chromium-review.googlesource.com/c/chromium/src/+/860567 is a CL.

### bu...@chromium.org (2018-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fe3c71592ccc6fd6f3909215e326ffc8fe0c35ce

commit fe3c71592ccc6fd6f3909215e326ffc8fe0c35ce
Author: Jungshik Shin <jshin@chromium.org>
Date: Sat Jan 13 01:11:09 2018

Add more confusable character map entries

When comparing domain names with top 10k domain names for confusability,
characters with diacritics are decomposed into base + diacritic marks
(Unicode Normalization Form D) and diacritics are dropped before
calculating the confusability skeleton because two characters with and
without a diacritics is NOT regarded as confusable.

However, there are a dozen of characters (most of them are Cyrillic)
with a diacritic-like mark attached but they are not decomposed into
base + diacritics by NFD (e.g. U+049B, қ; Cyrillic Small Letter Ka
with Descender).  This CL treats them the same way as their "base"
characters. For instance, қ (U+049B) is treated as confusable with
Latin k because к (U+043A; Cyrillic Small Letter Ka) is.

They're curated from the following sets:

[:IdentifierStatus=Allowed:] &  [:Ll:] &
  [[:sc=Cyrillic:] -
  [[\u01cd-\u01dc][\u1c80-\u1c8f][\u1e00-\u1e9b][\u1f00-\u1fff]
  [\ua640-\ua69f][\ua720-\ua7ff]]] &
[:NFD_Inert=Yes:]

[:IdentifierStatus=Allowed:] &  [:Ll:] &
  [[:sc=Latin:] - [[\u01cd-\u01dc][\u1e00-\u1e9b][\ua720-\ua7ff]]] &
[:NFD_Inert=Yes:]

[:IdentifierStatus=Allowed:] &  [:Ll:] & [[:sc=Greek:]] &
[:NFD_Inert=Yes:]

Bug: 793628,798892
Test: components_unittests --gtest_filter=*IDN*
Change-Id: I20c6af13defa295f6952f33d75987e87ce1853d0
Reviewed-on: https://chromium-review.googlesource.com/860567
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Reviewed-by: Eric Lawrence <elawrence@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/master@{#529129}
[modify] https://crrev.com/fe3c71592ccc6fd6f3909215e326ffc8fe0c35ce/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/fe3c71592ccc6fd6f3909215e326ffc8fe0c35ce/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/fe3c71592ccc6fd6f3909215e326ffc8fe0c35ce/components/url_formatter/top_domains/test_skeletons.gperf
[modify] https://crrev.com/fe3c71592ccc6fd6f3909215e326ffc8fe0c35ce/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2018-01-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-13)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-01-16)

http://xn--wikiedia-s6a.org/ (wikiþedia.org) is now blocked in canary. 

Note that wikiþedia.com is not blocked because wikipedia.com is not in the top domain list. (at the moment, wikipedia.com is redirected to wikipedia.org ; when we update our top domain list, wikipedia.com may be added to the list). 


### ch...@gmail.com (2018-01-16)

Oops! Sorry in https://crbug.com/chromium/798892#c0 I meant wikiþedia.org not wikiþedia.com.

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-01-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-09)

This bug requires manual review: Less than 21 days to go before AppStore submit on M65
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-09)

[Bulk Edit]

+awhalley@ (Security TPM) for M65 merge review

### aw...@google.com (2018-02-09)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cc0bbcbe7c986094da8e58c37a21fdd179b686b0

commit cc0bbcbe7c986094da8e58c37a21fdd179b686b0
Author: meacer <meacer@chromium.org>
Date: Fri Oct 25 01:09:31 2019

Restrict Latin Small Letter Thorn (U+00FE) to Icelandic domains

This character (þ) can be confused with both b and p when used in a domain
name. IDN spoof checker doesn't have a good way of flagging a character as
confusable with multiple characters, so it can't catch spoofs containing
this character. As a practical fix, this CL restricts this character to
domains under Iceland's ccTLD (.is). With this change, a domain name containing
"þ" with a non-.is TLD will be displayed in punycode in the UI.

This change affects less than 10 real world domains with limited popularity.

Bug: 798892, 843352, 904327, 1017707
Change-Id: Ib07190dcde406bf62ce4413688a4fb4859a51030
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1879992
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/heads/master@{#709309}

[modify] https://crrev.com/cc0bbcbe7c986094da8e58c37a21fdd179b686b0/components/url_formatter/spoof_checks/idn_spoof_checker.cc
[modify] https://crrev.com/cc0bbcbe7c986094da8e58c37a21fdd179b686b0/components/url_formatter/spoof_checks/idn_spoof_checker.h
[modify] https://crrev.com/cc0bbcbe7c986094da8e58c37a21fdd179b686b0/components/url_formatter/url_formatter.cc


### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-03)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-03)

This issue was migrated from crbug.com/chromium/798892?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090044)*
