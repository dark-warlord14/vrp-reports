# Security: disallow "Canadian Syllabics" unicode block from IDN domains

| Field | Value |
|-------|-------|
| **Issue ID** | [40087567](https://issues.chromium.org/issues/40087567) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Internationalization |
| **CVE IDs** | CVE-2017-5076, CVE-2017-7764 |
| **Reporter** | sa...@erbbysam.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2017-05-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chromium should prevent the “Canadian Syllabics” unicode block from rendering in domain names with characters from other unicode blocks. This was observed in data found in the Certificate Transparency log while seeking to quantify the IDN impersonation/phishing problem (raw data attached).

I have not contacted other browsers at this time.

**VERSION**  

Chrome Version: Chromium Version 60.0.3089.0 (Developer Build) (64-bit)  

Operating System: Ubuntu 16.04.2 LTS

**REPRODUCTION CASE**  

There are a series of characters in the “CANADIAN SYLLABICS” unicode block which can be used to impersonate other domains. I believe mixing this block with other unicode blocks should be disallowed and the punycode value should be displayed. The characters within this set that I believe could be abused:  

<http://www.fileformat.info/info/unicode/block/unified_canadian_aboriginal_syllabics/list.htm>  

(I do not know the registration status of any of the domains below)  

<http://xn--youtue-084a.com/> -- youtuᖯe.com -- example domain  

<http://xn--youtbe-z72a.com/> -- youtᑌbe.com -- example domain  

<http://xn--uny-8wq.com/> -- ᑭuny.com -- example domain  

<http://xn--oor-hxq.com> -- ᑯoor.com -- example domain  

<http://xn--ego-73q.com/> -- ᒪego.com -- example domain  

<http://xn--fc-lym.com/> -- fcᒿ.com -- example domain is not fc2.com (alexa top 1m #97) -- this is likely the hardest to see (based on the fonts I’m using)  

<http://xn--ulu-7sr.com/> -- ᕼulu.com -- example domain  

<http://invalid.xn--acebook-yp9a.com/> -- ᖴacebook.com -- example domain

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

N/A

---- background ----  

(please excuse the length of this report)  

To form the attached lists, I cross referenced the Google CT Pilot log and the Alexa top 1 million domains (only .com domains).  

There are a fair number of false positives (non-abusive domain impersonations or python unidecode failures), but I choose not to manually remove them.

---- Other unicode characters observed ----

As mentioned in the Chromium IDN policy “We’re working on additional fixes, for example, for confusables within one script set -- “l” (lowercase L) could be confused with “I” (small dotless i character).” I would encourage you to continue this work, the following examples highlight the seriousness of this issue, this data is taken from the attached documents:  

(all domains below will render as unicode in Chromium Version 60.0.3089.0 (Developer Build) (64-bit))

ĸ, 22, 0x138, "LATIN SMALL LETTER KRA"  

96074858, 1509667199, xn--faceboo-jhb.com, facebooĸ.com , ĸ, facebook.com, 3, 1  

86142753, 1507679999, xn--autodes-jhb.com, autodesĸ.com , ĸ, autodesk.com, 697, 1

ł, 5, 0x142, "LATIN SMALL LETTER L WITH STROKE"  

94011919, 1524055021, xn--ppe-8ka60c.com, àppłe.com , àł, apple.com, 69, 1  

94724468, 1500291180, xn--sack-01a.com, słack.com , ł, slack.com, 205, 1

ı, 100, 0x131, "LATIN SMALL LETTER DOTLESS I"  

18331655, 1488327078, xn--reddt-q4a.com, reddıt.com , ı, reddit.com, 7, 1  

95900673, 1500493680, xn--t-fka.com, tı.com , ı, ti.com, 3235, 1  

84518766, 1497998760, xn--gml-kua34j.com, gmȧıl.com , ȧı, gmail.com, 22463, 1  

95900424, 1500493860, xn--fat-jua.com, fıat.com , ı, fiat.com, 54102, 1  

94504694, 1509148799, xn--curacao-egamng-hgc.com, curacao-egamıng.com , ı, curacao-egaming.com, 524456, 1  

94724500, 1500493920, xn--suzu-kza.com, ısuzu.com , ı, isuzu.com, 866480, 1

ì, 25, 0xec, "LATIN SMALL LETTER I WITH GRAVE"  

95900680, 1500670920, xn--twttr-7raz.com, twìttèr.com , ìè, twitter.com, 11, 1  

85019386, 1507161599, xn--polonex-3ya.com, polonìex.com , ì, poloniex.com, 1595, 1  

83724035, 1497798600, xn--gma-pma40b.com, gmaìĺ.com , ìĺ, gmail.com, 22463, 1

---- Special case observed ---

2 interesting domains observed bypasses Chromium checks by using only cyrillic characters:  

07022746, 1443571199, xn--80aac5cct.com, таобао.com , таобао, taobao.com, 10, 1  

10303999, 1461542399, xn--e1anr4f.com, тіме.com , тіме, time.com, 817, 1

## Attachments

- [1-domain_list_sorted_by_alexa.txt](attachments/1-domain_list_sorted_by_alexa.txt) (text/plain, 161.9 KB)
- [2-unicode_chars_observed.txt](attachments/2-unicode_chars_observed.txt) (text/plain, 7.5 KB)
- [3-combined_list.txt](attachments/3-combined_list.txt) (text/plain, 281.8 KB)

## Timeline

### el...@chromium.org (2017-05-08)

[Empty comment from Monorail migration]

[Monorail components: UI>Internationalization UI>Security>UrlFormatting]

### oc...@chromium.org (2017-05-08)

assigning to jshin@ who seem to be handling these. ptal, thanks!

### js...@chromium.org (2017-05-08)

Thanks for the report. 

I've been thinking of  considering dropping CANS or adding a rule to block mixing of Latin+Cans. 

Especially bad ones like fcᒿ.com and youtuᖯe.com would be blocked by my similarity check CL pending review. 


### js...@chromium.org (2017-05-09)

Decided to add a rule to block mixing of Latin + Cans. 

If I block Cans entirely, about 300 domains would be blocked out of a million .com domains (most of them are 'innocent' :-)). 




