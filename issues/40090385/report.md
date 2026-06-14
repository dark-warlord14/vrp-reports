# WebVTT CORS bypass using ServiceWorker

| Field | Value |
|-------|-------|
| **Issue ID** | [40090385](https://issues.chromium.org/issues/40090385) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>Video, Blink>ServiceWorker |
| **Platforms** | Mac |
| **Reporter** | s....@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2018-02-03 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36

Steps to reproduce the problem:
1. Go to https://attack.shhnjk.com/VTT_steal.html
2. Reload the page

What is the expected behavior?
https://attack.shhnjk.com/ does not have access to https://test.shhnjk.com/vtt.vtt

What went wrong?
CORS check for WebVTT can be bypassed when same-origin resource is intercepted by SW and redirected to cross-origin resource. This repros after the fix of https://crbug.com/chromium/780435, so this is a different bug.

Did this work before? N/A 

Chrome version: 64.0.3282.119  Channel: n/a
OS Version: OS X 10.13.3
Flash Version:

## Timeline

### el...@chromium.org (2018-02-03)

We started enforcing origin restrictions here only relatively recently, in https://crbug.com/chromium/633885.

Bypass via ServiceWorker is mentioned in #3 of https://crbug.com/chromium/808334.

[Monorail components: Blink>Media>Video Blink>ServiceWorker]

### mk...@chromium.org (2018-02-05)

Assigning medium severity, as I believe we have MIME-type restrictions on track files. If that turns out not to be the case, and this exposes more kinds of data cross-origin, we should bump the severity.

japhet@: Would you mind taking a look at this, since you added the CORS restrictions in the first place (no good deed... :) )? falken@ can probably help figure out what the right interaction with Service Workers ought to be.

### sh...@chromium.org (2018-02-05)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-02-05)

Re #2: We don't have a MIME-restriction per-se, but we do require that the file starts with the exact text "WEBVTT" followed by SP, TAB, or LF:
https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/html/track/vtt/VTTParser.cpp?l=192&rcl=b0e53acd2ae9fe474ee32a1fc631dad2dc182709, meaning an attacker would need an injection in the file. Further exploitability discussion here: https://bugs.chromium.org/p/chromium/issues/detail?id=633885#c16


### fa...@chromium.org (2018-02-06)

It seems to me the fix for https://crbug.com/chromium/633885 (https://codereview.chromium.org/2400433002) checks that CORS was on or the request URL is allowed to be requested.

With service workers the request URL origin and response URL origin can be different. So we likely must also check FetchResponseType like what https://chromium-review.googlesource.com/828564 added.

### in...@chromium.org (2018-02-06)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-02-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c0bca399136db67de29a7ffae1ed802fd5b42768

commit c0bca399136db67de29a7ffae1ed802fd5b42768
Author: Matt Falkenhagen <falken@chromium.org>
Date: Fri Feb 09 04:08:29 2018

service worker: Disallow opaque responses for WebVTT.

WebVTT loading code was determining if a response was cross-origin by looking
at request URL. But a service worker may have intercepted the request and
provided a response from cross-origin.

Bug: 808825
Cq-Include-Trybots: master.tryserver.chromium.linux:linux_mojo
Change-Id: Ia121c0a8eae782de93d9777603426500a9709f8c
Reviewed-on: https://chromium-review.googlesource.com/907013
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#535625}
[modify] https://crrev.com/c0bca399136db67de29a7ffae1ed802fd5b42768/services/network/public/cpp/resource_response_info.h
[add] https://crrev.com/c0bca399136db67de29a7ffae1ed802fd5b42768/third_party/WebKit/LayoutTests/external/wpt/media/foo-no-cors.vtt
[add] https://crrev.com/c0bca399136db67de29a7ffae1ed802fd5b42768/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/vtt-frame.html
[add] https://crrev.com/c0bca399136db67de29a7ffae1ed802fd5b42768/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/webvtt-cross-origin.https.html
[modify] https://crrev.com/c0bca399136db67de29a7ffae1ed802fd5b42768/third_party/WebKit/Source/core/loader/TextTrackLoader.cpp
[modify] https://crrev.com/c0bca399136db67de29a7ffae1ed802fd5b42768/third_party/WebKit/Source/core/loader/TextTrackLoader.h
[modify] https://crrev.com/c0bca399136db67de29a7ffae1ed802fd5b42768/third_party/WebKit/Source/platform/loader/fetch/ResourceResponse.cpp
[modify] https://crrev.com/c0bca399136db67de29a7ffae1ed802fd5b42768/third_party/WebKit/Source/platform/loader/fetch/ResourceResponse.h


### aw...@chromium.org (2018-02-12)

Any more changes expected or can we mark this as fixed? Thanks!

### go...@chromium.org (2018-02-13)

M65 Stable promotion is coming VERY soon. Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and request a merge  into the release branch ASAP. Thank you.

### fa...@chromium.org (2018-02-14)

I don't expect more code changes but I wanted to add tests that involve redirects and make sure things work. I ran into https://crbug.com/chromium/810288 while attempting that (which turned out to be a red herring).

### fa...@chromium.org (2018-02-14)

The tests at https://chromium-review.googlesource.com/c/chromium/src/+/918261 look passing locally so no further code changes are needed.

I'll mark this as Fixed.

I'm unclear whether this qualifies as a RBS that requires merging. I believe this bug has been in service worker since inception (Chrome 40-ish?), so it's not a recent regression. My inclination is to not merge as it could conceivably unstabilize stable late in the game.

### bu...@chromium.org (2018-02-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/038e2d8e8775b6262ff5997b6f4a820702713106

commit 038e2d8e8775b6262ff5997b6f4a820702713106
Author: Matt Falkenhagen <falken@chromium.org>
Date: Wed Feb 14 08:42:28 2018

service worker: Add tests for cross-origin WebVTT responses with redirects.

This is a follow-up to: https://chromium-review.googlesource.com/c/chromium/src/+/907013

Tests only; the code seems to work.

R=horo, kinuko

Bug: 808825
Change-Id: I6b86a4dac159b754cfe5e6b92ac390c07de89ab3
Reviewed-on: https://chromium-review.googlesource.com/918261
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#536679}
[modify] https://crrev.com/038e2d8e8775b6262ff5997b6f4a820702713106/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/webvtt-cross-origin.https.html


### sh...@chromium.org (2018-02-14)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-02-15)

Fix is in 66.0.3345.0. Per c#12 I don't intend to merge this, but let me know if you disagree.

### aw...@chromium.org (2018-02-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-02-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-26)

Congrats s.h.h.n.j.k@! The VRP panel decided to award $500 for this report - thanks!

### aw...@chromium.org (2018-02-27)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-03-02)

Hmm, I think this vuln is more severe and $500 seems less. Since WebVTT doesn't care about response taint, I think we can use Range reponse from SW to  provide necessary prefix ("WEBVTT" followed by SP, TAB, or LF) and then
redirect further request to cross-origin HTML and get content.

See: http://sirdarckcat.blogspot.co.uk/2015/10/range-responses-mix-match-leak.html

### s....@gmail.com (2018-03-02)

Alright, seems like setting range header in SW doesn't initiate further request from client. Sad :(

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-03-19)

Since this landed in Feb, no merge needed for 66. 

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/808825?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>Video, Blink>ServiceWorker]
[Monorail blocked-on: crbug.com/chromium/808334]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090385)*
