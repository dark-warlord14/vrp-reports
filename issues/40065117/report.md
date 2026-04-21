# Security: Document PiP URL spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40065117](https://issues.chromium.org/issues/40065117) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2023-05-31 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

In some Chrome configurations\*, a Document PiP window title displays the URL instead of the origin, which can be spoofed due to the fact that the URL is not elided correctly.

**VERSION**  

Chrome Version: 113.0.5672.127 + stable  

Operating System: Windows 11

**REPRODUCTION CASE**

1. Open poc.html
2. Click the button

\* I was only able to reproduce this with certain user data profiles, which makes me think that this is caused by a finch feature or similar. I have attached the active variations below, I hope that this will help in figuring out which configuration is causing this to happen.

The bug allows spoofing the apparent origin of a PiP window opened by a website.

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 659 B)
- [poc.png](attachments/poc.png) (image/png, 59.4 KB)
- [version.txt](attachments/version.txt) (text/plain, 50.1 KB)

## Timeline

### st...@gmail.com (2023-05-31)

Also reproduced in 114.0.5735.91

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-06-01)

Thanks for the interesting report! It took me a little bit but I was able to figure out why this only reproduced for you in some profiles but not others -- it requires that you have the "Always Show Full URLs" setting enabled in the Omnibox (along with having the DocumentPictureInPictureAPI feature enabled). This appears to be interacting badly with how the PIP window URL display is being handled, allowing a pretty convincing spoof.

I'm tentatively setting this as Severity-Medium as it doesn't allow complete control over the origin in the PIP window, but it is pretty borderline.

steimel@ could you take a look? I'm not sure where the PIP window URL is being formatted in code, but if you point me to the location I'm happy to advise on possible fixes (as a UrlFormatter owner).





[Monorail components: Blink>Media>PictureInPicture]

### ct...@chromium.org (2023-06-01)

Just realized I wasn't completely clear in https://crbug.com/chromium/1450376#c3: per our severity guidelines [1] this seems to be a Severity-Medium, but it is borderline Severity-High ("complete control over the apparent origin in the Omnibox")

[1]: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md

### [Deleted User] (2023-06-01)

[Empty comment from Monorail migration]

### st...@chromium.org (2023-06-01)

The PiP window's URL is set using LocationBarModel::GetURLForDisplay(). We depend on the fact that we return true for ShouldTrimDisplayUrlAfterHostName(), but looks like eventually ShouldPreventElision() can circumvent that:

https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/omnibox/browser/location_bar_model_impl.cc;l=89;drc=66941d1f0cfe9155b400aef887fe39a403c1f518

So I think we just need to override ShouldPreventElision() to always return false in PictureInPictureBrowserFrameView

### st...@chromium.org (2023-06-01)

adding sky@ to cc as they are the reviewer on the CL for the fix

### st...@chromium.org (2023-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-06-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dc77f9839826a27e2f0bb5210f50920a890412e7

commit dc77f9839826a27e2f0bb5210f50920a890412e7
Author: Tommy Steimel <steimel@chromium.org>
Date: Fri Jun 02 18:00:17 2023

pip2: Always elide the URL in the titlebar

This CL ensures that the URL in a document picture-in-picture window is
always elided, even when the user has selected "Always Show Full URLs"
in the omnibox.

Bug: 1450376
Change-Id: I6275e0ff9d3a9a860e5e4086732d717c47bdc3fc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4581312
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1152637}

[modify] https://crrev.com/dc77f9839826a27e2f0bb5210f50920a890412e7/chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.cc
[modify] https://crrev.com/dc77f9839826a27e2f0bb5210f50920a890412e7/chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.h


### st...@chromium.org (2023-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-03)

[Empty comment from Monorail migration]

### st...@gmail.com (2023-06-03)

This was quick! Verified that this no longer reproduces in 116.0.5811.0.

### [Deleted User] (2023-06-03)

Requesting merge to beta M115 because latest trunk commit (1152637) appears to be after beta branch point (1148114).

Merge review required: M115 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-04)

Requesting merge to beta M115 because latest trunk commit (1152637) appears to be after beta branch point (1148114).