### sh...@chromium.org (2017-05-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-05-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e2fde40094b4c9b56a7e6342ab1c8bbe75381761

commit e2fde40094b4c9b56a7e6342ab1c8bbe75381761
Author: jshin <jshin@chromium.org>
Date: Sat May 13 01:57:13 2017

Disallow mixing of Canadian Syllabary and [a-z]

BUG=719199
TEST=components_unittests --gtest_filter=*IDNToUn*

Review-Url: https://codereview.chromium.org/2871643005
Cr-Commit-Position: refs/heads/master@{#471538}

[modify] https://crrev.com/e2fde40094b4c9b56a7e6342ab1c8bbe75381761/components/url_formatter/url_formatter.cc
[modify] https://crrev.com/e2fde40094b4c9b56a7e6342ab1c8bbe75381761/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2017-05-13)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-05-13)

> ---- Other unicode characters observed ----

That's dealt with in another bug. 

BTW, I'd not regard these two as confusable:

таобао.com => taobao.com : anyway, taobao.com registered the former. So, they're bundled. 

тіме.com  => time.com : interestingly, тіме.com is redirected to baidu.com 



### sh...@chromium.org (2017-05-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### sa...@erbbysam.com (2017-05-16)

Thanks for the quick fix here!

This issue is also present in Firefox and has been reported to Mozilla under https://bugzilla.mozilla.org/show_bug.cgi?id=1364283

### bu...@chromium.org (2017-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91

commit a8add0308ba6067eb3de5a8fe82f9c2f2460ad91
Author: jshin <jshin@chromium.org>
Date: Fri May 19 06:49:10 2017

Add checks against spoofing attempt at top domains

Remove diacritic marks from a hostname and calculate the confusability
skeleton of the accent-free name. Look it up in the pre-calculated list of
the skeletons of top 10k domains.

Removing diacritic marks from a hostname is equivalent to comparing names with
the primary collation strength in the root locale. To make them equivalent,
three mappings are added (ł > l; ø > o; đ > d) on top of the diacritic-removal.
Also add two more mappings ([кĸκ] > k,  п > n) to supplement the Unicode's
confusables list.

Binary file size increase: ~ 59kB for the DAFSA representation of top
domain name skeletons.

The IDN display policy check takes ~ 2µs longer on the average (3.3 µs => 5.5µs)
on my machine per the test run over ~1 million IDNs in com TLD).

It adds about 1500 domains to the list of domains to display in Punycode out
of ~ 1 million IDNs in com TLD. (3018 => 4571)

In addition, disallow combining diarctic marks unless they're preceded by
Latin-Greek-Cyrillic.

BUG=703750,714628,719199,722639
TEST=components_unittests --gtest_filter=*IDNToUni*

