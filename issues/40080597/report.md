# Security: Completely spoofable origin, including lock sign

| Field | Value |
|-------|-------|
| **Issue ID** | [40080597](https://issues.chromium.org/issues/40080597) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox, UI>Internationalization |
| **Platforms** | Android, Linux, Mac |
| **Reporter** | zc...@gmail.com |
| **Assignee** | mg...@chromium.org |
| **Created** | 2014-10-08 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**  

<http://example.org/>

## Attachments

- [lockicon.png](attachments/lockicon.png) (image/png, 41.5 KB)
- [Screen Shot 2014-10-10 at 10.25.11 AM.png](attachments/Screen Shot 2014-10-10 at 10.25.11 AM.png) (image/png, 7.0 KB)
- [Screen Shot 2014-10-10 at 10.24.42 AM.png](attachments/Screen Shot 2014-10-10 at 10.24.42 AM.png) (image/png, 40.3 KB)
- [Screen Shot 2014-10-10 at 4.01.26 PM.png](attachments/Screen Shot 2014-10-10 at 4.01.26 PM.png) (image/png, 22.8 KB)
- [Screen Shot 2014-10-10 at 3.59.55 PM.png](attachments/Screen Shot 2014-10-10 at 3.59.55 PM.png) (image/png, 13.7 KB)
- [Screen Shot 2014-10-10 at 4.09.14 PM.png](attachments/Screen Shot 2014-10-10 at 4.09.14 PM.png) (image/png, 22.5 KB)
- [windows_phish.png](attachments/windows_phish.png) (image/png, 32.2 KB)
- [Screen Shot 2014-10-29 at 10.48.16 AM.png](attachments/Screen Shot 2014-10-29 at 10.48.16 AM.png) (image/png, 17.8 KB)

## Timeline

### mb...@chromium.org (2014-10-08)

This looks like a duplicate of https://crbug.com/chromium/101772, but it's been a while since this has been considered. I won't mark this as a duplicate yet in case anyone else wants to comment on this.

### zc...@gmail.com (2014-10-08)

I could reproduce this on Android also, fwiw.

### me...@chromium.org (2014-10-08)

It's indeed very similar to https://crbug.com/chromium/101772 but this one seems more convincing since it's not using the title bar or a data url.

For what it's worth IE doesn't render the lock character (Firefox does) or any other unicode characters. I'm not sure if this can be fixed in Chrome without changing the whole url handling mechanism.

### mb...@chromium.org (2014-10-08)

[Empty comment from Monorail migration]

### me...@chromium.org (2014-10-08)

Marty: It doesn't work on Windows :) Fixing OS labels.

### mb...@chromium.org (2014-10-08)

Good catch. Thanks.

### fe...@chromium.org (2014-10-09)

I agree with meacer in #3, this is much more convincing.

### fe...@chromium.org (2014-10-09)

cc palmer@, commander of knowing thy origin

### pa...@chromium.org (2014-10-09)

I suspect the problem may be worse. On Twitter you can find lots of trickery in people's names, and in tweets, for example. (Can't find any good examples now, of coruse.)

I bet that by expanding on the weirdness described e.g. here http://marijnhaverbeke.nl/blog/cursor-in-bidi-text.html and elsewhere that an attacker could get the lock to appear over the "blank page" favicon, or at least at the beginning of the URL string, that we show on HTTP page-loads.

It might be that we filter out all the cursor movement/weird horizontal space/bidi-confusing unicode code points. But I'm not sure.

Would it help to use Punycode for parts of the URL other than the hostname...? If they trigger certain blacklisted (or, not whitelisted) code points like the lock...?

### zc...@gmail.com (2014-10-09)

You're right about RTL tricks. Paste the following into the address bar: اexample.org/

### zc...@gmail.com (2014-10-10)

Hmm, the Arabic gets punycoded when pressing Enter. But using an IP as the host makes RTL work: http://127.0.0.1/اexample.org/

### zc...@gmail.com (2014-10-10)

More elaborate example:

http://127.0.0.1/اhttps://

### fe...@chromium.org (2014-10-10)

Re #10 and #12: neither of these yield working spoofs for me. Can you screenshot what you're seeing for me? Thanks.

### me...@chromium.org (2014-10-10)

I can reproduce #12 on Linux. @felt, try this URL:

http://127.0.0.1/%D8%A7%F0%9F%94%92https://%F0%9D%90%AC%F0%9D%90%9E%F0%9D%90%9C%F0%9D%90%AE%F0%9D%90%AB%F0%9D%90%9E.%F0%9D%90%9B%F0%9D%90%9A%F0%9D%90%A7%F0%9D%90%A4%F0%9D%90%A8%F0%9D%90%9F%F0%9D%90%9A%F0%9D%90%A6%F0%9D%90%9E%F0%9D%90%AB%F0%9D%90%A2%F0%9D%90%9C%F0%9D%90%9A.%F0%9D%90%9C%F0%9D%90%A8%F0%9D%90%A6/login/enroll/entry/olbEnroll.go?.jpg

