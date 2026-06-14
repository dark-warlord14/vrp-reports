# Security: CSP isn't applied to Service Workers in Chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [40083537](https://issues.chromium.org/issues/40083537) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature, Blink>ServiceWorker |
| **CVE IDs** | CVE-2016-1682 |
| **Reporter** | ki...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2016-01-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

CSP checks are not happening for loading service workers

**VERSION**  

Chrome Version: 47.0.2526.106 (64-bit) and 47.0.2526.111 (64-bit) stable  

Operating System: Ubuntu 15.04 - have seen on Windows 8.1 stable + unstable branch also

**REPRODUCTION CASE**

Visit: <https://blazing-fire-305.firebaseapp.com/> (Feel free to request source access)  

Various test URLs exist there with descriptions of the expected outcomes.

Essentially child-src and frame-src don't seem to be preventing loading of the worker in any of the example cases where they should be doing.  

When these directives are not being set and I have a default-src of 'none' I should always see workers blocked.

I am expecting in the console to see CSP errors rather than 'offline worker registered'.  

The same experience has been seen with HTTP header CSP policies.

Loading the code in the latest FireFox the following CSP error is triggered:  

"Content Security Policy: The page's settings blocked the loading of a resource at <https://blazing-fire-305.firebaseapp.com/offline-worker.js> ("default-src 'none'")."

## Timeline

### lg...@chromium.org (2016-01-21)

jww@: I don't know whether to consider this a vulnerability, or whether the spec [1] applies to the worker as well as its fetches.

Could you take this?

[1] https://www.w3.org/TR/CSP2/#processing-model-workers

### jw...@chromium.org (2016-01-21)

I'm pretty sure this is a security bug; the CSP should block the worker (and does in Firefox).

Mike, I can take a look at this, unless you already have a good sense of what's going wrong. Let me know.

### lg...@chromium.org (2016-01-21)

[Empty comment from Monorail migration]

### jw...@chromium.org (2016-01-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-21)

[Empty comment from Monorail migration]

### lg...@chromium.org (2016-01-21)

Setting to M48 based on severity guidelines, but we can revise to M49.

### cl...@chromium.org (2016-02-12)

jww@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ra...@chromium.org (2016-02-18)

jww: Any update on this? Thanks!

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

jww@: Uh oh! This issue is still open and hasn't been updated in the last 48 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### jw...@chromium.org (2016-03-16)

estark, I thought you were looking at Workers and CSP at one point, so I'm assigning to you. If not, let's chat about this at some point.

### cl...@chromium.org (2016-04-06)

estark@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### es...@chromium.org (2016-04-06)

I'll take a look at this today.

### es...@chromium.org (2016-04-06)

+falken for SW expertise

Nothing fancy here -- it looks like the main scripts for SWs are loaded outside the normal Blink resource loading path and CSP checks aren't applied to them. I have a CL with a fix here: https://codereview.chromium.org/1861253004/

