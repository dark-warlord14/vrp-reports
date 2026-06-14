# MediaError message property leaks cross-origin response status

| Field | Value |
|-------|-------|
| **Issue ID** | [40090985](https://issues.chromium.org/issues/40090985) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media, Blink>SecurityFeature>SameOriginPolicy |
| **Platforms** | Linux |
| **Reporter** | ac...@gmail.com |
| **Assignee** | hu...@chromium.org |
| **Created** | 2018-04-03 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0

Steps to reproduce the problem:
1. Visit https://output.jsbin.com/nejatopusi
2. Enter a URL in the input box, click the "Test" button
(The URL will be loaded as the `src` of an audio element.) 

What is the expected behavior?
Cross-origin response status should not be detectable by scripts unless necessary CORS headers are sent by the server.

What went wrong?
The message property of the MediaError interface contains a different string for resources that loads successfully. This allows an attacker to infer the response status for a cross-origin resource.

Did this work before? N/A 

Chrome version: 64.0.3282.167 (Official Build) Built on Ubuntu , running on Ubuntu 17.10 (64-bit)  Channel: n/a
OS Version: 17.04
Flash Version: 

Detecting cross-origin response status can be used in various attacks such as inferring login status and detecting servers on the LAN. 

The following paper from 2015 gives an overview of attacks that are enabled by a similar AppCache-based vulnerability: https://www.cc.gatech.edu/~slee3036/papers/lee:appcache.pdf

## Timeline

### ac...@gmail.com (2018-04-03)

In particular, MediaError.message contains the following string for cross-origin resources that load successfully:
"DEMUXER_ERROR_COULD_NOT_OPEN: FFmpegDemuxer: open context failed"

A script can load any cross-origin URL as <audio>/<video> src to detect its status (200 OK or not).

### el...@chromium.org (2018-04-03)

Given that the Audio/Video elements intentionally expose richer information like the Duration of the loaded audio/video[1], does this error message actually expose any new information?


[1] https://bayden.com/test/video.html

[Monorail components: Blink>Media Blink>SecurityFeature>SameOriginPolicy]

### el...@chromium.org (2018-04-03)

Ah, I think the claim here is that this information is exposed even in the scenario where the target URL returns a non-Audio/non-Video response type?

### el...@chromium.org (2018-04-03)

Note to the Sheriff: This is somewhat similar to https://crbug.com/chromium/826187, and the mitigation for that may be useful here.

### ac...@gmail.com (2018-04-03)

Yes, indeed. It could detect the status of text/html or similar non-media resources.

### sh...@chromium.org (2018-04-03)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2018-04-03)

Thanks for your assessment elawrence@! 

Assign to hubbe@chromium.org, since it is quite similar to https://bugs.chromium.org/p/chromium/issues/detail?id=826187.

hubbe@, please feel free to merge these two issues if you see fit. Thanks!

### ji...@chromium.org (2018-04-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-17)

hubbe: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2018-04-17)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-05-08)

Any update here? I see the bug is marked as started. Were you able to make progress?

### hu...@chromium.org (2018-05-08)

Yes, I expect to have a CL checked in today or tomorrow.


### bu...@chromium.org (2018-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4504a474c069d07104237d0c03bfce7b29a42de6

commit 4504a474c069d07104237d0c03bfce7b29a42de6
Author: Fredrik Hubinette <hubbe@google.com>
Date: Wed May 09 20:56:54 2018

defeat cors attacks on audio/video tags

Neutralize error messages and fire no progress events
until media metadata has been loaded for media loaded
from cross-origin locations.

Bug: 828265, 826187
Change-Id: Iaf15ef38676403687d6a913cbdc84f2d70a6f5c6
Reviewed-on: https://chromium-review.googlesource.com/1015794
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Fredrik Hubinette <hubbe@chromium.org>
Cr-Commit-Position: refs/heads/master@{#557312}
[add] https://crrev.com/4504a474c069d07104237d0c03bfce7b29a42de6/third_party/WebKit/LayoutTests/http/tests/media/media-load-nonmedia-crossorigin.html
[modify] https://crrev.com/4504a474c069d07104237d0c03bfce7b29a42de6/third_party/blink/renderer/core/html/media/html_media_element.cc
[modify] https://crrev.com/4504a474c069d07104237d0c03bfce7b29a42de6/third_party/blink/renderer/core/html/media/html_media_element.h


### es...@chromium.org (2018-05-18)

Does the above commit fix the bug, or is there more work to do?

### hu...@chromium.org (2018-05-18)

It should be fixed.


### sh...@chromium.org (2018-05-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-04)

Nice one acargunes@! The Chrome VRP panel decided to award $500 for this report. A member of our finance team will be in touch to arrange payment. Also, how would you like to to credited in our release notes?

### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### ac...@gmail.com (2018-06-04)

Thanks! Can you please use the following:
"Gunes Acar and Danny Y. Huang of Princeton University, Frank Li of UC Berkeley"

### sh...@chromium.org (2018-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-06-08)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/828265?no_tracker_redirect=1

[Multiple monorail components: Blink>Media, Blink>SecurityFeature>SameOriginPolicy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090985)*
