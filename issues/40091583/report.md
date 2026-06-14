# ServiceWorker circumvents same-origin restrictions for Audio

| Field | Value |
|-------|-------|
| **Issue ID** | [40091583](https://issues.chromium.org/issues/40091583) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>CORS, Blink>ServiceWorker, Blink>WebAudio |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | yh...@chromium.org |
| **Created** | 2018-06-06 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/webau.html
2. Reload the page
3. Play audio on the left side

What is the expected behavior?
MediaElementAudioSource outputs zeroes due to CORS access restrictions.

What went wrong?
Patch of https://crbug.com/chromium/826552 is incomplete. It solved the issue of redirect but patch can be bypassed using Service Worker.

Did this work before? N/A 

Chrome version: 67.0.3396.62  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### go...@chromium.org (2018-06-06)

[Empty comment from Monorail migration]

[Monorail components: Blink>ServiceWorker]

### fa...@chromium.org (2018-06-06)

Can I have access to 826552?

### fa...@chromium.org (2018-06-06)

cc people from https://chromium-review.googlesource.com/c/chromium/src/+/1069540

### yh...@chromium.org (2018-06-06)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>CORS Blink>WebAudio]

### fa...@chromium.org (2018-06-06)

This is similar to https://crbug.com/chromium/780435.

The fix probably needs to have plumbing like https://chromium-review.googlesource.com/c/chromium/src/+/828564

### yh...@chromium.org (2018-06-06)

+1

Sorry for overlooking the issue.

### fa...@chromium.org (2018-06-06)

Sorry for all these service worker security issues...

### pa...@chromium.org (2018-06-06)

First of all, A+ on the horse neighing sound sample. All PoCs should come with such good audio tracks. :)

Do we think of this as primarily a Service Worker bug, or as a CORS bug? Or as a WebAudio bug?

I'm going to call this Low severity, but I'm open to arguments that it could be Medium. (Highly-sensitive authenticated-only audio leaking cross-origin? Does this apply to more than just audio? Video?) So far I'm imagining public/semi-public podcasts leaking across origins, but is there more? Let us know; we like paying higher bounties.

### s....@gmail.com (2018-06-06)

>Does this apply to more than just audio? Video?
Here is a PoC for video.
https://test.shhnjk.com/webvideo.html

### s....@gmail.com (2018-06-07)

Without other bug (e.g. range request bug), this bug can only steal audio data of cross-origin audio/video file. But I don't think this is a low severity bug (this should be medium).

### sh...@chromium.org (2018-06-07)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-06-08)

FWIW, a WebAudio customer mentioned that leaking audio this way was not that important to them because it's not really any worse than the analog hole.  It *would* be an issue if you could download 1 hour audio clip in a few seconds.  The way it works now is that you'd have to wait for 1 hour to get all the data.

I'd also like to know if this is a WebAudio issue or not.  If it is, I'll definitely need help in figuring out how to detect that a service worker redirected the audio.

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-07-30)

falken: Would you mind taking an initial look and reassigning if it seems more like a WebAudio issue?

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-09-21)

Sorry I have left this bug alone for some time. yhirano@ has been looking at issues like these lately. yhirano@ could you take a look?

### yh...@chromium.org (2018-09-21)

I made a failing test at https://chromium-review.googlesource.com/c/chromium/src/+/1238098/2. rtoy@, reporter, is the test verifying what you are expecting?

### yh...@chromium.org (2018-09-21)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-09-21)

The webaudio parts of the test look right.  The expected output should be all zeroes.  Thanks for looking in to this!

### bu...@chromium.org (2018-10-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a9cbaa7a40e2b2723cfc2f266c42f4980038a949

commit a9cbaa7a40e2b2723cfc2f266c42f4980038a949
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Wed Oct 10 08:35:22 2018

Simplify "WouldTaintOrigin" concept in media/blink

Currently WebMediaPlayer has three predicates:
 - DidGetOpaqueResponseFromServiceWorker
 - HasSingleSecurityOrigin
 - DidPassCORSAccessCheck
. These are used to determine whether the response body is available
for scripts. They are known to be confusing, and actually
MediaElementAudioSourceHandler::WouldTaintOrigin misuses them.

This CL merges the three predicates to one, WouldTaintOrigin, to remove
the confusion. Now the "response type" concept is available and we
don't need a custom CORS check, so this CL removes
BaseAudioContext::WouldTaintOrigin. This CL also renames
URLData::has_opaque_data_ and its (direct and indirect) data accessors
to match the spec.

Bug: 849942, 875153
Change-Id: I6acf50169d7445c4ff614e80ac606f79ee577d2a
Reviewed-on: https://chromium-review.googlesource.com/c/1238098
Reviewed-by: Fredrik Hubinette <hubbe@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#598258}
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/content/renderer/media/stream/webmediaplayer_ms.cc
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/content/renderer/media/stream/webmediaplayer_ms.h
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/content/renderer/media_capture_from_element/html_video_element_capturer_source_unittest.cc
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/media/blink/multibuffer_data_source.cc
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/media/blink/multibuffer_data_source.h
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/media/blink/multibuffer_data_source_unittest.cc
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/media/blink/resource_multibuffer_data_provider.cc
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/media/blink/url_index.cc
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/media/blink/url_index.h
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/media/blink/webmediaplayer_impl.cc
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/media/blink/webmediaplayer_impl.h
[add] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-audio-tainting.https.html
[delete] https://crrev.com/50436d878b2e92de4231fda47328a8a4e884ecc3/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-video-cache.https-expected.txt
[delete] https://crrev.com/50436d878b2e92de4231fda47328a8a4e884ecc3/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-video.https-expected.txt
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/third_party/blink/public/platform/web_media_player.h
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/third_party/blink/renderer/core/html/media/html_media_element.cc
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/third_party/blink/renderer/core/html/media/html_media_element.h
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/third_party/blink/renderer/modules/webaudio/base_audio_context.cc
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/third_party/blink/renderer/modules/webaudio/base_audio_context.h
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/third_party/blink/renderer/modules/webaudio/media_element_audio_source_node.cc
[modify] https://crrev.com/a9cbaa7a40e2b2723cfc2f266c42f4980038a949/third_party/blink/renderer/platform/testing/empty_web_media_player.h


### yh...@chromium.org (2018-10-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-11)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2018-10-17)

This should be medium severity.

### sh...@chromium.org (2018-10-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-22)

And $1,000 for this one :-)

### aw...@chromium.org (2018-10-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-10-26)

(Already in 71)

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-01-17)

This issue was migrated from crbug.com/chromium/849942?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>CORS, Blink>ServiceWorker, Blink>WebAudio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091583)*
