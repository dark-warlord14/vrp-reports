# Security: IDN spoofing with Combining Dot Above U+0307

| Field | Value |
|-------|-------|
| **Issue ID** | [40088533](https://issues.chromium.org/issues/40088533) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox, UI>Internationalization |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gn...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2017-07-28 |
| **Bounty** | $500.00 |

## Description

DESCRIPTION:
IDN allows spoofing in Omnibox

VERSION
Chrome Version: Version 60.0.3112.78 (Official Build) (64-bit) stable
Operating System: Ubuntu 16.04.2 LTS

REPRODUCTION CASE

http://xn--unicode-8he.org/

>>> "xn--unicode-8he.org".decode("idna")
u'uni\u0307code.org'



## Attachments

- [Screenshot from 2017-07-29 00-54-17.png](attachments/Screenshot from 2017-07-29 00-54-17.png) (image/png, 35.5 KB)
- [Screen Shot 2017-08-25 at 15.46.44.png](attachments/Screen Shot 2017-08-25 at 15.46.44.png) (image/png, 45.9 KB)
- [Screen Shot 2017-08-25 at 15.52.11.png](attachments/Screen Shot 2017-08-25 at 15.52.11.png) (image/png, 37.2 KB)

## Timeline

### el...@chromium.org (2017-07-28)

This spoof works in Chrome 62.3168, although it's possible that registrar policies would prevent it from being registered.

https://unicode-table.com/en/0307/

Maybe related to https://crbug.com/chromium/727092?



[Monorail components: UI>Browser>Omnibox UI>Internationalization]

### va...@chromium.org (2017-07-31)

jshin@ -- this is similar to other IDN spoofing bugs that you have fixed in the past so assigning to you for fixing or triage. thanks.

Please note that the spoof is somewhat apparent.

### el...@chromium.org (2017-07-31)

"Somewhat apparent" seems generous. I don't think more than one user in a thousand would ever notice this, even when looking closely. It's a pixel-perfect spoof on Android. 

### el...@chromium.org (2017-08-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-08-02)

Well,  unicode.org is not in the top domain list :-)  so this type of look-alike is passed through. It's a known issue. 

http://xn--microsoft-6jf.com/  (mi\u0307crosoft.com) is not allowed. 

So, "high value" domains (if they're in the list) are ok as shown in the above example. 

Repeated combining marks are also blocked. However, in this case, Latin small letter i is already normalized (it cannot be decomposed further - e.g. into dotless i + combining dot above - U+0307; if it were, "i + U+0307" would be blocked by the repeated combining mark rule).

We can think of blocking a sequence like 'i + U+0307, j + U+0307, etc". 


### js...@chromium.org (2017-08-03)

> Repeated combining marks are also blocked. 

An example. "café" followed by U+0301 is blocked.  ( café́.com ==> xn--caf-dma49x.com/) 

### el...@chromium.org (2017-08-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-08-10)

See https://crbug.com/chromium/727092#c3 for U+3xx block. 

### sh...@chromium.org (2017-08-25)

jshin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2017-08-25)

I agree that we should forbid i\u0307

BTW, this isn't quite as much of a problem on a Mac, see screenshot1. The dot is clearly strange. And of course, the behavior might be different on Windows / Linux (or on different versions of them). 

However, I tested out various results, and some fonts "absorb" the dot and others don't, even on a Mac. See screenshot 2 (also https://docs.google.com/a/google.com/document/d/1XRQIFoBfKbcpClOXoOje35-Z20GVDo_M16G89vwfYSI/edit?usp=sharing)

Question: are there settings that will change the font showing in the address bar on Chrome?

### do...@chromium.org (2017-08-30)

Friendly security sheriff ping: is there progress on resolving this issue?

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-08)

jshin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2017-09-14)

> Question: are there settings that will change the font showing in the address bar on Chrome?

Afaik,there's no way to change that.  

Anyway, thank you for testing, Mark. 

