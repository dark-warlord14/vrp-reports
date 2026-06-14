# [IDN Phishing] Use the "xn--fgb" character to hide the real URL: Block U+0620 on Mac only.

| Field | Value |
|-------|-------|
| **Issue ID** | [40087822](https://issues.chromium.org/issues/40087822) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox>SecurityIndicators, UI>Internationalization |
| **Platforms** | Mac |
| **CVE IDs** | CVE-2017-7763 |
| **Reporter** | wh...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2017-05-23 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

I would like to report URL phishing method.  

There is possibility to use the "xn--fgb" character to hide the real domain address. The "xn--fgb" character allows to use spaces in the address.

Example (url bar):  

google.com .com

Simple Code:  

<a href="http://google.com.xn--fgb.com">link</a>

Attackers can register a new domain or create subdomains on their own hosting.

**VERSION**  

Chrome Version: 58.0.3029.110 (64-bit)  

Operating System: Mac OS 10.12.5

**REPRODUCTION CASE**  

PoC (more "a", more spaces):  

<a href="http://google.com.xn--fgbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com">link</a>

Recommendation:  

The browser should truncate all "spacing" characters in the domain name.

## Attachments

- [phishingidn.jpg](attachments/phishingidn.jpg) (image/jpeg, 105.1 KB)
- [Songti.nooutline.html](attachments/Songti.nooutline.html) (text/plain, 20.4 KB)

## Timeline

### va...@chromium.org (2017-05-23)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-05-23)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox>SecurityIndicators]

### ke...@chromium.org (2017-05-23)

This is a variant of https://crbug.com/chromium/714196. Also Mac only. It still repros on Mac Canary so apparently the fix for that wasn't broad enough.

rsesek did the fix for 714196, but unfortunately he isn't available; is there anyone else who can take this?

[Monorail components: UI>Internationalization UI>Security>UrlFormatting]

### ke...@chromium.org (2017-05-23)

[Empty comment from Monorail migration]

### mg...@chromium.org (2017-05-24)

This maybe be an RTL issue since it involves an Arabic character. Or it may just be the same as https://crbug.com/chromium/714196.

Notes:
xn--fgb is the IDNA encoding of 'ؠ', U+0620 ARABIC LETTER KASHMIRI YEH.
xn--fgbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa is the IDNA encoding of 43 U+0620s in a row.

The URL "http://google.com.xn--fgbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com" is represented in human-readable text as "google.com.ؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠؠ.com". There should be no special problems relating to RTL, because the Arabic characters appear in the middle of Latin characters.

### sh...@chromium.org (2017-05-24)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-05-26)

jshin@: Feel free to pass it on if there is a better owner for this.

### js...@chromium.org (2017-05-26)

Somehow a faulty font or two on Mac OS X claim to support U+0620 but actually has just empty but with non-zero advance glyph for the character?  That is https://crbug.com/chromium/714196. 

If that's the case, we also have to report this to Apple. I wonder why on earth Mac OS X such 'interesting' fonts .....   




### js...@chromium.org (2017-05-26)

Anyway, U+0620 is pretty rare. For branch, we can just drop it from the list of eligible characters ONLY on Mac as is done for https://crbug.com/chromium/714196. 



### js...@chromium.org (2017-05-27)

Like https://crbug.com/chromium/714196, it's "Kaiti SC" (one of Chinese fonts: a couple of other Chinese fonts do the same). Why on earth do they claim to cover U+0620 when all they have for the character is empty advancing glyph?  



### js...@chromium.org (2017-05-27)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-05-28)

Somehow I can't find Kaiti SC font file on my Mac.  I want to see what other characters have an issue described in https://crbug.com/chromium/725660#c10. That requires me to inspect the font. 

BTW, Songti SC also has this issue. It has 447 glyphs without any contour !!! (some of them are supposed to have no contour, but a lot of them NEED to have contour but do not)

### js...@chromium.org (2017-05-28)

I found Kaiti SC and Kaiti TC in /System/Library/Assets/com_apple_MobileAsset_Font3/AssetData  (not in /System/Library/Fonts nor in /Library/Fonts). 




### js...@chromium.org (2017-05-29)

Songti SC has 363 characters (a few of them are space-like so that no contour makes sense, but the rest should have contours) mapped to glyphs without any outline at all. 

It's not just limited to U+0620 and a few Tibetan characters blocked earlier. Interestingly, out of those 363 characters, it appears that a relatively small number of characters are rendered with Songti SC in the UI.  I haven't checked them all, though. (need to come up with  a way to check them all mechanically). 

Kaiti SC has over 1000 glyphs with no outline. Most of them are CJK Ideographs in plane 2. Fortunately, Omnibox does not pick up Kaiti SC for plane 2 CJK ideographs. 

Will report to Apple. 

In the meantime, I'll block U+0620 first. If there are more to block, I'll add them. 

### js...@chromium.org (2017-05-30)

Filed a bug via Apple bug reporter tool ( 32458012 ). 

Songti SC is picked as a fallback font to cover a lot of characters (Arabic, Tibetan, Yi, Mongolian), but Songti SC has empty glyphs for them (no outline). Open the attached file to get the list of characters with this problem.

(U+Exxx can be ignored because they're PUA code points). 





### js...@chromium.org (2017-05-30)

Fortunately, only two characters are IDN-allowed characters out of 300 characters with empty glyphs in Songti SC/TC.  They're U+18AA and U+0620 

Moreover, U+18AA will not be rendered with Songti SC in Omnibox. So, only U+0620 needs to be dropped on Mac OS until the upstream fixes the font issue. 



### js...@chromium.org (2017-05-30)

> Fortunately, only two characters are IDN-allowed characters out of 300 characters with empty glyphs in Songti SC/TC.  They're U+18AA and U+0620 

I meant there are 6 of them, but 4 of them (Tibetan U+0F8C - U+0F8F) are already blocked by rsesek's CL. 

### js...@chromium.org (2017-05-30)

https://chromium-review.googlesource.com/c/517669/ will take care of this issue. 



### bu...@chromium.org (2017-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b9f51ee9599e574847906c650240ea2e4fbc69fb

commit b9f51ee9599e574847906c650240ea2e4fbc69fb
Author: Jungshik Shin <jshin@chromium.org>
Date: Wed May 31 07:51:56 2017

Block U+0620 on Mac from being shown in Unicode in IDN

Mac OS UI fonts renders U+0620 as blank. (radar/32458012)

Bug: chromium:725660
Test: components_unittests --gtest_filter=*IDNToUni*
Change-Id: Ib7d678aae0379e8ac53064663660a7840e5fd3bd
Reviewed-on: https://chromium-review.googlesource.com/517669
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/master@{#475842}
[modify] https://crrev.com/b9f51ee9599e574847906c650240ea2e4fbc69fb/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/b9f51ee9599e574847906c650240ea2e4fbc69fb/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2017-05-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-31)

[Empty comment from Monorail migration]

### wh...@gmail.com (2017-05-31)

Thank you very much for fix! :-)

Best Regards,
Artur

### aw...@chromium.org (2017-06-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-05)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-06-08)

My CL in https://crbug.com/chromium/725660#c19 should be very safe. It's just adding a character to the blacklist on Mac. 


### sh...@chromium.org (2017-06-08)

Your change meets the bar and is auto-approved for M60. Please go ahead and merge the CL to branch 3112 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-06-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-08)

Congratulations! The VRP Panel decided to award $2,000 for this report!! A member of our finance team will be in touch to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-06-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c91a9c1a2bb001b42381f9196a44bea9a31cd671

commit c91a9c1a2bb001b42381f9196a44bea9a31cd671
Author: Jungshik Shin <jshin@chromium.org>
Date: Fri Jun 09 20:01:16 2017

[M60 merge] Block U+0620 on Mac from being shown in Unicode in IDN

Mac OS UI fonts renders U+0620 as blank. (radar/32458012)

TBR=jshin@chromium.org

(cherry picked from commit b9f51ee9599e574847906c650240ea2e4fbc69fb)

Bug: chromium:725660
Test: components_unittests --gtest_filter=*IDNToUni*
Change-Id: Ib7d678aae0379e8ac53064663660a7840e5fd3bd
Reviewed-on: https://chromium-review.googlesource.com/517669
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#475842}
Reviewed-on: https://chromium-review.googlesource.com/530044
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3112@{#297}
Cr-Branched-From: b6460e24cf59f429d69de255538d0fc7a425ccf9-refs/heads/master@{#474897}
[modify] https://crrev.com/c91a9c1a2bb001b42381f9196a44bea9a31cd671/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/c91a9c1a2bb001b42381f9196a44bea9a31cd671/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2017-06-14)

Firefox release notes for the latest mentions https://crbug.com/chromium/714196 (Tibetan characters invisible on Mac). 

https://www.mozilla.org/en-US/security/advisories/mfsa2017-15/#CVE-2017-7763

They didn't mention U+0620. Maybe, have to think about merging to M59? 



### js...@chromium.org (2017-06-14)

The fix for https://crbug.com/chromium/714196 was just merged to M59. The fix for this CL is of the same nature except that another character is blocked on Mac. 

Given Firefox release note/disclosure, we'd better merge this fix to M59 as well. 

A fix is a 1-liner and should be safe. Baked in canary and dev (and possibly beta-60). 

### ab...@chromium.org (2017-06-15)

This merge request missed the RC deadline for M59 stable. We'll need to consider this for a future respin, if that happens.  

### ab...@chromium.org (2017-06-16)

approving merge for M59. 

### js...@chromium.org (2017-06-20)

Thanks for the apporval. merged to M59 (3071) 

### sh...@chromium.org (2017-06-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2017-06-20)

https://chromium-review.googlesource.com/c/540917/ is 3071 branch merge CL. It's landed, but bugdroid somehow hasn't recorded it yet. 

### js...@chromium.org (2017-06-20)

https://chromium.googlesource.com/chromium/src/+/d02373c39ebdc1fb9ef3534502fd57814b680d17 

### aw...@chromium.org (2017-06-28)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-19)

This issue was migrated from crbug.com/chromium/725660?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox>SecurityIndicators, UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087822)*
