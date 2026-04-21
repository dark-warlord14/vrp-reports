# Security: Whole-script confusable domain label spoofing (Cyrillic)

| Field | Value |
|-------|-------|
| **Issue ID** | [40086586](https://issues.chromium.org/issues/40086586) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox, UI>Internationalization |
| **Reporter** | wr...@slicealias.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2017-01-20 |
| **Bounty** | $2,000.00 |

## Description

See https://www.xn--80ak6aa92e.com/ - if you compare with https://www.apple.com/, URL looks identical on Windows and Linux. On OS X, the font is slightly different, and it is potentially possible to distinguish between the two.

The domain xn--80ak6aa92e.com is currently proxying requests to apple.com to demonstrate how difficult it is to distinguish the malicious domain. I will  take it offline in the near future.

This issue also exists in Firefox and has been reported to them as well. On Safari, the URL does not appear as "apple.com", likely because Safari interprets some of the characters as belonging to a different language.

## Timeline

### pa...@chromium.org (2017-01-20)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox UI>Localization]

### pa...@chromium.org (2017-01-20)

For reference:

>>> x = "аррӏе"
>>> x.decode("utf-8")
u'\u0430\u0440\u0440\u04cf\u0435'

All Cyrillic (http://www.fileformat.info/info/unicode/char/0435/index.htm).

I had thought that we had a system in which, if your normal locale/language settings indicate you use a language that does not use (e.g.) Cyrillic, then we'd show Punycode? But Cyrillic users would see the Cyrillic? Did that regress, or am I misremembering?

### jw...@chromium.org (2017-01-20)

mgiuca@, are you the right person to take a look at this?

[Monorail components: UI>Security>UrlFormatting]

### mg...@chromium.org (2017-01-23)

#0:

> The domain xn--80ak6aa92e.com is currently proxying requests to apple.com to demonstrate how difficult it is to
> distinguish the malicious domain. I will  take it offline in the near future.

If you want to, in good faith, demonstrate a vulnerability like this, you should not proxy to the real site; that can be seen as an actual phishing attempt. Instead just show a simple page that demonstrates you were able to register the domain. If you don't publish the link anywhere, I *believe* this will not run afoul of our responsible disclosure rule for reporting bugs.

#2 Python 2's Unicode support makes me sad.

>>> x = "аррӏе"
>>> print(ascii(x))
'\u0430\u0440\u0440\u04cf\u0435'

These are all Cyrillic confusables with the ASCII letters "apple". This is what's known as a "whole-script confusable" (not mixing letters from different scripts). It's very hard to stop this by technical means since there's nothing intrinsically wrong with it; it's just a collection of Cyrillic letters like any Russian word.

This is a well-known problem which used to be documented here:
https://www.chromium.org/developers/design-documents/idn-in-google-chrome
but that section was recently removed because it was out of date.

> I had thought that we had a system in which, if your normal locale/language
> settings indicate you use a language that does not use (e.g.) Cyrillic, then
> we'd show Punycode? But Cyrillic users would see the Cyrillic? Did that
> regress, or am I misremembering?

That system has been gone for about a year now (jshin did it). I believe the rationale was a) for compatibility with Firefox, b) because it meant all users got a different experience and c) it didn't actually stop exploits, just segmented which users were exploitable.

Anyway, there has been an internal discussion on this very topic over the past week. It's clear that this is a problem but there is no easy fix (other than removing Cyrillic characters from domains entirely).

I think in the short term this is WontFix (might be a dupe). Assigning to Jungshik who knows this stuff.

### pk...@chromium.org (2017-01-23)

To summarize my comment from the internal discussion: I think the primary action here should be that the browser vendors, as a group, have a formal dialog with registrars to (a) report individual bad cases and (b) convince registrars to enact policies to prevent registration of such confusables.

The registrar for .com should not allow "apple.com" and "аррӏе.com" to be registered to different organizations.

Separately, perhaps there is a secondary solution where the Safe Browsing pipeline can look for domain names that are whole-script confusable with other known domain names and use that as a very strong signal of bad intent.

I don't know who should take point on these actions, but I think they amount to more than "WontFix".

### wr...@slicealias.com (2017-01-23)

The growing nature of unicode might make it difficult for registrars to maintain a blacklist and block malicious domains. There are also existing domains such as http://xn--80aj.com/ that may be confusing but serve a legitimate purpose.

What about handling punycode domains the Safari way (with a whitelist), as specified on https://www.chromium.org/developers/design-documents/idn-in-google-chrome. 

### es...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### mg...@chromium.org (2017-01-23)

> There are also existing domains such as http://xn--80aj.com/ that may be
> confusing but serve a legitimate purpose.

What legitimate purpose does http://xn--80aj.com/ (еа.com) serve? Is that a legitimate Cyrillic domain?

