# Stealing cross-origin video pixel with HLS

| Field | Value |
|-------|-------|
| **Issue ID** | [40091946](https://issues.chromium.org/issues/40091946) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media>Video |
| **Platforms** | iOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | da...@chromium.org |
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
Even though the video is loaded from https://test.shhnjk.com/hls/testa.m3u8, actual video data is requested from served from https://vuln.shhnjk.com/video.m3u8 which is cross-origin. But Chrome leaks video's pixels to the page. This might be because same-origin check is happening with video URL.

Did this work before? N/A 

Chrome version: 67.0.3396.87  Channel: stable
OS Version: 11.4.1
Flash Version: 

This is a bug of WKWebView

## Timeline

### do...@chromium.org (2018-07-17)

+danyao, can you follow up on this please? Thanks! Assigning medium severity as this is a cross-origin data leak.

[Monorail components: Internals>Media>Video]

### do...@chromium.org (2018-07-17)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-07-17)

This bug needs a fix from WebKit, where as https://crbug.com/chromium/864283 needs fix from Blink. This is why I submitted 2 separate bugs.

### sh...@chromium.org (2018-07-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-17)

[Empty comment from Monorail migration]

### da...@chromium.org (2018-07-17)

Filed WebKit bug: https://bugs.webkit.org/show_bug.cgi?id=187731
and Radar: <rdar://problem/42290703>

### s....@gmail.com (2018-07-17)

Could you reopen https://crbug.com/chromium/864283 for the bug in Chrome for Android?

### da...@chromium.org (2018-07-17)

dominickn@: can you reopen https://crbug.com/chromium/864283 for the bug in Chrome for Android per https://crbug.com/chromium/864286#c7? I don't have permission to view that bug.

### do...@chromium.org (2018-07-17)

#8: done. I didn't see the different OS tag when I merged the two, sorry OP.

### do...@chromium.org (2018-07-17)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-07-26)

Hi, is it possible to CC me on webkit the bug? I would like to see the progress and the patch. Thanks!

### da...@chromium.org (2018-07-27)

Done.

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-10-12)

Hi, this bug is now fixed in The WebKit. Can we mark this bug as fixed?

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-01)

This bug requires manual review: Less than 29 days to go before AppStore submit on M71
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2018-11-01)

Danyao, does this need merge? If not, feel free to remove the labels.

### aw...@chromium.org (2018-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-02)

$4,000 for this report - thanks as ever!

### aw...@google.com (2018-11-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2018-11-06)

Re https://crbug.com/chromium/864286#c21: This bug doesn't need merge because the bug is fixed in WebKit land.

### sh...@chromium.org (2019-01-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ph...@igalia.com (2019-05-08)

I can reproduce this issue in Chrome Version 73.0.3683.103 (Official Build) (64-bit) on Linux. Although the video fails to load, the exploit is triggered. Is this... expected?

### da...@google.com (2019-05-09)

It's just the black frame we present when the video fails to load.

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/864286?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/864283]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091946)*
