# Security: Cross-origin information leak via subresource integrity (SRI), fetch and Service Workers

| Field | Value |
|-------|-------|
| **Issue ID** | [40090509](https://issues.chromium.org/issues/40090509) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Network>FetchAPI, Blink>SecurityFeature, Blink>ServiceWorker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | yh...@chromium.org |
| **Created** | 2018-02-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

I have found an oracle that attackers can use to check whether an arbitrary remote resource matches a given hash. This vulnerability is the result of combining three APIs: SRI, fetch and Service Workers.

Subresource integrity (SRI) instructs the browser to check the integrity a remote resource, by computing the hash of the response with a pre-computed (expected) hash.  

This feature requires the remote resource to enable CORS, to prevent cross-origin information leakage [sri-1].

A request initiated via fetch can also include a SRI hash, via the "integrity" parameter.  

Step 12 of the fetch algorithm [fetch-2] states:

> If response is not a network error and request’s integrity metadata is not the empty string, run these substeps:
> 
> 1. Wait for response’s body.
> 2. If response’s body’s stream has not errored, and response does not match request’s integrity metadata, set response and internalResponse to a network error.
> 
> This operates on response as this algorithm is not supposed to observe internalResponse. That would allow an attacker to use hashes as an oracle.

The fetch API can be used to perform a cross-origin request without CORS by setting the mode to no-cors. The resulting response is opaque, and it does supposedly not offer any way to read the state of the response.

Service Workers can intercept cross-origin requests, and respond with opaque responses.

Together, the following issues ensues:

1. A web page triggers a resource request (cross-origin, no-cors, without SRI).
2. The Service Worker intercepts the request, and:
   - uses fetch(url, {mode: 'no-cors', integrity: '...'})  
     
     to get an opaque response, which internally holds the result of the SRI check.
   - responds with this opaque response to the original request.
3. The web page checks whether the resource has loaded:
   - If loaded, assume that the SRI check has passed.
   - If failed to load, the SRI check has failed.

**VERSION**  

Chrome : 64.0.3282.167 (stable) + 66.0.3349.0 (canary)  

Firefox is NOT affected (the CORS requirement is enforced for SRI, tested in Firefox 58)

**REPRODUCTION CASE**  

Visit <https://robwu.nl/s/service-worker-sri/> and try the two examples (click on the "Check SRI hash" button):

- SRI match detected : <https://robwu.nl/s/service-worker-sri/?url=https%3A%2F%2Fexample.com&sri=sha256-NYfLd2zg5OgjfyFYALff%2B6DyWGXLhFUOh%2BqLusg4xCM%3D>
- SRI mismatch detected: <https://robwu.nl/s/service-worker-sri/?url=https%3A%2F%2Fexample.com&sri=sha256-bogus>

The two cases should be indistinguishable. However, in Chrome, the first outputs "SRI hash matches" and the second "SRI hash does not match".

To fix this bug, Chrome should only allow the "integrity" parameter to be used in fetch if the request is either same-origin or cors (but not no-cors).

[sri-1] <https://www.w3.org/TR/SRI/#cross-origin-data-leakage>  

[fetch-2] <https://fetch.spec.whatwg.org/#main-fetch>

## Timeline

### ro...@robwu.nl (2018-02-15)

[Comment Deleted]

### ro...@robwu.nl (2018-02-15)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-02-15)

Nice find, Rob!

### el...@chromium.org (2018-02-15)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-02-15)

tyoshino@, does this proposal: "Chrome should only allow the "integrity" parameter to be used in fetch if the request is either same-origin or cors (but not no-cors)" seem workable?

### sh...@chromium.org (2018-02-16)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-03-01)

falken@: Do you know who would be a good owner for this bug, since tyoshino@ is leaving the project?

### mk...@chromium.org (2018-03-01)

A response that was made in `no-cors` mode should not be eligible for SRI verification (https://w3c.github.io/webappsec-subresource-integrity/#is-response-eligible). I think I agree that rejecting the call to `fetch()` in that case is reasonable.

I'm on a Chromebook at the moment, so I can't verify the Firefox behavior, but if it also returns a rejected promise, then we should follow suit, and send a PR against the spec at the same time.

### ro...@robwu.nl (2018-03-01)

#8 In the report I stated:

> Firefox is NOT affected (the CORS requirement is enforced for SRI, tested in Firefox 58)

I.e. when I run the PoC in Firefox 58, the promise is rejected,
and the console displays the following printed error message:
“https://example.com/” is not eligible for integrity checks since it’s neither CORS-enabled nor same-origin.

followed by the following warning message:
Loading failed for the <script> with source “https://example.com/#sriHash=sha256-NYfLd2zg5OgjfyFYALff+6DyWGXLhFUOh+qLusg4xCM=”.

followed by the following error message:
Failed to load ‘https://example.com/#sriHash=sha256-NYfLd2zg5OgjfyFYALff+6DyWGXLhFUOh+qLusg4xCM=’. A ServiceWorker passed a promise to FetchEvent.respondWith() that rejected with ‘TypeError: NetworkError when attempting to fetch resource.’

### sh...@chromium.org (2018-03-02)

falken: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@chromium.org (2018-03-05)

The proposal "Chrome should only allow the "integrity" parameter to be used in fetch if the request is either same-origin or cors" and matching Firefox's behavior "“https://example.com/” is not eligible for integrity checks since it’s neither CORS-enabled nor same-origin." sounds good to me.

I would be grateful if Network API team can take this bug as it falls in their area of code. yhirano, WDYT?

Resetting to Untriaged as I'm unassigning myself, but you can kick it back to me if you'd like.

### yh...@chromium.org (2018-03-05)

This is yet-another-bug caused by SRI verification implemented in FetchManager apart from Resource. We should fail SRI verification for non-eligible responses blindly. We have the logic in one of SubresourceIntegrity::CheckSubresourceIntegrity but we don't have it for another overloading.

### yh...@chromium.org (2018-03-05)

At this moment I don't think the spec has a problem.

### yh...@chromium.org (2018-03-05)

Actually we have a web platform test which has been broken... see https://chromium-review.googlesource.com/c/chromium/src/+/948184.

### yh...@chromium.org (2018-03-05)

+toyoshim@ for CORS

### bu...@chromium.org (2018-03-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5a4aa3bcaf8a52637ef445b2d2d6112364984122

commit 5a4aa3bcaf8a52637ef445b2d2d6112364984122
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Mon Mar 05 06:54:21 2018

Fix a typo in a web platform test for fetch/integrity

The test has succeeded unexpectedly, so this CL also adds an
expectation file.

Bug: 812667
Change-Id: I649a7663c54f83ccb951c5a4bf075b588908b088
Reviewed-on: https://chromium-review.googlesource.com/948184
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#540789}
[add] https://crrev.com/5a4aa3bcaf8a52637ef445b2d2d6112364984122/third_party/WebKit/LayoutTests/external/wpt/fetch/api/basic/integrity-expected.txt
[add] https://crrev.com/5a4aa3bcaf8a52637ef445b2d2d6112364984122/third_party/WebKit/LayoutTests/external/wpt/fetch/api/basic/integrity-sharedworker-expected.txt
[add] https://crrev.com/5a4aa3bcaf8a52637ef445b2d2d6112364984122/third_party/WebKit/LayoutTests/external/wpt/fetch/api/basic/integrity-worker-expected.txt
[modify] https://crrev.com/5a4aa3bcaf8a52637ef445b2d2d6112364984122/third_party/WebKit/LayoutTests/external/wpt/fetch/api/basic/integrity.js


### bu...@chromium.org (2018-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c7bfc96d2c218e8b1592d379da1fe256767cdf27

commit c7bfc96d2c218e8b1592d379da1fe256767cdf27
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Tue Mar 06 13:49:09 2018

Reject SRI blindly when response is ineligible for validation

We should reject SRI blindly when the response is not eligible for
integrity validation. The logic is correctly implemented in
ResourceLoader but not in FetchManager.

Bug: 812667
Change-Id: If0c29e2e541a1bb3edb09a72fbba3ae55c134303
Reviewed-on: https://chromium-review.googlesource.com/948229
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Cr-Commit-Position: refs/heads/master@{#541092}
[delete] https://crrev.com/ad6532e12c92025b6417b20b5bc0d31d385f4f2a/third_party/WebKit/LayoutTests/external/wpt/fetch/api/basic/integrity-expected.txt
[delete] https://crrev.com/ad6532e12c92025b6417b20b5bc0d31d385f4f2a/third_party/WebKit/LayoutTests/external/wpt/fetch/api/basic/integrity-sharedworker-expected.txt
[delete] https://crrev.com/ad6532e12c92025b6417b20b5bc0d31d385f4f2a/third_party/WebKit/LayoutTests/external/wpt/fetch/api/basic/integrity-worker-expected.txt
[modify] https://crrev.com/c7bfc96d2c218e8b1592d379da1fe256767cdf27/third_party/WebKit/Source/core/fetch/FetchManager.cpp
[modify] https://crrev.com/c7bfc96d2c218e8b1592d379da1fe256767cdf27/third_party/WebKit/Source/platform/loader/SubresourceIntegrity.h


### yh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### yh...@chromium.org (2018-03-07)

I would like to merge c7bfc96d2c218e8b1592d379da1fe256767cdf27 to M66 branch.

### sh...@chromium.org (2018-03-08)

Your change meets the bar and is auto-approved for M66. Please go ahead and merge the CL to branch 3359 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yh...@chromium.org (2018-03-08)

Mike, do you think we need to merge the fix to M65?

### bu...@chromium.org (2018-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/14673da4cdca78325a0bedd677856e3b4848678b

commit 14673da4cdca78325a0bedd677856e3b4848678b
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Thu Mar 08 10:06:31 2018

Reject SRI blindly when response is ineligible for validation

We should reject SRI blindly when the response is not eligible for
integrity validation. The logic is correctly implemented in
ResourceLoader but not in FetchManager.

(cherry picked from commit c7bfc96d2c218e8b1592d379da1fe256767cdf27)

Bug: 812667
Change-Id: I03027dbefdd8068b6dcca6d52156964749ab1c44
Reviewed-on: https://chromium-review.googlesource.com/948229
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#541092}
Reviewed-on: https://chromium-review.googlesource.com/954778
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/branch-heads/3355@{#5}
Cr-Branched-From: 31d0bb0369f909177f2ce90b439f296bcf9c90cb-refs/heads/master@{#539001}
[modify] https://crrev.com/14673da4cdca78325a0bedd677856e3b4848678b/third_party/WebKit/Source/core/fetch/FetchManager.cpp
[modify] https://crrev.com/14673da4cdca78325a0bedd677856e3b4848678b/third_party/WebKit/Source/platform/loader/SubresourceIntegrity.h


### sh...@chromium.org (2018-03-08)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-09)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-19)

Thanks Rob, $1,000 for this report!

### aw...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### yh...@chromium.org (2018-04-06)

Reopening the bug as I merged the fix to a wrong branch. Re-requesting merge https://crrev.com/14673da4cdca78325a0bedd677856e3b4848678b to 66.

### yh...@chromium.org (2018-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-06)

This bug requires manual review: We are only 10 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cm...@google.com (2018-04-06)

 awhalley@ please take care of this merge request.

### cm...@google.com (2018-04-10)

This should be merged today if it should be in the Android stable build

### aw...@google.com (2018-04-10)

cmasso@ - good for 66

### cm...@google.com (2018-04-10)

Please merge this today!

### bu...@chromium.org (2018-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9622d2d1dc2795fb4414e5921df4098e79b3aabf

commit 9622d2d1dc2795fb4414e5921df4098e79b3aabf
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Wed Apr 11 09:04:07 2018

Reject SRI blindly when response is ineligible for validation

We should reject SRI blindly when the response is not eligible for
integrity validation. The logic is correctly implemented in
ResourceLoader but not in FetchManager.

TBR=yhirano@chromium.org

(cherry picked from commit c7bfc96d2c218e8b1592d379da1fe256767cdf27)

Bug: 812667
Change-Id: If0c29e2e541a1bb3edb09a72fbba3ae55c134303
Reviewed-on: https://chromium-review.googlesource.com/948229
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#541092}
Reviewed-on: https://chromium-review.googlesource.com/1004977
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/branch-heads/3359@{#677}
Cr-Branched-From: 66afc5e5d10127546cc4b98b9117aff588b5e66b-refs/heads/master@{#540276}
[modify] https://crrev.com/9622d2d1dc2795fb4414e5921df4098e79b3aabf/third_party/WebKit/Source/core/fetch/FetchManager.cpp
[modify] https://crrev.com/9622d2d1dc2795fb4414e5921df4098e79b3aabf/third_party/WebKit/Source/platform/loader/SubresourceIntegrity.h


### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-05-10)

Is there anything left to do here, or can we mark it as Fixed?

### yh...@chromium.org (2018-05-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/812667?no_tracker_redirect=1

[Multiple monorail components: Blink>Network>FetchAPI, Blink>SecurityFeature, Blink>ServiceWorker]
[Monorail mergedwith: crbug.com/chromium/828888]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090509)*
