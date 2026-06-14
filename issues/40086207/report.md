# Security: Unicode hyphens in domain names are not blacklisted

| Field | Value |
|-------|-------|
| **Issue ID** | [40086207](https://issues.chromium.org/issues/40086207) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | ar...@rawsec.net |
| **Assignee** | mg...@chromium.org |
| **Created** | 2016-12-14 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The Unicode glyphs U+2010 (HYPHEN) and U+2011 (NON-BREAKING HYPHEN) are not converted to Punycode when used in domain names, thus allowing spoofing via IDN homograph attacks.

(I notified Mozilla about the same issue.)

**VERSION**  

Chrome Version: 55.0.2883.87 stable  

Operating System: Linux 4.8.12-2-ARCH

**REPRODUCTION CASE**  

This is a bank: <https://www.deutsche-bank.de/>  

This is not a bank: [https://www.deutsche‐bank.de/](https://www.deutsche%E2%80%90bank.de/)

The different hyphen characters are effectively indistinguishable in my browser's URL bar. Instead, the latter domain should be displayed as "xn--deutschebank-n09f.de".

These two characters seem to be the only remaining instances where hyphen-confusables don't end up as Punycode, as I checked against this list: <http://unicode.org/cldr/utility/confusables.jsp?a=-&r=None>

## Timeline

### el...@chromium.org (2016-12-14)

Repros in Chrome 57.2950. Punycode hits the wire, but address bar shows the unencoded character.

[Monorail components: UI>Security>UrlFormatting]

### el...@chromium.org (2016-12-14)

url_formatter.cc seems like the likely home for a fix:
bool IDNSpoofChecker::Check(base::StringPiece16 label)

### mb...@chromium.org (2016-12-15)

[Empty comment from Monorail migration]

### el...@chromium.org (2016-12-15)

jshin@ is fixing this as simple as:

--- a/components/url_formatter/url_formatter.cc
+++ b/components/url_formatter/url_formatter.cc
@@ -469,6 +469,8 @@ void IDNSpoofChecker::SetAllowedUnicodeSet(UErrorCode* status) {
   // should be safe. When used with a non-Hebrew script, it'd be filtered by
   // other checks in place.
   allowed_set.remove(0x338u);   // Combining Long Solidus Overlay
+  allowed_set.remove(0x2010u);  // Hyphen
+  allowed_set.remove(0x2011u);  // Non-breaking hyphen
   allowed_set.remove(0x2027u);  // Hyphenation Point

   uspoof_setAllowedUnicodeSet(checker_, &allowed_set, status);

... or is it more subtle than that?


### sh...@chromium.org (2016-12-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-16)

[Empty comment from Monorail migration]

### sl...@google.com (2016-12-19)

[Empty comment from Monorail migration]

### mg...@chromium.org (2016-12-19)

Since creis is OOO, I will take this. Looks straightforward. #4 should be sufficient.

### mg...@chromium.org (2016-12-19)

[Empty comment from Monorail migration]

### rs...@chromium.org (2016-12-19)

mgiuca: Should we coordinate with Mozilla to make sure we take the same/similar approach (or close to it)? jshin@ tried to sync up and align with FF folks, and to communicate&track where we diverged (as mentioned in https://www.chromium.org/developers/design-documents/idn-in-google-chrome )

armin: Do you have a bug number reference for Mozilla so that we can use that for discussions?

### mg...@chromium.org (2016-12-19)

Hmm, if this needs to block on coordinating with Moz then maybe jshin should do it. He has a lot of experience with confusables and coordinating efforts with Mozilla.

Jungshik you there?

### rs...@chromium.org (2016-12-20)

mgiuca@: I wasn't thinking block so much as having a parallel chat with them to make sure we don't miss anything :) 

### ar...@rawsec.net (2016-12-20)

rsleevi: It's bug #1323338: https://bugzilla.mozilla.org/show_bug.cgi?id=1323338

Approaching Mozilla on this is probably a good idea as they did some additional investigation on the implementation of IDNA2008 which might be relevant here, too.

### mg...@chromium.org (2016-12-21)

CL to fix: https://codereview.chromium.org/2597523004/

Thanks for the suggestion and poking, elawrence@. It turns out we did not need to add U+2011 as that character is automatically normalized to U+2010 (and I added a test for this). So only U+2010 needed to be added to the blacklist.

### mg...@chromium.org (2016-12-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2016-12-21)

Sorry that I'm late here. A fix suggested seems good to me. I'll mark in the CL and add it to CQ. 
 


### js...@chromium.org (2016-12-21)

BTW, thanks a lot for catching this, armin@

### js...@chromium.org (2016-12-21)

To land a CL, I need Peter's owner approval. 

In the meantime, offline, I'll ask armin@ to add my mozilla account to the mozilla bug (https://crbug.com/chromium/673971#c13) so that I can coordinate with them. 

### bu...@chromium.org (2016-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/60f6c0ff8de89ed3a4e4a7c182a0477edfacbfee

commit 60f6c0ff8de89ed3a4e4a7c182a0477edfacbfee
Author: Jungshik Shin <jshin@chromium.org>
Date: Thu Dec 22 00:30:36 2016

url_formatter: Remove U+2010 from the displayable character set.

Fix suggested by elawrence.
CL by mgiucia@ (landed by jshin@ on his behalf).

BUG=673971
TEST=components_unittests --gtest_filter=*IDN*Uni*
R=jshin@chromium.org, pkasting@chromium.org

Review-Url: https://codereview.chromium.org/2597523004 .
Cr-Commit-Position: refs/heads/master@{#440282}

[modify] https://crrev.com/60f6c0ff8de89ed3a4e4a7c182a0477edfacbfee/components/url_formatter/url_formatter.cc
[modify] https://crrev.com/60f6c0ff8de89ed3a4e4a7c182a0477edfacbfee/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2016-12-22)

Requesting Merge to 56. 


### sh...@chromium.org (2016-12-22)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-12-22)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### sh...@chromium.org (2016-12-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-12-29)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-01-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-01-03)

I'm merging it to M56 branch now. Sorry for missing the merge approval on Dec 22. 



### bu...@chromium.org (2017-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ebb863dc1f62c21c578834de595a2ba54a36f1f1

commit ebb863dc1f62c21c578834de595a2ba54a36f1f1
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue Jan 03 21:23:41 2017

url_formatter: Remove U+2010 from the displayable character set.

Fix suggested by elawrence.
CL by mgiucia@ (landed by jshin@ on his behalf).

BUG=673971
TEST=components_unittests --gtest_filter=*IDN*Uni*
R=jshin@chromium.org, pkasting@chromium.org

Review-Url: https://codereview.chromium.org/2597523004 .
Cr-Commit-Position: refs/heads/master@{#440282}
(cherry picked from commit 60f6c0ff8de89ed3a4e4a7c182a0477edfacbfee)

Review-Url: https://codereview.chromium.org/2613603002 .
Cr-Commit-Position: refs/branch-heads/2924@{#654}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/ebb863dc1f62c21c578834de595a2ba54a36f1f1/components/url_formatter/url_formatter.cc
[modify] https://crrev.com/ebb863dc1f62c21c578834de595a2ba54a36f1f1/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2017-01-03)

I came across https://crbug.com/chromium/633922 (git drover issue), but merge seems to have succeeded. 

### mg...@chromium.org (2017-01-05)

Jungshik: Thanks for dealing with landing and merging while I was away!

### js...@chromium.org (2017-01-05)

You're welcome, Matt ! (and thank you for the CL). 

As for Mozilla, they also blocked U+2010 (Thanks, armin@ for copying me to the two mozilla bugs on this). And, one related ICU bug was filed by a DENic folk: 

http://bugs.icu-project.org/trac/ticket/12906



### aw...@chromium.org (2017-01-09)

[Empty comment from Monorail migration]

### aw...@google.com (2017-01-10)

Nice one!  The panel decided to reward $2,000 for this report.

### aw...@chromium.org (2017-01-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-19)

This issue was migrated from crbug.com/chromium/673971?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086207)*