> What about handling punycode domains the Safari way (with a whitelist)

We do have a whitelist. Essentially you're suggesting that we remove Cyrillic and Greek characters from the list. I'm not sure we want to go down that path.

### wr...@slicealias.com (2017-01-23)

Registrars are likely not going to revoke existing domains that are confusing such as the ea.com domain, and the ideal solution should be make it possible to distinguish existing domains that are identical. What about displaying Cyrillic and Greek characters with a different style on Linux and Windows, the way it is already done on OS X?

### pk...@chromium.org (2017-01-23)

I don't know what you mean by "with a different style".  You mean, in a different font?  Or were you referring to Safari using punycode in https://crbug.com/chromium/683314#c0?  Users won't notice/understand the meaning of the former, and the latter is intentional.

### sh...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-01-23)

Would this bug be more correctly titled: "Regression: Whole-script confusable labels allowed by IDN Policy"?

With a regressing CL of https://bugs.chromium.org/p/chromium/issues/detail?id=336973#c34 ?

### mg...@chromium.org (2017-01-23)

I don't think this is really a regression -- for example anyone who had Russian as a language would've been subject to this spoof before that change. This just makes the policy consistent for all users and therefore exposes all users to the whole-script confusable spoofing. I'll retitle it though.

### js...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-01-31)

[Empty comment from Monorail migration]

### xz...@chromium.org (2017-02-01)

[Empty comment from Monorail migration]

### xz...@chromium.org (2017-02-01)

+CC reporter from https://crbug.com/chromium/687286.

### sh...@chromium.org (2017-02-09)

jshin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2017-02-15)

https://codereview.chromium.org/2683793010/ has a draft CL to check for domains entirely made up of a small set of Cyrillic letters that look like Latin letters. 

