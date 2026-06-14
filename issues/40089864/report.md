# Security: IDN URL Spoofing with Cyrillic 	

| Field | Value |
|-------|-------|
| **Issue ID** | [40089864](https://issues.chromium.org/issues/40089864) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox, UI>Internationalization |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2017-12-10 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 65.0.3289.0 (Official Build) canary (64-bit)  

Operating System: All

**REPRODUCTION CASE**

- Expected:  
  
  <http://xn--80aa0cn49azm.com>  
  
  <http://xn--80aktqg1j12a.com>
- Actual:  
  
  [http://рауҏаӏ.com](http://%D1%80%D0%B0%D1%83%D2%8F%D0%B0%D3%8F.com)  
  
  [http://мұѕрасе.com](http://%D0%BC%D2%B1%D1%95%D1%80%D0%B0%D1%81%D0%B5.com)

## Timeline

### el...@chromium.org (2017-12-10)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox UI>Internationalization]

### js...@chromium.org (2017-12-11)

ҏ: U+048F  :  no decomposition
ұ: U+04B1 (Kazakh) : no decomposition.  confusables list has  'y' (Latin Small Letter Y) + combining short stroke overlay (U+0335). 

Both are under 'Extended Cyrillic' subheading.  (
https://unicode.org/cldr/utility/list-unicodeset.jsp?a=\p{subhead=Extended%20Cyrillic} )

When dropping rarely used LGC recently, I didn't drop this and 'Cyrillic supplement' block (and 'Cyrillic - Historic*' sub-block) but meant to review them for further action. 


[Monorail components: UI>Security>UrlFormatting]

### sh...@chromium.org (2017-12-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-12-11)

https://crbug.com/chromium/793628#c2 was sent without being completed. 
At the moment, mapping U+048F (ҏ ) to 'p' and U+04B1 (ұ) to 'y' before calculating the skeleton (instead of disallowing them downright) is  the best solution. 

Moreover, 'Extended Cyrillic' sub-block and 'Cyrillic supplementary' block have to be examined for other cases like that. 



### js...@chromium.org (2017-12-11)

> Moreover, 'Extended Cyrillic' sub-block and 'Cyrillic supplementary' block have to be examined for other cases like that. 


https://goo.gl/bcjPQu  :  NFD_Inert Cyrillic letters currently allowed. Need to go over them all to see if there's any letters to add to the list of characters to be mapped to ASCII-latin before calculating the skeleton. 



### js...@chromium.org (2017-12-11)

> 'Cyrillic - Historic*' sub-block

Forgot that this sub-block is not allowed anyway. 


### js...@chromium.org (2017-12-11)

> add to the list of characters to be mapped to ASCII-latin before calculating the skeleton. 

The list is used to match against top domains (virtually all of them in ASCII-Latin. There's only one exception). 

### js...@chromium.org (2017-12-11)

A subset of characters to consider from https://goo.gl/bcjPQu

 қ 	U+049B	CYRILLIC SMALL LETTER KA WITH DESCENDER
 ҝ 	U+049D	CYRILLIC SMALL LETTER KA WITH VERTICAL STROKE
 ҟ 	U+049F	CYRILLIC SMALL LETTER KA WITH STROKE
 ҡ 	U+04A1	CYRILLIC SMALL LETTER BASHKIR KA
 ң 	U+04A3	CYRILLIC SMALL LETTER EN WITH DESCENDER

### el...@chromium.org (2017-12-12)

Repros in M63.

### sh...@chromium.org (2017-12-13)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-12-16)

I thought of two ways to handle this, but it turned out that the 2nd way wouldn't work. So, I'm left with the following:

Map U+049B (қ) etc to 'k' (do the same for other Cyrillic characters with "accent" that are not decomposed into base + combining mark) before calculating the skeleton of an incoming domain. 



### sh...@chromium.org (2017-12-30)

jshin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2018-01-10)

I'm also looking at these two sets:

[:IdentifierStatus=Allowed:] &  [:Ll:] & [[:sc=Latin:]] & [:NFD_Inert=Yes:]

[:IdentifierStatus=Allowed:] &  [:Ll:] & [[:sc=Greek:]] & [:NFD_Inert=Yes:]


### js...@chromium.org (2018-01-10)

For Latin, use this set: 

[:IdentifierStatus=Allowed:] &  [:Ll:] & [[:sc=Latin:] -[\u01cd-\u01dc] - [\u1e00-\u1e9b] - [\ua720-\ua7ff]] & [:NFD_Inert=Yes:]




### js...@chromium.org (2018-01-10)

https://chromium-review.googlesource.com/#/c/chromium/src/+/860567 is a CL. I nee to add tests. 


### js...@chromium.org (2018-01-10)

[Empty comment from Monorail migration]

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


### ch...@gmail.com (2018-01-13)

Thanks for the fix :-)

### js...@chromium.org (2018-01-13)

Thank you for the report :-). 


### sh...@chromium.org (2018-01-13)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-01-16)

Too late for 63. Will try to get in for 64 after baking in canary/dev. 


### js...@chromium.org (2018-01-16)

Verified in two versions of canary (the latest being 65.0.3322.3 ). 

### js...@chromium.org (2018-01-17)

Made the latest dev channel release as well. 

Asking for merge approval to 64. The actual change [1]  is rather small (a lot of test entries were added along with comments). 


[1] https://chromium-review.googlesource.com/c/chromium/src/+/860567/9/components/url_formatter/idn_spoof_checker.cc



### sh...@chromium.org (2018-01-17)

This bug requires manual review: Less than 2 days to go before AppStore submit on M64
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cm...@chromium.org (2018-01-18)

I don't think this is critical enough to be cherry picked into M64 at this point but letting awhalley@ to make the call.

### aw...@google.com (2018-01-18)

cmasso@, yep, this can wait until M65

### cm...@chromium.org (2018-01-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-22)

Thanks for the report, the VRP panel awarded $500 for this.

### aw...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-14)

This issue was migrated from crbug.com/chromium/793628?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089864)*
