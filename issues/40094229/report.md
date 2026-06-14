# Isolate chrome.google.com from *.google.com

| Field | Value |
|-------|-------|
| **Issue ID** | [40094229](https://issues.chromium.org/issues/40094229) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Sandbox>SiteIsolation, Webstore |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2019-03-06 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3714.0 Safari/537.36 Edg/74.1.93.0

Steps to reproduce the problem:
1. Go to https://www.google.com/
2. Open console, type `window.open("https://chrome.google.com/robots.txt")` and hit enter
3. Observe that both tabs are committed in the same process

What is the expected behavior?
https://www.google.com/ and https://chrome.google.com/robots.txt aren't committed in the same process.

What went wrong?
https://crbug.com/chromium/937487 solved the privilege API leakage. But side affects of merging *.google.com and chrome.google.com is still there. While I wasn't able to exploit side affects yet, there is no garantee that it'll remain safe in the future.

For example, if Chrome Web Store starts using service worker, attacker can suddenly gain script execution in CWS because cache storage is shared origin-wide (which is same for local storage, etc). Similarly, if attacker could control content of some file, that might allow AppCache registration in the origin. And there are many other possibilities due to the fact that path is hardly a security boundary.

As such, I think we should isolate chrome.google.com from *.google.com.

Did this work before? N/A 

Chrome version: 74.0.3714.0  Channel: canary
OS Version: 10.0
Flash Version:

## Timeline

### al...@chromium.org (2019-03-06)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation]

### cr...@chromium.org (2019-03-06)

Indeed, this might be worth doing, under the assumption that (1) there may be more ways for chrome.google.com content to get an attack into a chrome.google.com/webstore process, and (2) there are hopefully fewer exploitable endpoints on chrome.google.com, relative to all of google.com.

I doubt it would break things on chrome.google.com, assuming nothing there uses document.domain.

lottie@: Do you have a sense for what's hosted on chrome.google.com these days?  Hopefully it's not an issue to isolate them from the rest of google.com (still outside the privileged CWS process), and hopefully there isn't much marketing or third party content there.


### cr...@chromium.org (2019-03-06)

[Empty comment from Monorail migration]

[Monorail components: Webstore]

### oc...@chromium.org (2019-03-07)

creis, assigning this to you for now :) please assign someone else if there's someone more suitable, thanks!

### cr...@chromium.org (2019-03-07)

I'm OOO until Tuesday; maybe Alex can help triage or investigate this while I'm gone?

### sh...@chromium.org (2019-03-07)

[Empty comment from Monorail migration]

### Ju...@microsoft.com (2019-03-09)

This impact stable too.

### wf...@chromium.org (2019-03-09)

[Empty comment from Monorail migration]

### al...@chromium.org (2019-03-12)

lottie@: ping about Charlie's question in https://crbug.com/chromium/939108#c2.  I think we wouldn't mind giving chrome.google.com additional process isolation as a way to further protect the CWS; this would be similar to the isolation we already provide to accounts.google.com.  But we're curious what kind of content (besides the web store) chrome.google.com actually contains today, and how trustworthy that content is, both to evaluate the risk of CWS being compromised by that content vs the rest of google.com, and the potential effect on process count (which I'd expect to be very small, as long as chrome.google.com doesn't have widely visited pages with cross-site iframes).

### lo...@chromium.org (2019-03-12)

I searched the gfe mapping tests and found 8 occurrences (CWS, accounts, Chrome Kids UI etc): https://screenshot.googleplex.com/TVCvsqRP8dM. 

There's also some gws redirects, suggesting the device manage is using the domain (//depot/google3/googledata/gws/redirects/part/chrome.part):
https://chrome.google.com/manage/su

There's Chrome sync data: https://chrome.google.com/sync

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### Ju...@microsoft.com (2019-07-11)

Option 1 explained in https://bugs.chromium.org/p/chromium/issues/detail?id=982326#c29 can also be used in this bug.

All necessary tokens can be accessed by fetching the extension page since it's same-origin.
E.g.
fetch("https://chrome.google.com/webstore/detail/chromevox/kgejglhpjiefppelpmljglcjbhoiplfn").then(r=>r.text()).then(r=>{console.log(r)})

So remotely adding extension (even though it requires user to click allow before installing extension) to user's synced settings is possible using this bug.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/81d2a29e67041bdd078dfc3b1dbe0f83159c1338

commit 81d2a29e67041bdd078dfc3b1dbe0f83159c1338
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Tue Jul 16 01:14:38 2019

Isolate the Chrome Web Store origin from the rest of its site.

This CL adds the Chrome Web Store origin to the list of isolated
origins applied globally at startup.  This puts a process boundary
between content hosted at the CWS origin (usually
https://chrome.google.com) and the rest of the site
(https://*.google.com), to make it less likely that an attack
somewhere on google.com can influence the CWS.  See
https://crbug.com/939108 for discussion/motivation.

Note that navigating to a URL that matches the CWS origin+path (i.e.,
https://chrome.google.com/webstore) already forces a BrowsingInstance
swap (see ChromeContentBrowserClientExtensionsPart::
ShouldSwapBrowsingInstancesForNavigation), but that does not include
non-CWS paths at the same origin (e.g., chrome.google.com/ or
chrome.google.com/foo).  An attacker that has control over google.com
could thus place a chrome.google.com/foo frame in the same process and
then attempt to influence the CWS via origin-wide mechanisms like
ServiceWorker.

Bug: 939108
Change-Id: I42c707986d7ad85b68ca6c32985fc7cd0359d098
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1698999
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#677584}

[modify] https://crrev.com/81d2a29e67041bdd078dfc3b1dbe0f83159c1338/chrome/browser/chrome_content_browser_client.cc
[modify] https://crrev.com/81d2a29e67041bdd078dfc3b1dbe0f83159c1338/chrome/browser/chrome_content_browser_client_browsertest.cc
[modify] https://crrev.com/81d2a29e67041bdd078dfc3b1dbe0f83159c1338/chrome/browser/chrome_navigation_browsertest.cc
[modify] https://crrev.com/81d2a29e67041bdd078dfc3b1dbe0f83159c1338/chrome/browser/extensions/chrome_content_browser_client_extensions_part.cc
[modify] https://crrev.com/81d2a29e67041bdd078dfc3b1dbe0f83159c1338/chrome/browser/extensions/chrome_content_browser_client_extensions_part.h


### al...@chromium.org (2019-07-23)

r677584 is in 77.0.3855.0+, and I've just verified that this is fixed in Mac Canary 77.0.3861.0.

### sh...@chromium.org (2019-07-24)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-24)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-25)

Congrats! The Panel decided to reward $500 for this report!

### sh...@chromium.org (2019-10-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-20)

This issue was migrated from crbug.com/chromium/939108?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Webstore]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094229)*
