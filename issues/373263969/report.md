# Ensure not reusing ScriptResource via Blink MemoryCache across worlds

| Field | Value |
|-------|-------|
| **Issue ID** | [373263969](https://issues.chromium.org/issues/373263969) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Blink>Loader, Blink>Workers |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | jl...@chromium.org |
| **Assignee** | yy...@chromium.org |
| **Created** | 2024-10-14 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Copy payload from <https://issues.chromium.org/issues/371011220>
2. Replace content.js
3. Start server via index.py

# Problem Description

Hello, this ticket is a continuation of the issue: <https://issues.chromium.org/issues/371011220>.

Unlike Firefox and Safari, Chrome allows the insertion of the Link header on subresource requests. In this case, there is no check that ensures the Link is processed from the Isolated World, and it passes through the service worker.

This also affects all other Link headers, such as preload and prefetch.

# Summary

Chrome Extension Isolation bypass

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A

## Attachments

- [content.js](attachments/content.js) (text/javascript, 396 B)
- [index.py](attachments/index.py) (text/x-python, 659 B)

## Timeline

### se...@gmail.com (2024-10-14)

That is, any request containing Link headers will be redirected to the service worker. From there, the service worker can return a response that also includes a Link header pointing to chrome-extension://.

Perhaps this issue can be resolved by either removing the loading of the Link header for subresources or adding additional checks, similar to the solution for the previous issue.

(The example I provided is somewhat unrealistic and is simply intended to help understand this issue in relation to the previous one.)

### es...@chromium.org (2024-10-15)

I can't reproduce this on Canary or Stable. The webpage just shows "slonser text". The only chrome-extension:// request I see is to chrome-extension://invalid -- is that supposed to be the case?

### se...@gmail.com (2024-10-15)

Hi! Reproduced just now on Stable and Dev, If you see `chrome-extension://invalid`, maybe you need to change `chrome-extension://hoikbdahecchfemppcfiipbbenhnpnhp` (index.py) by your extension origin.

### pe...@google.com (2024-10-15)

Thank you for providing more feedback. Adding the requester to the CC list.

### es...@chromium.org (2024-10-15)

Ah yes, now it works, thanks! Extensions folks, PTAL.

### pe...@google.com (2024-10-15)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-10-15)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### yy...@chromium.org (2024-10-17)

Ah the access is permitted upon web accessible resource point of view because the manifest says:
    "web_accessible_resources": [ {
        "matches": [ "http://*/*", "https://*/*" ],
        "resources": [ "assets/example.js" ],
        "use_dynamic_url": false
     } ]


### jl...@chromium.org (2024-10-22)

Thank you for reporting this sevakokorin80!

I've confirmed that rel="modulepreload" is what allows this (preload and prefetch don't seem to).

To illustrate what is happening here I'll describe the steps (sevakokorin80@ let me know if this agrees with your understanding):

1. going to localhost:5000 causes the browser to load the page (index.html) and install the service worker
2. We inject the extension content script (content.js) at document end (when the page has finished loading)
3. content.js fetches localhost:5000/abobus and waits for the response
4. the web server (index.py) sees the request and responds with an additional header of:
   `Link: <chrome-extension://<id>/example.js>;rel="modulepreload";`
