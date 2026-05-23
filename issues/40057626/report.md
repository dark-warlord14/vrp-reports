# Leaking size of cross-origin resources by using Range Requests, Service Workers, Fetch API, and the Cache API

| Field | Value |
|-------|-------|
| **Issue ID** | [40057626](https://issues.chromium.org/issues/40057626) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>PerformanceAPIs>ResourceTiming, Blink>ServiceWorker, Internals>Media>Network |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2021-10-16 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a cross-origin resource is used in an audio/video tag, a request containing the Range header asking for "bytes=0-" is issued.  

If the request is intercepted using a Service Worker and we respond with an arbitrary Content-Range header, e.g:  

e.respondWith(new Response("A", {status: 206, headers: { "Content-Range": "bytes 0-5000/13337" }}));

Chrome will be tricked into thinking it got the first 5000 bytes of the "audio/video" and then ask for the remaining bytes by issuing a new request containing the "Range: bytes=5000-" header.

If we also intercept the following request and send it again using the Fetch API, the request will be sent containing the "Range: bytes=5000-" header and there will be two possible outcomes:

1. The server will return a "416 Range Not Satisfiable" response status code if the cross-origin response size is smaller than 5000 bytes.
2. The server will return a "206 Partial Content" response status code if the cross-origin response size is bigger than 5000 bytes.

If we store a reference to the response and use Cache API's cache.put function to cache it, we can detect whether the response returned a 206 status code by listening to its error event given cache.put is not able to cache partial responses (<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/cache_storage/cache.cc;l=105>).

This oracle then allows an attacker to detect the possible outcomes mentioned above and leak the exact size of cross-origin resources that accept range requests.

In the PoC, the size of <https://www.google.com/robots.txt> is being brute-forced starting on byte 7250. In a real attack, it would be trying to get the size through binary search.

This vulnerability is useful for XS-Search attacks. A real-world example is <https://medium.com/@luanherrera/xs-searching-googles-bug-tracker-to-find-out-vulnerable-source-code-50d8135b7549> (more on <https://github.com/xsleaks/xsleaks/wiki/Real-World-Examples>).

This is a variation of a bug I reported a few years ago (<https://bugs.chromium.org/p/chromium/issues/detail?id=990849>).

Here's a video reproducing the issue:  

<https://youtu.be/LEHwg8xjBdE>

**VERSION**  

Chrome Version: 94.0.4606.81 (Official Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Access <https://lbherrera.github.io/lab/chrome/range-9e133f5d/index.html>
2. Click on the "check" button and after a moment you should see messages about the leaked size of the cross-origin resource.

I have also attached the files used in the PoC - if you prefer, you can reproduce the attack by downloading and hosting index.html and sw.js on a web server.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [index.html](attachments/index.html) (text/plain, 2.5 KB)
- [sw.js](attachments/sw.js) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2021-10-16)

[Empty comment from Monorail migration]

### bd...@chromium.org (2021-10-18)

Thanks for the report. I'm assigning a High severity as this leaks the size of a cross-origin resource.


[Monorail components: Blink>PerformanceAPIs>ResourceTiming Blink>ServiceWorker Internals>Media>Network]

### [Deleted User] (2021-10-18)

[Empty comment from Monorail migration]

### yo...@chromium.org (2021-10-19)

We had a similar attack [1] that was using the Resource Timing API to get at the same info, which we fixed a while ago. As this is using the cache API to get the "is this a partial response" bit, assigning to wanderview@. 

[1] https://bugs.chromium.org/p/chromium/issues/detail?id=990849&q=owner%3Ame%20206%20video&can=1 

### wa...@chromium.org (2021-10-19)

Would making cache_storage reject on putting a 416 solve this problem?  Then you would not be able to distinguish between the two.  Are there other status codes that might result besides these two?

### wa...@chromium.org (2021-10-19)

My work on this might be a bit delayed since I am currently busy with other P1 security issues.  Also, folks I'd like to discuss this with our OOO for a bit.

### wa...@chromium.org (2021-10-19)

According to the rfc the main alternative is for the server to return a 200:

https://httpwg.org/specs/rfc7233.html#status.416

Clearly we have to support 200 puts.  So blocking 416 puts would not be a full solution.

Perhaps a better alternative would be to not reject 206 puts for opaque responses.  We can either:

1) store the 206 as treat it as the same footgun as accidentally storing a 404 for opaque responses, or
2) convert the 206 to a 404 error or other error when storing an opaque response