When the check is on unconditionally (PS #1), about 800 domains in .рф is blocked out of 861657 IDNs (as of March 2016) in рф (0.1%). 

PS #2 applies the check only to domains with a non-IDN TLD (com, net, uk, etc). I'll collect the stat against com and a couple of other gTLDs. 

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### em...@chromium.org (2017-03-22)

@jshin, could you provide an update here? are you on track for M59 for this short-term fix?

### bu...@chromium.org (2017-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/08cb718ba7c3961c1006176c9faba0a5841ec792

commit 08cb718ba7c3961c1006176c9faba0a5841ec792
Author: jshin <jshin@chromium.org>
Date: Thu Mar 23 21:25:32 2017

Block domain labels made of Cyrillic letters that look alike Latin

Block a label made entirely of Latin-look-alike Cyrillic letters when the TLD is not an IDN (i.e. this check is ON only for TLDs like 'com', 'net', 'uk', but not applied for IDN TLDs like рф.

BUG=683314
TEST=components_unittests --gtest_filter=U*IDN*

Review-Url: https://codereview.chromium.org/2683793010
Cr-Commit-Position: refs/heads/master@{#459226}

[modify] https://crrev.com/08cb718ba7c3961c1006176c9faba0a5841ec792/components/url_formatter/url_formatter.cc
[modify] https://crrev.com/08cb718ba7c3961c1006176c9faba0a5841ec792/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2017-03-24)

Fixed in the trunk

### sh...@chromium.org (2017-03-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-03-24)

[Empty comment from Monorail migration]

[Monorail components: -UI>Localization UI>Internationalization]

### aw...@google.com (2017-03-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-10)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-10)

Congratulations! The VRP panel decided to award $2,000 for this report.  A member of our finance team will be in touch shortly to arrange payment.  Cheers!

### aw...@chromium.org (2017-04-10)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-14)

Requesting merge per email conversation.

### sh...@chromium.org (2017-04-14)

This bug requires manual review: We are only 10 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2017-04-15)

Per https://crbug.com/chromium/683314#c31, approving for M58. Please merge. 

### aw...@chromium.org (2017-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-17)

Merge to M58 https://codereview.chromium.org/2823803004

### go...@chromium.org (2017-04-18)

Per https://crbug.com/chromium/683314#c36 if this is already merged to M58, please apply "merge-merged-3029" label and remove "Merge-Approved-58" label. Thank you.

### sh...@chromium.org (2017-04-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-04-18)

I was expecting bugdroid to do its thing, ha well.

Double checked the cherry pick is showing up on https://chromium.googlesource.com/chromium/src/+log/refs/branch-heads/3029 so I think we're all good.

### js...@chromium.org (2017-04-18)

sorry about the delay. I'm merging to m58 now. 


### js...@chromium.org (2017-04-18)

ooops. it's already merged. 


### aw...@google.com (2017-04-18)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-19)

Opening up bug since the issue is public.

### aw...@chromium.org (2017-04-19)

[Empty comment from Monorail migration]

### to...@chromium.org (2017-04-21)

How would you guys feel about using a pre-generated list of homoglyphs (https://github.com/codebox/homoglyph) to test domains vs. the Alexa 1000 top domains?

Basically -- render in punycode any domain that "looks like" a top site, but isn't really.

### mo...@mertinkat.net (2017-04-24)

Adding cyrillic character "к"[1] which looks like latin "k" to the "cyrillic_letters_latin_alike_" variable[2] would be a good idea.

>>> x = "ӏіпкеԁіп.com"
>>> x.decode("utf-8")
u'\u04cf\u0456\u043f\u043a\u0435\u0501\u0456\u043f.com'


[1] http://www.fileformat.info/info/unicode/char/043a/index.htm
[2] https://cs.chromium.org/chromium/src/components/url_formatter/url_formatter.cc?type=cs&q=cyrillic_letters_latin_alike_+package:%5Echromium$&l=335

### ma...@google.com (2017-04-24)

In practice it looks distinct enough to not be a problem; look at "looк
кids" to see how they look strange enough to alert people.

Mark

### mo...@mertinkat.net (2017-04-24)

[Comment Deleted]

### mo...@mertinkat.net (2017-04-24)

ъut thҽп somҽ othҽг cyrillic chaгactҽгs aгe also distiпct ҽпough (like ъ, Ь, ҽ)...

### to...@gmail.com (2017-04-24)

@ https://crbug.com/chromium/683314#c49: I think we need a list of all fonts used for the omnibar over the various OSes. That it looks distinctive on your PC doesn't mean it does for everybody

### lg...@chromium.org (2017-04-24)

re: last few comments: This bug is about perfect spoofs. Other near-homoglyphs are https://crbug.com/chromium/703750.

### mo...@mertinkat.net (2017-04-24)

Ok guys, this is only for "perfect spoofs"? Well, then I don't understand why you added these characters: "ъЬҽпгѵѡ". These are not perfect spoofs with the font used in the address bar in Chrome 58 on Windows 7 and 10.

The "к" character is not a perfect spoof either but might be misleading for an unexperienced user just like the characters "ъЬҽпгѵѡ".
And (like https://crbug.com/chromium/683314#c50 said) it also depends on the font used in Chrome which means that there might be a perfect spoof or not for any of the given characters in "cyrillic_letters_latin_alike_".

That said I'd appreciate if I could have access to https://crbug.com/chromium/703750.

Thanks!


### lg...@chromium.org (2017-04-24)

[Empty comment from Monorail migration]

### mo...@mertinkat.net (2017-04-26)

Would you accept a pull request to add that character? Or shall we just leave it as inconsistent as it is?

Not sure what to do and I don't have access to 703750 in case this is not the right place to discuss cyrillic/latin similarities.

### me...@chromium.org (2017-04-26)

https://crbug.com/chromium/683314#c54: I opened up https://crbug.com/chromium/703750.

### aa...@google.com (2017-05-09)

[Empty comment from Monorail migration]

### mm...@chromium.org (2017-06-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### bl...@gmail.com (2018-09-14)

[Comment Deleted]

### bl...@gmail.com (2018-09-14)

[Comment Deleted]

### bl...@gmail.com (2018-09-14)

[Comment Deleted]

### be...@gmail.com (2018-09-14)

[Comment Deleted]

### bl...@gmail.com (2018-09-14)

[Comment Deleted]

### be...@gmail.com (2018-09-14)

[Comment Deleted]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### tr...@gmail.com (2022-11-07)

Metoo

### is...@google.com (2022-11-07)

This issue was migrated from crbug.com/chromium/683314?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Internationalization, UI>Security>UrlFormatting]
[Monorail blocking: crbug.com/chromium/687286]
[Monorail mergedwith: crbug.com/chromium/687286, crbug.com/chromium/719143, crbug.com/chromium/735458]
[Monorail components added to Component Tags custom field.]

### ac...@gmail.com (2024-04-20)

In a reply to the comment #6, I prefer not to rely on registrars as they can be slow, incompetent or just corrupt. Examples with .com registrars are best scenarios. This mindset is like hoping for the best from all registrars... All the time...

Standards and browsers should have more secure options and checks IMHO.

### ac...@gmail.com (2024-04-20)

I also have a related note about URL/domain display using confusing characters along the text after noting the comment #6 here and testing it against latest Canary version.

See a new issue about it: https://issues.chromium.org/issues/335829874

### pe...@google.com (2024-11-06)

The older reward-topanel [issue 40051657](https://issues.chromium.org/issues/40051657) has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.

### am...@google.com (2024-11-14)

silly bot, the older issue is not actually older, but an artifact of issue IDs being out of order from the buganizer migration and this issue already has a VRP reward

### au...@gmail.com (2025-11-02)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086586)*