falken: it looks like redirects aren't allowed for SWs, so we don't have to worry about applying CSP when following a redirect. (https://code.google.com/p/chromium/codesearch#chromium/src/content/browser/service_worker/service_worker_write_to_cache_job.cc&sq=package:chromium&type=cs&l=230&rcl=1459941399) Is my understanding correct? Also, should that OnReceivedRedirect() implementation be cancelling the request?

### es...@chromium.org (2016-04-06)

[Empty comment from Monorail migration]

### fa...@chromium.org (2016-04-07)

> falken: it looks like redirects aren't allowed for SWs, so we don't have to worry about applying CSP when following a redirect. (https://code.google.com/p/chromium/codesearch#chromium/src/content/browser/service_worker/service_worker_write_to_cache_job.cc&sq=package:chromium&type=cs&l=230&rcl=1459941399) Is my understanding correct?

Yes redirects are not allowed for fetching the SW main script. For reference, the spec decided that here: https://github.com/slightlyoff/ServiceWorker/issues/618 and Firefox also disallows it: https://bugzilla.mozilla.org/show_bug.cgi?id=1131271

I'm not sure if we decided anything for import scripts from the SW though. The current Chrome impl is rejecting them.

> Also, should that OnReceivedRedirect() implementation be cancelling the request?

I'm not sure. The other error cases in that class are just calling NotifyStartError() as well. What is the difference between NotifyStartError() and Kill() (I presume that is what is meant by "cancelling the request"?)

[Monorail components: -Security Blink>ServiceWorker]

### bu...@chromium.org (2016-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5289a5d4c98681e9a0f2d28da0c7aa35e282db57

commit 5289a5d4c98681e9a0f2d28da0c7aa35e282db57
Author: estark <estark@chromium.org>
Date: Thu Apr 07 16:14:40 2016

Check CSP before registering ServiceWorkers

Service Worker registrations should be subject to the same CSP checks as
other workers. The spec doesn't say this explicitly
(https://www.w3.org/TR/CSP2/#directive-child-src-workers says "Worker or
SharedWorker constructors"), but it seems to be in the spirit of things,
and it matches Firefox's behavior.

BUG=579801

Review URL: https://codereview.chromium.org/1861253004

Cr-Commit-Position: refs/heads/master@{#385775}

[add] https://crrev.com/5289a5d4c98681e9a0f2d28da0c7aa35e282db57/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/resources/service-worker.js
[add] https://crrev.com/5289a5d4c98681e9a0f2d28da0c7aa35e282db57/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/service-worker-allowed.html
[add] https://crrev.com/5289a5d4c98681e9a0f2d28da0c7aa35e282db57/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/service-worker-blocked-expected.txt
[add] https://crrev.com/5289a5d4c98681e9a0f2d28da0c7aa35e282db57/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/service-worker-blocked.html
[modify] https://crrev.com/5289a5d4c98681e9a0f2d28da0c7aa35e282db57/third_party/WebKit/Source/modules/serviceworkers/ServiceWorkerContainer.cpp


### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### es...@chromium.org (2016-04-15)

I've verified that the reproduction in the original report works as expected in Canary, so requesting a merge to M50.

### ti...@google.com (2016-04-15)

[Automated comment] Less than 2 weeks to go before stable on M50, manual review required.

### cl...@chromium.org (2016-04-15)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### go...@chromium.org (2016-04-15)

Approving merge to M50 branch 2661 per https://crbug.com/chromium/579801#c19. Please merge ASAP. Thank you.

### bu...@chromium.org (2016-04-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d9f7916c961a0a1511dc8919da76f429e116a7e7

commit d9f7916c961a0a1511dc8919da76f429e116a7e7
Author: Emily Stark <estark@google.com>
Date: Sat Apr 16 00:39:27 2016

Check CSP before registering ServiceWorkers

Service Worker registrations should be subject to the same CSP checks as
other workers. The spec doesn't say this explicitly
(https://www.w3.org/TR/CSP2/#directive-child-src-workers says "Worker or
SharedWorker constructors"), but it seems to be in the spirit of things,
and it matches Firefox's behavior.

BUG=579801

Review URL: https://codereview.chromium.org/1861253004

Cr-Commit-Position: refs/heads/master@{#385775}
(cherry picked from commit 5289a5d4c98681e9a0f2d28da0c7aa35e282db57)

Review URL: https://codereview.chromium.org/1898483002 .

Cr-Commit-Position: refs/branch-heads/2661@{#593}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[add] https://crrev.com/d9f7916c961a0a1511dc8919da76f429e116a7e7/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/resources/service-worker.js
[add] https://crrev.com/d9f7916c961a0a1511dc8919da76f429e116a7e7/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/service-worker-allowed.html
[add] https://crrev.com/d9f7916c961a0a1511dc8919da76f429e116a7e7/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/service-worker-blocked-expected.txt
[add] https://crrev.com/d9f7916c961a0a1511dc8919da76f429e116a7e7/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/service-worker-blocked.html
[modify] https://crrev.com/d9f7916c961a0a1511dc8919da76f429e116a7e7/third_party/WebKit/Source/modules/serviceworkers/ServiceWorkerContainer.cpp


### cl...@chromium.org (2016-04-16)

[Empty comment from Monorail migration]

### es...@chromium.org (2016-04-16)

I tried to cherry-pick this back to M50, but it didn't apply cleanly and I messed it up and broke the build and reverted the cherry-pick. :( Since it's medium severity and M50 is going to stable soon, I'm now thinking it might be better to just let this roll out with M51.

### ti...@google.com (2016-05-24)

Thanks for your report! As we're getting closer to M51, we'll consider this report under our Chrome Security Rewards Program - full details here: https://www.google.com/about/appsecurity/chrome-rewards/

I'll update this issue once I have a decision from the reward panel.

### ki...@gmail.com (2016-05-25)

Regarding the comment on service workers not in the spec it is in the latest:
https://w3c.github.io/webappsec-csp/#directive-child-src

It should probably be added to 7.2.2 of http://w3c.github.io/webappsec-csp/2/ though so added that to an open bug on the spec :).

### ti...@google.com (2016-05-25)

Congratulations - Our reward panel decided to award $1,000 for this report.

The CVE-ID for this issue is CVE-2016-1682. You're credited in our release notes at http://googlechromereleases.blogspot.com/2016/05/stable-channel-update_25.html as "kingstonmailbox". If you would like to use a different name for credit, please let me know and I can update the release notes.

Someone from our finance team should be in touch within 7 days to collect payment details. If that doesn't happen, please either update this bug or reach out to me at timwillis@.

Thanks again for your report!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

### ki...@gmail.com (2016-05-25)

My IRC and twitter handle(KingstonTime) is probably better as I don't really use this email. Thanks for fixing this!

### ti...@google.com (2016-05-25)

No worries - updated: http://googlechromereleases.blogspot.com/2016/05/stable-channel-update_25.html

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

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

### aw...@google.com (2018-06-08)

The reward for this report is being donated to the Against Malaria Foundation :-)

### is...@google.com (2018-06-08)

This issue was migrated from crbug.com/chromium/579801?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature, Blink>ServiceWorker]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083537)*
