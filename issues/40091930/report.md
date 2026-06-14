# Security:IDN url spoofing using U+4e00

| Field | Value |
|-------|-------|
| **Issue ID** | [40091930](https://issues.chromium.org/issues/40091930) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zx...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2018-07-14 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
http://xn--ipaddress-w75n.com/

What is the expected behavior?

What went wrong?
As you disallow U+30FC(ー), but U+4e00(一) still available for spoofing U+002d(-)

Did this work before? N/A 

Chrome version: 67.0.3396.99  Channel: stable
OS Version: 10.0
Flash Version: Shockwave Flash 30.0 r0

## Attachments

- [ip.jpg](attachments/ip.jpg) (image/jpeg, 3.3 KB)

## Timeline

### zx...@gmail.com (2018-07-14)

And see https://www.verisign.com/assets/languagefiles/JPN.html U+4e00 is in the allow set

### es...@chromium.org (2018-07-14)

Another one for you, meacer.

[Monorail components: UI>Browser>Omnibox UI>Security>UrlFormatting]

### me...@chromium.org (2018-07-21)

The fix is to add a pattern for U+4e00 when it's used out of context, but I'm not quite sure what the right context is.

U+30FC is Hiragana-Katakana prolonged sound and is blocked outside Hiragana or Katakana. U+40ee is a generic CJK ideograph, should it be blocked outside either of these scripts, or simply when it appears beside [a-z]?

jshin: Apologies for pulling you into this bug, but do you have an opinion here, as I'm still familiarizing myself with IDN code?


### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-07-30)

sffc: Would be interested in your thoughts re https://crbug.com/chromium/863661#c3.

### sf...@chromium.org (2018-07-30)

In public ICU, both of these strings pass the spoof check, because CJK and ASCII are allowed together.  If one passes and the other fails in Chrome, then it must be because of a custom patch.  I'm not familiar with exactly how spoof checking works in Chrome.

### sf...@chromium.org (2018-07-30)

More precisely, I'm curious to see where in the code U+30FC is handled, and that spot might be a reasonable place to add U+4E00.

There are also a number of other characters in this confusable class that might be worth adding also:

https://unicode.org/cldr/utility/character.jsp?a=30FC

### me...@chromium.org (2018-07-30)

Yes, Chrome has extra rules to block certain combination of characters and scripts: https://cs.chromium.org/chromium/src/components/url_formatter/idn_spoof_checker.cc?rcl=a1e9bc8bbbc83c785a3bfa4b5db1396475cd26ea&l=323


### sf...@chromium.org (2018-07-30)

Ok, so my naive reaction as a non-CJK speaker is that all the "long-dash" confusables should be added alongside U+30FC in that pattern.  However, I do not claim to understand these scripts; it would be wise to check with a native speaker to see what makes sense.

### sh...@chromium.org (2018-08-14)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2018-08-22)

We can't use the same blocking rules for u+4e00 as u+30fc: u+4e00 is the character for "one" and is a component of many phrases that don't consist of Japanese kana.

I don't know what blocking rule we should use though: I've never seen a punycode CJK domain name, and I'm not sure how creative people are about mixing ascii and CJK in that context, so it's hard for me to evaluate what the impact of various blocking heuristics would be.

### dc...@chromium.org (2018-08-23)

[Empty comment from Monorail migration]

### ag...@chromium.org (2018-08-23)

[Empty comment from Monorail migration]

### yu...@chromium.org (2018-08-23)

+1 to https://crbug.com/chromium/863661#c11.  u+4e00 is "one", and we shouldn't simply block it.

I talked offline with Japanese IME team, and found that they think that this is a (sort of) defect of Punycode itself and we don't have an universally-applicable solution that works for all cases.

They introduced to me the following article.  Essentially, this is the same issue, I think.
https://thehackernews.com/2017/04/unicode-Punycode-phishing-attack.html

They showed one idea: Chrome has an indicator of green "Secure" protocol in Omnibox.  As same, Chrome can have an indicator for Punycode URL, or can change the foreground and/or background color of Omnibox to indicate that the URL is Punycode.

I personally think this idea makes sense.


### dc...@chromium.org (2018-08-23)

https://crbug.com/chromium/863661#c12: for the moment, we've been using heuristics to try to detect malicious homoglyph attacks. If a punycode name fails, we fall back to showing the raw encoding. So we were wondering if there was a reasonable heuristic we could use for u+4e00 to fallback to the raw encoded name.

However, I was thinking about this more, and I think even the current heuristics don't always adequately handle confusables. For example, an example using u+30fc and u+4e00:

https://xn--lck2gxb.example.com/ (https://カレー.example.com/, using u+30fc)
vs
https://xn--lck2g660g.example.com/ (https://カレ一.example.com, malicious, using u+4e00)

We can't (easily) block u+4e00 in this context without blocking legitimate phrases that follow the same structure (kana, followed by u+4e00, potentially followed by more kanji/kana). The problem extends the other way as well: someone could add u+30fc at the end of a kana phrase to replace a u+4e00 at the beginning of the next phrase.

### dc...@chromium.org (2018-08-23)

Other CJK confusables for u+30fc / u+4e00:

⼀ (u+2f00: Kangxi Radical One): note that many things in the list of radicals are similarly problematic: https://en.wikipedia.org/wiki/List_of_Unicode_radicals
ㄧ (u+3127: Bopomofo Letter I)

Another confusable for Japanese: ニ (u+30cb: Katakana Letter Ni) and 二 (u+4e8c: Ideograph two; twice CJK)

There's probably others.

### sh...@chromium.org (2018-08-28)

meacer: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### jd...@chromium.org (2018-10-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-30)

Re https://crbug.com/chromium/863661#c11: I looked into the list of all punycode domains. Out of 800K+ domains,
- About 600 have U+4E00 in eTLD+1.
- About 50 mix U+4E00 with an [a-z] character in eTLD+1.
- About 5 have U+4E00 next to an [a-z] character in eTLD+1.

These are pretty small compared to the potential impact of some of the other changes we've been making.

So I suggest the following heuristic:
Block U+4E00 unless it's mixed with Hiragana, Katagana or other CJK ideographs [\u4e00-\u9fff]

Doing this results in around 40 more domains to be punycoded out of 800K+. 27 of these contain ASCII characters and are true positives. The rest is a variety: some of them mix U+4E00 with U+30FC, for example. I think this is an acceptable tradeoff.

dcheng and others, WDYT?

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### dc...@chromium.org (2019-05-02)

I'm not sure it solves the issue of confusables within CJK itself, but it seems better than doing nothing... so sure =)

### dr...@chromium.org (2019-05-31)

Friendly security sheriff ping - any update on this?

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-06-14)

