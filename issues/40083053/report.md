# Privacy: browser history sniffing attack using HSTS + CSP

| Field | Value |
|-------|-------|
| **Issue ID** | [40083053](https://issues.chromium.org/issues/40083053) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>SSL, Privacy, UI>Browser>History |
| **CVE IDs** | CVE-2016-1617 |
| **Reporter** | je...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2015-10-19 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**  

I wrote a PoC for reliably sniffing browser history in Chrome/Firefox by observing which domains have associated HSTS entries. I showed it to Chris Palmer, who suggested I file it here :). The code is pretty well-commented but basically it works like this:

1. User visits attacker page
2. Browser attempts to load images from various HSTS domains over HTTP
3. Attacker has set a CSP policy that restricts images to HTTP, so image sources are blocked before they are redirected to HTTPS. This is crucial; if the browser completes a request to the HTTPS site, then it will receive the HSTS pin, and the attack will no longer work when the user visits the page again.
4. When an image gets blocked by CSP, its onerror handler is called. In this case, the onerror handler does some tricks to time how long it took for the image to be redirected from HTTP to HTTPS. If this time is on the order of a millisecond, it was an HSTS redirect (no network request was made), which means the user has visited the image's domain before. If it's on the order of 100 milliseconds, then a network request probably occurred, meaning that the user hasn't visited the image's domain.

This also works in incognito mode (can see which hosts the user has visited in their non-incognito session) and chrome on android. I haven't tried other platforms.

Please note this will be shown as part of a demo of new browser fingerprinting methods at Toorcon next Sunday (10/25).

**VERSION**  

Chrome Version: 46.0.2490.71 stable  

Operating System: OSX 10.10.4

**REPRODUCTION CASE**  

Live demo at <http://zyan.scripts.mit.edu/sniffly/>. Source files also attached. (Please don't share the link.)

## Attachments

- [index.html](attachments/index.html) (text/html, 1.2 KB)
- [index.js](attachments/index.js) (text/javascript, 14.2 KB)
- [index.html](attachments/index.html) (text/html, 1.3 KB)
- [index.js](attachments/index.js) (text/javascript, 2.8 KB)

## Timeline

### pa...@chromium.org (2015-10-19)

See also:
https://code.google.com/p/chromium/issues/detail?id=311296
https://code.google.com/p/chromium/issues/detail?id=258667


### pa...@chromium.org (2015-10-19)

(Taking ownership only to make sure somebody does. Feel free to take it if the spirit moves you.)

### pa...@chromium.org (2015-10-19)

(Taking ownership only to make sure somebody does. Feel free to take it if the spirit moves you.)

### oc...@chromium.org (2015-10-19)

Assuming this impacts stable.

### oc...@chromium.org (2015-10-19)

[Empty comment from Monorail migration]

### lg...@chromium.org (2015-10-19)

Note that the HSTS portion of this is https://crbug.com/chromium/436451, which is currently WontFix: https://crbug.com/436451#c34

### cl...@chromium.org (2015-10-19)

[Empty comment from Monorail migration]

### je...@gmail.com (2015-10-21)

Thank you for the prompt replies. FWIW, I found this type of timing attack also works using plain ol' 301 redirect caches instead of HSTS. Assuming 301's are cached based on full URL (not just origin), this can be potentially used to reveal full URLs in browsing history by guess-and-check.

To repro:
1. Open an incognito tab in chrome
2. Load some URLs that 301 to HTTPS, such as http://americanexpress.com/ and http://surveymonkey.com/
3. Load the attached index.html and index.js

This attack will populate the cache, so it won't work again if you reload index.html.

-yan

### pa...@chromium.org (2015-10-21)

[Empty comment from Monorail migration]

### ke...@chromium.org (2015-10-22)

[Empty comment from Monorail migration]

### en...@chromium.org (2015-10-27)

[Empty comment from Monorail migration]

### pa...@chromium.org (2015-11-12)

I verified that the 301 redirect version, #8, also works.

I am not sure how solvable this problem is, without also breaking something else.

Here is 1 idea, and I have no idea how good or bad of an idea it is: The attack seems to rely on the ability to set a CSP policy like "img-src: http://*" (presumably all of the *-src CSP directives could be used, in the same way). It seems odd to me that CSP enables affirmatively unsafe behavior, so I wonder if we could disallow or deprecate using *-src to set non-secure origins as sources? If browsers did not honor such policies, would that mitigate or solve this history leak problem?

Would it be acceptable, if it did work?

I am no CSP expert, so I leave it to people who are.

I suspect trying to obscure cache timing is unlikely to work at all, or well enough. That's why I am thinking CSP-related approaches.

### pa...@chromium.org (2015-11-12)

[Empty comment from Monorail migration]

### mk...@chromium.org (2015-11-19)

Sorry, I made the change to the CSP spec, but neglected to fix the implementation. Doing that this morning.

### mk...@chromium.org (2015-11-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-11-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/568075bbc5d16239a5cbdeb579a8768f9836f13e

commit 568075bbc5d16239a5cbdeb579a8768f9836f13e
Author: mkwst <mkwst@chromium.org>
Date: Thu Nov 19 11:54:24 2015

CSP: Source expressions can no longer lock sites into insecurity.

