# Performance API is not consistent for preloaded requests which can be used to leak the size of cross-origin resources

| Field | Value |
|-------|-------|
| **Issue ID** | [40057937](https://issues.chromium.org/issues/40057937) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader>Preload, Blink>PerformanceAPIs, Blink>ServiceWorker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | pm...@chromium.org |
| **Created** | 2021-11-17 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a cross-origin resource is used in an audio/video tag, a request containing the Range header asking for "bytes=0-" is issued. If the request is intercepted using a Service Worker and we respond with an arbitrary Content-Range header, e.g:  

e.respondWith(new Response("A", {status: 206, headers: { "Content-Range": "bytes 0-5000/13337" }}));

Chrome will be tricked into thinking it got the first 5000 bytes of the audio/video and then ask for the remaining bytes by issuing a new request containing the "Range: bytes=5000-" header.

If we also intercept the following request and send it again using the Fetch API, the request will be sent again containing the "Range: bytes=5000-" header and there will be two possible outcomes:

1. The server will return a "416 Range Not Satisfiable" response status code if the cross-origin response size is smaller than 5000 bytes.
2. The server will return a "206 Partial Content" response status code if the cross-origin response size is bigger than 5000 bytes.

We can then preload a random resource (using <link preload>), and by using a service worker, intercept the request and respond to it with the response from the previous fetch (which contains a 416 or 206 status code response).

If the preload's response is set to contain a 206 status code response, it will fail and be canceled, and each time you try to preload the same resource, a new performance entry will be added.

Otherwise, if the preload's response is set to contain a 416 status code, the preload will work, and each time you try to preload the same resource, no new performance entry will be added, as you can only successfully preload resources once.

This oracle allows an attacker to detect the possible outcomes mentioned above and leak the exact size of cross-origin resources that accept range requests.

In the PoC, the size of <https://www.google.com/robots.txt> is being brute-forced starting on byte 7250. In a real attack, it would be trying to get the size through binary search.

This vulnerability is useful for XS-Search attacks. A real-world example is <https://medium.com/@luanherrera/xs-searching-googles-bug-tracker-to-find-out-vulnerable-source-code-50d8135b7549> (more on <https://github.com/xsleaks/xsleaks/wiki/Real-World-Examples>).

This is a variation of <https://crbug.com/chromium/990849> (which I reported a few years ago) and <https://crbug.com/chromium/1260649> (which was recently reported and fixed).

**VERSION**  

Chrome Version: 96.0.4664.45 (Official Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Access <https://lbherrera.github.io/lab/chrome/range-preload-1e2388ffe/index.html>
2. Click on the "check" button and after a moment you should see messages about the leaked size of the cross-origin resource.

I have also attached the files used in the PoC - if you prefer, you can reproduce the attack by downloading and hosting index.html and sw.js on a web server.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [index.html](attachments/index.html) (text/plain, 3.1 KB)
- [sw.js](attachments/sw.js) (text/plain, 929 B)

## Timeline

### [Deleted User] (2021-11-17)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-11-18)

Thanks for the report! Assigning to wanderview@ as per https://crbug.com/chromium/1260649.

[Monorail components: Blink>PerformanceAPIs Blink>ServiceWorker]

### [Deleted User] (2021-11-18)

[Empty comment from Monorail migration]

### wa...@chromium.org (2021-11-18)

As the oracle here is due to preload behavior I think the loading team needs to take this.  Assigning to Kouhei to triage.

[Monorail components: Blink>Loader>Preload]

### yo...@chromium.org (2021-11-19)

[Empty comment from Monorail migration]

### pm...@chromium.org (2021-11-19)

I don't think this is limited to the performance API (though that's the leak vector).  Even if the fetches weren't reported, communication between the page and the service worker could be used to see how many preloads are used vs go to the wire.

The core issue is that the 206's are errors that show as canceled which causes it to be removed from the preload cache in the resource fetcher: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc;l=1935

The 416's are non-error loads that go through the regular finish path that doesn't remove the preloads: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc;l=1855

The success/error logic doesn't appear to be scoped to specific resources so preloads are treated like normal fetches which makes me a bit nervous to change the success/failure condition in the general sense.  The cleanest spot solution would likely be to remove the preload under successful conditions if it is a link-preload and the response is a 416 (could also scope it specifically to cross-origin responses).  We could also more generally remove any 4xx+ preloads from the cache but that would change the behavior for 404's (which may be desired but is beyond the oracle attack).

I'm happy to make the spot fix for 416's removing the preload if it seems reasonable or defer to others if we want to tackle it with a broader change to loading in general.

### wa...@chromium.org (2021-11-19)

Not all servers respond with 416, though.  See:

https://httpwg.org/specs/rfc7233.html#status.416

Some respond with 200s.  So removing 416s would still allow an attacker to discern between 206 or not for servers that send 200 in these condition.

Can we permit 206 in the preload cache when its a no-cors cross-origin request?  This is basically what we decided to do for cache_storage.  Leaking the state of a no-cors cross-origin request is the underlying problem here.

### pm...@chromium.org (2021-11-19)

I'll take a look to see how much plumbing is involved to not treat 206 for preloaded range requests for cors resources as a canceled error (at least for the purposes of preload).

### pm...@chromium.org (2021-11-19)

Ah, here we go and it's pretty explicit: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/resource_loader.cc;l=1106

On first glance it feels a bit dangerous to keep an explicitly blocked resource in the prefetch cache rather than running it through the error path. What I think might work better is if we always remove anything from the preload cache where response.HasRangeRequested() is set to true. There shouldn't be any case where a preload triggers a range request and that will keep the behavior consistent for 200, 206 and 416.

### [Deleted User] (2021-11-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pm...@chromium.org (2021-11-22)

To keep things consistent with the logic in ResourceLoader, the plan is to reject things from the preload cache under the same conditions:

- The response had a range request when it was actually sent
- The response is opaque
- The original request did not include a range

There shouldn't be any case where a preload starts with a range request but, in case there are this will make sure it is consistent in behavior with the case where the request gets canceled upstream in ResourceLoader.

### wa...@chromium.org (2021-11-22)

Can we instead make the header conditional a DCHECK then?  It seems like that would make the intent more clear with less risk of leaking opaque response data in the wild.

### pm...@chromium.org (2021-11-22)

The request error path removes a URL from the preload cache if a request is canceled (ignoring if the request that generated the error was a preload request itself): https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc;l=1935

The loader logic that initiates the cancel also doesn't care about preloads specifically. It just checks to see if a response was opaque and had a range request but the original request did not (i.e. a service worker rewrote the request under the covers).
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/resource_loader.cc;l=1106

To make sure the preload cache is 100% consistent in the "success" case (where a non-206 response is a success) we should mirror that same logic.

If we switch to a DCHECK and check only in the case of invalid preloads then there may still be some strange edge case that gets missed (intermingling preloads and fetches).

What is the risk of leaking opaque response data?  The proposed change only flushes an entry from the cache in conditions where it is currently kept. Nothing additional is being stored (we aren't storing the failed cases to match the success cases, we are clearing out the cache in the success case to match the error case).

### wa...@chromium.org (2021-11-22)

Hmm, ok.  I guess I don't fully understand the constraints on preload manager.  As long as an opaque response with HasRangeRequested will always be prevented from being in preload cache I guess it solves the issue.

### gi...@appspot.gserviceaccount.com (2021-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a5f630e5f94da28a926d60da7dde194acd8697f0

commit a5f630e5f94da28a926d60da7dde194acd8697f0
Author: Patrick Meenan <pmeenan@chromium.org>
Date: Mon Nov 29 19:10:38 2021

Prevent opaque range request responses from entering the preload cache

ResourceLoader cancels range request responses that were not initiated
with range request headers causing them to error out and be cleared from
the preload cache. Other responses (200, 416, error, etc) complete
successfully and would otherwise enter the preload cache, making them
observable.

This prevents opaque range responses of any kind from persisting in the
preload cache (which would not naturally have any anyway).

Bug: 1270990
Change-Id: Ife9922fe0b88e39722f3664ddd091a1516892157
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3294001
Reviewed-by: Ben Kelly <wanderview@chromium.org>
Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
Commit-Queue: Patrick Meenan <pmeenan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#946055}

[modify] https://crrev.com/a5f630e5f94da28a926d60da7dde194acd8697f0/third_party/blink/web_tests/external/wpt/fetch/range/resources/utils.js
[modify] https://crrev.com/a5f630e5f94da28a926d60da7dde194acd8697f0/third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc
[modify] https://crrev.com/a5f630e5f94da28a926d60da7dde194acd8697f0/third_party/blink/web_tests/external/wpt/fetch/range/sw.https.window.js
[modify] https://crrev.com/a5f630e5f94da28a926d60da7dde194acd8697f0/third_party/blink/web_tests/external/wpt/fetch/range/sw.https.window-expected.txt
[modify] https://crrev.com/a5f630e5f94da28a926d60da7dde194acd8697f0/third_party/blink/web_tests/external/wpt/fetch/range/resources/range-sw.js
[add] https://crrev.com/a5f630e5f94da28a926d60da7dde194acd8697f0/third_party/blink/web_tests/external/wpt/fetch/range/resources/partial-text.py


### pm...@chromium.org (2021-11-30)

Fixed and no longer reproduces with the test case in the current canary.

### pm...@chromium.org (2021-11-30)

Requesting merge to 96 and 97.

Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
High-severity security issue.

What changes specifically would you like to merge?
https://chromium.googlesource.com/chromium/src/+/a5f630e5f94da28a926d60da7dde194acd8697f0

Have the changes been released and tested on canary?
Yes

Is this a new feature?
No


### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-30)

Merge review required: M97 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-30)

Merge review required: M96 is already shipping to stable.

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

### pm...@chromium.org (2021-11-30)

1. Why does your merge fit within the merge criteria for these milestones?
High Severity security issue

2. What changes specifically would you like to merge?
https://chromium-review.googlesource.com/c/chromium/src/+/3294001

3. Have the changes been released and tested on canary?
Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No, N/A

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
1 - Access https://lbherrera.github.io/lab/chrome/range-preload-1e2388ffe/index.html
2 - Click Check
3 - Verify that it keeps checking beyond 7165 bytes

### [Deleted User] (2021-12-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-12-02)

merge approved for M96, please merge to branch 4664 ASAP so this fix can be in by stable cut tomorrow and included in the next week's stable refresh 

merge approved for M97, please merge to branch 4692 at your earliest convenience. thanks! 

### gi...@appspot.gserviceaccount.com (2021-12-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dbde8795233ac77de05b9309210bcf6a137f8959

commit dbde8795233ac77de05b9309210bcf6a137f8959
Author: Patrick Meenan <pmeenan@chromium.org>
Date: Fri Dec 03 18:15:17 2021

Prevent opaque range request responses from entering the preload cache

ResourceLoader cancels range request responses that were not initiated
with range request headers causing them to error out and be cleared from
the preload cache. Other responses (200, 416, error, etc) complete
successfully and would otherwise enter the preload cache, making them
observable.

This prevents opaque range responses of any kind from persisting in the
preload cache (which would not naturally have any anyway).

(cherry picked from commit a5f630e5f94da28a926d60da7dde194acd8697f0)

Bug: 1270990
Change-Id: Ife9922fe0b88e39722f3664ddd091a1516892157
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3294001
Reviewed-by: Ben Kelly <wanderview@chromium.org>
Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
Commit-Queue: Patrick Meenan <pmeenan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#946055}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3313416
Auto-Submit: Patrick Meenan <pmeenan@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1222}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/dbde8795233ac77de05b9309210bcf6a137f8959/third_party/blink/web_tests/external/wpt/fetch/range/resources/utils.js
[modify] https://crrev.com/dbde8795233ac77de05b9309210bcf6a137f8959/third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc
[modify] https://crrev.com/dbde8795233ac77de05b9309210bcf6a137f8959/third_party/blink/web_tests/external/wpt/fetch/range/sw.https.window.js
[modify] https://crrev.com/dbde8795233ac77de05b9309210bcf6a137f8959/third_party/blink/web_tests/external/wpt/fetch/range/sw.https.window-expected.txt
[modify] https://crrev.com/dbde8795233ac77de05b9309210bcf6a137f8959/third_party/blink/web_tests/external/wpt/fetch/range/resources/range-sw.js
[add] https://crrev.com/dbde8795233ac77de05b9309210bcf6a137f8959/third_party/blink/web_tests/external/wpt/fetch/range/resources/partial-text.py


### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-12-06)

Congratulations, Luan! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and nice work! 

### pb...@google.com (2021-12-07)

Your change has been approved for M97 branch 4692,please go ahead and merge the CL's to M97 branch manually asap so that they would be part of tomorrows Beta release.thank you

### [Deleted User] (2021-12-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pm...@chromium.org (2021-12-07)

Sorry, fighting the CQ bots - the Fuscia bot specifically has been in a bad state preventing the merge.

https://chromium-review.googlesource.com/c/chromium/src/+/3313302

### pm...@chromium.org (2021-12-07)

Filed a trooper bug to hopefully get the CQ issues sorted out: https://bugs.chromium.org/p/chromium/issues/detail?id=1277581

### am...@google.com (2021-12-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3244f616e74119cc190a90db8af746f7de98dc96

commit 3244f616e74119cc190a90db8af746f7de98dc96
Author: Patrick Meenan <pmeenan@chromium.org>
Date: Wed Dec 08 00:55:25 2021

Prevent opaque range request responses from entering the preload cache

ResourceLoader cancels range request responses that were not initiated
with range request headers causing them to error out and be cleared from
the preload cache. Other responses (200, 416, error, etc) complete
successfully and would otherwise enter the preload cache, making them
observable.

This prevents opaque range responses of any kind from persisting in the
preload cache (which would not naturally have any anyway).

