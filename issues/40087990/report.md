# Near homograph URL Spoofing with Arabic

| Field | Value |
|-------|-------|
| **Issue ID** | [40087990](https://issues.chromium.org/issues/40087990) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Internationalization |
| **Reporter** | ra...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2017-06-06 |
| **Bounty** | $1,000.00 |

## Description

http://xn--google-yri.com/ (does not show in punnycode)

What went wrong?
By adding this *ِ* (notice the weird thing under asterisk) we can actually spoof the URL (espicially the inexperienced users)

More info:

U+0650, ARABIC KASRA

## Attachments

- [PoC.png](attachments/PoC.png) (image/png, 18.3 KB)

## Timeline

### el...@chromium.org (2017-06-06)

This one looks reasonably compelling. It's not clear that .COM's registration policy would allow this domain to be registered though.

[Monorail components: Blink>JavaScript>Internationalization UI>Security>UrlFormatting]

### jo...@chromium.org (2017-06-06)

not js related

[Monorail components: -Blink>JavaScript>Internationalization]

### ra...@gmail.com (2017-06-06)

Try: domain.pk for the registration.

### el...@chromium.org (2017-06-06)

Indeed, this spoofing domain is live. 

[Monorail components: UI>Internationalization]

### lg...@chromium.org (2017-06-06)

jshin@, could we blacklist the character that produces the tick?

### mg...@chromium.org (2017-06-07)

This could be a special case of https://crbug.com/chromium/726950 (mixing different scripts).

However, because U+0650 is in the "Mark, Nonspacing" category, it raises the question why punctuation marks like this aren't being universally blocked from appearing in URLs.

### el...@chromium.org (2017-06-07)

Re #6: Maybe I'm missing something, but this isn't punctuation, is it?

Nonspacing mark: A combining character with the General Category of Nonspacing
Mark (Mn) or Enclosing Mark (Me).
• The position of a nonspacing mark in presentation depends on its base character. It generally does not consume space along the visual baseline in and of itself.
• Such characters may be large enough to affect the placement of their base character relative to preceding and succeeding base characters. For example, a circumflex applied to an “i” may affect spacing (“î”), as might the character U+20DD combining enclosing circle.

Perhaps this is more similar to https://crbug.com/chromium/727092 ?

### js...@chromium.org (2017-06-07)

elawrence@ is right. This is not a punctuation. 

Yes, it's similar to https://crbug.com/chromium/727092, but fixing that one wouldn't block this one. 

U+0650 has ScriptExtension=Arabic and Syriac even though Script is Inherited.
https://crbug.com/chromium/727092 is about ScriptExtension={Common,Inherited}. 

So, if we disallow mixing of Latin with any script other than {CJK, Common, Inherited} based on ScriptExtension property, this one would be blocked. That is https://crbug.com/chromium/726950.  Currently, we block mixing of Latin + any scripts other than Greek/Cyrillic (and a few more) bsaed on ScriptExtension values. 

And, this can be registered in Verisign controlled domains because its script mixing rule does not use ScriptExtension but just use Script property. And it allows any characters with Script=Inherited and Script=Common to be mixed with any other script.   Firefox has the same issue because it also does the same as Verisign does. 

And, this one is not blocked by BiDi check, either because its Bidi class is  NSM ( http://unicode.org/cldr/utility/character.jsp?a=0650 )

https://cs.chromium.org/chromium/src/third_party/icu/source/common/uts46.cpp?rcl=dfa798fe694702b43a3debc3290761f22b1acaf8&l=1025

  // 5. In an LTR label, only characters with the BIDI properties L, EN,
  // ES, CS, ET, ON, BN and NSM are allowed.


I'm more tempted to switch over to 'strictly restrictive' rules (https://crbug.com/chromium/726950).
 
An alternative is to just block RTL scripts (Hebrew, Arabic) from mixing with Latin.  (Syriac/Adlam are  disallowed anyway). 


### js...@chromium.org (2017-06-08)

Problematic Arabic NSMs that would crack through various filters:

https://goo.gl/CfmGR6 :  
[:Bidi_Class=Nonspacing_Mark:] &  [:Identifier_Statusβ=Allowed:] &   [:ScriptExtensionsβ=Arabic|Syriac:] 

Arabic — Tashkil from ISO 8859-6 items: 8

 ً 	U+064B	ARABIC FATHATAN
 ٌ 	U+064C	ARABIC DAMMATAN
 ٍ 	U+064D	ARABIC KASRATAN
 َ 	U+064E	ARABIC FATHA
 ُ 	U+064F	ARABIC DAMMA
 ِ 	U+0650	ARABIC KASRA
 ّ 	U+0651	ARABIC SHADDA
 ْ 	U+0652	ARABIC SUKUN
Arabic — Combining maddah and hamza items: 3

 ٓ 	U+0653	ARABIC MADDAH ABOVE
 ٔ 	U+0654	ARABIC HAMZA ABOVE
 ٕ 	U+0655	ARABIC HAMZA BELOW
Arabic — Tashkil items: 1

 ٰ 	U+0670	ARABIC LETTER SUPERSCRIPT ALEF


Hebrew: https://goo.gl/iPpTcQ
 [:Bidi_Class=Nonspacing_Mark:] &  [:Identifier_Statusβ=Allowed:] &   [:ScriptExtensionsβ=Hebrew:] 

 ִ 	U+05B4	HEBREW POINT HIRIQ


### js...@chromium.org (2017-06-08)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-06-08)

Verisign's Latin script policy (https://www.verisign.com/assets/idn/idn-latin.html )  does allow U+0650 and others in the above list except for U+05B4 because its script is Heberew. 

A new similarity check in M60 (diracritic-free + confusability skeleton check) is likely to catch this case against top domains, though. Hmm... it does not. 








### js...@chromium.org (2017-06-08)

http://xn--abc-yql.com/ 

abcฺ.com  with Thai character Phinthu (U+03EA) after 'c' : this cannot be registered at .com TLD (both Script and ScriptExtension of U+03EA are Thai), but we allow it (because we allow mixing of Latin and scripts other than Greek/Cyrillic). The risk is pretty low due to Verisign and Thai ccTLD policy.  

Nonetheless, a case has been building up for switching back to 'strictly restrictive' script mixing from 'moderately restrictive' (https://crbug.com/chromium/726950) *unless* we can come up with a clever way to detect 'base + combining mark' sequences where 'base' and 'combing mark' come from two unrelated scripts (e.g. a Latin base letter + Thai/Arabic combining mark). Even better would be to come up with a way to detect 'base + combining mark' sequences that are NOT used in ANY language. That way, even Latin + U+03xx would be blocked if it's not used in any language at all. 






### lg...@chromium.org (2017-06-08)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-06-08)

https://goo.gl/ZBoLCm is better than what's given in https://crbug.com/chromium/729979#c9 (the result is the same, but better matches my intention). 

[:Bidi_Class=Nonspacing_Mark:] &  [:Identifier_Statusβ=Allowed:] &   [:ScriptExtensionsβ=/Arabic/:] 

--------------

As for https://crbug.com/chromium/729979#c12:

https://goo.gl/kv5NWR  : an example with Thai  : 12 Thai NSM's allowed to mix with Latin by Chrome 
 [:gC=Nonspacing_Mark:] &  [:Identifier_Statusβ=Allowed:] &   [:ScriptExtensionsβ=/Thai/:] 


https://goo.gl/Nhvtgz : 0 code points - Thai NSM's allowed to mix with Latin by Verisign's rules

 [[:gC=Nonspacing_Mark:] &  [:Identifier_Statusβ=Allowed:] &   [:ScriptExtensionsβ=/Thai/:]] - [:sc=Thai:] 

And, there are a lot of S/SE Asian scripts with NSMs allowed to mix with Latin by Chrome (but not by Verisign). 


### js...@chromium.org (2017-06-08)

> A new similarity check in M60 (diracritic-free + confusability skeleton check) is likely to catch this case against top domains, though. Hmm... it does not. 

The reason it does not is that I skip 'dropping NSM' step (transliteration step) for cases in this bug to speed things up. 

  // If input has any characters outside Latin-Greek-Cyrillic and [0-9._-],
  // there is no point in getting rid of diacritics because combining marks
  // attached to non-LGC characters are already blocked.
  if (lgc_letters_n_ascii_.span(ustr_host, 0, USET_SPAN_CONTAINED) ==
      ustr_host.length())
    transliterator_.get()->transliterate(ustr_host);




### js...@chromium.org (2017-06-08)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-06-08)

https://chromium-review.googlesource.com/c/528348 is a narrow-range CL to address this issue alone. 

It'd have been better if comments 12, 14, 15 had been posted to https://crbug.com/chromium/726950 . 


### bu...@chromium.org (2017-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/536f72f4eeb63af895ee489c7244ccf2437cd157

commit 536f72f4eeb63af895ee489c7244ccf2437cd157
Author: Jungshik Shin <jshin@chromium.org>
Date: Fri Jun 09 04:59:19 2017

Disallow Arabic/Hebrew NSMs to come after an unrelated base char.

Arabic NSM(non-spacing mark)s and Hebrew NSMs are allowed to mix with
Latin with the current 'moderately restrictive script mixing policy'.
They're not blocked by BiDi check either because both LTR and RTL labels
can have an NSM.

Block them from coming after an unrelated script (e.g. Latin + Arabic
NSM).

Bug: chromium:729979
Test: components_unittests --gtest_filter=*IDNToUni*
Change-Id: I5b93fbcf76d17121bf1baaa480ef3624424b3317
Reviewed-on: https://chromium-review.googlesource.com/528348
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#478205}
[modify] https://crrev.com/536f72f4eeb63af895ee489c7244ccf2437cd157/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/536f72f4eeb63af895ee489c7244ccf2437cd157/components/url_formatter/url_formatter_unittest.cc


### sh...@chromium.org (2017-06-09)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-06-09)

I think this has to be merged to M-60. Will request for merge to 3112 after a few days of baking in canary (and dev if released). 



### ra...@gmail.com (2017-06-09)

Any bounty for this?

### sh...@chromium.org (2017-06-10)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-06-12)

Typically, issues at Low severity are not awarded. However, I think this issue falls right on the boundary of Low/Medium (the spoof isn't perfect, but it isn't limited to Arabic), so I'll leave it for the panel to consider.

### js...@chromium.org (2017-06-14)

Requesting for merge to M60 branch. It's a simple/safe patch. 

### sh...@chromium.org (2017-06-14)

This bug requires manual review: M60 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-06-16)

security bug, with a simple and safe fix. Approving merge for M60

### sh...@chromium.org (2017-06-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2017-06-20)

Hmm... it's merged to M60 yesterday (3112 branch), but somehow it's not recorded here by bugdroid. 

https://chromium-review.googlesource.com/c/540716/



### js...@chromium.org (2017-06-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-27)

Congratulations rayyanh12@! The VRP panel decided to award $1,000 for this bug! Thanks for the report.

### aw...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/729979?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087990)*