Somehow, I forgot to land my CL ( https://chromium-review.googlesource.com/c/chromium/src/+/607907 ). I just sent it to CQ. 


### bu...@chromium.org (2017-09-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1f6acd54ee3765d5c1a6f14fc31ddd4a74145314

commit 1f6acd54ee3765d5c1a6f14fc31ddd4a74145314
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue Sep 19 23:32:13 2017

IDN display: Block U+0307 after i or U+0131

U+0307 (dot above) after i, j, l, or U+0131 (dotless i) would be
very hard to see if possible at all. This is not blocked
by the 'repeated diacritic' check because i is not decomposed
into dotless-i + U+0307. So, it has to be blocked separately.

Also, change the indentation in the output of
idn_test_case_generator.py .

This change blocks 80+ domains out of a million IDNs in .com TLD.

BUG=750239
TEST=components_unittests --gtest_filter=*IDN*

Change-Id: I4950aeb7aa080f92e38a2b5dea46ef4e5c25b65b
Reviewed-on: https://chromium-review.googlesource.com/607907
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Matt Giuca <mgiuca@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#502987}
[modify] https://crrev.com/1f6acd54ee3765d5c1a6f14fc31ddd4a74145314/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/1f6acd54ee3765d5c1a6f14fc31ddd4a74145314/components/url_formatter/url_formatter_unittest.cc
[modify] https://crrev.com/1f6acd54ee3765d5c1a6f14fc31ddd4a74145314/tools/security/idn_test_case_generator.py


### js...@chromium.org (2017-09-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-09-21)

Merge-requesting for M62. This CL is very safe and has been baked in canary. 

### sh...@chromium.org (2017-09-21)

This bug requires manual review: M62 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-09-22)

Approving merge to M62. branchL3

### ab...@chromium.org (2017-09-22)

branch:3202*

### as...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### ca...@chromium.org (2017-10-02)

Reminder to please merge to M62 branch 3202 asap.

### aw...@chromium.org (2017-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-10-06)

The VRP panel decided to award $500 for this report - many thanks!

### aw...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/37891167031e03efa0b5ef073d79f3c525bfb1cf

commit 37891167031e03efa0b5ef073d79f3c525bfb1cf
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue Oct 10 20:46:20 2017

[Merge M62] IDN display: Block U+0307 after i or U+0131

U+0307 (dot above) after i, j, l, or U+0131 (dotless i) would be
very hard to see if possible at all. This is not blocked
by the 'repeated diacritic' check because i is not decomposed
into dotless-i + U+0307. So, it has to be blocked separately.

Also, change the indentation in the output of
idn_test_case_generator.py .

This change blocks 80+ domains out of a million IDNs in .com TLD.

BUG=750239
TEST=components_unittests --gtest_filter=*IDN*
TBR=abdulsyed

Change-Id: I4950aeb7aa080f92e38a2b5dea46ef4e5c25b65b
Reviewed-on: https://chromium-review.googlesource.com/607907
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Matt Giuca <mgiuca@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#502987}(cherry picked from commit 1f6acd54ee3765d5c1a6f14fc31ddd4a74145314)
Reviewed-on: https://chromium-review.googlesource.com/709919
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3202@{#645}
Cr-Branched-From: fa6a5d87adff761bc16afc5498c3f5944c1daa68-refs/heads/master@{#499098}
[modify] https://crrev.com/37891167031e03efa0b5ef073d79f3c525bfb1cf/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/37891167031e03efa0b5ef073d79f3c525bfb1cf/components/url_formatter/url_formatter_unittest.cc
[modify] https://crrev.com/37891167031e03efa0b5ef073d79f3c525bfb1cf/tools/security/idn_test_case_generator.py


### js...@chromium.org (2017-10-13)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-10-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### me...@chromium.org (2020-11-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-09-02)

[Empty comment from Monorail migration]

### is...@google.com (2022-09-02)

This issue was migrated from crbug.com/chromium/750239?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Omnibox, UI>Internationalization]
[Monorail mergedwith: crbug.com/chromium/774842]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088533)*
