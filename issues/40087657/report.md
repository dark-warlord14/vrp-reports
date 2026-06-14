# IDN URL Spoofing with TIFINAGH LETTER YAN

| Field | Value |
|-------|-------|
| **Issue ID** | [40087657](https://issues.chromium.org/issues/40087657) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox, UI>Internationalization |
| **Platforms** | Mac, Windows |
| **Reporter** | ra...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2017-05-16 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36

Steps to reproduce the problem:
there are some letters which are exactly look alike, I don't know if they're allowed or not but if they're allowed then we've got a serious problem over here.

For example: 

-) “ⵏ” U+2D4F --> http://xn--appe-220c.com/ ( http://appⵏe.com )

What is the expected behavior?
It doesn't covert it into punnycode.

What went wrong?
In the above example; It is extremely difficult (nearly impossible) to distinguish b/w apple.com AND http://xn--appe-220c.com/

Did this work before? N/A 

Chrome version: 58.0.3029.81  Channel: n/a
OS Version: 10.0
Flash Version:

## Attachments

- [Screen Shot 2017-05-15 at 8.10.14 PM.png](attachments/Screen Shot 2017-05-15 at 8.10.14 PM.png) (image/png, 90.9 KB)

## Timeline

### ra...@gmail.com (2017-05-16)

What is the expected behavior?
It should convert the URL into punnycode*

### el...@chromium.org (2017-05-16)

Yet another IDN spoof. Mac screenshot attached.

Unicode Character 'TIFINAGH LETTER YAN' (U+2D4F)


[Monorail components: UI>Browser>Omnibox UI>Internationalization]

### pa...@chromium.org (2017-05-16)

I think we should create a single over-arching Confusables Are Confusing bug and dupe all these individual reports into that one. We shouldn't be handling each Unicode code-point in its own bug report...

### in...@chromium.org (2017-05-16)

I think with c#3, can someone from enamel triage all bugs assigned to jshin@ and club them into one with all current examples.

### sh...@chromium.org (2017-05-16)

[Empty comment from Monorail migration]

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


### js...@chromium.org (2017-05-22)