I have a CL at https://chromium-review.googlesource.com/c/chromium/src/+/1659678


### me...@chromium.org (2019-06-17)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/42a0034a20fd53a7b56aa8e65bb6fc4006bf680e

commit 42a0034a20fd53a7b56aa8e65bb6fc4006bf680e
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Wed Jun 19 23:19:07 2019

Block U+4E00 and U+3127 from IDN when used next to non-CJK characters

This CL blocks CJK unified ideograph 一 and Bopofomo letter I (ㄧ) from domain
names if they are next to non-CJK characters. As a result, the domain will be
shown as punycode.

U+2F00 (Kangxi Radical One) is a similar character but it's normalized to U+4E00
and implicitly blocked.

This change doesn't affect any popular domains. It also doesn't prevent attacks
with pure CJK characters, unfortunately. Such attacks are more likely to be
prevented by the lookalike domain warnings launched in M75.

Bug: 863661
Change-Id: I600fef90a0a1ebb12b3c707fa529e4a5711b2c0c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1659678
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Tommy Li <tommycli@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#670711}

[modify] https://crrev.com/42a0034a20fd53a7b56aa8e65bb6fc4006bf680e/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/42a0034a20fd53a7b56aa8e65bb6fc4006bf680e/components/url_formatter/url_formatter_unittest.cc


### me...@chromium.org (2019-06-19)

^ The CL should fix the original report, but I'll keep this open to look into other CJK ideographs.

### va...@chromium.org (2019-07-16)

👋 meacer@ -- any update on this? -- Thanks, Security Marshall.

### me...@chromium.org (2019-07-19)

Follow up CL: https://chromium-review.googlesource.com/c/chromium/src/+/1709769

I'll have another CL to block more characters.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/168897ad6c6d91cba183383cc1613e02dc39ae8f

commit 168897ad6c6d91cba183383cc1613e02dc39ae8f
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Fri Jul 19 19:07:03 2019

Block CJK ideographs looking like slashes in domain names

This CL blocks the following characters from appearing in unicode domain names
when they're surrounded by non-Japanese scripts:
 "丶" (CJK unified ideograph, U+4E36)
 "乀" (CJK unified ideograph, U+4E40)
 "乁" (CJK unified ideograph, U+4E41)
 "丿" (CJK unified ideograph, U+4E3F)

None of these characters are currently used in domain names so the real world
impact is nil.

Bug: 863661
Change-Id: Ifc3a40d46d957bc99383445a71577a0cba744aec
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1709769
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/heads/master@{#679205}

[modify] https://crrev.com/168897ad6c6d91cba183383cc1613e02dc39ae8f/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/168897ad6c6d91cba183383cc1613e02dc39ae8f/components/url_formatter/url_formatter_unittest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a33d878746723ba0505cb6bbddc92a53e8d1c318

commit a33d878746723ba0505cb6bbddc92a53e8d1c318
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Tue Jul 30 23:17:11 2019

Add skeleton mappings for characters that look like hyphens

These characters are already handled by the spoof checks and any domain
containing them are left as punycode. However, ICU generates different
skeletons for some of them, meaning lookalike URL checks don't always
catch domains containing these characters.

This CL fixes this so that two domains differing by one of these
hyphens/dashes always produce the same skeleton string.

Bug: 863661
Change-Id: Ia8d9400b49592d4b5f990323faf615485a8f83ea
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1726760
Auto-Submit: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#682500}

[modify] https://crrev.com/a33d878746723ba0505cb6bbddc92a53e8d1c318/components/url_formatter/spoof_checks/idn_spoof_checker.cc
[modify] https://crrev.com/a33d878746723ba0505cb6bbddc92a53e8d1c318/components/url_formatter/spoof_checks/idn_spoof_checker_unittest.cc


### me...@chromium.org (2019-07-30)

I'll land some more follow up CLs, but the original and the immediate issue is fixed, so I'm closing this for now. We should be able to merge the fix at https://crbug.com/chromium/863661#c32.

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-21)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-08-21)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/863661?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Security>UrlFormatting]
[Monorail mergedwith: crbug.com/chromium/974473]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091930)*
