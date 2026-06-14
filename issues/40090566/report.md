# Security: Whole-script confusable domain label spoofing (Cyrillic)

| Field | Value |
|-------|-------|
| **Issue ID** | [40090566](https://issues.chromium.org/issues/40090566) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Internationalization |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2018-02-20 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 66.0.3350.0 (Official Build) canary (64-bit)  

Operating System: All

**REPRODUCTION CASE**

<https://xn--80aa2cah8a7f79b.com> is shown [https://шӊатѕарр.com](https://%D1%88%D3%8A%D0%B0%D1%82%D1%95%D0%B0%D1%80%D1%80.com)

Note: This is similar to <https://crbug.com/chromium/793628>.

## Attachments

- [Screen Shot 2018-03-19 at 17.01.08.png](attachments/Screen Shot 2018-03-19 at 17.01.08.png) (image/png, 33.8 KB)

## Timeline

### el...@chromium.org (2018-02-20)

Is this a top-10K site?

[Monorail components: UI>Internationalization UI>Security>UrlFormatting]

### ch...@gmail.com (2018-02-20)

I think so, since https://xn--80aa1boaj3b9g.com is shown as expected.

### wf...@chromium.org (2018-02-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-02-20)

Thanks for the report. 

U+04CA (ӊ) was missed in https://crbug.com/chromium/793628 because it didn't look like capital H with a font (Symbola ) that happenen to render the character in 
https://goo.gl/orKdsQ for the following set. (the Unicode util page specifies a bunch of fonts and the first one covering U+04CA was 'symbola' with a rather unusual shape for U+04CA). 


[:IdentifierStatus=Allowed:] &  [:Ll:] &
  [[:sc=Cyrillic:] -
  [[\u01cd-\u01dc][\u1c80-\u1c8f][\u1e00-\u1e9b][\u1f00-\u1fff]
  [\ua640-\ua69f][\ua720-\ua7ff]]] &
[:NFD_Inert=Yes:]

### sh...@chromium.org (2018-02-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d52b8375cfe5b56194d3df09c18e7b64e5838369

commit d52b8375cfe5b56194d3df09c18e7b64e5838369
Author: Jungshik Shin <jshin@chromium.org>
Date: Wed Feb 21 18:40:39 2018

Add a few more entries to the confusables list for IDN

U+04CA (ӊ) => h
U+0E1F (ฟ) => w
U+0E23 (ร) => s

Bug: 813925, 813814
Test: components_unittests --gtest_filter=*IDN*
Change-Id: If81ea9bf1c1729f1b6ffc71d718dc5950ac825b5
Reviewed-on: https://chromium-review.googlesource.com/927741
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#538159}
[modify] https://crrev.com/d52b8375cfe5b56194d3df09c18e7b64e5838369/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/d52b8375cfe5b56194d3df09c18e7b64e5838369/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/d52b8375cfe5b56194d3df09c18e7b64e5838369/components/url_formatter/top_domains/test_skeletons.gperf
[modify] https://crrev.com/d52b8375cfe5b56194d3df09c18e7b64e5838369/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2018-02-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-24)

[Empty comment from Monorail migration]

### aw...@google.com (2018-02-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-07)

Thanks! $500 for this.

### aw...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: Less than 28 days to go before AppStore submit on M66
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cm...@google.com (2018-03-19)

Please verify the fix in the latest canary

### ch...@gmail.com (2018-03-19)

verified on canary 67.0.3375.0,  https://шӊатѕарр.comis is shown in punycode as expected. 

### cm...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-03-20)

The CL for this bug was landed on Feb 21 (a week before 66 branch). See https://crbug.com/chromium/813814#c7. 



### ab...@google.com (2018-03-20)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/813814?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090566)*