This is https://crbug.com/chromium/351639 + the lock icon I think.

### fe...@chromium.org (2014-10-10)

Oof. Yeah that is a really good spoof. The reason it wasn't working for me is because I have Omnitheatre turned on.

### fe...@chromium.org (2014-10-10)

The bold part looks better on mac but the lock doesn't show on the left.

### pa...@google.com (2014-10-10)

Here's what I see with #10 and #12 on Mac. Nice work! Very enjoyable, would get spoofed again, A+.

According to http://dev.chromium.org/developers/severity-guidelines this is Security_Severity-High.

### pa...@google.com (2014-10-10)

Hmm, my screenshots are from Chrome 37 on Mac, BTW. On Canary (M40), the spoof is the same.

### me...@chromium.org (2014-10-13)

By the way the lock doesn't show on Windows, but the rest of the spoof still works.  I think the non-lock part is related to https://crbug.com/chromium/351639 though.

Attached screenshot has an arrow icon, but there are other characters that can be more convincing.

### md...@chromium.org (2014-10-14)

[Assigning to felt@ for security sheriff triage.]

### pa...@chromium.org (2014-10-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-10-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-22)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-29)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### gr...@chromium.org (2014-10-29)

FWIW, this seems somewhat fixed in latest OSX Canary. (See screenshot)

