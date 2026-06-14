# Security: Address bar RTL spoofing using hebrew

| Field | Value |
|-------|-------|
| **Issue ID** | [40088882](https://issues.chromium.org/issues/40088882) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Omnibox, UI>Internationalization>RTL |
| **Platforms** | Mac, iOS |
| **Reporter** | xi...@gmail.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2017-08-31 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS
Address bar RTL spoofing using hebrew

VERSION
Chrome on macOS/IOS

REPRODUCTION CASE
poc.html
<meta http-equiv="content-type" content="text/html;charset=utf-8">

<a href="https://xn--ggbla1c4e.xn--ngbc5azd/#/סוֹ.סח" target="one">click me(in macOS)</a>
<a href="https://xn--ggbla1c4e.xn--ngbc5azd/#/             /סוֹ.סח" target="two">click me(in macOS)</a>
<a href="https://xn--ggbla1c4e.xn--ngbc5azd/?/סוֹ.סח" target="three">click me (in IOS/macOS)</a>


## Attachments

- [spoof.png](attachments/spoof.png) (image/png, 1.0 MB)
- [spoof1.png](attachments/spoof1.png) (image/png, 1.7 MB)
- [poc.html](attachments/poc.html) (text/plain, 374 B)
- [mac-hebrew-domain.png](attachments/mac-hebrew-domain.png) (image/png, 4.5 KB)

## Timeline

### el...@chromium.org (2017-08-31)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox UI>Internationalization>RTL]

### do...@chromium.org (2017-08-31)

mgiuca: can you please triage this?

### mg...@chromium.org (2017-09-01)

This seems to be a combination of two issues:

1. https://crbug.com/chromium/351639, a long-standing issue with the spec (not the implementation) about how RTL URLs are rendered in a confusing way. We are actively working on this.
2. A font issue, that "סוֹ.סח" apparently looks a lot like "no.io" on Mac (it looks extremely different on Linux).

If we assume #1 is solved, we still have to worry about the "סוֹ.סח" being encoded into a domain and looking very similar to ASCII characters. +jshin and +lgarron to comment on that (it's a font issue, really; these characters aren't normally lookalikes).

Note that the Holam (the dot above the 'ו') isn't allowed in IDNA domains, so the spoof is reduced to http://xn--9dbx.xn--cebt (which renders as "סו.סח"). Does that still warrant attention? Attached a screenshot of this in the Mac Omnibox.

### be...@chromium.org (2017-09-01)

[Empty comment from Monorail migration]

### mg...@chromium.org (2017-09-01)

Oops thanks ben.

### do...@chromium.org (2017-09-01)

Assigning medium severity since this is mainly a Mac issue due to fonts.

### mg...@chromium.org (2017-09-01)

Note that the character that most contributes to this (Samekh) is actually supposed to look exactly like an 'o' in sans-serif fonts:
https://en.wikipedia.org/wiki/Samekh

So this could just be subject to our standard whole-script confusables policy (not specifically an issue with the font).

### sh...@chromium.org (2017-09-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-14)

jshin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2017-09-14)

Thank you for the analysis. 

> spoof is reduced to  http://xn--9dbx.xn--cebt (which renders as "סו.סח")

Note that the best we can do about this is to make sure that they don't spoof 'frequently used domains'. 

Both of the following are allowed because io.com and no.com are not in the top 10k list (no.com is not even registered). 

xn--cebt.com
xn--9dbx.com 

Moreover, currently neither 'n' (Latin) or 'o' (Latin) has Hebrew confusable. So, even if 'no.com' or 'io.com' is in the top domain list, 
the above two Hebrew domains wouldn't be flagged.
  
Hebrew Samekh is in the confusable list for 'o'. 

We can locally add U+05D5 and U+05D7 to the confusable list, though. 







### sh...@chromium.org (2017-09-29)

jshin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-11-12)

jshin: regarding c#11, have U+05D5 and U+05D7 been added to the confusable list yet?

### js...@chromium.org (2017-12-04)

Sorry, dominickn@. I forgot about them. 

Let me add them to the confusables list. 


### js...@chromium.org (2017-12-05)


https://unicode.org/cldr/utility/confusables.jsp?a=%D7%95%D7%97%D7%A1&r=None

correction:

U+05D5 (ו ) is in the confusables list (confusable with lowercase Latin L rather than lowercase i)
U+05D7 ( ח ): not in the list
U+05E1 (ס):  in the list (confusable with Lowercase Latin O). 

I'll add U+05D7 to the list. 

As for U+05D5, an example given by Matt in https://crbug.com/chromium/760855#c3 uses U+05D5 followed by U+05B9 to make the sequence look like Latin lowercase I. 

Israel Internet Association's Hebrew IDN rules ( https://www.isoc.org.il/files/docs/ISOC-IL_Registration_Rules_v1.5_ENGLISH_-_26.6.2016.pdf ) allows only a small subset of Hebrew characters (U+05D0 ~ U+05EA). That is, U+05B9 is NOT allowed. 

As such, I'll just block all the Hebrew characters other than U+05D0 ~ U+05EA. 


### js...@chromium.org (2017-12-05)

Well, U+05B9 is already blocked. 