Review-Url: https://codereview.chromium.org/2784933002
Cr-Commit-Position: refs/heads/master@{#473109}

[modify] https://crrev.com/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91/components/url_formatter/BUILD.gn
[modify] https://crrev.com/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91/components/url_formatter/idn_spoof_checker.h
[add] https://crrev.com/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91/components/url_formatter/top_domains/BUILD.gn
[add] https://crrev.com/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91/components/url_formatter/top_domains/README
[add] https://crrev.com/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91/components/url_formatter/top_domains/alexa_domains.list
[add] https://crrev.com/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91/components/url_formatter/top_domains/alexa_skeletons.gperf
[add] https://crrev.com/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91/components/url_formatter/top_domains/make_alexa_top_list.py
[add] https://crrev.com/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91/components/url_formatter/top_domains/make_top_domain_gperf.cc
[modify] https://crrev.com/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91/components/url_formatter/url_formatter.cc
[modify] https://crrev.com/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91/components/url_formatter/url_formatter_unittest.cc


### bu...@chromium.org (2017-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4eec0f46bf71277f9de364ea8f4fb2f41d894b16

commit 4eec0f46bf71277f9de364ea8f4fb2f41d894b16
Author: tsergeant <tsergeant@chromium.org>
Date: Fri May 19 07:24:38 2017

Revert of Mitigate spoofing attempt using Latin letters. (patchset #47 id:850001 of https://codereview.chromium.org/2784933002/ )

Reason for revert:
This CL is causing compile to fail on Win x64:
https://build.chromium.org/p/chromium/builders/Win%20x64/builds/11432

FAILED: obj/components/url_formatter/top_domains/make_top_domain_gperf/make_top_domain_gperf.obj
make_top_domain_gperf.cc(46): error C2220: warning treated as error - no 'object' file generated
make_top_domain_gperf.cc(46): warning C4267: 'argument': conversion from 'size_t' to 'int', possible loss of data

Original issue's description:
> Add checks against spoofing attempt at top domains
>
> Remove diacritic marks from a hostname and calculate the confusability
> skeleton of the accent-free name. Look it up in the pre-calculated list of
> the skeletons of top 10k domains.
>
> Removing diacritic marks from a hostname is equivalent to comparing names with
> the primary collation strength in the root locale. To make them equivalent,
> three mappings are added (ł > l; ø > o; đ > d) on top of the diacritic-removal.
> Also add two more mappings ([кĸκ] > k,  п > n) to supplement the Unicode's
> confusables list.
>
> Binary file size increase: ~ 59kB for the DAFSA representation of top
> domain name skeletons.
>
> The IDN display policy check takes ~ 2µs longer on the average (3.3 µs => 5.5µs)
> on my machine per the test run over ~1 million IDNs in com TLD).
>
> It adds about 1500 domains to the list of domains to display in Punycode out
> of ~ 1 million IDNs in com TLD. (3018 => 4571)
>
> In addition, disallow combining diarctic marks unless they're preceded by
> Latin-Greek-Cyrillic.
>
> BUG=703750,714628,719199,722639
> TEST=components_unittests --gtest_filter=*IDNToUni*
>
> Review-Url: https://codereview.chromium.org/2784933002
> Cr-Commit-Position: refs/heads/master@{#473109}
> Committed: https://chromium.googlesource.com/chromium/src/+/a8add0308ba6067eb3de5a8fe82f9c2f2460ad91

TBR=rsleevi@chromium.org,pkasting@chromium.org,nick@chromium.org,brettw@chromium.org,emilyschechter@chromium.org,jshin@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=703750,714628,719199,722639

Review-Url: https://codereview.chromium.org/2889303003
Cr-Commit-Position: refs/heads/master@{#473118}

[modify] https://crrev.com/4eec0f46bf71277f9de364ea8f4fb2f41d894b16/components/url_formatter/BUILD.gn
[modify] https://crrev.com/4eec0f46bf71277f9de364ea8f4fb2f41d894b16/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/4eec0f46bf71277f9de364ea8f4fb2f41d894b16/components/url_formatter/idn_spoof_checker.h
[delete] https://crrev.com/f677dc5c2d440d6e074a1d624e8a0b7a68371e08/components/url_formatter/top_domains/BUILD.gn
[delete] https://crrev.com/f677dc5c2d440d6e074a1d624e8a0b7a68371e08/components/url_formatter/top_domains/README
[delete] https://crrev.com/f677dc5c2d440d6e074a1d624e8a0b7a68371e08/components/url_formatter/top_domains/alexa_domains.list
[delete] https://crrev.com/f677dc5c2d440d6e074a1d624e8a0b7a68371e08/components/url_formatter/top_domains/alexa_skeletons.gperf
[delete] https://crrev.com/f677dc5c2d440d6e074a1d624e8a0b7a68371e08/components/url_formatter/top_domains/make_alexa_top_list.py
[delete] https://crrev.com/f677dc5c2d440d6e074a1d624e8a0b7a68371e08/components/url_formatter/top_domains/make_top_domain_gperf.cc
[modify] https://crrev.com/4eec0f46bf71277f9de364ea8f4fb2f41d894b16/components/url_formatter/url_formatter.cc
[modify] https://crrev.com/4eec0f46bf71277f9de364ea8f4fb2f41d894b16/components/url_formatter/url_formatter_unittest.cc


### aw...@chromium.org (2017-05-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-19)

How about taking the change from #7 into 59?

### sh...@chromium.org (2017-05-20)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-05-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a586e96794b89bef4729b33369b8c2035564d376

commit a586e96794b89bef4729b33369b8c2035564d376
Author: jshin <jshin@chromium.org>
Date: Mon May 22 07:20:17 2017

Add checks against spoofing attempt at top domains

Original CL (https://codereview.chromium.org/2784933002) was reverted due to
a compile failure on win_x64 (not detected by CQ but detected post-landing).

That issue was addressed using checked_cast.

Remove diacritic marks from a hostname and calculate the confusability
skeleton of the accent-free name. Look it up in the pre-calculated list of
the skeletons of top 10k domains.

Removing diacritic marks from a hostname is equivalent to comparing names with
the primary collation strength in the root locale. To make them equivalent,
three mappings are added (ł > l; ø > o; đ > d) on top of the diacritic-removal.
Also add two more mappings ([кĸκ] > k,  п > n) to supplement the Unicode's
confusables list.

Binary file size increase: ~ 59kB for the DAFSA representation of top
domain name skeletons.

The IDN display policy check takes ~ 2µs longer on the average (3.3 µs => 5.5µs)
on my machine per the test run over ~1 million IDNs in com TLD).

It adds about 1500 domains to the list of domains to display in Punycode out
of ~ 1 million IDNs in com TLD. (3018 => 4571)

In addition, disallow combining diarctic marks unless they're preceded by
Latin-Greek-Cyrillic.

TBR=pkasting@chromium.org
BUG=703750,714628,719199,722639
TEST=components_unittests --gtest_filter=*IDNToUni*
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.win:win_chromium_x64_rel_ng,win10_chromium_x64_rel_ng

Review-Url: https://codereview.chromium.org/2897873002
Cr-Commit-Position: refs/heads/master@{#473519}

[modify] https://crrev.com/a586e96794b89bef4729b33369b8c2035564d376/components/url_formatter/BUILD.gn
[modify] https://crrev.com/a586e96794b89bef4729b33369b8c2035564d376/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/a586e96794b89bef4729b33369b8c2035564d376/components/url_formatter/idn_spoof_checker.h
[add] https://crrev.com/a586e96794b89bef4729b33369b8c2035564d376/components/url_formatter/top_domains/BUILD.gn
[add] https://crrev.com/a586e96794b89bef4729b33369b8c2035564d376/components/url_formatter/top_domains/README
[add] https://crrev.com/a586e96794b89bef4729b33369b8c2035564d376/components/url_formatter/top_domains/alexa_domains.list
[add] https://crrev.com/a586e96794b89bef4729b33369b8c2035564d376/components/url_formatter/top_domains/alexa_skeletons.gperf
[add] https://crrev.com/a586e96794b89bef4729b33369b8c2035564d376/components/url_formatter/top_domains/make_alexa_top_list.py
[add] https://crrev.com/a586e96794b89bef4729b33369b8c2035564d376/components/url_formatter/top_domains/make_top_domain_gperf.cc
[modify] https://crrev.com/a586e96794b89bef4729b33369b8c2035564d376/components/url_formatter/url_formatter.cc
[modify] https://crrev.com/a586e96794b89bef4729b33369b8c2035564d376/components/url_formatter/url_formatter_unittest.cc


### aw...@chromium.org (2017-05-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-22)

Congratulations samrerb@! The VRP panel decided to award $1,000 for this bug.  A member of our finance team will be in touch to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### rs...@chromium.org (2017-05-23)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-05-23)

This appears to be a very big change. Can we please confirm if this is safe to merge? Has this been well tested in canary/dev and is there enough unit test coverage?

### aw...@chromium.org (2017-05-23)

My merge request is for the change in #7 - jshin@, think that's reasonable for 59?

### ab...@chromium.org (2017-05-24)

friendly ping - jshin@ can you please confirm?

### js...@chromium.org (2017-05-25)

Yes, a change in https://crbug.com/chromium/719199#c7 should be merged to 59. 
(sorry for the late reply) 

### ab...@chromium.org (2017-05-25)

Thanks - confirmed with jshin@, it's a safe merge, tested, and with unit test coverage. Approving change in https://crbug.com/chromium/719199#c7 for M59. 

### ab...@chromium.org (2017-05-25)

branch number 3071. 

### aw...@chromium.org (2017-05-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/10cae5571e65f681a46115d41296d3a31d285e29

commit 10cae5571e65f681a46115d41296d3a31d285e29
Author: Jungshik Shin <jshin@chromium.org>
Date: Fri May 26 17:37:26 2017

Disallow mixing of Canadian Syllabary and [a-z]

Merging to 3071 (M59) branch.

BUG=719199
TEST=components_unittests --gtest_filter=*IDNToUn*
TBR=jshin@chromium.org

(cherry picked from commit e2fde40094b4c9b56a7e6342ab1c8bbe75381761)

Review-Url: https://codereview.chromium.org/2871643005
Cr-Original-Commit-Position: refs/heads/master@{#471538}
Change-Id: Ib5b7055b8ecf831e11be79dbe75f2738f4d527e6
Reviewed-on: https://chromium-review.googlesource.com/517223
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3071@{#702}
Cr-Branched-From: a106f0abbf69dad349d4aaf4bcc4f5d376dd2377-refs/heads/master@{#464641}
[modify] https://crrev.com/10cae5571e65f681a46115d41296d3a31d285e29/components/url_formatter/url_formatter.cc
[modify] https://crrev.com/10cae5571e65f681a46115d41296d3a31d285e29/components/url_formatter/url_formatter_unittest.cc


### aw...@chromium.org (2017-05-26)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-05-28)

It turned out that Verisign's script mixing policy does not allow Latin and Canadian syllabics. As a result, none of examples in this bug report (involving mixing Latin and Canadian syllabics) can be registered in any TLDs subject to Verisign's policy.  

https://www.verisign.com/en_US/channel-resources/domain-registry-products/idn/idn-policy/registration-rules/index.xhtml

All code points within an IDN must come from the same Unicode script. This is done to prevent confusable code points from appearing in the same IDN.

https://www.verisign.com/assets/idn/idn-canadian-aboriginal.html does not list any of [a-z]. 


### sa...@erbbysam.com (2017-05-28)

huh, you're correct - I never attempted to register any of the domains above as I was unaware of this policy. Attempting to register any of these domains results with an error "Parameter value policy error (IDN commingles multiple scripts)"

(using the first example above)
https://iwantmyname.com/?domain=youtu%E1%96%AFe
It appears that this is still register-able with certain ccTLD's, but that does significantly limit the scope of this issue.
Thanks,
Sam

### sa...@erbbysam.com (2017-05-28)

I've added this information to https://bugzilla.mozilla.org/show_bug.cgi?id=1364283 as well

### aw...@chromium.org (2017-05-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-05-31)

I'm not sure if this is worth CVE designation ;-). (well, "leaf names" can have any combinations....) 

samreb@: do you know any ccTLD under which this can be registered?  


### sa...@erbbysam.com (2017-06-01)

I have not been able to find any ccTLD's. A few accept youtuᖯe.*, only later to reject it.

### sa...@erbbysam.com (2017-07-20)

Hi, I intend to discuss this issue at a DEFCON (wall of sheep)talk next Friday 7/28. As information about this bug is public through CVE-2017-5076 and the Firefox CVE ( https://www.mozilla.org/en-US/security/advisories/mfsa2017-16/#CVE-2017-7764 ) I do not see any problem with this, but I did want to give you a headsup as this issue is still labeled as restricted.

### mg...@chromium.org (2017-07-21)

I think this is fine (this fix landed in Chrome months ago) (https://crrev.com/471538 is public).

### sh...@chromium.org (2017-08-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-19)

This issue was migrated from crbug.com/chromium/719199?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Internationalization, UI>Security>UrlFormatting]
[Monorail mergedwith: crbug.com/chromium/725461]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087567)*