Naive question: Would it make sense to apply IDNA2008 codepoints (http://tools.ietf.org/html/rfc5892) simply to the entire URL? 

Naive question 2: Would it make more sense to enforce protocol/domain/path as completely separate UI fields?

### fe...@chromium.org (2014-10-31)

Re #25: The lock is in the right place, but the origin is still "secure.bankofamerica.com" instead of 127.0.0.1. :(

### fe...@chromium.org (2014-10-31)

[Empty comment from Monorail migration]

### fe...@chromium.org (2014-10-31)

[Empty comment from Monorail migration]

### fe...@chromium.org (2014-10-31)

groby@: It does seem to make sense to me to enforce protocol/domain/path as completely separate fields, that are placed next to each other in the correct order; so perhaps you could forcibly flip one of them internally, but not change the ordering of the fields.

### ta...@opera.com (2014-10-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-07)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### me...@chromium.org (2014-11-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-15)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-22)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-29)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-07)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-08)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### pa...@chromium.org (2014-12-11)

I don't think felt was the right person to assign this to. Trying the chrome/browser/ui/omnibox/OWNERS.

### me...@chromium.org (2014-12-11)

Also see tarquinwj@'s comment from https://crbug.com/chromium/351639 (https://code.google.com/p/chromium/issues/detail?id=351639#c52). It looks like this bug should be duped into that one.

### pk...@chromium.org (2014-12-11)

Yes, the dupe was the wrong way.

Please update the security flags on that bug as necessary, as this bug is "high" and that is "low".

### me...@chromium.org (2014-12-12)

Adding label reward-topanel since this report prompted us to increase the severity of the original bug by providing interesting spoofing cases.

### cl...@chromium.org (2014-12-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-01)

Bulk update: removing view restriction from closed bugs.

### mg...@chromium.org (2015-06-02)

+Restrict-View-SecurityTeam (this is not fixed). (I have notified security team about #44.)

I would prefer *not* to have this as a dupe, as it is a more specialized case of that bug. (https://crbug.com/chromium/351639 is about general confusion about Arabic/Hebrew domains; it doesn't specifically mention this bug which involves spoofing an ASCII domain and is more serious.)

That other bug has been made public. I'd prefer to keep this bug private for now. The tentative fix I have for https://crbug.com/chromium/351639 also solves this.

(Also, it is not immediately obvious how to trigger this... I was trying to do this earlier with a Hebrew domain and Chrome caught me. The IP address, however, is successful.)

### cl...@chromium.org (2015-06-02)

[Empty comment from Monorail migration]

### mg...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### mg...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### mg...@chromium.org (2015-06-03)

I think this issue has split into two separate issues: a) the padlock icon and b) the RTL hack. I've filed separate sub-bugs so they can be individually tracked:

- https://crbug.com/chromium/495933 (the RTL hack), and
- https://crbug.com/chromium/495934 (the padlock icon).

### mb...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### mg...@chromium.org (2015-06-09)

First one is fixed:

commit 23285d3e9142d14bb162cd808692deacc5440330
Author: mgiuca <mgiuca@chromium.org>
Date: Tue Jun 09 06:31:41 2015

Added characters that look like padlocks to net IDN character blacklist.

This adds the following Unicode characters to the blacklist:
- U+1F50F LOCK WITH INK PEN
- U+1F510 CLOSED LOCK WITH KEY
- U+1F512 LOCK
- U+1F513 OPEN LOCK

This prevents LOCK characters from appearing in an internationalized
domain names, potentially looking like an SSL padlock icon (e.g.,
"

### bu...@chromium.org (2015-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1c7d9ce02925cf766fc508d4ee83424369e71548

commit 1c7d9ce02925cf766fc508d4ee83424369e71548
Author: mgiuca <mgiuca@chromium.org>
Date: Tue Jun 16 02:53:10 2015

Omnibox: Force text field to LTR context if it is a URL.

This means that URLs will be displayed in a left-to-right paragraph
context. Right-to-left runs are still rendered RTL, but will not flip
the whole URL around. For example (if "ABC" is Hebrew), this will render
"ABC.com" as "CBA.com", rather than "com.CBA".

This is consistent with the behaviour in the Omnibox drop-down items
(OmniboxResultView::CreateClassifiedRenderText) and status bubble
(StatusBubbleViews::SetURL).

BUG=495933,421332

Review URL: https://codereview.chromium.org/1189553002

Cr-Commit-Position: refs/heads/master@{#334537}

[modify] http://crrev.com/1c7d9ce02925cf766fc508d4ee83424369e71548/chrome/browser/ui/views/omnibox/omnibox_view_views.cc


### bu...@chromium.org (2015-06-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7c2cbc445a81424c7df48ebe61ec4d0dcadd5dff

commit 7c2cbc445a81424c7df48ebe61ec4d0dcadd5dff
Author: mgiuca <mgiuca@chromium.org>
Date: Wed Jun 24 03:59:47 2015

Added characters that look like padlocks to URL unescaping blacklist.

This blacklists the following Unicode characters:
- U+1F50F LOCK WITH INK PEN
- U+1F510 CLOSED LOCK WITH KEY
- U+1F512 LOCK
- U+1F513 OPEN LOCK

This prevents LOCK characters from appearing in a URL in the Chrome UI,
potentially looking like an SSL padlock icon (e.g., "google.com/

### in...@chromium.org (2015-07-01)

Are all the patches in. If yes, please mark bug as Fixed.

### mg...@chromium.org (2015-07-03)

All the patches are in, but I'm still concerned that the final one isn't going to stick in M45. (See discussion on https://codereview.chromium.org/1189553002).

Basically, this is causing the Omnibox to flicker back and forth between LTR and RTL modes as the suggestion changes between URL and Google Search. We might need to revert it until that issue is fixed.

https://crbug.com/chromium/421514 has a potential fix for this, but it's currently behind a field trial.

### mg...@chromium.org (2015-07-03)

[Empty comment from Monorail migration]

### pk...@chromium.org (2015-07-03)

Did you test to see if, when enabled properly, the field trial does address this?

### mg...@chromium.org (2015-07-06)

#57: It seems more stable with that field trial enabled, but it still has a tendency to flip between URL and Google Search as you're typing.

I'll write more comments on https://crbug.com/chromium/421514.

### mg...@chromium.org (2015-07-06)

Another thing I've just noticed through testing is that if you are using a standard TLD, it stays on the URL result nicely (both with and without the field trial). The flipping issue is only a problem if using a non-standard TLD.

Since non-standard TLDs are not yet very common (even in RTL languages) I think it should be OK to keep this fix in there. It *is* a serious security issue despite having been around for a long time.

### cl...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### mg...@chromium.org (2015-07-13)

OK, the fixes have stuck. I'm considering this one fixed. Thanks very much to zcorpan who reported these two issues.

### cl...@chromium.org (2015-07-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-07-31)

Looks risky for M44, will let roll in m45.

### ti...@google.com (2015-08-31)

Congratulations - Our reward panel decided to award you $1,000 for this report. 

We'll credit you in the Chrome release notes as "zcorpan". Please let me know if you'd like to use a different name.

Our finance team shall be in contact to collect payment details sometime this week. Please contact me at timwillis@ with any questions or update this bug.


*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### mg...@chromium.org (2015-08-31)

Congratulations, zcorpan! Thanks again for your help making Chrome more secure.

### ti...@google.com (2015-09-04)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-23)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-10-19)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/421332?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Omnibox, UI>Internationalization]
[Monorail blocked-on: crbug.com/chromium/495933, crbug.com/chromium/495934]
[Monorail blocking: crbug.com/chromium/351639]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080597)*