https://goo.gl/eZNpjA ([:Identifier_Status=Allowed:] & [:sc=Hebrew:] ) has the following characters (other than [U+05D0, U+05EA] . I'll look into tightening the set further in another bug. 


 ִ 	U+05B4	HEBREW POINT HIRIQ

Hebrew — Yiddish digraphs items: 3

 ‎װ‎ 	U+05F0	HEBREW LIGATURE YIDDISH DOUBLE VAV
 ‎ױ‎ 	U+05F1	HEBREW LIGATURE YIDDISH VAV YOD
 ‎ײ‎ 	U+05F2	HEBREW LIGATURE YIDDISH DOUBLE YOD
Hebrew — Punctuation items: 2

 ‎׳‎ 	U+05F3	HEBREW PUNCTUATION GERESH
 ‎״‎ 	U+05F4	HEBREW PUNCTUATION GERSHAYIM

### js...@chromium.org (2017-12-05)

סוֹ.com  :  This will be shown in punycode due to U+05B9. 
סח.com  : This is currently shown in Unicode. It'll be blocked by adding U+05D7 (ח) to the list (to be confusable with Latin lowercase N). 

### js...@chromium.org (2017-12-05)

> סח.com  : This is currently shown in Unicode. It'll be blocked by adding U+05D7 (ח) to the list (to be confusable with Latin lowercase N).

Only if there's 'no.com'  in the top 10k list, it'll be blocked.

However, it's a bit more complicated because we need a 'visual' skeleton match (as opposed to 'logical') skeleton match.  I'll hold this off from M63. (when writing https://crbug.com/chromium/760855#c18, I meant to add it to 
https://chromium-review.googlesource.com/805214) ). 


### ra...@chromium.org (2018-01-30)

jshin: Friendly ping from security sheriff. Any update here? 

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### xi...@gmail.com (2018-04-12)

Any update here?

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-12-03)

jshin is no longer working on Chromium, assigning to myself.

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### xi...@gmail.com (2019-02-21)

Any update here?

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### ad...@google.com (2019-05-02)

Chatted with meacer@. We think this might be solvable only by pixel-wise comparison of URIs relative to browsing history - there is a plan to get some interns to look into this. ccing Carlos and Livvie as the interns will be in their bubble.

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-08-19)

Carlos and Livvie: does this still seem possibly in-scope for the TrickURI automation stuff?
- a friendly security marshal

### li...@chromium.org (2019-08-19)

Partially--I'd say being able to do pixel-wise comparison is within scope, but we aren't yet doing anything about comparing relative to browsing history (vs top site).

### ct...@chromium.org (2019-09-03)

Per our new(ish) spoofing triage guidelines, dropping this to Severity-Low since it doesn't actually affect any top domains.

Based on https://crbug.com/chromium/760855#c18 and https://crbug.com/chromium/760855#c19 we should add U+05D7 -> n to the local confusables mapping: https://crrev.com/c/1780950 will add that. I think this should close out this bug.

For the remaining threads of conversation here:

We are tracking the RTL component ordering issue in https://crbug.com/chromium/351639. This will most likely require a spec change (which I've taken on but haven't gotten around to yet).

https://crbug.com/chromium/722167 tracks whole-script confusables -- I'll add a note there that we might want to have a Hebrew-Latin mapping for this case (for labels that contain only Hebrew-Latin confusables as discussed in this bug).

The remaining piece (how to detect these when there isn't a top domain to match against) sounds like a separate enhancement to our existing confusables detection rather than a remaining part of the bug here. We don't currently consider confusables against per-user history/engagement but it is something we have been looking into. We've launched our Lookalike warning for top domains (https://crbug.com/chromium/843361), and are experimenting with also applying it to per-user browsing history, which could help catch some of these.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d99aae95a0e37de6fe673ffdc5734f91ad7e8e52

commit d99aae95a0e37de6fe673ffdc5734f91ad7e8e52
Author: Christopher Thompson <cthomp@chromium.org>
Date: Tue Sep 03 23:26:18 2019

Add U+05D7 to confusables mapping

This maps U+05D7 (ח) to lowercase Latin n and adds a test domain and
test case for the mapping.

Bug: 760855
Change-Id: I67f532b32785caba7aa1c7d497fdfd20b4820a56
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1780950
Reviewed-by: Tommy Li <tommycli@chromium.org>
Commit-Queue: Christopher Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/heads/master@{#692910}

[modify] https://crrev.com/d99aae95a0e37de6fe673ffdc5734f91ad7e8e52/components/url_formatter/spoof_checks/idn_spoof_checker.cc
[modify] https://crrev.com/d99aae95a0e37de6fe673ffdc5734f91ad7e8e52/components/url_formatter/spoof_checks/idn_spoof_checker_unittest.cc
[modify] https://crrev.com/d99aae95a0e37de6fe673ffdc5734f91ad7e8e52/components/url_formatter/spoof_checks/top_domains/test_domains.list
[modify] https://crrev.com/d99aae95a0e37de6fe673ffdc5734f91ad7e8e52/components/url_formatter/spoof_checks/top_domains/test_domains.skeletons


### ct...@chromium.org (2019-09-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-04)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-06)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $500 for this report :) 

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-17)

Description says this affects iOS too.

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

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

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/760855?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Internationalization>RTL]
[Monorail blocked-on: crbug.com/chromium/351639]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088882)*