(cherry picked from commit a5f630e5f94da28a926d60da7dde194acd8697f0)

Bug: 1270990
Change-Id: Ife9922fe0b88e39722f3664ddd091a1516892157
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3294001
Reviewed-by: Ben Kelly <wanderview@chromium.org>
Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
Commit-Queue: Patrick Meenan <pmeenan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#946055}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3313302
Auto-Submit: Patrick Meenan <pmeenan@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4692@{#801}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/3244f616e74119cc190a90db8af746f7de98dc96/third_party/blink/web_tests/external/wpt/fetch/range/resources/utils.js
[modify] https://crrev.com/3244f616e74119cc190a90db8af746f7de98dc96/third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc
[modify] https://crrev.com/3244f616e74119cc190a90db8af746f7de98dc96/third_party/blink/web_tests/external/wpt/fetch/range/sw.https.window.js
[modify] https://crrev.com/3244f616e74119cc190a90db8af746f7de98dc96/third_party/blink/web_tests/external/wpt/fetch/range/sw.https.window-expected.txt
[modify] https://crrev.com/3244f616e74119cc190a90db8af746f7de98dc96/third_party/blink/web_tests/external/wpt/fetch/range/resources/range-sw.js
[add] https://crrev.com/3244f616e74119cc190a90db8af746f7de98dc96/third_party/blink/web_tests/external/wpt/fetch/range/resources/partial-text.py


### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### yy...@google.com (2022-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@google.com (2022-03-30)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1270990?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Loader>Preload, Blink>PerformanceAPIs, Blink>ServiceWorker]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057937)*