5. content.js then attempts to dynamically import chrome-extension://<id>/example.js
6. content.js is served the (previously changed and cached) contents of example.js from cache
7. content.js executes the changed contents of example.js (rather than the original content of example.js located at chrome-extension://<id>/example.js).

So this is very similar to the previous bug, but the Link header insertion causes the browser to GET chrome-extension://<id>/example.js, but since this is from the main world the web server worker is allowed to intercept this fetch (this part is fine). But when our content.js goes to dynamically import example.js it gets the cached version, not the on-disk version.

This happens because the Link header causes the browser to insert the (changed example.js) into the document's module map
(specifically we cache the resource [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc;l=1386;drc=08efa89c7d73d72e6ebcddbf053c41a230dc1ba8)) and when we handle the dynamic import we serve the Link cached version (due to [this](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc;l=1417-1419;drc=08efa89c7d73d72e6ebcddbf053c41a230dc1ba8)) rather than the on-disk version.

It's doesn't seem to be a trivial quick fix because bypassing the [cached response](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc;l=1417-1419;drc=08efa89c7d73d72e6ebcddbf053c41a230dc1ba8) causes a [(D)CHECK](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc;l=1736-1738;drc=08efa89c7d73d72e6ebcddbf053c41a230dc1ba8) to be hit where we don't want to [create a new Resource](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc;l=1446;drc=08efa89c7d73d72e6ebcddbf053c41a230dc1ba8) if there is one already in the MemoryCache

### se...@gmail.com (2024-10-23)

Hello, yes, you understood the problem correctly. I agree that solving this issue could be challenging.
I think that the behavior where fetch loads a Link is generally strange.
In my opinion, a subresource request should not trigger the loading of Link headers.
From my observations, this doesn't happen in other browsers (Firefox, Safari).
I haven't been able to find a part of the web standards that describes this behavior, but it seems that it has almost no examples of usage by real websites.

### se...@gmail.com (2024-10-23)

Oh, I found that this behaviour just not specified in web standards yet.
<https://github.com/whatwg/html/issues/8865>

### se...@gmail.com (2024-10-25)

Perhaps it's worth considering disabling modulepraload interception with service-worker? It seems that this will protect against future problems.

### ap...@google.com (2024-10-31)

Project: chromium/src  

Branch: main  

Author: Yoshisato Yanagisawa <[yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5961018>

Make GetCacheIdentifier() respect GetSkipServiceWorker().

---


Expand for full commit details
```
Make GetCacheIdentifier() respect GetSkipServiceWorker(). 
 
Since the current GetCacheIdentifier() ignores GetSkipServiceWorker(), 
GetCacheIdentifier() returns ServiceWorkerId even if GetSkipServiceWorker() 
is true if the ServiceWorker has a fetch handler. 
 
To make the isolated world respected as an isolated world, the cache 
identifier should not be shared with a page under a ServiceWorker control. 
 
Bug: 372512079, 373263969 
Change-Id: Idd2d8900f2f720e0a4dc9837e2eb56474c60b587 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5961018 
Reviewed-by: Justin Lulejian <jlulejian@chromium.org> 
Reviewed-by: Kouhei Ueno <kouhei@chromium.org> 
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1376006}

```

---

Files:

- M `third_party/blink/renderer/core/html/parser/html_srcset_parser.cc`
- M `third_party/blink/renderer/core/inspector/inspector_network_agent.cc`
- M `third_party/blink/renderer/core/inspector/inspector_page_agent.cc`
- M `third_party/blink/renderer/core/loader/image_loader.cc`
- M `third_party/blink/renderer/core/testing/internals.cc`
- M `third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc`
- M `third_party/blink/renderer/platform/loader/fetch/resource_fetcher.h`

---

Hash: 75f322ad1f64c0bc56fa77ab877b48d72cdb903c  

Date:  Thu Oct 31 01:01:31 2024


---

### jl...@chromium.org (2024-10-31)

Hi sevakokorin80@,

Could you see if 132.0.6809.0 (currently in canary) prevents this Link headers bypass for you? The above fix ensures we're checking for the skipping of SW fetch for isolated worlds when caching (script) resources.

### se...@gmail.com (2024-11-01)

Hi, 132.0.6809.0 prevents bypass for me.

### pe...@google.com (2024-11-05)

Security Merge Request Consideration: Requesting merge to stable (M130) because latest trunk commit (1376006) appears to be after stable branch point (1356013).
Security Merge Request Consideration: Requesting merge to beta (M131) because latest trunk commit (1376006) appears to be after beta branch point (1368529).
Security Merge Request - Manual Review: Merge review required: M130 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M131 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [130, 131].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dc...@chromium.org (2024-11-05)

From the secondary security shepherd: is this considered a dupe of [issue 372512079](https://issues.chromium.org/issues/372512079) or [issue 371011220](https://issues.chromium.org/issues/371011220)?

### yy...@google.com (2024-11-05)

I understand that this issue and issue 372512079 are the same root cause, but I believe it is natural to give a credit to sevakokorin80@gmail.com.
issue 372512079  has been filed upon crbug.com/371011220#comment23.
Attack code mentioned in crbug.com/372512079#comment8 is based on attack code written in #comment1.
Therefore, I should say that without this issue and crbug.com/371011220#comment23, issue 372512079 has not been resolved.


### am...@chromium.org (2024-11-06)

This fix has been on Canary for > 1 week and not seeing any issues in Canary data to prevent merging;
M131 merge approved for <https://crrev.com/c/5961018>
Please merge this fix to branch 6778 at your convenience.
M131 Stable RC for release on Tuesday has already been cut, so once this is merged it would be included in a Stable respin of M131.

Please do not merge to M130 Extended Stable at this time; M130 Extended RC has not yet been cut, so this should not be merged to M130 until at the time or after it has been including in an M131 Stable release. Thank you.

### am...@chromium.org (2024-11-06)

I've re-added the M130 merge review tag to ensure I have revisited this issue to approve for M130.

### ap...@google.com (2024-11-07)

Project: chromium/src  

Branch: refs/branch-heads/6778  

Author: Yoshisato Yanagisawa <[yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6002191>

[M131] Make GetCacheIdentifier() respect GetSkipServiceWorker().

---


Expand for full commit details
```
[M131] Make GetCacheIdentifier() respect GetSkipServiceWorker(). 
 
Since the current GetCacheIdentifier() ignores GetSkipServiceWorker(), 
GetCacheIdentifier() returns ServiceWorkerId even if GetSkipServiceWorker() 
is true if the ServiceWorker has a fetch handler. 
 
To make the isolated world respected as an isolated world, the cache 
identifier should not be shared with a page under a ServiceWorker control. 
 
(cherry picked from commit 75f322ad1f64c0bc56fa77ab877b48d72cdb903c) 
 
Bug: 372512079, 373263969 
Change-Id: Idd2d8900f2f720e0a4dc9837e2eb56474c60b587 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5961018 
Reviewed-by: Justin Lulejian <jlulejian@chromium.org> 
Reviewed-by: Kouhei Ueno <kouhei@chromium.org> 
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1376006} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6002191 
Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
Commit-Queue: Kouhei Ueno <kouhei@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6778@{#1849} 
Cr-Branched-From: b21671ca172dcfd1566d41a770b2808e7fa7cd88-refs/heads/main@{#1368529}

```

---

Files:

- M `third_party/blink/renderer/core/html/parser/html_srcset_parser.cc`
- M `third_party/blink/renderer/core/inspector/inspector_network_agent.cc`
- M `third_party/blink/renderer/core/inspector/inspector_page_agent.cc`
- M `third_party/blink/renderer/core/loader/image_loader.cc`
- M `third_party/blink/renderer/core/testing/internals.cc`
- M `third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc`
- M `third_party/blink/renderer/platform/loader/fetch/resource_fetcher.h`

---

Hash: 923797bac92541669bd90bf69515a8bdb7f2c98c  

Date:  Thu Nov 07 10:14:59 2024


---

### pe...@google.com (2024-11-07)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### am...@chromium.org (2024-11-13)

please go ahead and merge this fix to branch 6723 at your earliest convenience -- thank you

### sp...@google.com (2024-11-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
$1,000 for report baseline / lower impact web platform privilege escalation as a carry over from the already rewarded report of crbug.com/371011220


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-14)

Congratulations! Thank you for this report, and again for your efforts on your original report, Vsevolod. Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-11-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-11-19)

Project: chromium/src  

Branch: refs/branch-heads/6723  

Author: Yoshisato Yanagisawa <[yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6000194>

[M130] Make GetCacheIdentifier() respect GetSkipServiceWorker().

---


Expand for full commit details
```
[M130] Make GetCacheIdentifier() respect GetSkipServiceWorker(). 
 
Since the current GetCacheIdentifier() ignores GetSkipServiceWorker(), 
GetCacheIdentifier() returns ServiceWorkerId even if GetSkipServiceWorker() 
is true if the ServiceWorker has a fetch handler. 
 
To make the isolated world respected as an isolated world, the cache 
identifier should not be shared with a page under a ServiceWorker control. 
 
(cherry picked from commit 75f322ad1f64c0bc56fa77ab877b48d72cdb903c) 
 
Bug: 372512079, 373263969 
Change-Id: Idd2d8900f2f720e0a4dc9837e2eb56474c60b587 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5961018 
Reviewed-by: Justin Lulejian <jlulejian@chromium.org> 
Reviewed-by: Kouhei Ueno <kouhei@chromium.org> 
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1376006} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6000194 
Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6723@{#2247} 
Cr-Branched-From: 985f2961df230630f9cbd75bd6fe463009855a11-refs/heads/main@{#1356013}

```

---

Files:

- M `third_party/blink/renderer/core/html/parser/html_srcset_parser.cc`
- M `third_party/blink/renderer/core/inspector/inspector_network_agent.cc`
- M `third_party/blink/renderer/core/inspector/inspector_page_agent.cc`
- M `third_party/blink/renderer/core/loader/image_loader.cc`
- M `third_party/blink/renderer/core/testing/internals.cc`
- M `third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc`
- M `third_party/blink/renderer/platform/loader/fetch/resource_fetcher.h`

---

Hash: 59d46b95c01984a5b09c060a98a17d81eafc2f11  

Date:  Tue Nov 19 00:59:24 2024


---

### pe...@google.com (2024-12-06)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-12-06)

1. 2 CLs <https://crrev.com/c/5962436/2> and <https://crrev.com/c/6001522>
2. Low, only one simple conflict
3. 130, 131
4. Yes

### ap...@google.com (2024-12-11)

Project: chromium/src  

Branch: refs/branch-heads/6478  

Author: Yoshisato Yanagisawa <[yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6001522>

[M126-LTS] Make GetCacheIdentifier() respect GetSkipServiceWorker().

---


Expand for full commit details
```
[M126-LTS] Make GetCacheIdentifier() respect GetSkipServiceWorker(). 
 
M126 merge issues: 
  third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc: 
    RequestResource()/CreateResourceForLoading(): The kScopeMemoryCachePerContext 
    feature check isn't present in the original CL. 
 
Since the current GetCacheIdentifier() ignores GetSkipServiceWorker(), 
GetCacheIdentifier() returns ServiceWorkerId even if GetSkipServiceWorker() 
is true if the ServiceWorker has a fetch handler. 
 
To make the isolated world respected as an isolated world, the cache 
identifier should not be shared with a page under a ServiceWorker control. 
 
(cherry picked from commit 75f322ad1f64c0bc56fa77ab877b48d72cdb903c) 
 
Bug: 372512079, 373263969 
Change-Id: Idd2d8900f2f720e0a4dc9837e2eb56474c60b587 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5961018 
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1376006} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6001522 
Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6478@{#2006} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `third_party/blink/renderer/core/html/parser/html_srcset_parser.cc`
- M `third_party/blink/renderer/core/inspector/inspector_network_agent.cc`
- M `third_party/blink/renderer/core/inspector/inspector_page_agent.cc`
- M `third_party/blink/renderer/core/loader/image_loader.cc`
- M `third_party/blink/renderer/core/testing/internals.cc`
- M `third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc`
- M `third_party/blink/renderer/platform/loader/fetch/resource_fetcher.h`

---

Hash: 7a58557512d5d17eddae11cd3be57a14beeb6cee  

Date:  Wed Dec 11 08:28:26 2024


---

### pe...@google.com (2025-02-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $1,000 for report baseline / lower impact web platform privilege escalation as a carry over from the already rewarded report of crbug.com/371011220

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/373263969)*
