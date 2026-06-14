# Stealing cross-origin video pixel with HLS

| Field | Value |
|-------|-------|
| **Issue ID** | [40091945](https://issues.chromium.org/issues/40091945) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Media>Video |
| **Platforms** | Android |
| **Reporter** | s....@gmail.com |
| **Assignee** | tg...@chromium.org |
| **Created** | 2018-07-17 |
| **Bounty** | $4,000.00 |

## Description

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/hls/steal.html
2. Play video on the top
3. Click on get image

What is the expected behavior?
Access to cross-origin video's pixel is denied

What went wrong?
Even though the video is loaded from https://test.shhnjk.com/hls/testa.m3u8, actual video data is requested from served from https://vuln.shhnjk.com/video.m3u8 which is cross-origin. But Chrome leaks initial video pixel to the page. This might be because same-origin check is happening with video URL but due to HLS architecture, that video file still allows loading cross-origin video.

Did this work before? N/A 

Chrome version: 67.0.3396.87  Channel: stable
OS Version: 6.0.1
Flash Version:

## Timeline

### do...@chromium.org (2018-07-17)

[Empty comment from Monorail migration]

### do...@chromium.org (2018-07-17)

D'oh, sorry about closing this - didn't see the "Android" tag as opposed to iOS.

+cc some media folks, can you follow up on this please?

[Monorail components: Internals>Media>Video]

### ml...@chromium.org (2018-07-17)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-07-17)

Here's a PoC to steal any frame of video. It will steal the video frame when you click on the get image button.

https://test.shhnjk.com/hls/blink_steal.html

### tg...@chromium.org (2018-07-18)

dalecurtis@ suggested a fix offline. I will take a closer look and test things out tomorrow.

### sh...@chromium.org (2018-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/153f8457c7867d5c9b627c11b52f5de0671d2fff

commit 153f8457c7867d5c9b627c11b52f5de0671d2fff
Author: Thomas Guilbert <tguilbert@chromium.org>
Date: Thu Jul 19 05:03:58 2018

Fix HasSingleSecurityOrigin for HLS

HLS manifests can request segments from a different origin than the
original manifest's origin. We do not inspect HLS manifests within
Chromium, and instead delegate to Android's MediaPlayer. This means we
need to be conservative, and always assume segments might come from a
different origin. HasSingleSecurityOrigin should always return false
when decoding HLS.

Bug: 864283
Change-Id: Ie16849ac6f29ae7eaa9caf342ad0509a226228ef
Reviewed-on: https://chromium-review.googlesource.com/1142691
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Commit-Queue: Thomas Guilbert <tguilbert@chromium.org>
Cr-Commit-Position: refs/heads/master@{#576378}
[modify] https://crrev.com/153f8457c7867d5c9b627c11b52f5de0671d2fff/media/blink/webmediaplayer_impl.cc
[modify] https://crrev.com/153f8457c7867d5c9b627c11b52f5de0671d2fff/media/blink/webmediaplayer_impl.h


### tg...@chromium.org (2018-07-19)

I will verify on Dev tomorrow

### sh...@chromium.org (2018-07-20)

[Empty comment from Monorail migration]

### tg...@chromium.org (2018-07-20)

Canary doesn't have the patch yet. Snoozing till Monday

### aw...@chromium.org (2018-07-23)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### tg...@chromium.org (2018-07-23)

Verified on Canary 70.0.3498.0

### sh...@chromium.org (2018-08-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-03)

This bug requires manual review: M69 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@chromium.org (2018-08-03)

[Empty comment from Monorail migration]

### da...@chromium.org (2018-08-04)

This is already in the m69 branch, no action needed.

### aw...@chromium.org (2018-08-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-08-06)

Thanks again s.h.h.n.j.k@, $4,000 for this one.

### s....@gmail.com (2018-08-06)

Great! Thanks!

### aw...@chromium.org (2018-08-06)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/864283?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/864286]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091945)*