Merge review required: M115 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-05)

Requesting merge to beta M115 because latest trunk commit (1152637) appears to be after beta branch point (1148114).

Merge review required: M115 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@chromium.org (2023-06-05)

1. Which CLs should be backmerged? (Please include Gerrit links.)
crrev.com/c/4581312

2. Has this fix been tested on Canary?
Yes

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
No stability issues

4. Does this fix pose any known compatibility risks?
No known compatibility risks

5. Does it require manual verification by the test team? If so, please describe required testing.
No

### am...@chromium.org (2023-06-06)

m115 merge approved, please merge this fix to branch 5790 so this fix by EOD tomorrow / Tuesday 6 June so this fix can be included in the next M115 beta update -- ty

### gi...@appspot.gserviceaccount.com (2023-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/072893c8a5739f777ac98a173e2a31753704b50e

commit 072893c8a5739f777ac98a173e2a31753704b50e
Author: Tommy Steimel <steimel@chromium.org>
Date: Tue Jun 06 15:46:16 2023

pip2: Always elide the URL in the titlebar

This CL ensures that the URL in a document picture-in-picture window is
always elided, even when the user has selected "Always Show Full URLs"
in the omnibox.

(cherry picked from commit dc77f9839826a27e2f0bb5210f50920a890412e7)

Bug: 1450376
Change-Id: I6275e0ff9d3a9a860e5e4086732d717c47bdc3fc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4581312
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1152637}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4590806
Auto-Submit: Tommy Steimel <steimel@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/branch-heads/5790@{#407}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/072893c8a5739f777ac98a173e2a31753704b50e/chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.cc
[modify] https://crrev.com/072893c8a5739f777ac98a173e2a31753704b50e/chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.h


### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations, Thomas! The VRP Panel has decided to award you $5,000 for this report. Thank you for this solid report! The reward amount decided on for this security UI spoof (high quality with functional exploit) was that this doesn't allow for a complete attacker control and a fully arbitrary URL spoof in the PIP window. A very clever bug nonetheless! Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-20)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@chromium.org (2023-06-21)

1. Was this issue a regression for the milestone it was found in?
No, this issue was not a regression

2. Is this issue related to a change or feature merged after the latest LTS Milestone?
The feature is in an OT from M111-M115, and launching fully in M116

### rz...@google.com (2023-06-23)

[Empty comment from Monorail migration]

### rz...@google.com (2023-06-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-06-27)

1. https://crrev.com/c/4638224
2. Low, no conflicts
3. 115
4. Yes

### gm...@google.com (2023-06-28)

[Empty comment from Monorail migration]

### gm...@google.com (2023-07-13)

Based on https://crbug.com/chromium/1450376#c25. We don't need this on LTS-108, but we will need it in LTC-114 (after taking over the branch at the end of July). 
@rzanoni, please move your merge request to 114. I will delay approval until we are ready to merge on the 114 branch.

### am...@chromium.org (2023-07-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-08-29)

1. https://crrev.com/c/4821507
2. Low, no conflicts
3. 115
4. Yes

### gm...@google.com (2023-09-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4acb7d117f70b27d5fb08f3e34f3258c8350d717

commit 4acb7d117f70b27d5fb08f3e34f3258c8350d717
Author: Tommy Steimel <steimel@chromium.org>
Date: Thu Sep 07 18:45:16 2023

[M114-LTS] pip2: Always elide the URL in the titlebar

This CL ensures that the URL in a document picture-in-picture window is
always elided, even when the user has selected "Always Show Full URLs"
in the omnibox.

(cherry picked from commit dc77f9839826a27e2f0bb5210f50920a890412e7)

Bug: 1450376
Change-Id: I6275e0ff9d3a9a860e5e4086732d717c47bdc3fc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4581312
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1152637}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4821507
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1590}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/4acb7d117f70b27d5fb08f3e34f3258c8350d717/chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.cc
[modify] https://crrev.com/4acb7d117f70b27d5fb08f3e34f3258c8350d717/chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.h


### rz...@google.com (2023-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1450376?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065117)*
