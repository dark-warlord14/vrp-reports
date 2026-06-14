# Security: Whole-script confusable domain label spoofing (Cyrillic)

| Field | Value |
|-------|-------|
| **Issue ID** | [40089282](https://issues.chromium.org/issues/40089282) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox, UI>Internationalization |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2017-10-12 |
| **Bounty** | $500.00 |

## Description

VERSION
Chrome Version: 63.0.3236.0 (Official Build) canary (64-bit)
Operating System: Mac

REPRODUCTION CASE

http://xn--c1ad2baa8a0g.com >> \u0442\u0448\u0456\u0442\u0442\u0435\u0433.com >> тшіттег.com 

## Attachments

- [Windows10-Chrome63.png](attachments/Windows10-Chrome63.png) (image/png, 7.6 KB)
- [Screen Shot 2017-12-11 at 23.56.23.png](attachments/Screen Shot 2017-12-11 at 23.56.23.png) (image/png, 161.5 KB)

## Timeline

### el...@chromium.org (2017-10-12)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox UI>Internationalization]

### wf...@chromium.org (2017-10-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-13)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-10-17)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-10-17)

Another example: http://www.xn--80aj7b8a.com >> еьау.com 

Interesting that this domain appears to be registered for real.

### ch...@gmail.com (2017-10-20)

This is similar to https://crbug.com/chromium/683314 and https://crbug.com/chromium/714628.

### el...@chromium.org (2017-10-25)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-10-27)

jshin, can you take this or find a good person for it?

### sh...@chromium.org (2017-10-27)

jshin: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2017-11-01)

тшіттег.com :  hmm.... how similar/confusable is this to twitter.com ? 

еьау.com  :  how about this ?  

> Interesting that this domain appears to be registered for real.

Because еьау is entirely made of Cyrillic letters, registrars do not block it. 


To block the above two, 'т' and 'ь' have to be added to the confusability set. 

### ca...@gmail.com (2017-11-02)

Yes, my bug (774253) has been marked as a duplicate but I could register шнатѕарр.com.



### sh...@chromium.org (2017-11-16)

jshin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2017-11-18)

The confusables list for 'tw' and 'тш'

https://unicode.org/cldr/utility/confusables.jsp?a=%D1%82%D1%88+tw&r=None



### js...@chromium.org (2017-11-18)

The confusable list for "шнѕ' ad  'whs' . 

https://unicode.org/cldr/utility/confusables.jsp?a=%D1%88%D0%BD%D1%95+whs&r=None



### bu...@chromium.org (2017-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b3f0207c14fccc11aaa9d4975ebe46554ad289cb

commit b3f0207c14fccc11aaa9d4975ebe46554ad289cb
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue Dec 05 09:35:25 2017

Add a few more confusable map entries

1. Map Malaylam U+0D1F to 's'.
2. Map 'small-cap-like' Cyrillic letters to "look-alike" Latin lowercase
letters.

The characters in new confusable map entries are replaced by their Latin
"look-alike" characters before the skeleton is calculated to compare with
top domain names.

Bug: 784761,773930
Test: components_unittests --gtest_filter=*IDNToUni*
Change-Id: Ib26664e21ac5eb290e4a2993b01cbf0edaade0ee
Reviewed-on: https://chromium-review.googlesource.com/805214
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#521648}
[modify] https://crrev.com/b3f0207c14fccc11aaa9d4975ebe46554ad289cb/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/b3f0207c14fccc11aaa9d4975ebe46554ad289cb/components/url_formatter/idn_spoof_checker.h
[modify] https://crrev.com/b3f0207c14fccc11aaa9d4975ebe46554ad289cb/components/url_formatter/top_domains/alexa_domains.list
[modify] https://crrev.com/b3f0207c14fccc11aaa9d4975ebe46554ad289cb/components/url_formatter/top_domains/alexa_skeletons.gperf
[modify] https://crrev.com/b3f0207c14fccc11aaa9d4975ebe46554ad289cb/components/url_formatter/top_domains/make_alexa_top_list.py
[modify] https://crrev.com/b3f0207c14fccc11aaa9d4975ebe46554ad289cb/components/url_formatter/url_formatter_unittest.cc


### ch...@gmail.com (2017-12-05)

[Comment Deleted]

### ch...@gmail.com (2017-12-11)

Verified on 65.0.3291.0 on Mac and Linux. Fixed.


### ch...@gmail.com (2017-12-15)

Shouldn't be marked as fixed?

### el...@chromium.org (2017-12-17)

A patch has landed but perhaps jshin@ plans to do more work here. 

### js...@chromium.org (2018-01-03)

Sorry for the delay. For this particular issue, we can declare it to be fixed. 

I asked for merge of the CL in https://crbug.com/chromium/773930#c15 in https://crbug.com/chromium/784761. 

### sh...@chromium.org (2018-01-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/908ed3e510e06341b8e9143c5e5cea94dad30e30

commit 908ed3e510e06341b8e9143c5e5cea94dad30e30
Author: Jungshik Shin <jshin@chromium.org>
Date: Fri Jan 05 19:46:54 2018

[M64 branch] Add a few more confusable map entries

1. Map Malaylam U+0D1F to 's'.
2. Map 'small-cap-like' Cyrillic letters to "look-alike" Latin lowercase
letters.

The characters in new confusable map entries are replaced by their Latin
"look-alike" characters before the skeleton is calculated to compare with
top domain names.

TBR=jshin@chromium.org

(cherry picked from commit b3f0207c14fccc11aaa9d4975ebe46554ad289cb)

Bug: 784761,773930
Test: components_unittests --gtest_filter=*IDNToUni*
Change-Id: Ib26664e21ac5eb290e4a2993b01cbf0edaade0ee
Reviewed-on: https://chromium-review.googlesource.com/805214
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#521648}
Reviewed-on: https://chromium-review.googlesource.com/852973
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3282@{#421}
Cr-Branched-From: 5fdc0fab22ce7efd32532ee989b223fa12f8171e-refs/heads/master@{#520840}
[modify] https://crrev.com/908ed3e510e06341b8e9143c5e5cea94dad30e30/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/908ed3e510e06341b8e9143c5e5cea94dad30e30/components/url_formatter/idn_spoof_checker.h
[modify] https://crrev.com/908ed3e510e06341b8e9143c5e5cea94dad30e30/components/url_formatter/top_domains/alexa_domains.list
[modify] https://crrev.com/908ed3e510e06341b8e9143c5e5cea94dad30e30/components/url_formatter/top_domains/alexa_skeletons.gperf
[modify] https://crrev.com/908ed3e510e06341b8e9143c5e5cea94dad30e30/components/url_formatter/top_domains/make_alexa_top_list.py
[modify] https://crrev.com/908ed3e510e06341b8e9143c5e5cea94dad30e30/components/url_formatter/url_formatter_unittest.cc


### aw...@google.com (2018-01-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-01-12)

Thanks! The VRP Panel decided to reward $500 for this report.  Cheers!

### aw...@chromium.org (2018-01-12)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/773930?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Omnibox, UI>Internationalization]
[Monorail mergedwith: crbug.com/chromium/774253]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089282)*