I think (1) might be a bit more principled.  It makes opaque responses a bit more footgunny, but that seems to be the unfortunate consequence of their no-cors cross-site behavior.

### [Deleted User] (2021-10-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2021-10-28)

CL out for review:

https://chromium-review.googlesource.com/c/chromium/src/+/3251749

### wa...@chromium.org (2021-10-28)

Note, I have agreement from mozilla and the spec editor to make this change via private communication.  Apple was also included in the discussion, but they did not respond.

### wa...@chromium.org (2021-10-28)

I also verified the CL prevents the PoC linked in the original report above.

### gi...@appspot.gserviceaccount.com (2021-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/802faa035409ac7cbb58ad1a385bb8507fe99077

commit 802faa035409ac7cbb58ad1a385bb8507fe99077
Author: Ben Kelly <wanderview@chromium.org>
Date: Tue Nov 02 16:49:07 2021

CacheStorage: Store partial opaque responses.

Fixed: 1260649
Change-Id: If83156096e6aecec55490330d03c56c0c26120bc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3251749
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Cr-Commit-Position: refs/heads/main@{#937400}

[modify] https://crrev.com/802faa035409ac7cbb58ad1a385bb8507fe99077/third_party/blink/web_tests/external/wpt/service-workers/cache-storage/script-tests/cache-put.js
[modify] https://crrev.com/802faa035409ac7cbb58ad1a385bb8507fe99077/third_party/blink/renderer/modules/cache_storage/cache.cc
[modify] https://crrev.com/802faa035409ac7cbb58ad1a385bb8507fe99077/content/browser/cache_storage/legacy/legacy_cache_storage_cache.cc


### [Deleted User] (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-02)

Requesting merge to extended stable M94 because latest trunk commit (937400) appears to be after extended stable branch point (911515).

Requesting merge to stable M95 because latest trunk commit (937400) appears to be after stable branch point (920003).

Requesting merge to beta M96 because latest trunk commit (937400) appears to be after beta branch point (929512).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-03)

Merge review required: M96 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-03)

Merge review required: M95 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-03)

Merge review required: M94 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-05)

tentatively approving merge to M96; please ensure there are no stability issues or other concerns before merging; as long as there are no issues, please merge to branch 4664 by EOD Monday, 8 November so this can be included in the stable RC cut for M94 next week. Thank you! 

### am...@chromium.org (2021-11-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1fcfb942bd8a1def685cc1da09bfb26aaf2eac4b

commit 1fcfb942bd8a1def685cc1da09bfb26aaf2eac4b
Author: Ben Kelly <wanderview@chromium.org>
Date: Fri Nov 05 19:47:08 2021

CacheStorage: Store partial opaque responses.

(cherry picked from commit 802faa035409ac7cbb58ad1a385bb8507fe99077)

Fixed: 1260649
Change-Id: If83156096e6aecec55490330d03c56c0c26120bc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3251749
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Ben Kelly <wanderview@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#937400}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3264366
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4664@{#774}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/1fcfb942bd8a1def685cc1da09bfb26aaf2eac4b/third_party/blink/web_tests/external/wpt/service-workers/cache-storage/script-tests/cache-put.js
[modify] https://crrev.com/1fcfb942bd8a1def685cc1da09bfb26aaf2eac4b/third_party/blink/renderer/modules/cache_storage/cache.cc
[modify] https://crrev.com/1fcfb942bd8a1def685cc1da09bfb26aaf2eac4b/content/browser/cache_storage/legacy/legacy_cache_storage_cache.cc


### am...@google.com (2021-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-11)

Congratulations, Luan! The VRP Panel has decided to award you $2000 for this report. Nice work! 

### am...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1260649?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>PerformanceAPIs>ResourceTiming, Blink>ServiceWorker, Internals>Media>Network]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057626)*