The CL landed again with a small change is too 'big' to be merged to 58 or 59. (https://crbug.com/chromium/722639#c8)

https://codereview.chromium.org/2894313002/ is a simple CL to address this issue directly and can be "merged" to branches. The file being changed (idn_spoof_check.cc) was spun off from url_format.cc so that a separate branch CL (the change would be exactly the same, but in different files) is necessary. 


### js...@chromium.org (2017-05-22)

See also https://crbug.com/chromium/724968

### js...@chromium.org (2017-05-24)

https://codereview.chromium.org/2894313002/ is in the CQ. 

### bu...@chromium.org (2017-05-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ae6f339fba0736224fdca0b96d2bb1cda42d8ad3

commit ae6f339fba0736224fdca0b96d2bb1cda42d8ad3
Author: jshin <jshin@chromium.org>
Date: Wed May 24 07:46:41 2017

Block Tifinagh + Latin mix

BUG=chromium:722639
TEST=components_unittests --gtest_filter=*IDNToU*

Review-Url: https://codereview.chromium.org/2894313002
Cr-Commit-Position: refs/heads/master@{#474199}

[modify] https://crrev.com/ae6f339fba0736224fdca0b96d2bb1cda42d8ad3/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/ae6f339fba0736224fdca0b96d2bb1cda42d8ad3/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2017-05-24)

[Empty comment from Monorail migration]

### ra...@gmail.com (2017-05-24)

Does it qualify for a bounty?

### sh...@chromium.org (2017-05-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-05-26)

Andrew, is there a reason to merge a fix for 719199 to M59 while not merging a fix for this to M59?  I'm talking about a CL in https://crbug.com/chromium/722639#c12 (NOT a CL in https://crbug.com/chromium/722639#c8). 

Because of the code reorg, merge has to be done manually, but in terms of complexity, the cl for 719199 is exactly the same as the CL in https://crbug.com/chromium/722639#c12.  

Well, in terms of urgency, they're about the same, too. 

### aw...@chromium.org (2017-05-26)

jshin@ - mainly because the change in #12 hasn't made it out to dev yet, which is the usual prerequisite for merges to beta at this stage of the game.

But thanks for calling out, it would be good to take.  What do you think abdulsyed@?

### js...@chromium.org (2017-05-26)

Thanks, Andrew !

(it's more work for me to do a manual merge, but it's better for Chrome, I guess :-)). 


### js...@chromium.org (2017-05-28)

Hmm... actually, we'd not have to bother with merging to 59 branch assuming Verisign follows their script mixing policy. (if they do,   http://xn--appe-220c.com/  cannot be registered). 

Verisign's script-mixing policy would not allow mixing Latin + Tifinagh. Domains under ccTLD do not, either. 

https://www.verisign.com/en_US/channel-resources/domain-registry-products/idn/idn-policy/registration-rules/index.xhtml  : see section 3

https://www.verisign.com/assets/idn/idn-tifinagh.html  does not have [a-z]. OTOH, it has all sorts of 'crazy' combining marks and other characters with Unicode script = Common or Inherited. That's the case of any script policy of Verisign. We need to reach out to get rid of most of those characters (most of them are not allowed by our policy anyway). 



### ab...@chromium.org (2017-05-29)

Based on chat conversation, it's a minimal change, safe merge, and similar cl in crbug/719199 already approved. Approving change in #12 for merge (if still needed). 

### el...@chromium.org (2017-05-29)

> Domains under ccTLD do not, either. 

For all ccTLDs? Is that documented somewhere?

### js...@chromium.org (2017-05-30)

> For all ccTLDs? Is that documented somewhere?

I have not checked all the ccTLDs, but all of them only allow :

1) non-IDN ccTLDs:  allows only [a-z], [0-9], hyphen (ASCII)
2) IDN ccTLDs:  
   a) script native to that IDN (e.g. Israeli IDN only allows Hebrew) + [0-9] + Hyphen
   b) CJK IDN ccTLDs: allows [a-z] in addition to the a). 

 

### bu...@chromium.org (2017-05-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/553ab9ee6347f304fdc581ddcc0d8c84dc6c39e3

commit 553ab9ee6347f304fdc581ddcc0d8c84dc6c39e3
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue May 30 22:23:12 2017

[M59] Block Tifinagh + Latin mix

BUG=chromium:722639
TEST=components_unittests --gtest_filter=*IDNToU*
TBR=abdulsyed@chromium.org


Review-Url: https://codereview.chromium.org/2894313002
Cr-Original-Commit-Position: refs/heads/master@{#474199}
Change-Id: Ia01b85118cb4923a42823174bef4b4327f8c31b4
Reviewed-on: https://chromium-review.googlesource.com/518336
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3071@{#726}
Cr-Branched-From: a106f0abbf69dad349d4aaf4bcc4f5d376dd2377-refs/heads/master@{#464641}
[modify] https://crrev.com/553ab9ee6347f304fdc581ddcc0d8c84dc6c39e3/components/url_formatter/url_formatter.cc
[modify] https://crrev.com/553ab9ee6347f304fdc581ddcc0d8c84dc6c39e3/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2017-05-30)

Anyway, just merged to the branch. 


### lg...@chromium.org (2017-05-31)

[Empty comment from Monorail migration]

[Monorail components: UI>Security>UrlFormatting]

### aw...@chromium.org (2017-06-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-05)

Changing severity to medium given mitigations in #20

### aw...@chromium.org (2017-06-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-05)

Congratulations! The panel decided to award $1,000 for this bug. A member of our finance team will be in touch to arrange payment.

Also, how would you like to be credited in any release notes that may include this bug?

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-06-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-19)

This issue was migrated from crbug.com/chromium/722639?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Internationalization, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087657)*