CSP's matching algorithm has been updated to make clever folks like Yan
slightly less able to gather data on user's behavior based on CSP
reports[1]. This matches Firefox's existing behavior (they apparently
changed this behavior a few months ago, via a happy accident[2]), and
mitigates the CSP-variant of Sniffly[3].

On the dashboard at https://www.chromestatus.com/feature/6653486812889088.

[1]: https://github.com/w3c/webappsec-csp/commit/0e81d81b64c42ca3c81c048161162b9697ff7b60
[2]: https://bugzilla.mozilla.org/show_bug.cgi?id=1218524#c2
[3]: https://bugzilla.mozilla.org/show_bug.cgi?id=1218778#c7

BUG=544765,558232

Review URL: https://codereview.chromium.org/1455973003

Cr-Commit-Position: refs/heads/master@{#360562}

[modify] http://crrev.com/568075bbc5d16239a5cbdeb579a8768f9836f13e/third_party/WebKit/Source/core/frame/csp/CSPSource.cpp
[modify] http://crrev.com/568075bbc5d16239a5cbdeb579a8768f9836f13e/third_party/WebKit/Source/core/frame/csp/CSPSourceListTest.cpp
[modify] http://crrev.com/568075bbc5d16239a5cbdeb579a8768f9836f13e/third_party/WebKit/Source/core/frame/csp/CSPSourceTest.cpp


### cl...@chromium.org (2015-12-10)

mkwst@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-01)

mkwst@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### mk...@chromium.org (2016-01-01)

This is mitigated via r360562 above, which adopted the behavior Firefox is running with (`img-src http:` === `img-src http: https:`). This won't fix variants of the attack that rely on cache timing, but it removes the trivial DOM event that the PoC relied on for 100% accuracy.

### cl...@chromium.org (2016-01-01)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2016-01-08)

Merge Requested for M48 - branch 2564

### ti...@google.com (2016-01-08)

Your change meets the bar and is auto-approved for M48 (branch: 2564)

### ti...@google.com (2016-01-11)

@mkwst: Can you please land this today? Last M48 beta candidate cuts 12 Jan @ 5pm MTV time.

### bu...@chromium.org (2016-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ab830edb26a1f56f660b06459d70e1d48a707975

commit ab830edb26a1f56f660b06459d70e1d48a707975
Author: Mike West <mkwst@google.com>
Date: Tue Jan 12 08:56:39 2016

CSP: Source expressions can no longer lock sites into insecurity.

CSP's matching algorithm has been updated to make clever folks like Yan
slightly less able to gather data on user's behavior based on CSP
reports[1]. This matches Firefox's existing behavior (they apparently
changed this behavior a few months ago, via a happy accident[2]), and
mitigates the CSP-variant of Sniffly[3].

On the dashboard at https://www.chromestatus.com/feature/6653486812889088.

[1]: https://github.com/w3c/webappsec-csp/commit/0e81d81b64c42ca3c81c048161162b9697ff7b60
[2]: https://bugzilla.mozilla.org/show_bug.cgi?id=1218524#c2
[3]: https://bugzilla.mozilla.org/show_bug.cgi?id=1218778#c7

BUG=544765,558232

Review URL: https://codereview.chromium.org/1455973003

Cr-Commit-Position: refs/heads/master@{#360562}
(cherry picked from commit 568075bbc5d16239a5cbdeb579a8768f9836f13e)

Review URL: https://codereview.chromium.org/1581573002 .

Cr-Commit-Position: refs/branch-heads/2564@{#538}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[modify] http://crrev.com/ab830edb26a1f56f660b06459d70e1d48a707975/third_party/WebKit/Source/core/frame/csp/CSPSource.cpp
[modify] http://crrev.com/ab830edb26a1f56f660b06459d70e1d48a707975/third_party/WebKit/Source/core/frame/csp/CSPSourceListTest.cpp
[modify] http://crrev.com/ab830edb26a1f56f660b06459d70e1d48a707975/third_party/WebKit/Source/core/frame/csp/CSPSourceTest.cpp


### bu...@chromium.org (2016-01-14)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/ab830edb26a1f56f660b06459d70e1d48a707975

commit ab830edb26a1f56f660b06459d70e1d48a707975
Author: Mike West <mkwst@google.com>
Date: Tue Jan 12 08:56:39 2016


### ti...@google.com (2016-01-19)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

Hi jenuis - our reward panel reviewed this issue and decided to award you $500 for bringing this issue to our attention (even if you only gave us a week to fix it!). Although you probably already know this, bugs that are made public before we have a chance to fix them aren't usually eligible for a reward, but the panel decided to give you a one-off $500 reward anyway.

We'll list your name in the Chrome release notes as "jenuis". If you'd like me to update it to another name, please let me know.

Someone from our finance team should be in contact within 7 days to collect some details for payment. If that doesn't happen, please either update the bug or contact me at timwillis@

I'll update this bug shortly with a CVE ID for your records. Thanks again for helping secure chrome and happy bug hunting!

### ti...@google.com (2016-01-20)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

CVE-2016-1617

### je...@gmail.com (2016-01-20)

 timwil...@google.com, please list my name as "Yan Zhu" in the release notes. Thanks!

### ti...@google.com (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-08)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/544765?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network>SSL, Privacy, Security, UI>Browser>History]
[Monorail blocked-on: crbug.com/chromium/558232]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083053)*
